# INFO — Round 3: AI background removal (folder comfyui-round2)

Prepared UTC: 2026-11-27T16:44:50.482215+00:00

This folder name follows the owner request. Task round 3 replaces magenta chroma key with local rembg/BiRefNet. It contains exactly four raw PNGs and four `_cut.png` outputs: the two explicitly named round-1 originals plus two new white-background generations. The earlier `comfyui-round1` folder is preserved. No game source was changed, no deployment was performed, and no LoRA/ComfyUI custom node was installed.

## Environment and model

- rembg **2.0.88**; ONNX Runtime **1.32.0**; Python **3.13.17**, installed in `C:\AI\ComfyUI-Local\.venv` with `rembg[cpu]`. Existing ComfyUI package versions were constrained and `pip check` passed.
- Model **birefnet-general**; **972,666,916 bytes** (927.61 MiB). No fallback model downloaded.
- Source: https://github.com/danielgatis/rembg/releases/download/v0.0.0/BiRefNet-general-epoch_244.onnx
- MD5 **7a35a0141cbbc80de11d9c9a28f52697**, matched checksum published in rembg's BiRefNet session; SHA-256 **58f621f00f5d756097615970a88a791584600dcf7c45b18a0a6267535a1ebd3c**.
- Software: https://github.com/danielgatis/rembg (MIT). Upstream model: https://huggingface.co/ZhengPeng7/BiRefNet (MIT). The ONNX conversion is the rembg official release named above.
- Actual provider: **CPUExecutionProvider**, **CPU**, 6 inference threads. ComfyUI SDXL generation remains on RTX 2070 SUPER via PyTorch CUDA 13.0. No CUDA Toolkit or ONNX GPU stack installed.
- Session construction/model optimization time: **6.263s**, once for this four-image batch. Per-image times below include opening, inference and PNG saving, exclude model download/import/session setup.
- Inference input normalized by rembg at 1024x1024. `alpha_matting=False`, `post_process_mask=False`. No magenta color key, no extra erosion/despill/recolor/threshold or manually edited mask. Output RGBA, original canvas 1024x1024, no crop. Soft alpha values are preserved.
- The original installation report in the previous folder predates rembg; this INFO is the current segmentation environment record. Pipeline is pending Luna/owner edge acceptance, not approved for mass production.

## Results

| Raw input | Output | CPU seconds | Fully transparent pixels | Partial alpha pixels | Fully opaque pixels |
|---|---|---:|---:|---:|---:|
| round1_warrior_raw.png | round1_warrior_cut.png | 36.393 | 761507 | 280117 | 6952 |
| round1_sword_icon_raw.png | round1_sword_icon_cut.png | 39.192 | 956676 | 58290 | 33610 |
| round3_warrior_white_raw.png | round3_warrior_white_cut.png | 37.028 | 655899 | 377058 | 15619 |
| round3_sword_icon_white_raw.png | round3_sword_icon_white_cut.png | 37.551 | 409321 | 564075 | 75180 |

RGB checks on foreground pixels with alpha >=250 (maximum absolute channel difference against input):

- `round1_warrior_cut.png`: 5
- `round1_sword_icon_cut.png`: 5
- `round3_warrior_white_cut.png`: 5
- `round3_sword_icon_white_cut.png`: 5

## New white-background generations

Two new seeds are intentionally used. The actual positive prompts contain no `magenta` requirement and end with `plain solid white background, studio product shot`. The sword prompt explicitly asks for one entire centered sword and no frame/shield/border/other objects. Negative prompts and all sampling parameters below are the exact submitted API graphs.

### heroes

Seed **812001**; API completion **15.115s**; GPU peak **7461MiB**, temperature peak **62C**.

```json
{
  "1": {
    "class_type": "CheckpointLoaderSimple",
    "inputs": {
      "ckpt_name": "sd_xl_base_1.0.safetensors"
    }
  },
  "2": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "a single cute chibi fantasy RPG warrior, full body, silver steel armor, red cape, holding one steel sword, entire head and both boots visible, centered with generous margin, detailed hand painted 2D game character illustration, plain solid white background, studio product shot",
      "clip": [
        "1",
        1
      ]
    }
  },
  "3": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "photograph, photorealistic, 3D render, text, watermark, cropped, out of frame, multiple views, character sheet, collage, duplicate objects, frame, shield, border, pink lighting, purple armor, gradient background, ground shadow, reflection",
      "clip": [
        "1",
        1
      ]
    }
  },
  "4": {
    "class_type": "EmptyLatentImage",
    "inputs": {
      "width": 1024,
      "height": 1024,
      "batch_size": 1
    }
  },
  "5": {
    "class_type": "KSampler",
    "inputs": {
      "seed": 812001,
      "steps": 25,
      "cfg": 6.5,
      "sampler_name": "euler",
      "scheduler": "normal",
      "denoise": 1.0,
      "model": [
        "1",
        0
      ],
      "positive": [
        "2",
        0
      ],
      "negative": [
        "3",
        0
      ],
      "latent_image": [
        "4",
        0
      ]
    }
  },
  "6": {
    "class_type": "VAEDecode",
    "inputs": {
      "samples": [
        "5",
        0
      ],
      "vae": [
        "1",
        2
      ]
    }
  },
  "7": {
    "class_type": "SaveImage",
    "inputs": {
      "filename_prefix": "heroes_warrior_white_round3_sdxl_s812001_20261127T163723971972Z",
      "images": [
        "6",
        0
      ]
    }
  }
}
```

### icons

Seed **812002**; API completion **15.233s**; GPU peak **7449MiB**, temperature peak **63C**.

```json
{
  "1": {
    "class_type": "CheckpointLoaderSimple",
    "inputs": {
      "ckpt_name": "sd_xl_base_1.0.safetensors"
    }
  },
  "2": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "a single ornate fantasy sword, centered, entire item visible, no frame, no shield, no border, no other objects, silver blade, gold crossguard, small cyan gemstone, hand painted 2D fantasy RPG inventory icon, generous margin, plain solid white background, studio product shot",
      "clip": [
        "1",
        1
      ]
    }
  },
  "3": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "photograph, photorealistic, 3D render, text, watermark, cropped, out of frame, multiple views, character sheet, collage, duplicate objects, frame, shield, border, pink lighting, purple armor, gradient background, ground shadow, reflection",
      "clip": [
        "1",
        1
      ]
    }
  },
  "4": {
    "class_type": "EmptyLatentImage",
    "inputs": {
      "width": 1024,
      "height": 1024,
      "batch_size": 1
    }
  },
  "5": {
    "class_type": "KSampler",
    "inputs": {
      "seed": 812002,
      "steps": 25,
      "cfg": 6.5,
      "sampler_name": "euler",
      "scheduler": "normal",
      "denoise": 1.0,
      "model": [
        "1",
        0
      ],
      "positive": [
        "2",
        0
      ],
      "negative": [
        "3",
        0
      ],
      "latent_image": [
        "4",
        0
      ]
    }
  },
  "6": {
    "class_type": "VAEDecode",
    "inputs": {
      "samples": [
        "5",
        0
      ],
      "vae": [
        "1",
        2
      ]
    }
  },
  "7": {
    "class_type": "SaveImage",
    "inputs": {
      "filename_prefix": "icons_sword_white_round3_sdxl_s812002_20261127T163740517904Z",
      "images": [
        "6",
        0
      ]
    }
  }
}
```

## Original round-1 recipes

These are byte-for-byte copies of `comfyui-round1/round1_warrior_raw.png` and `round1_sword_icon_raw.png`. Their recipes and original generation measurements are in the previous folder INFO. Warrior seed 424200; sword seed 27114402. No round-2 magenta retry image is substituted.

## SHA-256

- `round1_warrior_raw.png`: `5b82322612bce289a17a3e6a987d5e666f05286f862ebee7e5836621cf1dadab`
- `round1_warrior_cut.png`: `c6af85154b2c349839dcda4fc5ce28f9543b82c417b59f6f0f2d8cd917c2a56f`
- `round1_sword_icon_raw.png`: `d1163476be859d687b704fc915cad27a7fd53019afffe06d16921e0c532cc789`
- `round1_sword_icon_cut.png`: `8125b360bc1783d591296bdd43d56d04750eca72fcd6d3d20fefccff5b5b1bd1`
- `round3_warrior_white_raw.png`: `ff91486a169907ce2d45bb017c287ba852cf94687c35ae7ea4e62c94eadaed86`
- `round3_warrior_white_cut.png`: `3ad0fbce0a42b1c6a4613efa660541b25489f8eb48bb5a6c7987fc8cc3f2e9a2`
- `round3_sword_icon_white_raw.png`: `ed7d196695d70740cfda19b5d6dbac313a2a77d1fa6bc918cea2c426b3614fdb`
- `round3_sword_icon_white_cut.png`: `81893f976d3313bfa6fac1dc442be3e422dae71cd46648a616145a8cbe4915cb`

## Reproduce locally

The reusable script is `C:\AI\ComfyUI-Local\scripts\remove_background_ai.py`. It sets a private model cache, selects CPUExecutionProvider explicitly, reuses one session for all inputs and writes a JSON report. Example:

```powershell
& 'C:\AI\ComfyUI-Local\.venv\Scripts\python.exe' -u `
  'C:\AI\ComfyUI-Local\scripts\remove_background_ai.py' `
  --out-dir 'C:\AI\ComfyUI-Local\assets\ai-cut-review' `
  --report 'C:\AI\ComfyUI-Local\metadata\ai-cut-review.json' `
  'FULL_PATH_TO_RAW_PNG'
```

Model and images stay on this machine during segmentation. Only the explicitly authorized PNGs and this INFO are pushed to GitHub. A background remover does not recolor a pink subject, remove unwanted source objects by intent, create a missing sword tip, or guarantee alpha quality; inspect original vs cut at 100–400% on both white and dark backgrounds.

## Visual review and acceptance limits

BiRefNet removes the broad backgrounds and the round-1 sword glow much more cleanly than the earlier color key. Round-1 subject pink/magenta colors remain intentionally unchanged. The new white-background warrior retains face, armor, cape and sword details, with a small floating source flame still selected as foreground. The new sword prompt did NOT satisfy the no-frame/no-border composition: SDXL drew an ornate enclosing frame, and segmentation correctly retains that foreground object. Do not approve this image as a single isolated sword. Inspect all cuts at 100-400% on both light and dark backgrounds before accepting edges; this round does not claim production-ready masks or authorize mass monster generation.

Verification: all 4 cuts are RGBA 1024x1024 with transparency; round-1 input bytes match the already-published originals; all 86 pre-existing package versions remain unchanged; a PyTorch CUDA FP16 matrix operation still passed on RTX 2070 SUPER after rembg installation. Soft-alpha compositing in rembg can shift edge RGB (measured max difference 5 at alpha>=250); no extra recoloring was applied.

