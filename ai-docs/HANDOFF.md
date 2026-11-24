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

- Geometry v2: vault is a flattened half-ellipse (VRISE 40 ft), 5 bays per long wall with pilasters, dark gridded bay windows (gcs/window_dim, gcs/mullion), gold cornice (gcs/gold) over a trim band at the springline, a framed lunette per bay, mullion grids in the end windows. shots/20261123-1737/compare.jpg and pair.jpg.

- Geometry v3: end windows tall (top SPRING+16 ft) with arched heads (triangle-fan spandrels), dark glass; great end arch soffit (6 ft deep, gold inner edge) following the vault; pilasters 14 ft wide x 5 ft deep; floor texture scale 0.15. shots/20261123-1743 (compare.jpg).

- Marble floor: tools/make_floor.py writes a procedural 512 px VTF (2x2 rose-grey slabs, veins, joints; colour from the GCT_east_windows floor) to src/materials/gcs/floor_marble.vtf, gcs/floor uses it with a faint cubemap sheen; scale 0.1875 = 4 ft slabs. Checkering gone: shots/20261123-1747.

- Walls and vault: tools/make_walls.py writes procedural wall_ashlar.vtf (honey-cream limestone, 8 staggered courses x 3 blocks, light joints) and vault_sky.vtf (dark teal, gold stars); gcs/wall and gcs/vault use them. shots/20261123-1753 compare: walls and vault now read like the photos.

- Zodiac vault: tools/make_vault.py writes vault_mural.vtf (2048x1024, green field, Milky Way, ecliptic and equator as double gold lines with ticks, 12 stick-figure constellations); build_vmf.py maps it once over the vault's inner faces with per-segment UVs (xprism uvs=). gcs/vault uses it. shots/20261123-1757: vault reads like the photo.

- Lunettes: stepped cream hood (gcs/cream, tinted plaster003a, r 16-23 ft) with a gold outer edge; ashlar now 8x4 blocks (no wrap seam). shots/20261123-1803.

- Booth and clock: tools/make_clock.py writes clock_face.vtf (opal dial, black ticks and hands, brass bezel); gcs/clock is UnlitGeneric. Booth now cream base, dark glass with brass posts, gold cornice; brass column carries a 30 u four-faced clock, gold cap and acorn. build_vmf.py USHIFT centres the dial. New `clock` camera in gcs_shots.lua. shots/20261123-1807.

- Chandeliers: 16 brush chandeliers (gold rod from cornice, drum, two tiers of 8 glowing bulbs gcs/bulb, finial), one light each, down both long walls. Clock dials unmirrored (all four read 10:08). shots/20261123-1811.

- Departure board and flag: tools/make_board.py writes board.vtf (black LED board, dot-matrix rows; gcs/board UnlitGeneric) and flag.vtf (vertical US flag; gcs/flag). Board 40x10 ft over the ticket windows in the centre south bay; flag 20x38 ft hangs from the crown on gold rods at x=+24 ft. build_vmf.py FACEUV maps a texture once over a brush face. New cameras board, flag. shots/20261123-1818 (flag in 20261123-1815).

## Next
1. Zodiac figures could get drawn outlines (real ceiling has figure drawings, not only stick lines); lunette hoods could get relief carving (normal map or more steps).
2. Booth glass is flat blue-grey; real booth has brass grilles and ticket windows.
3. Measured references: HABS drawings for vault section and window/balcony heights; update refs/concourse-dimensions.md and build_vmf.py.
4. Board glyphs are stand-in dot clusters, not letters; chandeliers could become a polywright model with globes later.
5. Hammer++ for hand checks (optional).

## Small rulings (flagged)
- Zodiac constellations are simplified stick figures, not the real ceiling's figure drawings; band curves are stylised sinusoids.
- Vault rise 40 ft, estimated from photos (check against the HABS section).
- Flag placement (x=+24 ft, crown, 20x38 ft) and board size estimated, not measured.
- Stairs placed at both ends with 12 u risers / 18 u treads.
- Light levels (after surfaces v2): window point 45, window spot 225, booth 25, chandeliers 18, vault fill 10.
- An installed addon prints "FNaF SB Models are Pre-Caching" over the shots; harmless, ignore or launch with addons off later.

## Waiting on Mark
- Nothing yet. Look-and-feel sign-off comes once the concourse has real surfaces.

## Directive from Mark (2026-11-23)
- Use and improve every plugin involved (polywright, modwright, photowright, artwright, comfyui-gen...); fix gaps in the plugins' own repos.
- Get textures right from real photos (licensed/public domain, sources in refs/); after each compile, put screenshots beside photos from matching viewpoints and iterate until they match. This comes before item 1 below.
