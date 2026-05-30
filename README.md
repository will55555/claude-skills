# claude-skills

Canonical store of all Claude skills for Will's workspace.  
Notion is the source of truth for authoring. This repo is what gets deployed to machines.

## What's inside

| Skill | What it does |
|---|---|
| `session-context-sync` | End-of-session sync to Notion, Obsidian, and CLAUDE.md in one pass |
| `note-reader` | Read, search, and act on notes from Notion or Obsidian |
| `personal-os-dashboard` | Build interactive HTML personal dashboards |
| `docx` | Create, edit, and manipulate Word documents |
| `xlsx` | Create, edit, and analyze Excel spreadsheets |
| `pptx` | Create and edit PowerPoint presentations |
| `pdf` | Extract, fill, merge, and create PDF files |
| `skill-creator` | Create, improve, and eval new skills |
| `consolidate-memory` | Merge and prune memory files |
| `setup-cowork` | Guided Cowork setup for new installs |
| `schedule` | Create and manage scheduled tasks |

## New machine setup

```bash
# 1. Clone anywhere you like
git clone https://github.com/will55555/claude-skills

# 2. Run setup — it detects the path and confirms before linking
cd claude-skills
python setup.py
```

`setup.py` creates a junction/symlink from `~/.claude/skills` → this repo's `skills/` folder.  
Claude Code picks up all skills automatically after that. No hardcoded paths — works wherever you clone it.

> **Windows note:** Uses `mklink /J` (directory junction — no admin required).  
> **Mac/Linux:** Uses a standard symlink.

## Resuming on a new machine (Claude Code)

After setup, open any project and say:

```
sync from Notion
```

Claude Code will pull the latest project state from your Notion pages and resume without re-explaining.

## Session sync (Claude Desktop / Cowork)

At the end of any substantial session, say **"sync"** or **"wrap up"**.  
The `session-context-sync` skill writes to three targets in one pass:

| Target | What gets written |
|---|---|
| **Notion** | Project state, next action, progress log entry |
| **Obsidian** | Note candidates distilled from the session |
| **CLAUDE.md** | Context snapshot for Claude Code continuity |

## Re-installing skills in Cowork (new machine)

Skills for Cowork install as `.skill` files. On a new machine, tell Claude:

> "Install all skills"

Claude will repackage and present each `.skill` file for installation.

## Repo structure

```
claude-skills/
├── README.md
├── CLAUDE.md          ← Claude Code working memory for this repo
├── setup.py           ← one-time machine setup
├── .gitignore
└── skills/
    ├── session-context-sync/
    ├── note-reader/
    ├── personal-os-dashboard/
    ├── docx/
    ├── xlsx/
    ├── pptx/
    ├── pdf/
    ├── skill-creator/
    ├── consolidate-memory/
    ├── setup-cowork/
    └── schedule/
```

## Notion reference

- **Skills Library:** `36f89370-d497-819d-a89e-e9a7d9b13840`
- **Hub:** `35489370-d497-804f-bf0f-de6d0bee12a2`
- **claude-skills project page:** `37089370-d497-8123-a87d-e47bcd96f0e7`
