"""Pháp Sư motion strip, step 2: animate the rig (body + staff layers split from the cleaned reference) into
6 strip frames [idle1, idle2, run1, run2, cast1, cast2] and 2 skill poses, fit into 420x500 cells (feet y 487,
same as k13-k18), QC each cell, write strip 2520x500 + skill PNGs + contact sheets + GIF previews.
Usage: python mage_anim_compose.py <rig_dir_male> <rig_dir_female> <out_dir>
"""
import sys, json, math, subprocess, shutil
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage as ndi

CELL_W, CELL_H, BASE_Y, MARGIN = 420, 500, 487, 8
GENDER = {
    "male": {"hand": (398, 455), "orb": (466, 190, 58), "color": (90, 175, 255), "hem": 585},
    "female": {"hand": (405, 425), "orb": (496, 140, 62), "color": (185, 115, 255), "hem": 590},
}
# frame parameters: body lean (deg, + = top leans right), bob (px up), squash (sy), stride (px feet apart),
# staff rotation about the hand (deg, + = clockwise = orb swings forward/right), glow level, effect kind
FRAMES = {
    "idle1": dict(lean=0, bob=0, sy=1.0, stride=0, staff=0, glow=0.25, fx=None),
    "idle2": dict(lean=0, bob=0, sy=0.982, stride=0, staff=1.5, glow=0.35, fx=None),
    "run1": dict(lean=3, bob=0, sy=0.985, stride=10, staff=-6, glow=0.25, fx=None),
    "run2": dict(lean=3, bob=12, sy=1.01, stride=-6, staff=-10, glow=0.25, fx=None),
    "cast1": dict(lean=-2, bob=8, sy=1.0, stride=0, staff=-16, glow=0.9, fx="charge"),
    "cast2": dict(lean=3, bob=0, sy=0.99, stride=6, staff=12, glow=1.0, fx="burst"),
    "skill_charge": dict(lean=-2, bob=10, sy=1.0, stride=6, staff=-18, glow=1.0, fx="skill_charge"),
    "skill_release": dict(lean=6, bob=0, sy=0.985, stride=14, staff=40, glow=1.0, fx="skill_release"),
}
STRIP = ["idle1", "idle2", "run1", "run2", "cast1", "cast2"]
PAD = 260   # work canvas padding around the reference


def premul_transform(im, fn):
    """Apply a PIL geometric transform on premultiplied alpha (no dark fringes), return straight RGBA."""
    a = np.asarray(im).astype(float) / 255
    pm = np.dstack([a[..., :3] * a[..., 3:4], a[..., 3:4]])
    out = fn(Image.fromarray((pm * 255).round().astype(np.uint8), "RGBA"))
    b = np.asarray(out).astype(float) / 255
    rgb = np.where(b[..., 3:4] > 1e-4, b[..., :3] / np.maximum(b[..., 3:4], 1e-4), 0)
    return Image.fromarray((np.clip(np.dstack([rgb, b[..., 3:4]]), 0, 1) * 255).round().astype(np.uint8), "RGBA")


def rot(im, deg, center):
    return premul_transform(im, lambda x: x.rotate(-deg, resample=Image.BICUBIC, center=center))


def glow_layer(size, cx, cy, radius, color, strength):
    H, W = size[1], size[0]
    yy, xx = np.mgrid[:H, :W]
    d2 = ((xx - cx) ** 2 + (yy - cy) ** 2) / (radius ** 2)
    a = np.clip(strength * np.exp(-d2 * 2.2), 0, 1)
    core = np.clip(strength * np.exp(-d2 * 9), 0, 1)
    rgb = np.array(color, float)[None, None] * (1 - core[..., None]) + 255 * core[..., None]
    return Image.fromarray(np.dstack([rgb, a * 255]).round().astype(np.uint8), "RGBA")


def rays_layer(size, cx, cy, length, color, n=10, width=10, angle0=0, spread=360, strength=0.9):
    L = Image.new("RGBA", size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for i in range(n):
        ang = math.radians(angle0 - spread / 2 + spread * (i + 0.5) / n)
        ln = length * (0.6 + 0.4 * ((i * 7) % 5) / 4)
        x2, y2 = cx + ln * math.cos(ang), cy + ln * math.sin(ang)
        px, py = -math.sin(ang) * width / 2, math.cos(ang) * width / 2
        d.polygon([(cx + px, cy + py), (cx - px, cy - py), (x2, y2)], fill=tuple(color) + (int(200 * strength),))
    return L.filter(ImageFilter.GaussianBlur(3))


def aura_layer(alpha_img, color, grow=14, strength=0.55):
    A = np.asarray(alpha_img.split()[3]).astype(float) / 255
    g = ndi.gaussian_filter(ndi.binary_dilation(A > 0.5, iterations=grow).astype(float), grow / 2)
    a = np.clip(g * strength, 0, 1) * (1 - A * 0.0)
    rgb = np.ones(A.shape + (3,)) * np.array(color, float)
    return Image.fromarray(np.dstack([rgb, a * 255]).round().astype(np.uint8), "RGBA")


def ring_layer(size, cx, cy, rx, ry, color, strength=0.8):
    L = Image.new("RGBA", size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    for k, (w, a) in enumerate([(10, 0.35), (4, 0.9)]):
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=tuple(color) + (int(255 * a * strength),), width=w)
    d.ellipse([cx - rx * 0.7, cy - ry * 0.7, cx + rx * 0.7, cy + ry * 0.7], outline=tuple(color) + (int(180 * strength),), width=3)
    for i in range(12):
        t = 2 * math.pi * i / 12
        x, y = cx + rx * 0.85 * math.cos(t), cy + ry * 0.85 * math.sin(t)
        d.ellipse([x - 5, y - 3, x + 5, y + 3], fill=(255, 255, 255, int(220 * strength)))
    return L.filter(ImageFilter.GaussianBlur(1.2))


def largest_component(im, link_px=2):
    """Pipeline rule: keep the largest opaque component plus anything within link_px of it (soft edges)."""
    a = np.asarray(im).copy(); A = a[..., 3]
    lab, n = ndi.label(A > 16)
    if n <= 1: return im
    sz = ndi.sum(np.ones_like(A), lab, range(1, n + 1)); main = lab == (int(np.argmax(sz)) + 1)
    keep = ndi.binary_dilation(main, iterations=link_px)
    lab2 = np.unique(lab[keep & (lab > 0)]); ok = np.isin(lab, lab2) | (A <= 16)
    a[~ok, 3] = 0
    return Image.fromarray(a)


def frame(body, staff, gd, f):
    """Render one frame on a padded work canvas; returns RGBA and the feet point."""
    cfg = GENDER[gd]; W, H = body.size
    CW, CH = W + 2 * PAD, H + 2 * PAD
    feet = (PAD + W * 0.47, PAD + H - 12)
    b = Image.new("RGBA", (CW, CH)); b.alpha_composite(body, (PAD, PAD))
    s = Image.new("RGBA", (CW, CH)); s.alpha_composite(staff, (PAD, PAD))
    hand = (PAD + cfg["hand"][0], PAD + cfg["hand"][1])
    orb = (PAD + cfg["orb"][0], PAD + cfg["orb"][1])
    # stride: shift the boots band (below the robe hem) left/right per side
    if f["stride"]:
        a = np.asarray(b).copy(); y0 = PAD + cfg["hem"]; mid = int(feet[0])
        band = a[y0:].copy(); a[y0:] = 0
        left, right = band.copy(), band.copy(); left[:, mid:] = 0; right[:, :mid] = 0
        a[y0:] = np.maximum(a[y0:], np.roll(left, -f["stride"], 1))
        nz = np.roll(right, f["stride"], 1); m_ = nz[..., 3] > a[y0:][..., 3]; a[y0:][m_] = nz[m_]
        b = Image.fromarray(a)
    # staff rotation about the hand (hand travels with the staff layer)
    if f["staff"]:
        s = rot(s, f["staff"], hand)
        r = math.radians(f["staff"]); dx, dy = orb[0] - hand[0], orb[1] - hand[1]
        orb = (hand[0] + dx * math.cos(r) - dy * math.sin(r), hand[1] + dx * math.sin(r) + dy * math.cos(r))
    char = Image.new("RGBA", (CW, CH)); char.alpha_composite(b); char.alpha_composite(s)
    # squash about the feet, then lean about the feet, then bob
    if f["sy"] != 1.0:
        sy = f["sy"]; sx = 1 + (1 - sy) * 0.4
        char = premul_transform(char, lambda x: x.transform(x.size, Image.AFFINE,
                                (1 / sx, 0, feet[0] - feet[0] / sx, 0, 1 / sy, feet[1] - feet[1] / sy), resample=Image.BICUBIC))
        orb = (feet[0] + (orb[0] - feet[0]) * sx, feet[1] + (orb[1] - feet[1]) * sy)
    if f["lean"]:
        char = rot(char, f["lean"], feet)
        r = math.radians(f["lean"]); dx, dy = orb[0] - feet[0], orb[1] - feet[1]
        orb = (feet[0] + dx * math.cos(r) - dy * math.sin(r), feet[1] + dx * math.sin(r) + dy * math.cos(r))
    if f["bob"]:
        ch2 = Image.new("RGBA", (CW, CH)); ch2.alpha_composite(char, (0, -f["bob"])); char = ch2; orb = (orb[0], orb[1] - f["bob"])
    char = largest_component(char, link_px=0)
    col = cfg["color"]; R = cfg["orb"][2]
    out = Image.new("RGBA", (CW, CH))
    fx = f["fx"]
    if fx == "skill_charge":
        out.alpha_composite(ring_layer((CW, CH), feet[0], feet[1] - 4, 205, 50, col))
        out.alpha_composite(aura_layer(char, col, grow=16, strength=0.6))
    if fx == "skill_release":
        out.alpha_composite(aura_layer(char, col, grow=10, strength=0.4))
    out.alpha_composite(char)
    if f["glow"]:
        out.alpha_composite(glow_layer((CW, CH), orb[0], orb[1], R * (1.6 + 1.2 * f["glow"]), col, 0.55 * f["glow"]))
    if fx == "charge":
        out.alpha_composite(rays_layer((CW, CH), orb[0], orb[1], R * 2.2, col, n=8, width=8, strength=0.6))
    if fx == "burst":
        out.alpha_composite(rays_layer((CW, CH), orb[0], orb[1], R * 3.0, col, n=9, width=14, angle0=-10, spread=110, strength=0.85))
        out.alpha_composite(glow_layer((CW, CH), orb[0] + R * 1.2, orb[1], R * 1.8, col, 0.7))
    if fx == "skill_charge":
        out.alpha_composite(rays_layer((CW, CH), orb[0], orb[1], R * 3.2, col, n=14, width=10, strength=0.8))
        out.alpha_composite(glow_layer((CW, CH), orb[0], orb[1], R * 3.4, col, 0.75))
    if fx == "skill_release":
        out.alpha_composite(rays_layer((CW, CH), orb[0], orb[1], R * 5.0, col, n=11, width=22, angle0=-5, spread=70, strength=0.95))
        out.alpha_composite(glow_layer((CW, CH), orb[0] + R * 2.0, orb[1] + 5, R * 2.8, col, 0.85))
    out.char_alpha = np.asarray(char)[..., 3]   # character only, for fitting (effects may fade at the border)
    return out, feet


def fade_edges(a, margin):
    """Alpha ramps to 0 over `margin` px at the cell border (effects only; QC asserts the character never gets there)."""
    H, W = a.shape[:2]
    yy, xx = np.mgrid[:H, :W]
    d = np.minimum.reduce([xx, yy, W - 1 - xx, H - 1 - yy]).astype(float)
    k = np.clip((d - 5) / margin, 0, 1)   # exactly 0 in the 5 px border band
    a = a.copy(); a[..., 3] = (a[..., 3] * k).round().astype(np.uint8); return a


def drop_small_islands(cell, max_px=200):
    """Cell-level largest-component pass: opaque islands (alpha>128) smaller than max_px that are not the main body
    (e.g. a staff tip that separates after downscaling) are removed together with their soft edge."""
    a = np.asarray(cell).copy(); A = a[..., 3]
    lab, n = ndi.label(A > 128)
    if n <= 1: return cell
    sz = ndi.sum(np.ones_like(A), lab, range(1, n + 1)); main = int(np.argmax(sz)) + 1
    for j in range(1, n + 1):
        if j != main and sz[j - 1] < max_px:
            reg = ndi.binary_dilation(lab == j, iterations=2) & ~ndi.binary_dilation(lab == main, iterations=1)
            a[reg, 3] = 0
    return Image.fromarray(a)


def to_cell(im, feet, scale, cx_cell):
    W, H = im.size
    sm = premul_transform(im, lambda x: x.resize((round(W * scale), round(H * scale)), Image.LANCZOS))
    cell = Image.new("RGBA", (CELL_W, CELL_H))
    cell.alpha_composite(sm, (round(cx_cell - feet[0] * scale), round(BASE_Y - feet[1] * scale)))
    return cell


def qc_cell(cell, char_alpha=None):
    A = np.asarray(cell)[..., 3]
    edge = np.zeros_like(A, bool); edge[:4] = edge[-4:] = True; edge[:, :4] = edge[:, -4:] = True
    lab, n = ndi.label(A > 128)
    sizes = ndi.sum(np.ones_like(A), lab, range(1, n + 1)) if n else []
    main = int(max(sizes)) if n else 0
    stray = int(sum(1 for s in sizes if s < main and s >= 30))
    ys, xs = np.nonzero(A > 128)
    return {"edge_band_alpha_pct": round(100 * float((A[edge] > 0).mean()), 3), "edge_band_max_alpha": int(A[edge].max()),
            "opaque_components": int(n), "stray_opaque_islands_ge30px": stray, "main_component_px": main,
            "bbox": [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())] if len(xs) else None,
            "feet_y": int(ys.max()) if len(ys) else None}


def main():
    rig = {"male": Path(sys.argv[1]), "female": Path(sys.argv[2])}; out = Path(sys.argv[3]); out.mkdir(parents=True, exist_ok=True)
    report = {}
    for gd in ("male", "female"):
        body = Image.open(rig[gd] / f"{gd}_body.png").convert("RGBA"); staff = Image.open(rig[gd] / f"{gd}_staff.png").convert("RGBA")
        rend = {k: frame(body, staff, gd, f) for k, f in FRAMES.items()}
        # one scale + one x position for the 6 strip frames (no jitter), from the union bbox of opaque pixels
        target_h = 445 / body.size[1]
        xs0, xs1 = [], []
        for k in STRIP:
            im, feet = rend[k]; a = im.char_alpha; ys, xs = np.nonzero(a > 128)
            xs0.append(xs.min() - feet[0]); xs1.append(xs.max() - feet[0])
        span = max(xs1) - min(xs0)
        scale = min(target_h, (CELL_W - 2 * 14) / span)
        cx_cell = CELL_W / 2 - (min(xs0) + max(xs1)) / 2 * scale
        cells = {}
        for k in STRIP:
            im, feet = rend[k]; cells[k] = drop_small_islands(Image.fromarray(fade_edges(np.asarray(to_cell(im, feet, scale, cx_cell)), MARGIN)))
        # skill poses: own fit (bigger effects), same feet line
        for k in ("skill_charge", "skill_release"):
            im, feet = rend[k]; a = im.char_alpha; ys, xs = np.nonzero(a > 128)
            sc = min(target_h, (CELL_W - 28) / (xs.max() - xs.min()), (BASE_Y - 14) / (feet[1] - ys.min()))
            cx = CELL_W / 2 - ((xs.min() + xs.max()) / 2 - feet[0]) * sc
            cells[k] = drop_small_islands(Image.fromarray(fade_edges(np.asarray(to_cell(im, feet, sc, cx)), MARGIN)))
        strip = Image.new("RGBA", (CELL_W * 6, CELL_H))
        for i, k in enumerate(STRIP): strip.alpha_composite(cells[k], (i * CELL_W, 0))
        tag = "nam" if gd == "male" else "nu"
        strip.save(out / f"mage_{tag}_strip_2520x500.png", optimize=True)
        for k in ("skill_charge", "skill_release"): cells[k].save(out / f"mage_{tag}_{k}_420x500.png", optimize=True)
        report[gd] = {"strip_scale": round(scale, 4), "cells": {k: qc_cell(cells[k]) for k in cells}}
        # contact sheet on 3 backgrounds + GIF preview of the strip cycle
        rows = []
        for bgc in ((30, 30, 30), (255, 255, 255), (92, 103, 80)):
            r = Image.new("RGBA", (CELL_W * 8, CELL_H), bgc + (255,))
            for i, k in enumerate(STRIP + ["skill_charge", "skill_release"]): r.alpha_composite(cells[k], (i * CELL_W, 0))
            d = ImageDraw.Draw(r)
            for i in range(1, 8): d.line([(i * CELL_W, 0), (i * CELL_W, CELL_H)], fill=(255, 0, 0, 255), width=1)
            rows.append(r.convert("RGB"))
        sheet = Image.new("RGB", (CELL_W * 8, CELL_H * 3)); [sheet.paste(r, (0, i * CELL_H)) for i, r in enumerate(rows)]
        sheet.resize((sheet.width // 2, sheet.height // 2), Image.LANCZOS).save(out / f"mage_{tag}_contact.jpg", quality=90, subsampling=0)
        seq = ["idle1", "idle2"] * 2 + ["run1", "run2"] * 3 + ["cast1", "cast2", "cast2"]
        gif = [Image.alpha_composite(Image.new("RGBA", (CELL_W, CELL_H), (92, 103, 80, 255)), cells[k]).convert("RGB") for k in seq]
        gif[0].save(out / f"mage_{tag}_preview.gif", save_all=True, append_images=gif[1:], duration=[260] * 4 + [140] * 6 + [180, 260, 260], loop=0)
    (out / "qc.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    for gd, r in report.items():
        for k, q in r["cells"].items():
            print(gd, k, q["edge_band_alpha_pct"], q["edge_band_max_alpha"], q["opaque_components"], q["stray_opaque_islands_ge30px"], q["bbox"])


if __name__ == "__main__":
    main()
