# ASSET_INVENTORY: Fantasy: Huyền Thoại Lục Địa

Lập ngày 2026-11-28 từ bản v0.3.7 (`cfecb34`). Danh mục quái, boss, map, ngọc và skill lấy từ lớp DATA trong `index.html` và GDD.
Ký hiệu: ✅ có và đạt · 🟡 có nhưng cần sửa · 🔴 chỉ vẽ bằng code (cần thay) · ⬜ chưa có.

## A. Tài nguyên đang có (19 file)

| Khóa | Vai trò | Kích thước | Dung lượng | Trạng thái |
|---|---|---|---:|---|
| k1 | Tranh màn load | 1920×1280 | 605 KB | 🟡 lệch thiết kế hero |
| k2 / k3 | Hero Kiếm Sĩ Nam / Nữ | 515×640 / 572×640 | 90 / 97 KB | 🟡 viền tím |
| k4 / k5 | Hero Pháp Sư Nam / Nữ | 555×640 / 569×640 | 87 / 99 KB | 🟡 viền tím |
| k6 / k7 | Hero Cung Thủ Nam / Nữ | 501×640 / 502×640 | 98 / 91 KB | 🟡 viền tím |
| k0, k8–k12 | Chân dung ×6 | 800×800 | 66–80 KB | ✅ |
| k13–k18 | Dải 6 khung ×6 nhân vật | 2520×500 | 239–315 KB | 🔴 thay |
| | **Tổng** | | **khoảng 3,3 MB** | |

## B. Tài nguyên còn thiếu

### B1. Nhân vật người chơi (6 biến thể)
Mỗi biến thể, giai đoạn mẫu làm 4 hướng (**ĐÃ DUYỆT 2026-11-28**, căn cứ SPEC mục 1b + ART_DIRECTION.md, commit 243c0fa): vẽ thật 2 hướng xuống/lên, trái/phải bằng lật ngang:

| Animation | Số khung | Cách làm đề xuất |
|---|---:|---|
| Đứng (idle, thở) | 4 | Rig cắt mảnh |
| Chạy | 8 | Rig + 2–4 khung chính sinh bằng AI |
| Đánh thường | 5 | Khung chính AI (pose) + nội suy |
| 4 skill chính | 4–6 / skill | Khung chính AI + VFX tách riêng |
| Skill phụ chủ động | 3 | Pose chung + VFX |
| Trúng đòn | 2 | Rig |
| Tử vong | 5 | Rig + 1 khung nằm (AI) |
| Hồi sinh | 4 | Đảo ngược tử vong + VFX sáng |
| **Tổng / hướng** | **khoảng 50** | ×2 hướng ×6 nhân vật ≈ **600 khung** |

Kèm theo: 1 bảng tham chiếu (turnaround 4 góc) và 1 bảng màu chuẩn cho mỗi nhân vật.

### B2. Vũ khí đổi ngoại hình (cầm trên tay + icon)
3 loại (kiếm, trượng, cung) × 4 bậc (Lv1 Sắt · Lv20 Băng · Lv40 Hỏa · Lv60 Thần) = **12 sprite vũ khí rời** (gắn vào khớp tay của rig) + 12 icon.
Giáp/mũ đổi ngoại hình: giai đoạn sau. Đề xuất 3 bộ giáp × 3 phái, đổi màu bằng palette swap.

### B3. Quái (23 họ, dữ liệu đã có trong DATA). Phong cách chibi-fantasy **ĐÃ DUYỆT 2026-11-28** (căn cứ SPEC mục 1b + ART_DIRECTION.md, commit 243c0fa)
Rừng Xanh (Slime, Goblin, Sói Rừng, Goblin Cung Thủ, boss Chúa Sói) đã có thiết kế chi tiết ở `docs/MONSTER_DESIGN_RUNG_XANH.md`. Pháp Sư Goblin có trong DATA nhưng **chưa có trong bảng thiết kế đó**.

| Map | Quái |
|---|---|
| Rừng Xanh | Slime Ngọc, Goblin, Goblin Cung Thủ, Sói Rừng, Pháp Sư Goblin |
| Hang Tối | Dơi Quỷ, Nhện Độc, Xương Khô |
| Đầm Lầy Độc | Cóc Độc, Thằn Lằn Đầm |
| Sa Mạc Cát | Bọ Cạp Cát, Xác Ướp, Kền Kền |
| Núi Lửa | Hỏa Ma, Sói Lửa, Golem Dung Nham |
| Băng Nguyên | Sói Băng, Yêu Tuyết, Phù Thủy Băng |
| Lâu Đài Bóng Đêm | Kỵ Sĩ Hắc Ám, Ma Cà Rồng, Tà Giáo Đồ, Hồn Ma |

Mỗi họ: đứng 4 + di chuyển 6 + tấn công 4 + trúng đòn 2 + chết 4 = **khoảng 20 khung / hướng**. Theo chuẩn 4 hướng đã duyệt (vẽ xuống/lên + lật ngang) là khoảng 40 khung vẽ mỗi họ, tổng khoảng 920 khung. (Bản trước ghi "quái 1 hướng + lật", nay đã sửa cho khớp SPEC 1b.)
Tinh anh: dùng cùng sprite, phóng 1,25× + viền đỏ bằng code, **không vẽ riêng**. Lưu ý: GDD có Rắn độc, Pháp sư đầm lầy, Vệ binh cổ đại, Ác quỷ… chưa có trong DATA. Codex cần thống nhất danh sách trước.

### B4. Boss (7)
Chúa Sói Alpha · Nhện Chúa · Đầm Chúa · Pharaoh Cổ Đại · Rồng Lửa · Golem Băng · Chúa Quỷ Bóng Đêm.
Mỗi boss: đứng 4, di chuyển 6, 3 skill × 5, trúng đòn 2, chết 6, **bản phase 2** (đổi màu + chi tiết phát sáng) ≈ 35 khung / hướng × 2 hướng vẽ, khung 1024. Chibi-fantasy nhưng to (khoảng 3× quái cùng họ) và dữ: rune, sẹo, mắt phát sáng (**ĐÃ DUYỆT 2026-11-28**, căn cứ SPEC mục 1b + ART_DIRECTION.md, commit 243c0fa). Thêm chân dung boss 800×800 cho thông báo boss và bảng kết quả.

### B5. Map (7)
Mỗi map gồm:
- Nền đất dạng tile lặp liền mạch (2–3 biến thể)
- Lớp xa (parallax/vignette)
- Pack vật thể 15–25 món: cây, đá, phế tích, nhà… mỗi món có footprint va chạm
- Sông/đường dạng autotile
- Cầu, cổng dịch chuyển, khu an toàn, NPC đứng, khu boss (sàn đấu), điểm bí mật
- Thumbnail chọn map 7 × 640×360

Rừng Xanh làm trước làm **map chuẩn**.

### B6. Icon
| Nhóm | Số lượng | Kích thước gốc → dùng |
|---|---:|---|
| Skill chính | 12 | 512 → 96/64 |
| Skill phụ | 12 | 512 → 96/64 |
| HUD V2 (Nhân vật, Túi, Trang bị, Kỹ năng, Cài đặt) | 5 | 256 → 40 |
| Trang bị (4 ô × 4 bậc, mở rộng 10 ô) | 16 → 40 | 512 → 64 |
| Ngọc 5 màu | 5 hình gốc + 7 huy hiệu cấp (chồng bằng code) | 256 → 48 |
| Khung độ hiếm 4 màu | 4 | 9-slice |
| Bình HP/MP, vàng, nguyên liệu nâng cấp | khoảng 8 | 256 → 48 |
| Điểm trên minimap (boss, tinh anh, cổng, rương) | khoảng 6 | 64 |

### B7. Giao diện
Khung panel viền vàng cổ (9-slice), nút chính/phụ, nút ✕, vòng nút skill + lớp hồi chiêu, thanh HP/MP/EXP (khung + chất lỏng), joystick (đế + núm), thanh tải, thẻ chọn map ×7, màn kết quả boss, màn hồi sinh, paper-doll nhân vật (bóng nền), chân dung 9 NPC thành phố.

### B8. Hiệu ứng (VFX)
12 VFX skill (6–10 khung, cộng màu/additive), tia chạm, số sát thương (code), lên cấp, đồ rơi phát sáng theo độ hiếm, vòng cảnh báo boss (code + texture), hào quang trang bị +7/+10/+15 (3 tầng × 3 phái).

## C. Ước lượng khối lượng

| Nhóm | Ảnh gốc cần sinh (ước) | Ghi chú |
|---|---:|---|
| Nhân vật | khoảng 150 khung chính AI + rig | phần còn lại nội suy hoặc rig |
| Quái + boss | khoảng 30 thiết kế + khoảng 500 khung chính | đã tính 2 hướng vẽ (xuống/lên) |
| Map | khoảng 7 × 30 | |
| Icon + UI | khoảng 120 | |
| VFX | khoảng 40 sheet | |

Với tốc độ SDXL khoảng 15 s/ảnh trên RTX 2070S (sinh 3–4 ứng viên, chọn 1), riêng khâu sinh ảnh mất khoảng 35–55 giờ GPU. Khâu duyệt và làm sạch tốn nhiều thời gian hơn khâu sinh.
