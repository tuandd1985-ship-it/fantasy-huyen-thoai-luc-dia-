"""GAME-ART-CORE shared helpers: sprite-matte-clean + art-qc (CPU only, numpy/Pillow/scipy).
BiRefNet (rembg, birefnet-general already in C:\\AI\\ComfyUI-Local\\models\\rembg) is optional and
loaded only through birefnet_mask(); nothing is downloaded.
"""
import os
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
from scipy.signal import fftconvolve

COMFY_ROOT = Path(r"C:\AI\ComfyUI-Local")

# ---- parameters (plan section 4) ----
EDGE_BAND_PX = 2.5        # soft alpha kept only within this distance of transparency (plan: 1-3 px)
CORE_ALPHA = 0.85 * 255   # plan: alpha >= 0.85 -> core
SPECK_ALPHA, SPECK_AREA = 16, 50
REF_RADIUS = 6
SPILL_MARGIN = 6.0
HOLE_MIN_PX = 20          # enclosed low-alpha region counted as a hole if BiRefNet says foreground
BIR_FG = 0.5


def disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return (x * x + y * y <= r * r).astype(float)


def spill(rgb):  # magenta spill
    return np.minimum(rgb[..., 0], rgb[..., 2]) - rgb[..., 1]


def lum(rgb):
    return rgb[..., 0] * 0.299 + rgb[..., 1] * 0.587 + rgb[..., 2] * 0.114


def srgb_to_lab(rgb):
    c = rgb / 255.0
    c = np.where(c > 0.04045, ((c + 0.055) / 1.055) ** 2.4, c / 12.92)
    M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
    xyz = c @ M.T / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


THIN_RADIUS = 3  # parts thinner than ~2*THIN_RADIUS px (bow string, staff tip, hair strand) count as edge


def regions(A):
    tr = A == 0
    dist = ndi.distance_transform_edt(~tr)
    sil = A > 128
    thin = (A > 0) & ~ndi.binary_dilation(ndi.binary_opening(sil, structure=disk(THIN_RADIUS) > 0), iterations=1)
    band = (A > 0) & (((A > 0) & (A < 255)) | (dist <= EDGE_BAND_PX) | thin)
    core = (A > 0) & (dist > EDGE_BAND_PX + 1) & ~thin
    return dist, band, core


def _conv_stack(stack, k):
    """Zero-padded 'same' convolution of a stack of 2-D maps with one kernel, via FFT.
    Same result as ndi.convolve(mode="constant") up to float rounding (~1e-12); 10-50x faster for the
    r=12/24 px disks. Channel 0 must be the 0/1 reference mask: its neighbour count is an integer, so it is
    rounded to keep the exact `count > 0` tests of the direct convolution."""
    out = fftconvolve(stack, k[None], mode="same", axes=(1, 2))
    out[0] = np.rint(out[0])
    out[1:][np.abs(out[1:]) < 1e-9] = 0.0
    return out


def local_allowed_spill(rgb, ref):
    s = np.clip(spill(rgb), 0, None) * ref
    out = None
    for r in (REF_RADIUS, REF_RADIUS * 2, REF_RADIUS * 4):
        den, num = _conv_stack(np.stack([ref.astype(float), s]), disk(r))
        v = np.where(den > 0, num / np.maximum(den, 1e-6), np.nan)
        out = v if out is None else np.where(np.isnan(out), v, out)
    return np.nan_to_num(out, nan=0.0)


def local_ref_color(rgb, ref, r=REF_RADIUS):
    """mean colour of reference pixels nearby; widens the search for thin parts (bow string, staff)."""
    out, ok = None, None
    for rr in (r, r * 2, r * 4):
        refm = ref.astype(float)
        w, *ch = _conv_stack(np.stack([refm] + [rgb[..., i] * refm for i in range(3)]), disk(rr))
        c = np.stack(ch, -1) / np.maximum(w, 1e-6)[..., None]
        if out is None: out, ok = c, w > 0
        else: out = np.where(ok[..., None], out, c); ok = ok | (w > 0)
    return out, ok


PINK_HUE = (285.0, 372.0)   # magenta -> pink-red (wraps past 360 to 12 deg); legit reds are protected by the reference test
PINK_SAT = 0.15


def hue_sat(rgb):
    mx, mn = rgb.max(-1), rgb.min(-1); c = mx - mn
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    h = np.zeros_like(mx)
    m = c > 1e-6
    rr = m & (mx == r); gg = m & (mx == g) & ~rr; bb = m & ~rr & ~gg
    h[rr] = (60 * ((g - b)[rr] / c[rr])) % 360
    h[gg] = 60 * ((b - r)[gg] / c[gg]) + 120
    h[bb] = 60 * ((r - g)[bb] / c[bb]) + 240
    s = np.where(mx > 0, c / np.maximum(mx, 1e-6), 0)
    return h, s


PINK_VISIBLE_CHROMA = 10.0  # Lab C*; below this a pixel reads as neutral (hue of near-black pixels is noise)


def is_pink(rgb, cmin=0.0):
    h, s = hue_sat(rgb)
    hw = np.where(h < PINK_HUE[0] - 180, h + 360, h)  # unwrap so 0..12 deg sits after 360
    m = (hw >= PINK_HUE[0]) & (hw <= PINK_HUE[1]) & (s >= PINK_SAT)
    if cmin > 0:
        L = srgb_to_lab(rgb); m &= np.hypot(L[..., 1], L[..., 2]) >= cmin
    return m


def lab_to_srgb(lab):
    fy = (lab[..., 0] + 16) / 116; fx = fy + lab[..., 1] / 500; fz = fy - lab[..., 2] / 200
    f = np.stack([fx, fy, fz], -1)
    xyz = np.where(f > 0.206897, f ** 3, (f - 16 / 116) / 7.787) * np.array([0.95047, 1.0, 1.08883])
    Mi = np.array([[3.2406, -1.5372, -0.4986], [-0.9689, 1.8758, 0.0415], [0.0557, -0.2040, 1.0570]])
    c = xyz @ Mi.T
    c = np.where(c > 0.0031308, 1.055 * np.clip(c, 0, None) ** (1 / 2.4) - 0.055, 12.92 * c)
    return np.clip(c * 255, 0, 255)


# ---------------- BiRefNet (existing local model, CPU) ----------------
_session = None


def birefnet_mask(rgba_u8, bg=(127, 127, 127)):
    """Foreground probability 0..1 from BiRefNet on the sprite composited over neutral grey."""
    global _session
    os.environ.setdefault("U2NET_HOME", str(COMFY_ROOT / "models" / "rembg"))
    model = Path(os.environ["U2NET_HOME"]) / "birefnet-general.onnx"
    if not model.exists():
        raise SystemExit(f"BiRefNet model missing at {model}; refusing to download")
    if _session is None:
        from rembg import new_session
        _session = new_session("birefnet-general", providers=["CPUExecutionProvider"])
    im = Image.fromarray(rgba_u8, "RGBA")
    base = Image.new("RGBA", im.size, bg + (255,)); base.alpha_composite(im)
    m = _session.predict(base.convert("RGB"))[0]
    return np.asarray(m.resize(im.size, Image.BILINEAR)).astype(float) / 255.0


# ---------------- sprite-matte-clean ----------------
def clean(rgba_u8, bir=None):
    """Returns (cleaned_u8, info). Plan section 4 steps 3-4 for sprites that already have alpha."""
    a = rgba_u8.astype(float); rgb, A = a[..., :3].copy(), a[..., 3].copy()
    info = {}
    # remove detached faint specks
    lab, n = ndi.label(A > 0)
    if n:
        idx = np.arange(1, n + 1)
        sizes = ndi.sum(np.ones_like(A), lab, idx); amax = ndi.maximum(A, lab, idx)
        kill = idx[(sizes < SPECK_AREA) & (amax <= SPECK_ALPHA)]
        info["specks_removed"] = int(len(kill)); A[np.isin(lab, kill)] = 0
    # fill enclosed holes only where BiRefNet agrees it is foreground (keeps real gaps, e.g. bow string)
    solid = A >= CORE_ALPHA
    filled = ndi.binary_fill_holes(solid)
    hole = filled & ~solid
    hl, hn = ndi.label(hole)
    filled_px = 0
    if hn and bir is not None:
        for i in range(1, hn + 1):
            m = hl == i
            if bir[m].mean() >= BIR_FG:
                A[m] = 255; filled_px += int(m.sum())
    info["hole_px_filled"] = filled_px
    # solidify core: everything deeper than the edge band inside the silhouette is opaque
    dist, band, core = regions(A)
    core_soft = core & (A < 255)
    info["core_px_solidified"] = int(core_soft.sum())
    A[core] = 255
    dist, band, core = regions(A)
    # colour: local-reference magenta despill on the edge band, luminance kept
    ref = (A == 255) & ~band
    allowed = local_allowed_spill(rgb, ref)
    ex = np.clip(spill(rgb) - allowed - SPILL_MARGIN, 0, None) * band
    y0 = lum(rgb); out = rgb.copy(); out[..., 0] -= ex; out[..., 2] -= ex
    out += ((y0 - lum(out)) * band)[..., None]
    out = np.clip(out, 0, 255)
    info["edge_px_despilled"] = int((ex > 0).sum())
    # pink/magenta hue left on edge pixels whose local reference is NOT pink/purple: keep L*, take the
    # reference chroma direction (scaled to the pixel's own chroma). Legit purple parts are skipped.
    refc, ok = local_ref_color(out, ref)
    fix = band & ok & is_pink(out) & ~is_pink(refc)
    if fix.any():
        L = srgb_to_lab(out); R = srgb_to_lab(refc)
        cp = np.hypot(L[..., 1], L[..., 2]); cr = np.hypot(R[..., 1], R[..., 2])
        sc = np.minimum(1.0, cp / np.maximum(cr, 1e-6))
        new = L.copy(); new[..., 1] = R[..., 1] * sc; new[..., 2] = R[..., 2] * sc
        out[fix] = lab_to_srgb(new)[fix]
    info["edge_px_pink_rehued"] = int(fix.sum())
    out[A == 0] = 0
    return np.dstack([out, A]).round().astype(np.uint8), info


# ---------------- art-qc (plan section 7) ----------------
THRESH = {
    "core_solid_pct_min": 99.0, "core_holes_max": 0, "stray_islands_max": 0, "touch_frame_edge": False,
    "edge_cast_pct_max": 3.0, "edge_chroma_dE_median_max": 12.0, "palette_dE_mean_max": 8.0,
    "shape_change_pct_max": 4.0, "anchor_shift_px_max": 2, "sharpness_ratio_min": 0.98,
}


def palette(rgb, A, k=8):
    px = rgb[A == 255].astype(np.uint8)
    if len(px) < k: return np.zeros((0, 3))
    im = Image.fromarray(px.reshape(-1, 1, 3)).quantize(k, method=Image.Quantize.MEDIANCUT)
    pal = np.array(im.getpalette()[:k * 3]).reshape(k, 3)
    cnt = np.bincount(np.asarray(im).ravel(), minlength=k)
    return pal[np.argsort(-cnt)].astype(float)


def sharpness(rgba_u8, h=150):
    im = Image.fromarray(rgba_u8, "RGBA"); s = h / im.height
    im = im.resize((max(1, int(im.width * s)), h), Image.LANCZOS)
    base = Image.new("RGBA", im.size, (127, 127, 127, 255)); base.alpha_composite(im)
    g = np.asarray(base.convert("L")).astype(float)
    return float(ndi.laplace(g).var())


def qc(rgba_u8, ref_u8=None, bir=None):
    a = rgba_u8.astype(float); rgb, A = a[..., :3], a[..., 3]
    dist, band, core = regions(A)
    m = {}
    m["core_solid_pct"] = round(100 * float((A[core] == 255).mean()) if core.any() else 0, 3)
    solid = A >= CORE_ALPHA; hole = ndi.binary_fill_holes(solid) & ~solid
    hl, hn = ndi.label(hole); holes = 0
    for i in range(1, hn + 1):
        mm = hl == i
        if mm.sum() >= HOLE_MIN_PX and (bir is None or bir[mm].mean() >= BIR_FG): holes += 1
    m["core_holes"] = holes
    lab, n = ndi.label(A > 0); sizes = ndi.sum(np.ones_like(A), lab, range(1, n + 1)) if n else np.array([0])
    main = sizes.max() if n else 0
    m["stray_islands"] = int(((sizes > 0.003 * main) & (sizes < main)).sum())
    m["specks_lt50px"] = int((sizes < SPECK_AREA).sum())
    m["touch_frame_edge"] = bool((A[0] > 0).any() or (A[-1] > 0).any() or (A[:, 0] > 0).any() or (A[:, -1] > 0).any())
    ref = (A == 255) & ~band
    ex = np.clip(spill(rgb) - local_allowed_spill(rgb, ref) - SPILL_MARGIN, 0, None)
    refc, ok = local_ref_color(rgb, ref)
    pink = band & (A > 64) & ok & is_pink(rgb, PINK_VISIBLE_CHROMA) & ~is_pink(refc)
    # edge cast = edge pixels with excess magenta spill OR a pink hue their local reference does not have
    m["edge_cast_pct"] = round(100 * float(((ex > 15) | pink)[band].mean()), 3)
    m["edge_spill_only_pct"] = round(100 * float((ex[band] > 15).mean()), 3)
    m["edge_pink_hue_pct"] = round(100 * float(pink[band].mean()), 3)
    L1, L2 = srgb_to_lab(rgb), srgb_to_lab(refc)
    dE = np.hypot(L1[..., 1] - L2[..., 1], L1[..., 2] - L2[..., 2])
    sel = band & ok & (A > 128)
    m["edge_chroma_dE_median"] = round(float(np.median(dE[sel])), 2) if sel.any() else None
    m["sharpness"] = round(sharpness(rgba_u8), 2)
    m["size"] = [int(A.shape[1]), int(A.shape[0])]
    if ref_u8 is not None:
        r = ref_u8.astype(float); RA = r[..., 3]
        p0, p1 = srgb_to_lab(palette(r[..., :3], RA)), srgb_to_lab(palette(rgb, A))
        if len(p0) and len(p1):
            d = np.sqrt(((p0[:, None] - p1[None]) ** 2).sum(-1)); m["palette_dE_mean"] = round(float(d.min(1).mean()), 2)
        def bbox(X):
            ys, xs = np.nonzero(X > 128); return ys.min(), ys.max(), xs.min(), xs.max()
        b0, b1 = bbox(RA), bbox(A)
        h0, h1, w0, w1 = b0[1] - b0[0], b1[1] - b1[0], b0[3] - b0[2], b1[3] - b1[2]
        m["shape_change_pct"] = round(100 * max(abs(h1 - h0) / h0, abs(w1 - w0) / w0), 3)
        m["anchor_shift_px"] = int(abs(b1[1] - b0[1]))
        m["sharpness_ratio"] = round(m["sharpness"] / max(sharpness(ref_u8), 1e-6), 4)
        inner = core & (RA == 255)
        dd = np.abs(rgb - r[..., :3]).max(-1)
        m["interior_rgb_changed_px"] = int(((dd > 0) & inner).sum())
        m["interior_mean_abs_rgb_delta"] = round(float(dd[inner].mean()), 3)
    return m


def judge(m, profile="single"):
    """profile="multicolor" (Luna 2026-11-28): for multi-colour objects (flower clumps, potions, banners) the
    edge-vs-core chroma dE is not meaningful, so it is reported but not judged; such objects are judged on
    edge spill / fringe (edge_cast, plus grey_halo where the caller measures it) and MUST be signed off on the
    contact sheet by eye (r["visual_check_required"] is left False until a human ticks it)."""
    t = THRESH; r = {}
    if profile == "multicolor":
        r["core_solid"] = m["core_solid_pct"] >= t["core_solid_pct_min"]
        r["core_holes"] = m["core_holes"] <= t["core_holes_max"]
        r["stray_islands"] = m["stray_islands"] <= t["stray_islands_max"]
        r["not_touching_frame_edge"] = m["touch_frame_edge"] == t["touch_frame_edge"]
        r["edge_cast"] = m["edge_cast_pct"] < t["edge_cast_pct_max"]
        return r
    r["core_solid"] = m["core_solid_pct"] >= t["core_solid_pct_min"]
    r["core_holes"] = m["core_holes"] <= t["core_holes_max"]
    r["stray_islands"] = m["stray_islands"] <= t["stray_islands_max"]
    r["not_touching_frame_edge"] = m["touch_frame_edge"] == t["touch_frame_edge"]
    r["edge_cast"] = m["edge_cast_pct"] < t["edge_cast_pct_max"]
    r["edge_chroma_dE"] = m["edge_chroma_dE_median"] is not None and m["edge_chroma_dE_median"] < t["edge_chroma_dE_median_max"]
    if "palette_dE_mean" in m:
        r["palette"] = m["palette_dE_mean"] < t["palette_dE_mean_max"]
        r["shape"] = m["shape_change_pct"] <= t["shape_change_pct_max"] and m["anchor_shift_px"] <= t["anchor_shift_px_max"]
        r["sharpness"] = m["sharpness_ratio"] >= t["sharpness_ratio_min"]
    return r
