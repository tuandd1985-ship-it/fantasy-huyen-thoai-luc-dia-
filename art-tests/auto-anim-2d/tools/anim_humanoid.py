# AUTO-ANIM-2D step 3: motion set for an AutoRig humanoid (Rigby2D scripting API, runs via `rigby run`).
# Reusable for any hero rigged by AutoRig (same bone names). Arms use FK (IK mix 0) so weapons swing from the
# shoulder; legs use FK thigh/shin rotations. Rotations are degrees added to the setup pose (+ = counter-clockwise).
import rigby

for c in rigby.constraints():
    c.mix = 0.0          # FK everywhere: predictable, no IK pops

B = {b.name: b for b in rigby.bones()}
def has(n): return n in B

def anim(name, dur):
    for a in rigby.animations():
        if a.name == name:
            a.remove() if hasattr(a, "remove") else None
    return rigby.add_animation(name, dur)

def k(a, bone, ch, t, v, curve="ease_in_out"):
    if has(bone):
        B[bone].key(ch, v, time=t, animation=a.name, curve=curve)

def loop(a, bone, ch, values, dur, curve="ease_in_out"):
    n = len(values)
    for i, v in enumerate(values + [values[0]]):
        k(a, bone, ch, dur * i / n, v, curve)

# ---------------- idle: breathing ----------------
a = anim("idle", 1.6)
loop(a, "chest", "scale", [(1.0, 1.0), (1.0, 1.025)], 1.6)
loop(a, "hip", "translate", [(0, 0), (-2, 0)], 1.6)
loop(a, "head", "rotate", [0, 1.5], 1.6)
loop(a, "upperarm_r", "rotate", [0, 2.5], 1.6)
loop(a, "upperarm_l", "rotate", [0, -2.0], 1.6)

# ---------------- walk ----------------
a = anim("walk", 0.8)
loop(a, "thigh_l", "rotate", [20, 0, -20, 0], 0.8)
loop(a, "thigh_r", "rotate", [-20, 0, 20, 0], 0.8)
loop(a, "shin_l", "rotate", [0, -10, 0, 0], 0.8)
loop(a, "shin_r", "rotate", [0, 0, 0, -10], 0.8)
loop(a, "hip", "translate", [(0, 0), (6, 0), (0, 0), (6, 0)], 0.8)
loop(a, "chest", "rotate", [2, 0, -2, 0], 0.8)
loop(a, "head", "rotate", [-1.5, 0, 1.5, 0], 0.8)
loop(a, "upperarm_l", "rotate", [-10, 0, 10, 0], 0.8)
loop(a, "upperarm_r", "rotate", [5, 0, -5, 0], 0.8)

# ---------------- run ----------------
a = anim("run", 0.5)
loop(a, "thigh_l", "rotate", [34, 0, -34, 0], 0.5)
loop(a, "thigh_r", "rotate", [-34, 0, 34, 0], 0.5)
loop(a, "shin_l", "rotate", [0, -22, 0, 0], 0.5)
loop(a, "shin_r", "rotate", [0, 0, 0, -22], 0.5)
loop(a, "hip", "translate", [(0, 0), (16, 0), (0, 0), (16, 0)], 0.5)
loop(a, "hip", "rotate", [-5, -5, -5, -5], 0.5)
loop(a, "chest", "rotate", [3, 0, -3, 0], 0.5)
loop(a, "head", "rotate", [2, 0, -2, 0], 0.5)
loop(a, "upperarm_l", "rotate", [-22, 0, 22, 0], 0.5)
loop(a, "upperarm_r", "rotate", [10, 0, -10, 0], 0.5)

# ---------------- attack: wind-up then slash ----------------
a = anim("attack", 0.6)
for bone, keys in {
    "upperarm_r": [(0, 0), (0.18, -38), (0.30, 58), (0.42, 52), (0.6, 0)],
    "forearm_r": [(0, 0), (0.18, -10), (0.30, 14), (0.6, 0)],
    "chest": [(0, 0), (0.18, 6), (0.30, -8), (0.6, 0)],
    "head": [(0, 0), (0.18, 3), (0.30, -4), (0.6, 0)],
    "upperarm_l": [(0, 0), (0.18, -10), (0.30, 14), (0.6, 0)],
    "hip": [(0, 0), (0.30, -4), (0.6, 0)],
}.items():
    for t, v in keys: k(a, bone, "rotate", t, v, "ease_out" if 0.18 <= t <= 0.30 else "ease_in_out")
for t, v in [(0, (0, 0)), (0.18, (-3, 0)), (0.30, (-8, 0)), (0.6, (0, 0))]: k(a, "hip", "translate", t, v)

# ---------------- skill: raise sword overhead, power up, big downward strike ----------------
a = anim("skill", 1.0)
for bone, keys in {
    "upperarm_r": [(0, 0), (0.35, -58), (0.55, -62), (0.70, 72), (0.85, 66), (1.0, 0)],
    "forearm_r": [(0, 0), (0.35, -14), (0.70, 18), (1.0, 0)],
    "upperarm_l": [(0, 0), (0.35, 35), (0.70, -10), (1.0, 0)],
    "chest": [(0, 0), (0.35, 5), (0.70, -10), (1.0, 0)],
    "head": [(0, 0), (0.35, 4), (0.70, -5), (1.0, 0)],
    "thigh_l": [(0, 0), (0.70, 10), (1.0, 0)],
    "thigh_r": [(0, 0), (0.70, -10), (1.0, 0)],
}.items():
    for t, v in keys: k(a, bone, "rotate", t, v)
for t, v in [(0, (1, 1)), (0.35, (1.0, 1.06)), (0.55, (1.0, 1.08)), (0.70, (1.0, 0.95)), (1.0, (1, 1))]: k(a, "chest", "scale", t, v)
for t, v in [(0, (0, 0)), (0.35, (8, 0)), (0.70, (-10, 0)), (1.0, (0, 0))]: k(a, "hip", "translate", t, v)

# ---------------- hit: knock-back + red flash ----------------
a = anim("hit", 0.45)
for bone, keys in {"chest": [(0, 0), (0.08, -10), (0.45, 0)], "head": [(0, 0), (0.08, -12), (0.45, 0)],
                   "upperarm_r": [(0, 0), (0.08, 12), (0.45, 0)], "upperarm_l": [(0, 0), (0.08, -14), (0.45, 0)]}.items():
    for t, v in keys: k(a, bone, "rotate", t, v, "ease_out")
for t, v in [(0, (0, 0)), (0.08, (-2, -14)), (0.45, (0, 0))]: k(a, "hip", "translate", t, v, "ease_out")
for s in rigby.slots():
    s.key_color((1, 1, 1, 1), time=0, animation=a.name)
    s.key_color((1, 0.45, 0.45, 1), time=0.06, animation=a.name)
    s.key_color((1, 1, 1, 1), time=0.3, animation=a.name)

# ---------------- death: stagger, fall, fade ----------------
a = anim("death", 1.2)
for bone, keys in {"hip": [(0, 0), (0.25, -8), (0.75, 82), (1.2, 82)], "head": [(0, 0), (0.25, -10), (0.75, 6), (1.2, 6)],
                   "upperarm_r": [(0, 0), (0.25, 20), (0.75, -30), (1.2, -30)], "upperarm_l": [(0, 0), (0.75, 40), (1.2, 40)],
                   "thigh_l": [(0, 0), (0.75, -15), (1.2, -15)], "thigh_r": [(0, 0), (0.75, 10), (1.2, 10)]}.items():
    for t, v in keys: k(a, bone, "rotate", t, v, "ease_in" if t == 0.75 else "ease_in_out")
for t, v in [(0, (0, 0)), (0.25, (0, -6)), (0.75, (-120, -40)), (1.2, (-120, -40))]: k(a, "hip", "translate", t, v, "ease_in")
for s in rigby.slots():
    s.key_color((1, 1, 1, 1), time=0.8, animation=a.name)
    s.key_color((1, 1, 1, 0.0), time=1.2, animation=a.name)

print("animations:", [x.name for x in rigby.animations()])
