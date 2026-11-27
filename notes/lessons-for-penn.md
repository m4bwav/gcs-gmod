# Lessons from gm_grand_central for the Penn Station map

Written at the end of the Grand Central chain (session 59, 2026-11-26, release 0.19.0). Details and dates are in ai-docs/HANDOFF.md and ai-docs/log.md.

## Budget
- vbsp caps a map at 65,536 unique vertices, and the world model has its own t-junction cap ("Too many t-junctions"). Grand Central hit both by the exterior (61,765 verts). Check after every compile with `GarrysMod/bin/vbspinfo.exe` and log verts, faces and BSP size.
- Put each area's decoration in one func_brush, never func_detail on the world.
- Draw grids, grilles, mullions, balusters, lettering and cornice brackets as textures (alpha-tested or painted), mapped per face. Converting the end-window mullions and cornice brackets to textures saved about 3,500 verts each.
- Props (chandeliers, statues, railings, taxis, benches) are MDL models: tools/make_models.py writes SMD + QC in Python and compiles them with bin/studiomdl.exe. Models don't count against the vertex cap. Converting the chandeliers alone saved 12,000 verts.
- Final Grand Central: 49,703 verts, 31,000 faces, 107.5 MB BSP, nine chambers plus the main areas in one map.

## Build and compile
- Generate the VMF from a script (build_vmf.py): constants per area, helpers for arches, vaults, bays. Hand edits get lost.
- compile.sh deletes the old BSP first and stops on vbsp errors; otherwise vvis/vrad run on the stale BSP and a broken build ships (0.7.0 did).
- Never run two compiles or two GMod launches at once: the second GMod gives 20 fps wireframe shots.
- A zero-height brush gives "bad normal". A light inside a func_detail globe goes dark; put it below.
- Repo text is LF; write files from Python with newline='' or the diffs become whole-file rewrites.

## Screenshots and compare
- shots.sh launches gmod.exe with steam_appid.txt (4000) next to it, copies a client Lua autorun that moves the player to each camera (else brush entities outside the PVS never draw), render.Capture, then quits. Kill by PID only. CAMS="a b" shoots a subset. Don't wrap it in a short timeout: addon load can take 5 minutes.
- compare.py puts each shot next to a reference photo from the same viewpoint; fix the worst mismatch first. Photos from Wikimedia Commons with licences in refs/SOURCES.md.

## Release
- nav.sh builds the nav mesh in GMod (about 8 minutes); rerun after floor changes.
- package.sh builds the .gma (build/ is per worktree), runs gmpublish update and workshop_update.py for the description and previews. AddItemPreviewFile appends, so old previews pile up.
- Each release: README, wiki (docs/wiki pushed to the .wiki.git), Workshop, version tag and GitHub release with the .gma.

## Chain running
- One worktree per session; the stop check must read HANDOFF.md from origin/main, not the shared clone.
- Two chain drivers for one chain ran the same session twice. Check for a running chain_loop before starting one.
