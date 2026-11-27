# Bước A1: làm sạch viền 6 hero (GAME-ART-CORE, Claude, 2026-11-28)

Chi tiết cách làm, bảng kiểm thử và các vấn đề còn tồn tại: `docs/art/ART_PRODUCTION_PLAN.md` mục 10.

| Thư mục | Nội dung |
|---|---|
| `original/` | 6 WebP gốc, trích nguyên byte từ `assets-data-1.js` (k2–k7) |
| `cleaned_webp_q90/` | **Bản đề xuất đưa vào game**, cùng kích thước và tên phái như manifest `hero` |
| `cleaned_png/` | Bản lossless để lưu trữ |
| `compare/` | Ảnh trước/sau: 4 nền, phóng ×4 viền, tổng quan ở cỡ trong game |
| `qc_report.json` | Số đo trước/sau, SHA-256, dung lượng |
| `tools/` | Script chạy lại: `python tools/hero_edge_clean.py <thư mục chứa k2..k7.webp> <out>` rồi `python tools/hero_edge_compare.py <out>` |

Không dùng model AI, không tải gì. Chỉ cần numpy, Pillow, scipy. Chưa tích hợp vào game: chờ Luna đánh giá, sau đó Codex thay k2–k7.
