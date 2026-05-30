---
name: session-context-sync
description: |
  Unified session-end sync skill. Triggers at end of any substantial session — coding, planning, design, or learning. Handles three write targets in one pass: Notion (project state), Obsidian (note candidates), and CLAUDE.md (context snapshot for Claude Code). Trigger on: "sync", "wrap up", "end of session", "push to Notion", "update Notion", "update Obsidian", "update CLAUDE.md", or proactively when meaningful work was done on ROMS, PIOS, or any active project. Always prompt at session end — never skip when the session produced decisions, code, or learning artifacts.
---

# Session Sync Skill

Unified end-of-session sync across three targets: Notion, Obsidian, and CLAUDE.md.
Runs in a single pass at session end. Each target is independent — one can be skipped
without affecting the others.

---

## Target Overview

| Target | What gets written | Trigger condition | Source |
|---|---|---|---|
| **Notion** | Project state snapshot + progress log | Session produced Notion-worthy content (see classification below) | Desktop or Code |
| **Obsidian** | Note candidate(s) distilled from session | Session produced a concept, pattern, or decision worth keeping | Desktop or Code |
| **CLAUDE.md** | Context snapshot for Claude Code continuity | Session touched a repo-level project (ROMS, PIOS, etc.) | Desktop or Code |

Both Claude Desktop and Claude Code sessions sync to all three targets.
The session type determines what content is available, not which targets apply.

---

## Notion-Worthiness Classification

Not everything belongs in Notion. Apply this filter before including anything in the Notion sync:

**✅ Notion-worthy — always include:**
- Project state change (started, completed, blocked, unblocked)
- A decision made that affects the project direction or architecture
- Code built or shipped (file, method, feature, fix)
- A blocker surfaced or resolved
- A next action that is specific and actionable

**⚠️ Notion-worthy — include if substantial:**
- Design discussion that landed on a clear direction
- A spike or research session with a concrete conclusion
- Dependency or external factor that affects timeline

**❌ Not Notion-worthy — skip:**
- Pure learning / concept exploration with no project output
- Brainstorming that didn't converge
- Planning that produced no decisions
- Tooling setup that didn't touch a project
- Meta sessions (like designing this pipeline) unless a new project was created

When in doubt: ask "did the project state change?" If no → skip Notion.

---

## Step 1 — Extract session content

Pull the following from the current session:

- **Working Memory block** — Core Objective, Key Facts, Progress & Current State
- **Key decisions** — ADRs, design choices, implementation choices, anything marked decided
- **Code completed** — file names, method names, what was built or changed
- **Concepts learned** — patterns, tradeoffs, architecture principles, anything worth a note
- **Blockers** — anything flagged VERIFY, TODO, or unresolved
- **Next action** — the most specific next step discussed

If no Working Memory block exists, summarize from context directly.

---

## Step 2 — Classify session and determine targets

First identify session type:
- **Desktop chat** — planning, design, learning, debugging discussion
- **Claude Code** — active coding, devlog entries, file writes, repo changes

Then apply the Notion-worthiness classification above and infer targets:

```
Session classification:
→ Session type:  [Desktop / Code]
→ Notion:        [yes — reason] / [no — reason]
→ Obsidian:      [yes — candidate list] / [no]
→ CLAUDE.md:     [yes — which repo] / [no]
```

If all three apply, present a single combined preview before writing anything.
If only one applies, skip the others silently — do not ask about skipped targets.

---

## Step 3 — Show sync preview and confirm

Show a combined preview before any writes:

```
📤 Session Sync Preview

─── NOTION ──────────────────────────────
Project: [name]
Current State: [1-2 sentences]
Next Action: [1 sentence]
Blockers: [list or "None"]
Log entry: [date + 2-3 bullet summary]

─── OBSIDIAN ────────────────────────────
Note: [title]
Tags: #tag #tag
Vault path: [Projects/PIOS/ or Concepts/ etc.]
Sections: What / Why / How / Principles / Key Insight
[1-line preview of Key Insight]

─── CLAUDE.md ───────────────────────────
Repo: [project name]
Updates: Objective / Stack / State / Next Action / Blockers
[show diff from current CLAUDE.md if it exists]

Sync all? (yes / edit first / skip [notion|obsidian|claude])
```

Only proceed after confirmation. Accept inline edits if user says "edit first".

---

## Step 4A — Notion sync

### Database reference (do not search — use directly)

| Item | Value |
|---|---|
| Hub page | `35489370-d497-804f-bf0f-de6d0bee12a2` |
| Projects DB | `6eafacec-385d-4336-9f02-1f60839b82d3` |
| Data source | `collection://cf8f7353-f469-44bf-bbf2-56e1dfa280f3` |

### Known project page IDs

| Project | Page ID | Domain |
|---|---|---|
| ROMS | `36f89370-d497-8171-b111-e09ba33ec354` | Coding |
| PIOS | `36f89370-d497-8140-a5a9-d14f76ddaefd` | Coding |
| claude-skills | `37089370-d497-8123-a87d-e47bcd96f0e7` | Coding |

For unknown projects search DB first, create if missing (see Step 4A-new below).

### Page template sections

```
## 🎯 Overview         ← written once, rarely updated
## 📍 Current State    ← ALWAYS update on sync
## ⏭️ Next Action      ← ALWAYS update on sync
## 🚧 Blockers         ← ALWAYS update on sync (write "None active." if clear)
## 📋 Progress Log     ← ALWAYS prepend newest entry, never overwrite
```

### Log entry format (prepend, newest on top)

```markdown
---
### 2026-05-30
- Built X, implemented Y
- Decided: [key decision + rationale]
- Verified: [anything confirmed]
- Flagged: [anything marked VERIFY or blocked]
```

### Domain mapping for new projects

| Project type | Domain |
|---|---|
| ROMS, PIOS, Terra API, any SDE build | Coding |
| Terra Inc entity ops, strategy | Business |
| Investing, PIOS-governed capital | Finance |
| Everything else | Personal |

### Step 4A-new — Handle unknown projects

1. Search Projects DB by name via `notion-search` with data_source_url
2. If found — use that page ID
3. If not found — create via `notion-create-pages` with full template
4. Tell user to add the new page ID to this skill's known IDs table

---

## Step 4B — Obsidian sync

### Vault root — runtime discovery

Never hardcode the vault path. At sync time, try in order:

**Preferred (Claude Code):** Read the `OBSIDIAN_VAULT` env var from `~/.claude/settings.json` — set automatically by `setup.py` on new machines. If present, use it directly.

**Fallback (Claude Desktop / if env var not set):**
1. Call `Filesystem:list_allowed_directories`
2. Identify the entry containing "Obsidian" or "ObsidianVault" — that is the vault root
3. Use that path as the base for all writes this session

If neither resolves, ask the user for the path and remind them to run `setup.py` or add `OBSIDIAN_VAULT` to `~/.claude/settings.json` under `env`.

This makes the skill machine-agnostic — works on Windows, VM, or any future machine
as long as the Obsidian vault is in the allowed directories.

### Vault path registry

| Project / Topic | Vault path |
|---|---|
| ROMS | `Projects/ROMS/` |
| PIOS | `Projects/PIOS/` |
| Terra Inc | `Projects/Terra/` |
| Architecture / System Design | `Software Development/System Design/` |
| Languages / CS fundamentals | `Software Development/1-Languages/` |
| Full-stack patterns | `Software Development/2-Full-Stack Integration/` |
| DevOps / infra | `Software Development/DevsOp/` |
| Testing | `Software Development/Testing/` |
| Trading concepts | `Trading/` |
| Business / Terra strategy | `Business/` |
| AutoCAD | `AutoCAD/` |

If a new topic doesn't fit above, ask Will which folder before writing.

### Note format (always use this schema)

```markdown
> **What this note is:** [One sentence — what this note covers and why it was written]

#tag #tag #tag

### What is it?
[One concise paragraph — definition, no fluff]

### Why it matters
[Why this is worth knowing — consequence, impact, relevance to your work]

### How it works
[Mechanism, flow, or structure — as specific as the concept allows]

### The design principles behind it

| Principle | What it means |
|---|---|
| [name] | [1-line explanation] |

### Key insight
[One sentence that would make future-Will immediately recall why this mattered]

## Related Notes
- [[Note Title]] — [one-line description of relationship]
```

### Write procedure

```
1. Discover vault root via Filesystem:list_allowed_directories
2. Use Filesystem:write_file to write to:
   [discovered vault root]\[vault-path]\[note-title].md
3. Confirm write with Filesystem:read_file on the written path
```

**Claude Code alternative** (no Filesystem MCP available):
```
1. Read vault root from $OBSIDIAN_VAULT env var (set by setup.py in ~/.claude/settings.json)
2. Write using the Write tool to: [vault root]\[vault-path]\[note-title].md
3. Confirm using the Read tool on the written path
```

- Filename:
  - Concept / pattern notes (Software Development/, Trading/, etc.): `lowercase-hyphenated.md` (e.g. `dev-log-two-mode-pattern.md`)
  - Project notes inside a project folder (Projects/ROMS/, Projects/PIOS/, etc.): `NN - Title.md` with two-digit prefix matching the next available number in that folder (e.g. `12 - ROMS Auth Rehydration.md`)
- Never overwrite an existing note — if file exists, append a dated update section instead
- Confirm write succeeded with `cat` of the written file

### Surfacing note candidates

When the session produced multiple learnable concepts, list them all in the preview:

```
Obsidian candidates this session:
1. [concept name] → Concepts/Architecture/
2. [concept name] → Projects/PIOS/
Which should I write? (all / 1,2 / none)
```

---

## Step 4C — CLAUDE.md sync

### What CLAUDE.md is

A context snapshot committed to the repo root. Claude Code reads it at session start
to resume without re-explaining. It is not documentation — it is working memory for
the coding agent.

### CLAUDE.md schema

```markdown
# [Project Name] — Claude Code Context

## Objective
[One sentence: what this project is and what's being built]

## Stack
[Language, framework, key deps — one line each]

## Current State
[What's done, what's in progress — 2-4 bullets]

## Next Action
[The single most specific next coding task]

## Open Blockers
[Anything unresolved, needing verification, or waiting on info]

## Key Decisions Log
| Date | Decision | Rationale |
|---|---|---|
| [date] | [decision] | [why] |
```

### Write procedure

```bash
# Check if CLAUDE.md exists in repo root
cat ~/[repo-path]/CLAUDE.md 2>/dev/null || echo "NOT FOUND"

# Write or overwrite
cat > ~/[repo-path]/CLAUDE.md << 'EOF'
[formatted CLAUDE.md content]
EOF
```

- If CLAUDE.md already exists: merge new state with existing Decisions Log (never drop prior decisions)
- Repo paths: `~/projects/roms/`, `~/projects/pios/` — confirm with Will if unsure
- CLAUDE.md is committed to the repo — remind Will to `git add CLAUDE.md && git commit -m "chore: update claude context"` after writing

---

## Step 5 — Post-sync confirmation

After all writes complete, show a brief summary:

```
✅ Session sync complete

Notion    → [project] updated (Current State, Next Action, log entry prepended)
Obsidian  → [note title] written to [vault path]
CLAUDE.md → [project] context snapshot written to [repo path]

Remind: git add CLAUDE.md && git commit if you haven't already.
```

If any target was skipped, note it:
```
Obsidian  → skipped (no new concepts this session)
```

---

## Step 6 — Deploy to claude-skills repo

**This step is not optional when a skill was updated or created this session.** Always run it after any session that touched a skill.

Triggers:
- A skill was updated (content changed, new section added, etc.)
- A new skill was created this session
- User says "sync", "deploy", or "push to repo"

For all other sessions (no skill changes), offer it and let Will skip.

```
Deploy updated skills to claude-skills repo? (yes / skip)
```

### What to write

- **Updated skill**: overwrite `<repo-root>/skills/<skill-name>/SKILL.md` with current content
- **New skill**: create `<repo-root>/skills/<skill-name>/SKILL.md` (mkdir if needed)
- **Both**: write all changed skills in one commit

### Path resolution (always follow this order)

1. **Use the path where CLAUDE.md was read from** — that directory IS the repo root.
2. **If that path doesn't exist or isn't writable**, fall back to the GitHub URL:
   `https://github.com/will55555/claude-skills`
   Then notify Will:
   > ⚠️ Local repo path not found — could not write to disk. Reference: https://github.com/will55555/claude-skills
   > Run `python setup.py` from your clone, or tell me the correct path and I'll update CLAUDE.md.
3. **Never guess a path** (e.g. `~/claude-skills`). Never silently skip — always tell Will what happened.

### If path is valid

1. Write each changed SKILL.md to `<repo-root>/skills/<skill-name>/SKILL.md`
2. Run:
   ```bash
   cd <repo-root> && git add -A && git commit -m "chore: sync skills from Notion $(date +%Y-%m-%d)"
   ```
3. Remind Will to `git push` if the repo has a remote.

---

## Error handling

| Error | Action |
|---|---|
| Notion MCP timeout | Retry once; if fails, show preview content and tell user to paste manually |
| Vault path not found | Ask user to confirm vault root before writing |
| CLAUDE.md repo path unknown | Ask user for repo path — do not guess |
| Ambiguous project name | Ask user to confirm before any write |
| Multiple projects in one session | Sync each separately, confirm each |
| Note file already exists | Append dated update section, never overwrite |
| claude-skills repo not found | Skip Step 6, note in summary |
