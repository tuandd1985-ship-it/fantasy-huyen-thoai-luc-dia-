# Kiếm Sĩ Nam: lắp ghép chuyển động từ bộ phận của Codex

GAME-ART-CORE (Claude), 2026-11-28. Nguồn: `../` (14 bộ phận, commit 47f322b). **Chỉ xoay và dịch bộ phận quanh điểm trục trong `parts.json`; không vẽ thêm, không dùng AI vẽ lại.** Không sửa source game.

## 1. Kiểm tra ghép chồng (`overlay_check.png`)
Xếp 14 PNG theo `z` ở dáng gốc, so với `assembled.png`:
- **Lệch khung bao: 0 px** (cả 4 cạnh); IoU alpha **1,000**; chênh màu **0,00/255**; **0 px** lệch alpha.
- Kết luận: `parts.json` + PNG khớp tuyệt đối với `assembled.png`.

## 2. Ba chuyển động
Ô 768×640, chân y = 620. Dùng nguyên canvas của Codex, **thu nhỏ đều 0,95 quanh điểm chân**: canvas gốc chỉ chừa 10 px phía trên chỏm lông, nên khi nhân vật nhún lên hoặc vung kiếm sẽ chạm mép ô. Cây khớp đúng `parent` của Codex (thân → đầu, tay, chân, choàng; tay phải → cẳng tay → bàn tay + kiếm). Chân luôn được đặt lại chạm đất sau khi xoay.

| File | Khung | durations_ms | hit_frame | Cách dựng |
|---|---:|---|---:|---|
| `kiemsi_nam_idle_2f.png` | 2 | 600, 600 | – | Thân ngả nhẹ, đầu và hai tay nhích 1,5–2,5°, choàng đung đưa |
| `kiemsi_nam_run_6f.png` | 6 | 6 × 90 | – | Đùi ±24°, cẳng chân gập 10–20°, tay trái đánh ±26° ngược chân, tay kiếm lắc nhẹ, choàng bay sau, nhấp 4 px |
| `kiemsi_nam_tram_kiem_8f.png` | 8 | 60, 90, 90, 50, 110, 120, 90, 90 | 4 | Lấy đà: tay kiếm vòng ra sau đầu → chém chéo xuống, đẩy người tới 46–48 px → giữ → về |

- Xem nhanh: `contact.jpg`, `preview_idle.gif`, `preview_run.gif`, `preview_tram_kiem.gif` (chạy đúng thời gian, có vạch chân và chữ HIT).
- Số liệu và QC từng ô: `animations.json`.

## 3. QC
| Tiêu chí | Kết quả |
|---|---|
| Mỗi ô 1 nhân vật | 1 khối đặc ở mọi ô, 0 mảnh rời |
| Mép ô | Alpha **0 %** ở 16/16 ô |
| Chân | idle, tram_kiem: y 619–620; run: 616–620 (nhấp nhô khi chạy là cố ý) |
| Khớp khi xoay | Không hở ở vai, khuỷu, cổ tay, hông, gối (`joints_zoom.jpg`, khung chém và khung chạy biên độ lớn nhất) |

## 4. Giới hạn: dáng KHÔNG đạt được chỉ bằng xoay bộ phận (Luna quyết)
1. **Lấy đà Trảm Kiếm**: để kiếm vòng ra sau đầu, em đổi thứ tự vẽ tay kiếm xuống dưới đầu trong 2 khung lấy đà (`z` theo khung, xem `motions_kiemsi_codex.json`). Khi đó **lưỡi kiếm gần như bị đầu che hết**, chỉ lộ mũi kiếm. Muốn thấy rõ kiếm giơ cao phía trên đầu cần **bàn tay + kiếm ở góc cầm khác** (lưỡi hướng lên/ra sau). Xoay bộ phận hiện có chỉ cho ra lưỡi nằm sau đầu hoặc đè lên mặt.
2. **Chạy**: nhân vật vẫn **nhìn thẳng ra trước** vì chỉ có dáng chính diện. Chạy sang ngang trông như chạy tại chỗ, game phải lật ngang. Chạy ngang thật cần bộ phận **nhìn nghiêng**.
3. **Chân chibi ngắn** bị váy giáp che phần đùi, nên bước chân nhìn thấy chủ yếu ở cẳng chân và bàn chân.
4. **Đòn chém ngang/xoay người (Kiếm Vũ), nhìn từ sau, quay lưng**: không làm được bằng bộ phận chính diện; cần thêm bộ phận nhìn nghiêng hoặc nhìn sau.
5. Như REPORT của Codex: nắm tay cầm kiếm to hơn và áo choàng xoè hơn ảnh đang dùng trong game. Em giữ nguyên, không chỉnh.

## Tái lập
`python tools/parts_rig.py .. tools/motions_kiemsi_codex.json <out>` (khoảng 20 giây).
- File chuyển động là JSON khung khoá: góc từng bộ phận, dịch gốc, thứ tự vẽ theo khung.
- **Dùng lại được cho nhân vật khác có cùng tên bộ phận.**


## Đòn đánh thường (2026-11-29)
`kiemsi_nam_attack_5f.png`: 5 khung, durations_ms [70, 80, 60, 100, 90] (tổng 400 ms), **hit_frame 2**. chém thường: nâng kiếm lên vai → chém chéo xuống, đẩy người tới 26 px → theo đà → về.
- QC: mép ô alpha 0.0 %, 1 khối chính mỗi ô, chân y 620–620.
- Cùng tỉ lệ (0,95 quanh chân), cùng điểm chân và cùng bộ phận với idle/run, nên chuyển từ chạy sang đánh **không đổi người**.
- Xem: `preview_attack.gif`; so 6 hero: `../../attack_all_heroes.jpg`.
