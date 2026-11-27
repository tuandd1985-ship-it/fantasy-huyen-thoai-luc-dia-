# ART_DIRECTION — FANTASY: HUYỀN THOẠI LỤC ĐỊA
Tiêu chuẩn hình ảnh và animation. SPEC.md ưu tiên cao nhất; mục nào chưa được Do phê duyệt ghi PROPOSED.

## Hình định hướng chính thức (từ 2026-11-27)
- File `reference-zip/assets/Concept.png` (trong bộ Fantasy_RPG_Muse.zip Do gửi) là ĐỊNH HƯỚNG CHẤT LƯỢNG đồ họa + giao diện chính thức: HUD viền vàng cổ trên nền tối, Kiếm Sĩ choàng đỏ chém xoáy vàng giữa bầy sói, elite viền đỏ, minimap trên phải, panel paper-doll có ✕, dải 7 map đúng palette. Số liệu trong ảnh chỉ minh họa, không phải thông số thật. Concept là ảnh tĩnh tham chiếu — asset gameplay phải tự tạo có animation, không dùng ảnh concept làm gameplay.
- Đối chiếu chi tiết và các điểm PROPOSED/xung đột từ bộ zip: xem BAO-CAO-DOI-CHIEU-ZIP.md.

## Phong cách chung
- Fantasy trung cổ, bán hiện thực; cảm hứng Diablo Immortal / MU Online / Ragnarok nhưng tài nguyên tự tạo, đồng nhất một thế giới.
- Bảng màu: nền map trầm + điểm sáng ma thuật (vàng/pha lê/lửa/băng theo khu vực); nhân vật nổi bật hơn nền bằng viền sáng và hào quang theo phái.
- CẤM dùng làm đồ họa chính thức: hình tròn/hình vuông đơn sắc, emoji, hình vẽ sơ sài, ảnh tĩnh kéo trên màn hình thay animation.

## MỞ ĐẦU GAME (Do chốt 2026-11-27 22:21)
- Màn hình chờ load: tranh giới thiệu nhân vật chính đối đầu quái vật + tên game "FANTASY — HUYỀN THOẠI LỤC ĐỊA" + thanh tải dữ liệu, hiện trong lúc game tải, xong mới vào chọn nhân vật.
- Luồng vào game (Do chốt 2026-11-27 22:58): BỎ màn ô chọn nhân vật ở ngoài — qua màn load là vào thẳng sân khấu 3 nhân vật; nhân vật đã lưu truy cập qua nút nhỏ "Nhân vật đã lưu" trên sân khấu. KHÓA NGANG TOÀN BỘ: máy dọc là hiện lớp phủ xoay ngang ngay từ đầu, mọi màn đều ngang.
- Sân khấu chọn/tạo nhân vật (cập nhật theo 2 ảnh mẫu Do gửi 2026-11-27 22:27, thay ý "3 bệ đá thẳng hàng"): cảnh THẢO NGUYÊN TOÀN CẢNH FULL MÀN HÌNH (cỏ xanh, sông nhỏ, cối xay gió, trời mây — không panel tối ở giữa), 3 nhân vật chính đứng rải tự nhiên trong cảnh, icon tròn + tên phái trên đầu mỗi nhân vật; chạm chọn thì nhân vật nổi bật + hiện chi tiết gọn bên phải (biểu đồ sao, đổi Nam/Nữ tại chỗ); ô tên dưới giữa, nút Vào game góc dưới phải.

## PHONG CÁCH NHÂN VẬT: CHIBI TOÀN BỘ (Do chốt 2026-11-27 22:10 — THAY THẾ hướng bán hiện thực cho riêng phần nhân vật người chơi)
- Nhân vật người chơi vẽ kiểu **CHIBI ĐẸP** ở MỌI nơi xuất hiện: sprite trong sân LẪN chân dung (màn hình chọn/tạo nhân vật, HUD, panel). Đầu to, tỉ lệ dễ thương, giáp/vũ khí/kiểu tóc vẽ rõ và sắc nét, màu tươi nổi bật trên nền map, nhìn là phân biệt được phái + giới tính ngay.
- Chân dung bán hiện thực đã vẽ ở các vòng trước (Kiếm Sĩ/Pháp Sư) KHÔNG còn là chuẩn — phải vẽ lại chibi đồng bộ cả 6 biến thể ở vòng hình ảnh kế tiếp.
- Quái/boss/map giữ phong cách Fantasy như Concept.png, nhưng tông màu/độ sáng phải hài hòa với nhân vật chibi (nhân vật luôn nổi bật nhất khung hình). Nếu sau này Do muốn quái cũng chibi thì chốt riêng.

## Nhân vật
- 6 biến thể (3 phái × Nam/Nữ), mỗi biến thể: chân dung chi tiết + sprite trong sân đồng bộ (cùng giáp/vũ khí/màu chủ đạo).
- Bộ animation bắt buộc cho mỗi nhân vật: đứng yên (idle), chạy, đánh thường, thi triển 4 skill chính, dùng skill phụ chủ động, nhận sát thương, tử vong, hồi sinh. Nhân vật trong sân phải ĐỌC ĐƯỢC phái và giới tính ở kích thước chơi thật.
- Trang bị thay đổi ngoại hình thật theo ô (vũ khí trước tiên, sau đó giáp/mũ): cấp đồ càng cao hình càng đẹp; hiệu ứng +7 phát sáng, +10 hào quang, +15 hiệu ứng đặc biệt.
- Trạng thái hiện tại (2026-11-27): chân dung Kiếm Sĩ/Pháp Sư (nam/nữ) đã vẽ lại chất lượng cao; Cung Thủ còn bộ cũ — CHƯA ĐẠT, phải vẽ lại đồng bộ. Sprite trong sân là vẽ canvas có hoạt ảnh đánh/trúng đòn nhưng chi tiết còn dưới chuẩn — thuộc diện THIẾT KẾ LẠI ở giai đoạn chuẩn (xem GAP_ANALYSIS.md).

## Quái, boss, map
- Mỗi họ quái một silhouette riêng, đọc được hành vi từ hình (bay = có cánh, tank = to/chậm, độc = tông xanh/tím...).
- Boss: mô hình riêng (không phóng to quái thường), animation skill riêng, vòng cảnh báo vùng nguy hiểm hiện trước khi skill nổ, đổi màu/phase ở <50% HP.
- Map: lớp xa/gần tạo chiều sâu, vật thể có bóng; mỗi khu vực một tông màu + vật trang trí riêng (Rừng Xanh: cây, sông, cầu gỗ, phế tích...). Rừng Xanh là map CHUẨN chất lượng để nhân rộng.

## Giao diện
- HUD ngang theo sơ đồ GDD mục III; icon chức năng nhỏ gọn dạng dock, popup có nút ✕; font dễ đọc trên iPhone, tránh tai thỏ (safe-area).
- Icon skill/icon trang bị: vẽ riêng theo từng skill/món, nền theo độ hiếm (khung màu: xám Thường, xanh Hiếm, tím Sử thi, vàng Huyền thoại).

## Nhịp độ (Do chốt 2026-11-27)
- KHÔNG cần nhanh: bố cục và hình ảnh được phép làm lâu, ĐẸP là tiêu chí trên hết. Không cắt giảm chất lượng đồ họa để rút ngắn thời gian.
- Hình mẫu tham khảo: Luna tự tạo tài nguyên riêng, không bắt buộc Do cung cấp. Nếu Do gửi ảnh phong cách anh thích (game/tác phẩm bất kỳ), Luna bám theo gu đó nhưng vẫn vẽ tài nguyên riêng, không sao chép nguyên bản.

## Quy trình duyệt (bắt buộc)
Thiết kế/trình bản xem trước (màn hình chính, chiến đấu, Rừng Xanh, 1 nhân vật mẫu đủ bộ animation) → Do duyệt phong cách → mới sản xuất hàng loạt cho các phái/map còn lại.
