"""Cross-platform (Windows / Mac / Linux) version of sync.sh, autopush.sh and ship.sh.
Usage:  python scripts/gitsync.py sync | push | ship"""
import os
import subprocess
import sys

MAX = 50 * 1024 * 1024  # never commit files > 50 MB


def git(*args, check=False):
    r = subprocess.run(["git", *args], capture_output=True, text=True)
    if check and r.returncode:
        sys.exit(f"git {' '.join(args)} failed:\n{r.stderr}")
    return r


def branch():
    return git("branch", "--show-current").stdout.strip()


def commit_all(msg):
    git("add", "-A")
    for f in git("diff", "--cached", "--name-only").stdout.splitlines():
        if os.path.isfile(f) and os.path.getsize(f) > MAX:
            git("reset", "-q", "--", f)
            print("skipped big file:", f)
    if git("diff", "--cached", "--quiet").returncode:
        git("commit", "-qm", msg)


def push():
    b = branch()
    if b in ("", "main"):
        sys.exit("On main: switch to your own branch first (git checkout -b <firstname>).")
    commit_all(f"update {b}")
    r = git("push", "-u", "origin", b)
    print(f"pushed {b}" if r.returncode == 0 else f"push failed:\n{r.stderr}")


def sync():
    b = branch()
    git("fetch", "-q", "origin")
    if b == "main":
        git("pull", "--ff-only", "-q", "origin", "main")
        print("WARNING: on main. Work on your own branch.")
        return
    commit_all(f"wip({b}): auto-save before sync")
    if git("rev-parse", "--verify", "--quiet", f"origin/{b}").returncode == 0:
        if git("pull", "--rebase", "-q", "origin", b).returncode:
            git("rebase", "--abort")
            sys.exit(f"CONFLICT pulling origin/{b}: resolve it by hand.")
    if git("merge", "--no-edit", "-q", "origin/main").returncode:
        git("merge", "--abort")
        sys.exit(f"CONFLICT merging origin/main into {b}: resolve it by hand.")
    print(f"{b} up to date with origin/main")


def ship():
    b = branch()
    push()
    git("fetch", "-q", "origin")
    git("checkout", "-q", "main", check=True)
    git("pull", "--ff-only", "-q", "origin", "main", check=True)
    if git("merge", "--no-edit", b).returncode:
        git("merge", "--abort")
        git("checkout", "-q", b)
        sys.exit("CONFLICT with main: run 'python scripts/gitsync.py sync' on your branch, fix, then ship again.")
    git("push", "-q", "origin", "main", check=True)
    git("checkout", "-q", b)
    print(f"{b} merged into main and pushed.")


if __name__ == "__main__":
    os.chdir(git("rev-parse", "--show-toplevel", check=True).stdout.strip())
    {"sync": sync, "push": push, "ship": ship}[sys.argv[1] if len(sys.argv) > 1 else "push"]()
