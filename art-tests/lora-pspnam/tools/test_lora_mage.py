"""A/B test of the Pháp Sư Nam LoRA: same OpenPose skeletons / seeds as v2.
modes: ipa = v2 method (IP-Adapter, no LoRA); lora = LoRA only (no IP-Adapter); lora_ipa = both (IP weight 0.35).
Usage: python test_lora_mage.py <out_dir> <lora_file_name> <strength> [poses] [seeds]
"""
import sys, json, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
os.environ.setdefault("MAGE_SKEL", "0.82")
import comfy_api as c
import gen_mage_v2 as gm
from PIL import Image, ImageDraw

out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
lora, strength = sys.argv[2], float(sys.argv[3])
poses = sys.argv[4].split(",") if len(sys.argv) > 4 else ["idle", "run", "cast1", "cast2", "skill_charge", "skill_release"]
seeds = [int(s) for s in sys.argv[5].split(",")] if len(sys.argv) > 5 else [742001]
cdir = Path("C:/Users/DOTUAN~1/AppData/Local/Temp/claude/0026eb623bf958f6/d9570d91-8ab6-4e18-b704-35c9c91712aa/scratchpad/game/src/art-tests/hero-edge-clean/cleaned_png")
refsrc = gm.REF_BODY["male"]; rp = out / "_ref_male.png"; gm.ref_square(refsrc).save(rp); ref_name = c.upload(rp)
log = {}
for ps in poses:
    pp = out / f"_pose_{ps}.png"; gm.pose_img(ps).save(pp); pose_name = c.upload(pp)
    for sd in seeds:
        for mode in ("ipa", "lora", "lora_ipa"):
            g, pos = gm.wf("male", ps, sd, ref_name, pose_name, 0.6 if mode == "ipa" else 0.35)
            if mode != "ipa":
                g["30"] = {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["1", 0], "lora_name": lora, "strength_model": strength}}
                g["5"]["inputs"]["positive"] = ["12", 0]
                g["2"]["inputs"]["text"] = "pspnam, " + pos
                if mode == "lora":
                    g["5"]["inputs"]["model"] = ["30", 0]
                    for k in ("20", "21", "22"): g.pop(k)
                else:
                    g["20"]["inputs"]["model"] = ["30", 0]
            tag = f"{mode}_{ps}_s{sd}"
            _, t = c.run(g, out / f"{tag}.png", timeout=1800)
            log[tag] = {"mode": mode, "pose": ps, "seed": sd, "lora": lora if mode != "ipa" else None, "lora_strength": strength if mode != "ipa" else None,
                        "ip_weight": 0.6 if mode == "ipa" else (0.35 if mode == "lora_ipa" else None), "seconds": t}
            print(tag, t, flush=True)
(out / "ab_log.json").write_text(json.dumps(log, indent=1), encoding="utf-8")
cols = len(poses) * len(seeds); S = Image.new("RGB", (cols * 256, 3 * 352 + 10), "white"); d = ImageDraw.Draw(S)
for j, mode in enumerate(("ipa", "lora", "lora_ipa")):
    i = 0
    for ps in poses:
        for sd in seeds:
            S.paste(Image.open(out / f"{mode}_{ps}_s{sd}.png").convert("RGB").resize((256, 341)), (i * 256, j * 352 + 10)); i += 1
    d.text((4, j * 352), {"ipa": "CU: IP-Adapter", "lora": "MOI: LoRA", "lora_ipa": "LoRA + IP-Adapter nhe"}[mode], fill="red")
S.save(out / "ab_compare.jpg", quality=88)
