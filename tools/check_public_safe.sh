#!/usr/bin/env bash
# Public-safety gate. Exits 1 if any tracked or untracked (non-ignored) file matches a pattern that
# must never reach a public repository, 0 if clean, 2 if it cannot run.
#
#   tools/public-safe-patterns.txt        generic patterns, committed
#   tools/public-safe-patterns.local.txt  specific private names, gitignored and never committed
#   ~/.config/kb-kg/public-safe-patterns.local.txt
#                                         the same list kept outside the repository, so that every
#                                         worktree and clone on this machine finds it; the gate loads
#                                         it as well (path overridden by KB_KG_PRIVATE_PATTERNS, or
#                                         by XDG_CONFIG_HOME for the folder)
#
# This repository is public, so every commit is published with its whole history. Run this before
# every commit. If no private-name list is found anywhere the gate warns and still exits 0.
set -u

cd "$(git rev-parse --show-toplevel)" || exit 2

self=tools/check_public_safe.sh
generic=tools/public-safe-patterns.txt
local_file=tools/public-safe-patterns.local.txt
saved_file="${KB_KG_PRIVATE_PATTERNS:-${XDG_CONFIG_HOME:-${HOME:-}/.config}/kb-kg/public-safe-patterns.local.txt}"

pats=$(mktemp)
trap 'rm -f "$pats"' EXIT

private_loaded=0
for f in "$generic" "$local_file" "$saved_file"; do
  [ -f "$f" ] || continue
  grep -vE '^[[:space:]]*(#|$)' "$f" >> "$pats"
  [ "$f" = "$generic" ] || private_loaded=1
done

if [ ! -s "$pats" ]; then
  echo "check_public_safe: no patterns loaded" >&2
  exit 2
fi
if [ "$private_loaded" -eq 0 ]; then
  echo "check_public_safe: WARNING no private-name list found ($local_file or $saved_file), so private repository names are NOT being checked" >&2
fi

rc=0
checked=0
while IFS= read -r f; do
  case "$f" in
    "$self" | "$generic" | "$local_file") continue ;;
  esac
  [ -f "$f" ] || continue
  checked=$((checked + 1))
  if grep -nIHEf "$pats" -- "$f"; then
    rc=1
  fi
done < <(git ls-files -co --exclude-standard)

if [ "$rc" -eq 0 ]; then
  echo "check_public_safe: clean ($checked files)"
else
  echo "check_public_safe: FAILED, fix the lines above before committing" >&2
fi
exit "$rc"
