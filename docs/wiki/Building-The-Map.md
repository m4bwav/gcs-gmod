## What you need

- Windows with Garry's Mod installed. Its `bin/` folder holds `vbsp.exe`, `vvis.exe`, `vrad.exe` and `bspzip.exe`.
- Python 3 with Pillow and numpy (`pip install pillow numpy`). `tools/texsheet.py` also needs `srctools`.
- A POSIX shell such as Git Bash, since the build scripts are `sh`.

## Point the scripts at Garry's Mod

`tools/compile.sh` and `tools/shots.sh` read `GMOD` and fall back to `D:/SteamLibrary/steamapps/common/GarrysMod`:

```sh
export GMOD="C:/Program Files (x86)/Steam/steamapps/common/GarrysMod"
```

## Compile

```sh
sh tools/compile.sh
```

That runs `build_vmf.py` to write `src/gm_grand_central.vmf`, then vbsp, vvis and vrad (`-both`). It packs `src/materials/gcs/*` into the BSP with bspzip and copies the BSP into `garrysmod/maps/`. The materials are also copied into `garrysmod/materials/gcs/`.

For quick iteration, `FAST=1 sh tools/compile.sh` passes `-fast` to vvis and vrad.

## Play

In Garry's Mod, open the console and run `map gm_grand_central`.

## Screenshots

```sh
sh tools/shots.sh
```

This puts a client Lua script into `garrysmod/lua/autorun/client` and launches `gmod.exe` on the map. The script captures a fixed set of cameras and then quits. Output goes to `shots/<stamp>/` with a `contact.jpg`. Launching `gmod.exe` directly needs `steam_appid.txt` (containing `4000`) in the Garry's Mod folder, and `shots.sh` writes it for you.

## Regenerating textures

The generated VTFs are committed, so you only need these when you change one: `make_vault.py`, `make_floor.py`, `make_walls.py`, `make_clock.py`, `make_board.py`, `make_window.py` and `make_shaft.py`. See [Tools](Tools).
