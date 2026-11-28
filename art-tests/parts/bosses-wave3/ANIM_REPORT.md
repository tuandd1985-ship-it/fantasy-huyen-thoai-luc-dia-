# 4 boss: lắp ghép chuyển động từ bộ phận của Codex

GAME-ART-CORE (Claude), 2026-11-28. Nguồn: các thư mục boss ở đây (commit 88f93f7). **Chỉ xoay và dịch bộ phận quanh điểm trục; không vẽ thêm.** Không sửa source game.

- Mỗi boss có `anim/`:
  - dải PNG theo hành động (ô 768×640, chân y = 620, thu nhỏ 0,92 để chừa chỗ cho cú lao hoặc bật nhảy);
  - `animations.json` (durations_ms, hit_frame, loop, QC);
  - `preview_*.gif`, `contact.jpg`, `motions_<id>.json`.
- Xem nhanh: `anim_contact_1.jpg` (Chúa Sói, Đầm Chúa), `anim_contact_2.jpg` (Pharaoh, Chúa Quỷ).
- Ngoài **idle, move, attack, hurt** như quái thường, mỗi boss có **2 skill** dựng theo mô tả kỹ năng trong README của Codex.

| ID | Boss | Ghép chồng | Hành động |
|---|---|---|---|
| `wolfLord` | Chúa Sói Alpha | lệch [0, 0, 0, 0] px, IoU 1.0 | idle 2f (1100 ms); move 4f (360 ms); attack 6f (600 ms, hit 3); skill_charge 7f (940 ms, hit 3); skill_howl 7f (1000 ms, hit 3); hurt 3f (320 ms) |
| `toadKing` | Đầm Chúa | lệch [0, 0, 0, 0] px, IoU 1.0 | idle 2f (1200 ms); move 5f (620 ms); attack 6f (620 ms, hit 3); skill_slam 7f (1000 ms, hit 4); skill_summon 7f (900 ms, hit 3); hurt 3f (320 ms) |
| `pharaoh` | Pharaoh Cổ Đại | lệch [0, 0, 0, 0] px, IoU 1.0 | idle 2f (1200 ms); move 4f (600 ms); attack 6f (610 ms, hit 3); skill_summon 6f (900 ms, hit 2); skill_aoe 7f (820 ms, hit 3); hurt 3f (320 ms) |
| `demonLord` | Chúa Quỷ Bóng Đêm | lệch [0, 0, 0, 0] px, IoU 1.0 | idle 4f (1200 ms); move 4f (560 ms); attack 6f (620 ms, hit 3); skill_charge 7f (940 ms, hit 3); skill_aoe 7f (860 ms, hit 3); hurt 3f (320 ms) |

## Skill từng boss
- **Chúa Sói**:
  - `skill_charge`: thu bốn chân, hạ đầu (giữ 260 ms để báo trước), rồi lao 40 px; gây sát thương ở khung lao.
  - `skill_howl`: ngẩng đầu hú, đuôi vẫy; game sinh sói con theo nhịp này.
- **Đầm Chúa**:
  - `skill_slam`: co chân, nén thân, nâng đầu (báo trước khoảng 560 ms), bật cao rồi đáp; gây sát thương ở khung chạm đất.
  - `skill_summon`: phồng người kêu, để gọi cóc.
- **Pharaoh**:
  - `skill_summon`: nhấc trượng cao, giữ, để gọi xác ướp.
  - `skill_aoe`: nhấc trượng rồi dập xuống; gây sát thương ở khung dập. Mũi trượng chạm thấp hơn đường chân khoảng 13 px là cố ý (trượng cắm đất).
- **Chúa Quỷ**:
  - `skill_charge`: thu cánh, cúi người rồi lao.
  - `skill_aoe`: bung cánh, giơ tay rồi hạ xuống nổ diện rộng.

## QC
- **Ghép chồng khớp tuyệt đối cả 4** (lệch 0 px, IoU 1,0). **Mép ô alpha 0 %** ở mọi khung. Khớp không hở; đã soi cổ Chúa Sói, vai Đầm Chúa và lớp cánh Chúa Quỷ như Codex dặn.

## Giới hạn (Luna quyết)
1. Cú lao/nhảy trong ảnh chỉ dịch tối đa 40 px trong ô. Quãng lao thật trên map do game di chuyển boss.
2. Hiệu ứng nổ, triệu hồi, vòng cảnh báo, đổi pha vẫn để game vẽ, đồng bộ theo `hit_frame`.
3. Đầm Chúa, Pharaoh, Chúa Quỷ nhìn thẳng: di chuyển ngang trông như bước tại chỗ, game lật ảnh theo hướng. Chúa Sói nhìn ngang, đi sang trái phải lật.
4. Như Codex ghi: trượng Pharaoh liền với cẳng tay trái nên không xoay riêng được.
5. 3 boss còn lại (Nhện Chúa, Golem Băng, Rồng Lửa) đã có chuyển động ở bộ quái 1–2, chưa có skill riêng kiểu boss. Có thể thêm nếu Luna cần.
