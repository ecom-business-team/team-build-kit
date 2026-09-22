#!/usr/bin/env python3
"""PreToolUse hook on the Skill tool: the drop-in folder for commands.

When /<skill> is invoked and <workspace>/.claude/skills.d/<skill>.md exists, its text is injected into
Claude's context via additionalContext, so a person's own additions to a kit command ride along with it.
The folder is the person's: the kit never writes it, so an update cannot touch it (the conf.d pattern —
the package owns its file, you own a sibling the package reads). A plugin-prefixed name ("pack:prd")
resolves to its last segment. Silent (exit 0, no output) when there is nothing to add. Never blocks.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.abspath(os.path.join(HERE, "..", ".."))
ADDITIONS = os.path.join(ROOT, ".claude", "skills.d")
CAP = 9000  # additionalContext is capped at 10,000 chars by Claude Code
NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]*$")


def skill_name(tool_input):
    raw = tool_input.get("skill") if isinstance(tool_input, dict) else None
    if not isinstance(raw, str):
        return None
    name = raw.strip().lstrip("/").rsplit(":", 1)[-1]
    return name if NAME.match(name) else None


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    if payload.get("tool_name") != "Skill":
        return
    name = skill_name(payload.get("tool_input") or {})
    if not name:
        return
    path = os.path.join(ADDITIONS, name + ".md")
    if not os.path.isfile(path):
        return
    try:
        with open(path, encoding="utf-8", errors="ignore") as fh:
            body = fh.read().strip()
    except OSError:
        return
    if not body:
        return
    rel = f".claude/skills.d/{name}.md"
    head = (f"[Skill additions] This workspace adds to /{name}: `{rel}` is yours (the kit never writes it, "
            f"updates never touch it). Apply it alongside the skill's own steps.")
    if len(head) + len(body) + 8 > CAP:
        text = f"{head} It is {len(body)} chars long and is not inlined -> Read {rel} before continuing."
    else:
        text = f"{head}\n\n===== {rel} =====\n{body}"
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext": text}}))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # never block a tool call
        sys.stderr.write(f"skill_additions: {exc}\n")
    sys.exit(0)
