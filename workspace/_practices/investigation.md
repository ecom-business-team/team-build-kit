# Hypothesis-Driven Investigation

When investigating a system issue, never let speculation outpace verification.

1. **State the hypothesis** as a specific testable claim — not a general suspicion.
   - Bad: "approved_at might be getting corrupted."
   - Good: "Workflow 6.0 overwrites approved_at to NOW() on every transition into ready_to_launch, learning, and complete, regardless of whether it was previously set."
2. **State the test** — what objective data proves it true or false? Specific query, specific expected output, specific threshold.
3. **Run the test BEFORE discussing fixes, implications, or backfill plans.** If you're reasoning about downstream effects before the underlying claim is verified, stop. Test first.
4. **Report the data first, interpretation second.** Show the numbers raw before labeling them "smoking gun." Let the owner see the data the way you see it.
5. **Isolate one claim at a time.** Don't bundle speculative claims into one decision request. Prove or refute one, then move on.

**Failure modes this prevents:** treating an agent's audit summary as ground truth · building fix paths on unverified bugs · speculating instead of running one query · cascading assumptions compounding uncertainty.

**Applies to:** workflow audits, schema findings, bug investigations, cross-system contracts, data integrity questions. Tied to "diagnose deep, fix shallow" and "go to the source."

## Deriving a filter from observed errors? Census the full retention window, not the incident

When you build a rule that keys on *observed* failure signatures — an error-message allowlist, a classifier, a retry filter — the sample you derive it from decides its coverage, and one incident is a monoculture of one failure mode.

**The method:** enumerate every historical instance the platform still retains, run the *actual deployed rule* over them — export the live code and replay it, don't re-implement it — and report matched / unmatched with the unmatched ones named. Cheap, and it turns "the signatures look stable" into a number. Replaying the deployed code also means the fixture's *shape* comes from the real payload instead of being invented, which is the failure mode a hand-built stub hides.

**Then say which way the rule fails.** An allowlist that fails CLOSED (no match → no action → status quo) can be extended lazily and is safe to ship incomplete. One that fails OPEN cannot. Put that sentence in the doc, next to the rule.

## An outage: ask first whether we caused it

"The provider went down" is a hypothesis like any other. The cheapest test is our own record: today's session log, the recent deploys, and any load tests or bulk jobs that ran just before the first error. Read those before anything else. The cause changes the answers. A self-inflicted outage can recur the next time the same job runs, so the recovery must include the rule that stops it happening again, and the handoff must not tell the owner that a vendor failed.

## After an outage, a clean error list is not a clean system

Recovery starts from the error list, but the list only holds the failures the tools recognised. Also compare throughput in the outage window with the hour before it (rows written, runs per workflow). A drop the errors don't explain is a silent loss, and it has to be found run by run, in successful runs that ended too early.
