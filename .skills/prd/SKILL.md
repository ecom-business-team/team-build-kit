---
name: prd
description: Design a system change as a verified bridge from a 100%-resolved beginning state to a defined desired state. Locks current reality with zero assumptions, finds the simplest viable path (reusing existing infrastructure), verifies every cross-system dependency live, and runs the full design-rigor pass — so the build can be one-shot with zero scope change. Middle step in the /memo → /prd → /build lifecycle.
---

# /prd

**Definition of done:** A PRD makes the gap between **where we are** and **where we want to be** so completely understood and verified that the build cannot surprise us. Its exit condition is a hard guarantee: **`/build` can be executed in one shot, with zero scope change.** Every assumption about the current state is resolved to 100%, every cross-system dependency is probed live and confirmed to respond as assumed, and every design check has passed — *before a single build action is taken.* This is **Gate 2: "I've designed it right."**

Why the bar is this high: if anything is discovered mid-build that forces a course change, it triggers rework that cascades through everything downstream. The cheapest place to find that problem is here, in the PRD, before anything is committed. We do **all** the verification up front so `/build` becomes pure execution — no planning, no scope decisions, no surprises.

**The PRD must be self-contained.** A big memo + PRD can consume a lot of context — so often the build runs in a *fresh session*. The emitted PRD document has to carry everything a new session needs to one-shot the build, with **zero** reliance on the conversation that produced it. The test: hand the PRD file (and nothing else) to a session with no memory of this work — can it build the whole thing without asking a single clarifying question? If anything required to build lives only in the chat — a decision, a verified response shape, a "we agreed to…" — it isn't done until it's written into the PRD.

**This PRD always derives from a memo,** but the memo is not load-bearing: when ground truth gathered in Phase 1 contradicts the memo's assumed solution, the PRD is shaped by reality and the memo gets revised — never deferred to.

## Core disciplines (read before starting)

- **Zero assumptions about the beginning state.** Any variance in the start state corrupts the entire downstream build. The current-state picture must be at 100% resolution, observed from live systems — never inferred from docs or memory alone.
- **Reuse over rebuild.** The most common failure: a session doesn't fully understand what already exists, so it builds redundant new tables/workflows instead of small additions to existing infrastructure. Every new artifact must justify why an existing one couldn't be extended.
- **Reduce, don't merge.** Find the *smallest* change that bridges the gap. Do not incorporate every piece of context the agents return. Synthesis-by-merge is the enemy.
- **Agents explore, one mind designs.** Agents gather ground truth and propose whole-solution candidates. They never each own a *project* of the build and scope it independently — that fragments the design and forces reconciliation after. The main session is the single designer.

## Usage

```
/prd [link to memo or description of what to design]
/prd design the payout dispute system (see _admin/memos/payout_disputes.md)
/prd scope the new brand analytics dashboard
```

## When to Use

- After a `/memo` has cleared Gate 1 and recommended a build
- When a significant system change needs architectural design before implementation
- When multiple systems, entities, or boundaries will be affected

## When NOT to Use

- Bug fixes or config tweaks (use `/quick-fix`)
- Strategic decisions not yet clarified (use `/memo` first)
- The change is trivial (single table, single workflow, no boundary crossings, nothing to verify — go straight to `/build`)

---

## Phase 1: LOCK THE BEGINNING STATE (100% resolution, zero assumptions)

**Goal:** A perfect, verified picture of exactly what we are working from — and what already exists that we can reuse.

**Inside existing work** (an initiative `state.md` holds this memo's milestone): read that `state.md`, then print the orientation card (template §4.10) before spawning any agent.

Spawn **one ground-truth agent per system/area the build touches.** This is the safe place to parallelize: these agents *observe and report facts* — they do not design, so dividing by area causes no fragmentation. The main session reassembles their reports into **one** coherent picture.

Generalize the agents to the actual systems involved. Common areas (assign whichever apply):

| Area | What the agent verifies (facts only, no recommendations) |
|------|----------------------------------------------------------|
| **Automations / workflows** | Observe each live automation directly — its configuration, connections, credentials, current data flow, and which ones this touches. |
| **Data stores** | Inspect a real sample of the live data for every relevant store — field names, types, relationships, value conventions, indexes, stored procedures, views. Observe, never infer from docs. |
| **App / frontend** | Routes, API handlers, env config, deploy state. |
| **Code / scripts** | Modules, entry points, dependencies, current behavior. |
| **External services / APIs** | What endpoints exist, auth, request/response shapes actually returned. |
| **Context & contracts** | **Inside an initiative, the initiative `state.md` first** — its milestone table and handed-forward tray are the entry to the archived PRDs and logs, which are then read by section, never whole. Then CONTEXT.md, `system_contracts.md`, decision log, the triggering memo, memory, and `_admin/_archive/` for prior projects that touched these systems (read the archived PRD's relevant sections — original design decisions and lessons live there). **If the workspace has no standard living docs to read, stop and run `/new-workspace` (brownfield) first** — a PRD can't resolve the beginning state against a documentation substrate that doesn't exist. |

Use the right observation tool for the workspace's declared stack — load its tool-skill where one exists. Observe live state; never infer.

**Every Phase 1 agent must also return a reusable-assets inventory** for its area: existing tables, fields, automations, stored procedures, contracts, and patterns that are *adjacent to this build and could be extended.* This inventory is what prevents redundant rebuilds in Phase 7.

**Wait for all agents. Reassemble into one briefing:**

```
BEGINNING STATE (verified):

Systems involved:
- [system] — [current state, key facts]

Kind of thing built:
- [one of the six kinds (documentation_standard.md §4), or a composite naming its parts — and the proof each kind requires]
- [the kind today, read from what the thing is now, against its CONTEXT.md Kind line: same | changed from X, because …] · owes: [the documents that kind owes, from the _shared Part 2 table and the root §4 kinds table] · missing: [none | each one, which becomes work in this PRD]

Schema / data:
- [table] — [columns, relationships, conventions]

Existing contracts:
- [boundary] — [current shape]

REUSABLE ASSETS (already exist — candidates to extend, not rebuild):
- [table/automation/stored procedure/pattern] — [what it does, how it might be extended]

Constraints from prior decisions:
- [decision #N] — [what it constrains]

Open assumptions still unverified: [list — must be empty before Phase 6 completes]
```

**Walk the picture with the user.** Confirm understanding. Flag anything that contradicts the memo's assumed solution — revise the memo now, don't carry assumptions forward.

**Gate:** zero assumptions remain about what exists. If any fact is inferred rather than observed, go verify it.

---

## Phase 2: DEFINE THE DESIRED STATE

**Goal:** One clear statement of "solved looks like X," pulled from the memo's success definition.

- State the desired end state in one paragraph — observable and concrete.
- **Beginning state + desired state = the gap.** Everything downstream bridges exactly this gap and nothing more.

---

## Phase 3: MINIMUM-VIABLE DERIVATION (mandatory gate)

**The most important step. Do not skip. Do not let the memo's proposed solution carry forward unchallenged.**

Before any path agent runs, YOU answer in writing:

> Given the verified beginning state — **including everything in the reusable-assets inventory** — what is the single smallest change that bridges the gap to the desired state?

Write it as one paragraph. Be ruthlessly minimal: one field, one step, one query, one extension of an existing component — the literal smallest. The minimal version is minimal precisely **because** it reuses what already exists. No "and also," no "while we're here."

Then ask:
- **Does the smallest version actually reach the desired state?** (Re-read the gap — does minimal close it?)
- **Does it have a foreseen downstream break?** (Blast-radius check: which consumers / contracts / tables does it touch? Is anything documented today that this breaks?)
- **If both answers are clean → the minimal version IS the PRD.** Skip Phase 4 and 5, proceed to Phase 6 (verify it live), then Phase 7. Do NOT manufacture sections to make the PRD feel "complete."
- **Only if the minimal version genuinely cannot reach the desired state** (name the specific failure mode) do you proceed to multi-path generation.

Present the derivation to the user and confirm before proceeding.

---

## Phase 4: GENERATE CANDIDATE PATHS (only if minimal is insufficient)

There are a thousand ways to bridge a gap across systems with dependencies. When minimal can't, get independent takes before committing.

Spawn fresh-context agents, each handed the **same complete picture**: beginning state + reusable-assets inventory + desired state + the named failure mode that ruled out minimal.

**Each agent designs the ENTIRE bridge, end-to-end, from a different angle. No agent owns a project.** This is the explicit guard against fragmentation — every proposal is a complete path from start state to desired state, not a component someone else has to integrate.

Assign one angle per agent:

| Angle | Framing (applied to the whole bridge) |
|-------|----------------------------------------|
| **Subtraction** | What is the smallest set of edits to existing artifacts that bridges the whole gap? |
| **Reuse** | What existing pattern already solves a structurally identical problem — apply it across the whole bridge? |
| **Elimination** | Can the gap be made not-exist by changing an upstream condition instead of building? |
| **External** | Is there an existing tool/service/feature that bridges the gap so we build less? |

Launch 2-4 in parallel. Each returns one complete path: the changes required, what it touches, every component, and why it's the simplest viable bridge from that angle.

---

## Phase 5: GRADE & SELECT

**Goal:** Pick the best complete path. **You do NOT merge.**

Evaluate each path against: simplicity, reuse of existing infra, blast radius, and how cleanly it reaches the desired state. The asymmetry between angles is what surfaces the minimum — merging destroys it. If two paths are equally simple but differ in tradeoff, that's a design decision for the user. If none are simple enough, the gap was framed wrong — re-frame.

Present the candidates and the selected path to the user. Confirm before proceeding.

---

## Phase 6: MAP COMPONENTS + VERIFY EVERY DEPENDENCY LIVE (the one-shot core)

**Goal:** Prove the end-to-end process works *before* committing to build. This is what makes one-shot possible.

1. **Enumerate every component** of the chosen path — every table/column to add or change, every workflow/node, every contract, every endpoint, every handoff.
2. **Probe every cross-system dependency live.** For each webhook, service, endpoint, RPC, and external API the path depends on: actually call it / inspect it and confirm it responds exactly as the design assumes. Do not assume a response shape — observe it.
   **Trace platform automations as consumers, not just workflows.** If the design changes any status/field value, enumerate every platform-native automation (board automations, DB triggers, scheduled rules) that fires ON that value — they are invisible consumers that never appear in workflow-to-workflow tracing. A status a build stops transiting silently starves every automation listening for it. (Lesson, 2026-07-24: an impact map declared a consumer unaffected; that consumer's board automation on `status→approved` was never traced, and the new one-step path would have silently dropped a grading step; caught only at build time, forcing a PRD amendment.)
   **Verify the property you depend on, not the artifact's existence.** A key that exists may be the wrong tier; a tool that "works" is only verified on the code paths it has actually run. Probe the specific property the design rests on (key tier/scope, the exact branch, the exact response field) — existence checks pass while the design-breaking detail hides underneath. (Lesson, 2026-07: a push tool's INSERT path had never once executed because the key it held was the wrong tier; the artifact existed, the property did not.)
   **If the design changes a filter, report, or count semantic: replay the producer end-to-end against CURRENT live data** (dry-run style), not just per-dependency probes. Per-dependency probes verify each piece in isolation; only a full replay reveals how the new semantic interacts with the data that already exists. (Lesson, 2026-07-14: every dependency of a daily report probed ✅, yet items already dispositioned would have re-reported forever; caught only by the /build dry run, forcing a mid-build PRD amendment.)
3. **Record a validation log:**

```
VALIDATION LOG:
| # | Assumption the design rests on | How tested | Result | Status |
|---|--------------------------------|------------|--------|--------|
| 1 | Webhook X returns {field: type} | Fired test payload | Returned {…} | ✅ confirmed |
| 2 | Table Y has column Z (uuid)     | SELECT … LIMIT 5  | Present, uuid | ✅ confirmed |
| 3 | Service W accepts batch writes  | …                 | …      | ❌ does not — revise path |
```

4. **The owner reads a rendered draft (a document people read).** When the chosen path creates a document people read, or reshapes one (its structure, its picture or its printed shape changes; not a row or a sentence), draft the part the design rests on and show it to the owner as its reader will see it: its generated page when `render.py` has a plan for it, the markdown preview when it has none, printed in the session when it is session output such as a card. Record the owner's verdict as a validation-log row, in their words, with the date: ✅ when they accept the draft, ❌ while a change they asked for is open. A change they ask for is designed in now and the draft is shown again. Why: a map's plan once approved a shape from a drawing that could not be rendered; the owner's first real read came after the second work item and cost a build cycle.

**Exit:** every assumption in the log is ✅ confirmed and the entire end-to-end path is verified to work. Any ❌ sends you back to revise the design (Phase 4/5) — better here than mid-build. **The "Open assumptions" list from Phase 1 must now be empty.**

---

## Phase 7: DESIGN RIGOR PASS (every check must pass — same rigor, session-run)

**Goal:** On the chosen, verified design, run every mental model. The session does this work; the human supplies judgment where flagged. Document pass/fail for each in the PRD. **Do not proceed until all pass.**

The three exit artifacts (the drawable picture of the design) are the centerpiece:

- **Domain model (ERD)** — every entity and how they relate (1:1, 1:many, many:many). Which exist vs. are new.
- **Value stream** — how value flows from trigger to outcome, with every cross-system handoff marked.
- **System narrative (C4 Level 1)** — one paragraph, plain language: what this system does and how its pieces connect. If you can't tell it in a paragraph, the design isn't clear yet.

Then the checks:

| # | Check | What it enforces |
|---|-------|------------------|
| 1 | **Entity-Relationship** | All entities identified, relationships mapped (the ERD). |
| 2 | **State lifecycle** | Every core entity has a `status` field (string/enum, **not** booleans) and a full state map — *including the states you're tempted to skip* (paused, disputed, archived, error). Beginners omit these entirely. |
| 3 | **Entity lifecycle** | Every entity's create→…→terminal path is mapped. |
| 4 | **Transition timestamps** | Every state transition has a timestamp field (`matched_at`, `approved_at`). |
| 5 | **Value stream** | Flow traced end-to-end, trigger to outcome. |
| 6 | **Domain boundaries** | Every system has clear ownership, one interface point (table/webhook/RPC/API), and an explicit contract (produces + consumes, with field shapes). |
| 7 | **Output isolation** | Each system writes only to its own output; no system mutates another's data. Cross-system reads via views/contracts. |
| 8 | **Idempotency** | Every operation touching money or critical state can safely run twice. |
| 9 | **Reuse over rebuild** | **Every new artifact carries a one-line reuse rejection: "Couldn't extend `existing_thing` because ___."** If you can't write it, extend the existing artifact instead. New tables/workflows are built minimum-viable and most-efficient. |
| 10 | **Blast radius** | Affected systems listed; unaffected systems explicitly confirmed; the impact map is complete. |
| 11 | **Pre-mortem** | "3 months out, this failed badly — what went wrong?" Top 3 failure scenarios with defenses. **Time-window check:** if the design stretches the time between two steps that used to run back-to-back (a draft that persists, a queue that buffers, an approval that waits), explicitly ask "what can change in the world between step A and step B, and does step B re-verify it?" Guards written for a minutes-long window silently break at days. (Lesson, 2026-07-15: a design stretched assemble→push from minutes to days; push never re-checked that its inputs were still in the state assemble had seen; caught only at /ship.) |
| 12 | **Expand-and-contract** | If modifying existing contracts, the migration path is defined (add new → migrate consumers → remove old). |

If any check fails, fix the design before continuing.

---

## Phase 8: ONE-SHOT READINESS GATE

**Goal:** The final test before handing to `/build`.

Ask, explicitly: **Could a fresh session — given only this PRD file, with zero memory of this conversation — execute the build in one shot with zero scope change?**

- Is every component specified concretely enough to build without a judgment call?
- Is every dependency verified (validation log all ✅)?
- Is every design check passed?
- **Is every decision, agreed shape, and verified response actually written into the PRD** — nothing load-bearing left in the chat? (Re-read as if you've never seen this project: is anything missing?)
- Does every end-to-end work item over something that branches carry a path table, with no gap row left unresolved?
- When Phase 6 required the owner's read of a rendered draft, is their verdict in the validation log?
- Is there any "we'll figure that out during build" anywhere? (If yes — it isn't done. Figure it out now.)

If anything is unresolved, name it and resolve it. Only when the answer is an unqualified **yes** is the PRD done.

---

## Phase 9: FINALIZE PRD

### PRD Format

```markdown
# PRD: [Project Name]

**Constraint:** [One sentence — the bottleneck this addresses]
**Memo:** [relative path to memo, e.g. ../memos/payout_disputes.md]
**Initiative:** [relative path to the planning folder's state.md and the roadmap item, or "standalone"]
**Kind:** [one of the six kinds, or a composite naming its parts, with the proof each requires — from the Phase 1 briefing] · owes: [documents] · missing: [none | each, with the work item that adds it]
**Date:** [Date]
**Status:** Draft / Approved

---

## 1. Beginning State (verified)

> **In plain words:** [one to three full sentences a non-technical reader can follow — what this section says, fully said, no fragments, and no section numbers, file names, commands or lifecycle jargon: a reader who never opens the technical body must be able to say back what the section claims. Every `##` section and every `### Work Item` opens with this line; the companion shows it first and folds the technical body beneath it.]

[Reassembled current-state picture + reusable-assets inventory]

## 2. Desired State
[One paragraph — what "solved" looks like. Beginning + desired = the gap.]

## 3. Chosen Path
[The selected bridge. If multi-path was run, one line on why this beat the alternatives.]

## 4. System Narrative (C4 L1)
[One plain-language paragraph: what this does and how the pieces connect.]

## 5. Domain Model (ERD)
[Entities + relationships. Which exist vs. new.]

## 6. State & Entity Lifecycles
### [Entity]
[States (incl. skipped ones), transitions, triggers, validations, side effects, timestamp fields]
```chain
[Label]: [state] → [state] → [terminal state]
```
[One line per lifecycle; the companion draws each line as a strip; write states as short names, not clauses.]

## 7. Value Stream
[Trigger → outcome, with handoff points marked]
```chain
[trigger] → [step] → **[handoff]** → [outcome]
```
[One line per stream; bold the handoffs; the prose below keeps the full sentences.]

## 8. Domain Boundaries
### [System]
- **Ownership:** … **Interface:** … **Produces:** {field: type} **Consumes:** {field: type}

## 9. Proposed Changes
[New/modified tables, workflows, contracts — old vs. new where applicable. Each new artifact carries its reuse rejection.]

## 10. Impact Map
**Affected:** … **Unaffected (confirmed):** … **Migration path (if modifying contracts):** …

## 11. Validation Log
[The Phase 6 table — every dependency probed live, all ✅]

## 12. Work Items
> **Rule:** when the blast-radius router (`/build` Phase 4) will fire, no work item contains the publish or the cutover. The last work item verifies against the staged artifact (the bytes on disk that the publish would send) and `/ship` Phase 5 publishes. A live URL is never a prerequisite for an end-to-end check (found at a ship review, 2026-09-22).
> **Rule (every path):** when a work item's verification is end to end and the thing it proves branches (more than one way through: personas, modes, connected or not, error exits), the work item carries a path table (Path · Covered by, the persona or fixture · Proof). List every path the design creates. A path nobody covers is written as a gap row, never left out (`testing_standard.md` rule 10).
### Work Item 1: [Name]
- **Scope:** [system/boundary] — one work item = everything inside one boundary
- **Produces:** [output contract — explicit shape]
- **Depends on:** [nothing / WI-N]
- **Paths:** [the path table, when the rule above applies]
- **Verification:** [specific test or check]

## 13. Design Rigor Checklist
| # | Check | Pass |
| 1 | ERD / entities & relationships | Y/N |
| 2 | State lifecycles (incl. skipped states) | Y/N |
| 3 | Entity lifecycles | Y/N |
| 4 | Transition timestamps | Y/N |
| 5 | Value stream traced | Y/N |
| 6 | Domain boundaries (ownership+interface+contract) | Y/N |
| 7 | Output isolation | Y/N |
| 8 | Idempotency (money/critical ops) | Y/N |
| 9 | Reuse-over-rebuild (every new artifact justified) | Y/N |
| 10 | Blast radius mapped | Y/N |
| 11 | Pre-mortem (top 3 + defenses) | Y/N |
| 12 | Expand-and-contract (if applicable) | Y/N |

## 14. Pre-mortem
### Failure Scenario 1: [Name]
- **What goes wrong:** … **Defense:** …
(×3)

## 15. One-Shot Readiness
- [ ] Every component buildable with zero further decisions
- [ ] Validation log all ✅
- [ ] All rigor checks passed
- [ ] The owner's read of a rendered draft is in the validation log (when the PRD creates or reshapes a document people read; otherwise mark it n/a)
- [ ] Self-contained: a fresh session could one-shot this from the PRD alone (nothing load-bearing left in chat)
- [ ] No "figure it out during build" remaining
```

### Where to save

- `{workspace}/_admin/prds/{project-name}/{project_name}_prd.md` (snake_case file name matching the project).
- Create the project directory if needed. Drafts may live in `_admin/prds/_drafts/` until approved.
- Render the companion at Draft and again at Approved: `python3 ~/.claude/skills/_shared/companion/render.py {workspace}/_admin/prds/{project-name}/{project_name}_prd.md` writes `{project_name}_prd.html` beside it (the plain-words lines first, the technical body folded); then open the page in the default browser when the machine has an opener (`open` on macOS, `xdg-open` on Linux; skip silently otherwise), so it is on screen the moment the document is written. The reviewer approves from the page; the markdown stays the source.
- Memos stay in `_admin/memos/` — link to the memo by relative path in the **Memo** field. One memo may spawn multiple PRDs.
- Completed projects are archived to `_admin/_archive/{project-name}/` by `/build` at close.
- **At approval, create the project's `state.md`** beside the PRD from template §4.8 of `~/.claude/skills/_shared/documentation_standard.md` (Position: Next = WI-1; Verify block = the branch head and test layer as they stand; Held; Needs {owner}; Pointers into this PRD and the contracts), and inside an initiative set the initiative `state.md` milestone row to "PRD approved YYYY-MM-DD; build not started" and its In-flight row to this project. `/build` Phase 1 resumes from it.

### Present for approval

The PRD must be approved before `/build`. Confirm with the user:
- Does this match your intent?
- Are work items scoped by boundary?
- Any concerns about the pre-mortem scenarios?
- **Is the one-shot readiness section an honest, unqualified yes?**

**Mark status "Approved" once confirmed.**

---

## Close: hand off or pause

The approved PRD at `{workspace}/_admin/prds/{project-name}/{project_name}_prd.md` is self-contained — it carries everything `/build` needs, with nothing load-bearing left in chat. Don't auto-advance.

Print the gate document's TLDR, then the **handoff card** (template §4.10), and stop. Its values:
- **Ribbon:** memo ✅ → PRD ✅ → build 0/N → ship ☐ → close ☐ → outcome ☐; WI-1 ▶ (the one `state.md` Next names), the rest ☐.
- **Done:** PRD approved at Gate 2, one-shot ready, with {N} work items. Proved by the validation log, every row ✅.
- **Next:** **Build it:** run `/build {project-name}` (Phase 1-B creates the log; `state.md` already exists), with the line from `python3 .claude/tools/orientation_cost.py --now build`.
- **Needs {owner}:** the keyboard steps or decisions the PRD names as theirs, with task ids.
- **Written:** `{workspace}/_admin/prds/{project-name}/state.md` (Next = WI-1) · `{project_name}_prd.html` · the initiative `state.md` (In flight → this project).

---

## Principles

- **The beginning state is the foundation.** Any variance there corrupts everything downstream. 100% resolution, observed from live systems, zero assumptions.
- **Verify before you commit.** Every dependency is probed live in the PRD, not discovered in the build. The validation log is the proof.
- **One-shot is the exit.** If `/build` would have to make a single scope decision, the PRD isn't done.
- **Self-contained or it's not done.** The PRD carries everything; a fresh session builds from it alone. Anything load-bearing left in the chat is a defect, because the build often runs in a new session.
- **Reuse over rebuild.** Extend what exists. A new artifact you can't justify against the reusable-assets inventory is redundant.
- **Reduce, don't merge.** The smallest bridge that reaches the desired state — never the union of every agent's idea.
- **Agents explore, one mind designs.** Parallelize observation freely; never distribute the design.
- **Boundaries first, internals second.** Get the boundaries right and the internals follow.
- **Explicit over implicit.** Every contract, boundary, and state is written down. If it's not in the PRD, it doesn't exist.
