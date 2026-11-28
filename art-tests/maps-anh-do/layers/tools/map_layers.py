"""Split the painted map_1_x2 into a ground layer + per-object tall layers (tree canopies, upper part of tall
rocks / crystals) for engine Y-sort, plus a canopy mask. Geometry/size/colour of the source are untouched:
objects are exact pixel cut-outs of the source, alpha feathered OUTWARD so ground + objects re-composite the source.
Usage: python map_layers.py segment|build <map_x2.webp> <out_dir>
"""
import sys, json, math, time
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage as ndi
sys.path.insert(0, str(Path(__file__).parent))
import maps_upscale_grade as mg

FEATHER = 3          # px, outward feather of object alpha (spec 2-4 px)
BASE_KEEP = 0.30     # rocks / crystals: bottom 30 % of the object's height stays in the ground layer
MIN_TREE, MIN_ROCK = 2500, 1800


def oklab(im):
    lab = mg.to_oklab(im.astype(np.float32) / 255); L, a, b = lab[..., 0], lab[..., 1], lab[..., 2]
    return L, np.hypot(a, b), np.degrees(np.arctan2(b, a)) % 360


def segment(im):
    L, C, h = oklab(im)
    Ls = ndi.gaussian_filter(L, 4)
    sd = np.sqrt(np.clip(ndi.gaussian_filter(L * L, 5) - ndi.gaussian_filter(L, 5) ** 2, 0, None))
    green = (h > 105) & (h < 170) & (C > 0.035)
    # --- tree canopies: darker-than-grass green, textured (leaf clusters with dark outlines)
    cand = green & (Ls < 0.635)
    cand |= (L < 0.5) & ndi.binary_dilation(cand, iterations=3)
    m = ndi.binary_opening(cand, iterations=3)
    m = ndi.binary_closing(m, iterations=6)
    m = ndi.binary_fill_holes(m)
    # bright crown tops: textured green next to the canopy
    lab0, n0 = ndi.label(m); sz0 = ndi.sum(np.ones_like(L), lab0, range(1, n0 + 1))
    k0 = np.zeros(n0 + 1, bool); k0[1:] = sz0 > MIN_TREE; m = k0[lab0]
    # bright crown tops: saturated mid-light green within 6 px of the canopy
    top = (h > 115) & (h < 160) & (C > 0.10) & (L < 0.76) & ndi.binary_dilation(m, iterations=6)
    m = ndi.binary_fill_holes(ndi.binary_closing(m | top, iterations=2))
    lab_, n = ndi.label(m)
    idx = np.arange(1, n + 1)
    sz = ndi.sum(np.ones_like(L), lab_, idx); tex = ndi.mean(sd, lab_, idx); dark = ndi.mean(L, lab_, idx)
    keep = np.zeros(n + 1, bool); keep[1:] = (sz > MIN_TREE) & (tex > 0.040)
    trees = keep[lab_]
    tree_stats = {"components_raw": int(n), "kept": int(keep.sum())}
    # --- rocks (cool grey, low chroma) and crystals (saturated blue/purple/gold, bright), excluding water
    water = (C > 0.10) & (h > 195) & (h < 250) & (L > 0.55)
    water_big = ndi.binary_opening(water, iterations=2)
    wl, wn = ndi.label(water_big); wsz = ndi.sum(np.ones_like(L), wl, range(1, wn + 1))
    water_region = np.isin(wl, 1 + np.nonzero(wsz > 40000)[0])
    water_region = ndi.binary_dilation(water_region, iterations=30)
    rock = (C < 0.055) & ((h > 170) & (h < 300) | (C < 0.025)) & (L > 0.42) & (L < 0.93) & (sd > 0.035)
    crystal = (C > 0.07) & (((h > 200) & (h < 330)) | ((h > 70) & (h < 100) & (L > 0.72))) & (L > 0.5) & (sd > 0.04)
    blue = (h > 185) & (h < 255) & (C > 0.06)
    bl, bn = ndi.label(ndi.binary_opening(blue, iterations=2)); bsz = ndi.sum(np.ones_like(L), bl, range(1, bn + 1))
    river = ndi.binary_dilation(np.isin(bl, 1 + np.nonzero(bsz > 20000)[0]), iterations=35)
    rc = (rock | crystal) & ~water_region & ~river & ~trees
    rc = ndi.binary_closing(ndi.binary_opening(rc, iterations=2), iterations=5)
    rc = ndi.binary_fill_holes(rc)
    rl, rn = ndi.label(rc); ridx = np.arange(1, rn + 1)
    rsz = ndi.sum(np.ones_like(L), rl, ridx)
    sl = ndi.find_objects(rl)
    rkeep = np.zeros(rn + 1, bool)
    for i, s in enumerate(sl):
        hh, ww = s[0].stop - s[0].start, s[1].stop - s[1].start
        rkeep[i + 1] = rsz[i] > MIN_ROCK and hh >= 45 and hh >= 0.55 * ww      # tall-ish objects only
    rocks = rkeep[rl]
    return trees, rocks, tree_stats, {"components_raw": int(rn), "kept": int(rkeep.sum())}


def overlay(im, trees, rocks, path):
    ov = im.astype(float).copy()
    ov[trees] = ov[trees] * 0.45 + np.array([255, 0, 255]) * 0.55
    ov[rocks] = ov[rocks] * 0.45 + np.array([255, 140, 0]) * 0.55
    Image.fromarray(ov.astype(np.uint8)).resize((im.shape[1] // 2, im.shape[0] // 2)).save(path, quality=85)


if __name__ == "__main__":
    mode, src, out = sys.argv[1], Path(sys.argv[2]), Path(sys.argv[3]); out.mkdir(parents=True, exist_ok=True)
    im = np.asarray(Image.open(src).convert("RGB"))
    if mode == "segment":
        t0 = time.time(); trees, rocks, ts, rs = segment(im)
        np.save(out / "_trees.npy", trees); np.save(out / "_rocks.npy", rocks)
        overlay(im, trees, rocks, out / "_seg_overlay.jpg")
        print("trees", ts, "%.1f%%" % (100 * trees.mean()), "rocks", rs, "%.1f%%" % (100 * rocks.mean()), round(time.time() - t0, 1), "s")
