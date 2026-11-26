#!/bin/sh
# Generate the nav mesh for nextbots and NPCs: launch GMod on gm_grand_central with sv_cheats,
# tools/lua/gcs_nav.lua runs nav_generate (nav_quicksave 1), the map reloads, the Lua writes the
# area count and quits. Copies maps/gm_grand_central.nav to src/ (package.sh ships it). Run after compile.sh.
G="${GMOD:-D:/SteamLibrary/steamapps/common/GarrysMod}"
QW="C:/Users/m4bwa/.claude/plugins/cache/mark-local/quirkwright/0.2.1/skills/quirkwright/scripts/qw.py"
cd "$(dirname "$0")/.."
D="$G/garrysmod/data"
echo 4000 > "$G/steam_appid.txt"
mkdir -p "$G/garrysmod/lua/autorun/server" "$D"
cp tools/lua/gcs_nav.lua "$G/garrysmod/lua/autorun/server/gcs_nav.lua"
rm -rf "$D/gcs_nav" "$G/garrysmod/maps/gm_grand_central.nav"; echo go > "$D/gcs_nav_go.txt"
"$G/gmod.exe" -windowed -w 1280 -h 720 -novid -nojoy -condebug +sv_cheats 1 +map gm_grand_central &
for n in $(seq 1 240); do [ -f "$D/gcs_nav/done.txt" ] && break; sleep 5; done
sleep 5
PID=$(python "$QW" pid gmod.exe 2>/dev/null | python -c "import json,sys; m=json.load(sys.stdin)[\"matches\"]; print(m[0].get(\"pid\",\"\") if m else \"\")")
[ -n "$PID" ] && taskkill //PID "$PID" //F
rm -f "$G/garrysmod/lua/autorun/server/gcs_nav.lua" "$D/gcs_nav_go.txt"
cat "$D/gcs_nav/done.txt" 2>/dev/null || { echo "no nav: see $G/garrysmod/console.log"; exit 1; }
cp "$G/garrysmod/maps/gm_grand_central.nav" src/
ls -la src/gm_grand_central.nav
