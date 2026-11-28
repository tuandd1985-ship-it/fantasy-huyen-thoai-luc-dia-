# Áo giáp và giày cho sáu nhân vật

48 icon do ImageGen tạo dựa trên sprite hiện hành của Kiếm Sĩ, Pháp Sư và Cung Thủ, mỗi phái có bản Nam và Nữ. Mỗi nhân vật có 4 áo và 4 đôi giày. PNG RGBA 256×256 dành cho hậu kỳ, WebP lossless RGBA 96×96 dành cho UI. [Xem icon ở 64 và 32 px](preview-icons.jpg) · [Manifest và prompt](manifest.json).

## Thử mặc

Mở `preview.html` trong trình duyệt từ repo đã clone. Chọn một trong sáu nhân vật, nhập cấp thử nghiệm, rồi chọn áo hoặc giày. Có thể mặc trộn bậc giữa hai ô, tháo từng món và nâng tới +10. Khi hạ cấp, món không đủ điều kiện được tháo. Phòng thử giữ lựa chọn riêng cho mỗi nhân vật trong phiên mở trang. [Ảnh chạy thử](preview-fitting.png)

| Cấp mở thử | Bộ | Phòng thủ | HP | Lực chiến trang bị |
|---:|---|---:|---:|---:|
| 1 | Khởi Hành | 7 | 42 | 32 |
| 20 | Băng Lam | 44 | 226 | 185 |
| 40 | Hỏa Đồng | 83 | 420 | 346 |
| 60 | Thiên Kim | 122 | 614 | 508 |

Số đo là tổng áo và giày cùng bậc ở +0, làm tròn chỉ số cơ sở theo công thức `CONFIG.itemSlots` trong [code game](../../index.html). Bản thử chọn giá trị trung tâm, chưa đưa biến động khi rơi đồ, độ hiếm hay khảm ngọc vào. Mỗi bậc nâng cộng 8% chỉ số gốc của món, tối đa +10, theo mô hình hiện tại. Trong bài thử, áo Thiên Kim +1 và giày Thiên Kim +0 đạt 534 lực chiến.

Bản thử đổi màu trực tiếp trên các lớp thân, choàng, tay trên và giáp chân của rig. Phom áo, giày và hình thêu chi tiết ở bậc cao trong icon là thiết kế tham khảo. Để mặc đúng các chi tiết đó trong chuyển động chính thức, cần bộ lớp thay thế theo từng món và các khung góc nhìn tương ứng.

## Bàn giao Luna

- ID icon là `<classId>-<gender>/<slot>-lv<tier>`, ví dụ `mage-female/armor-lv20`. `armor` và `boots` khớp tên ô đang dùng. Có thể đánh giá icon trong túi đồ và bảng trang bị trước khi tích hợp ngoại hình.
- Cấp nhân vật, cấp món `il`, độ hiếm và +n hiện là các dữ liệu riêng. Bốn mốc cấp bên trên là lựa chọn cho bản thử. Trước khi áp vào tiến trình chính thức, quyết định trường cấp yêu cầu của từng món và nguồn rơi tương ứng với mốc 40/60. Giữ nguyên vật phẩm và ô trang bị trong dữ liệu lưu cũ.
- Playwright Edge đã kiểm tra sáu nhân vật, khóa cấp, thay riêng áo và giày, tăng lực chiến qua từng bậc, nâng và tháo món, ảnh nạp đầy đủ, giao diện rộng 390 px không cuộn ngang.
