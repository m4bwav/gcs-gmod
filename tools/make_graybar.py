"""Graybar Passage wall stone: gcs/gb_stone, warm grey ashlar in courses (4 courses of 128 px,
blocks 256 px long, each course offset by half a block), thin pale joints, mottled faces.
At 0.25 scale a course is 32 u (2.7 ft) and a block 64 u, like the photos (refs/photos/GCT_Graybar_Passage.jpg).
Writes src/materials/gcs/gb_stone.vtf and shots/tex/gb_stone.png. Needs pip srctools pillow numpy."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from srctools import vtf

N = 512
rng = np.random.default_rng(31)
noise = Image.fromarray((rng.random((64, 64)) * 255).astype(np.uint8)).resize((N, N), Image.BICUBIC)
base = np.asarray(noise, np.float32) / 255 * 14 - 7
img = np.zeros((N, N, 3), np.float32)
for j in range(4):
    off = 128 * (j % 2)
    for i in range(-1, 3):
        x0, v = i * 256 + off, rng.integers(-8, 9)
        xs = slice(max(x0, 0), min(x0 + 256, N))
        img[j * 128:(j + 1) * 128, xs] = (196 + v, 188 + v, 172 + v)
img += base[..., None]
im = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))
d = ImageDraw.Draw(im)
for j in range(4):
    y = j * 128
    d.line([(0, y), (N, y)], fill=(222, 216, 204), width=3)
    for i in range(-1, 3):
        x = (i * 256 + 128 * (j % 2)) % N
        d.line([(x, y), (x, y + 128)], fill=(222, 216, 204), width=3)
im = im.filter(ImageFilter.GaussianBlur(0.6))
im.save("shots/tex/gb_stone.png")
tex = vtf.VTF(N, N, fmt=vtf.ImageFormats.RGB888)
tex.get().copy_from(np.dstack([np.asarray(im), np.full((N, N), 255, np.uint8)]).tobytes(), vtf.ImageFormats.RGBA8888)
tex.compute_mipmaps()
with open("src/materials/gcs/gb_stone.vtf", "wb") as f:
    tex.save(f)
