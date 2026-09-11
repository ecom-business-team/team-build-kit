---
name: build
description: Execute an approved PRD as pure implementation — no planning, no scope decisions. The PRD already verified every dependency and guaranteed a one-shot build; this skill implements the work items, verifies each against the PRD, updates living docs, then checks the blast-radius router and hands off to /ship if the build crosses the line. Final step in the /memo → /prd → /build lifecycle.
---

# /build

**Definition of done:** Build turns the PRD into reality through **pure execution.** The PRD has already done the thinking — it verified every dependency live and guaranteed the build can be one-shot with zero scope change. So `/build` does not plan, design, or decide; it implements the work items, verifies each against the PRD's contracts and validation log, and updates living documentation. When the build's blast radius crosses the line, it routes to `/ship` for the Gate-3 review before anything goes live.

**The PRD is the only context you need.** A correct PRD is self-contained — you should be able to run this build in a fresh session, from the PRD alone, with nothing from prior conversation. If you find yourself needing context that isn't in the PRD, that's a PRD failure: stop and flag it, don't reconstruct it from memory.

**Scope decisions during build are failure signals, not normal events.** If a genuine fork, an unexpected discovery, or a scope expansion appears mid-build, the PRD did **not** achieve one-shot. Do not drift the design in place. Stop and escalate back to `/prd` (see Scope Escalation below). The whole point of the one-shot constraint is that this almost never happens — and when it does, the fix is upstream.

## Usage

```
/build [project name or link to PRD]
/build auto-categorizer
/build resume   (picks up from project_log.md)
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

## Phase 1: LOAD CONTEXT (from the PRD alone)

**Goal:** Fully understand what's been designed — from the PRD, not from memory.

1. Read the PRD completely. It is self-contained by design; treat it as the single source of truth.
2. Read the CONTEXT.md and `system_contracts.md` for the systems involved.
3. If resuming: read the existing `project_log.md` and skip to the current work item.
4. Create the project log (if new build):

**File:** `{workspace}/_admin/prds/{project-name}/project_log.md`

```markdown
# Project Log: {Name}

**Started:** {date}
**PRD:** [{project_name}_prd.md]({project_name}_prd.md)
**Status:** In Progress

---

## Current State
- **Last completed:** [none]
- **Next:** Work Item 1
- **Blockers:** none

---

## Changes Made
<!-- Append after each work item -->

## Decisions
<!-- Append as decisions are made during build -->

## Scope Changes
<!-- Append ONLY if something deviated from the PRD — should be empty in a clean one-shot -->
```

5. Present a brief summary:

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

### Step 2: Log
Append to the project log immediately:

```markdown
### Work Item N — [Name]
**Completed:** {date}
**Changes:** [what changed, where, why — schema/workflow/code specifics]
**Contract changes:** [new/modified contracts, if any]
**Decisions:** [implementation decisions + rationale]
```

Update Current State (last completed / next / blockers).

### Step 3: Per-Item Verification
Verify against the PRD:
- Does the output match the contract specified for this work item?
- Run the verification step the PRD defined for it.
- Does it behave as the validation log predicted?
- If it doesn't match: fix it now. (If the fix requires a design change, that's a scope escalation, not a build fix.)

### Step 4: Update Living Docs
At the end of each work item, update affected living docs **to the Documentation Standard** (`~/.claude/skills/_shared/documentation_standard.md` — same templates and content rules the docs were created from):
- **CONTEXT.md** — if structure changed (new workflows, tables, folders)
- **system_contracts.md** — if boundaries were added/modified
- **Open-item register** — did this work close an entry in the workspace's missing-wires / open-inputs register (a `DATA_CONTRACT.md`, a blockers table)? **Mark it closed now, in the same sitting.** Building a wire and recording that it is built are two acts, and only the first has a deadline, so the second is the one that silently rots. A register that lists shipped work as missing sends the next PRD looking for something that already exists.
- **Decision log** — if decisions were made
- **Changelog** — entry for what was built

**If a required living doc doesn't exist**, don't hand-roll it ad hoc — that's how formats drift. Flag it and run `/new-workspace` to instantiate the substrate to standard, then resume. `/build` maintains the docs; `/new-workspace` owns creating them.

Flag proposed updates for approval before writing.

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
7. **Work item reconciliation** — every work item complete, every verification confirmed.

Present results:

```
END-OF-BUILD VERIFICATION:
CONFIRMED:
  ✅ [item — how verified]
GAPS:
  ❌ [item — what's missing — fix now / escalate]
```

Fix contained gaps now. A gap that requires design work is a scope escalation.

---

## Phase 4: BLAST-RADIUS ROUTER → /ship

**Goal:** Decide whether this build needs the Gate-3 ship review before it goes live.

Check the router. Does **any** of these apply?
- **Someone other than you depends on it**, or
- **It writes or changes real data**, or
- **Its output is relied on to make important decisions** (accuracy carries weight even if it persists nothing), or
- **It touches money / outside parties / business-critical truth.**

- **If any fire → STOP. Do not let it go live.** The build is halted at the router — nothing goes live until `/ship` clears the Gate-3 review (what breaks · who notices · fallback · contingency · how we fix it). Don't auto-advance; ask the user explicitly:
  > **Blast radius crossed the line — this needs `/ship` (Gate 3) before anything goes live.** Run **`/ship`** now — or pick it up in a new session? (Nothing ships until it clears; `project_log.md` records the router result so a fresh session resumes the review.)
- **If none fire → ship freely.** Proceed to Close.

State the router result explicitly in the log so it's auditable.

---

## Phase 5: CLOSE

**Run this phase ONLY when the Phase 4 router is clean.** If the router fired, you stopped at Phase 4 — `/ship` owns the review, go-live, and close from there; do not run Phase 5 here. (Close lives in `/build` for clean-router builds and in `/ship` for crossing builds.)

### Step 1: Learning Capture
Ask the user:
- "What worked well that we should keep doing?"
- "What was painful or slow?"
- "What would you do differently?"

Append to `project_log.md`:

```markdown
## Lessons Learned
**What worked:** …
**What was painful:** …
**What to do differently:** …
```

If a lesson suggests an improvement to the mental models, the design checklist, or these skills — propose the specific change. These compound.

### Step 2: Final Documentation
1. Any remaining living-doc updates.
2. `project_log.md`: Status → **Complete**, add completion date, list any deferred follow-ups.
3. Changelog: summary entry for the full build.

### Step 3: Archive
Move the entire `{workspace}/_admin/prds/{project-name}/` directory to `{workspace}/_admin/_archive/{project-name}/`.
- Ensure `_admin/_archive/` exists.
- The archived folder contains the PRD + project_log.md (with lessons).
- The memo stays in `_admin/memos/` (linked from the PRD); move it to `_admin/memos/_done/` if its build is fully shipped.

### Step 4: Summary
Present a final summary.

---

## Session Recovery

If a session ends mid-build:
1. Next session: `/build resume` or `/build [project-name]`.
2. Read `project_log.md` → "Current State" tells you exactly where you are.
3. Read "Changes Made" for what's built so far; read the PRD for remaining work items.
4. Present: "Resuming. Work Items 1-N complete. Starting Work Item N+1."
5. Continue — no re-planning, no re-validation of completed items.

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

---

## Principles

- **The PRD is the contract.** Build exactly what it says. The PRD already absorbed every decision; your job is fidelity, not invention.
- **Pure execution.** If you're deciding scope, you've left `/build`. Stop and go upstream.
- **The PRD is self-sufficient.** A fresh session builds from it alone. Needing more = a PRD gap to flag, not a memory to reconstruct.
- **Log as you go.** Every meaningful change logged in the moment — your insurance against session loss.
- **Verify at two levels.** Per-item against its contract; end-of-build against the whole PRD.
- **Update the map when you change the territory.** Living docs updated at the end of each work item, not at the end of the build.
- **The router decides ship.** Internal/reversible → ship freely. Crosses the line → `/ship` first, no exceptions.
