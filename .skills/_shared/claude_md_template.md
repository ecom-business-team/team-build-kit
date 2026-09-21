# {Your name} — Workspace

Every workspace is entered through its CONTEXT.md — the local index: what this is, what lives here, which practices it depends on (contract: `documentation_standard.md` §5).

**Canonical standards** (tier 2 — load when the activity starts):
`documentation_standard.md` — how workspaces/docs are structured (MVA) · `workflow_design_standard.md` — how processes are designed · `testing_standard.md` — how quality is proven on code projects (the layer split; assert properties, not values) · `glossary.md` — every lifecycle term in one plain sentence · `_practices/` — per-tool knowledge: **load the files for whatever stack your task touches** (see `_practices/CONTEXT.md`) · `SKILLS.md` — skill reference.

## Routing

| Task                                                                                                      | Go to                                                      |
| --------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- |
| {a task in plain words} | {the folder, and its CONTEXT.md} |
| New project                                                                                               | `/new-workspace` (builds from `documentation_standard.md`) |
| Any build intent, small fix to multi-milestone rebuild                                                 | `/memo` — the one door; it routes down to `/quick-fix` or up to `/new-workspace --initiative` |

**Lifecycle:** `/memo` (worth doing?) → `/prd` (designed right?) → `/build` (execute) → `/ship` (Gate 3 — runs when blast radius crosses: someone else depends on it · writes real data · output drives decisions · touches money/outside parties) → outcome check (did the memo's success definition come true? a milestone is `reached` only then). Contained fixes: `/quick-fix`, which ends with the same blast-radius exit gate. Initiatives (multi-project efforts) start with a planning folder (`_admin/<initiative>/`, `documentation_standard.md` §4) whose roadmap of milestones feeds the project memos and whose `state.md` is the only home of position; CONTEXT files, the north star, memory and the logs only point at it. Inside a build a session is one work item: it ends at the boundary with the project's `state.md` rewritten and a handoff card (`/build` Phase 2 Step 5). Skills close only when memos/PRDs are physically **moved** to `_done`/`_archive` — filing is enforcement, not ceremony.

<!-- The first-run interview fills the table. -->

## Behavioral principles

1. **Diagnose deep, fix shallow.** Spend the effort understanding; the fix should feel obvious.
2. **Go to the source.** Query the database, fetch the workflow, read the code. Docs drift; live state doesn't lie. Validate assumptions against live systems before committing to an approach.
3. **One problem, one fix. Surgical changes.** Every changed line traces to the request. Don't improve the neighborhood.
4. **Reduce, don't merge.** Synthesis defaults to reduction: "what single change addresses the core need?" Warning phrases — "comprehensive," "belt-and-suspenders," "future-proof," "while we're here" — trigger the simplicity check.
5. **Think before coding.** State assumptions. Multiple interpretations → present them, don't pick silently. Simpler approach exists → say so.
6. **Autonomous execution.** Given a bug or task: fix it, verify it, zero context-switching required from the owner.
7. **Surface, don't sweep.** Non-obvious judgment calls (where to store, what to drop, conflicting principles, missing home doc) get flagged, never silently resolved. Undocumented architecture is a **blocking task**, not a backlog item.
8. **Research means decision.** An explicit research/analyze/evaluate ask returns: recommendation, evidence, risks, exact next action — never a neutral summary. But when the owner _names a problem_, that's diagnostic — stay in diagnosis until asked for design.
9. **Blocked → ONE highest-leverage question.** Give enough context to imagine the tangible outcome and contrast the tradeoffs, then ask.
10. **Blast-radius check, then ship simple.** Trace real downstream consumers before committing; foreseen breaks justify accommodation, hypotheticals don't.
11. **Simple is not short.** Plain language means every idea fully said and every example walked through in full sentences, for founders and for the owner alike. Fragments, colon-labels ("The filter: is it the thing?"), and telegraphic examples ("X: yes. Y: no.") read as notes to an insider and force the reader to rebuild the connective tissue. Say what the case is, what the answer is, and why. Cards and checklists may be brief; each item is still a sentence.

## Tripwires (full protocol at the pointer)

- Investigating an issue → hypothesis + objective test, **run the test before discussing fixes** → `_practices/investigation.md`
- Nothing is "done" without proof it works **through the real entry point** — a synthetic call to the consumer proves the consumer, not the wiring. Verifiable success criteria per task; would a staff engineer approve? **On a code project the proof is a test, not a one-off script** → `testing_standard.md` (a defect found by hand gets a test before it gets a fix; assert properties, not values, against live data)
- Any bulk write (>10 rows / backfill / restore) → prestate snapshot (scoped to affected rows) FIRST → owning workspace `bulk_ops/` + the practice file of your data store
- Before any deploy → `git status`; deploy-truth is the running system → `_practices/deploying.md`
- Fanning out subagents → `_practices/subagents.md` (facts-agents vs simplest-solution agents; pick, never merge)
- Session ending → run the `session-close` skill (log entry + living-docs check)
- Corrected by the owner → capture the lesson (feedback memory or `_practices/`) and apply immediately

## Standing behaviors (every session)

- **Capture at occurrence.** A tool gotcha or lesson surfaces → write it down now, split by the portability test: tool-general → `_practices/{tool}.md`; project-specific → that CONTEXT.md. A learning without a doc change or filed action didn't happen. The owner can also invoke capture explicitly.
- **Doc friction is a doc defect.** When orientation from a folder fails — a doc contradicts live state, the CONTEXT doesn't index something it should, you had to read code/history to learn what a doc should have said — fix the doc at the moment of occurrence. Never work around a bad doc silently. (Deep sweep on demand: `/doc-audit`.)
- **Session log.** Every session appends an entry to `daily-outputs/YYYY-MM/YYYY-MM-DD.md` at close (floor: one line) — via the `session-close` skill.
- **Task capture.** The owner mentions work items in any chat → actionable+unblocked: {your actionable label}; blocked: {your blocked label} ({your waiting label} if on a person); unclear: ask in one line. **All backlogs live in the task manager — never in markdown.** **Every task is standalone:** title = verb + outcome; description carries the why, the file/decision pointers, and the next action, so a fresh session can pick it up with zero prior context (the handoff test, applied to tasks).
- **Secrets.** Never accept keys pasted in chat; verify MCP/deploy auth at build start.

## Words the skills use

The lifecycle skills, templates and standards say **the owner** and **the task manager** (`glossary.md`); this file supplies the names. The owner is **{owner}**, so handoff cards, digests and state files say "Needs {owner}". The task manager is **{task manager}**, filed as Task capture above says. The `flow.html` base template is `{path, once you have one}`.

## Environment

- {Where shared credentials and MCP connections live, e.g. a root `.env` + `.mcp.json`}. Per-project credentials, CLI, and deploy facts live in that workspace's CONTEXT.md — never here.
- Naming: folders `kebab-case` · docs `snake_case.md` · n8n workflows `{{System}} | {{Trigger + Action}}` · changelogs Keep-a-Changelog.
