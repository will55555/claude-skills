#!/usr/bin/env python3
"""
One-time setup for claude-skills on a new machine.

Steps:
  1. Symlink ~/.claude/skills → this repo's skills/ folder
  2. Write ~/.claude/mcp.json with Notion MCP server (prompts for token)

Usage:
    python setup.py
"""
import json
import os
import sys
import shutil
import subprocess
from pathlib import Path

REPO_DIR = Path(__file__).parent.resolve()
SKILLS_SRC = REPO_DIR / "skills"
CLAUDE_DIR = Path.home() / ".claude"
CLAUDE_SKILLS = CLAUDE_DIR / "skills"
MCP_CONFIG = CLAUDE_DIR / "mcp.json"


def setup_skills_symlink():
    print("── Step 1: Skills symlink ──────────────────────────")
    print(f"  Repo:   {REPO_DIR}")
    print(f"  Target: {CLAUDE_SKILLS}")

    CLAUDE_DIR.mkdir(parents=True, exist_ok=True)

    if CLAUDE_SKILLS.is_symlink():
        current = Path(os.readlink(CLAUDE_SKILLS))
        if current == SKILLS_SRC:
            print("✅ Already linked correctly.")
            return
        print(f"⚠️  Symlink exists but points to {current}. Relinking...")
        CLAUDE_SKILLS.unlink()
    elif CLAUDE_SKILLS.exists():
        backup = Path(str(CLAUDE_SKILLS) + ".bak")
        print(f"⚠️  {CLAUDE_SKILLS} exists as a directory. Backing up to {backup}")
        shutil.move(str(CLAUDE_SKILLS), str(backup))

    if sys.platform == "win32":
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


def setup_notion_mcp():
    print()
    print("── Step 2: Notion MCP ──────────────────────────────")

    if MCP_CONFIG.exists():
        existing = json.loads(MCP_CONFIG.read_text(encoding="utf-8"))
        if "notion" in existing.get("mcpServers", {}):
            print("✅ Notion MCP already configured — skipping.")
            return
        print("⚠️  mcp.json exists but has no Notion entry. Adding it.")
    else:
        existing = {"mcpServers": {}}

    print("  Notion integration token needed.")
    print("  Get it from: notion.so/my-integrations → your integration → Internal Integration Secret")
    print("  (starts with ntn_ or secret_)")
    token = input("  Paste token: ").strip()
    if not token:
        print("⚠️  No token provided — skipping Notion MCP setup.")
        return

    existing.setdefault("mcpServers", {})["notion"] = {
        "command": "npx",
        "args": ["-y", "@notionhq/notion-mcp-server"],
        "env": {
            "OPENAPI_MCP_HEADERS": json.dumps({
                "Authorization": f"Bearer {token}",
                "Notion-Version": "2022-06-28"
            })
        }
    }

    MCP_CONFIG.write_text(json.dumps(existing, indent=2), encoding="utf-8")
    print(f"✅ Written: {MCP_CONFIG}")
    print("   Restart Claude Code to activate. Then share your Notion pages")
    print("   with the integration: page ··· menu → Connections → your integration.")


def setup_obsidian_vault():
    print()
    print("── Step 3: Obsidian vault ──────────────────────────")

    settings_path = CLAUDE_DIR / "settings.json"
    existing = {}
    if settings_path.exists():
        existing = json.loads(settings_path.read_text(encoding="utf-8"))

    if existing.get("env", {}).get("OBSIDIAN_VAULT"):
        print(f"✅ OBSIDIAN_VAULT already set: {existing['env']['OBSIDIAN_VAULT']}")
        return

    print("  Path to your Obsidian vault root (the folder containing your notes).")
    print("  Example: C:\\Users\\you\\Documents\\ObsidianVault")
    vault = input("  Paste path: ").strip()
    if not vault:
        print("⚠️  No path provided — skipping Obsidian vault setup.")
        return

    existing.setdefault("env", {})["OBSIDIAN_VAULT"] = vault
    settings_path.write_text(json.dumps(existing, indent=2), encoding="utf-8")
    print(f"✅ OBSIDIAN_VAULT written to {settings_path}")


def main():
    print("claude-skills setup")
    print()
    setup_skills_symlink()
    setup_notion_mcp()
    setup_obsidian_vault()
    print()
    print("Done! Next: open Claude Code and run 'deploy from Notion' to pull the latest skills.")


if __name__ == "__main__":
    main()
