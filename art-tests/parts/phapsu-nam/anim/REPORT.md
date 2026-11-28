# Pháp Sư Nam: lắp ghép chuyển động từ bộ phận của Codex

GAME-ART-CORE (Claude), 2026-11-28. Nguồn: `../` (14 bộ phận, commit 3255cd9). **Chỉ xoay và dịch bộ phận quanh điểm trục trong `parts.json`; không vẽ thêm, không dùng AI vẽ lại.** Không sửa source game.

## Kiểm tra ghép chồng (`overlay_check.png`)
**Lệch khung bao 0 px, IoU alpha 1,000, chênh màu 0, 0 px lệch** → khớp tuyệt đối với `assembled.png`.

## Chuyển động
Ô 768×640, chân y = 620; thu nhỏ đều 0,95 quanh chân như Kiếm Sĩ, vì canvas gốc chỉ chừa 12 px phía trên chóp mũ.

| File | Khung | durations_ms | hit_frame | Cách dựng |
|---|---:|---|---:|---|
| `phapsu_nam_idle_2f.png` | 2 | 600, 600 | – | Đầu, hai tay, thân, tà áo nhích 0,6–2,5° |
| `phapsu_nam_run_6f.png` | 6 | 6 × 90 | – | Đùi ±22°, cẳng chân gập, tay phải đánh ±24°, tay trượng lắc nhẹ, tà áo bay, nhấp 4 px |
| `phapsu_nam_tung_phep_7f.png` | 7 | 70, 110, 130, 60, 140, 120, 100 | 4 | Giơ trượng thẳng lên cao, tay phải dang ra (tụ phép) → đẩy trượng chĩa ra trước, đầu trượng nghiêng ra ngoài, người lao tới 12 px → giữ → về |

- Thứ tự là cha trước con sau (vai → khuỷu → cổ tay + trượng). Trượng được bù góc ở cổ tay nên giữ thẳng đứng khi giơ cao và nghiêng khoảng 30° ra ngoài khi phóng.
- Xem: `contact.jpg`, `preview_*.gif`; số liệu ở `animations.json`.

## QC
- Mép ô alpha **0 %** ở 15/15 ô; mỗi ô 1 khối; chân y 616–620 (run nhấp nhô cố ý).
- Khớp vai, khuỷu, cổ tay không hở khi giơ trượng 90°. Như Codex lưu ý, đã thử động tác nâng trượng: **trượng không chạm vành mũ**.

## Giới hạn (Luna quyết)
1. Hiệu ứng phép (quả cầu sáng, tia phép) vẫn để game vẽ bằng code như hiện tại, không vẽ vào ảnh.
2. Chỉ có bộ phận nhìn thẳng: chạy ngang trông như chạy tại chỗ; dáng quay lưng hoặc nghiêng cần thêm bộ phận nhìn nghiêng hoặc nhìn sau.
3. Như REPORT của Codex: cổ áo rõ hơn và tà áo xoè hơn ảnh trong game.


## Đòn đánh thường (2026-11-29)
`phapsu_nam_attack_5f.png`: 5 khung, durations_ms [70, 90, 60, 110, 90] (tổng 420 ms), **hit_frame 2**. tung phép nhỏ: rút trượng về → vung trượng chĩa tới (đầu trượng nghiêng ra ngoài) → giữ → về.
- QC: mép ô alpha 0.0 %, 1 khối chính mỗi ô, chân y 620–620.
- Cùng tỉ lệ (0,95 quanh chân), cùng điểm chân và cùng bộ phận với idle/run, nên chuyển từ chạy sang đánh **không đổi người**.
- Xem: `preview_attack.gif`; so 6 hero: `../../attack_all_heroes.jpg`.


## Skill 2–4 và trúng đòn (2026-11-29)
| Skill | File | Khung | durations_ms | hit_frame | Alpha mép | Cách dựng |
|---|---|---:|---|---:|---|---|
| Băng Phong | `phapsu_nam_bang_phong_7f.png` | 7 | [80, 90, 90, 90, 90, 100, 100] (640 ms) | 2 | 0.0 % | quét trượng ngang qua trước người 2 nhịp (gió băng) |
| Lôi Đình | `phapsu_nam_loi_dinh_6f.png` | 6 | [80, 120, 140, 180, 120, 100] (740 ms) | 3 | 0.0 % | giơ trượng thẳng trời, tay kia dang, nhấc người 12–14 px, giữ (sét đánh ở khung giữ) |
| Thiên Thạch | `phapsu_nam_thien_thach_7f.png` | 7 | [90, 140, 180, 80, 160, 120, 100] (870 ms) | 3 | 0.0 % | hai tay giơ cao tụ phép lâu, rồi đẩy trượng xuống phía trước (thiên thạch rơi) |
| Trúng đòn | `phapsu_nam_hurt_3f.png` | 3 | [80, 110, 110] (300 ms) | – | 0.0 % | bật lùi 14 px, đầu ngả, tay văng, rồi hồi |

- Cùng tỉ lệ, điểm chân và bộ phận với idle/run/attack. Mỗi ô 1 khối chính.
- **Giới hạn (Luna quyết):**
- Hiệu ứng băng, sét, thiên thạch do game vẽ theo `hit_frame`.
- Bản nữ: tóc liền đầu nên không bay; tay phải bị tóc che một phần khi dang.
