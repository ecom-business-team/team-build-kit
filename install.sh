#!/usr/bin/env bash
# Team Build Kit installer.
#   Always: installs every .skills/ line the MANIFEST lists into ~/.claude/skills/.
#   With TBK_WORKSPACE=<folder>: also places every workspace/ line into that folder (kit-owned files,
#   refreshed by /update-build-kit; your CLAUDE.md is never touched). settings.json is merged, not replaced.
#   Refuses three targets and changes nothing: a path that is not a folder, your home folder, the kit folder itself.
# Atomic: downloads everything to a temp folder first; installs only if every listed file arrives.
# TBK_BASE overrides where the kit is fetched from (default: GitHub main; a local clone is TBK_BASE="file://$PWD").
set -u
BASE="${TBK_BASE:-https://raw.githubusercontent.com/zjamesblake/team-build-kit/main}"
TMP=$(mktemp -d); ok=1; W=""
# 1) the MANIFEST is the one list of what the kit ships — no list, no install
if ! curl -fsSL "$BASE/MANIFEST" -o "$TMP/MANIFEST"; then
  rm -rf "$TMP"; echo "❌ Could not fetch MANIFEST from $BASE. Nothing was changed — check your connection and try again."; exit 1
fi
SLIST=$(grep -E '^\.skills/'  "$TMP/MANIFEST")
WLIST=$(grep -E '^workspace/' "$TMP/MANIFEST")
if [ -n "${TBK_WORKSPACE:-}" ]; then
  W="${TBK_WORKSPACE%/}"
  [ -d "$W" ] || { rm -rf "$TMP"; echo "❌ TBK_WORKSPACE is not a folder: $W. Nothing was changed."; exit 1; }
  [ "$W" = "$HOME" ] && { rm -rf "$TMP"; echo "❌ TBK_WORKSPACE is your home folder. Nothing was changed."; exit 1; }
  [ -f "$W/MANIFEST" ] && { rm -rf "$TMP"; echo "❌ $W is the kit itself, not a workspace. Nothing was changed."; exit 1; }
  LIST="$SLIST"$'\n'"$WLIST"
else
  LIST="$SLIST"
fi
want=$(printf '%s\n' "$LIST" | grep -c .)
# 2) download EVERYTHING to a temp dir first — touch nothing installed yet
for p in $LIST; do
  mkdir -p "$TMP/$(dirname "$p")"; curl -fsSL "$BASE/$p" -o "$TMP/$p" || { ok=0; rm -f "$TMP/$p"; }
done
got=$(find "$TMP" -type f -not -name MANIFEST 2>/dev/null | wc -l | tr -d ' ')
# 3) only install if every listed file downloaded cleanly (atomic — never leave a half-updated kit)
if [ "$ok" = 1 ] && [ "$want" -gt 0 ] && [ "$got" = "$want" ]; then
  for p in $LIST; do
    case "$p" in
      .skills/*)   dest="$HOME/.claude/skills/${p#.skills/}" ;;
      workspace/*) dest="$W/${p#workspace/}" ;;
    esac
    if [ "$p" = "workspace/.claude/settings.json" ] && [ -f "$dest" ]; then
      # merge the kit's hook groups into the settings the person already has; theirs are kept
      python3 - "$dest" "$TMP/$p" <<'PY'
import json, sys
dest, kit = sys.argv[1], sys.argv[2]
d = json.load(open(dest)); k = json.load(open(kit))
hooks = d.setdefault("hooks", {}); added = 0
for event, groups in k.get("hooks", {}).items():
    have = {h.get("command") for g in hooks.get(event, []) for h in g.get("hooks", [])}
    for g in groups:
        if any(h.get("command") not in have for h in g.get("hooks", [])):
            hooks.setdefault(event, []).append(g); added += 1
json.dump(d, open(dest, "w"), indent=2); open(dest, "a").write("\n")
print(f"   settings.json: merged {added} kit hook group(s) (yours kept)")
PY
    else
      mkdir -p "$(dirname "$dest")"; cp "$TMP/$p" "$dest"
    fi
  done
  rm -rf "$TMP"
  echo "✅ Team Build Kit installed ($got files — every line the MANIFEST lists for this install)."
  echo "   In Claude Code you now have:$(printf '%s\n' "$SLIST" | grep -E '^\.skills/[^_][^/]*/SKILL\.md$' | sed -E 's#^\.skills/([^/]+)/SKILL\.md$# /\1#' | tr -d '\n')"
  if [ -n "$W" ]; then
    echo "   Workspace files: $(printf '%s\n' "$WLIST" | grep -c .) into $W (kit-owned; refreshed by /update-build-kit; your CLAUDE.md is never touched)."
    echo "   Next: open $W in Claude Code."
  else
    echo "   New here? Type /onboard to create your workspace."
  fi
else
  rm -rf "$TMP"; echo "❌ Install failed ($got/$want downloaded). Nothing was changed — check your connection and try again."; exit 1
fi
