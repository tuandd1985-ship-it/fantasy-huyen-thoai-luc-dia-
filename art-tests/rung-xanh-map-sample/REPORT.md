# REPORT: Mẫu map Rừng Xanh (SDXL Base có sẵn, không dùng model mới)

GAME-ART-CORE (Claude) · 2026-11-28 · Model `sd_xl_base_1.0.safetensors` có sẵn, chỉ dùng node gốc của ComfyUI, không tải gì, không cài gì. Tách nền dùng quy trình **matte-clean** đã chốt ở Bước A (BiRefNet có sẵn, chạy CPU).

## Kết luận nhanh
- **Tile cỏ 1024² liền mạch: ĐẠT về kỹ thuật**, ghép 2×2 không thấy đường nối. Độ chênh ở mép nối so với chênh trung bình bên trong: ngang 1,17, dọc 0,85; xấp xỉ 1 nghĩa là liền.
- **Về phong cách: CHƯA ĐẠT.** Tile quá rực, nhiều hoa hồng li ti và nét cỏ gần ảnh thật. Trong ảnh ghép, hero chưa nổi bật nhất khung (trái ART_DIRECTION). Cần làm lại tông trầm hơn và ít hoa (xem mục "Chưa đạt").
- **6 vật thể: 5/6 đạt toàn bộ QC**, 6/6 không còn quầng xám ở viền (< 3 %). Khóm hoa trượt chỉ số ΔE sắc độ viền (15,8), vì hoa nhiều màu sát mép; kiểm tra bằng mắt thấy viền sạch.
- Thời gian: sinh 19 ảnh (1 tile, 1 lượt sửa đường nối, 18 ứng viên vật thể) mỗi ảnh khoảng 17–20 s; tách nền + QC 6 vật thể trên CPU khoảng 10 phút.

## Cách làm
1. **Tile**: sinh 1024² với prompt tile của PROMPT_LIBRARY mục 6. Dịch ảnh nửa chu kỳ để đường nối dồn vào giữa, inpaint dải chữ thập 96 px (denoise 0,7, chỉ node `SetLatentNoiseMask` có sẵn), rồi trộn mềm vào ảnh.
2. **Vật thể**: sinh trên nền xám nhạt (không ghi màu sặc sỡ cho nền), 2–3 seed mỗi món, chọn bản tốt nhất. Đá cổng và bụi cây phải sinh lại với prompt chặt hơn, vì lần đầu ra bảng nhiều mảnh hoặc ra dáng cây con.
3. **Matte-clean**: BiRefNet → alpha → **khử màu nền theo toán học với nền xám đã biết**, F = (I − (1−α)·B)/α (mục 4 bước 4). Pixel có alpha < 0,25 lấy màu đặc lân cận → xóa đốm → làm đặc lõi → khử màu viền → cắt sát nội dung, chừa 12 px.

## Kết quả QC (ngưỡng ART_PRODUCTION_PLAN mục 7 + chỉ số quầng xám < 3 %)

| Vật thể | Seed | Lõi đặc % (≥ 99) | Lỗ lõi | Đảo rời | Chạm mép | Quầng xám % trước → sau | Ám magenta % | ΔE sắc độ viền (< 12) | Mảng đặc | Kích thước cắt | Kết quả |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Cây sồi | 728102 | 99,999 | 0 | 0 | không | 0,19 → 0,62 | 0 | 7,9 | 1 | 882×1020 | ĐẠT |
| Tảng đá rêu | 728102 | 99,987 | 0 | 0 | không | 4,89 → 1,28 | 0 | 8,9 | 4 | 853×713 | ĐẠT |
| Cột đá cổ | 728101 | 99,996 | 0 | 0 | không | 2,40 → 0,47 | 0 | 7,6 | 4 | 695×1024 | ĐẠT |
| Bụi cây | 728104 | 100 | 0 | 0 | không | 0,65 → 0,40 | 0 | 10,7 | 1 | 1010×921 | ĐẠT |
| Khóm hoa | 728101 | 99,953 | 0 | 0 | không | 2,59 → 2,73 | 0,02 | **15,8 ✗** | 12 | 921×970 | trượt ΔE sắc độ viền |
| Đá cổng dịch chuyển | 728105 | 99,998 | 0 | 0 | không | 2,42 → 2,54 | 0,03 | 5,5 | 1 | 965×994 | ĐẠT |

"Mảng đặc" lớn hơn 1 là các mảnh nhỏ tách rời có chủ đích: lá rơi, vụn đá, cánh hoa. Chúng đều nhỏ hơn 0,3 % diện tích nên không bị tính là đảo rời. Số đo đầy đủ ở `qc.json`; prompt, seed và thời gian từng ảnh ở `generation.json`.

## Ảnh để duyệt
- `scene_test_1280x720.jpg`: **ảnh ghép thử** ở khung 1280×720. Tile lặp ở cỡ 384 px, vật thể đặt theo thứ tự chiều sâu 2.5D, bóng elip do code vẽ (như game). Có **Kiếm Sĩ Nam (bản đã làm sạch ở Bước A) cao 150 px** để so tỉ lệ.
- `props_on_backgrounds.jpg`: 6 vật thể trên nền đen, trắng và cỏ, để soi viền.
- `tile_2x2_check.jpg`: tile lặp 2×2 để kiểm tra đường nối.

## Đã đạt
- Vật thể đồng bộ một phong cách: vẽ tay, viền đậm, góc 3/4 từ trên xuống, hợp với hero chibi.
- Viền sạch trên cả 3 nền; không quầng xám, không ám magenta; lõi đặc, không lỗ.
- Tile liền mạch thật, quy trình chỉ dùng node gốc.
- Màu xanh lục ngọc của đá cổng còn giữ được dù đi qua bước tách nền.

## Chưa đạt / vấn đề còn tồn tại
1. **Tile cỏ quá rực và nhiều chi tiết**: độ sáng TB 80/255 nhưng bão hòa cao, hoa hồng dày đặc, nét cỏ gần ảnh thật. Kết quả là nền tranh chú ý với hero và vật thể. Đề xuất làm lại: prompt `soft painted grass, muted green, sparse tiny flowers, low contrast` cộng giảm bão hòa khoảng 20 % bằng script; hoặc dựng tile từ 2–3 lớp màu phẳng có vân nhẹ.
2. **Khóm hoa**: ΔE sắc độ viền 15,8 > 12 (hoa vàng, trắng, hồng sát mép nên chỉ số đo cao); bằng mắt viền sạch. Món này cũng **trùng màu với hoa trong tile**, nên ở cỡ 60 px gần như lẫn vào nền.
3. **Đá cổng dịch chuyển** gồm 2 phần: cổng đá phía sau và bệ tròn phía trước. Cần Codex xác nhận engine có vẽ được dạng 2 lớp (cổng sau nhân vật, bệ dưới chân) hay muốn 1 khối.
4. **Cây sồi** có sẵn vệt rễ tối dưới gốc, có thể trùng với bóng elip do code vẽ. Nên sinh lại với `no ground, no shadow` nếu Luna muốn bóng hoàn toàn do code.
5. Kích thước vật thể trong ảnh ghép là em tự đề xuất (cây 300 px, cột 220 px, đá cổng 200 px, tảng đá 110 px, bụi 95 px, khóm hoa 60 px, so với hero 150 px). Cần Luna/Codex chốt cùng footprint va chạm.
6. Chưa có lớp đường, sông, cầu, lớp xa/gần; chưa đưa vào game.

## Thư mục
| Đường dẫn | Nội dung |
|---|---|
| `tile_co_rung_xanh_1024.png` | Tile liền mạch |
| `props_clean/*.png` | 6 vật thể RGBA đã tách nền và cắt sát |
| `props_raw/*.png` | Ảnh gốc SDXL của 6 bản được chọn |
| `scene_test_1280x720.jpg`, `props_on_backgrounds.jpg`, `tile_2x2_check.jpg` | Ảnh duyệt |
| `qc.json`, `generation.json` | Số đo QC; prompt, seed, thời gian |
| `tools/` | `comfy_api.py`, `gen_rung_xanh_map.py`, `process_map_props.py`, `gac_matte.py` |
