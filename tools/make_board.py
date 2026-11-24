"""Procedural departure board over the ticket windows and the hanging US flag.
board.vtf (1024x256): black LED board, header row, amber/white rows of train times,
destinations and track numbers in a blocky dot-matrix hand. flag.vtf (512x256): the
US flag hung horizontally (union at the viewer's upper left), public-domain design.
Writes src/materials/gcs/{board,flag}.vtf and previews in shots/tex/.
Needs pip srctools pillow numpy."""
import random
import numpy as np
from PIL import Image, ImageDraw
from srctools import vtf

random.seed(7)
AMBER, WHITE, GREEN = (255, 176, 40), (235, 235, 225), (90, 220, 110)
DEST = ["STAMFORD", "NEW HAVEN", "WHITE PLAINS", "POUGHKEEPSIE", "CROTON-HARMON", "NEW CANAAN",
        "DANBURY", "WASSAIC", "SOUTHEAST", "GREENWICH", "HARLEM-125 ST", "NORTH WHITE PL",
        "BREWSTER", "TARRYTOWN", "WATERBURY", "MOUNT KISCO"]
LINE = ["NEW HAVEN", "HARLEM", "HUDSON"]


def save(img, name):
    img.save("shots/tex/%s.png" % name)
    rgb = np.asarray(img.convert("RGB"))
    h, w = rgb.shape[:2]
    tex = vtf.VTF(w, h, fmt=vtf.ImageFormats.RGB888)
    tex.get().copy_from(np.dstack([rgb, np.full((h, w), 255, np.uint8)]).tobytes(), vtf.ImageFormats.RGBA8888)
    tex.compute_mipmaps()
    with open("src/materials/gcs/%s.vtf" % name, "wb") as f:
        tex.save(f)
    print("wrote src/materials/gcs/%s.vtf" % name)


def board():
    S = 2
    W, H = 1024*S, 256*S
    img = Image.new("RGB", (W, H), (8, 8, 10))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W-1, H-1], outline=(150, 112, 50), width=6*S)            # brass frame
    d.rectangle([6*S, 6*S, W-6*S, 30*S], fill=(20, 40, 90))                      # header band
    cols = [16, 120, 330, 760, 900]                                              # time, line, dest, track, status
    def text(x, y, s, col, h):
        """Dot-matrix stand-in: each glyph a cluster of lit cells."""
        cw = h * 0.62
        for k, ch in enumerate(s):
            if ch == " ":
                continue
            gx = x + k*cw
            rnd = random.Random(ord(ch))
            for cy in range(5):
                for cx in range(3):
                    if rnd.random() < 0.62:
                        px, py = gx + cx*cw/4, y + cy*h/6
                        d.rectangle([px, py, px + cw/4.6, py + h/7], fill=col)
    for c, label in zip(cols, ["TIME", "LINE", "DESTINATION", "TRACK", "STATUS"]):
        text(c*S, 11*S, label, WHITE, 14*S)
    t = 7*60 + 2
    for r in range(8):
        y = (38 + r*27)*S
        t += random.choice((4, 6, 9, 11))
        col = AMBER if r % 2 == 0 else WHITE
        text(cols[0]*S, y, "%d:%02d" % (t//60, t % 60), col, 18*S)
        text(cols[1]*S, y, random.choice(LINE), col, 18*S)
        text(cols[2]*S, y, DEST[r*2 % len(DEST)], col, 18*S)
        text(cols[3]*S, y, str(random.randint(11, 42)), col, 18*S)
        text(cols[4]*S, y, "ON TIME" if r % 3 else "BOARDING", GREEN if r % 3 == 0 else col, 18*S)
    save(img.resize((1024, 256), Image.LANCZOS), "board")


def flag():
    # Horizontal flag 1.9:1, hung flat like the concourse flag: stripes run across.
    W, H = 760, 400
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)
    red, blue = (178, 34, 52), (60, 59, 110)
    sh = H / 13
    for k in range(0, 13, 2):
        d.rectangle([0, k*sh, W, (k+1)*sh - 1], fill=red)
    uw, uh = W*0.4, sh*7
    d.rectangle([0, 0, uw, uh], fill=blue)
    for row in range(9):
        n = 6 if row % 2 == 0 else 5
        for k in range(n):
            x = uw/12 * (2*k + 1 + (row % 2))
            y = uh/10 * (row + 1)
            r = sh*0.3
            d.polygon([(x + r*np.cos(a), y + r*np.sin(a)) for a in
                       [np.pi/2*3 + i*np.pi*4/5 for i in range(5)]], fill=(255, 255, 255))
    save(img.resize((512, 256), Image.LANCZOS), "flag")


board()
flag()
