# PROMPT_LIBRARY: Fantasy: Huyền Thoại Lục Địa

Trạng thái: **PROPOSED v0.1**. Chưa chạy thử, sẽ hiệu chỉnh theo kết quả đợt mẫu (bước B). Bản máy đọc được (JSON) sẽ nằm ở `skills/fantasy-prompt-library/` sau khi được duyệt.

**ĐÃ DUYỆT 2026-11-28** (căn cứ SPEC mục 1b + ART_DIRECTION.md, commit 243c0fa): quái/boss chibi-fantasy đồng bộ hero; sprite mẫu 4 hướng (vẽ xuống/lên, lật ngang ra trái/phải). Quái Rừng Xanh lấy nguyên văn từ `docs/MONSTER_DESIGN_RUNG_XANH.md` (bản chuẩn của dự án).

## 0. Luật chung (áp dụng cho mọi prompt)
1. **Không bao giờ ghi màu sặc sỡ cho nền** (magenta, green screen…) của chủ thể cần tách. Mặc định dùng `simple background, plain white background` cho khớp MONSTER_DESIGN. **PROPOSED:** với chủ thể có mảng trắng (bờm Sói Rừng, Yêu Tuyết, Xương Khô, highlight của slime) thì dùng `plain light grey background`, để bước tách nền không ăn mất phần trắng.
2. Mỗi prompt gồm: `[CHẤT LƯỢNG] + [PHONG CÁCH NHÀ] + [NHẬN DIỆN] + [DÁNG / HÀNH ĐỘNG] + [KHUNG HÌNH]`. Phần NHẬN DIỆN giữ **nguyên văn** giữa các lần sinh.
3. Mỗi lượt chỉ một chủ thể; ghi rõ `solo, full body, entire character visible`.
4. Không có chữ, logo hay watermark. Chữ trong UI do engine vẽ.
5. Cố định seed cho mỗi nhân vật (ghi trong bảng NHẬN DIỆN); chỉ đổi seed khi muốn tìm biến thể.
6. Model mặc định: Animagine XL 4.0 cho nhân vật, quái và icon (dùng tag kiểu danbooru); SDXL Base cho map (câu tự nhiên).

## 1. Khối dùng chung

**Q (chất lượng, Animagine):** `masterpiece, high score, great score, absurdres`

**STYLE_CHIBI (phong cách nhà):** `chibi, super deformed, 2.5 heads tall, cute fantasy rpg game character, clean bold outline, dark brown lineart, cel shading with soft gradients, vibrant saturated colors, glossy highlights, mobile game art, top-left lighting`

**STYLE_MONSTER:** `chibi fantasy monster, cute but menacing, game enemy sprite, clean bold outline, dark brown lineart, cel shading, readable silhouette, mobile rpg game art`

**FRAME_SPRITE:** `solo, full body, entire character visible, feet visible, centered, three-quarter view from above, simple background, plain white background` (đổi `white` thành `light grey` theo luật 0.1)

**DIR (4 hướng, ĐÃ DUYỆT 2026-11-28, căn cứ SPEC mục 1b + ART_DIRECTION.md, commit 243c0fa):** `DOWN` = `facing viewer, three-quarter front view from above` · `UP` = `facing away from viewer, three-quarter back view from above`. Trái/phải không sinh riêng: lật ngang bằng engine hoặc script.

**NEG_BASE:** `lowres, bad anatomy, bad hands, extra digits, fewer digits, missing fingers, extra limbs, cropped, out of frame, worst quality, low quality, low score, bad score, average score, blurry, jpeg artifacts, text, signature, watermark, username, logo, multiple views, duplicate, 2girls, 2boys, colored background, gradient background, pink background, purple background, scenery, realistic, photorealistic, 3d render`

**NEG_SHEET** (thêm khi sinh dải khung): `overlapping characters, inconsistent size, different outfits`

## 2. NHẬN DIỆN 6 nhân vật (khóa theo chân dung k0, k8–k12)

| Mã | Khối NHẬN DIỆN (nguyên văn) | Palette chính | Seed |
|---|---|---|---|
| `SW_M` | `1boy, swordsman, short spiky silver-blue hair, big blue eyes, steel knight helmet with open visor and red plume, polished silver plate armor with gold trim, red cape, large steel greatsword with gold cross-guard` | bạc #C9CED6 · đỏ #B8322C · vàng #D9A441 | 410101 |
| `SW_F` | `1girl, swordswoman, long brown hair in high ponytail, gold circlet, big amber eyes, silver plate armor with gold trim, red cape, steel longsword with ornate guard` | bạc · nâu #7A4A2A · đỏ | 410102 |
| `MG_M` | `1boy, young wizard, dark navy hair, big blue eyes, small white goatee, tall navy wizard hat with gold moon and star embroidery, navy robe with gold trim, wooden staff with glowing blue orb` | navy #1F2D5C · vàng · lam #4FB3FF | 410201 |
| `MG_F` | `1girl, sorceress, very long wavy lavender hair, big violet eyes, crystal hair ornament, teal and violet layered robe with silver trim, wooden staff topped with large purple crystal` | lavender #B79AE0 · teal #2F7E8C · tím #7B4FD0 | 410202 |
| `AR_M` | `1boy, ranger archer, messy brown hair, big green eyes, green hooded cloak, brown leather armor with belts, quiver of arrows on back, wooden longbow` | lục #3E7A3A · nâu da #6B4528 | 410301 |
| `AR_F` | `1girl, ranger archer, auburn hair in long side braid, big brown eyes, green hooded cloak, brown leather armor, quiver on back, wooden longbow` | lục · nâu đỏ #9A4A24 | 410302 |

Lưu ý MG_F: tóc và áo tím gần màu nền cũ, nên **bắt buộc dùng nền xám** và bước khử màu theo toán học.

## 3. Dáng và hành động (ghép sau NHẬN DIỆN, đi kèm xương OpenPose)

| Mã | Prompt dáng |
|---|---|
| `IDLE` | `standing relaxed, weapon held at side, slight smile` + DIR |
| `RUN_KEY` | `running, mid stride, leaning forward, cape flowing back` + DIR |
| `ATK_SW` | `dynamic horizontal sword slash, sword swung across body, motion, determined expression` |
| `ATK_MG` | `casting spell, staff raised forward, orb glowing, magic circle at feet` |
| `ATK_AR` | `drawing bow, arrow nocked, aiming forward, focused expression` |
| `HURT` | `recoiling from hit, leaning back, eyes squeezed shut` |
| `DEATH` | `collapsed lying on ground, eyes closed, weapon dropped beside` |
| `TURN` | `character turnaround sheet, front view, three-quarter view, side view, back view, same character, consistent outfit` (+ `multiple views` **xóa khỏi** NEG) |

Skill (tạo dáng và VFX riêng; VFX sinh trên nền đen để cộng màu):
- Kiếm Sĩ: Trảm Kiếm `overhead downward slash` · Kiếm Vũ `spinning sword attack, whirlwind of golden slashes` · Địa Chấn `sword plunged into ground, shockwave cracks` · Thiên Kiếm `giant spectral golden sword descending from sky`.
- Pháp Sư: Hỏa Cầu `launching fireball` · Băng Phong `ice storm vortex` · Lôi Đình `chain lightning from staff` · Thiên Thạch `summoning meteor shower`.
- Cung Thủ: Xuyên Tiễn `piercing glowing arrow` · Liên Tiễn `rapid multi-shot fan of arrows` · Độc Tiễn `green poison arrow` · Vạn Tiễn `rain of arrows from sky`.

## 4. Quái (STYLE_MONSTER + FRAME_SPRITE)

| Map | Mã | Prompt nhận diện |
|---|---|---|
| Rừng Xanh (nguyên văn MONSTER_DESIGN) | slime | `cute chibi emerald-green slime monster, round translucent jelly dome body, glossy white highlight on top, big round black eyes, small happy smile, tiny leaf sprout on its head, no arms, no legs` |
| | goblin | `mischievous chibi goblin warrior, dark green skin, big head, long pointy ears, small fang grin, torn brown leather armor, orange neck scarf, holding a spiked wooden club, short legs, brown boots` |
| | goblinArcher | `chibi goblin archer, green skin, long pointy ears, brown hood, moss-green cloak, holding a short wooden bow, quiver of arrows on its back, one eye squinting aiming` |
| | wolf | `fierce chibi forest wolf, slim body, blue-grey fur, fluffy white neck mane and tail, pointy ears, sharp yellow eyes, visible claws, ready-to-pounce stance` |
| | goblinShaman (**chưa có trong MONSTER_DESIGN, PROPOSED**) | `chibi goblin shaman, dark green skin, long pointy ears, bone mask, feather headdress, orange neck scarf, staff with green glowing skull` |
| Hang Tối | bat / spider / skeleton | `purple demon bat, wide leathery wings` · `giant venomous spider, purple and black, glowing green markings` · `skeleton warrior, rusty sword and broken shield` |
| Đầm Lầy | toad / lizard | `poison toad, warty green-purple skin, toxic drool` · `swamp lizardman, mossy scales, spear` |
| Sa Mạc | scorpion / mummy / vulture | `giant sand scorpion, amber carapace` · `bandaged mummy, glowing eyes, slow heavy` · `desert vulture, ragged wings` |
| Núi Lửa | imp / fireWolf / magmaGolem | `fire imp, horns, flame tail` · `wolf made of fire, ember mane` · `huge magma golem, cracked rock body, lava glowing through cracks` |
| Băng Nguyên | iceWolf / yeti / iceWitch | `frost wolf, icy blue fur, ice crystals` · `big white yeti, frosty fur` · `ice witch, pale blue robes, ice staff` |
| Lâu Đài | darkKnight / vampire / cultist / wraith | `dark knight, black spiked armor, red glowing visor` · `vampire noble, red cape, pale skin` · `hooded cultist, red robe, dark tome` · `ghostly wraith, tattered translucent cloak, floating` |

Tinh anh: **không cần prompt riêng** (code phóng to + viền đỏ).

## 5. Boss (STYLE_MONSTER + `boss, large imposing, detailed, dramatic pose` + FRAME_SPRITE)
Chibi-fantasy nhưng to và dữ hơn hẳn quái thường: rune, sẹo, mắt phát sáng (**ĐÃ DUYỆT 2026-11-28**, căn cứ SPEC mục 1b + ART_DIRECTION.md, commit 243c0fa).
- Chúa Sói (nguyên văn MONSTER_DESIGN): `giant chibi alpha wolf boss, much bigger and more majestic than a normal wolf, dark charcoal-grey fur, long mane, glowing green rune markings on shoulder and hip, scar across left eye, glowing green eyes, bared fangs, menacing` · phase 2 (PROPOSED): `+ runes and eyes glowing brighter, green spirit aura`
Các boss sau đều là PROPOSED. Khi viết thiết kế chi tiết, đi theo khuôn MONSTER_DESIGN: dáng + màu + dấu hiệu riêng + tính cách, rồi mới viết prompt; nhớ thêm `chibi` vào đầu prompt.
- Nhện Chúa: `colossal spider queen, purple carapace, crown-like horns, venom dripping fangs`
- Đầm Chúa: `swamp lord, giant mossy toad-ogre, toxic bubbles, rotting crown`
- Pharaoh Cổ Đại: `ancient undead pharaoh, gold mask, sand-swirling staff, bandaged body`
- Rồng Lửa: `young fire dragon, red scales, molten belly glow, wings spread`
- Golem Băng: `ice golem titan, crystal armor plates, frozen core glowing blue`
- Chúa Quỷ Bóng Đêm: `demon lord, black armor, curved horns, dark greatsword, purple-black flames`

## 6. Map (SDXL Base, câu tự nhiên)

**Tile đất Rừng Xanh:**
`seamless tileable top-down game texture, lush forest grass ground with small clover patches and tiny flowers, soft hand painted style, even lighting, no shadows from objects, no objects, high detail` · NEG: `objects, trees, characters, perspective, horizon, text, seams, vignette`

**Vật thể map** (sinh từng món trên nền xám, rồi tách nền):
`single [round leafy oak tree | mossy boulder | ancient stone ruin pillar | wooden bridge segment | small wooden cottage with red roof | glowing teleport portal stone circle], hand painted fantasy rpg game asset, three-quarter top-down view, soft shading, vibrant, simple background, plain light grey background`

**Thumbnail map** (không tách nền): `wide fantasy landscape, [rừng: sunlit green forest with river and wooden bridge | hang: dark cave with glowing purple crystals | đầm: misty poison swamp with dead trees | sa mạc: golden desert with pyramids | núi lửa: volcanic land with lava rivers and stone bridges | băng: snowy mountains with frozen lake and ice temple | lâu đài: gothic castle at night with graveyard], painterly game key art, vibrant, soft light`

## 7. Icon (Animagine + Game icon LoRA, trigger `2d icon` đặt đầu prompt)
`2d icon, single [object], centered, game item icon, fantasy rpg, bold outline, glossy shading, vibrant, simple background, plain light grey background`
- Vũ khí theo bậc: `iron sword` → `ice crystal sword with frost` → `flaming sword with ember glow` → `divine golden holy sword with radiant light`. Tương tự cho trượng và cung.
- Ngọc: `[red|purple|green|yellow|blue] faceted gemstone, inner glow`.
- Bình: `round glass potion flask with [red|blue] liquid, cork stopper`.
- Skill: `2d icon, round skill emblem, [mô tả skill ở mục 3], dramatic, glowing` (khung tròn viền vàng do code vẽ).
- HUD V2 (glyph đơn sắc vàng cổ trên nền trong suốt, có thể vẽ vector thay vì sinh AI): nhân vật (mũ giáp), túi đồ, trang bị (khiên), kỹ năng (tia sét), cài đặt (bánh răng).

## 8. UI
`ornate antique gold metal frame border, fantasy rpg ui panel, dark navy semi-transparent center, engraved filigree corners, gems in corners, flat front view, symmetric, game ui asset, no text` → cắt 9-slice bằng script.
