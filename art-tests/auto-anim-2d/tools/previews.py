"""GIF previews (one per animation + all-in-one), filmstrip and QC (edge alpha, islands, feet line) for exported frames.
Usage: python previews.py <export_dir>"""
import sys, glob, json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

d = Path(sys.argv[1]); A = ["idle", "walk", "run", "attack", "skill", "hit", "death"]
BG = (78, 92, 64)
allf, qc, rows = [], {}, []
for a in A:
    fs = sorted(glob.glob(str(d / "frames*" / "*" / f"{a}_*.png")))
    ims = [Image.open(f).convert("RGBA") for f in fs]
    if not ims: continue
    fr = []
    for im in ims:
        b = Image.new("RGBA", im.size, BG + (255,)); b.alpha_composite(im); fr.append(b.convert("RGB"))
    dur = 83
    fr[0].save(d / f"preview_{a}.gif", save_all=True, append_images=fr[1:], duration=dur, loop=0)
    allf += fr if a in ("attack", "skill", "hit", "death") else fr * 2
    # QC per animation
    edge, isl, feet = [], [], []
    for im in ims:
        al = np.asarray(im)[..., 3]; e = np.zeros_like(al, bool); e[:2] = e[-2:] = True; e[:, :2] = e[:, -2:] = True
        edge.append(float((al[e] > 0).mean() * 100))
        lab, n = ndi.label(al > 128); isl.append(int(n))
        ys = np.nonzero(al.max(1) > 128)[0]; feet.append(int(ys.max()) if len(ys) else -1)
    qc[a] = {"frames": len(ims), "frame_size": list(ims[0].size), "edge_alpha_pct_max": round(max(edge), 3),
             "opaque_components_max": max(isl), "feet_y_min_max": [min(feet), max(feet)]}
    w, h = ims[0].size; sel = fr[:: max(1, len(fr) // 10)][:10]
    R = Image.new("RGB", (w // 2 * len(sel), h // 2 + 16), BG)
    for i, f in enumerate(sel): R.paste(f.resize((w // 2, h // 2)), (i * w // 2, 16))
    ImageDraw.Draw(R).text((4, 2), f"{a} ({len(ims)} frames @12fps)", fill="white"); rows.append(R)
allf[0].save(d / "preview_all.gif", save_all=True, append_images=allf[1:], duration=83, loop=0)
W = max(r.width for r in rows); S = Image.new("RGB", (W, sum(r.height for r in rows)), BG); y = 0
for r in rows: S.paste(r, (0, y)); y += r.height
S.save(d / "filmstrip.jpg", quality=88)
(d / "qc.json").write_text(json.dumps(qc, indent=1))
print(json.dumps(qc))
