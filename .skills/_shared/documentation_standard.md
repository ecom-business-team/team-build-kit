# Documentation Standard — Template Library

**The template library implementing the canonical standard at `{workspace root}/documentation_standard.md`** (the workspace-v2 MVA doc: context tiers, placement tests, Diátaxis type discipline, graduated doc sets — read it first; principles live there, templates live here). One canonical template per doc type, so any author's output is indistinguishable from any other's.

**Who points here:**
- `/new-workspace` — **creates** docs from these templates (greenfield) or maps reverse-engineered ground truth into them (brownfield).
- `/build` + `/ship` — **maintain** docs to these specs at the moment of change, and **verify** at close that the docs match the live system and conform to these templates.

When this Standard changes, every skill inherits it. Never copy a template into a skill — point here.

---

## Part 1 — Discernment Rules (what am I instantiating?)

Before any doc is created, place the thing on the spectrum. The level decides the doc set.

| Level | What it is | Examples | Test |
|-------|-----------|----------|------|
| **Workspace** (C4 L1) | A *container* holding multiple separately-built systems | `expense-tracker/`, `client-portal/` | "Does it hold ≥2 things I build and operate separately?" |
| **System** (C4 L3) | A single *buildable thing* with its own internal logic, state, and workflows | `bank-import/`, `categorizer/`, `reports/` | "Is it one thing I develop and run over time?" |
| **Leaf** | Static / reference material, no ongoing build | `course-notes/`, `reading/` | "Is there no ongoing build here?" |
| **Initiative** | A *sequence* of projects that build on each other toward one thesis, replacing or killing systems over months | `expense-tracker/_admin/rebuild/`, `client-portal/_admin/portal-v2/` | "Is this more than one shippable milestone, and does the order matter?" |

**The graduate-up rule (the common team case):** a thing often *starts* as a system that is its own workspace — one build, no container yet. It **graduates** to a workspace the moment it spawns a second system. When that happens, run `/new-workspace` again at the system level to split the second system out, and promote the shared docs (contracts, decisions) to the workspace root. Don't pre-build a container for systems that don't exist yet.

**The interview decides the level — not the user.** `/new-workspace` diagnoses the level from what the user describes and states it back ("This is a *system* — here's the doc set it needs and why"). The user confirms; they never have to know the taxonomy.

**The second question is the kind** (`documentation_standard.md` §4, "The third axis"; definitions in `glossary.md`). The level says how big the thing is; the kind says what it is made of, and it decides the documents a tier does not, the proof, and the practices. Ask in plain words about what runs:

| Kind | Ask |
|------|-----|
| **Automation** | "Is it rented tools wired together — a form, a board, a chat, a workflow tool — where you own the wiring and not the machines?" |
| **Service** | "Is it your own code that runs on its own, with no screen — a worker, a scheduled job, a bot?" |
| **Application** | "Is it your own code with a screen that people sign into?" |
| **Tool** | "Is it your own code that a person runs by hand to get an output — a report, a file?" |
| **Procedure** | "Is it instructions Claude follows — a skill, a hook, a ritual?" |
| **Knowledge** | "Is it something people read — notes, a runbook, a lesson, a mockup?" |

More than one yes inside one thing that owns one set of data is a **composite system**: name each part and its kind, and the `CONTEXT.md` carries a parts table (template 4.2). At workspace level, ask per system; a workspace whose systems share a database is a **system of systems** and takes the Full tier with its eight requirements. The interview decides the kind as it decides the level: state it back, the user confirms, and they never have to name it. On the brownfield fork the kind is not asked at all; it is read from what the agents observe deployed.

---

## Part 2 — The Graduated Doc Set (which docs does it need?)

Required docs scale with what exists. Never create a doc before it's earned — an empty doc is noise that reads as "covered" when it isn't.

| Doc | Required when | Level it lives at |
|-----|--------------|-------------------|
| **`CONTEXT.md`** | Always — every workspace, system, and leaf | The thing itself |
| **`change_log.md`** | The first build ships | Workspace (or system if standalone) |
| **`decision_log.md`** | The first non-obvious decision is made | Workspace root (cross-cutting) |
| **`system_contracts.md`** | The moment a **second** system shares a boundary with the first | Workspace root (cross-cutting) |
| **`architecture.md`** (L2) | Multiple systems with data flows between them | Workspace root |
| **`flow.html`** | The system's kind is automation, or a procedure whose steps change hands between people. Never for an application (it is not a process) | The system folder |
| **Kind + Proved by lines** (inside `CONTEXT.md`) | Always, from 2026-09-20; an index written earlier gains them at its next change by a build or a quick fix | The system's `CONTEXT.md` (template 4.2) |
| **Parts table** (inside `CONTEXT.md`) | The system is composite — several kinds ship as one unit | The system's `CONTEXT.md`, under the Kind line |
| **`north_star.md`** | An initiative is declared | The planning folder — the compass and the initiative's memo (template 4.11); decisions only, never progress |
| **planning-folder `CONTEXT.md`** | An initiative is declared | The planning folder — the index (template 4.9) |
| **`state.md`** (initiative) | A planning folder exists (`documentation_standard.md` §4) | The planning folder — the snapshot: project in flight, milestone table, handed-forward tray; ≤600 words, rewritten in place |
| **`state.md`** (project) | A PRD is approved | `_admin/prds/<project>/` — the snapshot: position, next, verify block, held, needs the owner; ≤400 words, rewritten in place; archived with the folder |
| **companion `.html`** | Beside each of the four gate documents (memo, PRD, project log, state file), written by the skill that writes the document | The document's folder; generated, never edited; moved with its source |

**Leaf** = `CONTEXT.md` header only (the opening paragraph with its Kind line, and Proved by). **Procedure** = its `SKILL.md` is the document, plus a row in `SKILLS.md`; it gets no `CONTEXT.md` of its own. **Standalone system** (its own workspace) = `CONTEXT.md` + `change_log.md` + `decision_log.md` as it earns them; contracts/architecture only after it graduates. **Mature workspace** = all of the above.

`flow.html` is not templated here — it has its own base template, named in the workspace's root CLAUDE.md under "Words the skills use". This Standard governs the markdown docs.

### The skeleton — folders that exist from day one

Documents are created when their phase starts (lazy); the folders they go into exist from creation (eager). `/onboard` creates the root skeleton; `/new-workspace` Phase 3 creates an area's.

**Root** (the workspace folder):

```
{workspace}/
├── AGENTS.md              ← one line, below
├── .gitignore             ← below
├── _admin/
│   ├── memos/_done/
│   ├── prds/
│   └── _archive/
├── daily-outputs/
├── bulk_ops/INDEX.md      ← template 4.12
├── .claude/skills.d/
└── tasks.md               ← only when the owner has no task manager this session can write to (template 4.13)
```

**Area**, by level and kind:

```
system      → _admin/memos/_done/ · _admin/prds/ · _admin/_archive/
workspace   → the same, plus bulk_ops/INDEX.md        (a container of systems)
leaf        → nothing
initiative  → its planning folder, unchanged
kind automation, or a procedure that changes hands
            → flow.html, copied from ~/.claude/skills/_shared/flow_base.html
```

The area's `CONTEXT.md` "What lives here" names each entry created.

Every folder the skeleton leaves empty gets an empty `.gitkeep` file, because git does not keep an empty folder and a clone or fresh checkout would otherwise arrive without it.

`AGENTS.md` text, exactly:

```
This workspace's map is CLAUDE.md. Read it first; it routes to every folder's CONTEXT.md.
```

`.gitignore` text, exactly, one per line:

```
.env
.DS_Store
__pycache__/
node_modules/
```

A bulk write's prestate goes in the owning area's `bulk_ops/`, or the workspace root's when the area has none.

---

## Part 3 — Universal Content Rules (apply to every doc)

1. **Point to the source of truth — don't copy it.** Reference identifiers, table and field names, and the system's own descriptions — never paste raw exports or schema dumps. When the live system changes, a reference still points right; a copy goes stale. (Where the live system stores its own descriptions — e.g. database field comments — those are authoritative; reference them by name rather than copying.)
2. **Accuracy over completeness.** Whatever is written must be 100% true *now*. A confidently-wrong line is worse than an omission. A thin accurate doc beats a thorough drifted one.
3. **Living, not historical.** These docs answer "what is true now?" — update them at the moment of change, not at session close. (Completed memos/PRDs/logs are the *static* record; these are not.)
4. **Never create empty sections.** Include a section only when it has content. A template section with no content is deleted, not left as a placeholder.
5. **One canonical home per fact.** If a fact crosses a system boundary it lives at the workspace root (contracts/decisions); if it's internal to one system it lives in that system's `CONTEXT.md`. Everywhere else references it.
6. **Plain language, fully said.** Write for a non-technical teammate: complete sentences, every idea fully said, the example walked through. Arrows and dots are notation for state sequences, paths and trees, never sentence glue; no colon-labels, no fragments. Use every lifecycle term exactly as the workspace's `glossary.md` defines it, and define any new term where it first appears.
7. **Two words the workspace supplies.** Skills, templates and standards say **the owner** (the person whose word the gates wait on) and **the task manager** (where every task and date lives). Wherever a document is written for a person, write the names the workspace's root `CLAUDE.md` declares under "Words the skills use", so a card reads "Needs Maria" in one workspace and "Needs Sam" in another; a `{owner}` slot in a template means the same. If the CLAUDE.md declares nothing, write the words themselves. Nothing in these templates or in the skills names a person or a tool directly; the check `.claude/tools/names_check.py`, run from the workspace root, derives the names from that section and the workspace's own folders and prints every line of the box that still carries one.

---
## Part 4 — The Templates (one per doc type)

Fill the skeleton; delete any section without content. These are the exact shapes — do not improvise structure.

---

### 4.1 — Workspace `CONTEXT.md` (L1 — the map)

**Purpose:** Answer "what is this workspace, what systems are inside it, and where do I go for X?" in one read. It is the routing layer.
**Maintained by:** `/build`/`/ship` when a system is added/renamed/removed.

```markdown
# {Workspace Name}

{One-paragraph description — what it does, who it's for, why it exists.}
{Example: "Expense tracking for a small team — routes receipts through import and categorisation before they reach the monthly report."}

**Tech Stack:** {technologies}
{Example: your automation tool, your database, your board, your chat app, your AI model}

---

## Systems & Routing                    ← only if ≥2 systems exist
| System | What it does | Go here for |
|--------|--------------|-------------|
| {folder}/ | {one line} | {tasks that belong here} |
| {Example: reports/} | {Builds the monthly spending report} | {Totals, categories, exports} |

## Canonical Homes                      ← only once cross-cutting docs exist
| Doc | What lives there |
|-----|------------------|
| system_contracts.md | Field mappings + boundary contracts |
| decision_log.md | Cross-cutting decisions + rationale |
| change_log.md | What shipped |

## Integrations                         ← only if external systems connect
| System | Purpose | Details |
|--------|---------|---------|
| {Example: a bank-sync service} | {Transaction import} | {API key in .env; sandbox + prod} |

## Quick Start                          ← only if non-obvious first steps exist
1. {Example: "Auth: gcloud auth application-default print-access-token"}
```

---

### 4.2 — System `CONTEXT.md` (L3 — the local index)

**Purpose:** Answer "how does this system work and where does X live?" without leaving the folder. This is what makes the handoff test pass.
**Maintained by:** `/build`/`/ship` at the end of each work item that changes structure.

```markdown
# {System Name}

{One-paragraph: what this system does and its current state.}

**Owns:** {the one thing this system is responsible for — its boundary in a sentence.}
{Example: "Owns the monthly report lifecycle from import to export. Does NOT own categorisation rules or bank credentials."}

**Kind:** {one sentence: one of the six kinds, or "a composite system: a {kind} with a {kind} on top and {kind}s beside it", and who writes its data.}
{Example: "A service (the import worker on the host) with an application on top (the review page) and procedures beside it (/onboard-account). It owns its import tables and is their one writer."}

**Proved by:** {the proof this kind requires (documentation_standard.md §4, the kinds table), as it exists here — or "not yet stated".}
{Example: "pytest on every change; a live probe of the deployed API before each deploy; the Ops Digest is its noticer."}

## Parts                                 ← only for a composite system
| Part | Kind | Code lives at | Writes |
|------|------|---------------|--------|
| {part} | {kind} | {path or repo} | {the tables or files it is the one writer of} |
| {Example: hosted module for ../categorizer/} | {service (a module)} | {service/src/importer/categorizer/} | {category_assignments} |

---

## What lives here
| File | What it is | Living / Disposable |
|------|-----------|---------------------|
| {file} | {purpose} | {living/disposable} |
| {Example: payout_calc.md} | {Calc logic + rate rules} | {living} |

## How to find X                        ← only for non-obvious lookups
| Question | Where to look |
|----------|---------------|
| {Example: "Why was a creator underpaid?"} | {payout_adjustments table + /payout-adjust} |

## Workflows                            ← only if it has workflows
| Workflow / component | ID / location | Trigger | Purpose |
|----------------------|---------------|---------|---------|
| {Example: Payout Calculation} | {automation id / file path} | {monthly schedule} | {computes per-creator totals} |

## Current State
- **Status:** {what's deployed / in progress}
- **Pending:** {open items, or "none"}

## Points up                            ← cross-system contracts this system participates in
- system_contracts.md — {which boundaries}
- decision_log.md — {relevant decisions}

## Points down                          ← only if it has sub-areas / where implementation lives
- {sub-folder}/ — {what's inside}
- {Example: scripts/ — Python recompute + backfill jobs}

## Don't Load (for this system)         ← only if sibling docs are commonly mis-loaded
- {folder}/ — {why irrelevant to this context}
```

---

### 4.3 — `system_contracts.md` (workspace root — cross-system)

**Purpose:** Single source of truth for every data handoff between systems. Change a field in one system → check here for what else must change.
**Required when:** a second system shares a boundary with the first.
**Maintained by:** `/build`/`/ship` whenever a field crosses a boundary is added/renamed/removed.

```markdown
# System Contracts

**Purpose:** Single source of truth for every data handoff between systems. When you change a field in one system, check this doc to see what else needs to change.

**Rule:** If a field crosses a system boundary, it goes in this doc. Update it whenever you add/rename/remove a boundary field.

---

## Canonical Field Names
These names mean the same thing everywhere. Never mix them.

| Canonical Name | Meaning | Example Value |
|---------------|---------|---------------|
| `{name}` | {meaning} | `{example}` |
| `creator_id` | Creator's public ID (generated on approval) | `CREATOR-X7K9M2` |
| `brand_id` | Brand slug (URL-safe identifier) | `dog-friendly` |

**When naming a URL param, hidden field, variable, or column — use the canonical name.**

---

## Boundary: {System A → System B}
**Produces:** `{field: type, ...}`
**Consumes:** `{field: type, ...}`
**Source of truth:** {where the value is authoritative}

{Example —
**Boundary: QA Pipeline → Payout System**
**Produces:** `{creator_id: text, submission_id: uuid, final_status: text, approved_at: timestamptz}`
**Consumes:** `{creator_id, approved_at}` (payout attributes spend to the approving period)
**Source of truth:** `submissions.final_status` — see its column comment}
```

---

### 4.4 — `decision_log.md` (workspace root — cross-cutting)

**Purpose:** Record major architectural/design decisions with rationale. Explains WHY things were built this way.
**Required when:** the first non-obvious decision is made.
**Maintained by:** `/build`/`/ship` (append) and `/prd` (when a design decision is locked). Append-only; numbered sequentially.

```markdown
# {Workspace} - Decision Log

**Purpose:** Record all major architectural and design decisions with rationale. Explains WHY things were built the way they are.
**Format:** Each entry includes the decision, alternatives considered, rationale, and potential future changes.
**Archive:** {Entries 1-N archived at `_admin/_archive/decision_log_archive.md`}   ← add once the log grows large

---

## Decision Index
N. [{Title}](#n-{anchor})

---

## {N}. {Title}
**Decision:** {what was decided}
**Alternatives considered:** {what else was on the table}
**Rationale:** {why this won}
**Future changes:** {what might revisit this, or "none anticipated"}
**Date:** {YYYY-MM-DD}

{Example —
## 51. Why Flat Rate Over Tiered or Pool Models
**Decision:** Pay creators a flat % of ad spend, not a tiered or shared-pool model.
**Alternatives considered:** Tiered rates by performance; a fixed monthly pool split across creators.
**Rationale:** Flat rate is predictable for creators and trivially auditable; tiers invite gaming and pool-splits punish high performers.
**Future changes:** Revisit if spend volume makes flat rate unsustainable.
**Date:** 2026-03-02}
```

---

### 4.5 — `change_log.md`

**Purpose:** What shipped, in human terms. Keep a Changelog format.
**Required when:** the first build ships.
**Maintained by:** `/build`/`/ship` with an entry per build.

```markdown
# Changelog

All notable changes to {workspace/system}. Format: [Keep a Changelog](https://keepachangelog.com).

## [Pre-Production]
### Added
- {what was built}
- {Example: "Payout adjustments: /payout-adjust skill + payout_adjustments table for underpayment top-ups."}
### Changed
- {what changed}
### Fixed
- {what was fixed}
```

---

### 4.6 — `architecture.md` (L2 — optional)

**Purpose:** How the systems connect — the container-level data-flow view between L1 (map) and L3 (system internals).
**Required when:** multiple systems with data flows between them.
**Maintained by:** `/build`/`/ship` when a cross-system flow is added or changed.

```markdown
# {Workspace} Architecture

How the systems connect. (System internals live in each system's CONTEXT.md; field-level contracts live in system_contracts.md — this is the flow view.)

---

## System Map
{Systems and the direction of data flow between them — ASCII diagram preferred.}
{Example:
  Bank Import ──transactions──▶ Categorizer ──categorized──▶ Reports
       │                              │
       └──────▶ Ops Dashboard ◀───────┘  (reads both via shared views)}

## Data Flows
| From | To | What flows | Via |
|------|----|-----------|----|
| {system} | {system} | {data} | {trigger / table / API call} |
| {Example: QA Pipeline} | {Payout System} | {approved submissions} | {submissions table} |
```

---

### 4.7 — Initiative `state.md` (the snapshot above the projects)

**Purpose:** Answer "where does this initiative stand, and what does the next project inherit?" in one read of at most 600 words. Rewritten in place, never appended. History lives in the archived project logs; decisions and the roadmap live in `north_star.md`.
**Maintained by:** `/memo` (milestone row → memo cleared), `/prd` (milestone row → PRD approved; In flight set), `/build` and `/ship` at close (milestone row → shipped; tray refilled), and any session that changes position.

```markdown
# State — {initiative}
<!-- SNAPSHOT. Rewritten in place at every project open/close and whenever the tray changes. Budget 600 words. Order + rationale: north_star.md §{roadmap}. History: the archived project logs. -->
**Updated:** {YYYY-MM-DD} · {what changed, one clause}

## In flight
- **Project:** {none | project name → `../prds/{project}/state.md`}
- **Next to open:** {project} (roadmap #{n}) → starts at `/memo`

## Milestones
| # | Milestone | Memo | PRD + log | Status |
|---|---|---|---|---|
| {n} | {name} | {path or —} | {path or —} | {queued · memo cleared {date} · PRD approved {date} · building WI-k of N · paused {date} (waiting on …) · shipped {date} · outcome check due {date} · ✅ reached {date} · killed {date} — reason} |

## What the next project inherits (the tray)
An item leaves when it is decided (→ north_star / decision_log), homed (→ a system doc), or done (→ closed in the task manager).

**Live and depended on:** {objects the next projects read or must not break — one line, pointing at the system doc that owns the facts}
**Held switches:** {flags nobody has flipped · task id}
**Undecided (the task manager):** {decision · id}
**Human steps outstanding:** {step · id · due}
**Verified facts the next projects rest on:** {one line each, source in brackets}
**Outcome checks pending:** {milestone · the memo's success definition, by pointer · due {date} · task id} — a milestone reads `reached` only when this is verified against real use (`_shared/project_close.md` §5)
```

---

### 4.8 — Project `state.md` (the snapshot inside a build)

**Purpose:** Answer "where is this build, what is next, and how do I know the snapshot is true?" in at most 400 words, so a fresh session resumes in minutes. Rewritten at every work-item boundary and every session end, never appended. The record is `project_log.md`.
**Maintained by:** `/prd` (creates it at approval), `/build` and `/ship` (rewrite per work item and per Gate-3 round), `session-close`.

```markdown
# State — {project}
<!-- SNAPSHOT. Rewritten in place at every work-item boundary and session end. Budget 400 words. History: project_log.md. -->
**Initiative:** {../../<initiative>/state.md | standalone} · **PRD:** {project}_prd.md · **Memo:** ../../memos/{project}.md
**Updated:** {YYYY-MM-DD HH:MM} · session {id8}

## Position
- **Stage:** {memo ✅ · PRD ✅ · build k/N · ship ☐ · close ☐ · outcome ☐}
- **Done:** {WI-1 … WI-k — verified; proof in the log}
- **Next:** {WI-k+1 — name (PRD §12) | end-of-build verification | Gate 3 round n | close}
- **Blocked:** {none | what · on whom · task id}
- **Router:** {not yet run | fired → /ship | clean}

## Verify before continuing (≤3 commands, expected results)
1. `{git -C … log -1 --format=%h {branch}}` → `{hash}`
2. `{the fast test layer}` → {green, N checks}
3. `{one live probe}` → {expected}

## Held
- {switch or deploy held, and on whose word}

## Needs {owner}
- {decision or keyboard step · task id}

## Pointers (read by section, never whole)
- {PRD §… · system_contracts.md Boundary … · {system}/CONTEXT.md "…" · _practices/….md §…}
```

---

### 4.9 — Planning-folder `CONTEXT.md` (the initiative's index)

**Purpose:** The local index of a planning folder (`documentation_standard.md` §4): what the initiative is, what lives in the folder, and how to resume in three lines that point at `state.md`. Position never lives here; decisions never live here.
**Maintained by:** whichever session adds or removes a file in the folder.

```markdown
# {Initiative} — {one line: what it converts or builds}

{One paragraph: what the initiative is, its close condition, and that every project runs /memo → /prd → /build → /ship.}

**Three documents, three jobs.** `north_star.md` is the **compass** (decisions, never progress). `state.md` is the **snapshot** (in flight · milestone table · handed-forward tray; ≤600 words, rewritten). This file is the **index**. About a decision, the north star wins; about position, `state.md` wins.

## What lives here
{tree with one-line purposes, each marked living / disposable / spec}

## How to resume in a fresh session
1. `cat state.md`.
2. Read the `north_star.md` sections the work touches — by section, never whole.
3. Dates, blocking decisions, open questions: the task manager's project "{name}".

## Practices
{the standards and _practices files a project loads}
```

---

### 4.10 — The handoff card (printed at every stop)

**Purpose:** Every stop — a gate cleared, a work item done, a session ending, work waiting on the owner — prints the same six lines, so the owner always sees where the work sits on the ladder (initiative › milestone › project › work item) and exactly what to type next. Emitted by `/memo`, `/prd`, `/build`, `/ship`, `/new-workspace`, `/convert-to-standard` and `session-close`. The same Where and Next lines live in the project `state.md` (its **Stage** and **Next** fields), so the SessionStart gate prints them at the top of the next session: the card at the end of one session and the gate line at the start of the next say the same thing.

```
HANDOFF
Where:  {initiative} · milestone {n} {name} · project: memo ✅ · PRD ✅ · build k/N · ship ☐ · close ☐ · outcome ☐
Done:   {what just finished} — proved by {the check and its result}
Next:   {what} — run: {exact command or prompt}
Context: {the line printed by python3 .claude/tools/orientation_cost.py --now {the step Next names}}
Needs {owner}: {decision or keyboard step · task id · due} | none
Written: {path to the project state.md; between projects, the initiative state.md}
```

A standalone build (no initiative) writes "standalone" in Where. "Next" is always the exact command the owner types, verbatim: a skill call with its argument (`/build {project}`, `/ship {project}`), never "any prompt" — the owner should never have to know where the state file lives.

**Context** is measured, never guessed: run the tool with the lifecycle step the Next line names (`memo`, `prd`, `build`, `ship` or `quick-fix`) and copy its line verbatim. If the command fails or prints anything other than one line starting `Context:` (the tool is missing, older than `--now`, or was run outside the workspace root), write `Context: not measured (the tool did not run) → hand off fresh` and hand off fresh. It adds that step's typical cost to the session's measured context and gives the verdict against 300k (`_practices/claude-code.md`, Context cost). Continue here when it says so; otherwise the owner types `/clear` and then the Next command. The owner's word overrides the verdict either way, and a build logs the override in `project_log.md`.

---

### 4.11 — `north_star.md` (the initiative's compass, and its memo)

**Purpose:** The one place every decision about an initiative lives — what it is for, what it must never do, how it will be built, in what order, and what is still open. It is the initiative's memo: the thesis, principles and journeys are the proposition, the non-goals are the boundary, the roadmap is the ordered set of milestones; every project memo points into it instead of restating it. It never carries progress — that is `state.md`. Written from the first two initiatives that used it (2026-09).
**Maintained by:** the session in which a decision is made — edited first, the same session. Open points become tasks in the task manager and are struck through here with the dated resolution when decided.

```markdown
# {Initiative} — north star

**The one document.** {One paragraph: everything decided about this lives here and every other artifact points here — CONTEXT.md is the index, state.md the snapshot, the task manager holds dates and open questions, the spec appendices are verified by the PRDs.}
**How it changes.** A decision is edited here first, the same session it is made. The compass sections rank what to build next; they are never acceptance criteria for a project.
**Status.** Lives in `state.md`.

## 1. Thesis and positioning
{What this is, in one paragraph, and what it is deliberately not a copy of. The status quo it beats.}

## 2. Principles we build by
{Numbered; each a sentence a project can be checked against. Non-negotiables inherited from live systems ("what true means here") go first.}

## 3. Actors and their perfect journeys
{Per actor: the journey as one paragraph of → steps, then "what today makes hard". These are the requirements.}

## 4. Objects and their lifecycles
{Per object: one line, its states from create to terminal.}

## 5. Architecture decisions
{Bulleted; each decided and dated, with what it supersedes.}

## 6. Cutover rules every project obeys
{Numbered rules for moving live behaviour without breaking it.}

## 7. Roadmap — the milestones
{Ordered list. Each: the name in bold, what will be true when it is reached, what it kills or replaces, what it depends on. The numbers are names; the run order is decided in dated notes here and tracked in state.md.}

## 8. What dies, what survives
{Table: today · verdict · at which milestone.}

## 9. Non-goals
{What this will never do, so a project memo can say what it is NOT by pointer.}

## 10. Open points
{Numbered; each is or becomes a task in the task manager; struck through with the dated resolution when decided.}

## Appendices
{Spec files the PRDs verify (an event catalogue, a screen inventory); disposable inputs (research files).}
```

Delete any section without content. A first version with only §1, §3, §7 and §10 is legitimate; the rest are written when their decisions exist. Keep paragraphs one idea long — a 400-word single line cannot be read by section.

---

### 4.12 — `bulk_ops/INDEX.md` (the undo register)

**Purpose:** One row per bulk write, so every large change can be found and undone from its prestate. Part of the skeleton (Part 2): created empty, with its header, by `/onboard` at the root and by `/new-workspace` for a workspace-level area.
**Maintained by:** the session that runs the bulk write — the prestate folder and the row are written before the write.

```markdown
# Bulk operations — index

One row per bulk write (more than 10 rows, a backfill or a restore). The prestate is snapshotted into the write's folder before the write; it is the undo.

| Date | Folder | What changed | Rows | Prestate | Reverted? |
|---|---|---|---|---|---|
```

---

### 4.13 — `tasks.md` (the task manager, when no app is connected)

**Purpose:** The one sanctioned markdown task list, used only when the owner has no task manager this session can write to. It is the task manager for that workspace: the lifecycle files tasks and outcome checks here by id, and the SessionStart gate prints every open line whose due date has arrived.
**Maintained by:** every skill that files a task (the same rules as any task manager: title = verb + outcome, the why, the pointer, the next action). A line is ticked when done, never deleted; ids are never reused.

```markdown
# Tasks

This workspace's task manager: no app is connected, so tasks live here. One line per task; tick it when done, never delete it; the session start prints every unticked line whose due date has arrived. Write each line exactly as `- [ ] T-001 · due YYYY-MM-DD · {verb + outcome} — {why} · next: {next action} · {pointer}` (the `due` part optional), because the session start reads only that shape.

## Next

## Blocked

## Waiting
```

Line format (the `due` part optional):

```
- [ ] T-001 · due YYYY-MM-DD · {verb + outcome} — {why} · next: {next action} · {pointer}
```

---

### 4.14 — Stage `CONTEXT.md` (one stage of a pipeline)

**Purpose:** The contract of one stage of a repeating process built in the pipeline form (`stages/NN_<stage>/` with `CONTEXT.md`, `references/`, `output/`): what it reads, what it does, what it writes, and the one thing a person checks before the next stage reads its output. Written by `/new-workflow` Phase 4P.
**Maintained by:** whoever changes the stage; the owner edits `output/` in place at the Human check.

```markdown
<!-- Adapted from ICM's stage-CONTEXT.md, MIT, © 2026 Jake Van Clief — github.com/RinDig/icm-architect -->
# {NN}_{stage} — {the job in five words}

One job: {…}.

## Inputs
- Working input: `../{previous stage}/output/{file}`
- References: {files in references/}
- Do NOT load: {…}

## Process
1. {…}

## Outputs
- {artifact} → `output/`

## Human check
{One concrete act a person does, stated as an action. They edit the output in place; the next stage reads whatever is there.}
```

The pipeline's own `CONTEXT.md` is template 4.2 with the Kind line `procedure (pipeline form)` and a stage table:

```markdown
| Stage | Job | Human check |
|---|---|---|
```

---

## Part 5 — Definition of Done (both forks converge here)

`/new-workspace` is done — greenfield **or** brownfield — when:

1. The thing's **level** (workspace / system / leaf / initiative) and its **kind** (one of the six, or the parts of a composite) are named and confirmed.
2. **Exactly the graduated doc set** for that level exists — nothing required missing, nothing unearned created.
3. Every doc **conforms to its template** in Part 4 (an outsider couldn't tell who authored it).
4. Every doc is **100% accurate to reality:**
   - **Greenfield** — accurate to the just-defined (minimal) reality.
   - **Brownfield** — *verified* against the live deployed system (the `/prd` Phase 1 bar: observed, not assumed), with interview only to fill genuine gaps.
5. Root `CLAUDE.md` routing is updated (flag for approval per the Living Documentation Rule).

The forks differ only in how the docs get populated and what "accurate" measures against — the destination is identical.
