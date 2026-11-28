# Pilot tách lớp map_1: nền + tán cây/ngọn đá theo Y-sort

GAME-ART-CORE (Claude), 2026-11-28. Nguồn: `../upscaled-x2/map_1_x2.webp` (2804×2244). Không sửa source game.

## Kết quả
| File | Nội dung |
|---|---|
| `map_1_ground.webp` | 2804×2244, **WebP lossless**. Map đã gỡ tán cây và phần ngọn đá/pha lê cao. **Ngoài vùng gỡ, pixel trùng từng byte với nguồn**: script kiểm `assert`. WebP có mất mát (q95) đã thử nhưng lệch màu khoảng 1,5/255 nên không dùng. |
| `objects/*.png` (194 file) | 166 tán cây (`tree_*`) + 28 ngọn đá/pha lê (`rock_*`). Pixel lấy nguyên từ nguồn; **alpha mềm 3 px ra phía ngoài**. |
| `layers.json` | Mỗi vật thể: `file`, `kind`, `bbox` [x, y, w, h] theo tọa độ thế giới 2804×2244, `baseY` (điểm cắm đất để Y-sort), `trunk_px`, `area_px`. Danh sách đã sắp theo `baseY`. |
| `map_1_canopy_mask.png` | Thang xám 2804×2244: trắng = vùng có vật thể che (tán + ngọn đá), mép mềm 3 px. |
| `layers_check_2x2.jpg` | Gốc / ghép lại / nền đã gỡ / mask kèm vạch đỏ `baseY`. |
| `demo_hero_under_canopy.jpg` | Hero đứng sau tán cây bị che tự nhiên; bên cạnh là cùng vị trí với tán mờ 35 %. |
| `segmentation_overlay.jpg` | Vùng tách: tím = tán cây, cam = đá/pha lê. |
| `build_info.json`, `tools/` | Số đo và script tái lập. |

**Kiểm chứng ghép lại:** vẽ `map_1_ground` (bản lossless) rồi chồng 194 vật thể theo thứ tự `baseY` → **chênh lệch tối đa 0, 0 pixel sai khác** so với `map_1_x2.webp`. Hình học, kích thước và tông màu giữ nguyên, nên lưới va chạm 100×80 của Luna vẫn khớp 100 %.

## Cách tách
1. **Tán cây**:
   - Chọn pixel xanh lá tối hơn cỏ trong không gian OKLab (L mượt < 0,635, hue 105–170).
   - Lọc nhiễu, đóng lỗ, bỏ cụm < 2 500 px.
   - Nới 6 px để lấy phần ngọn sáng của tán.
   - Chỉ giữ cụm có vân lá (độ lệch sáng cục bộ > 0,04), loại mảng cỏ tối trơn.
2. **Thân cây ở lại lớp nền**: pixel gỗ nâu ở nửa dưới mỗi cụm tán được trả về ground (57 079 px), vì thân là vật cản.
3. **Tách từng cây**: watershed trên bản đồ khoảng cách, đỉnh cách nhau ≥ 38 px. Cụm tán liền nhau được cắt thành từng cây.
4. **Đá/pha lê**:
   - Đá là xám lạnh ít màu; pha lê là xanh, tím hoặc vàng sáng.
   - Loại vùng gần sông/biển (nới 35 px quanh các khối nước lớn).
   - Chỉ giữ khối cao (cao ≥ 45 px, cao ≥ 0,55 × rộng).
   - **30 % chiều cao phía dưới ở lại nền (gốc đá)**, 70 % phía trên thành vật thể; `baseY` là đáy của cả khối.
   - **11 cụm "đá" thực chất là nước** (thác, mặt sông, mép biển): cùng tông xanh với pha lê nên bộ lọc màu không tách được. Em loại bằng danh sách tọa độ ghi trong `tools/map_layers_build.py` (`WATER_FP`).
5. **`baseY` của cây**: dò thân nâu ngay dưới đáy tán. Có thân thì `baseY` = cuối thân. Không thấy thân thì `baseY` = đáy tán + 8 px.
6. **Lấp nền dưới tán**:
   - Đã thử SDXL inpaint trước, nhưng model tự vẽ thêm tảng đá hồng, lều nâu và bóng lạ, nên **bỏ**.
   - Cách dùng: **ghép vân từ chính các mảng cỏ sạch của map_1** (32 ô mẫu 128 px, mảnh 96 px trộn Gauss).
   - Chỉnh màu từng lỗ theo vòng đất/cỏ quanh lỗ; 6 px sát mép lỗ chuyển dần từ màu nền liền kề (đường, bờ) sang vân cỏ.
7. Alpha mềm **ra phía ngoài** vùng vật thể. Trong dải mềm đó, nền vẫn là pixel gốc, nên ghép lại cho đúng nguồn tuyệt đối dù engine vẽ alpha thế nào.

## Vật thể khó, hạn chế
- **Chỉ 13/166 cây dò được thân rõ (≥ 10 px)**, vì phần lớn cây trong tranh có thân rất ngắn hoặc bị tán che. Với các cây này, `baseY` = đáy tán + 8 px. Nên kiểm lại vài cây to ở rìa khu rừng dày.
- **Khu rừng dày bị watershed cắt thành nhiều mảnh** (ví dụ cụm cây góc dưới trái và dưới giữa). Mỗi mảnh có `baseY` riêng nên Y-sort vẫn đúng từng phần. Chỗ cắt nằm trong tán, không thấy khi ghép.
- **Vài cụm pha lê tím nằm giữa rừng bị tính là tán cây** (do bước lấp lỗ). Chúng vẫn che hero đúng, nhưng thuộc loại `tree`.
- **Nền dưới tán lấp bằng vân cỏ** nên nhìn hơi loang, lộ ra khi tán mờ còn 35 %. Đúng tông map nhưng chưa đẹp bằng tranh gốc.
- **Mảng tối của bụi thấp, hàng rào và vạt cỏ đậm ở vài chỗ bị tính là "tán"**. Hero đi qua sẽ bị che nhẹ.
- 30,2 % diện tích map là vùng vật thể (tán + ngọn đá).

## Đề xuất cho engine
1. Vẽ `map_1_ground` → gom vật thể cùng hero/quái/đạn rơi vào **một danh sách Y-sort**: vật thể dùng `baseY`, nhân vật dùng y chân. Vật thể có `baseY` lớn hơn y chân hero thì vẽ sau, tức là che hero.
2. **Chỉ vẽ vật thể có bbox giao khung camera** (194 ảnh nhỏ, trung bình khoảng 140×130 px), giống cách đang cull prop.
3. **Làm mờ tán** dùng `layers.json` là đủ, mask chỉ để vẽ minimap/debug:
   - mỗi frame, lấy các vật thể có bbox chứa vùng thân hero (không chỉ điểm chân) **và** `baseY > chân hero`;
   - lerp alpha về 0,35 trong khoảng 0,2 s; khi hero ra khỏi thì lerp về 1.
4. **Va chạm**: lưới hiện có của Luna vẫn đúng. Thân cây nằm ở ground nên ô chặn của lưới vẫn khớp với thân cây đang nhìn thấy.
5. Quái và hero bị che hoàn toàn thì nên có viền mờ hoặc bóng xuyên tán (silhouette) để người chơi không mất dấu. Tùy Luna.

## Tái lập
```
python tools/map_layers.py segment map_1_x2.webp <out>
python tools/map_layers_build.py map_1_x2.webp <out>
```
Lưu ý: `map_layers_build.py` ghi ground ra WebP q95; bản đưa vào thư mục này là bản lưu lại dạng lossless từ `_map_1_ground_lossless.png`.
