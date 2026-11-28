"""Build step for map_layers: per-object layers (trees split by watershed, rock/crystal tops), SDXL ground fill under
removed areas, canopy mask, layers.json, exact re-composite check.
Usage: python map_layers_build.py <map_x2.webp> <out_dir>   (run map_layers.py segment first)
"""
import sys, json, time
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
sys.path.insert(0, str(Path(__file__).parent))
import map_layers as ml
import comfy_api as c

FEATHER, BASE_KEEP = ml.FEATHER, ml.BASE_KEEP
# rock/crystal components that are actually water (river surface, waterfall, sea edge); world (y, x) centroids
WATER_FP = [(30, 1014), (196, 508), (643, 999), (608, 42), (770, 199), (852, 55), (908, 1926), (1207, 2024),
            (1402, 1817), (2054, 2772), (2181, 2688)]
FILL_PROMPT = ("top-down painted fantasy rpg game map ground, soft green grass with small flowers, sandy dirt path, "
               "hand painted, cel shading, seamless continuation")
FILL_NEG = ("tree, trees, bush, rock, rocks, boulder, stone, crystal, pink, building, character, statue, ghost, "
            "text, watermark, frame, blurry, photo")
FILL_SEED, FILL_DENOISE = 740001, 0.72


def split_trees(trees):
    """Split merged canopy blobs into single crowns: watershed on the smoothed distance transform."""
    from skimage.segmentation import watershed
    from skimage.feature import peak_local_max
    dist = ndi.gaussian_filter(ndi.distance_transform_edt(trees), 3)
    pk = peak_local_max(dist, min_distance=38, threshold_abs=18, labels=ndi.label(trees)[0])
    markers = np.zeros(trees.shape, np.int32)
    for i, (y, x) in enumerate(pk): markers[y, x] = i + 1
    lab = watershed(-dist, markers, mask=trees)
    rest, rn = ndi.label(trees & (lab == 0))
    lab[rest > 0] = rest[rest > 0] + lab.max()
    return lab


def trunk_base(L, C, h, m):
    """baseY of a crown: follow brown trunk pixels below the crown bottom in a band around the crown centre."""
    ys, xs = np.nonzero(m); yb = ys.max()
    low = ys > yb - 12; xc = int(np.median(xs[low])) if low.any() else int(xs.mean())
    w = max(6, int((xs.max() - xs.min()) * 0.12)); H = L.shape[0]; trunk = 0
    for dy in range(1, 90):
        y = yb + dy
        if y >= H: break
        band = slice(max(0, xc - w), xc + w)
        brown = ((h[y, band] > 40) & (h[y, band] < 95) & (L[y, band] < 0.62) & (C[y, band] > 0.03)).mean()
        if brown < 0.25: break
        trunk = dy
    return int(yb + max(trunk, 8)), trunk


def prefill(im, M):
    _, (iy, ix) = ndi.distance_transform_edt(M, return_indices=True)
    f = im[iy, ix].astype(float)
    bl = np.stack([ndi.gaussian_filter(f[..., k], 6) for k in range(3)], -1)
    return np.where(M[..., None], bl, im).astype(np.uint8)


def sdxl_fill(pre, M, out, tile=1024, overlap=160):
    H, W = M.shape; acc = np.zeros(pre.shape, float); wsum = np.zeros((H, W)); k = 0
    ys = sorted(set(list(range(0, H - tile, tile - overlap)) + [H - tile]))
    xs = sorted(set(list(range(0, W - tile, tile - overlap)) + [W - tile]))
    for y0 in ys:
        for x0 in xs:
            mt = M[y0:y0 + tile, x0:x0 + tile]
            if mt.sum() < 50: continue
            grow = ndi.binary_dilation(mt, iterations=6)
            rgba = np.dstack([pre[y0:y0 + tile, x0:x0 + tile], np.where(grow, 0, 255).astype(np.uint8)])
            p = out / f"_fill_in_{k}.png"; Image.fromarray(rgba).save(p)
            wf = c.inpaint(c.upload(p), FILL_PROMPT, FILL_NEG, FILL_SEED + k, denoise=FILL_DENOISE)
            wf["7"]["inputs"]["filename_prefix"] = "game_art_core/map_fill"
            c.run(wf, out / f"_fill_out_{k}.png")
            g = np.asarray(Image.open(out / f"_fill_out_{k}.png").convert("RGB")).astype(float)
            # weight fades toward the tile border so overlapping tiles blend
            yy, xx = np.mgrid[:tile, :tile]; edge = np.minimum.reduce([yy, xx, tile - 1 - yy, tile - 1 - xx]).astype(float)
            wt = np.clip(edge / 64, 0.02, 1)
            acc[y0:y0 + tile, x0:x0 + tile] += g * wt[..., None]; wsum[y0:y0 + tile, x0:x0 + tile] += wt; k += 1
    return np.where((wsum > 0)[..., None], acc / np.maximum(wsum, 1e-6)[..., None], pre.astype(float)), k


def texture_fill(im, M, L, C, h, seed=7):
    """Fill M with patches of clean grass sampled from the map itself (no generated objects): candidate 192x192
    windows that are mostly grass and outside M; 128 px patches with Gaussian blending at a 64 px stride."""
    rng = np.random.default_rng(seed); H, W = M.shape
    grassish = (h > 105) & (h < 165) & (C > 0.05) & (L > 0.55) & (L < 0.82)
    win = 128; pool = []
    for y in range(0, H - win, 32):
        for x in range(0, W - win, 32):
            if M[y:y + win, x:x + win].mean() > 0.01: continue
            if grassish[y:y + win, x:x + win].mean() > 0.72: pool.append((y, x))
    P, st = 96, 48
    gy = np.exp(-((np.arange(P) - P / 2) ** 2) / (2 * (P / 4) ** 2)); wk = np.outer(gy, gy)
    acc = np.zeros(im.shape, float); ws = np.zeros((H, W))
    Mg = ndi.binary_dilation(M, iterations=P // 2)
    for y in range(-P // 2, H, st):
        for x in range(-P // 2, W, st):
            y0, x0 = max(0, y), max(0, x); y1, x1 = min(H, y + P), min(W, x + P)
            if y1 <= y0 or x1 <= x0 or not Mg[y0:y1, x0:x1].any(): continue
            sy, sx = pool[rng.integers(len(pool))]; oy, ox = rng.integers(0, win - P + 1, 2)
            patch = im[sy + oy:sy + oy + P, sx + ox:sx + ox + P].astype(float)
            py0, px0 = y0 - y, x0 - x
            acc[y0:y1, x0:x1] += patch[py0:py0 + (y1 - y0), px0:px0 + (x1 - x0)] * wk[py0:py0 + (y1 - y0), px0:px0 + (x1 - x0), None]
            ws[y0:y1, x0:x1] += wk[py0:py0 + (y1 - y0), px0:px0 + (x1 - x0)]
    tex = np.where((ws > 0)[..., None], acc / np.maximum(ws, 1e-6)[..., None], im.astype(float))
    return tex, len(pool)


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2]); t0 = time.time()
    im = np.asarray(Image.open(src).convert("RGB")); H, W = im.shape[:2]; L, C, h = ml.oklab(im)
    trees = np.load(out / "_trees.npy"); rocks = np.load(out / "_rocks.npy")
    rl, rn = ndi.label(rocks); cms = ndi.center_of_mass(rocks, rl, range(1, rn + 1)); dropped = 0
    for i, (cy, cx) in enumerate(cms):
        if any(abs(cy - y) < 25 and abs(cx - x) < 25 for y, x in WATER_FP): rocks[rl == i + 1] = False; dropped += 1
    # trunks stay in the ground layer (they are obstacles): brown wood pixels in the lower part of each crown blob
    wood = (h > 35) & (h < 98) & (C > 0.03) & (L < 0.60)
    tb, tn = ndi.label(trees); lower = np.zeros_like(trees)
    for i, s_ in enumerate(ndi.find_objects(tb)):
        y0, y1 = s_[0].start, s_[0].stop; cut = int(y0 + (y1 - y0) * 0.45)
        sub = np.zeros_like(trees); sub[s_] = tb[s_] == i + 1; sub[:cut] = False; lower |= sub
    trunk_px = ndi.binary_opening(wood & lower, iterations=1)
    trunk_px = ndi.binary_dilation(trunk_px, iterations=1) & lower
    trees = trees & ~trunk_px
    trunks_kept = int(trunk_px.sum())
    objs = []
    tl = split_trees(trees)
    for i, s in enumerate(ndi.find_objects(tl)):
        if s is None: continue
        m = np.zeros((H, W), bool); m[s] = tl[s] == i + 1
        if m.sum() < 800: continue
        base, trunk = trunk_base(L, C, h, m)
        objs.append({"kind": "tree", "mask": m, "baseY": base, "trunk_px": trunk})
    rl, rn = ndi.label(rocks)
    for i, s in enumerate(ndi.find_objects(rl)):
        full = np.zeros((H, W), bool); full[s] = rl[s] == i + 1
        y0, y1 = s[0].start, s[0].stop; cut = int(y1 - (y1 - y0) * BASE_KEEP)
        top = full.copy(); top[cut:] = False
        if top.sum() < 300: continue
        objs.append({"kind": "rock", "mask": top, "baseY": int(y1 - 1), "trunk_px": None})
    M = np.zeros((H, W), bool)
    for o in objs: M |= o["mask"]
    print("objects", len(objs), "removed %.1f%%" % (100 * M.mean()), "water fp dropped", dropped, flush=True)
    pre = prefill(im, M)
    tex, npool = texture_fill(im, M, L, C, h)
    ntiles = 0
    # inside each hole: grass texture, tone-matched to its ring; the first 6 px from the hole edge blend from the
    # nearest-ground prefill (continues path / bank colours) into the texture
    din = ndi.distance_transform_edt(M)
    wedge = np.clip(din / 6, 0, 1)[..., None]
    filled = pre.astype(float) * (1 - wedge) + tex * wedge
    # tone-match each filled hole to its surrounding ground ring so colours continue naturally
    ground = im.astype(float).copy(); hl, hn = ndi.label(M)
    for j, s in enumerate(ndi.find_objects(hl)):
        s2 = (slice(max(0, s[0].start - 14), s[0].stop + 14), slice(max(0, s[1].start - 14), s[1].stop + 14))
        hole = hl[s2] == j + 1; ring = ndi.binary_dilation(hole, iterations=10) & ~M[s2]
        f = filled[s2][hole]
        if ring.sum() >= 20:
            r = im[s2][ring].astype(float)
            f = (f - f.mean(0)) * np.clip(r.std(0) / np.maximum(f.std(0), 1), 0.6, 1.0) + r.mean(0)
        g = ground[s2]; g[hole] = f
    ground = np.where(M[..., None], ground, im).clip(0, 255).round().astype(np.uint8)
    assert np.array_equal(ground[~M], im[~M])          # outside the removed area the source is untouched
    Image.fromarray(ground).save(out / "map_1_ground.webp", quality=95, method=6)
    Image.fromarray(ground).save(out / "_map_1_ground_lossless.png")
    (out / "objects").mkdir(exist_ok=True)
    for f_ in (out / "objects").glob("*.png"): f_.unlink()
    meta = []; canopy = np.zeros((H, W)); objs.sort(key=lambda o: o["baseY"])
    for k, o in enumerate(objs):
        m = o["mask"]; d = ndi.distance_transform_edt(~m)
        a = np.clip(1 - d / (FEATHER + 1), 0, 1)                         # 1 inside, fades to 0 over FEATHER px outside
        ys, xs = np.nonzero(a > 0); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        rgba = np.dstack([im[y0:y1, x0:x1], (a[y0:y1, x0:x1] * 255).round().astype(np.uint8)])
        name = f"{o['kind']}_{k:03d}.png"; Image.fromarray(rgba).save(out / "objects" / name, optimize=True)
        canopy[y0:y1, x0:x1] = np.maximum(canopy[y0:y1, x0:x1], a[y0:y1, x0:x1])
        meta.append({"file": f"objects/{name}", "kind": o["kind"], "bbox": [int(x0), int(y0), int(x1 - x0), int(y1 - y0)],
                     "baseY": int(o["baseY"]), "trunk_px": o["trunk_px"], "area_px": int(m.sum())})
    Image.fromarray((canopy * 255).round().astype(np.uint8), "L").save(out / "map_1_canopy_mask.png", optimize=True)
    comp = Image.open(out / "_map_1_ground_lossless.png").convert("RGBA")
    for mo in meta: comp.alpha_composite(Image.open(out / mo["file"]).convert("RGBA"), (mo["bbox"][0], mo["bbox"][1]))
    comp_rgb = np.asarray(comp.convert("RGB")); comp.convert("RGB").save(out / "_recomposite.png")
    diff = np.abs(comp_rgb.astype(int) - im.astype(int))
    gw = np.asarray(Image.open(out / "map_1_ground.webp").convert("RGB")).astype(int)
    info = {"world": [W, H], "objects": len(meta), "trees": sum(x["kind"] == "tree" for x in meta),
            "rock_crystal_tops": sum(x["kind"] == "rock" for x in meta), "removed_area_pct": round(100 * float(M.mean()), 2),
            "recomposite_lossless_max_abs_diff": int(diff.max()), "recomposite_px_diff_gt1": int((diff.max(-1) > 1).sum()),
            "ground_webp_q95_vs_lossless_outside_removed_mean_abs": round(float(np.abs(gw - ground.astype(int))[~M].mean()), 3),
            "water_false_positives_dropped": dropped, "trunk_px_kept_in_ground": trunks_kept, "fill": "texture synthesis from clean grass windows of map_1 itself (pool %d windows), tone-matched per hole; SDXL inpaint tried first and rejected (invented boulders/huts)" % npool, "seconds": round(time.time() - t0, 1)}
    (out / "layers.json").write_text(json.dumps({"source": "art-tests/maps-anh-do/upscaled-x2/map_1_x2.webp", "world": [W, H],
        "ground": "map_1_ground.webp", "canopy_mask": "map_1_canopy_mask.png",
        "draw": "ground first; then every object at (bbox[0], bbox[1]), Y-sorted by baseY together with hero/monster feet y",
        "objects": meta}, indent=1), encoding="utf-8")
    (out / "build_info.json").write_text(json.dumps(info, indent=1), encoding="utf-8"); print(info)


if __name__ == "__main__":
    main()
