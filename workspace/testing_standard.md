# Testing Standard

**Canonical.** How quality is proven on code projects. Loaded by `/prd` (deciding what each layer must prove before the build starts) and `/build` (Phase 3 verification and the per-work-item checks). Sibling standards: `documentation_standard.md` (how docs are structured), `workflow_design_standard.md` (how processes are designed).

**Scope.** Code projects — anything with a repo, a build and a deploy. Automation built from connected systems (a workflow tool, a board, webhooks) is verified differently: its equivalent is the tripwire "proof through the real entry point", and its regression suite is the reconcile lanes. A project with neither is too small to need this. Which proof a thing owes is decided by its **kind**: the kinds table in `documentation_standard.md` §4 ("The third axis") assigns one to each of the six, and this standard is the method for the three kinds that are code — service, application and tool.

## The layer split, and why there is one

Fixtures and production data **fail differently**, so a suite built on either alone has a blind spot shaped like its author.

Fixtures are deterministic, fast, and only ever contain what someone imagined. Production data contains what actually happened, which is where the defects are — but it moves under you, needs credentials, and cannot gate a push.

So split the layers by **what each can actually prove**:

| Layer | Data | Runs | Proves |
|---|---|---|---|
| **Unit** | Fixtures | Every push | Pure logic: copy, formatting, parsing, crypto, calculations |
| **Invariant** | Live, **read-only** | Scheduled + before deploy | *Properties* of real data that must always hold |
| **Smoke** | Live + a disposable identity | Before deploy, and at `/ship` | The real app answers through the real entry point |

### The invariant layer is the one people skip

It is not an integration test. An integration test seeds a database and asserts exact values, which needs an environment you probably do not have and re-imports the fixture blind spot.

An invariant asserts a **property over whatever is really in there**: no record falls into the "unclassified" bucket, no child count disagrees with its parent, no row returned for one user belongs to another, no internal-only column is reachable from a user-facing view, no public credential can read a private object.

These are deterministic without fixtures, they hold today and must hold forever, and they fail loudly the moment someone edits a view carelessly.

## The rules

1. **Assert properties, not values, against live data.** "This brand has 264 approved batches" is a fact today and a false failure tomorrow. Assert the invariant the number obeys. **Zero is a value too** — the trap that catches people who already know this rule. "No batch is in the unclassified stage" looks like a property and is really a count that happened to be zero on the day it was written; it went red the moment a batch sat mid-processing, which is a normal thing for a batch to do. Ask what would have to be TRUE for the system to be broken, and assert that: not "none are unclassified" but "an unclassified one is always still being worked on, and none is stuck there."
2. **A defect found by hand gets a test before it gets a fix.** Otherwise it comes back quietly. Mark those cases so the next reader knows they are load-bearing.
3. **Test the real function, never a reimplementation of it.** A security check verified against a copy of its own logic is not verified. If a function is hard to test because of its imports, that is the code telling you to extract it.
4. **Cleanup is proven, not assumed.** Any test that creates an identity or a row deletes it and asserts the residue is zero, out loud.
5. **Never write to production from a test.** Read-only against real data; writes go through a disposable identity in the smoke layer.
6. **Mechanical defect classes get mechanical checks.** Dead links, missing env vars, orphaned references — anything a script can enumerate should not depend on someone noticing. This includes a defective **code shape**: when the bug is a line that is easy to type and reads as ordinary, scan the source for the shape rather than writing a test per call site. A per-site test has to be written by the same person who just forgot the guard, so it is missing exactly where it is needed; a scan also covers files that do not exist yet. Let a genuine exception opt out **in the source, with its reason**, so the exceptions stay countable.
7. **Green is not proof.** A build compiling says nothing about whether a page renders. The last layer is always a real request to a real deployment.

## What goes in CI, and what cannot

CI runs the hermetic layers: unit, lint, build, and the mechanical checks. Every push, no credentials.

The live layers run on a schedule and before a deploy. Two honest reasons they often cannot run per-push: they need production credentials, and preview URLs are frequently behind the host's access protection, so an unauthenticated runner cannot reach them. Say which applies rather than quietly omitting the layer.

## Cost control

- **No coverage gate.** Coverage rewards testing the easy half. Rule 2 is the gate instead.
- **Unit tests stay under a few seconds**, or they stop being run on save and start being skipped.
- **One suite per surface, not per file.** A smoke check per page and a unit file per module of real logic. Tests for glue are maintenance debt.

## Adding to a suite as a project grows

Every new surface adds, at most:

- unit tests for any **new pure logic** it introduced (often none)
- one **smoke check** that the surface renders and is correctly gated
- an **invariant** only if it introduced a new view, table or scoping rule
- nothing at all for the mechanical checks — they enumerate automatically

If a new screen needs more than that, it is carrying logic that belongs in a module.
