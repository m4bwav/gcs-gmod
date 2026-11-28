# Escalators yes, moving walkways no (2026-11-28, release 0.20.0)

## Decision
- **MetLife escalators added** to the main concourse: a pair (up lane by the wall, down lane beside it) along the north wall east of the Track 31 gate, x 846..1386, y 496..648, rising east at 30 degrees from the floor (z 0) to the east balcony (z 312), entering it through a gap in the north parapet. Lit METLIFE BUILDING 45 ST band on brass posts at the foot. build_vmf.py `metlife_escalators()`, constants `ESC_*`.
- **Existing static escalators now move**: the One Vanderbilt link (north lane up, south lane down) and both runs of Grand Central Madison (west two lanes down, east two lanes up). Both are real escalators in the real station, so they belong.
- **No moving walkways.** The real terminal has none, and no passage in the map is long enough to justify inventing one (Lexington Passage 200 ft, Market 240 ft are shop-lined walking halls in reality).

## Why the MetLife pair sits where it does
Real: the escalators to the MetLife Building and 45th St rise from the north side of the main concourse, through the north wall (source: web search 2026-11-28; Biltmore Room escalators, opened 2023, go *down* to Grand Central Madison, so the Biltmore well stays sealed). In the map the upper train shed sits right behind the north wall (96 u away), so a run through the wall cannot clear the shed roof. Flagged ruling: the pair runs inside the concourse along the north wall and lands on the east balcony, which is already walkable (stairs, the sealed lit balcony passages), so the top is not a dead end.

## How movement works
- Tread: one 8 u sloped brush per lane (the slope itself is the walkable ramp, 30 degrees, under the 45.6 degree walk limit), material gcs/esc_xp/xn/yp/yn = gcs/esc_tread.vtf (tools/make_escalator.py: four 16 u steps per 64 u, riser shadow, yellow nose) with a TextureScroll proxy at 1.5625 textures/s = 100 u/s. Angle 180 makes the steps move toward +u, 0 toward -u. `_yp/_yn` map u along +y through FACEUV.
- Carry: a trigger_push per lane (or lane pair in Madison), pushdir horizontal (pitch 0) at speed 100, plus 32 u end boxes on the flat at both ends. Horizontal push lets ground movement climb the slope; a push with a z component lifts the player off the ground every tick in Source.
- Test: tools/walk.sh + tools/lua/gcs_walk_sv.lua (ride with no input, walk against).
