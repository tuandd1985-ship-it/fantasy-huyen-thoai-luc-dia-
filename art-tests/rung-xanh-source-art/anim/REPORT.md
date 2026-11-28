# Animation từ ảnh dáng chính Rừng Xanh (Kiếm Sĩ Nam + Goblin cận chiến)

GAME-ART-CORE (Claude), 2026-11-28. Nguồn: các file `../*.png` (commit 0211e4b). **Không sửa ảnh nguồn, không sửa source game.**

## 1. Kiểm tra ảnh nguồn
- Tách tự động đúng **5 dáng Kiếm Sĩ** và **4 dáng Goblin** theo các khối alpha, không dính nhau.
- **Ảnh ImageGen có 2 lỗi alpha, đã sửa:**
  1. Lõi nhân vật **không đặc**: alpha chỉ 251–254, nên trong game nhân vật sẽ hơi trong. Đã làm đặc về 255 (Kiếm Sĩ 408 867 px, Goblin 479 643 px).
  2. **Lớp mù alpha 1–30** phủ khoảng 4,5 % ảnh. Đã xoá (Kiếm Sĩ 70 267 px, Goblin 65 074 px). Giữ dải viền mịn 2 px sát thân.
- Kiểm tra trên nền đen, trắng và cỏ (`poses_on_3bg.jpg`): viền sạch, không quầng.
- Dáng đã làm sạch, cắt sát: `poses_kiemsi/` (idle, tram_kiem, kiem_vu, dia_chan, thien_kiem), `poses_goblin/` (idle, windup, swing, hit).

## 2. Cách dựng animation
- Dùng **nguyên nét vẽ của dáng chính**; khung trung gian chỉ là biến đổi của chính dáng đó: co giãn lấy đà, nghiêng, đẩy tới, giữ nhịp, bật nhảy. Riêng Kiếm Vũ **lật ngang xen kẽ** để tạo cảm giác xoay người. Không có AI vẽ lại, nên mặt, giáp và vũ khí giữ đúng 100 %.
- **Ô 768×640, chân ở y = 620** ở mọi khung (sau khi nghiêng/co giãn đều đặt lại chân về đường này). Ô 420×500 của dải hiện tại không chứa được kiếm ngang của Kiếm Vũ và kiếm giơ cao của Thiên Kiếm.
- **Cỡ**: Kiếm Sĩ giữ đúng tỉ lệ với dải k13 đang chạy (dáng đứng cao 476 px kể cả kiếm giơ). Trong game vẽ ô cao = chiều cao hero × 640/476. Goblin: dáng đứng cao 500 px.
- **Không vẽ cứng hiệu ứng**: hiệu ứng skill có sẵn trong game (nứt đất Địa Chấn, tia lửa Kiếm Vũ, đại kiếm Thiên Kiếm) vẫn do code vẽ. File chỉ chứa nhân vật.
- **Thời gian + khung gây sát thương** nằm trong `animations.json` (`durations_ms`, `hit_frame`, `total_ms`) để Luna khớp với logic sát thương và hồi chiêu.

## 3. Sản phẩm
| File | Khung | Tổng (ms) | Khung gây sát thương | Diễn tiến |
|---|---:|---:|---:|---|
| `kiemsi_nam_idle_2f.png` | 2 | 1200 | – | Đứng thủ thế, thở |
| `kiemsi_nam_tram_kiem_6f.png` | 6 | 520 | 3 | Lấy đà ngả sau → chém chéo → đẩy tới → giữ → về |
| `kiemsi_nam_kiem_vu_7f.png` | 7 | 550 | 1 | Lấy đà → xoay kiếm ngang 4 nhịp (lật trái/phải) → về |
| `kiemsi_nam_dia_chan_7f.png` | 7 | 730 | 3 | Giơ kiếm bật lên (dùng dáng Thiên Kiếm) → cắm kiếm xuống đất (nén người) → giữ → về |
| `kiemsi_nam_thien_kiem_7f.png` | 7 | 900 | 4 | Giơ kiếm lên trời, bay lên, giữ (lúc gọi đại kiếm) → chém xuống → về |
| `goblin_melee_idle_2f.png` | 2 | 1000 | – | Đứng thở |
| `goblin_melee_attack_6f.png` | 6 | 640 | 3 | Đứng → giơ chuỳ ra sau → lấy đà mạnh → vung tới → theo đà → về |
| `goblin_melee_hit_3f.png` | 3 | 320 | – | Bật lùi nhăn mặt → hồi → đứng |
| `goblin_melee_strip_6f.png` | 6 | – | – | Dải 6 ô kiểu hero: [idle1, idle2, windup, swing, swing_follow, hit] |

- Xem nhanh: `contact_all.jpg` (mọi dải), `preview_<nhân vật>_<hành động>.gif` (đúng thời gian thật, chữ HIT đánh dấu khung gây sát thương, vạch vàng là đường chân).

## 4. QC (`animations.json` → `qc`)
| Tiêu chí | Kết quả |
|---|---|
| Mỗi ô đúng 1 nhân vật | Mỗi ô 1 khối đặc, 0 mảnh rời ≥ 30 px |
| Alpha ở dải mép ô | **0 %** mọi ô (sau khi nới ô 768 px và dịch các khung Kiếm Vũ ±40 px) |
| Chân thẳng hàng | y = 620 mọi khung, trừ khung **bật nhảy cố ý**: Địa Chấn 610/604, Thiên Kiếm 614/606 |
| Mặt, giáp, vũ khí | Giữ đúng nét gốc |

## 5. Lưu ý cho Luna
1. Game hiện chọn khung qua `animFrame()` trên dải 6 ô 420×500. Muốn dùng các dải skill này cần một đường vẽ theo hành động (skill id → file, `durations_ms`, `hit_frame`), vẽ ô theo tỉ lệ 640/476.
2. **Kiếm Vũ dùng lật ngang** nên ở khung lật, mặt, kiếm và áo choàng cũng bị lật; ở tốc độ 70 ms/khung trông như xoay người. Nếu cần xoay thật phải có thêm dáng nhìn từ sau (ảnh nguồn chưa có).
3. **Vũ khí đổi tay/hướng giữa các dáng** (README đã báo): Trảm Kiếm cầm hai tay chém xuống phải, Kiếm Vũ cầm tay trái chĩa ngang. Nối tiếp nhanh thì không lộ.
4. Chỉ có một góc 3/4 quay phải; hướng trái game tự lật như hiện tại.
5. **Ảnh map tham chiếu** (sông dọc, một cầu ngang, hai bãi cỏ) có bố cục khác `map_1` hiện dùng (nhiều nhánh sông, 7 cầu). Màu trầm, đúng ART_DIRECTION, hero sẽ nổi. Em **chưa xử lý** ảnh này. Nếu Luna muốn dùng làm sân chơi thì cần: nâng phân giải (×2 → khoảng 3344×1882) + tách lớp cây/tàn tích như pilot `maps-anh-do/layers` + lưới va chạm mới.

## Tái lập
`python tools/keypose_strips.py <thư mục ảnh nguồn> <out>` (cần `tools/mage_anim_compose.py`). Chạy khoảng 10 giây.
