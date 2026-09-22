---
name: onboard
description: First-run interview. Asks about your work in plain words, creates your workspace beside the kit with the kit's standards, hooks and practices in it, and writes your map (CLAUDE.md) and skills list. Run once per workspace; run again for another.
---

# /onboard

Set up your workspace from scratch. This skill asks you about your work, figures out how to organize it, creates a folder for it beside the kit with the kit's files inside, and writes the map that makes Claude Code effective for you.

## Usage

```
/onboard
```

Run it once when you first start using Claude Code. It takes about 5 minutes. Run it again, later, to create another workspace for a different body of work.

---

## Process

### Phase 1: WELCOME

Start with a brief, warm introduction. 2-3 sentences. No jargon.

Say something like:

> I'm going to ask you about your work so I can set up a workspace that makes you faster. This takes about 5 minutes. I'll ask some questions, show you what I'd create, and build it once you approve.

Do not explain the architecture. Do not mention CLAUDE.md or CONTEXT.md yet. The user doesn't need to know the internals. They just need to answer questions about their work.

---

### Phase 2: UNDERSTAND THE PERSON

Ask these questions conversationally. Follow the natural flow. If one answer covers multiple questions, don't re-ask.

**1. "What do you do? What's your role?"**
Listen for: job title, industry, team size, whether they work alone or with others.

**2. "What tools and software do you use day to day?"**
Listen for: apps, platforms, services. This tells you what integrations matter later.

**3. "What are the main things you're responsible for producing or delivering?"**
Listen for: outputs, deliverables, recurring work. Reports, campaigns, content, operations, whatever they make.

**While listening, identify natural workspace boundaries.** Distinct areas of work become separate workspaces. Look for:
- Different tools or tech stacks
- Different clients or projects
- Different types of output
- Work that has nothing to do with other work

If something is unclear, ask a follow-up. Don't move on until you understand the shape of their work.

**Then ask the four questions the map needs.** Still plain words; each answer fills a named slot in the map you will write in Phase 4. Record the answers as you go.

**4. "What should I call you?"**
Fills `{owner}` and `{Your name}`. Whatever they say is the name the handoff cards, the digests and the state files will use ("Needs Maria").

**5. "Where do your tasks and to-dos live — an app, a list, nowhere yet?"**
Fills `{task manager}`. An app name, "a notebook", or "nowhere yet" are all fine answers; write what they said.
Then: **"In it, how do you mark something ready to do, blocked, or waiting on someone? If you don't, I'll write plain words."**
Fills the three labels `{your actionable label}`, `{your blocked label}`, `{your waiting label}`. Defaults when they have none: `ready`, `blocked`, `waiting`.

**6. "Where will shared keys and logins live?"**
Fills the credentials line under Environment. Default when they have no answer: "a root `.env` you create yourself; never pasted in chat".

Two slots are not asked. `{tool}` stays literal in the map, because `_practices/{tool}.md` is the pattern the practice files follow. `{path, once you have one}` is written as "none yet" until the person has a `flow.html`.

---

### Phase 3: MAP THE WORKSPACES

**Reflect back what you heard:**

> It sounds like you have [N] main areas of work: [list them]. Does that sound right?

Wait for confirmation. Let them correct you.

**Then for each workspace, ask:**

> Tell me a bit more about [area]. What do you actually do here?

Listen for:
- Sub-projects or modules within the area
- Specific tools used in that area
- What they produce or deliver
- Pain points or things that slow them down
- Whether anything is already built there (files, workflows, tables, code) or it is starting clean

**Keep it conversational.** If the user gives short answers, the workspace is simple. If they go deep, it's complex and needs more structure.

**Gauge complexity for each workspace:**
- **Simple** (reference material, single-tool work): CONTEXT.md only
- **Medium** (a few connected pieces, one or two integrations): CONTEXT.md with sub-routing
- **Complex** (multiple integrations, team handoffs): CONTEXT.md + detailed routing

Each area becomes one routing row in the map: the task in plain words, and the folder with its CONTEXT.md.

---

### Phase 4: CONFIRM AND CREATE

#### 4a. Present the proposed structure

**Where the workspace goes.** The workspace is its own folder **beside the kit**, never inside it: the kit folder is a factory you can run again for another workspace. Propose the default and let the person confirm or give a path:
- Running from the kit folder (the current folder holds `MANIFEST` and `install.sh`): `<first name lowercase>-workspace` in the kit folder's parent. For Maria, with the kit at `~/Desktop/team-build-kit`, that is `~/Desktop/maria-workspace`.
- Running from anywhere else: `~/Desktop/<first name lowercase>-workspace`.

Show the full plan before creating anything. Use a visual folder map like this:

```
YOUR WORKSPACE
━━━━━━━━━━━━━━━━━━━━━━━━━━

~/Desktop/
├── <the kit folder>/                 ← the kit (stays where it is)
└── maria-workspace/                  ← your workspace
    ├── CLAUDE.md                     ← your map (always loaded)
    │   "I am [name]. I do [role].
    │    Tasks live in [task manager].
    │    Routing: see folders below."
    ├── SKILLS.md                     ← your skills list (one row per command)
    ├── {area-1}/
    │   └── CONTEXT.md                ← [area-1] context (loaded when here)
    ├── {area-2}/
    │   └── CONTEXT.md                ← [area-2] context (loaded when here)
    └── standards, practices, hooks   ← the kit's; refreshed by /update-build-kit
```

Explain briefly:
- "The CLAUDE.md at the top is your home base. It tells me where everything is, how you work, and what to call you."
- "Each area has a CONTEXT.md that describes what happens there."
- "The last line is the kit's own files — the standards the commands read, the practice notes, and four small hooks that keep notes about sessions. They update when you run /update-build-kit; your map and your folders are never touched by that."
- "When you work in a specific area, I only load what's relevant to that area. Everything else stays available but not active."

**Wait for approval before creating anything.**

#### 4b. Create

Order of operations. Stop at the first ❌ and say what happened.

1. **Create the folder.** `mkdir -p <folder>`. Refuse three targets and say why: the home folder itself; the kit folder (it holds `MANIFEST`); a folder that already holds a `CLAUDE.md` the person wants kept (offer to update it instead, or choose another folder).
2. **Install the kit's files into it.** The installer places the standards, practices, hooks and their registration, and never touches a `CLAUDE.md`:
   - from the kit folder: `TBK_BASE="file://$PWD" TBK_WORKSPACE="<folder>" bash install.sh`
   - from anywhere else, the kit's raw GitHub base and its installer:
     ```bash
     KIT_RAW="https://raw.githubusercontent.com/zjamesblake/team-build-kit"
     curl -fsSL "$KIT_RAW/main/install.sh" | TBK_WORKSPACE="<folder>" bash
     ```
   Confirm the ✅ line and the two counts it prints (skills installed; workspace files placed). On ❌ nothing was written; stop.
3. **Write `<folder>/CLAUDE.md`** from `~/.claude/skills/_shared/claude_md_template.md`. Copy the template whole and fill every slot; change nothing else:
   - `{Your name}` (line 1) → the name from question 4
   - the row `| {a task in plain words} | {the folder, and its CONTEXT.md} |` → one row per area from Phase 3, e.g. `| Client work, briefs, deliverables | `clients/` (its CONTEXT.md) |`
   - `{your actionable label}`, `{your blocked label}`, `{your waiting label}` → the three labels from question 5
   - `{owner}` (twice) → the name; `{task manager}` → the answer to question 5; `{path, once you have one}` → `none yet`
   - the Environment line `{Where shared credentials …}` → the answer to question 6
   - delete the comment line `<!-- The first-run interview fills the table. -->`
   - `{tool}` and the n8n naming literal `{{System}} | {{Trigger + Action}}` stay exactly as they are
   Check before moving on: apart from those two literals, no `{` remains in the file.
4. **Write `<folder>/SKILLS.md`.** Title `# Skills`, one sentence ("Every command available in this workspace, with what it does; `/new-workflow` adds a row when it creates a skill."), then a table `| Skill | What it does |` with one row per `~/.claude/skills/<name>/SKILL.md` whose folder does not start with `_`, the description being the first sentence of the frontmatter's `description:` line. This loop prints the rows:
   ```bash
   for f in ~/.claude/skills/*/SKILL.md; do
     n=$(basename "$(dirname "$f")"); case "$n" in _*) continue;; esac
     d=$(grep -m1 '^description:' "$f" | sed -E 's/^description: *//; s/^([^.]*\.).*/\1/')
     printf '| /%s | %s |\n' "$n" "$d"
   done
   ```
5. **Create each area** by following `~/.claude/skills/new-workspace/SKILL.md` with the new folder as the root — read that file and follow it; do not restate it here. Give it the area's name; it is greenfield unless the person said something is already built there, in which case pass `--brownfield`. It writes the area's `CONTEXT.md` (with its Kind and Proved-by lines) and adds the routing row to the map; if the row you wrote in step 3 already covers the area, keep one row, not two.
6. **Tell the person about the trust prompt:** "The first time Claude Code opens this folder it asks once whether to trust the folder's hooks. Say yes; they are the kit's and they only write notes inside this folder."

#### 4c. Present the completed map

Show the map once more with a ✓ per file, then print the handoff card in the shape every command in the kit prints:

```
WORKSPACE READY
━━━━━━━━━━━━━━━━━━━━━━━━━━

  maria-workspace/
    CLAUDE.md                          ✓ your map
    SKILLS.md                          ✓ your skills list
    {area-1}/CONTEXT.md                ✓
    {area-2}/CONTEXT.md                ✓
    standards · practices · hooks      ✓ N kit files

HANDOFF
Where:  standalone · your workspace
Done:   workspace created and mapped — N kit files, M areas
Next:   open <folder> in Claude Code, read why_we_build.html, then /memo your first small thing (the door decides its size)
Needs <owner>: none | the questions the interview left open
Written: <folder>/CLAUDE.md · SKILLS.md · <area>/CONTEXT.md × M
```

---

## Safety Rules

1. **Never overwrite existing files.** Check first. If a `CLAUDE.md` exists, offer to update it or choose another folder; never replace it.
2. **Always confirm before writing.** Show the plan (Phase 4a) and wait for explicit approval.
3. **Never write into the kit folder or the home folder.** The workspace is its own folder beside the kit.
4. **Stay organized.** All workspace paths use kebab-case for folders and snake_case.md for docs.
5. **No secrets in generated files.** Never create .env files or write credentials; the map only says where they live.
6. **Handle re-runs gracefully.** If the user runs /onboard again and some files exist, only create what's missing. Offer to update existing files.
7. **Never ask the person to name a kind or a level.** Those are read from what they describe; the area skill decides them.

---

## Tone and Style

- **Warm but efficient.** Friendly, brief. Not a chatbot personality exercise.
- **No jargon.** Don't say "scaffold," "architecture," or "context window." Say "set up," "structure," and "what I can see."
- **Don't over-explain.** The user doesn't need to know why the three-layer structure works. They just need their workspace set up.
- **Match their energy.** Short answers = keep it short. Detailed answers = engage.
- **Celebrate the finish.** When the workspace is created, make it feel like an accomplishment.

---

## Edge Cases

### User has only one area of work
That's fine. Create one area folder with its CONTEXT.md and a map that routes to it.

### User isn't sure how to describe their work
Ask for examples. "What did you work on this week?" or "Walk me through a typical day."

### User wants to organize existing files
Point the area at the existing folder and create it with `--brownfield`: the area skill documents the current state, not an aspirational one. Flag cleanup as a follow-up.

### User has very complex work (10+ areas)
Group related areas into parent workspaces. A marketing agency with 12 clients doesn't need 12 workspaces. They need a "clients" workspace with sub-routing per client, plus separate workspaces for internal ops.

### User names a folder that already has a CLAUDE.md
Check what exists. Offer to update the existing structure rather than replacing it, or pick another folder. Never overwrite.
