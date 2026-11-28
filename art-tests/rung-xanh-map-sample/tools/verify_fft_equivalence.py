import sys, json, time
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0, str(Path(__file__).parent))
import gac_matte as g, process_map_props as pm
out = Path(sys.argv[1]); tag = sys.argv[2]
for k in ("cay_soi_s728102", "khom_hoa_s728101"):
    bf = out / f"{k}_bir.npy"
    raw = np.asarray(Image.open(f"output/rung_xanh_map/props_raw/{k}.png").convert("RGB"))
    if not bf.exists(): np.save(bf, g.birefnet_mask(np.dstack([raw, np.full(raw.shape[:2], 255, np.uint8)])))
    bir = np.load(bf); T = {}
    t = time.perf_counter(); rgba, B = pm.matte_from_rgb(raw, bir); T["unmix"] = time.perf_counter() - t
    t = time.perf_counter(); qb = g.qc(rgba, None, bir); T["qc_before"] = time.perf_counter() - t
    t = time.perf_counter(); C, info = g.clean(rgba, bir); T["clean"] = time.perf_counter() - t
    t = time.perf_counter(); qa = g.qc(C, None, bir); T["qc_after"] = time.perf_counter() - t
    np.save(out / f"{k}_{tag}_C.npy", C)
    json.dump({"T": {a: round(b, 2) for a, b in T.items()}, "qc_before": qb, "qc_after": qa}, open(out / f"{k}_{tag}.json", "w"), default=float, indent=1)
    print(k, tag, {a: round(b, 2) for a, b in T.items()}, flush=True)
