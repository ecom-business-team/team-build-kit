# Proof checklist

Loaded by `/build` when the change first runs, and before anything ships. Every check applies to every build. A check is "not applicable" only when its subject is absent (no outside party, no fixture written, no destructive drop), ruled on the go page or in the brief's Result with that reason. A check the run could perform is performed: "not tested" is never a ruling for something testable now. Section 1 is what Ask did; check the brief against it. Each check names the lessons it carries, by their ids in the lesson catalogue (`1_lifecycle_anatomy.md` §3, in the lifecycle rebuild's evidence folder); every lesson there is carried by at least one check.

**A new lesson replaces or sharpens a check; it never appends a paragraph. The word budget is a test.**

## 1. Intent: the owner's decisions are settled before work starts

1. **Every edge the run will meet is ruled in the brief.** Before asking, read the brief as the reader who wants the edge case decided for them, once. Each edge it leaves open is a decision added to the brief, not a ruling made mid-run. Stop at that one read: a second pass that finds at most one more item ends it. [lessons: 42, S3]
2. **The owner reads the real thing, whole.** Anything the owner approves is the rendered page, the real screen or the real text people will receive, never a summary of it or a drawing that cannot render. A page rewritten whole is read whole again. [lessons: 26, U1]
3. **The owner can follow every word.** Each decision, finding and hole is said in plain sentences: what it is, what happens, and why it matters. A point the owner cannot follow is rewritten before it is ruled. [lessons: 15]
4. **The brief holds only what decides or proves.** No section restates another. A section that caught nothing in past builds is not added. [lessons: 27]

## 2. Truth: the change rests on observed live state

1. **Every reader of what changes is traced from the live system**, not from a document or memory. That means the code and queries that read it, platform automations that fire on it, the queue and worker that actually run the job (from the queue's configuration), reports that count it, every reader of a field a retired writer used to fill, and the tests and smoke checks that assert on it. [lessons: 5, 37, 39, 45]
2. **Every value a fixture or test writes on a live platform is traced** to what it triggers there before it is written. [lessons: 32]
3. **The target system's own obligations are found and kept.** The post-deploy checks its index or testing section names are in the Go steps. [lessons: 23]
4. **A quoted input is re-read live at use.** A count, an inventory, an account's state, a login right or a rollback target is read again when the build uses it, never taken from a runbook or an earlier note. [lessons: 14, S4]
5. **A parameter the design rests on is measured.** A time window, a duplicate gap or a rate limit is measured on real events, never assumed. [lessons: 34]
6. **Each outside party can reach what it is asked to use.** Confirm from live state that every person or brand sent to a page has the account and the access to open it. [lessons: 48]
7. **A dry run is dry.** Every write in it is stubbed, including cursors, counters and logs on the live system; prove it by reading the state before and after. [lessons: S6]
8. **The time between proof and go is re-checked.** At Go, after the rebase, every input the proof rested on is re-read; anything assembled earlier is checked again before it is pushed. [lessons: 4]
9. **Parallel work is read before it is assumed absent.** Read `git log` and `git status` on every file the build touches, the builds in flight, and the highest live numbers (contract boundaries, decision ids) at the moment of writing them. Append to shared logs; never rewrite them whole. [lessons: 8, 41]

## 3. Proof: it works through its real entry point, on every path

1. **Through the real entry point.** The proof runs the change the way a person or the schedule will: the real page, the real webhook, the real command. The result is read from the resulting state, never from the actor's own output. [lessons: 3]
2. **The property, not its precondition.** Prove what the design rests on: a signed integration answers one real signed delivery; a write path is executed, not just reachable; a dedupe key holds under the repeated writes production makes. [lessons: 2, 30, 40]
3. **Data like production's in every way that matters.** List how the fixture differs from production and probe each difference. That includes rows made the other ways production makes them, the oldest and the largest account, the live edge the schedule will see as well as a settled period, more than one period, and every reader kind. Evidence proves only the cases that share its traits. [lessons: 9, 19, 22, 29, 33, 44]
4. **A check runs on exactly the set it claims.** A rule drawn from some files is checked on all of them, or its claim is narrowed. [lessons: 10]
5. **Every path, the whole path.** That means every row of the brief's path table, each failure path, what the build does when each command it calls fails or is missing, the whole path a person walks with real inputs (not only the changed screens), and every page an outside party is sent after a money step. [lessons: 18, 47, 49]
6. **Every check can fail.** Show each new check failing once on a known bad input. A check run after an edit is run against the files before the edit. A keep-list check strips its matches. A new test is shown to run. NOT RUN is never a pass. A check makes the data it judges. [lessons: 17, 24, S5, S8]
7. **Every text that applies a rule obeys it.** For each rule the build writes, read every text that applies it (skill, template, drawing key, test, card) and check it against the rule. [lessons: 16, 25]
8. **Name the known problem.** Before ruling on a hole, ask what the field calls it (a managed-file problem, a lost update, a race) and use the known fix. [lessons: U2]

## 4. Protection: the six questions the go page answers

Asked when others rely on the change. Each is answered in the named section of `go.md`; an answer of "I don't know" or "nothing" is a hole, and a hole is fixed in the run or put to the owner, never left.

1. **What breaks?** → "What changes when you say go". Every reader from Truth 1, and what each sees. A bulk write has its prestate snapshot. [lessons: 13]
2. **Who notices?** → "If it goes wrong · Who notices". Name what used to fail loudly and would now fail quietly, and give it a detector. Find work owed by state, never by a cursor that a rollback would skip. [lessons: 6, S7]
3. **What's the fallback?** → "If it goes wrong · The fallback". What people do or see while it is broken.
4. **What's the contingency?** → "If it goes wrong · The undo". A mechanical undo: a command or a file, run once on the staged copy, with the state afterwards compared to the state before. Before any destructive drop, save the verbatim definition (the DDL, the workflow JSON) in the build folder. [lessons: 1, 20]
5. **How do we fix it?** → "When you type go here". The deploy steps, timed by measurement. A step over about 15 minutes is briefed with the fastest option. Nothing is published before go. [lessons: 7, 46, 13]
6. **What does it conclude without testing?** → "What I found … · Not tested, and why". Each conclusion is either proved or named. Evidence that would come from waiting on real use is simulated now. A gate states its reason and names the specific step it waits on, checked live. A rollout step a person takes later gates nothing. [lessons: 31, 36, 38]

## 5. Record: status, documents and follow-ups are true

1. **Status is where the owner reads it.** Every stage move is written to the brief header and through the position command where one exists. A failing write stops the build. The brief header is the only position; there is no second state file. [lessons: 12, S1, S2]
2. **Living documents are true when they say they are.** Each change is written when it becomes true; a change that is only true after go is written at Go. One rule lives in one place; other texts point to it. Archiving moves a file, never copies it. [lessons: 11, 35, U3]
3. **No follow-up is lost.** Every loose end is done now or filed in the task manager under one existing parent. Only the owner drops one. None is left only in the brief or a log. [lessons: 21, 28, 43]
