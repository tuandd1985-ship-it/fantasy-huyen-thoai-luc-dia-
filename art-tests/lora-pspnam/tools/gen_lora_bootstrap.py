"""LoRA v2 bootstrap: dynamic poses with LoRA v1 (0.7) + IP-Adapter 0.35, 1024x1024, white background.
Usage: MAGE_W=1024 MAGE_H=1024 python gen_lora_bootstrap.py <out_dir> <lora> <strength> <poses> <seeds>
"""
import sys, json, os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import comfy_api as c
import gen_mage_v2 as gm

out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
lora, strength = sys.argv[2], float(sys.argv[3])
poses = sys.argv[4].split(","); seeds = [int(s) for s in sys.argv[5].split(",")]
rp = out / "_ref_male.png"; gm.ref_square(gm.REF_BODY["male"]).save(rp); ref_name = c.upload(rp)
logf = out / "gen_log.json"; log = json.loads(logf.read_text()) if logf.exists() else {}
for ps in poses:
    pp = out / f"_pose_{ps}.png"; gm.pose_img(ps).save(pp); pose_name = c.upload(pp)
    for sd in seeds:
        tag = f"{ps}_s{sd}"
        if (out / f"{tag}.png").exists(): continue
        g, pos = gm.wf("male", ps, sd, ref_name, pose_name, 0.35)
        g["30"] = {"class_type": "LoraLoaderModelOnly", "inputs": {"model": ["1", 0], "lora_name": lora, "strength_model": strength}}
        g["20"]["inputs"]["model"] = ["30", 0]
        g["2"]["inputs"]["text"] = "pspnam, " + pos
        _, t = c.run(g, out / f"{tag}.png", timeout=1800)
        log[tag] = {"pose": ps, "seed": sd, "lora": lora, "strength": strength, "ip_weight": 0.35, "prompt": "pspnam, " + pos, "seconds": t}
        logf.write_text(json.dumps(log, indent=1), encoding="utf-8"); print(tag, t, flush=True)
