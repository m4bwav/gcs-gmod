"""The Campbell's surfaces, matched to refs/photos/GCT_Campbell_1.jpg and _3.jpg:
gcs/cb_wall (warm tan sandstone, 4 courses x 2 blocks per tile, dim joints), gcs/cb_wain (dark
oak wainscot panels with lighter rails), gcs/cb_ceil (painted ceiling: dark beam grid round 2 x 2
ochre panels with a red border and a green-gold stencil rosette) and gcs/cb_leaded (dense leaded
window, 8 x 8 amber panes per tile, glowing; UnlitGeneric). At the default 0.25 scale a tile is
128 u, so wall blocks are 5.3 x 2.7 ft, ceiling panels 5.3 ft and window panes 16 u.
Writes src/materials/gcs/cb_*.vtf and PNG previews in shots/tex/. Needs pip srctools pillow numpy."""
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from srctools import vtf

N = 512
rng = np.random.default_rng(23)


def save(img, name):
    img.save("shots/tex/%s.png" % name)
    rgba = np.dstack([np.asarray(img), np.full((N, N), 255, np.uint8)])
    tex = vtf.VTF(N, N, fmt=vtf.ImageFormats.RGB888)
    tex.get().copy_from(rgba.tobytes(), vtf.ImageFormats.RGBA8888)
    tex.compute_mipmaps()
    with open("src/materials/gcs/%s.vtf" % name, "wb") as f:
        tex.save(f)


def grain(amount):
    g = rng.normal(0, amount, (N, N, 1))
    return np.repeat(g, 3, axis=2)


# Sandstone: staggered blocks, each a slightly different warm tan, fine grain, darker joints.
img = Image.new("RGB", (N, N), (170, 128, 84))
d = ImageDraw.Draw(img)
for j in range(4):
    off = 128 if j % 2 else 0
    for i in range(3):
        v = int(rng.integers(-12, 13))
        x = i * 256 - off
        d.rectangle([x, j * 128, x + 255, j * 128 + 127], fill=(170 + v, 128 + v, 84 + v // 2))
a = np.asarray(img).astype(float) + grain(5)
img = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
d = ImageDraw.Draw(img)
for j in range(4):
    off = 128 if j % 2 else 0
    d.line([(0, j * 128), (N, j * 128)], fill=(104, 76, 48), width=3)
    for i in range(3):
        x = (i * 256 - off) % N
        d.line([(x, j * 128), (x, j * 128 + 127)], fill=(104, 76, 48), width=3)
save(img.filter(ImageFilter.GaussianBlur(0.7)), "cb_wall")

# Wainscot: two raised panels per tile, dark oak with streaky grain, lighter stiles and rails.
oak = np.zeros((N, N, 3))
streak = rng.normal(0, 1, (N, 1)) * 10
oak[:] = np.array([72, 44, 24]) + streak[:, :, None] * np.array([1, 0.7, 0.4])
oak = np.transpose(oak, (1, 0, 2)) + grain(3)
img = Image.fromarray(np.clip(oak, 0, 255).astype(np.uint8))
d = ImageDraw.Draw(img)
for i in range(2):
    x = i * 256
    d.rectangle([x, 0, x + 255, N - 1], outline=(110, 72, 40), width=28)
    d.rectangle([x + 40, 40, x + 215, N - 41], outline=(46, 26, 14), width=6)
save(img.filter(ImageFilter.GaussianBlur(0.5)), "cb_wain")

# Painted ceiling: dark beam grid, ochre panels, red border, gold-green stencil rosette.
img = Image.new("RGB", (N, N), (56, 34, 20))
d = ImageDraw.Draw(img)
for i in range(2):
    for j in range(2):
        x, y = i * 256 + 24, j * 256 + 24
        d.rectangle([x, y, x + 207, y + 207], fill=(150, 34, 26))
        d.rectangle([x + 14, y + 14, x + 193, y + 193], fill=(184, 140, 62))
        d.rectangle([x + 26, y + 26, x + 181, y + 181], outline=(70, 92, 54), width=4)
        cx, cy = x + 104, y + 104
        for k in range(8):
            t = k * np.pi / 4
            px, py = cx + 44 * np.cos(t), cy + 44 * np.sin(t)
            d.ellipse([px - 16, py - 16, px + 16, py + 16], fill=(70, 92, 54))
        d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(214, 172, 80))
        d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(150, 34, 26))
        for k in range(4):
            px, py = (x + 34, x + 174)[k % 2], (y + 34, y + 174)[k // 2]
            d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=(214, 172, 80))
a = np.asarray(img).astype(float) + grain(4)
save(Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8)), "cb_ceil")

# Leaded window: 8 x 8 panes, warm amber, each a touch different, dark lead cames.
img = Image.new("RGB", (N, N), (30, 22, 14))
d = ImageDraw.Draw(img)
for i in range(8):
    for j in range(8):
        v = int(rng.integers(-18, 19))
        d.rectangle([i * 64 + 4, j * 64 + 4, i * 64 + 59, j * 64 + 59], fill=(236 + v // 3, 196 + v, 128 + v))
save(img.filter(ImageFilter.GaussianBlur(0.6)), "cb_leaded")
