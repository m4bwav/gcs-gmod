"""Procedural textures for the 42nd Street exterior (area 5).
facade_stone.vtf: warm grey granite/limestone ashlar (colour sampled from the Commons photo
42nd_Street_Facade_Grand_Central_Terminal_October_2025); asphalt.vtf; sidewalk.vtf (concrete
slabs); office.vtf (glass curtain-wall grid, the tower west of the terminal); metlife.vtf (pale
precast grid, the tower behind); inscription.vtf (GRAND CENTRAL TERMINAL cut in the attic);
clock_out.vtf (the Tiffany clock: dark dial, gold Roman numerals and ring).
Writes src/materials/gcs/*.vtf and previews in shots/tex/. Needs pip srctools pillow numpy."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from srctools import vtf

rng = np.random.default_rng(5)


def noise(w, h, octaves=5):
    out = np.zeros((h, w))
    for o in range(octaves):
        s = 2 ** (o + 2)
        img = Image.fromarray((rng.random((s, s)) * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        out += (np.asarray(img, float) / 255 - .5) / 2 ** o
    return out


def save(rgb, name):
    rgb = np.clip(rgb, 0, 255).astype(np.uint8)
    h, w = rgb.shape[:2]
    Image.fromarray(rgb).save("shots/tex/%s.png" % name)
    tex = vtf.VTF(w, h, fmt=vtf.ImageFormats.RGB888)
    tex.get().copy_from(np.dstack([rgb, np.full((h, w), 255, np.uint8)]).tobytes(), vtf.ImageFormats.RGBA8888)
    tex.compute_mipmaps()
    with open("src/materials/gcs/%s.vtf" % name, "wb") as f:
        tex.save(f)
    print("wrote src/materials/gcs/%s.vtf" % name)


def ashlar(n, base, courses, blocks, joint, jdark):
    img = np.ones((n, n, 3)) * base + noise(n, n)[..., None] * 28 + rng.normal(0, 4, (n, n, 1))
    ch = n // courses
    for c in range(courses):
        y0 = c * ch
        img[y0:y0 + joint] *= jdark
        tint = rng.normal(0, 5, 3)
        off = (n // blocks // 2) * (c % 2)
        img[y0 + joint:y0 + ch] += tint
        for b in range(blocks):
            x = (b * n // blocks + off) % n
            img[y0:y0 + ch, x:x + joint] *= jdark
    return img


def font(px):
    for f in ("C:/Windows/Fonts/times.ttf", "C:/Windows/Fonts/georgia.ttf", "DejaVuSerif.ttf"):
        try:
            return ImageFont.truetype(f, px)
        except OSError:
            pass
    return ImageFont.load_default()


save(ashlar(512, (166, 160, 150), 4, 2, 3, .78), "facade_stone")       # 4 courses x 2 blocks per tile

a = np.ones((512, 512, 3)) * 62 + noise(512, 512)[..., None] * 18 + rng.normal(0, 9, (512, 512, 1))
save(a, "asphalt")

s = np.ones((512, 512, 3)) * (168, 164, 156) + noise(512, 512)[..., None] * 16 + rng.normal(0, 5, (512, 512, 1))
for k in (0, 256):
    s[k:k + 3] *= .7
    s[:, k:k + 3] *= .7
save(s, "sidewalk")

# Curtain wall: 8 x 8 panes per tile, blue sky reflection graded per pane, thin silver mullions.
o = np.zeros((512, 512, 3))
sky = noise(512, 512, 3)
for j in range(8):
    for i in range(8):
        c = np.array((70, 110, 150)) + rng.normal(0, 12, 3) + (8 - j) * 4
        o[j * 64:(j + 1) * 64, i * 64:(i + 1) * 64] = c
o += sky[..., None] * 40
for k in range(0, 512, 64):
    o[k:k + 5] = (190, 196, 200)
    o[:, k:k + 3] = (170, 176, 180)
save(o, "office")

# MetLife: pale precast frame, deep-set small dark windows, 8 x 16 per tile.
m = np.ones((512, 512, 3)) * (214, 210, 200) + noise(512, 512)[..., None] * 10
for j in range(16):
    for i in range(8):
        m[j * 32 + 8:j * 32 + 26, i * 64 + 14:i * 64 + 50] = np.array((58, 66, 74)) + rng.normal(0, 8, 3)
save(m, "metlife")

# Attic inscription: carved letters, darker inside, light lower edge.
w, h = 1024, 128
img = Image.fromarray(np.clip(ashlar(1024, (166, 160, 150), 1, 4, 2, .85)[:h], 0, 255).astype(np.uint8))
d = ImageDraw.Draw(img)
f = font(62)
txt = "GRAND  CENTRAL  TERMINAL"
tw = d.textlength(txt, font=f)
d.text(((w - tw) / 2 + 2, 32 + 2), txt, font=f, fill=(206, 196, 182))
d.text(((w - tw) / 2, 32), txt, font=f, fill=(92, 84, 74))
save(np.asarray(img, float), "inscription")

# Tiffany clock: 512 px, dark blue-black dial, gold ring, Roman numerals, gold hands at 10:08.
n = 512
img = Image.new("RGB", (n, n), (166, 160, 150))
d = ImageDraw.Draw(img)
c = n / 2
d.ellipse((4, 4, n - 4, n - 4), fill=(176, 140, 60))
d.ellipse((24, 24, n - 24, n - 24), fill=(26, 30, 40))
d.ellipse((150, 150, n - 150, n - 150), outline=(190, 150, 60), width=6)
f = font(50)
for k, r in enumerate(["XII", "I", "II", "III", "IIII", "V", "VI", "VII", "VIII", "IX", "X", "XI"]):
    a = math.radians(k * 30 - 90)
    x, y = c + 182 * math.cos(a), c + 182 * math.sin(a)
    tw = d.textlength(r, font=f)
    d.text((x - tw / 2, y - 30), r, font=f, fill=(222, 180, 70))
for ang, ln, wd in ((10 * 30 + 4 - 90, 120, 14), (8 * 6 - 90, 190, 9)):
    a = math.radians(ang)
    d.line((c, c, c + ln * math.cos(a), c + ln * math.sin(a)), fill=(222, 180, 70), width=wd)
d.ellipse((c - 14, c - 14, c + 14, c + 14), fill=(222, 180, 70))
save(np.asarray(img, float), "clock_out")

# Facade window: dark glass behind a dark-green iron grid, one cell per tile (64 px; the map
# scales it to 24 x 36 u), so the grilles cost no brushes (the BSP is near its vertex cap).
g = np.ones((64, 64, 3)) * (22, 30, 28) + rng.normal(0, 3, (64, 64, 1))
g[:, :6] = g[:, -6:] = (44, 62, 52)
g[:5] = g[-5:] = (44, 62, 52)
save(np.tile(g, (8, 8, 1)), "facade_win")
