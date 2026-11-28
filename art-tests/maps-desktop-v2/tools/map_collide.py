"""Desktop maps v2: Upscayl 4x master -> 2800x2800 game image (graded toward ART_DIRECTION) + collision grid 100x100
(RLE, same format as FOREST_GRID in index.html) + zones (safe / elite / boss / portal) + debug overlays.
Usage: python map_collide.py <maps_v2_dir>
"""
import sys, json, math
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
sys.path.insert(0, str(Path(__file__).parent))
import maps_upscale_grade as mg
Image.MAX_IMAGE_PIXELS = None

WORLD = 2800
GRID = 100
MAPS = {
    "m1": {"id": "rung_xanh_v2", "name": "Rừng Xanh (thế giới fantasy)", "grade": 0.66},
    "m2": {"id": "hoang_mac_nui_lua", "name": "Hoang Mạc Núi Lửa", "grade": 0.85},
    "m3": {"id": "hang_pha_le", "name": "Hang Pha Lê", "grade": 0.85},
    "m4": {"id": "bang_tuyet", "name": "Vương Quốc Băng Tuyết", "grade": 0.9},
    "m5": {"id": "lang_khoi_dau", "name": "Làng Khởi Đầu", "grade": 0.7},
}


def lab(im):
    L = mg.to_oklab(im.astype(np.float32) / 255)
    return L[..., 0], np.hypot(L[..., 1], L[..., 2]), np.degrees(np.arctan2(L[..., 2], L[..., 1])) % 360


# bridges / stairs the colour rules cannot see (stone arches, dark planks): opened by hand, normalised (cx, cy, w, h)
BRIDGES = {}   # replaced by connect_regions(): cheapest crossing = where the art has a bridge / ford
BUSY_PCT = {"m1": 78, "m2": 75, "m3": 75, "m4": 80, "m5": 70}


def obstacles(key, im):
    return _obstacles(key, im)


def _obstacles(key, im):
    """Pixels that are obstacles: water, lava, cliffs/rock masses, tree canopies, buildings, crystals.
    Everything else (grass, dirt road, sand, snow field, cave floor, plaza, wooden bridges) is walkable."""
    L, C, h = lab(im)
    Lb = ndi.gaussian_filter(L, 2.5)                     # blur away grass/snow brush strokes first
    tex = np.sqrt(np.clip(ndi.gaussian_filter(Lb * Lb, 5) - ndi.gaussian_filter(Lb, 5) ** 2, 0, None))
    bridge = (h > 40) & (h < 85) & (C > 0.05) & (C < 0.17) & (L > 0.35) & (L < 0.72)
    water = (h > 195) & (h < 265) & (C > 0.06) & (L < 0.86)
    dark = L < 0.40
    busy = tex > np.percentile(tex, BUSY_PCT.get(key, 80))                                   # cliffs, rock piles, tree clusters, roofs: high local contrast
    canopy = (h > 110) & (h < 175) & (L < 0.58) & (C > 0.05)
    pinktree = ((h > 330) | (h < 15)) & (C > 0.08) & (L > 0.55) & (tex > 0.05)
    if key == "m1":
        return water | canopy | pinktree | (busy & ~((h > 50) & (h < 105) & (C < 0.16)))
    if key == "m2":
        lava = (C > 0.15) & (h > 15) & (h < 85) & (L > 0.60)
        return lava | dark | busy
    if key == "m3":
        crystal = (C > 0.11) & ((h > 250) | (h < 20) | ((h > 190) & (h < 250)))
        return water | crystal | dark | busy
    if key == "m4":
        ice = (h > 200) & (h < 265) & (C > 0.09)
        pine = (h > 110) & (h < 200) & (L < 0.55)
        return ice | pine | (busy & (L < 0.85)) | (L < 0.45)
    if key == "m5":
        roof = (h > 250) & (h < 300) & (C > 0.06)
        paving = ndi.binary_opening((C < 0.05) & (L > 0.66), iterations=3)
        return (water | canopy | pinktree | roof | dark | busy) & ~paving
    raise KeyError(key)


def connect_regions(open_g, frac, min_cells=40):
    """Join every walkable region to the biggest one through the cheapest blocked cells (cost grows with the obstacle
    fraction), so crossings land on the painted bridges / fords; the path is opened 2 cells wide."""
    import heapq
    links = []
    while True:
        lab_, n = ndi.label(open_g)
        if n <= 1: break
        sz = ndi.sum(open_g, lab_, range(1, n + 1)); main = int(np.argmax(sz)) + 1
        others = [i + 1 for i in range(n) if i + 1 != main and sz[i] >= min_cells]
        if not others: break
        src = lab_ == others[0]; H, W = open_g.shape
        cost = np.where(open_g, 0.2, 1 + 20 * frac ** 2)
        dist = np.full((H, W), np.inf); prev = {}; pq = []
        for y, x in zip(*np.nonzero(src)): dist[y, x] = 0; heapq.heappush(pq, (0.0, y, x))
        goal = None
        while pq:
            d0, y, x = heapq.heappop(pq)
            if d0 > dist[y, x]: continue
            if lab_[y, x] == main: goal = (y, x); break
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = y + dy, x + dx
                if 0 < ny < H - 1 and 0 < nx < W - 1 and d0 + cost[ny, nx] < dist[ny, nx]:
                    dist[ny, nx] = d0 + cost[ny, nx]; prev[(ny, nx)] = (y, x); heapq.heappush(pq, (dist[ny, nx], ny, nx))
        if goal is None: open_g[src] = False; continue
        cur = goal; path = []
        while cur in prev: path.append(cur); cur = prev[cur]
        for y, x in path: open_g[y, x] = True; open_g[y, min(W - 2, x + 1)] = True; open_g[min(H - 2, y + 1), x] = True
        links.append(len([1 for y, x in path if frac[y, x] >= 0.35]))
    return open_g, links


def rle(grid):
    rows = []
    for r in range(grid.shape[0]):
        cols = np.nonzero(grid[r])[0]; parts = []
        if len(cols):
            s = p = cols[0]
            for c in list(cols[1:]) + [None]:
                if c is not None and c == p + 1: p = c; continue
                parts.append(f"{s}" if s == p else f"{s}-{p}")
                if c is not None: s = p = c
        rows.append(",".join(parts))
    return rows


def zones(open_grid):
    """safe = open cell furthest from obstacles near the bottom-centre; boss = biggest open blob far from safe; elite
    and portal = far apart open points. Normalised world coords (0..1)."""
    dist = ndi.distance_transform_edt(open_grid)
    H, W = open_grid.shape; yy, xx = np.mgrid[:H, :W]
    def best(score):
        s = np.where(open_grid, score, -1e9); i = np.unravel_index(np.argmax(s), s.shape); return i
    safe = best(dist + 0.8 * yy / H * 10 - 0.6 * np.abs(xx - W / 2) / W * 10)
    d_safe = np.hypot(yy - safe[0], xx - safe[1])
    boss = best(dist * 1.5 + d_safe * 0.15)
    d_boss = np.hypot(yy - boss[0], xx - boss[1])
    elite = best(dist + np.minimum(d_safe, d_boss) * 0.2)
    portal = best(dist * 0.6 + np.minimum(d_safe, np.minimum(d_boss, np.hypot(yy - elite[0], xx - elite[1]))) * 0.1 - d_safe * 0.05)
    f = lambda p, r: {"x": round((p[1] + 0.5) / W, 3), "y": round((p[0] + 0.5) / H, 3), "r": round(min(r, dist[p]) / W, 3)}
    return {"safe": f(safe, 8), "elite": f(elite, 10), "boss": f(boss, 10), "portal": f(portal, 3)}


def main():
    d = Path(sys.argv[1]); (d / "game").mkdir(exist_ok=True); (d / "debug").mkdir(exist_ok=True); out = {}
    for key, cfg in MAPS.items():
        src = np.asarray(Image.open(d / "src" / f"{key}.png").convert("RGB"))
        # ---- collision from the source (1254 px, 12.5 px per cell) ----
        ob = obstacles(key, src)
        ob = ndi.binary_opening(ob, iterations=1)
        L_, C_, h_ = lab(src)
        brg = (h_ > 40) & (h_ < 85) & (C_ > 0.05) & (C_ < 0.17) & (L_ > 0.35) & (L_ < 0.72)
        brg = ndi.binary_opening(brg, iterations=2)
        ob &= ~brg
        H, W = ob.shape; cs = H / GRID
        frac = np.array([[ob[int(r * cs):int((r + 1) * cs), int(c * cs):int((c + 1) * cs)].mean() for c in range(GRID)] for r in range(GRID)])
        open_g = frac < 0.35
        for (bx, by, bw, bh) in BRIDGES.get(key, []):
            open_g[int((by - bh / 2) * GRID):int((by + bh / 2) * GRID) + 1, int((bx - bw / 2) * GRID):int((bx + bw / 2) * GRID) + 1] = True
        open_g = ndi.binary_opening(open_g, iterations=1)          # drop single open specks inside obstacles
        lab_, n = ndi.label(open_g)
        if n:
            sz = ndi.sum(open_g, lab_, range(1, n + 1)); open_g = np.isin(lab_, 1 + np.nonzero(sz >= 40)[0])   # drop tiny pockets
        open_g[0, :] = open_g[-1, :] = open_g[:, 0] = open_g[:, -1] = False
        open_g, links = connect_regions(open_g, frac)
        blocked = ~open_g
        comp, ncomp = ndi.label(open_g)
        z = zones(open_g)
        # ---- game image: 4x master -> 2800 + grade ----
        big = Image.open(d / "up4" / f"{key}.png").convert("RGB").resize((WORLD, WORLD), Image.LANCZOS)
        mg.GROUND_CHROMA = cfg["grade"]
        g = Image.fromarray(mg.grade(np.asarray(big)))
        g.save(d / "game" / f"{cfg['id']}_2800.webp", quality=90, method=6)
        # ---- debug overlay ----
        ov = g.resize((1400, 1400)).convert("RGBA"); lay = Image.new("RGBA", ov.size); dr = ImageDraw.Draw(lay); c14 = 1400 / GRID
        for r in range(GRID):
            for c in range(GRID):
                if blocked[r, c]: dr.rectangle([c * c14, r * c14, (c + 1) * c14 - 1, (r + 1) * c14 - 1], fill=(255, 0, 0, 90))
        for name, col in (("safe", (60, 255, 60)), ("elite", (255, 200, 0)), ("boss", (255, 60, 255)), ("portal", (0, 230, 255))):
            p = z[name]; cx, cy, rr = p["x"] * 1400, p["y"] * 1400, max(10, p["r"] * 1400)
            dr.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], outline=col + (255,), width=4); dr.text((cx + 6, cy - 6), name, fill=col + (255,))
        ov.alpha_composite(lay); ov.convert("RGB").save(d / "debug" / f"{cfg['id']}_collision.jpg", quality=85)
        out[cfg["id"]] = {"name": cfg["name"], "image": f"game/{cfg['id']}_2800.webp", "world": [WORLD, WORLD], "grid": [GRID, GRID],
                          "cell_px": WORLD / GRID, "blocked_pct": round(100 * float(blocked.mean()), 1), "walkable_regions": int(ncomp),
                          "auto_crossings_cells": links, "zones": z, "grid_rle": rle(blocked)}
        print(key, cfg["id"], "blocked %.1f%%" % (100 * blocked.mean()), "regions", ncomp, "links", links, [int(v) for v in ndi.sum(open_g, comp, range(1, ncomp + 1))], flush=True)
    (d / "maps_collision.json").write_text(json.dumps(out, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
