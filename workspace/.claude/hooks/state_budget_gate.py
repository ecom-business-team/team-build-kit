#!/usr/bin/env python3
"""PostToolUse gate: a state.md is a SNAPSHOT (documentation_standard.md §6).

Fires after Edit / Write / MultiEdit / Bash. When the call touched a file named state.md,
count its words against the budget (a "Budget N words" marker in the file, else 400 under
_admin/prds/, else 600) and count date-led bullets (the shape a snapshot takes when it starts
accumulating history). Over budget or dated -> one additionalContext line back to the model.
Silent otherwise. Never blocks.
"""
import json
import os
import re
import sys

ROOT = os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()
DEFAULT_PROJECT, DEFAULT_PROGRAMME = 400, 600


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    ti = payload.get("tool_input") or {}
    candidates = []
    if ti.get("file_path"):
        candidates.append(ti["file_path"])
    if ti.get("command"):
        candidates += re.findall(r"[\w./~-]*state\.md", ti["command"])
    paths = []
    for c in candidates:
        if not c.endswith("state.md"):
            continue
        p = os.path.expanduser(c)
        if not os.path.isabs(p):
            p = os.path.join(payload.get("cwd") or ROOT, p)
        p = os.path.abspath(p)
        if os.path.isfile(p) and p not in paths:
            paths.append(p)
    msgs = []
    for path in paths:
        try:
            text = open(path, encoding="utf-8", errors="ignore").read()
        except OSError:
            continue
        m = re.search(r"[Bb]udget\s+(\d+)\s+words", text)
        budget = int(m.group(1)) if m else (DEFAULT_PROJECT if "/prds/" in path else DEFAULT_PROGRAMME)
        words = len(text.split())
        dated = re.findall(r"^\s*[-*]\s+\**\d{4}-\d{2}-\d{2}", text, re.M)
        rel = os.path.relpath(path, ROOT)
        if words > budget:
            msgs.append(f"{rel} is {words} words against a budget of {budget}. A snapshot over budget is carrying history: move dated content to project_log.md and rewrite state.md as a position.")
        if dated:
            msgs.append(f"{rel} has {len(dated)} date-led bullet(s). Date-led bullets are history; state.md holds the position, project_log.md holds the record.")
    if msgs:
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": "[State gate] " + " ".join(msgs)}}))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # never break a tool call
        sys.stderr.write(f"state_budget_gate: {exc}\n")
    sys.exit(0)
