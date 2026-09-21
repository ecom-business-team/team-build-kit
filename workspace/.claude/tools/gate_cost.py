#!/usr/bin/env python3
"""Gate-cost instrument — what a gate document costs the owner.

For each session id prefix given, read its transcript and report, for every write of a memo,
a PRD or a project log: the minutes until the owner's next turn, whether that turn reads as an
approval, and its first 60 characters; then the count of the owner's turns that were not approvals
(the clarifying turns), and the median minutes from the last document write to each approval.

Usage:  python3 .claude/tools/gate_cost.py <id8> [<id8> …]      the 8-char session-id prefixes
        python3 .claude/tools/gate_cost.py --file <transcript.jsonl> [--file …]
Baselines: record them in the project log of the build that measures them, and in the owner's
outcome-check task, so the next measurement has something to compare against.
Shares the transcript loader with orientation_cost.py and the human-turn filter with the
session ledger hook; a different question gets a sibling tool, not a fork.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent / "hooks")]
from orientation_cost import load  # noqa: E402  (importable: its report runs only under __main__)
from session_ledger import human_text  # noqa: E402

DOC_RE = re.compile(r"(?:^|[\s\"'`=(])((?:[\w./~-]*/)?(?:_admin/memos/[\w.-]+\.md|[\w.-]+_prd\.md|project_log\.md))")
WRITE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit"}
REDIRECT_RE = re.compile(r"(?:>>?|\btee(?:\s+-a)?)\s*(\S+)")
PY_WRITE_RE = re.compile(r"write_text\(|\.write\(|open\([^)]*['\"][wa]")
APPROVAL_RE = re.compile(r"\b(approved?|proceed|go ahead|looks? (?:great|good)|sounds (?:great|good)|ship it|lgtm|confirmed)\b|^(?:yes|yep|yeah|ok(?:ay)?|sure)\b", re.I)


def doc_path(text: str) -> str | None:
    """The gate-document path in `text`, from `_admin/` onwards when that folder is named."""
    m = DOC_RE.search(text or "")
    if not m:
        return None
    return re.sub(r"^.*?(?=_admin/)", "", m.group(1))


def doc_written(name: str, inp: dict) -> str | None:
    """The gate document this tool call writes, or None. Reads (cat, grep) never count."""
    if not isinstance(inp, dict):
        return None
    if name in WRITE_TOOLS:
        return doc_path(inp.get("file_path"))
    if name != "Bash":
        return None
    cmd = inp.get("command") or ""
    for target in REDIRECT_RE.findall(cmd):
        doc = doc_path(target.strip("'\""))
        if doc:
            return doc
    if PY_WRITE_RE.search(cmd) or re.search(r"\bsed -i\b", cmd):
        return doc_path(cmd)
    return None


def is_approval(text: str) -> bool:
    return bool(APPROVAL_RE.search(text.strip()))


def minutes(a: str, b: str) -> float:
    fa = dt.datetime.fromisoformat(a.replace("Z", "+00:00"))
    fb = dt.datetime.fromisoformat(b.replace("Z", "+00:00"))
    return (fb - fa).total_seconds() / 60


def analyse(recs: list[dict]) -> dict:
    """Pure: transcript records → {writes: [...], turns: [...], clarifying: n, approvals: n, median_minutes}."""
    events = []  # (ts, kind, payload) in transcript order
    for r in recs:
        if r.get("isSidechain"):
            continue
        ts = r.get("timestamp")
        if not ts:
            continue
        if r.get("type") == "assistant":
            for x in (r.get("message", {}) or {}).get("content") or []:
                if isinstance(x, dict) and x.get("type") == "tool_use":
                    doc = doc_written(x.get("name") or "", x.get("input") or {})
                    if doc:
                        events.append((ts, "write", doc))
        else:
            text = human_text(r)
            if text:
                events.append((ts, "turn", text))
    writes, turns = [], []
    last_write = None
    for i, (ts, kind, payload) in enumerate(events):
        if kind == "write":
            nxt = next(((t, p) for t, k, p in events[i + 1:] if k == "turn"), None)
            writes.append({
                "ts": ts, "doc": payload,
                "minutes": round(minutes(ts, nxt[0]), 1) if nxt else None,
                "approval": is_approval(nxt[1]) if nxt else None,
                "turn": nxt[1][:60] if nxt else None,
            })
            last_write = ts
        else:
            approval = is_approval(payload)
            turns.append({"ts": ts, "text": payload[:60], "approval": approval,
                          "minutes_since_write": round(minutes(last_write, ts), 1) if last_write else None})
    approvals = [t for t in turns if t["approval"]]
    clarifying = [t for t in turns if not t["approval"]]
    to_approval = [t["minutes_since_write"] for t in approvals if t["minutes_since_write"] is not None]
    return {
        "writes": writes, "turns": turns,
        "approvals": len(approvals), "clarifying": len(clarifying),
        "median_minutes": round(statistics.median(to_approval), 1) if to_approval else None,
        "minutes_to_approval": to_approval,
    }


def report(label: str, result: dict) -> str:
    out = [f"\n### {label} — {len(result['writes'])} document writes · {len(result['turns'])} owner turns"]
    for w in result["writes"]:
        if w["turn"] is None:
            out.append(f"  {w['ts'][11:19]}  {w['doc']}  → no owner turn followed")
        else:
            verdict = "approval" if w["approval"] else "not an approval"
            out.append(f"  {w['ts'][11:19]}  {w['doc']}  → {w['minutes']} min → {verdict}: {w['turn']!r}")
    out.append(f"  clarifying turns (not approvals): {result['clarifying']}"
               + (": " + " | ".join(repr(t['text']) for t in result['turns'] if not t['approval']) if result['clarifying'] else ""))
    if result["median_minutes"] is not None:
        out.append(f"  minutes from the last write to each approval: {result['minutes_to_approval']} · median {result['median_minutes']}")
    return "\n".join(out)


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.strip())
        return 0 if argv else 1
    rc = 0
    i = 0
    results = []
    while i < len(argv):
        if argv[i] == "--file":
            path = Path(argv[i + 1]); i += 2
            recs = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
            results.append(analyse(recs))
            print(report(path.name, results[-1]))
            continue
        try:
            path, recs = load(argv[i])
        except StopIteration:
            print(f"{argv[i]}: no transcript with that prefix", file=sys.stderr)
            rc = 1; i += 1
            continue
        results.append(analyse(recs))
        print(report(f"{argv[i]} ({path.name[:8]})", results[-1]))
        i += 1
    if len(results) > 1:
        print(pooled(results))
    return rc


def pooled(results: list[dict]) -> str:
    """One line across sessions: every write that an owner turn followed, pooled."""
    mins = sorted(w["minutes"] for r in results for w in r["writes"] if w["minutes"] is not None)
    clarifying = sum(r["clarifying"] for r in results)
    turns = sum(len(r["turns"]) for r in results)
    if not mins:
        return f"\n### all sessions — no document write was followed by an owner turn · {turns} owner turns · {clarifying} clarifying"
    return (f"\n### all sessions — {len(mins)} writes followed by an owner turn: {mins[0]}–{mins[-1]} min, "
            f"median {round(statistics.median(mins), 1)} · {turns} owner turns · {clarifying} clarifying")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
