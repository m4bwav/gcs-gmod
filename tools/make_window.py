"""Procedural window glass for the concourse windows: the real windows read as a pale,
glowing grid of small panes behind dark iron muntins (refs/photos/GCT_east_windows.jpg).
window_glass.vtf (256x256, tiles): 4x4 panes, slight per-pane tone variation, thick dark
bronze muntins. Writes src/materials/gcs/window_glass.vtf and a preview in shots/tex/.
Needs pip srctools pillow numpy."""
import random
import numpy as np
from PIL import Image, ImageDraw
from srctools import vtf

random.seed(11)
N, P = 256, 64
img = Image.new("RGB", (N, N), (46, 38, 28))   # dark bronze muntins (photo ~ 45 38 30)
d = ImageDraw.Draw(img)
for r in range(N // P):
    for c in range(N // P):
        k = random.uniform(-14, 10)
        top = (150 + k, 166 + k, 182 + k)            # cooler, dimmer panes (photo ~ 140 158 176)
        for y in range(P - 12):                      # pane, slightly brighter at the top
            t = y / (P - 12)
            col = tuple(int(v - 22*t) for v in top)
            d.line([c*P + 6, r*P + 6 + y, c*P + P - 7, r*P + 6 + y], fill=col)
img.save("shots/tex/window_glass.png")
rgb = np.asarray(img)
tex = vtf.VTF(N, N, fmt=vtf.ImageFormats.RGB888)
tex.get().copy_from(np.dstack([rgb, np.full((N, N), 255, np.uint8)]).tobytes(), vtf.ImageFormats.RGBA8888)
tex.compute_mipmaps()
with open("src/materials/gcs/window_glass.vtf", "wb") as f:
    tex.save(f)
print("wrote src/materials/gcs/window_glass.vtf")
