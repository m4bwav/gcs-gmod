#!/bin/sh
# Escalator ride test: launch GMod on gm_grand_central, tools/lua/gcs_walk_sv.lua rides each MetLife
# escalator lane with no input and walks against each, and writes PASS/FAIL lines. Run after compile.sh.
G="${GMOD:-D:/SteamLibrary/steamapps/common/GarrysMod}"
cd "$(dirname "$0")/.."
. tools/gmod_lock.sh; gmod_lock_take   # shared GMod lock, released on exit
D="$G/garrysmod/data"
echo 4000 > "$G/steam_appid.txt"
mkdir -p "$G/garrysmod/lua/autorun/server" "$D"
cp tools/lua/gcs_walk_sv.lua "$G/garrysmod/lua/autorun/server/gcs_walk_sv.lua"
rm -rf "$D/gcs_walk"; echo go > "$D/gcs_walk_go.txt"
gmod_snapshot
"$G/gmod.exe" -windowed -w 1280 -h 720 -novid -nojoy -condebug +sv_cheats 1 +map gm_grand_central &
for n in $(seq 1 ${WAIT:-180}); do [ -f "$D/gcs_walk/done.txt" ] && break; sleep 5; done
sleep 2
gmod_kill_own
rm -f "$G/garrysmod/lua/autorun/server/gcs_walk_sv.lua" "$D/gcs_walk_go.txt"
cat "$D/gcs_walk/result.txt" 2>/dev/null || { echo "no walk result: see $G/garrysmod/console.log"; exit 1; }
! grep -q FAIL "$D/gcs_walk/result.txt"
