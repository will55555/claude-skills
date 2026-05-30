#!/usr/bin/env python3
"""
One-time setup for claude-skills on a new machine.
Creates a symlink (or junction on Windows) from ~/.claude/skills → this repo's skills/ folder.

Usage:
    python setup.py
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

REPO_DIR = Path(__file__).parent.resolve()
SKILLS_SRC = REPO_DIR / "skills"
CLAUDE_DIR = Path.home() / ".claude"
CLAUDE_SKILLS = CLAUDE_DIR / "skills"


def main():
    print("claude-skills setup")
    print(f"  Repo:   {REPO_DIR}")
    print(f"  Target: {CLAUDE_SKILLS}")
    print()

    # Ensure ~/.claude exists
    CLAUDE_DIR.mkdir(parents=True, exist_ok=True)

    # Already a symlink/junction pointing to the right place
    if CLAUDE_SKILLS.is_symlink():
        current = Path(os.readlink(CLAUDE_SKILLS))
        if current == SKILLS_SRC:
            print("✅ Already set up correctly.")
            return
        else:
            print(f"⚠️  Symlink exists but points to {current}. Relinking...")
            CLAUDE_SKILLS.unlink()

    # Existing real directory — back it up
    elif CLAUDE_SKILLS.exists():
        backup = Path(str(CLAUDE_SKILLS) + ".bak")
        print(f"⚠️  {CLAUDE_SKILLS} exists as a directory. Backing up to {backup}")
        shutil.move(str(CLAUDE_SKILLS), str(backup))

    # Create symlink / junction
    if sys.platform == "win32":
        # Directory junctions don't require admin on Windows
        result = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(CLAUDE_SKILLS), str(SKILLS_SRC)],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"❌ Failed to create junction: {result.stderr}")
            sys.exit(1)
    else:
        CLAUDE_SKILLS.symlink_to(SKILLS_SRC, target_is_directory=True)

    print(f"✅ Linked: {CLAUDE_SKILLS} → {SKILLS_SRC}")
    print()
    print("Done! Claude Code will now read skills from this repo.")
    print("Next: open Claude Code and run 'deploy from Notion' to pull the latest skills.")


if __name__ == "__main__":
    main()
