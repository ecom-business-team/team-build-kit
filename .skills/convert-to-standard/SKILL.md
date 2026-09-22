---
name: convert-to-standard
description: Bring an existing folder or running system up to the standard with one command: observe what actually runs, name what kind of thing it is and how its parts fit, create exactly the documents it is missing, and hand it into the lifecycle with a handoff card. The door for existing work; /new-workspace is the door for new work.
---

# /convert-to-standard

You already have something: a folder of scripts, a workflow that runs every night, a spreadsheet with a process around it, a whole system nobody wrote down. This command looks at what is actually there, names what kind of thing it is, writes exactly the documents the standard says it is missing, and hands it into the lifecycle so the next change to it goes through `/memo` or `/quick-fix` like everything else. It is the door for existing work. `/new-workspace` is the door for new work; both end at the same place.

## Usage

```
/convert-to-standard <folder>                      — a folder on disk
/convert-to-standard <name of a running system>    — something that runs elsewhere (an automation, a hosted service); you say where its parts run
```

---

## Phase 1: Confirm the target and its level

Resolve the target: the folder's path, or the system's name and where each of its parts runs (which host, which automation platform, which database). State it back in one sentence.

Then ask only the **level** questions from `/new-workspace` Phase 1, in the same plain words:
- "Does it hold multiple things you build and run separately, or is it one buildable thing?"
- "Is this one build, or a sequence of milestones that build on each other over months?"

**Do not ask the fork** — this is existing work, so it is brownfield by definition. **Do not ask the kind** — what it is made of is observed in Phase 2, never asked. State back the level with the doc set it implies (`~/.claude/skills/_shared/documentation_standard.md`, Part 2) and stop for confirmation. If the person corrects the level or the scope, restate and stop again.

## Phase 2: Observe, then fill gaps

Run `/new-workspace` Phase 2b exactly as written (`~/.claude/skills/new-workspace/SKILL.md`, Steps 1–3): one ground-truth agent per area the target touches, facts only; reassemble the reports into one verified picture, including what each part is made of at runtime, which is where the kind comes from; then ask the person only what the files and the live system cannot say. Every line you will write must trace to something observed or explicitly confirmed. The steps are not restated here: one method, one place.

## Phase 3: Provision and verify

Run `/new-workspace` Phases 3 and 4 as written: exactly the doc set for the confirmed level and the observed kind, its `CONTEXT.md` with the Kind and Proved-by lines stated (or `not yet stated`, when the proof does not exist yet), canonical homes created if the level needs them, the root `CLAUDE.md` routing row added after approval, never overwriting an existing file. Before showing the plan, run the trace yourself: beside every line you intend to write, name the file, the observed run, or the person's answer it comes from. Who performs a manual step, who owns the code, whether a file is disposable, what the history was and what checks exist today are facts to observe or to ask, never to infer; a line with no source is cut. Then show the plan and wait for approval.

## Phase 4: Hand off

Print the handoff card (`documentation_standard.md` §4.10):

```
HANDOFF
Where:  standalone | {the initiative, when the folder belongs to one} · brought to standard
Done:   brought to standard — N parts observed, M facts confirmed by the person; files: {the paths written}
Next:   /memo {the first thing the person wants changed} | /quick-fix {a known small defect} — in a fresh session
Needs {owner}: {every question the files could not answer, filed to the task manager with its id} | none
Written: {the paths}
```

Next is always something the person can type verbatim. If nothing needs changing yet, Next is `/memo` for whatever they name first; the docs are now the substrate that command reads.

---

## Safety Rules

1. **Never overwrite existing files** — check first; offer update-or-skip.
2. **Confirm before writing** — show the Phase 3 plan and wait.
3. **Stay inside the target** — all paths relative to the target's root; the workspace root is touched only for the routing row and canonical homes.
4. **No secrets in generated files** — reference where credentials live, never their values.
5. **Never lower the bar** — a line you cannot trace to something observed or confirmed is cut, not kept.
