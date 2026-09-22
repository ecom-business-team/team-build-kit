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
