# HANDOFF: gm_grand_central

Status: in progress (Main Concourse blockout)
Updated: 2026-11-23

- Prompt: plans/2026-11-23-gcs-gmod-continue-prompt.md
- Plan: plans/gcs-gmod-plan.md
- Garry's Mod: D:/SteamLibrary/steamapps/common/GarrysMod; vbsp, vvis, vrad, bspzip, gmad, gmpublish are in its bin/.

## Done
- tools/build_vmf.py writes src/gm_grand_central.vmf: concourse at true scale, 20-segment barrel vault, end walls with three window openings and lit alcoves, balconies, two double staircases per end, octagonal information booth with clock block, ticket-window frames, lights, two spawns, cubemaps. Dev textures.
- tools/compile.sh: full vbsp/vvis/vrad (FAST=1 for quick), copies the BSP into garrysmod/maps. First compile: no leak, no missing materials.
- tools/lua/gcs_shots.lua: screenshot rig (render.Capture at set camera points, only when data/gcs_shots/go.txt exists). Not installed and never run: see below.

## Next
1. In-game screenshots. Auto mode refused the launch-and-capture command (install the Lua rig into garrysmod/lua/autorun, launch gmod.exe, then `taskkill /IM gmod.exe`). Either Mark allows it, or rewrite tools/shots.sh to kill by PID (quirkwright `qw.py pid`) and ask him first. Until then the map is compiled but unseen.
2. Measured references: find the HABS drawings for the vault section and the window/balcony heights; update refs/concourse-dimensions.md and the constants in build_vmf.py.
3. Hammer++ for hand checks (optional).

## Small rulings (flagged)
- Half-circle vault for now (real one is flatter).
- Stairs placed at both ends with 12 u risers / 18 u treads.

## Waiting on Mark
- Permission for the screenshot run (Next 1).
