---
name: update-build-kit
description: Pull the latest version of the Team Build Kit and re-install its skills. Use when there's a new version of the kit, or to make sure your lifecycle skills (new-workspace, memo, prd, build, ship, quick-fix) and the shared Documentation Standard are current. Never touches your own work — only refreshes the kit's skills.
---

# /update-build-kit

Refresh the Team Build Kit to its latest published version. This re-downloads the kit's skills and the shared Documentation Standard from GitHub and re-installs them into `~/.claude/skills/`. **It only touches the kit's own skills — never the user's workspaces or work.**

## When to Use

- You heard there's a new version of the kit.
- You want to confirm your lifecycle skills are current.

## When NOT to Use

- To change your own project files (that's `/quick-fix` or the lifecycle skills).

---

## How it works

The kit lives at a public GitHub repo. This skill pulls the current files straight from there, so it works whether the user cloned the repo or just downloaded the ZIP.

**Repo:** `https://github.com/zjamesblake/team-build-kit`
**Raw base:** `https://raw.githubusercontent.com/zjamesblake/team-build-kit/main` — `TBK_BASE` overrides it (a local clone: `TBK_BASE="file://$PWD"`).
**What ships:** every `.skills/` line in the kit's `MANIFEST`; the skill installs exactly those and nothing else.

### Step 1: Re-install from GitHub

Tell the user: *"Pulling the latest Team Build Kit and re-installing the skills — this won't touch any of your own work."* Then run:

```bash
BASE="${TBK_BASE:-https://raw.githubusercontent.com/zjamesblake/team-build-kit/main}"
TMP=$(mktemp -d); ok=1
# 1) the MANIFEST is the one list of what the kit ships — no list, no install
if ! curl -fsSL "$BASE/MANIFEST" -o "$TMP/MANIFEST"; then
  rm -rf "$TMP"; echo "Update FAILED: could not fetch MANIFEST from $BASE. Your existing kit is UNTOUCHED — nothing was changed. Check your connection and try again."; exit 1
fi
LIST=$(grep -E '^\.skills/' "$TMP/MANIFEST")
want=$(printf '%s\n' "$LIST" | grep -c .)
# 2) download EVERYTHING to a temp dir first — touch nothing installed yet
for p in $LIST; do
  mkdir -p "$TMP/$(dirname "$p")"; curl -fsSL "$BASE/$p" -o "$TMP/$p" || { ok=0; rm -f "$TMP/$p"; }
done
got=$(find "$TMP/.skills" -type f 2>/dev/null | wc -l | tr -d ' ')
# 3) only install if every listed file downloaded cleanly (atomic — never leave a half-updated kit)
if [ "$ok" = 1 ] && [ "$want" -gt 0 ] && [ "$got" = "$want" ]; then
  for p in $LIST; do
    dest="$HOME/.claude/skills/${p#.skills/}"
    mkdir -p "$(dirname "$dest")"; cp "$TMP/$p" "$dest"
  done
  rm -rf "$TMP"
  echo "Updated $got files (every .skills/ line the MANIFEST lists)."
else
  rm -rf "$TMP"; echo "Update FAILED ($got/$want downloaded). Your existing kit is UNTOUCHED — nothing was changed. Check your connection and try again, or re-download the repo."; exit 1
fi
```

> If the user also has the repo cloned locally and prefers git: `cd` into it, `git pull`, then re-run the install command from the kit's `CLAUDE.md`. The curl path above is the default because it needs no clone.

### Step 2: Verify

Confirm every `.skills/` file the MANIFEST lists was written (the command prints the count). The four core lifecycle skills (`prd`, `build`, `ship`, `new-workspace`) depend on `~/.claude/skills/_shared/documentation_standard.md` — make sure it's present. If a `curl` failed (no network, repo moved), say so plainly and stop; don't leave a half-updated set.

### Step 3: Confirm

Tell the user: *"Done — your Team Build Kit skills are current. Nothing in your own workspaces was touched."*

---

## Principles

- **Only the kit's skills change.** This never modifies the user's projects, docs, or data.
- **All-or-nothing.** If a download fails, report it and stop — a half-updated kit is worse than a stale one.
- **The source of truth is GitHub.** This skill pulls; it never edits the kit's contents locally.
