"""Pilot follow-up: turnaround locked by a 3-view chibi OpenPose sheet (front / side / back), open-face helmet prompt.
Usage: python pilot_turnaround_v2.py <out_dir>"""
import sys, json, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).parent))
import comfy_api as c
import pilot_animagine_openpose as p

CHAR2 = p.CHAR.replace("steel helmet with red plume", "open-face steel helmet with red plume, visible face")
POS = (f"{CHAR2}, character turnaround, reference sheet, three views, front view, side view, back view, standing, "
       f"holding sword, full body, simple background, plain light grey background, masterpiece, high score, great score, absurdres")
NEG = p.NEG.replace(", multiple views", "") + ", closed helmet, visor, tall, realistic proportions"
W, H = 1344, 768


def draw(views):
    im = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(im)
    for kp in views:
        for (a, b), col in zip(p.LIMBS, p.COLORS):
            if kp[a - 1] is None or kp[b - 1] is None: continue
            (x1, y1), (x2, y2) = kp[a - 1], kp[b - 1]
            mx, my, L = (x1 + x2) / 2, (y1 + y2) / 2, math.hypot(x2 - x1, y2 - y1) / 2
            ang = math.atan2(y2 - y1, x2 - x1); s = p.STICK
            d.polygon([(mx + L * math.cos(t) * math.cos(ang) - s * math.sin(t) * math.sin(ang),
                        my + L * math.cos(t) * math.sin(ang) + s * math.sin(t) * math.cos(ang)) for t in np.linspace(0, 2 * math.pi, 72)],
                      fill=tuple(int(v * 0.6) for v in col))
        for pt, col in zip(kp, p.COLORS):
            if pt is None: continue
            d.ellipse([pt[0] - p.DOT, pt[1] - p.DOT, pt[0] + p.DOT, pt[1] + p.DOT], fill=col)
    return im


def place(kp, cx, scale=0.75, top=20):
    return [None if q is None else (cx + (q[0] - 512) * scale, top + (q[1] - 250) * scale) for q in kp]


front = p.KP["a_dung_huong_xuong"]
side = [(560, 335), (505, 470), (500, 500), (520, 600), (545, 690), (510, 500), (530, 600), (555, 690),
        (500, 680), (505, 800), (505, 915), (510, 680), (515, 800), (520, 915),
        None, (540, 300), None, (490, 315)]                       # facing image right: one eye, one ear
back = [None, (512, 470), (604, 500), (629, 600), (639, 690), (420, 500), (395, 600), (385, 690),
        (562, 680), (569, 800), (574, 915), (462, 680), (455, 800), (450, 915), None, None, None, None]
if __name__ == "__main__":
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    draw([place(front, 230), place(side, 672), place(back, 1114)]).save(out / "pose_turnaround_3view.png")
    name = c.upload(out / "pose_turnaround_3view.png")
    log = {"prompt": POS, "negative": NEG, "seed": p.SEED, "jobs": {}}
    for tag, ck in (("animagine", p.ANIM), ("sdxl_base", p.BASE)):
        p.job(out, f"turnaround_v2_openpose_{tag}", p.wf(ck, POS, NEG, p.SEED, w=W, h=H, pose_name=name), log["jobs"])
    (out / "pilot_turnaround_v2_log.json").write_text(json.dumps(log, indent=1, ensure_ascii=False), encoding="utf-8")
