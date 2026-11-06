# Subagent Strategy

Subagents have two distinct purposes — **never blur them.**

## Type 1 — Ground-truth gathering ("what is true?")

One agent per area when the question is "what currently exists?": workflow state, schema, prior decisions, external API behavior. These agents return FACTS, never solutions.

- One area per agent (workflows OR schema OR context — never bundled)
- Read-only — they observe, they don't design
- Independent areas run in parallel; the agent reports facts, you synthesize

## Type 2 — Simplest-solution exploration ("what's the smallest bridge?")

Multiple agents on the SAME problem with IDENTICAL context (problem state, desired end state, Type-1 findings), each with one angle:

| Angle | Framing |
|-------|---------|
| **Subtraction** | Smallest edit to existing artifacts that solves this? |
| **Reuse** | What existing pattern already solves a structurally identical problem? |
| **Elimination** | Can the problem be made not-exist by changing the upstream condition? |
| **External** | Does an existing tool/service/feature solve this so we don't build? |

Each returns ONE candidate simplest solution. **Pick the simplest — NEVER merge.** Merging defeats the purpose; the asymmetry between angles is what surfaces the minimum. Two equally simple proposals with different tradeoffs = a real design decision for the owner. None simple enough = the problem was framed wrong — re-frame before designing.

## Why the split matters

One-agent-per-research-task rewards comprehensive coverage — outputs sum, scope grows through addition. Type 2 rewards finding the minimum — agents compete on simplicity, and the winner is selected, not summed. Use the type that matches the question.

## Side sessions: a relayed go does not authorize a live write

A go-ahead the owner gives in the master session and the master relays to a side session does not pass that session's permission check for a live write: deploys, migrations, env changes, `railway` cutovers. The check wants the owner's own words in the session that runs the write. Found 2026-11-06, in a task-manager burn-down: two production writes were refused in their side session as "Production Deploy" although the owner had said "Go A and B" in the master. So a side session prepares and proves each live write and stops, the master shows the owner what each write does, and the owner then types the go in that session themselves, linked from the master. Read-only work and doc edits in side sessions are unaffected.
