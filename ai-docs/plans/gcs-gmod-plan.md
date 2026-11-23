# gm_grand_central plan

## Route
- Write the map as VMF text from Python (`tools/build_vmf.py`), with brushes, displacements and entities generated from a measured layout. Agents can't drive the Hammer GUI, so they build the map as text. Hammer++ is still useful for hand fixes and for checking the map by eye.
- Compile headless with Garry's Mod's own `bin/vbsp.exe`, `vvis.exe` and `vrad.exe` (or the Hammer++ compilers, whichever tests better). Pack custom content with `bspzip` and package with `gmad`, then publish with `gmpublish` or the Workshop UI.
- Check in game: launch `gmod.exe -windowed -novid +map gm_grand_central`, then `screenshot` / `jpeg` from a set of spawn camera points (`shots/`). Look at the screenshots each time.
- Textures: original ComfyUI generations made seamless, at 512 or 1024 px, converted to VTF/VMT with VTFCmd (or similar). Props: simple custom models, mostly brushwork. Use HL2 and GMod stock assets wherever they read as real.

## Scale
One foot = 12 units (a player is 72 u, about 6 ft). The Main Concourse is about 275 x 120 ft with a roughly 125 ft vault, which comes to about 3300 x 1440 x 1500 u. That fits the grid easily, so build it at true scale and don't shrink it.

## Areas, in order
1. **Main Concourse (priority, done bar)**:
   - the barrel vault with the green-blue zodiac ceiling, its gold constellations and lit stars;
   - the three huge arched windows on each end wall, with light shafts;
   - the information booth with its four-faced opal clock;
   - the east and west marble double staircases;
   - the balconies, the ticket windows, the chandeliers, the flags, and the departure board over the ticket windows;
   - the floor in the right marble tones.

   The bar: a screenshot from the west balcony would be mistaken for the real place at a glance, the map compiles with no leaks, and it holds at least 60 fps on a mid-range PC.
2. Main dining concourse level below, with the ramps, the Whispering Gallery tiled arches (Guastavino tile) and the Oyster Bar.
3. Vanderbilt Hall and the 42nd Street entrance passage.
4. Upper-level track platforms: a few tracks with platforms and one or two static train cars to walk through.
5. Exterior: the 42nd Street facade with the Glory of Commerce statue group and its clock, the Park Avenue Viaduct, and enough street and skybox for Midtown to read.
6. Extras if the budget allows: lower-level tracks, the Biltmore Room, roleplay-friendly spaces (shops, offices), and a nav mesh for nextbots and NPCs.

## Budgets
- Keep the BSP and its packed content under about 150 MB in the Workshop.
- Use func_detail for all decoration, with areaportals between areas and hint brushes in the concourse.
- Give each area a cubemap and build cubemaps before upload.

## Workshop
- Title idea: "Grand Central Terminal (gm_grand_central)".
- Thumbnail: a real in-game shot of the concourse, graded, with no AI images standing in for the map.
- Tags: Map, Roleplay, Scenic.
- Don't use MTA logos.
