# REPORT: Tách cổng chính thức + bảng footprint + biến thể tile

GAME-ART-CORE (Claude) · 2026-11-28. Căn cứ [ENGINE_PROP_LAYER_SPEC](../../docs/art/ENGINE_PROP_LAYER_SPEC.md), Luna duyệt ở commit 28caab2:
- cổng tách bệ (ground) và vòm (sorted), dùng chung anchor;
- trigger trên bệ chỉ hiện nút tương tác, không tự chuyển màn;
- bụi trang trí và khóm hoa không va chạm;
- bóng dùng loại baked.

Không sửa source game. Không sinh ảnh mới: cổng tách từ `props_clean/da_cong_dich_chuyen.png` (bản a7ce924).

## 1. Tách cổng tại biên thật
- **Biên cắt là mép trên thật của bệ**, không phải đường ngang:
  - Tìm 398 cột ảnh mà giữa vòm và bệ có khe trong suốt.
  - Lấy hàng điểm ảnh đặc đầu tiên của bệ ở mỗi cột đó, rồi khớp một đường elip (tâm 476,8 / 655,9; bán trục 428,9 × 181,3 px nguồn).
  - Sai số khớp trung bình **2,4 px**. Một cột ngoại lệ là dải bóng xám ở chân vòm, đã được bỏ qua nhờ hàm mất mát bền.
- Giữ thêm 3 px phía trên elip cho bệ, để viền đen của mép bệ thuộc về bệ.
- Hai cụm cột hai bên không có elip đi qua nên dùng ngưỡng y = 540. Vòm không có pixel nào dưới hàng khoảng 490, còn thành bên của bệ bắt đầu từ khoảng 600.
- **Hai phần không chồng pixel nào.** Ghép bệ + vòm lại về đúng khung nguồn thì **trùng khớp từng byte** với ảnh gốc (`recomposite_identical: true`).
- `portal_split_check.jpg`: bên trái là đường cắt (đỏ) và anchor (vàng), bên phải tô màu cam = vòm, xanh = bệ.
- `portal_layer_scene.jpg`: ghép theo pass ground → sorted. Bên trái hero đứng sau vòm nên bị vòm che phần dưới. Bên phải hero đứng trên bệ nên được vẽ đè lên vòm.

| File | Layer | Kích thước hiển thị | anchorX, anchorY |
|---|---|---|---|
| `portal_platform.png` (953×511 nguồn) | ground | 206,4 × 111,9 | 103,2 ; 0,9 |
| `portal_back.png` (907×489 nguồn) | sorted, `sortY = 0` | 198,9 × 107,2 | 96,6 ; 101,8 |

- **Anchor chung** của group `forest-portal-01`:
  - Tọa độ nguồn (482,5 ; 476). x là trung điểm giữa hai cột ngoài; y là đường chân cột, tức hàng viền đen cuối cùng của đế cột, phía dưới chỉ còn dải bóng xám baked.
  - Tỉ lệ hiển thị 0,219316: cổng cao 218 px như trong scene của spec.
- Vẽ mỗi ảnh tại `(x − anchorX, y − anchorY)`. Vì vậy bệ tự nằm ngay dưới đường chân vòm; anchorY của bệ là 0,9 vì mép trên bệ gần trùng đường chân.

## 2. Bảng footprint (`props_layer.json`, đúng schema `PropPart` của spec)
Đơn vị là px thế giới ở hiển thị 1×. Offset tính từ anchor group; elip tính từ tâm, kích thước toàn phần. Mọi part đều dùng `shadow: {type: "baked"}`.

| Part | Layer | Cao hiển thị | Collision | Interaction | Nguồn số |
|---|---|---:|---|---|---|
| Bệ cổng `forest-portal-01-platform` | ground | 111,9 | none | **elip 131,7 × 55,7, tâm (−1,3 ; +39,5)**, tức 70 % mặt trên của bệ | đo trên elip mép bệ |
| Vòm cổng `forest-portal-01-arch` | sorted | 107,2 | **2 elip: 30,5 × 22,9 tại (−79,0 ; 0) và 28,7 × 21,5 tại (+78,7 ; 0)** | none | đo độ rộng đế 2 cột ngoài; cao = 0,75 × rộng |
| Cây sồi | sorted | 275 | elip 84 × 26 tại (0 ; 0) | none | giữ số của spec |
| Cột đá cổ | sorted | 215 | elip 76 × 28 tại (0 ; 0) | none | giữ số của spec |
| Tảng đá rêu | sorted | 115 | **elip 100 × 32** tại (0 ; 0) | none | **đổi từ 150 × 42**: cả ảnh đá chỉ rộng 137,6, đế rộng 99,2 |
| Bụi cây (trang trí) | sorted | 95 | none | none | Luna chốt |
| Khóm hoa | ground (decal) | 60 | none | none | Luna chốt |

- So với số thử trong spec: chân vòm ±78 với 28 × 22, trigger 150 × 48 tại +40. Số đo trên ảnh tách cuối khớp vị trí; trigger hẹp hơn một chút và cao hơn một chút để nằm gọn trong mặt bệ.
- **Anchor các prop khác** là tâm đáy đế: x = giữa bề ngang 15 % hàng dưới cùng của phần đặc; y = hàng đặc thấp nhất trừ 5 px.
- Độ rộng đế đo được ghi ở `measured_base_width_display_px` để Codex đối chiếu.
- **Cần Luna/Codex xác nhận**:
  1. Tảng đá 100 × 32 thay cho 150 × 42.
  2. Trigger 70 % mặt bệ.
  3. Vòm: phần giữa đi qua được nhưng ảnh vẽ khối đá liền. Khi đi qua, hero bị vòm che vì vòm vẽ theo sort; nếu muốn chặn cả khối giữa, thêm 1 elip khoảng 120 × 20 tại (0 ; −5).

## 3. Biến thể tile cỏ giảm độ rực: v2b (`../rung-xanh-map-sample/tile-v2/`)
Tile v2 chưa được duyệt nên em gửi thêm **1 biến thể v2b** để Luna so. Không sinh lại: dùng đúng nguồn seamless của v2 (seed 729003, inpaint 729503), chỉ đổi hậu kỳ:
- dời tông về xanh rêu trầm, bớt vàng ô liu;
- giảm bão hòa còn 55 %;
- giữ lại nhiều vân cỏ hơn v2 một chút (`FLATTEN_KEEP` 0,45; `CONTRAST` 0,95).

| Chỉ số | v1 | v2 | **v2b** |
|---|---:|---:|---:|
| Bão hòa TB của tile | 0,76 | 0,44 | **0,22** |
| Tỉ lệ bão hòa tile ÷ hero (Kiếm Sĩ Nam, TB 0,29) | 2,65 | 1,53 | **0,78** |
| Độ sáng TB của tile (hero: 130,7) | 80,2 | 111,8 | **≈ 98** |
| Màu TB RGB | 53 / 104 / 32 | 115 / 119 / 67 | ≈ 92 / 106 / 77 |
| Seam ngang / dọc | 1,12 / 1,40 | 1,33 / 1,02 | 1,32 / 1,00 |

- **v2b là bản duy nhất có nền kém bão hòa và tối hơn hero**, đúng ART_DIRECTION: nền map trầm, nhân vật nổi bật hơn nền.
- Không lộ seam; nhịp lặp ở lưới 3×3 giống v2.
- Ảnh duyệt: `compare_v2_vs_v2b.jpg` (scene v2 bên trái, v2b bên phải), `scene_test_v2b_1280x720.jpg`, `tile_v2b_2x2.jpg`, `tile_v2b_3x3.jpg`. Số đo ở `variant_v2b.json`.
- **Rủi ro**: v2b ngả xám rêu, có thể bị coi là hơi u. Nếu muốn ở giữa v2 và v2b thì chỉ cần chỉnh `SAT` hoặc `TARGET_RGB` trong `tools/tile_variant_v2b.py`.

## Tái lập
- `tools/split_portal.py <props_clean> <out> <tile> <hero>`
- `../rung-xanh-map-sample/tools/tile_variant_v2b.py`. Script tự kiểm rằng nguồn dựng lại cho ra đúng từng byte của tile v2 đã đẩy.
