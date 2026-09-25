# Workflow Design Standard

**Canonical.** How processes are designed and verified. Loaded by `/prd` (designing the value stream) and `/build` (Phase 3 end-of-build verification). Not for `/memo` (strategic) or `/quick-fix` (too small). Sibling standard: `documentation_standard.md` (how docs are structured).

## The 6-property step schema

Every step that crosses a system boundary or changes hands between actors must answer all six. Single-actor linear tasks within one system don't need it — a bullet list is fine.

| Property | Question |
|----------|----------|
| **Trigger** | What event starts this step? |
| **Action** | What happens? |
| **Owner** | Who does it? (Person name or "System") |
| **System** | Where does it happen? |
| **Output** | What does it produce? |
| **Handoff** | What does it trigger next? |

Blank property = under-defined step. Vague output ("brand has overview") needs specificity ("brand has program overview with pricing, lifecycle, and terms summary").

## Quality review — three questions about the flow as a whole

1. **What breaks?** For every handoff: what if the next step never happens? How long until someone notices? For every write: what happens if it runs twice?
2. **Who knows?** For every failure: notified, or silent? For every piece of state: where is the source of truth, and can it drift?
3. **What's the fallback?** For every automated step: does a human have a manual path? For every human step: is a system idle waiting, and does anyone know?

## The history rule: every change is recorded

Any build that holds important state records its history in an append-only event log. Important state is anything with a lifecycle, anything touching money or access, and any data other people rely on. The rule has five parts.

1. **What is recorded.** Every change of state and every meaningful action (a login, an approval, an impersonation, a manual correction). Clicks and page views are not history; they belong to product analytics. Requests and errors belong to the platform's logs. Keeping those out keeps the history readable and the database fast.
2. **Who and when.** Each event names its actor (a person, a service or a scheduled job, with an id), who they were acting as during an impersonation, when it happened, and when it was recorded.
3. **What caused it.** Each event carries a correlation id: the one action or job run that set it off. Every event that one action causes shares that id, so a single submission or payout can be read back as one thread from start to finish. This is what replaces a workflow tool's execution history when the tool is retired.
4. **Append-only.** Events are inserted, never edited or deleted. A mistake is corrected by a new event. Write access is limited to the named writers, and the retention period is stated.
5. **Named events, named writers.** Every event type comes from a written catalogue, never free text; the catalogue is the system's list of domain events. Each type names its writer. Prefer a database trigger that can never block the write it watches, so history is kept whichever program changes the table; the application writes the events that are not row changes, such as logins.

**When a system is replaced,** its successor writes the same events, and during the changeover the two streams are compared (a parallel run); the cutover ships only when they match. Before the old system is switched off, list everything it makes observable today (each step, branch and status its runs record), and give each item an event or a job-run record in the new system. Granularity that is not deliberately carried over is lost.

**Why.** This is the common standard, under three names: an audit log (what SOC 2 and ISO 27001 expect for changes to important data), domain events (the business moments a system records), and the event objects of payment platforms such as Stripe, where every change to every object emits a typed, timestamped event. It answers, for any object, what happened, who did it, when, and why, without anyone having to reconstruct it.

## Human review gates

For multi-stage workflows where quality matters more than speed: each stage produces output a human reviews before the next stage consumes it. The intermediate artifact (markdown, JSON, report) IS the communication channel — folder structure is the state machine; no orchestration code.

**Use gates for:** hybrid workflows where errors cascade across systems · content going to external stakeholders · multi-step skill sequences where each output feeds the next.
**Skip gates for:** fully automated system-to-system flows · internal tasks where speed wins · single steps with built-in verification.

## HTML flow diagrams

Each process system gets an interactive `flow.html` in its own folder — the detailed design reference. Structure:
- Phases as sections with colored step nodes; each node clickable → expands to the 6-property schema
- Color-coded by owner (automated=teal; manual by person=amber/blue/purple)
- Resolved decisions = green notes; open decisions = yellow notes
- Quality Review section at the bottom (the three questions)
- Base styling on the workspace's `flow.html` base template when the root CLAUDE.md names one under "Words the skills use"; until it does, a self-contained page with the same sections

Hosting: when the root CLAUDE.md names a publish hook beside the base template, that hook deploys every `flow.html` edit — no manual push — and a new system is added to the hook's mapping and to the index it publishes. Without one, the file is opened locally, like every other companion page.

**Coupled update rule:** when a process changes, its flow.html (and any team-facing doc) updates in the same session. Pure web apps don't need a flow.html — they're not processes.
