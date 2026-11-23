#!/usr/bin/env python3
"""PreToolUse hook: tier-2 retrieval-at-need for _practices/.

On the FIRST call to a tool family in a session (Supabase MCP, n8n MCP/REST, Railway, Vercel,
Google APIs, ClickUp, Discord, Supabase REST/psql; any other MCP server loads
_practices/<server>.md and <server>_conventions.md when they exist, the server name lowercased,
a claude.ai connector's claude_ai_ prefix stripped, and a hyphenated name with no file of its own
read as the family before the hyphen), inject the matching _practices/<tool>.md
into Claude's context via additionalContext. Once per file per session (marker files under
~/.claude/state/practices-gate/<session>/). Replaces reliance on CONTEXT.md pointers alone,
which most CONTEXT.md files turned out not to carry when audited.
Silent (exit 0, no output) when nothing is due. Never blocks a tool call.

A shell command loads a tool's file only when the tool is the command word of a segment: the start
of the line, or after `&&`, `||`, `;`, `|`, `(` or a new line, once leading VAR=value words and
wrappers (`npx`, `timeout 60`, `env`) are dropped. A tool named only as an argument, a file name,
quoted text or a heredoc body loads nothing. A pattern that is a web address or a variable name
matches anywhere in the text, because those are always arguments. A line that cannot be read as
shell (an unclosed quote) falls back to matching the tool's word anywhere.
"""
import json
import os
import re
import shlex
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("CLAUDE_PROJECT_DIR") or os.path.abspath(os.path.join(HERE, "..", ".."))
PRACTICES = os.path.join(ROOT, "_practices")
STATE_DIR = os.path.expanduser("~/.claude/state/practices-gate")
CAP = 9000  # additionalContext is capped at 10,000 chars by Claude Code

# A text rule (a pattern string) matches anywhere in the command. A command rule (a tuple of the
# command word and, optionally, the word that must follow it) matches only a segment's command word.
BASH_RULES = [
    (r"N8N_API|n8n\.cloud|/api/v1/(workflows|executions|credentials)|/webhook(-test)?/", ["n8n"]),
    (("railway",), ["railway", "deploying"]),
    (r"frame\.io|\bf\.io/", ["frameio"]),
    (("vercel",), ["vercel", "deploying"]),
    (r"googleapis\.com|GOOGLE_APPLICATION_CREDENTIALS", ["google-apis"]),
    (("gcloud", "auth"), ["google-apis"]),
    (r"api\.clickup\.com|CLICKUP_API", ["clickup"]),
    (r"discord(app)?\.com/api|DISCORD_BOT_TOKEN", ["discord"]),
    (r"api\.tally\.so|TALLY_API_KEY", ["tally"]),
    (r"supabase\.co/(rest|rpc)|SUPABASE_(URL|SERVICE|KEY|ANON)", ["supabase"]),
    (("psql",), ["supabase"]),
    (("postgrest",), ["supabase"]),
]
WRAPPERS = {"command", "exec", "time", "nohup", "env", "sudo", "npx", "bunx", "pnpm", "dlx", "-y", "--yes"}


def command_words(command):
    """The command word of each segment of a shell line, with the word after it: [(word, next word)].
    Quotes are respected, a heredoc body is skipped. Raises ValueError on a line shlex cannot read."""
    lex = shlex.shlex(command, posix=True, punctuation_chars="();<>|&\n")
    lex.whitespace, lex.whitespace_split, lex.commenters = " \t\r", True, ""
    segs, seg, pending, body_end, prev = [], [], [], None, "\n"
    for tok in lex:
        separator = set(tok) <= set("&|;()\n")
        if body_end is not None:                      # inside a heredoc body: skip to its end word
            if tok == body_end and "\n" in prev:
                body_end = pending.pop(0) if pending else None
        elif prev == "<<":                            # the heredoc's end word
            pending.append(tok.lstrip("-"))
        elif separator:
            if seg:
                segs.append(seg)
            seg = []
            if "\n" in tok and pending:
                body_end = pending.pop(0)
        else:
            if tok.startswith("`") and seg:           # a backtick opens a command inside the segment
                segs.append(seg)
                seg = []
            seg.append(tok)
        prev = tok
    if seg:
        segs.append(seg)
    out = []
    for seg in segs:
        i = 0
        while i < len(seg):
            t = seg[i]
            if "=" in t and t.split("=", 1)[0].replace("_", "").isalnum() and not t.startswith("-"):
                pass                                  # VAR=value
            elif t in WRAPPERS or t == "$":           # "$" is what shlex leaves of "$(" before the "("
                pass
            elif t == "timeout" and i + 1 < len(seg):
                i += 1
            else:
                break
            i += 1
        if i < len(seg):
            word = os.path.basename(seg[i].lstrip("`")).split("@")[0]
            out.append((word, seg[i + 1].rstrip("`") if i + 1 < len(seg) else ""))
    return out


def bash_files(cmd):
    try:
        words = command_words(cmd)
    except ValueError:
        words = None
    out = []
    for rule, files in BASH_RULES:
        if isinstance(rule, str):
            hit = re.search(rule, cmd)
        elif words is None:
            hit = re.search(r"\b" + r"\s+".join(map(re.escape, rule)) + r"\b", cmd)
        else:
            hit = any(w == rule[0] and (len(rule) == 1 or nxt == rule[1]) for w, nxt in words)
        if hit:
            out.extend(files)
    return out


def files_for(tool_name, tool_input):
    out = []
    if tool_name.startswith("mcp__supabase__"):
        out.append("supabase")
    elif tool_name.startswith("mcp__n8n-mcp__"):
        out.append("n8n")
    elif tool_name.startswith("mcp__"):
        # Any other MCP server: its same-named practice file and conventions file, when they exist.
        # The name is lowercased with any claude.ai connector prefix stripped (mcp__claude_ai_ClickUp__ -> clickup);
        # a name with no practice file of its own falls back to its family before the first hyphen (supabase-prod -> supabase).
        server = tool_name.split("__")[1].lower()
        if server.startswith("claude_ai_"):
            server = server[len("claude_ai_"):]
        if "-" in server and not os.path.exists(os.path.join(PRACTICES, server + ".md")):
            server = server.split("-")[0]
        out.extend([server, server + "_conventions"])
    elif tool_name == "Bash":
        out.extend(bash_files(tool_input.get("command", "") or ""))
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
