---
name: update-build-kit
description: Pull the latest version of the Team Build Kit and re-install it. Use when there's a new version of the kit, or to make sure your lifecycle skills (new-workspace, memo, prd, build, ship, quick-fix) and the shared Documentation Standard are current. Run from your workspace root and the kit-owned files in the workspace (hooks, tools, standards, practices) are refreshed too. Never touches your CLAUDE.md, SKILLS.md, or your own folders.
---

# /update-build-kit

Refresh the Team Build Kit to its latest published version. This runs the kit's own installer from GitHub: it re-downloads every file the kit's `MANIFEST` lists and re-installs the skills into `~/.claude/skills/`. Run from the root of a workspace the kit provisioned, and the kit-owned files inside that workspace are refreshed as well. **It only touches the kit's own files — never your CLAUDE.md, your SKILLS.md, or the folders you made.**

## When to Use

- You heard there's a new version of the kit.
- You want to confirm your lifecycle skills and the kit-owned workspace files are current.

## When NOT to Use

- To change your own project files (that's `/quick-fix` or the lifecycle skills).

---

## How it works

The kit lives at a public GitHub repo. This skill runs the kit's `install.sh` straight from there, so it works whether the user cloned the repo or just downloaded the ZIP. One script is the source of truth for what gets installed and where; this skill only decides whether to tell it about a workspace.

**Repo:** `https://github.com/zjamesblake/team-build-kit`
**Raw base:** `https://raw.githubusercontent.com/zjamesblake/team-build-kit/main` — `TBK_BASE` overrides it (a local clone: `TBK_BASE="file://$PWD"`).
**What ships:** every `.skills/` line in the kit's `MANIFEST` goes to `~/.claude/skills/`; every `workspace/` line goes to the workspace, when one is named. The installer installs exactly those and nothing else.

### Step 1: Run the installer from GitHub

**Run this from the workspace root.** Tell the user: *"Pulling the latest Team Build Kit and re-installing it — this won't touch any of your own work."* Then run:

```bash
W=""; [ -f "$PWD/.claude/kit_receipt" ] && [ ! -f "$PWD/MANIFEST" ] && W="$PWD"
curl -fsSL "${TBK_BASE:-https://raw.githubusercontent.com/zjamesblake/team-build-kit/main}/install.sh" | TBK_WORKSPACE="$W" bash
```

The rule the first line applies: the current folder is treated as a kit-provisioned workspace when the installer's receipt is present in it (`.claude/kit_receipt`, written when the kit's files were placed there) and it is not the kit folder itself. A folder that merely holds kit-looking files, with no receipt, is left alone. In that case the installer refreshes the kit-owned files in the workspace too — by the package-manager rule: a file whose bytes still match the receipt is refreshed; a file the person changed is **kept**, and the kit's new version is written beside it as `<file>.kit-new`. Those files are every `workspace/` line of the `MANIFEST` — the one list, read it for what ships today rather than trusting any sentence here — plus `.claude/settings.json`, which is **merged** (the kit's hook registrations are added if missing; the person's own hooks and permissions are kept). `CLAUDE.md`, `SKILLS.md`, and every folder the person made are never read or written.

When the folder is not a kit-provisioned workspace, only the skills are refreshed — today's behaviour for anyone who has never created a workspace.

> If the user also has the repo cloned locally and prefers git: `cd` into it, `git pull`, then run `TBK_BASE="file://$PWD" bash install.sh` from the clone (with `TBK_WORKSPACE=<their workspace folder>` to refresh the workspace too). The curl path above is the default because it needs no clone.

### Step 2: Verify

The installer prints the count of files it wrote, a `Skills:` line (placed · refreshed · already current · kept) and, when a workspace was named, a `Workspace files:` line with the same counts. The first update after v2026.9.21-4 also prints "First run under the receipt rule": the kit skills were refreshed as every update did before, and from then on a changed kit skill is kept. The four core lifecycle skills (`prd`, `build`, `ship`, `new-workspace`) depend on `~/.claude/skills/_shared/documentation_standard.md` — make sure it's present. If the installer printed a ❌ line (no network, repo moved, a refused folder), say so plainly and stop: it changes nothing on failure, so the existing kit is intact. If it printed a ⚠️ line, the files did install; the line says which of two things happened. A `settings.json` that could not be merged: the kit's hooks are not registered there, so show the person the line (the file is theirs to fix), then run the update again. A kit-owned file they had changed: it was kept, and the kit's new version sits beside it as `<file>.kit-new`. Show them the line and offer the choice in plain words: take the kit's version (`mv <file>.kit-new <file>`), or keep theirs and delete the `.kit-new` — in which case the line returns at every update, so their own rules are better kept where the kit reads them and never writes: `.claude/skills.d/<command>.md` in their workspace for a command, a file of their own indexed from their map for a note.

### Step 3: Confirm

Tell the user: *"Done — your Team Build Kit is current. Nothing of your own was touched."* Name the workspace folder if one was refreshed.

---

## Principles

- **Only the kit's files change.** Skills in `~/.claude/skills/`, and the kit-owned files in a kit-provisioned workspace. Never the person's CLAUDE.md, SKILLS.md, projects, docs, or data.
- **All-or-nothing.** The installer downloads everything first and writes nothing unless every file arrived — a half-updated kit is worse than a stale one.
- **One script.** This skill runs `install.sh`; it does not carry a copy of it, so the two can never disagree.
- **The source of truth is GitHub.** This skill pulls; it never edits the kit's contents locally.
