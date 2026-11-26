"""Grand Central Madison surfaces: gcs/md_panel (white enamel wall panels, 2 x 4 per tile,
thin grey joints, faint sheen streaks) and gcs/md_ceil (white ceiling slats with one bright
linear light strip down the middle of each tile). At the default 0.25 scale a tile is
128 u, so panels are about 5 x 2.7 ft and the light strips run every 10.7 ft.
Writes src/materials/gcs/md_panel.vtf, md_ceil.vtf and PNG previews in shots/tex/.
Needs pip srctools pillow numpy."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from srctools import vtf

N = 512
rng = np.random.default_rng(20)


def save(img, name):
    img.save("shots/tex/%s.png" % name)
    rgba = np.dstack([np.asarray(img), np.full((N, N), 255, np.uint8)])
    tex = vtf.VTF(N, N, fmt=vtf.ImageFormats.RGB888)
    tex.get().copy_from(rgba.tobytes(), vtf.ImageFormats.RGBA8888)
    tex.compute_mipmaps()
    with open("src/materials/gcs/%s.vtf" % name, "wb") as f:
        tex.save(f)


# Wall panels: near-white with a cool cast, each panel a touch different, soft vertical sheen.
img = Image.new("RGB", (N, N), (232, 234, 236))
d = ImageDraw.Draw(img)
for i in range(2):
    for j in range(4):
        v = int(rng.integers(-6, 7))
        d.rectangle([i * 256, j * 128, i * 256 + 255, j * 128 + 127], fill=(232 + v, 234 + v, 237 + v))
sheen = Image.fromarray((rng.random((1, 16)) * 255).astype(np.uint8)).resize((N, N), Image.BICUBIC)
img = Image.blend(img, Image.merge("RGB", [sheen.point(lambda s: 220 + s // 10)] * 3), 0.15)
d = ImageDraw.Draw(img)
for i in range(3):
    d.line([(i * 256 % N, 0), (i * 256 % N, N)], fill=(150, 154, 160), width=4)
for j in range(5):
    d.line([(0, j * 128 % N), (N, j * 128 % N)], fill=(150, 154, 160), width=4)
save(img.filter(ImageFilter.GaussianBlur(0.6)), "md_panel")

# Ceiling: white slats every 16 px, a glowing strip across the centre.
img = Image.new("RGB", (N, N), (222, 224, 226))
d = ImageDraw.Draw(img)
for y in range(0, N, 16):
    d.line([(0, y), (N, y)], fill=(190, 193, 197), width=2)
d.rectangle([0, N // 2 - 22, N, N // 2 + 22], fill=(170, 174, 180))
d.rectangle([0, N // 2 - 14, N, N // 2 + 14], fill=(255, 255, 252))
save(img.filter(ImageFilter.GaussianBlur(0.8)), "md_ceil")
