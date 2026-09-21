# Team Build Kit

**Build real, reliable tools in Claude Code — without needing to be an engineer.**

This kit gives you a simple, repeatable way to go from *"I have an idea"* to *"I shipped something I trust."* It installs a set of skills (commands you type in Claude Code) that walk you through three gates — **think it through → design it → make it safe to rely on** — so you don't end up deep in a half-built mess wondering if it'll hold up.

You don't need to know how any of it works under the hood. The skills carry the technical load; your job is to communicate clearly what you're trying to do.

---

## Quick install (already using Claude Code?)

You don't need to download anything. Paste this one line into Claude Code (or a terminal) — it installs the commands straight into Claude Code:

```
curl -fsSL https://raw.githubusercontent.com/zjamesblake/team-build-kit/main/install.sh | bash
```

Then type **`/new-workspace`** to begin. To update later, run **`/update-build-kit`**.

---

## Full setup (5 minutes — for first-time Claude Code users)

1. **Download this folder** — click `Code ▸ Download ZIP` above, unzip it, and put it somewhere sensible (your Desktop is fine).
2. **Open it in VS Code** — `File ▸ Open Folder`, pick this folder.
3. **Open the Claude Code panel** and type **`get started`**.

Claude will copy the skills into your Claude Code setup (it asks permission once) and confirm when they're ready. That's it — the commands below now work in **every** Claude Code session.

> Unlike a one-time setup, this kit **stays installed and stays current.** When the kit improves, run **`/update-build-kit`** to pull the latest.

---

## What you get

Type these in any Claude Code session:

| Command | When you use it | The gate |
|---------|-----------------|----------|
| **`/new-workspace`** | First — sets up a tidy home for your work so everything stays organized | (foundation) |
| **`/memo`** | You have an idea worth building | **Gate 1 — should this exist?** |
| **`/prd`** | The idea is worth it — now design it properly | **Gate 2 — is it designed right?** |
| **`/build`** | The design is solid — make it | (execution) |
| **`/ship`** | It works — but others will rely on it / it touches money or real data | **Gate 3 — is it safe to rely on?** |
| **`/quick-fix`** | Something small broke, or a tiny tweak — no ceremony needed | (below the gates) |

**Just experimenting?** Don't run anything. Play freely. The gates are for when you decide to build something real.

---

## Start here

1. **Open [`flow.html`](flow.html)** in your browser — it walks one complete example build (a simple expense tracker) through every gate, so you can see *why* each step exists before you do it yourself.
2. **Read [`HOW_WE_BUILD.md`](HOW_WE_BUILD.md)** — the short "why" behind the whole approach. The one idea to take away: **complexity is the enemy. If you can't explain it simply, it's probably too complicated.**

Then run `/new-workspace` and start building.

---

## Keeping it current

```
/update-build-kit
```

Pulls the latest version of the kit and re-installs the skills. Run it whenever you hear there's an update — your own work is never touched. What the kit ships is listed in `MANIFEST`; `workspace/` holds files a later version installs into your workspace.

---

*Built by Zachary Blake. The skills are a simplified projection of the same development lifecycle used to run production systems — stripped of any specific tools so they work whatever you build on.*
