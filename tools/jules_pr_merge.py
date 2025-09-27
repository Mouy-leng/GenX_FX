#!/usr/bin/env python3
"""
tools/jules_pr_merge.py
Jules PR Merge Mission (Python)
- Uses PyGithub for API operations and `git` for local merge attempts.
- Create conflict branches and PRs when manual resolution is required.
"""

import os
import re
import subprocess
import sys
import time
from typing import List

from github import Github, GithubException

# Configuration
MAIN_BRANCH = os.getenv("MAIN_BRANCH", "main")
TMP_PREFIX = "jules-temp"
CONFLICT_PREFIX = "jules-conflict"
SAFE_EXT_REGEX = re.compile(r".*\.(md|markdown|txt|yaml|yml|json|lock|cfg|ini|toml|gradle|xml)$", re.IGNORECASE)
POLL_ATTEMPTS = 6
POLL_DELAY = 2  # seconds
DRY_RUN = os.getenv("DRY_RUN", "false").lower() in ("1", "true", "yes")


def run(cmd: List[str], capture_output=False, check=True, cwd=None):
    if capture_output:
        return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=check, cwd=cwd)
    else:
        return subprocess.run(cmd, check=check, cwd=cwd)


def git(cmd: List[str], capture_output=False, check=True, cwd=None):
    return run(["git"] + cmd, capture_output=capture_output, check=check, cwd=cwd)


def log(*args):
    print("[jules]", *args, flush=True)


def ensure_tools():
    try:
        run(["git", "--version"], capture_output=True)
    except Exception:
        log("git is required in the runner.")
        sys.exit(1)


def github_client():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        log("GITHUB_TOKEN is required (set by Actions).")
        sys.exit(1)
    return Github(token)


def poll_mergeable(pr):
    # Sometimes GitHub needs time to compute mergeable — poll a few times.
    for i in range(POLL_ATTEMPTS):
        pr = pr.as_dict() if isinstance(pr, object) and hasattr(pr, "as_dict") else pr
        try:
            pr_obj = pr if not isinstance(pr, dict) else None
        except Exception:
            pr_obj = None
        # reload pr using API if possible (we may have a PullRequest object)
        try:
            pr = pr.refresh() if hasattr(pr, "refresh") else pr
        except Exception:
            pass
        # Try to get mergeable via attribute
        try:
            mergeable = getattr(pr, "mergeable", None)
        except Exception:
            mergeable = None
        if mergeable is not None:
            return mergeable  # True/False
        time.sleep(POLL_DELAY)
    # If still unknown, return False (don't trust)
    return False


def safe_to_auto_resolve(conflict_files: List[str]) -> bool:
    if not conflict_files:
        return False
    for f in conflict_files:
        if not SAFE_EXT_REGEX.match(f):
            return False
    return True


def list_conflict_files() -> List[str]:
    try:
        r = git(["diff", "--name-only", "--diff-filter=U"], capture_output=True, check=False)
        files = r.stdout.strip().splitlines()
        return [f for f in files if f.strip()]
    except Exception:
        return []


def main():
    ensure_tools()
    gh = github_client()
    repo_full = os.getenv("GITHUB_REPOSITORY")
    if not repo_full:
        log("GITHUB_REPOSITORY env var is required.")
        sys.exit(1)

    repo = gh.get_repo(repo_full)
    log("Repository:", repo_full)

    # Make sure local repo is up-to-date
    git(["fetch", "--all", "--prune"])
    git(["checkout", MAIN_BRANCH])
    git(["pull", "origin", MAIN_BRANCH])

    open_pulls = repo.get_pulls(state="open", sort="created", base=MAIN_BRANCH)
    pulls = list(open_pulls)
    if len(pulls) == 0:
        log("No open PRs.")
        return

    merged = []
    auto_fixed = []
    forked = []

    # Configure git user for commits done by Jules
    git(["config", "user.name", "jules-bot"])
    git(["config", "user.email", "jules-bot@example.com"])

    for pr in pulls:
        pr_number = pr.number
        head_ref = pr.head.ref
        title = pr.title
        log(f"Processing PR #{pr_number} — {head_ref} — '{title}'")

        # Check if mergeable via API (poll since compute may be delayed)
        try:
            pr = repo.get_pull(pr_number)  # reload
        except GithubException as e:
            log("Failed to reload PR from API:", e)
            continue

        mergeable = poll_mergeable(pr)
        log(f"API reports mergeable={mergeable}")

        # If mergeable True, attempt API merge (preserves metadata)
        if mergeable:
            if DRY_RUN:
                log("[DRY RUN] Would merge via API:", pr_number)
                merged.append(pr_number)
                # update local main for subsequent operations
                git(["checkout", MAIN_BRANCH])
                git(["pull", "origin", MAIN_BRANCH])
                continue
            try:
                # Use merge method 'merge' (merge commit) — adjust if you prefer 'squash'
                repo.merge(pr.head.sha, f"Merge PR #{pr_number}: {title}", pr.base.ref)
                log(f"✅ API merged PR #{pr_number}")
                merged.append(pr_number)
                # update local main
                git(["checkout", MAIN_BRANCH])
                git(["pull", "origin", MAIN_BRANCH])
                continue
            except GithubException as e:
                log("API merge failed:", e)
                # fall through to local attempt

        # Attempt local merge (fetch PR branch and merge)
        tmp_main = f"{TMP_PREFIX}-{pr_number}-main"
        tmp_merge = f"{TMP_PREFIX}-{pr_number}-merge"

        try:
            # ensure clean working tree
            git(["checkout", MAIN_BRANCH])
            git(["pull", "origin", MAIN_BRANCH])
            # create a temporary branch off main
            git(["checkout", "-b", tmp_main])
            # fetch pr branch to local tmp_merge
            git(["fetch", "origin", f"{head_ref}:{tmp_merge}"])

            # attempt merge without committing
            res = git(["merge", "--no-ff", "--no-commit", tmp_merge], check=False)
            if res.returncode == 0:
                # No conflicts -> commit and push to main
                git(["commit", "-m", f"Jules: Merged PR #{pr_number} ({head_ref}) locally"])
                if DRY_RUN:
                    log(f"[DRY RUN] Would push merged main for PR #{pr_number}")
                    auto_fixed.append(pr_number)
                else:
                    git(["checkout", MAIN_BRANCH])
                    # fast-forward main with temp branch
                    try:
                        git(["merge", "--ff-only", tmp_main])
                    except Exception:
                        # fallback to merging tmp_main
                        git(["merge", tmp_main])
                    git(["push", "origin", MAIN_BRANCH])
                    log(f"✅ Locally merged and pushed PR #{pr_number}")
                    merged.append(pr_number)
                # cleanup
                git(["branch", "-D", tmp_main])
                git(["branch", "-D", tmp_merge])
                continue
            else:
                # Conflicts present
                conflict_files = list_conflict_files()
                log(f"⚠️ Conflicts found in PR #{pr_number}: {conflict_files}")
                if safe_to_auto_resolve(conflict_files):
                    log("ℹ️ Conflicts are 'safe' types — attempting conservative auto-resolve (prefer PR changes).")
                    if DRY_RUN:
                        log("[DRY RUN] Would checkout --theirs for files:", conflict_files)
                        auto_fixed.append(pr_number)
                    else:
                        for f in conflict_files:
                            git(["checkout", "--theirs", "--", f])
                            git(["add", f])
                            log("  auto-resolved", f)
                        git(["commit", "-m", f"Jules: Auto-resolved minor conflicts for PR #{pr_number} (prefer PR changes)"])
                        git(["checkout", MAIN_BRANCH])
                        try:
                            git(["merge", "--ff-only", tmp_main])
                        except Exception:
                            git(["merge", tmp_main])
                        git(["push", "origin", MAIN_BRANCH])
                        log(f"✅ Auto-resolved and pushed PR #{pr_number}")
                        auto_fixed.append(pr_number)
                    # cleanup
                    git(["branch", "-D", tmp_main])
                    git(["branch", "-D", tmp_merge])
                    continue
                else:
                    # Complex conflicts -> create conflict branch and open PR for manual resolution
                    conflict_branch = f"{CONFLICT_PREFIX}-{pr_number}"
                    log(f"🛑 Complex conflicts — creating branch {conflict_branch} for manual resolution.")
                    # abort merge and create branch from main
                    git(["merge", "--abort"], check=False)
                    git(["checkout", MAIN_BRANCH])
                    git(["checkout", "-b", conflict_branch])
                    # try to merge tmp_merge to preserve conflict markers
                    git(["merge", "--no-ff", tmp_merge], check=False)
                    if DRY_RUN:
                        log(f"[DRY RUN] Would push branch {conflict_branch} and open PR for manual review.")
                        forked.append(pr_number)
                        # cleanup temp branches
                        git(["checkout", MAIN_BRANCH])
                        git(["branch", "-D", tmp_main], check=False)
                        git(["branch", "-D", tmp_merge], check=False)
                        git(["branch", "-D", conflict_branch], check=False)
                        continue
                    # push conflict branch and open PR
                    git(["push", "-u", "origin", conflict_branch])
                    body = (
                        f"Jules created this conflict branch from {MAIN_BRANCH}, merging in {head_ref}.\n\n"
                        "Automatic merge failed; manual conflict resolution required."
                    )
                    repo.create_pull(title=f"Conflict Resolution Needed: PR #{pr_number} - {title}",
                                     body=body,
                                     head=conflict_branch,
                                     base=MAIN_BRANCH)
                    log(f"🔔 Opened PR for conflict branch {conflict_branch} (for PR #{pr_number})")
                    forked.append(pr_number)
                    # cleanup temp branches locally
                    git(["checkout", MAIN_BRANCH])
                    git(["branch", "-D", tmp_main], check=False)
                    git(["branch", "-D", tmp_merge], check=False)
                    continue
        except Exception as exc:
            log("Error handling PR", pr_number, exc)
            try:
                git(["checkout", MAIN_BRANCH])
            except Exception:
                pass
            # attempt to delete temp branches to keep repo clean
            git(["branch", "-D", tmp_main], check=False)
            git(["branch", "-D", tmp_merge], check=False)
            continue

    # Summary
    log("========================================")
    log("Mission Summary:")
    log("Merged:", merged or "none")
    log("Auto-fixed & merged:", auto_fixed or "none")
    log("Forked for manual review:", forked or "none")
    log("Jules mission completed.")


if __name__ == "__main__":
    main()