"""Step B pilot: Kiếm Sĩ Nam turnaround (Animagine) + 3 locked poses with ControlNet OpenPose (xinsir),
SDXL Base vs Animagine on the same prompt / seed / sampler. Native ComfyUI nodes only.
Skeletons drawn with xinsir's recommended thick lines (stickwidth 4 * ratio 3 at 1024 px).
Usage: python pilot_animagine_openpose.py <out_dir>
"""
import sys, json, math, time, threading, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
sys.path.insert(0, str(Path(__file__).parent))
import comfy_api as c

BASE = "sd_xl_base_1.0.safetensors"
ANIM = "animagine-xl-4.0-opt.safetensors"
CN = "controlnet-openpose-sdxl-xinsir.safetensors"
SEED = 730001
STEPS, CFG, SAMPLER, SCHED = 28, 5.0, "euler_ancestral", "normal"   # Animagine 4.0 recommended settings

CHAR = ("1boy, solo, chibi, knight, light blue hair, blue eyes, steel helmet with red plume, silver plate armor, "
        "red cape, brown boots")
TAIL = ("full body, from slightly above, simple background, plain light grey background, "
        "masterpiece, high score, great score, absurdres")
NEG = ("lowres, bad anatomy, bad hands, extra digits, fewer digits, extra arms, extra legs, text, error, cropped, "
       "worst quality, low quality, low score, bad score, average score, signature, watermark, username, blurry, "
       "multiple views, scenery")
POSES = {
    "a_dung_huong_xuong": "standing, facing viewer, holding sword at side, neutral pose",
    "b_skill_kiem": "attacking, raising sword overhead with both hands, dynamic pose, wide stance, holding sword",
    "c_trung_don": "hurt, recoiling backwards, knocked back, arms flung out, leaning back, pained expression, holding sword",
}
TURN_POS = (f"{CHAR}, character turnaround, reference sheet, multiple views, front view, side view, back view, "
            f"standing, holding sword, full body, simple background, plain light grey background, "
            f"masterpiece, high score, great score, absurdres")
TURN_NEG = NEG.replace(", multiple views", "")

# OpenPose COCO-18 keypoints, chibi proportions (big head, short limbs), 1024x1024 canvas.
# Order: nose, neck, Rsho, Relb, Rwri, Lsho, Lelb, Lwri, Rhip, Rknee, Rank, Lhip, Lknee, Lank, Reye, Leye, Rear, Lear.
# Character faces the viewer, so its right side is image left.
KP = {
    "a_dung_huong_xuong": [(512, 330), (512, 470), (420, 500), (395, 600), (385, 690), (604, 500), (629, 600), (639, 690),
                           (462, 680), (455, 800), (450, 915), (562, 680), (569, 800), (574, 915),
                           (472, 300), (552, 300), (412, 315), (612, 315)],
    "b_skill_kiem": [(500, 360), (505, 495), (415, 520), (420, 400), (470, 300), (595, 520), (600, 405), (540, 300),
                     (455, 700), (380, 800), (340, 915), (555, 700), (630, 800), (675, 915),
                     (462, 330), (540, 330), (402, 345), (600, 345)],
    "c_trung_don": [(560, 330), (530, 470), (440, 490), (345, 450), (265, 420), (620, 500), (700, 470), (785, 430),
                    (480, 690), (440, 800), (470, 915), (580, 690), (640, 790), (700, 880),
                    (525, 295), (600, 300), (468, 300), (650, 320)],
}
LIMBS = [(2, 3), (2, 6), (3, 4), (4, 5), (6, 7), (7, 8), (2, 9), (9, 10), (10, 11), (2, 12), (12, 13), (13, 14),
         (2, 1), (1, 15), (15, 17), (1, 16), (16, 18)]
COLORS = [(255, 0, 0), (255, 85, 0), (255, 170, 0), (255, 255, 0), (170, 255, 0), (85, 255, 0), (0, 255, 0), (0, 255, 85),
          (0, 255, 170), (0, 255, 255), (0, 170, 255), (0, 85, 255), (0, 0, 255), (85, 0, 255), (170, 0, 255),
          (255, 0, 255), (255, 0, 170), (255, 0, 85)]
STICK = 4 * 3   # xinsir: stickwidth 4 * ratio 3 for 1000 <= max(W,H) < 2000
DOT = 4 * 3


def draw_pose(kp, size=1024):
    im = Image.new("RGB", (size, size), (0, 0, 0)); d = ImageDraw.Draw(im)
    for (a, b), col in zip(LIMBS, COLORS):
        (x1, y1), (x2, y2) = kp[a - 1], kp[b - 1]
        mx, my, L = (x1 + x2) / 2, (y1 + y2) / 2, math.hypot(x2 - x1, y2 - y1) / 2
        ang = math.atan2(y2 - y1, x2 - x1)
        pts = [(mx + L * math.cos(t) * math.cos(ang) - STICK * math.sin(t) * math.sin(ang),
                my + L * math.cos(t) * math.sin(ang) + STICK * math.sin(t) * math.cos(ang))
               for t in np.linspace(0, 2 * math.pi, 72)]
        d.polygon(pts, fill=tuple(int(v * 0.6) for v in col))
    for (x, y), col in zip(kp, COLORS):
        d.ellipse([x - DOT, y - DOT, x + DOT, y + DOT], fill=col)
    return im


def wf(ckpt, pos, neg, seed, w=1024, h=1024, pose_name=None, strength=1.0):
    g = c.txt2img(pos, neg, seed, w=w, h=h, steps=STEPS, cfg=CFG)
    g["1"]["inputs"]["ckpt_name"] = ckpt
    g["5"]["inputs"].update(sampler_name=SAMPLER, scheduler=SCHED)
    g["7"]["inputs"]["filename_prefix"] = "game_art_core/pilot_b"
    if pose_name:
        g["10"] = {"class_type": "ControlNetLoader", "inputs": {"control_net_name": CN}}
        g["11"] = {"class_type": "LoadImage", "inputs": {"image": pose_name}}
        g["12"] = {"class_type": "ControlNetApplyAdvanced", "inputs": {
            "positive": ["2", 0], "negative": ["3", 0], "control_net": ["10", 0], "image": ["11", 0],
            "strength": strength, "start_percent": 0.0, "end_percent": 1.0, "vae": ["1", 2]}}
        g["5"]["inputs"]["positive"] = ["12", 0]; g["5"]["inputs"]["negative"] = ["12", 1]
    return g


class VramPeak:
    def __enter__(self):
        self.peak, self.stop = 0, False
        def loop():
            while not self.stop:
                try:
                    v = int(subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                                           capture_output=True, text=True, timeout=5).stdout.strip())
                    self.peak = max(self.peak, v)
                except Exception:
                    pass
                time.sleep(0.5)
        self.t = threading.Thread(target=loop, daemon=True); self.t.start(); return self

    def __exit__(self, *a):
        self.stop = True; self.t.join()


def job(out, name, g, log):
    with VramPeak() as v:
        _, sec = c.run(g, out / f"{name}.png", timeout=1800)
    log[name] = {"seconds": sec, "vram_peak_mib_total_gpu": v.peak}
    print(name, log[name], flush=True)


if __name__ == "__main__":
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    log = {"settings": {"seed": SEED, "steps": STEPS, "cfg": CFG, "sampler": SAMPLER, "scheduler": SCHED,
                        "controlnet": CN, "cn_strength": 1.0, "stickwidth_px": STICK, "dot_radius_px": DOT,
                        "char_prompt": CHAR, "tail": TAIL, "negative": NEG, "poses": POSES, "turnaround_prompt": TURN_POS},
           "jobs": {}}
    for k, kp in KP.items():
        draw_pose(kp).save(out / f"pose_{k}.png")
    # 1) turnaround reference, both models, same seed
    for tag, ck in (("animagine", ANIM), ("sdxl_base", BASE)):
        job(out, f"turnaround_{tag}", wf(ck, TURN_POS, TURN_NEG, SEED, w=1344, h=768), log["jobs"])
    # 2) three locked poses, both models, same prompt / seed
    for k, desc in POSES.items():
        name = c.upload(out / f"pose_{k}.png")
        for tag, ck in (("animagine", ANIM), ("sdxl_base", BASE)):
            job(out, f"{k}_{tag}", wf(ck, f"{CHAR}, {desc}, {TAIL}", NEG, SEED, pose_name=name), log["jobs"])
    (out / "pilot_log.json").write_text(json.dumps(log, indent=1, ensure_ascii=False), encoding="utf-8")
