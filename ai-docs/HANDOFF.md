# HANDOFF: gm_grand_central

Status: in progress (0.14.0 released 2026-11-26: Grand Central Madison; Workshop 3845077025, GitHub v0.6.0)
Updated: 2026-11-24

- Prompt: plans/2026-11-25-gcs-gmod-60x-continue-prompt.md (60-session chain; then plans/2026-11-25-penn-gmod-60x-continue-prompt.md)
- Chain: session 10 of 60 (started 2026-11-25)
- Budget 2026-11-25 (vbspinfo, 0.6.0): unique verts 46,661/65,536 (71%), faces 41%, planes 22%, brushes 6%, BSP 59.6 MB of 150 MB.
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

- End windows fill the great arch: centre head SPRING+29.5 ft (inner arch edge is +30), sides SPRING+22 ft. shots/20261123-1905.

- Window glass: tools/make_window.py writes window_glass.vtf (4x4 pale panes, dark muntins, tiles at scale 0.25); gcs/window_glass (UnlitGeneric, $color 1.15) on end and long-wall bay windows; booth keeps gcs/window_dim. Windows now read pale and gridded like the photos. shots/20261123-1911.

- Sun shafts: tools/make_shaft.py writes shaft.vtf (soft-edged streaky beam, fades in past the balcony and out toward the floor); gcs/shaft is additive UnlitGeneric $color 2.4. One func_illusionary yprism beam per end window at the spotlight pitch (38 deg), 0.55 x window width, y faces nodraw. shots/20261123-1931 (compare.jpg).

- Booth interior: glass is a thin translucent ring (gcs/booth_glass, UnlitGeneric alpha 0.28); inside a cream counter with brass top under the glass, a cream cabinet core under the clock column, two warm lights. Reads see-through like the photos. shots/20261123-1935.

- Zodiac figures: each constellation sits on a gold-outlined limb silhouette (stick figure thickened, rounded, faint wash) in tools/make_vault.py. shots/20261123-1939/vault_up.jpg.

- Board lettering: make_board.py draws a real 5x7 dot-matrix font (round LEDs, unlit cells faint); legible in shots/20261123-1943/board.jpg.

- Lunette relief: alternate voussoirs of the middle hood ring stand 6 u proud, cream keystone at each crown. shots/20261123-1949.

- Booth interior lights 30 -> 55, warmer (reads lit through the glass). shots/20261123-1957.

- Flag 48x25 ft (sourced length, Gothamist; 1.9:1), spans the north centre bay. shots/20261123-2003/flag.jpg.

- Ticket windows: each of the 12 south-wall windows has a cream counter with brass top, dim glass behind a brass grille (bars every 1 ft), gold rail and cream lintel. shots/20261123-2007/board.jpg.

- TICKETS plaques: bronze plaque with gold 5x7 lettering centred on each ticket-window lintel (tickets.vtf from tools/make_board.py, gcs/tickets lit; FACEUV _tickets_uv maps one strip per 16 ft pitch, u flipped). shots/20261123-2014/tickets_crop.jpg.

- Ticket-window reveals: 10 u cream marble jambs frame each window's glass. shots/20261123-2022/board.jpg.

- Ticket-window arched heads: segmental cream spandrels (1.5 ft rise) between the reveals. shots/20261123-2027/board.jpg.

- Ticket-hall lamps: brass bracket lamp with a glowing globe on each ticket-window pier (13), dim warm light each (8). shots/20261123-2031/board.jpg.

- Balconies: cream marble parapets with a brass handrail, cream balcony slabs and stair treads (were grey stock trim). shots/20261123-2041/east_balcony.jpg.

- Cream marble: tools/make_walls.py writes cream_marble.vtf (seamless pale marble, thin warm veins); gcs/cream uses it (was stained stock plaster that read muddy on stair balustrades); pilaster plinths cream instead of grey trim. shots/20261123-2047/floor_east.jpg.

- Arcade passages: cream barrel vault continuing each opening arch (was a flat dark ceiling). shots/20261123-2052/arcade_west.jpg.

- arcade_west camera moved onto the centre arch axis under the balcony (old spot showed a black strip at the left edge). shots/20261123-2056/arcade_west.jpg.

- Under-balcony lamps: four brass ceiling lamps with glowing bulbs and a warm light (30) under each balcony; the soffit and stair sides no longer read black. shots/20261123-2102/arcade_west.jpg.

- Ticket wall: piers and the long cornice over the ticket windows are cream marble with a thin gold lower edge (were grey stock trim). shots/20261123-2116/floor_east.jpg.

- Zodiac figure drawings: tools/make_vault.py SHAPES draws a silhouette per sign (ram with curled horn, bull, twins, crab, lion with mane, robed virgin, scales, curled scorpion, centaur archer, goat-fish, water bearer with urn, two fish on a cord), gold outline and faint wash under the constellation. shots/20261123-2120/vault_up.jpg.

- Frame rate: tools/lua/gcs_shots.lua logs average fps per camera (frames 31-89) to fps.txt, copied into each shots/ folder. shots/20261123-2122: 146-147 fps at every camera on the RTX 5060 Ti, flat, so it is a frame cap (vsync or fps_max), not the map's limit. Wide margin over the 60 fps bar; a mid-range check (fps_max 0, mat_vsync 0, or a weaker GPU) is still open.

- Uncapped fps: `UNCAP=1 sh tools/shots.sh` adds +fps_max 0 +mat_vsync 0. shots/20261123-2124: 676-896 fps (worst floor_east), so even a GPU at a fifth of the 5060 Ti clears 100 fps. Budget is not a concern at this detail level.

- Release 0.1.0 (2026-11-23): Mark signed off in chat. Chandelier globes (shots/20261123-2134). Workshop https://steamcommunity.com/sharedfiles/filedetails/?id=3845077025 public with description (workshop/description.txt: modwright link, Z-Image Turbo banner note, Commons photo authors), 5 previews. Update an upload: gmad create -folder build/addon, gmpublish update -id 3845077025 -addon build/gm_grand_central.gma, then python tools/workshop_update.py 3845077025 --desc workshop/description.txt. GitHub release v0.1.0 carries the .gma.

- Area 2 blockout, playable (2026-11-23): ramps flank the west staircase in railed floor wells, run west under the balcony's side arches (1:6, Guastavino soffit) to the Whispering Gallery (50 ft groin vault, tools/make_tile.py herringbone gcs/guastavino); the Oyster Bar opens off its west side (4x4 tiled groins on piers, oak counter gcs/wood, stools, pendant lamps); a corridor between the ramps leads east to a dining concourse under the main floor (pylons, lit shop fronts, small lower booth). Floor at -22 ft. New cameras ramp_head, ramp_down, whisper, oyster, dining. Clean full compile, shots/20261123-2230 (lower.jpg) and -2232 (Oyster Bar lit). Refs: Commons GCT_Dining_Concourse.jpg (MTA, CC BY), Whispering_Gallery.jpg (CC BY-SA), Oyster Bar (Jazz Guy, CC BY), 1939 section (PD) - not yet downloaded.

- Area 2 detail pass 1 (2026-11-23): 5 Commons refs fetched (refs/SOURCES.md: dining info booth, dining clock, Whispering Gallery, Oyster Bar entrance, Detroit Publishing PD Oyster Bar). `python tools/compare.py shots/<stamp> lower` writes compare_lower.jpg (dining, whisper, oyster). Gallery in pale Guastavino (gcs/guastavino_pale, make_tile.py write_tile), cream corner piers and rib stubs, brass handrails, crown lamp, brighter; lower floors gcs/floor_low (mauve-grey, tinted floor_marble); dining has a coffered ceiling, cream beams between pylons, round brass ceiling lamps, west-bay lights (black pylon face fixed). make_map.py draws a second panel for the lower level with labels. Clean full compile, shots/20261123-2250 (compare_lower.jpg, pair_lower.jpg).

## Next
- True groin vaults (2026-11-23): groin() splits the plan along the diagonals and each triangle follows the barrel whose arch stands on its wall (_slab: convex xy polygon from a sloped plane up to a flat top). Gallery wall arches now read as lunettes; the Oyster Bar shows real groin lines. Clean full compile, shots/20261123-2304 (whisper.jpg, oyster.jpg).
- Area 2 detail pass 2 (2026-11-23): dining booth has a brass column and four-faced opal clock (gcs/clock, z -150..-120 so the dial tiles align); Oyster Bar entrance has a bronze OYSTER BAR band in the opening head (oysterbar.vtf from make_board.py, FACEUV _oysterbar_uv), oak posts, transom and amber side lights; oak-topped cream counters with stools along both Oyster Bar long walls. Anything at the gallery wall above Z+120 sits inside the groin's springing; keep wall details below it. New cameras ob_entry, dining_clock, ob_counter. Clean full compile, shots/20261123-2259.
- East ramps (2026-11-23): the ramp loop in lower_level() mirrors to the east end (e=-1); east ramps descend under the east wall's side arches to a coffered landing hall (EAST_D 40 ft) with three lit brass doors on its east wall (sealed until the platforms, area 4), and a corridor runs west into the dining concourse through a new opening in its east wall. Cameras east_ramp, east_down, east_land. Clean full compile, shots/20261123-2308.
- Release 0.2.0 (2026-11-24): level map labels both levels incl. east ramps/landing hall; README lower-level shots (shots/20261124-0749), wiki Changelog/Roadmap, Workshop gma + description + 5 new previews (the old 0.1.0 map preview is still there: AddItemPreviewFile appends; remove it by hand or add a RemoveItemPreview call to workshop_update.py), tag v0.2.0 with the .gma. The build/ folder must be recreated per worktree: build/addon/addon.json + maps/gm_grand_central.bsp, then gmad create.
- Release 0.3.0 (2026-11-24): Vanderbilt Hall (area 3). Passage through the concourse south wall's west bay (x -115..-102 ft, 16 ft high, 24 ft long) into a 200x64x56 ft hall (build_vmf.py vanderbilt(), VH_* constants): coffered ceiling, gold cornice + cream frieze, dado, grilled windows both long walls, five tiered chandeliers, pedimented east door, 42nd St vestibule with lit brass doors (sealed until area 5). Cameras vh_door, vanderbilt, vh_east, vh_42nd. shots/20261124-0759 (vh.jpg). Refs: 3 Commons photos (2 CC0, 1 CC BY-SA).
- vbsp limit hit: the world model is at the t-junction index cap ("Too many t-junctions", 65536). New areas put their decor in ONE func_brush per area (vanderbilt(): decor list -> func_brush vh_decor), not func_detail. Do the same for every later area.
- tools/package.sh: one-command release (`sh tools/package.sh "note" [previews...]`, DRY=1 builds the .gma only) after tools/compile.sh.
- Vanderbilt Hall detail pass 1 (2026-11-24): windows 16x36 ft, dark glass (gcs/vh_glass) behind a dark-green iron grid and frame (gcs/vh_grille); chandeliers bigger (rings r 54/40/26) under a tall bronze cage (8 bars, gold bands, gcs/bronze) on a chain; moulded cream panel with gold bead on both end walls; `vanderbilt` camera on the hall axis, new `vh_chand`. Clean full compile, shots/20261124-0806 (vh.jpg). No release (detail only).
- Release 0.4.0 (2026-11-24): area 4, upper-level track platforms. Three gates (12x12 ft, brass frames, TRACK 29/30/31 signs from make_board.py track_signs, FACEUV _sign_uv) in the concourse north wall at the bay centres x=-660/0/660 lead to a 170x300x18 ft shed (build_vmf.py platforms(), GATES/SH_*/PLATS/PITS/TRACKS): three island platforms (gcs/plat_tile, yellow gcs/plat_edge), six tracks in ballast pits 4 ft deep with rails and bumpers, brass railing round the pit ends, steel columns and beams (gcs/steel), white strips (gcs/fluor), three stainless cars (gcs/train, train_steel.vtf); the car west of Track 30 has two open doors and benches. Decor in func_brush plat_decor. Cameras gate, plat_head, plat_long, car_door, car_in; `python tools/compare.py shots/<stamp> plat`. Clean full compile, shots/20261124-0820. make_map.py panels now size to their own level.
- Release 0.5.0 (2026-11-24): area 5, the exterior. The vestibule's south wall is now the 42nd Street facade (build_vmf.py exterior(), YF/FCX/FX*/RZ/SKYZ/YS/EX* constants); its three doorways stand open. Facade: three 33x60 ft arched windows (gcs/facade_win: grid as texture, FACEUV 24x36 u cells), paired 8-sided columns, oval + tall windows in the inner narrow bays, entablature, cornice, attic with inscription.vtf, clock_out.vtf clock (13 ft) and a blocky Glory of Commerce group (gcs/statue). Terrace 10 ft deep at 24 ft with a stair at the east end, Park Avenue Viaduct deck across the street at the west end, street lamps, office/metlife towers (tools/make_exterior.py textures), MetLife box behind, toolsskybox, light_environment. Decor in func_brush ext_decor. Cameras vest_out, ext_door, ext_street, ext_clock, ext_viaduct, ext_west, ext_terrace. Clean full compile, 146 fps capped, shots/20261124-0833 and -0837. Refs: 2 Commons photos (CC BY-SA 4.0).
- VERTEX CAP: the BSP is at 61,765 of vbsp's 65,536 unique vertices (0.4.0 was 57,200). The first exterior try (bar-by-bar grilles, balusters) failed with "Too many unique verts". Anything more must cost almost no brush vertices: grids as textures, and from now on props as MDL models (polywright -> studiomdl), which do not count. Check with `python -c "from srctools.bsp import BSP,BSP_LUMPS;print(len(BSP('src/gm_grand_central.bsp').lumps[BSP_LUMPS.VERTEXES].data)//12)"`.
- MDL route (2026-11-24): tools/make_models.py builds props as SMD + QC in Python (Mesh.lathe/cyl/sphere) and compiles them with GMod's bin/studiomdl.exe into src/models/gcs/ (materials src/materials/models/gcs/*.vmt, VertexLitGeneric); compile.sh runs it and packs models + model materials into the BSP. The 10 concourse chandeliers are now prop_static models/gcs/chandelier.mdl (round globes): unique verts 61,765 -> 49,311. shots.sh takes CAMS="a b" to shoot only some cameras; the camera list holds all 41 again (the exterior session had cut it to 7). New camera chand. shots/20261124-0845. No release (no new area).
- Vanderbilt Hall chandeliers as models (2026-11-24): models/gcs/vh_chandelier.mdl (make_models.py vh_chandelier: rosette, chain, 8-bar bronze cage with gold bands, three rings of round globes, bowl core, finial; new model material bronze), prop_static with disableshadows=1 (with shadows on, the light below threw a dark streak up the wall). Unique verts 49,311 -> 44,286. Clean full compile, shots/20261124-0854. No release (no new area).
- Glory of Commerce as a model (2026-11-24): make_models.py statue_group() poses Mercury (arm out, caduceus, winged petasos, cloak), the eagle's spread wings, Hercules reclining with club and lion skin, Minerva seated with helmet, crest and shield, from tubes and ellipsoids (new Mesh.tube/blob/frame/slab, Figure helper; no Blender on this PC). Material models/gcs/statue ($nocull). prop_static at the pedestal top, angles 0 -90 0 (studiomdl turns SMD +x into model +y). Figure brushes removed; pedestal, clock and surround stay brushes. Unique verts 43,872. New camera statue. Clean full compile, shots/20261124-0910 (statue.jpg). No release.
- Eagles and taxis as models (2026-11-24): make_models.py eagle() (plinth, globe, raised wings, hooked beak; statue material) as prop_static on both top corners of the facade; taxi() (yellow sedan, dark glass, roof sign, tyres, lit headlamps; new model materials taxi, car_glass, tyre) x5 on 42nd Street, both lanes, solid 6. Cameras eagle, taxis. Clean full compile, shots/20261124-0917. No release (no new area).
- Pershing Square portal (2026-11-24): the viaduct runs on through a stone-framed opening (bronze PERSHING SQUARE band, make_board.py plaque()) in the building across 42nd Street; inside, a 90 ft pocket (build_vmf.py pershing(), PX0/PX1/PZ/PD/PY0) with a deck ramping down 10 ft to a dark tunnel mouth, coffered ceiling, six brass wall lamps, and the Pershing Square Cafe's lit storefront under the deck at street level. The nodraw outer hull's south wall now follows PY0 (it cut the pocket in two: area 2, drawn as sky). Cameras pershing, pershing_ramp, pershing_in; shots/20261124-0949 (pershing_sheet.jpg). Unique verts 44,610. No release (no new area).
- Rig: tools/shots.sh takes GARGS="..." for extra launch args; fps.txt flags "CAMERA IN SOLID".
- Release 0.6.0 (2026-11-24): the Biltmore Room. Doorway BD0..BD1 (x -1404..-1236, 16 ft) in the concourse north wall (added to gedges in build()) into a 40x80x30 ft room north of the concourse, west of the shed (build_vmf.py biltmore(), BX*/BY*/BH): cream marble floor and walls, beamed ceiling with ceiling lights, dentil cornice, brass sconces, arrivals board (dark glass, brass frame and mullions) on the north wall, railed escalator well 8 ft deep (sealed). Decor in func_brush bilt_decor. Cameras bilt_door, biltmore, bilt_board. Clean full compile, unique verts 46,664, shots/20261124-0955 and -0959. Refs: 3 Commons photos (MTA CC BY 2.0, TheCatalyst31 CC BY-SA 4.0).
- Biltmore polish (optional): the wall clock above the board (gcs/clock needs a face centred like USHIFT), board lettering (a NAME/DUE/TRACK texture from make_board.py), wider room (real one is larger; estimate), escalators down to the dining concourse.
- Release 0.6.1 (2026-11-25, chain session 1): nav mesh. tools/nav.sh launches GMod with sv_cheats, tools/lua/gcs_nav.lua (server autorun, gated by data/gcs_nav_go.txt) runs nav_quicksave 1 + nav_generate, reports the area count after the reload and quits; nav.sh copies maps/gm_grand_central.nav to src/ (gitignored) and package.sh ships it. 1,268 areas, 0.8 MB, about 8 min incl. addon load. Coverage per area not yet checked by eye (nav_edit 1); re-run nav.sh after every compile that changes walkable floors. BSP unchanged from 0.6.0 (46,661 verts).
- Chamber order (session 2 ruling, flagged): 1 lower-level track platforms; 2 Lexington Passage + Graybar Passage shops; 3 Grand Central Market; 4 the Campbell; 5 Transit Museum store; 6 Vanderbilt Ave / One Vanderbilt link; 7 Grand Central Madison deep concourse + escalators (likely needs a level split: depth and vertices); 8 Track 61 / M42 (fenced, dim); 9 Grand Hyatt / Lexington entrance. Reason: cheapest joins first (all off existing walls), the deep LIRR hall last.
- Lower-level tracks blockout, playable (session 2, 2026-11-25): build_vmf.py lower_tracks(), LGATES/LZ/LC/LSH_Y0. Two gates (TRACK 108 at x -480, TRACK 112 at x 480) in the dining concourse north wall (shop fronts there skipped), sloped passages 1:5 down 8 ft to a shed under the upper one (same PLATS/PITS/TRACKS, platform top LZ=-360, ceiling LC=-128 just under the upper ballast pits, 19 ft), riveted columns and beams, one fluor strip per platform, a closed car on track 474. Decor in func_brush low_decor. Hull ZB lowered. Cameras low_gate, low_ramp, low_head, low_long. Clean full compile, 49,781 unique verts, BSP 62.5 MB, 146 fps; shots/20261125-2216/low.jpg. Refs: 5 Commons (refs/SOURCES.md), facts in refs/concourse-dimensions.md.
- Release 0.7.0 (session 3, 2026-11-25): lower tracks detail pass 1: platforms raised to LZ=-308 (15 ft clear under LC), passages two lights each and a pendant globe at the gate; nav regenerated (1.06 MB). shots/20261125-2244. Verts 49,781. shots.sh waits WAIT*5 s (default 180 = 15 min) since addon load can pass 5 min. Level map not yet labelled for the lower tracks.
- Release 0.8.0 (session 4, 2026-11-25): Lexington Passage blockout (chamber 2): build_vmf.py lex_passage(), LEX_X0/X1/Y/H; arcade_bay(open_=True) opens the east centre floor arch; the east ramp landing hall's ceiling and walls now top out at z 0 (they poked 16 u above the floor). 200 ft, 26 ft wide, 22 ft high (photos say 10-12 ft, but the arch is 21 ft: lower it with a header later), 6 lit shop fronts a side, pendant lamps, Lexington doors. Hull X1 grown. Cameras lex_door, lex_in, lex_end. Clean full compile, 50,617 verts, 146 fps, shots/20261125-2258/sheet.jpg. Refs: 5 Commons photos (Lexington + Graybar), facts in refs/concourse-dimensions.md.
- 0.7.0 shipped the session-2 BSP: vbsp had failed ("bad normal": a zero-height sign post after LZ moved) and compile.sh piped vbsp through tail, so vvis/vrad ran on the old BSP. compile.sh now deletes the BSP first and stops on vbsp errors (src/vbsp.log). Never run two compile/shots jobs at once: the second GMod and the half-written BSP gave 20 fps wireframe shots.
- Release 0.9.0 (session 5, 2026-11-25): Graybar Passage: build_vmf.py graybar(), GB_* constants; opening cut in Lexington Passage's north wall at x LEX_X0+84..116 ft (shop fronts there skipped, header plate above to the vault top); five 32 ft groin bays (groin(), n=6, cream), crown 28 ft, pilasters with gold capitals, dado, two glass kiosks, vh_chandelier.mdl props per bay, lit doors north. Cameras gb_in, gb_up. Clean full compile, 51,435 verts, 144-147 fps, shots/20261125-2314/sheet.jpg. Ruling (flagged): Graybar runs north off Lexington (the real one runs parallel to it, west-east from the concourse to Lexington Ave).
- Release 0.10.0 (session 6, 2026-11-25): Grand Central Market: build_vmf.py market(), MK_* constants; door MK_D0..D1 (12x14 ft, gold frame) cut in Lexington Passage's south wall near the market's west end (shop fronts there skipped); hall x 2720..5600 (starts east of the east ramp soffits, which rise above z 0 west of x 2684), 28 ft wide, 15 ft coffered ceiling, centre dome bay to 21 ft with vh_chandelier.mdl, oak counters with cream tops and glass cases in runs along both walls, drum pendants, Lexington Ave doors east. Hull X1 grown. Cameras mk_door, mk_in, mk_dome. Clean full compile, 52,461 verts, 146 fps, shots/20261125-2329/sheet.jpg. Refs: 4 Commons photos, facts in refs/concourse-dimensions.md.
- Release 0.11.0 (session 7, 2026-11-25): the Campbell: build_vmf.py campbell(), CB_* constants; arcade_bay open_ also for the west balcony's south arch (z0 BALC_Z, c CB_C=-372); room x CB_X0..CB_X1 (-2660..-1970), y CB_C+-180, floor at BALC_Z, 25 ft: wood floor, dark ceiling, beams on gilt corbels, leaded window (gcs/window_glass) over a wood bar on the south wall, fireplace and hood on the west wall, green banquette north, sconces. Cameras cb_door, cb_room, cb_bar. Clean full compile, 52,843 verts, 146 fps, shots/20261125-2345/sheet.jpg. Ruling (flagged): reached from the west balcony, not by the real stair off Vanderbilt Ave; size from photos.
- Release 0.12.0 (session 8, 2026-11-26): Transit Museum store: build_vmf.py transit_store(), TM_*; Vanderbilt Hall's east wall cut at the pedimented door (12x11 ft, lit door panel removed); store 40x30x14 ft east of the hall: lit oak shelving, two glass cases, counter, vintage car cab end (gcs/train) on the east wall. Decor is func_detail: as a func_brush (tm_decor) it compiled, cast baked shadows, but never drew in game; no overlapping brush, limits fine; cause not found (watch for it in later rooms). Cameras tm_door, tm_in, tm_car. 53,094 verts, 146 fps, shots/20261126-0026/sheet.jpg. No refs fetched (Commons photos of the store not looked for); ruling (flagged): placed off Vanderbilt Hall, not the Shuttle Passage.
- Release 0.13.0 (session 9, 2026-11-26): One Vanderbilt link: build_vmf.py vanderbilt_link(), LK_*/LB_*; arcade_bay open_ now also for the west centre floor arch; link |y|<120 (ramp walls at 168, Campbell wall at -192..-128), flat to LK_E -2400, steel escalator slope to LK_W -2900 at z 240 (clears the Whispering Gallery top at z 64), ceiling 35 ft; lobby x -3500..-2900, |y|<300, 30 ft, glazed west wall over 4 lit doors. Decor func_brush vl_decor (draws fine). Cameras vl_link, vl_esc, vl_lobby. 53,494 verts, 145-147 fps, shots/20261126-0037/sheet.jpg. No refs fetched; ruling (flagged) on placement and sizes.
- Conversion pass 1 (session 10, 2026-11-26): the concourse end-window mullion bars (~300 func_detail brushes) are now one alpha-tested panel per window (gcs/endwin_a/b/c on make_board.py endwin_grid(): 8 columns, a bar every 96 u, FACEUV per window). Unique verts 53,494 -> 49,902. shots/20261126-0047/sheet.jpg. Not released yet (ships with the next release). Next heaviest decor by solids: concourse func_detail cream (1,089) and gold (673): staircase steps and balustrades, lunettes, pilasters; plat_decor 285, bilt_decor 186.
- NEXT: chamber 7, Grand Central Madison deep concourse: refs are in (refs/concourse-dimensions.md: >140 ft below Park Ave, escalators up to 180 ft long dropping 90 ft); refs first, then check depth and vertices; it likely needs a level split (askwright page, per the prompt). If so, go on to Track 61 / M42 (chamber 8) meanwhile. Vertex budget: 53k of the 58k line; a conversion pass (brush decor to models) is due before the next big chamber. Detail backlog: Graybar painted vault murals (texture), Lexington (lower ceiling with a header past the arch, real shop fronts with bronze frames, navy GCT sign). Lower tracks detail pass 2: real gate look (marble surround, carved oak-leaf half-round over a bronze door, pendant globe, "108 TRACKS 107" serif sign: make_board), lower ceiling (photos say 12-15 ft; ours 19), passage lights, hanging blue Metro-North signs, more cars as MDL models (make_models.py, M7). Label them on docs/level-map.png (make_map.py). Then chamber 2 (Lexington + Graybar passages).
- Platform polish (optional): ads/light boxes on the shed walls, platform-end tunnels, real track numbers, a polywright M7 model instead of brush cars. Optional Vanderbilt polish: big rosette ceiling panels, pilasters between windows.
- 2026-11-23 Mark: chain 20 sessions building the areas joined to the concourse (plan areas 2-6) with images, maps and models; update README, wiki, Workshop and release after each area. Start: area 2, dining concourse below the main floor via the ramps (find a floor plan and photos first; open a ramp opening in the concourse).
- Fold tools/workshop_update.py and the gmad/gmpublish route into modwright (its repo, worktree, tests, PR) - modwright has no GMod publishing guidance.
- Wiki is live (notes/2026-11-23-github-wiki.md); update it from docs/wiki/ when the map changes.
1. Zodiac figures are recognisable silhouettes now; finer line drawings inside them (eyes, fur, folds) could follow. Lunette hoods have voussoirs and keystones; garland carving would be a normal map.
2. Booth interior is in and brighter; clerks' props could follow. Ticket windows have TICKETS plaques and marble reveals and segmental arched heads and bracket lamps; clerks could follow.
3. Measured references: secondary-source check done (refs/concourse-dimensions.md, 2026-11-23): vault springline/rise agree with the build. Still open: a real HABS NY-5450 section or LPC report for balcony, sill and lunette heights; end windows maybe 33x60 ft (ours 26 ft wide, taller).
4. Chandeliers could become a polywright model with globes later.
5. Hammer++ for hand checks (optional).

## Small rulings (flagged)
- Lower tracks (session 2): gates numbered 108 and 112 (real gate reads 108/107); shed reuses the upper platform plan; 8 ft below the dining floor by a 1:5 slope (real: same level as the dining concourse, ~9 m under the upper tracks).
- Platforms (2026-11-24): put at concourse level north of the north wall (the real upper level), not behind the east landing hall doors HANDOFF had named; shed 300 ft long (real ~800 ft), 18 ft high, platforms 20 ft wide, track numbers 29-31 chosen, not the real ones at those gates.
- Vanderbilt Hall size 200x64x56 ft, passage in the concourse's west bay, hall floor level with the concourse (real one slightly higher, reached by a slope): estimates.
- Lower level at -22 ft, ramps 1:6 (real ones gentler and longer), gallery 50 ft square, Oyster Bar 96x80 ft, dining hall 167x100 ft: estimates, no measured plan yet. Only the west ramps so far.
- Licence: code in tools/ is MIT; map source, generated textures and screenshots are CC BY-SA 4.0 (matches the BY-SA reference photos). README banner is Z-Image Turbo seed 11, labelled as AI art, not an in-game shot.
- Sun shafts are fake volumetrics (additive brushes); a camera inside one sees haze, so they fade in only past the balcony edge.
- Zodiac constellations are simplified stick figures over simple silhouettes of each sign of each sign, not the real ceiling's figure drawings; band curves are stylised sinusoids.
- Vault rise 40 ft, estimated from photos (check against the HABS section).
- Bay window bottom 42 ft estimated from photo.
- Balcony arcade 14x14 ft openings, window sill BALC_Z+16 ft, centre end window head SPRING+29.5 ft are estimated from photos.
- Flag placement (north centre bay) and board size estimated; flag length sourced (48 ft), not measured.
- Stairs placed at both ends with 12 u risers / 18 u treads.
- Light levels (after surfaces v2): window point 45, window spot 225, booth 25, chandeliers 18, vault fill 10.
- An installed addon prints "FNaF SB Models are Pre-Caching" over the shots; harmless, ignore or launch with addons off later.

## Waiting on Mark
- Nothing.

## Directive from Mark (2026-11-23)
- Use and improve every plugin involved (polywright, modwright, photowright, artwright, comfyui-gen...); fix gaps in the plugins' own repos.
- Get textures right from real photos (licensed/public domain, sources in refs/); after each compile, put screenshots beside photos from matching viewpoints and iterate until they match. This comes before item 1 below.

- Remote: github.com/m4bwav/gcs-gmod, PUBLIC since 2026-11-23 (was private, (created 2026-11-23). Push main after every merge.

## Directive from Mark (2026-11-23, later): make the repo public
Mark approved making m4bwav/gcs-gmod public. Do it as one milestone, before more detail work:
1. Audit what would go public: refs/photos are Wikimedia images (licences in refs/SOURCES.md). Keep each only if its licence allows redistribution, with attribution in refs/SOURCES.md and the README; otherwise untrack it (gitignore) and keep it local. No game-ripped or paid content, no secrets, no personal paths that matter. If history holds something that must not go public, ask on an askwright page instead of rewriting history.
2. README with a ComfyUI hero banner (comfyui-gen, no Krea 2; the readme-banner rule), screenshots, how to build (tools/compile.sh) and play, credits/licences, a LICENSE file (pick one, flag the ruling).
3. Flip to public (`gh repo edit m4bwav/gcs-gmod --visibility public --accept-visibility-change-consequences`), add SECURITY.md, topics and a description.
4. GitHub wiki with wikiwright: Home, Building the map, Tools, Reference photos and accuracy, Roadmap (area order from the plan), Changelog. Check every page is live.
Push main after every merge.

Public-repo milestone steps 1-3 done 2026-11-23 (audit, README+banner+LICENSE+SECURITY, flipped public with topics and description). Step 4 (wiki) live 2026-11-23, 6 pages, 0 failures.
