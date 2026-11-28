# Công cụ lắp ghép animation từ bộ phận (chờ bộ phận Kiếm Sĩ Nam của Codex)

GAME-ART-CORE (Claude), 2026-11-28. Vai trò mới: **chỉ lắp ghép** bộ phận Codex đã tách, **xoay và dịch quanh điểm trục**. Không vẽ thêm dáng, không dùng AI vẽ lại.

Trạng thái: thư mục `art-tests/parts/kiemsi-nam/` **chưa có trên main**. Công cụ đã sẵn; bộ phận lên là chạy được ngay (khoảng 7 giây cho 3 chuyển động).

## `parts_rig.py`
```
python parts_rig.py <thư mục bộ phận> motions_kiemsi.json <out>
```
1. **Kiểm tra ghép chồng**: xếp các bộ phận theo `parts.json`, so với `assembled.png` → độ trùng alpha (IoU), lệch khung bao (px), chênh màu, số px lệch alpha. Xuất `overlay_check.png`: đỏ = chỉ có ở assembled, xanh dương = chỉ có ở bản ghép, xanh lá = trùng.
2. **Cây khớp (FK)**: mỗi bộ phận xoay quanh điểm trục của nó, rồi theo bộ phận cha. Nội suy mượt giữa các khung khoá (`motions_*.json`: góc theo độ cho từng bộ phận, dịch gốc `root`).
3. **Xuất đúng chuẩn**: ô 768×640, chân y = 620, `animations.json` (durations_ms, hit_frame, loop, QC từng ô), GIF xem trước có vạch chân và chữ HIT.

## Định dạng `parts.json` công cụ đọc được (đề nghị Codex theo mẫu này)
Xem `dryrun/parts.example.json`. Công cụ tự nhận các tên trường hay gặp:
- danh sách `parts` (mảng hoặc object);
- mỗi phần có `name`/`id`, `file`/`image`;
- vị trí góc trên trái của ảnh trong khung assembled: `x`,`y` / `pos` / `offset`;
- điểm trục: `pivot` / `anchor` / `joint` (mặc định toạ độ khung assembled; thêm `"pivot_space": "local"` nếu tính theo ảnh bộ phận);
- `parent`;
- thứ tự vẽ `z` / `order`.

Nên có các bộ phận: thân/hông, đầu, tay trên + cẳng tay (hoặc cả tay) mỗi bên, đùi + cẳng chân mỗi bên, áo choàng, vũ khí (tách khỏi bàn tay nếu muốn xoay riêng). **Phần khớp nên vẽ chồng ra một chút** dưới bộ phận kề bên để khi xoay không hở.

## Chạy thử (`dryrun/`)
- Dùng các lớp Kiếm Sĩ tự cắt từ đợt AUTO-ANIM (không phải bộ phận Codex) chỉ để kiểm tra công cụ.
- Ghép chồng: **IoU 0,998, lệch khung 0 px, chênh màu 0,03/255** (386 px lệch là vùng lấp dưới khớp).
- 3 chuyển động mẫu:

| Chuyển động | Khung | durations_ms | hit_frame |
|---|---:|---|---:|
| idle | 2 | 600, 600 | – |
| run | 6 | 6 × 90 | – |
| tram_kiem | 7 | 60, 90, 90, 50, 110, 120, 90 | 4 |

- QC: mép ô alpha 0 %, chân y 620–623.
- Chạy mất khoảng 7 giây.
