All scripts live in `tools/` in the repository.

| Script | What it does |
|---|---|
| `build_vmf.py` | Writes `src/gm_grand_central.vmf`: the concourse, vault, windows, balconies, stairs, booth, chandeliers, lights, spawns and cubemaps |
| `compile.sh` | Builds the VMF, runs vbsp, vvis and vrad, packs the materials and copies the BSP into Garry's Mod |
| `shots.sh` and `lua/gcs_shots.lua` | Launch the game and capture fixed camera views into `shots/` |
| `compare.py` | `python tools/compare.py <shotdir>` writes `compare.jpg`, with each shot beside the reference photo from the same viewpoint |
| `fetch_refs.py` | Downloads the reference photos listed in `refs/SOURCES.md` |
| `texsheet.py` | `python tools/texsheet.py out.jpg <regex>` makes a contact sheet of stock Garry's Mod materials |
| `make_vault.py` | The zodiac ceiling mural (2048x1024): green field, Milky Way, gold ecliptic and equator, 12 constellations |
| `make_floor.py` | Rose-grey marble slabs with veins and joints |
| `make_walls.py` | Limestone ashlar, the starry vault fallback, and the coffered arch soffit |
| `make_clock.py` | The opal clock face with its brass bezel |
| `make_board.py` | The departure board with a 5x7 dot-matrix font, and the flag |
| `make_window.py` | Pale window panes with dark muntins |
| `make_shaft.py` | The soft, streaky beam used for the fake sun shafts |

Some materials in `src/materials/gcs/` don't have their own texture. They tint stock Half-Life 2 textures that ship with Garry's Mod, so nothing from HL2 is redistributed.
