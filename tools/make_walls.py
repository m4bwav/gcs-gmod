"""Procedural wall ashlar and vault sky for the concourse, colours sampled by eye from
refs/photos (GCT_Main_Concourse, Flag_Ceiling): honey limestone blocks in staggered
courses with thin light joints, and a dark teal vault with scattered gold stars.
Writes src/materials/gcs/wall_ashlar.vtf, vault_sky.vtf and previews in shots/tex/.
Needs pip srctools pillow numpy."""
import numpy as np
from PIL import Image
from srctools import vtf

N = 512
rng = np.random.default_rng(11)


def fbm(n, octaves=6):
    out = np.zeros((n, n))
    for o in range(octaves):
        k = 4 * 2**o
        g = rng.random((k, k))
        img = Image.fromarray((g * 255).astype(np.uint8)).resize((n, n), Image.BICUBIC)
        out += (np.asarray(img, float) / 255 - .5) / 2**o
    return out


def save(rgb, name):
    Image.fromarray(rgb).save("shots/tex/%s.png" % name)
    tex = vtf.VTF(N, N, fmt=vtf.ImageFormats.RGB888)
    rgba = np.dstack([rgb, np.full((N, N), 255, np.uint8)])
    tex.get().copy_from(rgba.tobytes(), vtf.ImageFormats.RGBA8888)
    tex.compute_mipmaps()
    with open("src/materials/gcs/%s.vtf" % name, "wb") as f:
        tex.save(f)
    print("wrote src/materials/gcs/%s.vtf" % name)


# Ashlar: 8 courses, 3 blocks per course, alternate courses offset by half a block.
HONEY = np.array([222, 194, 150], float)
COURSES, BLOCKS = 8, 3
img = np.zeros((N, N, 3))
ch, bw = N // COURSES, N // BLOCKS
grain = fbm(N, 6)
for c in range(COURSES):
    off = (bw // 2) * (c % 2)
    for b in range(BLOCKS + 1):
        x0, x1 = max(0, b*bw - off), min(N, (b+1)*bw - off)
        if x1 <= x0:
            continue
        tint = 1 + rng.uniform(-.07, .07)
        warm = np.array([1, 1 + rng.uniform(-.03, .02), 1 + rng.uniform(-.06, .03)])
        img[c*ch:(c+1)*ch, x0:x1] = HONEY * warm * tint
img *= (1 + grain * 0.12)[..., None]
joint = np.zeros((N, N), bool)
for c in range(COURSES):
    joint[c*ch:c*ch+3, :] = True
    off = (bw // 2) * (c % 2)
    for b in range(BLOCKS + 1):
        x = (b*bw - off) % N
        joint[c*ch:(c+1)*ch, x:x+3] = True
img[joint] = HONEY * 1.08
save(np.clip(img, 0, 255).astype(np.uint8), "wall_ashlar")

# Vault: dark teal with soft cloudiness and gold stars of a few sizes.
TEAL = np.array([38, 104, 92], float)
img = TEAL * (1 + fbm(N, 5) * 0.18)[..., None]
y, x = np.mgrid[0:N, 0:N]
GOLD = np.array([236, 200, 120], float)
for _ in range(70):
    cx, cy = rng.integers(0, N, 2)
    r = rng.choice([1.2, 1.8, 2.6, 3.5], p=[.5, .3, .15, .05])
    d = np.hypot((x - cx + N/2) % N - N/2, (y - cy + N/2) % N - N/2)
    a = np.clip(1 - d / r, 0, 1)[..., None]
    img = img * (1 - a) + GOLD * a
save(np.clip(img, 0, 255).astype(np.uint8), "vault_sky")
