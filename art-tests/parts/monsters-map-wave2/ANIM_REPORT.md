# Quái bộ 2: lắp ghép chuyển động từ bộ phận của Codex

GAME-ART-CORE (Claude), 2026-11-28. Nguồn: các thư mục quái ở đây (commit 6359da6). **Chỉ xoay và dịch bộ phận quanh điểm trục trong `parts.json`; không vẽ thêm.** Không sửa source game.

- Mỗi quái có `anim/`: dải PNG theo hành động (ô 768×640, chân y = 620), `animations.json` (durations_ms, hit_frame, loop, QC), `preview_*.gif`, `contact.jpg`, `motions_<id>.json`.
- Xem nhanh: `anim_contact_1.jpg` (Nhện Độc, Nhện Chúa, Golem Băng), `anim_contact_2.jpg` (Golem Dung Nham, Phù Thủy Băng, Hỏa Ma).
- Hành động chung: **idle, move, attack (có khung gây sát thương), hurt**, giống bộ 1 nên game dùng chung logic.

| ID | Quái | Ghép chồng | Hành động | Alpha mép tối đa |
|---|---|---|---|---|
| `spider` | Nhện Độc | lệch [0, 0, 0, 0] px, IoU 1.0 | idle 2f (900 ms); move 4f (320 ms); attack 6f (600 ms, hit 3); hurt 3f (320 ms) | 0.0 % |
| `spiderQueen` | Nhện Chúa | lệch [0, 0, 0, 0] px, IoU 1.0 | idle 2f (900 ms); move 4f (320 ms); attack 6f (600 ms, hit 3); hurt 3f (320 ms) | 0.0 % |
| `iceGolem` | Golem Băng | lệch [0, 0, 0, 0] px, IoU 1.0 | idle 2f (1200 ms); move 4f (680 ms); attack 6f (800 ms, hit 3); hurt 3f (320 ms) | 0.0 % |
| `magmaGolem` | Golem Dung Nham | lệch [0, 0, 0, 0] px, IoU 1.0 | idle 2f (1200 ms); move 4f (680 ms); attack 6f (800 ms, hit 3); hurt 3f (320 ms) | 0.0 % |
| `iceWitch` | Phù Thủy Băng | lệch [0, 0, 0, 0] px, IoU 1.0 | idle 2f (1000 ms); move 4f (560 ms); attack 6f (680 ms, hit 3); hurt 3f (320 ms) | 0.0 % |
| `imp` | Hỏa Ma | lệch [0, 0, 0, 0] px, IoU 1.0 | idle 4f (800 ms); move 4f (400 ms); attack 6f (560 ms, hit 3); hurt 3f (320 ms) | 0.0 % |

## Cách dựng
- **Nhện Độc / Nhện Chúa**: 8 chân bước theo **2 nhóm 4 chân xen kẽ** (dáng bò thật của nhện); tấn công = giơ 2 chân trước lên rồi cắm xuống, thân chồm tới. Nhện Chúa biên độ nhỏ hơn cho cảm giác nặng.
- **Golem Băng / Golem Dung Nham**: bước nặng, nhún 5 px; tấn công = giơ hai tay qua vai (khựng), rồi **đập xuống**; khung đập là khung gây sát thương.
- **Phù Thủy Băng**: giơ trượng và tay trái tụ phép, rồi đẩy trượng ra trước. Đã thử giơ trượng tới biên độ lớn nhất ở vai (khớp chồng ít nhất theo Codex): không hở.
- **Hỏa Ma**: cánh vỗ, đuôi lắc; tấn công = kéo quả cầu lửa ra sau rồi ném tới (game vẽ quả cầu bay ra ở khung gây sát thương).

## QC
- **Ghép chồng khớp tuyệt đối cả 6** (lệch 0 px, IoU 1,0).
- **Mép ô alpha 0 %** ở mọi khung; khớp không hở.

## Giới hạn (Luna quyết)
1. Golem: cổ tay, khuỷu, đầu gối xoay theo cả đoạn (như Codex ghi), nên cú đập là cả cánh tay vung, không gập khuỷu.
2. Phù Thủy Băng: tay và trượng chung một lớp nên trượng luôn đi theo cẳng tay, không xoay riêng được.
3. Các quái nhìn thẳng: di chuyển ngang trông như bước tại chỗ; game lật ngang theo hướng.
4. Hiệu ứng (độc nhện, băng, lửa, nham thạch rơi, bóng) để game vẽ, đồng bộ theo `hit_frame`.
