#!/usr/bin/env bash
# Merge your branch into main and push. Run it from YOUR branch when your code works.
set -e
cd "$(git rev-parse --show-toplevel)"
b=$(git branch --show-current)
[ "$b" = "main" ] && { echo "Run this from your own branch, not main."; exit 1; }
bash scripts/autopush.sh
git fetch -q origin
git checkout -q main
git pull -q --ff-only origin main
if ! git merge --no-edit "$b"; then
  git merge --abort; git checkout -q "$b"
  echo "CONFLICT with main: run 'bash scripts/sync.sh' on your branch, fix the conflict, then rerun ship.sh"
  exit 1
fi
git push -q origin main
git checkout -q "$b"
echo "$b merged into main and pushed."
