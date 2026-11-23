# Deploying — cross-host truths

This file holds what a script cannot see. Three rules that a script can check are no longer prose: the pre-deploy check (`.claude/hooks/deploy_check.py`) refuses `railway up` or `vercel --prod` when the folder holds uncommitted changes, when the branch lacks commits the remote's `main` has, or when Python code uses a name that no longer exists. Where that hook is not installed, do the three by hand before every deploy: `git status`, `git fetch && git log HEAD..origin/main`, and `uvx ruff check --select F821 .`.

## What a deploy ships

- **A command-line deploy ships the folder, not a commit.** `railway up` and `vercel --prod` send the working directory as it is.
- **Work you are holding back must not sit in a folder someone else deploys from**, committed or not, because their next deploy ships it. Build it on a branch in a separate `git worktree` under `~/worktrees/`.
- **The remote's `main` must hold what runs.** When a service is deployed from a local branch, fast-forward the remote's `main` to that commit before the project closes. Other sessions build from `main`, so a later deploy from it would remove your work with no error. `git rev-list --left-right --count origin/main...<deployed branch>` reads `0 0` after the push.
- **The pre-deploy check compares with the remote's `main`, not with the running service.** When a service may have been deployed from a branch that was never pushed, read the running deployment's commit and confirm your branch contains it.
- **Commit and push a code project when it closes**, after verification, so git-integrated hosts pick the work up.

## Worktrees

- **Give each worktree its own Python environment**: `UV_PROJECT_ENVIRONMENT=$HOME/.venvs/<worktree-name> uv sync`, then `uv run …` with the same variable. A wrapper script that points every checkout at one shared environment with an editable install will silently repoint the main checkout's imports at the worktree's code, so do not run the project's `dev.sh` in a worktree unless it refuses there.
- **A test that reads a fixture by a path relative to a parent folder fails to collect in a worktree outside that folder.** Run that test from the main checkout and the rest in the worktree with `--ignore`.
- **The repository's local `main` is not the remote's.** It can be an old branch holding commits that were never pushed. Work from `origin/main` (`git fetch`, then branch from it or push `HEAD:main`); never `git checkout main` or `git pull` into it in a worktree, because that moves the worktree onto the stale branch.
- **A Next.js worktree can borrow the main checkout's packages through a `node_modules` symlink** for `tsc`, `eslint`, `vitest` and Playwright. Next 16's Turbopack dev server panics on the link, so start it with `next dev --webpack`. `next build` with the link works under `~/worktrees/` and fails under `/tmp`, so keep throwaway worktrees under `~/worktrees/` too.

## What is live, and who can reach it

- **Deploy state is read from the running system, never from `git log`.** Use the job queue, `/healthz`, or a route that flips from 404 to 401 when the new code is live. Some repos deploy with no git remote at all.
- **Before a deploy that activates something** (a cron, a cutover), read the live production state first. Do not assume it matches the branch.
- **Make one unauthenticated request to the target and look at what comes back**, with redirects unfollowed. Routing code cannot show a host-level access wall, so this request is the only thing that tells *deployed* from *reachable*. Repeat it after any change to access settings, because that change is a dashboard toggle with nothing in the repository.
- **Measure a scheduled job's real run time against the host's limit.** A job that runs locally can still time out on the host's clock.
- **On a git-integrated host, push the branch first and let its preview build.** It proves the build, the environment variables and the region settings while production still serves the old commit. Merge only when the preview is Ready.

## Taking a GitHub repo private

It is not one switch. The repo's GitHub Pages site is a separate public surface and stays published until it is deleted (`gh api -X DELETE repos/{owner}/{repo}/pages`); the CDN then serves its cached copy for up to ten minutes. Members' `git clone` over HTTPS can be refused with "Repository … is disabled" until the site is deleted. Afterwards, check as a stranger (the repo page, a raw file URL, the Pages URL with a cache-buster, the org's public repo list) and as a member (a plain `git clone`, not only `gh`).

## Keys

- **A key that is set with the right name can still be unusable.** Prove every new or replaced key at the step that sets it, with the cheapest real call the code will make, and compare a fingerprint, never the value. An Anthropic key that is not scoped to a workspace answers every call with a 400, and nothing in the variable shows it.
- **Rotating a key breaks every holder at once, and a rarely used holder fails weeks later and silently.** So:
  1. Keep a written list of holders, and add each holder in the session that gives it the key. The rotation is finished when every row is proved live.
  2. A key reached by two routes (a shared variable and a stored credential) is two holders. Point every consumer at one source before rotating.
  3. Prove the new key's shape with one live call before changing the fleet.
  4. Prove each holder through what its users do. A health check stays green on a dead key.

## Values written at login

When a release makes a page depend on something the login step stores (a claim, a cookie, a cached flag), everyone already signed in keeps their session and never runs the new login code. If "missing" means "no access", paying users are locked out with nothing logged. Count the open sessions that lack the value and fill it in the same ship step, or make "missing" fetch the value once.
