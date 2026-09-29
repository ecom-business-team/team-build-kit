# Team Build Kit

**Build real, reliable tools in Claude Code — without needing to be an engineer.**

## What this is

A way of building you can hold in one breath: six kinds of thing you might build, each defined in one sentence in `workspace/glossary.md`. An automation is tools you pay for, wired together. A service is your own code running on its own, with no screen. An application is your own code with screens people sign into. A tool is code a person runs by hand to get an output. A procedure is written steps Claude follows. Knowledge is something people read. On top of the six kinds there are three checkpoints a build passes through (think it through → design it → make it safe to rely on), and one short note, the state file, that says where every piece of work sits. Together these steps are the kit's lifecycle, the path every build follows from an idea to something finished and checked. The kit is files and skills. A skill is a command you type in Claude Code, such as `/memo`, whose written instructions Claude follows. The standards are three documents the commands read, which say how documents are laid out, how processes are designed and how quality is proved on code. The kit also has five small hooks. A hook is a small script Claude Code runs by itself at set moments, such as the start or the end of a session, and these five keep notes about your sessions, where a session is one conversation with Claude, from opening the chat to closing it. Nothing is hosted; it all lives on your machine.

---

## How to install

### The one thing to understand first

The kit comes in two halves, and they land in different places.

- **The commands** (`/memo`, `/prd`, `/build` and the rest) go into Claude Code itself. `/prd` is named after the PRD, the product requirements document, which is the written design that answers Checkpoint 2. They work in any folder you open.
- **The background parts** go into one folder of yours, called your **workspace**. These are the session notes, the daily check that tells you when a newer kit is out, the small tools the commands call (for example, the one that measures how full your conversation is, meaning how much Claude is holding in mind, so you know whether to carry on or start a fresh conversation), and the standards the commands read. They only run when Claude Code is opened **in that workspace folder**.

You get the most out of the kit when you have both halves and you do your work inside your workspace. With the commands alone, the commands still run, but nothing keeps notes, nothing tells you about updates, and the commands cannot find the tools and standards they expect.

### Pick the route that fits you

**Route 1: you are new to the kit (recommended).** This gives you both halves and a workspace in one go.

1. **Download this folder.** On the kit's GitHub page, click `Code ▸ Download ZIP`, unzip it, and put it on your Desktop.
2. **Open it in VS Code.** Use `File ▸ Open Folder` and pick this folder.
3. **Open the Claude Code panel** and type **`get started`**.

Claude installs the commands (it asks your permission once), interviews you about your work, and creates your workspace as a new folder **beside this one**, with the background parts already in it. This folder is the kit, and your workspace is its own folder next to it. Say `get started` again whenever you want another workspace.

**Route 2: you already use Claude Code and want a fresh workspace.** Paste this line into a terminal or into Claude Code. It installs the commands and nothing else:

```
K=https://raw.githubusercontent.com/ecom-business-team/team-build-kit; curl -fsSL $K/main/install.sh | bash
```

Then type **`/onboard`** in Claude Code. It interviews you and creates your workspace with the background parts in it. **Do not stop after the first line:** without `/onboard` you have the commands only.

**Route 3: you already have a folder you work in.** Run this line, with that folder's full path in place of `<your folder>`. It installs the commands and puts the background parts into your folder, beside your own files. It never changes your own files or your `CLAUDE.md`, the file that tells every Claude Code session where things live in that folder (the kit calls it your map):

```
K=https://raw.githubusercontent.com/ecom-business-team/team-build-kit; curl -fsSL $K/main/install.sh | TBK_WORKSPACE="<your folder>" bash
```

Then open that folder in Claude Code and type **`/convert-to-standard`**. It looks at what is already there and writes the documents the folder is missing, so the commands have something to stand on.

### After installing, whichever route you took

- **Always open Claude Code in your workspace folder** when you work. If you open it anywhere else, you have the commands but none of the background parts.
- **Say yes to the trust question.** The first time Claude Code opens your workspace, it asks once whether to trust the folder's hooks. Say yes: they are the kit's, and they only write notes inside that folder.
- **To check you are in a workspace,** look for a file called `.claude/kit_receipt` inside the folder. If it is there, the background parts are installed. If it is not, take Route 2 or Route 3 for that folder.

---

## What you get

| Command | What it does |
|---|---|
| **First run** | |
| `/onboard` | Interviews you about your work, creates your workspace beside the kit, and writes your map (your `CLAUDE.md`) and your skills list (`SKILLS.md`, the list of the commands your workspace has). |
| **Ways to start** | |
| `/new-workspace` | Sets up a tidy, documented home for something new you are about to build. |
| `/convert-to-standard` | Looks at something you already have, names what it is, writes the documents it is missing, and hands it into the lifecycle. |
| **Checkpoints** | |
| `/memo` | Checkpoint 1: says why this is worth building and what done looks like, before any design or code. |
| `/prd` | Checkpoint 2: writes the PRD, the design of the change. It checks every dependency, meaning anything the design relies on such as another system, a file or an account, against the real running systems rather than against documents, so the build runs in one go. |
| `/build` | Carries out an approved design one work item at a time. A work item is one bounded piece of the design that promises one output. At every stop it prints a handoff card, a short summary of where the work stands and exactly what to type next, and the card's Context line measures how full the conversation is and says whether to carry on or start a fresh conversation. |
| `/ship` | Checkpoint 3: the review a build passes before other people, real data or money depend on it. |
| `/quick-fix` | Fixes something small without the ceremony, and still asks the Checkpoint 3 questions at the end. |
| **Every session** | |
| `/session-close` | Writes the session's log entry and checks that the living documents, the ones kept true at the moment something changes, match what changed. |
| `/day` | Turns a day's session logs into one digest, a short paragraph that sums up the day, and files the loose threads in your task manager, the one app or file where every task and open question lives. |
| `/week` | Reviews the week's digests and names the one thing that kept getting in the way. |
| `/doc-audit` | Checks every living document against what actually exists and lists the defects to fix, for one area or the whole workspace. |
| **Your own skills** | |
| `/new-workflow` | Turns a process you keep repeating into a skill of your own, or, when a person checks the work after each stage, into a set of folders with one folder per stage, so each stage's output waits in its folder for that check, and adds it to your skills list. |
| **The kit** | |
| `/update-build-kit` | Pulls the latest kit and refreshes its files; run it from inside your workspace. |

**Just experimenting?** Play freely. The checkpoints are for building something real.

---

## Two ways to start

There are two ways to start: build something new with `/new-workspace`, or bring something that already exists up to standard with `/convert-to-standard`.

**New work** goes through `/new-workspace`. You describe the thing in plain words; it decides what kind of thing it is and which documents it needs, creates exactly those, and ends with a card saying what to type next.

**Existing work** goes through `/convert-to-standard`. Point it at a folder or a system that already runs. It observes what is actually there, writes only what it can trace to something it saw or you confirmed, and ends with the same card. Both ways to start lead to the same place: a documented thing the checkpoints can operate on.

---

## Start here

1. **Read [`why_we_build.md`](workspace/why_we_build.md)** — why we build this way, in plain words. Downloaded the kit? Open `workspace/why_we_build.html` for the same document with its diagrams drawn.
2. **Then [`lifecycle_map.md`](workspace/lifecycle_map.md)** — every way to start, the three checkpoints and the loop on one page, where the loop is the path every build follows, which closes only when a final outcome check confirms the problem is really gone; open `workspace/lifecycle_map.html` for the picture drawn.
3. **Then read [`worked_example.md`](workspace/worked_example.md)** — one small build followed through every checkpoint (`workspace/worked_example.html` for the drawn version).

The one idea: **complexity is the enemy. If you can't explain it simply, it's probably too complicated.**

---

## Your day with the kit

Three habits keep your workspace true, and the kit asks for them:

- **At the end of each session**, type `/session-close`. It writes one line in today's log and checks that the documents match what changed.
- **At the end of the day, or the next morning**, type `/day`. In about five minutes it turns the day's lines into a short digest and files the loose ends in your task manager.
- **Once a week**, type `/week`. In about twenty minutes it looks back over the week and names the one thing that kept getting in the way.

From the day after your first session, Claude mentions it when a day or a week has not been reviewed. It only mentions it; nothing runs until you type the command.

---

## What lands where

- **Your Claude Code's skills folder** gets the commands above; Route 2's one-line install touches nothing else.
- **Your workspace** (created by `/onboard`, or an existing folder named with `TBK_WORKSPACE`) gets the kit-owned files: the three standards, the glossary, the explainer (`why_we_build`, the page that says why the kit works this way) and worked example, the practice notes (short notes on how each tool behaves, in `_practices/`), and the five small hooks together with the settings file that tells Claude Code when to run them. These refresh when you update the kit. A small receipt in `.claude/` records what the kit placed, so an update can tell its own files from your edits: a file you changed is kept, and the kit's new version is put beside it as `.kit-new` with a note. The same holds for the commands in your skills folder.
- **Your own rules for a kit command** go in `.claude/skills.d/<command>.md` in your workspace (for example `.claude/skills.d/prd.md`). Claude reads that file whenever you run the command; the kit never writes there, so your rules survive every update.
- **Your map (`CLAUDE.md`), your skills list and every folder you make are yours.** The kit never touches them after the interview.
- **One question, once.** The first time Claude Code opens your workspace it asks whether to trust the folder's hooks. Say yes; they are the kit's and only write notes inside that folder.

---

## Keeping it current

Run `/update-build-kit` from inside your workspace. It pulls the latest kit, refreshes the commands and the kit-owned files there, and touches nothing of yours. Once a day, at the start of a session in your workspace, Claude checks whether a newer kit has been published and tells you in one line; it never updates on its own.

Looking for `HOW_WE_BUILD.md` or `flow.html`? Those June files were replaced by `workspace/why_we_build.md`, which carries the same why.

---

*Built by Zachary Blake. The skills are a simpler version of the lifecycle the author uses to run systems that a business depends on every day, with the author's own tools taken out so they work whatever you build on.*
