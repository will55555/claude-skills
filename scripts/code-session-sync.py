#!/usr/bin/env python3
"""
code-session-sync.py

Claude Code SessionEnd hook. Fires automatically when a coding session ends
in any mapped repo. Reads what changed (git log since last marker), maps the
repo to its Notion project, and invokes Claude headlessly to update that
project's Status/Last Synced + a change note.

Designed for a Lego-block coding style (assembling existing modules), not
raw line-by-line authorship — the change note describes what got
integrated/wired together, not diff stats or line counts.

KAFKA is intentionally not in the map — it's an Obsidian-only learning
sandbox and should never trigger a Notion update.
"""
import json
import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime, timezone

SKILLS_ROOT = Path(r"C:\Users\solan\OneDrive\Desktop\SDE\claude-skills")
MAP_FILE = SKILLS_ROOT / "config" / "repo-notion-map.json"
MARKER_DIR = SKILLS_ROOT / "config" / ".sync-markers"


def load_map():
    with open(MAP_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def get_repo_name(cwd: str) -> str:
    # Walk up from cwd to find which mapped repo folder we're inside of.
    parts = Path(cwd).parts
    repo_map = load_map()
    for part in parts:
        if part in repo_map:
            return part
    return None


def git_changes_since_marker(cwd: str, marker_path: Path) -> str:
    """Return a human-readable summary of what changed, favoring commit
    messages and touched files over raw diff stats — better fit for a
    block-assembly workflow than line counts."""
    since_arg = []
    if marker_path.exists():
        last_sha = marker_path.read_text().strip()
        since_arg = [f"{last_sha}..HEAD"]

    try:
        log = subprocess.run(
            ["git", "log", "--oneline", "-15", *since_arg],
            cwd=cwd, capture_output=True, text=True, timeout=15
        ).stdout.strip()
        files = subprocess.run(
            ["git", "diff", "--name-only", *since_arg] if since_arg else
            ["git", "diff", "--name-only", "HEAD~5", "HEAD"],
            cwd=cwd, capture_output=True, text=True, timeout=15
        ).stdout.strip()
    except Exception as e:
        return f"(git unavailable: {e})"

    if not log and not files:
        return ""
    return f"Recent commits:\n{log}\n\nFiles touched:\n{files}"


def current_sha(cwd: str) -> str:
    try:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=cwd,
            capture_output=True, text=True, timeout=10
        ).stdout.strip()
    except Exception:
        return ""


def main():
    raw = sys.stdin.read()
    try:
        hook_input = json.loads(raw) if raw.strip() else {}
    except json.JSONDecodeError:
        hook_input = {}

    cwd = hook_input.get("cwd") or os.getcwd()
    repo_name = get_repo_name(cwd)

    if not repo_name:
        # Not a mapped repo (e.g. KAFKA, or anything not in the map).
        # Silent no-op — this is expected, not an error.
        sys.exit(0)

    repo_map = load_map()
    project = repo_map[repo_name]

    MARKER_DIR.mkdir(parents=True, exist_ok=True)
    marker_path = MARKER_DIR / f"{repo_name}.sha"

    changes = git_changes_since_marker(cwd, marker_path)
    if not changes:
        # Nothing changed since last sync — don't touch Notion.
        sys.exit(0)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    prompt = f"""A Claude Code session just ended in the "{repo_name}" repo
(Notion project: {project['notion_project']}, page id {project['notion_page_id']}).

Here is what changed since the last sync:
{changes}

Update the Notion page at {project['notion_url']} :
- Set Status to Active if it isn't already.
- Set "Last Synced" to {today}.
- Append a short note (1-3 sentences) describing what was integrated or
  wired together this session, in plain language — this is a block-assembly
  workflow (existing modules/components being put together), so describe
  what changed functionally, not a line-by-line diff.
- Do NOT rewrite existing page content, only append the note and update the
  two properties above.
Report back in one line what you changed."""

    result = subprocess.run(
        ["claude", "-p", prompt],
        capture_output=True, text=True, timeout=180
    )

    # Record the marker regardless of Claude call success/failure detail,
    # but only advance it if the call didn't hard-fail, so a broken run
    # doesn't silently swallow the next session's changes too.
    if result.returncode == 0:
        sha = current_sha(cwd)
        if sha:
            marker_path.write_text(sha)

    log_path = MARKER_DIR / f"{repo_name}.log"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n[{today}] returncode={result.returncode}\n")
        f.write(result.stdout[-2000:])
        if result.returncode != 0:
            f.write("\nSTDERR:\n" + result.stderr[-2000:])


if __name__ == "__main__":
    main()
