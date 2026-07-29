# Claude Skills Glossary — "If Claude Is Down" Reference

Last verified against disk: **2026-07-28**, by directly reading every `SKILL.md`
in this repo — not from memory, not from the old Skills Snapshot page (which
was 7 weeks stale and missing 8 of these 13).

**How to keep this honest going forward:** don't hand-edit the table below
from memory. Re-derive it by reading `skills/*/SKILL.md` frontmatter each
time — the whole point of this file is that it can't drift the way the
Notion page did.

---

## Quick Lookup Table

| Skill | What it does | Trigger phrase | If Claude is unavailable |
|---|---|---|---|
| **ai-control** (hub, not auto-skill) | Engineering session governance — fetch order, Working Memory contract, execution boundaries, HUB_STATE.md tracking for 7 coding projects | `load hub` / auto-loads via repo CLAUDE.md pointer | Read `skills/ai-control/HUB_STATE.md` directly — it's the git-authoritative project status snapshot, human-readable as-is |
| **tracker-sync** | Surgical diff-sync of `command-center.html`'s project data from the Notion Projects DB (by page ID, not name) | `sync tracker` / `refresh tracker` / weekly Sunday | Open the Notion Projects DB directly — it's the real data, the dashboard is just a view on it |
| **session-context-sync** | Unified end-of-session sync: Notion (content + Status/Last Synced properties), Obsidian note candidates, HUB_STATE.md | `sync` / `wrap up` / proactively at session end | Manually update the project's Notion page and, if it's a hub-tracked project, `HUB_STATE.md`'s section for it |
| **session-rules** | Thin mirror of the Working Memory contract for web/mobile sessions that can't load the full hub | Automatic on substantive conversations | The Working Memory format is just 4 bullets (Core Objective/Key Facts/Progress/Next Step or Session Sync) — reconstructable from any recent chat by hand |
| **personal-os-dashboard** | Design system + build methodology for single-file HTML dashboards (colorways, component patterns, surgical-edit philosophy) | Building/updating any personal OS dashboard | Copy the CSS `:root` block from an existing dashboard (e.g. `ptos-os.html`) — the design tokens are self-contained in any file already built with it |
| **note-reader** | Read/search/summarize content from Notion or Obsidian on request | "check my notes", "pull up my Obsidian page", etc. | Just open Notion or the vault directly — this skill has no state of its own, it's a read-only convenience |
| **consolidate-memory** | Reflective pass over Claude's own memory files — merge duplicates, fix stale facts, prune the index | Explicit request to clean up memory | No manual equivalent — this is Claude-memory-specific; if Claude is down, memory isn't reachable anyway |
| **schedule** | Create or update a Cowork scheduled/recurring task | "every day", "each morning", "run this at noon" | Check Cowork's scheduled tasks list in the UI directly |
| **setup-cowork** | Guided first-time Cowork onboarding (role, plugins, connectors, try-a-skill) | New Cowork setup | One-time onboarding flow — no ongoing dependency once complete |
| **skill-creator** | Create, test, and iteratively improve skills (eval loops, benchmark viewer, description optimization) | Building/editing/testing a skill | No manual equivalent — but skills built with it are plain markdown, readable/editable by hand regardless |
| **docx / pdf / pptx / xlsx** | Anthropic's public document-creation skills — not custom-authored, part of the base skill set | Any Word/PDF/PowerPoint/Excel task | Use the native application directly (Word, Adobe, PowerPoint, Excel) |

**Not an active skill:** `skills/archive/` holds retired versions (`dev-log`
old copy, `session-rules-duplicate-OLD`) — historical reference only, never
triggers.

---

## Why this table exists

The old Skills Snapshot Notion page was a progress log (dated entries),
which is the wrong shape for "I need to know what exists and what to do
if Claude's unreachable." This file is a lookup table on purpose — skim it,
find the skill, read the fallback. History belongs in `DEV_LOG.md`, not here.

## Memory (the other single point of failure)

Skills are half the resilience story. The other half is Claude's memory —
durable facts, preferences, and project context that don't live in any
file. There's no local mirror of that today. `consolidate-memory` keeps
memory itself tidy, but doesn't export it anywhere readable without Claude.
If this becomes a real gap (not just a theoretical one), the fix is a
periodic "sync memory to Notion" pass — worth raising if it's ever actually
needed rather than building it preemptively.
