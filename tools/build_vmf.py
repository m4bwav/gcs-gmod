"""Build src/gm_grand_central.vmf from the measured layout (1 ft = 12 u).

Blockout stage: Main Concourse only. Run: python tools/build_vmf.py
"""
import math
from pathlib import Path

FT = 12
OUT = Path(__file__).resolve().parent.parent / "src" / "gm_grand_central.vmf"

# Main Concourse: 275 x 120 ft floor, vault crown ~125 ft. Long axis = x (east +x).
HX, HY = 275 * FT // 2, 120 * FT // 2      # 1650, 720
CROWN = 125 * FT                            # 1500
VRISE = 40 * FT                             # vault rise: a flattened half-ellipse, half-width HY
SPRING = CROWN - VRISE                      # springline (cornice) height
BAYS = 5                                    # bays along each long wall, one lunette each
WALL = 64
BALC_Z = 26 * FT                            # balcony floor height
BALC_D = 22 * FT                            # balcony depth from the end wall
BAY_Z0 = 42 * FT                            # bottom of the long-wall bay windows (photo estimate)
ARCH_W, ARCH_TOP, ARCH_D = 18 * FT, 21 * FT, 16 * FT   # floor arcade under each balcony
BARCH_W, BARCH_H = 14 * FT, 14 * FT        # balcony-level arcade behind each balcony

# src/materials/gcs: stock HL2 textures tinted to colours sampled from refs/photos.
TEX_FLOOR = "gcs/floor"
TEX_WALL = "gcs/wall"
TEX_VAULT = "gcs/vault"
TEX_TRIM = "gcs/trim"
TEX_GLOW = "gcs/window_glow"
TEX_GOLD = "gcs/gold"
TEX_GRID = "gcs/mullion"
TEX_DIM = "gcs/window_dim"
TEX_GLASS = "gcs/window_glass"  # pale pane grid for the big windows
TEX_CREAM = "gcs/cream"
TEX_CLOCK = "gcs/clock"
TEX_BULB = "gcs/bulb"
TEX_COFFER = "gcs/coffer"
TEX_DOOR = "gcs/door_glow"
TEX_SHAFT = "gcs/shaft"        # additive sun beam, nonsolid
NODRAW = "tools/toolsnodraw"

_id = [0]


def nid():
    _id[0] += 1
    return _id[0]


def sub(a, b): return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def dot(a, b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]


# Texture scale per material (default 0.25); smaller floor tiles read closer to the photos.
SCALE = {TEX_FLOOR: 0.1875,   # 512 px texture = 2x2 slabs of 4 ft
         TEX_WALL: 0.5,        # 8 courses x 4 blocks over 21 ft: 2.7 x 5.3 ft blocks
         TEX_COFFER: 0.375,    # 2x2 coffers over 16 ft
         TEX_CLOCK: 30/256}    # one 256 px dial per 30 u clock side
USHIFT = {TEX_CLOCK: 128}      # centre the dial on faces spanning -15..15

# Departure board over the ticket windows (faces +y) and the flag hung from the crown
# (faces +-x); both map their texture once over the front faces, the rest gets black/gold.
BOARD = (-20*FT, 20*FT, 17*FT, 27*FT)         # x0, x1, z0, z1: 40 x 10 ft, inside the centre bay
FLAG = (-24*FT, 24*FT, HY - 8*FT, HY - 8*FT + 2, SPRING - 33*FT, SPRING - 8*FT)   # x0, x1, y0, y1 (thin), z0, z1: north centre bay; 48 ft long (Gothamist), 1.9:1


def _board_uv(n):
    x0, x1, z0, z1 = BOARD
    su, sv = (x1-x0)/1024, (z1-z0)/256
    if n[1] > 0.5:
        return "[-1 0 0 %g] %g" % (x1/su, su), "[0 0 -1 %g] %g" % (z1/sv, sv)


def _flag_uv(n):
    x0, x1, _, _, z0, z1 = FLAG
    su, sv = (x1-x0)/512, (z1-z0)/256
    if abs(n[1]) > 0.5:
        s = -1 if n[1] > 0 else 1
        return "[%d 0 0 %g] %g" % (s, -s*(x0 if s > 0 else x1)/su, su), "[0 0 -1 %g] %g" % (z1/sv, sv)


def _tickets_uv(n):
    # One 1024 px strip per 16 ft window pitch; plaque centre (window x + 3 ft) lands on texel 512.
    su, sv = 16*FT/1024, 1.5*FT/64
    if n[1] > 0.5:
        return "[-1 0 0 704] %g" % su, "[0 0 -1 %g] %g" % (13.25*FT/sv, sv)


def _oysterbar_uv(n):
    # OYSTER BAR band over the gallery's west opening, y -120..120, faces +x.
    su, sv = 240/1024, 20/64
    if n[0] > 0.5:
        return "[0 1 0 %g] %g" % (120/su, su), "[0 0 -1 %g] %g" % ((LOW_Z + 120)/sv, sv)


FACEUV = {"gcs/facade_win": lambda n: ("[1 0 0 0] 0.375", "[0 0 -1 0] 0.5625"), "gcs/inscription": lambda n: _ext_uv(n, "ins"), "gcs/clock_out": lambda n: _ext_uv(n, "clock"),
          "gcs/oysterbar": _oysterbar_uv, "gcs/board": _board_uv, "gcs/flag": _flag_uv, "gcs/tickets": _tickets_uv}


def axes_for(n, s=0.25):
    ax = max(range(3), key=lambda i: abs(n[i]))
    if ax == 2:
        return "[1 0 0 0] %g" % s, "[0 -1 0 0] %g" % s
    if ax == 0:
        return "[0 1 0 0] %g" % s, "[0 0 -1 0] %g" % s
    return "[1 0 0 0] %g" % s, "[0 0 -1 0] %g" % s


def side(pts, n, tex, uv=None):
    p1, p2, p3 = pts[0], pts[1], pts[2]
    # Source plane winding: outward normal = (p3-p1) x (p2-p1)
    if dot(cross(sub(p3, p1), sub(p2, p1)), n) < 0:
        p2, p3 = p3, p2
    f = lambda p: "(%g %g %g)" % p
    uv = uv or (FACEUV[tex](n) if tex in FACEUV else None)
    u, v = uv or axes_for(n, SCALE.get(tex, 0.25))
    if not uv and tex == TEX_CLOCK and abs(n[2]) < 0.5 and n[0] - n[1] < 0:
        u = u.replace("[0 1 0", "[0 -1 0").replace("[1 0 0", "[-1 0 0")   # unmirror -x and +y dials
    if not uv and tex in USHIFT:
        u = u.replace(" 0] ", " %g] " % USHIFT[tex])
    return ('\tside\n\t{\n\t\t"id" "%d"\n\t\t"plane" "%s %s %s"\n\t\t"material" "%s"\n'
            '\t\t"uaxis" "%s"\n\t\t"vaxis" "%s"\n\t\t"rotation" "0"\n\t\t"lightmapscale" "16"\n'
            '\t\t"smoothing_groups" "0"\n\t}\n') % (nid(), f(p1), f(p2), f(p3), tex, u, v)


def prism(poly, z0, z1, tex, caps=None):
    """Convex polygon in xy (counter-clockwise), extruded z0..z1."""
    caps = caps or tex
    s = side([(x, y, z1) for x, y in poly], (0, 0, 1), caps)
    s += side([(x, y, z0) for x, y in poly], (0, 0, -1), caps)
    for i in range(len(poly)):
        a, b = poly[i], poly[(i+1) % len(poly)]
        n = (b[1]-a[1], -(b[0]-a[0]), 0)
        s += side([(a[0], a[1], z0), (b[0], b[1], z0), (b[0], b[1], z1)], n, tex)
    return "solid\n{\n\t\"id\" \"%d\"\n%s}\n" % (nid(), s)


def xprism(poly, x0, x1, tex, uvs=None):
    """Convex polygon in yz (counter-clockwise seen from +x), extruded x0..x1.
    uvs: optional {edge index: (uaxis, vaxis)} for the face on that edge."""
    s = side([(x1, y, z) for y, z in poly], (1, 0, 0), tex)
    s += side([(x0, y, z) for y, z in poly], (-1, 0, 0), tex)
    for i in range(len(poly)):
        a, b = poly[i], poly[(i+1) % len(poly)]
        n = (0, b[1]-a[1], -(b[0]-a[0]))
        s += side([(x0, a[0], a[1]), (x0, b[0], b[1]), (x1, b[0], b[1])], n, tex, (uvs or {}).get(i))
    return "solid\n{\n\t\"id\" \"%d\"\n%s}\n" % (nid(), s)


def yprism(poly, y0, y1, tex, uv=None, ends=None):
    """Convex polygon in xz (counter-clockwise seen from -y), extruded y0..y1.
    uv: one (u, v) for every face; ends: material for the two y faces (default tex)."""
    s = side([(x, y0, z) for x, z in poly], (0, -1, 0), ends or tex, uv)
    s += side([(x, y1, z) for x, z in poly], (0, 1, 0), ends or tex, uv)
    for i in range(len(poly)):
        a, b = poly[i], poly[(i+1) % len(poly)]
        n = (b[1]-a[1], 0, -(b[0]-a[0]))
        s += side([(a[0], y0, a[1]), (b[0], y0, b[1]), (b[0], y1, b[1])], n, tex, uv)
    return "solid\n{\n\t\"id\" \"%d\"\n%s}\n" % (nid(), s)


def halfdisc(cx, z0, r, n=10):
    return [(round(cx + r*math.cos(math.pi*i/n)), round(z0 + r*math.sin(math.pi*i/n))) for i in range(n+1)]


def ccw(poly):
    a = sum(poly[i][0]*poly[(i+1) % len(poly)][1] - poly[(i+1) % len(poly)][0]*poly[i][1] for i in range(len(poly)))
    return poly if a > 0 else poly[::-1]


def box(x0, y0, z0, x1, y1, z1, tex):
    return prism([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], z0, z1, tex)


def ngon(cx, cy, r, n, rot=0.0):
    return [(round(cx + r*math.cos(rot + 2*math.pi*i/n)), round(cy + r*math.sin(rot + 2*math.pi*i/n))) for i in range(n)]


def ent(cls, origin=None, solids="", **kv):
    kv = {"classname": cls, **kv}
    if origin:
        kv["origin"] = "%g %g %g" % origin
    body = "".join('\t"%s" "%s"\n' % (k, v) for k, v in kv.items())
    return "entity\n{\n\t\"id\" \"%d\"\n%s%s}\n" % (nid(), body, solids)



def arcade_bay(W, ents, sgn, xin, xout, c, z0, r, top, roof, ramp=False):
    """One arched opening in an end wall (z0..top, half-width r) and its lit passage.
    ramp: the opening leads to a ramp down to the dining concourse (lower_level builds it)."""
    xa, xb = sorted((xin, xout))
    arc = halfdisc(c, top - r, r, 8)
    for i in range(8):
        corner = (c + r, top) if i < 4 else (c - r, top)
        ents.append(ent("func_detail", solids=xprism(ccw([corner, arc[i], arc[i+1]]), xa, xb, TEX_WALL)))
    # Cream archivolt proud of the wall, on cream jambs.
    fa, fb = sorted((xin, xin - sgn*8))
    outer, inner = halfdisc(c, top - r, r + 18), halfdisc(c, top - r, r)
    for i in range(len(outer)-1):
        ents.append(ent("func_detail", solids=xprism(ccw([outer[i], outer[i+1], inner[i+1], inner[i]]), fa, fb, TEX_CREAM)))
    for y0 in (c - r - 18, c + r):
        ents.append(ent("func_detail", solids=box(fa, y0, z0, fb, y0 + 18, top - r, TEX_CREAM)))
    if ramp:
        return
    # Passage behind, sealed: warm cream corridor ending in lit glass doors with brass frames.
    pa, pb = sorted((xout, xout + sgn*ARCH_D))
    W(box(pa, c - r - WALL, z0 - WALL, pb, c + r + WALL, z0, TEX_FLOOR))
    W(box(pa, c - r - WALL, top, pb, c + r + WALL, top + roof, TEX_CREAM))
    W(box(pa, c - r - WALL, z0, pb, c - r, top, TEX_CREAM))
    W(box(pa, c + r, z0, pb, c + r + WALL, top, TEX_CREAM))
    # Cream barrel vault over the passage, continuing the opening's arch.
    for i in range(8):
        corner = (c + r, top) if i < 4 else (c - r, top)
        ents.append(ent("func_detail", solids=xprism(ccw([corner, arc[i], arc[i+1]]), pa, pb, TEX_CREAM)))
    xback = xout + sgn*ARCH_D
    ba, bb = sorted((xback, xback + sgn*WALL))
    W(box(ba, c - r - WALL, z0 - WALL, bb, c + r + WALL, top + WALL, TEX_DOOR))
    # Brass door frames: posts, transom bar and a header panel over the doors.
    fa2, fb2 = sorted((xback, xback - sgn*6))
    for yy in (c - r, c - 3*FT, c + 3*FT - 6, c + r - 6, c - 6, c):
        ents.append(ent("func_detail", solids=box(fa2, yy, z0, fb2, yy + 6, top, TEX_GRID)))
    ents.append(ent("func_detail", solids=box(fa2, c - r, z0 + 8*FT, fb2, c + r, z0 + 8*FT + 6, TEX_GRID)))
    ents.append(ent("func_detail", solids=box(fa2, c - r, z0 + 12*FT, fb2, c + r, top, TEX_CREAM)))
    # Pendant lamp.
    lx = sgn*(HX + WALL + ARCH_D//2)
    ents.append(ent("func_detail", solids=box(lx - 1, c - 1, top - 30, lx + 1, c + 1, top, TEX_GOLD)))
    ents.append(ent("func_detail", solids=box(lx - 8, c - 8, top - 44, lx + 8, c + 8, top - 30, TEX_BULB)))
    ents.append(ent("light", (lx, c, top - 60), _light="255 205 140 40"))
    ents.append(ent("light", (xback - sgn*24, c, z0 + 6*FT), _light="255 190 120 20"))


# Lower level (area 2). The Oyster Bar ramps flank the west staircase, run west under the
# balcony through the side arches and land at the Whispering Gallery; the Oyster Bar opens
# off its west side, and a corridor runs back east to the dining concourse under the floor.
LOW_Z = -22 * FT                    # dining level floor
RAMP_X0, RAMP_XF = -1100, -2684     # ramp head in the concourse floor, ramp foot (slope ~1:6)
RAMP_Y0, RAMP_Y1 = 300, 480         # ramp well, |y|; inside the side arches (264..480)
COR_Y = 168                         # half-width of the corridor between the ramps
GAL_X0 = RAMP_XF - 50 * FT          # Whispering Gallery, 50 ft square
OB_X1 = GAL_X0 - WALL
OB_X0 = OB_X1 - 4 * 288             # Oyster Bar, four 24 ft bays by four
DIN_X0, DIN_X1, DIN_Y = -1000, 1000, 600   # dining concourse under the main floor
EAST_D = 40 * FT                    # east ramp landing hall depth
TEX_TILE = "gcs/guastavino"
TEX_WOOD = "gcs/wood"
TEX_PALE = "gcs/guastavino_pale"   # Whispering Gallery glaze
TEX_LOWF = "gcs/floor_low"         # darker mauve-grey tile floor of the lower level


def groin(W, x0, x1, y0, y1, zs, rise, tex, n=8):
    """Groin vault over x0..x1, y0..y1 springing at zs: the solid is the intersection of two
    crossing barrels' solids, so the plan splits along the diagonals into four triangles and
    each triangle follows the barrel whose arch stands on its wall. n even. World brushes."""
    top = zs + rise + 16
    yc, hy, xc, hx = (y0+y1)/2, (y1-y0)/2, (x0+x1)/2, (x1-x0)/2
    a = [math.pi*i/n for i in range(n+1)]
    for axis in (0, 1):                      # 0: triangles on the x walls, profile across y
        c, h, oc, oh = (yc, hy, xc, hx) if axis == 0 else (xc, hx, yc, hy)
        prof = [(c + h*math.cos(t), zs + rise*math.sin(t)) for t in a]
        for sgn in (-1, 1):                  # wall at oc + sgn*oh
            for i in range(n):
                (u0, z0), (u1, z1) = prof[i], prof[i+1]
                # Diagonal: |v - oc|/oh = |u - c|/h; the strip runs from the wall to it.
                d0, d1 = oh*abs(u0 - c)/h, oh*abs(u1 - c)/h
                uv = [(u0, oc + sgn*oh), (u1, oc + sgn*oh), (u1, oc + sgn*d1), (u0, oc + sgn*d0)]
                if abs(d0 - oh) < 1e-6:
                    uv.pop(3)
                elif abs(d1 - oh) < 1e-6:
                    uv.pop(2)
                poly =ccw([(v, u) for u, v in uv]) if axis == 0 else ccw(list(uv))
                s = (z1 - z0) / (u1 - u0)
                zf = (lambda x, y, u0=u0, z0=z0, s=s: z0 + s*((y if axis == 0 else x) - u0))
                nb = (0, s, -1) if axis == 0 else (s, 0, -1)
                W(_slab(poly, zf, nb, top, tex))
    W(box(x0, y0, top, x1, y1, top + WALL, tex))


def _slab(poly, zf, nb, top, tex):
    """Convex xy polygon (ccw) from the plane z = zf(x, y) (outward normal nb) up to top."""
    r = lambda v: round(v, 2)
    s = side([(r(x), r(y), top) for x, y in poly], (0, 0, 1), tex)
    s += side([(r(x), r(y), r(zf(x, y))) for x, y in poly], nb, tex)
    for i in range(len(poly)):
        a, b = poly[i], poly[(i+1) % len(poly)]
        n = (b[1]-a[1], -(b[0]-a[0]), 0)
        s += side([(r(a[0]), r(a[1]), r(zf(*a))), (r(b[0]), r(b[1]), r(zf(*b))), (r(b[0]), r(b[1]), top)], n, tex)
    return "solid\n{\n\t\"id\" \"%d\"\n%s}\n" % (nid(), s)


def lower_level(W, ents):
    det = lambda s: ents.append(ent("func_detail", solids=s))
    Z, H = LOW_Z, 216
    # Ramps, one each side: a sloped floor slab, walls, rails round the well in the
    # concourse, and past the end wall a sloping Guastavino-tiled soffit.
    for e, s in ((e, s) for e in (1, -1) for s in (-1, 1)):   # e=-1 mirrors to the east end
        X = lambda x: e*x
        B = lambda x0, y0, z0, x1, y1, z1, t: box(min(X(x0), X(x1)), y0, z0, max(X(x0), X(x1)), y1, z1, t)
        P = lambda poly: ccw([(X(x), z) for x, z in poly])
        ya, yb = sorted((s*RAMP_Y0, s*RAMP_Y1))
        W(yprism(P([(RAMP_X0, 0), (RAMP_XF, Z), (RAMP_XF, Z - WALL), (RAMP_X0, -WALL)]), ya, yb, TEX_FLOOR))
        ia, ib = sorted((s*COR_Y, s*RAMP_Y0))
        oa, ob = sorted((s*RAMP_Y1, s*(RAMP_Y1 + WALL)))
        for wa, wb in ((ia, ib), (oa, ob)):
            W(B(-HX, wa, Z - WALL, RAMP_X0, wb, 0, TEX_CREAM))
            W(B(RAMP_XF, wa, Z - WALL, -HX, wb, ARCH_TOP, TEX_CREAM))
        x1 = -HX - WALL
        W(yprism(P([(x1, ARCH_TOP), (RAMP_XF, Z + H), (RAMP_XF, Z + H + WALL), (x1, ARCH_TOP + WALL)]), ya, yb, TEX_TILE))
        # Cream parapets with brass rails on the floor round the well.
        for ra, rb in (sorted((s*(RAMP_Y0 - 16), s*RAMP_Y0)), sorted((s*RAMP_Y1, s*(RAMP_Y1 + 16)))):
            det(B(-HX, ra, 0, RAMP_X0, rb, 42, TEX_CREAM))
            det(B(-HX, ra - 2, 42, RAMP_X0, rb + 2, 46, TEX_GOLD))
        det(B(RAMP_X0, ya, 0, RAMP_X0 + 16, yb, 42, TEX_CREAM))
        det(B(RAMP_X0 - 2, ya, 42, RAMP_X0 + 18, yb, 46, TEX_GOLD))
        for k in range(4):
            x = round(-HX - WALL - 100 - k*(-HX - WALL - 100 - RAMP_XF)/3.5)
            t = (x - RAMP_X0) / (RAMP_XF - RAMP_X0)
            ents.append(ent("light", (X(x), s*(RAMP_Y0+RAMP_Y1)//2, Z*t + 150), _light="255 205 150 30"))
    # East ramp foot: a cream landing hall (EAST_D deep) with a flat coffered ceiling; its
    # west side opens on a corridor back to the dining concourse, as the west ramps do.
    ex0, ex1, ey = -RAMP_XF, -RAMP_XF + EAST_D, RAMP_Y1
    W(box(ex0, -ey, Z - WALL, ex1, ey, Z, TEX_LOWF))
    W(box(ex0, -ey, Z + H, ex1, ey, Z + H + WALL, TEX_COFFER))
    W(box(ex1, -ey, Z - WALL, ex1 + WALL, ey, Z + H + WALL, TEX_CREAM))
    for s in (-1, 1):
        ya, yb = sorted((s*ey, s*(ey + WALL)))
        W(box(ex0, ya, Z - WALL, ex1 + WALL, yb, Z + H + WALL, TEX_CREAM))
        # Wall between ramp foot and corridor, up to the landing ceiling.
        wa, wb = sorted((s*COR_Y, s*RAMP_Y0))
        W(box(ex0 - WALL, wa, Z + H - 8, ex0, wb, Z + H + WALL, TEX_CREAM))
    W(box(ex0 - WALL, -COR_Y, Z + H - 8, ex0, COR_Y, Z + H + WALL, TEX_CREAM))
    # Brass-framed lit doors to the platforms (sealed until area 4) on the landing's east wall.
    for c in (-200, 0, 200):
        det(box(ex1 - 6, c - 60, Z, ex1, c + 60, Z + 132, TEX_GRID))
        det(box(ex1 - 8, c - 52, Z, ex1 - 6, c + 52, Z + 124, TEX_DOOR))
    for y in (-240, 0, 240):
        det(box(ex0 + EAST_D//2 - 8, y - 8, Z + H - 30, ex0 + EAST_D//2 + 8, y + 8, Z + H - 14, TEX_BULB))
        ents.append(ent("light", (ex0 + EAST_D//2, y, Z + H - 60), _light="255 210 160 40"))
    ents.append(ent("env_cubemap", (ex0 + EAST_D//2, 0, Z + 72)))
    W(box(DIN_X1 + WALL, -COR_Y, Z - WALL, ex0, COR_Y, Z, TEX_LOWF))
    W(box(DIN_X1 + WALL, -COR_Y, -WALL - 16, ex0 - WALL, COR_Y, 0, TEX_CREAM))
    for s in (-1, 1):
        wa, wb = sorted((s*COR_Y, s*RAMP_Y0))
        W(box(DIN_X1 + WALL, wa, Z - WALL, HX, wb, -WALL, TEX_CREAM))
    for x in range(DIN_X1 + 160, ex0, 320):
        ents.append(ent("light", (x, 0, -110), _light="255 210 160 25"))
    # Corridor between the ramps from the gallery east to the dining concourse.
    W(box(RAMP_XF, -COR_Y, Z - WALL, DIN_X0, COR_Y, Z, TEX_LOWF))
    W(box(RAMP_XF, -COR_Y, -WALL - 16, DIN_X0, COR_Y, 0, TEX_CREAM))
    for s in (-1, 1):
        wa, wb = sorted((s*COR_Y, s*RAMP_Y0))
        W(box(-HX, wa, Z - WALL, DIN_X0, wb, -WALL, TEX_CREAM))
    for x in range(RAMP_XF + 160, DIN_X0, 320):
        ents.append(ent("light", (x, 0, -110), _light="255 210 160 25"))

    # Whispering Gallery: a low groin vault of pale Guastavino tile where four arches meet,
    # each opening framed by a cream stone arch, brass handrails along the walls.
    gx0, gx1, gy = GAL_X0, RAMP_XF, RAMP_Y1
    W(box(gx0, -gy, Z - WALL, gx1, gy, Z, TEX_LOWF))
    for s in (-1, 1):
        ya, yb = sorted((s*gy, s*(gy + WALL)))
        W(box(gx0 - WALL, ya, Z - WALL, gx1, yb, 64, TEX_PALE))
    for y0, y1 in ((-gy, -120), (120, gy)):
        W(box(gx0 - WALL, y0, Z, gx0, y1, 64, TEX_PALE))
    W(box(gx0 - WALL, -120, Z + 120, gx0, 120, 64, TEX_PALE))
    zs, rise = Z + 10*FT, 9*FT
    groin(W, gx0, gx1, -gy, gy, zs, rise, TEX_PALE)
    # Cream stone ribs: a band of the arch profile 16 u deep along each wall face.
    gxc = (gx0 + gx1) / 2
    hx = (gx1 - gx0) / 2
    n = 8
    for x in (gx0 + 12, gx1 - 12):
        for i in range(n):
            t0, t1 = math.pi*i/n, math.pi*(i+1)/n
            a = (round(gy*math.cos(t0)), round(zs + rise*math.sin(t0)))
            b = (round(gy*math.cos(t1)), round(zs + rise*math.sin(t1)))
            a2 = (round((gy-30)*math.cos(t0)), round(zs + (rise-30)*math.sin(t0)))
            b2 = (round((gy-30)*math.cos(t1)), round(zs + (rise-30)*math.sin(t1)))
            det(xprism(ccw([a2, b2, b, a]), x - 12, x + 12, TEX_CREAM))
    for y in (-gy + 12, gy - 12):
        for i in range(n):
            t0, t1 = math.pi*i/n, math.pi*(i+1)/n
            a = (round(gxc + hx*math.cos(t0)), round(zs + rise*math.sin(t0)))
            b = (round(gxc + hx*math.cos(t1)), round(zs + rise*math.sin(t1)))
            a2 = (round(gxc + (hx-30)*math.cos(t0)), round(zs + (rise-30)*math.sin(t0)))
            b2 = (round(gxc + (hx-30)*math.cos(t1)), round(zs + (rise-30)*math.sin(t1)))
            det(yprism(ccw([a2, b2, b, a]), y - 12, y + 12, TEX_CREAM))
    # Cream piers in the four corners carry the ribs down to the floor.
    for x in (gx0, gx1 - 28):
        for y in (-gy, gy - 28):
            det(box(x, y, Z, x + 28, y + 28, zs, TEX_CREAM))
    # Brass handrail on short posts along the solid walls (y = +-gy) between the piers.
    for s in (-1, 1):
        y = s*(gy - 6)
        det(box(gx0 + 40, y - 2, Z + 34, gx1 - 40, y + 2, Z + 37, TEX_GOLD))
        for x in range(gx0 + 60, gx1 - 40, 96):
            det(box(x - 1, y - 1, Z + 4, x + 1, y + 1, Z + 34, TEX_GOLD))
    # One lamp at the crown and warm fill under each arch.
    det(box(gxc - 1, -1, zs + rise - 40, gxc + 1, 1, zs + rise + 2, TEX_GOLD))
    det(prism(ngon(gxc, 0, 10, 8, math.pi/8), zs + rise - 58, zs + rise - 40, TEX_BULB))
    ents.append(ent("light", (round(gxc), 0, zs + rise - 76), _light="255 210 165 70"))
    for x, y in ((gxc, gy - 120), (gxc, -gy + 120), (gx0 + 120, 0), (gx1 - 120, 0)):
        ents.append(ent("light", (round(x), y, Z + 90), _light="255 215 175 25"))
    ents.append(ent("env_cubemap", (round(gxc), 0, Z + 72)))
    # Oyster Bar entrance: bronze OYSTER BAR band in the head of the opening (the vault springs just above), oak door frames with a
    # transom bar and side lights, the doors themselves left open.
    det(box(gx0 - 8, -120, Z + 100, gx0 + 3, 120, Z + 120, "gcs/oysterbar"))
    det(box(gx0 - 8, -124, Z + 97, gx0 + 5, 124, Z + 100, TEX_GOLD))
    for y0 in (-120, 104, -84, 76):
        det(box(gx0 - WALL, y0, Z, gx0 + 2, y0 + (16 if abs(y0) > 100 else 8), Z + 120, TEX_WOOD))
    det(box(gx0 - WALL, -120, Z + 92, gx0 + 2, 120, Z + 100, TEX_WOOD))
    for ya, yb in ((-104, -84), (84, 104)):
        det(box(gx0 - 34, ya, Z, gx0 - 30, yb, Z + 92, TEX_DOOR))

    # Oyster Bar: 4 x 4 bays of shallow Guastavino groins on piers; a long oak counter.
    bx, by = 288, 240
    oy = 2*by
    W(box(OB_X0, -oy, Z - WALL, OB_X1, oy, Z, TEX_LOWF))
    for s in (-1, 1):
        ya, yb = sorted((s*oy, s*(oy + WALL)))
        W(box(OB_X0 - WALL, ya, Z - WALL, OB_X1, yb, 64, TEX_CREAM))
    W(box(OB_X0 - WALL, -oy, Z - WALL, OB_X0, oy, 64, TEX_CREAM))
    zs = Z + 11*FT
    for i in range(4):
        for j in range(4):
            x0, y0 = OB_X0 + i*bx, -oy + j*by
            groin(W, x0, x0 + bx, y0, y0 + by, zs, 6*FT, TEX_TILE)
            ents.append(ent("light", (x0 + bx//2, y0 + by//2, zs - 40), _light="255 195 130 45"))
            det(box(x0 + bx//2 - 1, y0 + by//2 - 1, zs - 10, x0 + bx//2 + 1, y0 + by//2 + 1, zs + 70, TEX_GOLD))
            det(prism(ngon(x0 + bx//2, y0 + by//2, 8, 8, math.pi/8), zs - 22, zs - 10, TEX_BULB))
    for i in range(1, 4):
        for j in range(1, 4):
            x, y = OB_X0 + i*bx, -oy + j*by
            det(box(x - 14, y - 14, Z, x + 14, y + 14, zs + 20, TEX_TILE))
    # Counter: oak top on a cream marble base, running down the middle with stools.
    cx0, cx1 = OB_X0 + 96, OB_X1 - 192
    det(box(cx0, -30, Z, cx1, 30, Z + 40, TEX_CREAM))
    det(box(cx0 - 6, -38, Z + 40, cx1 + 6, 38, Z + 43, TEX_WOOD))
    for x in range(cx0 + 24, cx1, 48):
        for y in (-56, 56):
            det(prism(ngon(x, y, 2, 6), Z, Z + 24, TEX_GOLD))
            det(prism(ngon(x, y, 8, 8, math.pi/8), Z + 24, Z + 28, TEX_WOOD))
    # Wall counters: oak-topped cream counters along both long walls, stools in front.
    for sg in (-1, 1):
        ya, yb = sorted((sg*oy, sg*(oy - 30)))
        det(box(OB_X0 + 48, ya, Z, OB_X1 - 96, yb, Z + 40, TEX_CREAM))
        ya, yb = sorted((sg*oy, sg*(oy - 38)))
        det(box(OB_X0 + 42, ya, Z + 40, OB_X1 - 90, yb, Z + 43, TEX_WOOD))
        for x in range(OB_X0 + 72, OB_X1 - 96, 48):
            y = sg*(oy - 58)
            det(prism(ngon(x, y, 2, 6), Z, Z + 24, TEX_GOLD))
            det(prism(ngon(x, y, 8, 8, math.pi/8), Z + 24, Z + 28, TEX_WOOD))
    ents.append(ent("env_cubemap", ((OB_X0+OB_X1)//2, -200, Z + 72)))

    # Dining concourse under the main floor: cream walls, pylons, lit shop fronts round
    # the edge and a small brass-topped lower information booth in the middle.
    W(box(DIN_X0, -DIN_Y, Z - WALL, DIN_X1, DIN_Y, Z, TEX_FLOOR))
    W(box(DIN_X0, -DIN_Y, -WALL - 16, DIN_X1, DIN_Y, -WALL, TEX_COFFER))
    for s in (-1, 1):
        ya, yb = sorted((s*DIN_Y, s*(DIN_Y + WALL)))
        W(box(DIN_X0 - WALL, ya, Z - WALL, DIN_X1 + WALL, yb, 0, TEX_CREAM))
    for y0, y1 in ((-DIN_Y, -COR_Y), (COR_Y, DIN_Y)):
        W(box(DIN_X1, y0, Z - WALL, DIN_X1 + WALL, y1, 0, TEX_CREAM))
    for y0, y1 in ((-DIN_Y, -COR_Y), (COR_Y, DIN_Y)):
        W(box(DIN_X0 - WALL, y0, Z - WALL, DIN_X0, y1, 0, TEX_CREAM))
    for x in range(DIN_X0 + 160, DIN_X1 - 100, 240):
        for s in (-1, 1):
            ya, yb = sorted((s*(DIN_Y - 4), s*DIN_Y))
            det(box(x - 90, ya, Z + 12, x + 90, yb, Z + 110, TEX_DOOR))
            det(box(x - 90, ya, Z + 120, x + 90, yb, Z + 140, TEX_GOLD))
        for y in (-320, 320):
            det(box(x - 16, y - 16, Z, x + 16, y + 16, -WALL - 16, TEX_CREAM))
        # Beams between the pylons; round brass lamps hung in the bays between them.
        det(box(x - 12, -DIN_Y, -WALL - 40, x + 12, DIN_Y, -WALL - 16, TEX_CREAM))
        for y in (-440, 0, 440):
            lx = x + 120
            if lx < DIN_X1 - 60:
                det(prism(ngon(lx, y, 18, 8, math.pi/8), -WALL - 30, -WALL - 16, TEX_GOLD))
                det(prism(ngon(lx, y, 14, 8, math.pi/8), -WALL - 38, -WALL - 30, TEX_BULB))
                ents.append(ent("light", (lx, y, -WALL - 60), _light="255 215 170 40"))
    for y in (-440, 0, 440):   # west end bay, so the first pylons are lit from both sides
        ents.append(ent("light", (DIN_X0 + 60, y, -WALL - 60), _light="255 215 170 30"))
    oct8 = lambda r: ngon(0, 0, r, 8, math.pi/8)
    det(prism(oct8(7*FT), Z, Z + 42, TEX_CREAM))
    det(prism(oct8(7*FT + 4), Z + 42, Z + 46, TEX_GOLD))
    det(prism(oct8(1*FT), Z + 46, Z + 90, TEX_GOLD))
    # Brass column with a four-faced opal clock, like the one upstairs.
    det(prism(oct8(10), Z + 46, -150, TEX_GOLD))
    det(prism([(-15, -15), (15, -15), (15, 15), (-15, 15)], -150, -120, TEX_CLOCK, TEX_GOLD))
    det(prism(oct8(20), -120, -116, TEX_GOLD))
    det(prism(oct8(10), -116, -104, TEX_GOLD))
    ents.append(ent("env_cubemap", (0, -300, Z + 72)))


# Vanderbilt Hall (area 3): the old main waiting room south of the concourse, reached
# through a passage in the west bay of the south wall. Flat gilded-cornice ceiling, ashlar
# walls, tall grilled windows, five tiered chandeliers; the 42nd Street vestibule opens
# off its south wall and ends in lit doors (sealed until the exterior, area 5).
VH_PX0, VH_PX1 = -115 * FT, -102 * FT     # passage through the concourse south wall
VH_PH = 16 * FT                           # passage height
VH_Y1 = -HY - WALL - 24 * FT              # hall's inner north face
VH_Y0 = VH_Y1 - 64 * FT                   # hall 200 x 64 ft (estimate)
VH_X0, VH_X1 = -130 * FT, 70 * FT
VH_H = 56 * FT
VS_X0, VS_X1, VS_D = -40 * FT, -20 * FT, 24 * FT   # 42nd Street vestibule


def vanderbilt(W, ents):
    # Decor goes into one func_brush: the world model is at vbsp's t-junction index cap (65536).
    decor = []
    det = decor.append
    # Hall shell.
    W(box(VH_X0, VH_Y0, -WALL, VH_X1, VH_Y1, 0, TEX_FLOOR))
    W(box(VH_X0, VH_Y0, VH_H, VH_X1, VH_Y1, VH_H + WALL, TEX_COFFER))
    W(box(VH_X0 - WALL, VH_Y0 - WALL, -WALL, VH_X0, VH_Y1 + WALL, VH_H + WALL, TEX_WALL))
    W(box(VH_X1, VH_Y0 - WALL, -WALL, VH_X1 + WALL, VH_Y1 + WALL, VH_H + WALL, TEX_WALL))
    for (y0, y1), (g0, g1, gh) in (((VH_Y1, VH_Y1 + WALL), (VH_PX0, VH_PX1, VH_PH)),
                                   ((VH_Y0 - WALL, VH_Y0), (VS_X0, VS_X1, 20 * FT))):
        W(box(VH_X0, y0, -WALL, g0, y1, VH_H, TEX_WALL))
        W(box(g1, y0, -WALL, VH_X1, y1, VH_H, TEX_WALL))
        W(box(g0, y0, gh, g1, y1, VH_H, TEX_WALL))
        W(box(g0, y0, -WALL, g1, y1, 0, TEX_FLOOR))
    # Passage from the concourse: cream walls and ceiling, a lamp.
    py0, py1 = VH_Y1 + WALL, -HY - WALL
    W(box(VH_PX0, py0, -WALL, VH_PX1, py1, 0, TEX_FLOOR))
    W(box(VH_PX0 - WALL, py0, -WALL, VH_PX0, py1, VH_PH + WALL, TEX_CREAM))
    W(box(VH_PX1, py0, -WALL, VH_PX1 + WALL, py1, VH_PH + WALL, TEX_CREAM))
    W(box(VH_PX0, py0, VH_PH, VH_PX1, py1, VH_PH + WALL, TEX_CREAM))
    pc = (VH_PX0 + VH_PX1) // 2
    ents.append(ent("light", (pc, (py0 + py1) // 2, VH_PH - 40), _light="255 210 150 30"))
    # Cream jambs, lintel and gold edge framing both ends of the passage.
    for ya, yb in ((-HY, -HY + 12), (VH_Y1 - 12, VH_Y1)):
        for x0, x1 in ((VH_PX0 - 24, VH_PX0), (VH_PX1, VH_PX1 + 24)):
            det(box(x0, ya, 0, x1, yb, VH_PH, TEX_CREAM))
        det(box(VH_PX0 - 24, ya, VH_PH, VH_PX1 + 24, yb, VH_PH + 24, TEX_CREAM))
        det(box(VH_PX0 - 24, ya, VH_PH + 24, VH_PX1 + 24, yb, VH_PH + 30, TEX_GOLD))
    # Vestibule to 42nd Street with lit brass doors.
    vy1, vy0 = VH_Y0 - WALL, VH_Y0 - WALL - VS_D
    W(box(VS_X0, vy0, -WALL, VS_X1, vy1, 0, TEX_FLOOR))
    W(box(VS_X0 - WALL, vy0 - WALL, -WALL, VS_X0, vy1, 20 * FT + WALL, TEX_CREAM))
    W(box(VS_X1, vy0 - WALL, -WALL, VS_X1 + WALL, vy1, 20 * FT + WALL, TEX_CREAM))
    W(box(VS_X0, vy0, 20 * FT, VS_X1, vy1, 20 * FT + WALL, TEX_CREAM))
    # The vestibule's south wall is the 42nd Street facade (exterior()); its three doorways stand open.
    dw = (VS_X1 - VS_X0) // 3
    for k in range(3):
        x0 = VS_X0 + k * dw
        det(box(x0, vy0, 0, x0 + 12, vy0 + 8, 13 * FT, TEX_GOLD))
    det(box(VS_X1 - 12, vy0, 0, VS_X1, vy0 + 8, 13 * FT, TEX_GOLD))
    det(box(VS_X0, vy0, 12 * FT, VS_X1, vy0 + 8, 13 * FT, TEX_GOLD))
    det(box(VS_X0 + 12, vy0, 13 * FT, VS_X1 - 12, vy0 + 4, 19 * FT, TEX_DOOR))
    ents.append(ent("light", ((VS_X0 + VS_X1) // 2, vy0 + 120, 16 * FT), _light="255 215 160 40"))
    # Tall dark-green grilled windows on both long walls (dark glass behind a green iron grid), cream sills.
    for yw, s in ((VH_Y1, -1), (VH_Y0, 1)):
        for cx in range(VH_X0 + 30 * FT, VH_X1 - 20 * FT + 1, 40 * FT):
            if VH_PX0 - 10 * FT < cx < VH_PX1 + 10 * FT or VS_X0 - 10 * FT < cx < VS_X1 + 10 * FT:
                continue
            wz0, wz1, hw = 14 * FT, 50 * FT, 8 * FT
            ga, gb = sorted((yw, yw + s * 2))
            det(box(cx - hw, ga, wz0, cx + hw, gb, wz1, "gcs/vh_glass"))
            ma, mb = sorted((yw + s * 2, yw + s * 6))
            for j in range(-4, 5):
                det(box(cx + j * 24 - 2, ma, wz0, cx + j * 24 + 2, mb, wz1, "gcs/vh_grille"))
            for z in range(wz0, wz1 + 1, 36):
                det(box(cx - hw, ma, z - 2, cx + hw, mb, z + 2, "gcs/vh_grille"))
            fa, fb = sorted((yw, yw + s * 10))
            for x0, x1 in ((cx - hw - 8, cx - hw), (cx + hw, cx + hw + 8)):
                det(box(x0, fa, wz0, x1, fb, wz1 + 8, "gcs/vh_grille"))
            det(box(cx - hw - 8, fa, wz1, cx + hw + 8, fb, wz1 + 8, "gcs/vh_grille"))
            sa, sb = sorted((yw, yw + s * 18))
            det(box(cx - hw - 12, sa, wz0 - 12, cx + hw + 12, sb, wz0, TEX_CREAM))
    # Gilded cornice and cream frieze round the ceiling; marble dado at the foot of the walls.
    for d, z0, z1, tex in ((48, VH_H - 30, VH_H, TEX_GOLD), (24, VH_H - 72, VH_H - 30, TEX_CREAM)):
        det(box(VH_X0, VH_Y1 - d, z0, VH_X1, VH_Y1, z1, tex))
        det(box(VH_X0, VH_Y0, z0, VH_X1, VH_Y0 + d, z1, tex))
        det(box(VH_X0, VH_Y0 + d, z0, VH_X0 + d, VH_Y1 - d, z1, tex))
        det(box(VH_X1 - d, VH_Y0 + d, z0, VH_X1, VH_Y1 - d, z1, tex))
    for x0, y0, x1, y1 in ((VH_X0, VH_Y1 - 6, VH_PX0 - 24, VH_Y1), (VH_PX1 + 24, VH_Y1 - 6, VH_X1, VH_Y1),
                           (VH_X0, VH_Y0, VS_X0, VH_Y0 + 6), (VS_X1, VH_Y0, VH_X1, VH_Y0 + 6),
                           (VH_X0, VH_Y0 + 6, VH_X0 + 6, VH_Y1 - 6), (VH_X1 - 6, VH_Y0 + 6, VH_X1, VH_Y1 - 6)):
        det(box(x0, y0, 0, x1, y1, 8 * FT, TEX_CREAM))
    # Each end wall carries a large moulded panel frame (cream, gold inner bead) above the door height.
    for xw, s in ((VH_X0, 1), (VH_X1, -1)):
        fa, fb = sorted((xw, xw + s * 6))
        ga, gb = sorted((xw, xw + s * 8))
        y0, y1, z0, z1 = VH_Y0 + 14 * FT, VH_Y1 - 14 * FT, 22 * FT, VH_H - 10 * FT
        for b in ((y0, z0, y0 + 10, z1), (y1 - 10, z0, y1, z1), (y0, z0, y1, z0 + 10), (y0, z1 - 10, y1, z1)):
            det(box(fa, b[0], b[1], fb, b[2], b[3], TEX_CREAM))
        for b in ((y0 + 10, z0 + 10, y0 + 12, z1 - 10), (y1 - 12, z0 + 10, y1 - 10, z1 - 10),
                  (y0 + 10, z0 + 10, y1 - 10, z0 + 12), (y0 + 10, z1 - 12, y1 - 10, z1 - 10)):
            det(box(ga, b[0], b[1], gb, b[2], b[3], TEX_GOLD))
    # East end: a doorway with a carved cream pediment, lit glass doors behind.
    ex, cy = VH_X1, (VH_Y0 + VH_Y1) // 2
    det(box(ex - 10, cy - 6 * FT, 0, ex - 6, cy + 6 * FT, 11 * FT, TEX_DOOR))
    for y0, y1 in ((cy - 8 * FT, cy - 6 * FT), (cy + 6 * FT, cy + 8 * FT)):
        det(box(ex - 24, y0, 0, ex - 6, y1, 13 * FT, TEX_CREAM))
    det(box(ex - 30, cy - 9 * FT, 13 * FT, ex - 6, cy + 9 * FT, 15 * FT, TEX_CREAM))
    det(box(ex - 36, cy - 9 * FT, 15 * FT, ex - 6, cy + 9 * FT, 15 * FT + 4, TEX_GOLD))
    det(xprism(ccw([(cy - 4 * FT, 15 * FT + 4), (cy + 4 * FT, 15 * FT + 4), (cy, 20 * FT)]), ex - 26, ex - 6, TEX_CREAM))
    # Five chandeliers down the centre: models/gcs/vh_chandelier.mdl from tools/make_models.py.
    for k in range(5):
        x = VH_X0 + (2 * k + 1) * (VH_X1 - VH_X0) // 10
        zc = VH_H - 30 * FT
        ents.append(ent("prop_static", (x, cy, zc), model="models/gcs/vh_chandelier.mdl", angles="0 0 0", solid="0", disableshadows="1", disablevertexlighting="0"))
        ents.append(ent("light", (x, cy, zc - 90), _light="255 220 170 45"))
    ents.append(ent("light", ((VH_X0 + VH_X1) // 2, cy, VH_H - 60), _light="255 225 180 15"))
    ents.append(ent("env_cubemap", ((VH_X0 + VH_X1) // 2, cy, 160)))
    ents.append(ent("env_cubemap", (pc, (py0 + py1) // 2, 100)))
    ents.append(ent("func_brush", solids="".join(decor), targetname="vh_decor", Solidity="2",
                    disableshadows="1", vrad_brush_cast_shadows="1"))


# The exterior (area 5): the 42nd Street facade through the Vanderbilt vestibule doors
# (photo: 42nd_Street_Facade_Grand_Central_Terminal_October_2025). Three great arched windows
# between paired columns, oval windows over the narrow bays, entablature, attic with the
# GRAND CENTRAL TERMINAL inscription, the Tiffany clock under the Glory of Commerce group
# (Mercury, Hercules, Minerva) on top; a balustraded terrace with a stair at the east end;
# the Park Avenue Viaduct crossing 42nd Street at the west end; office towers round the
# street and the MetLife tower behind; sky above (toolsskybox, light_environment).
VEST_Y0 = VH_Y0 - WALL - VS_D               # vestibule inner south face
YF = VEST_Y0 - WALL                         # facade face (faces -y)
FCX = (VS_X0 + VS_X1) // 2                  # facade axis = vestibule axis = hall centre
FHW = 160 * FT                              # facade half-width (estimate)
FX0, FX1 = FCX - FHW, FCX + FHW
RZ = 134 * FT                               # attic top / roof
SKYZ = 320 * FT
SW = 30 * FT                                # sidewalk depth
YS = YF - 110 * FT                          # face of the towers across 42nd Street
EX0, EX1 = FCX - 230 * FT, FCX + 230 * FT   # street ends
RN = 120 * FT                               # roof behind the facade, north of YF
TER_Z, TER_D = 24 * FT, 10 * FT             # terrace top and depth
WIN = (-80 * FT, 0, 80 * FT)                # great windows (x offsets), 33 ft wide
WIN_HW, WIN_Z0 = 198, 28 * FT
WIN_SP = WIN_Z0 + 60 * FT - WIN_HW          # arch springline: windows 60 ft tall
PAIRS = (-116 * FT, -40 * FT, 40 * FT, 116 * FT)
VIA_X0, VIA_X1 = FX0, FX0 + 34 * FT         # Park Avenue Viaduct deck
CLK_R, CLK_Z = 78, RZ + 15 * FT             # 13 ft clock


def _ext_uv(n, which):
    if n[1] > -0.5:
        return None
    if which == "ins":
        x0, x1, z1, w, h = FCX - 40 * FT, FCX + 40 * FT, 120 * FT, 1024, 128
        su, sv = (x1 - x0) / w, 10 * FT / h
    else:
        x0, z1, su = FCX - CLK_R, CLK_Z + CLK_R, 2 * CLK_R / 512
        sv = su
    return "[1 0 0 %g] %g" % (-x0 / su, su), "[0 0 -1 %g] %g" % (z1 / sv, sv)


def _arch_ring(cx, zs, r0, r1, y0, y1, tex, n=12):
    out = []
    for i in range(n):
        a, b = math.pi * i / n, math.pi * (i + 1) / n
        q = [(cx + r1 * math.cos(a), zs + r1 * math.sin(a)), (cx + r1 * math.cos(b), zs + r1 * math.sin(b)),
             (cx + r0 * math.cos(b), zs + r0 * math.sin(b)), (cx + r0 * math.cos(a), zs + r0 * math.sin(a))]
        out.append(yprism(ccw([(round(x), round(z)) for x, z in q]), y0, y1, tex))
    return out


def exterior(W, ents):
    decor = []
    det = decor.append
    STONE, GRILLE, GLASS, WINTEX = "gcs/facade_stone", "gcs/vh_grille", "gcs/vh_glass", "gcs/facade_win"
    # Facade wall with the vestibule doorway; roof slab behind the attic.
    W(box(FX0, YF, -WALL, VS_X0, VEST_Y0, RZ - WALL, STONE))
    W(box(VS_X1, YF, -WALL, FX1, VEST_Y0, RZ - WALL, STONE))
    W(box(VS_X0, YF, 20 * FT, VS_X1, VEST_Y0, RZ - WALL, STONE))
    W(box(VS_X0, YF, -WALL, VS_X1, VEST_Y0, 0, TEX_FLOOR))
    W(box(FX0, YF, RZ - WALL, FX1, YF + RN, RZ, STONE))
    W(box(FX0, YF + RN, RZ - WALL, FX1, YF + RN + WALL, SKYZ, "tools/toolsskybox"))
    # Street: sidewalks either side of the roadway, a double yellow centre line.
    W(box(EX0, YF - SW, -WALL, EX1, YF, 0, "gcs/sidewalk"))
    W(box(EX0, YS, -WALL, EX1, YS + 20 * FT, 0, "gcs/sidewalk"))
    W(box(EX0, YS + 20 * FT, -WALL, EX1, YF - SW, -8, "gcs/asphalt"))
    ym = (YS + 20 * FT + YF - SW) // 2
    for y in (ym - 8, ym + 4):
        det(box(EX0, y, -8, EX1, y + 4, -7, "gcs/plat_edge"))
    # Towers: across the street (glass, pale precast, glass), at both street ends, beside the terminal.
    for x0, x1, tex in ((EX0, FCX - 70 * FT, "gcs/office"), (FCX - 70 * FT, FCX + 60 * FT, "gcs/metlife"),
                        (FCX + 60 * FT, EX1, "gcs/office")):
        W(box(x0, YS - WALL, -WALL, x1, YS, SKYZ, tex))
    W(box(EX0 - WALL, YS - WALL, -WALL, EX0, YF + RN + WALL, SKYZ, "gcs/office"))
    W(box(EX1, YS - WALL, -WALL, EX1 + WALL, YF + RN + WALL, SKYZ, "gcs/office"))
    W(box(EX0, YF, -WALL, FX0, YF + RN + WALL, SKYZ, "gcs/office"))
    W(box(FX1, YF, -WALL, EX1, YF + RN + WALL, SKYZ, "gcs/metlife"))
    W(box(EX0 - WALL, YS - WALL, SKYZ, EX1 + WALL, YF + RN + WALL, SKYZ + WALL, "tools/toolsskybox"))
    W(box(FCX - 100 * FT, YF + 60 * FT, RZ, FCX + 100 * FT, YF + 110 * FT, SKYZ, "gcs/metlife"))   # MetLife
    # Terrace along the facade at the windows' foot, with a stair down to the sidewalk at the east end.
    W(box(FX0, YF - TER_D, TER_Z - 2 * FT, FX1, YF, TER_Z, STONE))
    W(box(FX0, YF - TER_D, 0, VS_X0, YF, TER_Z - 2 * FT, STONE))          # solid under the terrace, open at the door
    W(box(VS_X1, YF - TER_D, 0, FX1 - 32 * FT, YF, TER_Z - 2 * FT, STONE))
    sx = FX1 - 4
    for k in range(24):
        W(box(sx - (k + 1) * 14, YF - TER_D - 8 * FT, 0, sx - k * 14, YF - TER_D, (k + 1) * 12, STONE))
    W(box(sx - 24 * 14, YF - TER_D, 0, sx, YF, TER_Z - 2 * FT, STONE))
    by0, by1 = YF - TER_D, YF - TER_D + 8
    for x0, x1 in ((FX0, VIA_X0), (VIA_X1, sx - 24 * 14 - 8)):
        if x1 <= x0:
            continue
        det(box(x0, by0, TER_Z, x1, by1, TER_Z + 6, STONE))
        det(box(x0, by0 - 2, TER_Z + 36, x1, by1 + 2, TER_Z + 42, STONE))
        det(box(x0, by0 + 2, TER_Z + 6, x1, by1 - 2, TER_Z + 36, STONE))   # solid balustrade: the BSP is near its vertex cap
    det(box(FX0, YF - TER_D - 4, TER_Z - 2 * FT, FX1, YF - TER_D, TER_Z, STONE))   # terrace fascia
    det(box(FX0, YF - 12, 0, FX1, YF, 3 * FT, STONE))                              # plinth
    # Great arched windows: dark glass, green iron grid, stone archivolt, jambs and keystone.
    for dx in WIN:
        cx = FCX + dx
        hw, z0, zs = WIN_HW, WIN_Z0, WIN_SP
        det(yprism(ccw([(cx - hw, z0), (cx + hw, z0)] + halfdisc(cx, zs, hw, 8)[:-1] + [(cx - hw, zs)]), YF - 2, YF, WINTEX))
        for d in _arch_ring(cx, zs, hw, hw + 30, YF - 12, YF, STONE, 8):
            det(d)
        for x0, x1 in ((cx - hw - 30, cx - hw), (cx + hw, cx + hw + 30)):
            det(box(x0, YF - 12, z0, x1, YF, zs, STONE))
        det(box(cx - hw - 36, YF - 16, z0 - 18, cx + hw + 36, YF, z0, STONE))         # sill
        det(box(cx - 20, YF - 18, zs + hw - 6, cx + 20, YF, zs + hw + 40, STONE))      # keystone
    # Paired fluted columns (12-sided) on bases, capitals under the entablature; oval and
    # tall windows between the inner pairs.
    for px in PAIRS:
        for dx in (-6 * FT, 6 * FT):
            x, y = FCX + px + dx, YF - 30
            det(box(x - 38, y - 38, TER_Z, x + 38, YF, TER_Z + 18, STONE))
            det(prism(ngon(x, y, 30, 8, math.pi / 8), TER_Z + 18, 86 * FT, STONE))
            det(box(x - 40, y - 40, 86 * FT, x + 40, YF, 90 * FT, STONE))
        if abs(px) < 60 * FT:
            cx = FCX + px
            ell = [(round(cx + 48 * math.cos(2 * math.pi * i / 10)), round(70 * FT + 66 * math.sin(2 * math.pi * i / 10))) for i in range(10)]
            rim = [(round(cx + 62 * math.cos(2 * math.pi * i / 10)), round(70 * FT + 80 * math.sin(2 * math.pi * i / 10))) for i in range(10)]
            det(yprism(ccw(rim), YF - 6, YF, STONE))
            det(yprism(ccw(ell), YF - 8, YF - 6, GLASS))
            det(box(cx - 48, YF - 2, 32 * FT, cx + 48, YF, 58 * FT, WINTEX))
            det(box(cx - 60, YF - 10, 58 * FT, cx + 60, YF, 59 * FT, STONE))
    # Entablature, cornice, attic band, inscription panel, top cornice.
    det(box(FX0, YF - 4 * FT, 90 * FT, FX1, YF, 100 * FT, STONE))
    det(box(FX0, YF - 7 * FT, 100 * FT, FX1, YF, 104 * FT, STONE))
    det(box(FX0, YF - 2 * FT, 104 * FT, FX1, YF, 126 * FT, STONE))
    det(box(FCX - 40 * FT, YF - 2 * FT - 4, 110 * FT, FCX + 40 * FT, YF - 2 * FT, 120 * FT, "gcs/inscription"))
    det(box(FX0, YF - 4 * FT, 126 * FT, FX1, YF, RZ, STONE))
    # Glory of Commerce: pedestal and the clock in a stone surround; the figures are a model.
    det(box(FCX - 34 * FT, YF - 4 * FT, RZ, FCX + 34 * FT, YF + 24 * FT, RZ + 8 * FT, STONE))
    det(yprism(ccw([(FCX - 11 * FT, RZ + 8 * FT), (FCX + 11 * FT, RZ + 8 * FT)] + halfdisc(FCX, RZ + 16 * FT, 11 * FT, 10)[:-1]
                   + [(FCX - 11 * FT, RZ + 16 * FT)]), YF - 3 * FT, YF + 10 * FT, STONE))
    det(yprism(ngon_xz(FCX, CLK_Z, CLK_R + 6, 20), YF - 3 * FT - 4, YF - 3 * FT, "gcs/gold"))
    det(yprism(ngon_xz(FCX, CLK_Z, CLK_R, 20), YF - 3 * FT - 8, YF - 3 * FT - 4, "gcs/clock_out"))
    # Figures as one model (make_models.py statue_group): brushes cost too many vertices.
    ents.append(ent("prop_static", (FCX, YF + 3 * FT, RZ + 8 * FT), model="models/gcs/statue_group.mdl",
                    angles="0 -90 0", solid="0", disableshadows="1"))   # studiomdl turns SMD +x to model +y
    # Bronze eagles on the facade's top corners (make_models.py eagle).
    for x in (FX0 + 6 * FT, FX1 - 6 * FT):
        ents.append(ent("prop_static", (x, YF - 2 * FT, RZ), model="models/gcs/eagle.mdl",
                        angles="0 -90 0", solid="0", disableshadows="1"))
    # Yellow cabs on 42nd Street (make_models.py taxi), both directions.
    for dx, y, yaw in ((-170, 62, 90), (-20, 62, 90), (150, 62, 90), (-90, 36, -90), (100, 36, -90)):
        ents.append(ent("prop_static", (FCX + dx * FT, YS + y * FT, -8), model="models/gcs/taxi.mdl",
                        angles="0 %d 0" % yaw, solid="6"))
    # Park Avenue Viaduct crossing 42nd Street: deck at terrace level, arched steel fascias,
    # bronze railings, a lit portal into the building across the street.
    W(box(VIA_X0, YS, TER_Z - 4 * FT, VIA_X1, YF - TER_D, TER_Z, "gcs/sidewalk"))
    n, ya, yb = 10, YS, YF - TER_D
    for x0, x1 in ((VIA_X0 - 10, VIA_X0), (VIA_X1, VIA_X1 + 10)):
        for i in range(n):
            y0, y1 = ya + (yb - ya) * i // n, ya + (yb - ya) * (i + 1) // n
            zb = lambda y: round(TER_Z - 4 * FT - 6 * FT * math.sin(math.pi * (y - ya) / (yb - ya)))
            det(xprism(ccw([(y0, zb(y0)), (y1, zb(y1)), (y1, TER_Z - 2 * FT), (y0, TER_Z - 2 * FT)]), x0, x1, "gcs/steel"))
        det(box(x0, ya, TER_Z - 2 * FT, x1, yb, TER_Z, "gcs/gold"))
    for x in (VIA_X0 + 4, VIA_X1 - 4):
        det(box(x - 3, ya, TER_Z + 38, x + 3, yb, TER_Z + 42, "gcs/bronze"))
        det(box(x - 1, ya, TER_Z, x + 1, yb, TER_Z + 38, "gcs/vh_grille"))
    det(box(VIA_X0 + 16, YS, TER_Z, VIA_X1 - 16, YS + 2, TER_Z + 12 * FT, TEX_DOOR))
    ents.append(ent("light", ((VIA_X0 + VIA_X1) // 2, YS + 100, TER_Z + 8 * FT), _light="255 215 160 60"))
    # Street lamps along the north kerb.
    for k in range(-3, 4):
        x, y = FCX + k * 60 * FT + 30 * FT, YF - SW + 24
        if not (FX0 - 10 * FT < x < EX1 - 10 * FT) or VIA_X0 - 4 * FT < x < VIA_X1 + 4 * FT:
            continue
        det(prism(ngon(x, y, 5, 8), 0, 20 * FT, GRILLE))
        det(prism(ngon(x, y, 12, 8), 20 * FT, 21 * FT, GRILLE))
        det(prism(ngon(x, y, 9, 8), 19 * FT - 10, 20 * FT, TEX_BULB))
        ents.append(ent("light", (x, y, 18 * FT), _light="255 235 200 40"))
    ents.append(ent("light_environment", (FCX, YS + 40 * FT, 60 * FT), angles="0 75 0", pitch="-42",
                    _light="255 248 236 420", _ambient="160 180 215 220"))
    ents.append(ent("env_cubemap", (FCX, YF - 50 * FT, 6 * FT)))
    ents.append(ent("env_cubemap", ((VIA_X0 + VIA_X1) // 2, YF - 50 * FT, TER_Z + 6 * FT)))
    ents.append(ent("func_brush", solids="".join(decor), targetname="ext_decor", Solidity="2",
                    disableshadows="1", vrad_brush_cast_shadows="1"))


def ngon_xz(cx, cz, r, n):
    return ccw([(round(cx + r * math.cos(2 * math.pi * i / n)), round(cz + r * math.sin(2 * math.pi * i / n))) for i in range(n)])


# Upper-level track platforms (area 4). Three gates in the concourse north wall (bay centres)
# lead through short passages to a low dark train shed; tracks run north, three island
# platforms (rose tile, yellow edge), riveted steel columns, fluorescent strips; a Metro-North
# car stands open on the track west of the centre platform (photos: Grand_Central_Station_tracks,
# Metro_North_M7a_Rainbow_Heart_Sticker_Grand_Central).
GATES = ((-660, 29), (0, 30), (660, 31))   # gate x, track number on the sign
GATE_W, GATE_H = 12 * FT, 12 * FT
SH_Y0 = HY + WALL + 8 * FT                 # shed south face
SH_Y1 = SH_Y0 + 300 * FT                   # 300 ft of platform (real ones run ~800 ft)
SH_X = 85 * FT                             # shed half-width
SH_H = 18 * FT
PIT = 4 * FT                               # rail head below platform
HEAD = 20 * FT                             # cross-platform strip at the platform heads
PLATS = ((-780, -540), (-120, 120), (540, 780))
PITS = ((-SH_X, -780), (-540, -120), (120, 540), (780, SH_X))
TRACKS = (-900, -474, -186, 186, 474, 900)
CAR_X = (-246, -126)                       # walk-in car on track -186, 10 ft wide
CAR_Y0 = SH_Y0 + HEAD + 5 * FT
CAR_L = 85 * FT


def _sign_uv(gx):
    def uv(n):
        su, sv = 96/512, 24/128
        if n[1] < -0.5:
            return "[1 0 0 %g] %g" % (-(gx - 48)/su, su), "[0 0 -1 %g] %g" % (180/sv, sv)
    return uv


for _gx, _n in GATES:
    FACEUV["gcs/track%d" % _n] = _sign_uv(_gx)


def platforms(W, ents):
    # Decor goes into one func_brush (world model is at vbsp's t-junction cap).
    decor = []
    det = decor.append
    T_TILE, T_EDGE, T_DARK, T_STEEL = "gcs/plat_tile", "gcs/plat_edge", "gcs/shed_dark", "gcs/steel"
    # Shed shell: walls, dark ceiling, head strip, platforms, ballast pits.
    W(box(-SH_X, SH_Y0, SH_H, SH_X, SH_Y1, SH_H + WALL, T_DARK))
    W(box(-SH_X - WALL, SH_Y0, -PIT - WALL, -SH_X, SH_Y1, SH_H + WALL, T_DARK))
    W(box(SH_X, SH_Y0, -PIT - WALL, SH_X + WALL, SH_Y1, SH_H + WALL, T_DARK))
    W(box(-SH_X - WALL, SH_Y1, -PIT - WALL, SH_X + WALL, SH_Y1 + WALL, SH_H + WALL, T_DARK))
    W(box(-SH_X, SH_Y0, -PIT - WALL, SH_X, SH_Y0 + HEAD, 0, T_TILE))
    for x0, x1 in PLATS:
        W(box(x0, SH_Y0 + HEAD, -PIT - WALL, x1, SH_Y1, 0, T_TILE))
    for x0, x1 in PITS:
        W(box(x0, SH_Y0 + HEAD, -PIT - WALL, x1, SH_Y1, -PIT, "gcs/ballast"))
    # South wall of the shed and the gate passages through the concourse north wall.
    edges = [-SH_X - WALL] + [e for gx, _ in GATES for e in (gx - GATE_W//2, gx + GATE_W//2)] + [SH_X + WALL]
    for j in range(0, len(edges), 2):
        W(box(edges[j], HY + WALL, -WALL, edges[j + 1], SH_Y0, SH_H + WALL, TEX_CREAM))
    for gx, n in GATES:
        g0, g1 = gx - GATE_W//2, gx + GATE_W//2
        W(box(g0, HY + WALL, GATE_H, g1, SH_Y0, SH_H + WALL, TEX_CREAM))
        W(box(g0, HY, -WALL, g1, SH_Y0, 0, TEX_FLOOR))
        ents.append(ent("light", (gx, (HY + SH_Y0)//2, GATE_H - 30), _light="255 215 160 25"))
        # Brass gate frame and TRACK sign on the concourse face; the same sign hangs in the shed.
        det(box(g0 - 10, HY - 4, 0, g0, HY, GATE_H + 10, TEX_GOLD))
        det(box(g1, HY - 4, 0, g1 + 10, HY, GATE_H + 10, TEX_GOLD))
        det(box(g0, HY - 4, GATE_H, g1, HY, GATE_H + 10, TEX_GOLD))
        det(box(gx - 48, HY - 3, 156, gx + 48, HY, 180, "gcs/track%d" % n))
        sy = SH_Y0 + HEAD + 2 * FT
        det(box(gx - 48, sy, 156, gx + 48, sy + 3, 180, "gcs/track%d" % n))
        det(box(gx - 50, sy - 1, 180, gx + 50, sy + 4, 184, T_STEEL))
        det(box(gx - 2, sy, 184, gx + 2, sy + 3, SH_H, T_STEEL))
    # Brass railing round the pit ends, bumpers and rails.
    for x0, x1 in PITS:
        y = SH_Y0 + HEAD
        det(box(x0, y - 2, 40, x1, y + 2, 44, TEX_GOLD))
        det(box(x0, y - 2, 20, x1, y + 2, 22, TEX_GOLD))
        for x in range(x0 + 4, x1, 48):
            det(box(x - 1, y - 1, 0, x + 1, y + 1, 40, TEX_GOLD))
    for t in TRACKS:
        det(box(t - 40, SH_Y0 + HEAD, -PIT, t + 40, SH_Y0 + HEAD + 24, -12, T_STEEL))
        for r in (-30, 26):
            det(box(t + r, SH_Y0 + HEAD + 24, -PIT, t + r + 4, SH_Y1, -PIT + 6, T_STEEL))
    # Yellow edges, steel columns (platform centres and between paired tracks), cross beams,
    # fluorescent strips with cool lights.
    for x0, x1 in PLATS:
        det(box(x0, SH_Y0 + HEAD, 0, x0 + 24, SH_Y1, 1, T_EDGE))
        det(box(x1 - 24, SH_Y0 + HEAD, 0, x1, SH_Y1, 1, T_EDGE))
    beams = range(SH_Y0 + 30 * FT, SH_Y1, 30 * FT)
    for y in beams:
        det(box(-SH_X, y - 8, SH_H - 20, SH_X, y + 8, SH_H, T_STEEL))
        for cx, z0 in ((-660, 0), (0, 0), (660, 0), (-330, -PIT), (330, -PIT)):
            det(box(cx - 8, y - 8, z0, cx + 8, y + 8, SH_H - 20, T_STEEL))
    for x0, x1 in PLATS:
        cx = (x0 + x1) // 2
        for y in beams:
            for ox in (-60, 60):
                det(box(cx + ox - 4, y + 40, SH_H - 28, cx + ox + 4, y + 30 * FT - 40, SH_H - 22, "gcs/fluor"))
        for y in range(SH_Y0 + HEAD + 15 * FT, SH_Y1, 40 * FT):
            ents.append(ent("light", (cx, y, SH_H - 50), _light="235 240 255 45"))
        ents.append(ent("env_cubemap", (cx, SH_Y0 + 60 * FT, 64)))
    for y in range(SH_Y0 + 40 * FT, SH_Y1, 80 * FT):
        for x in (-330, 330, -900, 900):
            ents.append(ent("light", (x, y, SH_H - 60), _light="200 210 230 12"))
    # Metro-North cars: a walk-in car on track -186 with two open doors on the platform
    # side, benches and lights; a closed car coupled behind it and another on track 474.
    cx0, cx1 = CAR_X
    T_TR = "gcs/train"

    def car(x0, x1, y0, y1, doors):
        det(box(x0, y0, -PIT + 8, x1, y1, 0, T_TR))                         # underframe
        det(box(x0 + 4, y0 + 4, 0, x1 - 4, y1 - 4, 1, "gcs/car_floor"))      # floor
        det(box(x0, y0, 150, x1, y1, 162, T_TR))                            # roof
        det(box(x0, y0, 0, x1, y0 + 4, 150, T_TR))                          # ends
        det(box(x0, y1 - 4, 0, x1, y1, 150, T_TR))
        for wx0, wx1, dd in ((x0, x0 + 4, ()), (x1 - 4, x1, doors)):
            cuts = [y0 + 4] + [e for d in dd for e in (d - 36, d + 36)] + [y1 - 4]
            for j in range(0, len(cuts), 2):
                a, b = cuts[j], cuts[j + 1]
                det(box(wx0, a, 0, wx1, b, 62, T_TR))
                det(box(wx0, a, 62, wx1, b, 96, "gcs/vh_glass"))
                det(box(wx0, a, 96, wx1, b, 150, T_TR))
            for d in dd:
                det(box(wx0, d - 36, 88, wx1, d + 36, 150, T_TR))
    d1, d2 = CAR_Y0 + CAR_L // 4, CAR_Y0 + 3 * CAR_L // 4
    car(cx0, cx1, CAR_Y0, CAR_Y0 + CAR_L, (d1, d2))
    car(cx0, cx1, CAR_Y0 + CAR_L + 24, CAR_Y0 + 2 * CAR_L + 24, ())
    car(414, 534, CAR_Y0 + 10 * FT, CAR_Y0 + 10 * FT + CAR_L, ())
    for y in range(CAR_Y0 + 60, CAR_Y0 + CAR_L - 40, 54):
        if any(abs(y - d) < 60 for d in (d1, d2)):
            continue
        for bx0, bx1 in ((cx0 + 4, cx0 + 44), (cx1 - 44, cx1 - 4)):
            det(box(bx0, y, 1, bx1, y + 20, 18, "gcs/vh_grille"))
            det(box(bx0, y + 20, 1, bx1, y + 26, 36, "gcs/vh_grille"))
    for y in (CAR_Y0 + 200, CAR_Y0 + CAR_L // 2, CAR_Y0 + CAR_L - 200):
        det(box(-190, y - 100, 146, -182, y + 100, 150, "gcs/fluor"))
        ents.append(ent("light", (-186, y, 120), _light="235 240 255 18"))
    ents.append(ent("func_brush", solids="".join(decor), targetname="plat_decor", Solidity="2",
                    disableshadows="1", vrad_brush_cast_shadows="1"))


def build():
    world, ents = [], []
    W = world.append

    # Sealed outer hull (nodraw) so the interior can't leak while geometry is rough.
    O = 256
    X0, X1, Y0, Y1, Z1 = OB_X0 - 128, -RAMP_XF + EAST_D + 2*WALL + 128, YS - 2*WALL - 128, SH_Y1+WALL+64, SKYZ+WALL+64
    X0, X1 = min(X0, EX0 - 2*WALL - 128), max(X1, EX1 + 2*WALL + 128)
    ZB = LOW_Z - 2*WALL - 64
    W(box(X0, Y0, ZB, X1, Y1, ZB+64, NODRAW))
    W(box(X0, Y0, Z1, X1, Y1, Z1+64, NODRAW))
    W(box(X0, Y0-64, ZB, X1, Y0, Z1+64, NODRAW))
    W(box(X0, Y1, ZB, X1, Y1+64, Z1+64, NODRAW))
    W(box(X0-64, Y0-64, ZB, X0, Y1+64, Z1+64, NODRAW))
    W(box(X1, Y0-64, ZB, X1+64, Y1+64, Z1+64, NODRAW))

    # Floor (cut by the two west ramp wells) and long walls.
    W(box(RAMP_X0, -HY, -WALL, -RAMP_X0, HY, 0, TEX_FLOOR))
    for y0, y1 in ((-HY, -RAMP_Y1), (-RAMP_Y0, RAMP_Y0), (RAMP_Y1, HY)):
        W(box(-HX, y0, -WALL, RAMP_X0, y1, 0, TEX_FLOOR))
        W(box(-RAMP_X0, y0, -WALL, HX, y1, 0, TEX_FLOOR))
    lower_level(W, ents)
    # South wall, cut by the passage to Vanderbilt Hall in its west bay.
    W(box(-HX, -HY-WALL, -WALL, VH_PX0, -HY, SPRING, TEX_WALL))
    W(box(VH_PX1, -HY-WALL, -WALL, HX, -HY, SPRING, TEX_WALL))
    W(box(VH_PX0, -HY-WALL, VH_PH, VH_PX1, -HY, SPRING, TEX_WALL))
    W(box(VH_PX0, -HY-WALL, -WALL, VH_PX1, -HY, 0, TEX_FLOOR))
    vanderbilt(W, ents)
    exterior(W, ents)
    # North wall, cut by the three track gates.
    gedges = [-HX] + [e for gx, _ in GATES for e in (gx - GATE_W//2, gx + GATE_W//2)] + [HX]
    for j in range(0, len(gedges), 2):
        W(box(gedges[j], HY, -WALL, gedges[j+1], HY+WALL, SPRING, TEX_WALL))
    for gx, _ in GATES:
        W(box(gx - GATE_W//2, HY, GATE_H, gx + GATE_W//2, HY+WALL, SPRING, TEX_WALL))
    platforms(W, ents)

    # Barrel vault, segmented flattened half-ellipse around the x axis.
    # The inner faces carry the zodiac mural (2048x1024) once: u along x, v along the arc.
    N = 20
    r0, r1 = 0, WALL
    p = lambda r, a: (round((HY+r)*math.cos(a)), round(SPRING + (VRISE+r)*math.sin(a)))
    arc = [p(r0, math.pi*i/N) for i in range(N+1)]
    seg = [math.dist(arc[i], arc[i+1]) for i in range(N)]
    su, sv = 2*HX/2048, sum(seg)/1024
    s0 = 0
    for i in range(N):
        a0, a1 = math.pi*i/N, math.pi*(i+1)/N
        poly = [p(r1, a0), p(r1, a1), p(r0, a1), p(r0, a0)]
        q0, q1 = arc[i], arc[i+1]
        ty, tz = (q1[0]-q0[0])/seg[i], (q1[1]-q0[1])/seg[i]
        uv = ("[1 0 0 %g] %g" % (HX/su, su),
              "[0 %g %g %g] %g" % (ty, tz, (s0 - (q0[0]*ty + q0[1]*tz))/sv, sv))
        W(xprism(poly, -HX, HX, TEX_VAULT, {2: uv}))
        s0 += seg[i]
    # Corners behind the vault so the wall tops are solid.
    W(box(-HX, -HY-WALL, SPRING, HX, -HY, SPRING+8, TEX_TRIM))
    W(box(-HX, HY, SPRING, HX, HY+WALL, SPRING+8, TEX_TRIM))

    # End walls with three tall arched windows (blockout: rectangular openings into glowing alcoves).
    win_w, win_z0, win_z1 = 26*FT, BALC_Z + 16*FT, SPRING + 22*FT
    win_zc = SPRING + 29*FT + 6                # the centre window rises higher, under the crown
    centres = [-31*FT, 0, 31*FT]            # close-set, as in the photos: narrow piers between
    for sgn in (-1, 1):
        xin, xout = sgn*HX, sgn*(HX+WALL)
        xa, xb = min(xin, xout), max(xin, xout)
        # Arcades: three arched openings under the balcony and three behind it, each into a
        # short sealed passage. Wall bands between them are solid.
        for y0, y1 in ((-HY, -RAMP_Y1), (-RAMP_Y0, RAMP_Y0), (RAMP_Y1, HY)):   # ramps pass under the side arches
            W(box(xa, y0, -WALL, xb, y1, 0, TEX_WALL))
        W(box(xa, -HY, ARCH_TOP, xb, HY, BALC_Z, TEX_WALL))
        W(box(xa, -HY, BALC_Z + BARCH_H, xb, HY, win_z0, TEX_WALL))
        for z0, aw, ah in ((0, ARCH_W, ARCH_TOP), (BALC_Z, BARCH_W, BARCH_H)):
            top = z0 + ah
            aedges = [-HY] + [e for c in centres for e in (c-aw//2, c+aw//2)] + [HY]
            for j in range(0, len(aedges), 2):
                W(box(xa, aedges[j], z0, xb, aedges[j+1], top, TEX_WALL))
            for c in centres:
                arcade_bay(W, ents, sgn, xin, xout, c, z0, aw//2, top, min(WALL, BALC_Z - ARCH_TOP) if z0 == 0 else WALL,
                           ramp=(z0 == 0 and c != 0))
        W(box(xa, -HY, win_zc, xb, HY, CROWN+WALL, TEX_WALL))
        W(box(xa, -HY, win_z1, xb, -win_w//2, win_zc, TEX_WALL))
        W(box(xa, win_w//2, win_z1, xb, HY, win_zc, TEX_WALL))
        edges = [-HY] + [e for c in centres for e in (c-win_w//2, c+win_w//2)] + [HY]
        for j in range(0, len(edges), 2):
            W(box(xa, edges[j], win_z0, xb, edges[j+1], win_z1, TEX_WALL))
        # Alcove behind: glowing back panel.
        xg0, xg1 = sorted((sgn*(HX+WALL+192), sgn*(HX+WALL+224)))
        W(box(xg0, -HY, win_z0-32, xg1, HY, win_zc+32, TEX_GLASS))
        # Arched heads: fill the corners above each arch with triangle fans.
        for c in centres:
            r, zt = win_w//2, (win_zc if c == 0 else win_z1)
            arc = halfdisc(c, zt - r, r, 8)
            for i in range(8):
                corner = (c + r, zt) if i < 4 else (c - r, zt)
                ents.append(ent("func_detail", solids=xprism(ccw([corner, arc[i], arc[i+1]]), xa, xb, TEX_WALL)))
        for c in centres:
            ents.append(ent("light", (sgn*(HX+WALL+96), c, (win_z0+win_z1)/2),
                            _light="255 240 215 60", _quadratic_attn="0", _linear_attn="1", _fifty_percent_distance="900", _zero_percent_distance="2400"))
            ents.append(ent("light_spot", (sgn*(HX+WALL+150), c, win_z1-40),
                            angles="-38 %d 0" % (180 if sgn > 0 else 0), pitch="-38",
                            _light="255 235 200 110", _inner_cone="30", _cone="65", _exponent="1",
                            _distance="0", _fifty_percent_distance="2600", _zero_percent_distance="5200"))

        # Sun shafts: one additive beam per window, falling inward at the spotlight pitch.
        a = math.radians(38)
        dx, dz = -sgn*math.cos(a), -math.sin(a)
        x0 = sgn*HX
        for c in centres:
            zt = (win_zc if c == 0 else win_z1) - 6*FT
            zb = win_z0 + 2*FT
            L, lb = (zt - 8) / -dz, (zb - 8) / -dz   # slant lengths to the floor
            poly = ccw([(x0, zb), (x0, zt), (round(x0 + dx*L), 8), (round(x0 + dx*lb), 8)])
            w = round(win_w * 0.55)
            y0 = c - w//2
            su, sv = w/256, L/256
            uv = ("[0 1 0 %g] %g" % (-y0/su, su),
                  "[%g 0 %g %g] %g" % (dx, dz, -(dx*x0 + dz*zt)/sv, sv))
            ents.append(ent("func_illusionary", solids=yprism(poly, y0, y0 + w, TEX_SHAFT, uv, NODRAW), disableshadows="1"))

    # Mullion grid in the end windows, gilded band across each end at the springline.
    for sgn in (-1, 1):
        xm0, xm1 = sorted((sgn*(HX+WALL//2), sgn*(HX+WALL//2+4)))
        for c in centres:
            for k in range(1, 8):
                y = c - win_w//2 + k*win_w//8
                ents.append(ent("func_detail", solids=box(xm0, y-3, win_z0, xm1, y+3, win_zc if c == 0 else win_z1, TEX_GRID)))
            for z in range(win_z0 + 48, win_zc if c == 0 else win_z1, 96):
                ents.append(ent("func_detail", solids=box(xm0, c-win_w//2, z-3, xm1, c+win_w//2, z+3, TEX_GRID)))
        xa, xb = sorted((sgn*HX, sgn*(HX-24)))
        for j in range(0, len(edges), 2):
            ents.append(ent("func_detail", solids=box(xa, edges[j], SPRING-40, xb, edges[j+1], SPRING, TEX_GOLD)))
        # Paired engaged columns on the piers between the windows, gilded capitals.
        xc0, xc1 = sorted((sgn*HX, sgn*(HX-3*FT)))
        for py in (-31*FT//2, 31*FT//2):
            for dy in (-2*FT, 2*FT):
                y = py + dy
                ents.append(ent("func_detail", solids=box(xc0, y-18, BALC_Z, xc1, y+18, SPRING-64, TEX_CREAM)))
                ents.append(ent("func_detail", solids=box(xc0, y-24, SPRING-64, xc1, y+24, SPRING-40, TEX_GOLD)))
                ents.append(ent("func_detail", solids=box(xc0, y-24, BALC_Z, xc1, y+24, BALC_Z+18, TEX_TRIM)))
        # The great end arch: a deep soffit following the vault, gilded on its inner edge.
        e = lambda dy, dz, a: (round((HY-dy)*math.cos(a)), round(SPRING + (VRISE-dz)*math.sin(a)))
        for i in range(N):
            a0, a1 = math.pi*i/N, math.pi*(i+1)/N
            xa, xb = sorted((sgn*HX, sgn*(HX-6*FT)))
            ents.append(ent("func_detail", solids=xprism(ccw([e(0, 0, a0), e(0, 0, a1), e(11*FT, 9*FT, a1), e(11*FT, 9*FT, a0)]), xa, xb, TEX_COFFER)))
            xa, xb = sorted((sgn*(HX-5*FT), sgn*(HX-6*FT-8)))
            ents.append(ent("func_detail", solids=xprism(ccw([e(11*FT, 9*FT, a0), e(11*FT, 9*FT, a1), e(12*FT, 10*FT, a1), e(12*FT, 10*FT, a0)]), xa, xb, TEX_GOLD)))

    # Long walls: pilasters between bays, a tall dark window grid in each bay, the
    # gilded cornice at the springline and a lunette window cut into the vault above.
    bay = 2*HX // BAYS
    for sgn in (-1, 1):
        yw = sgn*HY
        inset = lambda d0, d1: sorted((yw - sgn*d0, yw - sgn*d1))
        for k in range(BAYS + 1):
            x = -HX + k*bay
            ya, yb = inset(0, 60)
            ents.append(ent("func_detail", solids=box(max(x-7*FT, -HX), ya, 0, min(x+7*FT, HX), yb, SPRING-72, TEX_WALL)))
            ya, yb = inset(0, 72)
            ents.append(ent("func_detail", solids=box(max(x-8*FT, -HX), ya, 0, min(x+8*FT, HX), yb, 3*FT, TEX_CREAM)))
        for k in range(BAYS):
            cx = -HX + k*bay + bay//2
            w = bay//2 - 10*FT
            ga, gb = inset(0, 2)
            ents.append(ent("func_detail", solids=box(cx-w, ga, BAY_Z0, cx+w, gb, SPRING-8*FT, TEX_GLASS)))
            ma, mb = inset(2, 6)
            for j in range(-3, 4):
                ents.append(ent("func_detail", solids=box(cx + j*w//4 - 3, ma, BAY_Z0, cx + j*w//4 + 3, mb, SPRING-8*FT, TEX_GRID)))
            for z in range(BAY_Z0, SPRING-8*FT+1, 96):
                ents.append(ent("func_detail", solids=box(cx-w, ma, z-3, cx+w, mb, z+3, TEX_GRID)))
            # Lunette: half-disc glass standing on the cornice, poking through the vault.
            la, lb = inset(88, 92)
            ents.append(ent("func_detail", solids=yprism(halfdisc(cx, SPRING, 16*FT), la, lb, TEX_GLOW)))
            # Sculpted cream surround (Flag_Ceiling photo): a wide stepped hood, gold-edged.
            for r0, r1, d0, d1, tex in ((16, 19, 92, 112, TEX_CREAM), (19, 23, 92, 104, TEX_CREAM), (23, 24, 92, 100, TEX_GOLD)):
                fa, fb = inset(d0, d1)
                outer, inner = halfdisc(cx, SPRING, r1*FT), halfdisc(cx, SPRING, r0*FT)
                for i in range(len(outer)-1):
                    # Carved relief: alternate voussoirs of the middle ring stand 6 u proud.
                    a, b = inset(d0, d1 + 6) if r0 == 19 and i % 2 == 0 else (fa, fb)
                    ents.append(ent("func_detail", solids=yprism([outer[i], outer[i+1], inner[i+1], inner[i]], a, b, tex)))
            # Keystone at the crown of the hood.
            ka, kb = inset(92, 118)
            ents.append(ent("func_detail", solids=box(cx - 2*FT, ka, SPRING + 15*FT, cx + 2*FT, kb, SPRING + 25*FT, TEX_CREAM)))
            ra, rb = inset(92, 96)
            for j in (-2, -1, 0, 1, 2):
                top = SPRING + int(16*FT*math.sqrt(1 - (j*6/16)**2)) - 4
                ents.append(ent("func_detail", solids=box(cx + j*6*FT - 3, ra, SPRING, cx + j*6*FT + 3, rb, top, TEX_GRID)))
            ents.append(ent("light", (cx, yw - sgn*200, SPRING + 80), _light="200 220 240 8"))
        ca, cb = inset(0, 88)
        ents.append(ent("func_detail", solids=box(-HX, ca, SPRING-40, HX, cb, SPRING, TEX_GOLD)))
        ca, cb = inset(0, 72)
        ents.append(ent("func_detail", solids=box(-HX, ca, SPRING-72, HX, cb, SPRING-40, TEX_TRIM)))
        # Modillion band (east_balcony photo): cream brackets every 2 ft under an overhanging crown.
        ca, cb = inset(88, 104)
        ents.append(ent("func_detail", solids=box(-HX, ca, SPRING-10, HX, cb, SPRING, TEX_GOLD)))
        ma, mb = inset(72, 100)
        for x in range(-HX + 12, HX - 6, 24):
            ents.append(ent("func_detail", solids=box(x-5, ma, SPRING-40, x+5, mb, SPRING-10, TEX_CREAM)))

    # Balconies at both ends with a parapet.
    for sgn in (-1, 1):
        xa, xb = sorted((sgn*HX, sgn*(HX-BALC_D)))
        ents.append(ent("func_detail", solids=box(xa, -HY, BALC_Z-24, xb, HY, BALC_Z, TEX_CREAM)))
        rx = sgn*(HX-BALC_D)
        ra, rb = sorted((rx, rx+sgn*-16))
        for y0, y1 in ((-HY, -24*FT), (24*FT, HY)):
            # Cream marble parapet with a brass handrail on top, like the stair balustrades.
            ents.append(ent("func_detail", solids=box(ra, y0, BALC_Z, rb, y1, BALC_Z+42, TEX_CREAM)))
            ents.append(ent("func_detail", solids=box(ra-2, y0, BALC_Z+42, rb+2, y1, BALC_Z+46, TEX_GOLD)))
        # Ceiling lamps under the balcony so the floor arcade and stair sides aren't black.
        lx = sgn*(HX - BALC_D//2)
        for ly in (-3*HY//4, -HY//4, HY//4, 3*HY//4):
            ents.append(ent("func_detail", solids=box(lx-10, ly-10, BALC_Z-32, lx+10, ly+10, BALC_Z-24, TEX_GOLD)))
            ents.append(ent("func_detail", solids=box(lx-7, ly-7, BALC_Z-40, lx+7, ly+7, BALC_Z-32, TEX_BULB)))
            ents.append(ent("light", (lx, ly, BALC_Z-64), _light="255 205 145 30"))

    # Double staircases: two flights per end, landing on the balcony.
    rise, run = 12, 18
    steps = BALC_Z // rise
    for sgn in (-1, 1):
        for yc in (-8*FT, 8*FT):
            y0, y1 = sorted((yc, yc + (1 if yc > 0 else -1)*14*FT))
            for k in range(steps):
                xs = sgn*(HX-BALC_D) - sgn*(steps-k)*run
                xa, xb = sorted((xs, xs+sgn*run))
                ents.append(ent("func_detail", solids=box(xa, y0, 0, xb, y1, (k+1)*rise, TEX_CREAM)))
            # Solid cream balustrades on both sides with a brass handrail, newel at the foot.
            xf, xt = sgn*(HX-BALC_D) - sgn*steps*run, sgn*(HX-BALC_D)
            for ya, yb in ((y0-18, y0), (y1, y1+18)):
                wall = [(xf, 0), (xt, 0), (xt, BALC_Z+42), (xf, 42)]
                rail = [(xf, 42), (xt, BALC_Z+42), (xt, BALC_Z+46), (xf, 46)]
                ents.append(ent("func_detail", solids=yprism(ccw(wall), ya, yb, TEX_CREAM)))
                ents.append(ent("func_detail", solids=yprism(ccw(rail), ya-2, yb+2, TEX_GOLD)))
                na, nb = sorted((xf, xf-sgn*24))
                ents.append(ent("func_detail", solids=box(na, ya-3, 0, nb, yb+3, 54, TEX_CREAM)))
                ents.append(ent("func_detail", solids=box(na+4, ya+1, 54, nb-4, yb-1, 66, TEX_GOLD)))

    # Information booth with the four-faced clock above it.
    # Booth: cream marble base, dark glass with brass posts, gold cornice; the clock sits
    # on a brass column: four opal dials (30 u = 2.5 ft) under a gold cap and acorn finial.
    for y in (-440, 0, 440):   # west end bay, so the first pylons are lit from both sides
        ents.append(ent("light", (DIN_X0 + 60, y, -WALL - 60), _light="255 215 170 30"))
    oct8 = lambda r: ngon(0, 0, r, 8, math.pi/8)
    det = lambda *a: ents.append(ent("func_detail", solids=prism(*a)))
    det(oct8(13*FT), 0, 3*FT, TEX_CREAM)
    # Glass is a thin translucent ring; inside, a cream counter runs round under the
    # glass and a cream cabinet core holds up the clock column, lit warm.
    ring = lambda ro, ri, z0, z1, tex: [det(ccw([ro[i], ro[(i+1) % 8], ri[(i+1) % 8], ri[i]]), z0, z1, tex)
                                        for i in range(8)]
    ring(oct8(12.5*FT), oct8(12.4*FT), 3*FT, 8*FT, "gcs/booth_glass")
    ring(oct8(12.4*FT), oct8(10.5*FT), 3*FT, 4*FT, TEX_CREAM)
    ring(oct8(12.4*FT), oct8(10.4*FT), 4*FT, 4*FT+2, TEX_GOLD)
    det(oct8(4*FT), 3*FT, 8*FT, TEX_CREAM)
    det(oct8(4.3*FT), 7*FT, 8*FT, TEX_GOLD)
    ents.append(ent("light", (0, 7*FT, 7*FT), _light="255 220 160 55"))
    ents.append(ent("light", (0, -7*FT, 7*FT), _light="255 220 160 55"))
    for x, y in oct8(13*FT):
        det(ngon(x, y, 6, 4, math.pi/4), 3*FT, 8*FT, TEX_GOLD)
    # Brass grille on the glass: two mullions per face, a counter ledge and a top rail.
    out, inn = oct8(12.75*FT), oct8(12.55*FT)
    for i in range(8):
        a, b, ai, bi = out[i], out[(i+1) % 8], inn[i], inn[(i+1) % 8]
        for t in (1/3, 2/3):
            px, py = a[0]+(b[0]-a[0])*t, a[1]+(b[1]-a[1])*t
            det(ngon(px, py, 3, 4, math.pi/4), 3*FT, 8*FT, TEX_GOLD)
        det(ccw([a, b, bi, ai]), 4*FT, 4*FT+3, TEX_GOLD)
        det(ccw([a, b, bi, ai]), 7*FT, 7*FT+2, TEX_GOLD)
    det(oct8(13.5*FT), 8*FT, 9*FT, TEX_GOLD)
    det(oct8(12*FT), 9*FT, 10*FT, TEX_CREAM)
    det(oct8(2.5*FT), 10*FT, 11*FT, TEX_GOLD)
    det(oct8(1*FT), 11*FT, 150, TEX_GOLD)
    det([(-15, -15), (15, -15), (15, 15), (-15, 15)], 150, 180, TEX_CLOCK, TEX_GOLD)
    det(oct8(20), 180, 184, TEX_GOLD)
    det(oct8(12), 184, 192, TEX_GOLD)
    det(oct8(6), 192, 200, TEX_GOLD)
    ents.append(ent("light", (0, 0, 20*FT), _light="255 225 170 25"))

    # Ticket windows along the south wall: a row of recess frames.
    for k in range(-6, 7):
        x = k*16*FT
        ents.append(ent("func_detail", solids=box(x-6*FT, -HY+0, 0, x-5*FT, -HY+3*FT, 14*FT, TEX_CREAM)))
        # Brass bracket lamp on each pier: wall plate, arm, cup and a glowing globe.
        lx, ly = x-5.5*FT, -HY+3*FT
        det(ngon(lx, ly+2, 4, 6), 10.5*FT, 12*FT, TEX_GOLD)
        ents.append(ent("func_detail", solids=box(lx-1, ly, 11*FT, lx+1, ly+16, 11*FT+2, TEX_GOLD)))
        det(ngon(lx, ly+18, 5, 8, math.pi/8), 11*FT-4, 11*FT, TEX_GOLD)
        det(ngon(lx, ly+18, 6, 8, math.pi/8), 11*FT, 11*FT+10, TEX_BULB)
        ents.append(ent("light", (lx, ly+30, 11*FT+4), _light="255 210 150 8"))
        if k < 6:
            # Each window: cream marble counter with a brass top, brass-grilled dim glass, cream lintel.
            w0, w1 = x-5*FT, x+11*FT
            ents.append(ent("func_detail", solids=box(w0, -HY, 0, w1, -HY+2*FT, 3.5*FT, TEX_CREAM)))
            ents.append(ent("func_detail", solids=box(w0, -HY, 3.5*FT, w1, -HY+2*FT+3, 3.5*FT+2, TEX_GOLD)))
            ents.append(ent("func_detail", solids=box(w0, -HY, 3.5*FT+2, w1, -HY+4, 10*FT, TEX_DIM)))
            for gx in range(int(w0)+12, int(w1)-11, 12):
                ents.append(ent("func_detail", solids=box(gx-1, -HY+4, 3.5*FT+2, gx+1, -HY+7, 10*FT, TEX_GOLD)))
            # Cream marble reveals frame the glass on both sides.
            for j0, j1 in ((w0, w0+10), (w1-10, w1)):
                ents.append(ent("func_detail", solids=box(j0, -HY, 3.5*FT+2, j1, -HY+2*FT, 10*FT, TEX_CREAM)))
            # Segmental arched head: cream spandrels between the reveals, 1.5 ft rise.
            xl, xr, zs, zt = w0+10, w1-10, 8.5*FT, 10*FT
            a, s = (xr - xl)/2, zt - zs
            R, xc = (a*a + s*s)/(2*s), (xl + xr)/2
            pts = [(round(xc + dx), round(zt - R + math.sqrt(R*R - dx*dx)))
                   for dx in (-a + 2*a*i/8 for i in range(9))]
            for i in range(8):
                corner = (xl, zt) if i < 4 else (xr, zt)
                ents.append(ent("func_detail", solids=yprism(ccw([corner, pts[i], pts[i+1]]), -HY, -HY+2*FT, TEX_CREAM)))
            ents.append(ent("func_detail", solids=box(w0, -HY, 10*FT, w1, -HY+2*FT, 11*FT, TEX_GOLD)))
            ents.append(ent("func_detail", solids=box(w0, -HY, 11*FT, w1, -HY+18, 14*FT, TEX_CREAM)))
            # Bronze TICKETS plaque centred on the lintel.
            det([(x, -HY+18), (x+6*FT, -HY+18), (x+6*FT, -HY+20), (x, -HY+20)],
                11.75*FT, 13.25*FT, "gcs/tickets", TEX_GOLD)
    # Cream marble cornice over the ticket windows with a thin gold lower edge.
    ents.append(ent("func_detail", solids=box(-100*FT, -HY, 14*FT, 100*FT, -HY+4*FT-2, 14*FT+2, TEX_GOLD)))
    ents.append(ent("func_detail", solids=box(-100*FT, -HY, 14*FT+2, 100*FT, -HY+4*FT, 16*FT, TEX_CREAM)))
    bx0, bx1, bz0, bz1 = BOARD
    det([(bx0, -HY), (bx1, -HY), (bx1, -HY+16), (bx0, -HY+16)], bz0, bz1, "gcs/board", TEX_GOLD)

    # The flag hangs in the north centre bay from a gold pole bracketed to the wall.
    fx0, fx1, fy0, fy1, fz0, fz1 = FLAG
    ents.append(ent("func_detail", solids=box(fx0, fy0, fz0, fx1, fy1, fz1, "gcs/flag")))
    ents.append(ent("func_detail", solids=box(fx0-6, fy0-3, fz1, fx1+6, fy1+3, fz1+6, TEX_GOLD)))
    for x in (fx0+12, fx1-12):
        ents.append(ent("func_detail", solids=box(x-2, fy0, fz1+2, x+2, HY, fz1+6, TEX_GOLD)))

    def globe(cx, cy, cz, r):
        # A glowing globe: three stacked octagonal slices approximating a sphere.
        for z0, z1, k in ((-1.0, -0.5, 0.75), (-0.5, 0.5, 1.0), (0.5, 1.0, 0.75)):
            det(ngon(cx, cy, max(2, round(r*k)), 8, math.pi/8), round(cz+z0*r), round(cz+z1*r), TEX_BULB)

    # Chandeliers down both long sides: a gold rod from the cornice, a gold drum with
    # two tiers of glowing bulbs, a finial below; a light at each body.
    for x in range(-HX+300, HX-299, 450):
        for y in (-HY+120, HY-120):
            zc = 32*FT
            # Model (tools/make_models.py): rod, drum, two tiers of globes, finial; no brush vertices.
            ents.append(ent("prop_static", (x, y, zc), model="models/gcs/chandelier.mdl", angles="0 0 0", solid="0"))
            ents.append(ent("light", (x, y, zc-64), _light="255 214 160 18"))
        ents.append(ent("light", (x, 0, SPRING+300), _light="160 200 210 10"))

    ents.append(ent("env_tonemap_controller", (0, 0, 64), targetname="tonemap"))
    # Clamp auto exposure and bloom so the pale stone doesn't blow out.
    ents.append(ent("logic_auto", (0, 0, 96), spawnflags="1").replace("}\n",
        '\tconnections\n\t{\n'
        '\t\t"OnMapSpawn" "tonemap,SetAutoExposureMin,0.5,0,-1"\n'
        '\t\t"OnMapSpawn" "tonemap,SetAutoExposureMax,1.2,0,-1"\n'
        '\t\t"OnMapSpawn" "tonemap,SetBloomScale,0.25,0,-1"\n\t}\n}\n'))
    ents.append(ent("info_player_start", (-HX+BALC_D//2, 0, BALC_Z+8), angles="0 0 0"))
    ents.append(ent("info_player_start", (0, -400, 8), angles="0 90 0"))
    ents.append(ent("env_cubemap", (0, 0, 200)))
    ents.append(ent("env_cubemap", (-HX+BALC_D//2, 0, BALC_Z+100)))

    world_s = 'world\n{\n\t"id" "%d"\n\t"mapversion" "1"\n\t"classname" "worldspawn"\n\t"skyname" "sky_day01_01"\n%s}\n' % (nid(), "".join(world))
    head = 'versioninfo\n{\n\t"editorversion" "400"\n\t"editorbuild" "8000"\n\t"mapversion" "1"\n\t"formatversion" "100"\n\t"prefab" "0"\n}\n'
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(head + world_s + "".join(ents), encoding="ascii", newline="\n")
    print("wrote", OUT, _id[0], "ids")


if __name__ == "__main__":
    build()
