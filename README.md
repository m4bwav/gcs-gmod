![gm_grand_central](docs/banner.jpg)

# gm_grand_central

**Play it:** [Steam Workshop: Grand Central Terminal (gm_grand_central)](https://steamcommunity.com/sharedfiles/filedetails/?id=3845077025)

A Garry's Mod map of the Main Concourse and the lower level of Grand Central Terminal in New York, built at true scale (1 ft = 12 units). It's a work in progress. The concourse and the dining level are in; Vanderbilt Hall, the platforms and the 42nd Street facade come after it (see the [plan](ai-docs/plans/gcs-gmod-plan.md)).

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

### Level map

![Rough plan of the Main Concourse and the lower level](docs/level-map.png)

Drawn from the map source by `tools/make_map.py`: walls and fixtures at chest height, balconies in light tone, red dots for the two spawns.

## What's in it

- The concourse at about 275 x 120 ft, with a flattened barrel vault that has a 40 ft rise
- A zodiac ceiling mural: green field, gold ecliptic and equator, 12 constellations
- Three arched windows at each end, with mullion grids and fake sun shafts
- The information booth, with its four-faced opal clock
- Double staircases at both ends, balconies, and arcades at floor and balcony level
- Ticket windows, a dot-matrix departure board, 16 chandeliers, and the flag
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

- Built with [modwright](https://github.com/m4bwav/modwright), a Claude Code plugin for modding games.
- In-map textures are procedural (scripts in `tools/`) or stock Half-Life 2 materials; no AI-generated images are in the map.

- Code (`tools/`): MIT, see [LICENSE](LICENSE).
- Map source, generated textures and screenshots: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
- Reference photos in `refs/photos/` come from Wikimedia Commons under CC0, CC BY 2.0/4.0 and CC BY-SA 4.0. They are used for colour sampling and side-by-side comparison only. Authors, licences and links are in [refs/SOURCES.md](refs/SOURCES.md): Ɱ, Billie Grace Ward, Russ Allison Loar, Charvey90, ArnoldReinhold.
- The README banner is an AI image (Z-Image Turbo, Apache-2.0, seed 11), not an in-game shot.
- This project has no connection to the MTA or Metro-North and uses none of their logos.
