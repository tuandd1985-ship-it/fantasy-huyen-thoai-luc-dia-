# Cung Thủ Nam: lắp ghép chuyển động từ bộ phận của Codex

GAME-ART-CORE (Claude), 2026-11-28. Nguồn: `../` (15 bộ phận, commit 3255cd9). **Chỉ xoay và dịch bộ phận quanh điểm trục; không vẽ thêm.** Không sửa source game.

## Kiểm tra ghép chồng (`overlay_check.png`)
**Lệch khung bao 0 px, IoU alpha 1,000, chênh màu 0, 0 px lệch** → khớp tuyệt đối với `assembled.png`.

## Chuyển động
Ô 768×640, chân y = 620, thu nhỏ 0,95 quanh chân.

| File | Khung | durations_ms | hit_frame | Cách dựng |
|---|---:|---|---:|---|
| `cungthu_nam_idle_2f.png` | 2 | 600, 600 | – | Đầu, tay, áo choàng, ống tên nhích nhẹ |
| `cungthu_nam_run_6f.png` | 6 | 6 × 90 | – | Chân bước xen kẽ, tay phải đánh, áo choàng + ống tên lắc, nhấp 4 px |
| `cungthu_nam_ban_cung_7f.png` | 7 | 70, 120, 140, 160, 50, 120, 100 | 4 | Nâng cung → tay phải đưa lên ngực (kéo dây) → giữ ngắm → **buông**: tay phải bật ra sau, cung giật nhẹ, người lùi 10 px → về |

## QC
- Mép ô alpha **0 %** ở 15/15 ô; mỗi ô 1 khối; chân y 616–620.
- Điểm gắn ống tên (Codex ghi là khớp chồng ít nhất) không hở, vì ống tên chỉ lắc ±4°.

## Giới hạn (Luna quyết)
1. **Không thể hiện được dây cung căng**: dây cung vẽ liền với cung (`hand_l_bow.png`), nên khi kéo, dây vẫn thẳng, tay phải chỉ đưa tới gần dây. Muốn thấy dây căng cần Codex tách **dây cung thành mảnh riêng** (hoặc thêm một ảnh cung ở trạng thái căng để đổi khung).
2. **Không có mũi tên** trên tay; mũi tên bay ra để game vẽ như hiện tại.
3. Ở góc nhìn thẳng, động tác kéo cung ngắn và kín (tay phải che sau ngực, đầu); biên độ nhìn thấy nhỏ hơn Kiếm Sĩ hoặc Pháp Sư. Dáng ngắm nghiêng cần bộ phận nhìn nghiêng.
4. Như REPORT của Codex: tay cầm cung duỗi hơn, mũ và tà áo choàng rộng hơn ảnh trong game.


## Đòn đánh thường (2026-11-29)
`cungthu_nam_attack_5f.png`: 5 khung, durations_ms [60, 90, 60, 110, 80] (tổng 400 ms), **hit_frame 2**. bắn thường: nâng cung + kéo dây nhanh → buông (tay phải bật ra sau, lùi 10 px) → theo đà → về.
- QC: mép ô alpha 0.0 %, 1 khối chính mỗi ô, chân y 619–620.
- Cùng tỉ lệ (0,95 quanh chân), cùng điểm chân và cùng bộ phận với idle/run, nên chuyển từ chạy sang đánh **không đổi người**.
- Xem: `preview_attack.gif`; so 6 hero: `../../attack_all_heroes.jpg`.


## Skill 2–4 và trúng đòn (2026-11-29)
| Skill | File | Khung | durations_ms | hit_frame | Alpha mép | Cách dựng |
|---|---|---:|---|---:|---|---|
| Liên Tiễn | `cungthu_nam_lien_tien_8f.png` | 8 | [60, 80, 50, 80, 50, 80, 50, 100] (550 ms) | 2 | 0.0 % | kéo–buông 3 lần liên tiếp (3 khung buông: 2, 4, 6; hit_frame = lần đầu) |
| Độc Tiễn | `cungthu_nam_doc_tien_6f.png` | 6 | [70, 120, 200, 60, 140, 100] (690 ms) | 3 | 0.0 % | ngắm lâu giữ dây 200 ms, buông mạnh |
| Vạn Tiễn | `cungthu_nam_van_tien_6f.png` | 6 | [80, 120, 160, 60, 160, 100] (680 ms) | 3 | 0.0 % | chĩa cung lên trời, kéo, buông (mưa tên) |
| Trúng đòn | `cungthu_nam_hurt_3f.png` | 3 | [80, 110, 110] (300 ms) | – | 0.0 % | bật lùi 14 px, đầu ngả, tay văng, rồi hồi |

- Cùng tỉ lệ, điểm chân và bộ phận với idle/run/attack. Mỗi ô 1 khối chính.
- **Giới hạn (Luna quyết):**
- Dây cung liền với cung nên không căng khi kéo (cả 3 skill).
- Liên Tiễn: game bắn 3 mũi ở các khung buông 2, 4, 6 (hit_frame ghi lần đầu).
