# claude-skills Dev Log

## 2026-05-30 — Repo initialized and skills library deployed

### What this is and why it exists
This repo is the canonical source of truth for all Claude Code skills. Skills live here (not on individual machines) so they can be versioned, synced, and deployed to any machine from a single place. Notion mirrors the skills for readability and authoring, but this repo is what Claude Code actually reads.

The key insight: Claude Code resolves skills from a symlink. `setup.py` creates that symlink on each machine, pointing Claude Code's skill directory at this repo. From that point on, pulling this repo = deploying new/updated skills instantly — no manual copy-paste.

---

### How to set up a new machine

```bash
git clone <repo-url> ~/claude-skills
cd ~/claude-skills
python setup.py
```

That's all. The symlink is created once; every subsequent `git pull` automatically updates available skills.

---

### How to deploy skills (Notion → repo)

When Notion has the latest version and you want to push it into the repo:

1. For each skill in the Known Skills table in `CLAUDE.md`, fetch the Notion page via the Notion MCP
2. Extract the raw `SKILL.md` content (frontmatter + body, strip Notion metadata wrapper)
3. Write to `skills/<skill-name>/SKILL.md`
4. Commit: `git add -A && git commit -m "chore: deploy skills from Notion $(date +%Y-%m-%d)"`

Trigger phrase: "deploy", "sync from Notion", or "pull skills"

---

### How to push skills (repo → Notion)

When the repo has changes that Notion doesn't reflect yet:

1. For each skill, read `skills/<skill-name>/SKILL.md`
2. Update the corresponding Notion page content via the Notion MCP
3. Commit any local changes: `git add -A && git commit -m "chore: sync skills $(date +%Y-%m-%d)"`

Trigger phrase: "push to Notion" or "sync skills to Notion"

---

### Skill inventory

| Skill | Purpose |
|-------|---------|
| `session-context-sync` | End-of-session sync → Notion, Obsidian, CLAUDE.md |
| `consolidate-memory` | Deduplicate and prune memory files |
| `docx` | Word document creation and editing (.docx) |
| `note-reader` | Read notes from Notion / Obsidian |
| `pdf` | PDF read, fill, merge, split, OCR |
| `personal-os-dashboard` | Single-file HTML personal command-center dashboards |
| `pptx` | PowerPoint deck creation and editing (.pptx) |
| `schedule` | Scheduled remote agent cron jobs |
| `setup-cowork` | Cowork onboarding and plugin setup |
| `skill-creator` | Skill authoring framework with evals and benchmarks |
| `xlsx` | Excel workbook read/write/recalc (.xlsx) |

---

### Design decisions worth knowing

**Why `docx`, `pptx`, and `xlsx` each duplicate the OOXML schema bundle?**
Each skill is intentionally self-contained — no cross-skill dependencies. Duplication is the tradeoff for portability and isolation. If one skill's schema needs updating, it doesn't break the others.

**Why `skill-creator` has multi-agent evaluators?**
Building a new skill reliably requires iterative testing against real benchmarks. `skill-creator` includes `analyzer.md`, `comparator.md`, and `grader.md` agents plus a benchmark runner so new skills can be scored before being added to the library.

**Why Notion as the authoring surface?**
Notion is easier to read and edit than raw markdown for non-code content. The repo is the deploy target, not the authoring surface — that's why the deploy flow goes Notion → repo, not the other way around by default.
