#!/usr/bin/env python3
"""PreToolUse hook: tier-2 retrieval-at-need for _practices/.

On the FIRST call to a tool family in a session (Supabase MCP, n8n MCP/REST, Railway, Vercel,
Google APIs, ClickUp, Discord, Supabase REST/psql), inject the matching _practices/<tool>.md
into Claude's context via additionalContext. Once per file per session (marker files under
~/.claude/state/practices-gate/<session>/). Replaces reliance on CONTEXT.md pointers alone,
which most CONTEXT.md files turned out not to carry when audited.
Silent (exit 0, no output) when nothing is due. Never blocks a tool call.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.abspath(os.path.join(HERE, "..", ".."))
PRACTICES = os.path.join(ROOT, "_practices")
STATE_DIR = os.path.expanduser("~/.claude/state/practices-gate")
CAP = 9000  # additionalContext is capped at 10,000 chars by Claude Code

BASH_RULES = [
    (r"N8N_API|n8n\.cloud|/api/v1/(workflows|executions|credentials)|/webhook(-test)?/", ["n8n"]),
    (r"\brailway\b", ["railway", "deploying"]),
    (r"\bvercel\b", ["vercel", "deploying"]),
    (r"googleapis\.com|\bgcloud auth\b|GOOGLE_APPLICATION_CREDENTIALS", ["google-apis"]),
    (r"api\.clickup\.com|CLICKUP_API", ["clickup"]),
    (r"discord(app)?\.com/api|DISCORD_BOT_TOKEN", ["discord"]),
    (r"api\.tally\.so|TALLY_API_KEY", ["tally"]),
    (r"supabase\.co/(rest|rpc)|SUPABASE_(URL|SERVICE|KEY|ANON)|\bpsql\b|\bpostgrest\b", ["supabase"]),
]


def files_for(tool_name, tool_input):
    out = []
    if tool_name.startswith("mcp__supabase__"):
        out.append("supabase")
    elif tool_name.startswith("mcp__n8n-mcp__"):
        out.append("n8n")
    elif tool_name == "Bash":
        cmd = tool_input.get("command", "") or ""
        for pattern, files in BASH_RULES:
            if re.search(pattern, cmd):
                out.extend(files)
    seen, uniq = set(), []
    for f in out:
        if f not in seen:
            seen.add(f)
            uniq.append(f)
    return uniq


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return
    tool_name = payload.get("tool_name") or ""
    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        tool_input = {}
    files = files_for(tool_name, tool_input)
    if not files:
        return
    sid = payload.get("session_id") or "unknown"
    key = f"{sid}__{payload.get('agent_id') or 'main'}"
    marker_dir = os.path.join(STATE_DIR, key)
    os.makedirs(marker_dir, exist_ok=True)

    due = []
    for f in files:
        path = os.path.join(PRACTICES, f + ".md")
        marker = os.path.join(marker_dir, f)
        if os.path.exists(marker) or not os.path.exists(path):
            continue
        due.append((f, path))
        open(marker, "w").close()
    if not due:
        return

    label = tool_name if tool_name != "Bash" else "Bash(" + ", ".join(f for f, _ in due) + ")"
    parts = [
        f"[Practices gate] First {label} use this session. Tier-2 retrieval-at-need: the practice file(s) "
        f"below are loaded now. Project parameters (IDs, service names, credential locations) live in the "
        f"owning workspace CONTEXT.md; read it if you have not. Files: "
        + ", ".join(f"_practices/{f}.md" for f, _ in due)
    ]
    total = len(parts[0])
    for f, path in due:
        try:
            with open(path, encoding="utf-8", errors="ignore") as fh:
                body = fh.read()
        except OSError:
            continue
        block = f"\n\n===== _practices/{f}.md =====\n{body.strip()}"
        if total + len(block) > CAP:
            block = f"\n\n===== _practices/{f}.md ===== (not inlined, {len(body)} chars) -> Read it before continuing."
        parts.append(block)
        total += len(block)
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                             "additionalContext": "".join(parts)}}))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # never block a tool call
        sys.stderr.write(f"practices_gate: {exc}\n")
    sys.exit(0)
