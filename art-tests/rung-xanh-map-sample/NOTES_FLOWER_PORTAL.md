# Ghi chú: khóm hoa và đá cổng dịch chuyển (theo đánh giá Luna 2026-11-28)

## Khóm hoa
- **Giữ nguyên bản hiện tại**, không sửa để ép ΔE. Luna đã chấp nhận phần viền và matte.
- **Bổ sung art-qc profile `multicolor`** (`tools/gac_matte.py`, `judge(m, profile="multicolor")`) cho vật thể đa sắc:
  - **Không chấm** ΔE sắc độ viền-lõi; vẫn ghi số đo để tham khảo.
  - **Chấm**: lõi đặc, lỗ lõi, đảo rời, chạm mép, **edge spill/fringe** (`edge_cast`); quầng xám nếu sinh trên nền xám.
  - **Bắt buộc duyệt bằng mắt** trên contact sheet 3 nền (đen, trắng, cỏ).
  - Chấm lại khóm hoa hiện tại theo profile này: **ĐẠT toàn bộ** (edge_cast 0,02 %, quầng xám 2,73 % < 3 %).
- **Khóm hoa v2** chỉ làm sau khi tile v2 được chốt: thảm hoa thấp sát đất, hoa nhỏ, thưa và ít màu, không giống bó hoa hay icon, không có va chạm.

## Đá cổng dịch chuyển: giữ nguồn, chưa tách bản cuối
- File nguồn: `props_raw/da_cong_dich_chuyen_s728105.png` (SDXL gốc) và `props_clean/da_cong_dich_chuyen.png` (965×994, đã matte-clean, 1 khối liền).
- Hai vùng, tọa độ trên `props_clean/da_cong_dich_chuyen.png`:

| Vùng | Tên xuất dự kiến | Phạm vi y (ước lượng) | Vai trò lớp |
|---|---|---|---|
| Vòm, cổng đá phía sau | `portal_back` | khoảng 13 đến 520 (chỗ thắt hẹp nhất là y ≈ 520) | vẽ **sau** nhân vật |
| Bệ tròn phía trước, dưới | `portal_platform` | khoảng 520 đến 980 | vẽ **dưới chân** hoặc trước nhân vật, tùy hợp đồng |

- Hai vùng dính liền nhau ở chân vòm, không phải 2 mảnh rời. Đường cắt cuối phải theo mép bệ, không cắt thẳng ngang.
- **Chờ hợp đồng layer/anchor của Codex.** Khi có, sẽ xuất 2 PNG `portal_back` và `portal_platform` cùng kích thước khung, cùng group ID và anchor, để ghép lại khớp từng pixel.
