# Quái tách lớp trên map của anh Do

Bộ 2 gồm 6 quái mới được vẽ thành 47 mảnh bằng ImageGen. Dùng ảnh tạo hình và ảnh map của anh Do làm tham chiếu màu. Bản này dùng chung quy ước Canvas 768×640, pivot tọa độ canvas và thứ tự z như lô trước.

| Quái | Mảnh | Vị trí dùng trong scene |
|---|---:|---|
| `spider` · Nhện Độc | 10 | Hang pha lê |
| `spiderQueen` · Nhện Chúa | 10 | Hang pha lê |
| `imp` · Hỏa Ma | 9 | Hang dung nham, đấu trường lửa |
| `magmaGolem` · Golem Dung Nham | 6 | Hang dung nham, đấu trường lửa |
| `iceWitch` · Phù Thủy Băng | 6 | Hang băng, đấu trường băng |
| `iceGolem` · Golem Băng | 6 | Hang băng, đấu trường băng |

Các mảnh đã được ghép lại bằng [công cụ Claude](../../auto-anim-2d/parts-assembler/parts_rig.py), khớp từng pixel RGBA với `assembled.png`. Mọi khớp có vùng chồng ở −20°, 0° và +20°. Hai loài nhện dùng bốn mẫu chân cho tám chân điều khiển riêng. Tay và trượng Phù Thủy Băng hiện chung một lớp. Cổ tay khuỷu và đầu gối của golem xoay theo cả đoạn. Vai Phù Thủy Băng là khớp có phần chồng nhỏ nhất với 140 pixel quanh trục, nên xem lại lúc giơ trượng hết biên độ.

## Mở cảnh thử

Mở `preview.html` từ thư mục repo đã tải về. Chọn map, bật hoặc tắt chuyển động, thử động tác và hiện điểm neo. Vị trí, hướng và cỡ hiển thị nằm trong `scene-data.js`, đo bằng pixel ảnh map gốc. `map-checks.json` ghi hash xác nhận cả năm nền trong repo trùng byte với ảnh Desktop. Cảnh sử dụng thêm ba rig từ [lô trước](../monsters-biomes-v1): Dơi Quỷ, Sói Băng và Rồng Lửa.

- Hang pha lê có 6 vị trí. [Xem ảnh](crystal.jpg)
- Hang băng có 5 vị trí. [Xem ảnh](ice.jpg)
- Hang dung nham có 5 vị trí. [Xem ảnh](lava.jpg)
- Đấu trường băng và lửa có 3 vị trí mỗi cảnh. [Đấu trường băng](iceArena.jpg) · [Đấu trường lửa](fireArena.jpg)

Đã chạy Playwright qua cả 5 cảnh, xác nhận 22 vị trí nạp đủ lớp, nút thử động tác làm đổi khung hình, công tắc điểm neo hoạt động và không tràn ngang tại 390 px. Các vị trí trên đường được đặt theo ảnh. Cảnh thử dùng nền nguyên khối nên lớp cây, đá và vách hiện không che quái theo chiều sâu. Đây là nơi duyệt hình và chuyển động sơ bộ. Khi đưa vào màn chơi chính cần khai báo vùng đi được, cầu, vách và logic gặp quái theo vị trí.
