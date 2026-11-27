# Báo cáo cài đặt ComfyUI local

Cài tại `C:\AI\ComfyUI-Local`. Ổ C là SSD SanDisk Ultra II 480GB; K là USB HDD Buffalo HD-PNFU3 (đối chiếu trang hãng).

Python 3.13.17 riêng + .venv; ComfyUI 0.46.0; frontend 1.59.15; PyTorch 2.14.1+cu130; torchvision 0.29.1+cu130.

Commit ComfyUI: `7c78b5641ab2d6cb7f7766a183a8a43a59de0a8b`.

Driver NVIDIA 610.88, hỗ trợ CUDA driver 13.3; PyTorch dùng CUDA runtime 13.0. Đã xác nhận sm_75 và phép nhân ma trận FP16 trên cuda:0 RTX 2070 SUPER. Không cài CUDA Toolkit riêng, không đổi driver/PATH, không sửa môi trường Codex/Claude Code hoặc dự án SANEI. Python embedded có sẵn thiếu venv nên đã dùng Python đầy đủ riêng có chữ ký Python Software Foundation hợp lệ.

## Model và cấu hình

Chỉ SDXL Base 1.0 chính thức, 6.938.078.334 bytes (~6,46 GiB). SHA-256 đã khớp nguồn chính thức: `31e35c80fc4829d14f90153f4c74cd59c90b779f6afe05a74cd6120b893f7e5b`. Giấy phép CreativeML Open RAIL++-M; bản gốc và model card ở licenses/. Không cài refiner, LoRA, Manager hay custom node. Các package comfy-kitchen/comfy-aimdo/templates là dependency chính thức của ComfyUI.

1024×1024, batch 1, 25 steps, Euler/normal, CFG 6.5; UNet và text encoder FP16, VAE FP32 tránh lỗi VAE FP16 của SDXL; PyTorch attention, async offload và quản lý bộ nhớ tự động. Đặt reserve-vram 1GB, tắt preview; giá trị này không phải giới hạn VRAM cứng. Chưa gặp CUDA OOM trong các lượt thử.

## Kết quả mẫu bàn giao

| Loại | API hoàn thành (s) | VRAM GPU max (GiB) | RAM ComfyUI max (GiB) | GPU max (°C) |
|---|---:|---:|---:|---:|
| heroes | 15.69 | 7.24 | 8.74 | 65 |
| monsters | 15.25 | 7.30 | 8.37 | 66 |
| icons | 15.29 | 7.37 | 8.47 | 67 |
| backgrounds | 15.65 | 7.30 | 8.46 | 66 |

Đo chu kỳ 1 giây: VRAM là tổng toàn GPU gồm desktop/ứng dụng khác; RAM là working set cây tiến trình ComfyUI, không phải private committed bytes. Thời gian gồm request, queue, nạp model và sinh/lưu PNG server; không gồm tải ảnh về hoặc tách nền. Những mẫu này dùng model đã nạp; lượt đầu tiên là 19,70 giây. Mọi lượt thử và sample đo chi tiết được giữ trong metadata/.

Có 8 lượt sinh trong quá trình thử/chỉnh prompt. Bản đầu chưa tuân thủ nền magenta; giữ nguyên raw và metadata để đối chiếu. ACCEPTANCE-PREVIEW.png chỉ dùng bốn mẫu mới nhất theo loại.

## API và script

API chỉ bind 127.0.0.1:8188, đã xác nhận socket đang LISTEN. /system_stats, /object_info, POST /prompt, /history/{id}, /view đã được kiểm tra bằng các lượt sinh ảnh thật. Không mở API ra LAN/Internet, không chỉnh firewall. START-COMFYUI.cmd và STOP-COMFYUI.cmd quản lý đúng tiến trình riêng; kiểm tra dừng/khởi động lại được ghi trong lifecycle-check.json.

Workflow giao diện: workflows/game_asset_basic.json. Workflow API: workflows/game_asset_basic_api.json. Các link node được kiểm tra cấu trúc; chưa kiểm tra thao tác mở trong giao diện vì công cụ trình duyệt từ chối quyền truy cập local. Người dùng cần mở workflow khi nghiệm thu.

## Pipeline tài nguyên

scripts/generate_asset.py gửi prompt, chờ history, lấy ảnh, key nền magenta nối mép theo màu thực tế, xử lý alpha và viền, lưu raw/processed/category và JSON đầy đủ. Backgrounds bỏ qua key. Thư mục heroes, monsters, weapons, icons, backgrounds, animations đã tạo. Chưa tạo animation, chưa tích hợp vào source game.

Keying là thuật toán màu, không phải segmentation; không đảm bảo tóc/glow/chi tiết màu tím hoàn hảo. Cần nghiệm thu art và viền trên nền sáng/tối. Kết quả QA từng mẫu:

- heroes: `{"method": "adaptive border-connected magenta key, alpha uncompositing, one-pixel rim despill", "estimated_background_rgb": [182.0, 67.0, 130.0], "background_is_magenta": true, "transparent_pixels": 786025, "transparent_fraction": 0.7496118545532227, "partial_alpha_pixels": 11365, "remaining_opaque_magenta_pixels": 0, "needs_visual_review": true}`
- monsters: `{"method": "adaptive border-connected magenta key, alpha uncompositing, one-pixel rim despill", "estimated_background_rgb": [185.0, 23.0, 121.0], "background_is_magenta": true, "transparent_pixels": 663370, "transparent_fraction": 0.6326389312744141, "partial_alpha_pixels": 4088, "remaining_opaque_magenta_pixels": 0, "needs_visual_review": true}`
- icons: `{"method": "adaptive border-connected magenta key, alpha uncompositing, one-pixel rim despill", "estimated_background_rgb": [143.0, 15.0, 104.0], "background_is_magenta": true, "transparent_pixels": 854846, "transparent_fraction": 0.8152446746826172, "partial_alpha_pixels": 3613, "remaining_opaque_magenta_pixels": 0, "needs_visual_review": true}`
- backgrounds: `{"background_removal": false, "needs_visual_review": true}`

Dung lượng thư mục hiện tại: 11.14 GiB; ổ C còn 166.63 GiB. Bao gồm Python riêng, .venv, dependency, model, log, workflow và ảnh thử.

Hướng dẫn Codex/Claude Code: GAME_ASSET_PIPELINE.md. Phiên bản đầy đủ: requirements-lock.txt, installation-manifest.json. Ảnh preview: ACCEPTANCE-PREVIEW.png. Dừng mọi phát triển thêm để người dùng nghiệm thu.

Nguồn: https://github.com/comfyanonymous/ComfyUI ; https://pytorch.org/get-started/previous-versions/ ; https://huggingface.co/stabilityai/stable-diffusion-xl-base-1.0 ; https://www.buffalo.jp/product/series/HD-PNFU3
