"""Build the LoRA dataset for Pháp Sư Nam (trigger 'pspnam'): reference + v1 rig frames + v2 IP-Adapter frames,
each matted (BiRefNet GPU), upscaled with Upscayl when small, centred on white 1024x1024 (character ~880 px tall),
caption .txt next to each image. Output folder goes under ComfyUI/input/ so LoadImageTextDataSetFromFolder sees it.
Usage: python lora_dataset_mage.py <out_dir>
"""
import sys, subprocess, json
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0, str(Path(__file__).parent))
import compose_mage_v2 as cm

UPS = Path(r"C:\Program Files\Upscayl\resources")
TRIG = "pspnam"
BASE_CAP = (f"{TRIG}, 1boy, solo, chibi, young wizard, dark blue messy hair, blue eyes, small white goatee, wide-brimmed pointed "
            "dark blue wizard hat with gold trim and crescent moon, dark blue wizard robe and cape with gold embroidery, brown belt, "
            "brown boots, wooden staff with glowing blue orb")
TAIL = "full body, white background, simple background"
O = Path("C:/AI/GAME-ART-CORE/output")
REF = Path("C:/Users/DOTUAN~1/AppData/Local/Temp/claude/0026eb623bf958f6/d9570d91-8ab6-4e18-b704-35c9c91712aa/scratchpad/game/src/art-tests/hero-edge-clean/cleaned_png/hero-mage-male.png")
V1_POSE = ["standing, holding staff", "standing, holding staff", "running, holding staff", "running, holding staff",
           "casting spell, raising staff", "casting spell, staff forward, magic burst"]
V2_POSE = {"idle": "standing, holding staff", "run": "running, leaning forward, cape flowing", "run2": "running, mid stride",
           "cast1": "winding up a spell, staff pulled back", "cast2": "thrusting staff forward, arm extended, glowing orb",
           "skill_charge": "charging magic, staff raised overhead, magic aura", "skill_release": "unleashing a spell, lunging forward, magic blast"}


def upscale(png, out):
    subprocess.run([str(UPS / "bin/upscayl-bin.exe"), "-i", str(png), "-o", str(out), "-s", "4", "-m", str(UPS / "models"),
                    "-n", "digital-art-4x", "-f", "png"], check=True, capture_output=True)
    return Image.open(out).convert("RGBA")


def place(rgba, H=880):
    a = rgba.crop(rgba.getbbox()); s = H / a.height
    if a.width * s > 980: s = 980 / a.width
    a = a.resize((round(a.width * s), round(a.height * s)), Image.LANCZOS)
    cv = Image.new("RGBA", (1024, 1024), (255, 255, 255, 255)); cv.alpha_composite(a, ((1024 - a.width) // 2, 1024 - 40 - a.height))
    return cv.convert("RGB")


def main():
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True); tmp = O / "_lora_tmp"; tmp.mkdir(exist_ok=True)
    items = []
    # 1) reference (+ mirrored) -- upscale 4x first (555x640 source)
    r = upscale(REF, tmp / "ref_up.png")
    items += [(r, "standing, holding staff, front view"), (r.transpose(Image.FLIP_LEFT_RIGHT), "standing, holding staff, front view")]
    # 2) v1 rig frames: identical staff/orb as the reference (cells 420x500 -> upscale)
    st = Image.open(O / "mage_anim/final/mage_nam_strip_2520x500.png").convert("RGBA")
    for i in range(6):
        c = st.crop((i * 420, 0, (i + 1) * 420, 500)); p = tmp / f"v1_{i}.png"; c.save(p)
        items.append((upscale(p, tmp / f"v1_{i}_up.png"), V1_POSE[i]))
    for k, cap in (("skill_charge", "charging magic, staff raised, magic aura"), ("skill_release", "unleashing a spell, staff forward, magic blast")):
        items.append((upscale(O / f"mage_anim/final/mage_nam_{k}_420x500.png", tmp / f"v1_{k}_up.png"), cap))
    # 3) v2 picked frames (already matted, 768x1024 source) + extra v2 male generations of seed 741001 (matted here)
    for k, cap in V2_POSE.items():
        f = O / f"mage_v2_final/_matte_male_{k}_raw.png"
        if f.exists(): items.append((Image.open(f).convert("RGBA"), cap))
    for k in ("run", "run2", "cast1", "cast2", "skill_release"):
        f = O / f"mage_v2c/raw_male_{k}_s741001_ip60.png"
        if f.exists(): items.append((cm.matte(f), V2_POSE[k]))
    for f_ in out.glob("*"): f_.unlink()
    meta = []
    for i, (im, cap) in enumerate(items):
        place(im).save(out / f"{i:03d}.png")
        txt = f"{BASE_CAP}, {cap}, {TAIL}"; (out / f"{i:03d}.txt").write_text(txt, encoding="utf-8"); meta.append(txt)
    (O / "lora_dataset_captions.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")
    print(len(items), "images")


if __name__ == "__main__":
    main()
