# REPORT: Tile cỏ Rừng Xanh v2

GAME-ART-CORE (Claude) · 2026-11-28 · SDXL Base có sẵn, cùng quy trình seamless như v1: dịch nửa chu kỳ, inpaint dải chữ thập bằng `SetLatentNoiseMask`, trộn mềm. Cộng thêm một bước hậu kỳ **an toàn với liền mạch**: mọi bộ lọc dùng `mode='wrap'`.

## Cách làm
- **Prompt**: `soft painted grass, muted olive green, low contrast, broad flat grass patches, short sparse grass strokes, a few tiny scattered flowers, stylized hand painted rpg map ground, flat even lighting`.
- **Negative**: `dense flowers, flower carpet, pink flowers, long grass blades, realistic, photo, high detail, high contrast, saturated…`.
- **Hậu kỳ**:
  - san phẳng mảng sáng tối tần số thấp (chỉ giữ 35 % biến thiên ở thang trên 90 px), vì chính các mảng này làm lộ nhịp lặp;
  - giảm tương phản chi tiết còn 80 %;
  - giảm bão hòa còn 80 %.
- 3 seed ứng viên (729001–729003), **chọn 729003** (inpaint 729503) vì ít lộ nhịp lặp nhất khi ghép 3×3.

## QC
| Chỉ số | v1 | **v2 (729003)** | Ghi chú |
|---|---:|---:|---|
| Seam ngang / dọc (chênh ở mép nối ÷ chênh trung bình giữa 2 cột/hàng bên trong) | 1,12 / 1,40 | **1,33 / 1,02** | Xấp xỉ 1 là liền; soi phóng to góc nối 4 tile không thấy đường nối |
| Bão hòa trung bình | 0,76 | **0,44** | |
| Độ lệch chuẩn độ sáng (tương phản) | 32,8 | **3,4** | |
| Độ lệch chuẩn độ sáng tần số thấp (mảng lộ nhịp lặp) | 3,04 | **0,24** | |
| Pixel hồng/đỏ (hoa hồng) | 5,3 % | **0 %** | |
| Màu trung bình RGB | 53 / 104 / 32 | 115 / 119 / 67 | Xanh ô liu trầm |

v1 được đo lại bằng cùng công thức nên số seam khác số trong REPORT v1.

## Ảnh để duyệt
- `scene_test_v2_1280x720.jpg`: cùng bộ 6 vật thể và Kiếm Sĩ Nam cao 150 px, tile hiển thị ở cỡ 384 px như v1.
- `tile_v2_2x2.jpg`, `tile_v2_3x3.jpg`: kiểm seam và nhịp lặp.
- `candidates/`: 3 ứng viên (scene + ảnh gốc), lưới 3×3 để so nhịp lặp.

## Tự đánh giá theo tiêu chí của Luna
- **Nền trầm, hero là điểm đọc đầu tiên: ĐẠT.** Trong scene, hero và vật thể nổi rõ trên nền.
- **Không thấy seam: ĐẠT.**
- **Không nhận rõ nhịp lặp: ĐẠT ở lưới 3×3.** Bản 729002 có hoa trắng nên lộ nhịp, vì vậy không chọn.
- **Rủi ro**:
  - Tile hơi **phẳng và ngả vàng ô liu**. Nếu Luna muốn xanh hơn hoặc thêm vân, chỉ cần chỉnh 2 tham số hậu kỳ (`FLATTEN_KEEP`, `SAT`), không cần sinh lại.
  - Hoa gần như không thấy ở cỡ 384 px; phần hoa giao cho **khóm hoa v2** (vật thể riêng) sau khi tile được chốt.

## Tái tạo
`../tools/gen_tile_v2.py`; tham số và thời gian ở `generation.json`. Mỗi ứng viên: txt2img khoảng 20 s, inpaint seam khoảng 20 s, hậu kỳ dưới 2 s.
