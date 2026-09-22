---
name: doc-audit
description: Comprehensive docs-vs-reality audit — fan-out agents diff every living doc against ground truth (CONTEXT file-tables vs actual folders, workflow master tables vs the live automation tool, the data dictionary vs the live schema, deploy facts vs running systems, practices pointers vs existing files). Trigger-based, not calendar-based — run before major builds (/memo for anything big), after long gaps, or whenever the workspace feels drifty. Output: defect list with proposed fixes, applied on approval.
user_invocable: true
---

# /doc-audit — verify the map matches the territory

**Purpose:** the living-doc rule is a promise; this skill tests it. Continuous verification happens at-touch (tier-1: "doc friction is a doc defect") — this is the deep sweep for everything usage doesn't touch. The first run of it is recorded below the marker.

**Scope:** one area (`/doc-audit <folder>`) or the whole workspace (`/doc-audit`).

**Cadence:** monthly full sweep (a recurring task in the task manager) + on-trigger (before major builds, after long gaps, when drifty). The monthly run may scope to the workspaces touched that month; the contracts class (below) always runs for any workspace with a contracts doc.

## Method

Fan out read-only Explore agents, one per verification class (parallel; facts only, no fixes — Type-1 agents per `_practices/subagents.md`):

1. **Index integrity:** every CONTEXT.md's file-table and points-up/points-down links vs. the actual folder (`ls`) — missing entries, dead links, files present but unindexed, disposables that outlived their job.
2. **Live-system tables:** workflow master tables vs. the live automation tool's API (IDs, names, active state); the data dictionary vs. the live schema (by the generator that writes it, where one exists); deploy facts (URLs, service names) vs. running systems where probeable read-only.
3. **Lifecycle hygiene:** live memo/PRD trays vs. archives (unfiled shipped work, live/archive twins, "In Progress" logs with stale dates); `_practices/` pointers in CONTEXT.mds vs. files that actually exist.
4. **State leakage:** grep for backlog/TODO/open-questions sections re-accumulating in markdown (they belong in the task manager).
5. **Cross-system contracts** (the PRD-grade class): for each boundary documented in `system_contracts.md` (or the workspace's contracts doc), contract-test it against LIVE state — fetch the producer's actual output shape and the consumer's actual expectation (live workflow JSON, live schema, live API responses) and diff both against what the contract doc claims. Method: `_practices/integration-audit.md`; same observe-live-never-infer discipline as `/prd` Phase 1. This is the class that catches the dangerous drift — a contract doc that's wrong is worse than one that's missing.
6. **Kind conformance** (added 2026-09-20 with the kinds axis, `documentation_standard.md` §4 "The third axis"): every system `CONTEXT.md` created from 2026-09-20 carries a **Kind** and a **Proved by** line; a composite's Kind paragraph names every module or job under its code root that another folder documents, and that folder's index points back. An older index without the lines is a class-B gap, never a class-A defect, per the standard's "Existing indexes" rule.
## Then

- Classify findings: **A** doc contradicts reality (fix required) · **B** doc incomplete (index gap) · **C** hygiene (stale/unfiled).
- Present the full defect list with proposed fixes as ONE batch → apply on approval, one commit per class.
- Anything revealing a *process* leak (not just a doc defect) → flag it: the fix is upstream in a skill or standard, not in the doc.

## Rules

- Read-only until approval. Never "improve" docs beyond the found defects (surgical changes).
- Zero-finding classes get reported too — "verified clean" is a result (class-sweep completeness).
- Findings about live systems follow hypothesis-before-fix: verify against the source before labeling a doc wrong.
