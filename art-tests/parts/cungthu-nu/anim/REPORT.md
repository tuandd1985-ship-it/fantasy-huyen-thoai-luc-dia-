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
