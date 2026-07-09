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
| `session-rules` | ARCHIVED as full skill 2026-07-09 — gutted to a thin Working Memory mirror; full system now lives in the Engineering Hub |
| `setup-cowork` | Cowork onboarding and plugin setup |
| `skill-creator` | Skill authoring framework with evals and benchmarks |
| `xlsx` | Excel workbook read/write/recalc (.xlsx) |
| ~~`dev-log`~~ | ARCHIVED 2026-07-09 — absorbed into the Engineering Hub's Documentation Protocol; frontmatter neutralized, kept for schema reference only |

Note: `skills/ai-control/` (the Engineering Hub) is NOT in this table — it's intentionally not a
frontmattered, auto-discovered skill (see its own `HUB.md` Mission section for why), and it is NOT
part of the Notion deploy/push flow above (see the 2026-07-09 entry below for why).

---

### Design decisions worth knowing

**Why `docx`, `pptx`, and `xlsx` each duplicate the OOXML schema bundle?**
Each skill is intentionally self-contained — no cross-skill dependencies. Duplication is the tradeoff for portability and isolation. If one skill's schema needs updating, it doesn't break the others.

**Why `skill-creator` has multi-agent evaluators?**
Building a new skill reliably requires iterative testing against real benchmarks. `skill-creator` includes `analyzer.md`, `comparator.md`, and `grader.md` agents plus a benchmark runner so new skills can be scored before being added to the library.

**Why Notion as the authoring surface?**
Notion is easier to read and edit than raw markdown for non-code content. The repo is the deploy target, not the authoring surface — that's why the deploy flow goes Notion → repo, not the other way around by default.

---

## 2026-07-09 — Engineering Hub v1.1 built and deployed

### What this is and why it exists
Personal (not Terra-specific) session/behavior control system, adapted from Will's work
Engineering Hub. Lives at `skills/ai-control/` as four plain docs (HUB.md, HUB_GUIDE.md,
HUB_STATE.md, TASKS.md) — deliberately NOT a frontmattered skill, reached via `load hub` or a
repo's CLAUDE.md pointer, not the symlink/auto-discovery mechanism described above.

### Key design decisions
- **Git is sole source of truth for `ai-control/`**; Notion may hold an informational dupe of hub
  state, never authoritative. This is the deliberate exception to this repo's Notion-authored-skills
  pattern above — the hub's fast local-edit design (Linear Fetch, `sync state`) needs one writer.
- **Linear Fetch Mode + snapshot-vs-log growth rule**: hot files (HUB_STATE sections) stay
  constant-size and overwritten in place; only cold files (DEV_LOGs) grow — guarantees single-pass
  retrieval regardless of how much history accumulates.
- **dev-log and session-rules skills absorbed** into the hub (Documentation Protocol, Working
  Memory Contract respectively); session-rules kept only as a thin WM-only mirror for web/mobile
  sessions that can't read local hub files.
- **Universal Sync & Fallback Queue**: Notion doubles as an informational dupe AND a drainable
  queue for content that missed its real target (git/Obsidian) when unreachable, tagged
  `#SyncQueue` and retried on next sync.
- **`sync skills` trigger** (git-only, local write + supplied commands, never auto-pushed) is
  deliberately distinct from this file's "push to Notion"/"deploy" phrases above — dropped the
  `push skills` variant specifically to reduce collision risk; full resolution still open.

### Files created/modified
- `skills/ai-control/HUB.md`, `HUB_GUIDE.md`, `HUB_STATE.md`, `TASKS.md` — new
- `skills/session-rules/SKILL.md` — gutted to WM-only mirror
- `skills/session-context-sync/SKILL.md` — Step 4C rewritten (HUB_STATE write, not CLAUDE.md);
  Target Overview updated with git-authority rule + Universal Sync & Fallback Queue
- `skills/archive/dev-log/SKILL.md` — neutralized (absorbed into hub Documentation Protocol)
- `skills/archive/session-rules-duplicate-OLD/SKILL.md` — found and neutralized; had been sitting
  in a stray "New folder/" with a colliding `name: session-rules` and drifted Notion IDs from
  before this session's ID-table cleanup

### Error — path references pointed at the wrong location
**Where:** HUB.md, HUB_GUIDE.md, session-rules, session-context-sync — all referenced
`claude-skills/ai-control/` when the real deployed location is `claude-skills/skills/ai-control/`.
**Root cause:** written before the files were actually placed on disk; assumption never verified
against the real deploy path.
**Fix:** corrected every reference across all four files.
**Why not leave it:** the GitHub raw URL, CLAUDE.md pointer template, and git reminder commands
would all have pointed at a path that doesn't exist.

### Known limitations / next
- CLAUDE.md pointers not yet placed in terra-api, roms, pios, terra-hq-site (SKILLS-005) — verify
  actual relative folder depth before pasting (default template assumes siblings under SDE/)
- Trigger-name collision between `sync skills` and this repo's "sync skills to Notion"/"deploy"
  phrases — partially mitigated, not fully resolved; needs Will's decision
- This repo's Notion mirror of session-context-sync is stale relative to tonight's edits — risk if
  "deploy"/"pull skills" runs before Notion is updated to match (SKILLS-014)
- Not yet dogfooded: first real test is `load hub tapi` in a fresh Claude Code session (SKILLS-006)
