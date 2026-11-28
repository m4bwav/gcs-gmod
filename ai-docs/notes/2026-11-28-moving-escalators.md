# Moving escalators in Source/GMod: what worked (2026-11-28)

- **trigger_push with a horizontal pushdir** (`0 <yaw> 0`, speed 100, spawnflags 1) carries a standing player up and down a 30 degree brush slope. A push with a z part would lift the player off the ground each tick (CTriggerPush), so keep pitch 0 and let ground movement follow the slope.
- Add 32 u trigger boxes on the flat at both ends, so the push grabs a player stepping on and carries them off the top.
- The slope brush itself is the walkable ramp (no separate playerclip needed); 30 degrees is far under the 45.6 degree walk limit. Watch for lips: a 2 u plate placed on the slope side of the top edge made a 19 u wall (One Vanderbilt link bug, fixed).
- Scrolling steps: a LightmappedGeneric with a TextureScroll proxy on `$basetexturetransform`. Rate = speed / texture world length (100 / 64 = 1.5625). Angle 180 moves the steps toward +u, 0 toward -u. Tread texture tools/make_escalator.py (four 16 u steps per 256 px at scale 0.25).
- Test: tools/walk.sh + tools/lua/gcs_walk_sv.lua (StartCommand hook; ride = forwardmove 0, walk against = forwardmove 200). Results 2026-11-28: all 10 routes PASS; MetLife ride 5.6 s up / 5.8 s down, Madison run 12.4-12.9 s. Walk-test start points must sit on a lane, not on a balustrade (two Madison routes first started on balustrade x and stuck).
- New areas still go in one func_brush per area (esc_decor); +~500 unique verts (49,703 -> 50,195).
