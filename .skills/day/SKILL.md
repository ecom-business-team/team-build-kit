---
name: day
description: Process the day's session logs (~5 min) — verify every session logged, promote clear-cut learnings to their canonical homes, file open threads to the task manager, append a one-paragraph digest. The daily pump between write-optimized logs and read-optimized knowledge. Run at end of day or next morning. (Repurposed 2026-08-26 from the personal-OS ritual, now archived.)
user_invocable: true
---

# /day — operational daily digest

**Purpose:** the daily pump. Session logs are write-optimized exhaust; this skill moves what matters into read-optimized homes so future sessions retrieve it. Target: 5 minutes. Not a planning ritual — a processing pass.

**When:** end of day, or next morning for the previous day (auto-detect: if today's file has entries and it's evening → today; if morning → most recent unprocessed day).

## Steps

1. **Read the day's file** — `daily-outputs/YYYY-MM/YYYY-MM-DD.md`. If it's missing or thin, reconstruct from `daily-outputs/sessions.jsonl` (one row per session: time window, auto title, first prompt, tool/write counts, transcript path — the SessionEnd hook writes it; rows with `substantial: true` and `logged: false` are the gaps). Open the transcript's first prompt + tool calls when a row isn't enough; `git log --since/--until` and the task manager's activity are secondary exhaust. Note the gap — abandoned sessions are acceptable losses, invisible days are not. (The SessionStart gate lists unlogged sessions and unprocessed days to every new session, so this step is normally already done.)

2. **Promotion pass over the day's "Learned" entries.** For each capture pointer, verify the capture actually landed in its canonical home (`_practices/{tool}.md` or the project CONTEXT.md). **A learning without a doc change or filed action didn't happen** — if one is only prose in the log, place it now (portability test: tool-general → `_practices/`; project-specific → CONTEXT.md). Flag anything that looks tier-1-worthy (universal + behavioral + silent-failure) for `/week` — don't promote to CLAUDE.md daily.

3. **Open-threads sweep.** Every "Open:" item either has a task reference or gets one now, labelled as the workspace's CLAUDE.md task rules say, in the matching project. Markdown holds no live state overnight.

4. **Append the digest** to the bottom of the day's file:

```
## Digest (/day, run HH:MM)
One paragraph: what the day actually was — the through-line, not a list.
Promotions: {n} to _practices, {n} to CONTEXT, {n} flagged for /week · Threads filed: {n} · Sessions: {n}
```

5. **One line to the owner:** the paragraph + anything flagged. No ceremony. Then a dedicated **`Needs {owner}:`** section — every item that requires their word (an approval, a decision, a question), one full sentence each with the outcome of each answer, and nothing else in it. Never bury an ask inside a digest paragraph. If there is nothing, write `Needs {owner}: nothing.` (Owner's ruling, 2026-09-15.)

## Rules

- Never copy content into the digest that lives elsewhere — pointers only.
- Don't editorialize quality or productivity — that's `/week`'s pattern job, and only when patterns are real.
- If the day had zero sessions, skip silently — no empty files.
