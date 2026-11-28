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
