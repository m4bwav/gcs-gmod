"""Procedural Guastavino tile for the Whispering Gallery and Oyster Bar vaults: buff
terracotta tiles (6 x 12 in) in a herringbone, thin pale joints, each tile a little
different in tone and glaze, colours by eye from Commons photos of the gallery.
Writes src/materials/gcs/guastavino.vtf (512 px = 8 ft at scale 0.1875) and a preview
in shots/tex/. Needs pip srctools pillow numpy."""
import numpy as np
from PIL import Image
from srctools import vtf

N = 512
rng = np.random.default_rng(23)
BUFF = np.array([214, 178, 128], float)
JOINT = np.array([226, 214, 190], float)

# Herringbone on a 45 deg lattice: unit = 1 tile width (w px), tiles are 2w x w.
w = 32 / np.sqrt(2)   # diagonal step 32 px so the lattice tiles over 512 px
yy, xx = np.mgrid[0:N, 0:N].astype(float)
u, v = (xx + yy) / (w * np.sqrt(2)), (xx - yy) / (w * np.sqrt(2))
# Classic herringbone: a period-2 staircase of horizontal and vertical 2x1 tiles.
uf, vf = np.floor(u).astype(int), np.floor(v).astype(int)
k = (uf - vf) % 4                       # which step of the staircase
horiz = k < 2
P = 16                                  # lattice period over 512 px; wrap ids so tiles match across the seam
tile_id = np.where(horiz, ((uf - (k % 2)) % P) * 7919 + (vf % P) * 104729,
                   (uf % P) * 7919 + ((vf - ((uf - vf) % 2)) % P) * 104729 + 1)
fu, fv = u - uf, v - vf
edge_u = np.where(horiz, ((k % 2 == 0) & (fu < .06)) | ((k % 2 == 1) & (fu > .94)), (fu < .06) | (fu > .94))
edge_v = np.where(horiz, (fv < .06) | (fv > .94), (((uf - vf) % 2 == 0) & (fv > .94)) | (((uf - vf) % 2 == 1) & (fv < .06)))
joint = edge_u | edge_v

# Per-tile tone: hash the id into a brightness and warmth jitter.
h = (np.sin(tile_id * 12.9898) * 43758.5453) % 1
h2 = (np.sin(tile_id * 78.233) * 12543.123) % 1
tone = BUFF * (0.88 + 0.2 * h[..., None])
tone[..., 0] += (h2 - .5) * 14
tone[..., 2] -= (h2 - .5) * 10
grain = rng.normal(0, 4, (N, N, 1))
img = np.where(joint[..., None], JOINT, tone + grain)
img = np.clip(img, 0, 255).astype(np.uint8)

Image.fromarray(img).save("shots/tex/guastavino.png")
tex = vtf.VTF(N, N, fmt=vtf.ImageFormats.RGB888)
tex.get().copy_from(np.dstack([img, np.full((N, N), 255, np.uint8)]).tobytes(), vtf.ImageFormats.RGBA8888)
tex.compute_mipmaps()
with open("src/materials/gcs/guastavino.vtf", "wb") as f:
    tex.save(f)
print("wrote src/materials/gcs/guastavino.vtf")

# Dark oak for the Oyster Bar counters: long brown streaks along u.
g = np.cumsum(rng.normal(0, 1, (N, 1)), 0) * 0.6 + rng.normal(0, 3, (N, N))
streak = np.sin(np.linspace(0, 40 * np.pi, N)[:, None] + g / 6) * 10
wood = np.array([92, 58, 34], float) + (streak + rng.normal(0, 3, (N, N)))[..., None] * np.array([1, .7, .45])
wood = np.clip(wood, 0, 255).astype(np.uint8)
Image.fromarray(wood).save("shots/tex/wood.png")
tex = vtf.VTF(N, N, fmt=vtf.ImageFormats.RGB888)
tex.get().copy_from(np.dstack([wood, np.full((N, N), 255, np.uint8)]).tobytes(), vtf.ImageFormats.RGBA8888)
tex.compute_mipmaps()
with open("src/materials/gcs/wood.vtf", "wb") as f:
    tex.save(f)
print("wrote src/materials/gcs/wood.vtf")
