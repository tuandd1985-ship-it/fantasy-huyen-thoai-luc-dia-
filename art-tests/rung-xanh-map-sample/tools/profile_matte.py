"""Profile matte-clean + QC per step on one map prop. Usage: python profile_matte.py <raw.png> [out.json]"""
import sys, time, json, cProfile, pstats, io
from pathlib import Path
import numpy as np
from PIL import Image
sys.path.insert(0, str(Path(__file__).parent))
import gac_matte as g, process_map_props as pm

raw = np.asarray(Image.open(sys.argv[1]).convert("RGB")); T = {}
def step(name, f, *a):
    t = time.perf_counter(); r = f(*a); T[name] = round(time.perf_counter() - t, 2); return r
pr = cProfile.Profile(); pr.enable()
bir = step("1_birefnet", g.birefnet_mask, np.dstack([raw, np.full(raw.shape[:2], 255, np.uint8)]))
rgba, B = step("2_unmix_known_bg", pm.matte_from_rgb, raw, bir)
step("3_qc_before", g.qc, rgba, None, bir)
C, info = step("4_clean", g.clean, rgba, bir)
step("5_qc_after", g.qc, C, None, bir)
step("6_grey_halo", pm.halo_pct, C, B)
pr.disable()
T["total"] = round(sum(T.values()), 2); print(T)
s = io.StringIO(); pstats.Stats(pr, stream=s).sort_stats("tottime").print_stats(8); print(s.getvalue()[:2500])
if len(sys.argv) > 2: Path(sys.argv[2]).write_text(json.dumps(T, indent=1))
np.save(Path(sys.argv[1]).with_suffix(".clean_ref.npy") if len(sys.argv) > 3 else "/dev/null", C) if False else None
