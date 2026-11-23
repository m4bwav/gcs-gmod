# Log

- 2026-11-23: Project created. Gmod Workshop search found no existing Grand Central map. Continue prompt and plan written; main concourse is priority.
- 2026-11-23: Blockout v1 compiled (no leak). Auto mode refused the GMod launch + taskkill-by-name screenshot run; rig not written.
- 2026-11-23: Screenshot rig written and working (Lua captures and quits; PID-only fallback). Direct gmod.exe launch needs steam_appid.txt=4000. Lights cut ~3x plus tonemap controller; first readable shots in shots/20261123-1135.
- 2026-11-23: Stock HL2 stone/plaster swapped in; first try blew out to white (light levels tuned for dark dev textures). Lights cut ~3x more plus tonemap clamp via logic_auto fixed it (shots/20261123-1444). Bash-tool heredocs can't hold doubled backslashes; edit generator with Edit tool.
- 2026-11-23: Mark: use+improve all plugins (polywright, modwright...); textures from photos; match screenshots to photos. Added to continue prompt and HANDOFF.
- 2026-11-23: Surfaces v2: HL2 has no light marble floor; tile/tilefloor010a and stone/stonewall024a ashlar fit best (contact sheets via new tools/texsheet.py + srctools). Brighter surfaces needed lights halved. shots/20261123-1716. Repo has no remote; worktree merged locally.
- 2026-11-23: Photo refs from Commons + tinted VMTs + compare sheet (shots/20261123-1731). lights/white001 points at Lights/White002; custom VMTs must use that. An addon precache takes ~60 s, so shots.sh waits up to 300 s now (empty shot dirs = timeout).
