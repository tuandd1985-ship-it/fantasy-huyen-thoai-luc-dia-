"""Pháp Sư strip v2: Animagine XL 4.0 + ControlNet OpenPose (xinsir) + IP-Adapter Plus SDXL (identity from the cleaned
reference). One character per generation, white background, 768x1024. 3/4 view facing right (game flips for left).
Usage: python gen_mage_v2.py <out_dir> <cleaned_png_dir> [male|female ...] [--poses=a,b] [--seeds=1,2] [--ipw=0.7]
"""
import sys, json, math, time
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).parent))
import comfy_api as c
import pilot_animagine_openpose as p

import os as _os
W, H = 768, int(_os.environ.get("MAGE_H", "1024"))
STEPS, CFG = 30, 5.0
CHAR = {
    "male": ("1boy, solo, chibi, young wizard, dark blue messy hair, blue eyes, (small white goatee beard:1.3), wide-brimmed pointed dark "
             "blue wizard hat with gold trim and crescent moon, dark blue wizard robe and cape with gold embroidery, brown belt "
             "with gold star buckle, brown boots, gnarled brown wooden staff with a glowing blue crystal orb mounted on top of the staff"),
    "female": ("1girl, solo, chibi, long wavy lavender purple hair, purple eyes, diamond crystal hair clip, no hat, teal and blue "
               "wizard robe with silver trim and crescent moons, purple dress, purple boots, brown wooden staff with silver blade "
               "ornament and a glowing purple crystal orb mounted on top of the staff, holding the staff in one hand"),
}
TAIL = ("full body, face clearly visible, three-quarter view facing right, thick clean outline, cel shading, "
        "simple background, white background, masterpiece, high score, great score, absurdres")
NEG = ("closed helmet, visor, face covered, mask, multiple characters, overlapping figures, 2boys, 2girls, multiple views, "
       "reference sheet, cropped, out of frame, lowres, bad anatomy, bad hands, extra arms, extra legs, two staffs, extra staff, "
       "text, watermark, signature, worst quality, low quality, low score, bad score, blurry, scenery, ground, shadow, "
       "gradient background, dark background, floating orb, detached orb, orb above head, halo, giant orb, floating crystal, magic swirl, swirling ribbon, crescent moon behind head, "
       "bubble, wind effect, sparkle trail, aura, magic circle behind")
POSE_TXT = {
    "idle": "standing calmly, holding staff upright beside body, gentle smile",
    "run": "running fast, body leaning forward, cape and robe flowing behind, staff trailing behind in one hand, dynamic motion",
    "run2": "running fast, mid stride, body leaning forward, cape flowing behind, staff trailing behind, dynamic motion",
    "cast1": "winding up a spell, leaning back, staff pulled back behind the body, small glowing orb, focused face",
    "cast2": "thrusting staff forward with arm fully extended, leaning forward, large bright glowing orb, magic burst at the orb",
    "skill_charge": "charging a spell, staff raised high above head with both hands, bright glowing orb on the staff, determined",
    "skill_release": "lunging forward unleashing a spell, staff pointed forward with extended arms, bright glowing orb on the staff, cape flying",
}
# chibi proportions measured on the cleaned reference (feet y ~965, height ~860): eyes 550, nose 590, neck 645,
# shoulders 665, hips 820. 3/4 view facing right: face shifted right, far ear hidden.
X = 370


def kp(lean=0, nose_dx=22, arms=None, legs=None, dy=0):
    nx, ny = X + lean + nose_dx, 590 + dy; neck = (X + lean * 0.7, 645 + dy)
    rs, ls = (neck[0] - 70, 668 + dy), (neck[0] + 70, 668 + dy)
    re, rw, le, lw = arms
    rh, lh = (X - 38, 820), (X + 38, 820)
    rk, ra, lk, la = legs or ((X - 40, 890), (X - 42, 962), (X + 40, 890), (X + 42, 962))
    eyes = [(nx - 50, 552 + dy), (nx + 62, 552 + dy)]
    ears = [(nx - 135, 568 + dy), None]
    return [(nx, ny), neck, rs, re, rw, ls, le, lw, rh, rk, ra, lh, lk, la, eyes[0], eyes[1], ears[0], ears[1]]


POSES = {
    "idle": kp(arms=((X - 90, 728), (X - 98, 778), (X + 110, 700), (X + 140, 735))),
    "run": kp(lean=55, arms=((X - 60, 720), (X - 150, 760), (X + 175, 640), (X + 215, 600)),
              legs=((X + 30, 870), (X + 120, 900), (X - 70, 900), (X - 160, 920))),
    "run2": kp(lean=50, dy=-14, arms=((X - 40, 735), (X - 130, 790), (X + 150, 660), (X + 190, 640)),
               legs=((X - 20, 885), (X - 70, 950), (X + 60, 870), (X + 70, 935))),
    "cast1": kp(lean=-45, arms=((X - 150, 640), (X - 230, 590), (X + 110, 705), (X + 165, 700)),
                legs=((X - 70, 890), (X - 110, 962), (X + 50, 890), (X + 90, 962))),
    "cast2": kp(lean=50, arms=((X - 100, 700), (X - 160, 730), (X + 200, 650), (X + 300, 635)),
                legs=((X - 70, 885), (X - 140, 955), (X + 70, 880), (X + 130, 955))),
    "skill_charge": kp(arms=((X - 125, 590), (X - 70, 480), (X + 160, 590), (X + 90, 480)),
                       legs=((X - 60, 888), (X - 95, 962), (X + 60, 888), (X + 95, 962))),
    "skill_release": kp(lean=70, arms=((X + 110, 690), (X + 230, 660), (X + 210, 650), (X + 320, 620)),
                        legs=((X - 90, 880), (X - 180, 950), (X + 90, 875), (X + 160, 955))),
}
import os
SKEL_SCALE, FEET = float(os.environ.get("MAGE_SKEL", "0.82")), (X, 965)     # shrink around the feet so the big chibi head + hat fit with margin
_DY = H - 1024 - (10 if H < 1024 else 0)   # shorter canvas: move the skeleton up so the head sits near the top
POSES = {k: [None if q is None else (FEET[0] + (q[0] - FEET[0]) * SKEL_SCALE + 14, FEET[1] + (q[1] - FEET[1]) * SKEL_SCALE + _DY)
             for q in v] for k, v in POSES.items()}
LIMBS, COLORS = p.LIMBS, p.COLORS


def pose_img(name):
    im = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(im); pts = POSES[name]
    for (a, b), col in zip(LIMBS, COLORS):
        if pts[a - 1] is None or pts[b - 1] is None: continue
        (x1, y1), (x2, y2) = pts[a - 1], pts[b - 1]
        mx, my, L = (x1 + x2) / 2, (y1 + y2) / 2, math.hypot(x2 - x1, y2 - y1) / 2
        ang = math.atan2(y2 - y1, x2 - x1); s = p.STICK
        d.polygon([(mx + L * math.cos(t) * math.cos(ang) - s * math.sin(t) * math.sin(ang),
                    my + L * math.cos(t) * math.sin(ang) + s * math.sin(t) * math.cos(ang)) for t in np.linspace(0, 2 * math.pi, 72)],
                  fill=tuple(int(v * 0.6) for v in col))
    for pt, col in zip(pts, COLORS):
        if pt is None: continue
        d.ellipse([pt[0] - p.DOT, pt[1] - p.DOT, pt[0] + p.DOT, pt[1] + p.DOT], fill=col)
    return im


# identity reference WITHOUT the staff/orb (body layer split from the cleaned reference in mage-anim v1), so IP-Adapter
# learns face/hair/hat/robe only and does not copy the big orb into the composition
REF_BODY = {"male": Path(r"C:/AI/GAME-ART-CORE/output/mage_anim/rig/seed0/male_body.png"),
            "female": Path(r"C:/AI/GAME-ART-CORE/output/mage_anim/rig_f/seed0/female_body.png")}


def ref_square(png):
    r = Image.open(png).convert("RGBA"); r = r.crop(r.getbbox())
    s = 900 / max(r.size); r = r.resize((round(r.width * s), round(r.height * s)), Image.LANCZOS)
    cv = Image.new("RGBA", (1024, 1024), (255, 255, 255, 255)); cv.alpha_composite(r, ((1024 - r.width) // 2, (1024 - r.height) // 2))
    return cv.convert("RGB")


def wf(gender, pose, seed, ref_name, pose_name, ipw):
    pos = f"{CHAR[gender]}, {POSE_TXT[pose]}, {TAIL}"
    g = p.wf(p.ANIM, pos, NEG, seed, w=W, h=H, pose_name=pose_name)
    g["7"]["inputs"]["filename_prefix"] = "game_art_core/mage_v2"
    g["5"]["inputs"]["steps"] = STEPS
    g["20"] = {"class_type": "IPAdapterUnifiedLoader", "inputs": {"model": ["1", 0], "preset": "PLUS (high strength)"}}
    g["21"] = {"class_type": "LoadImage", "inputs": {"image": ref_name}}
    g["22"] = {"class_type": "IPAdapterAdvanced", "inputs": {"model": ["20", 0], "ipadapter": ["20", 1], "image": ["21", 0],
                                                            "weight": ipw, "weight_type": "linear", "combine_embeds": "concat",
                                                            "start_at": 0.0, "end_at": 0.8, "embeds_scaling": "V only"}}
    g["5"]["inputs"]["model"] = ["22", 0]
    return g, pos


if __name__ == "__main__":
    out = Path(sys.argv[1]); cdir = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True); args = sys.argv[3:]
    genders = [a for a in args if a in CHAR] or ["male", "female"]
    poses = next((a.split("=")[1].split(",") for a in args if a.startswith("--poses=")), list(POSES))
    seeds = next(([int(x) for x in a.split("=")[1].split(",")] for a in args if a.startswith("--seeds=")), [741001])
    ipws = next(([float(x) for x in a.split("=")[1].split(",")] for a in args if a.startswith("--ipw=")), [0.7])
    logf = out / "gen_log.json"; log = json.loads(logf.read_text(encoding="utf-8")) if logf.exists() else {}
    for gd in genders:
        refsrc = REF_BODY.get(gd) if REF_BODY.get(gd) and REF_BODY[gd].exists() else cdir / f"hero-mage-{gd}.png"
        rp = out / f"_ref_{gd}.png"; ref_square(refsrc).save(rp); ref_name = c.upload(rp)
        for ps in poses:
            pp = out / f"_pose_{ps}.png"; pose_img(ps).save(pp); pose_name = c.upload(pp)
            for sd in seeds:
                for ipw in ipws:
                    tag = f"{gd}_{ps}_s{sd}_ip{int(ipw * 100)}"
                    g, pos = wf(gd, ps, sd, ref_name, pose_name, ipw)
                    _, t = c.run(g, out / f"raw_{tag}.png", timeout=1800)
                    log[tag] = {"gender": gd, "pose": ps, "seed": sd, "model": p.ANIM, "controlnet": p.CN, "cn_strength": 1.0,
                                "ipadapter": "ip-adapter-plus_sdxl_vit-h + CLIP-ViT-H-14 (PLUS high strength)", "ip_weight": ipw,
                                "ip_weight_type": "linear", "ip_end_at": 0.8, "ip_reference": "body layer without staff (art-tests/mage-anim/rig/)", "steps": STEPS, "cfg": CFG, "sampler": "euler_ancestral/normal",
                                "size": [W, H], "prompt": pos, "negative": NEG, "seconds": t,
                                "reference": f"art-tests/hero-edge-clean/cleaned_png/hero-mage-{gd}.png"}
                    print(tag, t, flush=True)
                    logf.write_text(json.dumps(log, indent=1, ensure_ascii=False), encoding="utf-8")
