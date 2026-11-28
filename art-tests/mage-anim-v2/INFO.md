# Pháp Sư v2: dải chuyển động sinh bằng IP-Adapter (biên độ dáng lớn)

GAME-ART-CORE (Claude), 2026-11-28. Không sửa source game. Đủ cả **Nam** và **Nữ**.

## Sản phẩm (nam)
| File | Nội dung |
|---|---|
| `mage_nam_strip_2520x500.png` | 6 ô 420×500, nền trong suốt: [idle1, idle2, run1, run2, cast1, cast2] |
| `mage_nam_skill_charge_420x500.png`, `mage_nam_skill_release_420x500.png` | 2 ảnh skill rời |
| `mage_nam_contact.jpg` | 8 ô trên nền đen / trắng / cỏ; vạch đỏ là ranh giới ô, vạch vàng là y 487 |
| `mage_nam_preview.gif` | Chu kỳ thở → chạy → tung phép |
| `qc.json`, `generation_male.json`, `raw/` | Số đo QC; prompt, seed, model từng khung; ảnh gốc đã chọn |

## Bóng hình từng khung
| Khung | Dáng | Nguồn (seed) |
|---|---|---|
| idle1 | Đứng yên, gậy dựng bên người | `idle` s741003 |
| idle2 | Như idle1, co nhẹ chiều dọc 1,8 % (thở), quầng cầu sáng hơn chút | `idle` s741003 |
| run1 | Người đổ về trước (+9°), áo choàng bay sau, gậy kéo phía sau | `run` s741002 |
| run2 | Giữa sải chân, nhấp lên 10 px, người đổ trước | `run2` s741002 |
| cast1 | Lấy đà: ngả sau (−6°), gậy rút về phía sau đầu, quầng cầu nhỏ | `cast1` s741002 |
| cast2 | Đâm gậy ra trước, tay kia duỗi, người đổ trước (+8°), quầng cầu to và sáng | `cast2` s741002 |
| skill tụ phép | Hai tay giơ gậy, xoáy phép quanh người | `skill_charge` s741002 |
| skill phóng phép | Lao người, chĩa gậy, luồng phép | `skill_release` s741002 |

## Cách làm
1. **Sinh**: mỗi lần 1 nhân vật, 768×1024, nền trắng.
   - Model **Animagine XL 4.0** + **ControlNet OpenPose xinsir** (xương chibi nét dày, góc 3/4 quay phải) + **IP-Adapter Plus SDXL** (CLIP-ViT-H), weight 0,6 linear, end_at 0,8.
   - 30 bước, euler_ancestral, CFG 5.
   - **Ảnh tham chiếu IP-Adapter là lớp thân KHÔNG gậy** tách từ `art-tests/hero-edge-clean/cleaned_png/hero-mage-male.png` (xem `art-tests/mage-anim/rig/`). Nếu dùng nguyên ảnh có gậy, IP-Adapter chép cả quả cầu to lơ lửng vào bố cục.
   - Prompt và seed đầy đủ từng khung: `generation_male.json`.
2. **Tách nền** theo quy trình đã chốt: BiRefNet → pixel trắng trơn thành trong suốt → giữ khối lớn nhất → `gac_matte.clean`.
   - Từ đợt này BiRefNet chạy trên GPU qua `onnxruntime-directml`: khoảng 3,5 s/ảnh thay vì khoảng 47 s trên CPU.
   - Tiền xử lý giữ đúng như rembg; mask lệch tối đa 0,004 so với bản CPU.
3. **Ghép ô**:
   - Nghiêng người theo khung (xoay quanh chân), thêm quầng sáng quả cầu (cast2 mạnh, cast1 nhỏ).
   - **Chuẩn hoá cỡ từng khung** theo khoảng từ chân lên vành mũ, nên mũ, mặt và người cùng cỡ dù mỗi lần sinh to nhỏ khác nhau.
   - Chân đặt ở y ≈ 487.

## QC nam (`qc.json`)
| Tiêu chí | Kết quả |
|---|---|
| Chân thẳng hàng 6 ô | feet_y = 486, 486, 489, 489, 488, 489 → **lệch 3 px** (≤ 3) |
| Alpha ở dải mép 4 px | **0 %** ở cả 8 ô |
| Mỗi ô đúng 1 nhân vật | **1 khối đặc**, 0 mảnh rời ≥ 30 px ở cả 8 ô |
| Mặt rõ, râu bạc, mũ rộng | Có ở mọi khung |

## Hạn chế
- **Gậy không giống hệt nhau giữa các khung**: có khung gậy móc cong, có khung gậy thẳng. Quả cầu xanh và màu gỗ thì nhất quán. Đây là giới hạn khi sinh từng khung riêng; muốn gậy giống hệt thì phải ghép lớp gậy cố định như bản v1.
- Trang trí mũ/áo đổi nhẹ giữa các khung (họa tiết vàng).
- Ở idle, tay không cầm gậy có một chi tiết vàng nhỏ.

## Bản nữ
File: `mage_nu_strip_2520x500.png`, `mage_nu_skill_charge_420x500.png`, `mage_nu_skill_release_420x500.png`, `mage_nu_contact.jpg`, `mage_nu_preview.gif`. Prompt, seed và model từng khung nằm trong `generation_female.json`.

| Khung | Dáng | Nguồn (seed) |
|---|---|---|
| idle1 / idle2 | Đứng, tay cầm pha lê giơ nhẹ, gậy dựng bên người; idle2 thở 1,8 % | `idle` s741012 |
| run1 / run2 | Lao về trước, gậy kéo ngang người, tóc và áo bay sau | `run` / `run2` s741012 |
| cast1 | Lấy đà: gậy rút về phía sau, tay kia chụm quả cầu nhỏ | `cast1` s741012 |
| cast2 | Đâm gậy (đầu vòng) chĩa lên trước, chân dang rộng | `cast2` s741012 |
| skill tụ phép | Hai tay nắm gậy ngang, ánh sáng tụ ở đầu gậy | `skill_charge` s741011 |
| skill phóng phép | Lao người, chĩa gậy dài ra trước | `skill_release` s741012 |

**Vì sao bản nữ phải sinh lại:** ở khung 768×1024, nhân vật nữ không đội mũ nên phía trên đầu còn trống khoảng 400 px. Model tự lấp khoảng trống đó bằng vòm, đĩa trăng hoặc xoáy phép dính liền vào tóc, và gỡ tự động không sạch. Cách sửa: sinh trên **khung 768×768**, xương đặt sát mép trên. Hết hẳn vòm; chỉ 1/14 ảnh còn vòng sáng và ảnh đó không được chọn.

**QC nữ:**
- chân y = 487, 487, 487, 486, 488, 489 (lệch 3 px);
- dải mép 0 % alpha ở cả 8 ô;
- mỗi ô 1 khối đặc, 0 mảnh rời.

**Hạn chế riêng của bản nữ:**
- Gậy và quả cầu khác nhau giữa các khung (gậy gỗ có lúc mũi giáo, có lúc đầu vòng); quả cầu tím không phải lúc nào cũng nằm trên gậy. Vì vậy quầng sáng quả cầu do code chỉ hiện ở một số khung.
- Khung cast2 có vệt sáng xanh mỏng dưới chân, do model vẽ.
- Mắt, tóc, kẹp pha lê và áo xanh ngọc giữ đúng tham chiếu.
