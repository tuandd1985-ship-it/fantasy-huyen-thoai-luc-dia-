# FANTASY — Huyền Thoại Lục Địa

Game Action RPG Fantasy chibi 2.5D cho điện thoại (màn hình ngang), chạy bằng một file web tĩnh duy nhất.

## Chạy game

Mở `index.html` trong trình duyệt là chơi được ngay — giữ 3 file `index.html`, `assets-data-1.js`, `assets-data-2.js` cùng một thư mục (hai file data chứa toàn bộ hình ảnh dạng data URI, `index.html` tự nạp). Khi triển khai lên Cloudflare, Worker phục vụ cả 3 file.

## Cấu trúc

- `index.html` — toàn bộ game: engine, dữ liệu cân bằng (DATA), giao diện. Ảnh được tra cứu qua bảng `__A` (khóa k0–k18) do hai file data cung cấp; trong mã gốc của game, manifest `ASSETS` / `ASSET_FILES` khai báo literal mọi đường dẫn ảnh (`assets/...`) — khi sửa ảnh phải giữ manifest này để bản xuất/đóng gói nhúng đủ ảnh.
- `assets-data-1.js`, `assets-data-2.js` — dữ liệu hình ảnh (19 ảnh: tranh mở đầu, 6 chân dung, 6 ảnh nhân vật, 6 dải khung hình chuyển động), tách từ bản đóng gói một file để vừa giới hạn đẩy GitHub.
- `docs/` — tài liệu dự án: `SPEC.md` (chuẩn cao nhất, mọi thay đổi phải theo), `ART_DIRECTION.md`, `BALANCE.md`, `ARCHITECTURE.md`, `ROADMAP.md`, `PROGRESS.md`, `CHANGELOG.md`, `HUD_V2.md`, `GDD.md`.

## Quy ước làm việc chung (Luna / Codex / Claude Code)

- Đọc `docs/SPEC.md` trước khi sửa; đề xuất chưa được anh Do duyệt phải ghi rõ PROPOSED, không tự ghi đè SPEC.
- Nhân vật dùng phong cách CHIBI toàn bộ (sprite + chân dung); màn hình ngang là chuẩn duy nhất; game tự xoay hình 90° khi khung hiển thị dọc.
- Sau khi sửa: ghi thêm một dòng vào `docs/CHANGELOG.md`, kiểm tra cú pháp JS (`node --check` trên các khối script trích ra) và mô tả rõ đã kiểm chứng gì / chưa kiểm chứng gì (đặc biệt: chưa test trên iPhone thật thì nói rõ).
- Không đưa API token hay bí mật vào code frontend.
