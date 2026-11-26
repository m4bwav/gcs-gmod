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
SHORT = ["STAMFORD", "RYE", "DANBURY", "WASSAIC", "BREWSTER", "BEACON", "GREENWCH", "OSSINING",
         "CROTON", "MT KISCO", "DOVER PL", "TARRYTWN", "NORWALK", "PELHAM", "SCARSDLE", "KATONAH",
         "PEEKSKIL", "YONKERS", "HARRISON", "DARIEN", "WESTPORT", "FAIRFLD", "SOUTHPRT", "MILFORD"]
LINE = ["NEW HAVEN", "HARLEM", "HUDSON"]


# 5x7 dot-matrix font: each glyph is 7 rows of 5 bits (MSB = left column).
FONT = {
    "A": "0E 11 11 1F 11 11 11", "B": "1E 11 11 1E 11 11 1E", "C": "0E 11 10 10 10 11 0E",
    "D": "1E 11 11 11 11 11 1E", "E": "1F 10 10 1E 10 10 1F", "F": "1F 10 10 1E 10 10 10",
    "G": "0E 11 10 17 11 11 0F", "H": "11 11 11 1F 11 11 11", "I": "0E 04 04 04 04 04 0E",
    "J": "07 02 02 02 02 12 0C", "K": "11 12 14 18 14 12 11", "L": "10 10 10 10 10 10 1F",
    "M": "11 1B 15 15 11 11 11", "N": "11 11 19 15 13 11 11", "O": "0E 11 11 11 11 11 0E",
    "P": "1E 11 11 1E 10 10 10", "Q": "0E 11 11 11 15 12 0D", "R": "1E 11 11 1E 14 12 11",
    "S": "0F 10 10 0E 01 01 1E", "T": "1F 04 04 04 04 04 04", "U": "11 11 11 11 11 11 0E",
    "V": "11 11 11 11 11 0A 04", "W": "11 11 11 15 15 15 0A", "X": "11 11 0A 04 0A 11 11",
    "Y": "11 11 11 0A 04 04 04", "Z": "1F 01 02 04 08 10 1F",
    "0": "0E 11 13 15 19 11 0E", "1": "04 0C 04 04 04 04 0E", "2": "0E 11 01 02 04 08 1F",
    "3": "1F 02 04 02 01 11 0E", "4": "02 06 0A 12 1F 02 02", "5": "1F 10 1E 01 01 11 0E",
    "6": "06 08 10 1E 11 11 0E", "7": "1F 01 02 04 08 08 08", "8": "0E 11 11 0E 11 11 0E",
    "9": "0E 11 11 0F 01 02 0C", ":": "00 0C 0C 00 0C 0C 00", "-": "00 00 00 1F 00 00 00",
    ".": "00 00 00 00 00 0C 0C",
}


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
    cols = [16, 120, 330, 730, 860]                                              # time, line, dest, track, status
    def text(x, y, s, col, h):
        """5x7 dot-matrix lettering: one round LED per lit cell, unlit cells faintly visible."""
        p = h / 7.0
        dim = tuple(int(v*0.10) + 10 for v in col)
        for k, ch in enumerate(s):
            gx = x + k*6*p
            rows = [int(b, 16) for b in FONT.get(ch, "00 00 00 00 00 00 00").split()]
            for cy, bits in enumerate(rows):
                for cx in range(5):
                    lit = bits >> (4 - cx) & 1
                    px, py = gx + cx*p, y + cy*p
                    d.ellipse([px, py, px + p*0.8, py + p*0.8], fill=col if lit else dim)
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


def tickets():
    # 1024x64 strip spanning one 16 ft window pitch; the bronze plaque with raised gold
    # TICKETS lettering sits in texels 320..704 (the 6 ft plaque over each window).
    W, H = 1024, 64
    img = Image.new("RGB", (W, H), (60, 42, 22))
    d = ImageDraw.Draw(img)
    d.rectangle([320, 0, 703, H-1], fill=(34, 26, 18), outline=(196, 156, 72), width=4)
    d.rectangle([328, 8, 695, H-9], outline=(120, 92, 44), width=1)
    p, word = 5, "TICKETS"
    x0 = 512 - (len(word)*6 - 1)*p/2
    for k, ch in enumerate(word):
        rows = [int(b, 16) for b in FONT[ch].split()]
        for cy, bits in enumerate(rows):
            for cx in range(5):
                if bits >> (4 - cx) & 1:
                    px, py = x0 + (k*6 + cx)*p, 14 + cy*p
                    d.rectangle([px, py, px + p - 1, py + p - 1], fill=(230, 190, 96))
    save(img, "tickets")


def plaque(word, name):
    # 1024x64 bronze band, raised gold 5x7 lettering (OYSTER BAR, PERSHING SQUARE).
    W, H = 1024, 64
    img = Image.new("RGB", (W, H), (40, 30, 20))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W-1, H-1], outline=(196, 156, 72), width=4)
    p = 6
    x0 = 512 - (len(word)*6 - 1)*p*1.5/2
    for k, ch in enumerate(word):
        if ch == " ":
            continue
        rows = [int(b, 16) for b in FONT[ch].split()]
        for cy, bits in enumerate(rows):
            for cx in range(5):
                if bits >> (4 - cx) & 1:
                    px, py = x0 + (k*6 + cx)*p*1.5, 11 + cy*p
                    d.rectangle([px, py, px + p*1.5 - 1, py + p - 1], fill=(230, 190, 96))
    save(img, name)


def arrivals():
    # Biltmore Room arrivals board, 1024x256: four panels split by the brass mullions, each a
    # split-flap column (white letters on dark flap tiles with a hinge line): ARRIVALS header,
    # then six trains (time, origin). Mapped once over the board glass (build_vmf _arrivals_uv).
    W, H = 1024, 256
    img = Image.new("RGB", (W, H), (14, 14, 16))
    d = ImageDraw.Draw(img)
    p = 3
    def flap(x, y, s, col):
        for k, ch in enumerate(s):
            gx = x + k*6*p
            d.rectangle([gx - 2, y - 3, gx + 5*p + 1, y + 7*p + 2], fill=(34, 34, 38))
            rows = [int(b, 16) for b in FONT.get(ch, "00 00 00 00 00 00 00").split()]
            for cy, bits in enumerate(rows):
                for cx in range(5):
                    if bits >> (4 - cx) & 1:
                        d.rectangle([gx + cx*p, y + cy*p, gx + cx*p + p - 1, y + cy*p + p - 1], fill=col)
            d.line([gx - 2, y + 3.5*p, gx + 5*p + 1, y + 3.5*p], fill=(8, 8, 8), width=1)
    rng = random.Random(61)
    t = 6*60 + 48
    for q in range(4):
        x0 = q*256 + 8
        flap(x0 + (240 - (8*6 - 1)*p)//2, 14, "ARRIVALS", (240, 225, 170))
        d.line([x0, 44, x0 + 240, 44], fill=(150, 112, 50), width=2)
        for r in range(6):
            t += rng.choice((2, 4, 6))
            dest = SHORT[(q*6 + r)*5 % len(SHORT)]
            flap(x0 + 2, 58 + r*32, "%d:%02d" % (t//60, t % 60), (235, 235, 225))
            flap(x0 + 2 + 5*6*p, 58 + r*32, dest, (235, 235, 225))
    save(img, "arrivals")


def track_signs():
    # 512x128 black gate signs with white serif-less "TRACK nn" (photo: Grand_Central_Station_tracks).
    for n in (29, 30, 31, 108, 112):
        W, H = 512, 128
        img = Image.new("RGB", (W, H), (22, 22, 24))
        d = ImageDraw.Draw(img)
        d.rectangle([0, 0, W-1, H-1], outline=(150, 150, 150), width=4)
        word, p = "TRACK %d" % n, 9
        x0 = W/2 - (len(word)*6 - 1)*p/2
        for k, ch in enumerate(word):
            if ch == " ":
                continue
            for cy, bits in enumerate(int(b, 16) for b in FONT[ch].split()):
                for cx in range(5):
                    if bits >> (4 - cx) & 1:
                        px, py = x0 + (k*6 + cx)*p, 32 + cy*p
                        d.rectangle([px, py, px + p - 1, py + p - 1], fill=(240, 238, 228))
        save(img, "track%d" % n)


def train_steel():
    # 512x512 stainless car side: brushed grey with fine horizontal streaks, riveted vertical
    # panel seams every 128 px (photo: Metro_North_M7a_Rainbow_Heart_Sticker_Grand_Central).
    rng = np.random.default_rng(3)
    a = 178 + rng.normal(0, 6, (512, 1)) + rng.normal(0, 3, (512, 512))
    a = np.clip(a, 0, 255)
    img = Image.fromarray(np.dstack([a, a + 2, a + 6]).clip(0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    for x in range(0, 512, 128):
        d.line([(x, 0), (x, 511)], fill=(120, 122, 126), width=2)
        for y in range(8, 512, 32):
            d.ellipse([x + 5, y, x + 8, y + 3], fill=(150, 152, 156))
    save(img, "train_steel")


def endwin_grid():
    # 512x512 RGBA mullion grid for the concourse end windows: 8 x 8 clear cells (alpha 0) between
    # 8 px dark bronze bars, so one alpha-tested panel replaces ~50 bar brushes per window (vertex budget).
    a = np.zeros((512, 512, 4), np.uint8)
    for k in range(9):
        p = min(k * 64, 511)
        a[max(p - 4, 0):p + 4, :, :] = (52, 50, 44, 255)
        a[:, max(p - 4, 0):p + 4, :] = (52, 50, 44, 255)
    Image.fromarray(a, "RGBA").save("shots/tex/endwin_grid.png")
    tex = vtf.VTF(512, 512, fmt=vtf.ImageFormats.RGBA8888)
    tex.get().copy_from(a.tobytes(), vtf.ImageFormats.RGBA8888)
    tex.compute_mipmaps()
    with open("src/materials/gcs/endwin_grid.vtf", "wb") as f:
        tex.save(f)
    nl, tab = chr(10), chr(9)
    for name in ("endwin_a", "endwin_b", "endwin_c"):
        with open("src/materials/gcs/%s.vmt" % name, "w", newline="") as f:
            f.write('"LightmappedGeneric"' + nl + "{" + nl + tab + '"$basetexture" "gcs/endwin_grid"' + nl
                    + tab + '"$alphatest" "1"' + nl + tab + '"$surfaceprop" "metal"' + nl + "}" + nl)
    print("wrote src/materials/gcs/endwin_grid.vtf")


board()
flag()
tickets()
plaque("OYSTER BAR", "oysterbar")
plaque("PERSHING SQUARE", "pershing")
track_signs()
train_steel()
endwin_grid()
arrivals()
