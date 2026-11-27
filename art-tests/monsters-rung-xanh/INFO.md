# INFO — Bộ quái Rừng Xanh

Chuẩn bị UTC: 2026-11-27T17:25:44.376211+00:00

Phạm vi chủ dự án đã duyệt: 5 loại quái, mỗi loại 2 seed; SDXL 1024×1024 nền trắng + rembg BiRefNet; không LoRA/plugin mới; không sửa source game hoặc deploy. Bộ này gồm đúng **10 raw PNG + 10 cut PNG RGBA**, là ảnh tĩnh để nghiệm thu, chưa có animation và chưa tích hợp vào runtime game.

## Bảng thiết kế gốc được lưu làm khuôn cho các map sau

Phong cách chung (giữ trong mọi positive prompt):

`2D chibi game art, thick bold outlines, cel shading, vibrant colors, full body, three-quarter view, single character, plain solid white background`

Negative chung (giữ trong mọi negative prompt):

`frame, border, emblem, multiple characters, other objects, text, watermark, gradient background, shadow, realistic, 3D render`

| Mã asset | Mô tả chủ dự án cung cấp |
|---|---|
| `monster_slime` | cute chibi emerald-green slime monster, round translucent jelly dome body, glossy white highlight on top, big round black eyes, small happy smile, tiny leaf sprout on its head, no arms, no legs |
| `monster_goblin` | mischievous chibi goblin warrior, dark green skin, big head, long pointy ears, small fang grin, torn brown leather armor, orange neck scarf, holding a spiked wooden club, short legs, brown boots |
| `monster_wolf` | fierce chibi forest wolf, slim body, blue-grey fur, fluffy white neck mane and tail, pointy ears, sharp yellow eyes, visible claws, ready-to-pounce stance |
| `monster_goblin_archer` | chibi goblin archer, green skin, long pointy ears, brown hood, moss-green cloak, holding a short wooden bow, quiver of arrows on its back, one eye squinting aiming |
| `boss_wolf_lord` | giant chibi alpha wolf boss, much bigger and more majestic than a normal wolf, dark charcoal-grey fur, long mane, glowing green rune markings on shoulder and hip, scar across left eye, glowing green eyes, bared fangs, menacing |

Các chi tiết nhận diện: Slime xanh ngọc + mầm lá; Goblin xanh đậm + khăn cam/giáp nâu/chùy gỗ; Sói lông xanh xám + bờm/đuôi trắng; Goblin cung thủ mũ nâu + áo choàng xanh rêu/cung ngắn/bao tên; Chúa Sói than xám + rune/mắt xanh phát sáng/sẹo mắt trái. Boss cần có kích thước hiển thị lớn hơn sói thường khi tích hợp sau này; việc scale trong game chưa thực hiện và không thể suy ra chỉ từ cùng canvas1024.

## Cách dựng prompt và hai seed

Hai seed gốc là **628401** và **628402**. Sau QA, Goblin dùng **947201/947202**, boss dùng **947301/628402** để loại ảnh nhân đôi/ảnh chân dung. Mỗi loại cuối cùng vẫn có đúng2seed. Biến thể1 không có hậu tố, biến thể2 dùng `_s2` trước `_raw.png`/`_cut.png`. Seed không tự đảm bảo đồng nhất style; cần nhìn và duyệt từng ảnh.

Lượt đầu bám văn bản nguyên bản nhưng model vẽ Slime có tay/chân/mũ kính và Goblin có sừng/vũ khí sai. Các ứng viên đó đã được giữ local và loại khỏi thư mục công bố. Lượt bàn giao vẫn giữ nguyên hai seed, thêm mô tả chủ thể có trọng số ở đầu và negative riêng để loại anatomy/phụ kiện sai; toàn bộ prompt chung vẫn có mặt. Với Slime, yêu cầu không tay/chân được chuyển sang negative rõ ràng, tránh đưa tên bộ phận vào positive. Không đổi model/sampler/CFG để tạo biến thể. Actual graph từng ảnh ở cuối là công thức tái tạo chính xác.

## Môi trường và tài nguyên

- ComfyUI0.46.0, Python3.13.17 riêng, PyTorch2.14.1+cu130/torchvision0.29.1+cu130, NVIDIA RTX2070 SUPER8GB, driver610.88. API chỉ127.0.0.1:8188.
- SDXL Base1.0 chính thức; SHA256 `31e35c80fc4829d14f90153f4c74cd59c90b779f6afe05a74cd6120b893f7e5b`; CreativeML Open RAIL++-M: https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0 .
- Tất cả: 1024×1024, batch1, Euler/normal,25 steps,CFG6.5,denoise1; UNet/text encoderFP16,VAEFP32. Positive được gửi nguyên văn bằng `--exact-prompt --background white`, không thêm prefix magenta hoặc studio/product-shot ngoài mô tả đã ghi.
- rembg **2.0.88**, ONNX Runtime **1.32.0**; provider thực tế **CPUExecutionProvider**; **CPU**,6 threads.
- Model **birefnet-general**, **972,666,916 bytes** (927.61MiB), SHA256 `58f621f00f5d756097615970a88a791584600dcf7c45b18a0a6267535a1ebd3c`. Source: https://github.com/danielgatis/rembg/releases/download/v0.0.0/BiRefNet-general-epoch_244.onnx ; upstream model MIT: https://huggingface.co/ZhengPeng7/BiRefNet . Model không được đưa vào repo.
- Nạp session **6.778s** ở lượt10ảnh. Sinh GPU và tách CPU chồng thời gian. Wall lượt refined đầu **449.48s**, không gồm thay3ứng viên sau QA, lượt bị loại, cleanup cuối hoặc đẩy GitHub; không dùng số này làm tổng thời gian toàn bộ công việc. Bảng dưới dùng số đo đúng của10file cuối.
- `alpha_matting=False`, `post_process_mask=False`. Theo docs/MONSTER_DESIGN_RUNG_XANH.md vừa được Muse bổ sung, sau BiRefNet chỉ giữ thành phần liên thông8 lớn nhất của alpha>16, chừa2pixel soft-edge. Không chroma key, không recolor/crop/mask thủ công. Lọc có thể bỏ chi tiết mảnh tách rời; cần kiểm dây cung, đầu mũi tên và mầm lá ở100–400%.

## Thời gian thực tế và thông số từng ảnh

Thời gian gen tính từ submit API tới completed history (có queue/nạp model nếu xảy ra), chưa tính tải raw/client. Cut gồm mở ảnh/inference/lưu PNG, không gồm nạp model/import. VRAM là tổng GPU gồm desktop; RAM là working set cây tiến trình ComfyUI, không gồm worker rembg. Peaks lấy mẫu1giây. Vì GPU/CPU chạy đồng thời, số đo có thể chậm hơn thử từng ảnh đơn.

| Asset | Seed | Gen s | Cut CPU s | GPU peak MiB | Comfy RAM MiB | GPU max °C |
|---|---:|---:|---:|---:|---:|---:|
| `monster_slime_raw.png` | 628401 | 16.15 | 44.15 | 7400 | 8915.5 | 64 |
| `monster_slime_s2_raw.png` | 628402 | 27.73 | 48.42 | 7880 | 9271.5 | 61 |
| `monster_goblin_raw.png` | 947201 | 19.28 | 47.83 | 7436 | 9191.0 | 66 |
| `monster_goblin_s2_raw.png` | 947202 | 22.30 | 40.31 | 7931 | 9095.0 | 63 |
| `monster_wolf_raw.png` | 628401 | 25.48 | 40.43 | 7272 | 8771.8 | 64 |
| `monster_wolf_s2_raw.png` | 628402 | 36.88 | 51.21 | 6419 | 8742.6 | 63 |
| `monster_goblin_archer_raw.png` | 628401 | 32.29 | 46.44 | 7564 | 8612.0 | 63 |
| `monster_goblin_archer_s2_raw.png` | 628402 | 23.59 | 37.27 | 6574 | 8890.2 | 64 |
| `boss_wolf_lord_raw.png` | 947301 | 24.49 | 39.70 | 7626 | 8979.0 | 63 |
| `boss_wolf_lord_s2_raw.png` | 628402 | 25.56 | 39.21 | 7134 | 9028.6 | 63 |

## QA và trạng thái nghiệm thu

Các kiểm tra file:20PNG mở được;10cutRGBA1024×1024, có pixelalpha0 và foregroundalpha≥250; SHA256 khớp record. Đây là kiểm tra tính toàn vẹn, không tự chứng minh đúng art/anatomy. Cut preview đã xem trên nền xanh cỏ, raw được giữ để đối chiếu. Chưa tự chọn seed chiến thắng, chưa đổi balance/scale/animation hoặc khai báo ASSETS.

- `monster_slime_cut.png`: CHƯA KHỚP HOÀN TOÀN: đã bỏ anatomy tay/chân kiểu người, nhưng có các thân lá lớn hai bên thay vì một mầm lá nhỏ trên đỉnh; màu xanh và mặt dễ đọc. Không coi là bản Slime đã đạt brief.
- `monster_slime_s2_cut.png`: ỨNG VIÊN ƯU TIÊN cho Slime: thân thạch tròn không tay/chân, mắt đen, mầm lá phía trên; mầm lá vẫn lớn hơn mô tả tiny, cần duyệt giọt thạch và silhouette trên cỏ.
- `monster_goblin_cut.png`: CHƯA ĐẠT vũ khí: da xanh, giáp nâu, khăn cam và một nhân vật đã rõ, nhưng SDXL vẫn vẽ đầu rìu kim loại thay chùy gỗ có đinh. Không dùng làm Goblin melee chính thức khi chưa sửa/duyệt.
- `monster_goblin_s2_cut.png`: CHƯA ĐẠT vũ khí/anatomy: có đầu tròn bằng gỗ nhưng còn đầu nhọn kim loại ở phía kia và nốt giống sừng trên đầu. Da xanh/khăn cam/giáp nâu đủ nhận diện; cần sửa trước khi chốt.
- `monster_wolf_cut.png`: Ứng viên dáng đứng, mắt vàng, lông xanh xám/trắng; thiên về sói con hiền, chưa đạt tư thế fierce ready-to-pounce. Độ cel-shading khác seed2, cần chọn style thống nhất.
- `monster_wolf_s2_cut.png`: ỨNG VIÊN ƯU TIÊN cho Sói: bốn chân, thân thấp sẵn sàng vồ, mắt vàng, lông xanh xám và bờm trắng; kiểm mép lông/móng ở100–400%.
- `monster_goblin_archer_cut.png`: ỨNG VIÊN ƯU TIÊN cho Cung thủ: một chủ thể, cung gỗ và dây cung nhận diện rõ; hood còn xanh thay vì nâu, ống tên chưa nổi bật, chưa đủ để tick toàn bộ brief.
- `monster_goblin_archer_s2_cut.png`: Có tư thế ngắm và cung gỗ, nhưng cung lớn hơn yêu cầu short bow, hood xanh thay nâu; kiểm hình bàn tay, dây cung và ống tên trước khi chọn.
- `boss_wolf_lord_cut.png`: CHƯA KHỚP palette: đã là toàn thân thay chân dung, nhưng lông xanh sáng nhiều hơn than xám, rune/sẹo mắt trái chưa rõ. Chỉ là biến thể so sánh, không chốt boss.
- `boss_wolf_lord_s2_cut.png`: ỨNG VIÊN ƯU TIÊN cho Boss: thân than xám, bờm dài, mắt/rune xanh, răng nanh, khác sói thường; sẹo mắt trái chưa rõ và kích thước3x trong game chưa triển khai, cần duyệt riêng.

Mỗi asset cần chủ dự án/Muse duyệt: loài/anatomy đúng; đọc được silhouette trên cỏ; màu/viền/đổ bóng thống nhất; đúng phụ kiện; không chữ/khung/phụ vật; đủ toàn thân và margin; không viền nền hoặc mất chi tiết mảnh; chọn s1/s2. Chưa có phê duyệt nghiệm thu thì không tự đưa vào game.

## Hash và foreground bbox

- `monster_slime_raw.png` SHA256 `c016673b78f558a6cdafa5e29edea3a07c7503f75cd7532d9106bf27dff26a8e`
- `monster_slime_cut.png` SHA256 `ec8f31d9582cb551305c9a1ac4adf99c92be13b6c37698219bb851e68f1ecd27`; bbox alpha>127 `[82, 170, 966, 898]`, alpha0 `619768`, alpha1..254 `414034`.
- `monster_slime_s2_raw.png` SHA256 `1556a818c783a43136569139582d843f9083911002bf30c60cebcc95e1c78b68`
- `monster_slime_s2_cut.png` SHA256 `9760c62b605ef33477d7a6474771fb77693c7328cde328256632fb1aa102a267`; bbox alpha>127 `[142, 76, 877, 925]`, alpha0 `660049`, alpha1..254 `364567`.
- `monster_goblin_raw.png` SHA256 `9a0400f8c5e8b71e6202e34fe1f90556dbcd0efb6f7da3c8bc840e61fb25d75e`
- `monster_goblin_cut.png` SHA256 `1fe5faac6cd95e595dfe55d7567464b4b0c10f81e011070054dc711390ff43fb`; bbox alpha>127 `[78, 56, 940, 948]`, alpha0 `675756`, alpha1..254 `366688`.
- `monster_goblin_s2_raw.png` SHA256 `ad6e5857d038bc57f58a37d780dda5047b7df11896937fc9ee653d769b01601e`
- `monster_goblin_s2_cut.png` SHA256 `d453da7c67d35b4a60d5c2c68866c45fea514d1d46371dd9fb77485d60905c38`; bbox alpha>127 `[33, 45, 909, 974]`, alpha0 `679255`, alpha1..254 `365415`.
- `monster_wolf_raw.png` SHA256 `fc442fb8fb8ed0e21b3660f59b86cf159a846ce6491aeaf0c64e101de7c77c23`
- `monster_wolf_cut.png` SHA256 `0f1a88e55a56651013e1da5fab3f13f976cd3c016771e22da2c604b1dd7ad1f6`; bbox alpha>127 `[191, 52, 908, 982]`, alpha0 `689376`, alpha1..254 `318876`.
- `monster_wolf_s2_raw.png` SHA256 `5ac79cdca59031011e393f950630f738fa2d6af8629db58237fa0a3d6bdf3967`
- `monster_wolf_s2_cut.png` SHA256 `c2787fc7683babef44c365e78121ecce247a347faa07e41547d534ec26ece9d4`; bbox alpha>127 `[27, 61, 978, 950]`, alpha0 `552644`, alpha1..254 `472649`.
- `monster_goblin_archer_raw.png` SHA256 `f52103fad14058f619e30942f3798486cb27fd830dec2cab3920ba99445f0fda`
- `monster_goblin_archer_cut.png` SHA256 `49ee4784639e3beda73a17ec6ae8844656b117f0162a7cc4f99d8dcfbe92cae3`; bbox alpha>127 `[78, 40, 992, 967]`, alpha0 `644936`, alpha1..254 `382606`.
- `monster_goblin_archer_s2_raw.png` SHA256 `83c74b10014ab2cf05587094768a5ce1c328632c011230389ec4a0684bd640be`
- `monster_goblin_archer_s2_cut.png` SHA256 `5b5fbc68181742e861b33f817ad3f0d72576147166aa1854f9b020b6fdb5921d`; bbox alpha>127 `[45, 42, 922, 943]`, alpha0 `804545`, alpha1..254 `226279`.
- `boss_wolf_lord_raw.png` SHA256 `5cdec45317387dc79735f4d31d83fd4f1fa80d76c9b37f8da62407e03886e32c`
- `boss_wolf_lord_cut.png` SHA256 `69a7aa36fe0dfeb227611d27d50a967217039435f9c9d17b79cb3cfd0b1ba1fd`; bbox alpha>127 `[73, 119, 948, 932]`, alpha0 `701809`, alpha1..254 `320610`.
- `boss_wolf_lord_s2_raw.png` SHA256 `e0afe2956cb7867dd442bc5fce0a8d7b447b54355852ed23aeb1c7c31e4338cf`
- `boss_wolf_lord_s2_cut.png` SHA256 `201f52776c7ad01df082775b9e2bdff5f7e945bb9bc7341b7242605a8b98d18f`; bbox alpha>127 `[39, 23, 992, 997]`, alpha0 `527330`, alpha1..254 `500566`.

## Actual API workflow cho từng ứng viên

Để sinh lại: POST `http://127.0.0.1:8188/prompt` body `{"prompt": <graph>}`, đợi history, lấy raw qua `/view`. Tách lại bằng script `C:\AI\ComfyUI-Local\scripts\remove_background_ai.py --largest-component` với các raw mong muốn và model cache local. Cùng seed nhưng khác phiên bản/GPU/precision có thể không khớp từng bit.

### monster_slime_raw.png

Prompt ID `1ce4504e-46bb-49f7-b374-11edeb948644`.

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
      "text": "(one armless legless emerald-green slime blob:1.4), a single low round jelly mound, a tiny leaf sprout growing directly from its top, 2D chibi game art, thick bold outlines, cel shading, vibrant colors, full body, three-quarter view, single character, plain solid white background, cute chibi emerald-green slime monster, round translucent jelly dome body, glossy white highlight on top, big round black eyes, small happy smile, tiny leaf sprout on top of its jelly dome, entire silhouette visible with generous white margin, isolated game sprite",
      "clip": [
        "1",
        1
      ]
    }
  },
  "3": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "frame, border, emblem, multiple characters, other objects, text, watermark, gradient background, shadow, realistic, 3D render, cropped, cut off, close up, scenery, forest background, room, landscape, ground, floor, background decoration, arms, legs, hands, feet, humanoid, torso, neck, astronaut, helmet, spacesuit, glass container, bowl, jar, pot, floating leaves, bubbles",
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
      "seed": 628401,
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
      "filename_prefix": "monsters_monster_slime_refined_forest_production_sdxl_s628401_20261127T171100143110Z",
      "images": [
        "6",
        0
      ]
    }
  }
}
```

### monster_slime_s2_raw.png

Prompt ID `fb54ce1c-9169-476b-b7be-a5e781bdafa4`.

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
      "text": "(one armless legless emerald-green slime blob:1.4), a single low round jelly mound, a tiny leaf sprout growing directly from its top, 2D chibi game art, thick bold outlines, cel shading, vibrant colors, full body, three-quarter view, single character, plain solid white background, cute chibi emerald-green slime monster, round translucent jelly dome body, glossy white highlight on top, big round black eyes, small happy smile, tiny leaf sprout on top of its jelly dome, entire silhouette visible with generous white margin, isolated game sprite",
      "clip": [
        "1",
        1
      ]
    }
  },
  "3": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "frame, border, emblem, multiple characters, other objects, text, watermark, gradient background, shadow, realistic, 3D render, cropped, cut off, close up, scenery, forest background, room, landscape, ground, floor, background decoration, arms, legs, hands, feet, humanoid, torso, neck, astronaut, helmet, spacesuit, glass container, bowl, jar, pot, floating leaves, bubbles",
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
      "seed": 628402,
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
      "filename_prefix": "monsters_monster_slime_s2_refined_forest_production_sdxl_s628402_20261127T171130302910Z",
      "images": [
        "6",
        0
      ]
    }
  }
}
```

### monster_goblin_raw.png

Prompt ID `b15cc74d-02a5-43a6-ae74-980c512853f0`.

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
      "text": "(a single goblin warrior:1.25), dark green skin, (torn brown leather armor:1.25), (small orange scarf around the neck:1.25), big head, long pointy ears, small fang grin, (holding a short thick brown wooden cudgel:1.5), (a rounded wooden club head with a few iron nail studs:1.3), short legs, brown boots, 2D chibi game art, thick bold outlines, cel shading, vibrant colors, full body, three-quarter view, single character, plain solid white background, solo, entire body centered with generous white margin",
      "clip": [
        "1",
        1
      ]
    }
  },
  "3": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "frame, border, emblem, multiple characters, other objects, text, watermark, gradient background, shadow, realistic, 3D render, two characters, group, lineup, character sheet, turnaround, duplicate, horns, antlers, wings, extra weapons, two weapons, axe, hatchet, battleaxe, spear, lance, pointed spearhead, sword, metal blade, polearm, staff, bow, shield, orange shirt, orange vest, white shirt, hat, hood, signature, ground, floor, scenery, cropped, extra arms, extra legs",
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
      "seed": 947201,
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
      "filename_prefix": "monsters_monster_goblin_last_candidate_sdxl_s947201_20261127T172027689169Z",
      "images": [
        "6",
        0
      ]
    }
  }
}
```

### monster_goblin_s2_raw.png

Prompt ID `3b1975e2-b96f-4976-972d-d51128d4faab`.

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
      "text": "(a single goblin warrior:1.25), dark green skin, (torn brown leather armor:1.25), (small orange scarf around the neck:1.25), big head, long pointy ears, small fang grin, (holding a short thick brown wooden cudgel:1.5), (a rounded wooden club head with a few iron nail studs:1.3), short legs, brown boots, 2D chibi game art, thick bold outlines, cel shading, vibrant colors, full body, three-quarter view, single character, plain solid white background, solo, entire body centered with generous white margin",
      "clip": [
        "1",
        1
      ]
    }
  },
  "3": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "frame, border, emblem, multiple characters, other objects, text, watermark, gradient background, shadow, realistic, 3D render, two characters, group, lineup, character sheet, turnaround, duplicate, horns, antlers, wings, extra weapons, two weapons, axe, hatchet, battleaxe, spear, lance, pointed spearhead, sword, metal blade, polearm, staff, bow, shield, orange shirt, orange vest, white shirt, hat, hood, signature, ground, floor, scenery, cropped, extra arms, extra legs",
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
      "seed": 947202,
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
      "filename_prefix": "monsters_monster_goblin_s2_last_candidate_sdxl_s947202_20261127T172050176339Z",
      "images": [
        "6",
        0
      ]
    }
  }
}
```

### monster_wolf_raw.png

Prompt ID `94923c80-da9d-48f2-b7f7-e79226d5bcd2`.

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
      "text": "(one four-legged blue-grey wolf animal:1.3), a low crouching ready-to-pounce pose, white fluffy neck fur, 2D chibi game art, thick bold outlines, cel shading, vibrant colors, full body, three-quarter view, single character, plain solid white background, fierce chibi forest wolf, slim body, blue-grey fur, fluffy white neck mane and tail, pointy ears, sharp yellow eyes, visible claws, ready-to-pounce stance, entire silhouette visible with generous white margin, isolated game sprite",
      "clip": [
        "1",
        1
      ]
    }
  },
  "3": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "frame, border, emblem, multiple characters, other objects, text, watermark, gradient background, shadow, realistic, 3D render, cropped, cut off, close up, scenery, forest background, room, landscape, ground, floor, background decoration, humanoid, biped, human hands, clothing, armor, weapon, collar, standing upright, sitting, fox, yellow mane",
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
      "seed": 628401,
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
      "filename_prefix": "monsters_monster_wolf_refined_forest_production_sdxl_s628401_20261127T171300080245Z",
      "images": [
        "6",
        0
      ]
    }
  }
}
```

### monster_wolf_s2_raw.png

Prompt ID `44cb498f-43b0-4720-86fe-99c4a272ada9`.

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
      "text": "(one four-legged blue-grey wolf animal:1.3), a low crouching ready-to-pounce pose, white fluffy neck fur, 2D chibi game art, thick bold outlines, cel shading, vibrant colors, full body, three-quarter view, single character, plain solid white background, fierce chibi forest wolf, slim body, blue-grey fur, fluffy white neck mane and tail, pointy ears, sharp yellow eyes, visible claws, ready-to-pounce stance, entire silhouette visible with generous white margin, isolated game sprite",
      "clip": [
        "1",
        1
      ]
    }
  },
  "3": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "frame, border, emblem, multiple characters, other objects, text, watermark, gradient background, shadow, realistic, 3D render, cropped, cut off, close up, scenery, forest background, room, landscape, ground, floor, background decoration, humanoid, biped, human hands, clothing, armor, weapon, collar, standing upright, sitting, fox, yellow mane",
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
      "seed": 628402,
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
      "filename_prefix": "monsters_monster_wolf_s2_refined_forest_production_sdxl_s628402_20261127T171329870058Z",
      "images": [
        "6",
        0
      ]
    }
  }
}
```

### monster_goblin_archer_raw.png

Prompt ID `faa9ad2d-9fd0-4b41-8c7f-acece334f6ed`.

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
      "text": "(one green-skinned goblin archer:1.3), brown hood, moss green cloak, (holding and aiming a short wooden bow with a visible bowstring:1.3), 2D chibi game art, thick bold outlines, cel shading, vibrant colors, full body, three-quarter view, single character, plain solid white background, chibi goblin archer, green skin, long pointy ears, brown hood, moss-green cloak, holding a short wooden bow, quiver of arrows on its back, one eye squinting aiming, entire silhouette visible with generous white margin, isolated game sprite",
      "clip": [
        "1",
        1
      ]
    }
  },
  "3": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "frame, border, emblem, multiple characters, other objects, text, watermark, gradient background, shadow, realistic, 3D render, cropped, cut off, close up, scenery, forest background, room, landscape, ground, floor, background decoration, horns, antlers, wings, pale skin, brown skin, human skin, staff, spear, sword, club, gun, shield, oversized bow",
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
      "seed": 628401,
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
      "filename_prefix": "monsters_monster_goblin_archer_refined_forest_production_sdxl_s628401_20261127T171411485086Z",
      "images": [
        "6",
        0
      ]
    }
  }
}
```

### monster_goblin_archer_s2_raw.png

Prompt ID `2ee55cb6-af36-457c-8dca-8b2c1177a648`.

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
      "text": "(one green-skinned goblin archer:1.3), brown hood, moss green cloak, (holding and aiming a short wooden bow with a visible bowstring:1.3), 2D chibi game art, thick bold outlines, cel shading, vibrant colors, full body, three-quarter view, single character, plain solid white background, chibi goblin archer, green skin, long pointy ears, brown hood, moss-green cloak, holding a short wooden bow, quiver of arrows on its back, one eye squinting aiming, entire silhouette visible with generous white margin, isolated game sprite",
      "clip": [
        "1",
        1
      ]
    }
  },
  "3": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "frame, border, emblem, multiple characters, other objects, text, watermark, gradient background, shadow, realistic, 3D render, cropped, cut off, close up, scenery, forest background, room, landscape, ground, floor, background decoration, horns, antlers, wings, pale skin, brown skin, human skin, staff, spear, sword, club, gun, shield, oversized bow",
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
      "seed": 628402,
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
      "filename_prefix": "monsters_monster_goblin_archer_s2_refined_forest_production_sdxl_s628402_20261127T171448158886Z",
      "images": [
        "6",
        0
      ]
    }
  }
}
```

### boss_wolf_lord_raw.png

Prompt ID `44fa18fb-67b3-464c-9a49-027145c97b14`.

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
      "text": "(full-body four-legged alpha wolf animal:1.4), (all four paws and entire tail visible:1.3), (small subject surrounded by wide white margin:1.25), dark charcoal grey fur, long mane, glowing green runes on shoulder and hip, scar across left eye, glowing green eyes, bared fangs, menacing, giant majestic wolf boss, 2D chibi game art, thick bold outlines, cel shading, vibrant colors, full body, three-quarter view, single character, plain solid white background",
      "clip": [
        "1",
        1
      ]
    }
  },
  "3": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "frame, border, emblem, multiple characters, other objects, text, watermark, gradient background, shadow, realistic, 3D render, portrait, headshot, face close-up, cropped, cut off, out of frame, large face, disembodied head, humanoid, biped, human hands, clothing, armor, weapon, collar, forest, landscape, scenery, ground, floor, white fur, blue eyes, yellow eyes",
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
      "seed": 947301,
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
      "filename_prefix": "monsters_boss_wolf_lord_last_candidate_sdxl_s947301_20261127T172115917016Z",
      "images": [
        "6",
        0
      ]
    }
  }
}
```

### boss_wolf_lord_s2_raw.png

Prompt ID `30fab842-f6ae-4ac6-a65c-6bf4ab55bf16`.

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
      "text": "(one huge four-legged charcoal-grey alpha wolf animal:1.3), (glowing green eyes and green runes on shoulder and hip:1.3), a long mane, scar across its left eye, 2D chibi game art, thick bold outlines, cel shading, vibrant colors, full body, three-quarter view, single character, plain solid white background, giant chibi alpha wolf boss, much bigger and more majestic than a normal wolf, dark charcoal-grey fur, long mane, glowing green rune markings on shoulder and hip, scar across left eye, glowing green eyes, bared fangs, menacing, entire silhouette visible with generous white margin, isolated game sprite",
      "clip": [
        "1",
        1
      ]
    }
  },
  "3": {
    "class_type": "CLIPTextEncode",
    "inputs": {
      "text": "frame, border, emblem, multiple characters, other objects, text, watermark, gradient background, shadow, realistic, 3D render, cropped, cut off, close up, scenery, forest background, room, landscape, ground, floor, background decoration, humanoid, biped, human hands, clothing, armor, weapon, collar, standing upright, sitting, white fur, blue eyes, yellow eyes",
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
      "seed": 628402,
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
      "filename_prefix": "monsters_boss_wolf_lord_s2_refined_forest_production_sdxl_s628402_20261127T171547621676Z",
      "images": [
        "6",
        0
      ]
    }
  }
}
```

## Ghi chú nghiệm thu bắt buộc

Bộ này CHƯA đạt100% bảng thiết kế: cả hai Goblin vẫn sai dạng chùy gỗ có đinh; Slime s1 lá quá lớn; mũ Cung thủ chưa đúng nâu; rune/sẹo Boss cần duyệt. Có25lượt sinh SDXL gồm ứng viên bị loại để chọn10file cuối, không phải chỉ10request. Không đánh dấu là bộ production-ready và không tích hợp khi chưa được chủ dự án duyệt. Bảng thiết kế chuẩn do Muse lưu: [MONSTER_DESIGN_RUNG_XANH.md](../../docs/MONSTER_DESIGN_RUNG_XANH.md).
