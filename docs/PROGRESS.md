# PROGRESS — FANTASY: HUYỀN THOẠI LỤC ĐỊA
Cập nhật: 2026-11-28 (sau bản v0.4.0 — đợt tích hợp asset).

## Đã xong
- SPEC.md (yêu cầu gốc, Do phê duyệt dần qua các vòng chốt 2026-11-27) + GDD.md (bản thiết kế v2) + bộ tài liệu Master Instruction: ART_DIRECTION, ARCHITECTURE, BALANCE, ROADMAP, GAP_ANALYSIS, TEST_REPORT, CHANGELOG.
- Bản mẫu chơi được (web tĩnh): tạo nhân vật 3 ô/đặt tên/3 phái × Nam-Nữ, chiến đấu tay + AUTO, lên cấp + điểm thân thể/skill, rơi/mặc/nâng cấp đồ, khảm ngọc (code), 7 map khung, minimap, va chạm, cài đặt, panel Lộ trình. Chi tiết kiểm chứng: TEST_REPORT.md.
- Vòng sửa theo test lần 1 của Do: dock icon gọn + popup ✕, nút toàn màn hình, vẽ lại 4 chân dung (Kiếm Sĩ/Pháp Sư).

## Đã xong thêm
- GIAI ĐOẠN 1 + HUD V2 (2026-11-27 22:03): màn hình chiến đấu đúng sơ đồ GDD; Rừng Xanh chuẩn (sông/cầu va chạm, khu an toàn, vùng tinh anh, khu boss); 4 họ quái Rừng Xanh; boss Chúa Sói riêng + 3 skill có cảnh báo + phase; Kiếm Sĩ Nam mẫu đủ animation + kiếm đổi hình theo đồ; nạp bảng số GDD (chỉ số 3 phái, 12 skill chính, 4 phụ/phái, ngọc 7 cấp + caps); HUD V2 (5 icon tròn trên phải cạnh minimap, PanelManager pause/resume). Kiểm thử harness: AUTO màn 1 12/12 (3 phái) + 30/30 Pháp Sư, boss 4/4, va chạm sông/cầu/khu an toàn PASS, PanelManager 8/8. Chưa test: iPhone thật, farm tay dài hạn.
- v0.2.2 — Màn hình vào game tách state riêng (in-gate), sân phủ kín 100dvh, sửa lỗi HP 386/385, thêm lớp nhắc xoay ngang.
- v0.3 — Nhân vật CHIBI TOÀN BỘ (Do chốt): 6 chân dung chibi mới; sprite trong sân vẽ lại theo tỉ lệ chibi.
- v0.3.1 — Màn load/giới thiệu (tranh 3 anh hùng chibi đấu quái mới vẽ + tên game + thanh tải); sân khấu tạo nhân vật thành thảo nguyên 3 bệ đá, ô tên viền vàng trên cùng, nút Bắt đầu khóa tới khi tên hợp lệ.
- v0.3.2 — Màn tạo nhân vật làm lại theo 2 ảnh mẫu Do gửi: thảo nguyên FULL MÀN (sông, cối xay gió cánh quay), 3 nhân vật đứng rải tự nhiên trong cảnh, icon phái trên đầu, chạm chọn hiện panel phải (biểu đồ sao, Nam/Nữ).
- v0.3.3 — Thay hình nhân vật vẽ code bằng ẢNH AI chibi toàn thân (6 file hero-*.webp tách nền sạch): dùng ở màn chọn và trong sân với đủ hiệu ứng trạng thái. Kiểm chứng: tạo nhân vật "KiemTest" vào Rừng Xanh OK, node --check 7/7, audit pass, không lỗi console.
- Giai đoạn 0: XONG (GAP_ANALYSIS + kế hoạch giai đoạn 1 được Do phê duyệt 21:44). Giai đoạn 1: XONG (22:03).
- Do gửi bộ Fantasy RPG V2 lúc 21:54 (reference-zip-v2/): thay đổi duy nhất là HUD V2, đã chốt và triển khai. Bộ Fantasy_RPG_Muse.zip lúc 21:48 (reference-zip/): đã đọc hết + BAO-CAO-DOI-CHIEU-ZIP.md; Do duyệt kế hoạch 5 bước, chỉ bác khóa tính năng theo cấp.

- v0.4.0 — ĐỢT TÍCH HỢP ASSET (2026-11-28): quái Rừng Xanh + boss bằng ảnh thật, hero bản làm sạch viền, vá lỗi dải Pháp Sư (dùng ảnh tĩnh), nền tile v2b, cổng 2 lớp + prop ellipse theo ENGINE_PROP_LAYER_SPEC. Probe headless của builder PASS (cổng/va chạm/đạn/Pháp Sư/map khác hồi quy), Luna kiểm chứng độc lập bản xuất + live Cloudflare. Chi tiết: CHANGELOG.

## Đang chờ Do
- Do test bản v0.4.0 trên iPhone thật (quái ảnh thật, cổng tương tác, Pháp Sư tĩnh) và cho ý kiến.
- Chốt có đưa Pháp Sư Goblin vào pool spawn của Rừng Xanh không (hiện đã có ảnh + mapping, chưa spawn).

## Chưa đạt / tồn đọng (không đánh dấu hoàn thành)
- Lưu tiến trình thật theo máy (cần Cloudflare, giai đoạn 3).
- Boss màn sâu + khảm ngọc trọn vòng: chưa kiểm chứng trực tiếp.
- Kiểm thử iPhone thật: chưa thực hiện (chỉ qua audit khung hình).
