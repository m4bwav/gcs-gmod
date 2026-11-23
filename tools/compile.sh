#!/bin/sh
# Full compile of src/gm_grand_central.vmf and copy into Garry's Mod maps.
set -e
G="D:/SteamLibrary/steamapps/common/GarrysMod"
cd "$(dirname "$0")/.."
python tools/build_vmf.py
"$G/bin/vbsp.exe" -game "$G/garrysmod" src/gm_grand_central 2>&1 | tail -15
"$G/bin/vvis.exe" -game "$G/garrysmod" ${FAST:+-fast} src/gm_grand_central 2>&1 | tail -4
"$G/bin/vrad.exe" -game "$G/garrysmod" ${FAST:+-fast} -both src/gm_grand_central 2>&1 | tail -4
cp src/gm_grand_central.bsp "$G/garrysmod/maps/"
ls -la src/gm_grand_central.bsp
