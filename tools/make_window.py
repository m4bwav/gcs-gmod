"""Procedural window glass for the concourse windows: the real windows read as a pale,
glowing grid of small panes behind dark iron muntins (refs/photos/GCT_east_windows.jpg).
window_glass.vtf (256x256, tiles): 4x4 panes, slight per-pane tone variation, thin dark
muntins. Writes src/materials/gcs/window_glass.vtf and a preview in shots/tex/.
Needs pip srctools pillow numpy."""
import random
import numpy as np
from PIL import Image, ImageDraw
from srctools import vtf

random.seed(11)
N, P = 256, 64
img = Image.new("RGB", (N, N), (40, 42, 44))
d = ImageDraw.Draw(img)
for r in range(N // P):
    for c in range(N // P):
        k = random.uniform(-14, 10)
        top = (196 + k, 204 + k, 210 + k)
        for y in range(P - 6):                      # pane, slightly brighter at the top
            t = y / (P - 6)
            col = tuple(int(v - 22*t) for v in top)
            d.line([c*P + 3, r*P + 3 + y, c*P + P - 4, r*P + 3 + y], fill=col)
img.save("shots/tex/window_glass.png")
rgb = np.asarray(img)
tex = vtf.VTF(N, N, fmt=vtf.ImageFormats.RGB888)
tex.get().copy_from(np.dstack([rgb, np.full((N, N), 255, np.uint8)]).tobytes(), vtf.ImageFormats.RGBA8888)
tex.compute_mipmaps()
with open("src/materials/gcs/window_glass.vtf", "wb") as f:
    tex.save(f)
print("wrote src/materials/gcs/window_glass.vtf")
