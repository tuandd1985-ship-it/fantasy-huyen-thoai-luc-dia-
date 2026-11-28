import sys, json
from PIL import Image, ImageDraw
d = sys.argv[1]; m = json.load(open(d + "/animations.json")); rows = []; BG = (78, 92, 64)
for n, a in m["actions"].items():
    S = Image.open(d + "/" + a["file"]); k = a["frames"]; R = Image.new("RGB", (k * 240, 214), BG)
    for i in range(k):
        b = Image.new("RGBA", (768, 640), BG + (255,)); b.alpha_composite(S.crop((i * 768, 0, (i + 1) * 768, 640))); dr = ImageDraw.Draw(b)
        dr.rectangle([0, 0, 767, 639], outline=(255, 0, 0)); dr.line([(0, 620), (768, 620)], fill=(255, 220, 0))
        if a["hit_frame"] == i: dr.text((10, 10), "HIT", fill=(255, 60, 60))
        R.paste(b.convert("RGB").resize((240, 200)), (i * 240, 14))
    ImageDraw.Draw(R).text((3, 1), n + " ms=" + str(a["durations_ms"]), fill="white"); rows.append(R)
W = max(r.width for r in rows); T = Image.new("RGB", (W, sum(r.height for r in rows)), BG); y = 0
for r in rows: T.paste(r, (0, y)); y += r.height
T.save(d + "/contact.jpg", quality=88)
