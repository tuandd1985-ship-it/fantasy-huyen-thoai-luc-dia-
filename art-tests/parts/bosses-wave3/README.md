# Bốn boss tách mảnh

29 mảnh vẽ riêng bằng ImageGen, mỗi PNG RGBA sử dụng canvas 768×640. Mỗi thư mục có ảnh tham chiếu, ảnh ghép, bảng so sánh và `parts.json` ghi lớp z, trục và cây cha–con. Hai chân chạm đất của mỗi dáng đứng có đáy ở hàng y=620.

| Boss | Mảnh | Điểm dựng animation theo kỹ năng hiện có |
|---|---:|---|
| [Chúa Sói Alpha](wolfLord/comparison.png) | 7 | Thu bốn chân và hạ đầu trước khi lao. Ngẩng đầu và vẫy đuôi ở nhịp hú. Dùng hiệu ứng riêng khi gọi sói. |
| [Đầm Chúa](toadKing/comparison.png) | 6 | Co chân, nén thân và nâng đầu để báo nổ diện rộng. Gọi cóc ở nhịp phục hồi. |
| [Pharaoh Cổ Đại](pharaoh/comparison.png) | 8 | Nhấc trượng gọi xác ướp, hạ trượng dẫn nhịp nổ diện rộng. Trượng và cẳng tay trái cùng một lớp. |
| [Chúa Quỷ Bóng Đêm](demonLord/comparison.png) | 8 | Thu cánh trước cú lao, bung cánh và hạ tay khi nổ diện rộng. Gọi hồn ma bằng hiệu ứng riêng. |

Bốn dáng ghép khớp từng pixel RGBA bằng [công cụ Claude](../../auto-anim-2d/parts-assembler/parts_rig.py). Trục nằm trên pixel đặc của cả cha và con. Mọi khớp còn vùng chồng ở góc −20°, 0° và +20°. Thử chuyển động từng mảnh đã tạo khung khác dáng nghỉ. Nhện Chúa và Golem Băng ở [lô 2](../monsters-map-wave2/), Rồng Lửa ở [lô 1](../monsters-biomes-v1/). Đủ ảnh tách mảnh cho bảy boss theo ID hiện tại.

## Duyệt cảnh thử

[Chúa Sói trên đấu trường Xuân](wolfLord-bossxuan.jpg) dùng đúng ảnh Desktop. Điểm đặt lấy từ vùng `boss` của [lưới va chạm đã có](../../maps-anh-do/collision/maps_collision.json). Một dải 145 ô quanh hướng ngang tâm đều đi được. Đây là kiểm tra vị trí mẫu. Quãng lao, bán kính va chạm và thời điểm gây sát thương vẫn lấy từ game khi tích hợp. [Tọa độ và SHA-256](arena-placement.json)

Chúa Sói mới có đuôi ít xanh hơn sprite đang chạy. Đầm Chúa có tư thế đối xứng hơn. Khi Claude dựng chuyển động lớn, xem thêm cổ Chúa Sói, đường ráp vai Đầm Chúa và lớp cánh Chúa Quỷ. Các hiệu ứng nổ, triệu hồi và đổi pha dùng logic riêng của game. Bộ ảnh hiện ở `art-tests`.
