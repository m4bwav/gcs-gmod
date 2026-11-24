"""Procedural zodiac mural for the concourse vault, mapped once over the whole vault
(u along the 275 ft length, v along the arc from the north springline to the south one).
Colours sampled from refs/photos/Grand_Central_Station_Flag_Ceiling.jpg: deep green field,
gold stars, gold band lines. Layout after the real ceiling: the ecliptic and the equator as
two gold arcs crossing the length, twelve zodiac constellations as stick figures along the
ecliptic, a faint Milky Way. Figures are simplified: stick constellations over gold-outlined silhouettes of each sign
(small creative ruling, see HANDOFF).
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


# Figure silhouettes per sign, in SC units relative to the constellation origin: each is a list
# of ("e", x0, y0, x1, y1) ellipses, ("p", [(x, y), ...]) polygons and ("l", [(x, y), ...], width) strokes.
def _arc(cx, cy, r, a0, a1, n=10):
    return [(cx + r*np.cos(np.radians(a)), cy + r*np.sin(np.radians(a))) for a in np.linspace(a0, a1, n)]


def _fish(x, y, d):
    return [("e", x-.45, y-.2, x+.45, y+.2), ("p", [(x+.4*d, y), (x+.75*d, y-.25), (x+.75*d, y+.25)])]


def _person(x, y, s=1.):
    return [("e", x-.13*s, y-.95*s, x+.13*s, y-.68*s), ("p", [(x-.15*s, y-.66*s), (x+.15*s, y-.66*s), (x+.32*s, y+.3*s), (x-.32*s, y+.3*s)])]


SHAPES = [
    [("e", -.1, -.45, 1.0, .1), ("e", .9, -.65, 1.35, -.3), ("l", _arc(1.05, -.6, .22, 180, 470), .12),
     ("l", [(.05, 0), (.0, .45)], .1), ("l", [(.85, 0), (.9, .45)], .1)],                       # aries: ram with curled horn
    [("e", -.1, -.35, 1.0, .35), ("e", .9, -.55, 1.45, -.05), ("l", [(1.0, -.5), (.85, -.85)], .1),
     ("l", [(1.35, -.5), (1.5, -.85)], .1), ("l", [(.1, .3), (.05, .7)], .12), ("l", [(.8, .3), (.85, .7)], .12)],  # taurus
    _person(0, .9, .9) + _person(.5, .9, .9) + [("l", [(.1, .3), (.4, .3)], .08)],                # gemini: twins holding hands
    [("e", .05, .15, .75, .65), ("l", _arc(.0, .1, .2, 90, 320), .1), ("l", _arc(.8, .1, .2, -140, 90), .1)]
    + [("l", [(.15 + .15*i, .6), (.05 + .2*i, .85)], .06) for i in range(4)],                     # cancer: crab with claws
    [("e", .1, -.4, 1.4, .25), ("e", -.15, -.7, .55, .05), ("l", [(1.35, -.1), (1.75, .2), (1.8, .6)], .08),
     ("l", [(.25, .2), (.2, .65)], .12), ("l", [(1.2, .2), (1.25, .65)], .12)],                   # leo: lion with mane
    _person(.6, .55, 1.1) + [("p", [(.3, .0), (.95, .0), (1.25, .9), (.0, .9)]), ("l", [(.75, -.2), (1.3, -.05)], .07)],  # virgo: robed woman with sheaf
    [("l", [(.6, -.4), (.6, .6)], .08), ("l", [(-.05, -.25), (1.25, -.25)], .08),
     ("p", [(-.25, .25), (.15, .25), (-.05, .4)]), ("p", [(1.05, .25), (1.45, .25), (1.25, .4)]),
     ("l", [(-.05, -.25), (-.25, .25)], .04), ("l", [(-.05, -.25), (.15, .25)], .04),
     ("l", [(1.25, -.25), (1.05, .25)], .04), ("l", [(1.25, -.25), (1.45, .25)], .04)],           # libra: scales
    [("e", -.15, -.15, .6, .3), ("l", [(.5, .1), (.9, .4), (1.2, .8), (1.5, 1.15), (1.8, 1.1), (1.9, .85)], .16),
     ("l", _arc(-.25, -.15, .18, 90, 300), .08), ("l", _arc(-.25, .3, .18, 60, 270), .08)],       # scorpio: curled tail
    [("e", .0, .0, 1.0, .45), ("l", [(.1, .4), (.05, .8)], .1), ("l", [(.9, .4), (.95, .8)], .1)]
    + _person(.95, .1, .8) + [("l", _arc(1.25, -.35, .45, -70, 70), .06), ("l", [(.95, -.35), (1.55, -.35)], .04)],  # sagittarius: centaur archer
    [("e", .0, -.2, .8, .3), ("e", .6, -.5, 1.0, -.15), ("l", [(.7, -.45), (.55, -.8)], .08),
     ("l", [(.8, .25), (1.2, .45), (1.5, .3)], .18), ("p", [(1.45, .3), (1.7, .05), (1.75, .5)])],  # capricorn: goat-fish
    _person(.4, .5, 1.1) + [("e", .55, -.2, .95, .15), ("l", [(.9, .1), (1.1, .4), (1.3, .2), (1.5, .5), (1.7, .3)], .1)],  # aquarius: urn and stream
    _fish(.2, -.1, -1) + _fish(1.9, .1, 1) + [("l", [(.3, .1), (1.0, .55), (1.8, .25)], .04)],     # pisces: two fish on a cord
]


def figure(ox, oy, shape):
    """Gold-outlined figure silhouette with a faint lighter wash behind a constellation: a
    simplified stand-in for the real ceiling's gold-line figure drawings."""
    m = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(m)
    P = lambda x, y: (ox + x*SC, oy + y*SC)
    for part in shape:
        if part[0] == "e":
            (x0, y0), (x1, y1) = P(*part[1:3]), P(*part[3:5])
            md.ellipse([x0, y0, x1, y1], fill=255)
        elif part[0] == "p":
            md.polygon([P(*q) for q in part[1]], fill=255)
        else:
            md.line([P(*q) for q in part[1]], fill=255, width=max(2, int(part[2]*SC)), joint="curve")
    m = m.filter(ImageFilter.GaussianBlur(.04*SC)).point(lambda v: 255 if v > 110 else 0)
    img.paste(Image.new("RGB", img.size, (66, 136, 100)),
              (0, 0), m.filter(ImageFilter.GaussianBlur(3*S)).point(lambda v: v*60//255))
    a = np.asarray(m) > 0
    grow = a.copy()
    for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1), (-1, 1), (1, -1)):
        grow |= np.roll(np.roll(a, dy, 0), dx, 1)
    edge = grow & ~a
    img.paste(Image.new("RGB", img.size, (214, 182, 112)), (0, 0), Image.fromarray(edge.astype(np.uint8)*255))


for i, (stars, lines) in enumerate(FIGS):
    t = (i + .5) / 12
    cx = t * w - .8*SC
    cy = ecl(t) * h + (-1.6 if i % 2 else .6) * SC     # alternate above and below the band
    figure(cx, cy, SHAPES[i])
    pts = [(cx + sx*SC, cy + sy*SC) for sx, sy in stars]
    for a, b in lines:
        dr.line([pts[a], pts[b]], fill=(200, 170, 100), width=S)
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
