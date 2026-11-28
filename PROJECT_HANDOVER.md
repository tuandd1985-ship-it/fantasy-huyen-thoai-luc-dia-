# PROJECT HANDOVER — FANTASY: HUYỀN THOẠI LỤC ĐỊA

**Cập nhật: 2026-11-28 ~23:40 JST, bởi Luna (Muse).** Tài liệu này là điểm bắt đầu cho BẤT KỲ agent nào (Claude, Codex, Luna phiên sau) vào làm tiếp. Đọc hết trước khi sửa code. (Bản bàn giao cũ ở v0.3.7 đã được thay thế hoàn toàn bởi bản này.)

---

## 1. Trạng thái hiện tại (sự thật đã kiểm chứng)

- **Bản LIVE: v0.8.0 + 2 đợt sửa lỗi nóng (tối 2026-11-28)** tại https://fantasy-game.tuandd19985.workers.dev — anh Do test trên iPhone qua link này (Safari / icon màn hình chính, KHÔNG qua webview của app Muse).
- GitHub repo này (`main`) chứa source `index.html` + `assets-data-*.js` tương ứng bản live. Mọi thay đổi phải giữ đồng bộ 2 nơi: Cloudflare (live) ↔ GitHub.
- Anh Do vừa test bản sửa lỗi cuối và CHƯA xác nhận lại sau đợt sửa thứ hai (hộp thoại NPC kẹt + camera). Nếu anh báo vẫn lỗi, ưu tiên xử lý trước mọi việc khác.

## 2. Game là gì

Action RPG chibi fantasy 2.5D cho điện thoại (landscape): joystick 8 hướng, camera bám hero, AUTO + đánh tay, 3 phái × nam/nữ (Kiếm Sĩ / Pháp Sư / Cung Thủ), mỗi phái 4 skill chính (mở Lv1/8/15/25) + 2 buff chủ động + 2 bị động. Trang bị 4 slot (Vũ khí, Áo giáp, Giày, Nhẫn), cường hoá +cấp (+8%/cấp), khảm ngọc, ghép 3 ngọc cùng loại+cấp. Tối đa 3 nhân vật/thiết bị, lưu localStorage (autosave). Tài liệu gốc: `docs/` (SPEC.md là luật cao nhất, GDD, ART_DIRECTION, BALANCE, ARCHITECTURE, ROADMAP, PROGRESS, CHANGELOG, GAP_ANALYSIS).

## 3. Kiến trúc & cách deploy (ĐỌC KỸ — khác thường)

- Source thật của game là một **Space (web artifact) phía Luna**, không nằm trong repo này. Repo này là bản sao phát hành: `index.html` (bản split) + `assets-data-1..25.js` chứa toàn bộ asset dạng data URI (~57MB tổng). **Đừng sửa tay các file data** — chúng được sinh từ bản export bằng script split (chia để không file nào vượt giới hạn KV 25MB/key và giới hạn đẩy GitHub).
- Live chạy trên Cloudflare Workers + KV (namespace FANTASY_GAME): Worker phục vụ `/` từ key `index_split`, `/assets-data-N.js` từ key `data_N`, `/health` → ok, `/mono` → redirect `/` (định dạng monolith đã bỏ từ v0.7.0).
- Quy trình phát hành của Luna: sửa Space → export → `node --check` 7 khối script → split → deploy KV → đối chiếu byte-size từng file data với live → cập nhật docs → push GitHub (so blob trước, chỉ đẩy file đổi; đẩy TỪNG file data một vì đẩy cặp >~6MB bị HTTP 413).
- Token Cloudflare nằm trong Secure Vault của Luna — **không bao giờ ghi token vào code/frontend/repo**.

## 4. Thế giới game (v0.8.0 — thay thế hẳn cơ chế "màn" cũ)

- **17 map liên thông, KHÔNG khoá màn, KHÔNG điều kiện qua màn** (chỉ đạo của anh Do): đánh quái → làm nhiệm vụ → lên cấp; dải cấp chỉ là gợi ý.
- Điểm bắt đầu: **Làng Khởi Đầu** (`lang`) — map an toàn, 4 NPC tạm do Luna tạo: Trưởng Làng (3 nhiệm vụ treo thưởng lặp lại), Thương Nhân (mở shop), Thợ Rèn (mở cường hoá), Y Sĩ (hồi đầy HP/MP miễn phí). NPC dùng dải idle bộ phận của hero làm hình tạm.
- Di chuyển: **15 cặp cổng đá 2 chiều** (Băng 1 ⇄ Băng 2 có 2 cặp bắc/nam) + **bảng Dịch chuyển** trong panel bản đồ lớn (chạm map là tới safe zone, miễn phí).
- Chuỗi map: Làng → Thảo Nguyên 1 (rung_xanh_v2) → Thảo Nguyên 2 (tranh map_1 cũ) → Thảo Nguyên Băng (map_3) → Băng Nguyên 1 (map_4) ⇄ Băng Nguyên 2 (bang_tuyet) → Sa Mạc Hoang Mạc (hoang_mac_nui_lua) → Núi Lửa (map_5); nhánh: Hang Tối (hang1) → Hang Pha Lê (hang_pha_le), Hang Băng (hang2), Hang Lửa (hang3); 3 Đấu Trường boss (bossxuan/boss_bang/bosslua — boss hồi sinh 5 phút). **Đầm Lầy Độc + Lâu Đài Bóng Đêm: có trong danh sách, trạng thái "Sắp mở"** — chưa có tranh (Codex chưa vẽ).
- Va chạm: lưới RLE của Claude cho 14 map ở `art-tests/maps-desktop-v2/maps_collision.json` (5 map mới, 100×100, thế giới 2800×2800) và `art-tests/maps-anh-do/collision/maps_collision.json` (9 map cũ, 100×80). Game giải mã 2 JSON này lúc khởi động (chúng nằm trong assets của Space: `assets/maps2/`). Luna đã kiểm: mọi map vùng đi được là 1 vùng liên thông lớn nhất áp đảo; map_3/map_5 có túi nhỏ tách rời → engine có quy tắc **vùng lớn nhất**: mọi điểm spawn/cổng/NPC/đáp dịch chuyển đều bị ép vào vùng liên thông lớn nhất.
- Quái biome (rig bộ phận Codex + Claude lắp, Luna QC đạt): **bat** (hang, bay bổ nhào), **mummy** (sa mạc, tank chậm), **fireDragon** (núi lửa, đánh xa, ×1.3; bản cỡ boss ở Đấu Trường Lửa), **iceWolf** (map băng, cận chiến nhanh; bản Vương ở Đấu Trường Băng). **toad + wraith đã đăng ký dữ liệu nhưng CHƯA spawn** (chờ tranh Đầm Lầy/Lâu Đài). Quái Rừng Xanh cũ (slime/goblin/wolf/goblinArcher/goblinShaman) giữ nguyên; Goblin Shaman đã có trong vùng elite của Thảo Nguyên 1.

## 5. Phân vai (anh Do chốt 2026-11-28)

- **Codex = vẽ tĩnh**: hero/monster tách bộ phận, tranh map, icon. Vẽ nhân vật chuyển động thì tách sẵn bộ phận (mỗi bộ phận 1 PNG trong suốt trên canvas chung 768×640, chân y=620, `parts.json` có trục + thứ tự lớp, kèm `assembled.png` + `comparison.png`).
- **Claude = animation & kỹ thuật hình**: lắp ghép chuyển động TỪ bộ phận (chỉ xoay/dịch quanh trục, không tự vẽ), tách lớp map, upscale, lưới va chạm. Đầu ra: dải PNG + `animations.json` (durations_ms + hit_frame) + GIF xem trước + REPORT.md, đẩy vào `art-tests/`.
- **Luna = game**: hướng đi/spec, bố cục/HUD, tích hợp mọi asset vào engine, QC độc lập mọi lô (tự ghép chồng đo lệch pixel, đo từng ô dải), deploy Cloudflare + đồng bộ GitHub, viết lệnh giao việc cho Codex/Claude (anh Do chuyển tiếp).
- Anh Do đã **uỷ toàn quyền cho Luna** trong workflow game (tự quyết, không hỏi từng bước) — nhưng thẻ duyệt của nền tảng Muse cho thao tác ghi ra ngoài (push GitHub) là khoá hệ thống, Luna không tắt được; cách giảm: gom việc, đẩy ít lần.

## 6. Chuẩn asset đã nghiệm thu (đừng phá)

- Hero: cả 6 nhân vật có bộ phận (QC ghép chồng lệch **0px**) + dải idle/run/skill-1 do Claude lắp, đã vào game v0.7.2 (thư mục Space `assets/anim2/`, ô 768×640, chân 620). Kiếm Sĩ Nam thêm bộ skill key-pose đủ 4 skill (v0.7.0, `assets/anim/`).
- **Chuẩn hoá kích thước hero (bài học đắt giá)**: các dải có chiều cao hình thật KHÁC nhau (bộ phận ~586px, key-pose ~470px, dải cũ ~476px). Engine nay **tự đo khung bao alpha thật của từng dải/từng khung lúc nạp** và chuẩn hoá mọi trạng thái về chiều cao vẽ 105px. TUYỆT ĐỐI không quay lại hằng số tỉ lệ cố định cho mọi dải — đó là nguồn lỗi "đứng một cỡ, đánh một cỡ" anh Do đã báo.
- Icon: hệ icon phẳng của Codex (48 icon, `assets/icons2/`) là hệ chính từ v0.7.1; bộ icon vẽ tay của Luna (`assets/icons/`) là dự phòng. Icon áo/giày theo bậc (48 icon, `assets/equip/`) hiện trong Túi đồ/Trang bị theo phái+giới+bậc cấp món (1–19→lv1, 20–39→lv20, 40–59→lv40, 60+→lv60) — chỉ hiển thị.
- HUD: bố cục V3 (cụm skill vòng cung quanh nút đánh thường dưới-phải; hàng icon tròn có nhãn trên-phải cạnh minimap; panel dạng cửa sổ nổi, mở panel = tạm dừng combat/AUTO, đóng khôi phục đúng trạng thái). Cụm fight-pad tự thu nhỏ theo chiều cao khung (×0.82 <540px, ×0.7 <440px).

## 7. Hai sự cố live ngày 2026-11-28 và cách đã sửa (đọc để không tái phạm)

1. **Vào game chỉ thấy UI, không thấy map/nhân vật**: hero khởi tạo thiếu `y` → khung vẽ đầu tiên gọi gradient với NaN → vòng lặp game chết hẳn (rAF đăng ký ở cuối loop). Đã sửa: hero có toạ độ hợp lệ từ đầu; loop đăng ký rAF NGAY ĐẦU vòng; guard isFinite cho gradient. → Bài học: vòng lặp phải tự cứu; không để 1 lỗi khung hình giết cả game.
2. **Kẹt hộp thoại NPC + camera phóng to mờ + minimap sai hình** (ảnh iPhone thật của anh Do): hộp tương tác NPC có scrim phủ kín chặn joystick nên không đi ra được để hộp tự đóng → thêm nút ✕ riêng + scrim mềm (pointer-events:none) + không bật lại khi còn đứng cạnh; canvas lệch kích thước khi webview đổi khung không bắn sự kiện → gán style width/height tường minh + watchdog resize trong loop; minimap vẽ trước khi tranh tải xong → chỉ vẽ khi naturalWidth>0 và vẽ lại khi onload. → Bài học: **mọi bản phát hành phải có probe RENDER THẬT vào được gameplay** (v0.8.0 chỉ test logic nên lọt lỗi này tới tay anh Do).

## 8. Việc đang dở / tiếp theo (theo thứ tự ưu tiên)

1. **Chờ anh Do xác nhận bản sửa lỗi thứ hai** (mục 7.2). Nếu còn lỗi → sửa tiếp trước mọi việc.
2. **Hoàn thiện redesign v0.9.0** theo brief của anh Do + 5 ảnh tham chiếu (`docs/art/ui-reference/ref-1..5`): design system navy #14263D / khung #294C70 / viền vàng #D5AC60 / chữ #F5E8CA. ĐÃ VÀO ở đợt sửa lỗi: nền fullscreen thật (đã bỏ CSS rotate — máy dọc hiện nhắc xoay, PWA standalone + orientation landscape khai báo manifest), 5 panel icon (Nhân Vật/Túi Đồ 8×5/Trang Bị 4 slot/Kỹ Năng/Cài Đặt) đúng áo + ✕ + cuộn trong panel. CÒN THIẾU: màn **Chọn nhân vật theo ref-5** (slot trái, hero lớn giữa chạy idle, thông tin phải, nút Vào game nổi bật) và rà soát đối chiếu từng màn hình với ảnh mẫu. BẤT BIẾN: không thêm Lực Chiến/tiền tệ/slot mới (ảnh mẫu có nhưng game không có — dữ liệu game thắng ảnh), không đổi công thức/save.
3. **Tối ưu tải**: tổng ~57MB nạp lần đầu là nặng. Hướng đã thống nhất: **lazy-load theo map** (chỉ tải asset của map khi vào) — làm cùng đợt rollout map mới.
4. **Claude còn nợ**: skill 2–4 + đánh thường + trúng đòn cho 6 hero từ bộ phận; **Codex còn nợ**: 2 biến thể tay cầm kiếm + bộ phận nhìn nghiêng của Kiếm Sĩ Nam; tranh **Đầm Lầy Độc** và **Lâu Đài Bóng Đêm** (vẽ xong thì spawn toad/wraith + mở 2 map); map Rừng Xanh "sạch" mới (ít chi tiết vụn, đất trống dễ đọc) thay dần tranh cũ nếu đạt QC.
5. **Chưa quyết** (đừng tự ý làm): lưu server đa thiết bị — giai đoạn sau, chưa làm.
6. **Capacitor**: nếu anh Do muốn khoá fullscreen cứng kiểu app native (iOS không cho web/PWA khoá xoay/fullscreen bằng code), phương án đóng gói Capacitor đã được Luna nêu — chờ anh quyết, chưa triển khai.

## 9. Quy tắc làm việc bất biến

- SPEC.md là luật cao nhất; đề xuất chưa duyệt ghi PROPOSED, không ghi đè SPEC; thay đổi lớn phải có gap report + anh Do duyệt + kế hoạch bảo toàn dữ liệu.
- Không bao giờ tuyên bố "mượt trên iPhone" từ test desktop; FPS 60 phải đo trên máy thật (game có đồng hồ FPS bật trong Cài đặt).
- Báo cáo với anh Do: NGẮN, tiếng Việt, chỉ nói đã xong gì + anh cần xem gì. Bảng thông số dài để trong tài liệu như file này.
- Lệnh giao cho Claude/Codex: để TOÀN BỘ trong MỘT code block để anh Do chạm copy 1 lần.
- Khi Luna đọc code trên GitHub phải nói rõ repo/branch/đường dẫn file.
