---
name: new-workflow
description: Turn a repeating process into a reusable skill through a guided interview. Walks you through identifying the steps, what Claude can handle vs. what needs your judgment, and saves it as a skill you can invoke with a single command, or as a pipeline of stage folders when the process has reviewed stages. The daily driver for building your skill library.
---

# /new-workflow

Turn something you do regularly into a reusable skill. This walks you through the process step by step, then saves it so you can run it with one command next time.

## Usage

```
/new-workflow
/new-workflow weekly client report
/new-workflow "the thing I do every Monday morning"
```

## When to Use

- You notice you're doing something for the second (or third, or tenth) time
- You just explained a process to Claude and want to save it
- You want to turn a manual task into a single command
- Any time you think "I wish I could just type one thing and get this done"

---

## Process

### Phase 1: SURFACE THE PROCESS

Start simple. Get them talking about what they do.

**Ask:**

> "Tell me about a process you do regularly. What's the end result you need to produce?"

Then:

> "Walk me through how you do it today. Step by step, in order."

**Listen for and capture:**
- What **triggers** it (a request, a date, an event, a decision)
- What **steps** happen, in what order
- What **tools** are used at each step
- What the **final output** looks like
- How **often** they do it
- How **long** it takes them currently

**Keep it conversational.** Don't interrogate. If they give you a rough overview, that's often enough. Ask follow-ups only on steps that seem unclear or where you need to know what "good" looks like.

---

### Phase 2: MAP THE STEPS

Break the process into clear steps (typically 3-7). For each step, figure out:

| Question | What you're capturing |
|----------|----------------------|
| What goes IN? | Input from previous step or external source |
| What does the user DO? | Their judgment, decisions, creative input |
| What can Claude handle? | Drafting, analysis, formatting, research |
| What comes OUT? | Output for next step or final delivery |

**Present it back** simply:

```
Here's what I'm hearing:

WORKFLOW: {name}
Trigger: {what kicks it off}
Frequency: {how often}
Current time: {how long it takes now}

Steps:
  1. {step} — {who does it: you / Claude / both}
  2. {step} — {who does it}
  3. {step} — {who does it}
  4. {step} — {who does it}

Final output: {what gets delivered}
```

Get confirmation. Let them correct the steps, reorder, add or remove.

**Then ask the shape question:** "Does this process have more than one stage where you stop and check the output before the next stage uses it — and have you run it at least twice?" Yes to both → the pipeline form (Phase 4P builds it instead of Phase 4). Otherwise → one skill (Phase 4, unchanged).

---

### Phase 3: IDENTIFY WHAT CLAUDE HANDLES

For each step, be explicit about what gets automated vs. what needs their input:

```
Here's how I'd split the work:

CLAUDE HANDLES (automated):
  - {step/task} — {what Claude does}
  - {step/task} — {what Claude does}

YOU DECIDE (needs your judgment):
  - {step/task} — {why this needs you}

COLLABORATIVE (Claude drafts, you refine):
  - {step/task} — {Claude does X, you review/adjust}
```

**Make the value visible.** Show them what gets taken off their plate. This is the payoff moment.

---

### Phase 4: BUILD THE SKILL

**Tell the user what you're about to do:**

> "I'm going to save this as a skill called /{skill-name}. Next time you need to do this, you just type that command and I'll walk you through it, handling the automated parts and asking for your input where needed."

**Create the skill file** at `~/.claude/skills/{skill-name}/SKILL.md`:

```markdown
---
name: {skill-name}
description: {One-line description of what this workflow produces. Include trigger and output so it's clear when to use it.}
---

# /{skill-name}

{What this does in one sentence.}

## Usage

\```
/{skill-name}
/{skill-name} {optional parameter if applicable}
\```

## When to Use

- {Trigger condition 1}
- {Trigger condition 2}

---

## Process

### Step 1: {Name}

**Input needed:** {what to start with, or what to ask the user for}

**Do:**
{Clear instructions for what Claude should do at this step.
Be specific about format, quality bar, and what "done" looks like.}

**Output:** {what this step produces}

---

### Step 2: {Name}

**Input needed:** {output from Step 1 + any user decisions}

**Do:**
{Instructions for this step.}

**Output:** {what this step produces}

---

### Step 3: {Name}
...

---

## Quality Check

Before delivering the final output, verify:
- [ ] {criterion 1 — does it meet the stated quality bar?}
- [ ] {criterion 2 — is the format correct?}
- [ ] {criterion 3 — anything missing?}

If any check fails, fix it before delivering. Note what went wrong so the skill can be updated.

---

## Notes

{Any context the skill needs to work well. Things like:
- Voice/tone requirements
- Formatting standards
- Where to find inputs
- Who receives the output}
```

**Adapt the template to the actual workflow.** Simple workflows get fewer steps. Complex ones get more detail. The quality check section is always present (closed loop thinking).

---

### Phase 4P: BUILD THE PIPELINE (only when the shape question said yes to both)

The process has stages a person reviews, so each stage gets its own folder and the next stage reads whatever the person left in the previous one's `output/`.

1. **The pipeline index.** Create `<area>/<workflow-slug>/CONTEXT.md` from template 4.2 in `~/.claude/skills/_shared/documentation_standard.md`, with the Kind line `procedure (pipeline form)`, a "What lives here" that names `stages/` and `_runs/` (earlier runs' outputs, moved there when a new run starts), and the stage table (Stage · Job · Human check) from template 4.14.
2. **One folder per stage.** For each stage from Phase 2, create `stages/NN_<stage>/CONTEXT.md` from template 4.14 (Inputs · Process · Outputs · Human check). The Phase 3 "YOU DECIDE" item for that stage becomes its Human check, stated as one action. Create the stage's `references/` and `output/` folders empty, each holding only an empty `.gitkeep` so git keeps it.
3. **A short runner skill** at `~/.claude/skills/<workflow-slug>/SKILL.md`, whose Process is: "Find the first stage whose `output/` is empty (a `.gitkeep` does not count) or older than its input. If that stage is not stage 01, first ask the owner whether the previous stage's Human check is done; if not, stop there. If every stage is done, the run is complete: say so, and when the owner starts a new run, move every stage's `output/` files into `_runs/{YYYY-MM-DD}/NN_<stage>/` beside `stages/` and begin at stage 01. Read that stage's `CONTEXT.md` and nothing it says not to load; do its Process; write to its `output/`; stop and ask the owner to do its Human check."

Then continue to Phase 5 (the first run walks stage 01) and Phase 6, which applies to both forms.

---

### Phase 5: FIRST RUN

After creating the skill, offer:

> "Want to run through this right now with a real example? That way we can make sure it works and adjust anything that's off."

If yes:
1. Invoke the skill as if they typed the command
2. Walk through each step with real content
3. At the end, ask: "How was that? Anything to adjust?"
4. If they have corrections, update the skill file immediately

If no:
> "You're all set. Next time you need to do this, just type /{skill-name} and I'll handle it. If anything needs adjusting after you use it a few times, just tell me and I'll update the skill."

---

### Phase 6: UPDATE THE MAP

After creating the skill, update the workspace:
1. If there's a relevant CONTEXT.md that should reference this workflow, add it
2. If the workspace has a `SKILLS.md`, append one row `| /<skill-name> | <one-sentence description> |`
3. Remind the user: "This skill is now available in any session, anywhere in your workspace. Just type /{skill-name}."

---

## The Daily Practice (embedded in how this skill works)

This skill IS the daily practice:

1. **Observe** — You noticed you do this process regularly
2. **Encode** — We just mapped it out and saved it as a skill
3. **Run** — Next time, you invoke it with one command
4. **Verify** — The quality check catches issues
5. **Improve** — You tell me what to adjust, I update the skill

Every time you run /new-workflow, your workspace gets more powerful. Every skill you build is one less thing you have to re-explain or redo from scratch.

---

## Guidelines

- **Use their language.** Name steps and the skill using the words they actually use, not process consultant terms.
- **Don't over-engineer.** Match the real process, not an idealized version. Capture reality first.
- **Make the quality check meaningful.** Generic checks ("is it good?") are useless. Specific checks ("does the report include week-over-week comparison?") actually catch problems.
- **Skills are living.** Tell the user they can (and should) update skills as their process evolves. "Just tell me to update /{skill-name} and describe what changed."
- **Keep skills focused.** One skill, one outcome. If a process produces two very different outputs, it might be two skills.
- **3-7 steps is the sweet spot.** Fewer than 3 means it's too simple to need a skill. More than 7 means steps can probably be combined.

---

## Edge Cases

### User can't articulate their process clearly
Ask them to walk through the most recent time they did it. Concrete examples are easier than abstractions. "What did you do last Monday when you made that report?"

### Process involves tools Claude can't access
Note this in the skill as a step where the user provides input. "At this step, pull the data from [tool] and paste it here." The skill still saves time by handling everything around that manual step.

### User wants to modify an existing skill
Read the existing skill file, ask what's changed, make the update. This isn't /new-workflow, but mention to the user: "Just tell me 'update /skill-name' anytime and describe what to change."

### The workflow is very simple (2 steps)
That's fine. A two-step skill that saves 15 minutes is still worth having. Don't add steps for the sake of complexity.
