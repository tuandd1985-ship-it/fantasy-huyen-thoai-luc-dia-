"""Matte-clean + QC for map props generated on light grey, then composite on the grass tile.
Usage: python process_map_props.py <rung_xanh_map dir> <hero_png_for_scale>
"""
import sys, json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage as ndi
sys.path.insert(0, str(Path(__file__).parent))
import gac_matte as g

PICK = {"cay_soi": 728102, "tang_da_reu": 728102, "cot_da_co": 728101,
        "bui_cay": 728104, "khom_hoa": 728101, "da_cong_dich_chuyen": 728105}
HALO_DIST = 28.0      # edge pixel this close to the grey background colour = grey halo
HALO_MAX_PCT = 3.0


def matte_from_rgb(rgb_u8, bir):
    rgb = rgb_u8.astype(float)
    bd = np.concatenate([rgb[:8].reshape(-1, 3), rgb[-8:].reshape(-1, 3), rgb[:, :8].reshape(-1, 3), rgb[:, -8:].reshape(-1, 3)])
    B = np.median(bd, 0)
    a = np.clip(bir, 0, 1); a[a < 0.04] = 0
    # plan section 4 step 4: colour unmixing with the known background, F = (I - (1-a) B) / a
    F = (rgb - (1 - a)[..., None] * B) / np.maximum(a, 1e-3)[..., None]
    F = np.clip(F, 0, 255)
    low = (a > 0) & (a < 0.25)  # unmixing is unstable at very low alpha: use nearby solid colour instead
    ref = a > 0.95
    refc, ok = g.local_ref_color(rgb, ref)
    F[low & ok] = refc[low & ok]
    out = np.where((a > 0)[..., None], F, rgb)
    return np.dstack([out, a * 255]).round().astype(np.uint8), B


def halo_pct(rgba, B):
    a = rgba.astype(float); A = a[..., 3]
    _, band, _ = g.regions(A)
    sel = band & (A > 64)
    d = np.sqrt(((a[..., :3] - B) ** 2).sum(-1))
    return round(100 * float((d[sel] < HALO_DIST).mean()), 3) if sel.any() else 0.0


def crop(rgba, pad=12):
    A = rgba[..., 3]; ys, xs = np.nonzero(A > 8)
    y0, y1, x0, x1 = max(0, ys.min() - pad), min(A.shape[0], ys.max() + pad + 1), max(0, xs.min() - pad), min(A.shape[1], xs.max() + pad + 1)
    return rgba[y0:y1, x0:x1]


def on(im, bg):
    b = Image.new("RGBA", im.size, bg + (255,)); b.alpha_composite(im); return b.convert("RGB")


def main():
    d = Path(sys.argv[1]); hero = Image.open(sys.argv[2]).convert("RGBA")
    (d / "props_clean").mkdir(exist_ok=True)
    rep = {"items": [], "thresholds": dict(g.THRESH, grey_halo_pct_max=HALO_MAX_PCT)}
    cleaned = {}
    for k, s in PICK.items():
        raw = np.asarray(Image.open(d / "props_raw" / f"{k}_s{s}.png").convert("RGB"))
        bir = g.birefnet_mask(np.dstack([raw, np.full(raw.shape[:2], 255, np.uint8)]))
        rgba, B = matte_from_rgb(raw, bir)
        before = g.qc(rgba, None, bir)
        C, info = g.clean(rgba, bir)
        q = g.qc(C, None, bir); q["grey_halo_pct"] = halo_pct(C, B); before["grey_halo_pct"] = halo_pct(rgba, B)
        j = g.judge(q); j["grey_halo"] = q["grey_halo_pct"] < HALO_MAX_PCT
        lab, n = ndi.label(C[..., 3] > 128)
        Cc = crop(C); Image.fromarray(Cc).save(d / "props_clean" / f"{k}.png", optimize=True)
        cleaned[k] = Image.fromarray(Cc)
        rep["items"].append({"prop": k, "seed": s, "bg_estimate": B.round(1).tolist(), "clean_info": info,
                             "qc_before_clean": before, "qc": q, "pass": j, "all_pass": all(j.values()),
                             "opaque_components": int(n), "size_cropped": list(Cc.shape[1::-1])})
        print(k, "PASS" if all(j.values()) else [x for x, v in j.items() if not v], "halo", before["grey_halo_pct"], "->", q["grey_halo_pct"], flush=True)
    (d / "qc.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False, default=lambda o: o.item() if hasattr(o, "item") else str(o)), encoding="utf-8")

    # contact: each prop on black / white / grass
    tile = Image.open(d / "tile_co_rung_xanh_1024.png").convert("RGB")
    rows = []
    for k, im in cleaned.items():
        s = 300 / max(im.size); im2 = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        cells = [on(im2, (0, 0, 0)), on(im2, (255, 255, 255))]
        gb = tile.resize((512, 512)).crop((0, 0, im2.width, im2.height)).convert("RGBA"); gb.alpha_composite(im2); cells.append(gb.convert("RGB"))
        rows.append(cells)
    W = 3 * 310 + 10; H = sum(max(c.height for c in r) + 10 for r in rows) + 10
    S = Image.new("RGB", (W, H), (245, 245, 245)); y = 10
    for r in rows:
        x = 10
        for c_ in r: S.paste(c_, (x, y)); x += 310
        y += max(c_.height for c_ in r) + 10
    S.save(d / "props_on_backgrounds.jpg", quality=95, subsampling=0)

    # scene composite 1280x720 at game scale (hero about 150 px tall, as in v0.3.7)
    cell = tile.resize((384, 384), Image.LANCZOS)
    scene = Image.new("RGBA", (1280, 720))
    for x in range(0, 1280, 384):
        for y in range(0, 720, 384): scene.paste(cell, (x, y))
    heights = {"cay_soi": 300, "cot_da_co": 220, "da_cong_dich_chuyen": 200, "tang_da_reu": 110, "bui_cay": 95, "khom_hoa": 60}
    place = [("cay_soi", 170, 330), ("cot_da_co", 1080, 300), ("da_cong_dich_chuyen", 640, 260), ("tang_da_reu", 420, 600),
             ("bui_cay", 880, 620), ("khom_hoa", 300, 690), ("bui_cay", 1180, 520), ("khom_hoa", 760, 690), ("cay_soi", 1000, 690)]
    items = [(k, x, y) for k, x, y in place] + [("__hero", 560, 560)]
    for k, x, yb in sorted(items, key=lambda t: t[2]):  # painter's order by foot y (2.5D depth)
        im = hero if k == "__hero" else cleaned[k]
        h = 150 if k == "__hero" else heights[k]
        s = h / im.height; im2 = im.resize((max(1, int(im.width * s)), h), Image.LANCZOS)
        sh = Image.new("RGBA", scene.size); ImageDraw.Draw(sh).ellipse([x - im2.width * 0.35, yb - 10, x + im2.width * 0.35, yb + 8], fill=(0, 0, 0, 90))
        scene.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)))
        scene.alpha_composite(im2, (int(x - im2.width / 2), int(yb - im2.height)))
    scene.convert("RGB").save(d / "scene_test_1280x720.jpg", quality=95, subsampling=0)


if __name__ == "__main__":
    main()
