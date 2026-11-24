# Grand Central Terminal map for Garry's Mod continue prompt

Work from `D:/m4bwa/Claude/Projects/Ai/gcs-gmod`.

Goal: `gm_grand_central`, a Garry's Mod map of New York's Grand Central Terminal, published on the Steam Workshop (item 3845077025). The Main Concourse shipped in 0.1.0. Now build the hallways, chambers and features joined to it, in the plan's area order (dining concourse with ramps, Whispering Gallery and Oyster Bar; Vanderbilt Hall and the 42nd Street passage; track platforms; exterior; extras), each one reached by walking from the concourse through a real opening. Mark asked (2026-11-23) for this to use images, maps and models:
   - images: real photos of each area (licensed or public domain, logged in refs/SOURCES.md) for colour, layout and side-by-side compare.jpg after each compile; procedural or ComfyUI textures (never Krea 2);
   - maps: floor plans and sections of the real terminal as layout references, and `tools/make_map.py` regenerating docs/level-map.png (extend it to label every area);
   - models: polywright props compiled to MDL (benches, ticket machines, Oyster Bar counters, train car, statue group) where brushwork reads poorly, packed into the BSP.

   "Update everything" after each finished area: README (screenshots, level map, what's in it), the GitHub wiki from docs/wiki/, the Workshop item (`gmpublish update -id 3845077025` then `tools/workshop_update.py` for description and previews), a version bump with a tag and GitHub release (pre-approved), and HANDOFF.md.

1. Load state: read `ai-docs/HANDOFF.md`, the end of `ai-docs/log.md` and `ai-docs/plans/gcs-gmod-plan.md` (scope, scale, tool route, area order). Compare HANDOFF.md's age with run logs, build outputs and commits, and trust the newer evidence. Skills to read when the step needs them: comfyui-gen (textures, ceiling mural, Workshop thumbnail), artwright-judge (choosing between texture takes), askwright (questions), quirkwright (Windows shell, paths and waits), labwright (which GPU is free), grindwright (when every lane in front of you is waiting on Mark). Also polywright (props, chandeliers, booth clock), modwright (Source/GMod modding), photowright and artwright (photo analysis). Standing rule from Mark (2026-11-23): use every plugin that fits, and when one falls short, improve it in its own repo (worktree, tests, merge by the PR rules) and log it. Textures come from real photos of Grand Central (licensed or public domain, sources logged in refs/): sample colour, tone and pattern from them, and after each compile match the screenshots against the photos from the same viewpoints, side by side under shots/, until they read alike.
2. Read answers: for any askwright set HANDOFF.md names, run `ask.py read`, act on answered questions, close them, then record the use with `ask.py consume <set> --note "<what you did>"` (or the set stays on the unprocessed list). "Not sure" and unanswered questions stay open, and you never fill them in with your guess.
3. Order of work: take the next item HANDOFF.md names, then the next in the plan. Inside each area the order is blockout, then playable compile, then detail, then lighting, then optimisation. Each area reaches playable compile and joins the concourse before the next one gets detail; keep the 150 MB and fps budgets. Run independent batches (texture generation, reference gathering, prop modelling) as subagents and keep only their short reports. Every map change ends in a full compile (vbsp, vvis, vrad) that loads in Garry's Mod, plus screenshots saved under `shots/`. Update HANDOFF.md at each milestone.
4. Stop before anything that needs Mark:
   - nothing per area: Workshop updates and releases are pre-approved; put a progress page on askwright only for real design questions;
   - paid assets, or content ripped from another game;
   - anything that changes the plan's scope rules.

   Workshop uploads and updates are pre-approved (vault rule). Downloads of tools and models for this work are pre-approved. Small creative rulings are yours: decide them, log them and flag them in HANDOFF.md. Questions go on an askwright page named in HANDOFF.md, and other work carries on.
5. Stop early if HANDOFF.md says `Status: finished`, or if nothing can move without Mark. Say what waits.
6. Project limits (stricter than the standing rules, and why):
   - Never use Krea 2 for any texture or image in this map, because the map is public.
   - Only original or properly licensed assets, because Workshop takedowns hit whole maps.
   - The map must load on a mid-range PC, so keep the budgets in the plan.
7. To hand over: run the wrap-up (evergreen-wrapup, if installed), update the log and HANDOFF.md, and only then print the start command: `Execute D:/m4bwa/Claude/Projects/Ai/gcs-gmod/ai-docs/plans/2026-11-23-gcs-gmod-continue-prompt.md`. State goes in HANDOFF.md, never in this file.
