---
name: session-close
description: Close out a working session — append the session-log entry to daily-outputs/, verify living docs reflect what changed, surface bulk ops, delete orphans. Run at true close moments (session ending, project archived, batch done), invoked explicitly. The SessionEnd hook records a ledger row (`daily-outputs/sessions.jsonl`); the SessionStart gate surfaces any session that skipped this step to the next session for reconstruction. NOT after every milestone inside a larger flow.
---

# Session Close

**When:** true close moments — the session is ending, a project archived, a batch finished, or the owner says "close this out." NOT mid-build with the next step queued (just report the handoff and stop). Heuristic: closing a *session/project*, or a *task within one*? If the latter, skip.

## 1. Session-log entry (always — floor is one line)

Append to `daily-outputs/YYYY-MM/YYYY-MM-DD.md` (create month folder/file if absent):

```
## HH:MM · {workspace} · {build|quick-fix|ops|discussion}
**Focus:** one line — what this session was about
**Did:** bullets pointing at commits / decisions / tasks filed (pointers, not copies)
**Learned:** pointers to captures made (_practices/, CONTEXT.md) — or "none"
**Open:** threads left hanging → file to the task manager, reference the task here
```

Trivial session = one line: `## HH:MM · workspace · quick-fix — shipped X (commit abc123)`. Every session logs; selective logging kills the habit. The log is an index of exhaust — never duplicate content that lives in commits, practices, or the task manager.

**If a project is in flight, end the session with the handoff card** (template §4.10 in `~/.claude/skills/_shared/documentation_standard.md`), whole and as markdown. The log entry points at `state.md`; the card is what the owner reads.

**Append, never rewrite.** `cat >> file <<'EOF'` at the end of the file — never Write/overwrite the whole file and never add a second `# ` header (two sessions share a day; a rewrite clobbers or reorders the other one's entries — happened 2026-09-02).

**Reconstructing a past session** (listed by the SessionStart telemetry gate from `daily-outputs/sessions.jsonl`): one line under that day's file, heading ends with `(session <id8>)` so the gate stops listing it — e.g. `## 15:14 · {workspace} · ops — re-ran one applicant's form (reconstructed, session eace0ab2)`. Read the transcript only if the ledger row isn't enough.

## 2. Living-docs check (when the session modified a system)

1. **System CONTEXT.md** reflects what changed? Update at the moment of change ideally — verify now. For each folder with a `CONTEXT.md` that gained a file this session, run `python3 .claude/tools/index_check.py <folder>` and name every unnamed entry before closing.
2. **flow.html** — process changed? Edit it (hook auto-publishes).
3. **Team-facing doc, and exports** — flag if a team doc needs updating. If the workspace is the source of something distributed elsewhere, its root CLAUDE.md names the export check under "Words the skills use": run it now, read what it shows, and act on it before closing.
4. **Lifecycle filing** — build completed? Memo/PRD **moved** (never copied) to `_done`/`_archive`; project folder archived. (/build and /ship enforce this at their own close.)
5. **Decision log** — non-obvious decision made? Append it.
6. **Canonical homes** — contract/workflow/schema changed? Update `system_contracts.md` + affected CONTEXT.md THIS session. Architectural fact existing only in memory/chat = move it to its home now (surface, don't sweep).
7. **No orphans** — delete one-time scripts, scratch files, temp outputs.
8. **New gotchas captured?** Tool-general → `_practices/{tool}.md`; project-specific → that CONTEXT.md. A learning without a doc change or filed action didn't happen.
9. **Project in flight?** The project's `state.md` (and the initiative's, if a project opened or closed this session) is rewritten — position, next, verify block, held, needs the owner — and the log entry points at it, never restates it. A session that ends mid-work-item still rewrites it (Next = "finish WI-N: …"). Position written only in the log entry is position lost. After the rewrite, render the companion: `python3 ~/.claude/skills/_shared/companion/render.py <that state.md>` writes `handoff.html` beside it; then open the page in the default browser when the machine has an opener (`open` on macOS, `xdg-open` on Linux; skip silently otherwise), so it is on screen the moment the document is written. Then `python3 ~/.claude/skills/_shared/companion/render.py --stale {workspace}/_admin` lists every companion under `_admin/` (where the memos, PRDs, logs and state files live) that is older than its source — re-render each one it names; run it whether or not a project is in flight. When gate documents live under more than one `_admin/` folder (several workspaces in one repository), point it at the root that holds them all — it walks the tree and lists only companions, so a wider root costs a second, not noise.

## 3. Bulk-ops surfacing (if any UPDATE/DELETE >10 rows, backfill, restore, or recompute ran)

Say explicitly: *"Bulk write ran this session: N rows in {workspace}. bulk_ops/<YYYYMMDD>_<slug>/ created with prestate + README?"* If pre-state wasn't snapshotted before the write, say so — never paper over it.

**The key word is "flag."** Every change gets acknowledged — handled or explicitly deferred. Nothing silently drifts.
