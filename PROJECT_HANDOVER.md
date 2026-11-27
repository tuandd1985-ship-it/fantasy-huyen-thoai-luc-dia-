# PROJECT HANDOVER — FANTASY: HUYỀN THOẠI LỤC ĐỊA

Tài liệu bàn giao để ChatGPT / Codex / Claude Code tiếp tục phát triển mà không cần phân tích lại từ đầu.
Cập nhật: 2026-11-28. Phiên bản game hiện tại: **v0.3.7**. Chủ dự án: Do (Tony Đỗ) — mọi thay đổi lớn phải được anh duyệt.

## 1–4. Định danh & trạng thái

- **GitHub:** https://github.com/tuandd1985-ship-it/fantasy-huyen-thoai-luc-dia- (lưu ý: tên repo có dấu `-` thừa ở cuối)
- **Chế độ:** Public
- **Branch phát triển:** `main` — commit game mới nhất: `52638110` ("Thêm assets-data-1.js"); trước đó `5065305f` (index.html + assets-data-2.js), `8bb3e49c` (tài liệu).
- **Link chơi thử (production):** https://fantasy-game.tuandd19985.workers.dev — Cloudflare Worker `fantasy-game` phục vụ bản đóng gói một file từ KV namespace `FANTASY_GAME` (key `index_html`). Đã kiểm chứng live: HTTP 200, đủ 10.164.614 bytes, mọi khối script đạt `node --check`.
- **Đồng bộ:** toàn bộ source mới nhất (v0.3.7) ĐÃ có trên GitHub — đã đối chiếu mã băm từng file (index.html, assets-data-1.js, assets-data-2.js, README.md khớp 100%). Kèm commit bàn giao này: `PROJECT_HANDOVER.md`, thư mục `cloudflare/` (worker + script triển khai) và `docs/CHANGELOG.md` cập nhật. Không còn thay đổi nào chưa push.

## 5. Công nghệ

- HTML5 + CSS + **JavaScript thuần (vanilla)** — KHÔNG game engine, KHÔNG thư viện ngoài, KHÔNG bước build.
- Vẽ game bằng Canvas 2D + DOM cho HUD/panel; vòng lặp delta-time.
- Hosting: Cloudflare Workers + KV (tài khoản của chủ dự án; thông tin bí mật/token KHÔNG nằm trong repo — tuyệt đối không đưa token vào code/repo).
- Định hướng tương lai (chỉ là PROPOSED, CHƯA được duyệt chuyển đổi): TypeScript + Phaser 3 + Vite + PWA. **Không tự ý đổi engine/kiến trúc** — xem mục 13.

## 6. Cấu trúc repo & module

```
index.html          Toàn bộ game: engine + DATA + UI (giữ cùng thư mục với 2 file dưới)
assets-data-1.js    Bảng ảnh __A phần 1 (data URI): tranh mở đầu, chân dung, nhân vật
assets-data-2.js    Bảng ảnh __A phần 2: dải khung hình chuyển động
docs/               SPEC.md (chuẩn cao nhất), GDD.md, ART_DIRECTION.md, BALANCE.md,
                    ARCHITECTURE.md, ROADMAP.md, PROGRESS.md, CHANGELOG.md, HUD_V2.md
cloudflare/         worker.js (phục vụ game từ KV) + deploy_game.py (nạp file game vào KV)
```

Vì sao tách 3 file: bản đóng gói một file nặng ~10 MB (41 lượt nhúng ảnh, rút gọn còn 19 ảnh duy nhất) vượt giới hạn một lần đẩy GitHub nên tách ảnh thành 2 file JS. Khi chạy, `index.html` nạp 2 file data trước rồi game tra ảnh qua bảng `__A` (khóa k0–k18).

Phân lớp trong code (bắt buộc giữ, chi tiết ở `docs/ARCHITECTURE.md`): **DATA** (mọi bảng số: quái/boss/đồ/ngọc/skill/map/EXP/tỉ lệ rơi — không hardcode vào engine) · **ENGINE** (vòng lặp, chiến đấu, va chạm, AI quái, camera, minimap) · **GAME STATE** (theo từng nhân vật) · **UI** (HUD V2, PanelManager, màn chọn/tạo nhân vật) · **ASSETS** (manifest `ASSETS`/`ASSET_FILES` khai báo literal mọi đường dẫn ảnh `assets/...` trong bản gốc — phải giữ literal, không nối chuỗi động, để công cụ đóng gói nhúng đủ ảnh) · **STORAGE** (điểm gắn duy nhất `persist()`).

## 7. Tính năng ĐÃ hoàn thành (đã kiểm thử tự động bằng harness chạy engine thật)

- Mở game: màn hình tải (tranh 3 anh hùng chibi + thanh tiến trình thật) → vào thẳng sân khấu chọn nhân vật (thảo nguyên toàn màn); game tự xoay hình 90° khi khung hiển thị dọc, khóa trải nghiệm ngang.
- Chọn/tạo nhân vật: 3 phái (Kiếm Sĩ / Pháp Sư / Cung Thủ) × Nam/Nữ — chibi toàn bộ; panel chi tiết có biểu đồ sao chỉ số; ô nhập tên viền vàng Fantasy, nút Vào game khóa tới khi tên hợp lệ (2–14 ký tự, không trùng); tối đa 3 ô nhân vật, tiến trình tách riêng; nút "Nhân vật đã lưu" khi đã có nhân vật.
- Chiến đấu: đánh tay + AUTO (biết thả diều cho phái xa), phản hồi ngay khi chạm, giữ để đánh liên tục, đệm lệnh trước khi hết hồi chiêu; 4 skill chính/phái mở ở Lv1/8/15/25 + skill phụ; điểm thân thể + điểm skill khi lên cấp.
- Nhân vật có dải 6 khung hình thật (2 đứng thở, 2 chạy bước chân rõ, 2 vung đòn đồng bộ đòn đánh); chạy có quán tính tăng/giảm tốc; không còn lỗi phóng to/thu nhỏ khi chạm nhanh (đã khóa zoom webview).
- Map Rừng Xanh chuẩn: sông + cầu (va chạm thật, đạn bị chặn), vùng an toàn, vùng tinh anh, khu boss; camera bám và dừng ở biên; minimap; HUD V2 (5 icon tròn viền vàng trên phải cạnh minimap, panel mở thì tạm dừng chiến đấu/AUTO và khôi phục đúng trạng thái khi đóng).
- Quái: 4 họ Rừng Xanh (Slime, Goblin, Sói, Goblin bắn cung) khác hành vi; boss Chúa Sói 3 skill có vùng cảnh báo + nổi giận dưới 50% HP. Va chạm trượt theo vật cản, không xuyên, không kẹt.
- Trang bị/ngọc: rơi đồ tự nhặt, mặc/nâng cấp đồ, khảm ngọc theo bảng 7 cấp (code có, xem mục 9 về kiểm chứng); cài đặt đồ họa/âm lượng nhạc–hiệu ứng riêng, rung.
- Kiểm thử đã đạt: AUTO qua màn 1 cả 3 phái (12/12 + 30/30 lượt Pháp Sư), boss 4/4, va chạm + PanelManager đạt, 0 lỗi console.

## 8. Đang dở / chưa thực hiện

- **Lưu tiến trình bền**: bản hiện tại là bản tĩnh — tải lại trang là mất tiến trình. Cần bản server-backed trên Cloudflare (giai đoạn 3; điểm gắn `persist()` đã chừa sẵn).
- 6 map còn lại mới có khung dữ liệu; nội dung/đồ họa chuẩn mới hoàn thiện ở Rừng Xanh. Boss các màn sâu + vòng khảm ngọc trọn vẹn chưa kiểm chứng trực tiếp (cần farm dài).
- Cốt truyện + hệ thống nhiệm vụ (7 viên đá nguyên tố vs Chúa Quỷ), thành phố trung tâm + 9 NPC, kho đồ.
- Trang bị 10 ô + phát sáng +7/+10/+15 + đổi ngoại hình theo đồ (hiện mới đạt một phần ở nhân vật mẫu Kiếm Sĩ Nam).
- Màn hình Kết quả boss, Hồi sinh chuẩn; tính năng mở rộng (pet, set đồ, phụ bản, tháp…) theo `docs/ROADMAP.md`.
- **Chờ chủ dự án duyệt phong cách giai đoạn 1** (nhân vật chibi AI + cơ chế hiện tại) trước khi nhân rộng — và chờ anh test v0.3.7 trên iPhone thật (độ nhạy đòn đánh, chạy mượt).

## 9. Lỗi đã biết / vấn đề mở

- Tiến trình mất khi tải lại trang (mục 8) — hạn chế lớn nhất hiện tại.
- CHƯA test trên iPhone thật; mọi kiểm thử tới nay là trình duyệt/mô phỏng + harness Node. Không tuyên bố "mượt trên iPhone".
- Khung chạy của Cung Thủ Nữ dùng dáng bước–ngắm (AI sinh lẫn dáng ngắm); vài khung Pháp Sư còn sót mảnh nhỏ của nhân vật bên cạnh ở mép ảnh (nhân vật chính nguyên vẹn).
- Chuyển động joystick sau khi tự xoay hình mới kiểm chứng bằng hình học, chưa có probe kéo thực tế.
- File game một file ~10 MB: tải lần đầu chậm trên mạng yếu; bản GitHub phải giữ đủ 3 file cùng thư mục mới chạy.

## 10. Chạy & kiểm thử trên Windows 11

Không cần cài gì ngoài trình duyệt (và Node.js nếu muốn kiểm tra cú pháp):

```bat
git clone https://github.com/tuandd1985-ship-it/fantasy-huyen-thoai-luc-dia-.git
cd fantasy-huyen-thoai-luc-dia-
python -m http.server 8000
:: mở http://localhost:8000 — hoặc mở thẳng index.html bằng trình duyệt
```

- Kiểm tra cú pháp: trích các khối `<script>` trong index.html ra file .js rồi chạy `node --check` từng khối (bản hiện tại: 7/7 đạt ở bản đóng gói, 12/12 đạt ở bản tách file).
- Kiểm thử gameplay: chơi thử ở khung ngang; bật AUTO để soi kẹt đường/va chạm; mở từng panel kiểm tra tạm dừng–khôi phục.
- Triển khai Cloudflare (chỉ chủ dự án/người được ủy quyền có token): nạp bản đóng gói một file vào KV bằng `cloudflare/deploy_game.py`, Worker ở `cloudflare/worker.js`. Quy trình phát hành: Preview → Production, có version + CHANGELOG + phương án rollback.

## 11. Hình ảnh, nhân vật, chuyển động, hiệu ứng

- Ảnh: WebP nhúng dạng data URI. Nhân vật chibi do AI vẽ từ chân dung tham chiếu, nền magenta được tách (keying) bằng PIL/scipy; dải chuyển động 6 khung cắt từ một dải ngang, mỗi khung đã soi bằng mắt.
- Chuyển động trong sân: biến đổi (transform) + đổi khung theo quãng đường chạy (sải chân khớp tốc độ từng phái), bob theo nhịp bước, lật hướng mượt; khung vung đòn đồng bộ thời điểm ra đòn/skill.
- Hiệu ứng chiến đấu: hạt (particle) có trần số lượng, quái ở xa "ngủ" để không lag; vòng cảnh báo vùng nguy hiểm cho skill boss; vũ khí nhân vật mẫu đổi hình theo trang bị.
- Quy ước bắt buộc khi thêm ảnh: khai báo đường dẫn literal trong manifest `ASSETS`/`ASSET_FILES`; giữ phong cách: nhân vật = chibi dễ thương, quái/boss/map = fantasy theo ảnh mẫu `Concept.png` (xem `docs/ART_DIRECTION.md`).

## 12. Tích hợp ảnh từ ComfyUI + SDXL (đang triển khai trên PC của chủ dự án)

- Máy: Windows, RTX 2070 Super; Codex đang cài ComfyUI (thư mục dự kiến `K:\AI\ComfyUI-Local` nếu ổ K là SSD) + kiểm thử 4 ảnh mẫu, ghi thông số (thời gian/VRAM/RAM/nhiệt GPU) vào `test-images/INFO.md`, thông tin môi trường vào `ENV.md`, lưu workflow mẫu `game_asset_basic.json`, có script start/stop và API cục bộ `http://127.0.0.1:8188` (POST `/prompt`). Chưa cài thêm LoRA/plugin ngoài phạm vi đã duyệt.
- Quy ước ảnh cho game: toàn thân, căn giữa, nền phẳng **magenta #FF00FF** để tách nền tự động, xuất PNG, đặt tên `hero_<phai>_<gioi>.png`, `monster_<ten>.png`, `icon_<ten>.png`.
- Luồng tích hợp: ComfyUI sinh ảnh → tách nền/cắt khung (PIL) → khai báo vào manifest ASSETS → đóng gói lại → đẩy GitHub + triển khai Cloudflare → kiểm chứng trên link thật.
- Ưu tiên sản xuất đầu tiên: bộ quái + boss thay cho quái vẽ bằng code; lưu ý bài toán khó nhất là giữ nhân vật nhất quán giữa các khung hình (dùng ảnh tham chiếu + cùng seed/workflow).

## 13. Tài liệu thiết kế & quy tắc đã thống nhất (BẮT BUỘC tuân thủ)

Đọc theo thứ tự: `docs/SPEC.md` (chuẩn cao nhất — toàn bộ yêu cầu đã chốt: 3 phái × Nam/Nữ, skill Lv1/8/15/25, 7 map, nâng cấp + khảm ngọc theo một công thức %, không khóa tính năng theo cấp, HUD V2, chibi toàn bộ, ngang tự xoay, 3 ô nhân vật…) → `docs/GDD.md` (bảng số thiết kế) → `docs/BALANCE.md` (cân bằng) → `docs/ART_DIRECTION.md` → `docs/ARCHITECTURE.md` → `docs/ROADMAP.md` → `docs/PROGRESS.md` / `docs/CHANGELOG.md` / `docs/HUD_V2.md`.

Quy tắc làm việc của chủ dự án:
- Đề xuất chưa được duyệt phải ghi rõ **PROPOSED**, không tự ghi đè SPEC; không thay đổi kiến trúc lớn/viết lại toàn bộ khi chưa có báo cáo gap + duyệt + kế hoạch bảo toàn dữ liệu.
- Không đánh dấu tính năng là hoàn thành khi chưa kiểm thử; không tuyên bố mượt trên iPhone khi chưa test máy thật.
- Sau mỗi thay đổi: thêm dòng vào `docs/CHANGELOG.md`, kiểm tra cú pháp JS, nói rõ đã kiểm chứng gì / chưa kiểm chứng gì.
- Không công khai thông tin bảo mật; token API không bao giờ vào frontend/repo.
