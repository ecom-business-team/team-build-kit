# Project close — one procedure, two entry points

**Who points here:** `/build` Phase 5 (the blast-radius router was clean, so the build ships itself) and `/ship` Phase 6 (the router fired, Gate 3 cleared, go-live is done). Both run this file top to bottom. The procedure lives once so it cannot drift between the two skills — it did, twice, on 2026-09-20.

A project has three end states. **Complete** — it shipped; the normal path, §1–§6. **Killed** — the owner decided it will not ship; §K. **Paused** — not an end state: work stopped waiting on a person or a decision; §P, and the project stays in flight.

## 1. Learning capture (provisional)
Ask the owner: what worked · what was painful · what to do differently. Append to `project_log.md` under **Lessons Learned** and mark them *provisional — written before real use; the outcome check (§5) adds what real use showed*. If a lesson suggests a change to a mental model, a checklist or a skill, propose the specific change now; these compound.

## 2. Final documentation
- Close the register entries this build satisfied (the missing-wires / open-inputs table the workspace's PRDs read first): mark each built wire closed with what built it; downgrade any that turned out to be a data or decision problem rather than a missing wire.
- Remaining living-doc updates — CONTEXT.md, `system_contracts.md`, decision log, changelog — to the Documentation Standard. **System facts only** in system docs; position stays in `state.md`.
- `project_log.md`: Status → **Complete**, completion date, deferred follow-ups (each a task in the task manager, by id).
- Project `state.md`: Position → complete; Stage ribbon `memo ✅ · PRD ✅ · build N/N · ship ✅ (or n/a) · close ✅ · outcome ☐ (due {date})`.

## 3. Archive — BLOCKING (filing is enforcement, not ceremony)
Always **move**, never copy — a copy left in the live tray becomes a divergent fork (one audit found five of them).
- `{workspace}/_admin/prds/{project}/` → `{workspace}/_admin/_archive/{project}/` — the PRD, `project_log.md` and the final `state.md` travel together.
- `{workspace}/_admin/memos/{project}.md` and its companion `{project}.html` → `{workspace}/_admin/memos/_done/`, together (the page moves with its source; if the memo has no companion yet, render it first with the command in §4).
- Verify: `ls` both live trays — nothing of this project remains. If filing cannot happen, say so explicitly; never close silently unfiled.

## 4. Initiative state (skip for a standalone project)
Rewrite `{workspace}/_admin/{initiative}/state.md`:
- Milestone row → `shipped {date} · outcome check due {date}`, pointing at the log's Go-live section.
- In flight → none · Next to open → the roadmap's next milestone (→ `/memo`).
- The handed-forward tray gains this project's **held switches**, **undecided** items (task ids), **human steps outstanding** (in order, dated), the **verified facts** later projects rest on (one line each, source in brackets), and an **Outcome checks pending** line (§5).
Budget 600 words; the state gate warns past it. An item leaves the tray when decided, homed, or done.
Then render its companion: `python3 ~/.claude/skills/_shared/companion/render.py {workspace}/_admin/{initiative}/state.md` writes `handoff.html` beside it (the milestones and the tray); then open the page in the default browser when the machine has an opener (`open` on macOS, `xdg-open` on Linux; skip silently otherwise), so it is on screen the moment the document is written.

## 5. Schedule the outcome check (the loop back to Gate 1)
Ship proves the build is safe to rely on. It does not prove the memo's problem is solved, and nothing else in the lifecycle checks that, so this step does:
1. Copy the memo's **Success Definition** verbatim.
2. Pick the check date: the day after the date the success definition itself names, if it names one; otherwise **14 days after go-live**. The window exists because outcome evidence is real people doing real things, which takes days, not a smoke run.
3. Create a task in the task manager, in the workspace's project — title `Outcome check: {project} — verify the memo's success definition against live use`, due on the check date, labelled actionable as the workspace's CLAUDE.md task rules say. Its description carries: the success definition point by point; for each point **how to verify it through the real entry point** (a live query, a real user's event, a digest reading — never the test suite alone); what "reached" looks like; the rule *if the launch moves, reschedule this task with it — never close it unmet*; and where to record (below).
4. Write the same line into the initiative tray under **Outcome checks pending** (milestone · due · task id) — or, for a standalone project, into the archived `project_log.md` Status.

### Running the check (when the task fires — any session)
1. Read the task. Verify each point of the success definition against live data, through the real entry point. Record the evidence.
2. **Reached:** milestone row → `reached {date}` (pointer to the evidence); remove the item from the tray; append an **Outcome** section to the archived `project_log.md` — what the memo predicted, what happened, the evidence — and turn the provisional lessons into final ones (what the Ship Review predicted against what real use showed). Promote anything general to `_practices/` or a standard. Close the task.
3. **Not reached:** name the gap per point. A gap that is a defect → `/quick-fix` or a new project. A gap that is a wrong success definition → say so and amend the memo in `_done/` with a dated note. A gap that is "not yet" → reschedule once, with the reason. The milestone stays `shipped` until reached.
4. Print the handoff card.

## 6. Handoff card
Template §4.10: Where = project close ✅ · outcome ☐ due {date}; Done = what shipped and how it was proved; Next = the roadmap's next milestone — run: `/memo {name}` in a fresh session — or the human steps that gate the launch, in order; Needs {owner} = every accepted residual and keyboard step with its task id; Written = the initiative `state.md`.

## K. Killing a project
Only on the owner's explicit word, with the reason in their words.
1. `project_log.md`: Status → **Killed {date}** — the reason; what was built and is live (each object: keep, or remove — a removal of real data follows the bulk-ops snapshot rule); what the memo's problem now waits on.
2. Anything live that the kill would orphan is removed or handed to a named owner **before** archiving. Nothing is left running unowned.
3. Project `state.md`: Position → killed; ribbon ends `· killed`.
4. Archive exactly as §3; the memo moves to `_done/` with one line prepended: *killed {date}: {reason}*.
5. Initiative `state.md`: milestone row → `killed {date} — {reason}`; its tray items removed or re-homed; Next to open reconsidered, and if the roadmap changes, edit `north_star.md` in the same session. Render its companion as in §4.
6. Handoff card: Next = the decision the kill leaves open, or the next milestone.

## P. Pausing a project (not a close)
1. Project `state.md`: Position → `Paused {date} — waiting on {who or what} · task id · resume when {condition}`; Stage ribbon unchanged; Next = `resume: {the first thing to do}`.
2. Initiative `state.md`: milestone row → `paused {date} (waiting on …)`. Render its companion as in §4.
3. The project stays in `prds/` and the SessionStart gate keeps printing it, by design: a paused project is still in flight and should stay visible. If it will not resume, kill it (§K).
