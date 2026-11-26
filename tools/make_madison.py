"""Grand Central Madison surfaces: gcs/md_floor (pale terrazzo), gcs/md_panel (white enamel wall panels, 2 x 4 per tile,
thin grey joints, faint sheen streaks) and gcs/md_ceil (white ceiling slats with one bright
linear light strip down the middle of each tile). At the default 0.25 scale a tile is
128 u, so panels are about 5 x 2.7 ft and the light strips run every 10.7 ft.
Writes src/materials/gcs/md_panel.vtf, md_ceil.vtf and PNG previews in shots/tex/.
Needs pip srctools pillow numpy."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from srctools import vtf

N = 512
rng = np.random.default_rng(20)


def save(img, name):
    img.save("shots/tex/%s.png" % name)
    rgba = np.dstack([np.asarray(img), np.full((N, N), 255, np.uint8)])
    tex = vtf.VTF(N, N, fmt=vtf.ImageFormats.RGB888)
    tex.get().copy_from(rgba.tobytes(), vtf.ImageFormats.RGBA8888)
    tex.compute_mipmaps()
    with open("src/materials/gcs/%s.vtf" % name, "wb") as f:
        tex.save(f)


# Wall panels: near-white with a cool cast, each panel a touch different, soft vertical sheen.
img = Image.new("RGB", (N, N), (232, 234, 236))
d = ImageDraw.Draw(img)
for i in range(2):
    for j in range(4):
        v = int(rng.integers(-6, 7))
        d.rectangle([i * 256, j * 128, i * 256 + 255, j * 128 + 127], fill=(232 + v, 234 + v, 237 + v))
sheen = Image.fromarray((rng.random((1, 16)) * 255).astype(np.uint8)).resize((N, N), Image.BICUBIC)
img = Image.blend(img, Image.merge("RGB", [sheen.point(lambda s: 220 + s // 10)] * 3), 0.15)
d = ImageDraw.Draw(img)
for i in range(3):
    d.line([(i * 256 % N, 0), (i * 256 % N, N)], fill=(150, 154, 160), width=4)
for j in range(5):
    d.line([(0, j * 128 % N), (N, j * 128 % N)], fill=(150, 154, 160), width=4)
save(img.filter(ImageFilter.GaussianBlur(0.6)), "md_panel")

# Floor: pale grey terrazzo, fine dark and white chips, faint joints every 256 px (8 ft at 0.25).
base = np.full((N, N, 3), (206, 205, 200), np.float32) + rng.normal(0, 3, (N, N, 1))
for col, n in (((120, 122, 126), 5000), ((250, 250, 246), 6000), ((168, 160, 150), 3000)):
    ys, xs = rng.integers(0, N, n), rng.integers(0, N, n)
    base[ys, xs] = col
    base[(ys + 1) % N, xs] = col
img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.5))
d = ImageDraw.Draw(img)
for i in range(3):
    d.line([(i * 256 % N, 0), (i * 256 % N, N)], fill=(172, 172, 170), width=2)
    d.line([(0, i * 256 % N), (N, i * 256 % N)], fill=(172, 172, 170), width=2)
save(img, "md_floor")

# Ceiling: white slats every 16 px, a glowing strip across the centre.
img = Image.new("RGB", (N, N), (222, 224, 226))
d = ImageDraw.Draw(img)
for y in range(0, N, 16):
    d.line([(0, y), (N, y)], fill=(190, 193, 197), width=2)
d.rectangle([0, N // 2 - 22, N, N // 2 + 22], fill=(170, 174, 180))
d.rectangle([0, N // 2 - 14, N, N // 2 + 14], fill=(255, 255, 252))
save(img.filter(ImageFilter.GaussianBlur(0.8)), "md_ceil")


def save_wide(img, name):
    w, h = img.size
    img.save("shots/tex/%s.png" % name)
    rgba = np.dstack([np.asarray(img), np.full((h, w), 255, np.uint8)])
    tex = vtf.VTF(w, h, fmt=vtf.ImageFormats.RGB888)
    tex.get().copy_from(rgba.tobytes(), vtf.ImageFormats.RGBA8888)
    tex.compute_mipmaps()
    with open("src/materials/gcs/%s.vtf" % name, "wb") as f:
        tex.save(f)


# Mosaic mural (gcs/md_mural, 1024 x 256, one wall): a stylised river of light, flowing bands of
# blue, teal, gold and coral with leaf and bird shapes, broken into 8 px tesserae with grout.
W2, H2 = 1024, 256
yy, xx = np.mgrid[0:H2, 0:W2].astype(np.float32)
pal = np.array([(28, 60, 120), (40, 120, 150), (90, 170, 160), (230, 190, 90), (225, 110, 80),
                (245, 235, 205), (60, 40, 100)], np.float32)
wave = (yy / H2 * 5 + np.sin(xx / 90) * 0.9 + np.sin(xx / 37 + 1.3) * 0.35) % len(pal)
img = Image.fromarray(pal[wave.astype(int)].astype(np.uint8))
d = ImageDraw.Draw(img)
for _ in range(26):
    cx, cy, r = int(rng.integers(20, W2 - 20)), int(rng.integers(30, H2 - 30)), int(rng.integers(10, 26))
    col = tuple(int(c) for c in pal[int(rng.integers(0, len(pal)))])
    if rng.random() < 0.5:
        d.ellipse([cx - r * 2, cy - r // 2, cx + r * 2, cy + r // 2], fill=col)
    else:
        d.polygon([(cx - r * 2, cy), (cx, cy - r // 3), (cx + r * 2, cy - r), (cx + r // 2, cy + r // 4)], fill=col)
a = np.asarray(img).astype(np.float32)
t = 8
a = a.reshape(H2 // t, t, W2 // t, t, 3).mean(axis=(1, 3))
a += rng.normal(0, 9, a.shape)
a = np.repeat(np.repeat(a, t, 0), t, 1)
a[::t, :] = (70, 68, 64)
a[:, ::t] = (70, 68, 64)
save_wide(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.4)), "md_mural")

# Storefront band (gcs/md_shops, 1024 x 256, the other wall): dark bronze fascia, lit sign strip,
# four glazed shop fronts with warm interiors and doors.
img = Image.new("RGB", (W2, H2), (34, 32, 30))
d = ImageDraw.Draw(img)
d.rectangle([0, 18, W2, 50], fill=(245, 240, 225))
names = ((180, 60, 50), (40, 90, 70), (40, 60, 110), (150, 110, 40))
for k in range(4):
    x0 = k * 256
    d.rectangle([x0 + 30, 26, x0 + 226, 42], fill=names[k])
    d.rectangle([x0 + 12, 62, x0 + 244, H2 - 8], fill=(255, 214, 150))
    for s in range(3):
        sy = 92 + s * 46
        d.rectangle([x0 + 20, sy, x0 + 236, sy + 6], fill=(120, 90, 60))
        for g in range(8):
            gx = x0 + 26 + g * 26 + int(rng.integers(-3, 4))
            d.rectangle([gx, sy - int(rng.integers(12, 26)), gx + 16, sy], fill=tuple(int(c) for c in pal[int(rng.integers(0, len(pal)))]))
    d.rectangle([x0 + 150, 62, x0 + 210, H2 - 8], fill=(200, 175, 135))
    for mx in (x0 + 12, x0 + 128, x0 + 150, x0 + 210, x0 + 244):
        d.rectangle([mx - 3, 62, mx + 3, H2 - 8], fill=(60, 50, 40))
    d.rectangle([x0 + 12, 58, x0 + 244, 64], fill=(60, 50, 40))
save_wide(img.filter(ImageFilter.GaussianBlur(0.5)), "md_shops")

# Floor band (gcs/md_band): charcoal terrazzo with white chips, laid as strips across the hall.
base = np.full((N, N, 3), (70, 72, 76), np.float32) + rng.normal(0, 3, (N, N, 1))
ys, xs = rng.integers(0, N, 7000), rng.integers(0, N, 7000)
base[ys, xs] = (225, 225, 220)
save(Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.5)), "md_band")
