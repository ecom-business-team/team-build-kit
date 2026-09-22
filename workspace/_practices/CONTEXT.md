# _practices/ — Stack-Practices Layer

Cross-project tool knowledge: how each tool in the stack behaves **anywhere**, learned once, retrieved at the moment of need. Tier 2 of the context architecture (see `documentation_standard.md`).

**Placement rule (the portability test):** a fact lives here only if it would still be true if any one project were deleted. Project parameters (service names, credentials locations, IDs, deploy commands) live in that project's CONTEXT.md, which links the practice files it depends on.

**Capture:** automatic standing behavior — gotchas are appended here at the moment of occurrence (split from their project-specific half at capture). The owner can also invoke capture explicitly. A learning without a doc change or filed action didn't happen.

**Loading:** two mechanisms. (1) Mechanical — the PreToolUse practices gate (`.claude/hooks/practices_gate.py`) injects the matching file into context on the first Supabase / n8n / Railway / Vercel / Google / ClickUp / Discord call of a session (once per file per session). (2) Navigational — each workspace CONTEXT.md lists its practice files ("deploys via Vercel → read `vercel.md` first") as the human-readable dependency list. Sessions load per-tool, on trigger — never all of this folder.

**Method practices** — how to work, whatever the stack. These ship with the kit.

| File | Covers |
|------|--------|
| deploying.md | Cross-host deploy truths (working-tree deploys, deploy-truth-is-live-state) |
| llm-workflows.md | Architecture principles for LLM-judgment systems |
| integration-audit.md | The 6-step cross-system integration audit |
| investigation.md | Hypothesis-driven investigation protocol (full text behind the tier-1 tripwire) |
| subagents.md | Subagent strategy — ground-truth vs simplest-solution agents |
| claude-code.md | The harness itself: hook events (what can inject context, timeouts, Stop-fires-per-turn), transcript JSONL shape, settings; **silent no-ops** (an unmatched `str.replace()`, an options object in the wrong argument slot) |

**Tool practices** — how one tool behaves anywhere. Yours accumulate below this line as you learn them, one file per tool, named after the tool (`vercel.md`, `supabase.md`); the practices gate in `.claude/hooks/practices_gate.py` loads a file on the first call to its tool once its name is in the gate's table. The kit ships none: your stack is yours.
