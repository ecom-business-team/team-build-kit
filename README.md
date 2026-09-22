# Team Build Kit

**Build real, reliable tools in Claude Code — without needing to be an engineer.**

## What this is

A way of building you can hold in one breath: six kinds of thing you might build, three gates a build passes through (think it through → design it → make it safe to rely on), and one state layer that says where every piece of work sits. The kit is files and skills: commands you type in Claude Code, the standards they read, and four small hooks that keep notes about your sessions. Nothing is hosted; it all lives on your machine.

---

## Quick install (already using Claude Code)

Paste this line into a terminal or into Claude Code. It installs the commands and changes nothing else:

```
K=https://raw.githubusercontent.com/zjamesblake/team-build-kit; curl -fsSL $K/main/install.sh | bash
```

Then type **`/onboard`** to create your workspace.

---

## Full setup (first time)

1. **Download this folder** — click `Code ▸ Download ZIP` above, unzip it, and put it on your Desktop.
2. **Open it in VS Code** — `File ▸ Open Folder`, pick this folder.
3. **Open the Claude Code panel** and type **`get started`**.

Claude installs the commands (it asks permission once), interviews you about your work, and creates your workspace **beside this folder**. This folder is the kit; your workspace is its own folder next to it. Run `get started` again for another workspace.

---

## What you get

| Command | What it does |
|---|---|
| **Doors** | |
| `/onboard` | Interviews you about your work, creates your workspace beside the kit, and writes your map and skills list. |
| `/new-workspace` | Sets up a tidy, documented home for something new you are about to build. |
| `/convert-to-standard` | Looks at something you already have, names what it is, writes the documents it is missing, and hands it into the lifecycle. |
| **Gates** | |
| `/memo` | Gate 1: says why this is worth building and what done looks like, before any design or code. |
| `/prd` | Gate 2: designs the change and checks every dependency live, so the build runs in one go. |
| `/build` | Carries out an approved design, one work item per session, with a handoff card at every stop. |
| `/ship` | Gate 3: the review a build passes before other people, real data or money depend on it. |
| `/quick-fix` | Fixes something small without the ceremony, and still asks the Gate 3 questions at the end. |
| **Every session** | |
| `/session-close` | Writes the session's log entry and checks the living documents match what changed. |
| `/day` | Turns a day's session logs into one digest and files the loose threads. |
| `/week` | Reviews the week's digests and names the one thing that kept getting in the way. |
| `/doc-audit` | Checks every living document against what actually exists and lists the defects to fix, for one area or the whole workspace. |
| **Your own skills** | |
| `/new-workflow` | Turns a process you keep repeating into a skill of your own, and adds it to your skills list. |
| **The kit** | |
| `/update-build-kit` | Pulls the latest kit and refreshes its files; run it from inside your workspace. |

**Just experimenting?** Play freely. The gates are for building something real.

---

## Two doors

**New work** goes through `/new-workspace`. You describe the thing in plain words; it decides what kind of thing it is and which documents it needs, creates exactly those, and ends with a card saying what to type next.

**Existing work** goes through `/convert-to-standard`. Point it at a folder or a system that already runs. It observes what is actually there, writes only what it can trace to something it saw or you confirmed, and ends with the same card. Both doors lead to the same place: a documented thing the gates can operate on.

---

## Start here

1. **Read [`why_we_build.md`](workspace/why_we_build.md)** — why we build this way, in plain words. Downloaded the kit? Open `workspace/why_we_build.html` for the same document with its diagrams drawn.
2. **Then read [`worked_example.md`](workspace/worked_example.md)** — one small build followed through every gate (`workspace/worked_example.html` for the drawn version).

The one idea: **complexity is the enemy. If you can't explain it simply, it's probably too complicated.**

---

## What lands where

- **Your Claude Code's skills folder** gets the commands above; the quick install touches nothing else.
- **Your workspace** (created by `/onboard`) gets the kit-owned files: the three standards, the glossary, the explainer and worked example, the practice notes, and five small hooks with their registration. These refresh when you update the kit. A small receipt in `.claude/` records what the kit placed, so an update can tell its own files from your edits: a file you changed is kept, and the kit's new version is put beside it as `.kit-new` with a note. The same holds for the commands in your skills folder.
- **Your own rules for a kit command** go in `.claude/skills.d/<command>.md` in your workspace (for example `.claude/skills.d/prd.md`). Claude reads that file whenever you run the command; the kit never writes there, so your rules survive every update.
- **Your map (`CLAUDE.md`), your skills list and every folder you make are yours.** The kit never touches them after the interview.
- **One question, once.** The first time Claude Code opens your workspace it asks whether to trust the folder's hooks. Say yes; they are the kit's and only write notes inside that folder.

---

## Keeping it current

Run `/update-build-kit` from inside your workspace. It pulls the latest kit, refreshes the commands and the kit-owned files there, and touches nothing of yours.

Looking for `HOW_WE_BUILD.md` or `flow.html`? Those June files were replaced by `workspace/why_we_build.md`, which carries the same why.

---

*Built by Zachary Blake. The skills are a simplified projection of the lifecycle that runs production systems, stripped of specific tools so they work whatever you build on.*
