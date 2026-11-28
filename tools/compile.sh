#!/bin/sh
# Full compile of src/gm_grand_central.vmf, pack src/materials into the BSP, copy into Garry's Mod maps.
set -e
G="${GMOD:-D:/SteamLibrary/steamapps/common/GarrysMod}"
cd "$(dirname "$0")/.."
. tools/gmod_lock.sh; gmod_lock_take   # shared GMod lock, released on exit
python tools/build_vmf.py
python tools/make_models.py
mkdir -p "$G/garrysmod/materials/gcs"
cp src/materials/gcs/* "$G/garrysmod/materials/gcs/"
# vbsp's exit code is lost in a pipe and it can fail while an old BSP stays on disk: remove it first
# and stop when vbsp reports a fatal error.
rm -f src/gm_grand_central.bsp
"$G/bin/vbsp.exe" -game "$G/garrysmod" src/gm_grand_central > src/vbsp.log 2>&1; tail -15 src/vbsp.log
if [ ! -f src/gm_grand_central.bsp ] || grep -q -i -E "bad normal|leaked|too many" src/vbsp.log; then echo "vbsp FAILED: see src/vbsp.log"; exit 1; fi
"$G/bin/vvis.exe" -game "$G/garrysmod" ${FAST:+-fast} src/gm_grand_central 2>&1 | tail -4
"$G/bin/vrad.exe" -game "$G/garrysmod" ${FAST:+-fast} -both src/gm_grand_central 2>&1 | tail -4
: > src/packlist.txt
for f in src/materials/gcs/*; do printf 'materials/gcs/%s\n%s\n' "$(basename "$f")" "$(cygpath -w "$PWD/$f" 2>/dev/null || echo "$PWD/$f")" >> src/packlist.txt; done
for f in src/materials/models/gcs/* src/models/gcs/*; do r="${f#src/}"; printf '%s\n%s\n' "$r" "$(cygpath -w "$PWD/$f" 2>/dev/null || echo "$PWD/$f")" >> src/packlist.txt; done
"$G/bin/bspzip.exe" -addlist src/gm_grand_central.bsp src/packlist.txt src/gm_grand_central.bsp 2>&1 | tail -2
cp src/gm_grand_central.bsp "$G/garrysmod/maps/"
ls -la src/gm_grand_central.bsp
