---
name: session-context-sync
description: |
  Unified session-end sync skill. Triggers at end of any substantial session — coding, planning, design, or learning. Handles three write targets in one pass: Notion (project state), Obsidian (note candidates), and the Engineering Hub's HUB_STATE.md (live project snapshot). Trigger on: "sync", "wrap up", "end of session", "push to Notion", "update Notion", "update Obsidian", "sync state", or proactively when meaningful work was done on any active project. Always prompt at session end — never skip when the session produced decisions, code, or learning artifacts.
---

# Session Sync Skill

Unified end-of-session sync across three targets: Notion, Obsidian, and the Engineering
Hub's HUB_STATE.md. Runs in a single pass at session end. Each target is independent —
one can be skipped without affecting the others.

Note: Notion page IDs and the Projects DB reference are NOT stored in this file — they
live in Claude memory (userMemories) as the single source of truth. Look them up there;
do not maintain a duplicate table here.

---

## Target Overview

| Target | What gets written | Trigger condition | Source |
|---|---|---|---|
| **Notion** | Project state snapshot + progress log | Session produced Notion-worthy content (see classification below) | Desktop or Code |
| **Obsidian** | Note candidate(s) distilled from session | Session produced a concept, pattern, or decision worth keeping | Desktop or Code |
| **HUB_STATE.md** | Active project section snapshot (overwrite in place) | Session touched a hub-tracked project (any Terra project, DSA, claude-skills, etc.) | Desktop or Code |

Both Claude Desktop and Claude Code sessions sync to all three targets.
The session type determines what content is available, not which targets apply.

---

## Notion-Worthiness Classification

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
- Meta sessions unless a new project was created

When in doubt: ask "did the project state change?" If no → skip Notion.

---

## Step 1 — Extract session content

- **Working Memory block** — Core Objective, Key Facts, Progress & Current State, Next Step
- **Key decisions** — ADRs, design choices, implementation choices
- **Code completed** — file names, method names, what was built or changed
- **Concepts learned** — patterns, tradeoffs, architecture principles
- **Blockers** — anything flagged VERIFY, TODO, or unresolved
- **Next action** — the most specific next step discussed (feeds HUB_STATE's Next Step field)

---

## Step 2 — Classify session and determine targets

```
Session classification:
→ Session type: [Desktop / Code]
→ Notion: [yes — reason] / [no — reason]
→ Obsidian: [yes — candidate list] / [no]
→ HUB_STATE: [yes — which project section] / [no]
```

---

## Step 3 — Show sync preview and confirm

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
[1-line preview of Key Insight]

─── HUB_STATE ───────────────────────────
Project section: [name — must match an existing HUB_STATE.md heading, or propose
                   a new one from the HUB_GUIDE section template]
Updates: Status / Active Task / Next Step / Blockers / Context (≤3 lines)

Sync all? (yes / edit first / skip [notion|obsidian|hubstate])
```

---

## Step 4A — Notion sync

### Database reference
Look up in Claude memory (userMemories): Hub page, Projects DB, data source, and known
project page IDs. Do not hardcode or duplicate these here — they drift when stored in
two places (this table drifted from session-rules' copy before consolidation).

### Page template sections

```
## 🎯 Overview         ← written once, rarely updated
## 📍 Current State    ← ALWAYS update on sync
## ⏭️ Next Action      ← ALWAYS update on sync
## 🚧 Blockers         ← ALWAYS update on sync (write "None active." if clear)
## 📋 Progress Log     ← ALWAYS prepend newest entry, never overwrite
```

### Log entry format

```markdown
---
### YYYY-MM-DD
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

1. Search Projects DB by name via `notion-search`
2. If found — use that page ID
3. If not found — create via `notion-create-pages` with full template
4. Tell Will to add the new page ID to Claude memory (not to this skill file)

---

## Step 4B — Obsidian sync

### Vault root — runtime discovery

**Preferred (Claude Code):** Read `OBSIDIAN_VAULT` env var from `~/.claude/settings.json`.

**Fallback (Claude Desktop):**
1. Call `Filesystem:list_allowed_directories`
2. Identify entry containing "Obsidian" or "ObsidianVault"

If neither resolves, ask Will and remind them to run `setup.py`.

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

### Note format

```markdown
> **What this note is:** [One sentence — what this note covers and why it was written]

#tag #tag #tag

### What is it?
[One concise paragraph]

### Why it matters
[Consequence, impact, relevance to your work]

### How it works
[Mechanism, flow, or structure]

### The design principles behind it

| Principle | What it means |
|---|---|
| [name] | [1-line explanation] |

### Key insight
[One sentence that would make future-Will immediately recall why this mattered]

## Related Notes
- [[Note Title]] — [one-line description of relationship]
```

### Filename convention
- Concept notes (`Software Development/`, `Trading/`, etc.): `lowercase-hyphenated.md`
- Project notes (`Projects/ROMS/`, `Projects/PIOS/`, etc.): `NN - Title.md` (two-digit prefix)

Never overwrite an existing note — append a dated update section instead.

---

## Step 4C — HUB_STATE.md sync

Replaces the former CLAUDE.md sync. Per-repo CLAUDE.md files are now thin pointers to
HUB_GUIDE.md and are not rewritten per session — live state lives in one place:
`claude-skills/skills/ai-control/HUB_STATE.md`.

### Procedure

1. Locate the project's existing section in HUB_STATE.md (heading match). If none
   exists, propose a new section using the template in HUB_GUIDE.md → "HUB_STATE
   Section Template" and confirm with Will before adding it.
2. OVERWRITE the section in place — Status, Active Task, Next Step, Blockers, Context.
   Do not append or accumulate history here; history belongs in the project's own
   DEV_LOG.md (Documentation Protocol, in HUB_GUIDE.md), not in HUB_STATE.
3. Keep the section within its ~15–20 line budget. Context field stays ≤3 lines —
   snapshot, not narrative.
4. Update the freshness stamp at the top of HUB_STATE.md.
5. If this session produced a dev-log-worthy phase or decision, hand off to the
   Documentation Protocol (HUB_GUIDE.md) for the actual DEV_LOG.md entry — HUB_STATE
   only gets the resulting Next Step / Status, not the narrative.

---

## Step 5 — Post-sync confirmation

```
✅ Session sync complete

Notion     → [project] updated
Obsidian   → [note title] written to [vault path]
HUB_STATE  → [project] section overwritten (claude-skills/skills/ai-control/HUB_STATE.md)

Remind: git add skills/ai-control/HUB_STATE.md && git commit && git push if not done.
```

---

## Step 6 — Deploy to claude-skills repo

**Mandatory when a skill or hub file was updated or created this session.**

### Path resolution

1. Use the path where the hub/skills were read from — that IS the repo root.
2. If not writable, fall back to `https://github.com/will55555/claude-skills` and notify Will.
3. Never guess a path. Never silently skip.

```bash
cd <repo-root> && git add -A && git commit -m "chore: sync session output $(date +%Y-%m-%d)"
```

Remind Will to `git push` — web/Desktop sessions read the pushed copy of the hub, so
an unpushed commit means those sessions see stale state.

---

## Error handling

| Error | Action |
|---|---|
| Notion MCP timeout | Retry once; show preview for manual paste if fails |
| Vault path not found | Ask Will to confirm vault root |
| HUB_STATE section not found for project | Propose new section from template; confirm before adding |
| Ambiguous project name | Confirm before any write |
| Multiple projects in session | Sync each separately |
| Note file already exists | Append dated update section |
| claude-skills repo not found | Fall back to GitHub URL, notify Will |
