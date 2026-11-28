"""Motions for Codex monster wave 2 (rotations in degrees, + = clockwise on screen)."""
import json
from pathlib import Path
from gen_monster_motions import loop, once, hurt

M = {}
# ---- Nhen Doc / Nhen Chua: tetrapod gait (two alternating groups of four legs) ----
A = ["leg_r_far_1", "leg_l_far_2", "leg_r_near_2", "leg_l_near_1"]
Bg = ["leg_l_far_1", "leg_r_far_2", "leg_l_near_2", "leg_r_near_1"]
def legs(group, amt):
    return {n: (amt if n.startswith("leg_r") else -amt) for n in group}
for sid, big in (("spider", 1.0), ("spiderQueen", 0.8)):
    up_a = dict(legs(A, 12 * big), **legs(Bg, -4 * big)); up_b = dict(legs(Bg, 12 * big), **legs(A, -4 * big))
    M[sid] = {"ground": ["leg_r_near_2", "leg_l_near_2", "leg_r_near_1", "leg_l_near_1"], "actions": {
        "idle": loop(450, [{}, dict(legs(A + Bg, 2), head=2)], [[0, 0], [0, 3]]),
        "move": loop(80, [up_a, {}, up_b, {}], [[0, -3], [0, 0], [0, -3], [0, 0]]),
        "attack": once([{"t": 0, "rot": {}},
                        {"t": 160, "rot": dict(legs(["leg_r_far_1", "leg_l_far_1"], 30), head=-8, body=-4), "root": [-6, -14]},
                        {"t": 270, "rot": dict(legs(["leg_r_far_1", "leg_l_far_1"], -16), head=10, body=5), "root": [14, 6]},
                        {"t": 420, "rot": {"head": 5, "body": 2}, "root": [8, 0]}, {"t": 580, "rot": {}}], [80, 100, 70, 130, 120, 100], 3),
        "hurt": hurt(dict(legs(A + Bg, 10), head=-10, body=-6))}}
# ---- Golem Bang / Golem Dung Nham: heavy stomp ----
for gid in ("iceGolem", "magmaGolem"):
    w1 = {"leg_r": 10, "leg_l": -6, "arm_r": -8, "arm_l": -6, "body": -2, "head": 2}
    w2 = {"leg_r": -6, "leg_l": 10, "arm_r": 6, "arm_l": 8, "body": 2, "head": -2}
    M[gid] = {"ground": ["leg_l", "leg_r"], "actions": {
        "idle": loop(600, [{}, {"arm_r": 2, "arm_l": -2, "head": 2, "body": 0.5}], [[0, 0], [0, 3]]),
        "move": loop(170, [w1, {}, w2, {}], [[0, 0], [0, -5], [0, 0], [0, -5]]),
        "attack": once([{"t": 0, "rot": {}},
                        {"t": 240, "rot": {"arm_r": 62, "arm_l": -62, "head": -6, "body": -4}, "root": [0, -12]},
                        {"t": 360, "rot": {"arm_r": 70, "arm_l": -70, "head": -8, "body": -5}, "root": [0, -16]},
                        {"t": 440, "rot": {"arm_r": -12, "arm_l": 12, "head": 8, "body": 6}, "root": [10, 0]},
                        {"t": 640, "rot": {"arm_r": -8, "arm_l": 8, "head": 5, "body": 4}, "root": [8, 0]}, {"t": 840, "rot": {}}],
                       [120, 120, 80, 80, 200, 200], 3),
        "hurt": hurt({"body": -6, "head": -10, "arm_r": 14, "arm_l": -14})}}
# ---- Phu Thuy Bang ----
M["iceWitch"] = {"ground": ["leg_l", "leg_r"], "actions": {
    "idle": loop(500, [{}, {"arm_r_staff": 3, "arm_l": -3, "head": 2}], [[0, 0], [0, 3]]),
    "move": loop(140, [{"leg_r": 12, "leg_l": -12, "arm_l": -8, "body": -2}, {}, {"leg_r": -12, "leg_l": 12, "arm_l": 8, "body": 2}, {}], [[0, 0], [0, -4], [0, 0], [0, -4]]),
    "attack": once([{"t": 0, "rot": {}},
                    {"t": 200, "rot": {"arm_r_staff": 30, "arm_l": -45, "head": -4, "body": -3}, "root": [-4, -6]},
                    {"t": 320, "rot": {"arm_r_staff": 34, "arm_l": -50, "head": -5, "body": -3}, "root": [-4, -8]},
                    {"t": 400, "rot": {"arm_r_staff": -14, "arm_l": 20, "head": 5, "body": 4}, "root": [10, 0]},
                    {"t": 560, "rot": {"arm_r_staff": -8, "arm_l": 12, "head": 3}, "root": [6, 0]}, {"t": 720, "rot": {}}],
                   [100, 100, 80, 80, 160, 160], 3),
    "hurt": hurt({"head": -10, "body": -6, "arm_r_staff": 12, "arm_l": -16})}}
# ---- Hoa Ma ----
M["imp"] = {"ground": ["leg_l", "leg_r"], "actions": {
    "idle": loop(200, [{"wing_r": 16, "wing_l": -16, "tail": 6}, {}, {"wing_r": -10, "wing_l": 10, "tail": -6}, {}], [[0, -3], [0, 0], [0, -3], [0, 0]]),
    "move": loop(100, [{"wing_r": 20, "wing_l": -20, "leg_r": 14, "leg_l": -14, "tail": 10, "body": -3}, {"body": -3},
                       {"wing_r": -12, "wing_l": 12, "leg_r": -14, "leg_l": 14, "tail": -10, "body": -3}, {"body": -3}], [[0, 0], [0, -8], [0, 0], [0, -8]]),
    "attack": once([{"t": 0, "rot": {}},
                    {"t": 160, "rot": {"arm_l": -30, "arm_r": 20, "wing_r": 24, "wing_l": -24, "head": -6, "body": -4}, "root": [-6, -10]},
                    {"t": 260, "rot": {"arm_l": 40, "arm_r": -10, "wing_r": -12, "wing_l": 12, "head": 6, "body": 5}, "root": [12, 0]},
                    {"t": 400, "rot": {"arm_l": 24, "head": 4, "body": 3}, "root": [8, 0]}, {"t": 560, "rot": {}}],
                   [80, 100, 60, 120, 100, 100], 3),
    "hurt": hurt({"head": -12, "body": -8, "wing_r": 24, "wing_l": -24, "tail": 14})}}

Path("monsters").mkdir(exist_ok=True)
for mid, m in M.items():
    out = {"prefix": mid, "native": True, "fit_scale": 0.95, "ground_parts": m["ground"], "actions": m["actions"]}
    Path(f"monsters/motions_{mid}.json").write_text(json.dumps(out, indent=1))
print("ok", list(M))
