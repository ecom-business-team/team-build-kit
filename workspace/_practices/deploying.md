# Deploying — cross-host truths

**CLI deploys ship the working tree, not git HEAD.** `railway up` and `vercel --prod` deploy the current working directory. Uncommitted work from another feature or owner sitting in the tree WILL ship. **Run `git status` before every deploy**; when foreign WIP is present, surface it before shipping it. The builder's side of the same rule: work you have built but are holding back (for example, a new scheduled job whose table is not applied yet) must not sit in a folder someone else deploys from, committed or not, because their next deploy ships it. Build it on a branch in a separate `git worktree` outside the deployed folder. Give the worktree its own Python environment (`UV_PROJECT_ENVIRONMENT=$HOME/.venvs/<worktree-name> uv sync`, then `uv run …` with the same variable) and never run the project's `dev.sh` there: a `dev.sh` that points every checkout at one shared venv holding an editable install means a `uv run` from the worktree silently repoints the main checkout's imports at the worktree's code (found 2026-10-05).

**Deploy-state truth lives in the running system, never in `git log`.** Verify via the job queue, `/healthz`, or a new-endpoint probe (a route that flips 404→401 when new code is live). Some repos deploy without a git remote at all — commits are irrelevant to what ships.

**When a deploy would activate something** (a cron, a cutover), verify the live prod state first — don't assume prod matches HEAD or the working tree.

**Platform runtime ceilings: validate the scheduled envelope live.** "Compiles and runs locally" says nothing about the platform clock — a Vercel Hobby job measured 288s of a 300s ceiling; its weekly variant hard-timed-out (2026-08-23). Measure real runs against the platform limit before relying on a schedule.

**Commit/push code projects at close-project time** — after verification, before archiving — so git-integrated deploys pick the work up.

## Establish the exposure surface by observation, before describing it (2026-09-19)

`git status` answers "what am I about to ship?". It does not answer "who will be able to reach it?", and that second question gets answered from memory far too often. A ship review for a platform stated that merging would make the new surfaces reachable by anyone holding the URL; it was inferred from the routing code, and it was wrong, because the host sat behind platform-level access protection that the application code cannot see.

So add one step to the pre-flight, next to `git status`: **make one unauthenticated request to the target and look at what comes back.** Not a health check, not an authenticated call — the request a stranger would make, with redirects unfollowed. It takes a second and it is the only thing that distinguishes *deployed* from *reachable*.

Do it again immediately after any change to the access posture, because that change is usually a dashboard toggle with no artifact in the repository and nothing in the build log.

**Taking a GitHub repo private is not one switch (2026-09-30).** Its GitHub Pages site is a separate public surface: a free-plan org cannot serve Pages from a private repo, yet the site stayed published (`public: true`) after the switch until it was deleted (`gh api -X DELETE repos/{owner}/{repo}/pages`). Even then the CDN kept serving the cached copy for up to its `max-age=600`. Right after the switch, members' `git clone` over HTTPS was refused with "Repository … is disabled" (403) while the API said `disabled: false`, and it cleared within a minute of deleting the site. Afterwards, check every surface as a stranger: the repo page, a raw file URL, the Pages URL (cache-busted) and the org's public repo list. Then check as a member: a plain `git clone`, not only `gh`.

## A branch push proves the deploy path before `main` moves (2026-09-24)

On a git-integrated host, push the branch first and let its preview build: it proves the build, the environment variables and the region settings on the host's own machines, while production still serves the old commit. A failure there costs nothing; the same failure after a merge is an outage. Merge only once the branch deployment is Ready.

## A value written at login is missing for every session already open at the deploy (2026-10-02)

When a release makes a page depend on something the login step stores (a claim in the auth user's metadata, a cookie, a cached flag), everyone who is already signed in keeps their session and never runs the new login code. Unless the release fills the value for them, they get whatever "missing" means. When "missing" means "no access", paying users are locked out with nothing logged. So when a release adds a login-written value, count the open sessions that lack it and backfill them in the same ship step, or make "missing" fetch the value once, before the deploy goes live.

## Rebase onto what runs at each deploy step, not at build (2026-10-08)

On a shared system, other projects deploy between your build and your ship. The base you built on can be one or more releases behind what is live by the time you deploy, so a deploy from that branch silently removes their work, and a fast-forward of `main` fails while a forced push drops their commits. Before each deploy step, read what the target runs now (the running deployment's commit, never `git log`), confirm your branch contains it, rebase if it does not, and re-run the suites on the rebased head. brand-reject's branches were rebased four times between build and go-live, because three other projects deployed in that window; the first check found the worker branch would have removed another project's matcher fix.
