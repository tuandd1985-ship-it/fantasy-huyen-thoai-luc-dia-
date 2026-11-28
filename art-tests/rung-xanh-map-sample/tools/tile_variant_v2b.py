"""Tile variant v2b: same seamless source as v2 (seed 729003 + inpaint 729503, no new generation), greener and less
yellow than v2, a little more grass texture, saturation kept clearly below the hero (ART_DIRECTION: map muted, hero pops).
Usage: python tile_variant_v2b.py <tile_v2_dir> <hero_png> <props_clean_dir>"""
import sys, json
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi
sys.path.insert(0, str(Path(__file__).parent))
import gen_tile_v2 as g

SEED = 729003
FLATTEN_KEEP, CONTRAST, SAT = 0.45, 0.95, 0.55
TARGET_RGB = np.array([92.0, 112.0, 70.0])    # muted moss green, darker and less yellow than v2 (115,119,67)


def rebuild_seamless(d):
    im = np.asarray(Image.open(d / f"_raw_{SEED}.png").convert("RGB"))
    h, w = im.shape[:2]; rolled = np.roll(np.roll(im, h // 2, 0), w // 2, 1).astype(float)
    a = np.full((h, w), 255, np.uint8); a[h // 2 - 48:h // 2 + 48, :] = 0; a[:, w // 2 - 48:w // 2 + 48] = 0
    f = np.asarray(Image.open(d / f"_inpaint_{SEED}.png").convert("RGB")).astype(float)
    m = np.asarray(Image.fromarray(255 - a).filter(ImageFilter.GaussianBlur(10))).astype(float)[..., None] / 255
    return rolled * (1 - m) + f * m


def post(x):
    low = np.stack([ndi.gaussian_filter(x[..., i], g.FLATTEN_SIGMA, mode="wrap") for i in range(3)], -1)
    mean = x.reshape(-1, 3).mean(0)
    y = TARGET_RGB + FLATTEN_KEEP * (low - mean) + CONTRAST * (x - low)     # recentre the palette on TARGET_RGB
    gr = y.mean(-1, keepdims=True); y = gr + SAT * (y - gr)
    return np.clip(y, 0, 255).round().astype(np.uint8)


def sat_luma(rgb):
    x = rgb.astype(float); mx, mn = x.max(-1), x.min(-1)
    return float(np.mean((mx - mn) / np.maximum(mx, 1))), float((x @ [0.299, 0.587, 0.114]).mean())


if __name__ == "__main__":
    d = Path(sys.argv[1]); t = post(rebuild_seamless(d))
    # sanity: rebuilt v2 equals the published v2 (same source, same v2 post)
    assert np.array_equal(g.post(rebuild_seamless(d)), np.asarray(Image.open(d / "tile_co_rung_xanh_v2_1024.png")))
    Image.fromarray(t).save(d / "tile_co_rung_xanh_v2b_1024.png")
    g.grid(t, 2, 512).save(d / "tile_v2b_2x2.jpg", quality=92, subsampling=0)
    g.grid(t, 3, 384).save(d / "tile_v2b_3x3.jpg", quality=92, subsampling=0)
    hero = Image.open(sys.argv[2]).convert("RGBA")
    g.scene(Image.fromarray(t), sys.argv[3], hero, d / "scene_test_v2b_1280x720.jpg")
    H = np.asarray(hero); hs, hl = sat_luma(H[..., :3][H[..., 3] > 200])
    res = {"source": {"txt2img_seed": SEED, "inpaint_seed": SEED + 500}, "post": {"flatten_keep": FLATTEN_KEEP, "contrast": CONTRAST,
           "saturation": SAT, "target_rgb": TARGET_RGB.tolist(), "flatten_sigma": g.FLATTEN_SIGMA}, "metrics": g.metrics(t),
           "hero_vs_tile": {}}
    for name, im in (("v1", "../rung_xanh_map/tile_co_rung_xanh_1024.png"), ("v2", "tile_co_rung_xanh_v2_1024.png"), ("v2b", "tile_co_rung_xanh_v2b_1024.png")):
        ts, tl = sat_luma(np.asarray(Image.open(d / im).convert("RGB")).reshape(-1, 3))
        res["hero_vs_tile"][name] = {"tile_saturation": round(ts, 3), "tile_luma": round(tl, 1), "hero_saturation": round(hs, 3),
                                     "hero_luma": round(hl, 1), "saturation_ratio_tile_over_hero": round(ts / hs, 2)}
    (d / "variant_v2b.json").write_text(json.dumps(res, indent=1, default=float), encoding="utf-8")
    print(json.dumps(res, indent=1, default=float))
