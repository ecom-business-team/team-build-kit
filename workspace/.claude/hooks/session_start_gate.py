#!/usr/bin/env python3
"""SessionStart hook: surface the telemetry backlog to the new session.

Plain stdout from a SessionStart hook is added to Claude's context, so this is the lazy pump:
  0. one line per build or project in flight: every `_admin/builds/*/brief.md` not done or killed
     (the /build skill) and every `_admin/prds/*/state.md` (the old lifecycle), plus the lines of
     each area's position command
  1-3. one telemetry line: substantial sessions with no session-log entry (the list itself prints
     with `--unlogged`), days with entries but no /day digest, the last ISO week without a /week review
  4. open tasks in the fallback list (tasks.md at the root) whose due date has come
  5. a newer Team Build Kit than the one installed (the receipt's version line against the
     published VERSION, fetched at most once a day; silent with no receipt, no line or no network)
Prints nothing when nothing is pending. Reconstructing missing entries is Claude's standing
behaviour (session-close); /day and /week are the owner's rituals -> mentioned, never run unasked.
"""
import datetime as dt
import glob
import json
import os
import re
import shlex
import subprocess
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(ROOT, "daily-outputs")
LEDGER = os.path.join(OUT, "sessions.jsonl")
KIT_REPO = "https://raw.githubusercontent.com/ecom-business-team/team-build-kit"  # the published kit; /main is added below
KIT_RAW = os.environ.get("TBK_BASE") or KIT_REPO + "/main"
VERSION_RE = re.compile(r"v\d+\.\d+\.\d+(?:-\d+)?")
LOOKBACK_DAYS = 14
IDLE_S = 86400  # a transcript written within a day may belong to a session that will resume
MAX_LIST = 6


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


CLOSED = ("done", "killed")  # brief stages that are no longer in flight (/build, "Stages")


def projects_in_flight():
    """Every /build brief not done or killed, and every old-lifecycle project state.md, in the
    workspace (documentation_standard.md §4). Depth-limited globs: node_modules and gitignored app
    checkouts are never walked. Returns (path, stage, next) per build in flight."""
    out = []
    for kind in ("builds/*/brief.md", "prds/*/state.md"):
        for pre in ("", "*/", "*/*/"):
            for path in sorted(glob.glob(os.path.join(ROOT, pre + "_admin/" + kind))):
                text = read(path)
                m = re.search(r"\*\*Next:\*\*\s*(.+)", text)
                nxt = (m.group(1).strip() if m else "?")[:120]
                st = re.search(r"\*\*Stage:\*\*\s*(.+)", text)
                stage = (st.group(1).strip() if st else "?")[:90]
                if kind.startswith("builds") and stage.split(" ")[0] in CLOSED:
                    continue
                out.append((os.path.relpath(path, ROOT), stage, nxt))
    return out


def position_commands():
    """Areas whose index names a task manager that holds position (documentation_standard.md §4.8,
    "Where the snapshot lives"): a `**Position command:**` line in an area CONTEXT.md one level down.
    Each command runs with `in-flight` (5 s) and its lines are printed; a failure prints one line."""
    out = []
    for path in sorted(glob.glob(os.path.join(ROOT, "*", "CONTEXT.md"))):
        m = re.search(r"^\*\*Position command:\*\*\s*`(.+?)`", read(path), re.M)
        if not m:
            continue
        area = os.path.basename(os.path.dirname(path))
        try:
            r = subprocess.run(shlex.split(m.group(1)) + ["in-flight"], cwd=ROOT, capture_output=True,
                               text=True, timeout=5)
            reason = None if r.returncode == 0 else f"exit {r.returncode}"
        except subprocess.TimeoutExpired:
            reason = "timed out after 5 s"
        except Exception as exc:
            reason = type(exc).__name__
        if reason:
            out.append(f"[State gate - SessionStart] {area}: position command failed ({reason}); "
                       f"check in-flight work by hand before building there.")
        else:
            out.extend(l for l in r.stdout.splitlines() if l.strip())
    return out


def tasks_due(today_s):
    """Open lines of the fallback task list (ROOT/tasks.md) whose due date is today or past.
    Absent file -> nothing."""
    out = []
    for line in read(os.path.join(ROOT, "tasks.md")).splitlines():
        m = re.match(r"^\s*- \[ \] (T-\d+)\b.*?\bdue (\d{4}-\d{2}-\d{2})", line)
        if m and m.group(2) <= today_s:
            out.append(f"[Task gate - SessionStart] DUE: {m.group(1)} {line.strip()[:140]} (tasks.md)")
    return out


def kit_update(today_s):
    """One line when the published kit differs from the installed one. The installed version is the
    '# version:' line install.sh writes into the skills receipt; the published one is fetched at most
    once a day and cached with the date, so every session that day repeats the line without a fetch."""
    m = re.search(r"^# version: (\S+)", read(os.path.expanduser("~/.claude/skills/.kit_receipt")), re.M)
    if not m:
        return []
    marker = os.path.expanduser("~/.claude/state/kit-version-check.json")
    try:
        cache = json.loads(read(marker) or "{}")
    except ValueError:
        cache = {}
    latest = cache.get("latest") if cache.get("date") == today_s else None
    if latest is None:
        try:
            with urllib.request.urlopen(f"{KIT_RAW}/VERSION", timeout=3) as r:
                found = VERSION_RE.search(r.read(4096).decode("utf-8", "ignore"))
        except Exception:
            return []  # offline or moved: say nothing, try again next session
        latest = found.group(0) if found else ""
        try:
            os.makedirs(os.path.dirname(marker), exist_ok=True)
            with open(marker, "w") as fh:
                json.dump({"date": today_s, "latest": latest}, fh)
        except OSError:
            pass
    if not latest or latest == m.group(1):
        return []
    return [f"[Kit gate - SessionStart] A newer Team Build Kit is out: installed {m.group(1)}, published {latest}. "
            f"-> mention /update-build-kit to the owner in one line (run it from the workspace root); do NOT run it unasked."]


def unlogged_lines(unlogged):
    """The per-session reconstruction list: printed by `--unlogged`, never at session start."""
    lines = [f"UNLOGGED SESSIONS ({len(unlogged)}). Standing behaviour (session-close skill): append a one-line "
             f"entry for each to daily-outputs/YYYY-MM/YYYY-MM-DD.md, reconstructed from the row (open the "
             f"transcript only if the row is not enough). The heading MUST contain '(session <id8>)' so this "
             f"gate stops listing it."]
    for r in unlogged[-MAX_LIST:]:
        fp = (r.get("first_prompt") or "").replace('"', "'")[:120]
        lines.append(
            f"- {r.get('date')} {r.get('started') or '?'}-{r.get('ended') or '?'} · id {r.get('id8')} · "
            f"{r.get('title') or 'untitled'} · first prompt: \"{fp}\" · tools {r.get('tool_calls')} · "
            f"writes {'yes' if r.get('write_signal') else 'no'} · transcript {r.get('transcript_path')}")
    if len(unlogged) > MAX_LIST:
        lines.append(f"- ... +{len(unlogged) - MAX_LIST} older rows in the ledger")
    return lines


def main():
    list_only = "--unlogged" in sys.argv[1:]
    try:
        payload = {} if list_only else json.load(sys.stdin)
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
    cutoff = (today - dt.timedelta(days=LOOKBACK_DAYS)).isoformat()

    unlogged = []
    for r in load_rows(cutoff):
        if not r.get("substantial") or r.get("logged"):
            continue
        if current_sid and r.get("session_id") == current_sid:
            continue  # the running session logs itself at close
        if r.get("id8") and r["id8"] in read(daily_path(r["date"])):
            continue  # reconstructed entry carries "(session <id8>)"
        try:
            if time.time() - os.path.getmtime(r.get("transcript_path") or "") < IDLE_S:
                continue  # possibly still open; it logs itself, or is listed once idle a full day
        except OSError:
            pass
        unlogged.append(r)
    if list_only:
        print("\n".join(unlogged_lines(unlogged)) if unlogged else "No unlogged sessions.")
        return

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
    positions = position_commands()
    due = tasks_due(today_s)
    kit = kit_update(today_s)
    if not (unlogged or unprocessed or week_missing or projects or positions or due or kit):
        return

    lines = [f"[State gate - SessionStart] IN FLIGHT: {rel} · {stage} · Next: {nxt}"
             for rel, stage, nxt in projects]
    lines.extend(positions)
    backlog = []
    if unlogged:
        backlog.append(f"{len(unlogged)} unlogged sessions (list: python3 .claude/hooks/session_start_gate.py --unlogged)")
    if unprocessed:
        backlog.append("/day due for " + ", ".join(d for d, _ in unprocessed))
    if week_missing:
        backlog.append(f"no /week for {week_tag}")
    if backlog:
        todo = (["reconstruct the unlogged sessions (session-close skill)"] if unlogged else []) + (
            ["mention /day and /week to the owner in one line, never run them unasked"] if unprocessed or week_missing else [])
        lines.append("[Telemetry gate - SessionStart] " + " · ".join(backlog) + " -> " + "; ".join(todo) + ".")
    lines.extend(due)
    lines.extend(kit)
    print("\n".join(lines))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # never block a session start
        sys.stderr.write(f"session_start_gate: {exc}\n")
    sys.exit(0)
