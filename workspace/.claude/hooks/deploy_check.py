#!/usr/bin/env python3
"""PreToolUse hook: the pre-deploy check. Refuses a command-line production deploy that would ship
something nobody chose to ship.

A command-line deploy (`railway up`, `vercel --prod`) ships the folder it runs in, not a commit.
Before one runs, this hook looks at that folder and refuses the command (exit 2, the reasons on
stderr, which Claude reads) when any of these is true:

  1. the folder holds uncommitted changes            -> they would ship
  2. the branch lacks commits the remote's main has  -> the deploy would remove someone's live work
  3. Python code uses a name that no longer exists   -> NameError at runtime (ruff F821)

Each check that cannot run (no git, no remote, no network, no ruff) is skipped and never refuses.
A deploy the owner has agreed to ship as it is carries `DEPLOY_CHECK=skip` in front of the command.
Silent (exit 0, no output) for every command that is not a production deploy. These three were
prose rules in `_practices/deploying.md` until 2026-11-15; that file keeps what a script cannot see.
"""
import json
import os
import shlex
import shutil
import subprocess
import sys

SEPARATORS = {"&&", "||", ";", "|", "&", "(", ")"}
WRAPPERS = {"command", "exec", "time", "nohup", "npx", "bunx", "pnpm", "dlx", "-y", "--yes"}
VERCEL_NOT_A_DEPLOY = {"ls", "list", "inspect", "logs", "env", "alias", "domains", "whoami", "link", "pull",
                       "project", "projects", "teams", "switch", "login", "logout", "certs", "dns", "bisect"}
FETCH_SECONDS, RUFF_SECONDS = 8, 25


def _segments(command):
    """The simple commands of a shell line, each a token list, quotes respected."""
    lex = shlex.shlex(command, posix=True, punctuation_chars=True)
    lex.whitespace_split = True
    seg = []
    for tok in lex:
        if tok in SEPARATORS or set(tok) <= set("&|;()"):
            if seg:
                yield seg
            seg = []
        else:
            seg.append(tok)
    if seg:
        yield seg


def _strip(seg):
    """Drop leading VAR=value words and wrappers; return (env words, the command's own words)."""
    env, i = [], 0
    while i < len(seg):
        t = seg[i]
        if "=" in t and t.split("=", 1)[0].replace("_", "").isalnum() and not t.startswith("-"):
            env.append(t)
        elif t in WRAPPERS:
            pass
        elif t == "perl" and i + 2 < len(seg) and seg[i + 1] == "-e":   # perl -e 'alarm N; exec @ARGV' cmd …
            i += 2
        elif t == "timeout" and i + 1 < len(seg):
            i += 1
        else:
            break
        i += 1
    return env, seg[i:]


def deploys(command, cwd):
    """Every production deploy in the command: (folder it runs in, the words, skip requested)."""
    out, here = [], cwd
    try:
        segs = list(_segments(command))
    except ValueError:
        return out
    for seg in segs:
        env, words = _strip(seg)
        if not words:
            continue
        if words[0] == "cd" and len(words) > 1:
            here = os.path.normpath(os.path.join(here, os.path.expanduser(words[1])))
            continue
        is_deploy = (words[:2] == ["railway", "up"] or
                     (words[0] == "vercel" and "--prod" in words and
                      not (len(words) > 1 and words[1] in VERCEL_NOT_A_DEPLOY)))
        if is_deploy and "--help" not in words and "-h" not in words:
            out.append((here, "railway up" if words[0] == "railway" else "vercel --prod", "DEPLOY_CHECK=skip" in env))
    return out


def _git(folder, *args, timeout=5):
    try:
        r = subprocess.run(["git", "-C", folder, *args], capture_output=True, text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired):
        return None
    return r


def problems(folder):
    found = []
    inside = _git(folder, "rev-parse", "--is-inside-work-tree")
    if inside is not None and inside.returncode == 0:
        dirty = _git(folder, "status", "--porcelain", "--", ".")
        lines = [l for l in (dirty.stdout.splitlines() if dirty and dirty.returncode == 0 else []) if l.strip()]
        if lines:
            shown = "\n".join("      " + l for l in lines[:12]) + (f"\n      … and {len(lines) - 12} more" if len(lines) > 12 else "")
            found.append(f"{len(lines)} uncommitted change(s) in the folder would ship:\n{shown}\n"
                         "    Commit what belongs to this deploy; move anything else out of this folder.")
        if _git(folder, "remote", "get-url", "origin") and _git(folder, "remote", "get-url", "origin").returncode == 0:
            fetched = _git(folder, "fetch", "-q", "origin", "main", timeout=FETCH_SECONDS)
            if fetched is not None and fetched.returncode == 0:
                missing = _git(folder, "rev-list", "--count", "HEAD..origin/main")
                n = int(missing.stdout.strip() or 0) if missing and missing.returncode == 0 else 0
                if n:
                    log = _git(folder, "log", "--oneline", "-5", "HEAD..origin/main")
                    found.append(f"the remote's main has {n} commit(s) this branch lacks, so the deploy would remove them:\n"
                                 + "\n".join("      " + l for l in (log.stdout.splitlines() if log else []))
                                 + "\n    Rebase onto origin/main, run the tests on the rebased head, then deploy.")
    if os.path.exists(os.path.join(folder, "pyproject.toml")) and shutil.which("uvx"):
        try:
            r = subprocess.run(["uvx", "ruff", "check", "--select", "F821", "--output-format", "concise", "--quiet", "."],
                               cwd=folder, capture_output=True, text=True, timeout=RUFF_SECONDS)
            hits = [l for l in r.stdout.splitlines() if "F821" in l]
            if hits:
                found.append(f"{len(hits)} use(s) of a name that is not defined (it would raise NameError when that line runs):\n"
                             + "\n".join("      " + l for l in hits[:8])
                             + "\n    Restore the name or remove its users.")
        except (OSError, subprocess.TimeoutExpired):
            pass
    return found


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return 0
    if payload.get("tool_name") != "Bash":
        return 0
    command = (payload.get("tool_input") or {}).get("command") or ""
    if "railway" not in command and "vercel" not in command:
        return 0
    refused = []
    for folder, what, skip in deploys(command, payload.get("cwd") or os.getcwd()):
        if skip:
            continue
        found = problems(folder)
        if found:
            refused.append(f"[Deploy check] `{what}` in {folder} was not run:\n" + "\n".join(f"  - {p}" for p in found))
    if refused:
        sys.stderr.write("\n".join(refused) + "\nTo ship the folder exactly as it is, tell the owner what will ship, and on "
                         "their yes put DEPLOY_CHECK=skip in front of the deploy command.\n")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
