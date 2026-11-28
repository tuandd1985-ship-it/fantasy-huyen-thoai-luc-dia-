"""Motions for Codex monster wave 4 (+ = clockwise)."""
import json
from pathlib import Path
from gen_monster_motions import loop, once, hurt

M = {}
walk = lambda a, extra1={}, extra2={}: [dict({"leg_r": a, "leg_l": -a}, **extra1), {}, dict({"leg_r": -a, "leg_l": a}, **extra2), {}]
# ---- Xuong Kho: kiem chem ----
M["skeleton"] = {"ground": ["leg_l", "leg_r"], "actions": {
    "idle": loop(500, [{}, {"head": 3, "arm_r_upper": 2, "arm_l_upper": -2}], [[0, 0], [0, 2]]),
    "move": loop(130, walk(14, {"arm_r_upper": 8, "arm_l_upper": 6}, {"arm_r_upper": -6, "arm_l_upper": -8}), [[0, 0], [0, -4], [0, 0], [0, -4]]),
    "attack": once([{"t": 0, "rot": {}}, {"t": 170, "rot": {"arm_r_upper": 40, "arm_r_sword": 18, "body": -3, "head": -3}, "root": [-6, 0]},
                    {"t": 270, "rot": {"arm_r_upper": -45, "arm_r_sword": -15, "body": 5, "head": 4}, "root": [12, 0]},
                    {"t": 420, "rot": {"arm_r_upper": -30, "arm_r_sword": -8, "body": 3}, "root": [8, 0]}, {"t": 580, "rot": {}}], [80, 100, 70, 130, 110, 100], 3),
    "hurt": hurt({"head": -14, "body": -6, "arm_r_upper": 14, "arm_l_upper": -16})}}
# ---- Than Lan Dam: vung vuot ----
M["lizard"] = {"ground": ["leg_l", "leg_r"], "actions": {
    "idle": loop(500, [{}, {"head": 3, "tail": 8, "arm_r": 2}], [[0, 0], [0, 2]]),
    "move": loop(110, walk(14, {"tail": 12, "arm_r": 8, "arm_l": -6}, {"tail": -12, "arm_r": -6, "arm_l": 8}), [[0, 0], [0, -5], [0, 0], [0, -5]]),
    "attack": once([{"t": 0, "rot": {}}, {"t": 160, "rot": {"arm_l": -50, "head": -6, "body": -3, "tail": 10}, "root": [-6, 0]},
                    {"t": 260, "rot": {"arm_l": 40, "arm_r": -10, "head": 6, "body": 5, "tail": -12}, "root": [12, 0]},
                    {"t": 400, "rot": {"arm_l": 20, "head": 3, "body": 2}, "root": [8, 0]}, {"t": 560, "rot": {}}], [80, 100, 70, 130, 100, 100], 3),
    "hurt": hurt({"head": -14, "body": -6, "tail": 14, "arm_r": 12, "arm_l": -12})}}
# ---- Bo Cap Cat: 8 chan + cang + duoi chich ----
A = ["leg_r_1", "leg_l_2", "leg_r_3", "leg_l_4"]; Bg = ["leg_l_1", "leg_r_2", "leg_l_3", "leg_r_4"]
lg = lambda g, a: {n: (a if "_r_" in n else -a) for n in g}
M["scorpion"] = {"ground": ["leg_r_1", "leg_l_1", "leg_r_2", "leg_l_2"], "actions": {
    "idle": loop(450, [{}, dict(tail=-4, claw_r=3, claw_l=-3)], [[0, 0], [0, 2]]),
    "move": loop(80, [dict(lg(A, 12), **lg(Bg, -4)), {}, dict(lg(Bg, 12), **lg(A, -4)), {}], [[0, -3], [0, 0], [0, -3], [0, 0]]),
    "attack": once([{"t": 0, "rot": {}}, {"t": 200, "rot": {"tail": -26, "claw_r": 10, "claw_l": -10, "body": -3}, "root": [-6, -4]},
                    {"t": 300, "rot": {"tail": 30, "claw_r": -8, "claw_l": 8, "body": 4}, "root": [10, 0]},
                    {"t": 460, "rot": {"tail": 16, "body": 2}, "root": [6, 0]}, {"t": 620, "rot": {}}], [100, 100, 70, 130, 120, 100], 3),
    "hurt": hurt(dict(lg(A + Bg, 8), tail=-14, claw_r=14, claw_l=-14, body=-5))}}
# ---- Ken Ken (bay) ----
up, dn = {"wing_r": 26, "wing_l": -26}, {"wing_r": -18, "wing_l": 18}
M["vulture"] = {"actions": {
    "idle": loop(150, [dict(up, tail=4), {}, dict(dn, tail=-4), {}], [[0, -6], [0, 0], [0, 6], [0, 0]]),
    "move": loop(100, [dict(up, body=-6), {"body": -6}, dict(dn, body=-6), {"body": -6}], [[0, -8], [0, 0], [0, 8], [0, 0]]),
    "attack": once([{"t": 0, "rot": {}}, {"t": 140, "rot": {"wing_r": 40, "wing_l": -40, "body": -10, "head": -8}, "root": [-10, -22]},
                    {"t": 260, "rot": {"wing_r": -30, "wing_l": 30, "body": 16, "head": 12}, "root": [24, 28]},
                    {"t": 380, "rot": {"wing_r": -10, "wing_l": 10, "body": 8, "head": 6}, "root": [16, 18]}, {"t": 540, "rot": {}}], [120, 120, 60, 100, 100, 100], 2),
    "hurt": hurt({"wing_r": 34, "wing_l": -34, "body": -12, "head": -10})}}
# ---- Yeu Tuyet: dam nang ----
M["yeti"] = {"ground": ["leg_l", "leg_r"], "actions": {
    "idle": loop(600, [{}, {"arm_r": 2, "arm_l": -2, "head": 2}], [[0, 0], [0, 3]]),
    "move": loop(160, walk(10, {"arm_r": -8, "arm_l": -6, "body": -2}, {"arm_r": 6, "arm_l": 8, "body": 2}), [[0, 0], [0, -5], [0, 0], [0, -5]]),
    "attack": once([{"t": 0, "rot": {}}, {"t": 220, "rot": {"arm_l": -70, "head": -6, "body": -4}, "root": [-8, 0]},
                    {"t": 320, "rot": {"arm_l": -76, "head": -7, "body": -5}, "root": [-10, 0]},
                    {"t": 400, "rot": {"arm_l": 20, "arm_r": -10, "head": 6, "body": 6}, "root": [14, 0]},
                    {"t": 580, "rot": {"arm_l": 10, "head": 3, "body": 3}, "root": [10, 0]}, {"t": 760, "rot": {}}], [110, 110, 80, 80, 180, 180], 3),
    "hurt": hurt({"head": -12, "body": -6, "arm_r": 14, "arm_l": -14})}}
# ---- Ma Ca Rong: huyet cau (tung) ----
M["vampire"] = {"ground": ["leg_l", "leg_r"], "actions": {
    "idle": loop(500, [{}, {"head": 2, "arm_r_upper": 2, "arm_l_upper": -2}], [[0, 0], [0, 2]]),
    "move": loop(140, walk(12, {"arm_r_upper": 6, "arm_l_upper": 6}, {"arm_r_upper": -6, "arm_l_upper": -6}), [[0, 0], [0, -4], [0, 0], [0, -4]]),
    "attack": once([{"t": 0, "rot": {}}, {"t": 200, "rot": {"arm_l_upper": -40, "arm_l_forearm": -30, "arm_r_upper": 20, "head": -4}, "root": [-4, 0]},
                    {"t": 320, "rot": {"arm_l_upper": -44, "arm_l_forearm": -34, "arm_r_upper": 24, "head": -5}, "root": [-4, 0]},
                    {"t": 400, "rot": {"arm_l_upper": 16, "arm_l_forearm": 10, "arm_r_upper": -8, "head": 5, "body": 4}, "root": [12, 0]},
                    {"t": 560, "rot": {"arm_l_upper": 8, "head": 3, "body": 2}, "root": [8, 0]}, {"t": 720, "rot": {}}], [100, 100, 80, 80, 160, 160], 3),
    # life drain: arms spread, slight hover, held
    "skill_drain": once([{"t": 0, "rot": {}}, {"t": 240, "rot": {"arm_r_upper": 40, "arm_l_upper": -40, "arm_r_forearm": 10, "arm_l_forearm": -10, "head": -6}, "root": [0, -10]},
                         {"t": 800, "rot": {"arm_r_upper": 44, "arm_l_upper": -44, "arm_r_forearm": 12, "arm_l_forearm": -12, "head": -8}, "root": [0, -14]},
                         {"t": 1000, "rot": {}}], [120, 120, 190, 190, 190, 190], 2),
    "hurt": hurt({"head": -12, "body": -6, "arm_r_upper": 16, "arm_l_upper": -16})}}

Path("monsters").mkdir(exist_ok=True)
for mid, m in M.items():
    out = {"prefix": mid, "native": True, "fit_scale": 0.95, "actions": m["actions"]}
    if "ground" in m: out["ground_parts"] = m["ground"]
    Path(f"monsters/motions_{mid}.json").write_text(json.dumps(out, indent=1))
print("ok", list(M))
