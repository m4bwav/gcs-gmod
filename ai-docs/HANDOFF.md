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

- End walls v2: end windows 28 ft wide at y=0/±38 ft, sill BALC_Z+6 ft, 7 mullions; paired cream engaged columns with gold capitals on the piers between windows. shots/20261123-1821.

- End wall arcade: three 18 ft arched openings (cream archivolts and jambs) under each balcony into sealed 16 ft passages with dim glass at the back; great end arch soffit uses gcs/coffer (procedural 2x2 cream coffers, gold rosettes, tools/make_walls.py); ashlar at scale 0.5 (2.7 x 5.3 ft blocks) with softer joints. shots/20261123-1826.

- Arcade passages lit: cream walls and ceiling, amber glass doors (gcs/door_glow) in brass frames with transom, pendant lamp, warm lights; new camera arcade_west. shots/20261123-1829.

- Balcony arcade: three 14x16 ft arched openings behind each balcony into lit passages (shared arcade_bay() in build_vmf.py); end windows now start at BALC_Z+20 ft; paired end columns stand on the balcony floor. New camera balc_arcade. shots/20261123-1836.

- east_balcony vs photo: long-wall bay windows raised to BAY_Z0 = 42 ft (stone lower storey). shots/20261123-1840/pair_east.jpg.

- End windows taller (sill BALC_Z+16 ft; centre window head SPRING+26 ft, sides SPRING+16 ft), balcony arcade 14 ft high, great end arch soffit 11 ft deep, modillion band (cream brackets every 2 ft) under an overhanging gold crown on both long walls. shots/20261123-1844.

- vault_up camera moved out of the booth clock column (was black); ashlar base colour paler cream [228 208 172] to match photos. shots/20261123-1847.

- End windows close-set (26 ft wide at y=0/�31 ft, heads SPRING+20/+28 ft), window spots softened (110, cone 65), flag moved to the north centre bay hanging from a gold pole (camera flag looks north). shots/20261123-1851.

- Flag horizontal like the photo: 38x20 ft, stripes across, union upper left (flag.vtf 512x256). shots/20261123-1857.

- Stairs and booth: each flight has solid cream balustrades with a brass handrail and newel posts at the foot; booth glass has a brass grille (two mullions per face, counter ledge at 4 ft, top rail at 7 ft). shots/20261123-1901.

## Next
0. From shots/20261123-1851 compare: the end windows are still a little short of the arch.
1. Zodiac figures could get drawn outlines (real ceiling has figure drawings, not only stick lines); lunette hoods could get relief carving (normal map or more steps).
2. Booth glass is still flat blue-grey behind the new grille; could get ticket-window openings or a lit interior.
3. Measured references: HABS drawings for vault section and window/balcony heights; update refs/concourse-dimensions.md and build_vmf.py.
4. Board glyphs are stand-in dot clusters, not letters; chandeliers could become a polywright model with globes later.
5. Hammer++ for hand checks (optional).

## Small rulings (flagged)
- Zodiac constellations are simplified stick figures, not the real ceiling's figure drawings; band curves are stylised sinusoids.
- Vault rise 40 ft, estimated from photos (check against the HABS section).
- Bay window bottom 42 ft estimated from photo.
- Balcony arcade 14x14 ft openings, window sill BALC_Z+16 ft, centre end window head SPRING+26 ft are estimated from photos.
- Flag placement (north centre bay, 38x20 ft horizontal) and board size estimated, not measured.
- Stairs placed at both ends with 12 u risers / 18 u treads.
- Light levels (after surfaces v2): window point 45, window spot 225, booth 25, chandeliers 18, vault fill 10.
- An installed addon prints "FNaF SB Models are Pre-Caching" over the shots; harmless, ignore or launch with addons off later.

## Waiting on Mark
- Nothing yet. Look-and-feel sign-off comes once the concourse has real surfaces.

## Directive from Mark (2026-11-23)
- Use and improve every plugin involved (polywright, modwright, photowright, artwright, comfyui-gen...); fix gaps in the plugins' own repos.
- Get textures right from real photos (licensed/public domain, sources in refs/); after each compile, put screenshots beside photos from matching viewpoints and iterate until they match. This comes before item 1 below.
