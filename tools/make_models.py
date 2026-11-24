"""Write props as SMD + QC and compile them to MDL with Garry's Mod's studiomdl.

Models do not count against vbsp's 65,536 unique-vertex cap, so round, many-sided
decoration (chandeliers, globes) belongs here instead of in brushes.

    python tools/make_models.py          # writes src/modelsrc/, compiles into src/models/

Output: src/models/gcs/<name>.{mdl,vvd,vtx...}, src/materials/models/gcs/*.vmt.
compile.sh copies both into garrysmod/ and packs them into the BSP.
"""
import math
import os
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
G = Path(os.environ.get("GMOD", "D:/SteamLibrary/steamapps/common/GarrysMod"))
SRC = ROOT / "src" / "modelsrc"
MAT = ROOT / "src" / "materials" / "models" / "gcs"

FT = 12
SPRING = 125 * FT - 40 * FT     # concourse springline, matches build_vmf.py
CHAND_Z = 32 * FT               # chandelier body height above the concourse floor

# Model materials: VertexLitGeneric twins of the brush materials.
VMTS = {
    "gold": '"VertexLitGeneric"\n{\n\t"$basetexture" "stone/stonewall033a"\n\t"$color2" "[1.25 0.95 0.45]"\n'
            '\t"$envmap" "env_cubemap"\n\t"$envmaptint" "[0.25 0.2 0.1]"\n\t"$surfaceprop" "metal"\n}\n',
    "bulb": '"UnlitGeneric"\n{\n\t"$basetexture" "lights/white002"\n\t"$color2" "[1.0 0.86 0.6]"\n\t"$model" "1"\n}\n',
}


class Mesh:
    def __init__(self):
        self.tris = []      # (material, [(pos, normal, uv)] * 3)

    def quad(self, mat, a, b, c, d):
        # Corners counter-clockwise seen from outside; each item (pos, normal, uv).
        self.tris.append((mat, [a, b, c]))
        self.tris.append((mat, [a, c, d]))

    def lathe(self, mat, prof, cx, cy, cz, n=16):
        """Revolve a profile [(r, z)] from bottom to top about the vertical axis at (cx, cy)."""
        for i in range(len(prof) - 1):
            (r0, z0), (r1, z1) = prof[i], prof[i + 1]
            dr, dz = r1 - r0, z1 - z0
            ln = math.hypot(dr, dz) or 1
            nr, nz = dz / ln, -dr / ln            # outward normal of this band in (r, z)
            for j in range(n):
                t0, t1 = 2 * math.pi * j / n, 2 * math.pi * (j + 1) / n
                def v(r, z, t, u):
                    p = (cx + r * math.cos(t), cy + r * math.sin(t), cz + z)
                    nrm = (nr * math.cos(t), nr * math.sin(t), nz)
                    return (p, nrm, (u, z / 64.0))
                self.quad(mat, v(r0, z0, t0, j / n), v(r0, z0, t1, (j + 1) / n),
                          v(r1, z1, t1, (j + 1) / n), v(r1, z1, t0, j / n))

    def cyl(self, mat, cx, cy, r, z0, z1, n=16):
        # Closed cylinder: bottom cap, side, top cap as a lathe profile.
        self.lathe(mat, [(0, z0), (r, z0), (r, z1), (0, z1)], cx, cy, 0, n)

    def sphere(self, mat, cx, cy, cz, r, n=10):
        prof = [(r * math.sin(math.pi * k / n), -r * math.cos(math.pi * k / n)) for k in range(n + 1)]
        self.lathe(mat, prof, cx, cy, cz, 2 * n)

    def smd(self):
        out = ["version 1", "nodes", '0 "root" -1', "end", "skeleton", "time 0", "0 0 0 0 0 0 0", "end", "triangles"]
        for mat, vs in self.tris:
            out.append(mat)
            for p, nrm, uv in vs:
                out.append("0 %.3f %.3f %.3f %.4f %.4f %.4f %.4f %.4f" % (*p, *nrm, *uv))
        out.append("end")
        return "\n".join(out) + "\n"


def chandelier():
    """Concourse chandelier, origin at the body centre: gold rod up to the cornice, a gold drum
    with two tiers of eight glowing globes, a finial and a big bottom globe."""
    m = Mesh()
    m.cyl("gold", 0, 0, 2, 48, SPRING - CHAND_Z, 8)
    m.lathe("gold", [(0, -36), (5, -36), (5, -30), (8, -30), (8, -6), (22, -6), (24, 0), (22, 6),
                     (12, 6), (12, 44), (14, 48), (0, 48)], 0, 0, 0, 24)
    for tier, (r, z) in enumerate(((30, 11), (18, 35))):
        for a in range(8):
            t = 2 * math.pi * (a + 0.5 * tier) / 8
            x, y = r * math.cos(t), r * math.sin(t)
            m.cyl("gold", x * 0.5, y * 0.5, 1.2, z - 6, z - 4, 6)   # arm stub under each globe
            m.sphere("bulb", x, y, z, 5, 6)
    m.sphere("bulb", 0, 0, -46, 10, 10)
    return m


MODELS = {"chandelier": chandelier}


def build():
    SRC.mkdir(parents=True, exist_ok=True)
    MAT.mkdir(parents=True, exist_ok=True)
    for name, text in VMTS.items():
        (MAT / f"{name}.vmt").write_text(text, encoding="ascii", newline="\n")
    gmat = G / "garrysmod" / "materials" / "models" / "gcs"
    gmat.mkdir(parents=True, exist_ok=True)
    for f in MAT.glob("*.vmt"):
        shutil.copy(f, gmat)
    out = ROOT / "src" / "models" / "gcs"
    out.mkdir(parents=True, exist_ok=True)
    for name, fn in MODELS.items():
        (SRC / f"{name}.smd").write_text(fn().smd(), encoding="ascii", newline="\n")
        (SRC / f"{name}.qc").write_text(
            f'$modelname "gcs/{name}.mdl"\n$body body "{name}.smd"\n$cdmaterials "models/gcs/"\n'
            f'$staticprop\n$surfaceprop "metal"\n$sequence idle "{name}.smd"\n', encoding="ascii", newline="\n")
        r = subprocess.run([str(G / "bin" / "studiomdl.exe"), "-game", str(G / "garrysmod"), "-nop4",
                            str(SRC / f"{name}.qc")], capture_output=True, text=True)
        if r.returncode or "ERROR" in r.stdout:
            raise SystemExit(r.stdout[-2000:] + r.stderr[-1000:])
        built = G / "garrysmod" / "models" / "gcs"
        for f in built.glob(f"{name}.*"):
            shutil.copy(f, out)
        print("built", name, sorted(p.name for p in out.glob(f"{name}.*")))


if __name__ == "__main__":
    build()
