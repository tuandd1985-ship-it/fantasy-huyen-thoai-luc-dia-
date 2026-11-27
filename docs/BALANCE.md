# BALANCE — FANTASY: HUYỀN THOẠI LỤC ĐỊA
Thông số và công thức cân bằng. Nguồn số liệu: GDD.md mục V, IX, X (Do phê duyệt qua bản thiết kế v2). Mọi số ở đây phải nằm trong DATA của game, chỉnh ở đây + file cấu hình, không sửa engine.

## Công thức lõi
- Chỉ số cuối = Chỉ số gốc × (1 + tổng % cộng dồn) + chỉ số cộng thẳng. Hiển thị nguồn % (skill/đồ/ngọc) trong panel nhân vật.
- Mỗi cấp lên: +5 điểm thân thể, +2 điểm skill, cộng chỉ số tự tăng theo cấp (đường cong ở DATA).

## Chỉ số khởi đầu (Lv1)
| Chỉ số | Kiếm Sĩ | Pháp Sư | Cung Thủ |
| HP | 350 | 200 | 260 |
| Mana | 100 | 220 | 150 |
| Tấn công | 35 | 48 | 40 |
| Phòng thủ | 25 | 10 | 15 |
| Chí mạng | 5% | 7% | 12% |
| Né tránh | 3% | 5% | 10% |
| Tốc đánh/giây | 1.0 | 0.8 | 1.3 |

## Skill
Bảng sát thương/hồi chiêu/mana của 12 skill chính + 12 skill phụ: xem GDD.md mục V (chuẩn). Mở khóa skill chính ở Lv1/8/15/25.

## Ngọc (ghép 3 viên cấp n → 1 viên cấp n+1)
Cấp 1 +2% · Cấp 2 +4% · Cấp 3 +7% · Cấp 4 +11% · Cấp 5 +16% · Cấp 6 +22% · Cấp 7 +30%.
Loại: Đỏ tấn công, Tím chí mạng, Lục HP, Vàng tốc độ, Lam phòng thủ.
CAPS bắt buộc (chống bất tử/đánh vô hạn — giá trị cap cụ thể là PROPOSED, chờ chốt khi cân bằng giai đoạn 2): chí mạng, né tránh, tốc đánh phải có trần cứng trong DATA.

## Trang bị và rơi đồ
- Độ hiếm/lỗ khảm: Thường 0, Hiếm 1, Sử thi 2, Huyền thoại 3.
- Boss: luôn rơi ít nhất 1 món Hiếm+ (bảng đảm bảo riêng); rơi bổ sung theo drop table từng bậc boss — boss càng mạnh tỉ trọng Sử thi/Huyền thoại càng cao; first-kill có bonus. Quái tinh anh: drop tốt hơn quái thường cùng map.
- BẢNG ĐẢM BẢO RƠI TỪ BOSS theo map (Hiếm/Sử thi/Huyền thoại %) — Do DUYỆT 2026-11-27 theo bộ zip: Map1 90/9/1 · Map2 85/13/2 · Map3 78/18/4 · Map4 70/24/6 · Map5 60/30/10 · Map6 50/35/15 · Map7 40/40/20.
- Nâng cấp trang bị: thất bại KHÔNG phá hủy đồ (MVP, Do duyệt 2026-11-27); tỷ lệ thành công từng mốc + sẽ chốt riêng bằng test/bảng DATA trước khi khóa.
- Quái: chỉ số scale theo dải cấp map × hệ số map (DATA); độ khó bám sức nhân vật cùng cấp.

## Ghi chú cân bằng đã kiểm chứng (2026-11-27)
- Bản mẫu đầu: AUTO màn 1 chết 0/8 (quá khó) → đã chỉnh: giới hạn quái theo màn, bầy sói/tinh anh chỉ từ màn 3, AUTO thả diều cho phái đánh xa → Kiếm Sĩ và Pháp Sư AUTO qua màn 1, lên Lv2. Bài học: mọi thay đổi độ khó phải test AUTO cả 3 phái.
