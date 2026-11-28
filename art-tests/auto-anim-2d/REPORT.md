# Thử nghiệm AUTO-ANIMATION-2D: Rigby2D (+ đối chiếu TextRig)

GAME-ART-CORE (Claude), 2026-11-28. **Thử nghiệm, chưa đưa vào game.** Không ghi đè asset gốc, không sửa source game.
Hero thử: **Kiếm Sĩ Nam** (`hero-swordsman-male`, bản đã làm sạch ở Bước A).

## 1. Xác minh công cụ
| | Rigby2D | TextRig |
|---|---|---|
| Repo | github.com/jaisurya-dev-art/rigby2d, commit 064e35c, bản 0.6.1, cập nhật 27/11/2026, khoảng 400 sao, public beta | github.com/blackoutbuild/textrig, commit 24de122, cập nhật 23/09/2026, 11 sao |
| Giấy phép | **MIT hoặc Apache-2.0**; demo có giấy phép riêng | **MIT** |
| Làm được gì | Trình dựng xương 2D đầy đủ (xương, mesh, IK, physics), **AutoRig** từ PSD/SVG/PNG đã tách lớp, dòng lệnh `rigby`, API Python, xuất skeleton JSON 3.8–4.3 / `.skel` và **sprite sheet** (JSON kiểu TexturePacker/Aseprite + PNG). Có runtime JS/PixiJS/Phaser | Agent vẽ đa giác cắt **từ một ảnh phẳng**, tự lấp vùng bị che, xuất rig **DragonBones** |
| Giới hạn chính | **AutoRig không tự cắt ảnh phẳng**: cần các bộ phận nằm ở lớp riêng | Cần pnpm, Chromium headless, tải thêm model u2net khoảng 176 MB; kết quả là rig DragonBones (định dạng cũ) |
| Phần cứng | Node.js 20+; AutoRig, script và xuất sprite **chạy trên CPU**, không cần VRAM | Python + Node + Chromium |

**Chọn**: Rigby2D làm lõi (xương, chuyển động, xuất). Phần **tách bộ phận từ ảnh phẳng** em tự viết (`tools/auto_cut.py`), không cài TextRig vì máy đã có BiRefNet và hero đã tách nền.

## 2. Đã cài (thư mục độc lập `C:\AI\AUTO-ANIM-2D\`)
- **Node.js v26.13.1** bản zip portable, lấy từ nodejs.org, SHA-256 khớp danh sách mã băm chính thức; không cài vào hệ thống.
- Thư viện của Rigby2D (`npm ci --ignore-scripts`, không tải Chromium). Không tải model AI nào, không đăng ký dịch vụ nào.

## 3. Quy trình (`tools/run_pipeline.sh`, 1 lệnh)
1. **Tách bộ phận** (`auto_cut.py`): áo choàng, chân phải, chân trái, thân, tay trái, đầu, tay phải + kiếm.
   - Vùng lấy theo mẫu chibi (`templates/kiemsi_nam.json`), cộng tách theo màu: áo choàng đỏ; kiếm là điểm ảnh thép ít bão hoà dính liền với lưỡi kiếm.
   - Phần bị che phía sau được **lấp màu** để không hở lỗ khi khớp xoay.
2. **Ghép PSD** (`layers_to_psd.mjs`, dùng thư viện `ag-psd` có sẵn trong Rigby2D).
3. **AutoRig** (`rigby autorig`): **16 xương** (hip, chest, head, upperarm/forearm, thigh/shin hai bên) + 4 IK, 7 slot. Nhận đúng 6/7 lớp; áo choàng tự gắn vào xương gần nhất.
4. **Bộ chuyển động** (`anim_humanoid.py`, API Python của Rigby2D): **idle, walk, run, attack, skill, hit, death**.
   - Script dùng tên xương chuẩn của AutoRig, nên **dùng lại được cho mọi hero** rig bằng AutoRig.
5. **Xuất**: sprite sheet JSON + PNG (trang ≤ 2048 px), khung PNG rời, skeleton JSON 4.3 + atlas, GIF xem trước, QC.

## 4. Kết quả (`kiemsi_nam/`)
- **GIF**: `preview_idle.gif`, `preview_walk.gif`, `preview_run.gif`, `preview_attack.gif`, `preview_skill.gif`, `preview_hit.gif`, `preview_death.gif`, `preview_all.gif`. Ảnh tổng hợp: `filmstrip.jpg`. Kiểm tra phần cắt: `parts_check.jpg`.
- **Cho game web/iPhone**:
  - `sheets/loop_idle_walk_run/` (1 trang 1771×1910);
  - `sheets/once_attack_skill_hit_death/` (2 trang, mỗi trang ≤ 1917 px).
  - Định dạng JSON hash TexturePacker/Aseprite, có `frameTags` cho từng chuyển động, `pivot` ở gốc chân, `duration` 83 ms (12 fps). PixiJS/Phaser đọc thẳng; canvas thuần đọc được bằng vài dòng code.
- **Cho runtime xương** (mượt hơn, nhẹ hơn): `skeleton/kiemsi_nam.json` + `.atlas` + `.png`. File dự án `kiemsi_nam_anim.rigby` mở được bằng Rigby2D để chỉnh tay.

| Chuyển động | Số khung (12 fps) | Mô tả |
|---|---:|---|
| idle | 19 | Thở (ngực co giãn), đầu và tay đung đưa nhẹ |
| walk | 10 | Đùi ±20°, nhấp nhô 6 px, tay đánh nhịp |
| run | 6 | Đùi ±34°, nhấp nhô 16 px, người ngả trước |
| attack | 8 | Giơ kiếm lên qua đầu, chém xuống ngang |
| skill | 13 | Giơ kiếm cao, ngực phồng tụ lực, bổ mạnh xuống |
| hit | 6 | Bật lùi, chớp đỏ toàn thân |
| death | 15 | Lảo đảo, ngã nghiêng, mờ dần |

## 5. Đo đạc (máy i5-14400F / RTX 2070S 8 GB / 48 GB RAM)
| Công đoạn | Thời gian |
|---|---:|
| Tách bộ phận + lấp vùng bị che | 1,7 s |
| Ghép PSD | 0,6 s |
| AutoRig | 0,6 s |
| Script 7 chuyển động | 1,6 s |
| Xuất sprite sheet + khung + skeleton | 7,5 s |
| GIF + QC | 10,8 s |
| **Tổng 1 nhân vật (máy chạy)** | **22,7 s** |

- **VRAM**: không đổi trong suốt quá trình (giữ ở 4 312 MiB do ComfyUI đang giữ model); quy trình chạy hoàn toàn trên CPU nên **không có nguy cơ thiếu VRAM**.
- **RAM**: rất thấp (Node + Python, dưới 1 GB).
- **Thời gian người**: lần đầu mỗi hero cần dựng file mẫu vùng bộ phận (khoảng 10–15 phút, Claude làm, không cần anh Do). Các lần sau chỉ là 1 lệnh.

## 6. QC (`qc.json`) và đánh giá theo tiêu chuẩn
| Tiêu chuẩn | Kết quả |
|---|---|
| Không biến dạng bất thường | **Đạt.** Các mảnh xoay cứng theo xương; mesh thân cong nhẹ |
| Không đổi mặt, trang phục | **Đạt 100 %.** Pixel lấy nguyên từ ảnh gốc, không AI vẽ lại |
| Tay chân, vũ khí chuyển động tự nhiên | **Đạt một phần.** Kiếm vung qua đầu rõ ràng; chân ngắn bị giáp và áo choàng che nên bước đi khó thấy |
| Liên tục, không giật | **Đạt.** Nội suy ease, vòng lặp nối liền (bỏ khung trùng ở cuối vòng) |
| Nền trong suốt, không viền thừa | **Đạt.** Alpha ở dải mép 2 px = 0 % ở mọi khung |
| PNG sheet + dữ liệu cho web iPhone | **Đạt.** Trang ≤ 2048 px, JSON có pivot, thời lượng, frameTags |
| Không thiếu VRAM | **Đạt.** Không dùng GPU |

**Lỗi và giới hạn thực tế:**
1. Vài **sợi viền tóc tối** dính vào mép lưỡi kiếm, đi theo kiếm khi vung. Cần làm sạch thêm mép phần cắt vũ khí.
2. Lúc lấy đà, **kiếm vẽ đè lên mặt**, vì lớp tay phải nằm trên cùng. Sửa bằng cách đổi thứ tự vẽ theo khung (Rigby2D có `key_draw_order`).
3. **Vùng lấp phía sau** là màu loang mờ. Chỉ lộ ra khi khớp xoay mạnh (đòn chém), ở cỡ hiển thị 150 px khó thấy.
4. **Chân chibi rất ngắn**, bị váy giáp và áo choàng che, nên walk/run chủ yếu thể hiện qua nhấp nhô và nghiêng người.
5. **Tách bộ phận chưa tự động 100 %**: mỗi hero cần một file mẫu vùng (vị trí cổ, hông, vùng tay cầm vũ khí). Tách hoàn toàn tự động cần thêm model nhận diện khung xương người (DWPose/OpenPose detector, khoảng 200 MB); theo yêu cầu chưa tải model lớn nên chưa làm.
6. Rigby2D đang ở bản public beta (0.6.1).

## 7. Kết luận và đề xuất
- **Rigby2D đáp ứng được** phần xương, chuyển động và xuất: nhanh (khoảng 23 s/nhân vật), miễn phí, chạy local, giữ nguyên ngoại hình, xuất đúng chuẩn web.
- **Hướng AUTO-ANIMATION-2D**:
  1. Thêm detector khung xương (DWPose, chạy được trên 8 GB) để **tự tìm vị trí khớp**, bỏ file mẫu tay → tách bộ phận tự động hoàn toàn.
  2. Giao diện đơn giản: chọn PNG → xem trước phần tách → chọn bộ chuyển động → xem trước → xuất.
  3. Bộ chuyển động `anim_humanoid.py` dùng lại cho cả 6 hero; Rigby2D còn có `retarget_animation` để chép chuyển động giữa các nhân vật.
- **Cho game**: Luna có thể dùng ngay sprite sheet (giống dải hiện tại, chỉ khác bố cục trang), hoặc về lâu dài dùng skeleton JSON + runtime JS để mượt hơn và nhẹ hơn.

## Tái lập
```
C:\AI\AUTO-ANIM-2D\tools\run_pipeline.sh kiemsi_nam <source.png> tools/templates/kiemsi_nam.json
```
Cần Rigby2D tại `C:\AI\AUTO-ANIM-2D\_vendor\rigby2d` (đã `npm ci --ignore-scripts`) và Node tại `C:\AI\AUTO-ANIM-2D\tools\node`.

## 8. Cải tiến v2 (2026-11-28): lấp vùng của TextRig + physics áo choàng và chùm lông
1. **Lấp vùng bị che bằng thuật toán của TextRig** (`tools/third_party/textrig/fill_occlusions.py`, MIT, commit 24de122; chỉ dùng file này, chỉ cần numpy/scipy, **không cài TextRig, không tải model, không cần Chromium**).
   - Vùng nông: kéo dài màu điểm gần nhất.
   - Vùng sâu: khuếch tán hài hoà nhiều tầng (từ thô đến mịn), rồi làm mờ có mặt nạ.
   - Kết quả: hết vệt tối hình que lộ ra phía sau kiếm khi chém (`compare_before_after_frames.jpg`, hàng trên là trước, hàng dưới là sau).
2. **Physics** (Rigby2D physics constraint: inertia 0,6, strength 60, damping 0,85):
   - Chùm lông mũ tách thành lớp `hair_plume` → AutoRig tạo xương `hair` treo từ đầu.
   - Áo choàng đặt tên `tail_cape` → AutoRig tạo chuỗi 3 xương `tail1`–`tail3`, kèm mesh có trọng số.
   - Gắn physics vào cả 4 xương: chùm lông và áo choàng ngả theo quán tính khi vung kiếm, chạy, ngã. Rigby2D chạy physics một vòng trước khi xuất nên vòng lặp nối liền.
3. AutoRig nhận **8/8 lớp**, dựng 20 xương (thêm `hair`, `tail1`–`tail3`).
4. Sửa lỗi phát hiện trong lúc làm: các mảnh vụn dưới 40 px của chùm lông/đầu từng bị gộp vào lớp thân, làm lớp thân cao 576 px và AutoRig đặt sai vai (tay và chuôi kiếm tách khỏi lưỡi kiếm). Giờ mảnh vụn được giao cho phần chạm vào nó nhiều nhất; lớp thân về 344×216.
5. **Thời gian**: tổng **25,1 s/nhân vật** (cắt + lấp vùng 2,7 s). Không dùng VRAM. Mép ô alpha 0 % ở mọi khung.
6. **Còn lại**: sợi viền tóc dính mép kiếm; kiếm vẽ đè mặt lúc lấy đà; ở cỡ 150 px trong game, độ bay của áo choàng còn nhẹ, có thể tăng `strength`/`inertia` nếu Luna muốn rõ hơn.

`compare_before_after.gif`: chạy, chém, skill; trái là trước, phải là sau.
