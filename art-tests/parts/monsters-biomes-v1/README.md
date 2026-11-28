# Quái vẽ tách bộ phận cho Claude

Sáu rig đầu tiên từ sáu map sau Rừng Xanh, tổng 39 mảnh vẽ riêng bằng ImageGen. Mỗi thư mục dùng ID quái của game và có `reference.png`, PNG bộ phận, `parts.json`, `assembled.png` và `comparison.png`. [Xem bảng sáu quái](preview.jpg)

| ID | Map | Mảnh | Chuyển động có thể dựng |
|---|---|---:|---|
| `bat` · Dơi Quỷ | Hang Tối | 4 | Vỗ hai cánh riêng, nghiêng đầu, bổ nhào theo thân |
| `toad` · Cóc Độc | Đầm Lầy Độc | 6 | Co bốn chân để nhảy, nghiêng đầu theo nhịp phun độc |
| `mummy` · Xác Ướp | Sa Mạc Cát | 8 | Bước lê, đưa tay tấn công, giật khi trúng đòn |
| `fireDragon` · Rồng Lửa | Núi Lửa | 9 | Vỗ cánh, quật đuôi, cúi đầu và vươn chân |
| `iceWolf` · Sói Băng | Băng Nguyên | 7 | Chạy bốn chân, hạ đầu khi lao, vẫy đuôi |
| `wraith` · Hồn Ma | Lâu Đài Bóng Đêm | 5 | Bồng bềnh, vung tay và lượn đuôi khói |

## Lắp và kiểm tra

Đặt tất cả PNG RGBA 768×640 tại (0,0), theo thứ tự z tăng dần. Các điểm trục tính từ góc trên trái của canvas. Dùng cây cha–con trong `parts.json` để lan truyền biến đổi. Chân tiếp đất theo `groundTouch` ở y=620. Dơi và Hồn Ma treo trên đường đất. Độ mờ ma và hiệu ứng đòn xử lý khi vẽ trong game.

Dáng nghỉ của cả sáu rig khớp từng pixel RGBA khi ghép bằng [công cụ Claude](../../auto-anim-2d/parts-assembler/parts_rig.py). Mọi điểm trục nằm trên pixel đặc của cả cha và con. Đã xác nhận từng khớp giữ vùng chồng khi xoay riêng tại −20°, 0° và +20°. Thử thêm một mảnh chuyển động mỗi rig để xác nhận cây khớp hoạt động.

## Luna duyệt

Cóc Độc nhìn thẳng hơn và phần nấm ở lưng ít lộ. Sói Băng có dáng dài hơn mẫu gốc. Chân Xác Ướp và Sói Băng xoay nguyên đoạn, phù hợp chạy thử trước. Khi dựng chuyển động biên độ lớn, xem đường ráp cùng thứ tự che khuất của cánh Rồng Lửa và tay Hồn Ma. Hiệu ứng hơi thở, độc, trúng đòn và bóng xử lý ở lượt animation.
