# HUD v2 — Bố cục đã được chủ dự án duyệt

- Thay thanh icon dưới màn hình bằng 5 icon tròn ở phía trên bên phải, ngay bên trái minimap. Thứ tự: Nhân vật, Túi đồ, Trang bị, Kỹ năng, Cài đặt. Bản đồ lớn mở bằng cách chạm minimap.
- Icon nền tối bán trong suốt, viền vàng cổ, biểu tượng rõ, không có chữ bên dưới. Kích thước hiển thị 36–40 CSS px, vùng chạm tối thiểu 44 × 44 CSS px, không chồng vùng chạm. Có sáng nhẹ khi chọn, chấm đỏ khi có thông báo phù hợp.
- Giữ HP/MP trên trái, joystick dưới trái, đánh thường và 4 skill dưới phải, EXP sát mép dưới. Tôn trọng safe area cả hai hướng xoay ngang; màn hình hẹp thì co khoảng cách hoặc gom menu phụ, không thu nhỏ vùng chạm dưới chuẩn.
- Mặc định đóng tất cả panel. Chạm icon mở panel tương ứng; chạm lại, nút X hoặc chạm ngoài đóng. Chạm icon khác chuyển panel trực tiếp; chỉ một panel mở. Minimap mở bản đồ lớn theo cùng quy tắc.
- Khi mở panel offline, tạm dừng chiến đấu/AUTO, xóa input joystick đang giữ; khi đóng khôi phục trạng thái trước đó, không tự bật AUTO nếu trước đó tắt. Không truyền thao tác chạm panel xuống sân chơi. Không reload trang.
- Dùng UIManager/PanelManager chung; registry icon/panel, quản lý focus, trạng thái pause và safe area. Không sửa logic chiến đấu riêng cho từng panel.
- Nghiệm thu: 5 icon đúng vị trí; không còn dock dưới; mỗi icon mở đúng panel; chuyển panel không chồng; X/chạm ngoài/chạm lại đóng; minimap mở bản đồ; pause/resume đúng; không đánh nhầm; kiểm tra iPhone ngang hai chiều và màn hình hẹp.

Hình assets/HUD_v2.png là sơ đồ bố trí, không phải asset chính thức. Concept.png cũ chỉ tham khảo phong cách; nếu khác bố cục thì HUD v2 được ưu tiên. SPEC gốc vẫn là chuẩn cho các yêu cầu khác.
