# Muse: tiếp nhận review v0.3.7

Đọc [FANTASY_PROJECT_REVIEW.md](../../FANTASY_PROJECT_REVIEW.md) trước. Đây là báo cáo + bằng chứng, **không phải bản vá game**. Chờ anh Do duyệt gói sửa cụ thể.

Baseline source: `02ec5850e865f834321143e86adf4fadb3c62964`. Các commit art về sau không sửa engine/gameplay. Dữ liệu kiểm thử ghi Windows/Chrome; không có kết luận Safari/iPhone thật đã đạt.

## Kết quả cần ưu tiên

- AUTO stage1: 12/12 fixture cơ bản; mage mở rộng 28/30, hai seed 109/130 timeout 600 giây mô phỏng. Repro riêng trong trang mới có ảnh và tọa độ.
- Map lớn không pause và nút X ngoài viewport 844×390; keyboard và ultimate timer có thể tác động combat trong pause.
- Reload mất save/settings; công thức stats và mana shield có sai lệch đo được.
- 6 ngoại hình vào game được; production logic khớp source sau chuẩn hóa manifest ảnh; local có lỗi helper ảnh, production capture không có exception đó.

## Chạy lại (không sửa game)

Trong thư mục `reviews/v0.3.7`, cài riêng công cụ test, dùng Chrome có sẵn:

```sh
npm install --no-save --package-lock=false playwright-core@1.65.1
node review-tests.cjs
node reproduce-stalls.cjs
```

Lệnh test sẽ ghi đè kết quả trong `evidence/` và tạo trace. Nên chạy ở clone/worktree test riêng để giữ bằng chứng ban đầu; đối chiếu SHA trong `evidence-manifest.json`. Không commit node_modules hoặc kết quả chạy lại vào main khi chưa được duyệt. Muốn tái hiện đúng baseline, các file game phải còn khớp commit baseline, không dùng engine đã sửa.

Harness dùng file://, font Google bị chặn chủ động; viewport844×390/DPR1, thêm390×844. Mô phỏng dùng engine thật với RNG seeded, dt0,05; tạm stub UI/audio/minimap trong **trang test** để chạy nhanh. Không thay CONFIG hay file source. Trạng thái sinh trong test đều là fixture, không phải save người dùng.

Để tránh tăng repo với nội dung lặp, trace31,47MB và bản production capture10,16MB giữ local, chỉ công bố SHA. Runner sẽ SKIP T14 khi thiếu `evidence/production.html`; có thể tải production hiện tại riêng để kiểm tra, nhưng nếu production đã thay đổi thì không còn là capture gốc. Kết quả T14 đã ghi trong `review-tests.json` là của capture tại thời điểm review, không phải lần chạy mới.

Hai script portable chỉ đổi đường dẫn và import Playwright so với script đã dùng trên máy Codex; logic kiểm thử còn nguyên. `static-audit.json` giữ kết quả và hash toàn bộ file baseline; script audit/extracted scripts giữ local.

## Ảnh và pipeline AI

- [Vòng magenta: 6 raw + INFO](../../art-tests/comfyui-round1/)
- [BiRefNet: 4 raw + 4 cut + INFO](../../art-tests/comfyui-round2/)
- Vòng BiRefNet rembg2.0.88 chạy CPU36–39s/ảnh; SDXL CUDA khoảng15s/ảnh. Kiểm tra mép trên nền sáng/tối. Icon kiếm nền trắng vẫn có khung ngoài ý muốn; không đánh dấu thành asset sword đã đạt chỉ vì alpha có nền trong suốt.

Không có yêu cầu tự triển khai refactor, đổi engine, sửa balance, push patch hoặc deploy trong gói bàn giao này.
