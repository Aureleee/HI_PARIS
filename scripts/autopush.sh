#!/usr/bin/env bash
# After each answer: commit everything and push own branch. Never pushes main.
cd "$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
branch=$(git branch --show-current)
[ "$branch" = "main" ] && { echo "[autopush] on main, nothing pushed"; exit 0; }
[ -z "$branch" ] && exit 0

git add -A
# safety: unstage any file > 50 MB
git diff --cached --name-only -z | while IFS= read -r -d '' f; do
  if [ -f "$f" ] && [ "$(wc -c < "$f")" -gt 52428800 ]; then
    git reset -q -- "$f"; echo "[autopush] skipped big file: $f"
  fi
done

if ! git diff --cached --quiet; then
  git commit -qm "auto($branch): $(date +%H:%M)"
fi
git push -q -u origin "$branch" 2>/dev/null || echo "[autopush] push failed for $branch"
exit 0
