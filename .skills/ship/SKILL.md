---
name: ship
description: Checkpoint 3 — "others can rely on it". The resilience review a build must clear before it goes live, triggered when the blast radius crosses the line (someone else depends on it, it writes/changes real data, its output is relied on for important decisions, or it touches money / outside parties / business-critical truth). Surfaces what breaks / who notices / fallback / contingency / how-we-fix / what it concludes without testing, dispositions every hole (fix / escalate / accept), then takes the build live and closes the project. Invoked by /build when the router fires.
---

# /ship

**Definition of done:** Ship proves a build is safe for **others to rely on** before it goes live, then takes it live and closes the project. It is **Checkpoint 3** — and it only triggers when the blast radius is real. The build already works (that's `/build`); ship answers a different question: *when this runs in production and something goes wrong, what happens?* If you can't answer what breaks, who notices, the fallback, the contingency, how we fix it, and what it concludes without testing — it does not go live.

**This is the human review checkpoint.** For your own builds, it's a deliberate self-review before exposing something real. For the team, this is the point where they bring the build to you — the resilience review is exactly the judgment a non-technical builder can't self-administer. **The written review is the audit surface:** it's what lets you (or a fresh session) verify the checkpoint was cleared honestly, not rubber-stamped.

## Trigger

`/build` routes here when **any** blast-radius condition fires:
- **Someone other than you depends on it**, or
- **It writes or changes real data**, or
- **Its output is relied on to make important decisions** (accuracy carries weight even if it persists nothing — a report, an analysis, a number someone acts on), or
- **It touches money / outside parties / business-critical truth.**

If none fire, there is no `/ship` — `/build` ships freely and closes the project itself. Ceremony proportional to risk.

## Usage

```
/ship [project name]
/ship payout-disputes
```

## When to Use

- `/build` finished, verified, and its blast-radius router fired
- Before any build with real blast radius goes live or is exposed to others

## When NOT to Use

- The router is clean (internal, reversible, no real data) — `/build` handles close
- The build isn't verified yet (finish `/build` Phase 3 first)
- Nothing has been built (use `/memo` → `/prd` → `/build`)

## Prerequisite

A `/build` that passed end-of-build verification, with `state.md` recording the router result. **Orient from the project's `state.md` first** (`/build` Phase 1-A: read it, run its verify block, print the orientation card, template §4.10, with **Doing** = the Checkpoint 3 review of {project}; **Checked** = the verify block's results; **Inherits** = Held and Needs {owner}; **Next** = the review written, and the stop for the owner's sign-off and go) — it names the held steps and what needs the owner. Then read the PRD's pre-mortem and impact map by section, and the project log only where `state.md` points. This review builds on them.

---

## Phase 1: NAME THE BLAST RADIUS

State exactly which router condition(s) fire and **who/what is exposed**:
- Who depends on this, and on what exactly?
- What real data does it write or change?
- What money / outside party / business-critical truth does it touch?

This sets the depth of the review. A workflow that moves money to creators gets a harder look than one that writes an internal status field someone reads.

---

## Phase 2: RESILIENCE REVIEW (the Checkpoint 3 content)

Answer all six in writing. This is the heart of the checkpoint — reuse the CLAUDE.md Workflow Design Standard quality lens.

| Question | What to answer |
|----------|----------------|
| **What breaks?** | Every failure mode. For every handoff: what if the next step never fires — how long until someone notices? For every write: what happens if it runs twice? (idempotency) **And: which collaborators does the test suite supply itself, and does the real one have the same shape?** A hand-made stub is fine for values and dangerous for interfaces — a suite that builds its own resolver, client or config object can pass green while production throws on the first call, because the fixture's *shape* was invented rather than taken from the thing it stands in for. **And: what do all the tests have in common?** The same fixture factory, the same creation path, the same kind of actor. Build one fixture the other way production also makes it: a suite whose every record is born by one route hides exactly the records production creates differently. (Lesson, 2026-09-08: every check created its admin through one route, which always wrote a profile row; admins made the older way had none, and finalizing a record threw a foreign-key error that four work items of green tests never met.) |
| **Who notices?** | For each failure: does someone get notified (owner + specific next action), or does it fail silently? Where is the source of truth, and can it drift? **And: when the build splits, isolates or extracts a component, what used to fail loudly and now fails quietly?** Isolation improves resilience and degrades observability at the same time, because the coupling removed is often what was doing the alerting. (Lesson, 2026-08-20: splitting one worker into two lanes meant a dead lane no longer stopped the daily report, so the system looked healthy while its jobs sat waiting; a new detector had to be built at this checkpoint.) |
| **What's the fallback?** | For each automated step that fails: is there a manual path forward? For each human step: is a system sitting idle waiting, and does anyone know? |
| **What's the contingency?** | If it goes wrong in production: what's the rollback or kill switch? Can we undo go-live in one step? |
| **How do we fix it?** | The recovery procedure, written down concretely — so the person on the hook at 2am can follow it. |
| **What does it conclude without testing?** | For every gate, canary, smoke test, spot-check, sample, or `limit 1` read: what does it decide about items it never examined, and what makes the examined item representative? Check **both** directions — a *pass* that authorizes untested items, and a *failure* that condemns them. If nothing establishes representativeness, that's a hole. A probe that only proves a precondition is not proof of the thing itself: an unsigned call answered 401 proves a webhook secret is *set*, not that it is the *right* one, so the proof of a signed integration is one real signed delivery answered 200 and recorded. (Lesson, 2026-10-03: the 401 check passed while the secret had never been saved, and thousands of real deliveries were refused over four hours with nothing recorded and no alert.) **And for every step that waits** (on real users, real events, a day of data, another project's deploy): could we produce that evidence ourselves today, through the real entry point? If yes, the wait is a hole, fixed by replacing it with the simulation (`/prd` §12 "Rule (simulate, don't wait)"); if no, name what cannot be simulated. A question about whether real use succeeds moves to the outcome check instead of blocking go-live. (Lesson, 2026-10-07: launch-section's ten-push gate guarded nobody, and its buyer-push step was proved on a fixture in minutes.) |

Every answer of "I don't know" or "nothing" where there should be something is a **hole**. Holes are not noted and moved past — they go to Phase 3 for disposition.

---

## Phase 3: DISPOSITION (what we actually do about the holes)

Finding holes is worthless if nothing happens to them. **First, write every hole for the owner in four plain sentences:** what it is, why it happened, what we should do about it, and the cost if we do not. The technical detail follows those four; the owner signs off on what they can understand, and a hole they cannot follow is not ready for a disposition (the owner's rule, 2026-09-22). **Then every hole from Phase 2 gets exactly one disposition before go-live:**

| Disposition | When it applies | Action |
|-------------|-----------------|--------|
| **Fix now** | The hole is a *missing safeguard* you can build in this scope — no failure alert, no idempotency guard, no retry, no manual-fallback path | Build the safeguard, then re-run that resilience question. Go-live stays blocked until it's in. This is the default. |
| **Escalate** | The hole is a *design flaw*, not a missing safeguard — a silent-drift source of truth, two systems writing one field, an architecture that can't support the needed fallback | Stop. Return to `/prd` (or `/memo` if the underlying problem was mis-framed). You do not bolt a safeguard onto a broken design. |
| **Accept** | A real but acceptable residual — the cost to close it exceeds the risk, it is reversible, and the contingency is written down | **First, name what this problem is called in the field that has had it longest** — a name usually comes with a mechanism, and a hole that looked too costly to close often turns out to be a solved problem (a tool that overwrote a person's edits at update was the package managers' managed-file problem, fixed in an hour once named). Only then record the decision and the contingency. **Requires explicit human sign-off.** For the team, this is the call they bring to the owner — it is not theirs to make alone. |

**Go-live check:** every hole is now either **Fixed** or **Accepted-with-sign-off.** An undispositioned hole blocks go-live — no exceptions. A hole you quietly tolerate is exactly the failure this check exists to prevent (Surface, don't sweep).

Record each hole and its disposition in the Ship Review (Phase 6).

**Follow-ups: the session tail.** A follow-up found during the review is handled by the rule in the `session-close` skill, "Follow-ups": a small one goes on the session tail and is done before the stop unless the owner chooses to file it; substantial or people-dependent work is filed and announced in three parts. Everything still open at the close comes back to the owner at the residual review (Phase 6, Step 2).

**A Checkpoint 3 round ends at a stop.** When a round ends (review written, blockers fixed, or waiting on the owner), rewrite `state.md` (Position: Checkpoint 3 round N done; Next: …; Held; Needs {owner}), run `python3 .claude/tools/orientation_cost.py --now ship`, print the ship review's TLDR, then the handoff card (template §4.10) with its Context line; its Residuals block carries every hole this round accepted or left open, in its five parts, and follow the verdict exactly as `/build` Phase 2 Step 5: continue into the next round here, or stop for a fresh session. A round waiting on the owner stops regardless.

---

## Phase 4: PRE-FLIGHT CHECKS

Confirm before flipping the switch:
- **Idempotency** — every money/critical operation can safely run twice (re-affirm from the PRD).
- **Reversibility** — go-live can be undone in one step (cutover, not a one-way door).
- **Monitoring** — every automated event posts to the team's notification channel with what happened, the link, who's tagged (by their ID in that channel), and their specific next action. A notification without an owner and an action is useless. (CLAUDE.md Operational Standards.)
- **Bulk-ops safety** — if go-live involves a bulk data change (backfill / mass update or delete of > 10 records / restore / recompute): snapshot pre-state first into the owning area's `bulk_ops/{YYYYMMDD}_{slug}/` (or the workspace root's), with a row in its `INDEX.md` and a README. Don't go live without it. (Session Close Protocol #9.)
- **Drop safety** — if the build dropped (or its contract phase will drop) any schema object, confirm the verbatim definitions were persisted to the project folder BEFORE the drop. If any drop happened un-snapshotted, say so explicitly in the review — don't paper over it.

---

## Phase 5: GO LIVE

1. **Publish, on the owner's go.** When the build has a publish (a push to a public repository, a deploy, a release: the step `/prd` §12 and `/build` Phase 3 item 8 hand to this phase), state the exact command, what it sends and where, then ask the owner for the go and wait. Run it only on an explicit go, which covers that one command; an approval given earlier, of the review or of anything else, is not the go. With no publish, skip this step.
2. **Cut over.** Prefer additive cutover — build new alongside old and swap the entry point (e.g. swap the webhook URL) rather than mutating production in place.
3. **Smoke test in production** — fire one real transaction end-to-end and confirm the value stream completes as the PRD specified.
4. **Confirm monitoring fired** — the live event actually posted to the team's notification channel with the right owner and action.
5. Record the go-live result in `project_log.md`.

If the smoke test fails: execute the contingency from Phase 2, do not leave it half-live, and return to `/build` Scope Escalation or `/prd` as needed.

---

## Phase 6: CLOSE

`/ship` owns the close for builds that cross the line (we don't use `/close-project`).

### Step 1: Record the Checkpoint 3 review
Append to `project_log.md`:

```markdown
## Ship Review (Checkpoint 3)
**Blast radius:** [which conditions fired + who/what is exposed]
**What breaks:** …
**Who notices:** …
**Fallback:** …
**Contingency:** …
**How we fix it:** …
**Concludes without testing:** [each gate/canary/sample → what it decides about untested items, what makes the sample representative, both pass and fail directions — or "none: every item is examined individually"]
**Holes & dispositions:**
- [hole — four plain sentences: what it is · why it happened · what we should do · the cost if we do not] → Fixed: [safeguard built] / Escalated: [back to /prd, why] / Accepted: [residual + contingency + who signed off]
**Go-live:** [date, cutover method, smoke-test result, monitoring confirmed]
**Residual rulings:** [each item from Step 2 → done now / scheduled {date, task id} / dropped (reason)]
```

Then render the log's companion: `python3 ~/.claude/skills/_shared/companion/render.py {workspace}/_admin/prds/{project-name}/project_log.md` writes `ship_review.html` beside it (the last Ship Review section with its Go-live, the questions as fields, every hole with its disposition); then open the page in the default browser when the machine has an opener (`open` on macOS, `xdg-open` on Linux; skip silently otherwise), so it is on screen the moment the document is written. If the review is appended before the cutover and the Go-live line is filled in later, re-run the same command then, so the page carries the go-live.

### Step 2: Residual review (before the close)
List, in one block, every item still open from this project: each task it filed at any stage (memo, PRD, build, this review), each Needs {owner} item, and each hole this review accepted. Find them in the handoff cards' **Filed this session**, **Residuals** and **Needs {owner}** lines and in the project log. The outcome-check task the shared close files is not on the list. Write each item in the five parts of a residual (template §4.10: Noticed, The issue, If left, The fix, Recommend), and make The fix the exact next action: the command, or the step and who takes it. An item this session could do, even one filed earlier, is listed with Recommend: now. Then ask the owner to rule each item, and act on the ruling:
- **Do now.** It is done in this session, before the close, and its task, if it has one, is completed.
- **Schedule.** Its task gets a date and an owner; an accepted hole with no task gets one here.
- **Drop.** Its task, if it has one, is closed with the reason. Dropping an accepted hole drops only its follow-up; the acceptance signed at Phase 3 stands.

Nothing leaves the ship without a ruling, and the owner's ruling wins, including a schedule for something the session could have done. Record each ruling on the Ship Review's **Residual rulings** line, then re-render its page (the Step 1 command). The close card (the shared close, §6) then carries only the scheduled items, each with its date and task id: a step only the owner can take under Needs {owner}, everything else under Residuals.

### Step 3: The shared close
Everything after the review is **one shared procedure**, `~/.claude/skills/_shared/project_close.md`, run top to bottom. It captures the lessons (provisional until real use), brings the living documents current including the register entries this build satisfied, archives the project folder and moves the memo to `_done/` (a blocking step), rewrites the initiative's state file (the milestone row becomes shipped and the tray is refilled), **schedules the outcome check** (the memo's success definition, verified against real use on the date it names or 14 days after go-live, after which the milestone reads `reached`), and prints the handoff card with the go-live state and the monitoring owners now in place.

---

## Principles

- **Working ≠ shippable.** `/build` makes it work; `/ship` makes it safe to rely on. They are different bars.
- **The router sets the ceremony.** Internal and reversible → no ship. Real blast radius → full review, no exceptions.
- **Silent failure is the enemy.** Every failure mode must have a noticer with an action. If nobody finds out, it isn't shippable.
- **Every hole gets a disposition.** Fix it, escalate it, or consciously accept it with sign-off — but never just note it and ship. An undispositioned hole blocks go-live.
- **The review is the audit surface.** A written Checkpoint 3 review is what proves the checkpoint was cleared honestly — for the team, that's what you actually review.
- **Cut over, don't mutate.** Build alongside and swap the entry point, so go-live is reversible in one step.
