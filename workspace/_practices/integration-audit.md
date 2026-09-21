# Cross-System Integration Audit

Repeatable 6-step audit for any multi-system pipeline (e.g. form → automation → database → board → notifications). Run it when systems drift or before changing a boundary.

1. Pull live workflow/config JSON for ALL connected automations (via API — never from docs).
2. Extract node names/types, database queries, board custom-field IDs, notification-target sources.
3. Build a cross-system field-trace matrix: source → automation → database → board → notification.
4. Contract-test every boundary: does the producer's output match the consumer's expected input?
5. Compare database config values against values hardcoded in automations.
6. Classify discrepancies: **A** blocking · **B** important · **C** cosmetic.

**What it reliably finds:** URL param name/value mismatches between workflows (`brand` vs `brand_id`) · deleted columns still referenced in automation code with broken fallbacks · hardcoded values that should be dynamic · orphaned schema columns (added early, omitted from forms, never populated).

Pairs with the reconciliation rule: run board↔database reconciliation BEFORE reporting metrics from either — drift has shifted reported metrics by 30+ percentage points.

## Auditing a proxy endpoint (server credential + caller-supplied id)

Any endpoint that forwards a **caller-supplied identifier** to an upstream API using a **server-side credential** is an authorization decision wearing a proxy's clothes. The question is never "is this person signed in" — it is **"may this person reach THIS resource."** The two diverge silently, because the credential's reach is invisible from the code.

**The sweep, in order:**

1. **List the endpoints that hold a server credential** and interpolate anything from `req.query` / `req.body` into an upstream URL.
2. **For each, ask what the credential can actually reach** — not what the app uses it for. Go and enumerate it. In one audit (2026-09-10) a board token turned out to reach two *different businesses'* spaces, through an endpoint every employee could call.
3. **Separate resource selectors from filters.** A hardcoded list id with a caller-supplied `assigneeId` is a filter *within* something the caller may already read in full — not a carrier. Trace it before you fix it; two of the six suspects in that sweep were clean, and a third only filtered our own tables.
4. **Prefer an allowlist of the permitted** over a denylist of the forbidden. A denylist expands silently: every namespace, list or workbook added later is unprotected *by default*, and nobody revisits the gate when adding a feature.
5. **When ids can't be enumerated, authorize on the response.** Task/record ids are unbounded, so fetch first and check what came back belongs to an allowlisted parent. Usually free — the payload already carries the parent id.
6. **Authenticate before authorizing,** so the allowlist isn't anonymously probeable.
7. **Encode every passthrough param.** Unencoded interpolation lets a caller append extra upstream query params onto your request.

**Verify with two tiers, against production, using minted tokens** — one ordinary user and one admin. Assert both directions: every legitimate `(resource, tab/list/key)` pair the frontend requests still returns 200, and each cross-boundary attempt returns a *named* 403. Enumerate the legitimate set from the frontend (`grep` the call sites) rather than from memory; in the sheets pass that caught a sixth workbook that would otherwise have broken. Delete the temp users afterwards.

**The tell that you are looking at this bug:** a comment in the file already explaining why it is currently safe. Someone saw it, wrote it down, and it stayed a comment instead of becoming a decision. A latent-risk note with a trigger condition in it is a filed bug that was never filed — grep for them.
