# Cung Thủ Nữ tách bộ phận

16 mảnh vẽ riêng bằng ImageGen dựa trên sprite `__A.k16` trong `assets-data-1.js` ở `main` tại `3382a53`. Tách bím tóc và ống tên. Dây cung, cung và bàn tay trái nằm trên cùng một PNG. [Ảnh đối chiếu với game](comparison.png)

Mỗi PNG RGBA có canvas 768×640 với nền trong suốt, alpha 0 hoặc 255 và hai chân chạm hàng y=620. Đặt mọi mảnh tại (0,0), ghép theo z tăng dần. Dùng trục tọa độ canvas và cây cha–con trong [parts.json](parts.json) khi dựng chuyển động.

Đã đối chiếu ảnh ghép bằng [công cụ Claude](../../auto-anim-2d/parts-assembler/parts_rig.py). Dáng trung tính khớp từng pixel RGBA với [assembled.png](assembled.png). Mỗi trục nằm trên cả mảnh cha và con. Thử xoay độc lập tại −20°, 0° và +20°, mọi khớp giữ vùng chồng.

**Luna duyệt.** Phần chồng nhỏ nhất 452 px tại cổ tay cầm cung. Tay cầm cung duỗi hơn ảnh trong game. Dây cung ở dáng trung tính là ảnh cố định và cần kiểm tra lại khi dựng tư thế kéo dây. Chuyển động nhiều khớp và đổi lớp che khuất cần kiểm tra trong lượt animation.
