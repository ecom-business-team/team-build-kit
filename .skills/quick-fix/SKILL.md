---
name: quick-fix
description: Diagnose and fix small issues without project scaffolding — and end with the same blast-radius exit gate as /build (if others depend on it or it writes real data, the six Gate-3 questions run inline before it goes live). Use for bug fixes, config tweaks, workflow adjustments, or minor enhancements that don't require new architecture. Emphasizes deep diagnosis over quick action.
---

# /quick-fix

Diagnose and fix a focused issue. No tickets, no project scaffolding — just understand, fix, verify, update docs.

## Usage

```
/quick-fix the daily summary is showing stale data
/quick-fix the signup email isn't sending the confirmation link
/quick-fix update the default rate to 8%
```

## When to Use

- Bug fixes (something broke or behaves wrong)
- Config tweaks (change a value, update a setting)
- Workflow adjustments (modify existing automation behavior)
- Minor enhancements (small improvement to existing functionality)
- One-off corrections (data fixes, field updates)

## When NOT to Use (use /memo → /prd → /build instead)

- New workflows or new database tables
- Changes spanning 3+ systems
- Anything requiring new architecture or design decisions
- Work that will take multiple sessions

---

## Phase 1: UNDERSTAND (spend the most time here)

The goal is to fully understand the problem space before touching anything.

### Step 1: Orient

1. Read the relevant workspace CONTEXT.md
2. Identify which systems are involved (automations, data stores, app, code, external services, etc.)
3. If the user described a symptom ("DM isn't sending"), do NOT assume you know the cause yet

### Step 2: Gather ground truth

Go to the source. Don't rely on docs alone — check live state.

- **Automation issue?** Inspect the live automation directly — its actual configuration and current behavior.
- **Data store issue?** Inspect the live schema and a real sample of the data.
- **Code issue?** Read the relevant files.
- **Data issue?** Query the actual data to see what's there vs what's expected.

Use the right tool for the workspace's stack — load its tool-skill where one exists.

### Step 3: Map the scope

Before proceeding, answer these questions:

1. **What exactly is the problem?** (not the symptom — the root cause)
2. **What is the blast radius?** (what else touches the same data/workflow/boundary?)
3. **Does this cross a system boundary?** If yes, check `system_contracts.md`.
4. **How many things need to change?** If the answer is more than ~3 files/components/queries, stop and suggest `/memo` → `/prd` → `/build`.

### Step 4: Present the diagnosis

Present the user with:
- **Root cause:** what's actually wrong and why
- **What needs to change:** specific components, fields, code, config
- **What does NOT need to change:** confirm the blast radius is contained
- **Risk:** what could go wrong with the fix (low/medium/high)

**Wait for user confirmation before proceeding to Phase 2.**

---

## Phase 2: FIX

The fix should feel mechanical at this point — the hard thinking was Phase 1.

1. Implement the change (edit code, update an automation, change data, etc. — using the workspace's stack)
2. If the fix involves a system boundary change, note it for doc updates
3. Keep it minimal — fix the problem, don't improve the neighborhood

---

## Phase 3: VERIFY

1. Test that the original problem is resolved **with the proof the system's kind requires**: the **Kind** line of its `CONTEXT.md` names the kind, and the kinds table in `documentation_standard.md` §4 ("The third axis") names the proof — replay through the real entry point for an automation; tests plus a live probe for a service; smoke through the real login for an application; tests on fixtures plus a real-data check for a tool; a cold read for a procedure; review against its sources for knowledge. The method for the code kinds is `testing_standard.md`.
2. Spot-check that adjacent functionality still works
3. If there's an easy way to trigger the flow end-to-end, do it

---

## Phase 3.5: EXIT GATE — the blast-radius router (the same rule as `/build`)

A quick fix skips design; it never skips the exit gate. Before the fix goes live — the deploy, the replay, the bulk write, the workflow re-activation — ask the four router questions: **Does someone other than you depend on it? Does it write or change real data? Is its output relied on for decisions? Does it touch money, outside parties or business-critical truth?**

- **None fire →** ship it; go to Phase 4.
- **Any fire →** answer the six Gate-3 questions **inline, in miniature** — a paragraph, not a review document — before anything goes live:
  1. **What breaks** if this runs twice, or half-runs? (idempotency, for every write)
  2. **Who notices** if it fails, and how fast? (a noticer with an owner and an action — or "silent", which is a hole)
  3. **What is the fallback** — the manual path if the automated one fails?
  4. **What is the contingency** — the one-step undo? (a bulk write needs its prestate snapshot FIRST: `bulk_ops/`, the tripwire)
  5. **How do we fix it** at 2 am — the procedure, written where the next person looks?
  6. **What does it conclude without testing** — what did the canary or the sample decide about the items it never examined, and what makes them representative?

  Every "nothing" or "don't know" is a hole: **fix it now** (add the noticer, the snapshot, the idempotency guard) or **escalate** to `/memo` — never note it and proceed. Record the six answers in the session-log entry (a quick fix has no project log) and say out loud what went live.

Why this exists: quick-fix is the most-used path and it does write real data — rows replayed through a webhook, statuses re-fired on a board — on discipline alone until now. One exit dimension, blast radius, now covers both paths; intake keeps its own question, does this need design.

---

## Phase 4: UPDATE LIVING DOCS

Per the Living Documentation Rule:

1. Check if any living documents reference the changed entity
2. Flag proposed updates for approval
3. Add a changelog entry if the change is meaningful (skip for trivial config tweaks)
4. If the system's `CONTEXT.md` predates 2026-09-20 and has no **Kind** and **Proved by** lines, add them now — two lines, from what Phase 1 observed.

**Do NOT create:** project folders, tickets, PROJECT_LOG, retrospectives, or decision log entries. This is a quick fix.

---

## Scope Escalation

If at any point during Phase 1 you discover:

- The root cause requires new database tables or columns
- Multiple workflows need coordinated changes
- The fix requires architectural decisions with real tradeoffs
- The blast radius is larger than expected

**Stop.** Tell the user: "This is bigger than a quick fix. Here's what I found — I'd recommend starting with `/memo` to identify the constraint, then `/prd` to design it properly." Present your Phase 1 findings so the work isn't lost.

---

## Principles

- **Diagnose deep, fix shallow.** Spend 70% of effort understanding, 30% fixing.
- **Go to the source.** Never assume docs are correct — check live systems.
- **One problem, one fix.** Don't bundle unrelated improvements.
- **Minimal blast radius.** Change the least amount possible to solve the problem.

## Design Principles (think in these terms)

Quick fixes don't require the full PRD checklist, but should still respect these fundamentals:

- **Boundaries:** Does this fix stay within one system's ownership? If it crosses a boundary, check the contract at that boundary.
- **Output isolation:** Don't have one system mutate another system's data as a shortcut. Each system writes its own output.
- **State lifecycles:** If the fix involves a status or state change, verify the entity has a proper status field and lifecycle — don't add boolean flags as quick patches.
- **Contracts:** If the fix changes what a system produces or consumes, that's a contract change — flag it for doc updates and consider downstream impact.
- **Idempotency:** If the fix touches anything involving money or critical state, verify the operation can safely run twice.

If applying these principles reveals the fix is more complex than expected, escalate to `/memo` → `/prd` → `/build`.
