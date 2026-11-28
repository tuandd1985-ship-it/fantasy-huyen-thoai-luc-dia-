# 6 quái: lắp ghép chuyển động từ bộ phận của Codex

GAME-ART-CORE (Claude), 2026-11-28. Nguồn: các thư mục quái ở đây (commit 3735e4e). **Chỉ xoay và dịch bộ phận quanh điểm trục trong `parts.json`; không vẽ thêm, không dùng AI vẽ lại.** Không sửa source game.

- Mỗi quái có `anim/`: dải PNG theo hành động (ô 768×640, chân y = 620; quái bay giữ nguyên độ cao như dáng gốc), `animations.json` (durations_ms, hit_frame, loop, QC), `preview_*.gif`, `contact.jpg`, `motions_<id>.json` (khung khoá).
- Xem nhanh 6 quái: `anim_contact_1.jpg` (Dơi, Cóc, Xác Ướp), `anim_contact_2.jpg` (Rồng, Sói, Hồn Ma).
- Hành động chung cho mọi quái: **idle, move, attack (có khung gây sát thương), hurt**. Chết, bóng, hiệu ứng độc/lửa/băng và độ mờ hồn ma vẫn để game vẽ.
- Thu nhỏ đều 0,95 quanh chân như hero, để chừa chỗ khi nhảy hoặc vung.

| ID | Quái | Ghép chồng với assembled.png | Hành động | Alpha mép tối đa |
|---|---|---|---|---|
| `bat` | Dơi Quỷ (bay) | lệch [0, 0, 0, 0] px, IoU 1.0 | idle 4f (560 ms); move 4f (360 ms); attack 6f (600 ms, hit 2); hurt 3f (320 ms) | 0.0 % |
| `toad` | Cóc Độc | lệch [0, 0, 0, 0] px, IoU 1.0 | idle 2f (1000 ms); move 6f (630 ms); attack 6f (580 ms, hit 3); hurt 3f (320 ms) | 0.0 % |
| `mummy` | Xác Ướp | lệch [0, 0, 0, 0] px, IoU 1.0 | idle 2f (1000 ms); move 4f (520 ms); attack 6f (600 ms, hit 3); hurt 3f (320 ms) | 0.0 % |
| `fireDragon` | Rồng Lửa | lệch [0, 0, 0, 0] px, IoU 1.0 | idle 4f (1040 ms); move 4f (440 ms); attack 6f (700 ms, hit 3); hurt 3f (320 ms) | 0.0 % |
| `iceWolf` | Sói Băng (nhìn ngang) | lệch [0, 0, 0, 0] px, IoU 1.0 | idle 2f (1000 ms); move 4f (340 ms); attack 6f (600 ms, hit 3); hurt 3f (320 ms) | 0.0 % |
| `wraith` | Hồn Ma (bay) | lệch [0, 0, 0, 0] px, IoU 1.0 | idle 4f (880 ms); move 4f (600 ms); attack 6f (620 ms, hit 3); hurt 3f (320 ms) | 0.0 % |

## Cách dựng từng con
- **Dơi**: hai cánh vỗ ngược nhau ±25°, thân nhấp nhô 6–8 px; tấn công = vụt lên rồi bổ nhào xuống phía trước; trúng đòn = cánh xoè, bật lùi.
- **Cóc**: di chuyển = **nhảy**: nhún, bật cao 46 px, đáp đất (chân luôn được đặt lại chạm đất, riêng lúc bay lên là cố ý rời đất); tấn công = ngửa đầu rồi phóng tới (khi phun độc, game vẽ tia độc ở khung 3).
- **Xác Ướp**: bước lê chân ±16°, tay đung đưa; tấn công = giơ hai tay rồi vồ xuống; trúng đòn = ngả người, tay văng.
- **Rồng Lửa**: cánh vỗ, đuôi quật, bốn chân bước xen kẽ; tấn công = ngẩng đầu, xoè cánh, rồi lao đầu xuống (game vẽ hơi lửa ở khung 3).
- **Sói Băng** (nhìn ngang, quay phải): phi bốn chân, thân nhấp 10 px, đuôi vẫy; tấn công = thu mình rồi vồ tới 36 px.
- **Hồn Ma**: bồng bềnh ±8 px, đuôi khói lượn; tấn công = giơ hai tay rồi cào chéo xuống.

## QC
- **Ghép chồng khớp tuyệt đối cả 6** (lệch 0 px, IoU 1,0).
- **Mép ô alpha 0 %** ở mọi khung; khớp không hở khi xoay.

## Giới hạn (Luna quyết)
1. Như Codex lưu ý: chân Xác Ướp và Sói Băng là **một đoạn liền** nên bước chân xoay cả chân, không gập gối.
2. Rồng Lửa và Cóc nhìn thẳng: di chuyển ngang trông như bước tại chỗ; game lật ngang theo hướng.
3. Sói Băng nhìn ngang: khi đi sang trái game phải lật ngang ảnh.
4. Không vẽ hiệu ứng (độc, lửa, băng, bóng): game vẽ như hiện tại, đồng bộ theo `hit_frame`.

## Tái lập
`python anim_tools/gen_monster_motions.py` rồi `python anim_tools/parts_rig.py <quái> <quái>/anim/motions_<id>.json <out>`. Mỗi quái chạy 7–11 giây.
