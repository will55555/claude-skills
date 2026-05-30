# claude-skills — Claude Code Context

## What this repo is
Canonical store of all Claude skills for Will's workspace.
Notion mirrors them for readability and authoring. This repo is what gets deployed to machines.

## Structure
```
claude-skills/
├── CLAUDE.md          ← this file (Claude Code working memory)
├── setup.py           ← one-time machine setup (creates symlink)
├── .gitignore
└── skills/
    ├── session-context-sync/
    │   └── SKILL.md
    ├── note-reader/
    │   └── SKILL.md
    └── personal-os-dashboard/
        └── SKILL.md
```

## New machine setup
```bash
git clone <repo-url> ~/claude-skills
cd ~/claude-skills
python setup.py
```
That's it. Claude Code will read skills from this repo going forward.

## Deploy — pull from Notion → write to repo

When user says "deploy", "sync from Notion", or "pull skills":

1. For each skill in the Known Skills table below, fetch the Notion page using the Notion MCP
2. Extract the raw SKILL.md content (frontmatter + body, strip Notion metadata wrapper)
3. Write to `skills/<skill-name>/SKILL.md`
4. Run: `git add -A && git commit -m "chore: deploy skills from Notion $(date +%Y-%m-%d)"`

## Push — write to repo → push to Notion

When user says "push to Notion" or "sync skills to Notion":

1. For each skill, read `skills/<skill-name>/SKILL.md`
2. Update the corresponding Notion page content
3. Run: `git add -A && git commit -m "chore: sync skills $(date +%Y-%m-%d)"` if any local changes

## Known Skills

| Skill | Notion Page ID |
|---|---|
| session-context-sync | 36f89370-d497-818c-848f-fd5f219f2396 |
| note-reader | 36f89370-d497-817089bcc30be8e9ef2d |
| personal-os-dashboard | TBD — add after first deploy |
| claude-skills | 37089370-d497-8123-a87d-e47bcd96f0e7 |

## Notion reference
- Skills Library page: `36f89370-d497-819d-a89e-e9a7d9b13840`
- Hub: `35489370-d497-804f-bf0f-de6d0bee12a2`
