# One build, start to finish

_A personal expense tracker, followed from the first install to a small change after it went live, in the words the commands themselves use._

You have a bank export and a question: where does the money go each month? This document follows that one small build through every step the kit gives you, so you can see what each step asks of you and what it hands back before you run one yourself. The kit is a set of skills for Claude Code, the AI assistant you build with, together with a few pages that explain them. A skill is a command you type, such as `/memo` or `/build`, whose written instructions Claude follows step by step.

The thing built is a **tool**: a script you run by hand that reads the export and writes a monthly report. One build like this, taken from its first note to its finish, is what the kit calls a project. Every project meets up to three checkpoints, which are questions it must answer before it moves on: whether it should exist, whether it is designed right, and whether other people can rely on it. The third one, Checkpoint 3, is a review that runs only when a mistake could travel beyond you. This tool touches real money, so Checkpoint 3 runs exactly once, and you will see where. Each section says what you type, what you see, and why, and the why is one sentence pointing at the explainer, the kit's page `why_we_build.html` that gives the reason for each step.

```chain
The lifecycle: install → /onboard → **/memo** → /prd → /build → /ship → outcome check → /quick-fix
A project's states: queued → cleared → approved → building → shipped → reached
```

The first line is the whole path in order: you install the kit, set up your workspace with `/onboard`, write a memo, which is a short note written before anything is built that answers Checkpoint 1, design the build with `/prd`, which writes the PRD, short for product requirements document, the written design that answers Checkpoint 2, build it with `/build`, review it with `/ship` when a mistake could reach beyond you, and later run the outcome check to see whether the problem is solved, while `/quick-fix` is the short path for small, known changes after that.

The second line is the states a project passes through: queued means it is planned but not started, cleared means its memo passed Checkpoint 1, approved means its PRD passed Checkpoint 2, building means the work is under way, shipped means it is live, and reached means the outcome check confirmed it solved the problem it was built for.

## Step 1 — Install the kit

**What you type.** Either the one line from the README, or `get started` inside the kit folder you downloaded.

**What you see.** A line that starts with ✅ and gives a file count, then the list of commands you now have, then one sentence: new here, type `/onboard`.

**Why.** The commands are files; nothing is hosted and nothing runs until you type a command (the explainer, "What you bring, and what the skills carry").

## Step 2 — Create your workspace

**What you type.** `/onboard`

**What you see.** Six questions in plain words: what you do, which tools you use, what you produce, what to call you, where your tasks live and how you mark them ready, blocked or waiting, and where your shared keys will live, meaning the one private file that holds the passwords and access keys your tools use. A readback of your areas of work, where an area is a folder in your workspace for one area of your work, such as `money/`. A folder map with your workspace placed beside the kit, never inside it. After you approve: the installer's ✅ line, then a handoff card, the short summary Claude prints at every stop, which your screen shows with headings (its markdown is below).

````markdown
## HANDOFF · standalone · your workspace

### Done
The workspace was created and mapped, with 20 kit files and 1 area.

### Filed this session
None.

### Residuals
None.

### Needs you
None.

### Next
**Open the folder in Claude Code**, read `why_we_build.html`, then run `/memo` for your first small thing.
`Context: the next step opens a new folder → fresh session`

### Written
- `CLAUDE.md` · `SKILLS.md` · `money/CONTEXT.md`
````

The card reads top to bottom. The header says standalone, which means this work is not part of an initiative, the larger kind of effort made of several projects that Step 4 describes. A session is one conversation with Claude, from opening the chat to closing it. Done says what this session finished. Filed this session lists the tasks written into your task manager for later, and here there are none. Residuals lists the things noticed and left unresolved, each with a note on whether it needs attention now. Needs you lists what only you can decide. Next is the exact command to run next, and the Context line under it measures how full the conversation has become and says whether to carry on in this one or start a fresh session. A new folder or a large next step also makes a fresh session the cheaper choice, which is why this card says fresh session even though little has been used. Written lists the files this step created: `CLAUDE.md` is your map, `SKILLS.md` is the list of your commands, and `money/CONTEXT.md` is the index of your money folder, a short page that says what the folder is, what lives in it and how to pick the work up.

**Why.** Your map, the `CLAUDE.md` file that tells every session where things live, carries your names, so every later card can say what it needs from you by name; the kit's files sit beside it and refresh without touching it (the explainer, "What you bring, and what the skills carry").

## Step 3 — Read the explainer, once

**What you type.** Nothing. Open `why_we_build.html` in your workspace and read it.

**What you see.** The page walks through a few ideas. There are two questions about size: how big the work is, which is a fix, a project or several projects, and how big the thing is, which is one part, a whole system or a whole workspace. There are six kinds of thing you can build: an automation is tools you pay for wired together, a service is your own code running on its own, an application is your own code with screens people sign into, a tool is code a person runs by hand, a procedure is written steps Claude follows, and knowledge is something people read. Then come the three checkpoints, the one short note that says where the work stands, and one idea above them all, which is that complexity is the enemy.

**Why.** Every step below is one of those sentences applied, so a single read makes the rest predictable (the explainer, "The one idea").

## Step 4 — Checkpoint 1: is it worth building?

**What you type.** `/memo expense tracker`

**What you see.** `/memo` works out the size first. It is not a quick fix, the kind of small, known change that needs no design, because nothing exists yet. It is not an initiative, a larger effort planned as a series of milestones (points where one more thing is true), each reached by its own project, because one milestone finishes it. So it is a project, and the memo, the short note that answers Checkpoint 1, asks the business questions: the problem (you cannot see where money goes), the cost of doing nothing (another month of guessing), the value (one report you act on), why now (the export is already on your disk), the boundary in one sentence (it reads one bank's export and writes one monthly report; it does not categorise automatically or touch the bank), and the success definition (by the end of next month one real export has produced a report you acted on). A companion page, a web page generated beside the memo so you can read it without the markdown, opens for you to approve from. Then a card: Next `/prd expense-tracker`.

**Why.** Checkpoint 1 asks whether the thing should exist at all, before any design, and a memo that says no is a win (the explainer, "Why three checkpoints, and why they check themselves", which means each checkpoint grades itself: if you cannot answer its question, you have not passed).

## Step 5 — Checkpoint 2: is it designed right?

**What you type.** `/prd expense-tracker`

**What you see.** The skill reads the memo and writes the PRD, the written design that answers Checkpoint 2. First it states the kind back: this is a tool, your own code that a person runs by hand, so its proof is tests on fixtures, small sample files that stand in for real input, for the logic, and one check of its output against a real export. It locks the beginning state, the exact picture of what exists today (here, the export's exact columns, read from the file, not assumed). It designs the smallest path (one script, one fixture folder, one report file), and it writes a validation log, a list of everything the design depends on, where every dependency was tried live today. The last section says the build can run in one go with no open decision. Approve, and a card names work item 1, the first bounded piece of the build, which promises one output.

**Why.** The kind decides the proof and the documents; naming it before building is what keeps a small thing small (the explainer, "Why six kinds").

## Step 6 — Build, work item by work item

**What you type.** `/build expense-tracker`. At each card, carry on in this session or start a fresh one, as its Context line says.

**What you see.** The first work item builds the parser and its tests, proves them, rewrites the project's `state.md` and prints a card whose Context line reads continue here, so the same session goes on to build the report writer. The `state.md` file is the project's state file, a short note that says where the project stands right now: what is done, what is next, and what is waiting on someone. At the end the skill runs the router, the check at the end of a build that asks four questions about the blast radius, meaning how far a mistake would travel, and routes the build to `/ship` or past it. The four questions ask whether someone other than you depends on it, whether it changes real data, whether its output is used to make decisions, and whether it touches money or anyone outside. Two answer yes: the report's numbers drive a decision about your spending, and the thing touches money. So the build halts and the card says Next `/ship expense-tracker`. The line below draws the tool's value stream, which is the path from what starts the tool to the result it produces.

```chain
The value stream: bank export → the script → monthly report → **a decision about spending**
```

**Why.** Position lives in one small file rewritten at every stop, so a session is cheap to end and cheap to resume; and the router, not your mood, decides whether Checkpoint 3 runs (the explainer, "Why one short note says where the work stands").

## Step 7 — Checkpoint 3: can you rely on it?

**What you type.** `/ship expense-tracker`

**What you see.** Six questions, answered in a paragraph. The first asks what breaks, and the answer is a column the bank renames, so the parser stops with a named error instead of a wrong total. The second asks who notices, and the answer is you, because the report refuses to write. The third asks for the fallback, which is what you do while the tool is broken, and here last month's report stays where it was, so you still have numbers to go on. The fourth asks for the contingency, which is what you do if the fallback is not enough either, and here, if last month's report cannot stand in and you need this month's numbers now, you open the export in a spreadsheet and total it by hand. The fifth asks how you fix it, and the answer is that the fixture that reproduces the rename becomes a test before the fix, then `/quick-fix`, then the same exit check, the four blast-radius questions asked at the end of every build and every quick fix. The sixth asks what the review concludes without testing, and the answer is nothing, because the one real export check ran. Every hole, meaning every question without a good answer, gets one of three verdicts: fixed now, escalated to someone who can decide it, or accepted with your sign-off. `/ship` also writes the lessons learned during the review into the project log, the project's running diary. Then the tool goes live, which for a tool you run by hand means you start relying on its report. The memo moves to `_done/`, and the project folder, `_admin/prds/expense-tracker/`, which holds the PRD, the project log, the state file and their pages, moves to `_archive/`. Both of those are filed inside `_admin/`, the folder at the top of your workspace that holds the planning documents, meaning the memos and the project folders with their PRDs, logs and state files. The outcome check is scheduled for a date two weeks out. The card that follows opens with a Progress block, which a card carries at its top whenever a project is in flight (the sample card in Step 2 has none because no project existed yet), and that block shows the project as shipped, while its Done block says the tool went live.

**Why.** Shipped is a promise other people can lean on; a tool that touches money earns that word only after the questions are answered (the explainer, "Why three checkpoints, and why they check themselves").

## Step 8 — Two weeks later: was the problem solved?

**What you type.** Nothing new. The scheduled task comes due; you open a session and answer it.

**What you see.** The memo's success definition, read back word for word: did one real export produce a report you acted on? You say yes, you cancelled two subscriptions. Every project's state file has a Stage line that shows how far the project has come (memo, PRD, build, ship, outcome), and in this project's state file, `state.md`, that line changes from shipped to reached. An initiative's state file would also carry a row for each of its projects, but this project belongs to no initiative, so its own Stage line is the only one that changes. The lessons `/ship` wrote into the project log get one more line about what real use showed.

**Why.** Shipped means the build is done; reached means the problem is gone, and only the second one was the point (the explainer, "Why shipped is not reached").

## Step 9 — Later: a small change

**What you type.** `/quick-fix rename the "eating out" category to "restaurants"`

**What you see.** A diagnosis first, then a two-line change and its test, then the same four router questions. This time none fires: the report's numbers do not change, no data is written, nobody else reads it. The fix ships freely, and the session ends with its entry in the day's log, a file that holds one entry per session with one file per day, and a card.

**Why.** The exit check is the same rule for the smallest fix as for the largest build; the size of the work changes how much ceremony it gets, never whether it is checked (the explainer, "Two questions about size, and where every idea starts").

## Step 10 — Every session ends the same way

**What you type.** Nothing; the skill you ran closes the session.

**What you see.** One entry in the day's log, a check that the living documents, the ones kept true at the moment something changes, still match what changed when the session changed a system, and the card. The card at the end of one session and the gate line at the start of the next say the same thing. The gate line is the one line a small script prints when the next session opens, saying where the work stands.

**Why.** History goes to the log and position goes to the state file, so nobody reads a transcript to find out where things stand (the explainer, "Why one short note says where the work stands").

## Where each step comes from

| Claim | Source that confirms it |
|---|---|
| The installer prints ✅, a count, the command list, and, when you have no workspace yet, a line telling you to type /onboard to create one | the kit's `install.sh`, the success branch |
| `/onboard` asks six questions, places the workspace beside the kit, installs the kit's files, prints the card | `onboard/SKILL.md`, Phase 2 questions 1–6, Phase 4a, Phase 4b, Phase 4c |
| The card's blocks: Progress (when there is an initiative or a project), Done, Filed this session, Residuals, Needs, Next, Written | `documentation_standard.md` (the template library) §4.10 |
| Every idea starts with `/memo`, which decides fix, project or initiative first | `memo/SKILL.md`, "When NOT to use" and "the initiative test" |
| The memo's six inputs: problem, cost of inaction, value, why now, boundary, success definition | `memo/SKILL.md`, the frontmatter description; `glossary.md`, "Checkpoint 1, the memo" |
| A companion page opens beside every checkpoint document | `glossary.md`, "Companion" |
| The PRD states the kind and the proof it requires | `prd/SKILL.md`, the "Kind" line of the PRD header |
| A tool is proved by tests on fixtures and one check against real data | `documentation_standard.md` (the root standard), the kinds table, "Tool" row |
| The PRD locks the beginning state live and ends with the one-shot readiness section | `prd/SKILL.md`, the definition of done and Phase 9 (the PRD's §15) |
| A build session ends every work item with `state.md` rewritten and a card, then carries on into the next work item or stops, as the card's Context line says | `build/SKILL.md`, Phase 2 Step 4 and Step 5 |
| The next session verifies three commands from the state file before continuing | `build/SKILL.md`, Phase 1-A |
| The router's four questions, and one yes sends the build to `/ship` | `build/SKILL.md`, Phase 4; `glossary.md`, "Blast radius" and "Router" |
| Ship's six questions: what breaks, who notices, fallback, contingency, how we fix it, what it concludes without testing | `ship/SKILL.md`, the definition of done |
| Ship moves the memo to `_done/` and the PRD folder to `_archive/`, and schedules the outcome check | `_shared/project_close.md`, §3 and §5 |
| A milestone reads reached only when the outcome check confirms the success definition | `glossary.md`, "Milestone" and "Outcome check"; the explainer, "Why shipped is not reached" |
| `/quick-fix` ends with the same four router questions | `quick-fix/SKILL.md`, Phase 3.5 |
| Every session ends with a log entry, and with a living-docs check when it changed a system | `session-close/SKILL.md`, §1 and §2 |
| The card at the end of a session and the gate line at the start of the next say the same thing | `documentation_standard.md` (the template library) §4.10, the purpose line |
