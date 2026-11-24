"""Procedural face for the information-booth clock: an opal (milky white) dial with black
Roman-style hour bars and minute ticks, black hands at about 10:08, in a brass bezel with
brass corners. One face per side of the clock housing.
Writes src/materials/gcs/clock_face.vtf and shots/tex/clock_face.png.
Needs pip srctools pillow numpy."""
import math
import numpy as np
from PIL import Image, ImageDraw
from srctools import vtf

N = 256
SS = 4                      # supersample, then downscale for smooth edges
M = N * SS
c = M / 2
img = Image.new("RGB", (M, M), (176, 134, 62))          # brass corners
d = ImageDraw.Draw(img)
R = M * 0.47
d.ellipse([c-R, c-R, c+R, c+R], fill=(214, 172, 86))     # brass bezel
d.ellipse([c-R*0.98, c-R*0.98, c+R*0.98, c+R*0.98], fill=(150, 112, 50))
r = R * 0.88
d.ellipse([c-r, c-r, c+r, c+r], fill=(246, 240, 222))    # opal dial
for k in range(60):
    a = 2*math.pi*k/60
    big = k % 5 == 0
    r0 = r * (0.78 if big else 0.90)
    w = M * (0.022 if big else 0.006)
    x0, y0 = c + r0*math.sin(a), c - r0*math.cos(a)
    x1, y1 = c + r*0.96*math.sin(a), c - r*0.96*math.cos(a)
    d.line([x0, y0, x1, y1], fill=(28, 24, 20), width=max(1, int(w)))


def hand(frac, length, width):
    a = 2*math.pi*frac
    d.line([c - r*0.12*math.sin(a), c + r*0.12*math.cos(a),
            c + r*length*math.sin(a), c - r*length*math.cos(a)],
           fill=(20, 18, 16), width=int(M*width))


hand((10 + 8/60) / 12, 0.52, 0.026)   # hour
hand(8 / 60, 0.80, 0.016)             # minute
d.ellipse([c-M*0.025, c-M*0.025, c+M*0.025, c+M*0.025], fill=(20, 18, 16))
img = img.resize((N, N), Image.LANCZOS)
img.save("shots/tex/clock_face.png")

rgb = np.asarray(img)
tex = vtf.VTF(N, N, fmt=vtf.ImageFormats.RGB888)
tex.get().copy_from(np.dstack([rgb, np.full((N, N), 255, np.uint8)]).tobytes(), vtf.ImageFormats.RGBA8888)
tex.compute_mipmaps()
with open("src/materials/gcs/clock_face.vtf", "wb") as f:
    tex.save(f)
print("wrote src/materials/gcs/clock_face.vtf")
