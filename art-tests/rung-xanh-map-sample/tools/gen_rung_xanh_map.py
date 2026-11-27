"""Rừng Xanh map sample: 1 seamless grass tile + 6 props on light grey (SDXL Base, native nodes).
Usage: python gen_rung_xanh_map.py <out_dir>
"""
import sys, json
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, str(Path(__file__).parent))
import comfy_api as c

TILE_POS = ("seamless tileable top-down game texture, lush forest grass ground with small clover patches and tiny "
            "flowers, soft hand painted style, even lighting, no shadows from objects, no objects, high detail")
TILE_NEG = "objects, trees, rocks, characters, perspective, horizon, sky, text, seams, vignette, border, frame, blurry, photo"

PROP_STYLE = ("hand painted fantasy rpg game asset, three-quarter top-down view, soft cel shading, vibrant colors, "
              "clean dark outline, centered, full object visible, simple background, plain light grey background")
PROP_NEG = ("text, watermark, logo, frame, border, multiple objects, scenery, landscape, ground plane, cast shadow, "
            "gradient background, colored background, cropped, blurry, photo, realistic, 3d render")
PROPS = {
    "cay_soi": "single round leafy oak tree with thick brown trunk and lush green crown",
    "tang_da_reu": "single mossy boulder, grey stone covered with green moss",
    "cot_da_co": "single ancient broken stone ruin pillar with carved runes and ivy",
    "bui_cay": "single round green leafy bush shrub",
    "khom_hoa": "single small clump of colorful wildflowers, yellow white and pink flowers with green leaves",
    "da_cong_dich_chuyen": "single magic teleport portal stone circle, ancient standing stones ring with glowing cyan runes on a round stone platform",
}
SEEDS = [728101, 728102]


def make_tile(out):
    raw = out / "tile_raw.png"
    pid, t = c.run(c.txt2img(TILE_POS, TILE_NEG, 728001), raw)
    im = np.asarray(Image.open(raw).convert("RGB"))
    h, w = im.shape[:2]
    rolled = np.roll(np.roll(im, h // 2, 0), w // 2, 1)  # seams now form a cross in the centre
    band = 96
    a = np.full((h, w), 255, np.uint8)
    a[h // 2 - band // 2:h // 2 + band // 2, :] = 0
    a[:, w // 2 - band // 2:w // 2 + band // 2] = 0
    Image.fromarray(np.dstack([rolled, a])).save(out / "tile_rolled_masked.png")
    name = c.upload(out / "tile_rolled_masked.png")
    fixed = out / "tile_inpaint.png"
    pid2, t2 = c.run(c.inpaint(name, TILE_POS, TILE_NEG, 728002, denoise=0.7), fixed)
    f = np.asarray(Image.open(fixed).convert("RGB")).astype(float)
    m = (Image.fromarray(255 - a).filter(ImageFilter.GaussianBlur(10)))
    m = np.asarray(m).astype(float)[..., None] / 255.0
    tile = (rolled * (1 - m) + f * m).round().astype(np.uint8)  # repainted cross, original elsewhere
    Image.fromarray(tile).save(out / "tile_co_rung_xanh_1024.png")
    return {"txt2img_seed": 728001, "inpaint_seed": 728002, "seconds": [t, t2], "prompt": TILE_POS, "negative": TILE_NEG}


def make_props(out):
    meta = {}
    (out / "props_raw").mkdir(exist_ok=True)
    for k, desc in PROPS.items():
        for s in SEEDS:
            p = f"{desc}, {PROP_STYLE}"
            pid, t = c.run(c.txt2img(p, PROP_NEG, s), out / "props_raw" / f"{k}_s{s}.png")
            meta[f"{k}_s{s}"] = {"prompt": p, "negative": PROP_NEG, "seed": s, "seconds": t}
            print(k, s, t, flush=True)
    return meta


if __name__ == "__main__":
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    meta = {"model": c.CKPT, "sampler": "dpmpp_2m karras", "steps": 28, "cfg": 6.5, "size": "1024x1024"}
    meta["tile"] = make_tile(out); print("tile", meta["tile"]["seconds"], flush=True)
    meta["props"] = make_props(out)
    (out / "generation.json").write_text(json.dumps(meta, indent=1, ensure_ascii=False), encoding="utf-8")
