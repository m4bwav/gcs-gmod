"""Procedural zodiac mural for the concourse vault, mapped once over the whole vault
(u along the 275 ft length, v along the arc from the north springline to the south one).
Colours sampled from refs/photos/Grand_Central_Station_Flag_Ceiling.jpg: deep green field,
gold stars, gold band lines. Layout after the real ceiling: the ecliptic and the equator as
two gold arcs crossing the length, twelve zodiac constellations as stick figures along the
ecliptic, a faint Milky Way. Figures are simplified (small creative ruling, see HANDOFF).
Writes src/materials/gcs/vault_mural.vtf and shots/tex/vault_mural.png. Needs srctools pillow numpy."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from srctools import vtf

W, H = 2048, 1024
S = 2                       # supersample
rng = np.random.default_rng(7)

GREEN = np.array([24, 98, 74], float)
GOLD = (232, 196, 116)


def fbm(w, h, octaves=6):
    out = np.zeros((h, w))
    for o in range(octaves):
        k = 4 * 2**o
        g = rng.random((k, 2*k))
        img = Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)
        out += (np.asarray(img, float) / 255 - .5) / 2**o
    return out


w, h = W*S, H*S
base = GREEN * (1 + fbm(w, h, 5) * 0.16)[..., None]
# Milky Way: a soft lighter band running diagonally.
y, x = np.mgrid[0:h, 0:w] / np.array([h, w])[:, None, None]
d = (y - (0.15 + 0.7*x))
mw = np.exp(-(d / 0.09)**2) * (0.6 + 0.8*np.clip(fbm(w, h, 6) + .5, 0, 1))
base = base * (1 - .35*mw[..., None]) + np.array([90, 150, 120]) * .35*mw[..., None]
img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))
dr = ImageDraw.Draw(img)

# Faint background stars.
for _ in range(900):
    cx, cy = rng.random() * w, rng.random() * h
    r = rng.choice([1.5, 2.2, 3.0], p=[.6, .3, .1]) * S
    dr.ellipse([cx-r, cy-r, cx+r, cy+r], fill=(200, 180, 120))

# Ecliptic and equator: two gold arcs across the length, crossing near the middle.
def band(fn, width=3):
    xs = np.linspace(0, w, 400)
    pts = [(xx, fn(xx / w) * h) for xx in xs]
    dr.line(pts, fill=GOLD, width=width*S)
    off = 9 * S
    dr.line([(px, py+off) for px, py in pts], fill=GOLD, width=max(1, width-1)*S)
    for i in range(0, len(pts), 8):        # degree ticks between the double lines
        px, py = pts[i]
        dr.line([(px, py), (px, py+off)], fill=GOLD, width=S)
    return pts

ecl = lambda t: 0.5 + 0.22*np.sin(2*np.pi*(t - .25))
equ = lambda t: 0.5 - 0.10*np.sin(2*np.pi*(t - .25))
band(ecl)
band(equ)

# Twelve zodiac figures as stick constellations (relative star coordinates, then lines).
FIGS = [
    ([(0, 0), (.4, -.3), (.9, -.2), (1.2, .2)], [(0, 1), (1, 2), (2, 3)]),                     # aries
    ([(0, 0), (.5, .1), (.9, -.2), (1.4, -.6), (.9, .4), (1.4, .7)], [(0, 1), (1, 2), (2, 3), (1, 4), (4, 5)]),  # taurus
    ([(0, 0), (0, 1), (.5, 0), (.5, 1), (0, .5), (.5, .5)], [(0, 1), (2, 3), (4, 5)]),       # gemini
    ([(0, 0), (.4, .3), (.8, 0), (.4, .9)], [(0, 1), (1, 2), (1, 3)]),                         # cancer
    ([(0, 0), (.3, -.4), (.7, -.3), (.8, .2), (1.6, .1), (1.7, .6), (.8, .6)], [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (3, 6)]),  # leo
    ([(0, 0), (.5, .2), (1, 0), (1.5, .3), (.5, .8), (1.2, .9)], [(0, 1), (1, 2), (2, 3), (1, 4), (2, 5)]),  # virgo
    ([(0, 0), (.6, -.3), (1.2, 0), (.6, .6)], [(0, 1), (1, 2), (2, 3), (3, 0)]),               # libra
    ([(0, 0), (.4, .1), (.8, .3), (1.1, .7), (1.3, 1.1), (1.7, 1.2), (1.9, .9)], [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6)]),  # scorpio
    ([(0, 0), (.5, .4), (1, .2), (.8, -.3), (.3, -.4), (1.3, .6)], [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (2, 5)]),  # sagittarius
    ([(0, 0), (.7, .5), (1.4, .4), (1.2, -.2)], [(0, 1), (1, 2), (2, 3), (3, 0)]),             # capricorn
    ([(0, 0), (.4, .3), (.8, .1), (1.2, .4), (1.6, .2), (.6, .9)], [(0, 1), (1, 2), (2, 3), (3, 4), (2, 5)]),  # aquarius
    ([(0, 0), (.6, .3), (1.2, .5), (1.5, .1), (1.8, -.3), (2.2, -.1)], [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5)]),  # pisces
]
SC = 0.075 * h
for i, (stars, lines) in enumerate(FIGS):
    t = (i + .5) / 12
    cx = t * w - .8*SC
    cy = ecl(t) * h + (-1.6 if i % 2 else .6) * SC     # alternate above and below the band
    pts = [(cx + sx*SC, cy + sy*SC) for sx, sy in stars]
    for a, b in lines:
        dr.line([pts[a], pts[b]], fill=(200, 170, 100), width=2*S)
    for px, py in pts:
        r = rng.choice([4, 5.5, 7]) * S
        dr.ellipse([px-r, py-r, px+r, py+r], fill=(255, 226, 150))

# A little glow around the gold.
img = img.resize((W, H), Image.LANCZOS)
glow = img.filter(ImageFilter.GaussianBlur(3))
rgb = np.maximum(np.asarray(img, float), np.asarray(glow, float) * .9 + np.asarray(img, float) * .1)
rgb = np.clip(rgb, 0, 255).astype(np.uint8)
Image.fromarray(rgb).save("shots/tex/vault_mural.png")

tex = vtf.VTF(W, H, fmt=vtf.ImageFormats.RGB888)
tex.get().copy_from(np.dstack([rgb, np.full((H, W), 255, np.uint8)]).tobytes(), vtf.ImageFormats.RGBA8888)
tex.compute_mipmaps()
with open("src/materials/gcs/vault_mural.vtf", "wb") as f:
    tex.save(f)
print("wrote src/materials/gcs/vault_mural.vtf")
