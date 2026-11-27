# THIẾT KẾ QUÁI — RỪNG XANH (Map 1, Lv1–10)

Bảng thiết kế hình dáng quái dùng cho pipeline ảnh ComfyUI + SDXL.
Lập: 2026-11-28 (Luna soạn, Do duyệt hướng tả rõ từng con).
Quy tắc chung ở `ART_DIRECTION.md` vẫn áp dụng; file này là bản chi tiết cho riêng Rừng Xanh.

## Phong cách chung (áp cho mọi prompt)

- 2D chibi game art, đầu to thân nhỏ, viền đậm rõ, tô màu cel shading, màu tươi.
- Góc nhìn 3/4, toàn thân trọn trong khung, một chủ thể duy nhất, nền trắng trơn.
- Negative chung: "frame, border, emblem, multiple characters, other objects, text,
  watermark, gradient background, shadow, realistic, 3D render".
- Yêu cầu pipeline: SDXL 1024×1024 → rembg birefnet-general → lọc mảnh thừa
  (giữ thành phần liên thông lớn nhất) → khai báo vào manifest ASSETS.

## Vì sao tả kỹ

- Slime và Goblin đều da xanh lá — phải có chi tiết tương phản riêng (lá trên đầu,
  khăn cam, giáp nâu) để trên nền cỏ xanh của Rừng Xanh vẫn đọc rõ từng con.
- Boss phải khác hẳn sói thường ngay từ cái nhìn đầu tiên: to hơn hẳn, rune phát
  sáng, sẹo qua mắt.

## 1. Slime Xanh (quái thường, bầy đàn)

- Dáng: giọt thạch tròn ú, thân hình vòm tròn, không tay không chân.
- Màu: xanh ngọc lục bảo tươi, nửa trong suốt, bóng highlight trắng trên đỉnh đầu.
- Mặt: mắt đen tròn long lanh, miệng cười nhỏ, hai má hồng nhẹ.
- Dấu hiệu riêng: một chiếc lá nhỏ mọc trên đỉnh đầu (dấu hiệu Rừng Xanh).
- Tính cách: ngây thơ, vô hại bề ngoài — quái mồi cho người chơi mới.

Prompt: "cute chibi emerald-green slime monster, round translucent jelly dome body,
glossy white highlight on top, big round black eyes, small happy smile, tiny leaf
sprout on its head, no arms, no legs"

## 2. Goblin (quái cận chiến)

- Dáng: đầu to, tai dài nhọn, chân ngắn đi giày da nâu.
- Màu: da xanh lá đậm; giáp da nâu rách; khăn quàng cổ cam.
- Mặt: tinh nghịch, nhe răng nanh nhỏ.
- Vũ khí: chùy gỗ có đinh.
- Tính cách: láu cá, hung hăng nhưng yếu — quái cận chiến cơ bản.

Prompt: "mischievous chibi goblin warrior, dark green skin, big head, long pointy
ears, small fang grin, torn brown leather armor, orange neck scarf, holding a
spiked wooden club, short legs, brown boots"

## 3. Sói Rừng (quái nhanh, vồ)

- Dáng: thân thon, tư thế sẵn sàng vồ, đuôi bông xù, móng vuốt rõ.
- Màu: lông xám xanh, bờm cổ trắng, mắt vàng sắc, tai dựng.
- Tính cách: hoang dã, nhanh nhẹn — quái tốc độ của map.

Prompt: "fierce chibi forest wolf, slim body, blue-grey fur, fluffy white neck
mane and tail, pointy ears, sharp yellow eyes, visible claws, ready-to-pounce
stance"

## 4. Goblin Cung Thủ (quái đánh xa)

- Dáng: nhỏ hơn Goblin thường một chút; đội mũ trùm nâu; áo choàng xanh rêu.
- Màu: da xanh lá; nâu (mũ, ống tên) + xanh rêu (áo choàng).
- Mặt: một mắt nheo lại ngắm bắn.
- Vũ khí: cung gỗ ngắn, ống tên đeo sau lưng.
- Tính cách: lén lút, giữ khoảng cách — dạy người chơi cách áp sát quái xa.

Prompt: "chibi goblin archer, green skin, long pointy ears, brown hood,
moss-green cloak, holding a short wooden bow, quiver of arrows on its back,
one eye squinting aiming"

## 5. Boss — Chúa Sói (Wolf Lord)

- Dáng: sói khổng lồ — cảm giác to gấp ~3 lần sói thường; bờm dài; uy nghi.
- Màu: lông xám đen; vệt rune xanh lá phát sáng trên vai và hông; mắt xanh lục
  phát sáng; sẹo dài qua mắt trái; răng nanh lộ.
- Tính cách: đáng sợ nhưng vẫn giữ nét chibi (đầu to) cho đồng bộ với game.
- Boss có 3 skill riêng + nổi giận dưới 50% HP (theo SPEC/GDD) — hình dáng phải
  xứng với vai trò đó.

Prompt: "giant chibi alpha wolf boss, much bigger and more majestic than a normal
wolf, dark charcoal-grey fur, long mane, glowing green rune markings on shoulder
and hip, scar across left eye, glowing green eyes, bared fangs, menacing"

## 6. Pháp Sư Goblin (quái phép đánh xa — có trong DATA, bổ sung 2026-11-28)

- Dáng: gầy và cao hơn Goblin thường một chút; đội mũ lông vũ; mặt nạ xương đeo trên trán.
- Màu: da xanh lá đậm; áo choàng tím nâu rách; khăn quàng cổ cam (dấu hiệu chung của họ Goblin).
- Vũ khí: trượng gỗ buộc đầu lâu nhỏ phát sáng xanh lá — nguồn phép của nó.
- Tính cách: ranh mãnh, đứng xa bắn phép — quái phép đầu tiên người chơi gặp.

Prompt: "chibi goblin shaman, dark green skin, long pointy ears, bone mask on
forehead, feather headdress, tattered purple-brown robe, orange neck scarf,
holding a wooden staff topped with a small green glowing skull"

## Quy ước đặt tên file (cho Codex)

- `monster_slime`, `monster_goblin`, `monster_wolf`, `monster_goblin_archer`,
  `monster_goblin_shaman`, `boss_wolf_lord` — mỗi con 2 seed (`_s2` cho seed thứ
  hai), `_raw.png` và `_cut.png`, thư mục `art-tests/monsters-rung-xanh/`, kèm
  `INFO.md`.
- Các map sau làm theo đúng khuôn này: mô tả dáng + màu + dấu hiệu riêng +
  tính cách, rồi mới viết prompt tiếng Anh.
