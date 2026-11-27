# STEP_B_DOWNLOADS: danh sách file định tải cho Bước B

Trạng thái: **CHỜ ANH DO DUYỆT TỪNG FILE. Chưa tải file nào.**
Lập ngày 2026-11-28 (Claude, GAME-ART-CORE). Dung lượng và SHA-256 lấy từ API của nguồn công bố (Hugging Face LFS / Civitai), chỉ đọc metadata, không tải model.
Sau khi tải sẽ kiểm SHA-256 trước khi dùng. File nào không khớp thì xóa và báo lại.
Nơi đặt: `C:\AI\ComfyUI-Local\ComfyUI\models\<thư mục>` (chỉ thêm file, không sửa ComfyUI, không cần custom node). Ổ C còn khoảng 165 GB.

| # | Ưu tiên | File | Thư mục đích | Dung lượng | Giấy phép | Thương mại |
|---|---|---|---|---:|---|---|
| B1 | **Cần** | `animagine-xl-4.0-opt.safetensors` | `checkpoints` | 6,94 GB | CreativeML Open RAIL++-M | ✅ Được |
| B2 | **Cần** | `diffusion_pytorch_model.safetensors` → đổi tên `controlnet-openpose-sdxl-xinsir.safetensors` | `controlnet` | 2,50 GB | Apache-2.0 | ✅ Được |
| B3 | Tùy chọn | `gameicon_sdxl_v1.safetensors` (Game Icon Forge) | `loras` | 0,23 GB | Civitai: cho phép bán ảnh | ✅ Được |
| B4 | Không đề xuất | `game_icon_v1.0.safetensors` (Game icon) | `loras` | 2,79 GB | Civitai: cho phép bán ảnh | ✅ Được |

**Tổng đề xuất (B1 + B2 + B3): khoảng 9,67 GB.**

---

## B1. Animagine XL 4.0 Opt (checkpoint SDXL anime/chibi)
- **Trang chính thức:** https://huggingface.co/cagliostrolab/animagine-xl-4.0 (không gated; commit repo `2b7c1b39`)
- **URL tải:** https://huggingface.co/cagliostrolab/animagine-xl-4.0/resolve/main/animagine-xl-4.0-opt.safetensors
- **Dung lượng:** 6.938.350.040 bytes
- **SHA-256:** `6327eca98bfb6538dd7a4edce22484a1bbc57a8cff6b11d075d40da1afb847ac`
- **Giấy phép:** CreativeML Open RAIL++-M, giữ nguyên bản gốc của SDXL. Model card ghi rõ được dùng thương mại, chỉnh sửa, phân phối. Điều kiện: kèm bản giấy phép, ghi rõ thay đổi nếu phân phối lại model, tuân thủ danh sách cấm sử dụng (nội dung phạm pháp/gây hại). Ảnh sinh ra được dùng trong game bán thương mại.
- **Mở khóa:** nhân vật, quái và boss chibi-fantasy đồng bộ với hero hiện có (SDXL Base vẽ chibi kém); icon skill/trang bị; turnaround nhân vật. Đây là model chính của PROMPT_LIBRARY.
- **Ghi chú:** chọn bản **Opt** (2025-02-13), vì theo model card bản này ổn định hơn, giải phẫu và màu tốt hơn bản thường. Bản thường `animagine-xl-4.0.safetensors` (6.938.434.056 bytes, SHA-256 `1d5b43ff75b6ab598502d4c779d2fbfa3dceca51c60c3b609640a60772333916`) **không cần tải**. Trên RTX 2070S dự kiến khoảng 15 s/ảnh 1024² như SDXL Base (cùng kiến trúc).

## B2. ControlNet OpenPose SDXL (xinsir)
- **Trang chính thức:** https://huggingface.co/xinsir/controlnet-openpose-sdxl-1.0 (không gated; commit repo `23f966cd`)
- **URL tải:** https://huggingface.co/xinsir/controlnet-openpose-sdxl-1.0/resolve/main/diffusion_pytorch_model.safetensors
- **Dung lượng:** 2.502.139.104 bytes
- **SHA-256:** `b8524e557a7df60d081f5d4a0eb109967d107df217943bf88c2d99b9ebcc06c5`
- **Giấy phép:** Apache-2.0, dùng thương mại được.
- **Mở khóa:** khóa dáng nhân vật theo xương OpenPose do script tự vẽ: các khung chính đánh thường, 4 skill, trúng đòn, tử vong; giữ dáng nhất quán giữa các nhân vật cùng phái. Chạy bằng node ControlNet có sẵn trong ComfyUI, **không cần custom node** (không dùng bộ tiền xử lý DWPose).
- **Ghi chú:** repo có thêm `diffusion_pytorch_model_twins.safetensors` (cùng dung lượng, SHA-256 `54a2afb1…12fa4`). **Không tải**, chỉ cần một bản.

## B3. Game Icon Forge LoRA (tùy chọn)
- **Trang chính thức:** https://civitai.com/models/2750041
- **URL tải:** https://civitai.com/api/download/models/3093666?fileId=2973208
- **Dung lượng:** 230.822 KB (khoảng 0,23 GB)
- **SHA-256 (Civitai công bố):** `CEB19401F06DCEE8E7FFCCB37AE6756904D1E794200AA62271B58DDCD5D6D646`
- **Giấy phép:** theo trang Civitai: được dùng ảnh thương mại, bán ảnh, phái sinh, không bắt buộc ghi công (`allowCommercialUse: Image, Rent, Sell…`). Bản gốc thuộc RAIL++-M addendum. **Cần anh Do xem trang trước khi duyệt**, vì điều khoản Civitai có thể được tác giả đổi.
- **Mở khóa:** icon vật phẩm fantasy RPG (vũ khí theo bậc, giáp, bình, ngọc) đồng bộ phong cách. Trigger `gicon`.
- **Ghi chú:** có thể chưa cần. Đề xuất thử icon bằng Animagine trước; chỉ tải nếu icon chưa đạt.

## B4. Game icon LoRA (không đề xuất)
- Trang: https://civitai.com/models/141066 · `game_icon_v1.0.safetensors` · 2.724.525 KB (**khoảng 2,79 GB**, quá lớn so với một LoRA thông thường) · SHA-256 `9E39A540E97173442ABBB319437080E4DC5A48087F43ED94C53BAFEF75E2E903` · thương mại: được (theo Civitai).
- Lý do không đề xuất: nặng gấp khoảng 12 lần B3 mà làm cùng một việc; bản năm 2023, cũ hơn.

---

## Anh Do duyệt
| File | Duyệt? |
|---|---|
| B1 Animagine XL 4.0 Opt (6,94 GB) | ☐ |
| B2 ControlNet OpenPose SDXL xinsir (2,50 GB) | ☐ |
| B3 Game Icon Forge LoRA (0,23 GB) | ☐ |
| B4 Game icon LoRA (2,79 GB) | ☐ (không đề xuất) |

Phần quái Rừng Xanh của Bước B vẫn **tạm hoãn** theo ART_PRODUCTION_PLAN, cho tới khi Luna đánh giá xong lô mẫu SDXL của Codex.
