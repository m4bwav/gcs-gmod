# Grand Central map, 60-session chain: detail and more chambers

Work from `D:/m4bwa/Claude/Projects/Ai/gcs-gmod`, in your own worktree (`git worktree add ../gcs-gmod-<topic> -b <topic> origin/main`); never switch the shared clone's branch. Remove the worktree after the merge.

Goal: carry `gm_grand_central` (Garry's Mod, Workshop 3845077025) through 60 sessions. Two lanes, alternated by value:
- **Detail:** make every existing area read like the real terminal (concourse, ramps, Whispering Gallery, Oyster Bar, dining concourse, Vanderbilt Hall, platforms, exterior, Pershing Square, Biltmore Room). After each compile, compare screenshots with photos taken from the same viewpoints (`tools/compare.py`) and fix the worst mismatch first.
- **Chambers:** add rooms joined to the existing map through real openings. Rough order (refs and a plan first, then decide the order and log it): lower-level track platforms under the dining concourse; Lexington Passage and Graybar Passage with shops; the Campbell (Campbell Apartment bar); Grand Central Market; the Transit Museum store; the Vanderbilt Avenue / One Vanderbilt link; the Grand Central Madison (LIRR) deep concourse with its long escalators; Track 61 and the M42 substation (fenced, dim); the Grand Hyatt / Lexington entrance. Add nav mesh and roleplay spaces where they fit.

## Keep going (read first)
A "session" below is one unit of work, not the end of the conversation. When an item finishes (merged, released, logged), bump the session number and start the next item in the same conversation straight away. Do not hand over after one item. Hand over only at a stop point (step 5 or 6), or when context is heavy; then start chainwright's unattended driver (`chain_loop.py --go`) yourself instead of printing a command and waiting.

## Budget rules (read before every change)
The hard limit is vbsp's 65,536 unique vertices, plus the t-junction cap on the world model; current usage is in HANDOFF.md. The 150 MB file budget comes second.
- After every compile, run `GarrysMod/bin/vbspinfo.exe` on the BSP. Log the unique vertices, faces and file size for each milestone in HANDOFF.md.
- New decoration goes in ONE `func_brush` per area, never in func_detail on the world.
- Show grids, grilles, mullions, balusters and lettering with textures. Build props (benches, lamps, counters, kiosks, escalators, trains, figures) as MDL models with `tools/make_models.py` and polywright. Models don't use up the vertex cap.
- Above 58,000 vertices, adding new brush detail is blocked until a conversion pass has turned existing heavy brush decor (stair balustrades, lamps, booth grilles, ticket-window grilles, chandeliers that are still brushes, platform railings) into models and brought the count back below 52,000.
- If the single BSP can't hold the next chamber, don't cut corners. Log that and propose a level split (a second map joined by a trigger_changelevel) on an askwright page, then carry on with detail work.

## Each session
1. Load state: `git fetch` first. Read `git show origin/main:ai-docs/HANDOFF.md`, the end of `ai-docs/log.md` and `ai-docs/plans/gcs-gmod-plan.md`. Trust the newest evidence (commits, shots, build logs). Skills to read when a step needs them: modwright, polywright, comfyui-gen (never Krea 2), artwright / artwright-judge, photowright, askwright, quirkwright, labwright, releasewright, grindwright. Standing rule: when a plugin falls short, improve it in its own repo and log it.
2. Read the answers on any askwright set HANDOFF.md names (`ask.py read`). Act on them, then run `ask.py consume`. Never fill in unanswered questions with your own guess.
3. Bump `Chain: session N of 60` in HANDOFF.md. Take the next item HANDOFF.md names. A new chamber goes through these stages in order: refs, blockout, playable compile joined to the map, detail, lighting. Run the batch jobs (reference gathering, textures, models) as subagents and keep only their short reports. Every map change ends with a full compile that loads in Garry's Mod, screenshots under `shots/`, and the vbspinfo numbers.
4. After each finished chamber, or a detail pass worth shipping: update the README, level map (`tools/make_map.py`), wiki (docs/wiki/) and Workshop (`sh tools/package.sh`), bump the version, tag it and cut a GitHub release. All of that is pre-approved.
5. Stop before anything that needs Mark: paid or ripped assets, a scope change, or a level split (askwright page). Small creative rulings are yours to make: decide, log and flag them in HANDOFF.md.
6. Stop early if HANDOFF.md says `Status: finished` or nothing can move without Mark. Say what's waiting.

## End of the chain
When `Chain: session 60 of 60` is done, or earlier if every chamber is in and the detail lane only has small polish left: cut a final release, set `Status: finished` in HANDOFF.md, and hand over to the Penn Station chain. Its prompt is `ai-docs/plans/2026-11-25-penn-gmod-60x-continue-prompt.md` in this repo. Carry over the lessons that apply (budget rules, model route, packaging script, compare rig) into a short `notes/lessons-for-penn.md`.

## Hand-over
Run evergreen-wrapup (if it's installed), update the log and HANDOFF.md, and only then print the start command. While the chain runs:
`Execute D:/m4bwa/Claude/Projects/Ai/gcs-gmod/ai-docs/plans/2026-11-25-gcs-gmod-60x-continue-prompt.md`
After the last session, print the Penn command from that prompt instead. State lives in HANDOFF.md, never in this file.
