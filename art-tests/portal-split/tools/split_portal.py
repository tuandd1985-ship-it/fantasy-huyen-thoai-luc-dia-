"""Official portal split (ENGINE_PROP_LAYER_SPEC, approved 28caab2): platform (ground) + arch (sorted), shared anchor,
cut along the real platform rim (ellipse fitted on the columns where arch and platform are separated by a gap),
plus the per-prop footprint table in the spec schema.
Usage: python split_portal.py <props_clean_dir> <out_dir> <tile_png> <hero_png>
"""
import sys, json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy.optimize import least_squares

DISPLAY_H = {"cay_soi": 275, "cot_da_co": 215, "tang_da_reu": 115, "bui_cay": 95, "khom_hoa": 60, "da_cong_dich_chuyen": 218}
FOOTPRINT = {"cay_soi": (84, 26), "tang_da_reu": (100, 32), "cot_da_co": (76, 28)}   # spec section 3; stone 150x42 > sprite width 138, set to its measured base (99 px)
GROUND_DECAL = {"khom_hoa"}            # ground decal, no collider (approved)
NO_COLLIDE = {"bui_cay"}               # decorative bush, no collider (approved)
RIM_MARGIN = 3                         # src px above the fitted rim kept with the platform (its dark outline)
ALPHA_ON = 128
OUTSIDE_RIM_Y = 540


def rim_samples(A):
    """Columns where a transparent gap separates arch (above) from platform (below): first opaque row after the gap."""
    xs, ys = [], []
    for x in range(A.shape[1]):
        col = A[420:620, x] > ALPHA_ON
        idx = np.nonzero(col)[0]
        if len(idx) < 2: continue
        gaps = np.nonzero(np.diff(idx) > 6)[0]
        if len(gaps): xs.append(x); ys.append(420 + idx[gaps[0] + 1])
    return np.array(xs, float), np.array(ys, float)


def fit_rim(xs, ys, A):
    opaque = np.nonzero(A.max(0) > ALPHA_ON)[0]
    def f(p, x):
        cx, cy, a, b = p
        return cy - b * np.sqrt(np.clip(1 - ((x - cx) / a) ** 2, 0, 1))
    p0 = [(opaque.min() + opaque.max()) / 2, 690, (opaque.max() - opaque.min()) / 2, 210]
    r = least_squares(lambda p: f(p, xs) - ys, p0, loss="soft_l1", f_scale=3)
    res = f(r.x, xs) - ys
    return r.x, f, float(np.abs(res).mean()), float(np.abs(res).max())


def foot_anchor(A, s):
    """Bottom-centre of the opaque base, in display px: x = middle of the base extent (bottom 15 % rows),
    y = 5 px above the lowest opaque row. Also returns the measured base width in display px."""
    ys = np.nonzero(A.max(1) > ALPHA_ON)[0]; yb = ys.max(); yt = ys.min()
    band = A[yb - int(0.15 * (yb - yt)):yb + 1] > ALPHA_ON
    xs = np.nonzero(band.any(0))[0]
    return round((xs.min() + xs.max()) / 2 * s, 1), round(yb * s - 5, 1), round((xs.max() - xs.min()) * s, 1)


def part(id_, group, image, w, h, ax, ay, layer, collision, interaction, sortY=0):
    return {"id": id_, "groupId": group, "image": image, "displayWidth": w, "displayHeight": h,
            "anchorX": ax, "anchorY": ay, "sortY": sortY, "layer": layer,
            "collision": collision, "interaction": interaction, "shadow": {"type": "baked"}}


if __name__ == "__main__":
    src, out, tile_p, hero_p = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4])
    out.mkdir(parents=True, exist_ok=True)
    P = np.asarray(Image.open(src / "da_cong_dich_chuyen.png").convert("RGBA")); A = P[..., 3]
    H, W = A.shape
    xs, ys = rim_samples(A)
    (cx, cy, a, b), f, err_mean, err_max = fit_rim(xs, ys, A)
    rim = f((cx, cy, a, b), np.arange(W)) - RIM_MARGIN
    outside = (np.arange(W) < cx - a) | (np.arange(W) > cx + a)
    rim[outside] = OUTSIDE_RIM_Y       # beyond the rim ellipse: arch shadow strip ends ~490, platform side starts ~600
    rim = np.minimum(rim, OUTSIDE_RIM_Y)  # near the ellipse ends the curve dips to the platform side wall; arch never reaches 540
    yy = np.arange(H)[:, None]
    plat_mask = yy >= rim[None, :]
    arch = P.copy(); arch[plat_mask, 3] = 0
    plat = P.copy(); plat[~plat_mask, 3] = 0
    # exact re-composite check (disjoint pixel sets)
    recomb = np.where(plat_mask[..., None], plat, arch)
    assert np.array_equal(recomb, P)

    # shared anchor: x = centre between the two outer pillars, y = their feet line (last dark outline row of the
    # pillar base; below it is only the baked grey ground strip)
    s = DISPLAY_H["da_cong_dich_chuyen"] / H
    r400 = np.nonzero(arch[400, :, 3] > ALPHA_ON)[0]
    cut_ = np.nonzero(np.diff(r400) > 3)[0]
    pillars = [(int(r400[0]), int(r400[cut_[0]])), (int(r400[cut_[-1] + 1]), int(r400[-1]))]
    lows = []
    for x0, x1 in pillars:
        for x in range(x0 + 5, x1 - 5):
            col = arch[440:500, x].astype(int)
            dark = np.nonzero((col[:, 3] > ALPHA_ON) & (col[:, :3].mean(1) < 100))[0]
            if len(dark): lows.append(440 + int(dark.max()))
    feet_y = int(np.median(lows))
    anc = ((pillars[0][0] + pillars[0][1] + pillars[1][0] + pillars[1][1]) / 4, float(feet_y))

    def crop(rgba):
        ys_, xs_ = np.nonzero(rgba[..., 3] > 0)
        y0, y1, x0, x1 = ys_.min(), ys_.max() + 1, xs_.min(), xs_.max() + 1
        return rgba[y0:y1, x0:x1], (int(x0), int(y0))
    arch_c, ao = crop(arch); plat_c, po = crop(plat)
    Image.fromarray(arch_c).save(out / "portal_back.png", optimize=True)
    Image.fromarray(plat_c).save(out / "portal_platform.png", optimize=True)

    # collision: one ellipse per outer pillar base, width = base width on the feet line, height = 0.75 * width
    feet = []
    for x0, x1 in pillars:
        row = np.nonzero(arch[feet_y - 6, x0 - 30:x1 + 30, 3] > ALPHA_ON)[0] + x0 - 30
        bx0, bx1 = row.min(), row.max()
        w_ = (bx1 - bx0) * s
        feet.append({"type": "ellipse", "offsetX": round(((bx0 + bx1) / 2 - anc[0]) * s, 1), "offsetY": 0.0,
                     "width": round(w_, 1), "height": round(w_ * 0.75, 1)})
    trig = {"type": "ellipse", "offsetX": round((cx - anc[0]) * s, 1), "offsetY": round((cy - anc[1]) * s, 1),
            "width": round(2 * a * 0.7 * s, 1), "height": round(2 * b * 0.7 * s, 1)}   # inner 70 % of the top surface

    parts = [
        part("forest-portal-01-platform", "forest-portal-01", "portal_platform.png",
             round(plat_c.shape[1] * s, 1), round(plat_c.shape[0] * s, 1),
             round((anc[0] - po[0]) * s, 1), round((anc[1] - po[1]) * s, 1), "ground", [{"type": "none"}], trig),
        part("forest-portal-01-arch", "forest-portal-01", "portal_back.png",
             round(arch_c.shape[1] * s, 1), round(arch_c.shape[0] * s, 1),
             round((anc[0] - ao[0]) * s, 1), round((anc[1] - ao[1]) * s, 1), "sorted", feet, {"type": "none"}),
    ]
    # other props: one sorted (or ground) part each, anchored at the base bottom-centre
    for k, dh in DISPLAY_H.items():
        if k == "da_cong_dich_chuyen": continue
        im = np.asarray(Image.open(src / f"{k}.png").convert("RGBA")); sk = dh / im.shape[0]
        ax, ay, base_w = foot_anchor(im[..., 3], sk)
        if k in FOOTPRINT:
            w_, h_ = FOOTPRINT[k]; col = [{"type": "ellipse", "offsetX": 0.0, "offsetY": 0.0, "width": w_, "height": h_}]
        else:
            col = [{"type": "none"}]
        parts.append(part(f"forest-{k}-01", f"forest-{k}-01", f"../rung-xanh-map-sample/props_clean/{k}.png",
                          round(im.shape[1] * sk, 1), dh, ax, ay, "ground" if k in GROUND_DECAL else "sorted", col, {"type": "none"}))
        parts[-1]["_measured_base_width"] = base_w   # info only: base extent at display size, to check the footprint
    meta = {"spec": "docs/art/ENGINE_PROP_LAYER_SPEC.md @ 28caab2", "units": "world px at 1x display; anchors from the top-left of the scaled image",
            "portal_registration": {"source_png": "rung-xanh-map-sample/props_clean/da_cong_dich_chuyen.png", "source_size": [W, H],
                                    "display_scale": round(s, 6), "shared_anchor_source_px": [round(anc[0], 1), anc[1]],
                                    "platform_crop_origin_source_px": list(po), "arch_crop_origin_source_px": list(ao),
                                    "rim_ellipse_source_px": {"cx": round(cx, 1), "cy": round(cy, 1), "a": round(a, 1), "b": round(b, 1)},
                                    "rim_fit_columns": int(len(xs)), "rim_fit_err_px": {"mean": round(err_mean, 2), "max": round(err_max, 2)},
                                    "rim_margin_px": RIM_MARGIN, "recomposite_identical": True},
            "parts": parts}
    (out / "props_layer.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")

    # previews: cut line on the source; parts tinted; layered scene
    v = Image.fromarray(P).convert("RGBA"); bg = Image.new("RGBA", v.size, (40, 40, 40, 255)); bg.alpha_composite(v)
    d = ImageDraw.Draw(bg)
    d.line([(x, float(rim[x])) for x in range(W)], fill=(255, 60, 60, 255), width=3)
    d.ellipse([anc[0] - 8, anc[1] - 8, anc[0] + 8, anc[1] + 8], outline=(255, 230, 0, 255), width=3)
    tint = Image.new("RGBA", v.size, (40, 40, 40, 255))
    ta = arch.copy(); ta[..., :3] = (ta[..., :3] * 0.5 + np.array([255, 120, 0]) * 0.5).astype(np.uint8)
    tp = plat.copy(); tp[..., :3] = (tp[..., :3] * 0.5 + np.array([0, 140, 255]) * 0.5).astype(np.uint8)
    tint.alpha_composite(Image.fromarray(tp)); tint.alpha_composite(Image.fromarray(ta))
    sheet = Image.new("RGB", (W * 2 + 30, H + 20), (20, 20, 20)); sheet.paste(bg.convert("RGB"), (10, 10)); sheet.paste(tint.convert("RGB"), (W + 20, 10))
    sheet.save(out / "portal_split_check.jpg", quality=92, subsampling=0)

    # layered scene: ground pass -> sorted pass by y (+sortY); hero behind arch, hero on platform
    tile = Image.open(tile_p).convert("RGBA").resize((384, 384), Image.LANCZOS)
    hero = Image.open(hero_p).convert("RGBA"); hero = hero.crop(hero.getbbox())
    hero = hero.resize((round(hero.width * 150 / hero.height), 150), Image.LANCZOS)
    def scene(hero_y):
        sc = Image.new("RGBA", (640, 420))
        for x in range(0, 640, 384):
            for y in range(0, 420, 384): sc.paste(tile, (x, y))
        X, Y = 320, 170
        def put(img_path, pt, x, y):
            im = Image.open(out / img_path).convert("RGBA").resize((round(pt["displayWidth"]), round(pt["displayHeight"])), Image.LANCZOS)
            sc.alpha_composite(im, (round(x - pt["anchorX"]), round(y - pt["anchorY"])))
        put("portal_platform.png", parts[0], X, Y)
        entries = [(Y + parts[1]["sortY"], "arch"), (hero_y, "hero")]
        for _, k in sorted(entries):
            if k == "arch": put("portal_back.png", parts[1], X, Y)
            else: sc.alpha_composite(hero, (round(X - hero.width / 2), round(hero_y - hero.height + 5)))
        return sc.convert("RGB")
    A1, B1 = scene(150), scene(230)
    S = Image.new("RGB", (1300, 440), (20, 20, 20)); S.paste(A1, (10, 10)); S.paste(B1, (660, 10))
    S.save(out / "portal_layer_scene.jpg", quality=92, subsampling=0)
    print(json.dumps(meta["portal_registration"], indent=1)); print(json.dumps(parts[:2], indent=1))
