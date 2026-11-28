"""Pháp Sư cut-out rig, step 1: split the cleaned reference into a STAFF layer (staff + orb + blade + holding hand)
and a BODY layer; the area the staff covered on the body is repainted with Animagine (native inpaint, white background),
then matted with BiRefNet -> largest component -> gac_matte.clean (pipeline chốt).
Usage: python mage_rig.py split <cleaned_png_dir> <out_dir>
"""
import sys, json, time
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi
sys.path.insert(0, str(Path(__file__).parent))
import comfy_api as c
import gac_matte as g
import pilot_animagine_openpose as p
import gen_mage_anim as m

# per gender, in reference pixel coords (male 555x640, female 569x640), measured on the gridded reference
RIG = {
    "male": {"orb": (466, 190, 58), "hand": (398, 455, 30),
             "poly": [(372, 80), (475, 70), (552, 185), (545, 260), (455, 330), (430, 470), (372, 625), (322, 625), (365, 470), (405, 300), (380, 200)],
             "seed": 732001},
    "female": {"orb": (496, 140, 62), "hand": (405, 425, 30),
               "poly": [(415, 80), (520, 60), (565, 175), (560, 240), (480, 260), (470, 345), (440, 470), (385, 625), (300, 625), (300, 560), (360, 470), (400, 330), (395, 200)],
               "seed": 732002},
}
REPAINT = {
    "male": ("1boy, solo, chibi, young wizard, dark blue messy hair, blue eyes, small white goatee, wide-brimmed pointed dark blue "
             "wizard hat with gold trim, dark blue wizard robe and cape with gold embroidery, brown boots, standing, empty hands, "
             "no staff, open empty hand, full body, white background, simple background, thick clean outline, cel shading, masterpiece, high score"),
    "female": ("1girl, solo, chibi, long wavy lavender purple hair, purple eyes, teal and blue wizard robe with silver trim, purple "
               "dress, purple boots, standing, empty hands, no staff, full body, white background, simple background, thick clean "
               "outline, cel shading, masterpiece, high score"),
}
NEG_REPAINT = "staff, stick, wand, weapon, orb, holding, holding object, black hat lining, multiple characters, text, watermark, lowres, worst quality, low quality, blurry"


def staff_mask(rgba, rig):
    H, W = rgba.shape[:2]
    poly = Image.new("L", (W, H), 0); ImageDraw.Draw(poly).polygon(rig["poly"], fill=255)
    P = np.asarray(poly) > 0
    rgb = rgba[..., :3].astype(float) / 255; A = rgba[..., 3] > 0
    h, s = g.hue_sat(rgb * 255) if False else (None, None)
    mx, mn = rgb.max(-1), rgb.min(-1); v = mx; sat = (mx - mn) / np.maximum(mx, 1e-6)
    r, gg, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    wood = (r > gg) & (gg >= b * 0.85) & (sat > 0.25) & (v > 0.12) & (v < 0.85)          # brown wood
    dark_line = (v < 0.22)                                                                # outline
    silver = (sat < 0.18) & (v > 0.45)                                                    # blade (female)
    yy, xx = np.mgrid[:H, :W]
    ox, oy, orr = rig["orb"]; orb = (xx - ox) ** 2 + (yy - oy) ** 2 <= (orr + 4) ** 2
    hx, hy, hr = rig["hand"]; hand = (xx - hx) ** 2 + (yy - hy) ** 2 <= hr ** 2
    skin = (r > 0.75) & (gg > 0.55) & (b > 0.45) & (r > b)
    M = P & A & (wood | silver | dark_line)
    M |= orb & A
    M |= hand & A & (skin | wood | dark_line)
    # keep only components touching the staff wood (drops hair/robe outline bits picked by dark_line)
    lab, n = ndi.label(ndi.binary_closing(M, iterations=2))
    keep = np.zeros(n + 1, bool)
    seeds = (wood & P) | orb | (hand & skin)
    keep[np.unique(lab[seeds & (lab > 0)])] = True; keep[0] = False
    M = keep[lab] & A
    M = ndi.binary_closing(M, iterations=2) & A
    M = ndi.binary_fill_holes(M) & A
    return M


def split(cdir, out, seed_add=0, only=None):
    out.mkdir(parents=True, exist_ok=True); info = {}
    for gd, rig in RIG.items():
        if only and gd not in only: continue
        rig = dict(rig, seed=rig["seed"] + seed_add)
        ref = np.asarray(Image.open(cdir / f"hero-mage-{gd}.png").convert("RGBA"))
        H, W = ref.shape[:2]
        M = staff_mask(ref, rig)
        staff = ref.copy(); staff[~M, 3] = 0
        Image.fromarray(staff).save(out / f"{gd}_staff.png")
        # repaint body: canvas 1.6x on white, mask = dilated staff area (Animagine native inpaint)
        sc = 1.6; CW, CH = 896, 1024
        big = Image.fromarray(ref).resize((round(W * sc), round(H * sc)), Image.LANCZOS)
        cv = Image.new("RGBA", (CW, CH), (255, 255, 255, 255)); ox, oy = (CW - big.width) // 2, CH - big.height - 8
        cv.alpha_composite(big, (ox, oy))
        hole = Image.fromarray((ndi.binary_dilation(M, iterations=5) * 255).astype(np.uint8)).resize(big.size, Image.NEAREST)
        hm = Image.new("L", (CW, CH), 0); hm.paste(hole, (ox, oy))
        a = np.asarray(cv).copy(); a[..., 3] = 255 - np.asarray(hm)
        Image.fromarray(a).save(out / f"_{gd}_inpaint_in.png")
        name = c.upload(out / f"_{gd}_inpaint_in.png")
        wf = c.inpaint(name, REPAINT[gd], NEG_REPAINT, rig["seed"], denoise=1.0, steps=28, cfg=5.0)
        wf["1"]["inputs"]["ckpt_name"] = p.ANIM
        wf["5"]["inputs"].update(sampler_name="euler_ancestral", scheduler="normal")
        wf["7"]["inputs"]["filename_prefix"] = "game_art_core/mage_rig"
        _, t = c.run(wf, out / f"_{gd}_inpaint_out.png", timeout=1800)
        rep = np.asarray(Image.open(out / f"_{gd}_inpaint_out.png").convert("RGB").crop((ox, oy, ox + big.width, oy + big.height)).resize((W, H), Image.LANCZOS))
        # body = original outside the hole, repainted inside; alpha from BiRefNet on the repainted image (white bg)
        holeS = ndi.binary_dilation(M, iterations=5)
        body_rgb = np.where(holeS[..., None], rep, ref[..., :3])
        bir = g.birefnet_mask(np.dstack([body_rgb, np.full((H, W), 255, np.uint8)]), bg=(255, 255, 255))
        # inside the hole: background was generated plain white -> near-white = transparent; else BiRefNet alpha,
        # and nothing new may appear outside the original silhouette grown by 2 px (no extra blobs)
        white = (rep.astype(int).min(-1) > 238) & (np.ptp(rep.astype(int), -1) < 12)
        inside = ndi.binary_dilation(ref[..., 3] > 0, iterations=2)
        ha = np.where(white | ~inside, 0, np.round(bir * 255))
        alpha = np.where(holeS, ha, ref[..., 3]).astype(np.uint8)
        # largest component (pipeline chốt)
        alpha = ndi.median_filter(alpha, 3) if False else alpha
        lab, n = ndi.label(alpha > 128)
        if n > 1:
            sizes = ndi.sum(np.ones_like(alpha), lab, range(1, n + 1)); big_id = int(np.argmax(sizes)) + 1
            near = ndi.binary_dilation(lab == big_id, iterations=3)
            alpha = np.where(near, alpha, 0).astype(np.uint8)
        body = np.dstack([body_rgb, alpha]).astype(np.uint8)
        body, cinfo = g.clean(body, bir)
        Image.fromarray(body).save(out / f"{gd}_body.png")
        info[gd] = {"staff_px": int(M.sum()), "inpaint_seconds": t, "seed": rig["seed"], "prompt": REPAINT[gd],
                    "negative": NEG_REPAINT, "model": p.ANIM, "rig": {k: v for k, v in rig.items() if k != "poly"}, "poly": rig["poly"]}
        # check sheet
        v = Image.new("RGBA", (W * 3, H), (60, 60, 60, 255))
        v.alpha_composite(Image.fromarray(ref), (0, 0)); v.alpha_composite(Image.fromarray(body), (W, 0)); v.alpha_composite(Image.fromarray(staff), (2 * W, 0))
        v.convert("RGB").save(out / f"_{gd}_split_check.jpg", quality=88)
        print(gd, info[gd]["staff_px"], t, flush=True)
    (out / "rig_split.json").write_text(json.dumps(info, indent=1, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    if sys.argv[1] == "split":
        sa = int(sys.argv[4]) if len(sys.argv) > 4 else 0
        o = Path(sys.argv[3]) / f"seed{sa}"
        split(Path(sys.argv[2]), o, sa, sys.argv[5].split(",") if len(sys.argv) > 5 else None)
