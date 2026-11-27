# GAME_ART_REVIEW: Fantasy: Huyền Thoại Lục Địa (v0.3.7)

Người lập: Claude (GAME-ART-CORE) · Ngày 2026-11-28 · Trạng thái: **ĐÁNH GIÁ, chưa sửa gì trong game**

Nguồn đã đọc: PROJECT_HANDOVER.md → SPEC.md → ART_DIRECTION.md → GDD.md → HUD_V2.md → ARCHITECTURE.md → PROGRESS.md (commit `cfecb34`).
Ảnh được trích xuất bằng script (`review/tools/extract_assets.py`), không đọc base64 vào context. Đã mở bản production `fantasy-game.tuandd19985.workers.dev` ở khung 1280×720 và chụp lại (`review/screenshots/`).

## 1. Phong cách mà chủ dự án đã chốt

| Hạng mục | Quy định (nguồn) |
|---|---|
| Nhân vật người chơi | **CHIBI ĐẸP ở mọi nơi**: đầu to, giáp/vũ khí/tóc rõ nét, màu tươi, nổi bật trên nền map, nhìn là biết phái và giới tính (ART_DIRECTION, chốt 22:10) |
| Quái / boss | **ĐÃ DUYỆT 2026-11-28: chibi-fantasy đồng bộ hero** (đầu to, viền đậm, màu tươi; hero vẫn nổi nhất khung). Boss phải TO và DỮ hơn hẳn quái thường: tỉ lệ lớn, rune/sẹo/mắt phát sáng (căn cứ SPEC mục 1b + ART_DIRECTION.md, commit 243c0fa). Thiết kế chi tiết Rừng Xanh: `docs/MONSTER_DESIGN_RUNG_XANH.md` |
| Map / môi trường | Theo định hướng chất lượng Concept.png; Concept.png vẫn là chuẩn chất lượng + giao diện tổng thể |
| Định hướng chất lượng | Concept.png: HUD viền vàng cổ trên nền tối, elite viền đỏ, panel paper-doll có ✕, dải 7 map đúng palette. **Concept.png không có trong repo** (nằm trong reference-zip trên máy Luna) |
| Góc nhìn | Top-down 2.5D hơi nghiêng, di chuyển tự do 8 hướng, màn hình ngang |
| Bị cấm | Hình tròn/vuông đơn sắc, emoji, hình vẽ sơ sài, ảnh tĩnh kéo trượt thay cho animation |
| Animation bắt buộc mỗi nhân vật | đứng, chạy, đánh thường, 4 skill, skill phụ chủ động, trúng đòn, tử vong, hồi sinh |
| Trang bị | Đổi ngoại hình thật; +7 phát sáng, +10 hào quang, +15 hiệu ứng đặc biệt; khung độ hiếm xám/xanh/tím/vàng |
| Nhịp độ | "ĐẸP là tiêu chí trên hết", không cắt giảm chất lượng để kịp giờ |
| Quy trình | Bản xem trước → Do duyệt phong cách → mới sản xuất hàng loạt |

## 2. Hiện trạng hình ảnh (đo trên production v0.3.7)

Toàn bộ ảnh thật gồm **19 file WebP** trong bảng `__A` (k0–k18). **Mọi thứ còn lại được vẽ bằng code Canvas:** quái, boss, map, cây, cầu, icon HUD, icon skill, panel, hiệu ứng.

| Nhóm | Khóa | Kích thước | Nhận xét |
|---|---|---|---|
| Tranh mở đầu | k1 | 1920×1280 | Đẹp, đúng chibi. **Lệch thiết kế** so với hero trong game: Kiếm Sĩ tóc đen thay vì bạc, Pháp Sư nữ đội mũ tím |
| Hero toàn thân ×6 | k2–k7 | khoảng 500–570×640 RGBA | Chất lượng cao, đồng bộ, đọc rõ phái và giới tính. Tất cả **nhìn thẳng (front)** |
| Chân dung ×6 | k0, k8–k12 | 800×800 | Đẹp, đồng bộ với hero. Dùng tốt cho HUD và panel |
| Dải chuyển động ×6 | k13–k18 | 2520×500 = 6 khung 420×500 | Đứng 2 khung gần như trùng nhau; chạy 2 khung; đánh 2 khung. Lỗi xem mục 3 |

### Ảnh chụp trong game
- `01_create_character.jpg`: sân khấu thảo nguyên đẹp, 3 hero chibi nổi bật. Panel phải còn kiểu UI web phẳng.
- `02/03_ingame_*.jpg`: **map Rừng Xanh vẽ bằng code**: nền xanh phẳng với các mảng tròn, cây kiểu "kẹo mút" giống nhau, sông phẳng, Goblin là hình code nhỏ và mờ. Hero chibi AI cao khoảng 150 px ở khung 720p, **chênh lệch phong cách rất lớn** với thế giới vẽ code. Ở biên dưới map lộ **vùng đen ngoài map** (SPEC 6c cấm điều này; thuộc phần code, đã ghi lại để Codex xem).
- `04_equipment_panel.jpg`: panel nền kem, bảng số và icon nét mảnh. **Chưa có paper-doll, chưa có viền vàng cổ** như Concept.
- HUD: 5 icon tròn nền tối đúng vị trí HUD V2, nhưng chỉ là glyph trắng đơn giản. Nút skill là vòng xám có chữ "Lv 8". Chưa có icon riêng cho từng skill như SPEC yêu cầu.

## 3. Lỗi kỹ thuật hình ảnh đã đo

### 3.1 Ám màu nền (magenta/tím)
Script `contact.py` đo các pixel viền đặc nằm sát vùng trong suốt có ánh magenta (R và B lớn hơn G ít nhất 40):

| Sprite | % pixel viền ám magenta | Ghi chú |
|---|---:|---|
| k2 Kiếm Sĩ Nam | 51,6 % | |
| k3 Kiếm Sĩ Nữ | 57,4 % | |
| k4 Pháp Sư Nam | 61,5 % | |
| k5 Pháp Sư Nữ | 94,9 % | Tóc tím trùng màu khóa nên số đo bị nhiễu, cần xem bằng mắt |
| k6 / k7 Cung Thủ | 59,2 % / 45,6 % | |
| k13–k18 dải chuyển động | 47–68 % | |

Ảnh phóng to `review/sheets/fringe_zoom.jpg` cho thấy **đường viền tối của áo choàng và giáp ngả tím** khi đặt trên nền tối hoặc sáng. Đó là viền outline bị trộn với magenta lúc tách nền.

**Ba nguyên nhân gốc** (có bằng chứng trong `art-tests/` của repo):
1. **Ghi màu nền vào prompt làm màu "chảy" sang chủ thể.** Ảnh SDXL vòng 1 có câu "flat magenta background" cho ra hiệp sĩ giáp hồng và goblin mặc áo tím (`review/sheets/sdxl_tests.jpg`). CLIP gắn tính từ màu cho cả cảnh, không chỉ cho nền.
2. **Chroma key cộng despill 1 pixel không đủ** khi outline có anti-alias: pixel viền là hỗn hợp giữa màu outline và magenta, chỉ giảm bão hòa thì vẫn còn ánh tím.
3. **Tách nền bằng BiRefNet mà không xử lý mask:** `round1_warrior_cut.png` chỉ có **6.952 pixel đặc hoàn toàn** trên khoảng 1 triệu pixel; phần lớn thân nhân vật chỉ bán trong suốt. Đặt vào game thì **màu cỏ của map hiện xuyên qua người**, đây cũng là một dạng "ám màu nền".

### 3.2 Dải chuyển động
- k16 (Pháp Sư Nữ): **mảnh của khung bên cạnh lọt vào mép** (quả cầu và tóc bị cắt ở mép khung 1–5). Handover đã ghi nhận lỗi này.
- k18 (Cung Thủ Nữ): khung "chạy" dùng dáng ngắm cung, không phải dáng chạy.
- Đứng thở 2 khung gần như trùng nhau; chạy chỉ có 2 khung nên khi chơi trông giật. Vũ khí đổi chiều và tỉ lệ giữa các khung (k13 khung 5–6).
- Chưa có khung trúng đòn, tử vong, hồi sinh và 4 skill. Hiện game giả lập bằng biến đổi transform.
- Chỉ có một hướng nhìn (chính diện) và lật trái/phải. SPEC đã duyệt "chuẩn sprite 8 hướng" nhưng chưa có asset nào.

## 4. Phân loại: GIỮ / SỬA / THAY

| Tài nguyên | Quyết định | Lý do |
|---|---|---|
| 6 chân dung (k0, k8–k12) | ✅ **GIỮ** | Đẹp, là chuẩn nhận diện nhân vật. Dùng làm **ảnh tham chiếu khóa (identity lock)** |
| 6 hero toàn thân (k2–k7) | ✅ **GIỮ + làm sạch viền** | Thiết kế đạt. Chỉ cần decontaminate viền tím (xử lý lại từ chính file, không vẽ lại) |
| Tranh mở đầu (k1) | 🟡 **GIỮ tạm**, cần Do quyết | Đẹp, nhưng thiết kế nhân vật lệch hero. Có thể giữ làm key art, hoặc vẽ lại cho khớp |
| 6 dải chuyển động (k13–k18) | 🔴 **THAY** | Lỗi mảnh lọt khung, sai dáng, ít khung, ám viền |
| Quái/boss vẽ code (23 họ + 7 boss) | 🔴 **THAY** | Thuộc nhóm "hình vẽ sơ sài" bị ART_DIRECTION cấm |
| Map vẽ code (cây, cỏ, sông, cầu, nhà) | 🔴 **THAY** | Nền phẳng, cây lặp lại, không có lớp xa/gần như SPEC 6 |
| Icon HUD / skill / trang bị / ngọc | 🔴 **THAY** | Glyph đơn giản, chưa có icon riêng theo skill hay món đồ |
| Khung panel / nút / thanh HP | 🟡 **NÂNG CẤP** | Bố cục HUD V2 đúng, chỉ thiếu "da" viền vàng cổ |
| Ảnh thử SDXL trong art-tests/ | ❌ **KHÔNG DÙNG** | Ám màu, sai phong cách, chỉ có giá trị làm bằng chứng lỗi |

## 5. Chuẩn hình ảnh

Hai dòng **Hướng sprite** và **Phong cách quái/boss** đã được Do duyệt ngày 2026-11-28 (căn cứ SPEC mục 1b + ART_DIRECTION.md, commit 243c0fa). Các dòng còn lại vẫn là PROPOSED.

| Thông số | Nội dung |
|---|---|
| Hướng sprite (**ĐÃ DUYỆT 2026-11-28**, căn cứ SPEC mục 1b + ART_DIRECTION.md, commit 243c0fa) | Giai đoạn mẫu làm **4 hướng**: 2 hướng vẽ thật là **xuống** và **lên** (góc 3/4 từ trên xuống khoảng 30°); **trái/phải có được bằng lật ngang**. Di chuyển 8 hướng vẫn do engine xử lý. Chuẩn 8 hướng đầy đủ chỉ xét lại khi làm bộ animation nhân vật chính thức |
| Phong cách quái/boss (**ĐÃ DUYỆT 2026-11-28**, căn cứ SPEC mục 1b + ART_DIRECTION.md, commit 243c0fa) | Chibi-fantasy đồng bộ hero. Boss to và dữ hơn hẳn quái thường trong cùng phong cách |
| Khung gốc nhân vật | 512×512, nhân vật cao khoảng 440 px, chân đặt trên đường cơ sở y = 480 (anchor chân). Hiển thị trong game ở khoảng 150 CSS px (giữ như hiện tại) |
| Tỉ lệ thân | Chibi 2,5 đầu (giữ đúng tỉ lệ k2–k7) |
| Tỉ lệ so với hero (PROPOSED) | Quái thường 0,7–1,0×; tinh anh 1,25× + viền đỏ (code); boss khoảng 3× quái cùng họ (Chúa Sói khoảng 3× Sói Rừng theo MONSTER_DESIGN), khung 1024×1024 |
| Nét viền | Outline nâu đậm hoặc xanh đen dày khoảng 3 px ở khung 512, **không dùng đen thuần, không dùng tím** |
| Ánh sáng | Nguồn sáng trên-trái, bóng đổ elip mềm do code vẽ (không vẽ bóng vào sprite) |
| Bảng màu | Nhân vật bão hòa cao; map trầm hơn 15–25 % độ sáng; mỗi map một màu nhấn (Rừng: vàng nắng · Hang: tím pha lê · Đầm: lục độc · Sa mạc: cam · Núi lửa: đỏ dung nham · Băng: lam · Lâu đài: tím than + đỏ) |
| Định dạng xuất | WebP RGBA q85, sprite atlas theo nhân vật/quái, mỗi map nạp riêng |

## 6. Quyết định của chủ dự án
1. ✅ **ĐÃ DUYỆT 2026-11-28** (căn cứ SPEC mục 1b + ART_DIRECTION.md, commit 243c0fa): quái/boss chibi-fantasy đồng bộ hero; boss to và dữ hơn hẳn quái thường.
2. ✅ **ĐÃ DUYỆT 2026-11-28** (căn cứ SPEC mục 1b + ART_DIRECTION.md, commit 243c0fa): sprite giai đoạn mẫu làm 4 hướng (vẽ xuống/lên, lật ngang ra trái/phải); 8 hướng xét lại ở giai đoạn animation chính thức.
3. ⏳ Còn chờ: gửi Concept.png vào repo, hoặc chép vào `C:\AI\GAME-ART-CORE\reference\`, để làm chuẩn so sánh (nhất là cho map).
