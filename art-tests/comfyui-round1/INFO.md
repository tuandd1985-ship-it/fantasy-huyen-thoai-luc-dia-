# INFO — ComfyUI raw art tests, rounds 1 and 2

Prepared UTC: 2026-11-27T16:23:36.263625+00:00.

Purpose: Luna downloads ORIGINAL raw PNGs to test background removal and edge despill. All six PNGs keep the original ComfyUI PNG metadata. No processed image is included. No game source was modified. No new model, LoRA, or plugin was installed.

Round 1 means the four acceptance samples shown in the previous installation handoff, not the earlier rejected prompt candidates. In particular, the delivered warrior seed was **424200** and the sword icon seed was **27114402**. Round 2 retains those exact corresponding seeds. The earlier warrior candidate seed 27114400 is not the delivered comparison baseline.

Round 2 appends this exact positive text:

`completely flat solid #FF00FF magenta background, uniform single color, no gradient, no shadow, no ground, no reflection`

Round 2 appends these negative terms (including the requested five terms):

`magenta color cast on subject, pink rim light, gradient background, shadow, watermark, pink clothing, purple clothing, pink armor, purple armor`

The existing client also prefixes `(plain solid bright magenta background:1.5), (one isolated subject:1.3), ` for non-background assets. The full actual submitted graphs below are authoritative. Prompt changes alter the result even with the same seed; seed preservation provides a controlled comparison, not identical pixels.

Environment: ComfyUI 0.46.0, Python 3.13.17, PyTorch 2.14.1+cu130, torchvision 0.29.1+cu130, NVIDIA RTX 2070 SUPER 8GB, driver 610.88. Local API: 127.0.0.1:8188 only. SDXL Base 1.0 official checkpoint SHA-256: `31e35c80fc4829d14f90153f4c74cd59c90b779f6afe05a74cd6120b893f7e5b`. 1024x1024, batch 1, 25 steps, CFG 6.5, Euler/normal, denoise 1.0; FP16 UNet/text encoder, FP32 VAE.

Model source/license: https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0 — CreativeML Open RAIL++-M, see LICENSE.md in that official repository. These files are art tests, not accepted production assets. Round 1 has visible color-cast/keying problems; all new images also require visual inspection. Landscapes/maps must keep their background.

Measurements: GPU VRAM is total device memory including desktop/other apps. RAM is the ComfyUI process-tree working set. Peaks are sampled every second. Generation time covers API submission to completed server history, including model load/queue where applicable, excluding client download and keying.

| File | Seed | API completion s | GPU VRAM peak MiB | Comfy RAM peak MiB | GPU peak C |
|---|---:|---:|---:|---:|---:|
| round1_warrior_raw.png | 424200 | 15.693 | 7418 | 8949.3 | 65 |
| round1_monster_raw.png | 27114401 | 15.247 | 7476 | 8572.1 | 66 |
| round1_sword_icon_raw.png | 27114402 | 15.285 | 7543 | 8668.6 | 67 |
| round1_fantasy_map_raw.png | 27114403 | 15.653 | 7475 | 8658.0 | 66 |
| round2_warrior_raw.png | 424200 | 19.242 | 7465 | 8491.9 | 62 |
| round2_sword_icon_raw.png | 27114402 | 15.369 | 7396 | 8519.6 | 64 |

## SHA-256 and complete reproducible API recipes

Send a recipe in `{"prompt": <workflow>}` to POST `/prompt`; wait for `/history/{prompt_id}`, fetch `/view`. Do not point a public game frontend at a developer localhost API. The archived installation report predates round 2; the round-2 records below are the new measurements.

### round1_warrior_raw.png

SHA-256: `5b82322612bce289a17a3e6a987d5e666f05286f862ebee7e5836621cf1dadab`. Prompt ID: `6422310f-0f2d-4db2-abe3-16ddcfc97922`.

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
      "text": "(plain solid bright magenta background:1.5), (one isolated subject:1.3), one full body knight, silver steel armor, red cape, holding sword, entire head and boots visible, 2D painted game illustration, clean silhouette, no ground shadow",
      "clip": [
        "1",
        1
      ]
    }
  },
  "3": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "purple armor, pink clothes, purple cape, gray background, white background, scenery, panels, multiple views, character sheet, collage, cropped, extra limbs, text, watermark",
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
      "seed": 424200,
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
      "filename_prefix": "heroes_fantasy_warrior_sdxl_s424200_20261127T160438898266Z",
      "images": [
        "6",
        0
      ]
    }
  }
}
```

### round1_monster_raw.png

SHA-256: `9bb4c7608b799d15d1e70c6fab2254953b0cd0dca6b6ab836e9ac0ed6caa3987`. Prompt ID: `06a3ea75-635c-43b3-b6cc-bf564cbe8132`.

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
      "text": "(plain solid bright magenta background:1.5), (one isolated subject:1.3), full body forest goblin monster, ears hands and feet visible, green skin, brown leather tunic, holding wooden club, centered with margin, painted 2D fantasy RPG illustration, clean silhouette, no ground shadow",
      "clip": [
        "1",
        1
      ]
    }
  },
  "3": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "photograph, 3d render, cropped, out of frame, extra limbs, extra fingers, deformed hands, duplicate, multiple views, panels, character sheet, collage, sketches, text, watermark, scenery, gradient background, ground shadow",
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
      "seed": 27114401,
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
      "filename_prefix": "monsters_forest_goblin_sdxl_s27114401_20261127T160050117650Z",
      "images": [
        "6",
        0
      ]
    }
  }
}
```

### round1_sword_icon_raw.png

SHA-256: `d1163476be859d687b704fc915cad27a7fd53019afffe06d16921e0c532cc789`. Prompt ID: `fd097f4d-524c-4341-b585-1495e185d14a`.

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
      "text": "(plain solid bright magenta background:1.5), (one isolated subject:1.3), one enchanted sword inventory icon, entire sword visible, silver blade, ornate gold crossguard, cyan rune, diagonal, centered with margin, painted 2D fantasy RPG illustration, clean silhouette, no ground shadow",
      "clip": [
        "1",
        1
      ]
    }
  },
  "3": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "photograph, 3d render, cropped, out of frame, extra limbs, extra fingers, deformed hands, duplicate, multiple views, panels, character sheet, collage, sketches, text, watermark, scenery, gradient background, ground shadow",
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
      "seed": 27114402,
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
      "filename_prefix": "icons_enchanted_sword_sdxl_s27114402_20261127T160107145083Z",
      "images": [
        "6",
        0
      ]
    }
  }
}
```

### round1_fantasy_map_raw.png

SHA-256: `60ce4817768379374b647b8053840fc0bbf70d3d2edfd7b1aa4224c65fdf5b84`. Prompt ID: `35ca4cc9-35e8-4034-a440-51956dde9c05`.

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
      "text": "fantasy RPG world map landscape, top down illustrated regional map, emerald forests, winding river, blue lake, stone castle village, golden roads, mountain range, hand painted 2D game map, rich coherent colors, readable terrain, full canvas environment, no labels, no lettering, no border",
      "clip": [
        "1",
        1
      ]
    }
  },
  "3": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "photograph, 3d render, text, watermark, blurry, low quality",
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
      "seed": 27114403,
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
      "filename_prefix": "backgrounds_fantasy_map_landscape_sdxl_s27114403_20261127T155945088257Z",
      "images": [
        "6",
        0
      ]
    }
  }
}
```

### round2_warrior_raw.png

SHA-256: `d91d92567e14742812c880024328862fea6523ff2be6b7bb804c8fcd2f3e423d`. Prompt ID: `7d6a9acd-31a5-40eb-a687-99d5c1db641c`.

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
      "text": "(plain solid bright magenta background:1.5), (one isolated subject:1.3), one full body knight, silver steel armor, red cape, holding sword, entire head and boots visible, 2D painted game illustration, clean silhouette, no ground shadow, completely flat solid #FF00FF magenta background, uniform single color, no gradient, no shadow, no ground, no reflection, clean silhouette, no ground shadow",
      "clip": [
        "1",
        1
      ]
    }
  },
  "3": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "purple armor, pink clothes, purple cape, gray background, white background, scenery, panels, multiple views, character sheet, collage, cropped, extra limbs, text, watermark, magenta color cast on subject, pink rim light, gradient background, shadow, watermark, pink clothing, purple clothing, pink armor, purple armor",
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
      "seed": 424200,
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
      "filename_prefix": "heroes_fantasy_warrior_round2_sdxl_s424200_20261127T162259713946Z",
      "images": [
        "6",
        0
      ]
    }
  }
}
```

### round2_sword_icon_raw.png

SHA-256: `5b7bf2bbd98057e4ed45a384b3d3d54d5c4c4269176ac4bc99d15052454edeb4`. Prompt ID: `8966f10e-5b27-4843-9f4d-690d614aa037`.

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
      "text": "(plain solid bright magenta background:1.5), (one isolated subject:1.3), one enchanted sword inventory icon, entire sword visible, silver blade, ornate gold crossguard, cyan rune, diagonal, centered with margin, painted 2D fantasy RPG illustration, clean silhouette, no ground shadow, completely flat solid #FF00FF magenta background, uniform single color, no gradient, no shadow, no ground, no reflection, clean silhouette, no ground shadow",
      "clip": [
        "1",
        1
      ]
    }
  },
  "3": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "photograph, 3d render, cropped, out of frame, extra limbs, extra fingers, deformed hands, duplicate, multiple views, panels, character sheet, collage, sketches, text, watermark, scenery, gradient background, ground shadow, magenta color cast on subject, pink rim light, gradient background, shadow, watermark, pink clothing, purple clothing, pink armor, purple armor",
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
      "seed": 27114402,
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
      "filename_prefix": "icons_enchanted_sword_round2_sdxl_s27114402_20261127T162320362127Z",
      "images": [
        "6",
        0
      ]
    }
  }
}
```

## Visual review of round 2

The prompt was submitted exactly as documented, but the requested uniform #FF00FF background was NOT achieved. The warrior still has a strong pink/magenta color cast, a gray-to-pink gradient background, and a ground shadow. The sword icon has an unwanted decorative frame/shield, a nonuniform dark magenta background, and does not satisfy the isolated single-sword composition. These are raw failure/comparison samples for Luna, not approved game assets. No further images were generated in this round.

