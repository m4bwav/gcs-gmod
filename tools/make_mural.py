"""Painted ceiling for Graybar Passage's groin bays: one 512 px tile per 32 ft bay, drawn in
plan (build_vmf.py maps it top-down, FACEUV gcs/gb_mural), so the diagonals are the groin
lines. Pale sky field, gold ribs on the groins, ochre border with a key pattern, a gold
sunburst at the crown and a star wreath in each cell. A stylised stand-in for the real
painted vaults, not a copy. Writes src/materials/gcs/gb_mural.vtf and shots/tex/gb_mural.png.
Needs pip srctools pillow numpy."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from srctools import vtf

N = 512
SKY, GOLD, OCHRE, DARK, CREAM = (156, 190, 196), (206, 166, 82), (176, 128, 70), (72, 84, 80), (236, 222, 190)
rng = np.random.default_rng(19)

img = Image.new("RGB", (N, N), SKY)
d = ImageDraw.Draw(img)
# Soft fresco mottling.
noise = Image.fromarray((rng.random((32, 32)) * 255).astype(np.uint8)).resize((N, N), Image.BICUBIC)
img = Image.blend(img, Image.merge("RGB", [noise.point(lambda v: 150 + v // 6)] * 3), 0.12)
d = ImageDraw.Draw(img)

# Border: ochre band with a cream key pattern, dark rules either side.
B = 34
d.rectangle([0, 0, N - 1, N - 1], outline=DARK, width=B)
d.rectangle([4, 4, N - 5, N - 5], outline=OCHRE, width=B - 8)
for k in range(0, N, 32):
    for x0, y0, horiz in ((k, 10, 1), (k, N - 24, 1), (10, k, 0), (N - 24, k, 0)):
        if horiz:
            d.line([(x0 + 6, y0 + 12), (x0 + 6, y0 + 2), (x0 + 22, y0 + 2), (x0 + 22, y0 + 10), (x0 + 14, y0 + 10)], fill=CREAM, width=3)
        else:
            d.line([(x0 + 12, y0 + 6), (x0 + 2, y0 + 6), (x0 + 2, y0 + 22), (x0 + 10, y0 + 22), (x0 + 10, y0 + 14)], fill=CREAM, width=3)

# Groin ribs on the diagonals.
for a, b in (((0, 0), (N, N)), ((N, 0), (0, N))):
    d.line([a, b], fill=DARK, width=20)
    d.line([a, b], fill=GOLD, width=12)
    d.line([a, b], fill=CREAM, width=2)

# Star wreath in each cell (between border and the crown).
c = N / 2
for ang in (0, 90, 180, 270):
    t = math.radians(ang)
    mx, my = c + 140 * math.cos(t), c + 140 * math.sin(t)
    d.ellipse([mx - 58, my - 58, mx + 58, my + 58], outline=GOLD, width=4)
    for i in range(12):
        s = math.radians(i * 30)
        lx, ly = mx + 46 * math.cos(s), my + 46 * math.sin(s)
        d.ellipse([lx - 7, ly - 4, lx + 7, ly + 4], fill=OCHRE)
    pts = [(mx + (26 if j % 2 == 0 else 11) * math.cos(math.radians(-90 + j * 36)),
            my + (26 if j % 2 == 0 else 11) * math.sin(math.radians(-90 + j * 36))) for j in range(10)]
    d.polygon(pts, fill=GOLD, outline=DARK)

# Crown sunburst.
for i in range(24):
    q = math.radians(i * 15)
    r = 70 if i % 2 == 0 else 50
    d.polygon([(c + 18 * math.cos(q - .2), c + 18 * math.sin(q - .2)), (c + r * math.cos(q), c + r * math.sin(q)),
               (c + 18 * math.cos(q + .2), c + 18 * math.sin(q + .2))], fill=GOLD)
d.ellipse([c - 26, c - 26, c + 26, c + 26], fill=GOLD, outline=DARK, width=3)
d.ellipse([c - 12, c - 12, c + 12, c + 12], fill=CREAM)

img = img.filter(ImageFilter.GaussianBlur(0.6))
img.save("shots/tex/gb_mural.png")
rgba = np.dstack([np.asarray(img), np.full((N, N), 255, np.uint8)])
tex = vtf.VTF(N, N, fmt=vtf.ImageFormats.RGB888)
tex.get().copy_from(rgba.tobytes(), vtf.ImageFormats.RGBA8888)
tex.compute_mipmaps()
with open("src/materials/gcs/gb_mural.vtf", "wb") as f:
    tex.save(f)
print("wrote src/materials/gcs/gb_mural.vtf")
