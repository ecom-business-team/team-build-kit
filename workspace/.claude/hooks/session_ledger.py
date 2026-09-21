#!/usr/bin/env python3
"""SessionEnd hook -> daily-outputs/sessions.jsonl (one row per session, upserted).

Why: SessionEnd cannot prompt the model, so instead it records the facts the NEXT session
needs to reconstruct a missing session-log entry (consumed by session_start_gate.py and the
session-close skill). Replaces an earlier breadcrumb comment that fired several times per session
and was never consumed.

Usage:
  hook      stdin = SessionEnd JSON {session_id, transcript_path, cwd, reason}
  backfill  session_ledger.py --backfill [--since YYYY-MM-DD] [--dir <transcripts dir>]
Never exits non-zero: a ledger failure must not break a session close.
"""
import datetime as dt
import glob
import json
import os
import re
import shutil
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.abspath(os.path.join(HERE, "..", ".."))
LEDGER = os.path.join(ROOT, "daily-outputs", "sessions.jsonl")
DEFAULT_TRANSCRIPTS = os.path.expanduser(os.path.join("~/.claude/projects", re.sub(r"[^A-Za-z0-9]", "-", ROOT)))
STATE_DIR = os.path.expanduser("~/.claude/state/practices-gate")

WRITE_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
MCP_WRITE_RE = re.compile(
    r"^mcp__.*__(add|update|complete|uncomplete|delete|reschedule|manage|move|reorder|apply|deploy"
    r"|create|insert|write|send|trigger|merge|reset|rebase)", re.I)
SQL_WRITE_RE = re.compile(r"\b(insert|update|delete|alter|create|drop|truncate|grant|revoke)\b", re.I)
BASH_WRITE_RE = re.compile(
    r"(>>|(?<![<>&\d])>\s*(?!/dev/null|&)\S|\btee\s|\bsed -i"
    r"|\bgit (commit|add|push|mv|rm|tag|reset|checkout|stash|cherry-pick|rebase|merge)\b"
    r"|\b(mv|rm|cp|mkdir|touch|chmod|ln)\s"
    r"|curl[^|\n]*\s-X\s*(POST|PUT|PATCH|DELETE)|curl[^|\n]*\s(-d|--data|--data-binary|-F)\s"
    r"|\brailway up\b|\bvercel\b|\bsupabase (db|functions|migration)\b"
    r"|open\([^)]*['\"](a|w)['\"]\s*\))")
LOG_WRITE_RE = re.compile(
    r"(>>?\s*\S*daily-outputs/|tee\s+(-a\s+)?\S*daily-outputs/|open\([^)]*daily-outputs/[^)]*['\"](a|w)['\"])")


def is_write(name, inp):
    if name in WRITE_TOOLS:
        return True
    if name == "Bash":
        return bool(BASH_WRITE_RE.search(inp.get("command", "") or ""))
    if name == "mcp__supabase__execute_sql":
        return bool(SQL_WRITE_RE.search(inp.get("query", "") or ""))
    return bool(MCP_WRITE_RE.match(name))


def is_log_write(name, inp):
    if name in WRITE_TOOLS:
        return "daily-outputs/" in str(inp.get("file_path", ""))
    if name == "Bash":
        return bool(LOG_WRITE_RE.search(inp.get("command", "") or ""))
    return False


def parse_transcript(path):
    info = dict(started=None, ended=None, cwd=None, branch=None, title=None, first_prompt=None,
                prompts=0, tool_calls=0, write_signal=False, logged=False)
    try:
        fh = open(path, encoding="utf-8", errors="ignore")
    except OSError:
        return info
    with fh:
        for line in fh:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get("isSidechain"):
                continue
            t = d.get("type")
            ts = d.get("timestamp")
            if ts and t in ("user", "assistant"):
                info["started"] = info["started"] or ts
                info["ended"] = ts
            if t == "ai-title" and d.get("aiTitle"):
                info["title"] = d["aiTitle"]
            info["cwd"] = info["cwd"] or d.get("cwd")
            info["branch"] = info["branch"] or d.get("gitBranch")
            msg = d.get("message") if isinstance(d.get("message"), dict) else None
            if not msg:
                continue
            content = msg.get("content")
            if t == "user" and not d.get("isMeta"):
                if isinstance(content, str):
                    text = content
                else:
                    text = " ".join(x.get("text", "") for x in (content or [])
                                    if isinstance(x, dict) and x.get("type") == "text")
                text = re.sub(r"\s+", " ", text or "").strip()
                if text and not text.startswith("<") and not text.startswith("[Request interrupted"):
                    info["prompts"] += 1
                    if info["first_prompt"] is None:
                        info["first_prompt"] = text[:160]
            elif t == "assistant" and isinstance(content, list):
                for x in content:
                    if not (isinstance(x, dict) and x.get("type") == "tool_use"):
                        continue
                    name = x.get("name") or ""
                    inp = x.get("input") or {}
                    if not isinstance(inp, dict):
                        inp = {}
                    info["tool_calls"] += 1
                    if is_write(name, inp):
                        info["write_signal"] = True
                    if is_log_write(name, inp):
                        info["logged"] = True
    return info


def to_local(ts):
    if not ts:
        return None
    try:
        return dt.datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone()
    except ValueError:
        return None


def build_row(session_id, transcript_path, reason, cwd_hint):
    info = parse_transcript(transcript_path)
    started = to_local(info["started"])
    ended = to_local(info["ended"])
    date = (started or dt.datetime.now()).strftime("%Y-%m-%d")
    substantial = bool(info["write_signal"] or info["prompts"] >= 2 or info["tool_calls"] >= 8)
    return {
        "session_id": session_id, "id8": session_id[:8], "date": date,
        "started": started.strftime("%H:%M") if started else None,
        "ended": ended.strftime("%H:%M") if ended else None,
        "reason": reason, "title": info["title"], "first_prompt": info["first_prompt"],
        "prompts": info["prompts"], "tool_calls": info["tool_calls"],
        "write_signal": info["write_signal"], "substantial": substantial, "logged": info["logged"],
        "cwd": info["cwd"] or cwd_hint, "branch": info["branch"], "transcript_path": transcript_path,
        "recorded_at": dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    }


def load_rows():
    rows = []
    if os.path.exists(LEDGER):
        with open(LEDGER, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except ValueError:
                    continue
    return rows


def write_rows(rows):
    os.makedirs(os.path.dirname(LEDGER), exist_ok=True)
    rows.sort(key=lambda r: (r.get("date") or "", r.get("started") or ""))
    tmp = LEDGER + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    os.replace(tmp, LEDGER)


def upsert(row):
    rows = [r for r in load_rows() if r.get("session_id") != row["session_id"]]
    rows.append(row)
    write_rows(rows)


def cleanup_markers(max_age_days=7):
    if not os.path.isdir(STATE_DIR):
        return
    cutoff = time.time() - max_age_days * 86400
    for d in os.listdir(STATE_DIR):
        p = os.path.join(STATE_DIR, d)
        try:
            if os.path.isdir(p) and os.path.getmtime(p) < cutoff:
                shutil.rmtree(p, ignore_errors=True)
        except OSError:
            pass


def backfill(args):
    since = "0000-00-00"
    tdir = DEFAULT_TRANSCRIPTS
    i = 0
    while i < len(args):
        if args[i] == "--since" and i + 1 < len(args):
            since = args[i + 1]; i += 2
        elif args[i] == "--dir" and i + 1 < len(args):
            tdir = os.path.expanduser(args[i + 1]); i += 2
        else:
            i += 1
    rows = load_rows()
    existing = {r.get("session_id"): r for r in rows}
    added = 0
    for path in sorted(glob.glob(os.path.join(tdir, "*.jsonl"))):
        sid = os.path.basename(path)[:-6]
        row = build_row(sid, path, "backfill", None)
        if row["date"] < since or (row["prompts"] == 0 and row["tool_calls"] == 0):
            continue
        if sid in existing and existing[sid].get("reason") != "backfill":
            continue  # a real SessionEnd row wins over a backfill
        existing[sid] = row
        added += 1
    write_rows(list(existing.values()))
    print(f"backfill: {added} rows written to {LEDGER}")


def backfill_missing(days=14, tdir=None):
    """Add ledger rows for transcripts that have none (SessionEnd does not fire when the
    window/process is killed, and such a session leaves no trace). Cheap: parses only
    transcripts modified in the last `days` days that are missing from the ledger."""
    tdir = tdir or DEFAULT_TRANSCRIPTS
    rows = load_rows()
    known = {r.get("session_id") for r in rows}
    cutoff = time.time() - days * 86400
    added = 0
    for path in glob.glob(os.path.join(tdir, "*.jsonl")):
        sid = os.path.basename(path)[:-6]
        if sid in known:
            continue
        try:
            if os.path.getmtime(path) < cutoff:
                continue
        except OSError:
            continue
        row = build_row(sid, path, "backfill", None)
        if row["prompts"] == 0 and row["tool_calls"] == 0:
            continue
        rows.append(row)
        added += 1
    if added:
        write_rows(rows)
    return added


def main():
    argv = sys.argv[1:]
    if argv and argv[0] == "--backfill":
        backfill(argv[1:])
        return
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}
    sid = payload.get("session_id")
    if not sid:
        return
    tp = os.path.expanduser(payload.get("transcript_path") or "")
    upsert(build_row(sid, tp, payload.get("reason"), payload.get("cwd")))
    cleanup_markers()


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # never break a session close
        sys.stderr.write(f"session_ledger: {exc}\n")
    sys.exit(0)
