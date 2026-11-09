# Ready for your go: {outcome, as in the brief}
<!-- Written at the end of Run when others rely on the change. The brief's header moves to **Stage:** go. Every section answers one of the six questions in proof_checklist.md, Protection. -->

**Your answers in the brief:** {reply}, on {YYYY-MM-DD} at {HH:MM}.
**Built and proved:** {HH:MM} to {HH:MM}. The build is staged and nothing is live yet.

## What changes when you say go

<!-- What breaks? Every visible change and every reader of what changes. -->
- {What a person or a system sees differently, in plain words. Name who sees no change.}
- **Documents updated at go:** {the living documents and what each gains}

## The proof

{Where every path was run: the staged copy, staging, the dry run. Say "Nothing here was simulated on paper" only when that is true.}

| Path | Result | Read from |
|---|---|---|
| {each row of the brief's proof table} | {✅ or ❌, and the observed result} | {the state it was read from: the table, the page, the message received} |

## What I found while building, and how I ruled

<!-- What does it conclude without testing? Every finding, and every checklist item ruled not applicable. -->
1. **{The finding.}**
   - **Ruled:** {what was done}
   - **Why I could decide it:** {why it is inside the brief, and how it was proved}

{"Nothing I found changed any of your answers." | the stop, the answer given and when}

**Not tested, and why:** {anything the proof does not cover, and why that is acceptable; or "nothing"}

## If it goes wrong

- **The undo.** {The command or file, what it restores, and the proof that it was run against the staged copy and the state afterwards matched today's.}
- **Who notices.** {What fails loudly, where it shows, who sees it and how soon. Name anything that used to fail loudly and now would not.}
- **The fallback.** {What people do or see while it is broken.}

## When you type "go" here

{The deploy steps in order, the paths re-run live afterwards, the status set, the documents updated, and how long it takes, measured. The outcome check that will be filed, and its date.}
