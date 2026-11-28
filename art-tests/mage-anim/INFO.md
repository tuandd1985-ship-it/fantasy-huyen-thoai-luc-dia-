# Dải chuyển động Pháp Sư mới (thay k15/k16)

GAME-ART-CORE (Claude) · 2026-11-28. Không sửa source game.

## Sản phẩm
| File | Nội dung |
|---|---|
| `mage_nam_strip_2520x500.png`, `mage_nu_strip_2520x500.png` | 6 ô 420×500, nền trong suốt, thứ tự **[đứng thở 1, đứng thở 2, chạy 1, chạy 2, tung phép 1, tung phép 2]**, chân ở y ≈ 487 như k13–k18 |
| `mage_{nam,nu}_skill_charge_420x500.png` | Tư thế skill 1: giơ gậy tụ phép mạnh (hào quang quanh người, vòng phép dưới chân, cầu phát sáng) |
| `mage_{nam,nu}_skill_release_420x500.png` | Tư thế skill 2: phóng phép (gậy chĩa ra trước, luồng phép từ quả cầu) |
| `mage_{nam,nu}_contact.jpg` | 8 ô trên nền đen / trắng / cỏ v2b, có kẻ vạch đỏ ranh giới ô để soi mép |
| `mage_{nam,nu}_preview.gif` | Xem nhanh chu kỳ thở → chạy → tung phép trên nền cỏ |
| `qc.json` | Số đo QC từng ô |
| `rig/` | Hai lớp dùng để dựng hình: thân (đã vẽ lại phần bị gậy che) và gậy (gậy, quả cầu, bàn tay cầm), kèm tham số tách |
| `attempts/` | Các lần thử sinh trực tiếp bằng Animagine + OpenPose (không đạt, lý do ở mục "Quy trình") |
| `tools/` | Script tái lập |

Kích thước nhân vật trong ô: cao khoảng 390 px (từ chóp mũ hoặc đỉnh tóc tới chân). Một tỉ lệ và một vị trí dùng chung cho cả 6 ô của mỗi dải nên khi chạy không bị giật. Tỉ lệ so với ảnh tham chiếu: nam 0,628, nữ 0,614.

## Quy trình (và vì sao khác dự kiến)
1. **Đã thử sinh từng khung bằng Animagine XL 4.0 + ControlNet OpenPose (xinsir) như yêu cầu, nhưng không đạt** (`attempts/`):
   - `0_incontext_panel`: đặt ảnh mẫu cạnh khung cần vẽ thì model để trống khung, vì prompt có `solo`.
   - `1_txt2img_openpose`: chỉ dùng prompt + OpenPose thì nhân vật lệch hẳn. Mặt khác, mất râu bạc, áo nữ tối màu, nền tối, bị cắt khung.
   - `2/3_img2img`: dùng ảnh mẫu làm ảnh khởi đầu thì giữ được ngoại hình, nhưng **dáng gần như không đổi kể cả ở mức vẽ lại 0,9**. Tay chân chibi quá ngắn nên OpenPose không kéo được; râu bạc biến thành râu đen.
   - IP-Adapter (công cụ giữ danh tính) đã tải nhưng chưa bật được vì ComfyUI đang khóa custom node.
2. **Cách đã dùng: dựng khớp từ chính ảnh tham chiếu** (`art-tests/hero-edge-clean/cleaned_png/hero-mage-{male,female}.png`), nên mặt, tóc, mũ rộng (nam), kẹp pha lê (nữ), gậy, quả cầu và màu áo đúng 100 % như ảnh gốc:
   - **Tách lớp gậy**: vùng khoanh quanh gậy + lọc màu (gỗ nâu, viền tối, lưỡi bạc) + hình tròn quả cầu + bàn tay cầm.
   - **Vẽ lại phần thân bị gậy che bằng Animagine XL 4.0** (inpaint, node gốc, **nền trắng trơn**). Sau đó tách nền: **BiRefNet (rembg) → pixel trắng trơn thành trong suốt → giữ thành phần lớn nhất → `gac_matte.clean`**, đúng pipeline đã chốt.

     | | Seed | Prompt (rút gọn) | Negative | Thông số |
     |---|---|---|---|---|
     | Nam | 732001 | `1boy, solo, chibi, young wizard, dark blue messy hair, blue eyes, small white goatee, wide-brimmed pointed dark blue wizard hat with gold trim, dark blue wizard robe and cape with gold embroidery, brown boots, standing, empty hands, no staff, open empty hand, full body, white background…` | `staff, stick, wand, weapon, orb, holding, holding object, black hat lining, multiple characters…` | 28 bước, euler_ancestral, CFG 5, denoise 1,0 trong vùng che |
     | Nữ | 732002 | `1girl, solo, chibi, long wavy lavender purple hair, purple eyes, teal and blue wizard robe with silver trim, purple dress, purple boots, standing, empty hands, no staff, open empty hand, full body, white background…` | như trên | như trên |

     Prompt đầy đủ ở `rig/rig_split_*.json`. Model `animagine-xl-4.0-opt.safetensors` (SHA-256 6327eca9…). Mỗi lần vẽ lại mất khoảng 18 s.
   - **Dựng 8 khung** (`tools/mage_anim_compose.py`). Thân và gậy được biến đổi theo bảng dưới; gậy xoay quanh bàn tay cầm.
   - **Hiệu ứng phép vẽ bằng code**: quầng sáng ở quả cầu, tia phép, hào quang, vòng phép. Màu xanh lam cho nam, tím cho nữ, theo màu quả cầu.

| Khung | Nghiêng thân | Nhấp nhô | Co giãn dọc | Bước chân | Xoay gậy | Hiệu ứng |
|---|---:|---:|---:|---:|---:|---|
| đứng thở 1 | 0° | 0 | 1,000 | 0 | 0° | quầng nhẹ ở cầu |
| đứng thở 2 | 0° | 0 | 0,982 (thở) | 0 | +1,5° | quầng nhẹ |
| chạy 1 | 3° | 0 | 0,985 | dang 10 px | −6° | quầng nhẹ |
| chạy 2 | 3° | lên 12 px | 1,010 | khép 6 px | −10° | quầng nhẹ |
| tung phép 1 | −2° | lên 8 px | 1,000 | 0 | −16° (giơ gậy lên) | tụ phép: quầng + tia |
| tung phép 2 | 3° | 0 | 0,990 | 6 px | +12° (chĩa ra trước) | phóng phép: tia nổ ra phía trước |
| skill tụ phép | −2° | lên 10 px | 1,000 | 6 px | −18° | hào quang quanh người, vòng phép dưới chân, quầng lớn |
| skill phóng phép | 6° | 0 | 0,985 | 14 px | +40° | hào quang nhẹ, luồng phép dài chĩa phía trước |

## QC (`qc.json`), tất cả 16 ô đạt
| Tiêu chí | Kết quả |
|---|---|
| Mỗi ô đúng 1 nhân vật | Mỗi ô có **1 thành phần đặc** (alpha > 128); **0 mảnh rời ≥ 30 px** |
| Không mảnh lạ ở mép ô | Dải mép 4 px: **0,0 % pixel có alpha, alpha lớn nhất 0** ở cả 16 ô |
| Mặt rõ | Mặt không bị gậy hay hiệu ứng che. Riêng ảnh skill tụ phép có hào quang mờ phủ nhẹ lên tóc |
| Gậy và quả cầu nhất quán | Cùng một lớp gậy cho mọi khung (chỉ xoay), cùng màu cầu |
| Chân | y = 483–489 (thấp nhất 483 ở khung chạy 2 nhấp lên) |

Hai đầu mũi gậy nữ bị tách thành mảnh rời khi thu nhỏ vào ô (khoảng 31 px). Đã bỏ bằng bước giữ thành phần lớn nhất ở cấp ô, nên đầu mũi gậy nữ ngắn đi khoảng 2 px.

## Hạn chế để Luna cân nhắc
- **Chạy** là chạy kiểu chibi: nhấp nhô, nghiêng người, bước chân dưới vạt áo, gậy lắc. Chân không sải rộng như dải cũ, vì chân bị áo choàng che gần hết.
- **Tung phép** chủ yếu thể hiện bằng xoay gậy + hiệu ứng; tay cầm không đổi tư thế.
- Bản nữ có thêm bàn tay trống do Animagine vẽ lại, nằm ngay dưới bàn tay cầm gậy. Ở các khung hiện tại nó bị gậy che gần hết.
- Nếu cho phép bật IP-Adapter (đã tải, khớp hash), em có thể sinh tư thế biên độ lớn hơn mà vẫn giữ mặt.

## Tái lập
```
python tools/mage_rig.py split <cleaned_png_dir> <out> 0 male       # thân + gậy nam (seed 732001)
python tools/mage_rig.py split <cleaned_png_dir> <out> 0 female     # nữ (seed 732002)
python tools/mage_anim_compose.py <rig_male_dir> <rig_female_dir> <out>
```
