"""Assemble animations from pre-cut character parts (Codex parts.json) by rotating parts about their pivots.
No new drawing: every frame only re-places the given part images (rotate/translate, hierarchical FK).

Usage: python parts_rig.py <parts_dir> <motions.json> <out_dir>
  parts_dir: parts.json + part PNGs (+ assembled.png for the overlay check)
  motions.json: {"actions": {name: {"keys": [{"t": ms, "rot": {part: deg}, "root": [dx, dy]}], "frames_ms": [...],
                 "hit_frame": i|null, "loop": bool}}}

parts.json is normalised by `load_parts`, accepting the usual spellings:
  part list under "parts" (list or dict); per part: name|id, file|image|src, position as x/y | pos | offset | left/top
  (top-left of the image in the assembled canvas), pivot as pivot|anchor|joint|origin ([x, y] or {x, y}), either in
  canvas coords (default) or local to the image ("pivot_space": "local"), parent|parentId, z|order|zIndex|draw_order.
"""
import sys, json, math, time
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

CELL_W, CELL_H, FEET_Y = 768, 640, 620


def _xy(v):
    if v is None: return None
    if isinstance(v, dict): return float(v.get("x", 0)), float(v.get("y", 0))
    return float(v[0]), float(v[1])


def load_parts(pdir):
    meta = json.loads((pdir / "parts.json").read_text(encoding="utf-8"))
    raw = meta.get("parts", meta)
    if isinstance(raw, dict): raw = [dict(v, name=v.get("name", k)) for k, v in raw.items()]
    space = meta.get("pivot_space", "canvas")
    parts = []
    for i, p in enumerate(raw):
        name = p.get("name") or p.get("id")
        f = p.get("file") or p.get("image") or p.get("src")
        img = Image.open(pdir / f).convert("RGBA")
        pos = _xy(p.get("pos") or p.get("offset") or p.get("position")) or (float(p.get("x", p.get("left", 0))), float(p.get("y", p.get("top", 0))))
        piv = _xy(p.get("pivot") or p.get("anchor") or p.get("joint") or p.get("origin")) or (pos[0] + img.width / 2, pos[1] + img.height / 2)
        if p.get("pivot_space", space) == "local": piv = (pos[0] + piv[0], pos[1] + piv[1])
        parts.append({"name": name, "img": img, "pos": pos, "pivot": piv, "parent": p.get("parent") or p.get("parentId"),
                      "z": float(p.get("z", p.get("order", p.get("zIndex", p.get("draw_order", i)))))})
    canvas = _xy(meta.get("canvas") or meta.get("size")) if (meta.get("canvas") or meta.get("size")) else None
    return parts, meta, canvas


def compose(parts, rot, root=(0.0, 0.0), canvas=(1024, 1024)):
    """FK: a part's transform = parent's transform then its own rotation about its pivot."""
    by = {p["name"]: p for p in parts}; M = {}
    def mat(name):
        if name in M: return M[name]
        p = by[name]; a = math.radians(rot.get(name, 0.0)); c, s = math.cos(a), math.sin(a)
        px, py = p["pivot"]
        own = np.array([[c, -s, px - c * px + s * py], [s, c, py - s * px - c * py], [0, 0, 1]])
        par = mat(p["parent"]) if p["parent"] in by else np.array([[1, 0, root[0]], [0, 1, root[1]], [0, 0, 1]], float)
        M[name] = par @ own; return M[name]
    W, H = int(canvas[0]), int(canvas[1]); out = Image.new("RGBA", (W, H))
    for p in sorted(parts, key=lambda q: q["z"]):
        m = mat(p["name"]) @ np.array([[1, 0, p["pos"][0]], [0, 1, p["pos"][1]], [0, 0, 1]], float)   # image px -> canvas
        inv = np.linalg.inv(m)
        lay = p["img"].transform((W, H), Image.AFFINE, tuple(inv[:2].ravel()), resample=Image.BICUBIC)
        out.alpha_composite(lay)
    return out


def ease(u): return 0.5 - 0.5 * math.cos(math.pi * u)


def sample(keys, t):
    """Interpolate key poses (eased) at time t ms."""
    if t <= keys[0]["t"]: k0 = k1 = keys[0]; u = 0
    elif t >= keys[-1]["t"]: k0 = k1 = keys[-1]; u = 0
    else:
        for a, b in zip(keys, keys[1:]):
            if a["t"] <= t <= b["t"]: k0, k1, u = a, b, (t - a["t"]) / max(1e-6, b["t"] - a["t"]); break
    u = ease(u); names = set(k0.get("rot", {})) | set(k1.get("rot", {}))
    rot = {n: k0.get("rot", {}).get(n, 0) * (1 - u) + k1.get("rot", {}).get(n, 0) * u for n in names}
    r0, r1 = k0.get("root", [0, 0]), k1.get("root", [0, 0])
    return rot, (r0[0] * (1 - u) + r1[0] * u, r0[1] * (1 - u) + r1[1] * u)


def to_cell(img, feet_xy, scale):
    W, H = img.size; s = scale
    im = img.resize((round(W * s), round(H * s)), Image.LANCZOS)
    cell = Image.new("RGBA", (CELL_W, CELL_H))
    cell.alpha_composite(im, (round(CELL_W / 2 - feet_xy[0] * s), round(FEET_Y - feet_xy[1] * s)))
    return cell


def qc_cell(cell):
    A = np.asarray(cell)[..., 3]; e = np.zeros_like(A, bool); e[:2] = e[-2:] = True; e[:, :2] = e[:, -2:] = True
    lab, n = ndi.label(A > 128); ys = np.nonzero(A.max(1) > 128)[0]
    sz = ndi.sum(np.ones_like(A), lab, range(1, n + 1)) if n else []
    return {"edge_alpha_pct": round(float((A[e] > 0).mean() * 100), 3), "opaque_components": int(n),
            "islands_ge30": int(sum(1 for v in sz if 30 <= v < max(sz))) if n else 0, "feet_y": int(ys.max()) if len(ys) else -1}


def main():
    pdir, mfile, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]); out.mkdir(parents=True, exist_ok=True)
    t0 = time.time(); parts, meta, canvas = load_parts(pdir)
    motions = json.loads(mfile.read_text(encoding="utf-8"))
    if canvas is None:
        canvas = (max(p["pos"][0] + p["img"].width for p in parts), max(p["pos"][1] + p["img"].height for p in parts))
    rest = compose(parts, {}, canvas=canvas)
    report = {"parts": len(parts), "canvas": list(canvas)}
    # 1) overlay check against assembled.png
    asm = pdir / "assembled.png"
    if asm.exists():
        ref = np.asarray(Image.open(asm).convert("RGBA").resize(rest.size)).astype(int); got = np.asarray(rest).astype(int)
        d = np.abs(ref - got); Aref, Agot = ref[..., 3] > 128, got[..., 3] > 128
        ys, xs = np.nonzero(Aref); yg, xg = np.nonzero(Agot)
        report["overlay_check"] = {
            "alpha_iou": round(float((Aref & Agot).sum() / max(1, (Aref | Agot).sum())), 4),
            "bbox_offset_px": [int(xg.min() - xs.min()), int(yg.min() - ys.min()), int(xg.max() - xs.max()), int(yg.max() - ys.max())] if len(xs) and len(xg) else None,
            "rgb_mean_abs_diff_inside": round(float(d[..., :3][Aref & Agot].mean()), 2) if (Aref & Agot).any() else None,
            "px_alpha_mismatch": int((Aref ^ Agot).sum())}
        diffimg = Image.fromarray(np.dstack([(Aref & ~Agot) * 255, (Aref & Agot) * 120, (Agot & ~Aref) * 255]).astype(np.uint8))
        diffimg.save(out / "overlay_check.png")
    # feet + scale from the rest pose
    A = np.asarray(rest)[..., 3]; ys = np.nonzero(A.max(1) > 128)[0]; yb = ys.max()
    xs = np.nonzero((A[max(0, yb - 30):yb + 1] > 128).any(0))[0]; feet = ((xs.min() + xs.max()) / 2, float(yb))
    scale = motions.get("height_px", 476) / (yb - ys.min())
    report["scale"] = round(scale, 4); report["actions"] = {}
    BG = (78, 92, 64)
    for name, act in motions["actions"].items():
        times = np.cumsum([0] + act["frames_ms"][:-1]); frames = []
        for t in times:
            rot, root = sample(act["keys"], t)
            frames.append(to_cell(compose(parts, rot, root, canvas), feet, scale))
        S = Image.new("RGBA", (CELL_W * len(frames), CELL_H))
        for i, f in enumerate(frames): S.alpha_composite(f, (i * CELL_W, 0))
        fn = f"{motions.get('prefix', 'char')}_{name}_{len(frames)}f.png"; S.save(out / fn, optimize=True)
        gif = []
        for i, f in enumerate(frames):
            b = Image.new("RGBA", f.size, BG + (255,)); b.alpha_composite(f); d = ImageDraw.Draw(b)
            d.line([(0, FEET_Y), (CELL_W, FEET_Y)], fill=(255, 220, 0, 90))
            if act.get("hit_frame") == i: d.text((10, 10), "HIT", fill=(255, 80, 80))
            gif.append(b.convert("RGB").resize((CELL_W // 2, CELL_H // 2)))
        gif[0].save(out / f"preview_{name}.gif", save_all=True, append_images=gif[1:], duration=act["frames_ms"], loop=0)
        report["actions"][name] = {"file": fn, "frames": len(frames), "durations_ms": act["frames_ms"], "hit_frame": act.get("hit_frame"),
                                   "loop": act.get("loop", False), "qc": [qc_cell(f) for f in frames]}
    report["seconds"] = round(time.time() - t0, 2)
    (out / "animations.json").write_text(json.dumps(report, indent=1), encoding="utf-8")
    print(json.dumps({k: (v["frames"], max(q["edge_alpha_pct"] for q in v["qc"]), [q["feet_y"] for q in v["qc"]]) for k, v in report["actions"].items()}),
          report.get("overlay_check"), report["seconds"])


if __name__ == "__main__":
    main()
