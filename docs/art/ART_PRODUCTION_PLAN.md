# ART_PRODUCTION_PLAN: GAME-ART-CORE

Trạng thái: **PROPOSED, chờ phê duyệt**, trừ 2 điểm đã chốt dưới đây. Chưa cài, chưa tải model, chưa sinh ảnh, chưa sửa source game.

**ĐÃ DUYỆT 2026-11-28** (căn cứ SPEC mục 1b + ART_DIRECTION.md, commit 243c0fa):
1. Sprite giai đoạn mẫu làm 4 hướng: vẽ thật xuống/lên, trái/phải bằng lật ngang. Chuẩn 8 hướng xét lại khi làm animation nhân vật chính thức.
2. Quái/boss chính thức chibi-fantasy đồng bộ hero; boss to và dữ hơn hẳn quái thường trong cùng phong cách.
Phạm vi: Claude phụ trách đồ họa và GAME-ART-CORE (`C:\AI\GAME-ART-CORE`). Codex phụ trách code, GAME-CORE và kiểm thử. Không đụng tới SANEI.
QUY TRÌNH CHUNG (Do chốt 2026-11-28 — thay dòng "Không commit/push/deploy" cũ, Luna sửa trực tiếp theo đối chiếu): làm xong việc gì thì đẩy thành phẩm lên GitHub repo này rồi báo cáo Luna; Luna test, tích hợp và ra việc tiếp theo. Quy trình này áp dụng cho cả Claude, Codex và Luna.

## 1. Nghiên cứu Skill (vòng 2)

| Repo | License | Bản chất | Chạy local / phí | Codex | Phù hợp 8 GB | Quyết định |
|---|---|---|---|---|---|---|
| **SlavaSexton/ComfyUI-Agent-Kit** (125★, 02/11/2026) | Apache-2.0 (≤ v3.1.0 là MIT) | Skill `comfyui` kiến thức rất sâu (2.288 dòng: 75 recipe model, thư viện node, matting nhiều tầng, KNOWN_ISSUES, `workflow_layout.py`) + `comfy_client.py` **chỉ dùng stdlib** | Local-first. Tuy nhiên "in-graph Claude nodes" **tốn API**, và installer cài `comfyui-mcp` qua npm global | Có (cùng định dạng SKILL.md) | Có mục chọn model theo VRAM | ✅ **Dùng phần skill + client**, chép vào thư mục dự án. ❌ **Không chạy installer** (vì ghi vào `~/.agents/skills`, `~/.codex/config.toml`, npm global). Bỏ phần Claude-node trả phí. Đặt `startPolicy=connect` để không tự khởi động ComfyUI khác |
| **NeoAnthropocene/comfyui-mcp-multiagent** | MIT | Fork của artokun/comfyui-mcp: **hơn gốc 3 commit, kém gốc 2.893 commit** | MCP có thể tự cài node, tự tải model, cần token Civitai/HF | Có | Đa số pack là video lớn | ❌ **Loại** (bị bỏ lại, cần Node 22, rủi ro tự cài). Chỉ mượn nội dung `prompt-engineering` (MIT) |
| **AlessandroFazenda/comfyui-agent-skills** | MIT | character / costume / environment sheet + upscale + video H3 | Local (cần comfy-mcp); skill vast.ai tốn tiền | Có | Tác giả đã test RTX 4060 8 GB (klein 4B) | 🟡 **Mượn quy trình**: sheet tham chiếu, "từng món → bộ đồ hoàn chỉnh", plate pack môi trường, duyệt prompt trước khi sinh. Không cài nguyên bộ (luật "mặc tối thiểu" phục vụ video, không hợp game) |
| 0x0funky/agent-sprite-forge (vòng 1) | MIT, 6k★ | Hậu kỳ sprite: QC sheet, soft-matte, cắt khung, căn chân, xuất Godot/Aseprite/GIF; `codeart2d` có **rig animation** | Hậu kỳ chạy local trên CPU. Router sinh ảnh mặc định gọi API trả phí | Có | Nhẹ | ✅ **Dùng** `generate2dsprite`, `generate2dmap`, `codeart2d` (phần rig). **Khóa router**: chỉ nhận PNG từ ComfyUI |
| dcc-mcp-comfyui (vòng 1) | MIT | Adapter MCP an toàn | Local | Có | Có | 🟡 Tham khảo cách validate workflow |
| Comfy-Org/comfy-skills (vòng 1) | MIT | Chạy trên Comfy Cloud | **Trả phí** | Có | — | ❌ Chỉ tham khảo tài liệu kỹ thuật consistency |

## 2. Kiến trúc GAME-ART-CORE (trên ổ C)

```text
C:\AI\GAME-ART-CORE\
  docs\            4 tài liệu này + báo cáo
  review\          bằng chứng đánh giá (ảnh chụp, contact sheet, script trích ảnh)
  reference\       ảnh khóa nhận diện: 6 chân dung + 6 hero (bản sao chỉ đọc từ game) + Concept.png (khi Do gửi)
  skills\          NGUỒN skill dùng chung (định dạng SKILL.md)
    comfyui\                 ← vendor ComfyUI-Agent-Kit (Apache-2.0), ghim commit 0d25905
    generate2dsprite\        ← vendor agent-sprite-forge (MIT), ghim commit 25203d0
    generate2dmap\, codeart2d\  ← như trên
    fantasy-art-director\    (MỚI) luật phong cách riêng của game này, định tuyến tác vụ, quy trình duyệt
    fantasy-prompt-library\  (MỚI) PROMPT_LIBRARY dạng máy đọc được (JSON + md)
    sprite-matte-clean\      (MỚI) tách nền không ám màu (mục 4)
    art-qc\                  (MỚI) kiểm tra chất lượng tự động (mục 7)
  .claude\skills\   → junction tới skills\  (Claude Code)
  .agents\skills\   → junction tới skills\  (Codex; cấp dự án, không ghi vào ~/.agents)
  workflows\       workflow API JSON (mục 6), có số phiên bản
  tools\venv\      venv RIÊNG: numpy, Pillow, scipy, opencv-python-headless (không cài vào venv ComfyUI)
  output\<đợt>\    raw / clean / sheets / qc / metadata
```

- ComfyUI `C:\AI\ComfyUI-Local` **giữ nguyên**: không cài lại, không đổi cờ chạy, không thêm custom node ở giai đoạn A–B. Model mới **chỉ thêm file** vào `models\`.
- Codex dùng chung: cùng skill (qua `.agents\skills`), cùng `workflows\*.json`, cùng lệnh CLI `tools\art.py <lệnh>` (Python thuần).

## 3. Checkpoint và LoRA cho Fantasy RPG 2D (chưa tải, chờ duyệt)

| Model | Vai trò | Dung lượng | License | Đánh giá |
|---|---|---:|---|---|
| SDXL Base 1.0 | Đã có. Map, đạo cụ | 6,5 GB | OpenRAIL++-M | Giữ |
| **Animagine XL 4.0** | **Nhân vật chibi, quái chibi-fantasy, icon** | khoảng 6,5 GB | CreativeML OpenRAIL++-M, thương mại được (kèm điều khoản sử dụng) | ★★★ Ứng viên chính, khớp phong cách k2–k12 nhất |
| Illustrious XL (bản cụ thể) | Phương án B | khoảng 6,5 GB | Mỗi bản một khác, phải kiểm từng file | ★ Chỉ dùng khi Animagine không đạt |
| NoobAI XL | — | — | Cấm thương mại | ❌ Loại |
| Game icon SDXL LoRA (civitai 141066) | Icon | khoảng 0,2 GB | RAIL++-M addendum | ★★ |
| Game Icon Forge LoRA | Icon vật phẩm | cần xác minh | RAIL++-M addendum | ★★ |
| ControlNet OpenPose SDXL (xinsir, cần xác minh) | Khóa dáng theo khung chính | khoảng 2,5 GB | Cần kiểm tra (công bố là Apache-2.0) | ★★★ Chạy bằng **node ControlNet native**. Ảnh xương do script tự vẽ, **không cần custom node DWPose** |
| FLUX.2 klein 4B (fp8 + Qwen3-4B + VAE) | Sửa ảnh theo nhiều ảnh tham chiếu: giữ danh tính, đổi dáng, đổi đồ | khoảng 12,5 GB | Apache-2.0 (bản 9B cấm thương mại, không dùng) | ★★ Node native, **chưa có số liệu trên Turing**, phải đo |
| LayerDiffuse (custom node) | Sinh RGBA gốc | khoảng 1 GB | Code Apache(?) / weight OpenRAIL-M | ⏸ Hoãn, vì cần bật custom node |
| IP-Adapter Plus (custom node, GPL-3.0) | Giữ danh tính bằng ảnh | khoảng 3,4 GB | GPL-3.0 | ⏸ Hoãn, cùng lý do |

Tổng nếu duyệt đủ mức B và C: khoảng 9 GB (B) + 12,5 GB (C). Ổ C còn khoảng 165 GB.
**Không tự động tải**: Claude sẽ liệt kê URL, SHA và license để Do duyệt từng file. Tải xong thì kiểm hash.

## 4. Khắc phục ám màu nền (ưu tiên số 1)

Quy trình `sprite-matte-clean` (chỉ chạy CPU, không cần custom node):
1. **Không ghi màu nền vào prompt.** Bỏ câu "magenta background". Thay bằng `simple background, plain light grey background` và đưa `colored background, gradient background` vào negative.
2. Sau khi sinh, **lấp nền về đúng một màu đã biết**: lấy mask BiRefNet thô, phủ vùng nền bằng xám #7F7F7F và chạy img2img denoise 0,15–0,25 để viền hòa vào màu xám trung tính. Bước này tùy chọn, bật khi viền có tóc rối.
3. **Tách alpha 2 tầng:** BiRefNet (đã có) → *solidify*: lõi (alpha ≥ 0,85, đã lấp lỗ) = 255; chỉ giữ alpha mềm trong **dải viền 1–3 px**. Bước này sửa lỗi "người bán trong suốt" (6.952 pixel đặc).
4. **Khử màu nền theo toán học (color unmixing)**: trên dải viền, F = (I − (1−α)·B)/α với B là màu nền đã biết, sau đó kẹp giá trị. Dùng `forge_matte` (soft-matte + auto-despill của ASF) làm phương án đối chứng.
5. **QC màu viền**: đo tỉ lệ pixel viền lệch về màu nền và ΔE (Lab) giữa viền và lõi lân cận. Ngưỡng đạt: **pixel viền ám < 3 %**, không còn pixel bán trong suốt ở lõi.
6. Áp dụng ngay cho **6 hero hiện có** (k2–k7) để sửa mà không vẽ lại. Ảnh "trước/sau" sẽ có trong đợt mẫu.

## 5. Giữ nhân vật nhất quán + chuyển động tự nhiên

Đề xuất **lai 3 tầng** (rẻ nhất mà nhất quán nhất trên 8 GB):

| Tầng | Dùng cho | Cách làm | Vì sao |
|---|---|---|---|
| **1. Rig cắt mảnh (2D skeletal)** | đứng, chạy, trúng đòn, tử vong, hồi sinh | Từ 1 ảnh chuẩn đã duyệt, cắt thành đầu/thân/2 tay/2 chân/vũ khí/áo choàng, đặt khớp xương, rồi tạo keyframe chuyển động (squash/stretch, overlap tóc và áo choàng, ease in/out) và xuất khung. Tham khảo `codeart2d/rig-animation` (ASF) và **công cụ AI Rig Editor của chủ dự án** (`Desktop\editor game`, có bộ cắt mảnh + xương; chỉ đọc, không sửa) | **Nhất quán 100 %** vì cùng một ảnh. Chuyển động mượt, nhiều khung mà không tốn GPU |
| **2. Khung chính sinh bằng AI có khóa dáng** | đánh thường, 4 skill, dáng đặc biệt | Ảnh tham chiếu + **xương OpenPose do script vẽ** → ControlNet (Animagine), cùng seed, cùng prompt nhận diện. Hoặc FLUX.2 klein 4B: "ảnh 1 = nhân vật, ảnh 2 = dáng". Sau đó QC palette so với ảnh chuẩn | Dáng mạnh, rõ hành động mà rig không làm đẹp được |
| **3. Hậu kỳ chuẩn hóa** | mọi khung | Căn chân (anchor), cùng tỉ lệ, khóa palette về màu ảnh chuẩn, `sheet_qc` (ASF): phát hiện mảnh lọt khung, khung trùng, trôi NCC | Sửa đúng những lỗi đang có ở k13–k18 |

Nguyên tắc nhất quán (theo Comfy-Org và Alessandro):
- Một bộ tham chiếu cố định cho mỗi nhân vật (turnaround + palette + 3 dấu hiệu nhận diện).
- **Không dùng output trước làm tham chiếu**, tránh trôi tích lũy.
- Tên và thông số nhận diện cố định trong prompt; cố định seed cho mỗi nhân vật.
- Vũ khí là **sprite rời gắn vào tay** nên đổi đồ không phải vẽ lại nhân vật (đáp ứng "trang bị đổi ngoại hình thật").

Video image-to-video (Wan/LTX) **không đưa vào kế hoạch**: model 14B cần lớn hơn 8 GB. Bản 5B chạy rất chậm trên Turing, kết quả còn phải key lại. Chỉ ghi nhận để nghiên cứu sau.

## 6. Workflow ComfyUI sẽ dựng (API JSON, chỉ dùng node native)

| ID | Mục đích | Model | Đầu ra |
|---|---|---|---|
| `wf_ref_sheet` | Bảng tham chiếu 4 góc của nhân vật/quái | Animagine | 1536×1024 nền xám |
| `wf_char_pose` | Khung chính theo xương | Animagine + ControlNet OpenPose | 1024 → 512 |
| `wf_char_edit` | Đổi dáng/đồ giữ danh tính (giai đoạn C) | klein 4B ReferenceLatent | 1024 |
| `wf_monster` / `wf_boss` | Quái/boss chibi-fantasy | Animagine | 1024 (boss 1024–1344) |
| `wf_map_tile` | Tile đất liền mạch | SDXL base + tiling (circular padding nếu có node native; nếu không thì offset + inpaint mép) | 1024 |
| `wf_map_props` | Pack vật thể trên nền xám | SDXL/Animagine | sheet 4×4 |
| `wf_icon` | Icon skill/đồ/ngọc | Animagine + Game icon LoRA | 1024 → 128/96/64 |
| `wf_ui_frame` | Khung viền vàng cổ 9-slice | SDXL | 1024 |
| `wf_refine` | img2img làm sạch, denoise thấp | cùng model | |

Thông số mặc định trên 8 GB: 1024², batch 1, 25–28 bước, dpmpp_2m karras / euler_a, CFG 5–7. Giữ `--reserve-vram 1`.

## 7. Kiểm tra chất lượng tự động (`art-qc`)

Chạy sau mỗi ảnh, ghi `qc.json` và **contact sheet trên 4 nền** (đen, trắng, cỏ map, nền đã key):

| Nhóm | Phép đo | Ngưỡng đạt (khởi điểm) |
|---|---|---|
| Alpha | % lõi đặc; lỗ trong lõi; số đảo rời; chạm mép khung | lõi ≥ 99 % đặc; 0 lỗ; 0 đảo lớn hơn 0,3 % diện tích; không chạm mép |
| Ám màu | % pixel viền lệch về màu nền; ΔE viền-lõi | < 3 %; ΔE < 12 |
| Palette | ΔE trung bình giữa 8 màu chủ đạo và palette tham chiếu | < 8 |
| Hình dáng | Chiều cao/bề rộng so với chuẩn; đường chân (anchor) | ±4 %; ±2 px |
| Dải khung | Khung trùng (NCC > 0,98); mảnh lọt (`sheet_qc spill`); trôi tỉ lệ | 0 |
| Độ nét | Phương sai Laplacian ở kích thước hiển thị | lớn hơn hoặc bằng mức của hero hiện có |
| Kỹ thuật | Kích thước, RGBA, dung lượng WebP | đúng chuẩn mục 5 GAME_ART_REVIEW |

Ảnh nào trượt sẽ bị đưa vào `rejected\` kèm lý do, và **không ảnh nào tự động vào game**. Bước cuối là Claude xem contact sheet bằng mắt rồi Do duyệt.

## 8. Lộ trình (mỗi bước dừng chờ duyệt)

| Bước | Việc | Cài / tải | Đầu ra để Do duyệt |
|---|---|---|---|
| **A** | Dựng GAME-ART-CORE: vendor skill, venv riêng, viết `sprite-matte-clean` + `art-qc`, workflow trên SDXL hiện có | khoảng 80 MB pip | **Trước/sau làm sạch viền 6 hero hiện có** + QC báo cáo |
| **B** | Tải Animagine XL 4.0 + ControlNet OpenPose (+ LoRA icon) | khoảng 9 GB | **Bộ ảnh mẫu phong cách** (4 hướng: vẽ xuống/lên + lật): 1 hero (Kiếm Sĩ Nam) có turnaround, 3 dáng chính, chạy 8 khung rig; Goblin + Sói + Slime + Goblin Cung Thủ theo `MONSTER_DESIGN_RUNG_XANH.md`; Chúa Sói; 1 góc Rừng Xanh (tile + 6 vật thể); 6 icon (3 skill, 2 đồ, 1 ngọc); 1 khung panel viền vàng. Có so sánh "SDXL không skill" với "GAME-ART-CORE". **PHẦN QUÁI RỪNG XANH TRONG BƯỚC B: TẠM HOÃN** (Do/Luna chốt 2026-11-28) — Codex đang sản xuất lô mẫu SDXL theo MONSTER_DESIGN_RUNG_XANH; chờ Luna đánh giá chất lượng lô đó rồi mới quyết có làm lại bằng Animagine hay không. Bước A triển khai trước |
| C (tùy chọn) | FLUX.2 klein 4B: đo VRAM/thời gian, so với ControlNet | khoảng 12,5 GB | Bảng so sánh nhất quán |
| D | Sản xuất hàng loạt theo ASSET_INVENTORY, Rừng Xanh trước | — | Theo từng gói |
| — | Bàn giao asset cho **Codex** tích hợp (manifest, atlas, nạp theo map) | — | Claude không sửa `index.html` |

## 9. Ghi chú cho Codex (không phải việc của Claude)
- Lộ vùng đen ở biên dưới Rừng Xanh khi spawn (ảnh `02_ingame_spawn_black_void.jpg`).
- Bản đóng gói 10 MB: khi thêm khoảng 1.500 khung, cần atlas WebP và nạp theo map, không nhúng hết vào một file.
- DATA có 23 quái, GDD liệt kê thêm vài họ chưa có. Cần chốt danh sách trước khi Claude vẽ.
