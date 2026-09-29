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

## A rule that bans a platform feature records the evidence behind it (2026-08-25)

A single failed attempt is easy to write down as "the feature is broken", and once it is a rule nobody re-tests it. One empty variable resolution became a ban on the platform's variables, and the ban put a secret key into 34 workflows instead. When a rule forbids a tool or feature, write beside it what was tried, what came back, and the date, so the next reader can re-test the claim instead of inheriting it.

## Sweeping a defect class

When a fix addresses a class of defect rather than a one-off, the instance that surfaced it is only the entry point, and a partial sweep leaves the class open with a record that says it is closed.

1. **Enumerate by the defect's shape, not by the category the first carrier sat in.** Draw the population from the property that defines the bug (every node of that type in every active workflow, every call site of that read), never from the folder or feature that was being worked on. Do it with a script, not by eye; in code, write the scan as a test, so the class cannot return in a file that does not exist yet (`testing_standard.md` rule 6).
2. **Classify every member and write all the sets down**, the clean ones with the reason they are safe (for example, "a terminal step with nothing downstream, so a failure loses a notification but cannot strand a record"). A sweep that is not written down gets re-run, or worse, assumed complete.
3. **Sweep the values, not the presence.** A setting switched on with its parameters unset still runs the defaults. State the effective value and the number it yields ("5 tries at 5 s is about a 25 s window"), never just "enabled".
4. **Compute the ceiling before claiming the fix.** The quantified value can show that the fix cannot work (a 25 s retry window against outages that last minutes), which turns a quick fix into a memo.
5. **Read what each carrier does.** Severity follows what the carrier does, not where the defect was filed; the damaging instances are often outside the module the sweep was filed against.
6. **A reasoning flaw is a class too.** When a gate concludes something about items it never tested, sweep the other gates for the same reasoning shape, and check the worked precedents first: the operator's real practice may already hold the stronger test, waiting to be promoted into the document.

If the same class turns up twice, the recurrence itself is the finding: say so, rather than fixing the second instance quietly.
