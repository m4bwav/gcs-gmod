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
TEX_CREAM = "gcs/cream"
TEX_CLOCK = "gcs/clock"
TEX_BULB = "gcs/bulb"
TEX_COFFER = "gcs/coffer"
TEX_DOOR = "gcs/door_glow"
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
FLAG = (-10*FT, 10*FT, HY - 8*FT, HY - 8*FT + 2, SPRING - 46*FT, SPRING - 8*FT)   # x0, x1, y0, y1 (thin), z0, z1: north centre bay


def _board_uv(n):
    x0, x1, z0, z1 = BOARD
    su, sv = (x1-x0)/1024, (z1-z0)/256
    if n[1] > 0.5:
        return "[-1 0 0 %g] %g" % (x1/su, su), "[0 0 -1 %g] %g" % (z1/sv, sv)


def _flag_uv(n):
    x0, x1, _, _, z0, z1 = FLAG
    su, sv = (x1-x0)/256, (z1-z0)/512
    if abs(n[1]) > 0.5:
        s = -1 if n[1] > 0 else 1
        return "[%d 0 0 %g] %g" % (s, -s*(x0 if s > 0 else x1)/su, su), "[0 0 -1 %g] %g" % (z1/sv, sv)


FACEUV = {"gcs/board": _board_uv, "gcs/flag": _flag_uv}


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


def yprism(poly, y0, y1, tex):
    """Convex polygon in xz (counter-clockwise seen from -y), extruded y0..y1."""
    s = side([(x, y0, z) for x, z in poly], (0, -1, 0), tex)
    s += side([(x, y1, z) for x, z in poly], (0, 1, 0), tex)
    for i in range(len(poly)):
        a, b = poly[i], poly[(i+1) % len(poly)]
        n = (b[1]-a[1], 0, -(b[0]-a[0]))
        s += side([(a[0], y0, a[1]), (b[0], y0, b[1]), (b[0], y1, b[1])], n, tex)
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



def arcade_bay(W, ents, sgn, xin, xout, c, z0, r, top, roof):
    """One arched opening in an end wall (z0..top, half-width r) and its lit passage."""
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
    # Passage behind, sealed: warm cream corridor ending in lit glass doors with brass frames.
    pa, pb = sorted((xout, xout + sgn*ARCH_D))
    W(box(pa, c - r - WALL, z0 - WALL, pb, c + r + WALL, z0, TEX_FLOOR))
    W(box(pa, c - r - WALL, top, pb, c + r + WALL, top + roof, TEX_CREAM))
    W(box(pa, c - r - WALL, z0, pb, c - r, top, TEX_CREAM))
    W(box(pa, c + r, z0, pb, c + r + WALL, top, TEX_CREAM))
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


def build():
    world, ents = [], []
    W = world.append

    # Sealed outer hull (nodraw) so the interior can't leak while geometry is rough.
    O = 256
    X0, X1, Y0, Y1, Z1 = -HX-O-WALL, HX+O+WALL, -HY-WALL-64, HY+WALL+64, CROWN+WALL+64
    W(box(X0, Y0, -WALL-64, X1, Y1, -WALL, NODRAW))
    W(box(X0, Y0, Z1, X1, Y1, Z1+64, NODRAW))
    W(box(X0, Y0-64, -WALL-64, X1, Y0, Z1+64, NODRAW))
    W(box(X0, Y1, -WALL-64, X1, Y1+64, Z1+64, NODRAW))
    W(box(X0-64, Y0-64, -WALL-64, X0, Y1+64, Z1+64, NODRAW))
    W(box(X1, Y0-64, -WALL-64, X1+64, Y1+64, Z1+64, NODRAW))

    # Floor and long walls.
    W(box(-HX, -HY, -WALL, HX, HY, 0, TEX_FLOOR))
    W(box(-HX, -HY-WALL, -WALL, HX, -HY, SPRING, TEX_WALL))
    W(box(-HX, HY, -WALL, HX, HY+WALL, SPRING, TEX_WALL))

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
    win_w, win_z0, win_z1 = 26*FT, BALC_Z + 16*FT, SPRING + 20*FT
    win_zc = SPRING + 28*FT                 # the centre window rises higher, under the crown
    centres = [-31*FT, 0, 31*FT]            # close-set, as in the photos: narrow piers between
    for sgn in (-1, 1):
        xin, xout = sgn*HX, sgn*(HX+WALL)
        xa, xb = min(xin, xout), max(xin, xout)
        # Arcades: three arched openings under the balcony and three behind it, each into a
        # short sealed passage. Wall bands between them are solid.
        W(box(xa, -HY, -WALL, xb, HY, 0, TEX_WALL))
        W(box(xa, -HY, ARCH_TOP, xb, HY, BALC_Z, TEX_WALL))
        W(box(xa, -HY, BALC_Z + BARCH_H, xb, HY, win_z0, TEX_WALL))
        for z0, aw, ah in ((0, ARCH_W, ARCH_TOP), (BALC_Z, BARCH_W, BARCH_H)):
            top = z0 + ah
            aedges = [-HY] + [e for c in centres for e in (c-aw//2, c+aw//2)] + [HY]
            for j in range(0, len(aedges), 2):
                W(box(xa, aedges[j], z0, xb, aedges[j+1], top, TEX_WALL))
            for c in centres:
                arcade_bay(W, ents, sgn, xin, xout, c, z0, aw//2, top, min(WALL, BALC_Z - ARCH_TOP) if z0 == 0 else WALL)
        W(box(xa, -HY, win_zc, xb, HY, CROWN+WALL, TEX_WALL))
        W(box(xa, -HY, win_z1, xb, -win_w//2, win_zc, TEX_WALL))
        W(box(xa, win_w//2, win_z1, xb, HY, win_zc, TEX_WALL))
        edges = [-HY] + [e for c in centres for e in (c-win_w//2, c+win_w//2)] + [HY]
        for j in range(0, len(edges), 2):
            W(box(xa, edges[j], win_z0, xb, edges[j+1], win_z1, TEX_WALL))
        # Alcove behind: glowing back panel.
        xg0, xg1 = sorted((sgn*(HX+WALL+192), sgn*(HX+WALL+224)))
        W(box(xg0, -HY, win_z0-32, xg1, HY, win_zc+32, TEX_DIM))
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
            ents.append(ent("func_detail", solids=box(max(x-8*FT, -HX), ya, 0, min(x+8*FT, HX), yb, 3*FT, TEX_TRIM)))
        for k in range(BAYS):
            cx = -HX + k*bay + bay//2
            w = bay//2 - 10*FT
            ga, gb = inset(0, 2)
            ents.append(ent("func_detail", solids=box(cx-w, ga, BAY_Z0, cx+w, gb, SPRING-8*FT, TEX_DIM)))
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
                    ents.append(ent("func_detail", solids=yprism([outer[i], outer[i+1], inner[i+1], inner[i]], fa, fb, tex)))
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
        ents.append(ent("func_detail", solids=box(xa, -HY, BALC_Z-24, xb, HY, BALC_Z, TEX_TRIM)))
        rx = sgn*(HX-BALC_D)
        ra, rb = sorted((rx, rx+sgn*-16))
        for y0, y1 in ((-HY, -24*FT), (24*FT, HY)):
            ents.append(ent("func_detail", solids=box(ra, y0, BALC_Z, rb, y1, BALC_Z+42, TEX_TRIM)))

    # Double staircases: two flights per end, landing on the balcony.
    rise, run = 12, 18
    steps = BALC_Z // rise
    for sgn in (-1, 1):
        for yc in (-8*FT, 8*FT):
            y0, y1 = sorted((yc, yc + (1 if yc > 0 else -1)*14*FT))
            for k in range(steps):
                xs = sgn*(HX-BALC_D) - sgn*(steps-k)*run
                xa, xb = sorted((xs, xs+sgn*run))
                ents.append(ent("func_detail", solids=box(xa, y0, 0, xb, y1, (k+1)*rise, TEX_TRIM)))

    # Information booth with the four-faced clock above it.
    # Booth: cream marble base, dark glass with brass posts, gold cornice; the clock sits
    # on a brass column: four opal dials (30 u = 2.5 ft) under a gold cap and acorn finial.
    oct8 = lambda r: ngon(0, 0, r, 8, math.pi/8)
    det = lambda *a: ents.append(ent("func_detail", solids=prism(*a)))
    det(oct8(13*FT), 0, 3*FT, TEX_CREAM)
    det(oct8(12.5*FT), 3*FT, 8*FT, TEX_DIM)
    for x, y in oct8(13*FT):
        det(ngon(x, y, 6, 4, math.pi/4), 3*FT, 8*FT, TEX_GOLD)
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
        ents.append(ent("func_detail", solids=box(x-6*FT, -HY+0, 0, x-5*FT, -HY+3*FT, 14*FT, TEX_TRIM)))
    ents.append(ent("func_detail", solids=box(-100*FT, -HY, 14*FT, 100*FT, -HY+4*FT, 16*FT, TEX_TRIM)))
    bx0, bx1, bz0, bz1 = BOARD
    det([(bx0, -HY), (bx1, -HY), (bx1, -HY+16), (bx0, -HY+16)], bz0, bz1, "gcs/board", TEX_GOLD)

    # The flag hangs in the north centre bay from a gold pole bracketed to the wall.
    fx0, fx1, fy0, fy1, fz0, fz1 = FLAG
    ents.append(ent("func_detail", solids=box(fx0, fy0, fz0, fx1, fy1, fz1, "gcs/flag")))
    ents.append(ent("func_detail", solids=box(fx0-6, fy0-3, fz1, fx1+6, fy1+3, fz1+6, TEX_GOLD)))
    for x in (fx0+12, fx1-12):
        ents.append(ent("func_detail", solids=box(x-2, fy0, fz1+2, x+2, HY, fz1+6, TEX_GOLD)))

    # Chandeliers down both long sides: a gold rod from the cornice, a gold drum with
    # two tiers of glowing bulbs, a finial below; a light at each body.
    for x in range(-HX+300, HX-299, 450):
        for y in (-HY+120, HY-120):
            zc = 32*FT
            det(ngon(x, y, 2, 6), zc+48, SPRING, TEX_GOLD)
            det(ngon(x, y, 22, 8, math.pi/8), zc-6, zc+6, TEX_GOLD)
            det(ngon(x, y, 12, 8, math.pi/8), zc+6, zc+48, TEX_GOLD)
            det(ngon(x, y, 8, 8, math.pi/8), zc-30, zc-6, TEX_GOLD)
            det(ngon(x, y, 5, 4), zc-40, zc-30, TEX_GOLD)
            for tier, (r, z0) in enumerate(((30, zc+6), (18, zc+30))):
                for a in range(8):
                    t = 2*math.pi*(a + 0.5*tier)/8
                    det(ngon(x + r*math.cos(t), y + r*math.sin(t), 4, 6), z0, z0+8, TEX_BULB)
            ents.append(ent("light", (x, y, zc-48), _light="255 214 160 18"))
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
