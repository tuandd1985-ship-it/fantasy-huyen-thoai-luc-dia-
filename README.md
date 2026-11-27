# FANTASY — Huyền Thoại Lục Địa

Game Action RPG Fantasy chibi 2.5D cho điện thoại (màn hình ngang), chạy bằng một file web tĩnh duy nhất.

## Chạy game

Mở `index.html` trong trình duyệt là chơi được ngay (toàn bộ hình ảnh đã nhúng trong file). Khi triển khai lên Cloudflare, Worker chỉ cần phục vụ file này.

## Cấu trúc

- `index.html` — toàn bộ game: engine, dữ liệu cân bằng (DATA), giao diện, hình ảnh nhúng dạng data URI. Đầu file có manifest `ASSETS` / `ASSET_FILES` khai báo literal mọi đường dẫn ảnh gốc (`assets/...`) — khi sửa ảnh phải giữ manifest này để công cụ xuất bản nhúng đủ ảnh.
- `docs/` — tài liệu dự án: `SPEC.md` (chuẩn cao nhất, mọi thay đổi phải theo), `ART_DIRECTION.md`, `BALANCE.md`, `ARCHITECTURE.md`, `ROADMAP.md`, `PROGRESS.md`, `CHANGELOG.md`, `HUD_V2.md`, `GDD.md`.

## Quy ước làm việc chung (Luna / Codex / Claude Code)

- Đọc `docs/SPEC.md` trước khi sửa; đề xuất chưa được anh Do duyệt phải ghi rõ PROPOSED, không tự ghi đè SPEC.
- Nhân vật dùng phong cách CHIBI toàn bộ (sprite + chân dung); màn hình ngang là chuẩn duy nhất; game tự xoay hình 90° khi khung hiển thị dọc.
- Sau khi sửa: ghi thêm một dòng vào `docs/CHANGELOG.md`, kiểm tra cú pháp JS (`node --check` trên các khối script trích ra) và mô tả rõ đã kiểm chứng gì / chưa kiểm chứng gì (đặc biệt: chưa test trên iPhone thật thì nói rõ).
- Không đưa API token hay bí mật vào code frontend.
