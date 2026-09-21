---
name: week
description: The operational weekly review (≤20 min) — read the week's daily logs + digests, run the promotion review (practices → tier 1 → team-build-kit candidates), sweep open threads, answer ONE diagnostic question (biggest recurring friction → one action), write the weekly summary. The bigger-patterns half of the /day–/week pump.
user_invocable: true
---

# /week — operational weekly review

**Purpose:** the bigger patterns. `/day` processes; `/week` notices what repeats. Target: ≤20 minutes. Lean digest + exactly one diagnostic — the full metrics loop stays shelved until it earns its way in.

**When:** end of week (Friday/weekend), or whenever a week has gone unprocessed.

## Steps

1. **Read the week's dailies** — `daily-outputs/YYYY-MM/` files for the ISO week, digests first, entries as needed. Cross-check against exhaust (`git log --since='7 days ago'` summary, the task manager's completed tasks) for invisible days.

2. **Promotion review** (the ladder's deliberate rung):
   - **`/day` flags → tier 1:** anything flagged tier-1-worthy this week — does it pass all three admission criteria (behavioral · majority of sessions · fails silently)? If yes, propose the exact CLAUDE.md line to the owner; never edit tier 1 without approval.
   - **Second occurrences:** a lesson that bit in a *second* project this week is proof of generality — promote to `_practices/` if it isn't there.
   - **Stability → team-build-kit:** any `_practices/` file or workflow module that's been stable for weeks and is genericizable → flag as a team-build-kit publication candidate (publication is deliberate editorial work, not automatic).

3. **Open-threads sweep:** anything that appeared as "Open" in ≥2 dailies without a task or resolution — surface it; recurring unfiled threads are the leak this system exists to close.

4. **The one diagnostic question:** *what was the biggest recurring friction this week, and what one action addresses it?* Evidence from the logs, one concrete action (filed to the task manager or proposed to the owner). One — not a list.

5. **Write the summary** — `daily-outputs/YYYY-MM/YYYY-Www_review.md`:

```
# Week {W} review ({dates})
**Shipped:** bullets w/ pointers
**Learned/promoted:** what moved up the ladder (+ tier-1/team-kit proposals)
**Friction:** the diagnostic answer + the one action
**Open into next week:** threads (all with task refs)
**Needs {owner}:** ONLY the items that require their word — approvals (tier-1 lines, kit publications), decisions, questions — one full sentence each, saying what happens on each answer. Nothing else goes here, and nothing that belongs here goes anywhere else.
```

6. **Report to the owner:** the summary, verbatim — it's designed to be read in one screen. The `Needs {owner}` section is the last thing on it, so their replies map one-to-one to the asks. (Owner's ruling, 2026-09-15: asks scattered through the report were easy to miss.)

## Rules

- Patterns need ≥2 occurrences — one incident is an anecdote, not a pattern.
- Propose, don't apply, anything touching tier 1 or team-build-kit.
- If a month-end lens is ever wanted, it's derivable from 4–5 of these summaries — no separate ritual exists.
