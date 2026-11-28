"""Hero motion sets for the Codex part rigs (6 heroes). Extends the existing idle/run/skill-1 files with the normal
attack, hurt and skills 2-4. Female sets reuse the male keys; ponytail/braid follow head/torso/cape with lag.
Usage: python gen_hero_motions.py <phase>   phase = attack | all
"""
import json, sys, copy
from pathlib import Path

T = Path(__file__).parent
HAIR = {"kiemsi": "ponytail", "cungthu": "braid"}


def seq(frames_ms, poses, hit, roots=None, z=None):
    """One key per frame start (pose i shown at frame i), plus the closing rest key."""
    keys, t = [], 0
    for i, p in enumerate(poses):
        k = {"t": t, "rot": p}
        if roots and roots[i]: k["root"] = roots[i]
        if z and z[i]: k["z"] = z[i]
        keys.append(k); t += frames_ms[i]
    keys.append({"t": t, "rot": {}})
    return {"loop": False, "frames_ms": frames_ms, "hit_frame": hit, "keys": keys}


def hurt(p):
    half = {k: round(v * 0.4, 1) for k, v in p.items()}
    return seq([80, 110, 110], [{}, p, half], None, [None, [-14, 0], [-6, 0]])


# ---------------- Kiếm Sĩ ----------------
BEHIND = {"hand_r_sword": 6.5, "arm_r_forearm": 6.4, "arm_r_upper": 6.3}
KS = {
    # chém thường: nâng kiếm lên vai -> chém chéo xuống -> theo đà -> về. hit = frame 2
    "attack": seq([70, 80, 60, 100, 90],
                  [{}, {"arm_r_upper": 18, "arm_r_forearm": 8, "hand_r_sword": 6, "torso": -3, "head": -2, "arm_l_upper": 8},
                   {"arm_r_upper": -40, "arm_r_forearm": -12, "hand_r_sword": -8, "torso": 6, "head": 3, "arm_l_upper": -14, "cape": -10},
                   {"arm_r_upper": -34, "arm_r_forearm": -8, "hand_r_sword": -6, "torso": 4, "head": 2, "arm_l_upper": -10, "cape": -6},
                   {"arm_r_upper": -12, "torso": 1, "cape": -2}],
                  2, [None, [-4, 0], [26, 0], [22, 0], [8, 0]]),
    "hurt": hurt({"torso": -8, "head": -10, "arm_r_upper": 14, "arm_l_upper": -16, "cape": 10}),
    # Kiếm Vũ: quét kiếm ngang 2 vòng trước người (không xoay lưng được), áo choàng tung
    "kiem_vu": seq([80, 70, 70, 70, 70, 90, 100],
                   [{"arm_r_upper": 14, "torso": -3, "cape": 6},
                    {"arm_r_upper": -42, "arm_r_forearm": -14, "hand_r_sword": -10, "torso": 6, "head": 3, "cape": -14},
                    {"arm_r_upper": -70, "arm_r_forearm": -24, "hand_r_sword": -18, "torso": 8, "head": 4, "arm_l_upper": -20, "cape": -20},
                    {"arm_r_upper": 10, "arm_r_forearm": 6, "torso": -4, "cape": 12},
                    {"arm_r_upper": -42, "arm_r_forearm": -14, "hand_r_sword": -10, "torso": 6, "cape": -14},
                    {"arm_r_upper": -70, "arm_r_forearm": -24, "hand_r_sword": -18, "torso": 8, "arm_l_upper": -20, "cape": -20},
                    {"arm_r_upper": -20, "torso": 2, "cape": -4}],
                   2, [None, [10, 0], [18, 0], [0, 0], [10, 0], [18, 0], [6, 0]]),
    # Địa Chấn: giơ kiếm ra sau đầu, nhún bật lên, bổ xuống cắm đất (thân nén), giữ
    "dia_chan": seq([80, 120, 90, 60, 160, 110, 100],
                    [{}, {"arm_r_upper": 38, "arm_r_forearm": 16, "hand_r_sword": 10, "torso": -6, "head": -4, "arm_l_upper": 14},
                     {"arm_r_upper": 44, "arm_r_forearm": 18, "hand_r_sword": 12, "torso": -7, "head": -5, "arm_l_upper": 16, "cape": 8},
                     {"arm_r_upper": -64, "arm_r_forearm": -30, "hand_r_sword": -24, "torso": 9, "head": 6, "arm_l_upper": -20, "cape": -16},
                     {"arm_r_upper": -66, "arm_r_forearm": -32, "hand_r_sword": -26, "torso": 10, "head": 6, "arm_l_upper": -22, "cape": -12},
                     {"arm_r_upper": -40, "arm_r_forearm": -16, "torso": 5, "cape": -6}, {"arm_r_upper": -10}],
                    3, [None, [0, -6], [0, -26], [14, 0], [16, 0], [8, 0], None], [None, BEHIND, BEHIND, None, None, None, None]),
    # Thiên Kiếm: giơ kiếm thẳng trời, bay lên, giữ (gọi đại kiếm), chém xuống, về
    "thien_kiem": seq([90, 100, 160, 200, 80, 140, 110],
                      [{"torso": -2}, {"arm_r_upper": 24, "arm_r_forearm": -30, "hand_r_sword": 6, "head": -6, "arm_l_upper": 10},
                       {"arm_r_upper": 30, "arm_r_forearm": -40, "hand_r_sword": 10, "head": -8, "arm_l_upper": 14, "cape": 10},
                       {"arm_r_upper": 32, "arm_r_forearm": -42, "hand_r_sword": 10, "head": -8, "arm_l_upper": 14, "cape": 14},
                       {"arm_r_upper": -60, "arm_r_forearm": -20, "hand_r_sword": -16, "torso": 8, "head": 5, "arm_l_upper": -18, "cape": -16},
                       {"arm_r_upper": -50, "arm_r_forearm": -16, "hand_r_sword": -12, "torso": 6, "cape": -10}, {"arm_r_upper": -14}],
                      4, [None, [0, -8], [0, -22], [0, -24], [16, 0], [12, 0], None]),
}
# ---------------- Pháp Sư (trượng ở tay trái, ảnh bên phải) ----------------
PS = {
    # tung phép nhỏ: rút trượng về -> vung trượng chĩa tới -> giữ -> về. hit = frame 2
    "attack": seq([70, 90, 60, 110, 90],
                  [{}, {"arm_l_upper": -14, "arm_l_forearm": -6, "hand_l_staff": -10, "torso": 2, "arm_r_upper": 10},
                   {"arm_l_upper": -40, "arm_l_forearm": -10, "hand_l_staff": 78, "arm_r_upper": -16, "torso": -4, "head": 2, "cape": -8},
                   {"arm_l_upper": -36, "arm_l_forearm": -8, "hand_l_staff": 70, "arm_r_upper": -12, "torso": -3, "cape": -5},
                   {"arm_l_upper": -14, "hand_l_staff": 24}],
                  2, [None, [-4, 0], [12, 0], [10, 0], [4, 0]]),
    "hurt": hurt({"torso": 8, "head": 10, "arm_l_upper": -12, "arm_r_upper": 18, "cape": -10}),
    # Băng Phong: quét trượng ngang qua trước người hai nhịp (gió băng)
    "bang_phong": seq([80, 90, 90, 90, 90, 100, 100],
                      [{}, {"arm_l_upper": -40, "arm_l_forearm": -10, "hand_l_staff": 80, "torso": -3},
                       {"arm_l_upper": -60, "arm_l_forearm": -14, "hand_l_staff": 104, "arm_r_upper": -20, "torso": -5, "cape": -10},
                       {"arm_l_upper": -24, "arm_l_forearm": -6, "hand_l_staff": 50, "arm_r_upper": 20, "torso": 3, "cape": 8},
                       {"arm_l_upper": -60, "arm_l_forearm": -14, "hand_l_staff": 104, "arm_r_upper": -20, "torso": -5, "cape": -10},
                       {"arm_l_upper": -50, "arm_l_forearm": -12, "hand_l_staff": 90, "torso": -4, "cape": -6}, {"arm_l_upper": -16, "hand_l_staff": 20}],
                      2, [None, [4, 0], [10, 0], [-4, 0], [10, 0], [8, 0], None]),
    # Lôi Đình: giơ trượng thẳng lên trời, tay kia dang, giữ (sét đánh xuống ở khung giữ)
    "loi_dinh": seq([80, 120, 140, 180, 120, 100],
                    [{}, {"arm_l_upper": -80, "arm_l_forearm": -22, "hand_l_staff": 100, "arm_r_upper": 44, "arm_r_forearm": 26, "torso": 2, "head": -3},
                     {"arm_l_upper": -92, "arm_l_forearm": -20, "hand_l_staff": 108, "arm_r_upper": 52, "arm_r_forearm": 30, "torso": 3, "head": -4, "cape": 6},
                     {"arm_l_upper": -94, "arm_l_forearm": -20, "hand_l_staff": 110, "arm_r_upper": 54, "arm_r_forearm": 30, "torso": 3, "head": -4, "cape": 8},
                     {"arm_l_upper": -60, "arm_l_forearm": -12, "hand_l_staff": 80, "arm_r_upper": 20, "head": 2}, {"arm_l_upper": -20, "hand_l_staff": 24}],
                    3, [None, [0, -6], [0, -12], [0, -14], [0, -4], None]),
    # Thiên Thạch: hai tay giơ cao tụ phép lâu, rồi đẩy trượng chém xuống phía trước (thiên thạch rơi)
    "thien_thach": seq([90, 140, 180, 80, 160, 120, 100],
                       [{}, {"arm_l_upper": -80, "arm_l_forearm": -22, "hand_l_staff": 100, "arm_r_upper": 60, "arm_r_forearm": 40, "head": -5},
                        {"arm_l_upper": -94, "arm_l_forearm": -22, "hand_l_staff": 110, "arm_r_upper": 70, "arm_r_forearm": 46, "head": -6, "cape": 8},
                        {"arm_l_upper": -20, "arm_l_forearm": -8, "hand_l_staff": 60, "arm_r_upper": -24, "torso": -6, "head": 4, "cape": -12},
                        {"arm_l_upper": -16, "arm_l_forearm": -6, "hand_l_staff": 56, "arm_r_upper": -20, "torso": -6, "head": 4, "cape": -10},
                        {"arm_l_upper": -10, "hand_l_staff": 30, "torso": -2}, {}],
                       3, [None, [0, -10], [0, -18], [14, 0], [16, 0], [6, 0], None]),
}
# ---------------- Cung Thủ (cung ở tay trái, ảnh bên phải) ----------------
DRAW = {"arm_l_upper": -24, "hand_l_bow": 24, "arm_r_upper": -100, "arm_r_forearm": -20, "torso": -3, "head": 2}
REL = {"arm_l_upper": -20, "hand_l_bow": 30, "arm_r_upper": 45, "arm_r_forearm": 20, "torso": 2, "cape": 6}
CT = {
    # bắn thường: nâng cung + kéo dây nhanh -> buông -> theo đà -> về. hit = frame 2 (buông dây)
    "attack": seq([60, 90, 60, 110, 80],
                  [{}, DRAW, REL, {"arm_l_upper": -14, "hand_l_bow": 20, "arm_r_upper": 28, "arm_r_forearm": 12, "cape": 4}, {"arm_l_upper": -6}],
                  2, [None, [-4, 0], [-10, 0], [-6, 0], None]),
    "hurt": hurt({"torso": 8, "head": 10, "arm_l_upper": 12, "arm_r_upper": 18, "cape": -10, "quiver": 8}),
    # Liên Tiễn: kéo-buông 3 lần liên tiếp. hit = lần buông đầu (game bắn 3 mũi theo nhịp 3 lần buông)
    "lien_tien": seq([60, 80, 50, 80, 50, 80, 50, 100],
                     [{}, DRAW, REL, DRAW, REL, DRAW, REL, {"arm_l_upper": -10}],
                     2, [None, [-4, 0], [-8, 0], [-4, 0], [-8, 0], [-4, 0], [-8, 0], None]),
    # Độc Tiễn: ngắm lâu (giữ dây), buông mạnh
    "doc_tien": seq([70, 120, 200, 60, 140, 100],
                    [{}, DRAW, dict(DRAW, arm_r_upper=-106, head=3), dict(REL, arm_r_upper=55), dict(REL, arm_r_upper=30), {}],
                    3, [None, [-4, 0], [-6, 0], [-14, 0], [-8, 0], None]),
    # Vạn Tiễn: chĩa cung lên trời, kéo dây, buông (mưa tên rơi xuống)
    "van_tien": seq([80, 120, 160, 60, 160, 100],
                    [{}, {"arm_l_upper": -70, "hand_l_bow": 40, "arm_r_upper": -120, "arm_r_forearm": -10, "head": -8, "torso": -2},
                     {"arm_l_upper": -80, "hand_l_bow": 44, "arm_r_upper": -128, "arm_r_forearm": -8, "head": -10, "torso": -3},
                     {"arm_l_upper": -80, "hand_l_bow": 50, "arm_r_upper": 20, "arm_r_forearm": 10, "head": -8, "cape": 6},
                     {"arm_l_upper": -60, "hand_l_bow": 40, "arm_r_upper": 14, "head": -4}, {"arm_l_upper": -10}],
                    3, [None, [0, -4], [0, -6], [-8, 0], [-4, 0], None]),
}
SETS = {"kiemsi": KS, "phapsu": PS, "cungthu": CT}
PHASE1 = {"attack"}


def with_hair(m, h):
    for a in m["actions"].values():
        for k in a["keys"]:
            r = k.setdefault("rot", {})
            if r: r[h] = round(-0.8 * (r.get("head", 0) + r.get("torso", 0)) + 0.6 * r.get("cape", 0), 1)
    return m


if __name__ == "__main__":
    phase = sys.argv[1] if len(sys.argv) > 1 else "all"
    for c, acts in SETS.items():
        base = json.loads((T / f"motions_{c}_codex.json").read_text())
        base["actions"] = {k: v for k, v in base["actions"].items() if k in ("idle", "run") or k in ("tram_kiem", "tung_phep", "ban_cung")}
        for k, v in acts.items():
            if phase == "all" or k in PHASE1: base["actions"][k] = copy.deepcopy(v)
        (T / f"motions_{c}_hero.json").write_text(json.dumps(base, indent=1))
        nu = copy.deepcopy(base); nu["prefix"] = f"{c}_nu"
        if c in HAIR: nu = with_hair(nu, HAIR[c])
        (T / f"motions_{c}_hero_nu.json").write_text(json.dumps(nu, indent=1))
    print("ok", phase)
