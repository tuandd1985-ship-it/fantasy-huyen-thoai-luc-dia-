# ARCHITECTURE — FANTASY: HUYỀN THOẠI LỤC ĐỊA
Kiến trúc source code. SPEC.md ưu tiên cao nhất. Thay đổi kiến trúc lớn phải báo cáo và chờ Do phê duyệt (Master Instruction mục 3); không xóa/viết lại toàn bộ source khi chưa có lý do kỹ thuật + phương án bảo toàn dữ liệu.

## Công nghệ
- Hiện tại: web artifact tĩnh (HTML/JS trong Muse Space) — bản mẫu kiểm chứng gameplay.
- Định hướng khi triển khai thật (PROPOSED, chờ duyệt cùng giai đoạn chuẩn): TypeScript + Phaser 3 + Vite + PWA nếu phù hợp; máy chủ Cloudflare (Worker + KV) cho lưu trữ/tài khoản ở giai đoạn triển khai. Mọi chuyển đổi phải có kế hoạch di trú dữ liệu nhân vật.

## Phân lớp bắt buộc (không trộn)
- DATA: toàn bộ bảng cấu hình — quái, boss, trang bị, ngọc, skill (nhân vật + quái), map, EXP, tỉ lệ rơi, công thức nâng cấp/ghép, caps cân bằng. TUYỆT ĐỐI không hardcode các số này vào engine.
- ENGINE: vòng lặp (delta-time), chiến đấu, va chạm/tìm đường, skill + hiệu ứng, sinh quái/AI hành vi, camera, minimap. Engine dùng chung cho mọi nhân vật/quái/map.
- GAME STATE: trạng thái từng nhân vật (cấp, điểm thân thể/skill, đồ, ngọc, vàng, map đã mở, nhiệm vụ) — tách theo từng nhân vật.
- UI: HUD, dock icon, popup (nhân vật/túi/skill/lò rèn/khảm/bản đồ/cửa hàng/cài đặt), màn hình chọn/tạo nhân vật, kết quả boss, hồi sinh.
- ASSETS: sprite, animation, chân dung, icon, hiệu ứng, âm thanh — nạp theo map/cần dùng.
- STORAGE: một điểm lưu duy nhất (hàm persist() hiện tại là điểm gắn này) — bản tĩnh lưu trong phiên; bản triển khai gắn Cloudflare KV qua API, có version schema + backup/rollback để cập nhật không mất dữ liệu người chơi.

## Nguyên tắc mở rộng
- Thêm map/quái mới (dùng hành vi đã hỗ trợ) = thêm DATA + ASSETS, không sửa ENGINE.
- Mỗi module một trách nhiệm rõ ràng; sửa module này không được phá module khác — regression test sau mỗi nhiệm vụ (xem TEST_REPORT.md).
- Hành vi quái chuẩn hóa thành nhóm: melee, ranged, flying, tank, swarm, poison/slow, support-healer, boss (skill theo kịch bản + phase).

## Bảo mật & phát hành (giai đoạn Cloudflare)
- Token API không đưa vào frontend/repo công khai (dùng Secure Vault như các app trước).
- Preview trước, Production sau; mỗi bản có version + CHANGELOG + phương án rollback; không ghi đè bản ổn định khi chưa kiểm thử Preview.
