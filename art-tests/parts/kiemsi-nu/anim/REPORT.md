# Kiếm Sĩ Nữ: lắp ghép chuyển động từ bộ phận của Codex

GAME-ART-CORE (Claude), 2026-11-28. Nguồn: `../` (15 bộ phận, commit e804ac3). **Chỉ xoay và dịch bộ phận quanh điểm trục trong `parts.json`; không vẽ thêm, không dùng AI vẽ lại.** Không sửa source game.

## Kiểm tra ghép chồng (`overlay_check.png`)
- Lệch khung bao **[0, 0, 0, 0]** px.
- IoU alpha **1.0**, chênh màu **0.0**, lệch alpha **0** px.
- Kết luận: khớp tuyệt đối với `assembled.png`.

## Chuyển động
Ô 768×640, chân y = 620, thu nhỏ 0,95 quanh chân. Dùng lại bộ chuyển động của bản nam: cùng tên bộ phận, cùng thời lượng và khung gây sát thương, nên game dùng chung logic. **Tóc đuôi ngựa** (`ponytail`, con của đầu) lắc ngược nhịp đầu/thân và theo áo choàng.

| File | Khung | durations_ms | hit_frame | Chân y | Alpha mép |
|---|---:|---|---:|---|---|
| `kiemsi_nu_idle_2f.png` | 2 | 600, 600 | – | 620–620 | 0.0 % |
| `kiemsi_nu_run_6f.png` | 6 | 90, 90, 90, 90, 90, 90 | – | 616–620 | 0.0 % |
| `kiemsi_nu_tram_kiem_8f.png` | 8 | 60, 90, 90, 50, 110, 120, 90, 90 | 4 | 620–620 | 0.0 % |

- Xem: `contact.jpg`, `preview_*.gif` (có vạch chân và chữ HIT). Số liệu: `animations.json`.
- QC: mỗi ô 1 khối đặc, 0 mảnh rời. Riêng `run` nhấp nhô 4 px là cố ý.

## Giới hạn (Luna quyết)
1. Lấy đà Trảm Kiếm: kiếm vòng ra sau đầu bị **đầu và tóc đuôi ngựa che gần hết** (giống bản nam). Cần bàn tay + kiếm ở góc cầm khác nếu muốn thấy rõ kiếm giơ cao.
2. Như Codex lưu ý: tay cầm kiếm và áo choàng lớn hơn ảnh trong game.
3. Chỉ có bộ phận nhìn thẳng: chạy ngang trông như chạy tại chỗ; dáng quay lưng hoặc nhìn nghiêng cần thêm bộ phận.


## Đòn đánh thường (2026-11-29)
`kiemsi_nu_attack_5f.png`: 5 khung, durations_ms [70, 80, 60, 100, 90] (tổng 400 ms), **hit_frame 2**. chém thường: nâng kiếm lên vai → chém chéo xuống, đẩy người tới 26 px → theo đà → về.
- QC: mép ô alpha 0.0 %, 1 khối chính mỗi ô, chân y 620–620.
- Cùng tỉ lệ (0,95 quanh chân), cùng điểm chân và cùng bộ phận với idle/run, nên chuyển từ chạy sang đánh **không đổi người**.
- Xem: `preview_attack.gif`; so 6 hero: `../../attack_all_heroes.jpg`.


## Skill 2–4 và trúng đòn (2026-11-29)
| Skill | File | Khung | durations_ms | hit_frame | Alpha mép | Cách dựng |
|---|---|---:|---|---:|---|---|
| Kiếm Vũ | `kiemsi_nu_kiem_vu_7f.png` | 7 | [80, 70, 70, 70, 70, 90, 100] (550 ms) | 2 | 0.0 % | quét kiếm ngang trước người 2 vòng, áo choàng tung, đẩy người 10–18 px |
| Địa Chấn | `kiemsi_nu_dia_chan_7f.png` | 7 | [80, 120, 90, 60, 160, 110, 100] (720 ms) | 3 | 0.0 % | giơ kiếm ra sau đầu, bật lên 26 px, bổ xuống cắm đất (mũi kiếm chạm thấp hơn đường chân ~10 px là cố ý), giữ |
| Thiên Kiếm | `kiemsi_nu_thien_kiem_7f.png` | 7 | [90, 100, 160, 200, 80, 140, 110] (880 ms) | 4 | 0.0 % | giơ kiếm lên, bay lên 22–24 px, giữ 360 ms (lúc gọi đại kiếm), chém xuống |
| Trúng đòn | `kiemsi_nu_hurt_3f.png` | 3 | [80, 110, 110] (300 ms) | – | 0.0 % | bật lùi 14 px, đầu ngả, tay văng, rồi hồi |

- Cùng tỉ lệ, điểm chân và bộ phận với idle/run/attack. Mỗi ô 1 khối chính.
- **Giới hạn (Luna quyết):**
- Chỉ có bộ phận nhìn thẳng: **Kiếm Vũ không xoay người được**, thể hiện bằng quét kiếm ngang 2 vòng + áo choàng tung. Muốn xoay thật cần bộ phận nhìn nghiêng/sau.
- **Thiên Kiếm**: kiếm giơ lên chỉ tới góc chéo trước mặt; dựng kiếm thẳng đứng trên đầu cần bàn tay + kiếm ở góc cầm khác (đầu sẽ che nếu vòng ra sau).
