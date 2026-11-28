"""Motions for the 4 Codex boss rigs: idle, move, attack, hurt + boss skills (charge / howl / slam / summon / aoe)."""
import json
from pathlib import Path
from gen_monster_motions import loop, once, hurt

M = {}
# ---- Chua Soi Alpha (nhin ngang, quay phai) ----
g1 = {"front_l": -24, "front_r": 16, "rear_l": 22, "rear_r": -16, "body": -3, "head": -3, "tail": -8}
g2 = {"front_l": 20, "front_r": -20, "rear_l": -20, "rear_r": 20, "body": 3, "head": 3, "tail": 8}
M["wolfLord"] = {"ground": ["front_l", "rear_l", "front_r", "rear_r"], "actions": {
    "idle": loop(550, [{}, {"head": 3, "tail": 8, "body": -1}], [[0, 0], [0, 2]]),
    "move": loop(90, [g1, {}, g2, {}], [[0, 0], [0, -10], [0, 0], [0, -10]]),
    "attack": once([{"t": 0, "rot": {}}, {"t": 150, "rot": {"head": -10, "body": -5, "front_l": 8, "front_r": 8, "tail": -10}, "root": [-12, 0]},
                    {"t": 260, "rot": {"head": 16, "body": 5, "front_l": -26, "front_r": -22, "tail": 10}, "root": [26, -8]},
                    {"t": 420, "rot": {"head": 10, "body": 3, "front_l": -10}, "root": [20, 0]}, {"t": 580, "rot": {}}], [80, 100, 70, 130, 120, 100], 3),
    # charge: crouch (all legs tucked, head low) then a long dash; damage on the dash frame
    "skill_charge": once([{"t": 0, "rot": {}},
                          {"t": 260, "rot": {"front_l": 22, "front_r": 22, "rear_l": -22, "rear_r": -22, "head": 14, "body": 4, "tail": -16}, "root": [-18, 14]},
                          {"t": 420, "rot": {"front_l": 22, "front_r": 22, "rear_l": -22, "rear_r": -22, "head": 16, "body": 4, "tail": -16}, "root": [-20, 16]},
                          {"t": 500, "rot": {"front_l": -34, "front_r": -30, "rear_l": 30, "rear_r": 30, "head": 6, "body": -4, "tail": 14}, "root": [60, -18]},
                          {"t": 700, "rot": {"front_l": -12, "rear_l": 10, "head": 4, "tail": 6}, "root": [44, 0]}, {"t": 900, "rot": {}}],
                         [130, 130, 80, 80, 200, 200, 120], 3),
    # howl (summon wolves): head up, tail wag
    "skill_howl": once([{"t": 0, "rot": {}}, {"t": 200, "rot": {"head": -28, "body": -6, "tail": 18, "front_l": -6}, "root": [-4, -6]},
                        {"t": 500, "rot": {"head": -32, "body": -7, "tail": -14, "front_l": -6}, "root": [-4, -8]},
                        {"t": 800, "rot": {"head": -30, "body": -6, "tail": 16}, "root": [-4, -6]}, {"t": 1000, "rot": {}}],
                       [100, 150, 150, 150, 150, 150, 150], 3),
    "hurt": hurt({"head": -16, "body": -6, "tail": -12})}}
# ---- Dam Chua (coc chua) ----
M["toadKing"] = {"ground": ["front_l", "front_r", "hind_l", "hind_r"], "actions": {
    "idle": loop(600, [{}, {"head": -2, "front_r": 2, "front_l": -2}], [[0, 0], [0, 4]]),
    "move": dict(once([{"t": 0, "rot": {}}, {"t": 110, "rot": {"hind_r": 16, "hind_l": -16, "head": 3}, "root": [0, 8]},
                       {"t": 240, "rot": {"hind_r": -18, "hind_l": 18, "front_r": -16, "front_l": 16, "head": -4}, "root": [8, -36]},
                       {"t": 380, "rot": {"front_r": 10, "front_l": -10, "head": 2}, "root": [12, -10]}, {"t": 500, "rot": {}}],
                      [110, 130, 130, 130, 120], None), loop=True),
    "attack": once([{"t": 0, "rot": {}}, {"t": 180, "rot": {"head": -10, "front_r": 6, "front_l": -6}, "root": [-8, 4]},
                    {"t": 290, "rot": {"head": 12, "front_r": -10, "front_l": 10}, "root": [10, -6]}, {"t": 450, "rot": {"head": 6}, "root": [6, 0]},
                    {"t": 600, "rot": {}}], [90, 110, 80, 130, 110, 100], 3),
    # slam (AoE): legs tucked, body squashed down, head raised = warning; then jump and land (damage on landing)
    "skill_slam": once([{"t": 0, "rot": {}},
                        {"t": 300, "rot": {"front_r": 18, "front_l": -18, "hind_r": 14, "hind_l": -14, "head": -12}, "root": [0, 14]},
                        {"t": 560, "rot": {"front_r": 20, "front_l": -20, "hind_r": 16, "hind_l": -16, "head": -14}, "root": [0, 16]},
                        {"t": 700, "rot": {"front_r": -20, "front_l": 20, "hind_r": -18, "hind_l": 18, "head": 6}, "root": [0, -70]},
                        {"t": 820, "rot": {"front_r": 14, "front_l": -14, "hind_r": 10, "hind_l": -10, "head": 8}, "root": [0, 10]},
                        {"t": 1020, "rot": {}}], [140, 140, 140, 140, 120, 120, 200], 4),
    # summon toads: puff up and croak
    "skill_summon": once([{"t": 0, "rot": {}}, {"t": 250, "rot": {"head": -16, "front_r": -6, "front_l": 6}, "root": [0, -8]},
                          {"t": 500, "rot": {"head": -10, "front_r": -4, "front_l": 4}, "root": [0, -4]},
                          {"t": 700, "rot": {"head": -16, "front_r": -6, "front_l": 6}, "root": [0, -8]}, {"t": 900, "rot": {}}],
                         [120, 130, 130, 130, 130, 130, 130], 3),
    "hurt": hurt({"head": -12, "front_r": 12, "front_l": -12})}}
# ---- Pharaoh Co Dai ----
M["pharaoh"] = {"ground": ["leg_l", "leg_r"], "actions": {
    "idle": loop(600, [{}, {"head": 2, "hand_l_staff": -2, "arm_r_upper": 3, "body": 0.6}], [[0, 0], [0, 3]]),
    "move": loop(150, [{"leg_r": 12, "leg_l": -12, "arm_r_upper": 8, "body": -2}, {}, {"leg_r": -12, "leg_l": 12, "arm_r_upper": -6, "body": 2}, {}],
                 [[0, 0], [0, -4], [0, 0], [0, -4]]),
    "attack": once([{"t": 0, "rot": {}}, {"t": 180, "rot": {"arm_r_upper": 50, "arm_r_forearm": 20, "head": -4}, "root": [-6, 0]},
                    {"t": 290, "rot": {"arm_r_upper": -20, "arm_r_forearm": -20, "head": 5, "body": 4}, "root": [12, 0]},
                    {"t": 450, "rot": {"arm_r_upper": -10, "body": 2}, "root": [8, 0]}, {"t": 600, "rot": {}}], [90, 110, 70, 130, 110, 100], 3),
    # summon mummies: lift the staff high
    "skill_summon": once([{"t": 0, "rot": {}}, {"t": 260, "rot": {"arm_l_upper": -55, "hand_l_staff": 20, "arm_r_upper": 40, "head": -6}, "root": [0, -6]},
                          {"t": 600, "rot": {"arm_l_upper": -60, "hand_l_staff": 22, "arm_r_upper": 46, "head": -8}, "root": [0, -8]},
                          {"t": 900, "rot": {}}], [130, 130, 170, 170, 150, 150], 2),
    # AoE: raise then slam the staff down
    "skill_aoe": once([{"t": 0, "rot": {}}, {"t": 260, "rot": {"arm_l_upper": -60, "hand_l_staff": 24, "head": -6, "body": -3}, "root": [0, -8]},
                       {"t": 380, "rot": {"arm_l_upper": 20, "hand_l_staff": -6, "head": 6, "body": 4}, "root": [8, 6]},
                       {"t": 600, "rot": {"arm_l_upper": 14, "hand_l_staff": -4, "head": 4, "body": 3}, "root": [6, 4]}, {"t": 820, "rot": {}}],
                      [130, 130, 120, 110, 110, 110, 110], 3),
    "hurt": hurt({"head": -12, "body": -6, "arm_r_upper": 20, "arm_l_upper": -10})}}
# ---- Chua Quy Bong Dem ----
M["demonLord"] = {"ground": ["leg_l", "leg_r"], "actions": {
    "idle": loop(300, [{"wing_r": 10, "wing_l": -10}, {}, {"wing_r": -6, "wing_l": 6}, {}], [[0, -3], [0, 0], [0, -3], [0, 0]]),
    "move": loop(140, [{"leg_r": 12, "leg_l": -12, "wing_r": 12, "wing_l": -12, "body": -2}, {}, {"leg_r": -12, "leg_l": 12, "wing_r": -8, "wing_l": 8, "body": 2}, {}],
                 [[0, 0], [0, -5], [0, 0], [0, -5]]),
    "attack": once([{"t": 0, "rot": {}}, {"t": 180, "rot": {"arm_r": 46, "arm_l": -20, "head": -4, "wing_r": 10, "wing_l": -10}, "root": [-8, 0]},
                    {"t": 290, "rot": {"arm_r": -30, "arm_l": 10, "head": 6, "body": 4, "wing_r": -8, "wing_l": 8}, "root": [14, 0]},
                    {"t": 450, "rot": {"arm_r": -14, "head": 3, "body": 2}, "root": [10, 0]}, {"t": 620, "rot": {}}], [90, 110, 70, 130, 120, 100], 3),
    # charge: wings folded in, crouch, then dash
    "skill_charge": once([{"t": 0, "rot": {}},
                          {"t": 260, "rot": {"wing_r": -26, "wing_l": 26, "arm_r": -10, "arm_l": 10, "head": 6, "body": 4}, "root": [-14, 10]},
                          {"t": 400, "rot": {"wing_r": -28, "wing_l": 28, "arm_r": -12, "arm_l": 12, "head": 8, "body": 5}, "root": [-16, 12]},
                          {"t": 480, "rot": {"wing_r": -30, "wing_l": 30, "arm_r": -30, "arm_l": 30, "head": 4, "body": 8}, "root": [54, -10]},
                          {"t": 680, "rot": {"wing_r": 6, "wing_l": -6, "body": 3}, "root": [40, 0]}, {"t": 880, "rot": {}}],
                         [130, 130, 80, 80, 200, 200, 120], 3),
    # AoE: wings spread wide, arms brought down
    "skill_aoe": once([{"t": 0, "rot": {}}, {"t": 260, "rot": {"wing_r": 30, "wing_l": -30, "arm_r": 50, "arm_l": -50, "head": -6}, "root": [0, -12]},
                       {"t": 380, "rot": {"wing_r": 34, "wing_l": -34, "arm_r": -26, "arm_l": 26, "head": 6, "body": 3}, "root": [0, 6]},
                       {"t": 620, "rot": {"wing_r": 20, "wing_l": -20, "arm_r": -16, "arm_l": 16, "head": 3}, "root": [0, 4]}, {"t": 860, "rot": {}}],
                      [130, 130, 120, 120, 120, 120, 120], 3),
    "hurt": hurt({"head": -12, "body": -6, "wing_r": 18, "wing_l": -18, "arm_r": 16, "arm_l": -16})}}

Path("monsters").mkdir(exist_ok=True)
for mid, m in M.items():
    out = {"prefix": mid, "native": True, "fit_scale": 0.92, "ground_parts": m["ground"], "actions": m["actions"]}
    Path(f"monsters/motions_{mid}.json").write_text(json.dumps(out, indent=1))
print("ok", list(M))
