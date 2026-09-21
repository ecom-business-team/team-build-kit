# Deploying — cross-host truths

**CLI deploys ship the working tree, not git HEAD.** `railway up` and `vercel --prod` deploy the current working directory. Uncommitted work from another feature or owner sitting in the tree WILL ship. **Run `git status` before every deploy**; when foreign WIP is present, surface it before shipping it.

**Deploy-state truth lives in the running system, never in `git log`.** Verify via the job queue, `/healthz`, or a new-endpoint probe (a route that flips 404→401 when new code is live). Some repos deploy without a git remote at all — commits are irrelevant to what ships.

**When a deploy would activate something** (a cron, a cutover), verify the live prod state first — don't assume prod matches HEAD or the working tree.

**Platform runtime ceilings: validate the scheduled envelope live.** "Compiles and runs locally" says nothing about the platform clock — a Vercel Hobby job measured 288s of a 300s ceiling; its weekly variant hard-timed-out (2026-08-23). Measure real runs against the platform limit before relying on a schedule.

**Commit/push code projects at close-project time** — after verification, before archiving — so git-integrated deploys pick the work up.

## Establish the exposure surface by observation, before describing it (2026-09-19)

`git status` answers "what am I about to ship?". It does not answer "who will be able to reach it?", and that second question gets answered from memory far too often. A ship review for a platform stated that merging would make the new surfaces reachable by anyone holding the URL; it was inferred from the routing code, and it was wrong, because the host sat behind platform-level access protection that the application code cannot see.

So add one step to the pre-flight, next to `git status`: **make one unauthenticated request to the target and look at what comes back.** Not a health check, not an authenticated call — the request a stranger would make, with redirects unfollowed. It takes a second and it is the only thing that distinguishes *deployed* from *reachable*.

Do it again immediately after any change to the access posture, because that change is usually a dashboard toggle with no artifact in the repository and nothing in the build log.
