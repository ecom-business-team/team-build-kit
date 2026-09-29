#!/usr/bin/env python3
"""referrers.py — lists every live file that points at a path, before that path is moved,
archived or deleted.  Reads only.

Usage, from the workspace root:  python3 .claude/tools/referrers.py <path> [<path> ...]
Searches every .md, .html, .json and .py file under the workspace root ($CLAUDE_PROJECT_DIR, else
the current directory) and the installed skills folder ($REFERRERS_SKILLS, else ~/.claude/skills).
A reference is any path-like string holding the target's name that resolves onto the target (or
into it, for a folder), tried against the referring file's own folder, the workspace root, the home
folder for `~/`, and as written when absolute.  So a relative link, a root-relative path and an
absolute path all count, and a same-named file elsewhere does not.
Not counted: files inside the target itself (they travel with it), and history — anything under an
`_archive/` or `_done/` folder, the session logs (`daily-outputs/`) and the bulk-write snapshots
(`bulk_ops/`) — records, whose pointers stay as written (_shared/project_close.md §I).  Skipped: dot-folders other than `.claude`, node_modules,
__pycache__, files over 2 MB.
Prints one line per reference ("file:line: the text") and a count per target.
Exit 0 when nothing live points at any target, 1 when something does (repoint each line, or move
it with the target), 2 when a target does not exist.
Rule: _shared/project_close.md §3 and §I — no move without a referrer check; a file is dead only
when nothing points at it.
"""
import os
import re
import sys
from pathlib import Path

ROOT = Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd()).resolve()
SKILLS = Path(os.environ.get("REFERRERS_SKILLS") or (Path.home() / ".claude" / "skills")).resolve()
EXTS = {".md", ".html", ".json", ".py"}
SKIP_DIRS = {"node_modules", "__pycache__"}
HISTORY = {"_archive", "_done", "daily-outputs", "bulk_ops"}
MAX_BYTES = 2_000_000


def files_under(base: Path):
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS and d not in HISTORY
                             and (not d.startswith(".") or d == ".claude"))
        for name in sorted(filenames):
            p = Path(dirpath) / name
            if p.suffix in EXTS:
                yield p


def resolves_onto(token: str, src: Path, target: Path) -> bool:
    token = re.sub(r"(#.*|:\d.*)$", "", token.strip("`'\"()[]<>,;"))
    if not token:
        return False
    if token.startswith("~/"):
        cands = [Path.home() / token[2:]]
    elif token.startswith("/"):
        cands = [Path(token)]
    else:
        cands = [src.parent / token, ROOT / token]
    for c in cands:
        try:
            r = Path(os.path.realpath(c))
        except ValueError:
            continue
        if r == target or target in r.parents:
            return True
    return False


def referrers(target: Path):
    name = re.escape(target.name)
    pattern = re.compile(r"[\w.~/-]*(?<![\w.-])" + name + r"(?![\w.-])(?:/[\w./-]*)?")
    bases = [ROOT] + ([SKILLS] if SKILLS.is_dir() and SKILLS != ROOT and ROOT not in SKILLS.parents else [])
    seen, out = set(), []
    for base in bases:
        for f in files_under(base):
            rf = f.resolve()
            if rf in seen or rf == target or target in rf.parents:
                continue
            seen.add(rf)
            try:
                if f.stat().st_size > MAX_BYTES:
                    continue
                text = f.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            if target.name not in text:
                continue
            for n, line in enumerate(text.splitlines(), 1):
                if target.name in line and any(resolves_onto(m.group(0), f, target) for m in pattern.finditer(line)):
                    out.append(f"{label(rf)}:{n}: {line.strip()[:160]}")
    return out


def label(p: Path) -> str:
    for base, prefix in ((ROOT, ""), (SKILLS, "~/.claude/skills/")):
        try:
            return prefix + p.relative_to(base).as_posix()
        except ValueError:
            pass
    return str(p)


def main(argv):
    if not argv:
        sys.exit(__doc__)
    found = 0
    for a in argv:
        t = Path(a).expanduser()
        target = Path(os.path.realpath(t if t.is_absolute() else Path.cwd() / t))
        if not target.exists():
            print(f"{a}: does not exist")
            return 2
        hits = referrers(target)
        for h in hits:
            print(h)
        print(f"{label(target)}: {len(hits)} live reference(s)")
        found += len(hits)
    return 1 if found else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
