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
SPRING = CROWN - HY                         # vault springs where a half-circle reaches the crown
WALL = 64
BALC_Z = 26 * FT                            # balcony floor height
BALC_D = 22 * FT                            # balcony depth from the end wall

TEX_FLOOR = "tile/tilefloor010a"
TEX_WALL = "stone/stonewall024a"
TEX_VAULT = "plaster/plasterwall041a"
TEX_TRIM = "stone/stonewall033a"
TEX_GLOW = "lights/white001"
NODRAW = "tools/toolsnodraw"

_id = [0]


def nid():
    _id[0] += 1
    return _id[0]


def sub(a, b): return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def dot(a, b): return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]


def axes_for(n):
    ax = max(range(3), key=lambda i: abs(n[i]))
    if ax == 2:
        return "[1 0 0 0] 0.25", "[0 -1 0 0] 0.25"
    if ax == 0:
        return "[0 1 0 0] 0.25", "[0 0 -1 0] 0.25"
    return "[1 0 0 0] 0.25", "[0 0 -1 0] 0.25"


def side(pts, n, tex):
    p1, p2, p3 = pts[0], pts[1], pts[2]
    # Source plane winding: outward normal = (p3-p1) x (p2-p1)
    if dot(cross(sub(p3, p1), sub(p2, p1)), n) < 0:
        p2, p3 = p3, p2
    f = lambda p: "(%g %g %g)" % p
    u, v = axes_for(n)
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


def xprism(poly, x0, x1, tex):
    """Convex polygon in yz (counter-clockwise seen from +x), extruded x0..x1."""
    s = side([(x1, y, z) for y, z in poly], (1, 0, 0), tex)
    s += side([(x0, y, z) for y, z in poly], (-1, 0, 0), tex)
    for i in range(len(poly)):
        a, b = poly[i], poly[(i+1) % len(poly)]
        n = (0, b[1]-a[1], -(b[0]-a[0]))
        s += side([(x0, a[0], a[1]), (x0, b[0], b[1]), (x1, b[0], b[1])], n, tex)
    return "solid\n{\n\t\"id\" \"%d\"\n%s}\n" % (nid(), s)


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

    # Barrel vault, segmented half-circle around the x axis.
    N = 20
    for i in range(N):
        a0, a1 = math.pi*i/N, math.pi*(i+1)/N
        r0, r1 = HY, HY+WALL
        p = lambda r, a: (round(r*math.cos(a)), round(SPRING + r*math.sin(a)))
        poly = [p(r1, a0), p(r1, a1), p(r0, a1), p(r0, a0)]
        W(xprism(poly, -HX, HX, TEX_VAULT))
    # Corners behind the vault so the wall tops are solid.
    W(box(-HX, -HY-WALL, SPRING, HX, -HY, SPRING+8, TEX_TRIM))
    W(box(-HX, HY, SPRING, HX, HY+WALL, SPRING+8, TEX_TRIM))

    # End walls with three tall arched windows (blockout: rectangular openings into glowing alcoves).
    win_w, win_z0, win_z1 = 22*FT, BALC_Z + 8*FT, SPRING + 30*FT
    centres = [-36*FT, 0, 36*FT]
    for sgn in (-1, 1):
        xin, xout = sgn*HX, sgn*(HX+WALL)
        xa, xb = min(xin, xout), max(xin, xout)
        W(box(xa, -HY, -WALL, xb, HY, win_z0, TEX_WALL))
        W(box(xa, -HY, win_z1, xb, HY, CROWN+WALL, TEX_WALL))
        edges = [-HY] + [e for c in centres for e in (c-win_w//2, c+win_w//2)] + [HY]
        for j in range(0, len(edges), 2):
            W(box(xa, edges[j], win_z0, xb, edges[j+1], win_z1, TEX_WALL))
        # Alcove behind: glowing back panel.
        xg0, xg1 = sorted((sgn*(HX+WALL+192), sgn*(HX+WALL+224)))
        W(box(xg0, -HY, win_z0-32, xg1, HY, win_z1+32, TEX_GLOW))
        for c in centres:
            ents.append(ent("light", (sgn*(HX+WALL+96), c, (win_z0+win_z1)/2),
                            _light="255 240 215 45", _quadratic_attn="0", _linear_attn="1", _fifty_percent_distance="900", _zero_percent_distance="2400"))
            ents.append(ent("light_spot", (sgn*(HX+WALL+150), c, win_z1-40),
                            angles="-38 %d 0" % (180 if sgn > 0 else 0), pitch="-38",
                            _light="255 235 200 225", _inner_cone="12", _cone="22", _exponent="1",
                            _distance="0", _fifty_percent_distance="2600", _zero_percent_distance="5200"))

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
    W_booth = ngon(0, 0, 13*FT, 8, math.pi/8)
    ents.append(ent("func_detail", solids=prism(W_booth, 0, 10*FT, TEX_TRIM)))
    ents.append(ent("func_detail", solids=prism(ngon(0, 0, 2*FT, 8, math.pi/8), 10*FT, 13*FT, TEX_TRIM)))
    ents.append(ent("func_detail", solids=prism(ngon(0, 0, 3*FT, 8, math.pi/8), 13*FT, 17*FT, TEX_GLOW)))
    ents.append(ent("light", (0, 0, 20*FT), _light="255 225 170 25"))

    # Ticket windows along the south wall: a row of recess frames.
    for k in range(-6, 7):
        x = k*16*FT
        ents.append(ent("func_detail", solids=box(x-6*FT, -HY+0, 0, x-5*FT, -HY+3*FT, 14*FT, TEX_TRIM)))
    ents.append(ent("func_detail", solids=box(-100*FT, -HY, 14*FT, 100*FT, -HY+4*FT, 16*FT, TEX_TRIM)))

    # Chandelier lights down both long sides, and soft fill under the vault.
    for x in range(-HX+300, HX-299, 450):
        for y in (-HY+120, HY-120):
            ents.append(ent("light", (x, y, 32*FT), _light="255 214 160 18"))
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
