"""Minimal stdlib client for the local ComfyUI (127.0.0.1:8188). Native nodes only."""
import json, time, uuid, urllib.request, urllib.parse
from pathlib import Path

HOST = "http://127.0.0.1:8188"
CKPT = "sd_xl_base_1.0.safetensors"


def _post(path, data, ctype="application/json"):
    req = urllib.request.Request(HOST + path, data=data, headers={"Content-Type": ctype})
    return json.load(urllib.request.urlopen(req, timeout=60))


def upload(path):
    b = "----gac" + uuid.uuid4().hex
    body = (f"--{b}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{Path(path).name}\"\r\n"
            f"Content-Type: image/png\r\n\r\n").encode() + Path(path).read_bytes() + \
           f"\r\n--{b}\r\nContent-Disposition: form-data; name=\"overwrite\"\r\n\r\ntrue\r\n--{b}--\r\n".encode()
    return _post("/upload/image", body, f"multipart/form-data; boundary={b}")["name"]


def run(wf, out_path, timeout=900):
    pid = _post("/prompt", json.dumps({"prompt": wf, "client_id": "game-art-core"}).encode())["prompt_id"]
    t0 = time.time()
    while time.time() - t0 < timeout:
        h = json.load(urllib.request.urlopen(f"{HOST}/history/{pid}", timeout=30))
        if pid in h and h[pid].get("outputs"):
            for node in h[pid]["outputs"].values():
                for im in node.get("images", []):
                    q = urllib.parse.urlencode({"filename": im["filename"], "subfolder": im["subfolder"], "type": im["type"]})
                    Path(out_path).write_bytes(urllib.request.urlopen(f"{HOST}/view?{q}", timeout=120).read())
                    return pid, round(time.time() - t0, 1)
        if pid in h and h[pid].get("status", {}).get("status_str") == "error":
            raise RuntimeError(json.dumps(h[pid]["status"])[:800])
        time.sleep(1.5)
    raise TimeoutError(pid)


def base(pos, neg, seed, steps=28, cfg=6.5):
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": CKPT}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {"text": pos, "clip": ["1", 1]}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"text": neg, "clip": ["1", 1]}},
        "5": {"class_type": "KSampler", "inputs": {"model": ["1", 0], "positive": ["2", 0], "negative": ["3", 0], "latent_image": ["4", 0],
                                                   "seed": seed, "steps": steps, "cfg": cfg, "sampler_name": "dpmpp_2m", "scheduler": "karras", "denoise": 1.0}},
        "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
        "7": {"class_type": "SaveImage", "inputs": {"images": ["6", 0], "filename_prefix": "game_art_core/rung_xanh"}},
    }


def txt2img(pos, neg, seed, w=1024, h=1024, **kw):
    wf = base(pos, neg, seed, **kw)
    wf["4"] = {"class_type": "EmptyLatentImage", "inputs": {"width": w, "height": h, "batch_size": 1}}
    return wf


def inpaint(image_name, pos, neg, seed, denoise=0.6, **kw):
    """image_name: uploaded RGBA png; transparent pixels = area to repaint (LoadImage mask = 1 - alpha)."""
    wf = base(pos, neg, seed, **kw)
    wf["8"] = {"class_type": "LoadImage", "inputs": {"image": image_name}}
    wf["9"] = {"class_type": "VAEEncode", "inputs": {"pixels": ["8", 0], "vae": ["1", 2]}}
    wf["4"] = {"class_type": "SetLatentNoiseMask", "inputs": {"samples": ["9", 0], "mask": ["8", 1]}}
    wf["5"]["inputs"]["denoise"] = denoise
    return wf
