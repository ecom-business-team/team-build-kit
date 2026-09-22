---
name: new-workspace
description: Instantiate (or bring up to standard) a workspace, system, leaf, or initiative (the planning folder above a sequence of projects) with its full living-documentation foundation. Diagnoses the level and the kind (what it is made of) from a short interview, then provisions exactly the doc set the level and the kind assign — greenfield (create from templates) or brownfield (reverse-engineer 100% ground truth from the live system, then fill gaps). Produces docs indistinguishable in format from the rest of the workspace, because every doc is generated from the canonical Documentation Standard. Run before /memo → /prd → /build so the lifecycle has a documentation substrate to stand on.
---

# /new-workspace

Stand up the **documentation foundation** for anything you'll build and operate over time — a new workspace, a new system inside one, or a leaf. The lifecycle skills (`/memo → /prd → /build → /ship`) *operate on* living docs; this skill is what creates and maintains the substrate they require.

**The single source of truth for all formats, rules, and the doc set is the Documentation Standard:** `~/.claude/skills/_shared/documentation_standard.md`. This skill is the *procedure*; the Standard is the *spec*. Read the Standard at the start of every run — never improvise structure, never copy a template in here.

## The three things this skill resolves

1. **Level** — is this a **workspace** (container of systems), a **system** (one buildable bounded context), or a **leaf** (static/reference)? The skill diagnoses it (Standard Part 1); the user confirms. The level decides the doc set (Standard Part 2).
2. **Kind** — what is it **made of**: automation, service, application, tool, procedure or knowledge, or a composite of several (Standard Part 1, the kinds table; definitions in the workspace `glossary.md`). The kind decides what the level cannot: the documents it adds (a `flow.html` for a process, none for an application), the proof it must pass, and the practices its `CONTEXT.md` lists.
3. **Fork** — is this **greenfield** (nothing built yet) or **brownfield** (already built, no standard docs)? The fork decides how the docs get populated. Both forks converge on the same end state (Standard Part 5).

## Usage

```
/new-workspace                      — interview decides level + fork
/new-workspace reports            — name given, interview the rest
/new-workspace --brownfield payout  — skip the fork question, go straight to extraction
/new-workspace --initiative platform-rebuild — the planning folder above a sequence of projects (compass, snapshot, index)
/convert-to-standard <folder>       — the same fork, by its own door
```

## When to Use

- Starting a brand-new build (greenfield) — before `/memo`
- Bringing an existing, undocumented build up to standard (brownfield)
- Adding a new system to an existing workspace
- A workspace has "graduated" — a system spawned a second system and needs splitting out

## When NOT to Use

- The thing already has standard-conformant docs (use `/build`/`/ship` to maintain them)
- A one-off fix (use `/quick-fix`)

---

## Phase 1: DISCERN — level, fork, kind

**Read the Documentation Standard first.** Then a short, conversational interview (not a form).

### Diagnose the LEVEL (Standard Part 1)
Ask enough to place the thing:
- "What is this — one sentence?"
- "Does it hold multiple things you build and run separately, or is it one buildable thing?"  → workspace vs system
- "Is there ongoing development here, or is it static/reference?" → system vs leaf
- "Is this one build, or a *sequence* of shippable milestones that build on each other and replace or kill systems over months?" → a project (send them to `/memo`) vs an **initiative**

**State the level back with reasoning, and the doc set it implies:**
```
This is a SYSTEM (one buildable bounded context — the payout lifecycle).
Per the Standard it needs: CONTEXT.md now; CHANGELOG.md + decision_log.md as it earns them.
It does NOT yet need system_contracts.md (no second system sharing a boundary).
Confirm?
```
Or, for the fourth level:
```
This is an INITIATIVE (a sequence of milestones, each its own project — e.g. a platform rebuild).
Per the Standard §4 it needs a planning folder `_admin/<initiative>/`: CONTEXT.md (the index, template 4.9),
state.md (the snapshot, 4.7) and north_star.md (the compass and the initiative's memo, 4.11). Research inputs
land as they arrive; spec appendices when a PRD needs them. Its first milestone then starts at /memo (short form).
Confirm?
```
The user confirms or corrects. They never have to know the taxonomy — you carry it.

### Determine the FORK
- "Is anything already built for this — workflows, tables, code, endpoints — or are we starting clean?"
  - **Nothing built → greenfield** (Phase 2a)
  - **Already built, no standard docs → brownfield** (Phase 2b)

### Diagnose the KIND (Standard Part 1, the kinds table)
Ask what runs, in the table's plain words — never the taxonomy: "Is it your own code, or tools you rent wired together? Does it have a screen people sign into? Does it run on its own, or does a person run it? Or is it instructions Claude follows, or something people read?" More than one yes inside one thing that owns one set of data → a composite; name each part. **Brownfield (the fork was settled just above): do not ask** — the Phase 2b agents observe what is deployed and the kind is read from that.

State the kind with the level, and what the kind changes:
```
This is a SYSTEM of kind SERVICE (your own code, running unattended on a host).
Per the Standard its CONTEXT.md carries its Kind and Proved-by lines; no flow.html (a service is not a process);
data_dictionary.md because it owns a table. Its proof: tests on every change, a live probe, and a noticer that fires.
Practices it will list: deploying.md and the host's and the database's practice files.
Confirm?
```

> **Graduate-up check:** if the user describes a second system appearing inside what was a standalone system, this is a *graduation*. Split the second system into its own folder and promote shared docs (contracts, decisions) to the workspace root. Don't pre-build a container for systems that don't exist.

---

## Phase 2a: GREENFIELD — define, then provision from templates

**For an initiative — the north-star interview.** The memo has six input rows; the north star has seven. Ask them in the owner's terms, in this order, and write each answer into its section of `north_star.md` (template 4.11) as you go:

| Ask the owner | Section it fills |
|---|---|
| "When this is finished, what will be true that is not true today — in one paragraph?" | §1 Thesis |
| "Who lives differently, and how does their day go, start to finish?" — one actor at a time, then "what makes that hard today?" | §3 Journeys — these are the requirements |
| "What dies, what survives, and what must never get worse while we do this?" | §8 Dies / survives · §2 Principles (the non-negotiables) |
| "What are the big steps, in order — and for each, what will be true when it is reached?" | §7 Roadmap — the milestones; each "what will be true" is that milestone's success definition |
| "Which step first, and why that one?" | §7 dated order note → `state.md` Next to open |
| "What will this never do?" | §9 Non-goals |
| "What don't we know yet?" | §10 Open points → one task each in the task manager |

Architecture decisions (§5) and cutover rules (§6) are written when they are decided — usually in the first PRD — never invented in the interview. What is not known goes to *Open points*, never guessed; a first version with only §1, §3, §7 and §10 is legitimate.

**Read it back before writing anything.** Two paragraphs, in plain words: *here is where we are going* (§1) and *here are the steps, in order, and what each one makes true* (§7). The owner confirms or corrects; only then provision. Stop when the first milestone is named with its "what will be true" — that is enough to open `/memo` (short form) for it. `state.md` starts with In flight = none, Next to open = that milestone, an empty tray.

The thing doesn't exist yet, so the docs describe what *will* exist (kept minimal and accurate).

Interview to fill what each required doc needs (follow the conversation; stop when you have enough):
- **Purpose** — what it does, who it's for, why it exists.
- **Tech / integrations** — stack, external services, APIs, databases.
- **Pieces** (workspace only) — the systems inside it and how they connect.
- **Boundaries** — what it owns vs. explicitly does not.
- **Gotchas** — prerequisites, credentials, non-obvious first steps.

Then go to Phase 3 with the answers mapped onto the Standard's templates.

---

## Phase 2b: BROWNFIELD — reverse-engineer 100% ground truth, then fill gaps

**For an initiative**, the material is planning matter rather than a running system — a handoff, an index, a Google Doc, a backlog, chat — plus the live systems it names. The agents read both; `north_star.md` records only what is decided (dated, with its source) and marks the rest open. Any project already shipped under the initiative gets its milestone row and its handed-forward items reconstructed from its archive into `state.md`.

The thing already exists with no standard docs. **The docs must describe what is *actually deployed* — verified, not assumed.** Apply the same bar as `/prd` Phase 1: observe the live system, don't infer.

### Step 1 — Observe (agents, one per area the build touches)
Spawn ground-truth agents (they report facts, not designs — divide by area freely, you reassemble). Use the right observation tool for the workspace's stack — load its tool-skill where one exists; observe live state, never infer:
- **Automations / workflows** — observe each live automation directly; its configuration, connections, credentials, data flow, identifiers.
- **Data stores** — inspect a real sample of the live data; fields, types, relationships, conventions, stored procedures, views, embedded descriptions.
- **App / code** — routes, handlers, modules, entry points, deploy state.
- **External services** — endpoints, auth, real request/response shapes.
- **Existing scraps** — any READMEs, notes, partial docs already lying around.
- **What each part is made of at runtime** — own code or rented tools, a screen or none, unattended or run by hand — so the kind is observed rather than asked, and whether another folder's code runs inside this unit.

### Step 2 — Reassemble into the verified picture
You (main session) reassemble agent reports into one coherent ground-truth picture: what exists, how it connects, what the boundaries actually are. Note anything observation can't settle — those become interview questions, not assumptions.

### Step 3 — Interview only to fill genuine gaps
Ask the user only what the live system can't tell you: *why* decisions were made (→ decision_log), what's intentional vs. accidental, what's deprecated, what the boundaries are *meant* to be.

Then go to Phase 3, mapping the verified picture onto the Standard's templates. Every line must trace to something observed or explicitly confirmed.

---

## Phase 3: PROVISION — write the doc set

1. **Determine the required set** for the confirmed level **and kind** (Standard Part 2, and the kinds table in `documentation_standard.md` §4). Create *exactly* that — nothing required missing, nothing unearned.
2. **Create the folder(s)** if greenfield (or if a brownfield system needs a home).
3. **Write each doc from its Standard template** (Part 4), applying the universal content rules (Part 3): point-to-source, accuracy over completeness, never empty sections, one canonical home.
4. **Create-if-missing for canonical homes:** if a required cross-cutting doc (`system_contracts.md`, `decision_log.md`) doesn't exist at the workspace root and the level now needs it, create it now — never defer (CLAUDE.md: undocumented architecture is a blocking task).
5. **Update root `CLAUDE.md` routing** — the Routing table, and the Workspaces table when the file has one. Flag for approval per the Living Documentation Rule before writing.

**Confirm the plan before creating anything** (show the folder tree + the doc set + why each doc). Never overwrite an existing file — if one exists, offer to update or skip.

---

## Phase 4: VERIFY — against the Definition of Done

Walk the Standard Part 5 checklist explicitly:
1. Level and kind named and confirmed (a composite names each part).
2. Exactly the graduated doc set exists — nothing required missing, nothing unearned.
3. Every doc conforms to its template (an outsider couldn't tell who authored it).
4. Every doc is 100% accurate:
   - Greenfield → accurate to the minimal just-defined reality.
   - **Brownfield → every line traces to something observed or explicitly confirmed** (the hard gate — no assumed facts).
5. Root CLAUDE.md routing updated.

For brownfield especially: re-read each doc and ask "could I have made this up?" If any line isn't backed by observation or confirmation, verify it or cut it.

---

## Phase 5: HANDOFF

Print the handoff card (Standard §4.10) for both forks — the summary lines become its Done and Written lines:

```
HANDOFF
Where:  standalone | {initiative} · {LEVEL} · {KIND} · {ready | brought to standard}: {name}
Done:   {LEVEL} · {KIND} {READY / BROUGHT TO STANDARD}: {name} — {folder}/CONTEXT.md ✓ · {canonical homes, if created} ✓ · root CLAUDE.md routing ✓ · fork: {greenfield | brownfield — N systems observed, M facts confirmed by interview}
Next:   /memo {first thing to build} (greenfield) | /prd {next change} or /memo {…} (brownfield — docs now reflect ground truth) — in a fresh session
Needs {owner}: {open questions filed to the task manager, with ids} | none
Written: {the paths written}
```

Next is always something the owner can type verbatim.

---

## Safety Rules

1. **Never overwrite existing files** — check first; offer update-or-skip.
2. **Confirm before writing** — show the Phase 3 plan and wait.
3. **Stay inside the target root** — all paths relative to the workspace/system root.
4. **Handle re-runs gracefully** — create only what's missing.
5. **No secrets in generated files** — reference `.env`, never create it.
6. **Brownfield: observe before you write** — no doc line that isn't traceable to the live system or an explicit answer.

---

## Principles

- **The Standard is the spec; this skill is the procedure.** All formats, rules, and the doc set live in `_shared/documentation_standard.md`. Point there — never duplicate it here, so a change to the Standard flows through automatically.
- **The interview carries the taxonomy.** The user describes their thing in plain terms; the skill decides the level, the kind and the doc set. They never have to learn the model.
- **Both forks, one destination.** Greenfield fills the templates forward; brownfield fills them from verified ground truth. The end state is identical: a standard-conformant, accurate doc set.
- **Accurate or cut.** Especially brownfield — a doc that describes what you *assume* is deployed is worse than no doc. Observe, then write.
- **Create the substrate, then hand off.** This skill produces the docs the lifecycle stands on; `/memo → /prd → /build → /ship` maintain them from there.
