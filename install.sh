#!/usr/bin/env bash
# Team Build Kit installer — installs every .skills/ file the MANIFEST lists into ~/.claude/skills/.
# Atomic: downloads everything to a temp folder first; installs only if every listed file arrives.
# TBK_BASE overrides where the kit is fetched from (default: GitHub main; a local clone is TBK_BASE="file://$PWD").
set -u
BASE="${TBK_BASE:-https://raw.githubusercontent.com/zjamesblake/team-build-kit/main}"
TMP=$(mktemp -d); ok=1
# 1) the MANIFEST is the one list of what the kit ships — no list, no install
if ! curl -fsSL "$BASE/MANIFEST" -o "$TMP/MANIFEST"; then
  rm -rf "$TMP"; echo "❌ Could not fetch MANIFEST from $BASE. Nothing was changed — check your connection and try again."; exit 1
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
  echo "✅ Team Build Kit installed ($got files — every .skills/ line the MANIFEST lists)."
  echo "   In Claude Code you now have:$(printf '%s\n' "$LIST" | grep -E '^\.skills/[^_][^/]*/SKILL\.md$' | sed -E 's#^\.skills/([^/]+)/SKILL\.md$# /\1#' | tr -d '\n')"
  echo "   Start with: /new-workspace"
else
  rm -rf "$TMP"; echo "❌ Install failed ($got/$want downloaded). Nothing was changed — check your connection and try again."; exit 1
fi
