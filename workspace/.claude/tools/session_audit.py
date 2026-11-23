#!/usr/bin/env python3
"""Session audit — what a workspace's own rules cost across its saved sessions, and what work was done.

Reads every main-thread transcript of this workspace and prints one table per month: how often the
owner had to correct, approve or ask for the close; how much of what Claude read and wrote was
instruction or process documents; how many tasks were filed and closed; which practice files the
gate loaded. It is the before-and-after measure for a change to the harness: run it, change one
thing, run it again a few weeks later.

Usage:  python3 .claude/tools/session_audit.py                    every month, table output
        python3 .claude/tools/session_audit.py --since 2026-11-15 only sessions started on or after
                                                                  (a date, or a full UTC time such as
                                                                  2026-11-15T18:30:00Z)
        python3 .claude/tools/session_audit.py --report out.json  everything the workspace audit reads:
                                                                  the summary, one row per session with
                                                                  its first ask and where its edits went,
                                                                  every instruction file with its size and
                                                                  use, and the flagged owner turns
        python3 .claude/tools/session_audit.py --json out.json    also dump the raw per-session rows
        python3 .claude/tools/session_audit.py --samples out.txt  also dump the flagged owner turns
        python3 .claude/tools/session_audit.py --dir <folder>     another transcript folder (tests)
        python3 .claude/tools/session_audit.py --root <folder>    another workspace root (tests)

A workspace's own names. The patterns below know the kit's documents. A workspace adds its own in
`.claude/session_audit.json`, a file it owns and the kit never writes:
    {"instruction": ["<regex>"], "process": ["<regex>"], "task_filed_commands": ["<regex>"]}
`instruction` and `process` extend what counts as an instruction or a process document;
`task_filed_commands` are shell commands that file one task each (a tracker's command line).

What it cannot see. It counts events and matches words; it does not judge whether an output was
good. `corrections` is a floor found by word patterns. Tasks are counted from a connected task
tool's add and complete calls and from `task_filed_commands`; a tracker closed another way is not
counted. It reads only this computer's saved sessions and writes only the files you name.
Shares the human-turn filter with the session ledger hook; a different question gets a sibling
tool, not a fork.
"""
from __future__ import annotations

import argparse
import collections
import datetime
import glob
import importlib.util
import json
import os
import re
import statistics
from pathlib import Path

HERE = Path(__file__).resolve().parent
WS_ROOT = os.environ.get("CLAUDE_PROJECT_DIR") or str(HERE.parents[1])

_spec = importlib.util.spec_from_file_location("session_ledger", HERE.parent / "hooks" / "session_ledger.py")
_ledger = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_ledger)
human_text = _ledger.human_text

# A read or edit of these is the workspace instructing Claude; of PROC, the workspace recording itself.
INSTR_BASE = (r"_practices/|documentation_standard|workflow_design_standard|testing_standard|glossary\.md"
              r"|lifecycle_map|SKILLS\.md|CONTEXT\.md|SKILL\.md|CLAUDE\.md|priorities\.md|skills\.d/")
PROC_BASE = r"state\.md|project_log|daily-outputs/|brief\.md|/go\.md|memo\.md|prd\.md|/memory/|sessions\.jsonl|_admin/audits/"
INSTR, PROC, FILED_CMDS = re.compile(f"({INSTR_BASE})"), re.compile(f"({PROC_BASE})"), []
CORRECT = re.compile(r"(^|\b)(no[,.] |nope|not what i|that'?s not|that is not|you (didn'?t|did not|missed|forgot|skipped"
                     r"|ignored|keep)|why (did|are|would) you|i (said|asked|told you)|wrong|incorrect|don'?t do that"
                     r"|still (not|broken|wrong|failing)|revert|undo that)", re.I)
UNCLEAR = re.compile(r"(i don'?t understand|i do not understand|confus|what does .{0,40} mean|too (long|much|verbose"
                     r"|dense|complex|wordy)|simpler|plain (english|language|words)|hard to (read|follow)|lost me)", re.I)
APPROVE = re.compile(r"^\W*(yes|yep|yeah|ok|okay|go|go ahead|proceed|please proceed|approved?|do it|continue"
                     r"|sounds (good|great)|perfect|great|ship it|confirmed?|correct|agreed|run it|start|trusted)\b", re.I)
ASKS_CLOSE = re.compile(r"(session close|close (it|this|the session) out|ready to close)", re.I)
READ_CMD = re.compile(r"\s*(cd [^;&]+(&&|;)\s*)?(cat|sed -n|head|tail|wc|grep|rg|ls)\b")
TASK_ADD = re.compile(r"_(add|create)[-_]?tasks?$", re.I)      # a connected task tool's add call
TASK_DONE = re.compile(r"_(complete|close)[-_]?tasks?$", re.I)  # and its complete call
GATE_FILE = re.compile(r"=====\s*(_practices/[\w\-.]+)")
MD_TOKEN = re.compile(r"[\w./~\-]+\.md")
SHORT = 60  # an owner turn under this many characters carries no new information beyond a go or a nudge
ASK_CHARS = 300


def configure(root):
    """Add the workspace's own patterns from <root>/.claude/session_audit.json, when it has one."""
    global INSTR, PROC, FILED_CMDS
    try:
        cfg = json.loads((Path(root) / ".claude" / "session_audit.json").read_text())
    except (OSError, ValueError):
        cfg = {}
    INSTR = re.compile("(" + "|".join([INSTR_BASE] + list(cfg.get("instruction") or [])) + ")")
    PROC = re.compile("(" + "|".join([PROC_BASE] + list(cfg.get("process") or [])) + ")")
    FILED_CMDS = [re.compile(x) for x in cfg.get("task_filed_commands") or []]


def transcripts_dir(root):
    return Path.home() / ".claude" / "projects" / re.sub(r"[^A-Za-z0-9]", "-", str(root))


def _result_sizes(content):
    out = []
    for b in content if isinstance(content, list) else []:
        if isinstance(b, dict) and b.get("type") == "tool_result":
            c = b.get("content")
            n = sum(len(x.get("text", "")) for x in c if isinstance(x, dict)) if isinstance(c, list) else len(c or "")
            out.append((b.get("tool_use_id"), n))
    return out


def _kind(path):
    return "instr" if INSTR.search(path or "") else "proc" if PROC.search(path or "") else "other"


def _rel(path, root):
    """A path as the workspace names it: relative to the root, or ~/… for the skills folder."""
    path = os.path.expanduser(path or "")
    for base, prefix in ((str(root), ""), (str(Path.home()), "~/")):
        if path.startswith(base.rstrip("/") + "/"):
            return prefix + path[len(base.rstrip("/")) + 1:]
    return path


def _count(inp):
    for k in ("tasks", "items", "ids"):
        if isinstance(inp.get(k), list) and inp[k]:
            return len(inp[k])
    return 1


def read_session(path, samples=None, root=WS_ROOT):
    s = collections.Counter()
    info = dict(id=os.path.basename(path)[:8], start=None, cost=0.0, gate_files=collections.Counter(),
                calls_before_first_edit=None, first_ask="", edit_folders=collections.Counter(),
                skills=collections.Counter(), instr_files=collections.Counter(), process_edits=collections.Counter())
    pending, edited, in_close = {}, False, False
    for line in open(path, errors="replace"):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if not isinstance(d, dict) or d.get("isSidechain"):
            continue
        t = d.get("type")
        if t == "cost-state":
            info["cost"] = d.get("totalCostUSD") or 0.0
        elif t == "attachment":
            a = d.get("attachment") or {}
            if a.get("type") == "hook_additional_context":
                for x in a.get("content") or []:
                    if isinstance(x, str):
                        s["hook_chars"] += len(x)
                        for f in GATE_FILE.findall(x):
                            info["gate_files"][f] += 1
                            info["instr_files"][f] += 1
                            s["gate_loads"] += 1
        elif t == "user":
            info["start"] = info["start"] or d.get("timestamp")
            if d.get("isCompactSummary"):
                s["compactions"] += 1
                continue
            for tid, n in _result_sizes((d.get("message") or {}).get("content")):
                s["read_chars"] += n
                s[pending.pop(tid, "other") + "_read_chars"] += n
            text = human_text(d)
            if not text:
                continue
            in_close = False
            s["turns"] += 1
            if s["turns"] == 1:
                info["first_ask"] = " ".join(text.split())[:ASK_CHARS]
                continue
            s["followups"] += 1
            flag = None
            if len(text) < SHORT:
                s["short"] += 1
                if ASKS_CLOSE.search(text):
                    s["asks_close"] += 1
                elif APPROVE.search(text):
                    s["approvals"] += 1
            if CORRECT.search(text[:600]):
                s["corrections"] += 1
                flag = "C"
            if UNCLEAR.search(text[:800]):
                s["unclear"] += 1
                flag = flag or "U"
            if flag and samples is not None:
                samples.append(f"[{flag}] {info['id']} {(d.get('timestamp') or '')[:10]} | {text[:400]}")
        elif t == "assistant":
            msg = d.get("message") or {}
            out = (msg.get("usage") or {}).get("output_tokens") or 0
            s["output_tokens"] += out
            if in_close:
                s["close_output_tokens"] += out
            for b in msg.get("content") or []:
                if not isinstance(b, dict) or b.get("type") != "tool_use":
                    continue
                s["tool_calls"] += 1
                name, inp = b.get("name", ""), b.get("input") or {}
                if in_close:
                    s["close_tool_calls"] += 1
                if name == "Skill":
                    info["skills"][inp.get("skill") or "?"] += 1
                    if inp.get("skill") == "session-close":
                        s["closes"] += 1
                        in_close = True
                elif name.startswith("mcp__") and TASK_ADD.search(name):
                    s["filed_tool"] += _count(inp)
                elif name.startswith("mcp__") and TASK_DONE.search(name):
                    s["closed_tool"] += _count(inp)
                elif name == "Read":
                    k = _kind(inp.get("file_path"))
                    pending[b.get("id")] = k
                    s[k + "_reads"] += 1
                    if k == "instr":
                        info["instr_files"][_rel(inp.get("file_path"), root)] += 1
                elif name == "Bash":
                    cmd = inp.get("command", "")
                    s["filed_cmd"] += sum(len(rx.findall(cmd)) for rx in FILED_CMDS)
                    if READ_CMD.match(cmd) and not re.search(r">\s*\S", cmd) and _kind(cmd) != "other":
                        pending[b.get("id")] = _kind(cmd)
                        s[_kind(cmd) + "_reads"] += 1
                        for tok in MD_TOKEN.findall(cmd):
                            if _kind(tok) == "instr":
                                info["instr_files"][_rel(tok, root)] += 1
                elif name in ("Edit", "Write", "MultiEdit", "NotebookEdit"):
                    k = _kind(inp.get("file_path"))
                    s[k + "_edits"] += 1
                    if k != "other":
                        info["process_edits"][_rel(inp.get("file_path"), root)] += 1
                    else:
                        rel = _rel(inp.get("file_path"), root)
                        info["edit_folders"]["(skills folder)" if rel.startswith("~/.claude/skills/") else
                                             "(outside the workspace)" if rel.startswith(("/", "~")) else
                                             rel.split("/")[0] if "/" in rel else "(root)"] += 1
                    if not edited:
                        edited = True
                        info["calls_before_first_edit"] = s["tool_calls"] - 1
    info.update(s)
    info["filed"] = s["filed_tool"] + s["filed_cmd"]
    return info if (s["turns"] or s["tool_calls"]) else None


def _pct(a, b):
    return round(100 * a / b, 1) if b else 0.0


def summarise(rows):
    tot = collections.Counter()
    for r in rows:
        tot.update({k: v for k, v in r.items() if isinstance(v, (int, float)) and not isinstance(v, bool)})
    n = len(rows)
    edits = tot["instr_edits"] + tot["proc_edits"] + tot["other_edits"]
    before = [r["calls_before_first_edit"] for r in rows if r["calls_before_first_edit"] is not None]
    return {
        "sessions": n,
        "cost_usd": round(sum(r["cost"] for r in rows)),
        "owner_followups": tot["followups"],
        "corrections_per_100": _pct(tot["corrections"], tot["followups"]),
        "unclear_per_100": _pct(tot["unclear"], tot["followups"]),
        "short_turns_pct": _pct(tot["short"], tot["followups"]),
        "approval_only_pct": _pct(tot["approvals"], tot["followups"]),
        "asks_for_close": tot["asks_close"],
        "session_closes": tot["closes"],
        "close_share_of_output_pct": _pct(tot["close_output_tokens"], tot["output_tokens"]),
        "sessions_that_filed_pct": _pct(sum(1 for r in rows if r["filed"]), n),
        "tasks_filed": tot["filed"],
        "task_tool_filed": tot["filed_tool"],
        "task_tool_closed": tot["closed_tool"],
        "process_edits_pct": _pct(tot["instr_edits"] + tot["proc_edits"], edits),
        "instruction_share_of_reading_pct": _pct(tot["instr_read_chars"], tot["read_chars"]),
        "instruction_kchars_per_session": round(tot["instr_read_chars"] / n / 1000, 1) if n else 0,
        "hook_kchars_per_session": round(tot["hook_chars"] / n / 1000, 1) if n else 0,
        "median_calls_before_first_edit": statistics.median(before) if before else None,
        "gate_loads": tot["gate_loads"],
        "compactions": tot["compactions"],
    }


def inventory(root, rows):
    """Every instruction file the workspace holds: its size, and in how many of these sessions it was used."""
    root = Path(root)
    used, skills = collections.Counter(), collections.Counter()
    for r in rows:
        used.update(set(r["instr_files"]))
        skills.update(set(r["skills"]))
    found = set()
    for pat in ("CLAUDE.md", "*.md", "_practices/*.md", "*/CONTEXT.md", "*/*/CONTEXT.md", "*/CLAUDE.md",
                ".claude/CONTEXT.md", ".claude/skills.d/*.md"):
        found.update(p for p in root.glob(pat) if p.is_file() and _kind(str(p.relative_to(root))) == "instr"
                     or p.is_file() and p.name == "CLAUDE.md")
    found.update(root / f for f in used if not f.startswith(("/", "~")) and (root / f).is_file())
    out = [{"path": str(p.relative_to(root)), "chars": p.stat().st_size,
            "sessions_used": used.get(str(p.relative_to(root)), 0)} for p in sorted(found)]
    for p in sorted((Path.home() / ".claude" / "skills").glob("*/SKILL.md")):
        out.append({"path": f"skill: {p.parent.name}", "chars": p.stat().st_size, "sessions_used": skills.get(p.parent.name, 0)})
    for r in out:
        if r["path"] == "CLAUDE.md":  # the map loads at the start of every session; nothing has to read it
            r["sessions_used"] = len(rows)
        r["cost"] = r["chars"] * r["sessions_used"]  # characters Claude spent on this file across the period
    return sorted(out, key=lambda r: (-r["cost"], -r["chars"]))


def report(rows, root, since, samples):
    folders, process = collections.Counter(), collections.Counter()
    for r in rows:
        folders.update(r["edit_folders"])
        process.update(r["process_edits"])
    return {
        "generated": datetime.date.today().isoformat(),
        "measured_to": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "since": since,
        "first_session": min((r["start"] or "")[:10] for r in rows),
        "last_session": max((r["start"] or "")[:10] for r in rows),
        "summary": summarise(rows),
        "edits_by_folder": dict(folders.most_common()),  # the work: every edit that is not to an instruction or process document
        "process_edits_by_file": dict(process.most_common(25)),  # the paperwork: edits to instruction and process documents
        "sessions": [{"id": r["id"], "date": (r["start"] or "")[:10], "first_ask": r["first_ask"],
                      "edits_by_folder": dict(r["edit_folders"]), "skills": dict(r["skills"]),
                      "tool_calls": r.get("tool_calls", 0), "calls_before_first_edit": r["calls_before_first_edit"],
                      "followups": r.get("followups", 0), "approvals": r.get("approvals", 0),
                      "corrections": r.get("corrections", 0), "tasks_filed": r["filed"]} for r in rows],
        "instruction_files": inventory(root, rows),
        "flagged_owner_turns": samples or [],
        "limits": "Counts events and matches words. Corrections are a floor. It does not judge whether the work was good.",
    }


def run(folder, since=None, samples=None, root=WS_ROOT):
    rows = []
    for f in sorted(glob.glob(os.path.join(str(folder), "*.jsonl"))):
        flagged = [] if samples is not None else None
        r = read_session(f, flagged, root)
        if r and r["skills"].get("workspace-audit") and not r["edit_folders"]:
            continue  # a run of the audit itself is not the owner's work
        if r and (not since or (r["start"] or "") >= since):
            rows.append(r)
            if flagged:
                samples.extend(flagged)  # only a measured session's turns are reported
    return rows


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("--root", default=WS_ROOT)
    p.add_argument("--dir")
    p.add_argument("--since")
    p.add_argument("--report")
    p.add_argument("--json")
    p.add_argument("--samples")
    a = p.parse_args(argv)
    configure(a.root)
    folder = a.dir or transcripts_dir(a.root)
    samples = [] if (a.samples or a.report) else None
    rows = run(folder, a.since, samples, a.root)
    if not rows:
        print("no sessions found in", folder, f"since {a.since}" if a.since else "")
        return 1
    groups = collections.OrderedDict()
    for r in rows:
        groups.setdefault((r["start"] or "unknown")[:7], []).append(r)
    cols = [("all", summarise(rows))] + [(m, summarise(v)) for m, v in sorted(groups.items())]
    print(f"{'measure':<36}" + "".join(f"{c:>10}" for c, _ in cols))
    for k in cols[0][1]:
        print(f"{k:<36}" + "".join(f"{str(v[k]):>10}" for _, v in cols))
    gate = collections.Counter()
    for r in rows:
        gate.update(r["gate_files"])
    if gate:
        print("\npractice files the gate loaded most:")
        for f, n in gate.most_common(8):
            print(f"  {n:>4}  {f}")
    if a.report:
        Path(a.report).write_text(json.dumps(report(rows, a.root, a.since, samples), indent=1, default=dict))
        print("\nreport data:", a.report)
    if a.json:
        Path(a.json).write_text(json.dumps(rows, indent=1, default=dict))
    if a.samples:
        Path(a.samples).write_text("\n".join(samples) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
