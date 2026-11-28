# Cung Thủ Nữ: lắp ghép chuyển động từ bộ phận của Codex

GAME-ART-CORE (Claude), 2026-11-28. Nguồn: `../` (16 bộ phận, commit e804ac3). **Chỉ xoay và dịch bộ phận quanh điểm trục trong `parts.json`; không vẽ thêm, không dùng AI vẽ lại.** Không sửa source game.

## Kiểm tra ghép chồng (`overlay_check.png`)
- Lệch khung bao **[0, 0, 0, 0]** px.
- IoU alpha **1.0**, chênh màu **0.0**, lệch alpha **0** px.
- Kết luận: khớp tuyệt đối với `assembled.png`.

## Chuyển động
Ô 768×640, chân y = 620, thu nhỏ 0,95 quanh chân. Dùng lại bộ chuyển động của bản nam: cùng tên bộ phận, cùng thời lượng và khung gây sát thương, nên game dùng chung logic. **Bím tóc** (`braid`, con của đầu) lắc theo nhịp.

| File | Khung | durations_ms | hit_frame | Chân y | Alpha mép |
|---|---:|---|---:|---|---|
| `cungthu_nu_idle_2f.png` | 2 | 600, 600 | – | 620–620 | 0.0 % |
| `cungthu_nu_run_6f.png` | 6 | 90, 90, 90, 90, 90, 90 | – | 616–620 | 0.0 % |
| `cungthu_nu_ban_cung_7f.png` | 7 | 70, 120, 140, 160, 50, 120, 100 | 4 | 620–620 | 0.0 % |

- Xem: `contact.jpg`, `preview_*.gif` (có vạch chân và chữ HIT). Số liệu: `animations.json`.
- QC: mỗi ô 1 khối đặc, 0 mảnh rời. Riêng `run` nhấp nhô 4 px là cố ý.

## Giới hạn (Luna quyết)
1. Dây cung liền với cung (`hand_l_bow.png`) nên **không căng được khi kéo**, giống bản nam. Cần tách dây cung thành mảnh riêng hoặc thêm ảnh cung căng.
2. Ở góc nhìn thẳng, động tác kéo dây bị khuất nên biên độ nhìn thấy nhỏ.
3. Chỉ có bộ phận nhìn thẳng: chạy ngang trông như chạy tại chỗ; dáng quay lưng hoặc nhìn nghiêng cần thêm bộ phận.


## Đòn đánh thường (2026-11-29)
`cungthu_nu_attack_5f.png`: 5 khung, durations_ms [60, 90, 60, 110, 80] (tổng 400 ms), **hit_frame 2**. bắn thường: nâng cung + kéo dây nhanh → buông (tay phải bật ra sau, lùi 10 px) → theo đà → về.
- QC: mép ô alpha 0.0 %, 1 khối chính mỗi ô, chân y 620–620.
- Cùng tỉ lệ (0,95 quanh chân), cùng điểm chân và cùng bộ phận với idle/run, nên chuyển từ chạy sang đánh **không đổi người**.
- Xem: `preview_attack.gif`; so 6 hero: `../../attack_all_heroes.jpg`.


## Skill 2–4 và trúng đòn (2026-11-29)
| Skill | File | Khung | durations_ms | hit_frame | Alpha mép | Cách dựng |
|---|---|---:|---|---:|---|---|
| Liên Tiễn | `cungthu_nu_lien_tien_8f.png` | 8 | [60, 80, 50, 80, 50, 80, 50, 100] (550 ms) | 2 | 0.0 % | kéo–buông 3 lần liên tiếp (3 khung buông: 2, 4, 6; hit_frame = lần đầu) |
| Độc Tiễn | `cungthu_nu_doc_tien_6f.png` | 6 | [70, 120, 200, 60, 140, 100] (690 ms) | 3 | 0.0 % | ngắm lâu giữ dây 200 ms, buông mạnh |
| Vạn Tiễn | `cungthu_nu_van_tien_6f.png` | 6 | [80, 120, 160, 60, 160, 100] (680 ms) | 3 | 0.0 % | chĩa cung lên trời, kéo, buông (mưa tên) |
| Trúng đòn | `cungthu_nu_hurt_3f.png` | 3 | [80, 110, 110] (300 ms) | – | 0.0 % | bật lùi 14 px, đầu ngả, tay văng, rồi hồi |

- Cùng tỉ lệ, điểm chân và bộ phận với idle/run/attack. Mỗi ô 1 khối chính.
- **Giới hạn (Luna quyết):**
- Dây cung liền với cung nên không căng khi kéo (cả 3 skill).
- Liên Tiễn: game bắn 3 mũi ở các khung buông 2, 4, 6 (hit_frame ghi lần đầu).
