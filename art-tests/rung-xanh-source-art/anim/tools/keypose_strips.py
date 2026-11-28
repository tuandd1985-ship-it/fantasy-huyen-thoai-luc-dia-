"""Key-pose sheets (ImageGen, true alpha) -> cleaned poses -> per-action strips with derived in-between frames.
Derived frames only re-use the key drawings (squash / lean / push / flip / hold), so face, outfit and weapon stay exact.
Usage: python keypose_strips.py <src_dir> <out_dir>
"""
import sys, json, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
sys.path.insert(0, "C:/AI/GAME-ART-CORE/tools")
import mage_anim_compose as mc   # premul_transform, rot, qc_cell

CELL, CELL_H, FEET_Y = 768, 640, 620


def components(A):
    lab, n = ndi.label(ndi.binary_dilation(A > 8, iterations=6)); out = []
    for i, s in enumerate(ndi.find_objects(lab)):
        m = np.zeros(A.shape, bool); m[s] = (lab[s] == i + 1)
        if (m & (A > 8)).sum() > 3000: out.append(m)
    return out


def clean_alpha(rgba):
    """ImageGen alpha: core is 251-254 (not opaque) and there is a faint 1-30 haze. Solidify the core, drop haze and
    specks, keep the anti-aliased edge (the 2 px band next to the solid body)."""
    a = rgba.astype(float); A = a[..., 3]
    solid = A >= 200
    solid = ndi.binary_fill_holes(solid)
    lab, n = ndi.label(solid)
    if n > 1:
        sz = ndi.sum(np.ones_like(A), lab, range(1, n + 1)); solid = np.isin(lab, 1 + np.nonzero(sz >= 60)[0])
    near = ndi.binary_dilation(solid, iterations=2)
    A2 = np.where(solid, 255, np.where(near, A, 0))
    A2 = np.where(near & ~solid & (A < 24), 0, A2)
    out = a.copy(); out[..., 3] = A2
    return out.round().astype(np.uint8), {"haze_px_removed": int(((A > 0) & (A2 == 0)).sum()), "core_px_solidified": int((solid & (A < 255)).sum())}


def crop_pose(im, m):
    a = im.copy(); a[~m, 3] = 0
    ys, xs = np.nonzero(a[..., 3] > 0); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    return Image.fromarray(a[y0:y1, x0:x1])


def feet_x(img):
    A = np.asarray(img)[..., 3]; ys = np.nonzero(A.max(1) > 128)[0]; yb = ys.max()
    band = A[max(0, yb - 40):yb + 1] > 128; xs = np.nonzero(band.any(0))[0]
    return float((xs.min() + xs.max()) / 2), float(yb)


def place(img, scale, fx_shift=0.0, sx=1.0, sy=1.0, lean=0.0, dy=0.0, flip=False, anchor_x=None):
    """Draw pose into a CELL x CELL canvas: feet centre at (CELL/2 + fx_shift, FEET_Y + dy), squash/stretch about the
    feet, lean (deg) about the feet, optional horizontal flip about the feet."""
    W, H = img.size; s = scale
    im = mc.premul_transform(img, lambda x: x.resize((max(1, round(W * s * sx)), max(1, round(H * s * sy))), Image.LANCZOS))
    if flip: im = im.transpose(Image.FLIP_LEFT_RIGHT)
    fx, fy = feet_x(im) if anchor_x is None else (anchor_x * s * sx if not flip else im.width - anchor_x * s * sx, feet_x(im)[1])
    cv = Image.new("RGBA", (CELL * 2, CELL * 2))
    ox, oy = CELL - fx, CELL - fy
    cv.alpha_composite(im, (round(ox), round(oy)))
    if lean: cv = mc.rot(cv, lean, (CELL, CELL))
    # re-anchor: after squash / lean the lowest opaque row must sit exactly on FEET_Y (+dy for jumps)
    A = np.asarray(cv)[..., 3]; ys = np.nonzero(A.max(1) > 128)[0]; low = ys.max()
    top = low - FEET_Y - round(dy)
    out = Image.new("RGBA", (CELL, CELL_H))
    out.alpha_composite(cv.crop((CELL - CELL // 2 - round(fx_shift), top, CELL + CELL // 2 - round(fx_shift), top + CELL_H)))
    return out


def strip(frames):
    S = Image.new("RGBA", (CELL * len(frames), CELL_H))
    for i, f in enumerate(frames): S.alpha_composite(f, (i * CELL, 0))
    return S


def main():
    src, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True); report = {}
    # ---------------- Kiếm Sĩ Nam ----------------
    im = np.asarray(Image.open(src / "swordsman-male-key-poses.png").convert("RGBA"))
    im, info = clean_alpha(im); comps = components(im[..., 3])
    boxes = []
    for m in comps:
        ys, xs = np.nonzero(m); boxes.append((int(ys.min() > 470), xs.min(), m))
    boxes.sort(key=lambda b: (b[0], b[1]))
    names = ["idle", "tram_kiem", "kiem_vu", "dia_chan", "thien_kiem"]
    P = {n: crop_pose(im, b[2]) for n, b in zip(names, boxes)}
    (out / "poses_kiemsi").mkdir(exist_ok=True)
    for n, p in P.items(): p.save(out / "poses_kiemsi" / f"{n}.png")
    S = 476 / P["idle"].height           # match the in-game k13 strip: idle (with raised blade) 476 px tall
    I = P["idle"]
    ks = {
        # name: [(pose, kwargs, duration_ms)], hit = index of the damage frame
        "tram_kiem": ([(I, {}, 60), (I, dict(sx=1.03, sy=0.96, lean=-6, fx_shift=-6), 90), (P["tram_kiem"], dict(fx_shift=6), 50),
                       (P["tram_kiem"], dict(fx_shift=16, sx=1.04, sy=0.97), 110), (P["tram_kiem"], dict(fx_shift=12), 120), (I, dict(sx=0.99, sy=1.01), 90)], 3),
        "kiem_vu": ([(I, dict(sx=1.03, sy=0.97, lean=-4), 80), (P["kiem_vu"], dict(fx_shift=-40), 70), (P["kiem_vu"], dict(flip=True, fx_shift=40), 70),
                     (P["kiem_vu"], dict(fx_shift=-40), 70), (P["kiem_vu"], dict(flip=True, fx_shift=40), 70), (P["kiem_vu"], dict(sx=1.03, sy=0.97, fx_shift=-40), 90), (I, {}, 100)], 1),
        "dia_chan": ([(I, {}, 60), (P["thien_kiem"], dict(dy=-10, sx=0.98, sy=1.03), 140), (P["thien_kiem"], dict(dy=-16, sx=0.97, sy=1.05), 90),
                      (P["dia_chan"], dict(sx=1.05, sy=0.94), 60), (P["dia_chan"], {}, 160), (P["dia_chan"], dict(sx=1.01, sy=0.99), 120), (I, {}, 100)], 3),
        "thien_kiem": ([(I, dict(sx=1.03, sy=0.96), 90), (P["thien_kiem"], dict(dy=-6), 100), (P["thien_kiem"], dict(dy=-14, sy=1.03), 160),
                        (P["thien_kiem"], dict(dy=-14, sy=1.03), 220), (P["tram_kiem"], dict(fx_shift=10, sx=1.04, sy=0.96), 80),
                        (P["tram_kiem"], dict(fx_shift=12), 140), (I, {}, 110)], 4),
    }
    meta = {"character": "swordsman-male", "cell": [CELL, CELL_H], "feet_y": FEET_Y, "scale_vs_source": round(S, 4),
            "draw_hint": "cell 768x640, feet y 620; idle (with raised blade) = 476 px, same scale as the k13 strip: draw the cell at hero_height_px * 640/476 tall",
            "alpha_clean": info, "actions": {}}
    for name, (seq, hit) in ks.items():
        frames = [place(p, S, **kw) for p, kw, _ in seq]
        strip(frames).save(out / f"kiemsi_nam_{name}_{len(frames)}f.png", optimize=True)
        meta["actions"][name] = {"file": f"kiemsi_nam_{name}_{len(frames)}f.png", "frames": len(frames),
                                 "durations_ms": [d for _, _, d in seq], "hit_frame": hit, "total_ms": sum(d for _, _, d in seq),
                                 "qc": [mc.qc_cell(f) for f in frames]}
    idle_frames = [place(I, S), place(I, S, sx=1.01, sy=0.985)]
    strip(idle_frames).save(out / "kiemsi_nam_idle_2f.png", optimize=True)
    meta["actions"]["idle"] = {"file": "kiemsi_nam_idle_2f.png", "frames": 2, "durations_ms": [600, 600], "hit_frame": None,
                               "qc": [mc.qc_cell(f) for f in idle_frames]}
    report["kiemsi_nam"] = meta
    # ---------------- Goblin cận chiến ----------------
    im = np.asarray(Image.open(src / "goblin-melee-key-poses.png").convert("RGBA"))
    im, info = clean_alpha(im); comps = components(im[..., 3])
    boxes = []
    for m in comps:
        ys, xs = np.nonzero(m); boxes.append((int(ys.min() > 620), xs.min(), m))
    boxes.sort(key=lambda b: (b[0], b[1]))
    gnames = ["idle", "windup", "swing", "hit"]
    G = {n: crop_pose(im, b[2]) for n, b in zip(gnames, boxes)}
    (out / "poses_goblin").mkdir(exist_ok=True)
    for n, p in G.items(): p.save(out / "poses_goblin" / f"{n}.png")
    gs = 500 / G["idle"].height
    gseq = {
        "idle": ([(G["idle"], {}, 500), (G["idle"], dict(sx=1.012, sy=0.985), 500)], None),
        "attack": ([(G["idle"], {}, 80), (G["windup"], dict(lean=-3), 120), (G["windup"], dict(lean=-6, sx=0.98, sy=1.02), 140),
                    (G["swing"], dict(fx_shift=10, sx=1.04, sy=0.96), 60), (G["swing"], dict(fx_shift=14), 140), (G["idle"], {}, 100)], 3),
        "hit": ([(G["hit"], dict(fx_shift=-10), 90), (G["hit"], dict(fx_shift=-6, sx=0.98, sy=1.02), 110), (G["idle"], {}, 120)], None),
    }
    gmeta = {"character": "goblin-melee", "cell": [CELL, CELL_H], "feet_y": FEET_Y, "scale_vs_source": round(gs, 4),
             "draw_hint": "idle goblin = 500 px tall in a 768x640 cell, feet at y 620", "alpha_clean": info, "actions": {}}
    # 6-cell combined strip in the hero order style: [idle1, idle2, windup, swing, swing_follow, hit]
    combo = [place(G["idle"], gs), place(G["idle"], gs, sx=1.012, sy=0.985), place(G["windup"], gs, lean=-5),
             place(G["swing"], gs, fx_shift=10, sx=1.04, sy=0.96), place(G["swing"], gs, fx_shift=14), place(G["hit"], gs, fx_shift=-8)]
    strip(combo).save(out / "goblin_melee_strip_6f.png", optimize=True)
    gmeta["strip6"] = {"file": "goblin_melee_strip_6f.png", "order": ["idle1", "idle2", "windup", "swing", "swing_follow", "hit"],
                       "qc": [mc.qc_cell(f) for f in combo]}
    for name, (seq, hit) in gseq.items():
        frames = [place(p, gs, **kw) for p, kw, _ in seq]
        strip(frames).save(out / f"goblin_melee_{name}_{len(frames)}f.png", optimize=True)
        gmeta["actions"][name] = {"file": f"goblin_melee_{name}_{len(frames)}f.png", "frames": len(frames),
                                  "durations_ms": [d for _, _, d in seq], "hit_frame": hit, "total_ms": sum(d for _, _, d in seq),
                                  "qc": [mc.qc_cell(f) for f in frames]}
    report["goblin_melee"] = gmeta
    (out / "animations.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    # GIF previews on the forest tile colour, at native timing
    BG = (78, 92, 64)
    for char, m in report.items():
        for name, a in m["actions"].items():
            S_ = Image.open(out / a["file"]); fr = []
            for i in range(a["frames"]):
                b = Image.new("RGBA", (CELL, CELL_H), BG + (255,)); b.alpha_composite(S_.crop((i * CELL, 0, (i + 1) * CELL, CELL_H)))
                d = ImageDraw.Draw(b); d.line([(0, FEET_Y), (CELL, FEET_Y)], fill=(255, 220, 0, 90))
                if a["hit_frame"] == i: d.text((10, 10), "HIT", fill=(255, 80, 80))
                fr.append(b.convert("RGB").resize((CELL // 2, CELL_H // 2)))
            fr[0].save(out / f"preview_{char}_{name}.gif", save_all=True, append_images=fr[1:], duration=a["durations_ms"], loop=0)
    print(json.dumps({c: {n: (a["frames"], max(q["edge_band_alpha_pct"] for q in a["qc"]), max(q["opaque_components"] for q in a["qc"]),
                              [q["feet_y"] for q in a["qc"]]) for n, a in m["actions"].items()} for c, m in report.items()}))


if __name__ == "__main__":
    main()
