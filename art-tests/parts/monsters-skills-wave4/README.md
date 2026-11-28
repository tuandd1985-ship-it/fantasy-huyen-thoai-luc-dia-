# Lô 4 · Quái tách mảnh và kỹ năng

Sáu quái dùng ID hiện có trong game. Bộ này có 46 mảnh PNG RGBA vẽ riêng bằng ImageGen, canvas 768×640 và trục theo tọa độ chung. Mỗi thư mục có ảnh tham chiếu, ảnh ghép, ảnh đối chiếu và `parts.json`. [Bảng sáu quái](preview-monsters.jpg)

| Quái | Map | Số mảnh | Động tác thử |
|---|---|---:|---|
| Xương Khô | Hang Tối | 8 | Chém kiếm |
| Thằn Lằn Đầm | Đầm Lầy Độc | 7 | Vung vuốt |
| Bọ Cạp Cát | Sa Mạc Cát | 12 | Chích độc |
| Kền Kền | Sa Mạc Cát | 5 | Sà xuống |
| Yêu Tuyết | Băng Nguyên | 6 | Đấm nặng |
| Ma Cà Rồng | Lâu Đài Bóng Đêm | 8 | Huyết cầu và nhịp hút máu |

Bọ Cạp Cát có hai mẫu chân vẽ riêng, đặt thành tám PNG điều khiển độc lập. Hai cánh Kền Kền là hai lớp. Cẳng tay và kiếm Xương Khô liền một lớp. Áo choàng Ma Cà Rồng gắn cùng thân. Hiệu ứng đạn vẽ riêng để tách nhịp tung và bay.

## Hiệu ứng và cách thử

12 hình hiệu ứng gồm sáu loại đạn, vòng hồi máu, vòng báo đòn, nổ lửa, vệt chém, ấn triệu hồi và băng vỡ. PNG cạnh dài tối đa 384 px và WebP RGBA lossless tối đa 192 px. [Bảng hiệu ứng](preview-fx.jpg) · [Manifest và prompt](fx-manifest.json)

Mở `preview.html` trong bản repo đã tải. Chọn một trong 16 kỹ năng, bấm **Thử đòn** hoặc bật tự phát lại. Các cảnh dùng nền Đấu trường Xuân có sẵn. [Huyết cầu](vampire-blood.jpg) · [Chích độc](scorpion-sting.jpg) · [Hồi máu](shaman-heal.jpg) · [Vòng báo nổ](dragon-nova.jpg) · [Vệt báo lao húc](wolf-charge.jpg)

`skill-data.js` ghi sự kiện, loại hiển thị và nhịp mẫu. Căn hiệu ứng thật với sự kiện va chạm của engine khi tích hợp. Báo vòng nổ và gầm giữ 0,9 giây, vệt lao giữ 0,7 giây theo [code game](../../index.html). Các thời gian còn lại phục vụ cảnh thử. Yêu Tuyết dùng hình băng vỡ cho cú đấm cận chiến. Kền Kền dùng động tác sà cho hành vi bay đánh gần. Hai minh họa này không đặt thêm trạng thái hoặc vùng sát thương.

## Kết quả kiểm tra

- Cả sáu rig ghép khớp từng pixel ở dáng nghỉ bằng [công cụ Claude](../../auto-anim-2d/parts-assembler/parts_rig.py). Mọi khớp giữ chồng ở −20°, 0° và +20°. Khuỷu phải Xương Khô có phần chồng nhỏ nhất là 219 pixel quanh trục, cần xem thêm khi chém rộng.
- Playwright đã chạy 16 cảnh qua trạng thái chuẩn bị hoặc báo đòn, tác động và về dáng nghỉ. Kiểm tra thấy khung hình thay đổi, ảnh nạp đủ, giao diện không tràn ngang ở 390 px.
- Bộ hình và cảnh thử nằm trong `art-tests` để Luna duyệt trước khi gắn vào engine. Sát thương, AI và bộ dữ liệu màn chơi vẫn lấy từ game.
