"""Step A: sprite-matte-clean + art-qc on the 6 game heroes (k2-k7).
Usage: python run_hero_matte_clean.py <dir with k2..k7.webp> <out_dir> <grass_screenshot.jpg>
"""
import sys, json, hashlib, time
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).parent))
import gac_matte as g

NAMES = {"k2": "swordsman-male", "k3": "swordsman-female", "k4": "mage-male",
         "k5": "mage-female", "k6": "archer-male", "k7": "archer-female"}


def backgrounds(size, grass_src):
    w, h = size
    yy, xx = np.indices((h, w)); chk = ((yy // 16 + xx // 16) % 2)[..., None]
    checker = Image.fromarray(np.where(chk == 1, 204, 245).repeat(3, -1).astype(np.uint8))
    tile = Image.open(grass_src).convert("RGB")
    grass = Image.new("RGB", (w, h))
    for y in range(0, h, tile.height):
        for x in range(0, w, tile.width): grass.paste(tile, (x, y))
    return {"den": Image.new("RGB", (w, h), (0, 0, 0)), "trang": Image.new("RGB", (w, h), (255, 255, 255)),
            "co_map": grass, "trong_suot": checker}


def comp(im, bg):
    b = bg.convert("RGBA"); b.alpha_composite(im); return b.convert("RGB")


def sheet(orig, clean, grass_src, path, title):
    th = 420; s = th / orig.height; W0 = int(orig.width * s)
    o, c = orig.resize((W0, th), Image.LANCZOS), clean.resize((W0, th), Image.LANCZOS)
    bgs = backgrounds((W0, th), grass_src)
    # zoom strip: 4x crop of a silhouette edge (left side, upper third)
    A = np.asarray(orig)[..., 3]; ys, xs = np.nonzero(A > 0)
    cy = int(np.percentile(ys, 35)); row = np.nonzero(A[cy] > 0)[0]; cx = int(row.min()) if len(row) else orig.width // 2
    box = (max(0, cx - 40), max(0, cy - 40), max(0, cx - 40) + 80, max(0, cy - 40) + 80)
    W = 8 + 4 * 2 * (W0 + 6) + 8; H = 30 + 22 + th + 20 + 22 + 240 + 10
    S = Image.new("RGB", (W, H), (250, 250, 250)); d = ImageDraw.Draw(S)
    d.text((8, 8), title, fill=(0, 0, 0))
    x = 8
    for name, bg in bgs.items():
        for lab, im in (("TRUOC", o), ("SAU", c)):
            d.text((x, 34), f"{lab} / nen {name}", fill=(0, 0, 0)); S.paste(comp(im, bg), (x, 52)); x += W0 + 6
        x += 4
    y = 52 + th + 24; x = 8
    zb = backgrounds((240, 240), grass_src)
    for name in ("den", "trang", "co_map", "trong_suot"):
        for lab, im in (("TRUOC", orig), ("SAU", clean)):
            z = im.crop(box).resize((240, 240), Image.NEAREST)
            S.paste(comp(z, zb[name]), (x, y)); d.text((x + 4, y + 4), f"{lab} x3", fill=(255, 0, 255) if name == "trang" else (255, 255, 0)); x += 246
    S.save(path, quality=95, subsampling=0)  # 4:4:4 so JPEG does not add its own colour fringe


def main():
    src, out, grass = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
    for sub in ("original", "cleaned", "sheets"): (out / sub).mkdir(parents=True, exist_ok=True)
    rep = {"tool": "GAME-ART-CORE sprite-matte-clean + art-qc (CPU)", "thresholds": g.THRESH,
           "params": {k: getattr(g, k) for k in ("EDGE_BAND_PX", "CORE_ALPHA", "SPECK_ALPHA", "SPECK_AREA", "REF_RADIUS", "SPILL_MARGIN", "HOLE_MIN_PX", "BIR_FG")},
           "birefnet": {"model": str(g.COMFY_ROOT / "models/rembg/birefnet-general.onnx"), "provider": "CPUExecutionProvider", "role": "fill enclosed holes only where BiRefNet says foreground; QC hole check"},
           "items": []}
    t0 = time.time()
    for k, name in NAMES.items():
        raw = (src / f"{k}.webp").read_bytes()
        (out / "original" / f"hero-{name}.webp").write_bytes(raw)
        O = np.asarray(Image.open(src / f"{k}.webp").convert("RGBA"))
        t = time.time(); bir = g.birefnet_mask(O); tb = time.time() - t
        C, info = g.clean(O, bir)
        Image.fromarray(C).save(out / "cleaned" / f"hero-{name}.png", optimize=True)
        wq = out / "cleaned" / f"hero-{name}.webp"
        Image.fromarray(C).save(wq, quality=90, alpha_quality=100, method=6, exact=True)
        Cd = np.asarray(Image.open(wq).convert("RGBA"))  # QC the file the game would actually load
        before = g.qc(O, O, bir); after = g.qc(Cd, O, bir)
        wl = out / "cleaned" / f"hero-{name}_lossless.webp"
        Image.fromarray(C).save(wl, lossless=True, quality=100, method=6, exact=True)
        after_ll = g.qc(np.asarray(Image.open(wl).convert("RGBA")), O, bir)  # lossless: interior must be untouched
        after["lossless_png_interior_rgb_changed_px"] = after_ll["interior_rgb_changed_px"]
        jb, ja = g.judge(before), g.judge(after)
        bir_iou = float(((bir >= 0.5) & (O[..., 3] > 128)).sum() / max(1, ((bir >= 0.5) | (O[..., 3] > 128)).sum()))
        rep["items"].append({"key": k, "name": name, "original_sha256": hashlib.sha256(raw).hexdigest(),
                             "cleaned_webp_sha256": hashlib.sha256(wq.read_bytes()).hexdigest(),
                             "bytes": {"original": len(raw), "cleaned_webp": wq.stat().st_size},
                             "birefnet_seconds": round(tb, 1), "birefnet_vs_alpha_iou": round(bir_iou, 4),
                             "clean_info": info, "before": before,
                             "after_webp_q90": after, "after_webp_lossless": after_ll,
                             "pass_before": jb, "pass_after_webp_q90": ja, "pass_after_webp_lossless": g.judge(after_ll),
                             "all_pass_webp_q90": all(ja.values()), "all_pass_webp_lossless": all(g.judge(after_ll).values())})
        rep["items"][-1]["bytes"]["cleaned_webp_lossless"] = wl.stat().st_size
        sheet(Image.fromarray(O), Image.open(wl).convert("RGBA"), grass, out / "sheets" / f"hero-{name}_truoc_sau.jpg",
              f"hero-{name} ({k})  TRUOC = ban dang dung trong game v0.3.7 | SAU = sprite-matte-clean (WebP lossless, ban de xuat)")
        print(k, name, "q90", [x for x, v in ja.items() if not v] or "PASS", "lossless", [x for x, v in g.judge(after_ll).items() if not v] or "PASS")
    rep["total_seconds"] = round(time.time() - t0, 1)
    (out / "qc.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False, default=lambda o: o.item() if hasattr(o, "item") else str(o)), encoding="utf-8")


if __name__ == "__main__":
    main()
