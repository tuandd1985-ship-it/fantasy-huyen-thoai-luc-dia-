"""Render an isolated prop contract scene and record deterministic test results."""
from pathlib import Path
from math import ceil, hypot
import json
import subprocess

from PIL import Image, ImageDraw, ImageFont, ImageStat

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SAMPLE = REPO / 'art-tests/rung-xanh-map-sample'
PROPS = SAMPLE / 'props_clean'
ART = REPO / 'art-tests'
FOOT = 14
FONT = ImageFont.truetype('DejaVuSans.ttf', 16) if (Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf').exists()) else ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 16)
TITLE = ImageFont.truetype(FONT.path, 24)
MASKS = {'oak': (84, 26), 'stone': (150, 42), 'pillar': (76, 28), 'bush': (84, 24)}
LOCATIONS = {'oak': (148, 275), 'pillar': (400, 275), 'portal': (645, 272),
             'stone': (148, 466), 'bush': (400, 466), 'flowers': (630, 459)}
feet = [(567, 272, 28, 22), (723, 272, 28, 22)]
trigger = (645, 312, 150, 48)


def sized(image, height):
    return image.resize((round(image.width * height / image.height), height), Image.Resampling.LANCZOS)


def asset(name):
    with Image.open(PROPS / (name + '.png')) as source:
        return source.convert('RGBA')


sprites = {key: sized(asset(name), height) for key, name, height in (
    ('oak', 'cay_soi', 275), ('pillar', 'cot_da_co', 215), ('stone', 'tang_da_reu', 115),
    ('bush', 'bui_cay', 95), ('flowers', 'khom_hoa', 60))}
with Image.open(ART / 'hero-matte-clean/cleaned/hero-swordsman-male_lossless.webp') as source:
    hero = sized(source.convert('RGBA').crop(source.convert('RGBA').getbbox()), 150)
with Image.open(ART / 'monsters-rung-xanh/monster_wolf_s2_cut.png') as source:
    monster = sized(source.convert('RGBA').crop(source.convert('RGBA').getbbox()), 85)
portal = sized(asset('da_cong_dich_chuyen'), 218)
# Split the composited sample only for this fixture. Final art needs two authored layers.
cut = round(portal.height * 485 / 994)
arch = portal.crop((0, 0, portal.width, cut))
platform = portal.crop((0, cut, portal.width, portal.height))
# The two render entries share the same ground anchor. Their offsets restore registration.
PORTAL_ANCHOR = LOCATIONS['portal']
tile = sized(Image.open(SAMPLE / 'tile_co_rung_xanh_1024.png').convert('RGBA'), 384)


def ellipse(box):
    x, y, w, h = box
    return x - w / 2, y - h / 2, x + w / 2, y + h / 2


def distance(point, box, footprint=0):
    x, y, w, h = box
    return hypot((point[0] - x) / (w / 2 + footprint), (point[1] - y) / (h / 2 + footprint))


def walk(start, velocity, count, bodies):
    x, y = start
    trace = [(x, y)]
    contacts = 0
    dx, dy = velocity
    substeps = max(1, ceil(hypot(dx, dy) / 3))
    for _ in range(count):
        for _ in range(substeps):
            x += dx / substeps
            y += dy / substeps
            for cx, cy, w, h in bodies:
                rx, ry = w / 2 + FOOT, h / 2 + FOOT
                vx, vy = x - cx, y - cy
                length = hypot(vx / rx, vy / ry)
                if length < 1:
                    contacts += 1
                    x, y = (cx + vx / length, cy + vy / length) if length else (cx + rx, cy)
            assert all(distance((x, y), box, FOOT) >= 1 - 1e-8 for box in bodies)
        trace.append((x, y))
    return trace, contacts


def path_result(trace, contacts):
    return {'start': trace[0], 'end': [round(v, 2) for v in trace[-1]],
            'contacts': contacts, 'points': [[round(v, 2) for v in p] for p in trace]}


footprints = {id: (*LOCATIONS[id], *size) for id, size in MASKS.items()}
paths = {}
for name in ('oak', 'stone', 'pillar'):
    x, y, *_ = footprints[name]
    trace, contacts = walk((x - 112, y + 48), (5, -2), 47, [footprints[name]])
    assert contacts and trace[-1][0] > x + 20
    paths[name] = path_result(trace, contacts)

for label, bodies in [('solid', [footprints['bush']]), ('none', [])]:
    x, y = LOCATIONS['bush']
    trace, contacts = walk((x - 112, y + 48), (5, -2), 47, bodies)
    assert (contacts > 0) == (label == 'solid')
    paths['bush_' + label] = path_result(trace, contacts)

path, hits = walk((645, 385), (0, -4), 36, feet)
inside = [distance(p, trigger) <= 1 for p in path]
enters = sum(b and not a for a, b in zip(inside, inside[1:]))
exits = sum(a and not b for a, b in zip(inside, inside[1:]))
assert hits == 0 and enters == exits == 1 and path[-1][1] < PORTAL_ANCHOR[1]
paths['portal_center'] = {**path_result(path, hits), 'trigger_enters': enters, 'trigger_exits': exits}
for label, (x, y, w, h) in zip(('left', 'right'), feet):
    trace, contacts = walk((x, y + 53), (0, -5), 28, feet)
    assert contacts and trace[-1][1] > y
    paths['portal_' + label] = {**path_result(trace, contacts), 'entered_platform_overlap': any(distance(p, trigger) <= 1 for p in trace)}


def paste(canvas, image, x, y, anchor_x=None, anchor_y=None):
    ax = image.width / 2 if anchor_x is None else anchor_x
    ay = image.height - 8 if anchor_y is None else anchor_y
    canvas.alpha_composite(image, (round(x - ax), round(y - ay)))


def ground():
    canvas = Image.new('RGBA', (800, 540))
    for x in range(0, 800, tile.width):
        for y in range(0, 540, tile.height):
            canvas.alpha_composite(tile, (x, y))
    canvas.alpha_composite(Image.new('RGBA', canvas.size, (20, 33, 26, 70)))
    return canvas


def scene(placement, show_debug=False):
    canvas = ground()
    x, y = PORTAL_ANCHOR
    paste(canvas, platform, x, y, anchor_y=0)
    fx, fy = LOCATIONS['flowers']
    paste(canvas, sprites['flowers'], fx, fy)
    draw_entries = [(py, name, sprites[name], px, None) for name, (px, py) in LOCATIONS.items() if name in ('oak', 'pillar', 'stone', 'bush')]
    draw_entries.append((y, 'arch', arch, x, cut))
    for name in ('oak', 'pillar', 'portal'):
        px, py = LOCATIONS[name]
        if placement == 'behind':
            hy, my = py - 27, py - 24
        elif placement == 'front':
            hy, my = py + 54, py + 58
        else:
            hy, my = py + (40 if name == 'portal' else 45), py + 52
        draw_entries.extend([(hy, name + '-hero', hero, px - (0 if name == 'portal' else 15), hero.height),
                             (my, name + '-monster', monster, px + 43, monster.height)])
    draw_entries.sort(key=lambda row: (row[0], row[1]))
    for py, _, image, px, ay in draw_entries:
        paste(canvas, image, px, py, anchor_y=ay)
    order = [entry[1] for entry in draw_entries]
    for prop in ('oak', 'pillar', 'portal'):
        pivot = 'arch' if prop == 'portal' else prop
        for actor in ('hero', 'monster'):
            assert (order.index(prop + '-' + actor) < order.index(pivot)) == (placement == 'behind')
    if show_debug:
        draw = ImageDraw.Draw(canvas)
        for box in [*footprints.values(), *feet]:
            draw.ellipse(ellipse(box), outline='#ff7f79', width=3)
        draw.ellipse(ellipse(trigger), outline='#6df6fc', width=3)
        for key in ('oak', 'pillar', 'stone', 'portal_center', 'portal_left', 'portal_right', 'bush_solid', 'bush_none'):
            draw.line([tuple(p) for p in paths[key]['points']], fill='#6df6fc' if key in ('portal_center', 'bush_none') else '#ffe184', width=3)
        draw.text((13, 503), 'Red = solid footprint  |  Cyan = trigger / walk-through  |  Yellow = collision path', font=FONT, fill='white', stroke_width=2, stroke_fill='#1a2419')
    return canvas, order


sheet = Image.new('RGB', (1600, 1180), '#14211b')
draw = ImageDraw.Draw(sheet)
orders = {}
for label, caption, x, y in [
    ('behind', 'A  Hero + wolf behind oak, column and arch', 0, 0),
    ('front', 'B  Hero + wolf in front', 800, 0),
    ('debug', 'C  Walk and overlap probes, hero on platform', 0, 580)]:
    canvas, orders[label] = scene(label, label == 'debug')
    draw.text((x + 16, y + 8), caption, fill='white', font=TITLE)
    sheet.paste(canvas.convert('RGB'), (x, y + 38))

draw.text((816, 588), 'D  Oak roots: baked only vs. extra code ellipse', fill='white', font=TITLE)
shadow_luma = {}
for i, alpha in enumerate((0, 71)):
    canvas = ground()
    if alpha:
        shade = Image.new('RGBA', canvas.size)
        ImageDraw.Draw(shade).ellipse(ellipse((405, 322, 120, 36)), fill=(0, 0, 0, alpha))
        canvas.alpha_composite(shade)
    paste(canvas, sprites['oak'], 405, 320)
    roi = canvas.convert('L').crop((363, 308, 447, 336))
    shadow_luma['code' if alpha else 'baked_only'] = round(ImageStat.Stat(roi).mean[0], 2)
    crop = canvas.crop((243, 192, 567, 360)).resize((360, 187), Image.Resampling.LANCZOS)
    sheet.paste(crop.convert('RGB'), (821 + 378 * i, 653))
    draw.text((821 + 378 * i, 629), 'Extra ellipse, alpha 0.28' if alpha else 'Sample roots only', font=FONT, fill='white')
draw.text((821, 858), f"Root ROI luma (0-255): {shadow_luma['baked_only']} -> {shadow_luma['code']}", font=FONT, fill='white')
draw.text((821, 907), 'Prototype uses the pinned sample; portal slices are temporary.', font=FONT, fill='white')
draw.text((821, 935), 'Collision paths and trigger counts are recorded in results.json.', font=FONT, fill='white')
draw.text((821, 963), 'Hero height 150 px. Flower decal has no collision.', font=FONT, fill='white')
sheet.save(HERE / 'scene.jpg', quality=92, subsampling=0)

source = (REPO / 'index.html').read_text(encoding='utf-8')
native_collision = source[source.index('const Collision = {'):source.index('</script>', source.index('const Collision = {'))]
js = 'const WORLD={w:1560,h:1180};const waterRects=[];const forestEnv=null;let obstacles=[];\n' + native_collision + '''
const circle = {x:400,y:400,r:42};
obstacles=[circle];
const at = {x:400,y:438,r:14};
const circleBlocks = Collision.resolve(at);
obstacles=[{x:358,y:400,r:14},{x:442,y:400,r:14}];
const walker={x:400,y:460,r:14};
const centerBlocked=[];
for(let i=0;i<24;i++) centerBlocked.push(Collision.move(walker,0,-180,1/30));
if(!circleBlocks || centerBlocked.some(Boolean) || walker.y>=400) process.exit(1);
console.log(JSON.stringify({wideCircleBlocksAtOffsetY38:circleBlocks,expected84x26EllipseWouldBlockAtOffsetY38:false,twoCircleFootCenterPass:walker.y<400,nativeEllipse:false}));
'''
native_draw = source[source.index('function draw() {'):source.index('  /* Bảng tên + thanh máu', source.index('function draw() {'))] + '}'
render_fixture = '''
const renderNative = (() => {
  const drawCalls=[];
  const noOp=()=>{};
  const nativeContext=new Proxy({}, {get(_, key) {
    if(key==='createRadialGradient') return ()=>({addColorStop:noOp});
    return noOp;
  }});
  const ctx=nativeContext, W=800,H=540, cam={x:0,y:0}, shake=0, telegraphs=[];
  const P={created:false}, timeNow=0, drops=[], monsters=[{x:220,y:295}], hero={x:200,y:260};
  const currentMap=()=>({map:{}});
  const Sprites={
    background(){drawCalls.push('background');},
    obstacle(){drawCalls.push('obstacle');},
    hero(){drawCalls.push('hero');},
    monster(){drawCalls.push('monster');},
  };
  obstacles=[{x:200,y:280,r:17}];
  eval(NATIVE_DRAW);
  if(drawCalls.join(',')!=='background,hero,obstacle,monster') process.exit(2);
  return drawCalls;
})();
'''
js = 'const NATIVE_DRAW=' + json.dumps(native_draw + '\ndraw();') + ';\n' + js.replace('console.log(JSON.stringify({','console.log(JSON.stringify({renderNative,')
js = js.replace('const circle =', render_fixture + '\nconst circle =')
native = json.loads(subprocess.check_output(['node', '-e', js], text=True))
head = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=REPO, text=True).strip()
pinned = 'a7ce924'
sample_files = [*PROPS.glob('*.png'), SAMPLE / 'tile_co_rung_xanh_1024.png']
for path in sample_files:
    blob = subprocess.check_output(['git', 'show', f'{pinned}:{path.relative_to(REPO).as_posix()}'], cwd=REPO)
    assert path.read_bytes() == blob, path
record = {'engine_snapshot': head, 'sample_commit': pinned, 'hero_height': hero.height,
          'render_orders': orders, 'native_engine_vm': native, 'paths': paths,
          'flower_has_collider': False, 'footprint_xywh': footprints, 'portal_feet_xywh': feet,
          'portal_trigger_xywh': trigger,
          'portal_group': {'id': 'trial-portal', 'world_anchor': PORTAL_ANCHOR, 'parts': ['ground:platform', 'sorted:arch']}, 'shadow_roi_mean_8bit_luma': shadow_luma,
          'fixture_limit': 'Pillow render and ellipse-expanded footprint prototype. Native Collision block tested separately in Node.'}
(HERE / 'results.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
print(json.dumps({'native': native, 'paths': {k: {a:b for a,b in v.items() if a != 'points'} for k,v in paths.items()}, 'shadow': shadow_luma}, indent=2))
