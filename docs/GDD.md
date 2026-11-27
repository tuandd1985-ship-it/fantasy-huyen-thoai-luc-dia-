# DESIGN V2 — FANTASY: HUYỀN THOẠI LỤC ĐỊA
Bản thiết kế đầy đủ Do chuyển cho Luna ngày 2026-11-27, BỔ SUNG và làm chi tiết cho SPEC.md (SPEC gốc vẫn hiệu lực; khi trùng lặp, số liệu cụ thể trong file này là chuẩn cân bằng ban đầu). Định hướng: Action RPG Fantasy 2.5D, cảm hứng Diablo Immortal / MU Online / Ragnarok nhưng thế giới và nhân vật riêng. Mục tiêu: cảm giác game nhập vai thật, không phải trang web có nhân vật di chuyển đánh quái đơn giản.
Lưu ý: các ảnh nhắc trong bản gốc (chân dung phái, sơ đồ HUD, panel trang bị, boss, bảng rơi đồ, mô phỏng công thức) là HÌNH THAM KHẢO PHONG CÁCH, không đính kèm trong tin nhắn — Luna tự xây dựng giao diện + tài nguyên đồ họa riêng, đồng bộ với nhau.

## I. Tổng thể
- Tên game: FANTASY — HUYỀN THOẠI LỤC ĐỊA
- Thể loại: Action RPG Fantasy. Nền tảng: iPhone, Android, trình duyệt PC.
- Màn hình ngang toàn màn hình; góc nhìn top-down 2.5D; di chuyển tự do 8 hướng.
- Đồ họa: Fantasy trung cổ, bán hiện thực. Chiến đấu thời gian thực, đánh tay + AUTO.
- Cấp độ ban đầu Lv1–70. 3 phái, 6 ngoại hình, 7 khu vực. Ngôn ngữ tiếng Việt (khung mở rộng). Máy chủ Cloudflare ở giai đoạn triển khai.

## II. Nhân vật và hình ảnh
- Kiếm Sĩ (Warrior): giáp nặng, kiếm lớn, HP cao, phòng thủ tốt; cấp cao giáp thêm hoa văn, ánh sáng, hiệu ứng năng lượng. Nam + Nữ.
- Pháp Sư (Mage): sát thương phép lớn, diện rộng; hiệu ứng lửa, băng, sấm sét, năng lượng ma thuật. Nam + Nữ.
- Cung Thủ (Archer): tốc độ cao, đánh xa, chí mạng lớn, né tránh, di chuyển linh hoạt. Nam + Nữ.
- Mỗi nhân vật có bộ animation riêng: đứng yên, chạy, đánh thường, thi triển 4 skill, nhận sát thương, tử vong, hồi sinh.
- TRANG BỊ THAY ĐỔI NGOẠI HÌNH THẬT: mặc đồ gì thì hình nhân vật đổi theo (kiếm thường → kiếm huyền thoại thì vũ khí trên tay đổi hình), không chỉ tăng chỉ số.

## III. HUD màn hình chiến đấu (ngang)
- Trên trái: chân dung, tên, cấp, HP, mana. Trên giữa: tên map, thông báo boss. Trên phải: minimap.
- Bên trái: nhiệm vụ thu gọn. Dưới trái: joystick. Dưới phải: đánh thường + 4 skill chính. Gần cụm skill: skill phụ, bình HP/MP, AUTO.
- Dưới giữa: dock icon chức năng. Mép dưới: thanh EXP.
- HUD tự thích ứng kích thước iPhone, tránh tai thỏ; đóng hết popup thì phần lớn màn hình là sân chơi.

## IV. Các màn hình chức năng (10)
1. Chọn nhân vật: 3 ô, mô hình, tên, cấp, phái, thời gian chơi gần nhất; nút Chơi tiếp / Tạo mới / Xóa.
2. Tạo nhân vật: chọn phái, giới tính, xem ngoại hình + đặc điểm chiến đấu, nhập tên, animation xem trước.
3. Nhân vật và trang bị: nhân vật giữa, ô trang bị xung quanh; lực chiến, HP, tấn công, phòng thủ, chí mạng, né, điểm thân thể chưa cộng.
4. Túi đồ: lưới vật phẩm, phân loại độ hiếm, lọc theo phái, sắp xếp, khóa đồ quý, so sánh chỉ số, bán hàng loạt.
5. Cây kỹ năng: tách skill chính/phụ; cấp hiện tại, cấp tiếp theo, sát thương, mana, hồi chiêu, điểm cần nâng.
6. Lò rèn: nâng cấp trang bị, chỉ số trước/sau, nguyên liệu, vàng, tỷ lệ thành công, hiệu ứng khi thành công.
7. Khảm ngọc: chọn trang bị, xem lỗ, chọn ngọc, tháo ngọc, ghép ngọc cấp cao.
8. Bản đồ thế giới: 7 khu vực, cấp yêu cầu, boss, vật phẩm có thể rơi, trạng thái mở khóa.
9. Cửa hàng NPC: bình máu/mana, nguyên liệu, trang bị cơ bản, bán vật phẩm.
10. Cài đặt: chất lượng đồ họa, âm thanh, hiệu ứng skill, rung màn hình, số sát thương, ngôn ngữ, thiết lập AUTO.

## V. Skill cụ thể (số liệu ban đầu — BẮT BUỘC để trong file cấu hình, chỉnh không sửa engine)
### Kiếm Sĩ
- Lv1 Trảm Kiếm: 180% sát thương, CD 3s, mana 10.
- Lv8 Kiếm Vũ: xoay kiếm diện rộng 250%, CD 7s, mana 20.
- Lv15 Địa Chấn: 350%, choáng quái thường 2s, CD 12s, mana 35.
- Lv25 Thiên Kiếm: đại kiếm diện rộng 650%, CD 25s, mana 60.
- Phụ: Lá Chắn Thép (chủ động, giảm 25% sát thương nhận); Cuồng Nộ (chủ động, +30% tốc đánh 8s); Hút Máu (bị động, hồi 5% sát thương gây ra); Thể Chất Thép (bị động, +10% HP tối đa).
### Pháp Sư
- Lv1 Hỏa Cầu: 200%, CD 3s, mana 15.
- Lv8 Băng Phong: diện rộng 260%, làm chậm 40%, CD 8s, mana 25.
- Lv15 Lôi Đình: sét nhiều mục tiêu 380%, CD 12s, mana 40.
- Lv25 Thiên Thạch: diện rộng 750%, CD 28s, mana 70.
- Phụ: Lá Chắn Mana (chủ động, mana hấp thụ sát thương); Hồi Mana Nhanh (chủ động, hồi 25% mana); Khuếch Đại Phép (bị động, +12% sát thương phép); Ma Lực Vô Tận (bị động, +15% mana tối đa).
### Cung Thủ
- Lv1 Xuyên Tiễn: xuyên mục tiêu 170%, CD 3s, mana 10.
- Lv8 Liên Tiễn: nhiều mũi tên, tổng tối đa 300%, CD 6s, mana 20.
- Lv15 Độc Tiễn: trực tiếp 200% + độc theo thời gian, CD 10s, mana 30.
- Lv25 Vạn Tiễn: mưa tên diện rộng, tổng tối đa 650%, CD 24s, mana 55.
- Phụ: Né Tránh (bị động, +8% né); Bước Chân Gió (chủ động, +30% tốc chạy và tốc đánh); Dấu Ấn Yếu Điểm (chủ động, tăng chí mạng lên mục tiêu); Mắt Đại Bàng (bị động, +10% tầm đánh).

## VI. 7 map (mỗi map: khu an toàn, NPC, cổng dịch chuyển, vùng quái thường, vùng tinh anh, khu boss, địa điểm bí mật)
1. Rừng Xanh Lv1–10: rừng, sông suối, cầu gỗ, phế tích. Quái: Slime, Goblin, Sói, Goblin cung thủ. Boss: Chúa Sói.
2. Hang Tối Lv10–20: hang đá, tinh thể phát sáng, đường hầm. Quái: Dơi, Nhện độc, Xương khô. Boss: Nhện Chúa.
3. Đầm Lầy Độc Lv20–30: nước độc, cây chết, sương mù. Quái: Quái bùn, Rắn độc, Pháp sư đầm lầy. Boss: Đầm Chúa.
4. Sa Mạc Cát Lv30–40: kim tự tháp, đền cổ, bão cát. Quái: Bọ cạp, Xác ướp, Vệ binh cổ đại. Boss: Pharaoh.
5. Núi Lửa Lv40–50: dung nham, cầu đá, thành trì lửa. Quái: Quỷ lửa, Golem dung nham. Boss: Rồng Lửa.
6. Băng Nguyên Lv50–60: núi tuyết, hồ băng, đền băng. Quái: Sói băng, Yêu tuyết, Vệ binh băng. Boss: Golem Băng.
7. Lâu Đài Bóng Đêm Lv60–70: lâu đài cổ, nghĩa địa, hầm ngục. Quái: Kỵ sĩ hắc ám, Ma cà rồng, Ác quỷ. Boss: Chúa Quỷ.

## VII. Boss (không phải quái phóng to: cơ chế + animation riêng + cảnh báo vùng nguy hiểm trước khi tung skill)
- Chúa Sói: lao húc, gầm choáng, triệu hồi đàn sói.
- Nhện Chúa: phun độc, giăng tơ, triệu hồi nhện con.
- Đầm Chúa: vũng độc, đập đất, hồi phục.
- Pharaoh: bão cát, lời nguyền, triệu hồi xác ướp.
- Rồng Lửa: phun lửa, đập cánh, mưa dung nham.
- Golem Băng: đóng băng, bão tuyết, giáp băng.
- Chúa Quỷ: kiếm hắc ám, triệu hồi quỷ, vùng hủy diệt.
- HP <50%: chuyển phase — đổi màu, tăng độ khó, mở thêm hành vi.

## VIII. Trang bị
- Giai đoạn hoàn thiện mở rộng lên 10 ô trang bị (bản đầu 4 ô theo SPEC, mở rộng dần).
- Độ hiếm: Thường (chỉ số cơ bản, 0 lỗ), Hiếm (chỉ số bổ sung, 1 lỗ), Sử thi (nhiều thuộc tính đặc biệt, 2 lỗ), Huyền thoại (thuộc tính mạnh, 3 lỗ).
- Trang bị theo cấp phải đẹp dần rõ rệt (vd kiếm: Lv1 Kiếm Sắt → Lv20 Kiếm Băng → Lv40 Hỏa Kiếm → Lv60 Thần Kiếm).
- Hiệu ứng nâng cấp: từ +7 bắt đầu phát sáng, +10 có hào quang, +15 có hiệu ứng đặc biệt.
- Tỷ lệ rơi boss: bảng riêng cho món Hiếm+ đảm bảo rơi từ boss; vật phẩm rơi bổ sung dùng bảng tỷ lệ riêng (bảng chi tiết trong bản gốc dạng hình — áp dụng nguyên tắc SPEC: boss càng mạnh tỉ lệ Sử thi/Huyền thoại càng cao, boss luôn rơi ít nhất 1 món Hiếm+).

## IX. Ngọc (5 loại: Đỏ tấn công, Tím chí mạng, Lục HP, Vàng tốc độ, Lam phòng thủ)
- Cấp 1 +2% (rơi từ quái); Cấp 2 +4% (3 viên cấp 1); Cấp 3 +7% (3 viên cấp 2); Cấp 4 +11% (3 viên cấp 3); Cấp 5 +16% (3 viên cấp 4); Cấp 6 +22% (3 viên cấp 5); Cấp 7 +30% (3 viên cấp 6).
- GIỚI HẠN CÂN BẰNG (caps) riêng cho chí mạng, né tránh và tốc đánh — tránh bất tử/đánh nhanh vô hạn. Caps để trong file cấu hình.

## X. Phát triển nhân vật
- Chỉ số khởi đầu: Kiếm Sĩ HP 350 / Mana 100 / ATK 35 / DEF 25 / Crit 5% / Né 3% / Tốc đánh 1.0. Pháp Sư HP 200 / Mana 220 / ATK 48 / DEF 10 / Crit 7% / Né 5% / 0.8. Cung Thủ HP 260 / Mana 150 / ATK 40 / DEF 15 / Crit 12% / Né 10% / 1.3.
- Mỗi cấp: +5 điểm thân thể, +2 điểm skill, ngoài chỉ số tự tăng theo cấp.
- Công thức: Chỉ số cuối = Chỉ số gốc × (1 + tổng % cộng dồn) + chỉ số cộng thẳng. Ví dụ mô phỏng trong bản gốc: gốc 1000, đồ +30%, skill phụ +20%, ngọc +15%, cộng thẳng +100 → 1750.

## XI. Cốt truyện và nhiệm vụ
- Cốt truyện: Lục địa được bảo vệ bởi 7 viên đá nguyên tố; Chúa Quỷ phá phong ấn, các vùng đất bị xâm chiếm. Người chơi từ một ngôi làng nhỏ, đánh bại thủ lĩnh từng vùng, thu hồi từng viên đá, mở đường đến lâu đài cuối.
- Loại nhiệm vụ: chính tuyến (hạ Chúa Sói mở Hang Tối), phụ tuyến (diệt 30 Goblin), thu thập (10 tinh thể), hằng ngày (diệt 100 quái), hằng tuần (hạ 5 boss), khám phá (rương bí mật), thành tựu (nâng đồ đầu tiên lên +10), thử thách (hạ boss không dùng bình máu).

## XII. NPC và thành phố trung tâm (khu an toàn, không quái)
Trưởng làng (nhiệm vụ chính), Thợ rèn (nâng cấp), Thợ kim hoàn (khảm/ghép ngọc), Thương nhân (mua bán), Dược sư (bình HP/mana), Thầy kỹ năng (nâng cấp skill), Người dịch chuyển (đi map), Thủ kho (cất đồ), Người săn boss (nhiệm vụ/thông tin boss).

## XIII. Mở rộng sau (kiến trúc phải chừa sẵn, không làm tất cả ngay)
- Giai đoạn 2: Pet đồng hành hỗ trợ nhặt đồ, Set Item, phụ bản nhiều tầng, tháp vô tận, thành tựu + danh hiệu.
- Giai đoạn 3: thú cưỡi, đồng bộ tài khoản nhiều máy.
- Giai đoạn 4: bảng xếp hạng online, bang hội, multiplayer, PvP, giao dịch giữa người chơi.

## XIV. Kiến trúc source (theo bản gốc, chi tiết bị cắt ở cuối tin nhắn — áp dụng bố cục 3 lớp của SPEC mục 8)
Nguyên tắc: tách dữ liệu/engine/giao diện để nâng cấp tính năng này không phát sinh lỗi ở tính năng khác; mọi thông số cân bằng nằm ở file cấu hình.
