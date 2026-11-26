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


def plaque(word, name, p=6):
    # 1024x64 bronze band, raised gold 5x7 lettering (OYSTER BAR, PERSHING SQUARE).
    W, H = 1024, 64
    img = Image.new("RGB", (W, H), (40, 30, 20))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W-1, H-1], outline=(196, 156, 72), width=4)
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


def md_screen():
    # Grand Central Madison departure screen, 1024x256: navy LCD with a white header strip
    # (DEPARTURES, TRACK), then six LIRR trains (time, destination, track) in white text and
    # one amber status column. Mapped over 280 u wide screens (build_vmf madison).
    W, H = 1024, 256
    img = Image.new("RGB", (W, H), (10, 26, 64))
    d = ImageDraw.Draw(img)
    p = 3
    def text(x, y, s, col, q=p):
        for k, ch in enumerate(s):
            rows = [int(b, 16) for b in FONT.get(ch, "00 00 00 00 00 00 00").split()]
            for cy, bits in enumerate(rows):
                for cx in range(5):
                    if bits >> (4 - cx) & 1:
                        d.rectangle([x + (k*6 + cx)*q, y + cy*q, x + (k*6 + cx)*q + q - 1, y + cy*q + q - 1], fill=col)
    d.rectangle([0, 0, W, 40], fill=(232, 236, 242))
    text(16, 9, "DEPARTURES", (10, 26, 64), 3)
    text(W - 16 - 5*6*3, 9, "TRACK", (10, 26, 64), 3)
    dests = ["BABYLON", "HUNTINGTON", "RONKONKOMA", "PORT WASH", "HEMPSTEAD", "FAR ROCKAWAY",
             "LONG BEACH", "OYSTER BAY"]
    rng = random.Random(1680)
    t = 7*60 + 3
    for r in range(6):
        y = 54 + r*34
        if r % 2:
            d.rectangle([0, y - 6, W, y + 27], fill=(16, 36, 80))
        t += rng.choice((4, 7, 11))
        text(16, y, "%d:%02d" % (t//60, t % 60), (240, 240, 240))
        text(150, y, dests[r], (240, 240, 240))
        text(620, y, "ON TIME" if r != 3 else "BOARDING", (250, 190, 60))
        text(W - 16 - 2*6*p - 40, y, "%d" % (201 + r*3 % 10), (240, 240, 240))
    save(img, "md_screen")


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


def text(d, word, cx, y, p, c):
    x0 = cx - (len(word)*6 - 1)*p/2
    for k, ch in enumerate(word):
        if ch == " ":
            continue
        for cy, bits in enumerate(int(b, 16) for b in FONT[ch].split()):
            for bx in range(5):
                if bits >> (4 - bx) & 1:
                    px, py = x0 + (k*6 + bx)*p, y + cy*p
                    d.rectangle([px, py, px + p - 1, py + p - 1], fill=c)


def plat_ads():
    # Backlit platform posters (photo: Grand_Central_Station_tracks): 256x384 px drawn, stretched to 256x512 (power of two) = 72x144 u,
    # invented campaigns (no real brands), a thin steel frame, bright as a light box.
    ads = [("ad_hudson", ((40, 90, 150), (240, 180, 90)), ["HUDSON", "VALLEY"], "BY TRAIN", "hills"),
           ("ad_show", ((90, 20, 60), (230, 60, 90)), ["TONIGHT", "ON 42"], "BROADWAY", "stars"),
           ("ad_coffee", ((60, 35, 20), (200, 140, 70)), ["MORNING", "BLEND"], "TRACK SIDE", "cup"),
           ("ad_city", ((20, 30, 50), (90, 170, 210)), ["NEW YORK", "AFTER 8"], "LATE TRAINS", "towers")]
    rnd = random.Random(9)
    for name, (c0, c1), head, tag, art in ads:
        W, H = 256, 384
        img = Image.new("RGB", (W, H))
        d = ImageDraw.Draw(img)
        for y in range(H):
            t = y / H
            d.line([(0, y), (W, y)], fill=tuple(int(a + (b - a)*t) for a, b in zip(c0, c1)))
        if art == "hills":
            d.ellipse([150, 60, 210, 120], fill=(250, 230, 160))
            d.polygon([(0, 300), (70, 200), (140, 260), (200, 190), (256, 250), (256, 384), (0, 384)], fill=(40, 90, 50))
            d.polygon([(0, 340), (100, 270), (256, 320), (256, 384), (0, 384)], fill=(60, 120, 60))
        elif art == "stars":
            for _ in range(40):
                x, y = rnd.randint(0, W), rnd.randint(0, 220)
                d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(255, 230, 160))
            d.polygon([(128, 140), (60, 330), (196, 330)], fill=(250, 200, 80))
        elif art == "cup":
            d.rectangle([78, 190, 178, 300], fill=(240, 235, 225))
            d.ellipse([170, 210, 210, 260], outline=(240, 235, 225), width=8)
            for k in range(3):
                d.line([(100 + k*25, 180), (110 + k*25, 140)], fill=(240, 235, 225), width=4)
        else:
            for x in range(0, W, 28):
                h = rnd.randint(110, 240)
                d.rectangle([x, H - h - 40, x + 22, H - 40], fill=(15, 20, 35))
                for wy in range(H - h - 30, H - 50, 14):
                    if rnd.random() < 0.5:
                        d.rectangle([x + 5, wy, x + 9, wy + 5], fill=(250, 220, 130))
        for i, word in enumerate(head):
            text(d, word, W/2, 24 + i*44, 5, (255, 255, 250))
        d.rectangle([0, H - 40, W, H], fill=(15, 15, 18))
        text(d, tag, W/2, H - 30, 3, (240, 220, 120))
        d.rectangle([0, 0, W-1, H-1], outline=(120, 122, 125), width=6)
        save(img.resize((256, 512), Image.LANCZOS), name)
        with open("src/materials/gcs/%s.vmt" % name, "w", newline="") as f:
            f.write('"UnlitGeneric"\n{\n\t"$basetexture" "gcs/%s"\n\t"$surfaceprop" "glass"\n}\n' % name)


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

def train_side():
    # 1024x256 Metro-North M7 car side, one car (85 ft = 1020 u) by 150 u from floor to roof
    # (photo: Metro_North_M7a_Rainbow_Heart_Sticker_Grand_Central): brushed stainless, a dark
    # window per bay with rounded corners, sliding doors at L/4 and 3L/4 with tall windows,
    # yellow door sills, MTA roundel and number beside each door, panel seams.
    rng = np.random.default_rng(5)
    W, H = 1024, 256
    a = 182 + rng.normal(0, 5, (H, 1)) + rng.normal(0, 3, (H, W))
    img = Image.fromarray(np.dstack([a, a + 2, a + 6]).clip(0, 255).astype(np.uint8))
    d = ImageDraw.Draw(img)
    u = W / 1020                                   # px per unit along the car
    z = lambda h: int(H - h * H / 150)             # height in units -> row
    doors = (255, 765)
    for x in range(0, W, 64):
        if all(abs(x - c * u) > 50 for c in doors):
            d.line([(x, z(140)), (x, z(4))], fill=(150, 152, 156), width=1)
    d.line([(0, z(140)), (W, z(140))], fill=(120, 122, 128), width=2)     # roof line
    d.line([(0, z(6)), (W, z(6))], fill=(110, 112, 116), width=3)         # sill
    for c in doors:
        x0, x1 = int((c - 36) * u), int((c + 36) * u)
        d.rectangle([x0 - 3, z(90) - 3, x1 + 3, H - 1], fill=(120, 122, 126))
        d.rectangle([x0, z(88), x1, H - 1], fill=(196, 198, 202))
        m = (x0 + x1) // 2
        d.line([(m, z(88)), (m, H - 1)], fill=(80, 82, 86), width=2)
        for wx in (x0 + 6, m + 6):
            d.rounded_rectangle([wx, z(78), wx + (x1 - x0) // 2 - 12, z(40)], 4, fill=(22, 26, 32))
        d.rectangle([x0, H - 6, x1, H - 1], fill=(230, 190, 30))
        for k, x in ((0, x0 - 30), (1, x1 + 12)):
            if k == 0:
                d.ellipse([x, z(70), x + 16, z(70) + 16], fill=(20, 60, 160))
                d.text((x + 3, z(70) + 3), "M", fill=(255, 255, 255))
            else:
                d.rectangle([x, z(64), x + 12, z(52)], fill=(250, 210, 40))
    bays = [(18, 220), (292, 728), (802, 1002)]
    for b0, b1 in bays:
        n = max(1, round((b1 - b0) / 75))
        w = (b1 - b0) / n
        for i in range(n):
            x0, x1 = int((b0 + i * w + 8) * u), int((b0 + (i + 1) * w - 8) * u)
            d.rounded_rectangle([x0 - 2, z(98) - 2, x1 + 2, z(62) + 2], 6, fill=(60, 62, 66))
            d.rounded_rectangle([x0, z(98), x1, z(62)], 5, fill=(26, 30, 38))
            d.line([(x0 + 4, z(96)), (x0 + 16, z(66))], fill=(70, 78, 90), width=2)
    save(img, "train_side")


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


def lex_sign():
    # Navy hanging blade sign at the west end of Lexington Passage (refs: Lexington_Passage.jpg):
    # white Helvetica-like LEXINGTON AV, an arrow, and green 4 5 6 subway bullets. 512x128,
    # mapped over a 120x30 u slab (build_vmf lexington), both faces read left to right.
    from PIL import ImageFont
    W, H = 1024, 256
    img = Image.new("RGB", (W, H), (18, 34, 78))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W - 1, H - 1], outline=(230, 232, 236), width=6)
    f = ImageFont.truetype("arialbd.ttf", 92)
    fb = ImageFont.truetype("arialbd.ttf", 64)
    d.text((40, 30), "Lexington Av", font=f, fill=(245, 245, 245))
    d.text((40, 150), "Subway", font=fb, fill=(245, 245, 245))
    for k, n in enumerate("456"):
        cx, cy = 330 + k*96, 186
        d.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=(0, 147, 60))
        d.text((cx, cy), n, font=fb, fill=(255, 255, 255), anchor="mm")
    ax, ay = 860, 186                                  # arrow pointing ahead (east)
    d.polygon([(ax - 70, ay - 14), (ax + 10, ay - 14), (ax + 10, ay - 40), (ax + 70, ay),
               (ax + 10, ay + 40), (ax + 10, ay + 14), (ax - 70, ay + 14)], fill=(245, 245, 245))
    save(img, "lex_sign")


def lex_shop(name, seed, SW=593, streaks=40):
    # Lexington Passage shop front (refs: Lexington_Passage.jpg): bronze mullions over lit glass,
    # warm interior with shelves of goods, a glass door, a transom. 1024 px = 380 u along the
    # wall (the shop pitch); the 220 u window is px 0..593, the rest is wall behind the frames.
    rnd = random.Random(seed)
    # din_shop reuses it with SW 768: the dining concourse's 180 u glass on a 240 u pitch.
    W, H = 1024, 512
    img = Image.new("RGB", (W, H), (205, 190, 160))
    d = ImageDraw.Draw(img)
    for y in range(H):                                  # interior: warm, brighter at the top
        t = y / H
        d.line([(0, y), (SW, y)], fill=(int(250 - 70*t), int(225 - 75*t), int(175 - 70*t)))
    door = rnd.choice((0, 1, 2))
    bays = [(i * SW // 3, (i + 1) * SW // 3) for i in range(3)]
    for i, (a, b) in enumerate(bays):
        if i == door:                                   # glass door: deeper shop behind
            d.rectangle([a + 20, 120, b - 20, H], fill=(120, 95, 70))
            d.rectangle([a + 40, 150, b - 40, H - 40], fill=(150, 120, 85))
            d.line([(b - 46, 300), (b - 46, 380)], fill=(200, 170, 90), width=6)
            continue
        for sy in (210, 320, 430):                      # shelves with goods
            d.rectangle([a + 10, sy, b - 10, sy + 8], fill=(90, 70, 50))
            x = a + 14
            while x < b - 24:
                w, hh = rnd.randint(10, 30), rnd.randint(30, 80)
                c = rnd.choice([(170, 40, 40), (40, 70, 140), (230, 220, 200), (60, 120, 70),
                                (200, 160, 60), (30, 30, 30), (150, 100, 160)])
                d.rectangle([x, sy - hh, x + w, sy], fill=c)
                x += w + rnd.randint(2, 8)
    for k in range(SW // streaks):                      # reflection streaks
        x = rnd.randint(0, SW)
        d.line([(x, H), (x + 160, 110)], fill=(255, 245, 225), width=rnd.randint(2, 6))
    br = (110, 80, 40)
    d.rectangle([0, 0, SW, 110], fill=(40, 34, 30))     # transom / dark name band
    d.rectangle([0, 104, SW, 116], fill=br)
    for a, b in bays:
        d.rectangle([a, 0, a + 10, H], fill=br)
    d.rectangle([SW - 10, 0, SW, H], fill=br)
    d.rectangle([0, H - 14, SW, H], fill=br)
    save(img, name)


def mk_display():
    # Grand Central Market bow window: lit market stalls behind the glass, tiered crates of
    # fruit and vegetables, bread on racks, cheese wheels, a striped awning at the top.
    # 1024 px = the 316 u window run, 512 px = 108 u (z 24..132).
    rnd = random.Random(5)
    W, H = 1024, 512
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(250 - 60*t), int(230 - 70*t), int(190 - 80*t)))
    for i in range(0, W, 64):                           # awning stripes
        d.rectangle([i, 0, i + 31, 70], fill=(40, 90, 60))
        d.rectangle([i + 32, 0, i + 63, 70], fill=(235, 225, 200))
    for i in range(0, W, 32):
        d.pieslice([i, 54, i + 32, 86], 0, 180, fill=(40, 90, 60) if i % 64 == 0 else (235, 225, 200))
    stalls = [(0, 260, "fruit"), (260, 520, "bread"), (520, 760, "fruit"), (760, 1024, "cheese")]
    for a, b, kind in stalls:
        d.rectangle([a + 6, 100, b - 6, 140], fill=(60, 45, 35))  # stall sign board
        d.rectangle([a + 14, 108, b - 14, 132], fill=(200, 170, 90))
        for r, y in enumerate((230, 330, 440)):          # three tiers
            d.rectangle([a + 10, y, b - 10, y + 14], fill=(120, 85, 50))
            x = a + 14
            while x < b - 40:
                w = rnd.randint(40, 60)
                if kind == "fruit":
                    d.rectangle([x, y - 10, x + w, y], fill=(150, 110, 60))
                    c = rnd.choice([(200, 40, 30), (240, 170, 30), (90, 150, 40), (230, 210, 60),
                                    (120, 40, 90), (240, 120, 40)])
                    for k in range(w // 12):
                        for j in range(2):
                            cx, cy = x + 6 + k * 12, y - 16 - j * 10
                            d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=c)
                elif kind == "bread":
                    for k in range(w // 20):
                        cx = x + 10 + k * 20
                        d.ellipse([cx - 10, y - 18, cx + 10, y], fill=(190, 130, 60))
                        d.line([(cx - 5, y - 12), (cx + 5, y - 8)], fill=(230, 190, 120), width=2)
                else:
                    d.ellipse([x, y - 30, x + w, y], fill=(240, 205, 100))
                    d.rectangle([x, y - 15, x + w, y], fill=(225, 185, 80))
                x += w + rnd.randint(4, 10)
    for k in range(10):                                 # faint reflections
        x = rnd.randint(0, W)
        d.line([(x, H), (x + 120, 90)], fill=(255, 245, 230), width=2)
    save(img, "mk_display")


def gb_kiosk():
    # Graybar Passage newsstand kiosk: lit glass over racks of magazines, bronze frame and
    # counter. 512 px = 120 u wide, 512 px = 96 u high (kiosk wall).
    rnd = random.Random(7)
    W = H = 512
    img = Image.new("RGB", (W, H), (240, 220, 170))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=(int(250 - 50*t), int(232 - 60*t), int(185 - 70*t)))
    for sy in (150, 250, 340):                          # racks of magazines
        d.rectangle([14, sy, W - 14, sy + 6], fill=(90, 70, 50))
        x = 18
        while x < W - 40:
            w, hh = rnd.randint(26, 40), rnd.randint(40, 70)
            c = rnd.choice([(190, 40, 40), (30, 60, 150), (240, 235, 220), (40, 130, 80),
                            (230, 180, 40), (20, 20, 20), (170, 90, 170), (230, 120, 40)])
            d.rectangle([x, sy - hh, x + w, sy], fill=c)
            d.rectangle([x + 3, sy - hh + 4, x + w - 3, sy - hh + 12], fill=(250, 250, 245))
            x += w + rnd.randint(3, 6)
    br = (110, 80, 40)
    d.rectangle([0, 360, W, H], fill=(70, 50, 30))      # counter front
    d.rectangle([0, 360, W, 374], fill=(200, 160, 80))
    for k in range(10):                                 # reflection streaks
        x = rnd.randint(0, W)
        d.line([(x, 360), (x + 90, 20)], fill=(255, 248, 230), width=rnd.randint(2, 4))
    for a in (0, W // 2 - 5, W - 10):
        d.rectangle([a, 0, a + 10, H], fill=br)
    d.rectangle([0, 0, W, 10], fill=br)
    save(img, "gb_kiosk")


def leaded(img, x0, y0, x1, y1, c):
    # Leaded glass: octagons of cell c with small square quarries between them, warm lit glass,
    # dark lead cames. Fills the box x0,y0..x1,y1 of img (drawn apart, then pasted, so it clips).
    w, h = x1 - x0, y1 - y0
    g = Image.new("RGB", (w, h), (238, 214, 160))
    d = ImageDraw.Draw(g)
    k = c * 0.29
    lead = (52, 42, 30)
    for gy in range(0, h + c, c):
        for gx in range(0, w + c, c):
            pts = [(gx + k, gy), (gx + c - k, gy), (gx + c, gy + k), (gx + c, gy + c - k),
                   (gx + c - k, gy + c), (gx + k, gy + c), (gx, gy + c - k), (gx, gy + k)]
            t = (gx * 7 + gy * 3) // c % 5
            d.polygon(pts, fill=(246 - 4*t, 226 - 3*t, 178 - 6*t), outline=lead)
            d.polygon([(gx + c - k, gy + c), (gx + c, gy + c - k), (gx + c + k, gy + c), (gx + c, gy + c + k)],
                      fill=(200, 150, 70), outline=lead)
    d.rectangle([0, 0, w - 1, h - 1], outline=lead, width=3)
    img.paste(g, (x0, y0))


def ob_door():
    # Oyster Bar entrance doors: oak leaf with a tall leaded-glass light (octagon quarries) and a
    # brass kick plate; ob_door 256x512 maps once over a leaf. ob_lead 256x256 tiles the side lights.
    W, H = 256, 512
    img = Image.new("RGB", (W, H), (120, 78, 42))
    d = ImageDraw.Draw(img)
    for x in range(0, W, 3):                            # oak grain
        d.line([(x, 0), (x, H)], fill=(112 + (x * 37) % 17, 72 + (x * 13) % 11, 38))
    leaded(img, 30, 30, W - 30, 400, 49)
    d.rectangle([22, 22, W - 22, 408], outline=(80, 50, 26), width=8)
    d.rectangle([14, 440, W - 14, H - 10], fill=(196, 156, 78))        # brass kick plate
    d.line([(14, 446), (W - 14, 446)], fill=(240, 210, 130), width=2)
    d.rectangle([W - 40, 230, W - 30, 300], fill=(210, 170, 90))      # pull handle
    save(img, "ob_door")
    img = Image.new("RGB", (256, 256))
    leaded(img, 0, 0, 256, 256, 64)
    save(img, "ob_lead")


def cornice_lit():
    # 256x64 RGBA for the concourse springline cornice (GCT_Main_Concourse photo: a row of bare bulbs
    # along the gilded cornice). Gold band, dark egg-and-dart groove, 4 warm bulbs per tile; alpha is
    # the $selfillum mask so only the bulbs and their halo glow.
    W, H = 256, 64
    img = Image.new("RGB", (W, H), (176, 138, 70))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 6], fill=(214, 178, 104))
    d.rectangle([0, 6, W, 9], fill=(120, 90, 44))
    for x in range(0, W, 16):
        d.ellipse([x + 3, 11, x + 13, 21], fill=(150, 112, 54), outline=(98, 72, 34))
        d.line([(x, 11), (x, 22)], fill=(98, 72, 34), width=2)
    d.rectangle([0, 23, W, 26], fill=(214, 178, 104))
    d.rectangle([0, H - 6, W, H], fill=(120, 90, 44))
    for x in range(0, W + 1, 64):   # cream modillion brackets between the bulbs (were brushes)
        d.rectangle([x - 12, 27, x + 12, H], fill=(96, 74, 40))
        d.rectangle([x - 10, 27, x + 10, H - 2], fill=(226, 206, 160))
        d.rectangle([x - 10, 27, x + 10, 31], fill=(246, 230, 190))
        d.ellipse([x - 7, H - 16, x + 7, H - 4], outline=(150, 120, 74), width=2)
    mask = Image.new("L", (W, H), 0)
    m = ImageDraw.Draw(mask)
    for k in range(4):
        cx, cy = k * 64 + 32, 44
        for r, c, a in ((19, (255, 214, 150), 90), (14, (255, 236, 190), 190), (10, (255, 250, 232), 255)):
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)
            m.ellipse([cx - r, cy - r, cx + r, cy + r], fill=a)
    img.save("shots/tex/cornice_lit.png")
    a = np.dstack([np.asarray(img), np.asarray(mask)])
    tex = vtf.VTF(W, H, fmt=vtf.ImageFormats.RGBA8888)
    tex.get().copy_from(a.tobytes(), vtf.ImageFormats.RGBA8888)
    tex.compute_mipmaps()
    with open("src/materials/gcs/cornice_lit.vtf", "wb") as f:
        tex.save(f)
    nl, tab = chr(10), chr(9)
    with open("src/materials/gcs/cornice_lit.vmt", "w", newline="") as f:
        f.write('"LightmappedGeneric"' + nl + "{" + nl + tab + '"$basetexture" "gcs/cornice_lit"' + nl
                + tab + '"$selfillum" "1"' + nl + tab + '"$selfillumtint" "[2 2 2]"' + nl + tab + '"$surfaceprop" "metal"' + nl + "}" + nl)
    print("wrote src/materials/gcs/cornice_lit.vtf")


def lunette():
    # 256x256 for the concourse lunettes (Flag_Ceiling / Main_Concourse photos: deep blue-grey glass
    # behind a fine bronze grille, heavier bars every 64 px). Painted grille replaces the 5 mullion
    # brushes per lunette (vertex budget); a faint $selfillum keeps the glass reading as daylight.
    W = 256
    rng = np.random.default_rng(45)
    g = np.zeros((W, W, 3), np.float32)
    y = np.linspace(0, 1, W)[:, None]
    g[..., 0], g[..., 1], g[..., 2] = 70 + 40 * y, 86 + 40 * y, 104 + 36 * y
    g += rng.normal(0, 6, (W, W, 1))
    img = Image.fromarray(np.clip(g, 0, 255).astype(np.uint8), "RGB")
    d = ImageDraw.Draw(img)
    for k in range(0, W, 16):
        d.line([(k, 0), (k, W)], fill=(58, 50, 38), width=2)
        d.line([(0, k), (W, k)], fill=(58, 50, 38), width=2)
    for k in range(0, W, 64):
        d.rectangle([k - 4, 0, k + 3, W], fill=(44, 38, 28))
        d.rectangle([0, k - 4, W, k + 3], fill=(44, 38, 28))
    save(img, "lunette")
    nl, tab = chr(10), chr(9)
    with open("src/materials/gcs/lunette.vmt", "w", newline="") as f:
        f.write('"LightmappedGeneric"' + nl + "{" + nl + tab + '"$basetexture" "gcs/lunette"' + nl
                + tab + '"$selfillum" "1"' + nl + tab + '"$selfillumtint" "[0.55 0.6 0.7]"' + nl + tab + '"$surfaceprop" "glass"' + nl + "}" + nl)


board()
flag()
tickets()
plaque("OYSTER BAR", "oysterbar")
plaque("PERSHING SQUARE", "pershing")
plaque("GRAND CENTRAL MARKET", "mk_sign", 5)
track_signs()
train_steel()
train_side()
endwin_grid()
arrivals()
md_screen()
lex_sign()
lex_shop("lex_shop_n", 11)
lex_shop("lex_shop_s", 23)
lex_shop("din_shop_n", 37, 768, 90)
lex_shop("din_shop_s", 41, 768, 90)
gb_kiosk()
mk_display()
ob_door()
plat_ads()
cornice_lit()
lunette()
