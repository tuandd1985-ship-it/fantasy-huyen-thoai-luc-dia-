# Vật cản cho 9 map cũ (bộ ảnh Desktop đợt trước): cho Muse đưa vào game

GAME-ART-CORE (Claude), 2026-11-28. Không sửa source game.

- **Ảnh game** đã có sẵn ở `../upscaled-x2/<map>_x2.webp`: 2804×2244, Upscayl 4× + chỉnh màu (xem README thư mục đó).
- **Lưới vật cản**: `maps_collision.json`, **100×80 ô, đúng cỡ và định dạng `FOREST_GRID_RLE`** của Rừng Xanh đang chạy. Mỗi ô khoảng 28×28 px; hàng 0 ở trên cùng; mỗi dòng liệt kê các khoảng cột bị chặn (`a-b` hoặc `a`). Muse dùng nguyên hàm giải mã đang có (`new Uint8Array(100 * 80)`).
- `zones`: safe / elite / boss / portal, toạ độ chuẩn hoá 0–1, `r` theo bề ngang.
- Kiểm tra bằng mắt: `debug/<map>_collision.jpg` (đỏ = chặn, vòng xanh lá = safe, vàng = elite, tím = boss, xanh dương = portal), tổng hợp ở `debug/all_collision.jpg`.

| Map | Tên | Ô chặn | Vùng đi được | Ô mở thêm để nối |
|---|---|---|---|---|
|map_3|Rừng Xanh 3 (góc tuyết)|62.6 %|2|5 |
|map_4|Băng Tuyết (sông băng)|42.0 %|1|4 |
|map_5|Dung Nham (góc tuyết)|84.2 %|2|146 |
|hang1|Hang Pha Lê Xanh|82.2 %|1|61 |
|hang2|Hang Băng|70.2 %|1|7 |
|hang3|Hang Dung Nham|90.6 %|1|126 |
|boss_bang|Đấu trường boss Băng|58.9 %|1|1 |
|bosslua|Đấu trường boss Lửa|60.2 %|1|0 |
|bossxuan|Đấu trường boss Xuân|58.2 %|1|2 |

## Cách tạo theo loại map
- **map_3, map_4 (rừng, tuyết)**: chặn sông, hồ băng, cây, vách đá, đá tảng; chừa cỏ, đường, tuyết, cầu.
- **hang1–3, map_5 (hang, cánh đồng dung nham)**: mở theo **các con đường sáng/phẳng** vẽ trong tranh; chặn dung nham, nước, pha lê, vách.
- **3 đấu trường boss**: mở đúng **sàn tròn + bậc thang lối vào**, phần còn lại (tường, cột, vực) chặn. Boss ở giữa sàn, người chơi vào từ bậc thang (safe), portal ở chân bậc.
- **Nối vùng**: mọi chỗ đi được được nối thành 1 khối. Chỗ bị cắt thì mở lối ở nơi vật cản mỏng nhất, thường trùng cầu hoặc khe đường. Riêng **map_3 còn 2 vùng** (góc tuyết dưới trái tách khỏi rừng): nếu cần, Muse mở thêm vài ô ở chỗ cầu gỗ.

## Muse cần lưu ý
1. **hang3 và map_5**: đường tối màu, nhiều chỗ phải nối thêm (34–95 ô), nên đường đi có thể hẹp hơn tranh. Xem `debug/` rồi sửa tay dòng RLE nếu cần mở rộng.
2. Ở map_3 và map_4, khu safe/boss nằm sát mép. Muse/Luna dời vào giữa tuỳ thiết kế.
3. Cây, nhà, vách vẽ liền trong tranh nên nhân vật luôn hiện đè lên; muốn đi khuất sau cần tách lớp như pilot `../layers/`.
4. Không làm vật cản cho **hang4–6** (cảnh nhìn ngang, nhiều tầng có thang, không hợp góc nhìn từ trên của game); nên dùng làm nền hoặc màn giới thiệu.

## Tái lập
`python tools/map_collide_old.py <thư mục có src/> ../upscaled-x2`
