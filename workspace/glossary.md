# Glossary — every lifecycle term, in one plain sentence

**Canonical.** When a document in this workspace uses one of these words, it means exactly this. A term that is not here is defined where it first appears and added here the same session. Written for a non-technical teammate first; if a definition needs another term, that term is in this glossary too. Contract: `documentation_standard.md` §6, "Plain language, fully said".

## How big is the work — from the smallest piece to the largest

| Term | What it means |
|---|---|
| **Session** | One conversation with Claude, from opening the chat to closing it. A session begins by reading the state file and ends by rewriting it and printing a handoff card. |
| **Work item** | One bounded piece of a project's design, kept inside one system (it does not reach across into another), that promises one output. A session does one work item, then carries on into the next or stops, as the handoff card's Context line decides: the measured size of the conversation so far, and whether a fresh one would be cheaper. |
| **Quick fix** | A small change that needs no design, run with `/quick-fix`. Either the problem is known, nothing new is being designed, and three or fewer files or settings change; or it is a chore, a known routine with no design question (such as closing an initiative), however many things it touches. It ends with the same exit check as a full build. |
| **Build** | The step where the design is turned into the real thing, one work item at a time, run with `/build`. In everyday speech it also means the thing being made. |
| **Project** | The work that reaches one milestone, or a standalone build: one memo, one PRD, one build, a ship review when the blast radius asks for it, one outcome check. While it is in flight it lives in `_admin/prds/<project>/`. |
| **Milestone** | A point on an initiative's roadmap, its written plan of projects in order, that says what will be true when one project ships. A milestone is *shipped* when the code is live and *reached* when the outcome check confirms the memo's success definition. |
| **Initiative** | A large build made of several milestones that build on each other, replacing or retiring systems over months. It is planned in one folder that holds a north star (its purpose and plan), a state file and an index (its CONTEXT.md). |
| **Where every idea starts** | Every idea starts with `/memo`, which works out how big it is and where it goes next: a small known change goes to a quick fix, one build becomes a project, and several builds become an initiative. Nobody has to decide the size themselves. |
| **The two size questions** | How big is this piece of work: a fix, a project, or several projects (with sessions and work items inside)? And how big is the thing being built: a part, a system, or a workspace? The first is about work, the second about things. |

## The checkpoints — the questions a build must answer before it moves on

| Term | What it means |
|---|---|
| **Checkpoint** | A question you must answer before you move on to the next step. It grades itself: if you cannot answer it, you have not passed, and you will know it yourself. When you can, the answer is written down and the owner approves it. There are three; the third runs only when the blast radius says a mistake would travel. |
| **Checkpoint 1, the memo** | "Should this exist?" The memo states the problem, what doing nothing costs, what solving it is worth, why now, what the thing is and what it is *not*, and how we will know it worked. It never says how. |
| **Checkpoint 2, the PRD** | "Is it designed right?" The PRD, short for product requirements document, is a verified picture of what exists today, a clear statement of what done looks like, and the smallest bridge between the two, with every dependency checked against the live system before anything is built. |
| **PRD** | Short for product requirements document: the written design that answers Checkpoint 2, made before anything is built. |
| **Checkpoint 3, the ship review** | "Is it safe for other people to rely on?" The ship review is the last check before the thing goes live. It runs only when the blast radius crosses the line, meaning at least one blast-radius question is answered yes, and it asks six things: what breaks, who notices, what the fallback is, what the contingency is, how we fix it, and what the tests conclude about things they never examined. |
| **Outcome check** | The loop back to Checkpoint 1. On a set date after go-live, the memo's success definition is checked against real people using the thing. Shipped is not the same as reached. |
| **Blast radius** | How far a mistake would travel. Four questions: does someone other than you depend on it, does it change real data, is its output used to make decisions, does it touch money or people outside. One yes means Checkpoint 3. |
| **Router** | The check at the end of a build or a quick fix that asks the four blast-radius questions and decides whether Checkpoint 3 is needed. It is also called the exit check. |
| **Success definition** | The memo's sentence "we will know this is solved when …", written so that it can actually be checked. The outcome check checks it. |
| **One-shot** | A build that needs no scope decisions because the PRD already made them all. A scope decision during a build means the PRD was not finished. |
| **Exit check** | Another name for the router: the four blast-radius questions asked at the end of every build and every quick fix, before anything goes live. |
| **Go-live** | The moment other people start relying on the thing, when it is published, deployed or switched on for them. |
| **Residual** | Something noticed at a stop and left unresolved, written on the handoff card with whether it needs attention now. |

## The documents — what each one is for

| Term | What it means |
|---|---|
| **North star** | An initiative's compass and founding document. It says why the whole effort exists, what it broadly sets out to improve, what must never get worse, and the inventory of everything it will build, in order, where each item is a project with its own memo, PRD and build. It holds decisions and never progress. Each project's memo points into it instead of restating why the effort exists. |
| **State file** (`state.md`) | A short note that says where a project (or an initiative) stands right now: what is done, what is next, and what is waiting on someone. It is rewritten every time something moves, kept to a few hundred words, and it is the only place that says where the work stands. The log is the diary, never read for that. |
| **Record** (`project_log.md`, the daily log) | What happened, appended and never edited. A record is never read to find out where we are; the state file is. |
| **Contract** | The document that says exactly what we are building: the PRD for a project, the north star for an initiative. |
| **The tray** ("what the next project inherits") | The part of an initiative's state file that lists what the next project depends on: what is live, which switches are still held, what is undecided, which human steps are outstanding, and which facts were verified. An item leaves the tray when it is decided, given a home in a system document, or done. |
| **Handoff card** | The card printed at every stop (a work item done, a checkpoint cleared, a wait on the owner, or the end of a session), as markdown: where the work sits and how far it has come (every milestone and work item marked done, current or to do), what just got done and how it was proved, every task filed and every residual left with whether each needs attention now, what only the owner can do, exactly what to type next with its Context line (which measures how full the conversation is and says whether to carry on or start fresh), and, last, where it was all written down. |
| **Context line** | The line on a handoff card that measures how full the conversation is and says whether to carry on in it or start a fresh one, which is cheaper once a conversation grows long. |
| **Orientation card** | The same card printed at the start of a session that resumes earlier work, before any other work: what the session will do, how far the work has come, what the checks found, what it inherits, and where it will stop. A misread is caught there, at the cost of a sentence. |
| **Companion** | The HTML page generated beside a checkpoint document (a memo, a PRD, a project log's ship review, a state file's handoff) so a person can approve from it without reading the markdown. The markdown stays the source; the skill that writes the document regenerates the page, and no one edits it by hand. |
| **The explainer** (`why_we_build.md`) | The one document that says why we build this way: three checkpoints, two size questions, six kinds of thing, and one short note that says where the work stands, and what goes wrong when each is ignored. It ships with the kit, its page is generated from it like a companion, and it never says where any project stands. |
| **Worked example** (`worked_example.md`) | One build walked start to finish in the kit's own words, so a new person sees what each step asks and what it hands back before they run one. It ships with the kit and its page is generated from it. |
| **The lifecycle map** (`lifecycle_map.md`) | The one page that shows the whole way of working at once: both ways to start, the three checkpoints, the initiative as a roadmap of projects, and the loop that closes only at the outcome check, with what each stage asks, produces and costs when skipped. It ships with the kit, its page is generated from it, and it never says where any project stands. |
| **CONTEXT.md** | The index of a folder: what this is, what lives here, and how to pick the work up in a fresh session. It never holds position and never holds decisions. |
| **system_contracts.md** | Every place where data crosses from one system to another: who writes it, who reads it, what each field means, and which single system owns it. |
| **decision_log.md** | Why things were built the way they were, one numbered and dated entry per decision, never edited afterwards. |
| **change_log.md** | What shipped, written for a human reader. |
| **data_dictionary.md** | Every table and column a workspace owns, generated from the database's own descriptions so it cannot drift. |
| **flow.html** | The clickable diagram of a process: its steps, who owns each one, and what hands off to what. |
| **Practices** (`_practices/`) | How a tool behaves anywhere, learned once and written down, loaded the moment that tool is touched. Each tool in the stack has one. |
| **The standards** | The three canonical documents: how documents are structured (`documentation_standard.md`), how processes are designed (`workflow_design_standard.md`), and how quality is proved on code (`testing_standard.md`). |
| **Planning folder** (`_admin/<initiative>/`) | The home of an initiative: its north star, its state file, its index, and its research inputs. |
| **Archive** | Where a closed project goes, whole: the PRD, the record and the final state file, moved and never copied. |
| **The skeleton** | The folders a workspace or area has from the day it is created, before any document goes in them; listed once in the template library. |
| **Living vs disposable** | A living document is kept true at the moment something changes. A disposable document is deleted the moment its job is done. Nothing sits in between. |

## The kinds — what a built thing is made of

| Term | What it means |
|---|---|
| **Automation** | Tools you rent, wired together, such as a workflow tool, a board, a form builder and a chat app. You own the wiring and the contracts between them, not the machines they run on. |
| **Service** | Your own code that runs on its own with no screen: a worker, a scheduled job, a bot. |
| **Application** | Your own code with a screen that people sign into. |
| **Tool** | Your own code that a person runs by hand to produce an output, such as a report or a file. |
| **Procedure** | Instructions that Claude follows: a skill, a hook, a ritual. |
| **The pipeline form** | A repeating process built as numbered stage folders, each with one named human check, instead of one skill; `/new-workflow` chooses it when the process has reviewed stages. |
| **Knowledge** | Something people read: a runbook, a lesson, a reference shelf, a mockup. |
| **Composite system** | One system made of several kinds that ship as one unit and own one set of data, such as a service with an application on top. Its index must say which part is which kind and where each part's code lives. |
| **System of systems** | Several systems that share a database or exchange data. Because they will drift apart, they need eight things the standard lists: one data core or explicit contracts, one writer per object, a contract at every boundary, a decision log and change log at the root, drift detection and repair, a noticer that sees across systems, an index that routes, and rules for moving behaviour between systems. |
| **Part, system, workspace** | How big the thing being built is: a part of a system, a system that does one job, and a workspace, the folder that holds all your systems. |

## How we prove that something works

| Term | What it means |
|---|---|
| **Real entry point** | The way a real user or a real trigger reaches the thing. Proof through it counts. A made-up call that skips the real way in proves only the piece it called, not the whole path to it. |
| **Handoff test** | Copy the folder to a fresh session with no memory. If work continues from the files alone, the documents pass. |
| **Cold read** | Asking a fresh session with no memory to orient itself from the files and report back what it understood. It is how the handoff test is run. |
| **Verification table** | A table with one row per claim a document makes and, beside it, the source that confirms the claim. It is how knowledge is proved: a reviewer checks each row against its source. |
| **Live invariant** | A test that reads the real database and checks a property that must always hold, never a specific number. |
| **Smoke test** | A real browser walking the real screens through the real login, with a disposable account that leaves nothing behind. |
| **Reconcile lane** | A procedure that finds where two systems have drifted apart, works out the cause, and repairs it. A lane that goes quiet is the proof that the old writer is gone. |
| **Noticer** | Whatever tells a person that something failed: a line in the daily digest with an owner and a next action. A failure with no noticer is a hole. |
| **Bulk write** | Any change to more than ten rows, or any backfill, restore or recompute. |
| **Prestate snapshot** | A copy of the affected rows, taken before a bulk write, so the write can be undone. |

## Ways of working

| Term | What it means |
|---|---|
| **Orient** | The first minutes of a session: read the state file, run the three checks it names, and print the orientation card. |
| **Session boundary** | The rule that at the end of every work item the state file is rewritten and a handoff card printed, and the session carries on or ends as the card's measured Context line decides; a session that ends leaves the next one to start fresh from the state file. |
| **Capture at occurrence** | Write a lesson down the moment it happens, in the tool's practice file if it is about the tool and in the project's index if it is about the project. |
| **Provision** | Create exactly the documents a thing needs, from the templates, and nothing more. |
| **Brownfield and greenfield** | Bringing something that already exists up to standard by observing what is actually deployed, versus starting a new thing from a clean sheet. |
| **Tier 1, 2, 3** | What loads always (the root CLAUDE.md), what loads when an activity starts (skills and practices), and what loads when you enter a folder (its documents). |
| **Minimum viable architecture (MVA)** | The smallest set of documents, checkpoints, practices and habits that lets an agentic harness build reliable systems and hand them between sessions and people. The kit is this. |
| **Agentic harness** | The environment in which Claude reads files, runs tools and follows skills. Claude Code is one. |
| **Skill** | A command you type in Claude Code, such as `/memo` or `/build`, whose written instructions Claude follows step by step. |
| **The kit** | The set of skills, standards and pages this glossary belongs to, installed into your workspace so that every build follows the same steps. |
| **The owner** | The person whose workspace this is and whose word the checkpoints wait on. Every workspace names its owner in its root CLAUDE.md under "Words the skills use"; skills and templates say "the owner" and write that name, so a handoff card reads "Needs Maria" in Maria's workspace. |
| **The task manager** | The one tool where every task, date and open question lives, never in any other markdown file (when no app is connected, `tasks.md` at the workspace root is the task manager). Named in the root CLAUDE.md beside the owner, with its filing rules; skills say "the task manager" and "task id" and file there. |
