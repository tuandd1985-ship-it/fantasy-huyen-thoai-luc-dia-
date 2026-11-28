"""Write motions_<id>.json for the six Codex monster rigs (rotations in degrees, + = clockwise on screen)."""
import json
from pathlib import Path


def loop(ms, poses, roots=None):
    n = len(poses); keys = []
    for i, p in enumerate(poses + [poses[0]]):
        k = {"t": i * ms, "rot": p}
        if roots: k["root"] = (roots + [roots[0]])[i]
        keys.append(k)
    return {"loop": True, "frames_ms": [ms] * n, "hit_frame": None, "keys": keys}


def once(keys, frames_ms, hit):
    return {"loop": False, "frames_ms": frames_ms, "hit_frame": hit, "keys": keys}


def hurt(extra):
    return once([{"t": 0, "rot": {}}, {"t": 80, "rot": extra, "root": [-14, -4]},
                 {"t": 200, "rot": {k: v * 0.4 for k, v in extra.items()}, "root": [-6, 0]}, {"t": 320, "rot": {}}], [80, 120, 120], None)


M = {}
# ---- Doi Quy (bay) ----
up, down = {"wing_r": 28, "wing_l": -28, "head": -2}, {"wing_r": -22, "wing_l": 22, "head": 2}
M["bat"] = {"actions": {
    "idle": loop(140, [up, {}, down, {}], [[0, -6], [0, 0], [0, 6], [0, 0]]),
    "move": loop(90, [dict(up, body=-8), {"body": -8}, dict(down, body=-8), {"body": -8}], [[0, -8], [0, 0], [0, 8], [0, 0]]),
    "attack": once([{"t": 0, "rot": {}}, {"t": 120, "rot": {"wing_r": 40, "wing_l": -40, "body": -12, "head": -8}, "root": [-10, -24]},
                    {"t": 240, "rot": {"wing_r": -30, "wing_l": 30, "body": 18, "head": 10}, "root": [24, 30]},
                    {"t": 360, "rot": {"wing_r": -10, "wing_l": 10, "body": 10, "head": 6}, "root": [18, 22]}, {"t": 520, "rot": {}}],
                   [120, 120, 60, 100, 100, 100], 2),
    "hurt": hurt({"wing_r": 35, "wing_l": -35, "body": -14, "head": -10})}}
# ---- Coc Doc ----
M["toad"] = {"ground": ["front_l", "front_r", "hind_l", "hind_r"], "actions": {
    "idle": loop(500, [{}, {"head": -2, "front_r": 2, "front_l": -2}], [[0, 0], [0, 3]]),
    "move": dict(once([{"t": 0, "rot": {}}, {"t": 90, "rot": {"hind_r": 18, "hind_l": -18, "head": 3}, "root": [0, 6]},
                       {"t": 200, "rot": {"hind_r": -20, "hind_l": 20, "front_r": -18, "front_l": 18, "head": -4}, "root": [10, -46]},
                       {"t": 330, "rot": {"front_r": 12, "front_l": -12, "head": 2}, "root": [16, -14]}, {"t": 440, "rot": {}, "root": [0, 0]}],
                      [90, 110, 110, 110, 110, 100], None), loop=True),
    "attack": once([{"t": 0, "rot": {}}, {"t": 160, "rot": {"head": -10, "front_r": 6, "front_l": -6}, "root": [-8, 4]},
                    {"t": 260, "rot": {"head": 12, "front_r": -10, "front_l": 10}, "root": [10, -6]}, {"t": 420, "rot": {"head": 6}, "root": [6, 0]},
                    {"t": 560, "rot": {}}], [80, 100, 80, 120, 100, 100], 3),
    "hurt": hurt({"head": -10, "front_r": 12, "front_l": -12})}}
# ---- Xac Uop ----
s1 = {"leg_r": 16, "leg_l": -16, "arm_r_upper": 12, "arm_l_upper": -6, "body": -2, "head": 3}
s2 = {"leg_r": -16, "leg_l": 16, "arm_r_upper": 6, "arm_l_upper": -12, "body": 2, "head": -3}
M["mummy"] = {"ground": ["leg_l", "leg_r"], "actions": {
    "idle": loop(500, [{}, {"head": 3, "arm_r_upper": 3, "arm_l_upper": -3, "body": 1}]),
    "move": loop(130, [s1, {"arm_r_upper": 9, "arm_l_upper": -9}, s2, {"arm_r_upper": 9, "arm_l_upper": -9}], [[0, 0], [0, -4], [0, 0], [0, -4]]),
    "attack": once([{"t": 0, "rot": {}},
                    {"t": 180, "rot": {"arm_r_upper": 70, "arm_l_upper": -70, "arm_r_forearm": 20, "arm_l_forearm": -20, "body": -4, "head": -5}, "root": [-6, 0]},
                    {"t": 300, "rot": {"arm_r_upper": -10, "arm_l_upper": 10, "arm_r_forearm": -25, "arm_l_forearm": 25, "body": 6, "head": 6}, "root": [14, 0]},
                    {"t": 440, "rot": {"body": 4, "head": 4}, "root": [10, 0]}, {"t": 600, "rot": {}}], [90, 110, 60, 120, 120, 100], 3),
    "hurt": hurt({"body": -8, "head": -12, "arm_r_upper": 25, "arm_l_upper": -25})}}
# ---- Rong Lua ----
f_up, f_dn = {"wing_r": 22, "wing_l": -22}, {"wing_r": -14, "wing_l": 14}
M["fireDragon"] = {"ground": ["foreleg_l", "foreleg_r", "hindleg_l", "hindleg_r"], "actions": {
    "idle": loop(260, [dict(f_up, tail=6, head=-2), {"tail": 0}, dict(f_dn, tail=-6, head=2), {"tail": 0}], [[0, 0], [0, -3], [0, 0], [0, -3]]),
    "move": loop(110, [dict(f_up, foreleg_r=14, foreleg_l=-14, hindleg_r=-12, hindleg_l=12, tail=10), {"tail": 0},
                       dict(f_dn, foreleg_r=-14, foreleg_l=14, hindleg_r=12, hindleg_l=-12, tail=-10), {"tail": 0}], [[0, 0], [0, -6], [0, 0], [0, -6]]),
    "attack": once([{"t": 0, "rot": {}}, {"t": 200, "rot": {"wing_r": 34, "wing_l": -34, "head": -12, "tail": 14, "body": -3}, "root": [-8, -10]},
                    {"t": 330, "rot": {"wing_r": -18, "wing_l": 18, "head": 14, "tail": -10, "body": 4, "foreleg_r": -10, "foreleg_l": 10}, "root": [14, 6]},
                    {"t": 520, "rot": {"wing_r": -10, "wing_l": 10, "head": 10, "body": 3}, "root": [12, 4]}, {"t": 700, "rot": {}}],
                   [100, 110, 70, 160, 140, 120], 3),
    "hurt": hurt({"head": -14, "wing_r": 24, "wing_l": -24, "tail": 12})}}
# ---- Soi Bang (nhin ngang, quay phai) ----
g1 = {"front_l": -26, "front_r": 18, "rear_l": 24, "rear_r": -18, "body": -3, "head": -3, "tail": -8}
g2 = {"front_l": 22, "front_r": -22, "rear_l": -22, "rear_r": 22, "body": 3, "head": 3, "tail": 8}
M["iceWolf"] = {"ground": ["front_l", "rear_l", "front_r", "rear_r"], "actions": {
    "idle": loop(500, [{}, {"head": 3, "tail": 8, "body": -1}]),
    "move": loop(85, [g1, {}, g2, {}], [[0, 0], [0, -10], [0, 0], [0, -10]]),
    "attack": once([{"t": 0, "rot": {}},
                    {"t": 160, "rot": {"head": -10, "body": -6, "front_l": 10, "front_r": 10, "rear_l": -14, "rear_r": -14, "tail": -14}, "root": [-16, 0]},
                    {"t": 280, "rot": {"head": 16, "body": 6, "front_l": -34, "front_r": -30, "rear_l": 26, "rear_r": 26, "tail": 12}, "root": [36, -14]},
                    {"t": 420, "rot": {"head": 12, "body": 4, "front_l": -14, "front_r": -12}, "root": [30, 0]}, {"t": 580, "rot": {}}],
                   [80, 100, 60, 140, 120, 100], 3),
    "hurt": hurt({"head": -16, "body": -6, "tail": -12})}}
# ---- Hon Ma (bay) ----
M["wraith"] = {"actions": {
    "idle": loop(220, [{"tail": 8, "arm_r": 4, "arm_l": -4}, {}, {"tail": -8, "arm_r": -4, "arm_l": 4}, {}], [[0, -8], [0, 0], [0, 8], [0, 0]]),
    "move": loop(150, [{"tail": 14, "body": -6, "arm_r": 8, "arm_l": 4}, {"body": -6, "tail": 4}, {"tail": -6, "body": -6, "arm_r": 2, "arm_l": -8}, {"body": -6}],
                 [[0, -6], [0, 0], [0, 6], [0, 0]]),
    "attack": once([{"t": 0, "rot": {}}, {"t": 180, "rot": {"arm_r": 60, "arm_l": -60, "head": -6, "body": -4, "tail": 10}, "root": [-8, -12]},
                    {"t": 300, "rot": {"arm_r": -35, "arm_l": 35, "head": 8, "body": 6, "tail": -12}, "root": [18, 8]},
                    {"t": 460, "rot": {"arm_r": -18, "arm_l": 18, "head": 4, "body": 4}, "root": [12, 4]}, {"t": 620, "rot": {}}],
                   [90, 110, 60, 140, 120, 100], 3),
    "hurt": hurt({"head": -12, "arm_r": 30, "arm_l": -30, "tail": 16})}}

Path("monsters").mkdir(exist_ok=True)
for mid, m in M.items():
    out = {"prefix": mid, "native": True, "fit_scale": 0.95, "actions": m["actions"]}
    if "ground" in m: out["ground_parts"] = m["ground"]
    Path(f"monsters/motions_{mid}.json").write_text(json.dumps(out, indent=1))
print("ok", list(M))
