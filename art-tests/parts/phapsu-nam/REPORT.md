# Pháp Sư Nam tách bộ phận

14 mảnh độc lập vẽ bằng ImageGen theo sprite `__A.k13` trong `assets-data-1.js`. Giữ mũ trăng sao, râu trắng, áo lam viền vàng và trượng gỗ gắn ngọc xanh. Tay trái và trượng nằm chung trong `hand_l_staff.png`. Prompt, hash nguồn và số đo từng khớp nằm trong metadata.

## Ghép và kiểm tra

Mỗi PNG RGBA dùng canvas 768×640, alpha nhị phân 0 hoặc 255, hai chân chạm hàng y=620. Đặt mọi mảnh tại (0,0) và ghép theo z tăng dần. Tọa độ trục tính theo canvas, trái và phải tính theo cơ thể nhân vật. Dùng quan hệ cha–con trong [parts.json](parts.json) khi dựng chuyển động.

Đã chạy hàm nạp ảnh và ghép lớp của [công cụ Claude](../../auto-anim-2d/parts-assembler/parts_rig.py). Dáng trung tính khớp [assembled.png](assembled.png) từng pixel RGBA. Tất cả trục nằm trên phần đặc của mảnh cha và mảnh con. Đã thử xoay độc lập từng mảnh tại −20°, 0°, +20°. Các phép thử này kiểm tra độ chồng khớp, cần xem thêm khi chuyển động nhiều khớp hoặc đổi lớp che khuất.

**Luna duyệt.** Phần chồng nhỏ nhất là 266 px tại khuỷu trái, trong cửa sổ 47×47 quanh trục. Cổ áo rõ hơn và hai tà áo xòe hơn ảnh trong game. Thử động tác nâng trượng để xem cổ tay, khuỷu trái và vị trí trượng so với vành mũ. [Ảnh đối chiếu](comparison.png)
