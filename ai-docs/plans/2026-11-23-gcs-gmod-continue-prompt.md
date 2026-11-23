# Grand Central Terminal map for Garry's Mod continue prompt

Work from `D:/m4bwa/Claude/Projects/Ai/gcs-gmod`.

Goal: `gm_grand_central`, a Garry's Mod map of New York's Grand Central Terminal, published on the Steam Workshop. **The Main Concourse comes first and matters most**: it has to be instantly recognisable and good enough to screenshot before any other area gets real time. The rest of the terminal follows in the order of the plan.

1. Load state: read `ai-docs/HANDOFF.md`, the end of `ai-docs/log.md` and `ai-docs/plans/gcs-gmod-plan.md` (scope, scale, tool route, area order). Compare HANDOFF.md's age with run logs, build outputs and commits, and trust the newer evidence. Skills to read when the step needs them: comfyui-gen (textures, ceiling mural, Workshop thumbnail), artwright-judge (choosing between texture takes), askwright (questions), quirkwright (Windows shell, paths and waits), labwright (which GPU is free), grindwright (when every lane in front of you is waiting on Mark). Also polywright (props, chandeliers, booth clock), modwright (Source/GMod modding), photowright and artwright (photo analysis). Standing rule from Mark (2026-11-23): use every plugin that fits, and when one falls short, improve it in its own repo (worktree, tests, merge by the PR rules) and log it. Textures come from real photos of Grand Central (licensed or public domain, sources logged in refs/): sample colour, tone and pattern from them, and after each compile match the screenshots against the photos from the same viewpoints, side by side under shots/, until they read alike.
2. Read answers: for any askwright set HANDOFF.md names, run `ask.py read`, act on answered questions, close them, then record the use with `ask.py consume <set> --note "<what you did>"` (or the set stays on the unprocessed list). "Not sure" and unanswered questions stay open, and you never fill them in with your guess.
3. Order of work: take the next item HANDOFF.md names, then the next in the plan. Inside each area the order is blockout, then playable compile, then detail, then lighting, then optimisation. Don't start detailing a later area while the Main Concourse is below its done bar in the plan. Run independent batches (texture generation, reference gathering, prop modelling) as subagents and keep only their short reports. Every map change ends in a full compile (vbsp, vvis, vrad) that loads in Garry's Mod, plus screenshots saved under `shots/`. Update HANDOFF.md at each milestone.
4. Stop before anything that needs Mark:
   - his look-and-feel sign-off on the Main Concourse (screenshots on an askwright page) before the first Workshop upload;
   - paid assets, or content ripped from another game;
   - anything that changes the plan's scope rules.

   Workshop uploads and updates are pre-approved (vault rule). Downloads of tools and models for this work are pre-approved. Small creative rulings are yours: decide them, log them and flag them in HANDOFF.md. Questions go on an askwright page named in HANDOFF.md, and other work carries on.
5. Stop early if HANDOFF.md says `Status: finished`, or if nothing can move without Mark. Say what waits.
6. Project limits (stricter than the standing rules, and why):
   - Never use Krea 2 for any texture or image in this map, because the map is public.
   - Only original or properly licensed assets, because Workshop takedowns hit whole maps.
   - The map must load on a mid-range PC, so keep the budgets in the plan.
7. To hand over: run the wrap-up (evergreen-wrapup, if installed), update the log and HANDOFF.md, and only then print the start command: `Execute D:/m4bwa/Claude/Projects/Ai/gcs-gmod/ai-docs/plans/2026-11-23-gcs-gmod-continue-prompt.md`. State goes in HANDOFF.md, never in this file.
