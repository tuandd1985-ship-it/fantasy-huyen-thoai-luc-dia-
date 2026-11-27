# REPORT: Bước A, sprite-matte-clean + art-qc cho 6 hero (k2–k7)

GAME-ART-CORE (Claude) · 2026-11-28 · Căn cứ: `docs/art/ART_PRODUCTION_PLAN.md` mục 4 (quy trình) và mục 7 (ngưỡng QC).
Bản này **thay thế** lượt thử A1 (`art-tests/hero-edge-clean/`). A1 chỉ khử màu viền; lượt này thêm BiRefNet, làm đặc lõi alpha, xử lý chi tiết mảnh và chấm điểm theo ngưỡng.

## Kết luận nhanh
- **Bản WebP lossless (đề xuất đưa vào game): 6/6 đạt chỉ số ám màu viền** (0,16–2,58 %, ngưỡng < 3 %). **5/6 đạt toàn bộ ngưỡng mục 7.** Cung Thủ Nữ trượt 1 chỉ số "ΔE sắc độ viền" (12,73 > 12), lý do ở mục "Chưa đạt".
- **Bản WebP q90 (nhỏ như bản gốc): chỉ 1/6 đạt toàn bộ.** Nén mất dữ liệu làm sắc hồng quay lại ở chi tiết mảnh (ám màu viền 2,0–6,7 %).
- Ruột nhân vật giữ nguyên tuyệt đối: 0 pixel đổi màu ở vùng lõi (đo trên bản lossless). Hình dáng, đường chân và độ nét không đổi.
- Không tải model mới, không cài gì, không cài custom node, không sửa source game. Chạy CPU, 6 ảnh hết 8,3 phút (BiRefNet khoảng 45 s mỗi ảnh). File `birefnet-general.onnx` có sẵn, đã kiểm tra không bị thay đổi.

## Quy trình (sprite-matte-clean)
1. **BiRefNet** (model có sẵn ở `C:\AI\ComfyUI-Local\models\rembg`, chạy CPU) trên sprite đặt lên nền xám trung tính. Dùng để **quyết định lấp lỗ**: chỉ lấp vùng kín bên trong khi BiRefNet xác nhận đó là nhân vật, nên khe hở thật (giữa dây cung và thân cung) được giữ. Độ trùng giữa mask BiRefNet và alpha hiện tại: IoU 0,997–0,999.
2. Xóa đốm quầng magenta tách rời (alpha ≤ 16, nhỏ hơn 50 px): 441–591 đốm mỗi ảnh.
3. **Làm đặc lõi**: mọi pixel sâu hơn dải viền 2,5 px có alpha 255; alpha mềm chỉ giữ ở dải viền. Có 118–285 pixel lõi bán trong suốt được làm đặc; lấp 15–78 pixel lỗ ở 3 ảnh.
4. **Khử màu viền** (chỉ trên dải viền và chi tiết mảnh dày ≤ 6 px như dây cung, đầu trượng):
   - (a) khử ánh magenta so với màu tham chiếu cục bộ, giữ độ sáng;
   - (b) pixel còn sắc hồng/tím/đỏ-hồng mà vùng xung quanh không có màu đó thì giữ độ sáng L* và lấy sắc độ của màu tham chiếu.
   - Phần vốn tím hoặc đỏ (tóc và trượng Pháp Sư Nữ, áo choàng và chùm lông Kiếm Sĩ) được bảo vệ, vì màu tham chiếu của chúng cũng tím/đỏ.

## Kết quả art-qc (ngưỡng mục 7). Đo trên file WebP lossless sau khi giải nén; ám màu q90 ghi trong ngoặc

| Hero | Lõi đặc % (≥ 99) | Lỗ lõi (0) | Đảo rời (0) | Đốm quầng | Chạm mép khung | Ám màu viền % (< 3) | ΔE sắc độ viền (< 12) | ΔE palette (< 8) | Đổi dáng % / chân px (≤ 4 / ≤ 2) | Độ nét (≥ 0,98) | Pixel lõi đổi màu | KB gốc / lossless / q90 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Kiếm Sĩ Nam | 99,93 → 100 | 0 → 0 | 0 → 0 | 480 → 0 | không | 81,6 → **0,16** (q90: 2,01) | 24,5 → 0,5 | 0,39 | 0 / 0 | 1,000 | 0 | 90 / 263 / 79 |
| Kiếm Sĩ Nữ | 99,90 → 100 | 1 → 0 | 0 → 0 | 578 → 0 | không | 84,1 → **2,58** (q90: 6,60) | 21,9 → 6,2 | 0,24 | 0 / 0 | 1,000 | 0 | 97 / 282 / 85 |
| Pháp Sư Nam | 99,92 → 100 | 0 → 0 | 0 → 0 | 591 → 0 | không | 75,4 → **0,91** (q90: 4,40) | 18,6 → 9,3 | 0,61 | 0 / 0 | 1,001 | 0 | 87 / 270 / 76 |
| Pháp Sư Nữ | 99,93 → 100 | 0 → 0 | 0 → 0 | 544 → 0 | không | 52,6 → **0,63** (q90: 3,05) | 12,8 → 6,3 | 0,08 | 0 / 0 | 1,000 | 0 | 99 / 307 / 88 |
| Cung Thủ Nam | 99,86 → 99,999 | 0 → 0 | 0 → 0 | 486 → 0 | không | 85,4 → **0,78** (q90: 6,66) | 28,8 → 10,4 | 0,44 | 0 / 0 | 1,001 | 0 | 98 / 297 / 85 |
| Cung Thủ Nữ | 99,88 → 100 | 1 → 0 | 0 → 0 | 441 → 0 | không | 82,4 → **1,01** (q90: 5,14) | 30,8 → **12,7 ✗** | 0,77 | 0 / 0 | 1,002 | 0 | 91 / 286 / 80 |

Định nghĩa "ám màu viền": tỉ lệ pixel trong dải viền còn ánh magenta vượt mức cho phép, **hoặc** có sắc hồng/tím/đỏ-hồng nhìn thấy được (Lab C* ≥ 10) trong khi vùng xung quanh không có màu đó. Ngưỡng C* ≥ 10 được thêm sau khi kiểm tra bằng mắt cho thấy pixel gần đen (độ sáng khoảng 30/255) cho ra sắc độ ngẫu nhiên, mắt không thấy hồng. Toàn bộ số đo chi tiết, kể cả từng chỉ số con, nằm trong `qc.json`.

## Đã đạt
- Hết quầng và viền tím/hồng quanh giáp, lưỡi kiếm, áo choàng, ống tên, thân cung trên cả 4 nền (đen, trắng, cỏ map, trong suốt). Xem `before_after/`.
- **Dây cung Cung Thủ Nữ** trước đây màu hồng; nay thành be/nâu nhạt, khớp chân dung gốc k12 (vẽ không qua tách nền).
- Lõi alpha đặc 100 %; hết lỗ bán trong suốt bên trong nhân vật.
- Màu, dáng và độ nét giữ nguyên: ΔE palette ≤ 0,8, đổi dáng 0 %, độ nét bằng hoặc hơn bản gốc.

## Chưa đạt / vấn đề còn tồn tại
1. **Cung Thủ Nữ: ΔE sắc độ viền 12,73 > 12.** Chỉ số này so màu outline với màu **phần tô bên trong**. Outline nâu đậm của Cung Thủ vốn khác xa áo choàng xanh lá theo thiết kế, nên chỉ số cao dù hết ám tím. Bằng mắt viền đạt. Đề nghị Luna chọn: (a) chấp nhận và đổi chỉ số này thành "so với outline tham chiếu"; hoặc (b) giữ ngưỡng và coi là chưa đạt.
2. **WebP q90 làm sắc hồng quay lại** ở chi tiết mảnh (nén mất dữ liệu trộn màu theo khối 2×2). Có 5/6 ảnh vượt ngưỡng ám màu. Đề xuất dùng **WebP lossless** (tổng 6 ảnh khoảng 1,7 MB thay cho khoảng 0,55 MB, tức tăng khoảng 1,1 MB). Bản q90 vẫn kèm theo nếu cần nhẹ.
3. Một đoạn dây cung của Cung Thủ hơi ngả xanh, do lấy màu tham chiếu từ áo choàng xanh gần đó. Chỉ thấy khi phóng to.
4. Outline ở mép một số chỗ thành nâu-xám trung tính thay vì nâu ấm như outline bên trong. Chỉ thấy khi phóng to ×3.
5. Nền "cỏ map" là ô cỏ cắt từ ảnh chụp game và lặp lại, nên có đường nối ô mờ. Đó là nền thử, không phải lỗi sprite.
6. **Chưa đạt chuẩn khung** ở GAME_ART_REVIEW mục 5 (khung 512×512, chân ở y = 480): ảnh giữ nguyên kích thước gốc 501–572×640, vì đổi khung không thuộc phạm vi bước A.
7. Chưa tích hợp vào game, chưa thử trên iPhone (việc của Luna/Codex sau khi duyệt). Dải chuyển động k13–k18 không xử lý.

## Thư mục
| Đường dẫn | Nội dung |
|---|---|
| `before_after/hero-*_truoc_sau.jpg` | 6 ảnh trước/sau trên 4 nền + phóng ×3 một đoạn viền (JPEG 4:4:4, không thêm viền màu do nén) |
| `qc.json` | Ngưỡng, tham số, số đo trước/sau cho cả lossless và q90, đạt/trượt từng chỉ số, SHA-256 |
| `original/` | 6 WebP gốc, trích nguyên byte từ `assets-data-1.js` |
| `cleaned/hero-*_lossless.webp` | **Bản đề xuất** |
| `cleaned/hero-*.webp` | Bản q90 (nhẹ) |
| `tools/` | `gac_matte.py` (matte-clean + art-qc), `run_hero_matte_clean.py`, ô nền cỏ `grass_tile.png` |

Chạy lại: `python tools/run_hero_matte_clean.py <thư mục k2..k7.webp> <out> tools/grass_tile.png` (cần numpy, Pillow, scipy, rembg + model BiRefNet có sẵn).
