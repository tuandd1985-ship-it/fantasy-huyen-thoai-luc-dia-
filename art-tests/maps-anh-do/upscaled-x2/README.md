# Map của anh Do: nâng phân giải + chỉnh màu, sẵn sàng thay vào game (×2)

GAME-ART-CORE (Claude), 2026-11-28. Không sửa source game.

## Là gì
15 map trong `../map/` (bỏ `tanthu1` vì trùng ảnh với `tanthu`) được xử lý như sau:
1. **Nâng phân giải 4× bằng Upscayl** có sẵn trên máy anh Do: `upscayl-bin`, model `digital-art-4x`, chạy GPU khoảng 6–7 s mỗi map. `upscaler_models_compare.jpg` so 3 model với cách kéo giãn ×2 hiện tại; `digital-art-4x` cho nét sạch, hợp tranh cel nhất.
2. **Hạ về đúng ×2 kích thước gốc**: 1402×1122 → **2804×2244** (bằng thế giới Rừng Xanh v0.5.0); 1536×1024 → 3072×2048.
   - **Hình học giữ nguyên tuyệt đối** so với ảnh gốc kéo giãn ×2, nên lưới va chạm 100×80 Luna đã phân tích cho `map_1` **vẫn khớp**; chỉ thay ảnh nền.
3. **Chỉnh màu theo ART_DIRECTION** (nền map trầm, nhân vật nổi bật hơn), làm trong không gian OKLab:
   - Giảm độ rực màu nền (cỏ, đất vàng, ô liu) còn 62 %, màu khác còn 80 %.
   - Giữ 92 % độ rực của **điểm sáng phép** (pha lê, dung nham, băng phát sáng, cổng) để phép thuật vẫn nổi.
   - Nén tương phản nhẹ. Hạ độ sáng trung bình của map sáng xuống khoảng 138 (map tuyết khoảng 158), thấp hơn hero (131–135 trên mặt hero).
4. Xuất **WebP q90**, mỗi file 0,9–2,1 MB.

`compare/<map>_before_after.jpg`: hàng trên là toàn map trước/sau; hàng dưới là một khung màn hình 640×480 ở tỉ lệ thế giới, có Kiếm Sĩ cao 150 px.

## Số đo (`maps_report.json`)
| Map | Kích thước game | Độ rực TB trước → sau | Độ sáng TB trước → sau |
|---|---|---|---|
| map_1 (Rừng Xanh, đang dùng) | 2804×2244 | 0,66 → 0,46 | 159 → 135 |
| map_2 / map_3 | 2804×2244 | 0,69 → 0,44 / 0,56 → 0,41 | 152 → 136 / 162 → 134 |
| map_4 (tuyết) | 2804×2244 | 0,26 → 0,26 | 193 → 154 |
| map_5 (dung nham + tuyết) | 2804×2244 | 0,64 → 0,55 | 77 → 70 |
| tanthu (làng) | 3072×2048 | 0,64 → 0,43 | 129 → 120 |
| hang1–3 (hang nhìn từ trên) | 2804×2244 | 0,52–0,71 → 0,40–0,62 | giảm 8–10 % |
| hang4–6 (hang nhìn ngang) | 3072×2048 | 0,59–0,87 → 0,53–0,83 | giảm khoảng 10 % |
| boss_bang / bosslua / bossxuan | 2804×2244 | 0,68 / 0,49 / 0,23 → 0,62 / 0,42 / 0,19 | giảm 8–14 % |

Map tối (hang, dung nham) có chỉ số "độ rực" cao vì công thức HSV khuếch đại màu tối. Nên đánh giá bằng ảnh `compare/`.

## Tỉ lệ chibi
`world_scale_x2_vs_x3.jpg` so khung màn hình ở thế giới ×2 và ×3 với hero 150 px:
- **×2**: cây, pha lê, cầu gỗ cân với hero chibi, chạy chéo map khoảng 20–24 s như Luna đo. **Đề xuất giữ ×2.**
- **×3** (4206×3366): vật thể to hơn, map "gần" hơn, chạy lâu hơn khoảng 1,5 lần. Nếu Luna muốn, em xuất lại từ bản 4× gốc mà không cần nâng phân giải lại.

Bản 4× gốc (5608×4488, khoảng 35 MB/map) giữ ở máy: `C:\AI\GAME-ART-CORE\output\maps\up4\`.

## Tái lập
`python tools/maps_upscale_grade.py <thư mục map> <out> <hero.png>`. Tham số chỉnh màu nằm ở đầu file.
