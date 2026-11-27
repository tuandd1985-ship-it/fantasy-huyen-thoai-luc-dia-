"""Step A: clean magenta fringe on existing hero sprites without changing their look.

Only pixels in the EDGE BAND are touched (partial-alpha pixels + opaque pixels within
BAND_PX of transparency). Interior pixels keep identical RGB. Silhouette is unchanged except:
  * detached near-invisible specks (alpha <= SPECK_ALPHA, component < SPECK_AREA px) -> alpha 0
  * interior alpha 250..254 (lossy-WebP noise, > INTERIOR_PX from transparency) -> 255
Colour fix = magenta despill relative to the LOCAL reference: spill s = min(R,B) - G.
Allowed spill comes from opaque core pixels nearby, so purple hair/robes/crystals stay purple.
Excess spill is removed from R and B, then luminance is restored with a neutral offset.

Usage: python hero_edge_clean.py <in_dir_with_kN.webp> <out_dir> [keys...]
Only numpy, Pillow, scipy. No network, no model.
"""
import sys, json, hashlib
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

BAND_PX = 2.5          # opaque pixels within this distance of transparency are edge band
CORE_PX = 3.5          # pixels farther than this are "core" (reference colours)
REF_RADIUS = 6         # neighbourhood for local allowed spill
SPECK_ALPHA = 16
SPECK_AREA = 50
INTERIOR_PX = 3.0
MARGIN = 6.0           # spill tolerance above local reference

NAMES = {"k2": "swordsman-male", "k3": "swordsman-female", "k4": "mage-male",
         "k5": "mage-female", "k6": "archer-male", "k7": "archer-female"}


def disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return (x * x + y * y <= r * r).astype(float)


def spill(rgb):
    return np.minimum(rgb[..., 0], rgb[..., 2]) - rgb[..., 1]


def lum(rgb):
    return rgb[..., 0] * 0.299 + rgb[..., 1] * 0.587 + rgb[..., 2] * 0.114


def masks(A):
    tr = A == 0
    dist = ndi.distance_transform_edt(~tr)
    part = (A > 0) & (A < 255)
    band = (A > 0) & (part | (dist <= BAND_PX))
    core = (A == 255) & (dist > CORE_PX)
    return tr, dist, part, band, core


def local_allowed_spill(rgb, core):
    k = disk(REF_RADIUS)
    s = np.clip(spill(rgb), 0, None) * core
    num = ndi.convolve(s, k, mode="constant")
    den = ndi.convolve(core.astype(float), k, mode="constant")
    allowed = np.where(den > 0, num / np.maximum(den, 1e-6), np.nan)
    # thin parts with no core nearby: widen search
    k2 = disk(REF_RADIUS * 2)
    num2 = ndi.convolve(s, k2, mode="constant"); den2 = ndi.convolve(core.astype(float), k2, mode="constant")
    allowed = np.where(np.isnan(allowed), np.where(den2 > 0, num2 / np.maximum(den2, 1e-6), 0.0), allowed)
    return allowed


def excess_spill(rgb, A):
    _, _, _, band, core = masks(A)
    ex = np.clip(spill(rgb) - local_allowed_spill(rgb, core) - MARGIN, 0, None)
    return ex, band


def qc(rgb, A):
    ex, band = excess_spill(rgb, A)
    tr = A == 0
    lab, n = ndi.label(A > 0)
    sizes = ndi.sum(np.ones_like(A), lab, range(1, n + 1)) if n else np.array([0])
    nb = ndi.binary_dilation(A < 10) & (A > 200)  # same definition as the v0.3.7 review
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    mag = (r > g + 40) & (b > g + 40)
    return {
        "band_px": int(band.sum()),
        "band_px_with_excess_spill_gt15_pct": round(100 * float((ex[band] > 15).mean()), 2),
        "band_mean_excess_spill": round(float(ex[band].mean()), 2),
        "legacy_magenta_cast_on_opaque_edge_pct": round(100 * float((mag & nb).sum()) / max(1, nb.sum()), 2),
        "components": int(n),
        "specks_lt50px": int((sizes < SPECK_AREA).sum()),
        "partial_alpha_px": int(((A > 0) & (A < 255)).sum()),
    }


def clean(rgba):
    a = rgba.astype(float)
    rgb, A = a[..., :3].copy(), a[..., 3].copy()
    # 1. remove detached faint specks
    lab, n = ndi.label(A > 0)
    if n:
        idx = np.arange(1, n + 1)
        sizes = ndi.sum(np.ones_like(A), lab, idx)
        amax = ndi.maximum(A, lab, idx)
        kill = idx[(sizes < SPECK_AREA) & (amax <= SPECK_ALPHA)]
        A[np.isin(lab, kill)] = 0
    # 2. snap interior near-opaque alpha noise
    tr, dist, part, band, core = masks(A)
    A[(A >= 250) & (A < 255) & (dist > INTERIOR_PX)] = 255
    tr, dist, part, band, core = masks(A)
    # 3. local-reference despill on edge band only
    allowed = local_allowed_spill(rgb, core)
    ex = np.clip(spill(rgb) - allowed - MARGIN, 0, None) * band
    y0 = lum(rgb)
    out = rgb.copy()
    out[..., 0] -= ex
    out[..., 2] -= ex
    dy = (y0 - lum(out)) * band
    out += dy[..., None]
    out = np.clip(out, 0, 255)
    # fully transparent pixels: neutral colour (avoids magenta in non-premultiplied filtering)
    out[A == 0] = 0
    res = np.dstack([out, A]).round().astype(np.uint8)
    return res, band


def main():
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    keys = sys.argv[3:] or list(NAMES)
    for sub in ("original", "cleaned_png", "cleaned_webp", "compare"):
        (dst / sub).mkdir(parents=True, exist_ok=True)
    report = {"params": {k: v for k, v in globals().items() if k.isupper() and k != "NAMES"}, "items": []}
    for k in keys:
        name = NAMES[k]
        raw = (src / f"{k}.webp").read_bytes()
        (dst / "original" / f"hero-{name}.webp").write_bytes(raw)
        im = np.asarray(Image.open(src / f"{k}.webp").convert("RGBA"))
        Image.fromarray(im).save(dst / "original" / f"hero-{name}.png")
        res, band = clean(im)
        png = dst / "cleaned_png" / f"hero-{name}.png"
        Image.fromarray(res).save(png, optimize=True)
        webp_ll = dst / "cleaned_webp" / f"hero-{name}.webp"
        Image.fromarray(res).save(webp_ll, lossless=True, method=6, exact=True)
        # verify webp round-trip is pixel exact
        rt = np.asarray(Image.open(webp_ll).convert("RGBA"))
        # smaller lossy option for the game bundle; QC is measured AFTER decode
        (dst / "cleaned_webp_q90").mkdir(exist_ok=True)
        webp_q = dst / "cleaned_webp_q90" / f"hero-{name}.webp"
        Image.fromarray(res).save(webp_q, quality=90, alpha_quality=100, method=6, exact=True)
        rq = np.asarray(Image.open(webp_q).convert("RGBA")).astype(float)
        after_q90 = qc(rq[..., :3], rq[..., 3])
        before, after = qc(im[..., :3].astype(float), im[..., 3].astype(float)), qc(res[..., :3].astype(float), res[..., 3].astype(float))
        diff = np.abs(res[..., :3].astype(int) - im[..., :3].astype(int)).max(-1)
        vis = im[..., 3] > 0
        item = {
            "key": k, "name": name, "size": list(im.shape[1::-1]),
            "original_sha256": hashlib.sha256(raw).hexdigest(),
            "cleaned_png_sha256": hashlib.sha256(png.read_bytes()).hexdigest(),
            "bytes": {"original_webp": len(raw), "cleaned_png": png.stat().st_size, "cleaned_webp_lossless": webp_ll.stat().st_size, "cleaned_webp_q90": webp_q.stat().st_size},
            "webp_roundtrip_exact": bool((rt == res).all()),
            "before": before, "after": after, "after_webp_q90_decoded": after_q90,
            "changes": {
                "rgb_changed_px": int(((diff > 0) & vis).sum()),
                "rgb_changed_outside_band_px": int(((diff > 0) & vis & ~band & (res[..., 3] > 0)).sum()),
                "max_rgb_delta_outside_band": int(diff[vis & ~band & (res[..., 3] > 0)].max()) if (vis & ~band & (res[..., 3] > 0)).any() else 0,
                "alpha_changed_px": int((res[..., 3] != im[..., 3]).sum()),
                "alpha_removed_specks_px": int(((im[..., 3] > 0) & (res[..., 3] == 0)).sum()),
                "mean_rgb_delta_in_band": round(float(diff[band].mean()), 2),
            },
        }
        report["items"].append(item)
        print(k, name, "before", before["band_px_with_excess_spill_gt15_pct"], "% ->", after["band_px_with_excess_spill_gt15_pct"], "%",
              "| specks", before["specks_lt50px"], "->", after["specks_lt50px"], "| outside-band changes", item["changes"]["rgb_changed_outside_band_px"],
              "| legacy", before["legacy_magenta_cast_on_opaque_edge_pct"], "->", after["legacy_magenta_cast_on_opaque_edge_pct"])
    (dst / "qc_report.json").write_text(json.dumps(report, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    main()
