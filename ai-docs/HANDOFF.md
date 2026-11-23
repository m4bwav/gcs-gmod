# HANDOFF: gm_grand_central

Status: in progress (Main Concourse blockout)
Updated: 2026-11-23

- Prompt: plans/2026-11-23-gcs-gmod-continue-prompt.md
- Plan: plans/gcs-gmod-plan.md
- Garry's Mod: D:/SteamLibrary/steamapps/common/GarrysMod; vbsp, vvis, vrad, bspzip, gmad, gmpublish are in its bin/.

## Done
- tools/build_vmf.py writes src/gm_grand_central.vmf: concourse at true scale, 20-segment barrel vault, end walls with three window openings and lit alcoves, balconies, two double staircases per end, octagonal information booth with clock block, ticket-window frames, lights, two spawns, cubemaps. Dev textures.
- tools/compile.sh: full vbsp/vvis/vrad (FAST=1 for quick), copies the BSP into garrysmod/maps. First compile: no leak, no missing materials.
- Screenshot rig works: tools/shots.sh copies tools/lua/gcs_shots.lua into garrysmod/lua/autorun/client, writes data/gcs_shots_go.txt, launches gmod.exe; the Lua shows 6 fixed cameras, render.Capture to data/gcs_shots/, then quits. Fallback kill is by PID (quirkwright qw.py pid), never by name. Output: shots/<stamp>/ plus contact.jpg.
- Launching gmod.exe directly needs steam_appid.txt (4000) in the GarrysMod folder, else a "Failed to initialize Steamworks API" dialog hangs it. shots.sh writes it.
- Lights cut about 3x and an env_tonemap_controller added: shots/20261123-1135 reads as the concourse, still bright because of the yellow dev textures.

- Stock HL2 surfaces in (floor stone/marblefloor001c, walls plaster/plasterwall005a, vault plaster/plasterceiling005a, trim plaster/plasterwall003a); lights cut ~3x again; logic_auto clamps tonemap exposure 0.5-1.2, bloom 0.25. shots/20261123-1444/contact.jpg reads as a stone hall, exposure good.

- Surfaces v2 (stock HL2 only): walls stone/stonewall024a (cream ashlar), floor tile/tilefloor010a (warm marble squares), vault plaster/plasterwall041a (pale green-blue stand-in until the zodiac texture), trim stone/stonewall033a. Lights halved again. shots/20261123-1716 reads as Grand Central. tools/texsheet.py makes contact sheets of stock materials (`python tools/texsheet.py out.jpg <regex>`, needs pip srctools); sheets in shots/tex/.

- Photo matching: 10 Commons photos in refs/photos (tools/fetch_refs.py, credits in refs/SOURCES.md, CC BY/BY-SA need Workshop attribution). Custom materials src/materials/gcs/*.vmt tint stock HL2 textures to photo-sampled colours; compile.sh copies them to garrysmod/materials and packs them into the BSP with bspzip. tools/compare.py <shotdir> writes compare.jpg (shot beside photo per viewpoint). shots/20261123-1731/compare.jpg: colours now read alike (teal vault, honey walls, pale floor, sky-blue windows).

## Next
1. Geometry gaps the compare sheet shows: wall pilasters and deep window bays along the long walls, gilded cornice band at vault springline, lunette (half-moon) clerestory windows cut into the vault, mullion grid in the end windows, flatter vault. Then photo-derived textures proper (marble floor, ashlar, zodiac ceiling; comfyui-gen, no Krea 2) and recompare.
2. Clock block is a grey box (booth clock model, polywright).
3. Measured references: HABS drawings for vault section and window/balcony heights; update refs/concourse-dimensions.md and build_vmf.py.
4. Chandeliers (polywright), ticket-window departure board, flags; then the zodiac ceiling.
5. Hammer++ for hand checks (optional).

## Small rulings (flagged)
- Half-circle vault for now (real one is flatter).
- Stairs placed at both ends with 12 u risers / 18 u treads.
- Light levels (after surfaces v2): window point 45, window spot 225, booth 25, chandeliers 18, vault fill 10.
- An installed addon prints "FNaF SB Models are Pre-Caching" over the shots; harmless, ignore or launch with addons off later.

## Waiting on Mark
- Nothing yet. Look-and-feel sign-off comes once the concourse has real surfaces.

## Directive from Mark (2026-11-23)
- Use and improve every plugin involved (polywright, modwright, photowright, artwright, comfyui-gen...); fix gaps in the plugins' own repos.
- Get textures right from real photos (licensed/public domain, sources in refs/); after each compile, put screenshots beside photos from matching viewpoints and iterate until they match. This comes before item 1 below.
