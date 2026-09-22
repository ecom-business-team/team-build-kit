# The lifecycle map

_Every door in, the three gates, one loop that closes only when the problem is solved._

This page is the map of the kit: the commands and standards you install, and the loop every piece of work moves through. You come in once, through one of two doors.

1. You want to build something new. The first door makes a place for it to live.
2. You already have something, and you want to bring it up to the standard. The second door looks at what you have and writes down what is missing.

Either way you arrive at the memo, a short written case for the build. The memo decides how big the work is, so you never have to. A small fix goes straight to a quick fix. A build that fits one project gets designed in a PRD, the design document, then built, and, if other people will rely on it, reviewed before it goes live. A build too big for one project becomes an initiative: a roadmap of projects, where each project runs the whole loop on its own. Every build passes the gates it needs, and nothing is finished until the outcome check says the problem the memo named is gone. Open any stage below to see what it asks, what it produces, and what goes wrong without it.

## The map

```map
node I   1,2       :: install / then /onboard
node N   2,1       :: /new-workspace / something new
node C   2,3       :: /convert-to-standard / something you have
node M   3,2 gate  :: /memo / worth doing?
node SZ  4,2 check :: how big is it?
node Q   5,1       :: /quick-fix / no design needed
node P   5,2 gate  :: /prd / designed right?
box  INI 5,4-7,4   :: an initiative: a roadmap of projects, one state file for the whole
node M1  5,4       :: milestone 1 / a project
node M2  6,4       :: milestone 2 / a project
node M3  7,4       :: milestone n / a project
node B   6,2       :: /build / make it work
node R   7,2 check :: blast radius?
node S   8,3 gate  :: /ship / safe to rely on?
node CL  9,2       :: close / and archive
node OC  10,2      :: outcome check / on its date
node D   10,1 end  :: reached
I -> N
I -> C
N -> M
C -> M
M -> SZ
SZ -> Q :: a small fix
SZ -> P :: one project
SZ -> INI :: several projects
M1 -> M2
M2 -> M3
INI ..> M :: each milestone runs the full loop from the memo
P -> B
B -> R
Q -> R
R -> CL :: only you
R -> S :: others rely on it
S -> CL
CL -> OC
OC -> D :: success definition true
OC ..> M :: not reached: back to the memo
```

```map
node K1 1,1       :: a command / what it does
node K2 2,1 gate  :: a gate / a person clears it
node K3 3,1 check :: a question
node K4 4,1 end   :: reached
```

- A plain box is a command you run, with what it does under its name.
- A dark box is a gate. A person clears it, in writing, before anything continues. There are three.
- A diamond is a question the kit answers for you. The first asks how big the work is; the second asks how far a mistake would travel.
- The outlined pill is the only end state. Reached means the memo's success definition came true in real use.

The dashed lines are the returns. Each milestone of an initiative comes back to the memo and runs the full loop as a project of its own. An outcome check that finds the problem still there sends you back to the memo too: a defect becomes a quick fix or a new project, and a wrong success definition corrects the memo. A quick fix leaves the map after the blast-radius question; close, archive and the outcome check belong to projects.

```chain
Every session, every day, every week: /session-close → /day → /week
```

Every session ends the same way: a log line, and when a project is in flight, the state file rewritten and a handoff card printed. The day's log is processed once a day and the week's once a week, so what one session learned is where the next one will look.

## Install, then /onboard — the whole way of working in one conversation

> **In plain words:** One command places the kit's files, and one interview turns them into a workspace of your own.

**Asks.**

- The install asks nothing. It places every file on the kit's list, all of them or none, and keeps a receipt of what it placed.
- The interview asks who you are and what you build, what to call you, where your tasks live, and where shared keys will live.
- It shows you the plan of folders before it creates anything, and waits for your yes.
- The first time the folder is opened, one prompt asks whether to trust the folder's hooks.

**Produces.**

- A workspace of your own, beside the kit, never inside it.
- In it, the standards, the glossary, the explainer, the worked example, the practice notes, and five small hooks that keep notes about sessions and read your own additions to a command.
- Your map, the file that tells every session where things live, with one routing row per area of your work. And your skills list.
- Each area of your work, created to the standard.
- The folders every workspace has from its first day, before any document goes in them: one for bulk changes with its index, and a task list when your tasks live in a file rather than a tool.
- A check that your task manager works: one test task filed, read back and completed, or a task list in a file when that fails.
- The whole workspace saved once in version control, so every later change can be undone in one step.
- A receipt, so a later update refreshes what you left alone and keeps what you changed, with the kit's new version placed beside it.
- A handoff card that names the first thing to do.

**Without it.**

1. **First:** the commands point at files that are not there, so every session starts from nothing.
2. **Then:** each person builds to a different standard, because no standard is in the room.
3. **In the end:** the way of working lives in one person's head, and every new teammate has to be walked through it by hand.

## /new-workspace — a place for something new

> **In plain words:** Before anyone builds a new thing, this makes the folder and the documents it will need, so the first build has somewhere to land.

**Asks.**

- How big the thing is. A whole workspace, a system, a small leaf inside one, or an initiative, which is a sequence of milestones that build on each other.
- What kind of thing it is made of. An automation, a service, an application, a tool, a procedure, or knowledge. The kind decides which documents it owes and how it is proved.
- For an initiative, a different interview: what will be true when it is finished, whose day changes, which systems are retired and what must never get worse, and the big steps in order.

**Produces.**

- Exactly the document set the level and the kind call for. Nothing missing, nothing extra.
- The area's folders, created empty on the first day: a place for memos, a place for designs and an archive, and for an automation a starting page for its flow diagram.
- An index at the door that says what the thing is, what kind it is, and how it is proved.
- A routing row in your map.
- A handoff card that points at the memo.

**Without it.**

1. **First:** code lands in a folder with no index, and the next session reads the whole tree to learn what is there.
2. **Then:** documents describe what someone assumed was deployed, which is worse than no document at all.
3. **In the end:** two systems quietly write the same field, and nobody can say which one is the source of truth.

## /convert-to-standard — something you already have

> **In plain words:** Something already exists, so this looks at what actually runs, names what kind of thing it is, and writes only the documents it is missing.

**Asks.**

- Only how big the target is.
- It never asks whether the thing exists, because it does. It never asks what kind it is, because the kind is read from what runs.
- After looking, it asks you only what the files and the live system cannot say.

**Produces.**

- Exactly the documents the kind owes, and no more.
- Every line traces to something observed or something you confirmed. A line with no source is cut.
- A handoff card into the lifecycle, so the next change goes through the memo or a quick fix like everything else.

**Without it.**

1. **First:** existing work stays undocumented, or gets documents written from memory that state guesses as facts.
2. **Then:** the next builder designs on a description that was never true.
3. **In the end:** a change breaks a consumer nobody knew existed, because no document named it.

## /memo — worth doing?

> **In plain words:** Every build starts here. The memo asks whether the thing should exist at all, and it works out how big the work is, so you do not have to.

**Asks.**

- First, it looks for the thing. It reads your map, your skills list, the memos and designs already written, and the area's index. If what you describe already exists or is already being built, it names the file and asks whether this is that thing or a different one.
- What the problem is, what doing nothing costs, what solving it is worth, and why now.
- What the thing is, in one sentence, and what it is deliberately not.
- How you will know it is solved, written so it can be checked later.
- How big it is. A throwaway, a thing only you depend on, or a change you can undo in one step is waved through with no memo; the map does not draw these, you simply do them. A contained fix is sent to a quick fix.
- Whether it is really several things. Three signs: success takes several releases that build on each other; systems are replaced or retired over months; the boundary keeps growing. Two of the three make it an initiative.

**Produces.**

- A short memo the owner approves. It says what and why, never how.
- Its honest answer may be "do not build". That is a good memo, not a failed one.
- A route: down to a quick fix, on to the design gate, or up to an initiative.
- Inside an initiative, each milestone comes back through this same door with a short memo that points into the north star instead of repeating it.

**Without it.**

1. **First:** building starts on an idea, so the first design decision is made by whoever happens to be typing.
2. **Then:** nobody can say afterwards whether it worked, because success was never defined.
3. **In the end:** a shelf of things that were built but never needed, each one owing maintenance.

## /quick-fix — no design needed

> **In plain words:** When the problem is known and nothing new has to be designed, this fixes it without a project. It still asks the blast-radius question before anything goes live.

**Asks.**

- What is actually wrong, read from the live system before anything is changed.
- How many things must change. More than about three, and it stops and sends you to the memo.
- It refuses a change that needs new tables or new architecture, or that spans several systems or several sessions.

**Produces.**

- A verified fix.
- The living documents it touched, brought up to date. No project folder, no log, no decision entries.
- Before go-live, the same blast-radius question as a full build. If a mistake would travel, the six questions of the ship review, described below, are answered right there, in a paragraph, and every "nothing" or "don't know" is fixed now or sent to the memo.

**Without it.**

1. **First:** every small defect becomes a project, or every small defect skips every check.
2. **Then:** fixes that write real data go live on discipline alone.
3. **In the end:** a fix that looked contained turns out to be three things, and the design happens inside the fix.

## The initiative — too big for one project

> **In plain words:** When the memo says the build is too big for one project, it becomes a roadmap of projects. One place knows where the whole thing stands, and each project runs the full loop on its own.

**Asks.**

- The north star. What will be true when it is finished, whose day changes, which systems are retired and what must never get worse, and the milestones in order.
- It asks for decisions, never for progress.

**Produces.**

- A planning folder with three documents. The north star, which also serves as the initiative's memo. One state file for the whole initiative. An index.
- One project per milestone. Each has its own memo, its own PRD, its own build, its own blast-radius check, and its own outcome check.
- The roadmap holds the order and the reasons, never status. Status lives in the state file's milestone table. A milestone moves from queued, to memo cleared, to PRD approved, to building, to shipped, and only after the outcome check, to reached.
- A tray, handed from each finished project to the next. What is live, what is held, what is undecided, what is verified.

**Without it.**

1. **First:** a multi-month effort runs as one giant project, and nothing ships until everything is done.
2. **Then:** decisions made in project two are argued again in project four, because they lived in a chat, not in the north star.
3. **In the end:** every session rebuilds its position from six to ten history-shaped documents, re-reading the same files up to twenty-nine times.

## /prd — designed right?

> **In plain words:** The PRD is the design. Before anything is built, it works out what is true today, what done looks like, and the smallest bridge between the two, and it checks every dependency against the live system.

**Asks.**

- What is true today. Observed from the live systems, never inferred from documents or memory alone.
- What done looks like.
- The smallest path that reuses what already exists. This is asked before any grander design is allowed.
- Whether every dependency on another system really responds the way the design assumes. Each one is called or inspected.
- Who consumes any value the design changes, including the platform's own automations that nobody lists.
- The rigor pass, which includes the blast radius and a pre-mortem.

**Produces.**

- A PRD that a fresh session can build from alone, with work items that build in one shot and no scope decision left over.
- A validation log of every dependency probed.
- An impact map and a pre-mortem, which the ship review reuses later.
- Its companion page, and the project's state file.

**Without it.**

1. **First:** the build discovers the real schema, the real contract, and the real consumer halfway through.
2. **Then:** scope changes mid-build, and each change is a design decision made without the design's context.
3. **In the end:** things nobody can explain get built, and when they break nobody can fix them.

## /build — make it work

> **In plain words:** The build is pure execution. It builds one work item per session, proves each one the way its kind is proved, and ends by asking the blast-radius question.

**Asks.**

- Nothing new. It reads the state file and the PRD, section by section, and executes.
- If a scope decision surfaces here, the PRD was not finished. The build stops and goes back upstream instead of deciding in place.
- At the end, the blast-radius question.

**Produces.**

- Each work item proved the way its kind is proved. A test, a replay through the real entry point, a browser check through the real login, or a cold read.
- The living documents updated as the territory changes.
- At every work-item boundary: the log appended, the state file rewritten in place, the handoff card printed, and the session stopped there.
- A route: close itself when a mistake would travel nowhere, or hand to the ship review.

**Without it.**

1. **First:** "done" means the code ran once on the builder's machine.
2. **Then:** position lives in the chat, so the next session works it out again from history, or guesses.
3. **In the end:** work is redone, contradicted, or silently abandoned between sessions.

## /ship — safe to rely on?

> **In plain words:** When other people will rely on the build, this asks what happens when it goes wrong. Nothing goes live until every hole has an answer.

**Asks.**

- It runs only when the blast-radius question says a mistake would travel: someone else depends on it, it writes real data, its output drives decisions, or it touches money or people outside. Otherwise there is no ship review.
- Six questions, in writing. What breaks. Who notices. What the fallback is. What the contingency is. How we fix it. And what a test that checked a sample tells us about the items it never looked at.
- For every hole: fix it now, send the design back to the PRD or the memo, or accept it with the owner's explicit sign-off. A hole with no decision blocks go-live.

**Produces.**

- A written review that a fresh reader can audit.
- A go-live that can be undone in one step, a smoke test in production, and monitoring confirmed to have fired.
- The shared close: provisional lessons, living documents brought current, the project archived, the milestone marked shipped, the tray refilled, the outcome check scheduled, and a handoff card.

**Without it.**

1. **First:** something fails in production and nobody is told.
2. **Then:** a number someone acted on was wrong, and the decision it drove stands.
3. **In the end:** a hole that was quietly tolerated becomes exactly the failure the gate existed to prevent.

## The outcome check — on its date

> **In plain words:** Shipping proves the build is safe. Only this checks whether the memo's problem is actually gone, with real people using the thing.

**Asks.**

- Each point of the memo's success definition, verified through the real entry point and never the test suite alone.
- It runs the day after the date the definition names, or fourteen days after go-live.
- It is a task in the task manager, and any session can run it. If the launch moves, the task moves with it.

**Produces.**

- Reached: the milestone row reads reached, and the archived log gains an Outcome section with the evidence.
- Not reached: a defect goes to a quick fix or a new project. A wrong success definition is corrected in the memo. "Not yet" is rescheduled once, with the reason given. Until then the milestone stays shipped.

**Without it.**

1. **First:** "done" gets called at ship, and the loop back to the memo never closes.
2. **Then:** a thing is live, stable and unused for months while everyone believes the problem is behind them.
3. **In the end:** the next memo is written about the symptoms of a problem the last build was meant to solve.

## /session-close, /day, /week — keep what each session learned

> **In plain words:** Every session ends the same way, and the day and the week are processed on a rhythm, so a lesson learned once is found again the next time it is needed.

**Asks.**

- At every close: at least one log line, the state file rewritten if a project is in flight, and the living documents checked against what changed.
- Once a day: which learnings move to their canonical home, and which open threads become tasks. A learning without a document change or a filed task did not happen.
- Once a week: what repeats, the biggest recurring friction and one action for it, and what to propose for your map or for the kit. Proposals only, never edits.

**Produces.**

- A daily log that is a short index of what happened, never a copy of what lives elsewhere.
- A digest per day and a summary per week, each ending with what needs the owner.

**Without it.**

1. **First:** the lesson leaves with the session that learned it.
2. **Then:** the same open thread appears in log after log with no task filed.
3. **In the end:** the method never improves, because nothing feeds it.

## Also in the kit, off the loop

Three commands sit beside the loop rather than on it. Run `/doc-audit` before a big build, after a long gap, or whenever the workspace feels drifty. It checks every living document against what is really there and proposes fixes. Run `/new-workflow` when a process repeats. It turns the steps into a command of your own, or, when a person checks the output of more than one stage and the process has run at least twice, into a pipeline of numbered stage folders, each with its one human check. Run `/update-build-kit` to refresh the kit's files without touching your map, your skills list, or the folders you made.

## Where each stage comes from

| Claim | Source that confirms it |
|---|---|
| Two doors in: one for something new, one for something you already have; both end at the same place | `convert-to-standard/SKILL.md`, opening paragraph ("the door for existing work; `/new-workspace` is the door for new work; both end at the same place") |
| The memo decides the size: down to a quick fix, on to a project, up to an initiative | `memo/SKILL.md`, "When the memo is too small — the initiative test" ("the one door with three exits"); `glossary.md`, "The door" |
| Nothing is finished until the outcome check confirms the memo's success definition; shipped is not reached | `glossary.md`, "Outcome check", "Milestone"; `why_we_build.md`, "Why shipped is not reached" |
| There are three gates, each cleared in writing by a person: the memo and the PRD are approved before the next step, and the written ship review is the audit surface | `memo/SKILL.md`, "Close: hand off or pause" ("Once approved"); `prd/SKILL.md`, "Present for approval"; `ship/SKILL.md`, "Definition of done" ("This is the human review gate… The written review is the audit surface") |
| Each milestone of an initiative runs the full loop from the memo as its own project | `documentation_standard.md`, §4 "Planning folder" ("Each project runs `/memo` → `/prd` → `/build` → `/ship`"); `memo/SKILL.md`, "Two forms" |
| An outcome check that is not reached sends you back to the memo: a defect becomes a quick fix or a new project, a wrong definition amends the memo, and only "not yet" reschedules | `_shared/project_close.md`, §5 "Running the check" item 3 |
| The blast-radius question decides whether the ship review runs at all; it asks how far a mistake would travel | `ship/SKILL.md`, "Trigger" ("If none fire, there is no `/ship`"); `glossary.md`, "Blast radius", "Router" |
| The memo's three exits are by size: a small fix, one project, several projects | `memo/SKILL.md`, "When you can SKIP the memo" (a contained fix → `/quick-fix`); "The initiative test" ("the one door with three exits") |
| The ship branch is taken when others rely on the build; when only you do, the build closes itself | `ship/SKILL.md`, "Trigger"; `build/SKILL.md`, "Phase 4: BLAST-RADIUS ROUTER" ("If none fire → ship freely") |
| Every session ends with a log line, and when a project is in flight the state file is rewritten and a handoff card printed; the day and the week are processed on a rhythm | `session-close/SKILL.md`, §1 and §2 item 9; `day/SKILL.md` and `week/SKILL.md`, "When" (the rhythm) and "Steps" |
| The install places every listed file or nothing, and keeps a receipt of what it placed; an update refreshes unchanged files and keeps changed ones, writing the kit's version beside them | `install.sh`, header comment (atomic; receipts; `.kit-new`, "the package-manager rule") |
| The install asks nothing; the workspace is made beside the kit, never inside it | `install.sh` (no prompt; its inputs are environment variables); `onboard/SKILL.md`, "Phase 4" 4a ("Where the workspace goes") |
| The interview asks who you are and what you build, what to call you, where your tasks live, and where shared keys live; it shows the plan before creating anything | `onboard/SKILL.md`, "Phase 2: UNDERSTAND THE PERSON" (questions 1–6); "Phase 4: CONFIRM AND CREATE" 4a |
| The workspace holds the skeleton folders from its first day, the task manager is proved by one test task (or a task list in a file), and the workspace is committed once | `onboard/SKILL.md`, "Phase 4" 4b step 3 ("Create the skeleton"), step 5 ("Prove the task manager"), step 8 ("Commit"); `_shared/documentation_standard.md`, "The skeleton — folders that exist from day one" |
| One prompt asks once whether to trust the folder's hooks | `onboard/SKILL.md`, "Phase 4" 4b step 9 |
| The workspace holds the standards, the glossary, the explainer, the worked example, the practice notes and five hooks; your map with a routing row per area; your skills list; each area created to the standard; a handoff card naming the next step | `onboard/SKILL.md`, "Phase 4" (the folder map, the five-hooks sentence, 4b steps 2, 4, 6 and 7, the handoff `Next:` line); `update-build-kit/SKILL.md`, the paragraph naming the workspace files; the kit's MANIFEST (`workspace/worked_example.md` and its page) |
| Without the kit's files the commands point at files that are not there | `update-build-kit/SKILL.md`, the sentence on the four core skills depending on the shared standard being present |
| The levels are workspace, system, leaf and initiative; the level question includes "one build, or a sequence of shippable milestones"; the kind decides the documents and the proof | `new-workspace/SKILL.md`, "The three things this skill resolves"; "Phase 1: DISCERN — level, fork, kind"; `documentation_standard.md`, §4 "The third axis: kind" |
| The six kinds are automation, service, application, tool, procedure, knowledge | `documentation_standard.md`, §4 "The third axis: kind" (the kinds table) |
| The north-star interview asks what will be true, whose day changes, what dies and must never get worse, and the steps in order with what is true at each | `new-workspace/SKILL.md`, "Phase 2a: GREENFIELD" ("For an initiative — the north-star interview") |
| It provisions exactly the document set for the level and kind, nothing missing and nothing unearned, with the kind and proof stated; a routing row is added; the handoff points at the memo | `new-workspace/SKILL.md`, "Phase 3: PROVISION" items 1–5; "Phase 5: HANDOFF"; `convert-to-standard/SKILL.md`, "Phase 3" (the Kind and Proved-by lines, the routing row) |
| The area's folders are created empty by level and kind, with a flow page for an automation, and the index check passes | `new-workspace/SKILL.md`, "Phase 3: PROVISION" item 3 ("Create the area's folders"); "Phase 4: VERIFY" item 6 |
| A document that describes what you assume is deployed is worse than no document | `new-workspace/SKILL.md`, "Principles" ("Accurate or cut") |
| Every built thing has an index that says what it is and how to pick it up; without one the tree has to be read | `documentation_standard.md`, §5 "CONTEXT.md — the required local index"; `why_we_build.md`, "Why two ladders, and why a door" |
| Two systems writing one field is a design flaw; one writer per object | `ship/SKILL.md`, "Phase 3: DISPOSITION" (Escalate: "two systems writing one field"); the initiative's north star, §7 ("a writer registry, one writer per object") |
| Convert asks only the level; never the fork, never the kind; the kind is observed | `convert-to-standard/SKILL.md`, "Phase 1: Confirm the target and its level" |
| It asks the person only what the files and the live system cannot say; every line traces to something observed or confirmed; a line with no source is cut | `convert-to-standard/SKILL.md`, "Phase 2: Observe, then fill gaps"; "Phase 3: Provision and verify"; "Safety Rules" item 5 ("Never lower the bar") |
| Its handoff sends the next change through the memo or a quick fix | `convert-to-standard/SKILL.md`, opening paragraph; "Phase 4: Hand off" (the `Next:` line) |
| An untraced consumer breaks when a change lands | `prd/SKILL.md`, "Phase 6" (the 2026-07-24 lesson: a consumer declared unaffected was never traced) |
| The memo asks the problem, cost of inaction, value, why now, one sentence plus what it is not, and a checkable success definition; it never says how | `memo/SKILL.md`, "The Required Input Contract"; "Definition of done"; `glossary.md`, "Gate 1, the memo", "Success definition" |
| The memo first looks for the thing in the map, the skills list, the memos, the designs and the area's index, and asks whether it is that thing or a different one | `memo/SKILL.md`, "First: does it already exist?" |
| Four cases skip the memo: throwaway, only-you, trivially reversible, a contained fix | `memo/SKILL.md`, "When you can SKIP the memo" |
| Three initiative questions; two of three make it an initiative | `memo/SKILL.md`, "When the memo is too small — the initiative test"; `documentation_standard.md`, §4 "Planning folder" (the contract paragraph) |
| The memo is approved by the owner and its correct conclusion may be "do not build" | `memo/SKILL.md`, "Close: hand off or pause" ("Once approved"); "The Required Input Contract" ("the memo's correct conclusion is don't build"); "The Framework" (The Ask: go/no-go); `why_we_build.md`, "Why gates, and why they check themselves" |
| Inside an initiative each milestone's memo is the short form pointing into the north star | `memo/SKILL.md`, "Two forms" ("a project on an initiative's roadmap") |
| A quick fix skips design and never the exit gate; it reads the live system first, stops at more than about three things, and refuses new tables, several systems, new architecture, or multi-session work | `quick-fix/SKILL.md`, "Phase 3.5" opening sentence; "When NOT to Use"; "Phase 1" Step 2 and Step 3; `glossary.md`, "Quick fix" |
| A quick fix is verified before it goes live, and it has no close, archive or outcome check of its own | `quick-fix/SKILL.md`, "Phase 3: VERIFY"; "Phase 3.5" ("a quick fix has no project log"); "Phase 4" ("Do NOT create: project folders…"); `_shared/project_close.md`, opening ("Who points here: `/build` Phase 5 … and `/ship` Phase 6") |
| A quick fix creates no project folder, log or decision entries, and updates the living documents it touched | `quick-fix/SKILL.md`, "Phase 4: UPDATE LIVING DOCS" |
| A quick fix ends with the same four questions; if any fires, the six answers are given inline in a paragraph; every "nothing" is fixed now or escalated | `quick-fix/SKILL.md`, "Phase 3.5: EXIT GATE" |
| Quick fixes wrote real data on discipline alone before the exit gate | `quick-fix/SKILL.md`, "Phase 3.5" ("Why this exists") |
| A fix that turns out bigger escalates to the memo instead of designing inside the fix | `quick-fix/SKILL.md`, "Scope Escalation" |
| The north star holds decisions, never progress | `glossary.md`, "North star"; `documentation_standard.md`, §4 "Planning folder" (the tree comment on `north_star.md`) |
| The planning folder holds the north star, one state file for the whole and an index; the north star is also the initiative's memo; the roadmap holds order and rationale, never status | `documentation_standard.md`, §4 "Planning folder" and its contract paragraph ("The north star is the initiative's memo"); `glossary.md`, "Initiative", "North star" |
| One project per milestone, each with its own memo, PRD, build, blast-radius check, ship review when needed, and outcome check | `documentation_standard.md`, §4 "Planning folder" (the contract paragraph); `glossary.md`, "Project" |
| A milestone moves queued → memo cleared → PRD approved → building → shipped → reached | `documentation_standard.md`, §4 "Planning folder" ("A milestone's states") |
| The tray lists what is live, what is held, what is undecided, what is verified, and is handed from each project to the next | `glossary.md`, "The tray"; `documentation_standard.md`, §4 "Where an initiative fact lives" ("What a project inherits") |
| Decisions belong in the compass, not in chat | `documentation_standard.md`, §4 "Where an initiative fact lives" ("Decisions" row); `glossary.md`, "North star" |
| Before the state split, sessions rebuilt position from six to ten history-shaped documents, re-reading the same files up to twenty-nine times | `documentation_standard.md`, §4 "Planning folder" (the state-split note); `why_we_build.md`, "Why one state layer" |
| The PRD locks the beginning state from live systems, never from documents or memory alone, then defines what done looks like | `prd/SKILL.md`, "Core disciplines"; "Phase 1: LOCK THE BEGINNING STATE"; "Phase 2: DEFINE THE DESIRED STATE"; `glossary.md`, "Gate 2, the PRD" |
| The minimal path that reuses what exists is a mandatory gate | `prd/SKILL.md`, "Phase 3: MINIMUM-VIABLE DERIVATION (mandatory gate)" |
| Every cross-system dependency is probed live; the platform's own automations are traced as consumers | `prd/SKILL.md`, "Phase 6: MAP COMPONENTS + VERIFY EVERY DEPENDENCY LIVE" |
| The rigor pass covers boundaries, contracts, lifecycles, blast radius and a pre-mortem | `prd/SKILL.md`, "Phase 7: DESIGN RIGOR PASS" (rows 10 and 11); "PRD Format" (§§5–8, 13–14) |
| The PRD is self-contained and one-shot: a fresh session builds from it alone, with no scope decision left | `prd/SKILL.md`, "Definition of done"; "The PRD must be self-contained"; "Phase 8: ONE-SHOT READINESS GATE"; `glossary.md`, "One-shot" |
| The PRD produces a validation log, an impact map, a pre-mortem, its companion page, and the project's state file | `prd/SKILL.md`, "PRD Format" (§§10, 11, 14); "Where to save"; `ship/SKILL.md`, "Prerequisite" (reads the pre-mortem and impact map) |
| Scope changes mid-build are design decisions made without the design's context; the build stops and escalates | `build/SKILL.md`, opening ("Scope decisions during build are failure signals"); "Scope Escalation"; `prd/SKILL.md`, "Phase 6" (the dated lessons) |
| Building what you cannot explain is how you end up unable to fix it | `why_we_build.md`, "Why gates, and why they check themselves" |
| The build orients from the state file (≤400 words, at most three checks) and reads the PRD by section | `build/SKILL.md`, "Phase 1: ORIENT"; `documentation_standard.md`, §6 (the 400-word budget) |
| Each work item is proved the way its kind is proved | `build/SKILL.md`, "Phase 2" Step 2; the initiative's north star, §2 principle 7 |
| Living documents are updated as the territory changes; at every work-item boundary the log is appended, the state file rewritten, the handoff rendered and printed, and the session stops | `build/SKILL.md`, "Phase 2" Step 3, Step 4 and Step 5; "Principles" ("Update the map when you change the territory"); `glossary.md`, "Work item", "Handoff card" |
| The build ends with the four router questions and either closes itself or hands to the ship review | `build/SKILL.md`, "Phase 4: BLAST-RADIUS ROUTER"; "Phase 5: CLOSE"; `glossary.md`, "Router" |
| Position not written to the state file is position lost, and a session that rebuilds it from history re-reads the same documents many times | `session-close/SKILL.md`, §2 item 9 ("Position written only in the log entry is position lost"); `build/SKILL.md`, opening ("don't reconstruct it from memory"); `documentation_standard.md`, §4 "Planning folder" ("rebuilt their position from six to ten history-shaped documents … re-read 15–29 times") |
| Ship runs only when one of the four conditions fires; otherwise there is no ship review | `ship/SKILL.md`, "Trigger"; `glossary.md`, "Blast radius", "Gate 3, ship" |
| The six questions: what breaks, who notices, fallback, contingency, how we fix it, what it concludes without testing | `ship/SKILL.md`, "Phase 2: RESILIENCE REVIEW"; `glossary.md`, "Gate 3, ship" |
| Every hole is fixed now, escalated, or accepted with the owner's sign-off; an undispositioned hole blocks go-live | `ship/SKILL.md`, "Phase 3: DISPOSITION" (the table and the go-live gate) |
| Go-live is undoable in one step, smoke-tested in production, with monitoring confirmed to have fired | `ship/SKILL.md`, "Phase 4: PRE-FLIGHT CHECKS" (Reversibility); "Phase 5: GO LIVE" |
| The shared close: provisional lessons, living documents current, archive, milestone shipped and tray refilled, outcome check scheduled, handoff card | `ship/SKILL.md`, "Phase 6" Step 2; `_shared/project_close.md`, §§1–6 |
| A silent failure is a hole; a quietly tolerated hole is the failure the gate exists to prevent | `ship/SKILL.md`, "Phase 2" ("Who notices?" row and the sentence that every "nothing" is a hole); "Phase 3" (the go-live gate sentence) |
| A wrong number someone acted on is exactly the case the "drives decisions" condition covers | `ship/SKILL.md`, "Trigger" (the third condition and its parenthetical) |
| The outcome check copies the success definition and verifies each point through the real entry point, never the test suite alone, the day after the named date or 14 days after go-live | `_shared/project_close.md`, §5 items 1–3 |
| The check is a task in the task manager, run in any session, moved with the launch and never closed unmet | `_shared/project_close.md`, §5 item 3 and "Running the check" |
| Reached: milestone row → reached, an Outcome section in the archived log, provisional lessons made final; not reached: defect, wrong definition, or not yet, milestone stays shipped | `_shared/project_close.md`, "Running the check" items 2–3; `documentation_standard.md`, §4 "Where an initiative fact lives" (last row) |
| Without the check, "done" is called at ship and a thing can be live, stable and unused for months | `why_we_build.md`, "Why shipped is not reached" |
| Ship proves safety, not that the memo's problem was solved; nothing else checks that | `_shared/project_close.md`, §5 opening sentence |
| Every session logs at least one line; the state file is rewritten if a project is in flight; living documents are checked; the handoff card is what the owner reads | `session-close/SKILL.md`, §1 ("Every session logs"), §2 item 9 |
| Daily: learnings move to their canonical home, open threads become tasks; a learning without a doc change or filed action did not happen | `day/SKILL.md`, "Steps" items 2–3 |
| Weekly: what repeats, one recurring friction and one action, and proposals, never edits, for your map or the kit | `week/SKILL.md`, "Steps" items 2 and 4; "Rules" ("Propose, don't apply, anything touching tier 1 or team-build-kit") |
| The daily log is an index of exhaust, never a copy of what lives in commits, practices or the task manager | `session-close/SKILL.md`, §1 |
| The digest and the summary each end with one section of what needs the owner | `day/SKILL.md`, "Steps" item 5; `week/SKILL.md`, "Steps" item 6 |
| Five small hooks keep notes about sessions and read your own additions to a command | `onboard/SKILL.md`, "Phase 4" 4a (the five-hooks sentence); the kit's MANIFEST (the five `.claude/hooks/` lines) |
| Recurring unfiled threads are the leak the capture layer exists to close | `week/SKILL.md`, "Steps" item 3 |
| `/doc-audit` runs before major builds, after long gaps, or whenever the workspace feels drifty, and proposes fixes | `doc-audit/SKILL.md`, description |
| `/new-workflow` turns a repeating process into a command of your own | `new-workflow/SKILL.md`, description |
| It builds the pipeline form, numbered stage folders each with one human check, when more than one stage is checked and the process has run twice | `new-workflow/SKILL.md`, "Phase 2: MAP THE STEPS" (the shape question); "Phase 4P: BUILD THE PIPELINE" |
| `/update-build-kit` refreshes the kit's files and never touches your map, your skills list or your folders | `update-build-kit/SKILL.md`, description |
| The build makes it work; the ship review makes it safe to rely on | `ship/SKILL.md`, "Principles" |
| Every command the kit ships appears once on this page: eleven on the loop or in the capture strip, three off the loop | the kit's MANIFEST (the `.skills/` lines) |
