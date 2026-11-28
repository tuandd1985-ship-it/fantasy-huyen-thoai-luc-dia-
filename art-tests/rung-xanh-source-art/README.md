# Ảnh nguồn Rừng Xanh cho Claude

Bộ mẫu lấy phong cách từ bản game đang chạy và các ảnh nguồn của dự án. Ảnh được tạo bằng ImageGen.

| Tệp | Nội dung |
|---|---|
| `rung-xanh-map-reference.png` | Cảnh tham chiếu 1672×941, RGB. Sông dọc, cầu gỗ ngang, hai bãi cỏ chiến đấu, cây và tàn tích ở rìa. |
| `swordsman-male-key-poses.png` | 1536×1024, RGBA. Hàng trên từ trái sang phải là đứng, Trảm Kiếm, Kiếm Vũ. Hàng dưới là Địa Chấn và Thiên Kiếm, ô cuối trống. |
| `goblin-melee-key-poses.png` | 1254×1254, RGBA. Hàng trên từ trái sang phải là đứng và lấy đà. Hàng dưới là vung chùy và trúng đòn. |

Hai bảng dáng đều có pixel alpha 0. Đây là ảnh nguồn để Claude kiểm tra viền, cắt khung, căn điểm chân và triển khai animation. Chỉ có một góc nhìn ba phần tư. Một số vũ khí đổi hướng qua từng dáng. Hiệu ứng kỹ năng, thời điểm gây sát thương và tốc độ animation do Claude nối theo logic hiện có.

Ảnh map là cảnh tham chiếu bố cục và phối màu, gồm prop đã vẽ chung vào cảnh. Đối chiếu hình học bản game với [map_1 và dữ liệu tách lớp](../maps-anh-do/layers/layers_report.md). Dùng [hợp đồng lớp vẽ](../../docs/art/ENGINE_PROP_LAYER_SPEC.md) khi kiểm tra prop. Đối chiếu dáng Kiếm Sĩ với [AUTO-ANIM-2D hiện có](../auto-anim-2d/REPORT.md).

Nguồn tham chiếu là [scene tile v2b](../rung-xanh-map-sample/tile-v2/scene_test_v2b_1280x720.jpg), [Kiếm Sĩ Nam](../hero-edge-clean/cleaned_png/hero-swordsman-male.png), [Goblin cận chiến](../monsters-rung-xanh/monster_goblin_cut.png) và [hướng art](../../docs/ART_DIRECTION.md).

## Prompt ImageGen

### Rừng Xanh

Use case: stylized-concept. Asset type: polished orthographic 2.5D RPG map gameplay art prototype for Rừng Xanh. Existing game scene is composition and palette reference. A muted olive fairytale forest, hand-painted 2D stylized daylight, overhead 60-degree camera, a narrow near-vertical blue river splits the playfield, a broad straight wooden bridge traverses river from left to right in upper middle, facing east bank. Broad open grassy combat clearing on both banks, readable muted grass with sparse small tufts, oak groups and small ruin fragments placed primarily at perimeter, clear paths to bridge. Match the reference's calm terrain values and low saturation so chibi actors would pop. Full-bleed widescreen 16:9 game camera view, no horizon, no characters, no monsters, no interface/text, no cast shadow vignette. Keep traversable ground visually flat, no jagged rocky elevations. Natural color separations for grass, water and wood.

### Kiếm Sĩ Nam

Use case: stylized-concept. Asset type: full-body key pose sprite source sheet for Fantasy Huyền Thoại Lục Địa. Reference is the original male swordsman already used by this game. Preserve his face, silver-blue hair, silver plate armor, red cape, single silver broadsword, glove and boot design precisely. Create exactly five separate full body sprites evenly spaced across two rows of three, leave bottom-right empty: top-left idle ready stance, top-center Trảm Kiếm strong forward diagonal slash, top-right Kiếm Vũ turning, sword extended horizontally, bottom-left Địa Chấn heavy downward strike with sword reaching ground, bottom-center Thiên Kiếm looking ahead wielding raised sword overhead. A slightly elevated 2.5D three-quarter game camera, same apparent height, same stylized chibi anatomy and clean confident outlines in every cell. Detailed vivid cel shading and faithful colors. Ample true transparent margins around each full body and sword, no pose overlaps, no cast shadows/ground, no motion effect, no labels, no additional objects. Only assembled full-body DRAWINGS as animation pose references for a separate animator. Do not draw exploded body parts or joints.

### Goblin cận chiến

Use case: stylized-concept. Asset type: game-ready reference art sheet of full-body animation key poses for forest goblin melee enemy. Match this game's attached Goblin source: identical head and ears, dark forest-green skin, orange neck scarf, brown torn leather, one spiked wooden club. Same slightly elevated three-quarter 2.5D camera, same detailed cel-shaded chibi design with bold contours. Exactly 4 sprites in a 2x2 equal grid: upper left idle ready, upper right anticipatory club raised behind shoulder, lower left powerful club swing forward, lower right recoil after being struck while still holding club. Same proportions, outfit and weapon in all 4 poses, same feet baseline in each row. Full figures and weapon isolated with wide true-alpha transparent gaps, no hard edge, no effects, no backgrounds, no shadow, no text, no exploded body parts.
