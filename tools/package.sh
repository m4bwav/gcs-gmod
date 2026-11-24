#!/bin/sh
# Package the compiled BSP as a .gma and update Workshop item 3845077025.
# Run tools/compile.sh first. Usage: sh tools/package.sh "change note" [preview.jpg ...]
# DRY=1 builds the .gma only.
set -e
G="${GMOD:-D:/SteamLibrary/steamapps/common/GarrysMod}"
ID="${WORKSHOP_ID:-3845077025}"
cd "$(dirname "$0")/.."
NOTE="${1:-Update}"
[ $# -gt 0 ] && shift
rm -rf build/addon && mkdir -p build/addon/maps
cp src/gm_grand_central.bsp build/addon/maps/
cat > build/addon/addon.json <<'EOF'
{
	"title": "gm_grand_central",
	"type": "map",
	"tags": ["scenic", "realism"],
	"ignore": []
}
EOF
"$G/bin/gmad.exe" create -folder build/addon -out build/gm_grand_central.gma | tail -2
ls -la build/gm_grand_central.gma
[ -n "$DRY" ] && exit 0
"$G/bin/gmpublish.exe" update -id "$ID" -addon build/gm_grand_central.gma -changes "$NOTE" | tail -3
python tools/workshop_update.py "$ID" --desc workshop/description.txt ${1:+--preview "$@"}
