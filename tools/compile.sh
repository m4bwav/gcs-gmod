#!/bin/sh
# Full compile of src/gm_grand_central.vmf, pack src/materials into the BSP, copy into Garry's Mod maps.
set -e
G="D:/SteamLibrary/steamapps/common/GarrysMod"
cd "$(dirname "$0")/.."
python tools/build_vmf.py
mkdir -p "$G/garrysmod/materials/gcs"
cp src/materials/gcs/* "$G/garrysmod/materials/gcs/"
"$G/bin/vbsp.exe" -game "$G/garrysmod" src/gm_grand_central 2>&1 | tail -15
"$G/bin/vvis.exe" -game "$G/garrysmod" ${FAST:+-fast} src/gm_grand_central 2>&1 | tail -4
"$G/bin/vrad.exe" -game "$G/garrysmod" ${FAST:+-fast} -both src/gm_grand_central 2>&1 | tail -4
: > src/packlist.txt
for f in src/materials/gcs/*; do printf 'materials/gcs/%s\n%s\n' "$(basename "$f")" "$(cygpath -w "$PWD/$f" 2>/dev/null || echo "$PWD/$f")" >> src/packlist.txt; done
"$G/bin/bspzip.exe" -addlist src/gm_grand_central.bsp src/packlist.txt src/gm_grand_central.bsp 2>&1 | tail -2
cp src/gm_grand_central.bsp "$G/garrysmod/maps/"
ls -la src/gm_grand_central.bsp
