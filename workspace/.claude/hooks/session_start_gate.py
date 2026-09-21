#!/usr/bin/env python3
"""SessionStart hook: surface the telemetry backlog to the new session.

Plain stdout from a SessionStart hook is added to Claude's context, so this is the lazy pump:
  1. substantial sessions with no session-log entry (from daily-outputs/sessions.jsonl)
  2. days with entries but no /day digest
  3. the last completed ISO week without a /week review
Prints nothing when nothing is pending. Reconstructing missing entries is Claude's standing
behaviour (session-close); /day and /week are the owner's rituals -> mentioned, never run unasked.
"""
import datetime as dt
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(ROOT, "daily-outputs")
LEDGER = os.path.join(OUT, "sessions.jsonl")
LOOKBACK_DAYS = 14
MAX_LIST = 6
TELEMETRY_START = "2026-08-26"  # the day the ledger began; sessions before it were never expected to log


def read(path):
    try:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            return fh.read()
    except OSError:
        return ""


def daily_path(date):
    return os.path.join(OUT, date[:7], f"{date}.md")


def load_rows(cutoff):
    rows = []
    for line in read(LEDGER).splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if (r.get("date") or "") >= cutoff:
            rows.append(r)
    rows.sort(key=lambda r: (r.get("date") or "", r.get("started") or ""))
    return rows


def projects_in_flight():
    """Every project state.md in the workspace = a build in flight (documentation_standard.md §4).
    Depth-limited globs: node_modules and gitignored app checkouts are never walked."""
    out = []
    for pat in ("*/_admin/prds/*/state.md", "*/*/_admin/prds/*/state.md"):
        for path in sorted(glob.glob(os.path.join(ROOT, pat))):
            text = read(path)
            m = re.search(r"\*\*Next:\*\*\s*(.+)", text)
            nxt = (m.group(1).strip() if m else "?")[:120]
            st = re.search(r"\*\*Stage:\*\*\s*(.+)", text)
            stage = (st.group(1).strip() if st else "")[:90]
            out.append((os.path.relpath(path, ROOT), len(text.split()), nxt, stage))
    return out


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}
    current_sid = payload.get("session_id")
    tdir = os.path.dirname(os.path.expanduser(payload.get("transcript_path") or "")) or None
    try:  # sessions whose SessionEnd never fired (killed window) still get a ledger row
        sys.path.insert(0, HERE)
        import session_ledger
        session_ledger.backfill_missing(days=LOOKBACK_DAYS, tdir=tdir)
    except Exception as exc:
        sys.stderr.write(f"session_start_gate: backfill skipped ({exc})\n")
    today = dt.date.today()
    today_s = today.isoformat()
    cutoff = max((today - dt.timedelta(days=LOOKBACK_DAYS)).isoformat(), TELEMETRY_START)

    unlogged = []
    for r in load_rows(cutoff):
        if not r.get("substantial") or r.get("logged"):
            continue
        if current_sid and r.get("session_id") == current_sid:
            continue  # the running session logs itself at close
        if r.get("id8") and r["id8"] in read(daily_path(r["date"])):
            continue  # reconstructed entry carries "(session <id8>)"
        unlogged.append(r)

    unprocessed = []
    daily_files = {}
    for path in sorted(glob.glob(os.path.join(OUT, "????-??", "????-??-??.md"))):
        date = os.path.basename(path)[:-3]
        daily_files[date] = path
        if date < cutoff or date >= today_s:
            continue
        text = read(path)
        entries = len(re.findall(r"^## (?!Digest)", text, re.M))
        if entries and "## Digest" not in text:
            unprocessed.append((date, entries))

    last_monday = today - dt.timedelta(days=today.weekday() + 7)
    last_sunday = last_monday + dt.timedelta(days=6)
    iso_year, iso_week, _ = last_monday.isocalendar()
    week_tag = f"{iso_year}-W{iso_week:02d}"
    week_has_days = any(last_monday.isoformat() <= d <= last_sunday.isoformat() for d in daily_files)
    week_candidates = [os.path.join(OUT, m.strftime("%Y-%m"), f"{week_tag}_review.md")
                       for m in (last_monday, last_sunday)]
    week_missing = week_has_days and not any(os.path.exists(p) for p in week_candidates)

    projects = projects_in_flight()
    if not (unlogged or unprocessed or week_missing or projects):
        return

    lines = []
    for rel, words, nxt, stage in projects:
        ws = rel.split("/_admin/")[0]
        lines.append(
            f"[State gate - SessionStart] PROJECT IN FLIGHT: {rel} ({words} words) · Stage: {stage or '?'} · Next: {nxt} -> before any work in "
            f"{ws}/: `cat` that file, run its 'Verify before continuing' block, announce the position (/build Phase 1-A). "
            f"project_log.md is the record - never read it for position.")
    lines.append("[Telemetry gate - SessionStart - source: daily-outputs/sessions.jsonl]")
    if unlogged:
        lines.append(
            f"UNLOGGED SESSIONS ({len(unlogged)}). Standing behaviour (session-close skill): append a one-line "
            f"entry for each to daily-outputs/YYYY-MM/YYYY-MM-DD.md, reconstructed from the row (open the "
            f"transcript only if the row is not enough). The heading MUST contain '(session <id8>)' so this "
            f"gate stops listing it. Do it before other work unless the user's request is urgent.")
        for r in unlogged[-MAX_LIST:]:
            fp = (r.get("first_prompt") or "").replace('"', "'")[:120]
            lines.append(
                f"- {r.get('date')} {r.get('started') or '?'}-{r.get('ended') or '?'} · id {r.get('id8')} · "
                f"{r.get('title') or 'untitled'} · first prompt: \"{fp}\" · tools {r.get('tool_calls')} · "
                f"writes {'yes' if r.get('write_signal') else 'no'} · transcript {r.get('transcript_path')}")
        if len(unlogged) > MAX_LIST:
            lines.append(f"- ... +{len(unlogged) - MAX_LIST} older rows in the ledger")
    if unprocessed:
        lines.append("UNPROCESSED DAYS (entries, no /day digest): "
                     + ", ".join(f"{d} ({n} entries)" for d, n in unprocessed)
                     + " -> mention /day to the owner in one line; do NOT run it unasked (the owner runs their own rituals).")
    if week_missing:
        lines.append(f"NO /week REVIEW for {week_tag} ({last_monday} to {last_sunday}) -> mention in the same line.")
    if lines and lines[-1].startswith("[Telemetry gate"):
        lines.pop()  # nothing telemetric pending; only the state lines remain
    print("\n".join(lines))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # never block a session start
        sys.stderr.write(f"session_start_gate: {exc}\n")
    sys.exit(0)
