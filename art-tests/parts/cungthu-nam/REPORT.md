# Cung Thủ Nam tách bộ phận

15 mảnh độc lập vẽ bằng ImageGen theo sprite `__A.k15` trong `assets-data-1.js`. Giữ mắt xanh, mũ trùm lục, giáp da nâu và cung gỗ. Tay trái, cung và dây cung nằm chung trong `hand_l_bow.png`. Ống tên được tách riêng và gắn theo thân. Prompt, hash nguồn và số đo từng khớp nằm trong metadata.

## Ghép và kiểm tra

Mỗi PNG RGBA dùng canvas 768×640, alpha nhị phân 0 hoặc 255, hai chân chạm hàng y=620. Đặt mọi mảnh tại (0,0) và ghép theo z tăng dần. Tọa độ trục tính theo canvas, trái và phải tính theo cơ thể nhân vật. Dùng quan hệ cha–con trong [parts.json](parts.json) khi dựng chuyển động.

Đã chạy hàm nạp ảnh và ghép lớp của [công cụ Claude](../../auto-anim-2d/parts-assembler/parts_rig.py). Dáng trung tính khớp [assembled.png](assembled.png) từng pixel RGBA. Tất cả trục nằm trên phần đặc của mảnh cha và mảnh con. Đã thử xoay độc lập từng mảnh tại −20°, 0°, +20°. Các phép thử này kiểm tra độ chồng khớp, cần xem thêm khi chuyển động nhiều khớp hoặc đổi lớp che khuất.

**Luna duyệt.** Phần chồng nhỏ nhất là 219 px tại điểm gắn ống tên, trong cửa sổ 47×47 quanh trục. Dáng mẫu duỗi tay cầm cung hơn, mũ và tà áo choàng rộng hơn ảnh trong game. Dây cung hiện liền với vũ khí. Khi dựng dáng kéo cung, cần xem cách biểu diễn dây căng và độ rõ ở kích thước chơi. [Ảnh đối chiếu](comparison.png)
