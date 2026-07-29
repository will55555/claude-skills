---
name: session-context-sync
description: |
  Unified session-end sync skill. Triggers at end of any substantial session — coding, planning, design, or learning. Handles four write targets in one pass: Notion (project state), Obsidian (note candidates), the Engineering Hub's HUB_STATE.md (live project snapshot), and Tasks DB (actionable items). Trigger on: "sync", "wrap up", "end of session", "push to Notion", "update Notion", "update Obsidian", "sync state", or proactively when meaningful work was done on any active project. Always prompt at session end — never skip when the session produced decisions, code, or learning artifacts.
---

# Session Sync Skill

Unified end-of-session sync across four targets: Notion, Obsidian, the Engineering
Hub's HUB_STATE.md, and Tasks DB. Runs in a single pass at session end. Each target is independent —
one can be skipped without affecting the others.

Note: Notion page IDs and the Projects DB reference are NOT stored in this file — they
live in Claude memory (userMemories) as the single source of truth. Look them up there;
do not maintain a duplicate table here.

Note: this skill is EXCLUDED from the repo's Notion deploy/push flow (see root `DEV_LOG.md`) as
of 2026-07-09 — it's too tightly coupled to hub-specific design (git-authority rule, Sync Queue)
to safely dual-author between Notion and git. Edit this file directly in the repo. Do not run
"deploy"/"pull skills" against this specific file, and do not "push to Notion" from it either.

---

## Target Overview

| Target | What gets written | Trigger condition | Source |
|---|---|---|---|
| **Git (ai-control hub)** | HUB.md/HUB_GUIDE.md/HUB_STATE.md/TASKS.md — AUTHORITATIVE | Any hub/skill file edited | Local write + git commands supplied (never auto-pushed) |
| **Notion** | Project state snapshot + progress log (page CONTENT) + Status/Last Synced (page PROPERTIES — see Step 4A-props); ALSO an informational mirror/dupe of hub state (never authoritative) | Session produced Notion-worthy content, or hub state changed | Desktop or Code |
| **Obsidian** | Note candidate(s) distilled from session | Session produced a concept, pattern, or decision worth keeping | Desktop or Code |
| **HUB_STATE.md** | Active project section snapshot (overwrite in place) | Session touched a hub-tracked project (any Terra project, DSA, claude-skills, etc.) | Desktop or Code |
| **Tasks DB** | New task rows (actionable items for routing to appropriate tool/hub) | Session surfaced an actionable item not already in Tasks DB — from chat commitments, buried TODOs in a Notion page touched this session, or action items from Gmail/Calendar tool results this session | Desktop or Code |

Both Claude Desktop and Claude Code sessions sync to all targets that apply.
The session type determines what content is available, not which targets apply.

**Source-of-truth rule:** Git is the sole authority for `ai-control/` (the Engineering Hub).
Notion may hold a dupe/mirror of hub state for visibility — useful on mobile, useless as an
edit-back path. On any conflict between Notion and git, git wins, always. This is the deliberate
exception to this repo's Notion-authored-skills pattern (see root `DEV_LOG.md` / `CLAUDE.md`) —
the hub's fast local-edit design (Linear Fetch, `sync state`) depends on git being the only writer.

---

## Universal Sync & Fallback Queue

Every `sync` invocation attempts ALL applicable targets in one pass. If a target succeeds,
write normally. If a target is unreachable, don't drop the content — queue it instead.

**Why Notion is the queue:** Notion is reachable from nearly every session type via MCP,
even when the "real" target (git, Obsidian, Tasks DB) isn't. So unreachable content gets written to
a **Notion Sync Queue** page, tagged with its true intended destination, and drained on a
future sync once that destination is reachable again.

### Queue entry format (written to the Sync Queue page in Notion)
```
#SyncQueue #target:<git|obsidian|notion|tasks>
Status: Pending
Payload: [the content that couldn't be written to its real destination]
Queued: [date]
Session type: [Desktop | Code | Mobile]
```

### Procedure
1. On `sync`, attempt each applicable target (git/hub, Notion, Obsidian, Tasks DB).
2. Any failure → write a queue entry to the Sync Queue page instead (create the page on
   first use; its ID then lives in Claude memory, not hardcoded in this skill).
3. At the START of every sync, before writing new content, check the Sync Queue for
   Pending items whose target is now reachable — drain them (write to the real
   destination), then mark that entry Synced (kept as history, not deleted).
4. **Last-resort fallback:** if Notion itself is unreachable (rare), fall back to a
   downloadable staged file in `/mnt/user-data/outputs/`, and tell Will explicitly that
   even the queue couldn't be written remotely.
5. Notion serves two distinct roles simultaneously: an informational DUPE of hub state
   (never authoritative — see Target Overview above), and a temporary QUEUE for anything
   that missed its real destination (tagged #SyncQueue, drained later). Don't confuse the
   two — dupes are permanent visibility copies; queue entries are transient and get marked
   Synced.

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
- **Task candidates** — scan three ways, tag each with its Source:
  1. *Claude-Chat*: commitment language in this session ("I need to", "I should", "remind me to", "have to follow up on", "next I'll") that isn't just a Next Action already captured above
  2. *Notion-Note*: unchecked TODO/checkbox lines on any Notion page read or edited this session that aren't already rows in Tasks DB
  3. *Email/Calendar*: actionable items surfaced in any Gmail/Calendar tool results returned this session (not a scheduled inbox scan — only what came up organically)

---

## Step 2 — Classify session and determine targets

```
Session classification:
→ Session type: [Desktop / Code]
→ Notion: [yes — reason] / [no — reason]
→ Obsidian: [yes — candidate list] / [no]
→ HUB_STATE: [yes — which project section] / [no]
→ Tasks DB: [yes — N candidates found] / [no]
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
Properties: Status → [Active/Blocked/Done, from session outcome] | Last Synced → [today]

─── OBSIDIAN ────────────────────────────
Note: [title]
Tags: #tag #tag
Vault path: [Projects/PIOS/ or Concepts/ etc.]
[1-line preview of Key Insight]

─── HUB_STATE ───────────────────────────
Project section: [name — must match an existing HUB_STATE.md heading, or propose
                   a new one from the HUB_GUIDE section template]
Updates: Status / Active Task / Next Step / Blockers / Context (≤3 lines)

─── TASKS DB ─────────────────────────────
1. [title] — Source: Claude-Chat — Domain: Coding — linked project: [name or none]
2. [title] — Source: Notion-Note — Domain: Personal — from page: [page name]
[list all candidates; omit section entirely if none found]

─── SYNC QUEUE (if any target unreachable) ──
[target] unreachable → queued in Notion Sync Queue, will retry next sync

Sync all? (yes / edit first / skip [notion|obsidian|hubstate|tasks])
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

### Step 4A-props — Update DB properties (required, not optional)

Content sections (Current State, Next Action, etc.) are page CONTENT. The
command-center.html dashboard and the tracker-sync skill read page
PROPERTIES only (Status, Priority, Last Synced) — they never parse page
body content. Writing content without updating properties means the
dashboard silently never reflects the sync, even though Notion looks
updated when you open the page directly.

Every Notion sync MUST also update, as actual database properties (not
text in the body):
- **Last Synced** → today's date, always, if any Notion write happened.
- **Status** → set from session outcome: session ended with the project
  blocked → "Blocked"; project finished/shipped → "Done"; anything else
  with real progress → "Active". Don't downgrade Active → Not Started
  just because a session was quiet — only move it to Not Started if the
  session explicitly determined no work has started yet.

Use `notion-update-page` with the property fields directly (same call
shape used elsewhere for Status/Priority/date properties) — do not encode
these as text inside the page body.

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

## Step 4D — Tasks DB sync

### Database reference
Tasks DB ID lives in Claude memory (userMemories), not here — same rule as Notion in Step 4A.

### Dedup check (mandatory before any write)
Query Tasks DB (title match, loose) for each candidate before creating it. If a
matching open task already exists, skip it silently — do not create a duplicate or
ask about it. Only net-new items go in the preview.

### Row fields
| Field | Value |
|---|---|
| Title | Short, action-first (e.g. "Follow up on Snorkel invoice timing") |
| Source | Claude-Chat / Notion-Note / Email / Calendar — select property (added to Tasks DB) |
| Domain | Coding / Engineering / Business / Finance / Personal / Work — existing select property on Tasks DB, reused for routing (do NOT create a separate "Type" property) |
| Captured | Today's date |
| Linked Project | Project page, if the task ties to one (ROMS, PIOS, Terra SDE, etc.) — else blank |
| Notes | 1 line of context — where it came from, e.g. "mentioned in session re: X" |

### Domain — routing taxonomy
This is what lets a hub or tool fetch only the tasks relevant to it (e.g. Claude Code
pulling only Coding tasks, Cowork pulling only Engineering/automation tasks). Reuses
the Tasks DB's existing Domain property (Work/Finance/Personal/Business/Coding) with
one addition — Engineering, added specifically for infra/automation/non-code build
work — rather than inventing a second parallel property:

| Domain | Covers | Typical fetcher |
|---|---|---|
| Coding | ROMS, PIOS, Terra API/SDE, any code change, bug, feature | Claude Code |
| Engineering | Infra, automation, Notion architecture, non-code build/ops work | Cowork |
| Work | FM-work-adjacent admin only (never FM technical detail — isolation rule applies) | Desktop/manual |
| Business | Terra Inc entity ops, contracts, LLC/Rung actions | Desktop/manual |
| Finance | Investing, PTOS, brokerage, debt strategy actions | Desktop/manual |
| Personal | Everything else (travel, house-hack, non-Terra) | Desktop/manual |

Inference order: (1) if Linked Project is set, inherit that project's Domain from the
Step 4A mapping table; (2) otherwise infer from content; (3) if genuinely ambiguous,
default to Personal and let Will re-tag in Notion rather than blocking the sync.
FM-work tasks are never auto-captured here — the isolation rule in memory still
applies; if a FM-related action item comes up, mention it in the sync preview as a
flagged item Will should add manually, not as an auto-created row.

### If the "Source" select property doesn't exist on Tasks DB yet
Don't fail silently and don't invent a schema change unprompted. Create the task with
Source prefixed in the title instead (e.g. "[Email] ..."), and flag once at the end
of sync: "Tasks DB has no Source property — want me to add one, or keep using the
title-prefix workaround?"

### Write order
Always show the TASKS preview (Step 3) and get confirmation before creating rows —
same bar as Notion/Obsidian/HUB_STATE. Never auto-create tasks silently, even ones
that look obvious.

---

## Step 5 — Post-sync confirmation

```
✅ Session sync complete

Notion     → [project] content + properties (Status/Last Synced) updated (or: queued in Sync Queue, target unreachable)
Obsidian   → [note title] written to [vault path] (or: queued)
HUB_STATE  → [project] section overwritten (claude-skills/skills/ai-control/HUB_STATE.md)
Tasks DB   → [N] task(s) created ([sources]) / none this session (or: queued)

Remind: git add skills/ai-control/HUB_STATE.md && git commit && git push if not done.
```

---

## Step 6 — Skill/hub git commands (delegate, don't duplicate)

**Mandatory when a skill or hub file was updated or created this session.**

This is the SAME action as HUB.md's `sync hub` trigger (Skill Update Trigger section) — don't
maintain separate git-command logic here. Full procedure lives there; summary:

1. List every skill/hub file touched this session.
2. Preview the change set — confirm before writing.
3. Write files locally via Filesystem tools (if reachable) — this IS executed, a real edit.
4. Supply the exact commands for Will to run (the agent CANNOT run git commands or call the
   GitHub API — no exec access, credentials prohibited). Use the path from HUB.md's Machine
   Paths table, not a hardcoded one:
   ```bash
   cd <repo root — see Machine Paths table>
   git add -A
   git commit -m "chore: sync hub <YYYY-MM-DD> — <short summary>"
   git push
   ```
5. State plainly that local write is done but push is NOT, until Will confirms it succeeded.
   Never say "pushed"/"synced" without that confirmation.

If the claude-skills repo isn't reachable this session, fall back to staged downloadable files
in `/mnt/user-data/outputs/` with the same commands.

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
| Target unreachable (any) | Write queue entry to Notion Sync Queue instead of dropping content |
| Notion itself unreachable (queue can't be written) | Fall back to downloadable staged file; notify Will explicitly |
| Tasks DB dedup match found | Skip creating that candidate silently, no prompt |
| Tasks DB missing Source property | Use title-prefix workaround, flag once at sync end (Source now exists as of 2026-07 — this is a fallback for future schema drift only) |
| Tasks DB missing Engineering Domain option | Same workaround — prefix title (e.g. "[Engineering] ..."), flag once (Engineering added to Domain as of 2026-07 — fallback only) |
| Tasks DB query/write fails | Retry once; show candidates for manual paste if it fails again |
