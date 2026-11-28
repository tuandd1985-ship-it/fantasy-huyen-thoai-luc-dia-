"""Collision grids for the older Desktop maps (art-tests/maps-anh-do): world 2804x2244 (images already in
upscaled-x2), grid 100x80 exactly like FOREST_GRID. Obstacle rules reuse map_collide themes (union per map).
Usage: python map_collide_old.py <maps_old_dir> <upscaled_x2_dir>
"""
import sys, json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
sys.path.insert(0, str(Path(__file__).parent))
import map_collide as mc

GW, GH = 100, 80
# theme keys of map_collide._obstacles: m1 forest, m2 lava, m3 crystal cave, m4 snow, m5 village
MAPS = {
    "map_3": ("Rừng Xanh 3 (góc tuyết)", ["m1", "m4"]),
    "map_4": ("Băng Tuyết (sông băng)", ["m4"]),
    "map_5": ("Dung Nham (góc tuyết)", "path"),
    "hang1": ("Hang Pha Lê Xanh", "path"),
    "hang2": ("Hang Băng", "path"),
    "hang3": ("Hang Dung Nham", "path"),
    # arenas: walkable = the round floor (ellipse cx, cy, rx, ry) + the entrance stairs (cx, cy, w, h)
    "boss_bang": ("Đấu trường boss Băng", ("arena", (0.50, 0.45, 0.40, 0.31), (0.50, 0.86, 0.12, 0.16))),
    "bosslua": ("Đấu trường boss Lửa", ("arena", (0.50, 0.47, 0.39, 0.31), (0.50, 0.86, 0.12, 0.16))),
    "bossxuan": ("Đấu trường boss Xuân", ("arena", (0.50, 0.47, 0.41, 0.31), (0.50, 0.87, 0.12, 0.15))),
}


def path_walkable(im, key=""):
    """Cave / lava-field maps: the walkable tracks are lighter, smoother strips than their surroundings."""
    L, C, h = mc.lab(im)
    Lb = ndi.gaussian_filter(L, 3)
    rel = Lb - ndi.gaussian_filter(L, 30)
    tex = np.sqrt(np.clip(ndi.gaussian_filter(Lb * Lb, 5) - ndi.gaussian_filter(Lb, 5) ** 2, 0, None))
    lava = (C > 0.15) & (h > 15) & (h < 85) & (L > 0.60)
    water = (h > 195) & (h < 265) & (C > 0.08) if key != "hang2" else np.zeros_like(L, bool)   # ice cave is blue all over
    crystal = C > (0.16 if key in ("hang1", "hang2") else 0.24)
    w = (rel > 0.015) & (tex < np.percentile(tex, 65)) & ~lava & ~water & ~crystal
    return ndi.binary_closing(ndi.binary_opening(w, iterations=1), iterations=2)


def obstacles(themes, im):
    # each theme rule keeps its own thresholds; a pixel is walkable only if every theme says it is free
    o = np.zeros(im.shape[:2], bool)
    for t in themes: o |= mc._obstacles(t, im)
    return o


def main():
    d, up = Path(sys.argv[1]), Path(sys.argv[2]); (d / "debug").mkdir(exist_ok=True); out = {}
    for key, (name, themes) in MAPS.items():
        src = np.asarray(Image.open(d / "src" / f"{key}.png").convert("RGB")); H, W = src.shape[:2]
        cy, cx = H / GH, W / GW
        if isinstance(themes, tuple):          # arena
            (ex, ey, rx, ry), (sx_, sy_, sw, sh) = themes[1], themes[2]
            gy, gx = (np.mgrid[:GH, :GW] + 0.5); gx = gx / GW; gy = gy / GH
            open_g = (((gx - ex) / rx) ** 2 + ((gy - ey) / ry) ** 2 <= 1) | ((np.abs(gx - sx_) <= sw / 2) & (np.abs(gy - sy_) <= sh / 2))
            frac = (~open_g).astype(float)
        else:
            ob = ~path_walkable(src, key) if themes == "path" else ndi.binary_opening(obstacles(themes, src), iterations=1)
            frac = np.array([[ob[int(r * cy):int((r + 1) * cy), int(c * cx):int((c + 1) * cx)].mean() for c in range(GW)] for r in range(GH)])
            open_g = frac < (0.72 if themes == "path" else 0.35)
            if themes != "path": open_g = ndi.binary_opening(open_g, iterations=1)
        lab_, n = ndi.label(open_g)
        if n:
            sz = ndi.sum(open_g, lab_, range(1, n + 1)); open_g = np.isin(lab_, 1 + np.nonzero(sz >= 30)[0])
        open_g[0, :] = open_g[-1, :] = open_g[:, 0] = open_g[:, -1] = False
        open_g, links = mc.connect_regions(open_g, frac, min_cells=30)
        blocked = ~open_g; comp, ncomp = ndi.label(open_g)
        z = mc.zones(open_g)
        if isinstance(themes, tuple):
            (ex, ey, rx, ry), (sx_, sy_, sw, sh) = themes[1], themes[2]
            z = {"safe": {"x": sx_, "y": round(sy_ - sh * 0.25, 3), "r": 0.04}, "boss": {"x": ex, "y": ey, "r": round(rx * 0.35, 3)},
                 "elite": {"x": round(ex - rx * 0.6, 3), "y": ey, "r": 0.06}, "portal": {"x": sx_, "y": round(sy_ + sh * 0.3, 3), "r": 0.03}}
        img = Image.open(up / f"{key}_x2.webp").convert("RGB")
        ov = img.resize((1402, 1122)).convert("RGBA"); lay = Image.new("RGBA", ov.size); dr = ImageDraw.Draw(lay)
        sx, sy = 1402 / GW, 1122 / GH
        for r in range(GH):
            for c in range(GW):
                if blocked[r, c]: dr.rectangle([c * sx, r * sy, (c + 1) * sx - 1, (r + 1) * sy - 1], fill=(255, 0, 0, 90))
        for nm, col in (("safe", (60, 255, 60)), ("elite", (255, 200, 0)), ("boss", (255, 60, 255)), ("portal", (0, 230, 255))):
            p = z[nm]; px, py, rr = p["x"] * 1402, p["y"] * 1122, max(10, p["r"] * 1402)
            dr.ellipse([px - rr, py - rr, px + rr, py + rr], outline=col + (255,), width=4); dr.text((px + 6, py - 6), nm, fill=col + (255,))
        ov.alpha_composite(lay); ov.convert("RGB").save(d / "debug" / f"{key}_collision.jpg", quality=85)
        out[key] = {"name": name, "image": f"../maps-anh-do/upscaled-x2/{key}_x2.webp", "world": [2804, 2244], "grid": [GW, GH],
                    "cell_px": [28.04, 28.05], "themes": themes, "blocked_pct": round(100 * float(blocked.mean()), 1),
                    "walkable_regions": int(ncomp), "auto_crossings_cells": links, "zones": z, "grid_rle": mc.rle(blocked)}
        print(key, "blocked %.1f%%" % (100 * blocked.mean()), "regions", ncomp, "links", links, flush=True)
    (d / "maps_collision_old.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
