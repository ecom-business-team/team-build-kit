---
name: workspace-audit
description: Audit your own workspace against the work you actually did. Reads your saved Claude Code sessions and your instruction files, measures what your rules cost, sorts the costliest rules with four questions, and writes a dated report with three lists (stop, change, add), each item with its evidence and a ready prompt. It changes nothing but the report it saves. Run it monthly, after a new model ships, or whenever the workspace feels heavy. Usage - /workspace-audit [since-date | all]
---

# /workspace-audit

## What it is for

Rules written for a weaker model stay in a workspace after the model no longer needs them. They cost reading, paperwork, filed tasks and waits for approval. This command shows the owner that cost against the work they really did, and names what to stop, what to change and what to add. The principle is **fewer rules, more checks**: when the result can be verified afterwards, the path to it needs no written rule.

**The one rule of this command: it changes nothing.** It writes one report file and nothing else. It never edits, moves or deletes an instruction, never files a task, never commits. Every removal is the owner's decision, made after reading the report.

## 1. The period

- With a date argument, measure sessions since that date. With `all`, measure every saved session.
- With no argument, read the reports in `_admin/audits/` and take the one whose closing numbers line has the latest `measured_to`. Measure since that time, so no session is counted twice. With no earlier report, measure the last 30 days, and say that this run sets the baseline.

## 2. Measure

Run, from the workspace root:

`python3 .claude/tools/session_audit.py --since {date} --report {scratch folder}/audit.json`

- The tool is missing: tell the owner to run `/update-build-kit`, and stop.
- It prints "no sessions found" (exit 1): tell the owner there is nothing to measure in the period, and stop.

Read `audit.json` whole. It holds the summary numbers, one row per session (the first ask, where the edits went, the skills run), the process documents that took the other edits (`process_edits_by_file`), every instruction file with its size and the number of sessions that used it, and the owner's turns flagged as corrections. The tool counts events and matches words. It does not judge whether the work was good, and neither does this report.

## 3. Work out four things

**The work.** Group the sessions into three to seven kinds of work from each session's first ask and its edit folders. For each kind: the number of sessions, the outcome the owner was after (quote one ask, at most 20 words), and where the edits went. A session with no first ask was started by another session; count it under the kind its edits show.

**The cost.** From `summary`: `median_calls_before_first_edit`, `process_edits_pct`, `tasks_filed` against `task_tool_closed`, `approval_only_pct`, `instruction_kchars_per_session`, `hook_kchars_per_session`. Put each beside the same number from the last report's closing block. A first run has no comparison; say so.

**The weight.** From `instruction_files`:
- the ten files with the highest `cost` (size times sessions that used them);
- the files and skills with `sessions_used` of 0, largest first. Unused in this period is not the same as useless: a rule for work that happens twice a year will show 0. Say this once in the report.
- Read `.claude/kit_receipt` when it exists. A file it names belongs to the kit, and an update replaces it. List heavy kit files apart, as feedback for whoever maintains the kit; they never go in the three lists.

**The sort.** Take the five costliest instruction files that the owner wrote (not kit files, not skills). Sort each file's rules with the four questions, one sub agent per file, read-only (`_practices/subagents.md`). Start all five in one message, in the foreground, and write nothing until all five have answered. With no sub agent tool, sort them yourself, one file at a time. Each rule goes into the first group that fits:

1. Claude can see it for itself in the folder or the live system → **DELETE**.
2. A script can say pass or fail → **CHECK**. Name the check in one line.
3. The action cannot be undone → **BLOCK** (stop it before it happens).
4. It is a judgment, or a fact Claude cannot see → **KEEP**, as one short line.

Each sub agent returns the count for each group, and for every rule not in KEEP: its first ten words, its group, and for CHECK the check. The counts are a judgment; two runs differ by a few rules.

## 4. Find the patterns

- **A correction made twice.** Read `flagged_owner_turns`. Two or more on the same subject are a candidate for a check, with both turns quoted.
- **A fact explained more than twice.** Read the first asks. The same background typed into three or more sessions is a candidate for one short note in the map.
- **A wait that repeats.** When `approval_only_pct` is above 15, find which skill ran in the sessions with the most approvals, and name it.

## 5. Write the report

Save it as `_admin/audits/{YYYY-MM-DD}.md` (when today's file exists, `{YYYY-MM-DD}-2.md`, never over an earlier report) in the shape below, then give the owner a summary of at most twelve lines in the chat with a link to the file. Delete `audit.json`.

Rules for the three lists:
- **No evidence, no item.** Every item cites a file with its numbers, or quotes an owner turn with its date.
- **At most five items in each list**, the costliest first. A longer list is not read.
- **Stop** is a rule Claude can see for itself, a file or skill with no use, or a ritual whose output nobody read. **Change** is a rule that becomes a check, a block, or one short line. **Add** is a check for a repeated correction, a short note for a repeated explanation, or a feature of the app that replaces a rule.
- **Every item ends with a ready prompt** in a code block, which the owner pastes to act on that item alone. The prompt names the file and the exact change, and asks Claude to show the change before making it.

```markdown
# Workspace audit · {date}
Period: {first date} to {last date} · {n} sessions · compared with {the last report's date | "no earlier report: this run is the baseline"}

## 1. The work you did
| Kind of work | Sessions | What you were after | Where the edits went |

## 2. What your rules cost
| Measure | This period | Last report | What it means |
(calls before the first edit · share of edits to process documents · tasks filed and closed · approval-only messages · instruction text read per session · text hooks add per session)

## 3. Where the workspace is heavier than the work
- The ten costliest instruction files (size, sessions that used them)
- Not used in this period (and the one-line caution)
- The sort of the five costliest files (per file: delete, check, block, keep)
- Kit files that are heavy (for the kit's maintainer)

## 4. Stop
### {what to stop}
**Why:** … **Evidence:** … 
(the ready prompt, in a code block)

## 5. Change
## 6. Add

## 7. What this report cannot tell you
It counts events and does not judge the work. The correction count is a floor. The sort is a judgment. It sees only work done in Claude Code. A rule's cost is measured; whether it is safe to remove is your call.

Also run `/doctor prompt-audit`, the built-in check for outdated and conflicting instructions.
Next audit: run `/workspace-audit` again after you act on this one. It will compare against this file.

<!-- numbers: {"date": "…", "measured_to": "{measured_to from audit.json}", "sessions": n, "median_calls_before_first_edit": n, "process_edits_pct": n, "tasks_filed": n, "task_tool_closed": n, "approval_only_pct": n, "instruction_kchars_per_session": n, "hook_kchars_per_session": n} -->
```

The last line is what the next run reads. Write it exactly, on one line.
