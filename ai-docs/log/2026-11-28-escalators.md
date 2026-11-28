# 2026-11-28 escalators (release 0.20.0)
- MetLife escalators added (build_vmf.py metlife_escalators, ESC_*): north wall east of the Track 31 gate, floor to east balcony, scrolling treads, trigger_push per lane, sign at the foot. One Vanderbilt link and Madison escalators now move too. No moving walkways (decisions/2026-11-28-escalators-and-walkways.md).
- tools/walk.sh + lua/gcs_walk_sv.lua: 10/10 PASS. Fixed a 19 u lip at the top of the One Vanderbilt escalator.
- gmod_lock.sh copied from penn-modern-gmod and wired into compile/shots/nav/package/walk (shots and nav now kill only their own gmod.exe).
- ob_door.vtf / ob_lead.vtf had never been committed (session 38); committed now.
- Full compile clean, 50,195 verts, BSP 109.3 MB, 597-874 fps uncapped, shots/20261128-0143.
