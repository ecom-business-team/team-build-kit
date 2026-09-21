# Team Build Kit — Setup

When the user says **"get started"** (or anything indicating they want to install), follow these instructions. This kit is **persistent** — it installs skills and then *stays in place* so the user can pull updates later. **Do NOT delete anything after install.**

## Step 1: Install the skills

Install every `.skills/` file the kit's `MANIFEST` lists into the user's global skills directory, taking them from this folder. Run this from the repo root:

```bash
TBK_BASE="file://$PWD" bash install.sh
```

Tell the user first: *"I'm installing the Team Build Kit's skills into your Claude Code — every file its MANIFEST lists. I just need your permission once to copy the files."*

## Step 2: Verify the install (smoke test)

Confirm the command printed ✅ with its file count. The four core lifecycle skills (`prd`, `build`, `ship`, `new-workspace`) **depend on** `~/.claude/skills/_shared/documentation_standard.md` — if it's missing, they break. If the command printed ❌, nothing was installed; re-run Step 1 before continuing.

## Step 3: Orient the user (do NOT skip)

Say:

> "Done — you now have `/new-workspace`, `/memo`, `/prd`, `/build`, `/ship`, `/quick-fix`, and `/update-build-kit` in every Claude Code session.
>
> One thing before you build anything: read **workspace/why_we_build.md** — why we build this way, in plain words (open **workspace/why_we_build.html** in your browser to see it with its diagrams). The one idea: complexity is the enemy. If you can't explain it simply, it's probably too complicated.
>
> When you're ready, run `/new-workspace` to set up a home for your work."

## Step 4: Do NOT clean up

This is a living kit. Leave `.skills/`, `workspace/`, `README.md`, and this file in place. They are how `/update-build-kit` re-installs the latest version. The repo folder is the kit, not a throwaway scaffold.

---

## If the user asks questions before installing

- **"What is this?"** — "A set of commands that walk you through building real tools properly — think it through, design it, make it safe. It takes 5 minutes to install. Type 'get started' when ready."
- **"Is this safe?"** — "It copies some skill files into your Claude Code settings (`~/.claude/skills/`). No system changes, no hidden installs. It never touches your own work."
- **"Do I need to know how to code?"** — "No. Everything is plain English. The skills do the technical part; you describe what you want."

## Notes

- Keep the tone warm and plain. Don't explain context windows, projections, or architecture during setup.
- The skills are stack-agnostic — they read whatever tools the user's workspace declares, so they work for any kind of build.
