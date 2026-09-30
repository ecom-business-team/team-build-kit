---
name: update-build-kit
description: Pull the latest version of the Team Build Kit and re-install it. Use when there's a new version of the kit, or to make sure your lifecycle skills (new-workspace, memo, prd, build, ship, quick-fix) and the shared Documentation Standard are current. Run from your workspace root and the kit-owned files in the workspace (hooks, tools, standards, practices) are refreshed too. Never changes your CLAUDE.md without your approval, and never touches SKILLS.md or your own folders.
---

# /update-build-kit

Refresh the Team Build Kit to its latest published version. This runs the kit's own installer from GitHub: it re-downloads every file the kit's `MANIFEST` lists and re-installs the skills into `~/.claude/skills/`. Run from the root of a workspace the kit provisioned, and the kit-owned files inside that workspace are refreshed as well. **It only changes the kit's own files. Your CLAUDE.md changes only in the sections you approve; your SKILLS.md and the folders you made are never touched.**

## When to Use

- You heard there's a new version of the kit.
- You want to confirm your lifecycle skills and the kit-owned workspace files are current.

## When NOT to Use

- To change your own project files (that's `/quick-fix` or the lifecycle skills).

---

## How it works

The kit lives at a public GitHub repo. This skill runs the kit's `install.sh` straight from there, so it works whether the user cloned the repo or just downloaded the ZIP. One script is the source of truth for what gets installed and where; this skill only decides whether to tell it about a workspace.

**Repo:** `https://github.com/ecom-business-team/team-build-kit`
**Raw base:** `https://raw.githubusercontent.com/ecom-business-team/team-build-kit/main` — `TBK_BASE` overrides it (a local clone: `TBK_BASE="file://$PWD"`).
**What ships:** every `.skills/` line in the kit's `MANIFEST` goes to `~/.claude/skills/`; every `workspace/` line goes to the workspace, when one is named. The installer installs exactly those and nothing else.

### Step 1: Run the installer from GitHub

**Run this from the workspace root.** Tell the user: *"Pulling the latest Team Build Kit and re-installing it — this won't change any of your own work without asking."* Then run:

```bash
W=""; [ -f "$PWD/.claude/kit_receipt" ] && [ ! -f "$PWD/MANIFEST" ] && W="$PWD"
curl -fsSL "${TBK_BASE:-https://raw.githubusercontent.com/ecom-business-team/team-build-kit/main}/install.sh" | TBK_WORKSPACE="$W" bash
```

The rule the first line applies: the current folder is treated as a kit-provisioned workspace when the installer's receipt is present in it (`.claude/kit_receipt`, written when the kit's files were placed there) and it is not the kit folder itself. A folder that merely holds kit-looking files, with no receipt, is left alone. In that case the installer refreshes the kit-owned files in the workspace too — by the package-manager rule: a file whose bytes still match the receipt is refreshed; a file the person changed is **kept**, and the kit's new version is written beside it as `<file>.kit-new`. Those files are every `workspace/` line of the `MANIFEST` — the one list, read it for what ships today rather than trusting any sentence here — plus `.claude/settings.json`, which is **merged** (the kit's hook registrations are added if missing; the person's own hooks and permissions are kept). `CLAUDE.md`, `SKILLS.md`, and every folder the person made are never read or written by the installer.

When the folder is not a kit-provisioned workspace, only the skills are refreshed — today's behaviour for anyone who has never created a workspace.

> If the user also has the repo cloned locally and prefers git: `cd` into it, `git pull`, then run `TBK_BASE="file://$PWD" bash install.sh` from the clone (with `TBK_WORKSPACE=<their workspace folder>` to refresh the workspace too). The curl path above is the default because it needs no clone.

### Step 2: Verify

The installer prints the count of files it wrote, a `Skills:` line (placed · refreshed · already current · kept) and, when a workspace was named, a `Workspace files:` line with the same counts. The first update after v2026.9.21-4 also prints "First run under the receipt rule": the kit skills were refreshed as every update did before, and from then on a changed kit skill is kept. The four core lifecycle skills (`prd`, `build`, `ship`, `new-workspace`) depend on `~/.claude/skills/_shared/documentation_standard.md` — make sure it's present. If the installer printed a ❌ line (no network, repo moved, a refused folder), say so plainly and stop: it changes nothing on failure, so the existing kit is intact. If it printed a ⚠️ line, the files did install; the line says which of two things happened. A `settings.json` that could not be merged: the kit's hooks are not registered there, so show the person the line (the file is theirs to fix), then run the update again. A kit-owned file they had changed: it was kept, and the kit's new version sits beside it as `<file>.kit-new`. Show them the line and offer the choice in plain words: take the kit's version (`mv <file>.kit-new <file>`), or keep theirs and delete the `.kit-new` — in which case the line returns at every update, so their own rules are better kept where the kit reads them and never writes: `.claude/skills.d/<command>.md` in their workspace for a command, a file of their own indexed from their map for a note.

### Step 3: Offer the kit's lines to your map

Run this step only when `$W` is set, the installer printed no ❌, and `$W/CLAUDE.md` exists; otherwise skip it silently. This step compares the map with the kit's CLAUDE.md template, which the installer has just refreshed, and writes nothing the person does not take. Run:

```bash
python3 ~/.claude/skills/_shared/map_update.py plan "$W/CLAUDE.md"
```

- **Exit 0:** the map already carries the kit's current lines. Say nothing and go to Step 4.
- **Exit 3:** say *"Your map (CLAUDE.md) is behind the kit's rules in N sections. Nothing changes unless you take it. Lines you wrote yourself are never changed; to keep your own wording of a kit rule, add your line beside the kit's rather than editing it."*, with N the number of sections the output lists (each starts with `## `; `## (top of the file)` counts). Then show the output exactly as printed, except the last line (`fingerprint: …`), and ask once: *"Take all N, name the ones to take, or none?"* If the output has a `~ your line:` entry, add: *"A line marked 'your line' is the kit's own older wording as it stands in your map; lines you wrote yourself are never listed."*
  - If the output has a `Values to ask for before these can be written:` line, ask after the person has said which sections to take, and only what those sections need: run the apply below first, and when it refuses with `Missing values: …` (it writes nothing then), ask for exactly the values it names, except `path, once you have one`, which is never asked (below), and run it again with them. Ask each as `/onboard`'s question (the question only: the connected-tool check and every proof step are not run here) (`~/.claude/skills/onboard/SKILL.md`, questions 4–6: the name, the task manager and its three labels, where shared credentials live). `path, once you have one` is not asked: pass it as `--slot 'path, once you have one=~/.claude/skills/_shared/flow_base.html'`, as `/onboard` writes it. Each value is written into the kit's line exactly where its slot stands, so give the words that fit there; the credentials value is a whole clause with no closing full stop (the kit's line adds one): the person's own words when their map states it, otherwise their answer. When the map already states a value in the person's own words (their own line about where credentials live, for example), offer that wording as the answer and ask only to confirm.
  - **On take:** run `python3 ~/.claude/skills/_shared/map_update.py apply "$W/CLAUDE.md" --expect <the fingerprint> --take "<heading>"`, with one `--take` per section taken (the heading exactly as shown after `## `, without the `: not in your map …` tail; the text above the first heading is `(top of the file)`) and one `--slot '<name>=<value>'` per value asked (single quotes: a name can hold backticks), with the names exactly as the `Values to ask for` line lists them, separated there by `; `. Show the lines it prints. The last, `To undo: cp …`, puts the map back exactly as it was before the write, for as long as the computer keeps its temporary files (a few days); say so, and that after that `git -C "$W" checkout -- CLAUDE.md` returns the map to its last commit. Then name any line of theirs that now says the same as a kit line (a value they already stated, or their own rewording of a kit rule, such as a second item 3), and say removing theirs is their choice.
  - **On none:** write nothing, and say the sections are offered again at the next update.
- **Any other exit, or no `python3`, or no `map_update.py`:** show the message and say *"Your map was left as it was; the kit itself is updated."* Then go to Step 4.

### Step 4: Confirm

Tell the user: *"Done — your Team Build Kit is current."* Name the workspace folder if one was refreshed, and the map sections written in Step 3, if any.

---

## Principles

- **Only the kit's files change.** Skills in `~/.claude/skills/`, and the kit-owned files in a kit-provisioned workspace. Never the person's SKILLS.md, projects, docs, or data; their CLAUDE.md only in sections they approve (Step 3).
- **All-or-nothing.** The installer downloads everything first and writes nothing unless every file arrived — a half-updated kit is worse than a stale one.
- **One script.** This skill runs `install.sh`; it does not carry a copy of it, so the two can never disagree.
- **The source of truth is GitHub.** This skill pulls; it never edits the kit's contents locally.
