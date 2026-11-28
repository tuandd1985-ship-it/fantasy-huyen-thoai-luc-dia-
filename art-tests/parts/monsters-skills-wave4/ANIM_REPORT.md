# Quái bộ 4: lắp ghép chuyển động từ bộ phận của Codex

GAME-ART-CORE (Claude), 2026-11-28. Nguồn: các thư mục quái ở đây (commit 8c3c804). **Chỉ xoay và dịch bộ phận quanh điểm trục; không vẽ thêm.** Không sửa source game.

- Mỗi quái có `anim/`:
  - dải PNG theo hành động (ô 768×640, chân y = 620; Kền Kền bay giữ độ cao gốc);
  - `animations.json` (durations_ms, hit_frame, loop, QC);
  - `preview_*.gif`, `contact.jpg`, `motions_<id>.json`.
- Xem nhanh: `anim_contact_1.jpg` (Xương Khô, Thằn Lằn, Bọ Cạp), `anim_contact_2.jpg` (Kền Kền, Yêu Tuyết, Ma Cà Rồng).
- Hành động: **idle, move, attack (có hit_frame), hurt** như các bộ trước. Ma Cà Rồng có thêm `skill_drain` (dang tay, bay nhẹ, giữ để hút máu).

| ID | Quái | Ghép chồng | Hành động |
|---|---|---|---|
| `skeleton` | Xương Khô | lệch [0, 0, 0, 0] px, IoU 1.0 | idle 2f (1000 ms); move 4f (520 ms); attack 6f (590 ms, hit 3); hurt 3f (320 ms) |
| `lizard` | Thằn Lằn Đầm | lệch [0, 0, 0, 0] px, IoU 1.0 | idle 2f (1000 ms); move 4f (440 ms); attack 6f (580 ms, hit 3); hurt 3f (320 ms) |
| `scorpion` | Bọ Cạp Cát | lệch [0, 0, 0, 0] px, IoU 1.0 | idle 2f (900 ms); move 4f (320 ms); attack 6f (620 ms, hit 3); hurt 3f (320 ms) |
| `vulture` | Kền Kền (bay) | lệch [0, 0, 0, 0] px, IoU 1.0 | idle 4f (600 ms); move 4f (400 ms); attack 6f (600 ms, hit 2); hurt 3f (320 ms) |
| `yeti` | Yêu Tuyết | lệch [0, 0, 0, 0] px, IoU 1.0 | idle 2f (1200 ms); move 4f (640 ms); attack 6f (740 ms, hit 3); hurt 3f (320 ms) |
| `vampire` | Ma Cà Rồng | lệch [0, 0, 0, 0] px, IoU 1.0 | idle 2f (1000 ms); move 4f (560 ms); attack 6f (680 ms, hit 3); skill_drain 6f (1000 ms, hit 2); hurt 3f (320 ms) |

## Khớp động tác với bảng thử của Codex
- **Xương Khô**: chém kiếm (giơ ra sau → chém ngang). Đã soi khuỷu phải (khớp chồng ít nhất) ở biên độ chém lớn nhất: không hở.
- **Thằn Lằn**: vung vuốt trái, đuôi quất ngược.
- **Bọ Cạp**: 8 chân bò theo 2 nhóm xen kẽ; **chích độc** = cong đuôi ra sau rồi chích tới (khung 3, dùng `fx/poison`).
- **Kền Kền**: vỗ cánh; tấn công = sà xuống phía trước (khung 2).
- **Yêu Tuyết**: kéo tay ra sau rồi **đấm nặng** (khung 3, dùng `fx/ice-hit`).
- **Ma Cà Rồng**: tung **huyết cầu** (kéo tay rồi đẩy ra, khung 3, dùng `fx/blood`) và `skill_drain`.

## QC
- **Ghép chồng khớp tuyệt đối cả 6** (lệch 0 px, IoU 1,0). **Mép ô alpha 0 %** ở mọi khung.
- **12 ảnh hiệu ứng `fx/`**: PNG cạnh dài 384 px và WebP 192 px, đều RGBA, **mép ảnh alpha 0 %**. Dùng được ngay; em không chỉnh.

## Giới hạn (Luna quyết)
1. Cẳng tay và kiếm Xương Khô liền một lớp, nên kiếm không xoay riêng ở cổ tay.
2. Áo choàng Ma Cà Rồng gắn liền thân, nên không bay khi di chuyển.
3. Quái nhìn thẳng thì game lật ảnh theo hướng đi.
4. Thời điểm bắn hoặc hiện hiệu ứng lấy theo `hit_frame`; đường bay đạn, sát thương và AI vẫn do game xử lý.
