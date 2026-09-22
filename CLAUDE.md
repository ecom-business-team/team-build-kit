# Team Build Kit — Setup

When the user says **"get started"** (or anything indicating they want to install), follow these five steps in order. This folder is the kit: it installs the commands, creates the user's workspace **beside itself**, and then stays in place. **Do NOT delete anything after install.**

## Step 1: Install the skills from this folder

Run this from the kit's root (the folder holding `MANIFEST` and `install.sh`):

```bash
TBK_BASE="file://$PWD" bash install.sh
```

Tell the user first: *"I'm installing the Team Build Kit's commands into your Claude Code — every skill its MANIFEST lists. I need your permission once to copy the files."*

## Step 2: Verify the install

Confirm the command printed ✅ with its file count and the list of commands. The lifecycle commands depend on `~/.claude/skills/_shared/documentation_standard.md`; if the command printed ❌, nothing was installed — re-run Step 1 before continuing.

## Step 3: Run the interview (do NOT skip)

**Read `.skills/onboard/SKILL.md` in this folder and follow it.** Reading the file directly means the interview runs now, in this session, whether or not Claude Code has noticed the new commands yet. The interview asks the user about their work in plain words, creates their workspace as a new folder **beside this one** (for example `~/Desktop/maria-workspace` next to `~/Desktop/team-build-kit`), installs the kit's workspace files into it from this folder, and writes their map (`CLAUDE.md`) and skills list (`SKILLS.md`).

## Step 4: Orient the user

After the interview's handoff card, say:

> "Three things to read before you build anything, all in your new workspace: **why_we_build.html** — why we build this way, in plain words; **lifecycle_map.html** — every door, the three gates and the loop on one page; and **worked_example.html** — one small build followed through every gate. The one idea: complexity is the enemy. If you can't explain it simply, it's probably too complicated.
>
> There are two doors. `/new-workspace` is for something new; `/convert-to-standard` is for something you already have. Both end with a card that says what to type next.
>
> The first time you open your workspace folder in Claude Code it asks once whether to trust the folder's hooks. Say yes — they are the kit's, and they only write notes inside that folder."

## Step 5: Leave this folder as it is

This folder is the factory. `.skills/` and `workspace/` are the files it installs from; `README.md` and this file are its front door. Saying `get started` again here makes another workspace. Updates run from inside a workspace with `/update-build-kit`, never from here.

---

## If the user asks questions before installing

- **"What is this?"** — "A set of commands that walk you through building real tools properly — think it through, design it, make it safe to rely on — plus the standards they read and a workspace to work in. It takes about ten minutes, most of it a conversation about your work. Type 'get started' when ready."
- **"Is this safe?"** — "It copies skill files into your Claude Code settings (`~/.claude/skills/`) and creates one new folder for your workspace beside this one, with some standards, notes and five small hooks inside it. No system changes, no hidden installs, nothing hosted. It never touches work that is already yours."
- **"Do I need to know how to code?"** — "No. Everything is plain English. The commands do the technical part; you describe what you want."
- **"Can I make more than one workspace?"** — "Yes. Say 'get started' here again, or type `/onboard` anywhere, and it creates another folder beside this one."

## Notes

- Keep the tone warm and plain. Don't explain context windows, projections, or architecture during setup.
- The skills are stack-agnostic — they read whatever tools the user's workspace declares, so they work for any kind of build.
