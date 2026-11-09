# Brief: {outcome, as a short title}
**Stage:** ask ({YYYY-MM-DD HH:MM})
**Next:** {one line: the owner's answers to the decisions below | the run | the go page | the outcome check on {date}}
**Risk:** {others rely on it | nobody relies on it}
**History:** ask {YYYY-MM-DD HH:MM}
<!-- Add `**Task:** {url}` here where the area's index names a position command. Add `**Answers:** {reply} ({YYYY-MM-DD HH:MM})` when the owner replies. The session-start gate reads **Stage:** and **Next:**. **Risk:** here is the short label; the "Who relies on it" paragraph below says why. -->

**Outcome:** {what is true for a person afterwards, in one or two plain sentences}

**Why:** {the priorities.md initiative it serves, or the existing system it fixes}

**Who relies on it:** {the router's answer in one sentence: who relies on it, or that nobody does, and why}. {Others rely on it: "So the run ends with a rehearsal, an undo and your go before anything goes live." | Nobody relies on it: "So I ship it when the proof passes and report with the proof."}

## What I found in the live system

- **{The thing looked at}.** {What is there, observed and not recalled, and how it was observed: the query, the page opened, the file read. The facts the decisions below rest on, including every reader of what changes.}

## Decisions for you

1. **{The question, in one sentence a reader can answer without the rest of the page}**
   - **a (recommended):** {option}
   - **b:** {option}

   {One sentence on what the other option costs.}

Reply with your choices in one line, for example "1a 2a". That reply is your approval: I then build, prove{, rehearse} and {come back with one page for your go | ship it and report with the proof}. I stop before that only if I find something that changes one of these answers.

{No decisions: "Nothing here needs your decision, so I am starting the run now."}

## How I'll prove it

| Path | Who or what I use | What counts as proof |
|---|---|---|
| {each path a person or a system takes through the change, including failure paths and every reader downstream} | {the data or fixture, and how it differs from production, if at all} | {the observed result that passes, read from the resulting state} |

**Out of scope:** {what this build will not touch}

<!-- Nobody relies on it: at the end of the run, add the section below. -->
## Result

| Path | Result | Read from |
|---|---|---|
| {every row of the proof table above} | {✅ or ❌, and what was observed} | {the state it was read from} |

**Rulings:** {each finding, how it was ruled, and why it was inside the brief; or "none"}
**Not tested, and why:** {anything a path did not cover; or "nothing"}
**Not applicable:** {each checklist item ruled not applicable, and the subject that is absent; or "none"}
**Follow-ups:** {each loose end and where it went: done, or filed (link) with a recommendation if it may not be worth doing; or "none"}
