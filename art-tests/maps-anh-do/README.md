# Ảnh map của anh Do (chép từ Desktop, 2026-11-28)

Nguồn: anh Do cung cấp (thư mục Desktop `map/`, `Warp/` và các file `map 1.jpg`, `map 2.png`, `map 3.png`). Ảnh giữ nguyên, không chỉnh sửa; chỉ đổi dấu cách trong tên file thành `_`. Đẩy lên để Luna xem và quyết định cách đưa vào game. Claude không sửa source game.

Xem nhanh toàn bộ: `contact_sheet.jpg`.

| File | Kích thước | Nội dung (nhận xét bằng mắt) |
|---|---|---|
| `map/map_1.png`, `map_2.png`, `map_3.png` | 1402×1122 | Rừng xanh: đường đất vàng, sông xanh, cầu gỗ, cây, đá, pha lê; `map_3` có góc tuyết dưới trái |
| `map/map_4.png` | 1402×1122 | Băng tuyết: sông băng, cây tuyết |
| `map/map_5.png` | 1402×1122 | Dung nham: nền đá nứt lửa; góc tuyết trên phải |
| `map/hang1.png`, `hang2.png`, `hang3.png` | 1402×1122 | Hang nhìn từ trên: hang pha lê xanh lá, hang băng, hang dung nham |
| `map/hang4.png`, `hang5.png`, `hang6.png` | 1536×1024 | Hang **nhìn ngang** (nhiều tầng, thang): pha lê xanh, băng, lửa. Khác góc nhìn 2.5D từ trên của game, phù hợp làm nền/minh họa hơn là sân chơi |
| `map/boss_bang.png`, `bosslua.png`, `bossxuan.png` | 1402×1122 | Đấu trường boss tròn: băng, lửa, xuân (hồng) |
| `map/tanthu.png` (1536×1024), `tanthu1.png` (3072×2048, bản lớn của cùng ảnh) | | Làng tân thủ: nhà mái xanh/đỏ/tím, quảng trường tròn giữa |
| `warp/dichchuyen.png` | 1024×1024, RGBA | Vòng cổng dịch chuyển phát sáng xanh/vàng, nền tối |
| `hi-res/map_1_4206x3366.jpg`, `map_2_2804x2244.png`, `map_3_2804x2244.png` | | Bản phân giải cao của `map_1/2/3` |

Không chép: `map 1_upscayl_3x_upscayl-lite-4x.png` (22 MB, cùng nội dung và cùng kích thước với `map 1.jpg`).

Ghi chú cho Luna khi tích hợp (chưa làm, chờ Luna quyết):
- Đây là **ảnh nền nguyên khối**, đã vẽ sẵn cây/đá/sông. Nếu dùng làm sân chơi thì vật cản và va chạm phải khai báo theo vị trí trên ảnh (không dùng prop rời như bộ Rừng Xanh), hoặc dùng làm nền minimap/màn chọn map.
- Các map rừng rất rực so với ART_DIRECTION (nền trầm hơn hero); nếu làm sân chơi có thể cần giảm bão hòa như tile v2b.
- `warp/dichchuyen.png` khác phong cách với cổng đá đã tách ở `art-tests/portal-split/`; Luna chọn bản nào dùng.
