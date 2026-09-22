# One build, start to finish

_A personal expense tracker, walked from the install to a shipped quick fix, in the kit's own words._

You have a bank export and a question: where does the money go each month? This document follows that one small build through every step the kit gives you, so you can see what each step asks of you and what it hands back before you run one yourself. The thing built is a **tool**: a script you run by hand that reads the export and writes a monthly report. It touches real money, so the third gate fires exactly once, and you will see where. Each section says what you type, what you see, and why, in one sentence pointing at the explainer.

```chain
The lifecycle: install → /onboard → **/memo** → /prd → /build → /ship → outcome check → /quick-fix
A project's states: queued → cleared → approved → building → shipped → reached
```

## Step 1 — Install the kit

**What you type.** Either the one line from the README, or `get started` inside the kit folder you downloaded.

**What you see.** A line that starts with ✅ and gives a file count, then the list of commands you now have, then one sentence: new here, type `/onboard`.

**Why.** The commands are files; nothing is hosted and nothing runs until you type a command (the explainer, "What you bring, and what the skills carry").

## Step 2 — Create your workspace

**What you type.** `/onboard`

**What you see.** Six questions in plain words: what you do, which tools you use, what you produce, what to call you, where your tasks live and how you mark them ready, blocked or waiting, and where shared keys will live. A readback of your areas of work. A folder map with your workspace placed beside the kit, never inside it. After you approve: the installer's ✅ line, then a card.

```
HANDOFF
Where:  standalone · your workspace
Done:   workspace created and mapped — 20 kit files, 1 area
Next:   open the folder in Claude Code, read why_we_build.html, then /memo your first small thing
Needs you: none
Written: CLAUDE.md · SKILLS.md · money/CONTEXT.md
```

**Why.** Your map carries your names, so every later card can say what it needs from you by name; the kit's files sit beside it and refresh without touching it (the explainer, "What you bring, and what the skills carry").

## Step 3 — Read the explainer, once

**What you type.** Nothing. Open `why_we_build.html` in your workspace and read it.

**What you see.** Two ladders, six kinds, three gates, one state layer, and one idea: complexity is the enemy.

**Why.** Every step below is one of those sentences applied, so a single read makes the rest predictable (the explainer, "The one idea").

## Step 4 — Gate 1: is it worth building?

**What you type.** `/memo expense tracker`

**What you see.** The door decides the size first. It is not a fix, because nothing exists yet. It is not an initiative, because one milestone finishes it. So it is a project, and the memo asks the business questions: the problem (you cannot see where money goes), the cost of doing nothing (another month of guessing), the value (one report you act on), why now (the export is already on your disk), the boundary in one sentence (it reads one bank's export and writes one monthly report; it does not categorise automatically or touch the bank), and the success definition (by the end of next month one real export has produced a report you acted on). A companion page opens beside the memo for you to approve from. Then a card: Next `/prd expense-tracker`.

**Why.** Gate 1 asks whether the thing should exist at all, before any design, and a memo that says no is a win (the explainer, "Why gates, and why they check themselves").

## Step 5 — Gate 2: is it designed right?

**What you type.** `/prd expense-tracker`

**What you see.** The skill reads the memo and states the kind back: this is a tool, your own code that a person runs by hand, so its proof is tests on fixtures for the logic and one check of its output against a real export. It locks the beginning state (the export's exact columns, read from the file, not assumed), designs the smallest path (one script, one fixture folder, one report file), and writes a validation log where every dependency was tried live today. The last section says the build can run in one go with no open decision. Approve, and a card names work item 1.

**Why.** The kind decides the proof and the documents; naming it before building is what keeps a small thing small (the explainer, "Why six kinds").

## Step 6 — Build, work item by work item

**What you type.** `/build expense-tracker`. At each card, carry on or start fresh as its Context line says.

**What you see.** The first work item builds the parser and its tests, proves them, rewrites the project's `state.md` and prints a card whose Context line reads continue here, so the same session goes on to build the report writer. At the end the skill walks the four router questions. Two answer yes: the report's numbers drive a decision about your spending, and the thing touches money. So the build halts and the card says Next `/ship expense-tracker`.

```chain
The value stream: bank export → the script → monthly report → **a decision about spending**
```

**Why.** Position lives in one small file rewritten at every stop, so a session is cheap to end and cheap to resume; and the router, not your mood, decides whether the third gate runs (the explainer, "Why one state layer, and why position is kept apart from history").

## Step 7 — Gate 3: can you rely on it?

**What you type.** `/ship expense-tracker`

**What you see.** Six questions answered in a paragraph. What breaks: a column the bank renames, so the parser stops with a named error instead of a wrong total. Who notices: you, because the report refuses to write. The fallback: last month's report stays where it was. The contingency: the fixture that reproduces the rename becomes a test before the fix. How you fix it: `/quick-fix`, then the same exit gate. What it concludes without testing: nothing, because the one real export check ran. Every hole gets a verdict, the tool goes live, the memo moves to `_done/` and the PRD folder to `_archive/`, and the outcome check is scheduled for a date two weeks out. The card's Where line now reads shipped.

**Why.** Shipped is a promise other people can lean on; a tool that touches money earns that word only after the questions are answered (the explainer, "Why gates, and why they check themselves").

## Step 8 — Two weeks later: was the problem solved?

**What you type.** Nothing new. The scheduled task comes due; you open a session and answer it.

**What you see.** The memo's success definition, read back word for word: did one real export produce a report you acted on? You say yes, you cancelled two subscriptions. The milestone's row changes from shipped to reached, and the lessons written at ship time get one line about what real use showed.

**Why.** Shipped means the build is done; reached means the problem is gone, and only the second one was the point (the explainer, "Why shipped is not reached").

## Step 9 — Later: a small change

**What you type.** `/quick-fix rename the "eating out" category to "restaurants"`

**What you see.** A diagnosis first, then a two-line change and its test, then the same four router questions. This time none fires: the report's numbers do not change, no data is written, nobody else reads it. The fix ships freely, and the session ends with its log line and a card.

**Why.** The exit gate is the same rule at the bottom of the ladder as at the top; the size of the work changes how much ceremony it gets, never whether it is checked (the explainer, "Why two ladders, and why a door").

## Step 10 — Every session ends the same way

**What you type.** Nothing; the skill you ran closes the session.

**What you see.** One entry in the day's log, a check that the living documents still match what changed when the session changed a system, and the card. The card at the end of one session and the gate line at the start of the next say the same thing.

**Why.** History goes to the log and position goes to the snapshot, so nobody reads a transcript to find out where things stand (the explainer, "Why one state layer, and why position is kept apart from history").

## Where each step comes from

| Claim | Source that confirms it |
|---|---|
| The installer prints ✅, a count, the command list, and "New here? Type /onboard" | the kit's `install.sh`, the success branch |
| `/onboard` asks six questions, places the workspace beside the kit, installs the kit's files, prints the card | `onboard/SKILL.md`, Phase 2 questions 1–6, Phase 4a, Phase 4b, Phase 4c |
| The card's five lines: Where · Done · Next · Needs · Written | `documentation_standard.md` (the template library) §4.10 |
| `/memo` is the one door and decides fix, project or initiative first | `memo/SKILL.md`, "When NOT to use" and "the initiative test" |
| The memo's six inputs: problem, cost of inaction, value, why now, boundary, success definition | `memo/SKILL.md`, the frontmatter description; `glossary.md`, "Gate 1, the memo" |
| A companion page opens beside every gate document | `glossary.md`, "Companion" |
| The PRD states the kind and the proof it requires | `prd/SKILL.md`, the "Kind" line of the PRD header |
| A tool is proved by tests on fixtures and one check against real data | `documentation_standard.md` (the root standard), the kinds table, "Tool" row |
| The PRD locks the beginning state live and ends with the one-shot readiness section | `prd/SKILL.md`, the definition of done and Phase 9 (the PRD's §15) |
| A build session is one work item; it ends with `state.md` rewritten and a card | `build/SKILL.md`, Phase 2 Step 4 and Step 5 |
| The next session verifies three commands from the snapshot before continuing | `build/SKILL.md`, Phase 1-A |
| The router's four questions, and one yes sends the build to `/ship` | `build/SKILL.md`, Phase 4; `glossary.md`, "Blast radius" and "Router" |
| Ship's six questions: what breaks, who notices, fallback, contingency, how we fix it, what it concludes without testing | `ship/SKILL.md`, the definition of done |
| Ship moves the memo to `_done/` and the PRD folder to `_archive/`, and schedules the outcome check | `_shared/project_close.md`, §3 and §5 |
| A milestone reads reached only when the outcome check confirms the success definition | `glossary.md`, "Milestone" and "Outcome check"; the explainer, "Why shipped is not reached" |
| `/quick-fix` ends with the same four router questions | `quick-fix/SKILL.md`, Phase 3.5 |
| Every session ends with a log entry, and with a living-docs check when it changed a system | `session-close/SKILL.md`, §1 and §2 |
| The card at the end of a session and the gate line at the start of the next say the same thing | `documentation_standard.md` (the template library) §4.10, the purpose line |
