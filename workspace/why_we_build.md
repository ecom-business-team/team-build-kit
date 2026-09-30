# Why we build this way

_What the kit does, in plain words, and the reason for each part._

The kit is a set of instructions for Claude Code, the AI assistant you build with, together with a few documents that keep your work in order. You describe a thing you want in plain words. The kit works out what kind of thing it is and what it needs.

Then three checkpoints decide, in order, whether it should exist, whether it is designed right, and whether other people can rely on it. While it is being built, one short note always says where the work stands, so you can stop at any moment and pick it up again later in minutes. And after it is finished and in use, we go back and check whether the problem was actually solved. Everything below explains one of those sentences.

## The one idea, if you remember nothing else

**Complexity is the enemy. If you can't explain it simply, it's probably too complicated — or built poorly.**

Nearly every build that goes wrong goes wrong the same way: it tried to do too much, too soon, and the person was in over their head before they noticed. Nothing in the kit exists to make building slower or more formal. Every checkpoint and every document is there to catch that one mistake while it is still cheap to fix, instead of later, when it has become a mess that nobody can explain.

A simple system is not a small one. It is one that a person can explain out loud in a paragraph, and the second checkpoint asks exactly that.

## Why three checkpoints, and why they check themselves

A checkpoint is a question you must answer before you move on to the next step. It grades itself: if you cannot answer the question, you have not passed, and you will know it yourself. When you can, you write the answer down, and the owner, the person whose work this is, approves it. There are three, and they come at different moments, because some questions are only worth asking once the earlier ones are answered.

| Checkpoint | The question | Answered by | When |
|---|---|---|---|
| Checkpoint 1 | Should this exist? | A memo | Before anything is built |
| Checkpoint 2 | Is it designed right? | A PRD | Before building starts |
| Checkpoint 3 | Can other people rely on it? | A ship review | Before it goes live, only when the blast radius says a mistake would travel |

**Checkpoint 1 asks whether this should exist.** You answer it by writing a memo, a short note written before anything is built. The memo says what problem the thing solves, what doing nothing costs, what solving it is worth, why now, what the thing is, in one sentence, and how you will know it worked. Most important of all, it says what the thing is *not*. A memo whose honest answer is "do not build this" is a win, because it just saved a build that was not worth making.

**Checkpoint 2 asks whether it is designed right.** You answer it with a PRD, short for product requirements document: the design, written down before any building starts. Claude works out on paper how the thing will work, checks that everything the design assumes is actually true in the systems you already run, and reuses what exists instead of inventing more. The test is whether you can explain the design in a short paragraph or draw it. If you cannot, you do not understand it yet, and building something you do not understand is how you end up unable to fix it when it breaks.

**Checkpoint 3 asks whether other people can rely on it.** You answer it with a ship review, the last check before the thing goes live, meaning before other people start relying on it, and it only happens when the stakes are real.

The kit measures the stakes with four questions, which together it calls the blast radius, meaning how far a mistake would travel:

- Does someone other than you depend on it?
- Does it change real data?
- Is its output used to make decisions?
- Does it touch money or anyone outside your team?

If every answer is no, the thing is a toy and you may play freely. If any answer is yes, it does not go live until the ship review has answered six questions:

- What happens when it breaks?
- Who notices?
- What is the fallback?
- What is the contingency, if the fallback fails too?
- How does it get fixed?
- What do the tests, the automatic checks written for it, take for granted without ever having checked it?

You never have to remember this yourself. At the end of every build and every small fix, Claude asks the four questions for you, so the checkpoint that matters most is the one you cannot skip by accident.

```chain
memo (Checkpoint 1) → PRD (Checkpoint 2) → build → ship review (Checkpoint 3) → **outcome check**
```

The last step, the outcome check, is explained further down this page. Skipping the checkpoints goes wrong in one of two ways. Without the first, "while I'm at it" turns a weekend idea into a month-long swamp. Without the third, something other people lean on goes live with nobody able to say how it fails or how to fix it.

## Two questions about size, and where every idea starts

Two questions sound alike and are not, and the kit answers both for you.

| The question | The answers |
|---|---|
| How big is this piece of work? | A fix, a project, or an initiative |
| How big is the thing being built? | A part, a system, or a workspace |

**How big is this piece of work?** It comes in three sizes. A fix is a small, known change that needs no design, and the kit handles it with `/quick-fix`, a single command, one of the slash commands you type to Claude. A project is one build that goes through the checkpoints: a memo, a PRD, the build itself and, when the stakes are real, a ship review. Several projects that build on each other make an initiative, a larger effort with a written plan. Each project on the plan runs through the checkpoints on its own, and the point where one more promised thing becomes true is called a milestone.

Whatever the size, the work is done in sessions. A session is one conversation with Claude, from opening the chat to closing it. It does one piece of the work at a time, called a work item, such as one part of a project's design, and it tells you when the conversation has grown long enough that a fresh start would be cheaper, because a very long conversation costs more to run and starts to lose detail.

**How big is the thing being built?** It is a part, a system or a workspace. A system is something that does one job, such as the process that sends invoices to your clients, and a part is one piece of it, such as the script that works out what each client owes. A workspace is the folder that holds all your systems. Every built thing has its place, and each folder has an index, a short page that says what the folder is, what lives in it, and how to pick it up in a fresh session.

**Every idea starts with `/memo`, which works out how big it is and where it goes next.** Whether it is a one-line fix or a rebuild that takes months, you type `/memo` and describe what you want. If it is small and known, it goes to a quick fix. If it is one build, it gets a memo and becomes a project. If it is several builds, it becomes an initiative with a plan. Nobody has to decide the size themselves.

Without these two questions you get the month-long "quick fix" that was never small, and the thing built with no system to belong to, so that six weeks later nobody knows where its documents are or who may change its data.

## Why one short note says where the work stands

Every project has a state file. The state file is a short note that says where the project stands right now: what is done, what is next, and what is waiting on someone. It is rewritten every time something moves, so it is always current and never grows into a history.

What happened along the way goes somewhere else, into the project's log, which is the diary: it is added to and never edited, and it is never read to find out where the work stands. An initiative has one state file too, for the plan as a whole.

At every stop, whether the work is finished, waiting on you, or the conversation has grown long, Claude prints a handoff card, a short summary that says the same things in the same order:

- where the work sits, and how far it has come;
- what just got done, and how it was proved;
- every task filed for later in your task manager, the one app or file where your tasks live, and everything noticed but left unresolved, with whether each needs attention now;
- what only you, the person whose workspace this is, can do;
- exactly what to type next, and whether to carry on in this conversation or start a fresh one;
- where all of this is written down.

A session that picks up earlier work opens with the same card, so a misread is caught before any work is done.

```chain
a session ends → the state file is rewritten → the next session reads only the state file
```

The reason is measured. Before the state file existed, a session that had to work out where a build stood rebuilt that picture from six to ten diary-like documents, reading anywhere from tens of thousands to well over a hundred thousand words, and re-reading the same files fifteen to thirty times inside one conversation. A note of a few hundred words, checked against the real files and systems it describes in minutes, gets a fresh session going and costs almost nothing.

What goes wrong is either of the two habits this forbids. Adding to the state file instead of rewriting it turns the note back into a diary, and reading the diary to find your place costs the very time the note was made to save.

## Why six kinds

A form wired to a spreadsheet is not shown to work the same way an app is, and neither is shown to work the same way a document is. So the proof, the evidence that a thing works, depends on what kind of thing it is, not on how big it is. The kit knows six kinds of built thing, and each one has its own way of being shown to work.

- An **automation** is tools you pay for but do not own, such as a form service and a spreadsheet, wired together. It is proved by replaying it through its real entry point, the form or the trigger that really starts it.
- A **service** is your own code that runs on its own with no screen. It is proved by tests, a live probe of the running thing, and a forced failure that its noticer, whatever tells a person that something broke, actually reports.
- An **application** is your own code with a screen that people sign into. It is proved by a real browser walking the real screens through the real login, plus checks that read its live data.
- A **tool** is your own code that a person runs by hand to produce an output. It is proved by tests on made-up sample data and one check of its output against real data.
- A **procedure** is instructions that Claude follows, such as a skill, a command like `/memo` whose written steps Claude carries out. It is proved by a cold read, a fresh session with no memory running it from the file alone.
- **Knowledge** is something people read. It is proved by review against a verification table, one row per claim beside the source that confirms it. This page is knowledge, and its table is the last section.

Because the kit asks what kind of thing it is first, it can set up exactly the documents that kind needs and reach for exactly that kind's proof, without you having to learn the list of kinds. What goes wrong when the kind is ignored is a checklist written for one kind applied to another. Every box gets ticked, and nothing has been proved.

## Why shipped is not reached

The ship review proves the build is safe for other people to rely on. It does not prove that the problem in the memo was solved, and nothing else in the lifecycle, the chain of steps from memo to outcome check, checks that. So the outcome check does. Every memo contains a success definition, one sentence that says "we will know this is solved when…" in words that can be checked. On a set date after go-live, the moment other people start relying on the thing, that sentence is checked against real people using it, and only then is the work counted as reached.

```chain
queued → memo cleared → PRD approved → building → shipped → **reached**
```

Read left to right, that line is the life of one project. It is planned but not started, then its memo is approved, then its PRD is approved, then it is being built, then it is live, and last, the outcome check has confirmed it solved the problem.

The outcome check is the loop back to the memo: it takes the memo's own sentence and checks it. Without it, "done" gets called at shipped, that loop never closes, and a thing can be live, stable and unused for months while everyone believes the problem is behind them.

## Why four layers, and where each one lives

The kit's content sits in four layers, and each layer has one home, so nobody has to wonder which file to change or which file an update will overwrite.

The **method** lives in the skills, the commands such as `/memo` and `/build`. They are written once for everyone and the kit refreshes them when it updates, so they are best left unedited. Your own rules for a command go in a file of your own, `.claude/skills.d/<command>.md` in your workspace, that the kit reads and never writes.

Your **judgment** lives in your folders: your map, the `CLAUDE.md` file that tells every session where things live, each folder's index, and your additions to a command. An update never touches them, except the kit's own lines in your map, which it offers for you to take or decline.

The **proof** lives at the checkpoints, in writing, and a person approves it. Before building, that means the memo and the PRD. Before anything is called done, it means the proof its kind requires, the tests or the cold read, written down where the owner can approve it. No checkpoint is cleared without a document someone approves.

The **position**, where the work stands, lives in one state file per project, a few hundred words rewritten in place. A fresh session starts from it, never from the log.

Without this split, an update overwrites a rule you wrote, and nobody can say which file is the kit's and which is yours. That is why the installer, the script that puts the kit into your workspace, keeps a receipt: a list of every file it placed, so the kit's files and yours can always be told apart.

## What you bring, and what the skills carry

You are not expected to know how to build anything technically. The skills carry that load. Your part is the part no tool can do for you.

| You decide | The skills handle |
|---|---|
| What is worth building. | Designing the pieces. |
| What "done" means. | Checking the technical assumptions against the live system. |
| What it is *not*. | Writing the actual thing. |
| Whether the stakes are acceptable. | Keeping the documents current. |

Say what you are trying to do, answer the checkpoints honestly, and the kit does the rest. If partway through something turns out bigger or harder than expected, a skill stops, tells you, and points you back to `/memo`. That is not failure. It is the system catching the problem while it is cheap to fix.

## Where each why comes from

| Claim | Source that confirms it |
|---|---|
| The one-breath sentence: describe the thing, the kit names its kind, three checkpoints, one short note apart from history, a check afterwards | the initiative's north star, §1 |
| The kit is a set of skills, standards and pages installed into your workspace | `glossary.md`, "The kit", "Skill" |
| "Complexity is the enemy" is the kit's one idea, kept word for word | the June explainer, "The one idea"; the initiative's north star, §2 principle 6 |
| Builds go wrong by doing too much too soon; the kit catches it while it is cheap | the June explainer, "The one idea" |
| A checkpoint is a question you must answer before moving on; it grades itself, and the owner approves the written answer | `glossary.md`, "Checkpoint"; the June explainer, "Why gates?" |
| Checkpoint 1 asks "should this exist?" and covers problem, cost of inaction, value, why now, what it is and is not, and the success definition | `glossary.md`, "Checkpoint 1, the memo" |
| Checkpoint 2 asks "is it designed right?", PRD is short for product requirements document, and every dependency is checked against the live system | `glossary.md`, "Checkpoint 2, the PRD" |
| Checkpoint 3 asks "is it safe for other people to rely on?", is answered by the ship review, and runs only when blast radius crosses the line | `glossary.md`, "Checkpoint 3, the ship review" |
| Blast radius is four questions about how far a mistake would travel, and one yes means Checkpoint 3 | `glossary.md`, "Blast radius" |
| Claude asks the four questions at the end of every build and quick fix | `glossary.md`, "Router", "Exit check" |
| The checkpoints come at different moments because some questions are only worth asking after earlier ones | the June explainer, "Why gates?" |
| Checkpoint 1 asks what the thing is in one sentence; a memo that says "do not build this" is a win; skipping it turns a weekend idea into a month-long swamp | the June explainer, "Gate 1" |
| Checkpoint 2 reuses what exists, and its test is whether you can explain the thing in a short paragraph or draw it | the June explainer, "Gate 2" |
| If no blast-radius answer is yes the thing is a toy; if any is yes it does not go live until the failure questions are answered | the June explainer, "Gate 3" |
| The ship review asks six things, of which what breaks, who notices and the fallback are three | `glossary.md`, "Checkpoint 3, the ship review" |
| The lifecycle runs memo, PRD, build, ship review, outcome check | `documentation_standard.md`, §4 (the planning-folder contract, and the milestone states) |
| The first size question is how big the work is: a fix, a project, or several projects that make an initiative | `glossary.md`, "The two size questions", "Quick fix", "Project", "Initiative" |
| The second size question is how big the thing is: a part, a system, a workspace | `glossary.md`, "Part, system, workspace" |
| A session is one conversation from opening the chat to closing it, and it does one work item at a time, saying when a fresh start is cheaper | `glossary.md`, "Session"; "Work item"; "Session boundary" |
| Projects on a plan that build on each other make an initiative, and each point the plan reaches is a milestone | `glossary.md`, "Project", "Milestone", "Initiative" |
| Every built thing has an index that says what it is, what lives in it, and how to pick it up in a fresh session | `glossary.md`, "CONTEXT.md"; `documentation_standard.md`, §5 (the required local index) |
| Every idea starts with `/memo`, which works out how big it is and where it goes next, so nobody sizes their own work | `glossary.md`, "Where every idea starts"; `documentation_standard.md`, §4 (the planning-folder contract) |
| Proof is by kind, not by size | the initiative's north star, §2 principle 7 |
| The six kinds and what each one is | `glossary.md`, "The kinds" (six rows) |
| The proof each kind must pass | `documentation_standard.md`, §4 (the kinds table); `glossary.md`, "Real entry point", "Cold read", "Verification table", "Live invariant", "Smoke test", "Noticer" |
| The kit asks the kind first and sets up and proves by it, without the person learning the list of kinds | the initiative's north star, §5 ("Kinds decide the document set, the proof and the practices"); §7, milestone 1's "reached when" |
| The state file is a short note of where a project stands (done, next, waiting on someone), rewritten every time something moves, and the only place that says where the work stands | `glossary.md`, "State file"; `documentation_standard.md`, §4 ("Three levels, one snapshot each") and §6 ("State is a snapshot, history is a log") |
| A fresh session starts from the state file and its checks in minutes | `glossary.md`, "Orient"; the initiative's north star, §1 |
| The log is the diary: added to, never edited, and never read to find out where the work stands | `glossary.md`, "Record" |
| The handoff card says the same things at every stop, including what was left unresolved, and a resuming session opens with the same card | `glossary.md`, "Handoff card", "Residual" and "Orientation card" |
| Sessions rebuilt their position from six to ten history-shaped documents, at a cost between tens of thousands and well over a hundred thousand words of reading, re-reading the same files fifteen to thirty times | `documentation_standard.md`, §4 ("State split from history 2026-09-20": 27k–237k tokens of orientation per session, the same files re-read 15–29 times) |
| The ship review proves safe to rely on, not that the problem was solved; the outcome check is the only step that checks that | the shared close procedure (`project_close.md`), §5; `glossary.md`, "Outcome check" |
| Go-live is when other people start relying on the thing; work is shipped when live and reached only when the outcome check confirms the success definition | `glossary.md`, "Go-live", "Milestone", "Success definition"; `documentation_standard.md`, §4 (the milestone states) |
| You decide what is worth building, what done means, what it is not, whether the stakes are acceptable; the skills design, check, write and keep the documents | the June explainer, "What you bring vs. what the skills handle" |
| When something turns out too big, a skill stops and points back to `/memo` | the June explainer, "When it gets too big"; `build/SKILL.md`, "Scope Escalation"; `glossary.md`, "Where every idea starts" |
| The kit's own files are refreshed by its updater and a file you changed is kept, with the kit's version written beside it; your own rules for a command go in a file the kit reads and never writes | `update-build-kit/SKILL.md`, "What ships" and "Step 2: Verify"; the initiative's north star, §5 (the box) |
| Your skills list and the folders you made are never read or written by an update; your map changes only in the sections you approve | `update-build-kit/SKILL.md`, description and "How it works" |
| The skills are written once for everyone | the initiative's north star, §2 principle 4 and §7 milestone 2 ("written once") |
| An update once overwrote a person's edits; the installer's receipt now records every kit-placed file so the kit's files and yours can be told apart | `ship/SKILL.md`, "Phase 3: DISPOSITION" (the Accept row's managed-file example); `install.sh`, header comment (receipts, the package-manager rule) |
| A checkpoint is cleared in writing by a person, and nothing is done without the proof its kind requires | `memo/SKILL.md`, "Close: hand off or pause"; `prd/SKILL.md`, "Present for approval"; `ship/SKILL.md`, "Definition of done"; `build/SKILL.md`, Phase 2 "Step 2: Per-Item Verification"; the initiative's north star, §2 principle 7 |
| Position lives in one state file per project, rewritten in place, and a fresh session starts from it, never from history | `glossary.md`, "State file", "Record"; `documentation_standard.md`, §6 "State is a snapshot, history is a log" |
