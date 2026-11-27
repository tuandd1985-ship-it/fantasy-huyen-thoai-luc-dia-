"""Before/after sheets for step A. Usage: python hero_edge_compare.py <stepA_dir>"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

BGS = {"dark": (24, 26, 32), "light": (238, 238, 238), "grass": (70, 110, 60), "map": (86, 128, 70)}


def on(im, c):
    b = Image.new("RGBA", im.size, c + (255,)); b.alpha_composite(im); return b.convert("RGB")


def edge_crops(a, n=3, size=72):
    """pick n crop centres on the silhouette edge with the most change (deterministic)."""
    A = a[..., 3]
    e = ndi.binary_dilation(A == 0, iterations=2) & (A > 0)
    ys, xs = np.nonzero(e)
    h, w = A.shape
    picks = []
    for frac in (0.18, 0.5, 0.82):  # top / middle / bottom of silhouette edge
        ty = int(h * frac); i = np.argmin(np.abs(ys - ty) + (xs > w // 2) * 0)
        cy, cx = ys[i], xs[i]
        y0 = int(np.clip(cy - size // 2, 0, h - size)); x0 = int(np.clip(cx - size // 2, 0, w - size))
        picks.append((x0, y0, x0 + size, y0 + size))
    return picks


def main():
    d = Path(sys.argv[1]); out = d / "compare"; out.mkdir(exist_ok=True)
    names = sorted(p.stem for p in (d / "cleaned_png").glob("*.png"))
    for name in names:
        o = Image.open(d / "original" / f"{name}.png").convert("RGBA")
        c = Image.open(d / "cleaned_webp_q90" / f"{name}.webp").convert("RGBA")
        th = 360; sc = th / o.height
        ow, oh = int(o.width * sc), th
        cols = list(BGS)
        W = 2 * len(cols) * (ow + 8) + 8; H = th + 40 + 3 * 300 + 30
        S = Image.new("RGB", (W, H), "white"); dr = ImageDraw.Draw(S)
        x = 8
        for bg in cols:
            for lab, im in (("TRUOC", o), ("SAU", c)):
                S.paste(on(im, BGS[bg]).resize((ow, oh), Image.LANCZOS), (x, 24))
                dr.text((x, 6), f"{lab} - nen {bg}", fill=(0, 0, 0)); x += ow + 8
        # 4x zoom edge crops, before/after on dark + light
        y = th + 50
        for box in edge_crops(np.asarray(o)):
            x = 8
            for bg in ("dark", "light"):
                for lab, im in (("TRUOC", o), ("SAU", c)):
                    S.paste(on(im.crop(box), BGS[bg]).resize((288, 288), Image.NEAREST), (x, y))
                    dr.text((x + 4, y + 4), f"{lab} x4 {bg}", fill=(255, 255, 0) if bg == "dark" else (0, 0, 0)); x += 296
            y += 300
        S.save(out / f"{name}_compare.jpg", quality=90)
    # overview: all 6 at game scale (~150 px) on map green
    tiles = []
    for name in names:
        for f in (d / "original" / f"{name}.png", d / "cleaned_webp_q90" / f"{name}.webp"):
            im = Image.open(f).convert("RGBA"); s = 150 / im.height
            tiles.append(on(im.resize((int(im.width * s), 150), Image.LANCZOS), BGS["map"]))
    W = sum(t.width for t in tiles) + 8 * (len(tiles) + 1)
    S = Image.new("RGB", (W, 190), "white"); dr = ImageDraw.Draw(S); x = 8
    for i, t in enumerate(tiles):
        S.paste(t, (x, 30)); dr.text((x, 10), "TRUOC" if i % 2 == 0 else "SAU", fill=(0, 0, 0)); x += t.width + 8
    S.save(out / "overview_game_scale.jpg", quality=92)


if __name__ == "__main__":
    main()
