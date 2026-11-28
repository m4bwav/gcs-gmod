"""Escalator textures for the MetLife escalators (build_vmf.py metlife_escalators).
Writes src/materials/gcs/esc_tread.vtf: 256 px = 64 u along the run, four 16 u steps, each a
grey cleated tread, a dark riser shadow and a yellow nose line. esc_up/esc_dn.vmt scroll it."""
import numpy as np
from PIL import Image, ImageDraw
from srctools import vtf

N = 256
img = Image.new("RGB", (N, N), (120, 122, 126))
d = ImageDraw.Draw(img)
for y in range(0, N, 6):                     # cleats run along the direction of travel (u)
    d.line([(0, y), (N, y)], fill=(70, 72, 76), width=2)
for k in range(4):
    x = k * 64
    d.rectangle([x, 0, x + 13, N], fill=(28, 29, 32))       # riser in shadow
    d.rectangle([x + 14, 0, x + 18, N], fill=(214, 180, 40))  # yellow step nose
    d.rectangle([x + 19, 0, x + 22, N], fill=(160, 162, 166))  # lit edge
img.save("shots/tex/esc_tread.png")
rgba = np.dstack([np.asarray(img), np.full((N, N), 255, np.uint8)])
tex = vtf.VTF(N, N, fmt=vtf.ImageFormats.RGB888)
tex.get().copy_from(rgba.tobytes(), vtf.ImageFormats.RGBA8888)
tex.compute_mipmaps()
with open("src/materials/gcs/esc_tread.vtf", "wb") as f:
    tex.save(f)
