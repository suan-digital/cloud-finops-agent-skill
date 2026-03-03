#!/usr/bin/env python3
"""Check if upstream submodules are behind their remote HEAD.

Uses local git operations instead of GitHub API calls — no auth token needed.

Checks:
  - Each submodule: pinned commit vs. remote HEAD
  - FOCUS spec: new release tags

Usage:
  python scripts/check-submodule-freshness.py          # check mode (CI)
  python scripts/check-submodule-freshness.py --fetch   # fetch remotes first

Exit codes:
  0 — all submodules are up to date
  1 — one or more submodules are behind
"""

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

SUBMODULES = {
    "framework": {
        "path": ".upstream/framework",
        "branch": "main",
    },
    "focus-spec": {
        "path": ".upstream/focus-spec",
        "branch": "main",
    },
    "kpis": {
        "path": ".upstream/kpis",
        "branch": "main",
    },
}


def git(args, cwd=None):
    """Run a git command and return stdout."""
    result = subprocess.run(
        ["git"] + args,
        cwd=cwd or REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=60,
    )
    return result.stdout.strip(), result.returncode


def get_pinned_commit(submodule_path):
    """Get the commit SHA that the submodule is pinned to."""
    full_path = REPO_ROOT / submodule_path
    out, rc = git(["rev-parse", "HEAD"], cwd=full_path)
    if rc != 0:
        return None
    return out


def get_remote_head(submodule_path, branch):
    """Get the remote HEAD commit for a submodule's tracked branch."""
    full_path = REPO_ROOT / submodule_path
    out, rc = git(["rev-parse", f"origin/{branch}"], cwd=full_path)
    if rc != 0:
        return None
    return out


def get_remote_tags(submodule_path):
    """Get all remote tags for a submodule."""
    full_path = REPO_ROOT / submodule_path
    out, rc = git(["tag", "--list"], cwd=full_path)
    if rc != 0:
        return []
    return [t.strip() for t in out.split("\n") if t.strip()]


def fetch_submodule(submodule_path):
    """Fetch latest from remote for a submodule."""
    full_path = REPO_ROOT / submodule_path
    _, rc = git(["fetch", "--tags", "origin"], cwd=full_path)
    return rc == 0


def commits_behind(submodule_path, branch):
    """Count how many commits the pinned commit is behind remote HEAD."""
    full_path = REPO_ROOT / submodule_path
    out, rc = git(["rev-list", "--count", f"HEAD..origin/{branch}"], cwd=full_path)
    if rc != 0:
        return -1
    try:
        return int(out)
    except ValueError:
        return -1


def check_focus_tags():
    """Check for newer FOCUS release tags."""
    tags = get_remote_tags(SUBMODULES["focus-spec"]["path"])
    # Filter to version tags (e.g., "1.0", "v1.3")
    version_tags = []
    for tag in tags:
        clean = tag.lstrip("v")
        parts = clean.split(".")
        if len(parts) >= 2 and all(p.isdigit() for p in parts):
            version_tags.append(clean)

    if not version_tags:
        return None

    # Sort by version number
    version_tags.sort(key=lambda v: [int(p) for p in v.split(".")])
    return version_tags[-1]


def main():
    do_fetch = "--fetch" in sys.argv

    # Validate submodules exist
    for name, info in SUBMODULES.items():
        full_path = REPO_ROOT / info["path"]
        if not full_path.exists() or not (full_path / ".git").exists():
            print(f"ERROR: Submodule {name} not initialized at {info['path']}")
            print("Run: git submodule update --init")
            sys.exit(1)

    # Fetch if requested
    if do_fetch:
        print("Fetching submodule remotes...")
        for name, info in SUBMODULES.items():
            print(f"  fetching {name}...")
            if not fetch_submodule(info["path"]):
                print(f"  WARNING: fetch failed for {name}")

    # Check each submodule
    behind = []
    print("\n## Submodule Freshness Check\n")

    for name, info in SUBMODULES.items():
        pinned = get_pinned_commit(info["path"])
        remote = get_remote_head(info["path"], info["branch"])

        if not pinned:
            print(f"  {name}: ERROR — could not read pinned commit")
            behind.append(name)
            continue

        if not remote:
            print(f"  {name}: SKIP — could not read remote (run with --fetch)")
            continue

        if pinned == remote:
            print(f"  {name}: up to date ({pinned[:12]})")
        else:
            count = commits_behind(info["path"], info["branch"])
            count_str = f"{count} commits" if count > 0 else "unknown distance"
            print(f"  {name}: BEHIND ({count_str})")
            print(f"    pinned: {pinned[:12]}")
            print(f"    remote: {remote[:12]}")
            behind.append(name)

    # Check FOCUS release tags
    latest_tag = check_focus_tags()
    if latest_tag:
        pinned = get_pinned_commit(SUBMODULES["focus-spec"]["path"])
        # Check if the pinned commit is at or after the latest tag
        full_path = REPO_ROOT / SUBMODULES["focus-spec"]["path"]
        tag_commit, _ = git(["rev-list", "-1", f"v{latest_tag}"], cwd=full_path)
        if not tag_commit:
            tag_commit, _ = git(["rev-list", "-1", latest_tag], cwd=full_path)
        if tag_commit and pinned:
            # Check if pinned is an ancestor of or equal to the tag
            _, rc = git(["merge-base", "--is-ancestor", tag_commit, pinned], cwd=full_path)
            if rc == 0:
                print(f"\n  FOCUS latest release: v{latest_tag} (included in pinned commit)")
            else:
                print(f"\n  FOCUS: new release v{latest_tag} available (not in pinned commit)")
                if "focus-spec" not in behind:
                    behind.append("focus-spec")

    # Summary
    if behind:
        print(f"\n{len(behind)} submodule(s) behind: {', '.join(behind)}")
        print("\nTo update:")
        print("  cd .upstream/<name> && git pull origin main")
        print("  cd ../.. && git add .upstream/<name> && git commit")
        sys.exit(1)
    else:
        print("\nAll submodules are up to date.")
        sys.exit(0)


if __name__ == "__main__":
    main()
