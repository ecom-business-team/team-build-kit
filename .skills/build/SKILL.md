---
name: build
description: Execute an approved PRD as pure implementation — no planning, no scope decisions. The PRD already verified every dependency and guaranteed a one-shot build; this skill implements the work items, verifies each against the PRD, updates living docs, then checks the blast-radius router and hands off to /ship if the build crosses the line. Final step in the /memo → /prd → /build lifecycle.
---

# /build

**Definition of done:** Build turns the PRD into reality through **pure execution.** The PRD has already done the thinking — it verified every dependency live and guaranteed the build can be one-shot with zero scope change. So `/build` does not plan, design, or decide; it implements the work items, verifies each against the PRD's contracts and validation log, and updates living documentation. When the build's blast radius crosses the line, it routes to `/ship` for the Gate-3 review before anything goes live.

**`state.md` tells you where you are; the PRD tells you what to build.** A correct PRD is self-contained — you should be able to run this build in a fresh session, from the PRD and the project's `state.md` alone, with nothing from prior conversation. If you find yourself needing context that isn't in either, that's a PRD or snapshot failure: stop and flag it, don't reconstruct it from memory.

**Scope decisions during build are failure signals, not normal events.** If a genuine fork, an unexpected discovery, or a scope expansion appears mid-build, the PRD did **not** achieve one-shot. Do not drift the design in place. Stop and escalate back to `/prd` (see Scope Escalation below). The whole point of the one-shot constraint is that this almost never happens — and when it does, the fix is upstream.

## Usage

```
/build [project name or link to PRD]
/build payout-disputes
/build resume   (picks up from state.md — the snapshot; project_log.md is the record)
```

## When to Use

- After a `/prd` has been completed, validated, and approved
- To resume a build interrupted mid-session

## When NOT to Use

- No approved PRD exists (use `/prd` first)
- Bug fixes or config tweaks (use `/quick-fix`)
- The PRD's one-shot readiness gate hasn't passed (finish `/prd` first)

## Prerequisite

A completed, approved PRD at `{workspace}/_admin/prds/{project-name}/{project_name}_prd.md`, with its one-shot readiness section an unqualified yes. If not, redirect to `/prd`.

---

## Phase 1: ORIENT (from `state.md`, then the PRD)

**Goal:** know the position in under five minutes and well under 50k tokens, then build. The project's `state.md` is the snapshot; `project_log.md` is the record. Orientation reads the snapshot and verifies it; it never reads the record for position.

**A. Resuming** — `{workspace}/_admin/prds/{project-name}/state.md` exists:
1. `cat state.md` (≤400 words). It names the last completed work item, the next one, blockers, held switches, what needs the owner, and a **Verify before continuing** block of at most three commands with their expected results.
2. Run every command in that block and compare. If anything disagrees, the snapshot is stale: repair `state.md` first (from `git log`, the branch head, and the *last* entry of `project_log.md`), then continue. Do not re-verify completed work items beyond this block — their proof is in the log.
3. Read the PRD **by section**: the work item named as Next, the validation-log rows it cites, and whatever the work item points at. Read `system_contracts.md`, the system CONTEXT.md and `_practices/` files by section too, following the anchors `state.md` carries.
4. Announce, then build:
```
RESUMING {project} at WI-N — {name}.
WI-1..N-1 done; snapshot verified by {the checks}. Held: {…}. Needs {owner}: {…}.
```

**B. First build session** — no `state.md` yet:
1. Read the PRD completely. It is self-contained by design; treat it as the single source of truth for *what to build*.
2. Read the CONTEXT.md and `system_contracts.md` sections the PRD points at. Inside an initiative (a planning folder exists), read the initiative `state.md` — its handed-forward tray is what this project inherits.
3. Create two files from the templates in `~/.claude/skills/_shared/documentation_standard.md` (§4.7–4.8):
   - `{workspace}/_admin/prds/{project-name}/project_log.md` — the **record**, append-only: Changes Made · Decisions · Scope Changes (empty in a clean one-shot). No "current state" section — position lives in the snapshot.
   - `{workspace}/_admin/prds/{project-name}/state.md` — the **snapshot**: Position (Done / Next = WI-1 / Blocked / Router) · Verify before continuing · Held · Needs {owner} · Pointers. Budget 400 words, rewritten in place, never appended.
   Set the initiative `state.md` "In flight" row to this project.
4. Announce:
```
READY TO BUILD: [project name]
PRD: [link]   Work Items: [N]   Starting: Work Item 1 — [name]
Proceeding.
```

---

## Phase 2: EXECUTE WORK ITEMS (pure execution)

**Goal:** Implement each PRD work item in order, with continuous tracking. No scope decisions.

For each work item:

### Step 1: Build
Implement exactly what the PRD specifies, using the workspace's declared stack (see its `CONTEXT.md`) and the right tool for each work item — never default to a tool the task doesn't call for. This may involve:
- Creating or changing data stores (tables, fields, stored procedures, views)
- Building automations / workflows
- Writing code, configuring integrations
Where a dedicated tool-skill exists for the stack you're using, load it for mechanics (see Stack Mechanics below).

Stay inside the designed boundaries. Standard implementation choices (node config, error handling, obvious details that align with the PRD) are yours to make — that's not a scope decision. A *scope* decision (a fork the PRD didn't resolve, a discovery that changes assumptions, work bigger than the PRD anticipated) → **stop, go to Scope Escalation.**

### Step 2: Per-Item Verification
Verify against the PRD:
- Does the output match the contract specified for this work item?
- Run the verification step the PRD defined for it.
- Run the proof the system's **kind** requires: read the **Kind** line of the system's `CONTEXT.md` and take the proof from the kinds table in `documentation_standard.md` §4 ("The third axis") — an automation replays through its real entry point; a service passes its tests and a live probe and its noticer fires; an application passes browser smoke through the real login and its live invariants; a tool passes tests on fixtures and a check on real data; a procedure passes a cold read in a fresh session; knowledge passes review against its verification table. The method for the code kinds is `testing_standard.md`. No Kind line yet → state the kind from what you observed and add the line in Step 3.
- Does it behave as the validation log predicted?
- If it doesn't match: fix it now. (If the fix requires a design change, that's a scope escalation, not a build fix.)

### Step 3: Update Living Docs
At the end of each work item, update affected living docs **to the Documentation Standard** (`~/.claude/skills/_shared/documentation_standard.md` — same templates and content rules the docs were created from):
- **CONTEXT.md** — if structure changed (new workflows, tables, folders). **System facts only** — what is deployed and how it is wired. Build progress never goes in a system doc; it goes in `state.md`. An index written before 2026-09-20 gains its **Kind** and **Proved by** lines here, on its first change.
- **system_contracts.md** — if boundaries were added/modified
- **Open-item register** — did this work close an entry in the workspace's missing-wires / open-inputs register (a `DATA_CONTRACT.md`, a blockers table)? **Mark it closed now, in the same sitting.** Building a wire and recording that it is built are two acts, and only the first has a deadline, so the second is the one that silently rots. A register that lists shipped work as missing sends the next PRD looking for something that already exists.
- **Decision log** — if decisions were made
- **Changelog** — entry for what was built

**If a required living doc doesn't exist**, don't hand-roll it ad hoc — that's how formats drift. Flag it and run `/new-workspace` to instantiate the substrate to standard, then resume. `/build` maintains the docs; `/new-workspace` owns creating them.

Flag proposed updates for approval before writing.

### Step 4: Record, then snapshot
Two writes and a render, in this order, committed together with the code:
1. **Append** to `project_log.md`:
```markdown
### Work Item N — [Name]
**Completed:** {date}
**Changes:** [what changed, where, why — schema/workflow/code specifics]
**Contract changes:** [new/modified contracts, if any]
**Decisions:** [implementation decisions + rationale]
**Verified by:** [the check, and its result]
```
2. **Rewrite** `state.md` in place: Done now includes WI-N; Next is WI-N+1 (or "end-of-build verification"); Blocked; Router; the **Verify before continuing** block updated to the new branch head, test counts and one live probe; Held; Needs {owner}; Pointers to the sections the next work item will need. Delete anything that reads as a dated event — that is history and it is already in the log. The PostToolUse state gate warns past 400 words or on a date-led bullet.
3. **Render** the handoff: `python3 ~/.claude/skills/_shared/companion/render.py {workspace}/_admin/prds/{project-name}/state.md` writes `handoff.html` beside it (the stage ribbon, the position, what needs the owner, the work items and milestones); then open the page in the default browser when the machine has an opener (`open` on macOS, `xdg-open` on Linux; skip silently otherwise), so it is on screen the moment the document is written.

### Step 5: Session boundary — stop here
A work item is the unit of a session. With WI-N verified, recorded and snapshotted, **stop and hand off**; do not begin WI-N+1 in this context:
Print the **handoff card** (template §4.10):
```
HANDOFF
Where:  {initiative} · milestone {n} {name} · project: memo ✅ · PRD ✅ · build N/{total} · ship ☐ · close ☐
Done:   WI-N — {name} — proved by {the check and its result}; committed {hash}
Next:   WI-N+1 — {name} — run: any prompt in a fresh session (/clear or a new chat); the SessionStart gate points at state.md
Needs {owner}: {decision or keyboard step · task id · due} | none
Written: {workspace}/_admin/prds/{project-name}/state.md · handoff.html
```
Why: measured build sessions that ran a whole project in one context reached 500k–1M tokens and re-read the same documents 15–29 times each; a fresh session that orients from a 400-word snapshot in two minutes is cheaper and more reliable than a long one. Two exceptions, both said out loud: the owner says "continue here" (log the override in the project log), or the next work item is docs-only.

### Repeat for each work item.

---

## Phase 3: END-OF-BUILD VERIFICATION

**Goal:** Full reconciliation — did we build exactly what the PRD specified?

Walk the PRD systematically against the live system:

1. **Entity check** — every entity in the PRD exists.
2. **Lifecycle check** — every state lifecycle implemented with status fields + transition timestamps.
3. **Boundary check** — every domain boundary has its interface and contract.
4. **Contract check** — every contract shape matches the PRD.
5. **Value stream check** — trace trigger → outcome end-to-end.
6. **Validation reconciliation** — every dependency the PRD probed still behaves as logged.
7. **Work item reconciliation** — every work item complete, every verification confirmed, and the kind's proof run.

Present results:

```
END-OF-BUILD VERIFICATION:
CONFIRMED:
  ✅ [item — how verified]
GAPS:
  ❌ [item — what's missing — fix now / escalate]
```

Fix contained gaps now. A gap that requires design work is a scope escalation. Then rewrite `state.md`: Done = every work item; Next = the blast-radius router.

---

## Phase 4: BLAST-RADIUS ROUTER → /ship

**Goal:** Decide whether this build needs the Gate-3 ship review before it goes live.

Check the router. Does **any** of these apply?
- **Someone other than you depends on it**, or
- **It writes or changes real data**, or
- **Its output is relied on to make important decisions** (accuracy carries weight even if it persists nothing), or
- **It touches money / outside parties / business-critical truth.**

- **If any fire → STOP. Do not let it go live.** The build is halted at the router — nothing goes live until `/ship` clears the Gate-3 review (what breaks · who notices · fallback · contingency · how we fix it). Don't auto-advance; ask the user explicitly:
  **Blast radius crossed the line — nothing goes live until `/ship` (Gate 3) clears.** Print the handoff card and stop:
```
HANDOFF
Where:  {initiative} · milestone {n} {name} · project: memo ✅ · PRD ✅ · build {N}/{N} · ship ☐ · close ☐
Done:   end-of-build verification passed; router FIRED ({which conditions})
Next:   the Gate-3 review — run: `/ship {project-name}`, in a fresh session
Needs {owner}: {keyboard steps the review will need · task id} | none
Written: state.md (Router: fired → /ship) · handoff.html · project_log.md (router result)
```
- **If none fire → ship freely.** Proceed to Close.

State the router result explicitly in the log **and in `state.md`** (Router: fired → `/ship` | clean) so it's auditable and so the next session knows which skill to run; then render the handoff again and open it (Phase 2 Step 4, item 3), whichever way the router went.

---

## Phase 5: CLOSE

**Run this phase ONLY when the Phase 4 router is clean.** If the router fired, you stopped at Phase 4 — `/ship` owns go-live and the close from there.

The close is **one shared procedure**, `~/.claude/skills/_shared/project_close.md`, run top to bottom. It captures the lessons (provisional until real use), brings the living documents current, archives the project folder (a blocking step), rewrites the initiative's state file, **schedules the outcome check** (the memo's success definition, verified against real use on a date, after which the milestone reads `reached`), and prints the handoff card. Killing or pausing a project is in the same file (§K and §P). It is not restated here so it cannot drift.

---

## Session Recovery

Phase 1-A is the recovery path, and there is nothing else to do: `cat state.md`, run its verify block, read the PRD by section, announce the position. If `state.md` is missing on a build that has clearly started (a `project_log.md` with entries exists), reconstruct it from the log's last entry and `git log` before doing anything else — that is a defect of the previous session, worth a line in Lessons Learned.

---

## Scope Escalation (the one-shot failure path)

If during Phase 2 the build needs a decision the PRD didn't resolve:

1. **Stop building.** This means the PRD did not achieve one-shot.
2. Tell the user: "Scope decision surfaced that the PRD didn't cover. Here's what and why."
3. Choose:
   - **Amend the PRD** — return to `/prd`, resolve and re-validate the affected section (including any dependency probes), then resume. *Default — preserves the one-shot guarantee for the rest.*
   - **Split** — finish the validated PRD scope, handle the new piece as a separate `/memo` → `/prd` → `/build`.
   - **Continue with acknowledged risk** — only for trivial, reversible deviations; log it in Scope Changes.
4. Log the decision in `project_log.md` under Scope Changes.

A non-empty Scope Changes section is a signal to tighten `/prd` next time — capture why the gap escaped verification in Lessons Learned.

---

## Stack Mechanics

Build with the workspace's declared stack and the right tool for the job — never default to a tool the task doesn't call for. Where a dedicated tool-skill exists for that stack, **load it for the mechanics** (e.g. the `n8n-*` skills for n8n, a database adapter for SQL stores).

Universal build hygiene, regardless of stack:

- **Validate before you commit** — check a created/changed artifact is correct before relying on it, not after.
- **Build incrementally** — small pieces, verify each as you go, rather than one large drop.
- **Prefer the platform's native capabilities**; reach for custom or glue code only when no native option exists.
- **Record what you create** — IDs, locations, endpoints — in `project_log.md`.
- **Read by section.** `sed -n` / `grep -n` a range of a large document; never `cat` a file over ~5k words. Every turn re-sends the whole context, so a whole-file read is paid for on every later turn of the session (`_practices/claude-code.md`).
- **Snapshot before you drop.** Before any destructive schema DDL (DROP of a table/view/function, column removal in a contract phase), persist the verbatim live definition (`pg_get_functiondef` / `pg_get_viewdef` / `CREATE TABLE` DDL, or the platform's equivalent) into the project folder. A summary is not a snapshot — restoration must be mechanical. (Lesson, 2026-07-03: a dropped view whose definition survived only as a summary.)

---

## Principles

- **The PRD is the contract.** Build exactly what it says. The PRD already absorbed every decision; your job is fidelity, not invention.
- **Pure execution.** If you're deciding scope, you've left `/build`. Stop and go upstream.
- **The PRD is self-sufficient.** A fresh session builds from it alone. Needing more = a PRD gap to flag, not a memory to reconstruct.
- **Log as you go.** Every meaningful change logged in the moment — your insurance against session loss.
- **Snapshot, then stop.** Position lives in `state.md`, rewritten at every work-item boundary; a session ends there and the next one resumes from the snapshot in minutes. History goes to the log and is never read for position.
- **Verify at two levels.** Per-item against its contract; end-of-build against the whole PRD.
- **Update the map when you change the territory.** Living docs updated at the end of each work item, not at the end of the build.
- **The router decides ship.** Internal/reversible → ship freely. Crosses the line → `/ship` first, no exceptions.
