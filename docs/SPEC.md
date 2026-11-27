# SPEC — Game Đánh Quái Fantasy (điện thoại)
File chỉ thị gốc của dự án. Mọi lần sửa/nâng cấp PHẢI đối chiếu file này trước, làm xong tick checklist ở cuối. Cập nhật file này ngay khi Do chốt thêm yêu cầu.
Khởi tạo: 2026-11-27. Chủ dự án: Do (Tony Đỗ). Người thực hiện: Luna.

## 1. Tổng quan
- TÊN GAME (chốt 2026-11-27 theo bản thiết kế v2): **FANTASY — HUYỀN THOẠI LỤC ĐỊA**. Thể loại Action RPG Fantasy 2.5D (cảm hứng Diablo Immortal / MU Online / Ragnarok, thế giới riêng), nền tảng iPhone/Android/trình duyệt PC, cấp độ ban đầu Lv1–70.
- BẢN THIẾT KẾ V2 (~/workspace/game-danh-quai-fantasy/DESIGN-V2.md) là phần bổ sung chi tiết của SPEC này: bảng skill cụ thể từng phái (sát thương/hồi chiêu/mana), chỉ số khởi đầu 3 phái, bảng ngọc 7 cấp + giới hạn cân bằng, chi tiết 7 map và skill từng boss, cốt truyện/nhiệm vụ, thành phố NPC, 10 màn hình chức năng, bố cục HUD chuẩn, lộ trình mở rộng (pet/set item/phụ bản/tháp vô tận → thú cưỡi/đồng bộ tài khoản → xếp hạng/bang hội/multiplayer/PvP/giao dịch). Khi SPEC và DESIGN-V2 khác nhau về SỐ LIỆU, lấy DESIGN-V2 làm chuẩn. Yêu cầu nổi bật của v2: animation riêng từng nhân vật (đứng/chạy/đánh/4 skill/trúng đòn/chết/hồi sinh), trang bị thay đổi NGOẠI HÌNH thật khi mặc, trang bị phát sáng từ +7 / hào quang +10 / hiệu ứng đặc biệt +15, boss có cảnh báo vùng nguy hiểm trước khi tung skill, mỗi map có khu an toàn + NPC + cổng dịch chuyển + vùng tinh anh + khu boss + điểm bí mật, giai đoạn hoàn thiện mở rộng lên 10 ô trang bị.
- Game Fantasy đẹp, chơi trên iPhone (web app, sau này deploy Cloudflare, thêm vào Màn hình chính như app thật).
- Vòng chơi cốt lõi: đánh quái theo level/map → lên cấp → nhặt trang bị rơi → mặc/nâng cấp trang bị → đánh map khó hơn + boss.
- Tiêu chí xuyên suốt: bố cục chặt chẽ, KHÔNG lag trên iPhone, sửa chữa/nâng cấp liên tục phải dễ (không chắp vá).

## 1b. Quyết định của Do ngày 2026-11-27 (sau báo cáo đối chiếu zip — BAO-CAO-DOI-CHIEU-ZIP.md)
- DUYỆT kế hoạch 5 bước trong báo cáo đối chiếu. Các đề xuất PROPOSED của bộ zip được duyệt theo kế hoạch, gồm: bảng % rơi đồ đảm bảo từ boss theo map, danh sách 10 ô trang bị cụ thể, nâng cấp thất bại không phá đồ (MVP), tùy chọn AUTO chi tiết, chuẩn sprite 8 hướng, lưu IndexedDB có schema/migration, mục tiêu hiệu năng + bài test dài, dock icon ở TRÊN GIỮA theo Concept.png (riêng vị trí icon này đã bị HUD V2 thay thế cùng ngày — xem mục 6d-bis: 5 icon tròn trên PHẢI cạnh minimap).
- NGOẠI LỆ DUY NHẤT: KHÔNG khóa tính năng theo cấp kiểu Lv3 AUTO/shop, Lv5 rèn, Lv10 skill phụ, Lv12 khảm, Lv18 ghép ngọc — GIỮ MỞ như SPEC gốc (AUTO, cửa hàng, lò rèn, skill phụ, khảm/ghép ngọc dùng được không chờ mốc cấp; chỉ skill CHÍNH vẫn mở theo Lv1/8/15/25 như mục 2).

## 2. Nhân vật
- 3 phái, mỗi phái bộ 4 skill RIÊNG (tổng 12 skill), mở khoá theo cấp Lv1 / Lv8 / Lv15 / Lv25, mỗi skill có icon + hiệu ứng riêng, có hồi chiêu + tốn mana:
  - Kiếm Sĩ: cận chiến, HP/phòng thủ cao.
  - Pháp Sư: đánh xa, sát thương phép lớn, HP thấp.
  - Cung Thủ: đánh xa, tốc độ + tỉ lệ chí mạng cao.
- Giới tính Nam/Nữ cho từng phái: 6 biến thể ngoại hình khác rõ (sprite, chân dung, tóc, trang phục). Giới tính CHỈ đổi ngoại hình, không đổi chỉ số.
- Chọn phái + giới tính ở màn hình tạo nhân vật, lưu cùng tiến trình.

## 2b. Skill phụ (hỗ trợ) và thăng tiến theo cấp (bổ sung 2026-11-27)
- 4 skill ở mục 2 là SKILL CHÍNH (đánh). Ngoài ra có SKILL PHỤ hỗ trợ cho skill chính và nhân vật, mỗi phái một bộ phụ riêng, ví dụ:
  - Kiếm Sĩ: Lá Chắn Thép (giảm sát thương nhận vào), Cuồng Nộ (tăng tốc đánh tạm thời), Hút Máu (đánh trúng hồi HP theo % sát thương).
  - Pháp Sư: Lá Chắn Mana (lấy mana đỡ đòn), Hồi Mana Nhanh, Khuếch Đại Phép (tăng sát thương skill chính).
  - Cung Thủ: Né Tránh (tỉ lệ né đòn), Bước Chân Gió (tăng tốc chạy + tốc đánh), Dấu Ấn Yếu Điểm (tăng chí mạng lên mục tiêu bị đánh dấu).
  - Skill phụ gồm loại chủ động (bấm dùng, có hồi chiêu) và bị động (luôn có tác dụng); icon + hiệu ứng riêng như skill chính.
  - Hiệu quả của skill phụ (và nhiều hiệu ứng khác) tính THEO PHẦN TRĂM là chính: +% dame, +% né, +% tốc độ... (xem công thức thống nhất ở mục 5).
- LÊN CẤP = MẠNH LÊN THẬT theo 2 đường, công thức/curves để ở lớp dữ liệu:
  - Cộng ĐIỂM THÂN THỂ (thuộc tính) mỗi cấp để người chơi tự cộng vào các chỉ số gốc (sức tấn công, HP, phòng thủ, tốc độ/chí mạng tuỳ phái) — thân thể mạnh lên vĩnh viễn.
  - Cộng ĐIỂM SKILL mỗi cấp để nâng cấp skill chính (tăng sát thương, giảm hồi chiêu) và skill phụ (tăng hiệu quả) theo từng bậc.
  - Cấp càng cao nhân vật càng mạnh rõ rệt (chỉ số gốc tự tăng theo cấp + điểm cộng thêm + skill được up).

## 2c. Tên nhân vật, nhiều nhân vật/tài khoản và Cài đặt (bổ sung 2026-11-27)
- TẠO TÊN NHÂN VẬT: ở màn hình tạo nhân vật có ô nhập TÊN (2–14 ký tự, chữ/số/dấu cách, không ký tự đặc biệt gây lỗi; kiểm tra trùng tên trong cùng máy/danh sách và báo rõ nếu trùng). Tên hiển thị trên đầu nhân vật trong game, ở panel nhân vật và ở danh sách chọn nhân vật.
- NHIỀU NHÂN VẬT / NHIỀU ACC: một máy có NHIỀU Ô NHÂN VẬT (tối thiểu 3 ô): mỗi ô là một nhân vật riêng với tiến trình riêng (phái, giới tính, tên, cấp, trang bị, ngọc, vàng, map đã mở, điểm thân thể/skill) — không lẫn dữ liệu giữa các nhân vật. Màn hình đầu game KHÔNG còn bảng danh sách ô nhân vật ở ngoài (Do chốt 2026-11-27): sau màn load/giới thiệu, vào THẲNG sân khấu tạo nhân vật 3 phái để chọn phái/giới tính/nhập tên rồi Vào game. Nhân vật ĐÃ LƯU chơi tiếp qua nút nhỏ "Nhân vật đã lưu" ở góc trên sân khấu — CHỈ hiện khi có nhân vật đã lưu — ấn vào mới mở danh sách ô để Chơi tiếp / tạo mới ở ô trống / xoá nhân vật (xác nhận 2 bước, tránh xoá nhầm); đã đủ 3 ô thì nút Vào game báo đã đầy và hướng sang nút "Nhân vật đã lưu". Mỗi người chơi cầm máy khác nhau thì dữ liệu nằm trên máy của họ; bản online/đăng nhập tài khoản đồng bộ nhiều máy để ở giai đoạn sau (kiến trúc lưu phải tách theo từng nhân vật ngay từ đầu để sau gắn tài khoản không phải làm lại).
- Lưu tự động theo từng nhân vật (khi lên cấp, nhặt/đổi đồ, qua map, thoát game) + có dấu thời gian chơi gần nhất ở danh sách chọn nhân vật.
- CÀI ĐẶT (Settings) — có màn hình riêng, mở được từ màn hình chính và trong game, lưu lại theo máy:
  - HÌNH ẢNH: chất lượng đồ hoạ Cao / Trung bình / Thấp (Thấp = giảm hạt hiệu ứng + tắt bóng để máy yếu không lag), bật/tắt hiệu ứng skill, bật/tắt rung màn hình khi trúng đòn lớn, hiện/tắt số sát thương.
  - ÂM THANH: nhạc nền (trượt âm lượng + bật/tắt riêng), âm thanh hiệu ứng/skill (trượt âm lượng + bật/tắt riêng), tắt toàn bộ tiếng.
  - KHÁC: bật/tắt rung (nếu thiết bị hỗ trợ), ngôn ngữ hiển thị để sẵn khung (hiện tại tiếng Việt).
  - Cài đặt áp dụng ngay khi đổi, không cần khởi động lại; nút Đặt lại mặc định.

## 3. Chiến đấu
- CẢ HAI chế độ: đánh tay (joystick + nút đánh + 4 nút skill) và AUTO (tự tìm quái, tự đánh, tự dùng skill khi hồi chiêu xong), có nút bật/tắt AUTO.
- Có mất máu thật hai chiều: quái đánh trúng → nhân vật trừ HP (số sát thương hiện rõ, thanh HP giảm); nhân vật đánh trúng → quái trừ HP. HP về 0: nhân vật thua/hồi sinh theo quy định, quái chết → rơi EXP/vàng/đồ.
- Chỉ số: HP, mana, tấn công, phòng thủ, chí mạng, tốc độ. EXP lên cấp tăng chỉ số.

## 4. Quái và boss (phong phú hình dáng LẪN skill/cách đánh)
- Nhiều họ quái theo khu vực map, mỗi họ hình riêng. Ví dụ: rừng — slime, goblin, sói; hang tối — dơi bay, nhện, xương khô; các khu sau mở thêm họ mới.
- Hành vi đa dạng: cận chiến lao vào; bắn xa giữ khoảng cách; bay; tank chậm máu trâu; nhanh yếu đi theo bầy; phun độc/làm chậm; hỗ trợ hồi máu cho đồng đội.
- Boss: có 2–3 skill riêng (triệu hồi lính, sát thương diện rộng, lao húc), xuống <50% HP thì đổi phase, khó hơn.
- Dữ liệu quái/skill quái nằm ở lớp cấu hình riêng: thêm họ quái mới = thêm dữ liệu + hình, không sửa engine.
- QUÁI MẠNH DẦN THEO CẤP VÀ MAP (bổ sung 2026-11-27): chỉ số quái (HP, tấn công, phòng thủ, tốc độ) tăng theo dải cấp của map và theo hệ số riêng từng map ở lớp dữ liệu; map sau quái mạnh hơn hẳn map trước, có biến thể tinh anh (elite: to hơn, viền khác, máu/sát thương cao hơn, tỉ lệ rơi đồ xịn cao hơn). Độ khó phải bám sát sức mạnh nhân vật cùng cấp — không quá dễ gây chán, không quá khó gây nản (cân bằng ở giai đoạn 2 theo góp ý của Do).

## 5. Trang bị — nâng cấp VÀ khảm (bổ sung 2026-11-27)
- Rơi từ quái/boss với độ hiếm: Thường / Hiếm / Sử thi / Huyền thoại. Các ô: vũ khí, áo giáp, giày, nhẫn (mở rộng sau được).
- Túi đồ: mặc, so sánh chỉ số trước/sau, bán đồ thừa.
- NÂNG CẤP: trang bị nâng bằng vàng/nguyên liệu (+1, +2, +3...), mỗi cấp + tăng chỉ số của món đó; tỉ lệ/công thức ở lớp dữ liệu.
- KHẢM NGỌC (socket): trang bị có số lỗ khảm theo độ hiếm (đồ càng hiếm càng nhiều lỗ, tối đa 3). Ngọc rơi từ quái/boss hoặc ghép từ ngọc cấp thấp; khảm vào để cộng chỉ số, tháo ra được (có thể tốn phí nhỏ). Các loại ngọc mẫu: Ngọc Đỏ +% sát thương, Ngọc Tím +% chí mạng, Ngọc Lục +% HP, Ngọc Vàng +% né tránh / +% tốc độ, Ngọc Lam +% phòng thủ. Ngọc cũng nâng cấp/ghép lên cấp cao hơn được.
- CHỈ SỐ THEO PHẦN TRĂM (áp dụng cho cả skill phụ, trang bị và ngọc): nhiều hiệu ứng tính bằng % thay vì số cố định — +% dame, +% né, +% tốc độ chạy, +% tốc đánh, +% HP, +% chí mạng... Công thức thống nhất ở engine: Chỉ số cuối = Chỉ số gốc × (1 + tổng % cộng dồn) + cộng thẳng; hiển thị rõ trong panel nhân vật từng nguồn % đến từ đâu (skill / đồ / ngọc) để người chơi tính toán được. Nhờ % nên càng về cấp cao các hiệu ứng này càng đáng giá, không bị lỗi thời.
- BOSS CÀNG MẠNH, ĐỒ HIẾM CÀNG DỄ RƠI: bảng tỉ lệ rơi (drop table) theo bậc boss ở lớp dữ liệu — boss map sau/bậc cao hơn có tỉ trọng Sử thi/Huyền thoại cao hơn hẳn boss yếu; boss luôn đảm bảo rơi ít nhất 1 món từ Hiếm trở lên, lần đầu hạ mỗi boss (first kill) thưởng thêm tỉ lệ đồ xịn. Quái tinh anh cũng theo nguyên tắc này ở mức thấp hơn.

## 6. Map, tương tác và VA CHẠM (yêu cầu cứng)
- Nhân vật TƯƠNG TÁC được với map, không phải nền trang trí: vật cản (cây, đá, tường, nhà) là vật thể thật.
- Hệ thống va chạm (collision) bắt buộc:
  - Nhân vật và quái KHÔNG đi xuyên vật cản, KHÔNG đi xuyên nhau, KHÔNG ra khỏi biên map.
  - Không kẹt: khi trượt theo cạnh vật cản phải di chuyển mượt (sliding), quái có tìm đường vòng đơn giản khi bị chặn, không đứng rung tại chỗ.
  - Đòn đánh/skill cũng theo va chạm: đánh trúng chỉ khi trong tầm + đúng hướng; đạn/skill bay trúng vật cản thì dừng.
- Map có lớp nền xa/gần tạo chiều sâu, mỗi khu vực một phong cách/màu riêng.

## 6b. Nhiều map (bổ sung 2026-11-27)
- Game phải có NHIỀU map cho phong phú, mở khoá dần theo cấp/điều kiện qua map trước; mỗi map: nền + phong cách riêng, họ quái riêng, boss riêng, dải cấp riêng. Danh sách dự kiến (tên/cấp có thể cân chỉnh ở lớp dữ liệu):
  1. Rừng Xanh (Lv1–10) — slime, goblin, sói; boss Chúa Sói.
  2. Hang Tối (Lv10–20) — dơi, nhện độc, xương khô; boss Nhện Chúa.
  3. Đầm Lầy Độc (Lv20–30) — quái độc, bùn; boss Đầm Chúa.
  4. Sa Mạc Cát (Lv30–40) — bọ cạp, xác ướp; boss Pharaoh.
  5. Núi Lửa (Lv40–50) — quỷ lửa, golem dung nham; boss Rồng Lửa Nhỏ.
  6. Băng Nguyên (Lv50–60) — sói băng, yêu tuyết; boss Golem Băng.
  7. Lâu Đài Bóng Đêm (Lv60+) — kỵ sĩ hắc ám, ma cà rồng; boss Chúa Quỷ (trùm cuối hiện tại, mở rộng tiếp về sau).
- Bản mẫu giai đoạn 1 làm trọn 1–2 map đầu + khung chọn map hiển thị các map sau (khoá/mở theo cấp), các map còn lại thêm ở giai đoạn 2 theo đúng khung này, không sửa engine.

## 6c. Camera và cách di chuyển (chốt 2026-11-27 khi Do hỏi; Do đổi sang NGANG cùng ngày)
- MÀN HÌNH NGANG (landscape) — Do đã chọn đổi từ dọc sang ngang (2026-11-27 21:01): khung hình rộng, nhìn map thoáng hơn; điều khiển 2 tay — joystick góc dưới trái, cụm nút đánh/skill góc dưới phải, HUD gọn ở các cạnh không che giữa màn hình.
- KHÓA NGANG TOÀN BỘ (Do chốt 2026-11-27): mở game mà máy đang DỌC thì lớp phủ "Xoay ngang máy để chơi" phủ kín NGAY TỪ MÀN HÌNH ĐẦU TIÊN — gồm cả màn load/giới thiệu và màn chọn/tạo nhân vật — xoay ngang mới dùng được. KHÔNG còn ngoại lệ "màn chọn nhân vật để dọc vẫn dùng bình thường" như bản trước; một cơ chế nhắc xoay ngang duy nhất cho mọi màn hình.
- Góc nhìn từ trên xuống hơi nghiêng (top-down 2.5D): thấy mặt đất, vật thể có chiều cao, nhân vật đứng trước/sau vật thể đúng chiều sâu.
- Di chuyển TỰ DO 8 HƯỚNG (lên, xuống, trái, phải và cả 4 hướng chéo) bằng joystick ảo — KHÔNG phải game đi dọc màn hình tự cuộn, KHÔNG phải đi ngang side-scroll chỉ trái/phải.
- Map RỘNG HƠN màn hình: CAMERA BÁM THEO nhân vật — nhân vật ở gần giữa khung hình, map cuộn theo khi di chuyển. Camera bám mượt (có độ trễ/lerp nhẹ, nhìn lệch nhẹ về phía đang chạy), tới biên map thì camera dừng lại, KHÔNG lộ vùng đen ngoài map.
- AUTO cũng dùng cùng hệ di chuyển + camera này (camera vẫn bám theo nhân vật khi auto chạy).
- MAP NHỎ (minimap) ở góc trên phải (Do yêu cầu 2026-11-27): khung bán trong suốt, hiển thị toàn cảnh map thu nhỏ — chấm nhân vật (sáng, ở giữa theo vị trí thật), chấm đỏ quái thường, chấm lớn/biểu tượng riêng cho quái tinh anh và boss, vị trí cổng ra/vào map và vật phẩm rơi chưa nhặt (chấm vàng). Chạm vào minimap thì phóng to thành bản đồ lớn giữa màn hình (tạm dừng di chuyển), chạm lần nữa đóng lại. Minimap cập nhật theo nhịp thưa (khoảng 5–10 lần/giây) chứ không vẽ lại mỗi khung hình, để không gây lag.

## 6d-bis. HUD V2 — bố cục CHUẨN MỚI, thay thế mọi bố cục HUD cũ (Do chốt 2026-11-27 qua bộ Fantasy RPG V2; file chuẩn: HUD_V2.md trong thư mục dự án)
- BỎ dock icon dưới màn hình và bố cục dock cũ. Thay bằng **5 icon TRÒN ở phía trên bên phải, ngay bên trái minimap**, thứ tự: **Nhân vật, Túi đồ, Trang bị, Kỹ năng, Cài đặt**. Bản đồ lớn mở bằng cách **chạm vào minimap** (không còn icon Bản đồ riêng).
- Icon: nền tối bán trong suốt, **viền vàng cổ**, biểu tượng rõ, **không có chữ bên dưới**; hiển thị 36–40 CSS px, vùng chạm tối thiểu 44×44 CSS px, không chồng vùng chạm; sáng nhẹ khi đang chọn, chấm đỏ khi có thông báo.
- Giữ nguyên: HP/MP trên trái, joystick dưới trái, đánh thường + 4 skill dưới phải, EXP sát mép dưới. Safe area cả hai chiều ngang; màn hình hẹp thì co khoảng cách/gom menu phụ, không thu nhỏ vùng chạm dưới chuẩn.
- Mặc định **đóng tất cả panel** — không panel thường trực che khu vực chiến đấu. Chạm icon mở panel tương ứng; chạm lại / nút ✕ / chạm ngoài thì đóng; chạm icon khác chuyển panel trực tiếp, chỉ 1 panel mở tại một thời điểm (minimap mở bản đồ lớn cũng theo quy tắc này).
- Mở panel (offline): **tạm dừng chiến đấu + AUTO**, xóa input joystick đang giữ; đóng panel thì khôi phục trạng thái trước đó, không tự bật AUTO nếu trước đó đang tắt. Chạm trên panel không truyền xuống sân chơi. Không reload trang.
- Kỹ thuật: dùng PanelManager/UIManager chung (registry icon/panel, quản lý focus, pause, safe area) — không sửa logic chiến đấu riêng cho từng panel.
- Nghiệm thu HUD V2: 5 icon đúng vị trí; không còn dock dưới; mỗi icon mở đúng panel; chuyển panel không chồng; ✕/chạm ngoài/chạm lại đóng được; minimap mở bản đồ lớn; pause/resume đúng; không đánh nhầm; kiểm tra iPhone ngang hai chiều + màn hình hẹp. Nếu Concept.png khác bố cục thì HUD V2 thắng; các yêu cầu khác vẫn theo SPEC gốc.

## 6d. Giao diện trong game — góp ý của Do sau test bản mẫu (2026-11-27, yêu cầu cứng cho mọi bản sau; riêng phần vị trí dock icon đã được mục 6d-bis HUD V2 thay thế)
- TOÀN MÀN HÌNH: game phải mở FULL màn hình ngang (dùng hết diện tích hiển thị, hỗ trợ nút bật toàn màn hình / nhắc xoay ngang khi cần, chừa đúng vùng an toàn tai thỏ) — không để khung game nhỏ lọt giữa màn hình.
- ICON NHỎ GỌN DẠNG DOCK: các chức năng Nhân vật, Túi đồ, Trang bị, Bản đồ, Cài đặt... chỉ là các ICON NHỎ GỌN xếp gọn một cụm ở cạnh màn hình, không bày panel to che sân chơi.
- PANEL DẠNG POPUP: ấn icon thì panel tương ứng HIỆN LÊN giữa màn hình (kích thước vừa phải, nền mờ phía sau), và panel nào cũng có NÚT X NHỎ ở góc để đóng nhanh; ấn ra ngoài panel hoặc ấn lại icon cũng đóng được. Chỉ mở 1 panel tại một thời điểm.
- HÌNH NHÂN VẬT PHẢI ĐẸP: góp ý test lần 1 — hình nhân vật bản mẫu chưa đẹp, phải nâng chất lượng sprite/chân dung nhân vật (và giữ đồng bộ quái/map/skill) ở mức Fantasy chỉn chu, không chấp nhận hình vẽ thô/đơn giản.

## 7. Hiệu năng — KHÔNG LAG (yêu cầu cứng)
- Mục tiêu chạy mượt trên iPhone: giới hạn số quái hiển thị cùng lúc, quái ở xa không hoạt động thì ngủ (không tính toán mỗi khung hình).
- Hiệu ứng skill dùng hạt (particle) có giới hạn số lượng, tự dọn sau khi kết thúc; không tạo rò rỉ bộ nhớ khi chơi lâu/chuyển map.
- Hình ảnh nén nhẹ, tải theo map cần dùng; vòng lặp game dùng delta-time để tốc độ ổn định bất kể khung hình.
- Sau mỗi lần sửa phải tự kiểm tra: chơi liên tục, chuyển map, bật AUTO lâu — không giật, không chậm dần.

## 8. Bố cục code (để sửa nhanh, không sót)
- Lớp DỮ LIỆU (cấu hình riêng, sửa cân bằng không đụng engine): quái, boss, trang bị, tỉ lệ rơi, skill (nhân vật + quái), map/level, công thức nâng cấp.
- Lớp ENGINE (module riêng từng chức năng): chiến đấu, va chạm/tìm đường, skill + hiệu ứng, trang bị/túi đồ, lưu tiến trình.
- Lớp GIAO DIỆN: màn hình tạo nhân vật, HUD (HP/mana/EXP), joystick + nút skill, panel nhân vật/túi đồ, panel "Kế hoạch & Lộ trình".
- Lưu tiến trình: level, phái, giới tính, trang bị, vàng, map đã mở — lưu trên máy, mở lại chơi tiếp; khoá/lỗi lưu không được làm mất trắng tiến trình.

## 9. Lộ trình
- Giai đoạn 1 (bản mẫu): trọn vòng chơi — tạo nhân vật 3 phái × Nam/Nữ, đánh tay + AUTO, 4 skill/phái, quái nhiều họ + boss, va chạm map, rơi đồ + nâng cấp, 1–2 map đầu, lưu tiến trình.
- Giai đoạn 2: Do chơi thử góp ý → cân bằng lại, thêm map/boss/họ quái.
- Giai đoạn 3: hoàn thiện đồ hoạ/âm thanh → deploy Cloudflare, icon Màn hình chính.

## 10. Checklist nghiệm thu mỗi bản (tick trước khi bàn giao)
- [ ] Tạo được nhân vật cả 3 phái, cả Nam và Nữ; vào game đúng ngoại hình đã chọn
- [ ] Đặt được tên nhân vật (báo lỗi khi trùng/quá ngắn/quá dài); tên hiện trên đầu nhân vật và ở danh sách chọn
- [ ] Tạo được nhiều nhân vật ở các ô khác nhau, tiến trình từng nhân vật riêng và không lẫn nhau; xoá nhân vật phải xác nhận
- [ ] Màn hình Cài đặt đổi được chất lượng hình ảnh + hiệu ứng và âm lượng nhạc/hiệu ứng riêng, áp dụng ngay và còn nguyên sau khi mở lại game
- [ ] Đánh tay và AUTO đều hoạt động, chuyển qua lại không lỗi
- [ ] 4 skill của phái đã chọn dùng được, có hồi chiêu/mana, hiệu ứng hiện rõ
- [ ] Skill phụ của phái hoạt động đúng (chủ động + bị động), nâng cấp bằng điểm skill được
- [ ] Lên cấp nhận điểm thân thể + điểm skill, cộng vào là chỉ số/skill mạnh lên thấy rõ
- [ ] Quái ở map sau mạnh hơn map trước đúng dải cấp; có quái tinh anh
- [ ] Màn hình chọn map hiện đủ các map, khoá/mở đúng theo cấp
- [ ] Quái đánh trúng làm nhân vật mất HP; nhân vật chết có xử lý; quái chết rơi EXP/vàng/đồ
- [ ] Không đi xuyên vật cản/biên map/quái khác; không kẹt khi trượt cạnh vật cản
- [ ] Nhặt đồ, mặc đồ (chỉ số thay đổi), nâng cấp đồ thành công
- [ ] Khảm ngọc vào đồ có lỗ được, tháo ra được, chỉ số % thay đổi đúng công thức và hiện rõ nguồn %
- [ ] Hạ boss bậc cao cho tỉ lệ đồ Sử thi/Huyền thoại cao hơn boss yếu; boss luôn rơi ít nhất 1 món Hiếm+
- [ ] Boss dùng skill riêng và đổi phase ở <50% HP
- [ ] Chơi + AUTO liên tục không lag dần, chuyển map không lỗi
- [ ] Tắt mở lại: tiến trình còn nguyên
- [ ] Game mở full màn hình ngang; các chức năng Nhân vật/Túi/Trang bị/Cài đặt là icon nhỏ gọn, ấn mở popup có nút X nhỏ để đóng, không che sân chơi khi đóng
