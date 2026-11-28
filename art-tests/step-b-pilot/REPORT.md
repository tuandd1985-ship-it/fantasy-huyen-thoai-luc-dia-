# REPORT: Pilot Bước B — Animagine XL 4.0 + ControlNet OpenPose SDXL (xinsir)

GAME-ART-CORE (Claude) · 2026-11-28 · Pilot nhỏ, chưa sản xuất hàng loạt. Chỉ dùng node gốc ComfyUI.

## 1. Model đã tải (anh Do duyệt B1 + B2; B3 hoãn, B4 không tải)
| ID | File | Dung lượng (byte) | SHA-256 kỳ vọng = thực tế | Giấy phép | Vị trí |
|---|---|---:|---|---|---|
| B1 | `animagine-xl-4.0-opt.safetensors` | 6 938 350 040 | `6327eca9…b847ac` **KHỚP** | CreativeML Open RAIL++-M | `ComfyUI/models/checkpoints/` |
| B2 | `controlnet-openpose-sdxl-xinsir.safetensors` (tên gốc `diffusion_pytorch_model.safetensors`) | 2 502 139 104 | `b8524e55…cc06c5` **KHỚP** | Apache-2.0 | `ComfyUI/models/controlnet/` |

- Tải vào thư mục tạm riêng, kiểm hash xong mới chuyển vào ComfyUI. Không đổi cấu hình ComfyUI, không cài custom node.
- Metadata (`models_installed.json`) và bản giấy phép lưu ở `C:\AI\GAME-ART-CORE\models\` (`MODELS.json`, `licenses/`).

## 2. Thiết lập pilot
- Cùng prompt, cùng seed 730001, cùng sampler cho cả hai model: `euler_ancestral`, 28 bước, CFG 5 (thiết lập khuyến nghị của Animagine 4.0). ControlNet strength 1,0, áp dụng 0–100 %.
- Xương OpenPose vẽ bằng script theo **hàm vẽ khuyến nghị của xinsir**: nét dày `stickwidth 4 × ratio 3 = 12 px`, chấm khớp bán kính 12 px ở khung 1024. Tỉ lệ xương là **chibi**: đầu to, tay chân ngắn.
- Nhân vật: Kiếm Sĩ Nam (tóc xanh nhạt, mũ sắt chùm lông đỏ, giáp bạc, áo choàng đỏ).

## 3. Kết quả

### Ảnh để duyệt
- `pilot_poses_compare.jpg`: 3 dáng × (xương | Animagine | SDXL Base).
- `pilot_turnaround_compare.jpg`: turnaround **không** khóa dáng (chỉ dùng prompt).
- `pilot_turnaround_v2_compare.jpg`: turnaround **khóa bằng xương OpenPose 3 góc** (trước, nghiêng, sau).
- Ảnh gốc ở `images/`.

### Dáng nào giữ được, dáng nào hỏng (tỉ lệ chibi, nhìn hơi từ trên)
| Dáng | Animagine + OpenPose | SDXL Base + OpenPose |
|---|---|---|
| a) đứng, hướng xuống | **Giữ tốt**: đúng dáng, đúng tỉ lệ chibi | Giữ được dáng; tỉ lệ chibi đạt |
| b) skill giơ kiếm qua đầu | **Giữ tốt**: hai tay giơ kiếm thẳng, chân dạng rộng đúng xương | **Hỏng**: bỏ qua tay giơ, kiếm cầm ngang |
| c) trúng đòn, dang tay ngả sau | **Giữ một phần**: tay dang và ngả sau đúng, nhưng thành dáng nhảy lên, kiếm cầm ngang, nền xanh nhạt | **Hỏng**: tự thêm khiên, tay không theo xương |
| Turnaround chỉ dùng prompt | **Hỏng**: ra hiệp sĩ người lớn, thiếu góc nghiêng, đầu chibi rời bên cạnh | **Hỏng**: người lớn, bố cục lộn xộn |
| Turnaround khóa OpenPose 3 góc | **Đạt bố cục**: đủ trước, nghiêng, sau, đúng chibi và cùng một bộ đồ | Đúng 3 góc nhưng lệch phong cách, cắt đầu, có thêm 1 hình nhỏ |

### Kết luận
1. **Animagine + OpenPose dày nét là cặp dùng được** cho chibi 2.5D. Dáng đứng và dáng skill biên độ lớn bám xương tốt. Turnaround **bắt buộc khóa bằng xương 3 góc**; chỉ dùng prompt thì không ra chibi.
2. **SDXL Base không nên dùng cho nhân vật**: hay bỏ qua xương ở dáng biên độ lớn và hay tự thêm đạo cụ.
3. **Vấn đề còn tồn tại**
   - **Danh tính chưa khớp hero trong game.** Animagine hiểu "knight" là mũ kín mặt, nên mặt bị che kể cả khi đã ghi "open-face helmet, visible face". Muốn khớp mặt và tóc của hero hiện có, cần thêm tham chiếu ảnh (IP-Adapter hoặc LoRA nhân vật). Cả hai đều chưa có, và đây là quyết định của Luna/anh Do. Trước mắt có thể thử bỏ mũ khỏi prompt.
   - **Màu nền chưa ổn định.** Animagine hay ra nền xanh nhạt thay vì xám nhạt. Không ảnh hưởng tách nền (BiRefNet), nhưng nên ghi màu nền cụ thể hơn.
   - **Dáng trúng đòn** cần xương có trọng tâm ngả rõ hơn và chân chạm đất; tag `hurt` dễ kéo thành dáng nhảy.
   - **Góc nhìn 2.5D từ trên** mới chỉ đạt "hơi từ trên". Muốn đúng góc của game cần xương vẽ phối cảnh nhìn xuống (vai và hông dẹt hơn, đầu che một phần cổ).

## 4. Thời gian và VRAM thực tế (RTX 2070 Super 8 GB)
| Việc | Thời gian / ảnh | VRAM đỉnh (toàn GPU) |
|---|---:|---:|
| Turnaround 1344×768, không ControlNet | 25,6 s | 7,37 GB |
| 1 dáng 1024², Animagine + ControlNet | 30–32 s | 7,33–7,93 GB |
| 1 dáng 1024², Base + ControlNet | 30 s | 7,33–7,39 GB |
| Turnaround 1344×768 + ControlNet | 30 s | 7,84–7,90 GB |

- VRAM đo bằng `nvidia-smi` cho **toàn GPU**, gồm khoảng 4,6 GB đang dùng sẵn trước khi chạy (màn hình và ComfyUI giữ model).
- ControlNet chạy được trong 8 GB, không lỗi hết bộ nhớ. ComfyUI tự đẩy bớt model sang RAM, nên lần đổi checkpoint đầu chậm hơn một chút.

## 5. Tái tạo
`tools/pilot_animagine_openpose.py` và `tools/pilot_turnaround_v2.py`. Prompt, seed và thời gian ở `pilot_log.json` và `pilot_turnaround_v2_log.json`.
