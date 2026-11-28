"""Pháp Sư motion strip (k15/k16 replacement): Animagine XL 4.0 + ControlNet OpenPose (xinsir), native nodes only.
Identity without IP-Adapter: in-context panel. Canvas 1536x1024 = [reference 768 | new pose 768]; the left half is the
cleaned reference sprite on white and is kept by SetLatentNoiseMask, only the right half is generated (one character),
OpenPose skeleton drawn on the right half only. Output = right half.
Usage: python gen_mage_anim.py <out_dir> <ref_male.png> <ref_female.png> [gender ...] [--poses a,b] [--seeds 1,2]
"""
import sys, json, math, time
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).parent))
import comfy_api as c
import pilot_animagine_openpose as p

W, H, HALF = 1536, 1024, 768
STEPS, CFG = 28, 5.0
CHAR = {
    "male": ("1boy, solo, chibi, young wizard, dark blue messy hair, blue eyes, small white goatee, "
             "wide-brimmed pointed dark blue wizard hat with gold trim and crescent moon and star symbols, "
             "dark blue wizard robe with gold embroidery, brown belt with gold star buckle, brown boots, "
             "gnarled brown wooden staff with glowing blue crystal orb on top"),
    "female": ("1girl, solo, chibi, long wavy lavender purple hair, purple eyes, smile, diamond crystal hair clip, no hat, "
               "teal and blue wizard robe with silver trim and crescent moon symbols, purple dress, purple boots, "
               "brown wooden staff with silver blade ornament and large glowing purple crystal orb on top"),
}
TAIL = ("full body, face clearly visible, cute, thick clean outline, cel shading, simple background, white background, "
        "masterpiece, high score, great score, absurdres")
NEG = ("closed helmet, visor, face covered, mask, multiple characters, overlapping figures, 2boys, 2girls, multiple views, "
       "reference sheet, cropped, out of frame, lowres, bad anatomy, bad hands, extra arms, extra legs, extra staff, "
       "two staffs, text, watermark, signature, worst quality, low quality, low score, bad score, blurry, scenery, "
       "ground shadow, gradient background")
POSE_TXT = {
    "idle": "standing, holding staff upright at side, relaxed, calm smile",
    "run1": "running, dynamic running pose, left leg forward, robe flowing, holding staff",
    "run2": "running, dynamic running pose, right leg forward, robe flowing, holding staff",
    "cast1": "casting spell, raising staff high above head with one hand, glowing orb, magic sparkles",
    "cast2": "casting spell, thrusting staff forward, magic blast from orb, other hand stretched out",
    "skill_charge": "charging powerful magic, holding staff overhead with both hands, glowing aura, swirling magic energy, determined face",
    "skill_release": "unleashing spell, leaning forward, pointing staff forward, huge magic burst from orb, open hand forward, cape flowing",
}

# Chibi skeletons measured on the cleaned reference sprites placed by ref_canvas (feet y 965, height 860, centre x ~385):
# eyes y 550 (+-73), ears 565 (+-150), nose 590, neck 645, shoulders 665 (+-85), hips 820 (+-45), ankles 960.
# COCO-18 order: nose, neck, Rsho, Relb, Rwri, Lsho, Lelb, Lwri, Rhip, Rknee, Rank, Lhip, Lknee, Lank, Reye, Leye, Rear, Lear.
# The character faces the viewer: its right = image left; staff in its left hand (image right) as in the reference.
CX = 385

def kp(dx=0, arms=None, legs=None, lean=0):
    x = CX + dx
    hx = x + lean
    face = [(hx, 590), (x, 645)]
    sh = [(x - 85, 665), (x + 85, 665)]
    (re, rw, le, lw) = arms or ((x - 105, 725), (x - 115, 775), (x + 120, 680), (x + 148, 710))
    (rk, ra, lk, la) = legs or ((x - 45, 890), (x - 48, 960), (x + 45, 890), (x + 48, 960))
    pts = [face[0], face[1], sh[0], re, rw, sh[1], le, lw, (x - 45, 820), rk, ra, (x + 45, 820), lk, la,
           (hx - 73, 550), (hx + 73, 550), (hx - 150, 565), (hx + 150, 565)]
    return pts

X = CX
POSES = {
    "idle": kp(),
    "run1": kp(lean=12, arms=((X - 125, 700), (X - 95, 650), (X + 120, 680), (X + 150, 705)),
               legs=((X - 70, 880), (X - 110, 935), (X + 55, 875), (X + 95, 955))),
    "run2": kp(lean=12, arms=((X - 120, 735), (X - 150, 770), (X + 115, 690), (X + 140, 720)),
               legs=((X - 40, 880), (X - 15, 960), (X + 70, 880), (X + 120, 930))),
    "cast1": kp(arms=((X - 135, 690), (X - 180, 690), (X + 130, 600), (X + 140, 520))),
    "cast2": kp(lean=10, arms=((X - 110, 720), (X - 135, 765), (X + 150, 665), (X + 225, 650)),
                legs=((X - 60, 885), (X - 85, 960), (X + 50, 885), (X + 70, 960))),
    "skill_charge": kp(arms=((X - 135, 600), (X - 120, 515), (X + 135, 600), (X + 120, 515)),
                       legs=((X - 60, 888), (X - 80, 962), (X + 60, 888), (X + 80, 962))),
    "skill_release": kp(dx=-15, lean=20, arms=((X + 10, 700), (X + 120, 690), (X + 150, 660), (X + 240, 640)),
                        legs=((X - 85, 880), (X - 130, 955), (X + 60, 880), (X + 95, 960))),
}


def pose_canvas(name):
    im = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(im)
    pts = [(x + HALF, y) for x, y in POSES[name]]
    for (a, b), col in zip(p.LIMBS, p.COLORS):
        (x1, y1), (x2, y2) = pts[a - 1], pts[b - 1]
        mx, my, L = (x1 + x2) / 2, (y1 + y2) / 2, math.hypot(x2 - x1, y2 - y1) / 2
        ang = math.atan2(y2 - y1, x2 - x1); s = p.STICK
        d.polygon([(mx + L * math.cos(t) * math.cos(ang) - s * math.sin(t) * math.sin(ang),
                    my + L * math.cos(t) * math.sin(ang) + s * math.sin(t) * math.cos(ang)) for t in np.linspace(0, 2 * math.pi, 72)],
                  fill=tuple(int(v * 0.6) for v in col))
    for (x, y), col in zip(pts, p.COLORS):
        d.ellipse([x - p.DOT, y - p.DOT, x + p.DOT, y + p.DOT], fill=col)
    return im


def ref_canvas(ref_png):
    """Reference on white in the left half (feet at y 965, height 860), right half transparent = repaint."""
    ref = Image.open(ref_png).convert("RGBA"); ref = ref.crop(ref.getbbox())
    s = 860 / ref.height; ref = ref.resize((round(ref.width * s), 860), Image.LANCZOS)
    cv = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    cv.alpha_composite(ref, (HALF // 2 - ref.width // 2, 965 - 860))
    a = np.asarray(cv).copy(); a[:, HALF:, 3] = 0
    return Image.fromarray(a)


def wf_t2i(gender, pose, seed, pose_name):
    """Single character per generation: 768x1024 txt2img + OpenPose (skeleton = right panel coords)."""
    pos = f"{CHAR[gender]}, {POSE_TXT[pose]}, {TAIL}"
    g = p.wf(p.ANIM, pos, NEG, seed, w=HALF, h=H, pose_name=pose_name)
    g["7"]["inputs"]["filename_prefix"] = "game_art_core/mage_anim"
    return g, pos


def wf_i2i(gender, pose, seed, init_name, pose_name, denoise):
    """img2img from the cleaned reference sprite on white (identity), OpenPose bends the limbs."""
    pos = f"{CHAR[gender]}, {POSE_TXT[pose]}, {TAIL}"
    g = p.wf(p.ANIM, pos, NEG, seed, w=HALF, h=H, pose_name=pose_name)
    g["7"]["inputs"]["filename_prefix"] = "game_art_core/mage_anim"
    g["8"] = {"class_type": "LoadImage", "inputs": {"image": init_name}}
    g["9"] = {"class_type": "VAEEncode", "inputs": {"pixels": ["8", 0], "vae": ["1", 2]}}
    g["5"]["inputs"]["latent_image"] = ["9", 0]; g["5"]["inputs"]["denoise"] = denoise
    g.pop("4", None)
    return g, pos


def wf(gender, pose, seed, ref_name, pose_name):
    pos = f"{CHAR[gender]}, {POSE_TXT[pose]}, {TAIL}"
    g = c.base(pos, NEG, seed, steps=STEPS, cfg=CFG)
    g["1"]["inputs"]["ckpt_name"] = p.ANIM
    g["5"]["inputs"].update(sampler_name="euler_ancestral", scheduler="normal", denoise=1.0)
    g["7"]["inputs"]["filename_prefix"] = "game_art_core/mage_anim"
    g["8"] = {"class_type": "LoadImage", "inputs": {"image": ref_name}}
    g["9"] = {"class_type": "VAEEncode", "inputs": {"pixels": ["8", 0], "vae": ["1", 2]}}
    g["4"] = {"class_type": "SetLatentNoiseMask", "inputs": {"samples": ["9", 0], "mask": ["8", 1]}}
    g["10"] = {"class_type": "ControlNetLoader", "inputs": {"control_net_name": p.CN}}
    g["11"] = {"class_type": "LoadImage", "inputs": {"image": pose_name}}
    g["12"] = {"class_type": "ControlNetApplyAdvanced", "inputs": {"positive": ["2", 0], "negative": ["3", 0], "control_net": ["10", 0],
                                                                  "image": ["11", 0], "strength": 1.0, "start_percent": 0.0,
                                                                  "end_percent": 1.0, "vae": ["1", 2]}}
    g["5"]["inputs"]["positive"] = ["12", 0]; g["5"]["inputs"]["negative"] = ["12", 1]
    return g, pos


if __name__ == "__main__":
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    refs = {"male": sys.argv[2], "female": sys.argv[3]}
    args = sys.argv[4:]
    genders = [a for a in args if a in refs] or ["male", "female"]
    poses = next((a.split("=")[1].split(",") for a in args if a.startswith("--poses=")), list(POSES))
    seeds = next(([int(x) for x in a.split("=")[1].split(",")] for a in args if a.startswith("--seeds=")), [731001])
    logf = out / "gen_log.json"; log = json.loads(logf.read_text(encoding="utf-8")) if logf.exists() else {}
    dens = next(([float(x) for x in a.split("=")[1].split(",")] for a in args if a.startswith("--denoise=")), [0.65])
    for gd in genders:
        init = out / f"_init_{gd}.png"
        rc = ref_canvas(refs[gd]).crop((0, 0, HALF, H)); bg = Image.new("RGB", rc.size, "white"); bg.paste(rc, mask=rc.split()[3]); bg.save(init)
        init_name = c.upload(init)
        for ps in poses:
            pc = out / f"_pose1_{ps}.png"
            pose_canvas(ps).crop((HALF, 0, W, H)).save(pc)
            pose_name = c.upload(pc)
            for sd in seeds:
              for dn in dens:
                g, pos = wf_i2i(gd, ps, sd, init_name, pose_name, dn)
                tag = f"{gd}_{ps}_s{sd}_d{int(dn * 100)}"
                _, t = c.run(g, out / f"raw_{tag}.png", timeout=1800)
                log[tag] = {"denoise": dn, "init": "cleaned reference sprite on white, feet y 965, height 860","model": p.ANIM, "controlnet": p.CN, "seed": sd, "steps": STEPS, "cfg": CFG,
                                          "sampler": "euler_ancestral/normal", "cn_strength": 1.0, "prompt": pos, "negative": NEG,
                                          "method": "img2img from cleaned reference + ControlNet OpenPose, one character per generation", "size": [HALF, H],
                                          "seconds": t}
                print(tag, t, flush=True)
                logf.write_text(json.dumps(log, indent=1, ensure_ascii=False), encoding="utf-8")
