# Bộ icon skill, quái và map

Ảnh nguồn để Claude và Luna duyệt. Đối chiếu [code game](../../index.html), [danh mục asset](../../docs/art/ASSET_INVENTORY.md) và [phong cách](../../docs/ART_DIRECTION.md).

- **24 kỹ năng người chơi**. Mỗi phái gồm 4 chính và 4 hỗ trợ, dùng cùng hình cho Nam/Nữ. Tên file khớp `id` trong cấu hình. Chọn ảnh theo cặp `classId + skillId`.
- **12 biểu tượng hành vi quái và chiêu boss**. Slime, Goblin, Goblin Cung Thủ và Sói có hình cho đòn riêng. Pháp Sư Goblin dùng `heal`. Chúa Sói dùng `charge`, `howl`, `summon`, cùng trạng thái `enrage`. Các boss khác chọn theo `skills[].type`; `charge` hiện mang hình đầu sói, phù hợp Chúa Sói. Đòn tầm xa và độc có biểu tượng dùng chung.
- **8 icon map và cổng**. Bảy icon đặt tên theo `map.id`. Danh sách map hiện dựng tiêu đề dạng văn bản trong `renderMaps()`; các biểu tượng phù hợp để đặt cạnh tên map.
- **4 ký hiệu minimap**. Boss, tinh anh, rương và điểm dẫn đường. Điểm dẫn đường là ảnh dự phòng cho tính năng chỉ hướng.

Mỗi ảnh có PNG RGBA 256×256 cho hậu kỳ và WebP lossless RGBA 96×96 để tích hợp. [Preview](preview.jpg) trình bày 64 px và 32 px trên nền HUD tối. [Manifest](manifest.json) ghi ID, đường dẫn, thứ tự ô, prompt ImageGen và hash ảnh nguồn.

Khi tích hợp, giữ nền nút, số hồi chiêu và trạng thái khóa từ UI hiện tại. Dùng ảnh 96 px bên trong nút, giảm kích thước trực quan theo vùng icon. Kiểm tra tiếp ký hiệu minimap ở kích thước hiển thị thực tế và trên cả nền sông lẫn nền cỏ.
