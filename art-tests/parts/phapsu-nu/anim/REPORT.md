# Pháp Sư Nữ: lắp ghép chuyển động từ bộ phận của Codex

GAME-ART-CORE (Claude), 2026-11-28. Nguồn: `../` (14 bộ phận, commit e804ac3). **Chỉ xoay và dịch bộ phận quanh điểm trục trong `parts.json`; không vẽ thêm, không dùng AI vẽ lại.** Không sửa source game.

## Kiểm tra ghép chồng (`overlay_check.png`)
- Lệch khung bao **[0, 0, 0, 0]** px.
- IoU alpha **1.0**, chênh màu **0.0**, lệch alpha **0** px.
- Kết luận: khớp tuyệt đối với `assembled.png`.

## Chuyển động
Ô 768×640, chân y = 620, thu nhỏ 0,95 quanh chân. Dùng lại bộ chuyển động của bản nam: cùng tên bộ phận, cùng thời lượng và khung gây sát thương, nên game dùng chung logic. Tóc dài nằm chung trong lớp đầu (không tách riêng), nên tóc đi theo đầu.

| File | Khung | durations_ms | hit_frame | Chân y | Alpha mép |
|---|---:|---|---:|---|---|
| `phapsu_nu_idle_2f.png` | 2 | 600, 600 | – | 620–620 | 0.0 % |
| `phapsu_nu_run_6f.png` | 6 | 90, 90, 90, 90, 90, 90 | – | 616–620 | 0.0 % |
| `phapsu_nu_tung_phep_7f.png` | 7 | 70, 110, 130, 60, 140, 120, 100 | 4 | 620–620 | 0.0 % |

- Xem: `contact.jpg`, `preview_*.gif` (có vạch chân và chữ HIT). Số liệu: `animations.json`.
- QC: mỗi ô 1 khối đặc, 0 mảnh rời. Riêng `run` nhấp nhô 4 px là cố ý.

## Giới hạn (Luna quyết)
1. Tóc dài **che tay phải** ở hầu hết khung (tay phải nằm dưới lớp tóc), nên tay phải dang ra khi tụ phép ít thấy hơn bản nam.
2. Khi giơ trượng cao, viên ngọc tím lên sát mép trên ô (vẫn trong ô, alpha mép 0 %). Codex ghi viên ngọc mẫu lớn hơn ảnh trong game.
3. Tóc không tách riêng nên không có chuyển động tóc bay; muốn có cần tách tóc sau thành mảnh riêng.
4. Chỉ có bộ phận nhìn thẳng: chạy ngang trông như chạy tại chỗ; dáng quay lưng hoặc nhìn nghiêng cần thêm bộ phận.


## Đòn đánh thường (2026-11-29)
`phapsu_nu_attack_5f.png`: 5 khung, durations_ms [70, 90, 60, 110, 90] (tổng 420 ms), **hit_frame 2**. tung phép nhỏ: rút trượng về → vung trượng chĩa tới (đầu trượng nghiêng ra ngoài) → giữ → về.
- QC: mép ô alpha 0.0 %, 1 khối chính mỗi ô, chân y 620–620.
- Cùng tỉ lệ (0,95 quanh chân), cùng điểm chân và cùng bộ phận với idle/run, nên chuyển từ chạy sang đánh **không đổi người**.
- Xem: `preview_attack.gif`; so 6 hero: `../../attack_all_heroes.jpg`.


## Skill 2–4 và trúng đòn (2026-11-29)
| Skill | File | Khung | durations_ms | hit_frame | Alpha mép | Cách dựng |
|---|---|---:|---|---:|---|---|
| Băng Phong | `phapsu_nu_bang_phong_7f.png` | 7 | [80, 90, 90, 90, 90, 100, 100] (640 ms) | 2 | 0.0 % | quét trượng ngang qua trước người 2 nhịp (gió băng) |
| Lôi Đình | `phapsu_nu_loi_dinh_6f.png` | 6 | [80, 120, 140, 180, 120, 100] (740 ms) | 3 | 0.0 % | giơ trượng thẳng trời, tay kia dang, nhấc người 12–14 px, giữ (sét đánh ở khung giữ) |
| Thiên Thạch | `phapsu_nu_thien_thach_7f.png` | 7 | [90, 140, 180, 80, 160, 120, 100] (870 ms) | 3 | 0.0 % | hai tay giơ cao tụ phép lâu, rồi đẩy trượng xuống phía trước (thiên thạch rơi) |
| Trúng đòn | `phapsu_nu_hurt_3f.png` | 3 | [80, 110, 110] (300 ms) | – | 0.0 % | bật lùi 14 px, đầu ngả, tay văng, rồi hồi |

- Cùng tỉ lệ, điểm chân và bộ phận với idle/run/attack. Mỗi ô 1 khối chính.
- **Giới hạn (Luna quyết):**
- Hiệu ứng băng, sét, thiên thạch do game vẽ theo `hit_frame`.
- Bản nữ: tóc liền đầu nên không bay; tay phải bị tóc che một phần khi dang.
