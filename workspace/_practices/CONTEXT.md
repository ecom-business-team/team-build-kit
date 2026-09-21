# _practices/ — Stack-Practices Layer

Cross-project tool knowledge: how each tool in the stack behaves **anywhere**, learned once, retrieved at the moment of need. Tier 2 of the context architecture (see `documentation_standard.md`).

**Placement rule (the portability test):** a fact lives here only if it would still be true if any one project were deleted. Project parameters (service names, credentials locations, IDs, deploy commands) live in that project's CONTEXT.md, which links the practice files it depends on.

**Capture:** automatic standing behavior — gotchas are appended here at the moment of occurrence (split from their project-specific half at capture). The owner can also invoke capture explicitly. A learning without a doc change or filed action didn't happen.

**Loading:** two mechanisms. (1) Mechanical — the PreToolUse practices gate (`.claude/hooks/practices_gate.py`) injects the matching file into context on the first Supabase / n8n / Railway / Vercel / Google / ClickUp / Discord call of a session (once per file per session). (2) Navigational — each workspace CONTEXT.md lists its practice files ("deploys via Vercel → read `vercel.md` first") as the human-readable dependency list. Sessions load per-tool, on trigger — never all of this folder.

| File | Covers |
|------|--------|
| deploying.md | Cross-host deploy truths (working-tree deploys, deploy-truth-is-live-state) |
| vercel.md | Vercel env vars, CLI, git integration, platform limits |
| railway.md | Railway multi-service deploys and verification |
| supabase.md | PostgREST behavior, connection budget, live-data write rules |
| n8n.md | Public REST API editing, MCP editing, node-level patterns |
| google-apis.md | Auth/token flow, Docs updates, shared-drive gotchas |
| clickup.md | Token/credential rotation discipline |
| discord.md | Bot-token API calls from scripts: Cloudflare 1010 / User-Agent, reading + deleting channel messages |
| tally.md | Webhooks are per form and NOT copied on duplicate (silent strand — detect via API totals vs consumer rows); API shape (Cloudflare UA 403, untitled hidden/calculated fields answer as dicts, paging); webhook timeout/retry |
| stripe.md | Hosted Invoices vs 24 h Checkout Sessions; payer-side bank-login failures leave no invoice events; void on out-of-band payment |
| whop.md | Membership LIST omits canceled memberships (resolve by id); v5 shapes, unix timestamps, key on the user id; OIDC discovery; **Whop demands a `nonce` for the `openid` scope and Supabase's custom OIDC provider sends none** |
| wise.md | Balance statements without SCA (proof a payment landed); transfer list has no names; order number ≠ transfer id; profile scoping |
| macos-local-dev.md | This machine: timestamps, iCloud venvs, UI automation; headless Chrome (screenshot loops wedge → one `--print-to-pdf`), HTML deck → PDF → pptx recipe |
| llm-workflows.md | Architecture principles for LLM-judgment systems |
| gemini.md | Files API storage cap (429 file_storage_bytes ≠ rate limit), 48h retention, file-not-ACTIVE 400 |
| meta.md | Marketing API: status vs effective_status, the account activity log (launch/kill events with actor + time; ADGROUP = ad), no created_time from insights, custom-conversion "ROAS" |
| integration-audit.md | The 6-step cross-system integration audit |
| testing-js.md | Vitest + Next (`server-only` does not resolve; layer-per-config), supabase-js needs a WebSocket stub in Node, ESLint ignores hiding the real error count, Playwright smoke traps, Turbopack's persistent dev cache serving stale CSS across restarts (`rm -rf .next/dev`). Method lives in `testing_standard.md` |
| investigation.md | Hypothesis-driven investigation protocol (full text behind the tier-1 tripwire) |
| subagents.md | Subagent strategy — ground-truth vs simplest-solution agents |
| claude-code.md | The harness itself: hook events (what can inject context, timeouts, Stop-fires-per-turn), transcript JSONL shape, settings; **silent no-ops** (an unmatched `str.replace()`, an options object in the wrong argument slot) |

n8n interactive procedure lives in the `n8n-*` skill suite; `n8n.md` holds instance behavior and API/MCP editing knowledge.
