"""Pháp Sư strip v2 assembly: picked raw generations (white bg) -> BiRefNet -> near-white transparent -> largest
component -> gac_matte.clean -> per-frame lean / breathing -> orb glow -> 420x500 cells (one scale per gender, feet y 487,
no x jitter) -> strip 2520x500 + 2 skill PNGs + QC + contact sheets + GIF.
Usage: python compose_mage_v2.py <raw_dir> <out_dir> <picks.json>
picks.json: {"male": {"idle": "raw_male_idle_s741001_ip60.png", "run": ..., "run2": ..., "cast1": ..., "cast2": ...,
             "skill_charge": ..., "skill_release": ...}, "female": {...}}
"""
import sys, json, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
sys.path.insert(0, str(Path(__file__).parent))
import gac_matte as g
import maps_upscale_grade as mg
import mage_anim_compose as mc

CELL_W, CELL_H, BASE_Y = 420, 500, 487
# frame: (source pose, lean deg (+ = forward/right), breathing sy, bob px, orb glow strength, glow radius x orb)
FRAMES = {
    "idle1": ("idle", 0, 1.0, 0, 0.25, 1.4),
    "idle2": ("idle", 0, 0.982, 0, 0.32, 1.5),
    "run1": ("run", 9, 1.0, 0, 0.25, 1.4),
    "run2": ("run2", 9, 1.0, 10, 0.25, 1.4),
    "cast1": ("cast1", -6, 1.0, 0, 0.35, 1.3),
    "cast2": ("cast2", 8, 1.0, 0, 0.95, 2.6),
    "skill_charge": ("skill_charge", 0, 1.0, 0, 0.9, 2.8),
    "skill_release": ("skill_release", 10, 1.0, 0, 1.0, 3.2),
}
STRIP = ["idle1", "idle2", "run1", "run2", "cast1", "cast2"]
ORB = {"male": ((190, 235), (90, 175, 255)), "female": ((270, 330), (185, 115, 255))}


def matte(raw_png):
    rgb = np.asarray(Image.open(raw_png).convert("RGB"))
    H, W = rgb.shape[:2]
    bir = g.birefnet_mask(np.dstack([rgb, np.full((H, W), 255, np.uint8)]), bg=(255, 255, 255))
    white = (rgb.astype(int).min(-1) > 240) & (np.ptp(rgb.astype(int), -1) < 10)
    a = np.where(white & (bir < 0.9), 0, np.round(bir * 255)).astype(np.uint8)
    lab, n = ndi.label(a > 128)
    if n > 1:
        sz = ndi.sum(np.ones_like(a), lab, range(1, n + 1)); main = lab == (int(np.argmax(sz)) + 1)
        keep = ndi.binary_dilation(main, iterations=2); a = np.where(keep, a, 0).astype(np.uint8)
    rgba, info = g.clean(np.dstack([rgb, a]).astype(np.uint8), bir)
    return Image.fromarray(rgba)


def body_top(A, frac):
    """First row (from the top) whose opaque width reaches frac * max row width: hat brim / hair mass, ignoring
    thin things sticking up (staff tips, hat tip, magic swirls)."""
    w = (A > 128).sum(1); rows = np.nonzero(w >= frac * w.max())[0]
    return int(rows.min()) if len(rows) else int(np.nonzero(w)[0].min())


def cut_above_crown(im):
    """Female: remove magic swirls / floating orbs the model added above the head (keep the rounded crown)."""
    a = np.asarray(im).copy(); A = a[..., 3]
    top = body_top(A, 0.55); ws = (A > 128).sum(1).max()
    cut = max(0, top - int(0.16 * ws))
    a[:cut, :, 3] = 0
    lab, n = ndi.label(a[..., 3] > 128)
    if n > 1:
        sz = ndi.sum(np.ones_like(A), lab, range(1, n + 1)); keep = ndi.binary_dilation(lab == int(np.argmax(sz)) + 1, iterations=2)
        a[~keep, 3] = 0
    return Image.fromarray(a)


def remove_pale_aura(im):
    """Female: drop the pale magic swirls / moon discs the model painted behind the head. Pale = very light, low
    chroma or cream, not skin; only large regions in the upper 55 % of the figure; hair (saturated lavender) is kept."""
    a = np.asarray(im).copy(); A = a[..., 3] > 0
    lab = mg.to_oklab(a[..., :3].astype(np.float32) / 255); L = lab[..., 0]; C = np.hypot(lab[..., 1], lab[..., 2])
    h = np.degrees(np.arctan2(lab[..., 2], lab[..., 1])) % 360
    skin = (h > 30) & (h < 75) & (C > 0.03) & (C < 0.11)
    pale = A & (L > 0.80) & ((C < 0.075) | ((h > 75) & (h < 115))) & ~skin
    ys = np.nonzero(A.any(1))[0]; top, bot = ys.min(), ys.max(); upper = np.zeros_like(A); upper[: int(top + 0.55 * (bot - top))] = True
    pl, n = ndi.label(ndi.binary_closing(pale, iterations=2) & upper)
    if n:
        sz = ndi.sum(np.ones_like(L), pl, range(1, n + 1))
        # only regions on the OUTSIDE of the silhouette (touching transparent background); the face is enclosed by
        # hair and never touches the background, so it is kept
        outside = ndi.binary_dilation(~A, iterations=3)
        touch = ndi.sum(outside & (pl > 0), pl, range(1, n + 1)) / np.maximum(sz, 1)
        edge_len = ndi.sum(ndi.binary_dilation(pl > 0, iterations=1) & outside, pl, range(1, n + 1))
        # never touch the face: pale regions within 25 px of the eyes (saturated purple irises) are protected
        eyes = A & (C > 0.12) & (h > 280) & (h < 335) & (L > 0.30) & (L < 0.62)
        el, en = ndi.label(eyes); esz = ndi.sum(np.ones_like(L), el, range(1, en + 1)) if en else []
        eyes = np.isin(el, 1 + np.nonzero((np.array(esz) > 80) & (np.array(esz) < 20000))[0]) if en else eyes
        near_eye = ndi.sum(ndi.binary_dilation(eyes, iterations=25) & (pl > 0), pl, range(1, n + 1)) > 0
        ok = (sz > 1500) & (edge_len > 60) & ~near_eye
        drop = np.isin(pl, 1 + np.nonzero(ok)[0])
        drop = ndi.binary_dilation(drop, iterations=2) & ~(A & (C > 0.09))
        a[drop, 3] = 0
    lb, m = ndi.label(a[..., 3] > 128)
    if m > 1:
        sz = ndi.sum(np.ones_like(L), lb, range(1, m + 1)); keep = ndi.binary_dilation(lb == int(np.argmax(sz)) + 1, iterations=2)
        a[~keep, 3] = 0
    return Image.fromarray(a)


def find_orb(im, gd):
    a = np.asarray(im); A = a[..., 3] > 200
    L, C, h = None, None, None
    lab = mg.to_oklab(a[..., :3].astype(np.float32) / 255); L = lab[..., 0]; C = np.hypot(lab[..., 1], lab[..., 2])
    h = np.degrees(np.arctan2(lab[..., 2], lab[..., 1])) % 360
    lo, hi = ORB[gd][0]
    m = A & (L > 0.62) & (C > 0.10) & (h > lo) & (h < hi)
    lb, n = ndi.label(ndi.binary_closing(m, iterations=2))
    if not n: return None
    sz = ndi.sum(np.ones_like(L), lb, range(1, n + 1)); i = int(np.argmax(sz)) + 1
    cy, cx = ndi.center_of_mass(lb == i); r = math.sqrt(sz[i - 1] / math.pi)
    return cx, cy, max(r, 12)


def frame_img(src, gd, f):
    _, lean, sy, bob, glow, gr = f
    im = src
    W, H = im.size; pad = 220
    cv = Image.new("RGBA", (W + 2 * pad, H + 2 * pad)); cv.alpha_composite(im, (pad, pad))
    A = np.asarray(cv)[..., 3]; ys, xs = np.nonzero(A > 128); feet = (float(np.median(xs[ys > ys.max() - 30])), float(ys.max()))
    orb = find_orb(cv, gd)
    if sy != 1.0:
        sx = 1 + (1 - sy) * 0.4
        cv = mc.premul_transform(cv, lambda x: x.transform(x.size, Image.AFFINE, (1 / sx, 0, feet[0] - feet[0] / sx, 0, 1 / sy, feet[1] - feet[1] / sy), resample=Image.BICUBIC))
        if orb: orb = (feet[0] + (orb[0] - feet[0]) * sx, feet[1] + (orb[1] - feet[1]) * sy, orb[2])
    if lean:
        cv = mc.rot(cv, lean, feet)
        if orb:
            r = math.radians(lean); dx, dy = orb[0] - feet[0], orb[1] - feet[1]
            orb = (feet[0] + dx * math.cos(r) - dy * math.sin(r), feet[1] + dx * math.sin(r) + dy * math.cos(r), orb[2])
    if bob:
        c2 = Image.new("RGBA", cv.size); c2.alpha_composite(cv, (0, -bob)); cv = c2
        if orb: orb = (orb[0], orb[1] - bob, orb[2])
    char_alpha = np.asarray(cv)[..., 3].copy()
    if orb and glow:
        cv.alpha_composite(mc.glow_layer(cv.size, orb[0], orb[1], orb[2] * gr, ORB[gd][1], 0.55 * glow))
    cv.char_alpha = char_alpha
    return cv, feet, orb


def main():
    raw, out, picks = Path(sys.argv[1]), Path(sys.argv[2]), json.loads(Path(sys.argv[3]).read_text(encoding="utf-8"))
    out.mkdir(parents=True, exist_ok=True); report = {"picks": picks}
    for gd, pk in picks.items():
        cache = {k: out / f"_matte_{gd}_{k}_raw.png" for k in pk}
        mats = {k: (Image.open(cache[k]).convert("RGBA") if cache[k].exists() else matte(raw / v)) for k, v in pk.items()}
        for k, v in mats.items():
            if not cache[k].exists(): v.save(cache[k])
        pass  # female v2f: no halo any more, crown cut not needed
        for k, v in mats.items(): v.save(out / f"_matte_{gd}_{k}.png")
        rend = {fr: frame_img(mats[f[0]], gd, f) for fr, f in FRAMES.items()}
        # per-frame size normalisation: same distance feet -> body top (hat brim / hair mass) in every frame,
        # derived from idle1 at ~430 px full height; feet on y 487; x = feet x at the cell centre, shifted only if needed
        frac = 0.35 if gd == "male" else 0.55
        cv0, f0, _ = rend["idle1"]; a0 = cv0.char_alpha; ys0 = np.nonzero(a0 > 128)[0]
        s_idle = 430 / (f0[1] - ys0.min()); target_body = s_idle * (f0[1] - body_top(a0, frac))
        cells, scales = {}, {}
        for k in STRIP + ["skill_charge", "skill_release"]:
            cv, feet, _ = rend[k]; a = cv.char_alpha; ys, xs = np.nonzero(a > 128)
            sc = target_body / (feet[1] - body_top(a, frac))
            sc = min(sc, (BASE_Y - 14) / (feet[1] - ys.min()), (CELL_W - 28) / (xs.max() - xs.min()))
            x0, x1 = (xs.min() - feet[0]) * sc, (xs.max() - feet[0]) * sc
            cx = CELL_W / 2 - (x0 + x1) / 2 * 0.0
            cx = min(max(cx, 14 - x0), CELL_W - 14 - x1)
            scales[k] = round(float(sc), 4)
            cells[k] = mc.drop_small_islands(Image.fromarray(mc.fade_edges(np.asarray(mc.to_cell(cv, feet, sc, cx)), 8)))
        scale = scales
        tag = "nam" if gd == "male" else "nu"
        strip = Image.new("RGBA", (CELL_W * 6, CELL_H))
        for i, k in enumerate(STRIP): strip.alpha_composite(cells[k], (i * CELL_W, 0))
        strip.save(out / f"mage_{tag}_strip_2520x500.png", optimize=True)
        for k in ("skill_charge", "skill_release"): cells[k].save(out / f"mage_{tag}_{k}_420x500.png", optimize=True)
        q = {k: mc.qc_cell(cells[k]) for k in cells}
        fy = [q[k]["feet_y"] for k in STRIP]
        report[gd] = {"frame_scales": scale, "feet_y_strip": fy, "feet_y_spread": int(max(fy) - min(fy)), "cells": q}
        rows = []
        for bgc in ((30, 30, 30), (255, 255, 255), (92, 103, 80)):
            r = Image.new("RGBA", (CELL_W * 8, CELL_H), bgc + (255,))
            for i, k in enumerate(STRIP + ["skill_charge", "skill_release"]): r.alpha_composite(cells[k], (i * CELL_W, 0))
            d = ImageDraw.Draw(r)
            for i in range(1, 8): d.line([(i * CELL_W, 0), (i * CELL_W, CELL_H)], fill=(255, 0, 0, 255))
            d.line([(0, BASE_Y), (CELL_W * 6, BASE_Y)], fill=(255, 220, 0, 160))
            rows.append(r.convert("RGB"))
        sh = Image.new("RGB", (CELL_W * 8, CELL_H * 3)); [sh.paste(r, (0, i * CELL_H)) for i, r in enumerate(rows)]
        sh.resize((sh.width // 2, sh.height // 2), Image.LANCZOS).save(out / f"mage_{tag}_contact.jpg", quality=90, subsampling=0)
        seq = ["idle1", "idle2"] * 2 + ["run1", "run2"] * 3 + ["cast1", "cast2", "cast2"]
        gif = [Image.alpha_composite(Image.new("RGBA", (CELL_W, CELL_H), (92, 103, 80, 255)), cells[k]).convert("RGB") for k in seq]
        gif[0].save(out / f"mage_{tag}_preview.gif", save_all=True, append_images=gif[1:], duration=[300] * 4 + [130] * 6 + [220, 300, 300], loop=0)
        print(gd, "scales", scale, "feet", fy, flush=True)
        for k, v in q.items(): print("  ", k, v["edge_band_alpha_pct"], v["opaque_components"], v["stray_opaque_islands_ge30px"], v["bbox"])
    (out / "qc.json").write_text(json.dumps(report, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
