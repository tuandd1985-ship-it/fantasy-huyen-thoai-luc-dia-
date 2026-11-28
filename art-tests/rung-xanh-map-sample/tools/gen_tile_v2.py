"""Rừng Xanh grass tile v2: muted, low contrast, sparse flowers. Same seamless method as v1
(roll half + inpaint the cross with native SetLatentNoiseMask), then a wrap-safe post-process:
flatten low-frequency light patches (they reveal the repeat), lower contrast and saturation.
Usage: python gen_tile_v2.py <out_dir> <props_clean_dir> <hero_png>
"""
import sys, json, time
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage as ndi
sys.path.insert(0, str(Path(__file__).parent))
import comfy_api as c

POS = ("seamless tileable top-down game ground texture, soft painted grass, muted olive green, low contrast, "
       "broad flat grass patches, short sparse grass strokes, a few tiny scattered flowers, stylized hand painted "
       "rpg map ground, flat even lighting, simple, calm")
NEG = ("dense flowers, flower carpet, pink flowers, long grass blades, tall grass, realistic, photo, photorealistic, "
       "high detail, high contrast, saturated, vibrant, objects, rocks, stones, trees, path, dirt road, characters, "
       "perspective, horizon, sky, text, seams, vignette, border, frame, blurry")
SEEDS = [729001, 729002, 729003]
FLATTEN_SIGMA = 90     # px, low-frequency light patches removed above this scale
FLATTEN_KEEP = 0.35    # keep 35 % of the low-frequency variation
CONTRAST = 0.80        # detail contrast around the local mean
SAT = 0.80             # saturation scale


def seamless(raw, seed, out):
    im = np.asarray(Image.open(raw).convert("RGB"))
    h, w = im.shape[:2]
    rolled = np.roll(np.roll(im, h // 2, 0), w // 2, 1)
    band = 96
    a = np.full((h, w), 255, np.uint8)
    a[h // 2 - band // 2:h // 2 + band // 2, :] = 0
    a[:, w // 2 - band // 2:w // 2 + band // 2] = 0
    p = out / f"_rolled_{seed}.png"; Image.fromarray(np.dstack([rolled, a])).save(p)
    fixed = out / f"_inpaint_{seed}.png"
    _, t = c.run(c.inpaint(c.upload(p), POS, NEG, seed + 500, denoise=0.7), fixed)
    f = np.asarray(Image.open(fixed).convert("RGB")).astype(float)
    m = np.asarray(Image.fromarray(255 - a).filter(ImageFilter.GaussianBlur(10))).astype(float)[..., None] / 255
    return (rolled * (1 - m) + f * m), t


def post(x):
    """All filters use mode='wrap' so the tile stays seamless."""
    low = np.stack([ndi.gaussian_filter(x[..., i], FLATTEN_SIGMA, mode="wrap") for i in range(3)], -1)
    mean = x.reshape(-1, 3).mean(0)
    low2 = mean + FLATTEN_KEEP * (low - mean)
    y = low2 + CONTRAST * (x - low)
    g = y.mean(-1, keepdims=True)
    y = g + SAT * (y - g)
    return np.clip(y, 0, 255).round().astype(np.uint8)


def metrics(t):
    x = t.astype(float)
    d = lambda a, b: np.abs(a - b).mean()
    inner_x = np.mean([d(x[:, i], x[:, i + 1]) for i in range(100, 900, 50)])
    inner_y = np.mean([d(x[i], x[i + 1]) for i in range(100, 900, 50)])
    mx, mn = x.max(-1), x.min(-1)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1), 0)
    lumi = x @ [0.299, 0.587, 0.114]
    low = ndi.gaussian_filter(lumi, 60, mode="wrap")
    return {"seam_ratio_x": round(d(x[:, -1], x[:, 0]) / inner_x, 3), "seam_ratio_y": round(d(x[-1], x[0]) / inner_y, 3),
            "mean_rgb": x.reshape(-1, 3).mean(0).round(1).tolist(), "mean_saturation": round(float(sat.mean()), 3),
            "luma_std": round(float(lumi.std()), 2), "lowfreq_luma_std": round(float(low.std()), 2),
            "pink_px_pct": round(100 * float(((x[..., 0] > x[..., 1] + 15) & (x[..., 2] > x[..., 1])).mean()), 3)}


def grid(t, n, cell=None):
    im = Image.fromarray(t)
    if cell: im = im.resize((cell, cell), Image.LANCZOS)
    s = im.width; G = Image.new("RGB", (s * n, s * n))
    for i in range(n):
        for j in range(n): G.paste(im, (i * s, j * s))
    return G


def scene(tile, props_dir, hero, path, cell=384):
    sc = grid(np.asarray(tile), 4, cell).crop((0, 0, 1280, 720)).convert("RGBA")
    props = {p.stem: Image.open(p).convert("RGBA") for p in Path(props_dir).glob("*.png")}
    heights = {"cay_soi": 300, "cot_da_co": 220, "da_cong_dich_chuyen": 200, "tang_da_reu": 110, "bui_cay": 95, "khom_hoa": 60}
    place = [("cay_soi", 170, 330), ("cot_da_co", 1080, 300), ("da_cong_dich_chuyen", 640, 260), ("tang_da_reu", 420, 600),
             ("bui_cay", 880, 620), ("khom_hoa", 300, 690), ("bui_cay", 1180, 520), ("khom_hoa", 760, 690), ("cay_soi", 1000, 690),
             ("__hero", 560, 560)]
    for k, x, yb in sorted(place, key=lambda t: t[2]):
        im = hero if k == "__hero" else props[k]
        h = 150 if k == "__hero" else heights[k]
        s = h / im.height; im2 = im.resize((max(1, int(im.width * s)), h), Image.LANCZOS)
        sh = Image.new("RGBA", sc.size); ImageDraw.Draw(sh).ellipse([x - im2.width * 0.35, yb - 10, x + im2.width * 0.35, yb + 8], fill=(0, 0, 0, 90))
        sc.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)))
        sc.alpha_composite(im2, (int(x - im2.width / 2), int(yb - im2.height)))
    sc.convert("RGB").save(path, quality=95, subsampling=0)


if __name__ == "__main__":
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    hero = Image.open(sys.argv[3]).convert("RGBA")
    meta = {"model": c.CKPT, "sampler": "dpmpp_2m karras", "steps": 28, "cfg": 6.5, "prompt": POS, "negative": NEG,
            "post": {"flatten_sigma": FLATTEN_SIGMA, "flatten_keep": FLATTEN_KEEP, "contrast": CONTRAST, "saturation": SAT},
            "candidates": {}}
    for s in SEEDS:
        raw = out / f"_raw_{s}.png"
        _, t1 = c.run(c.txt2img(POS, NEG, s), raw)
        sm, t2 = seamless(raw, s, out)
        t0 = time.time(); tile = post(sm); t3 = round(time.time() - t0, 2)
        Image.fromarray(tile).save(out / f"tile_v2_s{s}.png")
        meta["candidates"][s] = {"inpaint_seed": s + 500, "seconds": {"txt2img": t1, "inpaint": t2, "post": t3},
                                 "metrics_before_post": metrics(sm.round().astype(np.uint8)), "metrics": metrics(tile)}
        print(s, meta["candidates"][s]["metrics"], flush=True)
        grid(tile, 3, 384).save(out / f"_grid3_s{s}.jpg", quality=90)
        scene(Image.fromarray(tile), sys.argv[2], hero, out / f"_scene_s{s}.jpg")
    (out / "generation.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")
