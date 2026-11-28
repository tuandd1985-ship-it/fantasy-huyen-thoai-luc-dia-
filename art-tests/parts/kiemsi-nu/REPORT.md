# Kiếm Sĩ Nữ tách bộ phận

15 mảnh vẽ riêng bằng ImageGen dựa trên sprite `__A.k12` trong `assets-data-1.js` ở `main` tại `3382a53`. Tóc đuôi ngựa tách riêng và xoay theo đầu. Kiếm liền với bàn tay phải. [Ảnh đối chiếu với game](comparison.png)

Mỗi PNG RGBA có canvas 768×640 với nền trong suốt, alpha 0 hoặc 255 và hai chân chạm hàng y=620. Đặt mọi mảnh tại (0,0), ghép theo z tăng dần. Dùng trục tọa độ canvas và cây cha–con trong [parts.json](parts.json) khi dựng chuyển động.

Đã đối chiếu ảnh ghép bằng [công cụ Claude](../../auto-anim-2d/parts-assembler/parts_rig.py). Dáng trung tính khớp từng pixel RGBA với [assembled.png](assembled.png). Mỗi trục nằm trên cả mảnh cha và con. Thử xoay độc lập tại −20°, 0° và +20°, mọi khớp giữ vùng chồng.

**Luna duyệt.** Phần chồng nhỏ nhất 199 px tại khuỷu trái. Tay cầm kiếm và áo choàng lớn hơn ảnh trong game. Xem thêm điểm ráp khuỷu và thứ tự che khuất của tóc khi vung kiếm. Chuyển động nhiều khớp và đổi lớp che khuất cần kiểm tra trong lượt animation.
