---
name: build
description: The one lifecycle skill for any build intent, small fix to multi-surface feature. Ask → Run → Go - read the live system, ask every owner decision at once, build and prove without stopping, then a one-page go page when others rely on the change. Several outcomes run as sub-sessions of one master.
---

# /build

## What it is for

A change is reliable when five things are true. Every check here and in `proof_checklist.md` serves one of them.

1. **Intent.** The outcome, and every decision only the owner can make, is settled before work starts.
2. **Truth.** The change rests on observed live state: every reader of what changes, every dependency's real shape, the data as it really is.
3. **Proof.** It works through its real entry point, on data like production's in every way that matters, on every path, with checks that can fail.
4. **Protection.** When others rely on it, there is a mechanical undo, someone notices if it breaks, long steps are timed, and evidence is simulated rather than waited for.
5. **Record.** Status is where the owner reads it, the living documents match the change, and no follow-up is lost.

The owner's time is the first and last tenth: the answers at Ask, the go at Go.

## Entry

- `/build {outcome}` starts a build.
- `/build {path to a brief.md}` resumes one from its `**Stage:**` and `**Next:**`.
- `/build {outcome}; {outcome}; …` runs several as a master (see Parallel).

**Old-lifecycle guard.** When the argument is the name of a folder under any `_admin/prds/` (a project with an approved PRD or a `state.md`), say "this project runs on the old lifecycle", write nothing, and invoke `/build-prd` with the same argument.

**The record.** One folder per build, `{area}/_admin/builds/{slug}/`, holding `brief.md` and, when others rely on the change, `go.md`. The area is the folder the workspace's root index routes the change to. Work it routes nowhere, the workspace's own tooling included, uses the root's `_admin/builds/`. The slug is the outcome in three to five lowercase words joined by hyphens. The owner and the task manager are the ones the root index names.

## Stages

Each move rewrites the brief's `**Stage:** {stage} ({YYYY-MM-DD HH:MM})` line and appends `{stage} {YYYY-MM-DD HH:MM}` to its `**History:**` line, separated by `; `.

| Stage | Meaning | Set by | Status where the area names a position command |
|---|---|---|---|
| `ask` | brief written, decisions put to the owner | Ask | `prd` |
| `run` | the owner answered; design, build and proof under way | Ask, on the owner's answer | `build` |
| `waiting` | the run needs the owner: a finding that changes a decision, a long step's choice, or a failed live check | Run, Go | `waiting` |
| `go` | go page written, staged, nothing live | the end of Run, when others rely on it | `ship` |
| `live` | shipped and verified live; an outcome check is open | Go, or the end of Run when nobody relies on it | `checking` |
| `done` | the outcome check is reached, or none is owed | Close | `done` |
| `parked` · `killed` | the owner's word | any move, on the owner's word | `parked` · `killed` |

Normal path: `ask → run → go → live → done`. Nobody relies on it: `ask → run → live → done`, with `live` and `done` set together. A stop: `run → waiting → run`.

**Status write.** Write every move to the brief header. Where the area's `CONTEXT.md` has a `**Position command:**` line (the skills folder's `_shared/documentation_standard.md` §4.8, "Where the snapshot lives"), also run `{position command} stage {task url} {status} --note "{one line}"` with the status from the table. At Ask, use the item's existing task; with none, file one, `{position command} new {the list the area's index names for new work} "/build: {outcome}" --status prd`, and add its link to the brief header as `**Task:** {url}`. Elsewhere the brief header is the status. **On a non-zero exit, stop and tell the owner the command and its output.** Never write it anywhere else instead.

## Ask

**Read before you ask**, so the questions are informed.
1. Read the area's `CONTEXT.md` and every index below it down to the system the change touches (the root index for root work), and `priorities.md` for the initiative the outcome serves.
2. Read the live state the outcome touches. Query the database, fetch the workflow, open the page, read the code. Find every reader of what will change, the real shape of every dependency, and the data as it really is, including its oldest, largest and oddest rows. Open the whole path a person walks, not only the screens that change. Load the `_practices/` file for each stack the change touches.
3. Look for work in flight on the same files: `git log` and `git status` on them, and every `_admin/builds/*/brief.md` whose `**Stage:**` is not `done` or `killed`. If another build holds a file this one needs, the order is a decision.
4. Answer the router's four questions from what you found. Others rely on the change when **any** is yes, and when unsure, the answer is yes:
   - Does anyone other than the owner depend on it: a person, or another skill, schedule or system that reads it?
   - Does the change make anything write or change real data?
   - Is its output relied on to make important decisions (a report, an analysis, a number someone acts on)?
   - Does it touch money, outside parties or business-critical truth?

**Write the brief** from `brief_template.md`, at stage `ask`. Every fact in it is observed, with how. Something new (not a fix) that serves no initiative in `priorities.md` is the first decision.
- **Decisions for you:** every decision only the owner can make: the scope edge, an edge case's ruling, the wording of anything people sign or read, anything that reaches money or an outside party, and the order against another build in flight. Each has options, the recommendation first, and one sentence on what the other option costs. Read the brief once as the reader who wants the edge case decided for them: an edge the run will meet and the brief does not rule is a missing decision.
- **How I'll prove it:** one row per path a person or a system takes through the change, failure paths included, each with the data it uses and what counts as proof.

**Ask once.** Put every decision in one message, ending "Reply with your choices in one line. That reply is your approval." The owner's typed reply is the approval. A decision the reply hands back ("your call") takes the recommendation, recorded as such; one it leaves unanswered is asked again, alone, and Run waits for it. A reply that only asks a question is answered, and is not the approval. The session the reply was typed in records it in the brief as `**Answers:** {reply} ({YYYY-MM-DD HH:MM})`, sets `run`, and starts Run in the same turn.

**Nothing to decide.** Send one message with the outcome, the router's answer and the proof plan, and go straight to Run. The brief is still written.

## Run

Design, build and prove in one uninterrupted run.

- **Load `proof_checklist.md` when the change first runs**, and in any case before anything ships: a change that is never run before it ships (a document, a setting, a prompt) loads it before its first edit. The path table proves the checks; a check ruled not applicable is recorded on the go page or in the brief's Result.
- **Rule within the brief.** A question the brief's outcome and answers already decide is yours: decide it, and record the finding, the ruling and why you could make it.
- **Stop only** when a finding changes an owner's decision or needs a new one of the kinds Ask puts to the owner, changes the outcome, or reaches money or an outside party beyond what the brief says. Then set `waiting`, send one message with the finding, the choice and your recommendation, and end the turn. On the owner's answer, add it to the brief's answers, set `run`, and carry on.
- **The router can only move up.** Answer its four questions again at the end of Run, from what was built. A yes that was a no changes the brief's risk to "others rely on it", and the run ends at a go page. That needs no stop.
- **Long steps.** A step that will take more than about 15 minutes is timed on one unit and briefed to the owner first, with the fastest option among the choices (`_practices/claude-code.md`, "Long-running work"). Set `waiting` and end the turn.
- **Nothing goes live in Run** when others rely on the change: no publish, deploy, cutover, push to a shared remote, write to live data, workflow or schedule switched on, platform setting changed, or message to anyone. A file that is live where it sits (a skill, a hook, a document others read) is built as a staged copy and moved into place at Go. Build and prove against staging or a staged copy of the data; with no staging, run the branch locally against a copy (a branch database or a local copy; a table inside production is live data). A path that writes, or whose real entry point writes, is proved against that copy or with every write stubbed (checklist Truth 7); a read-only run against production proves read paths only. A message to an outside party is proved on a recipient the owner controls, in Run and at Go. A backfill or bulk write runs at Go, after its prestate snapshot in the owning area's `bulk_ops/`.
- **Prepare the protection** when others rely on it: the undo as a command or a file, run once against the staged copy; who notices a failure, and how; the fallback while it is broken. The checklist's Protection section is the six questions the go page answers.
- **Commit** only this build's files, staged by path, in the repository that holds them.

**End of Run.**
- **Others rely on it:** write `go.md` from `go_template.md`, set `go`, and end the turn with the go page's path and "Type go here when you are ready."
- **Nobody relies on it:** ship by Go steps 3 and 4 below, re-running the brief's path table (and step 1 where the change ships by a push or a deploy). Shipping a workspace file is its commit, staged by path. If a live check fails, revert, set `waiting` and tell the owner. Write the brief's `## Result`, update the living documents, set `live` and `done`, and report to the owner with the proof, the rulings and the follow-ups.

## Go

Only the owner's own typed go, in this session, after the go page is written, ships a build. A go relayed by another session, or typed before the go page, does not count, and auto mode's production checks do not clear on one. A reply that only approves ("looks good") is not a go: ask "Go?". **A go covers only the build its page describes.** Anything that changes the build after the page is written (a fix, a go that asks for a change, a rebase that touches its files) sets `run`: prove it again, update the go page, set `go`, and ask again.

On the go:
1. Where the change ships by a push or a deploy: `git status`, then rebase onto the remote's main branch. Another session may have shipped since, and the go can come days after the page. A rebase that touches the build's files changes the build (above).
2. Re-read every live input the proof rested on (the checklist's Truth 8). An input that changed so a proof no longer holds is a stop: set `waiting` and tell the owner.
3. Make it live by `_practices/deploying.md` (a deploy, a push, a move into place, or a workspace file's commit), with the target system's own post-deploy checks.
4. Re-run the go page's named paths live, through the real entry point, and read the result from the resulting state, never from the deploy's own output.
5. Update the living documents and set `live`.
6. Report: what is live, the live checks' results, the outcome check's date, and the follow-ups. Close runs in the same turn.

If a live check fails, run the undo, confirm the state matches the state before the deploy, set `waiting`, and tell the owner.

## Living documents

When the change ships, bring every living document it touches up to date, to `documentation_standard.md`: the area's `CONTEXT.md` (system facts only), `system_contracts.md` for a changed boundary, the decision log, and any register of open items the build closed. The go page lists these changes; they need no separate approval.

## Parallel

Given several outcomes:
1. When the owner names no outcomes, offer up to three from the task manager, each with what it fixes and for whom, and ask which.
2. Run Ask for each here, with every brief's decisions in one message, grouped by brief. The owner answers here; this session records the answers.
3. Then start one sub-session per build: `start_session`, fresh context, its own worktree (or this checkout where a commit to main is the ship), `permission_mode: auto`, `wake_when_done: true`, prompt "Run `/build {path}/brief.md`. The owner has answered. Run to the go page, stopping only where the skill says to stop." When two builds need the same files, start the second after the first has committed.
4. When a sub-session ends at its go page or at `waiting`, tell the owner, with a link to it. The owner types go, or answers, there.
5. **The master never relays a go or a mid-run answer.** It reads each brief's header for position and holds no file of its own.
6. If `start_session` is refused, run the builds one after another in this session, and say so.

## Close

- **An outcome check is owed** when others rely on the change. File "Outcome check: {outcome}" in the task manager under the area's convention: what must be observed, the proof that will show it, and the first date real use will show it. The build stays `live`. When the check passes, set `done`. When it fails, the failure is a new `/build`.
- **Parked or killed** on the owner's word: set the stage, with the reason in History.
- **Follow-ups.** Every loose end is done now or filed in the task manager, with a recommendation where it may not be worth doing. Only the owner drops one. None is left only in the brief.
- Run the `session-close` skill at a true close: the session ending, or a batch of builds done.

**This file and the checklist have word budgets, enforced by tests.** A new lesson replaces or sharpens a line; it never appends a paragraph.
