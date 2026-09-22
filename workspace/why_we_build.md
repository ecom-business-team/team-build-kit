# Why we build this way

_Two ladders, six kinds, three gates, one state layer, and the reason for each._

You describe a thing you want in plain words. The kit tells you what kind of thing it is and what it needs. Three gates then decide, in order, whether it should exist, whether it is designed right, and whether other people can rely on it. While it is being built, where we are is kept apart from what happened, so any session picks up in minutes. And after it ships, we go back and check whether the problem was actually solved. Everything below is the reason for one of those sentences.

## The one idea, if you remember nothing else

**Complexity is the enemy. If you can't explain it simply, it's probably too complicated — or built poorly.**

Nearly every build that goes wrong goes wrong the same way: it tried to do too much, too soon, and the person was in over their head before they noticed. Nothing in the kit exists to make building slower or more formal. Every gate, ladder and file is there to catch that one mistake while it is still cheap to fix, instead of later, when it has become a mess that nobody can explain. A simple system is not a small one. It is one that a person can say out loud in a paragraph, and the second gate asks exactly that.

## Why gates, and why they check themselves

A gate is a checkpoint you clear before moving on. Nobody grants passage. The gate asks a question, and if you cannot answer it, you have not passed, and you will know it yourself. There are three, and they fire at different moments, because some questions are only worth asking after the earlier ones.

The first gate is the memo, and it asks whether this should exist at all. Before anything real is built, you say what problem it solves, what doing nothing costs, what solving it is worth, why now, and what the thing is, in one sentence. Most important of all, you say what it is *not*. A memo whose honest answer is "do not build this" is a win, because it just saved a build that was not worth making.

The second gate is the PRD, and it asks whether the thing is designed right. It works out on paper how the thing will work, checks that everything the design assumes is true in the live system, and reuses what exists instead of inventing more. The test is whether you can explain it in a short paragraph or draw it. If you cannot, you do not understand it yet, and building something you do not understand is how you end up unable to fix it when it breaks.

The third gate is ship, and it asks whether other people can safely rely on the thing. It fires only when the stakes are real, and the kit measures that with four questions it calls blast radius. Does someone other than you depend on it? Does it change real data? Is its output used to make decisions? Does it touch money or anyone outside? If every answer is no, the thing is a toy and you may play freely. If any answer is yes, it does not go live until the ship review has answered what happens when it breaks, who notices, what the fallback is, and three more questions like them. You never decide that yourself. The router asks the four questions at the end of every build and every quick fix, so the most important gate is the one you cannot skip by accident.

```chain
memo → PRD → build → ship → **outcome check**
```

Skipping the gates goes wrong in one of two ways. Without the first gate, "while I'm at it" turns a weekend idea into a month-long swamp. Without the third, something other people lean on goes live with nobody able to say how it fails or how to fix it.

## Why two ladders, and why a door

Two questions sound alike and are not. One is how big a piece of *work* is. The other is how big the *thing being built* is. The kit keeps a ladder for each, and one door, `/memo`, that places work on the first.

```chain
The ladder of work: session → work item → project → milestone → initiative
The ladder of what exists: part → system → workspace
```

On the ladder of work, a session, one conversation with Claude from opening the chat to closing it, does one work item at a time, and stops when its measured size says a fresh start is cheaper. Work items make a project. A project reaches one milestone. Milestones that build on each other make an initiative. On the ladder of what exists, a workspace holds several systems, and a system holds its parts. Every built thing sits somewhere on the second ladder, and its index says what it is, what lives in it, and how to pick it up in a fresh session.

The door is where the ladder of work meets the person. Every build intent, from a one-line fix to a rebuild that takes months, starts at `/memo`. The door places the work on the ladder of work for you, sending it down to a quick fix, on to a project, or up to an initiative. Nobody has to decide the size themselves.

Without the ladders you get the month-long "quick fix" that was never small, and the thing built with no system to belong to, so that six weeks later nobody knows where its documents are or who may change its data.

## Why six kinds

A form wired to a board is not proved the way an app is, and neither is proved the way a document is. So proof is by kind, not by size. The kit knows six kinds of built thing, and each one has its own way of being shown to work.

- An **automation** is rented tools wired together. It is proved by replaying it through its real entry point, the form or the trigger that really starts it.
- A **service** is your own code that runs on its own with no screen. It is proved by tests, a live probe of the running thing, and a forced failure that its noticer, whatever tells a person that something broke, actually reports.
- An **application** is your own code with a screen that people sign into. It is proved by a real browser walking the real screens through the real login, plus checks that read its live data.
- A **tool** is your own code that a person runs by hand to produce an output. It is proved by tests on fixtures and one check of its output against real data.
- A **procedure** is instructions that Claude, the assistant doing the building, follows. It is proved by a cold read, a fresh session with no memory running it from the file alone.
- **Knowledge** is something people read. It is proved by review against a verification table, one row per claim beside the source that confirms it. This document is knowledge, and its table is the last section.

Because the kit asks the kind first, it can provision exactly the documents that kind needs and reach for exactly that kind's proof, without the person knowing the taxonomy. What goes wrong when kind is ignored is a checklist written for one kind applied to another. Every box gets ticked, and nothing has been proved.

## Why one state layer, and why position is kept apart from history

Every project and every initiative has one state file, and it is the only place where position is written. It is rewritten in place at every stop, under a word budget, and it is never appended. Everything that happened goes into the record, the project's log, which is appended and never edited, and never read to find out where we are. At every stop the handoff card says the same five things:

- where we are on the ladder of work;
- what just got done, and how it was proved;
- exactly what to type next;
- what only the owner can do;
- where all of this is written down.

```chain
a session ends → the state file is rewritten → the next session reads only the state file
```

The reason is measured. Before the split, a session that had to work out where a build stood rebuilt that picture from six to ten history-shaped documents, spending anywhere from tens of thousands to well over a hundred thousand words of reading, and re-reading the same files fifteen to thirty times inside one conversation. A snapshot of a few hundred words, checked against the live files in minutes, orients a fresh session and costs almost nothing.

What goes wrong is either of the two habits the split forbids. Appending to the state file turns the snapshot back into a history, and reading the record to find your place costs the very time the snapshot was made to save.

## Why shipped is not reached

Ship proves the build is safe to rely on. It does not prove that the problem in the memo was solved, and nothing else in the lifecycle checks that. So the outcome check does. On a set date after go-live, the memo's success definition is checked against real people using the thing, and only then does the milestone read *reached*.

```chain
queued → memo cleared → PRD approved → building → shipped → **reached**
```

Without it, "done" gets called at ship. The loop back to the memo never closes, and a thing can be live, stable and unused for months while everyone believes the problem is behind them.

## Why four layers, and where each one lives

This document sorts the kit's content into four layers and gives each layer one home, so nobody has to wonder which file to change or which file an update will overwrite.

**Method:** in the commands. They are written once for everyone and the kit refreshes them, so they are best left unedited; your own rules for a command go in a file of your own that the kit reads and never writes.
**Judgment:** in your folders: your map, each folder's index, your additions to a command. An update never touches them.
**Proof:** at the gates, in writing, by a person. Nothing is done without the proof its kind requires, and no gate clears without a document someone approves.
**Position:** in one state file per project, a few hundred words saying where it stands, rewritten in place. A fresh session orients from it, never from history.

Without the split, an update overwrites a rule you wrote, and nobody can say which file is the kit's and which is yours; the receipt the installer keeps is what tells them apart.

## What you bring, and what the skills carry

You are not expected to know how to build anything technically. The skills carry that load. Your part is the part no tool can do for you.

| You decide | The skills handle |
|---|---|
| What is worth building. | Designing the pieces. |
| What "done" means. | Checking the technical assumptions against the live system. |
| What it is *not*. | Writing the actual thing. |
| Whether the stakes are acceptable. | Keeping the documents current. |

Say what you are trying to do, answer the gates honestly, and the kit does the rest. If partway through something turns out bigger or harder than expected, a skill stops and tells you, and points you back to the door. That is not failure. It is the system catching the problem while it is cheap to fix.

## Where each why comes from

| Claim | Source that confirms it |
|---|---|
| The one-breath sentence: describe the thing, the kit names its kind, three gates, position apart from history, a check afterwards | the initiative's north star, §1 |
| "Complexity is the enemy" is the kit's one idea, kept word for word | the June explainer, "The one idea"; the initiative's north star, §2 principle 6 |
| Builds go wrong by doing too much too soon; the kit catches it while it is cheap | the June explainer, "The one idea" |
| A gate checks itself; nobody grants passage | the June explainer, "Why gates?" |
| Gate 1 asks "should this exist?" and covers problem, cost of inaction, value, why now, what it is and is not, and the success definition | `glossary.md`, "Gate 1, the memo" |
| Gate 2 asks "is it designed right?" and checks every dependency against the live system | `glossary.md`, "Gate 2, the PRD" |
| Gate 3 asks "is it safe for other people to rely on?" and runs only when blast radius crosses the line | `glossary.md`, "Gate 3, ship" |
| Blast radius is four questions, and one yes means Gate 3 | `glossary.md`, "Blast radius" |
| The router asks the four questions at the end of every build and quick fix | `glossary.md`, "Router" |
| The gates fire at different moments because some questions are only worth asking after earlier ones | the June explainer, "Why gates?" |
| Gate 1 asks what the thing is in one sentence; a memo that says "do not build this" is a win; skipping it turns a weekend idea into a month-long swamp | the June explainer, "Gate 1" |
| Gate 2 reuses what exists, and its test is whether you can explain the thing in a short paragraph or draw it | the June explainer, "Gate 2" |
| If no blast-radius answer is yes the thing is a toy; if any is yes it does not go live until the failure questions are answered | the June explainer, "Gate 3" |
| The ship review asks six things, of which what breaks, who notices and the fallback are three | `glossary.md`, "Gate 3, ship" |
| The lifecycle runs memo, PRD, build, ship, outcome check | `documentation_standard.md`, §4 (the planning-folder contract, and the milestone states) |
| The ladder of work is session, work item, project, milestone, initiative | `glossary.md`, "The ladder of work" |
| The ladder of what exists is part, system, workspace | `glossary.md`, "Part, system, workspace" |
| A session is one conversation from opening the chat to closing it, and it does one work item at a time, stopping when its measured size says a fresh start is cheaper | `glossary.md`, "Session"; "Work item"; "Session boundary" |
| Work items make a project, a project reaches one milestone, and milestones that build on each other make an initiative | `glossary.md`, "Project", "Milestone", "Initiative" |
| Every built thing has an index that says what it is, what lives in it, and how to pick it up in a fresh session | `glossary.md`, "CONTEXT.md"; `documentation_standard.md`, §5 (the required local index) |
| Every build intent starts at the door, which sizes the work so nobody sizes their own | `glossary.md`, "The door"; `documentation_standard.md`, §4 (the planning-folder contract) |
| Proof is by kind, not by size | the initiative's north star, §2 principle 7 |
| The six kinds and what each one is | `glossary.md`, "The kinds" (six rows) |
| The proof each kind must pass | `documentation_standard.md`, §4 (the kinds table); `glossary.md`, "Real entry point", "Cold read", "Verification table", "Live invariant", "Smoke test", "Noticer" |
| The kit asks the kind at intake and provisions and proves by it, without the person knowing the taxonomy | the initiative's north star, §5 ("Kinds decide the document set, the proof and the practices"); §7, milestone 1's "reached when" |
| Every project and every initiative has one state file; it is the only place position lives; rewritten, never appended, under a budget | `glossary.md`, "State file"; `documentation_standard.md`, §4 ("Three levels, one snapshot each") and §6 ("State is a snapshot, history is a log") |
| A fresh session orients from the state file and its checks in minutes | `glossary.md`, "Orient"; the initiative's north star, §1 |
| The record is the project's log, appended, never edited, and never read for position | `glossary.md`, "Record" |
| The handoff card says the same five things at every stop | `glossary.md`, "Handoff card" |
| Sessions rebuilt their position from six to ten history-shaped documents, at a cost between tens of thousands and well over a hundred thousand words of reading, re-reading the same files fifteen to thirty times | `documentation_standard.md`, §4 ("State split from history 2026-09-20": 27k–237k tokens of orientation per session, the same files re-read 15–29 times) |
| Ship proves safe to rely on, not that the problem was solved; the outcome check is the only step that checks that | the shared close procedure (`project_close.md`), §5; `glossary.md`, "Outcome check" |
| A milestone is shipped when live and reached only when the outcome check confirms the success definition | `glossary.md`, "Milestone"; `documentation_standard.md`, §4 (the milestone states) |
| You decide what is worth building, what done means, what it is not, whether the stakes are acceptable; the skills design, check, write and keep the documents | the June explainer, "What you bring vs. what the skills handle" |
| When something turns out too big, a skill stops and points back to the starting place, which is the door | the June explainer, "When it gets too big"; `glossary.md`, "The door" |
| The kit's own files are refreshed by its updater and a file you changed is kept, with the kit's version written beside it; your own rules for a command go in a file the kit reads and never writes | `update-build-kit/SKILL.md`, "What ships" and "Step 2: Verify"; the initiative's north star, §5 (the box) |
| Your map, your skills list and the folders you made are never read or written by an update | `update-build-kit/SKILL.md`, description and "How it works" |
| The commands are written once for everyone | the initiative's north star, §2 principle 4 and §7 milestone 2 ("written once") |
| An update once overwrote a person's edits; the installer's receipt now records every kit-placed file so the kit's files and yours can be told apart | `ship/SKILL.md`, "Phase 3: DISPOSITION" (the Accept row's managed-file example); `install.sh`, header comment (receipts, the package-manager rule) |
| A gate is cleared in writing by a person, and nothing is done without the proof its kind requires | `memo/SKILL.md`, "Close: hand off or pause"; `prd/SKILL.md`, "Present for approval"; `ship/SKILL.md`, "Definition of done"; the initiative's north star, §2 principle 7 |
| Position lives in one state file per project, rewritten in place, and a fresh session orients from it, never from history | `glossary.md`, "State file", "Record"; `documentation_standard.md`, §6 "State is a snapshot, history is a log" |
