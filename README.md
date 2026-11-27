![gm_grand_central](docs/banner.jpg)

# gm_grand_central

**Play it:** [Steam Workshop: Grand Central Terminal (gm_grand_central)](https://steamcommunity.com/sharedfiles/filedetails/?id=3845077025)

A Garry's Mod map of the Main Concourse, Vanderbilt Hall, the track platforms and the lower level of Grand Central Terminal in New York, built at true scale (1 ft = 12 units). It's a work in progress. The concourse, Vanderbilt Hall, the track platforms, the dining level and the 42nd Street exterior are in; extras come next (see the [plan](ai-docs/plans/gcs-gmod-plan.md)).

The map is written as VMF text by a Python script, not drawn in Hammer. Every custom texture (the zodiac vault, the marble floor, the ashlar, the clock face, the departure board) is drawn procedurally by a script in `tools/`, with colours sampled from openly licensed photos of the real building.

Screenshots from release 0.1.0 (shots/20261123-2134):

| | |
|---|---|
| ![East balcony](docs/east_balcony.jpg) | ![West balcony](docs/west_balcony.jpg) |
| ![Concourse floor](docs/floor_east.jpg) | ![Zodiac vault](docs/vault_up.jpg) |
| ![Information booth](docs/booth.jpg) | ![Booth clock](docs/clock.jpg) |
| ![Departure board](docs/board.jpg) | ![Flag](docs/flag.jpg) |
| ![West stairs](docs/stairs_west.jpg) | ![West arcade](docs/arcade_west.jpg) |

Lower level, added in 0.2.0 (shots/20261124-0749):

| | |
|---|---|
| ![Ramp down](docs/ramp_down.jpg) | ![Whispering Gallery](docs/whisper.jpg) |
| ![Oyster Bar](docs/oyster.jpg) | ![Dining concourse](docs/dining.jpg) |
| ![Dining concourse booth](docs/dining_clock.jpg) | ![East ramp](docs/east_down.jpg) |

Vanderbilt Hall, added in 0.3.0 (shots/20261124-0759):

| | |
|---|---|
| ![Vanderbilt Hall](docs/vh_east.jpg) | ![42nd Street doors](docs/vh_42nd.jpg) |
| ![Passage from the concourse](docs/vh_door.jpg) | ![Vanderbilt Hall from the west](docs/vanderbilt.jpg) |

Track platforms, added in 0.4.0 (shots/20261124-0820):

| | |
|---|---|
| ![Track gates in the north wall](docs/gate.jpg) | ![Platform head, Track 30](docs/plat_head.jpg) |
| ![Metro-North car with open doors](docs/car_door.jpg) | ![Inside the car](docs/car_in.jpg) |

The exterior, added in 0.5.0 (shots/20261124-0837):

| | |
|---|---|
| ![42nd Street facade](docs/ext_street.jpg) | ![Glory of Commerce and the clock from the viaduct](docs/ext_clock.jpg) |
| ![Biltmore Room](docs/biltmore.jpg) | ![Doorway to the Biltmore Room](docs/bilt_door.jpg) |
| ![Out through the vestibule doors](docs/vest_out.jpg) | ![Looking west along 42nd Street](docs/ext_west.jpg) |

### Level map

![Rough plan of the Main Concourse, Vanderbilt Hall , the track platforms and the lower level](docs/level-map.png)

Drawn from the map source by `tools/make_map.py`: walls and fixtures at chest height, balconies in light tone, red dots for the two spawns.

## What's in it

- The concourse at about 275 x 120 ft, with a flattened barrel vault that has a 40 ft rise
- A zodiac ceiling mural: green field, gold ecliptic and equator, 12 constellations
- Three arched windows at each end, with mullion grids and fake sun shafts
- The information booth, with its four-faced opal clock
- Double staircases at both ends, balconies, and arcades at floor and balcony level
- Ticket windows, a dot-matrix departure board, 16 chandeliers, and the flag
- Vanderbilt Hall (0.3.0): through a passage in the west bay of the south wall, a 200 x 64 ft hall with a coffered ceiling and gilded cornice, tall grilled windows, five tiered chandeliers, a pedimented east doorway and the 42nd Street vestibule with lit brass doors
- Track platforms (0.4.0): three brass-framed gates (Tracks 29, 30, 31) in the north wall lead to a low train shed with three island platforms in rose tile with yellow edges, riveted steel columns, fluorescent strips, a brass railing round the track ends, and three Metro-North cars; one stands open to walk through
- The exterior (0.5.0): out through the Vanderbilt vestibule onto 42nd Street: the facade with three great arched windows between paired columns, oval windows, the GRAND CENTRAL TERMINAL attic inscription, the clock under the Glory of Commerce group, a balustraded terrace with a stair, the Park Avenue Viaduct across the street, office towers, the MetLife tower behind, and open sky
- Grand Hyatt entrance (0.16.0): up a short stair from Lexington Passage, a glass-roofed atrium lobby with a fountain.
- Detail pass (0.17.1): Lexington blade sign, Campbell surfaces, Market door sign and Root Chandelier.
- Detail pass (0.18.5): carved eagle tympanums in the lunettes, honey-tan walls, grey floor marble, bronze-barred window glass and cooler, dimmer daylight in the concourse, closer to the photos.
- Detail pass (0.18.4): a row of lit bulbs along the concourse cornice, grilled blue-grey glass in the vault lunettes.
- Detail pass (0.18.3): backlit platform ads, turned-post brass railings at the track ends, glazed Market door side lights.
- Detail pass (0.18.2): dining concourse shop fronts and pylon capitals, a stone-and-glass lower information booth, leaded-glass Oyster Bar doors.
- Detail pass (0.18.1): Graybar newsstands, Biltmore Room wall clock, Market bow window with lit stalls and brass rail, M7 car sides on the upper platforms.
- Detail pass (0.18.0): Market storefront, Lexington shop windows, Madison mural, shop band and stainless escalators, Graybar stone walls and lit kiosks.
- Detail pass (0.17.0): Biltmore arrivals lettering, painted Graybar vaults, a white-panelled Grand Central Madison with terrazzo floor and departure screens.
- Lexington Passage detail (0.16.1): a lower beamed ceiling with brass dome pendants.
- Track 61 (0.15.0): beyond a fence at the north end of the lower tracks, the dim secret platform and its freight elevator.
- Grand Central Madison (0.14.0): from the dining concourse, long escalators down to the deep LIRR concourse, 140 ft below.
- One Vanderbilt link (0.13.0): through the west floor arch, escalators up to a glass-walled lobby on Vanderbilt Avenue.
- Transit Museum store (0.12.0): through Vanderbilt Hall's east door, a small shop with a vintage car's cab end.
- The Campbell (0.11.0): up on the west balcony, the old office-turned-bar with painted beams, a leaded window and a fireplace.
- Grand Central Market (0.10.0): off Lexington Passage, a long market hall with counters down both sides under a chandelier dome.
- Graybar Passage (0.9.0): north off Lexington Passage, groin-vaulted bays under brass chandeliers.
- Lexington Passage (0.8.0): through the east floor arch, a shop-lined passage east to the Lexington Avenue doors.
- Lower-level tracks (0.7.0): from the dining concourse, the TRACK 108 and 112 gates lead down to a low, dark second train shed under the upper tracks.
- Nav mesh (0.6.1): nextbots and NPCs can walk the map out of the box (tools/nav.sh rebuilds it).
- The Biltmore Room (0.6.0): through a marble doorway in the northwest of the concourse, the old arrival room with a beamed ceiling, dentil cornice, brass sconces, the old arrivals board in its brass frame and a railed escalator well
- The lower level (0.2.0): ramps from both ends of the concourse, the Whispering Gallery under a Guastavino tile groin vault, the Oyster Bar with its tiled vaults, counters and stools, the dining concourse with a coffered ceiling and a small clock booth, and an east landing hall

## Building

You need Windows, Garry's Mod (its `bin/` has vbsp, vvis, vrad and bspzip), Python 3 with Pillow and numpy, and a POSIX shell such as Git Bash.

```sh
export GMOD="C:/Program Files (x86)/Steam/steamapps/common/GarrysMod"   # wherever yours is
python tools/make_vault.py   # and the other make_*.py, only to regenerate textures
sh tools/compile.sh          # build_vmf.py, vbsp, vvis, vrad, bspzip, copy to garrysmod/maps
FAST=1 sh tools/compile.sh   # quicker vvis/vrad for iteration
sh tools/shots.sh            # optional: launch GMod, capture fixed cameras into shots/<stamp>/
```

Then in Garry's Mod: `map gm_grand_central`.

The textures in `src/materials/gcs/` are already generated, so you only need the `make_*.py` scripts when you change them. Some materials point at stock Half-Life 2 textures that ship with Garry's Mod; none of them are redistributed here.

## Credits and licences

- Built with [modwright](https://github.com/m4bwav/modwright), an agent plugin for modding games.
- In-map textures are procedural (scripts in `tools/`) or stock Half-Life 2 materials; no AI-generated images are in the map.

- Code (`tools/`): MIT, see [LICENSE](LICENSE).
- Map source, generated textures and screenshots: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
- Reference photos in `refs/photos/` come from Wikimedia Commons under CC0, CC BY 2.0/4.0 and CC BY-SA 4.0. They are used for colour sampling and side-by-side comparison only. Authors, licences and links are in [refs/SOURCES.md](refs/SOURCES.md): Ɱ, Billie Grace Ward, Russ Allison Loar, Charvey90, ArnoldReinhold, Chris Light (CC BY-SA 4.0), Lexcie (CC BY-SA 3.0), TheCatalyst31 and NicoARicoA (CC BY-SA 4.0).
- The README banner is an AI image (Z-Image Turbo, Apache-2.0, seed 11), not an in-game shot.
- This project has no connection to the MTA or Metro-North and uses none of their logos.
