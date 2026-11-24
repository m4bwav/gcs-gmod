#!/bin/sh
# Launch GMod on gm_grand_central, let tools/lua/gcs_shots.lua capture the cameras,
# copy the JPGs into shots/. UNCAP=1 lifts the frame cap (fps_max 0, vsync off) for the fps log. The Lua quits the game; fallback kill is by PID only.
G="${GMOD:-D:/SteamLibrary/steamapps/common/GarrysMod}"
QW="C:/Users/m4bwa/.claude/plugins/cache/mark-local/quirkwright/0.2.1/skills/quirkwright/scripts/qw.py"
cd "$(dirname "$0")/.."
D="$G/garrysmod/data"
echo 4000 > "$G/steam_appid.txt"
cp tools/lua/gcs_shots.lua "$G/garrysmod/lua/autorun/client/gcs_shots.lua"
EXTRA=""; [ -n "$UNCAP" ] && EXTRA="+fps_max 0 +mat_vsync 0"
mkdir -p "$D"; rm -rf "$D/gcs_shots"; echo go > "$D/gcs_shots_go.txt"
"$G/gmod.exe" -windowed -w 1600 -h 900 -novid -nojoy -condebug $EXTRA +map gm_grand_central &
for n in $(seq 1 60); do [ -f "$D/gcs_shots/done.txt" ] && break; sleep 5; done
sleep 5
PID=$(python "$QW" pid gmod.exe 2>/dev/null | python -c "import json,sys; m=json.load(sys.stdin)[\"matches\"]; print(m[0].get(\"pid\",\"\") if m else \"\")")
[ -n "$PID" ] && taskkill //PID "$PID" //F
rm -f "$G/garrysmod/lua/autorun/client/gcs_shots.lua" "$D/gcs_shots_go.txt"
stamp=$(date +%Y%m%d-%H%M); mkdir -p "shots/$stamp"
cp "$D"/gcs_shots/*.jpg "$D"/gcs_shots/fps.txt "shots/$stamp/" 2>/dev/null; ls "shots/$stamp"
cat "shots/$stamp/fps.txt" 2>/dev/null
