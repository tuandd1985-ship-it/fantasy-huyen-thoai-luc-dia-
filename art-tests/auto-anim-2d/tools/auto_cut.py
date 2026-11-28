"""AUTO-ANIM-2D step 1: cut a flat chibi hero PNG into same-size part layers for Rigby2D AutoRig.
Part regions come from a chibi template (head / torso / arms / legs / cape / weapon) placed on the
alpha silhouette; the template for each hero lives in templates/<hero>.json (polygons in source px).
Hidden areas behind moving parts are filled (nearest colour + masked blur) so no hole opens when a joint rotates.
Usage: python auto_cut.py <source.png> <template.json> <out_dir>
"""
import sys, json, time
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

ORDER = ["cape", "leg_r", "leg_l", "torso", "arm_l", "head", "arm_r"]   # back -> front (character sides)


def poly(shape, pts):
    m = Image.new("L", (shape[1], shape[0]), 0); ImageDraw.Draw(m).polygon([tuple(p) for p in pts], fill=255)
    return np.asarray(m) > 0


def fill_hidden(rgba, own, region, sigma=8):
    """Extend `own` part colours into `region` (pixels hidden by parts in front), soft alpha kept opaque."""
    rgb = rgba[..., :3].astype(float)
    _, (iy, ix) = ndi.distance_transform_edt(~own, return_indices=True)
    ext = rgb[iy, ix]
    w = ndi.gaussian_filter(own.astype(float), sigma)[..., None] + 1e-6
    blur = np.stack([ndi.gaussian_filter(rgb[..., c] * own, sigma) for c in range(3)], -1) / w
    ext_s = np.stack([ndi.gaussian_filter(ext[..., c], 6) for c in range(3)], -1)   # smooth the nearest-colour streaks
    mix = np.where(region[..., None], 0.35 * ext_s + 0.65 * blur, rgb)
    out = rgba.copy(); out[..., :3] = np.clip(mix, 0, 255).round()
    out[region, 3] = 255
    return out


def main():
    src, tpl, out = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text()), Path(sys.argv[3])
    out.mkdir(parents=True, exist_ok=True); t0 = time.time()
    im = np.asarray(Image.open(src).convert("RGBA")); H, W = im.shape[:2]; A = im[..., 3] > 8
    yy, xx = np.mgrid[:H, :W]
    r, g, b = [im[..., i].astype(int) for i in range(3)]
    red = (r > 90) & (r > 1.8 * g) & (r > 1.6 * b)
    armr = poly(im.shape, tpl["arm_r"]) & A
    if "weapon_zone" in tpl:   # grow the weapon by colour: low-saturation steel pixels connected to the cut, inside the zone
        mx, mn = im[..., :3].max(-1).astype(float), im[..., :3].min(-1).astype(float)
        sat = (mx - mn) / np.maximum(mx, 1)
        zone = poly(im.shape, tpl["weapon_zone"])
        steel = A & zone & ((sat < 0.16) | (mx < 70))
        lab, n = ndi.label(steel | armr)
        armr = np.isin(lab, np.unique(lab[armr & (lab > 0)])) & A
    arml = poly(im.shape, tpl["arm_l"]) & A & ~armr
    head = (yy < tpl["neck_y"]) & A & ~armr
    legs_zone = (yy >= tpl["hip_y"]) & (xx >= tpl["legs_x"][0]) & (xx <= tpl["legs_x"][1]) & ~red
    cape = red & (yy > tpl["cape_min_y"]) & A & ~armr & ~arml & ~head
    leg_r = legs_zone & (xx < tpl["legs_split_x"]) & A & ~cape
    leg_l = legs_zone & (xx >= tpl["legs_split_x"]) & A & ~cape
    torso = A & ~(armr | arml | head | cape | leg_r | leg_l)
    parts = {"cape": cape, "leg_r": leg_r, "leg_l": leg_l, "torso": torso, "arm_l": arml, "head": head, "arm_r": armr}
    # clean tiny islands into torso
    for k in list(parts):
        lab, n = ndi.label(parts[k])
        if n > 1:
            sz = ndi.sum(np.ones((H, W)), lab, range(1, n + 1)); keep = np.isin(lab, 1 + np.nonzero(sz >= 40)[0])
            parts["torso"] |= parts[k] & ~keep; parts[k] = keep
    # fills: what each part needs underneath the parts in front of it (underlap zone near its own pixels)
    layers = {}
    for i, k in enumerate(ORDER):
        m = parts[k]
        a = im.copy(); a[~m, 3] = 0
        front = np.zeros((H, W), bool)
        for k2 in ORDER[i + 1:]: front |= parts[k2]
        zone = ndi.binary_dilation(m, iterations=tpl.get("underlap", 18)) & front
        if k == "torso":   # torso also gets the area under the head bottom / arms near the shoulders
            zone |= ndi.binary_dilation(m, iterations=26) & front & (yy > tpl["neck_y"] - 30)
        if k in ("leg_r", "leg_l"):
            zone |= ndi.binary_dilation(m, iterations=14) & parts["torso"] & (yy > tpl["hip_y"] - 25)
        if zone.any() and k not in ("arm_r",):
            a = fill_hidden(a, m, zone)
        layers[k] = a
        Image.fromarray(a).save(out / f"{k}.png")
    # check sheet: parts tinted + exploded view
    tint = {"cape": (255, 80, 80), "leg_r": (80, 160, 255), "leg_l": (40, 100, 220), "torso": (120, 220, 120),
            "arm_l": (255, 200, 60), "head": (200, 120, 255), "arm_r": (255, 140, 0)}
    ov = Image.new("RGBA", (W, H), (40, 40, 40, 255))
    for k in ORDER:
        m = parts[k]; t = im.copy(); t[..., :3] = (t[..., :3] * 0.45 + np.array(tint[k]) * 0.55).astype(np.uint8); t[~m, 3] = 0
        ov.alpha_composite(Image.fromarray(t))
    ex = Image.new("RGBA", (W * 2, H + 60), (230, 230, 230, 255)); off = {"head": (0, -40), "arm_r": (-60, 0), "arm_l": (60, 0),
            "leg_r": (-30, 40), "leg_l": (30, 40), "cape": (0, 20), "torso": (0, 0)}
    for k in ORDER:
        ex.alpha_composite(Image.fromarray(layers[k]), (W // 2 + off[k][0], 40 + off[k][1]))
    S = Image.new("RGB", (W * 3, H + 60), (230, 230, 230)); S.paste(ov.convert("RGB"), (0, 30)); S.paste(ex.convert("RGB"), (W, 0))
    S.save(out / "_parts_check.jpg", quality=90)
    info = {k: int(parts[k].sum()) for k in ORDER}; info["seconds"] = round(time.time() - t0, 2)
    (out / "parts.json").write_text(json.dumps({"order": ORDER, "size": [W, H], "px": info}, indent=1))
    print(info)


if __name__ == "__main__":
    main()
