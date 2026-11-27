# FANTASY_PROJECT_REVIEW — tiếp nhận v0.3.7

Ngày thực hiện: 2026-11-28, Windows 11. Trạng thái: **REVIEW / PROPOSED — chưa triển khai sửa game**.

## 1. Kết luận và phạm vi

Đã clone repository vào `fantasy-rpg-review/repository`, đọc `PROJECT_HANDOVER.md` và `docs/SPEC.md` trước khi kiểm tra source. Đã đọc thêm GDD, BALANCE, ARCHITECTURE, ROADMAP, PROGRESS, ART_DIRECTION, CHANGELOG và HUD_V2.

- Baseline bàn giao: **`02ec5850e865f834321143e86adf4fadb3c62964`**, nhánh main tại lúc clone; không có tag Git `v0.3.7`. Nhãn v0.3.7 lấy từ bàn giao/CHANGELOG, không suy ra từ tên tag.
- Game là HTML/CSS/JavaScript thuần, Canvas 2D + DOM, không framework/build tool. `index.html` có **4.402 dòng**, 322.265 bytes.
- Có game loop, cấu hình DATA, 3 phái/6 ngoại hình, AUTO, 7 map dữ liệu, đồ/ngọc, collision và PanelManager thực tế. Đây là nền tảng nên kế thừa.
- **Chưa đạt nghiệm thu đầy đủ:** reload mất nhân vật/cài đặt; các đường pause chưa thống nhất; có lỗi đóng bản đồ ở viewport thấp; AUTO còn seed kẹt; công thức chỉ số và mana shield có sai lệch được kiểm chứng.
- Không đổi gameplay, framework, TypeScript, Vite hay Phaser; không deploy Cloudflare; không sửa các dự án SANEI.
- Ngoại lệ push được chủ dự án cho phép trong lúc review: chỉ ảnh thử/INFO trong `art-tests/comfyui-round1/`, commit `b2b38da7d8db525367331c5599d33f2e22122a5c`; vòng AI segmentation bổ sung `art-tests/comfyui-round2/`, commit **`49d41ea2921dbf40f74ac7fc7416fdbfc80f3b16`** (4 raw, 4 cut, INFO). Đã xác nhận remote main khớp commit và source game/docs/Cloudflare không khác baseline. Không coi việc duyệt ảnh thử là duyệt sửa source. Chủ dự án sau đó cho phép đẩy báo cáo này và bằng chứng để Muse đọc; việc công bố báo cáo không phải phê duyệt sửa game.

## 2. Bằng chứng và khả năng lặp lại

Các liên kết bằng chứng dưới đây dùng được trực tiếp trên GitHub. JSON/ảnh giữ nguyên từ lần kiểm thử; đường dẫn Windows trong log chỉ vị trí máy kiểm thử, không phải đường dẫn máy Muse:

| Bằng chứng | Nội dung |
|---|---|
| [static-audit.json](reviews/v0.3.7/evidence/static-audit.json) | SHA-256/size toàn bộ file baseline, script checks, ảnh và đối chiếu production |
| [production-http.json](reviews/v0.3.7/evidence/production-http.json) | HTTP 200 và header của production |
| [review-tests.json](reviews/v0.3.7/evidence/review-tests.json) | Kết quả UI, state probes, 46 lượt mô phỏng và frame timing |
| [first-run-bigmap-failure.json](reviews/v0.3.7/evidence/first-run-bigmap-failure.json) | Playwright không bấm được nút đóng bản đồ do ngoài viewport |
| [stall-reproduction.json](reviews/v0.3.7/evidence/stall-reproduction.json) | Hai seed kẹt tái hiện trong trang mới, có tọa độ và diễn biến |
| Trace Playwright | Giữ local, 31,47MB; không đưa blob lớn lặp ảnh vào repo. SHA-256 có trong evidence-manifest.json. Ảnh/JSON liên quan đã công bố. |
| [comfy-api-check.json](reviews/v0.3.7/evidence/comfy-api-check.json) | GET system_stats/queue/history của hai request sinh ảnh thật |
| [review-tests.cjs](reviews/v0.3.7/review-tests.cjs) | Harness kiểm tra, không phải source game |
| [reproduce-stalls.cjs](reviews/v0.3.7/reproduce-stalls.cjs) | Repro cô lập seed 109/130 |

Môi trường: Node **24.22.3**, Playwright-core **1.65.1**, Chrome **147.0.7727.139**, viewport chủ yếu **844×390, DPR 1**, thêm **390×844**. Không có npm trong PATH; đã dùng gói Playwright-core chính thức, tận dụng Chrome có sẵn, không cài browser hoặc package vào game.

Đã khởi động HTTP server chỉ bind 127.0.0.1:8765. Chrome/curl không kết nối được cổng này trong môi trường thực thi dù socket có LISTEN. Vì vậy kiểm thử browser hoàn thành bằng **file://**, chế độ được bàn giao hỗ trợ. Đây là giới hạn kiểm thử HTTP local, chưa có bằng chứng quy lỗi đó cho game. Production được tải qua HTTP thật rồi thực thi bản capture bằng file://; không tuyên bố đã thao tác browser trực tiếp trên production. Font Google được chủ động chặn trong browser test để ổn định, lỗi request font được phân biệt với lỗi app. Chưa kiểm thử Safari/WebKit, iPhone/Android thật, safe-area phần cứng hoặc phiên chơi dài 20–30 phút.

Cách chạy lại harness portable và giới hạn bản công bố: xem [reviews/v0.3.7/README.md](reviews/v0.3.7/README.md). Không cần sửa source game. Gói test dùng Playwright-core 1.65.1 và Chrome có sẵn. File production HTML 10,16MB và trace 31,47MB giữ local; không nhúng lặp vào GitHub. Kết quả đã ghi của T14 vẫn có trong JSON; runner công bố sẽ SKIP T14 nếu chưa cung cấp capture riêng.

Harness thay trạng thái trong **trang test**, không ghi source. Mô phỏng dùng engine thật, LCG seeded, dt=0,05 giây, timeout 600 giây game; tạm thay hàm UI/audio/minimap bằng no-op để chạy nhanh, không đổi CONFIG/balance. Đây là **giây mô phỏng**, không phải thời gian chơi trên điện thoại. Không được lấy frame timing của harness để kết luận FPS thực tế.

## 3. Đối chiếu bàn giao với source và production

| Nội dung bàn giao | Kết quả đối chiếu |
|---|---|
| Game đã lên production, 10.164.614 bytes | HTTP 200; body capture đúng **10.164.614 bytes**. Header `Cache-Control: no-store`. |
| Source tương ứng production | **6/7 khối script game khớp nguyên văn**. Khối đầu còn lại khớp sau thay data URI bằng khóa `__A.k*` theo ảnh tương ứng. Điều này xác nhận logic JS được kiểm tra khớp, không có nghĩa toàn bộ HTML giống byte-for-byte. |
| 19 ảnh duy nhất | Tìm thấy đúng **19 WebP**, gồm intro, 6 portrait, 6 hero, 6 strip 2520×500. |
| Kiểm tra cú pháp 12/12 source, 7/7 bundle | Lần này source có **13 thẻ script** tính cả bootstrap/helper và 2 file external; **13/13 PASS**, production **7/7 PASS**. Khác cách đếm/đóng gói so với ghi chú, không phải lỗi cú pháp. |
| 0 lỗi console | Bản repo có exception `Cannot set properties of null (setting 'src')` tại `index.html:554:119`; request placeholder `__ASSET_k0__`, `__ASSET_k1__` thất bại. Bản production capture không có JS exception trong probe tương đương. |
| Lưu tiến trình còn dở | Đúng: `Save.load()` luôn fresh, `Save.persist()` rỗng (`index.html:1094–1112`). Reload mất roster/cài đặt. Không cần có server mới lưu được trên máy. |
| AUTO 12/12 + 30/30 mage, boss 4/4 | Harness Muse không có trong repo. Kiểm tra độc lập đạt 12/12, **28/30 mage**, 4/4 boss theo fixture nêu dưới; không xác nhận lại được đúng tập seed/fixture Muse. |
| GAME STATE/STORAGE tách biệt | Có đối tượng Save/Roster và các module tên riêng, nhưng hầu hết phụ thuộc biến lexical global `P`, `hero`, arrays, UI và CONFIG. Chưa phải các module độc lập. |
| Manifest chứa literal `assets/...` | Bản repo thực tế tra `__A.k0…k18`, không có cây `assets/` gốc. Cần bổ sung source manifest/đóng gói chính thức trước khi mở rộng art. Không tự phục hồi đường dẫn bằng đoán tên. |
| README nói Worker phục vụ cả 3 file | `cloudflare/worker.js` chỉ trả `/`, `/index.html`, `/health`; URL khác 404. Production hiện dùng bundle một file từ KV; lời README đã lệch. |
| TEST_REPORT, GAP_ANALYSIS, Concept, DESIGN-V2 | Các file được nhắc không có trong repo. `docs/GDD.md` mang tiêu đề DESIGN V2 và có số liệu, nhưng ảnh Concept/ZIP và harness gốc thiếu. |

`docs/PROGRESS.md` vẫn cập nhật đến v0.3.3 và các ghi chú ART_DIRECTION/GDD/HUD có đoạn cũ (bán hiện thực, dock dưới, lớp phủ yêu cầu xoay máy) trong khi bàn giao/README nói chibi và tự xoay 90°. Cần bảng quyết định theo ngày, ưu tiên SPEC/HUD_V2 và các phê duyệt sau cùng; **không dùng mâu thuẫn tài liệu để tự đổi hành vi baseline**.

## 4. Kết quả kiểm thử chức năng

| ID | Kiểm tra | Kết quả / giới hạn |
|---|---|---|
| T01 | Boot local, preload | Game vào được sân chọn; 6 heroArt và 6 heroAnim tải được. Có exception helper ảnh như trên. |
| T02 | Tên ngắn/ký tự đặc biệt/tên hợp lệ | `A`, `Bad<>` bị chặn; `ValidHero` được bật Start. Chưa kiểm đầy đủ Unicode normalization/trùng tên và xóa 3-slot qua UI trong vòng này. |
| T03 | 3 phái × 2 giới | **6/6** tạo và vào game đúng class/gender, sheet có ảnh; chỉ số cùng phái không đổi theo giới. Phái được đặt trong fixture rồi nút Start được bấm thật; chưa bao phủ toàn bộ hit-target chọn phái trên canvas. |
| T04 | 5 panel, AUTO off/on | **10/10** open/close giữ cờ AUTO, pause và xóa joystick. Settings dùng overlay riêng, không tính như `.panel.active`. Chưa đủ chuỗi mọi thao tác chạm ngoài/chuyển panel trên iPhone. |
| T05 | Minimap → bản đồ lớn | Overlay hiện nhưng `uiPause=false`; không đi qua PanelManager. |
| T05b | Đóng bản đồ trên 844×390 | Nút X có y=-75,73…-39,73, ngoài màn hình; click thật timeout. Phải dùng Escape để tiếp tục test. |
| T06 | Bấm J khi panel đang mở | `uiPause=true` nhưng cooldown từ 0→0,5917 và projectile 0→1. |
| T07 | Cast ultimate rồi mở panel | Sau 300ms thực, HP mục tiêu 100000→98985 trong khi vẫn pause. |
| T08 | Công thức/collision/animation | Công thức và mana shield sai như mục 5. World clamp và qua cầu có phản hồi; test sông dừng tại x=742 đúng mép, chưa đủ để xác nhận chống xuyên ở mọi dt/tốc độ. |
| T09 | Reload | Nhân vật `PersistProbe`, vàng 4321 và quality low trở về fresh: roster 0, vàng 60, quality high. |
| T10 | Joystick khi tự xoay dọc | Kéo màn hình xuống 35px cho input local `jx=0,7, jy=0`, đúng phép quay; 5 HUD icon 44×44 không chồng trong snapshot đó. Dùng mouse pointer trong context hasTouch, **chưa phải multi-touch thật**. |
| T11 | Bảng CONFIG | 3 phái, skill mở Lv1/8/15/25, 4 support/phái, 7 map, 4 ô trang bị, ngọc 7 cấp và caps tồn tại. Không suy ra đã hoàn thành 7 map/10 ô từ việc có DATA. |
| T12 | AUTO seeded | 4 seed/phái = **12/12** qua stage1, Lv1 khởi đầu không gear; mage seeds 101–130 = **28/30**; boss swordsman Lv10, stage5, không gear/không cộng điểm, seeds 201–204 = **4/4**. Không phải test cân bằng đường farm đến boss. |
| T13 | Frame probe desktop | 180 frame/high: mean **14,69ms**, p95 **15,30ms**; 180/low: mean **14,71ms**, p95 **15,20ms**; không có frame >33,34ms trong cửa sổ ngắn này. Không chứng minh low tối ưu hoặc iPhone mượt. |
| T14 | Production capture | Boot bản bundle capture không có JS exception; ảnh `production-captured-create.png`. |

Hai seed mage bị timeout đã được tái hiện **trong trang mới**:

- Seed **109**: 7/8 kills sau 600 giây, hero (519,68;812,06), slime còn 30 HP tại (641,82;1003,80), distance 227,33, blocked=true.
- Seed **130**: 7/8 kills sau 600 giây, hero (396,64;599,80), goblinArcher còn 36 HP tại (461,73;817,92), distance 227,62.
- Đây là lỗi tiến triển AUTO có repro. Chưa khẳng định một nguyên nhân duy nhất; cần phân tích vật cản/đường đạn/đích và state stuck trước khi sửa. Ảnh: `reviews/v0.3.7/evidence/stall-seed-109.png`, `reviews/v0.3.7/evidence/stall-seed-130.png`.

Chưa kiểm chứng end-to-end: toàn bộ nâng cấp/thất bại/khảm/tháo/ghép, guaranteed boss drop theo mọi map, all boss skills/phases, HP0/revive chuẩn, shop/NPC/quest, long soak, luân phiên nhiều tab, account sync và điện thoại thật. Không tick các mục này là hoàn thành.

## 5. Lỗi có thể hành động, chưa sửa

| Mức | Lỗi, trigger và bằng chứng | Vị trí source baseline / hướng sửa PROPOSED |
|---|---|---|
| P1 | Reload mất toàn bộ tiến trình và cài đặt, T09. | Save/Roster `index.html:1094–1122`; thêm storage adapter + schema/migration/backup. |
| P1 | AUTO mage có seed không hoàn thành màn, T12 + repro cô lập 109/130. | `Combat.control` khoảng 3388–3470; `steerVelocity` 2832; collision 1571. Thêm regression trước khi điều chỉnh pathfinding/line-of-sight. |
| P1 | Bản đồ lớn không pause và X bị khuất ở 844×390, T05/T05b. | Listener `index.html:4300`, CSS big-map overlay; đưa map vào manager chung, giới hạn chiều cao/scroll header. |
| P1 | Ultimate dùng wall-clock timer gây damage trong lúc pause, T07. | `Skills.cast` khoảng 3539: `setTimeout(...,200)`. Đưa vào queue theo game time; kiểm điều kiện combat ở thời điểm apply. |
| P2 | Keyboard J/Space/Digit vẫn điều khiển combat khi pause/overlay/focus input, T06. | keydown 4340+, `Combat.basicAttack` 3344, `Skills.cast` 3481: guard dùng chung thay vì chỉ che nút. |
| P2 | Công thức % áp lên cả phần cộng thẳng: fixture base35, flat100, +30% cho **175,5**, công thức SPEC cho **145,5**. | `heroStats` khoảng 1413: `(baseAtk+flatAtk)*(1+pct)`. Chủ dự án phải xác nhận cách hiểu nguồn flat trước khi sửa balance; không âm thầm đổi combat. |
| P2 | Mana shield tăng mana khi damage sau DEF âm. Mage Lv10, 45 điểm DEF, DEF63,1, raw10: mana50→**57,1175**, vẫn nhận1HP, T08. | `heroTakeDamage` 2757+, cost tính trước clamp damage. Clamp đầu vào hấp thụ/cost, test damage<=DEF. |
| P2 | Helper portrait chạm phần tử chưa tồn tại, placeholder ảnh request sai; repo không đạt 0 console. | `index.html:554:119`; chuyển binding ảnh sang đúng lúc DOM sẵn sàng, thay placeholder có kiểm chứng. |
| P2 | Payload production nặng và không cache; 10,16MB dù source ba file 4,74MB. | `cloudflare/worker.js` no-store, ảnh inline lặp. Chỉ sửa đóng gói/hosting sau phê duyệt riêng, không deploy trong review. |
| P2 | Tài liệu/harness/asset references thiếu, tiến độ và hướng art mâu thuẫn. | docs/README/PROJECT_HANDOVER. Thu hồi đúng Concept/ZIP/harness, tạo manifest nguồn chuẩn. |

Lưu ý thêm cần xác minh: `updateProjectiles` gọi `Combat.dealDamage(..., true, ...)` cho cả projectile basic, khác melee basic `false`; có thể áp buff/skill-level lên basic ranged. Đây là **nghi vấn từ source**, chưa làm fixture riêng nên chưa đưa thành lỗi đã tái hiện. Các số scale HP/ATK quái, potion40%, spawn interval, safe-zone… còn nằm trong engine, chưa tuân thủ hoàn toàn nguyên tắc mọi số balance ở DATA.

## 6. Kiến trúc hiện tại và GAME-CORE dùng chung — PROPOSED

`CONFIG` tập trung phần lớn DATA; `Save/Roster` là state; `Items/Gems`, `Collision`, `Combat`, `Skills`, `Sprites`, `Minimap`, `UI`, `PanelManager`, `AudioFX` đã có ranh giới tên. Điểm yếu là dependency vòng qua globals và trộn render/DOM/audio với tính toán. `startStage()` vừa world/state vừa UI/persist; `update()` vừa combat vừa minimap/DOM; `heroStats()` đọc P, Items và buff global. Không cần viết lại engine để cải thiện.

GAME-CORE là **một implementation chung trong chính repo**, Codex và Claude Code cùng đọc cùng dùng, không hai bản engine, không service sinh ảnh nằm trong runtime game:

```text
game-core/
  data/          classes, skills, monsters, bosses, maps, drops, balance
  state/         character schema, roster, runtime world
  systems/       stats, combat, skills, collision, AI, loot, progression
  adapters/      clock, rng, storage, audio/effects event sinks
render/          Canvas 2D, sprites, camera, minimap
ui/              gate, input, HUD, panels, inventory/settings
art-pipeline/    công cụ phát triển local, không ship vào game
```

Contract dự kiến: core nhận `state + input + dt + rng`, phát sự kiện damage/loot/level/stage; renderer/UI đọc snapshot và gửi command; storage serialize character/settings riêng với runtime scene. RNG/clock phải inject để các test có cùng seed/time. `ItemId`, `CharacterId`, `SkillId` ổn định, không dùng index UI làm định danh lâu dài. Đây là ranh giới đích, chưa phải lời hứa có thể chuyển một lượt không rủi ro.

Để tiết kiệm token: thêm bản đồ module ngắn (owner, public API, dependencies, test tương ứng); task card ghi SPEC mục nào, file nào được sửa, acceptance; không đưa base64 assets vào context hằng ngày. Hai công cụ dùng cùng fixtures/harness và commit baseline. Với công việc đồng thời sau này, dùng worktree/nhánh riêng, một người/chức năng sở hữu một tập file; không sửa đồng thời cùng index.html.

## 7. Tách index.html nhưng bảo toàn hành vi — PROPOSED

1. **Đóng băng baseline và test trước:** SHA/hash file, snapshot UI và state traces; bổ sung tests seed109/130, pause, mana, formula. Ghi rõ known failures, không biến refactor thành thay balance.
2. **Tách cơ học CSS/JS:** giữ vanilla JS, thứ tự các classic script và lexical bindings như hiện tại; HTML giữ shell/markup; đưa nguyên từng khối sang file, chỉ gọi init sau khi đủ dependencies. Chưa đổi ESM/namespace/IIFE một lượt vì sẽ đổi scope và có thể phá file://.
3. **Tháo phụ thuộc theo từng module nhỏ:** data → serialization/state → math/stats → collision → loot → combat/skills/AI; đưa UI/audio thành adapters. Mỗi bước chỉ một ranh giới, có diff kiểm tra behavior trace.
4. **Tách UI/render/input:** registry PanelManager bao phủ map/settings/roster/item; chuỗi open/switch/close và pause có một chủ sở hữu. Các sửa bug baseline phải là thay đổi riêng đã duyệt, không trộn trong commit tách file.
5. **Chốt format module:** giữ classic JS namespace nếu muốn tiếp tục file://; chỉ cân nhắc ES modules sau khi đường chạy HTTP local ổn và chủ dự án duyệt bỏ/đổi file://. Không cần Phaser/TS/Vite cho kế hoạch này.

Tiêu chí bảo toàn: cùng CONFIG, RNG seed, dt và input stream → cùng state traces (HP/MP, kills, drops, inventory, XP, cooldown, stage), cùng asset/frame/panel/layout trong dung sai render đã duyệt. Phần bọc/binding thay đổi phải có test boot/resource, không chỉ node --check. Không cố giữ bug sau khi có quyết định sửa riêng; test golden được cập nhật kèm lý do và phê duyệt.

## 8. Lưu nhân vật bền vững — PROPOSED triển khai theo hướng IndexedDB đã có trong SPEC

Lưu local không đòi server. Đề xuất IndexedDB với stores `characters`, `roster`, `settings`, `backups`; metadata `schemaVersion`, `characterId`, `revision`, `updatedAt`. Snapshot character gồm toàn bộ P: name/class/gender, level/exp, allocation/points, skills/support, gold, inventory/equipped/gems/potions, stage/maxStage, first-kill flags và totals. Không lưu DOM/canvas/AudioContext/monster references hoặc circular runtime state.

- Giữ Save.persist là entry point; serialize immutable snapshot, xếp hàng ghi tuần tự/debounce, transaction ghi character + roster + revision nguyên tử. Lưu ở level-up, nhặt/đổi/nâng/khảm đồ, đổi map, đổi settings; không đợi duy nhất khi đóng tab.
- Migration có fixtures từ version trước, backup trước đổi schema, đọc kiểm lại, chỉ bỏ bản cũ sau transaction thành công. Dữ liệu lỗi/quota/private mode hiển thị trạng thái không lưu được, không tự fresh ghi đè save cũ.
- Export/import JSON có validation và checksum để backup ngoài browser. Checksum phát hiện hỏng dữ liệu, không phải chống gian lận. Có timestamp/revision cho từng nhân vật.
- Multi-tab dùng một writer (Web Locks nếu có) và BroadcastChannel/thông báo conflict; revision check trong transaction, không last-write-wins âm thầm.
- Có thể xin persistent storage nếu browser hỗ trợ nhưng vẫn cần backup: quyền persist không đồng nghĩa chống xóa dữ liệu hoặc bảo đảm trong private mode. IndexedDB, local và production có origin khác, cần export/import để di chuyển save.
- Cloud sync là bước riêng sau này: auth và API, transaction/revision/conflict policy. Worker KV hiện phục vụ file, **chưa có API save**; KV eventual consistency không nên được giả định là transaction/CAS mạnh cho save nhiều thiết bị. Cân nhắc D1/Durable Objects cho writer nếu được duyệt; không đổi stack hiện tại trong review.

Nghiệm thu: 3 nhân vật độc lập; reload/browser restart giữ tiến trình và settings; xóa xác nhận 2 bước; migration từ N−1/N−2; dữ liệu hỏng/quota/ghi lỗi không mất save tốt; multi-tab không ghi đè; backup import/export tương đương; offline write/reconnect rõ ràng. Phải test trên Safari/iPhone thật.

## 9. Đồ họa, animation, tải và FPS điện thoại — PROPOSED

Đồ họa thực tế có 6 bộ chibi; quái/maps còn vẽ code. `animFrame()` dùng idle0/1, run `[2,0,3,0]`, attack4/5, cast5, dead0 + transform; chưa có animation riêng đủ 4 skill/trúng đòn/chết/hồi sinh và 8 hướng như mục tiêu. Không coi scale/rotate ảnh là hoàn thành bộ animation SPEC. Thiếu Concept gốc nên chưa xác nhận được độ khớp art direction với ảnh tham chiếu.

Chỉ số tải/memory từ file và source (không phải peak RAM đo trên iPhone):

- Ba file game repo tổng **4.736.647 bytes**; production HTML **10.164.614 bytes** (khoảng 2,15 lần).
- Ước lượng nén zlib mức9: khoảng 3,41MB cho ba file và 7,49MB cho bundle; **không phải byte tải mạng đã đo**.
- 19 ảnh nếu giải mã RGBA lý thuyết: **63.658.240 bytes ≈60,71MiB**.
- `loadHeroArt()` tạo thêm **2 tint canvas cho mỗi hero và mỗi strip** cho cả 6 biến thể: xấp xỉ **73,37MiB** backing pixels nữa. Tổng hai nhóm khoảng **134,08MiB**, chưa canvas game, strings base64, ảnh decode/cache trùng hay GPU copies. Đây là ước tính theo kích thước, không phải RSS browser.
- DPR bị cap2, quái hoạt động cap5, particle có cap theo quality, minimap ~7Hz và AI xa bớt nhịp: đã có cơ chế tiết kiệm, nên giữ và đo trước khi thay.

Ưu tiên: xuất ảnh thành WebP/PNG alpha file rời theo manifest literal + content hash, cache immutable; HTML versioned/no-cache phù hợp thay vì nhét ảnh lặp/no-store cả gói. Intro kích thước theo màn hình; preload tối thiểu intro/nhân vật chọn/map hiện tại, tải phần còn lại khi cần. Chỉ tạo tint cho bộ đang dùng, lazy cache có giới hạn; không làm đủ tint cho 6 bộ ngay boot.

Đo profiler trước tối ưu: thời gian update/render, long tasks, heap/canvas allocations, số image decode và upload, FPS/điện năng trên máy mục tiêu. Cache terrain tĩnh/offscreen, cull đối tượng ngoài camera, dirty-update HUD, tránh tạo `[...monsters]`/sort mới trong mọi hot path nếu profiler xác nhận đáng kể. Điều chỉnh DPR/particle/shadow bằng quality có cấu hình, không giảm damage/update rate khiến đổi gameplay.

Tiêu chí đề xuất chờ duyệt: frame p95≤33,3ms trên mẫu iPhone/Android chỉ định (mục tiêu tốt 16,7ms); ít nhất20 phút AUTO/chuyển map không tăng memory không giới hạn; load cold/warm với profile mạng rõ, mục tiêu payload theo bản art đã chốt; nhìn rõ HUD ≥44px vùng chạm, safe-area cả hai chiều. Không chốt SLA dựa vào desktop headless 180 frame.

## 10. ComfyUI và pipeline art

ComfyUI chạy riêng tại `C:\AI\ComfyUI-Local`, API bind `127.0.0.1:8188`, SDXL GPU RTX2070 Super/CUDA. Đã kiểm GET system_stats/queue và history của **hai request thật vòng 2**, cả hai `success`, queue trống. Các vòng art tiếp theo không được coi là thay source game.

Luồng dùng chung Codex/Claude Code: CLI Python local → POST /prompt → poll history → GET /view → raw PNG + recipe/seed/hash → segmentation/crop/QA → manifest asset đã nghiệm thu. Game production không gọi thẳng localhost ComfyUI: điện thoại localhost là chính điện thoại, không phải PC; tránh public API, wildcard CORS và API key trong frontend.

Vòng magenta cho thấy model không tuân nền phẳng và màu nền lẫn vào giáp; chroma key có thể xóa chi tiết. Hai ảnh vòng 2 đã lưu đúng prompt nhưng vẫn sai nền/bố cục, ghi trong INFO. Chủ dự án sau đó duyệt **rembg/BiRefNet** và hai ảnh nền trắng: đã hoàn thành rembg **2.0.88**, ONNX Runtime **1.32.0**, **birefnet-general 972.666.916 bytes**, CPUExecutionProvider 6 threads. Bốn lượt tách lần lượt **36,393 / 39,192 / 37,028 / 37,551 giây**, nạp session6,263 giây (chưa tính import/download). 86 phiên bản package cũ giữ nguyên, PyTorch CUDA matrix test vẫn PASS. Hai ảnh trắng mới seed812001/812002 sinh trong15,115/15,233 giây. Kết quả/hashes/recipes/QA ở `art-tests/comfyui-round2/INFO.md`; preview local `ảnh raw/cut đã công bố tại [art-tests/comfyui-round2](art-tests/comfyui-round2/)`. Cut sạch nền hơn key, nhưng nguồn kiếm mới vẫn có khung ngoài ý muốn và source pink không được tự recolor. Đây là thử nghiệm để Luna nghiệm thu mép, chưa tự chốt pipeline hay sản xuất hàng loạt quái Rừng Xanh.

Định danh file pipeline hiện tại dài (`kind_name_sdxl_seed_timestamp`); handover yêu cầu tên logic `hero_<phai>_<gioi>`, `monster_<ten>`, `icon_<ten>`. Nên giữ tên/hash raw để truy xuất, chỉ tạo manifest/export alias logic sau nghiệm thu. Seed giống nhau không đảm bảo identity nhân vật qua nhiều pose; cần QA nhất quán theo model/workflow/reference trước khi duyệt mở rộng khác. Không tự cài LoRA/ControlNet/plugin.

## 11. Playwright và công cụ cần thiết

Playwright phù hợp kiểm boot/resources/console, 6 biến thể, panel/input/rotation, save/reload, state traces và chụp ảnh. Đã dùng thật, có screenshot/trace và phát hiện click ngoài viewport. Không phải chỉ đề xuất trên giấy.

- Bộ nguồn đã cài riêng ở `fantasy-rpg-review/tools/package`, metadata và integrity npm ở `reviews/v0.3.7/evidence/playwright-package.json`. Không thêm package.json/build step cho game.
- Snapshot tương lai phải cố định browser/OS/font/viewport/DPR, seed/RNG, clock, camera và trạng thái animation. Chụp raw screenshot không đủ thành visual regression; cần baseline được chủ dự án duyệt và threshold + mask vùng động rõ ràng.
- `toHaveScreenshot()` của Playwright Test có thể áp dụng khi thêm test runner được duyệt. Với Canvas, thêm state assertions để biết ảnh đúng nhưng gameplay sai; giữ trace khi fail. Emulation không thay thế Safari/iPhone thật.
- Công cụ đủ cho vòng kế tiếp: Git, Node, Playwright/Chrome; Python/Pillow/NumPy/SciPy và ComfyUI/rembg cho art local; Chrome DevTools cho perf. Thêm WebKit/Safari device testing và test IndexedDB khi làm storage. Chưa cần Phaser, TS, Vite, browser mới hay CI deploy credentials.

## 12. Kế hoạch phát triển theo SPEC và tiêu chí duyệt

| Ưu tiên | Gói công việc PROPOSED | Tiêu chí nghiệm thu trước bước sau |
|---|---|---|
| 0 | Thu đủ Concept/ZIP/harness, chốt thứ tự tài liệu và baseline | Có inventory file/hash, decision log, owner xác nhận known failures/thiếu evidence. |
| 1 | Vá boot asset/helper + pause manager/map/input/timer | 0 app exception/missing asset; map/panel giữ đúng AUTO và input; không damage/skill trong pause; X luôn thấy trên 844×390/667×375 và portrait-rotated. |
| 2 | Vá AUTO seed109/130 và xác minh công thức/mana/projectile | 46/46 fixture hoặc ngưỡng được duyệt; seed regression không timeout; formulas/caps/cooldown đúng quyết định balance; không đổi gameplay âm thầm. |
| 3 | IndexedDB local + backup/migration | Toàn bộ acceptance mục8, 3 slot, reload/restart thật; không còn mất save sau update. |
| 4 | Tách cơ học module và contracts GAME-CORE | Trace/golden của bản đã vá không đổi; script/resource checks pass; từng module sửa được và test độc lập. |
| 5 | Chốt art Rừng Xanh, 1 hero mẫu + quái/boss | Người dùng duyệt style/alpha/animation; đủ trạng thái cần thiết, không tự đưa ảnh thử vào game. |
| 6 | Asset caching/lazy decode, profiling mobile | Đạt budget đã duyệt trên thiết bị và mạng thật, soak ≥20 phút, không tăng memory vô hạn. |
| 7 | Nhân rộng nội dung | Map/boss/quest/city/NPC/10 slot theo SPEC/GDD sau khi gói1–6 đạt, từng vertical slice có test và owner duyệt. |
| Sau | Account/cloud sync/PWA và hosting | Kế hoạch auth/migration/conflict/rollback, preview và kiểm thử trước một lần phê duyệt deploy riêng. |

Mỗi gói là một thay đổi nhỏ, có file scope, checklists, known failures và rollback; update CHANGELOG/PROGRESS chỉ khi thực sự triển khai và test. **Chờ chủ dự án duyệt gói cụ thể trước khi sửa source.**

## 13. Nguồn kỹ thuật chính thức

- [Playwright visual comparisons](https://playwright.dev/docs/test-snapshots): baseline ảnh và môi trường render.
- [Playwright emulation](https://playwright.dev/docs/emulation) và [Trace Viewer](https://playwright.dev/docs/trace-viewer): cấu hình browser test và bằng chứng lỗi.
- [IndexedDB](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API), [persistent storage](https://developer.mozilla.org/en-US/docs/Web/API/StorageManager/persist): cơ sở lưu local và giới hạn persistence.
- [Cloudflare KV consistency](https://developers.cloudflare.com/kv/concepts/how-kv-works/): không coi KV là transaction store mạnh.
- [Canvas optimization](https://developer.mozilla.org/en-US/docs/Web/API/Canvas_API/Tutorial/Optimizing_canvas): cache/offscreen và tránh vẽ lại không cần thiết, áp dụng khi profiler xác nhận.
- [ComfyUI routes](https://docs.comfy.org/development/comfyui-server/comms_routes): submit/queue/history/view cho workflow local.

Các đề xuất kiến trúc/budget ở trên là suy luận thiết kế từ source và kết quả kiểm thử, **không phải thay đổi đã triển khai hoặc bảo đảm hiệu năng chưa đo**.
