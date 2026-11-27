#!/usr/bin/env bash
# Before each prompt: save local work, pull own branch, merge origin/main.
cd "$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
branch=$(git branch --show-current)
git fetch origin --quiet 2>/dev/null || { echo "[sync] fetch failed (offline?)"; exit 0; }

if [ "$branch" = "main" ]; then
  git pull --ff-only --quiet origin main 2>/dev/null
  echo "[sync] WARNING: on main. Do not work here. Ask the user to run: git checkout -b <firstname>"
  exit 0
fi

if [ -n "$(git status --porcelain)" ]; then
  git add -A
  git diff --cached --name-only -z | while IFS= read -r -d '' f; do
    if [ -f "$f" ] && [ "$(wc -c < "$f")" -gt 52428800 ]; then git reset -q -- "$f"; echo "[sync] skipped big file: $f"; fi
  done
  git diff --cached --quiet || git commit -qm "wip($branch): auto-save before sync"
fi

if git rev-parse --verify --quiet "origin/$branch" >/dev/null; then
  if ! git pull --rebase --quiet origin "$branch" 2>/dev/null; then
    git rebase --abort 2>/dev/null
    echo "[sync] CONFLICT pulling origin/$branch. Tell the user and resolve before continuing."
    exit 0
  fi
fi

if git rev-parse --verify --quiet origin/main >/dev/null; then
  if ! git merge --no-edit --quiet origin/main 2>/dev/null; then
    git merge --abort 2>/dev/null
    echo "[sync] CONFLICT merging origin/main into $branch. Tell the user and resolve before continuing."
    exit 0
  fi
fi
echo "[sync] $branch up to date with origin/main ($(git log -1 --format=%h origin/main 2>/dev/null))"
exit 0
