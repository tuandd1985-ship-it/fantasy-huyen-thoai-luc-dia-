# Pilot LoRA nhân vật: Pháp Sư Nam (`pspnam`)

GAME-ART-CORE (Claude), 2026-11-28. Thử nghiệm, **chưa dùng cho sản phẩm**. Không sửa source game.

## Đã làm
- **Công cụ**: kohya **sd-scripts** (Apache-2.0, commit 88ff6b5) trong môi trường riêng `C:\AI\GAME-ART-CORE\.venv-train`.
  - Dùng chung torch 2.14 của ComfyUI ở chế độ chỉ đọc; không cài gì vào ComfyUI.
  - Node `TrainLoraNode` có sẵn của ComfyUI đã thử trước: hết VRAM (cần khoảng 15 GB), ra loss NaN ở fp16 và không có bf16 trên card Turing, nên bỏ.
- **Dữ liệu**: 22 ảnh trên nền trắng 1024², xem `dataset_22.jpg`; caption ở `lora_dataset_captions.json`, từ khoá `pspnam`.
  - 2 ảnh tham chiếu sạch (thêm bản lật);
  - 8 khung v1 (cùng một lớp gậy);
  - 12 khung v2 (IP-Adapter).
- **Thiết lập cho card 8 GB** (`tools/train_lora_kohya.sh`):
  - SDXL Animagine XL 4.0, chỉ huấn luyện UNet, LoRA dim 16 / alpha 8;
  - AdamW8bit, lr 1e-4 cosine, fp16;
  - lưu sẵn latent và text encoder, gradient checkpointing, 1024 px.
- **Kết quả huấn luyện**: 1600 bước × 1,75 s = **khoảng 47 phút**, VRAM vừa đủ 8 GB, loss cuối 0,050.
  - File `pspnam_v1.safetensors` (85 MB, SHA-256 `05b95615…`) nằm ở `ComfyUI/models/loras/`, kèm các mốc 400/800/1200 bước. Không đẩy lên repo.

## So sánh (cùng khung xương OpenPose, cùng seed 742001)
Mỗi ảnh có 3 hàng: **cũ (IP-Adapter 0,6)** / **chỉ LoRA** / **LoRA + IP-Adapter nhẹ 0,35**.
- `ab_768x1024_strength080.jpg`: LoRA 0,8, khung dọc 768×1024.
- `ab_768x1024_strength055.jpg`, `ab_768x1024_step800_strength070.jpg`: mức nhẹ hơn và bản lưu ở mốc 800 bước.
- `ab_1024x1024_strength070.jpg`: khung vuông khớp lúc huấn luyện.

## Kết luận
- **Được**: danh tính giữ rất đều (râu bạc, mũ rộng viền vàng, áo xanh), nhất là **gậy gỗ xoắn đầu móc**. Gậy giờ giống nhau giữa các ảnh hơn hẳn cách cũ.
- **Chưa được**:
  1. Dáng bám khung xương kém hơn cách cũ. LoRA kéo về dáng đứng, vì 10/22 ảnh trong bộ dữ liệu là dáng đứng.
  2. Ở khung dọc 768×1024 nhân vật bị phóng to và cắt khung, nền ra màu xanh. Sinh trên khung vuông 1024 thì nền trắng, đủ người.
  3. Quả cầu xanh trên gậy lúc có lúc không.
- **Tốt nhất hiện tại**: **LoRA 0,7 + IP-Adapter 0,35 trên khung vuông 1024** (hàng 3 của `ab_1024x1024_strength070.jpg`): nền trắng, đủ người, mặt và gậy đều, dáng ở mức trung bình.

## Đề xuất bước tiếp (LoRA v2)
Dùng chính LoRA v1 + IP-Adapter để sinh thêm khoảng 30 ảnh dáng động (chạy, tung phép, skill), chọn ảnh đúng gậy có cầu. Sau đó huấn luyện lại với bộ dữ liệu cân bằng dáng (đứng ≤ 25 %), dự kiến khoảng 1 giờ. Khi LoRA đủ tốt, mỗi nhân vật mới chỉ mất khoảng 5 phút chuẩn bị ảnh + khoảng 47 phút máy tự huấn luyện.
