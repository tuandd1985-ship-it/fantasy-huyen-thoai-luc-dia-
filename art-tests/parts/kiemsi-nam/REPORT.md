# Kiếm Sĩ Nam vẽ tách mảnh

Pilot cho Claude lắp chuyển động và Luna duyệt hình. Ảnh chuẩn là Kiếm Sĩ Nam trong [hero-edge-clean](../../hero-edge-clean/cleaned_webp_q90/hero-swordsman-male.webp). Đã đối chiếu SHA-256 với ảnh đang nạp ở `__A.k11` trên `main` tại `9fdc347`.

## Cách làm

Vẽ riêng đầu, thân, choàng, tay và chân bằng ImageGen theo ảnh chuẩn. Tách các mảnh đã vẽ từ ba bảng nguồn độc lập, căn tỷ lệ và đặt lên canvas chung. Mỗi PNG RGBA 768×640 chứa một bộ phận. Hai chân chạm hàng pixel y=620. Mọi pixel có alpha 0 hoặc 255. Bàn tay phải và kiếm liền trong một PNG. Thiết kế chuẩn không có khiên hoặc bao kiếm riêng.

[parts.json](parts.json) có thứ tự z, trục xoay theo tọa độ canvas và quan hệ cha–con. Trái/phải tính theo cơ thể nhân vật. Để dựng dáng gốc, đặt mọi ảnh ở (0,0), ghép từ z thấp lên z cao. Khi làm animation, áp biến đổi của mảnh cha cho cả cây con trước rồi xoay mảnh con quanh trục riêng. [Ảnh ghép](assembled.png) và [ảnh đối chiếu](comparison.png) dùng đúng các PNG phát hành.

## Kiểm tra

- Ghép lại từ các PNG theo z cho dữ liệu RGBA giống `assembled.png` từng pixel.
- Cả 13 điểm nối nằm trên pixel đặc của mảnh cha và mảnh con. Thử từng mảnh con ở −20°, 0° và +20° so với mảnh cha. Quanh trục, phần chồng nhỏ nhất là 239 pixel trong vùng 47×47. Vai trái là điểm chồng ít nhất.
- Ảnh đối chiếu chuẩn hóa cùng chiều cao. Giữ mái tóc xanh bạc, chỏm đỏ, giáp bạc, áo choàng đỏ và kiếm thẳng. Mẫu có nắm tay cầm kiếm lớn hơn, áo choàng xòe hơn và chi tiết giáp vàng rõ hơn ảnh hiện hành. Luna duyệt các sai khác này trước khi nhân rộng.
- Chỉ kiểm tra dáng ghép tĩnh và vùng chồng khi xoay từng khớp. Cần xem lại đường ráp vai/khuỷu và thứ tự che khuất khi Claude làm chuyển động vung kiếm biên độ lớn.
