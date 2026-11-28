# 5 map mới (Desktop anh Do, 28/11) + lưới vật cản: cho Muse đưa vào game

GAME-ART-CORE (Claude), 2026-11-28. Không sửa source game.

## Đánh giá chất lượng ảnh gốc
- Cả 5 ảnh `source/m1..m5.png` chỉ **1254×1254**, nét đẹp, đúng phong cách chibi fantasy. Nhưng nếu kéo giãn thẳng lên thế giới game (khoảng 2800 px) thì sẽ **mờ, vỡ hạt**.
- Màu ảnh gốc **rất rực**, nhất là Rừng Xanh và Làng: nền sẽ tranh chú ý với hero, ngược ART_DIRECTION (nền trầm, hero nổi).
- **Đã xử lý**:
  - Upscayl `digital-art-4x` (5016²) rồi hạ về **2800×2800** → nét sạch.
  - Chỉnh màu OKLab: giảm độ rực nền, giữ sáng các điểm phép (pha lê, dung nham, băng).
  - So sánh trước/sau cùng một khung 640×480: `debug/quality_before_after.jpg`.

| id | Map | File game | Ô bị chặn | Vùng đi được |
|---|---|---|---:|---:|
| `rung_xanh_v2` | Rừng Xanh (sông + 3 cầu gỗ) | `game/rung_xanh_v2_2800.webp` | 50,4 % | 1 |
| `hoang_mac_nui_lua` | Hoang Mạc Núi Lửa | `game/hoang_mac_nui_lua_2800.webp` | 53,8 % | 1 |
| `hang_pha_le` | Hang Pha Lê | `game/hang_pha_le_2800.webp` | 63,5 % | 1 |
| `bang_tuyet` | Vương Quốc Băng Tuyết | `game/bang_tuyet_2800.webp` | 52,3 % | 1 |
| `lang_khoi_dau` | Làng Khởi Đầu (bên thác) | `game/lang_khoi_dau_2800.webp` | 70,6 % | 1 |

Mỗi file WebP 1,5–2,5 MB.

## Vật cản: `maps_collision.json`
**Cùng định dạng với `FOREST_GRID_RLE` đang chạy trong `index.html`**, nên Muse dùng lại được hàm giải mã có sẵn.
- `world`: [2800, 2800]; `grid`: [100, 100], mỗi ô 28×28 px.
- `grid_rle`: 100 dòng, mỗi dòng liệt kê khoảng **cột bị chặn** của hàng đó (`a-b` hoặc `a`; hàng 0 ở trên cùng). Đổi `new Uint8Array(100 * 80)` thành `100 * 100`.
- **Bị chặn**: sông, hồ, dung nham, vách đá, hàng cây, bụi lớn, nhà, mái, hàng rào dày, pha lê, núi lửa, viền bản đồ (1 ô).
- **Đi được**: cỏ, đường đất, cát, sàn hang, tuyết, quảng trường đá, cầu.
- `zones` (toạ độ chuẩn hoá 0–1, `r` theo bề ngang): `safe` (điểm xuất phát / khu an toàn), `elite`, `boss`, `portal`. Đặt tự động ở chỗ rộng nhất, xa nhau. Muse/Luna đổi tuỳ ý.
- `walkable_regions = 1` ở cả 5 map: mọi chỗ đi được đều nối với nhau. Chỗ nào sông/vách cắt ngang, công cụ tự mở **lối qua ở nơi vật cản mỏng nhất**, thường trùng cầu vẽ sẵn (`auto_crossings_cells` = số ô phải mở thêm cho mỗi lối).
- **Kiểm tra bằng mắt**: `debug/<id>_collision.jpg` (đỏ = chặn; vòng xanh lá = safe, vàng = elite, tím = boss, xanh dương = portal) và `debug/all_collision.jpg`.

## Muse cần lưu ý
1. Lưới tự động từ màu và độ chi tiết của tranh nên **có chỗ chưa khít**: vài bụi cây nhỏ còn đi xuyên, vài vạt cỏ bóng tối bị chặn. Xem file debug, ô nào sai thì sửa trực tiếp dòng RLE.
2. **Làng Khởi Đầu** chặn nhiều (70 %) vì dày nhà cửa, rào và cây; khu đi được chủ yếu là đường, quảng trường, bãi cỏ. Hợp làm map an toàn có NPC.
3. Cây và nhà vẽ liền trong tranh nên **nhân vật luôn vẽ đè lên**. Muốn đi "sau" cây/nhà đúng chiều sâu thì cần tách lớp như pilot `maps-anh-do/layers/`. Em chưa làm, chờ Luna quyết.
4. Ảnh gốc 1254² nằm ở `source/` nếu cần làm lại.

## Tái lập
`python tools/map_collide.py <thư mục có src/ và up4/>`. Bước up4 do Upscayl tạo; chạy khoảng 30 giây.
