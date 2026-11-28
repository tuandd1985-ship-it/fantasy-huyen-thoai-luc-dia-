"""Map pass for Do's painted maps: Upscayl 4x (digital-art-4x, local GPU) -> colour grade toward ART_DIRECTION
(map muted, hero pops; magic accents kept) -> world size x2 of the source (as v0.5.0 uses for Rừng Xanh) -> WebP.
Usage: python maps_upscale_grade.py <maps_dir> <out_dir> <hero_png>
"""
import sys, json, subprocess, time
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
Image.MAX_IMAGE_PIXELS = None

UPSCAYL = Path(r"C:\Program Files\Upscayl\resources")
MODEL = "digital-art-4x"
WORLD_SCALE = 2
# grade: chroma kept for "ground" hues (yellow/green/olive) vs everything else; emissive pixels (bright + saturated:
# crystals, lava, ice glow, portal) keep more chroma so the magic accents still read
GROUND_CHROMA, OTHER_CHROMA, EMISSIVE_CHROMA = 0.62, 0.80, 0.92
LUMA_GAIN, LUMA_CONTRAST = 0.93, 0.92
WEBP_Q = 90
LUMA_TARGET = {"map_4": 158}   # bright maps are pulled down to this mean luma (default 138); snow stays brighter
LUMA_TARGET_DEFAULT = 138
SKIP = {"tanthu1"}               # same picture as tanthu at 2x size


def srgb_to_lin(x): return np.where(x <= 0.04045, x / 12.92, ((x + 0.055) / 1.055) ** 2.4)
def lin_to_srgb(x): return np.where(x <= 0.0031308, x * 12.92, 1.055 * np.clip(x, 0, None) ** (1 / 2.4) - 0.055)


def to_oklab(rgb):
    l = srgb_to_lin(rgb)
    M1 = np.array([[0.4122214708, 0.5363325363, 0.0514459929], [0.2119034982, 0.6806995451, 0.1073969566], [0.0883024619, 0.2817188376, 0.6299787005]])
    M2 = np.array([[0.2104542553, 0.7936177850, -0.0040720468], [1.9779984951, -2.4285922050, 0.4505937099], [0.0259040371, 0.7827717662, -0.8086757660]])
    return np.cbrt(l @ M1.T) @ M2.T


def from_oklab(lab):
    M2i = np.array([[1, 0.3963377774, 0.2158037573], [1, -0.1055613458, -0.0638541728], [1, -0.0894841775, -1.2914855480]])
    M1i = np.array([[4.0767416621, -3.3077115913, 0.2309699292], [-1.2684380046, 2.6097574011, -0.3413193965], [-0.0041960863, -0.7034186147, 1.7076147010]])
    return np.clip(lin_to_srgb((lab @ M2i.T) ** 3 @ M1i.T), 0, 1)


def grade(rgb_u8, extra_gain=1.0):
    lab = to_oklab(rgb_u8.astype(np.float32) / 255)
    L, a, b = lab[..., 0], lab[..., 1], lab[..., 2]
    C = np.hypot(a, b); h = np.degrees(np.arctan2(b, a)) % 360
    ground = (h > 70) & (h < 150)                      # oklab hue: yellow ~100, green ~140
    emissive = (L > 0.78) & (C > 0.10) & ~ground
    k = np.where(ground, GROUND_CHROMA, OTHER_CHROMA); k = np.where(emissive, EMISSIVE_CHROMA, k)
    Lm = L.mean(); L2 = (Lm + (L - Lm) * LUMA_CONTRAST) * LUMA_GAIN
    L2 = L2 * extra_gain
    L2 = np.where(emissive, np.maximum(L2, L * 0.97), L2)
    out = from_oklab(np.dstack([L2, a * k, b * k]))
    return (out * 255).round().astype(np.uint8)


def sat_luma(rgb):
    x = rgb.astype(float); mx, mn = x.max(-1), x.min(-1)
    return float(np.mean((mx - mn) / np.maximum(mx, 1))), float((x @ [0.299, 0.587, 0.114]).mean())


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2]); hero = Image.open(sys.argv[3]).convert("RGBA")
    (out / "up4").mkdir(parents=True, exist_ok=True); (out / "game").mkdir(exist_ok=True); (out / "compare").mkdir(exist_ok=True)
    H = np.asarray(hero); hs, hl = sat_luma(H[..., :3][H[..., 3] > 200])
    hero150 = hero.crop(hero.getbbox()); hero150 = hero150.resize((round(hero150.width * 150 / hero150.height), 150), Image.LANCZOS)
    rep = {"upscaler": f"Upscayl upscayl-bin, model {MODEL}, x4", "world_scale": WORLD_SCALE,
           "grade": {"ground_chroma": GROUND_CHROMA, "other_chroma": OTHER_CHROMA, "emissive_chroma": EMISSIVE_CHROMA,
                     "luma_gain": LUMA_GAIN, "luma_contrast": LUMA_CONTRAST}, "hero_ref": {"saturation": round(hs, 3), "luma": round(hl, 1)}, "maps": {}}
    for f in sorted(src.glob("*.png")):
        if f.stem in SKIP: continue
        gain = 1.0
        t0 = time.time(); u4 = out / "up4" / f.name
        if not u4.exists():
            subprocess.run([str(UPSCAYL / "bin" / "upscayl-bin.exe"), "-i", str(f), "-o", str(u4), "-s", "4", "-m", str(UPSCAYL / "models"),
                            "-n", MODEL, "-f", "png", "-t", "256"], check=True, capture_output=True)
        t_up = round(time.time() - t0, 1)
        s0 = Image.open(f).convert("RGB"); W, Hh = s0.size; tw, th = W * WORLD_SCALE, Hh * WORLD_SCALE
        big = Image.open(u4).convert("RGB").resize((tw, th), Image.LANCZOS)
        g = Image.fromarray(grade(np.asarray(big)))
        tgt = LUMA_TARGET.get(f.stem, LUMA_TARGET_DEFAULT)
        for _ in range(3):   # pull bright maps down toward the target mean luma (map darker than the hero)
            _, lum = sat_luma(np.asarray(g.resize((W // 2, Hh // 2))))
            if lum <= tgt + 1: break
            gain = gain * (tgt / lum) ** 0.9
            g = Image.fromarray(grade(np.asarray(big), gain))
        gain = 1.0
        g.save(out / "game" / (f.stem + f"_x{WORLD_SCALE}.webp"), quality=WEBP_Q, method=6)
        b_s, b_l = sat_luma(np.asarray(s0)); a_s, a_l = sat_luma(np.asarray(g.resize((W, Hh))))
        rep["maps"][f.stem] = {"source": list(s0.size), "game_size": [tw, th], "upscale_seconds": t_up,
                               "saturation_before": round(b_s, 3), "saturation_after": round(a_s, 3), "luma_before": round(b_l, 1),
                               "luma_after": round(a_l, 1), "sat_ratio_map_over_hero_after": round(a_s / hs, 2),
                               "webp_bytes": (out / "game" / (f.stem + f"_x{WORLD_SCALE}.webp")).stat().st_size}
        # before/after: whole map + a 640x480 screen crop at world scale with the hero (centre of the map)
        thumb_b = s0.resize((560, round(560 * Hh / W))); thumb_a = g.resize((560, round(560 * Hh / W)))
        cx, cy = tw // 2, th // 2
        scr_b = s0.resize((tw, th), Image.BICUBIC).crop((cx - 320, cy - 240, cx + 320, cy + 240)).convert("RGBA")
        scr_a = g.crop((cx - 320, cy - 240, cx + 320, cy + 240)).convert("RGBA")
        for s_ in (scr_b, scr_a): s_.alpha_composite(hero150, (320 - hero150.width // 2, 400 - hero150.height))
        C = Image.new("RGB", (1300, 30 + thumb_b.height + 20 + 480 + 10), "white"); d = ImageDraw.Draw(C)
        d.text((10, 8), f"{f.stem}: TRUOC (anh goc, keo gian x2 nhu hien tai)", fill="black"); d.text((660, 8), "SAU (Upscayl 4x digital-art + chinh mau, x2)", fill="black")
        C.paste(thumb_b, (10, 30)); C.paste(thumb_a, (660, 30)); y = 30 + thumb_b.height + 20
        C.paste(scr_b.convert("RGB"), (10, y)); C.paste(scr_a.convert("RGB"), (660, y))
        C.save(out / "compare" / f"{f.stem}_before_after.jpg", quality=88)
        print(f.stem, rep["maps"][f.stem], flush=True)
    (out / "maps_report.json").write_text(json.dumps(rep, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()
