# ROADMAP — FANTASY: HUYỀN THOẠI LỤC ĐỊA
Kế hoạch triển khai. SPEC.md ưu tiên cao nhất. Mỗi giai đoạn: đọc SPEC + PROGRESS → xác định phạm vi/module/tiêu chí nghiệm thu → checkpoint → làm → test + regression → cập nhật PROGRESS/TEST_REPORT/CHANGELOG → Do nghiệm thu.

## Giai đoạn 0 — Nền móng tài liệu và đối chiếu (ĐANG LÀM, 2026-11-27)
- Bộ tài liệu 9 file + GAP_ANALYSIS. Đối chiếu bản game hiện tại với SPEC/GDD. Chờ Do phê duyệt kế hoạch này trước khi thay đổi lớn.

## Giai đoạn 1 — CHUẨN CHẤT LƯỢNG: màn hình chiến đấu + Rừng Xanh (ưu tiên theo Master Instruction mục 9)
- Thiết kế lại HUD chiến đấu đúng sơ đồ GDD, toàn màn hình ngang, dock icon + popup ✕ (đã có khung từ vòng sửa trước — nâng lên chuẩn).
- Rừng Xanh chất lượng cao làm chuẩn: map chi tiết (sông, cầu gỗ, phế tích), 4 họ quái (Slime, Goblin, Sói, Goblin cung thủ) với sprite + animation riêng, boss Chúa Sói đủ 3 skill + cảnh báo vùng nguy hiểm + phase <50%.
- 1 nhân vật mẫu (Kiếm Sĩ Nam) đủ bộ animation chuẩn ART_DIRECTION + trang bị đổi ngoại hình (vũ khí).
- Trình bản xem trước → Do duyệt phong cách → mới nhân rộng.

## Giai đoạn 2 — Nhân rộng nội dung theo chuẩn
- Đủ 6 biến thể nhân vật + animation; 7 map + 7 boss theo GDD; nhiệm vụ chính/phụ + cốt truyện 7 viên đá; thành phố NPC (9 NPC); 10 màn hình chức năng hoàn chỉnh; mở rộng 10 ô trang bị; cân bằng toàn cục (caps ngọc/chỉ số).

## Giai đoạn 3 — Triển khai Cloudflare + lưu trữ thật
- Chuyển STORAGE sang Cloudflare (Preview → Production, version + rollback), PWA/icon màn hình chính, kiểm thử trên iPhone thật. Đồng bộ tài khoản nhiều máy (theo GDD giai đoạn 3 của tính năng mở rộng).

## Giai đoạn 4 — Tính năng mở rộng (theo GDD mục XIII)
- GĐ2 tính năng: pet nhặt đồ, set item, phụ bản nhiều tầng, tháp vô tận, thành tựu/danh hiệu. GĐ3: thú cưỡi. GĐ4: xếp hạng online, bang hội, multiplayer, PvP, giao dịch — chỉ làm khi các giai đoạn trước ổn định và Do duyệt từng mục (PROPOSED).
