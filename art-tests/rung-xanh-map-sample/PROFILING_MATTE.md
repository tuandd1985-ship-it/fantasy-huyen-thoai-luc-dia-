# Profiling và tối ưu matte-clean (2026-11-28)

Đo trên 1 vật thể 1024² (`cay_soi`, CPU, cùng máy), lặp lại trên `khom_hoa` cho kết quả tương tự.

## Thời gian từng bước, một vật thể
| Bước | Trước | Sau | Ghi chú |
|---|---:|---:|---|
| 1. BiRefNet (ONNX, CPU) | ~50 s (+9 s nạp model lần đầu) | ~50 s | Chưa đổi. Suy luận model cố định 1024², không giảm được nếu không có GPU ONNX (sẽ phải cài thêm, nên không làm) |
| 2. Khử màu nền đã biết (unmix) | 11,6 s | **0,9 s** | |
| 3. QC trước làm sạch | 16,4 s | **2,6 s** | Chỉ để so trước/sau; có thể bỏ khi sản xuất |
| 4. Làm sạch (clean) | 16,9 s | **2,9 s** | |
| 5. QC sau làm sạch | 16,3 s | **2,5 s** | |
| 6. Quầng xám | 0,2 s | 0,2 s | |
| **Tổng / vật thể** | **~120 s** | **~59 s** | 6 vật thể: ~12 phút → ~6 phút |

Riêng phần màu tham chiếu (bước 2–5): **61 s → 8,9 s, nhanh khoảng 6,9 lần.**

## Nguyên nhân và cách sửa
- **Nguyên nhân**: cProfile cho thấy 54 s nằm ở `scipy.ndimage.correlate`, chủ yếu từ `local_ref_color` và `local_allowed_spill`. Hai hàm này tích chập trực tiếp với đĩa bán kính 6, 12, 24 px (đĩa 24 px có 1 809 phần tử mỗi pixel), làm 4 kênh × 3 bán kính, và bị gọi 4 lần cho mỗi vật thể.
- **Cách sửa**: chuyển sang **tích chập FFT** (`scipy.signal.fftconvolve`), cùng phép toán và cùng đệm số 0, gộp 4 kênh vào 1 lần gọi.
  - Kênh đếm pixel tham chiếu được làm tròn về số nguyên, để các phép thử `count > 0` giữ đúng như tích chập trực tiếp.
  - **Không đổi tham số, bán kính hay ngưỡng nào.**

## Kiểm tra không giảm chất lượng viền (`tools/verify_fft_equivalence.py`)
| Vật thể | Pixel khác / 1 048 576 | Chênh lớn nhất | QC sau làm sạch |
|---|---:|---:|---|
| cây sồi | 77 | 2/255 | **giống hệt** mọi chỉ số |
| khóm hoa | 264 | 1/255 | **giống hệt** mọi chỉ số |

Vài chục pixel lệch 1–2 mức là do sai số làm tròn số thực ở sát ngưỡng; mắt không thấy. QC trước làm sạch chỉ lệch ở chữ số thập phân thứ 3 (ví dụ 0,701 → 0,703 %).

Bản `gac_matte.py` trong `art-tests/hero-matte-clean/tools/` giữ nguyên làm hồ sơ của Bước A đã duyệt. Bản mới nằm ở `art-tests/rung-xanh-map-sample/tools/` và `C:\AI\GAME-ART-CORE\tools\`.
