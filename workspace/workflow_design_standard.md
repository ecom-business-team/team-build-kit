# Workflow Design Standard

**Canonical.** How processes are designed and verified. Loaded by `/build` at Run (designing and proving the value stream), by `/prd` (designing the value stream) and by the old build skill (`/build-prd` from the lifecycle switch: Phase 3 end-of-build verification). Not for `/memo` (strategic) or `/quick-fix` (too small). Sibling standard: `documentation_standard.md` (how docs are structured).

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

Blank property = under-defined step. A step a person does names exactly one action they take, said as something a person does (approve the memo, read the report and say go, send the invoice), never a vague "review"; a step that needs two human actions is two steps. A step that someone other than the owner will carry out is shown to that person before the design is fixed: input that arrives after the build costs a rebuild (seven days, once). Vague output ("brand has overview") needs specificity ("brand has program overview with pricing, lifecycle, and terms summary").

## Quality review — three questions about the flow as a whole

1. **What breaks?** For every handoff: what if the next step never happens? How long until someone notices? For every write: what happens if it runs twice?
2. **Who knows?** For every failure: notified, or silent? For every piece of state: where is the source of truth, and can it drift?
3. **What's the fallback?** For every automated step: does a human have a manual path? For every human step: is a system idle waiting, and does anyone know?

**A notice someone must receive is found by state, not by a cursor.** When a person has to be told about an outcome (their work was rejected, their payment failed), the sender looks for every outcome that has no notice yet, not for the events that arrived after its last position. A cursor moves past anything a failed or skipped pass missed, and that miss is permanent and silent; a read by state heals it on the next pass, and an invariant ("every outcome older than N minutes has its notice") proves it held. (2026-10-08, brand-reject ship H2: a worker rolled back while the app stayed live would have left rejected creators untold for good.)

## Rules for state and writes

Each rule names the silent failure it prevents.

**The record**
1. **One system holds the record; any other copy is a mirror.** Write the record first and the mirror second, and set a disagreeing mirror back to the record, never the reverse. A new writer of a mirrored status updates every mirror, or the two drift.
2. **A step acts on the record, not on the event that woke it.** A trigger that carries no intent (a status changed) reads the record first and stops when it does not hold the expected state, so a manual move cannot set off messages or money.

**Writes**
3. **A check followed by a change is one atomic database function,** and where two inserts can race, a unique index decides. Separate steps race when several arrivals land together.
4. **Every state write names the state it expects,** so a repeat changes nothing. Stuck work is recovered through the idempotent front door, never by re-running a non-idempotent step or writing its result by hand: a re-run sends its messages again.
5. **A consumer of someone else's retries stores the producer's event id** on the rows it creates and checks it first. Best-effort delivery is for cosmetic output, never for money or state.
6. **A lifecycle timestamp is written once, where it is null, by the step that makes the transition.** A lost one stays null, never estimated; a write placed after another writer moved the row never matches.
7. **A write keyed on a parent names the child states it may touch,** and a decision about a set is taken over the whole current set, doing nothing when the rows disagree. Otherwise a failed item inherits its siblings' success.
8. **A failed write stops the chain, and a message upstream of a state write has its failure caught.** Otherwise the next step runs on a state that was never saved, or an undeliverable notice strands the work.

**Reads and branches**
9. **Every branch has a loud place for the case it did not expect.** A router with no fallback drops what it cannot classify and reports success; a path that skips input says what it skipped, by field.
10. **A failed read is never shown as empty.** A failed query, a field missing from the SELECT, a table nothing writes any more and a stale snapshot all render a complete, wrong picture; a read that fails raises, and a snapshot carries its time.
11. **A rule that classifies the same things in two places is one function, imported,** matching exact names before prefixes. Two copies drift, and the drift shows up as money.

**Changing the shape of state**
12. **A new status value, or a reader given a wider population, is a change to every consumer.** List the consumers from the code, or the newly included rows, and rule each in or out before go-live. Removing a state also removes whatever fired on entering it.
13. **A build that starts acting on another system's output re-rates that system's known defects,** because a defect that was quiet while nothing acted on it now causes actions.

**Watching it run**
14. **The monitor runs outside what it monitors** and tells "cannot reach" from "refused my key". A recovery part (a retry handler, a re-queue job) gets a detector of its own.
15. **A step that falls due weeks later is triggered by a dated task created when the work starts.** Nobody remembers it otherwise.

**Money**
16. **Ask who fronts the cash, and when, before designing anything that pays or bills.**
17. **A gate about money reads the outside party,** and sums that agree do not prove completeness: keep one independent total from the source and the human spot-check against the source's own screen.

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

For multi-stage workflows where quality matters more than speed: each stage produces output, and exactly one person takes one named action on it (reads the report and approves it, corrects the list, says go) before the next stage consumes it. A vague "review" is not a check. The intermediate artifact (markdown, JSON, report) IS the communication channel — folder structure is the state machine; no orchestration code.

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
