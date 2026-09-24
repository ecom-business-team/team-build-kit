#!/usr/bin/env python3
"""index_check.py — proves every folder's index names what the folder holds.  Reads only.

Usage, from the workspace root:  python3 .claude/tools/index_check.py [--links] [folder ...]
No arguments: every folder under the workspace root ($CLAUDE_PROJECT_DIR, else the current
directory) that holds a CONTEXT.md, not descending into dot-folders, node_modules, __pycache__
or _archive.  For each folder the index text is CONTEXT.md plus INDEX.md when present; an entry
is every name in the folder except dot-entries, __pycache__, node_modules, CONTEXT.md, INDEX.md,
and X.html when X.md exists (a rendered page beside its source); an entry is unnamed when its
name does not appear anywhere in the index text.
Exit 0 when every index names everything, 1 on any unnamed entry, 2 when a folder named on the
command line has no CONTEXT.md.
--links also resolves every explicit relative path (one starting ./ or ../) written in a backtick
span or a markdown link target in each checked folder's own .md files, against that file's folder,
or against the base a file declares in its first 30 lines ("Every path below is relative to
`dir/`"), and lists each one that does not exist ("folder/file.md: broken ../x"); a path holding a wildcard
or a placeholder (* { <) is skipped, and a trailing #anchor or :line is dropped.  Any broken path
exits 1.  Why: 20 evidence links in a design record were one level too deep and never resolved,
while every row that cited them passed review (milestone 1.2, 2026-09-23).
Rule: documentation_standard.md §5 (the CONTEXT.md contract).  Scope note: a name that appears
only in passing counts as named; the check proves presence, not a good description.
"""
import os
import re
import sys
from pathlib import Path

SKIP_DIRS = {"node_modules", "__pycache__", "_archive"}
SKIP_ENTRIES = {"__pycache__", "node_modules", "CONTEXT.md", "INDEX.md"}


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return ""


def indexed_folders(root: Path):
    """Every folder under root holding a CONTEXT.md, in sorted walk order."""
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith(".") and d not in SKIP_DIRS)
        if "CONTEXT.md" in filenames:
            out.append(Path(dirpath))
    return out


def unnamed(folder: Path):
    """The folder's entries whose names are not in its index text."""
    text = read(folder / "CONTEXT.md") + "\n" + read(folder / "INDEX.md")
    names = set(os.listdir(folder))
    missing = []
    for name in sorted(names):
        if name.startswith(".") or name in SKIP_ENTRIES:
            continue
        if name.endswith(".html") and name[:-5] + ".md" in names:
            continue
        if name not in text:
            missing.append(name)
    return missing


DECLARED_BASE = re.compile(r"paths?\b[^.\n]*\brelative to `([^`]+)`", re.IGNORECASE)
REL_PATH = re.compile(r"`(\.\.?/[^`\s]+)`|\]\((\.\.?/[^)\s]+)\)")


def broken_links(folder: Path):
    """Relative paths written in the folder's own .md files that do not resolve."""
    out = []
    for md in sorted(folder.glob("*.md")):
        text = read(md)
        declared = DECLARED_BASE.search("\n".join(text.splitlines()[:30]))
        base = md.parent / declared.group(1) if declared else md.parent
        for m in REL_PATH.finditer(text):
            target = m.group(1) or m.group(2)
            if any(c in target for c in "*{<"):
                continue
            target = re.sub(r"(#.*|:\d.*)$", "", target)
            if not (base / target).exists():
                out.append(f"{md.name}: broken {target}")
    return sorted(set(out))


def main(argv):
    links = "--links" in argv
    argv = [a for a in argv if a != "--links"]
    root = Path(os.environ.get("CLAUDE_PROJECT_DIR") or os.getcwd())
    if argv:
        folders = [Path(a) for a in argv]
        absent = [f for f in folders if not (f / "CONTEXT.md").is_file()]
        if absent:
            for f in absent:
                print(f"{f}: no CONTEXT.md")
            return 2
    else:
        folders = indexed_folders(root)
    failing = 0
    broken = 0
    for folder in folders:
        try:
            label = folder.resolve().relative_to(root.resolve()).as_posix() or "."
        except ValueError:
            label = str(folder)
        missing = unnamed(folder)
        if missing:
            failing += 1
            print(f"{label}: unnamed {', '.join(missing)}")
        if links:
            for line in broken_links(folder):
                broken += 1
                print(f"{label}/{line}")
    print(f"{len(folders) - failing} of {len(folders)} indexes name everything")
    if links:
        print(f"{broken} broken relative paths")
    return 1 if failing or broken else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
