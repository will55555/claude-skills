---
name: session-context-sync
description: |
  Unified session-end sync skill. Triggers at end of any substantial session — coding, planning, design, or learning. Handles six write targets in one pass: each repo's own DEV_LOG.md (thorough, recipe-quality narrative — the ONLY target detailed enough to reproduce a session's work from), Notion (project state), Obsidian (note candidates), the Engineering Hub's HUB_STATE.md (live project snapshot), Tasks DB (new actionable items), and task reconciliation (fixes EXISTING repo TASKS.md/Notion/HUB_STATE rows this session's work shows are stale — runs every sync, not just on request; a full ecosystem-wide pass is a separate "reconcile all tasks" trigger). Trigger on: "sync", "wrap up", "end of session", "push to Notion", "update Notion", "update Obsidian", "sync state", or proactively when meaningful work was done on any active project. Always prompt at session end — never skip when the session produced decisions, code, or learning artifacts.
---

# Session Sync Skill

Unified end-of-session sync across five targets: each repo's own DEV_LOG.md, Notion, Obsidian,
the Engineering Hub's HUB_STATE.md, and Tasks DB. Runs in a single pass at session end. Each
target is independent — one can be skipped without affecting the others.

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
| **DEV_LOG.md (per-repo)** | Full phase-log narrative entry — WHY, not just WHAT; recipe-quality, reproducible on a fresh machine from the log alone (see Step 4E, Documentation Protocol in HUB_GUIDE.md) | Session shipped code, fixed a real bug, or made a decision worth reproducing later, in ANY hub-tracked repo touched this session | Local write via Filesystem tools |
| **Notion** | Project state snapshot + progress log (page CONTENT) + Status/Last Synced (page PROPERTIES — see Step 4A-props); ALSO an informational mirror/dupe of hub state (never authoritative) | Session produced Notion-worthy content, or hub state changed | Desktop or Code |
| **Obsidian** | Note candidate(s) distilled from session | Session produced a concept, pattern, or decision worth keeping | Desktop or Code |
| **HUB_STATE.md** | Active project section snapshot (overwrite in place) | Session touched a hub-tracked project (any Terra project, DSA, claude-skills, etc.) | Desktop or Code |
| **Tasks DB** | New task rows (actionable items for routing to appropriate tool/hub) | Session surfaced an actionable item not already in Tasks DB — from chat commitments, buried TODOs in a Notion page touched this session, or action items from Gmail/Calendar tool results this session | Desktop or Code |
| **Task reconciliation** (Step 4D-2) | Fixes to EXISTING task status — repo TASKS.md rows, Notion rows, HUB_STATE claims — that this session's work shows are stale; `ALL_TASKS.md` refresh when scope warrants it | Runs every sync, scoped to repo(s)/project(s) touched this session — always checked, not just when something looks obviously wrong | Local file edit + Notion, via Filesystem/MCP tools |

Both Claude Desktop and Claude Code sessions sync to all targets that apply.
The session type determines what content is available, not which targets apply.

**Why DEV_LOG is a real target now, not a footnote (2026-08-04):** earlier versions of this
skill only mentioned DEV_LOG.md inside HUB_STATE's own procedure ("hand off to the
Documentation Protocol"), with no actual step, preview, or confirmation gate — so a full sync
could run to completion, report "✅ Session sync complete," and never touch DEV_LOG.md at all.
That happened for real: a 2026-08-04 session shipped a large TFE-401 rework across 9 files, ran
this skill, synced Notion + HUB_STATE + this file cleanly, and DEV_LOG.md sat untouched since
2026-08-02 until Will asked "the sync didn't update the logs?" after the fact. HUB_STATE is a
snapshot by design (≤15-20 lines, no narrative) — it was never supposed to carry this detail,
and Notion's log entry is a compressed summary, not a recipe. DEV_LOG is the only target with
the room and the mandate (per HUB_GUIDE's Documentation Protocol) to be thorough enough that
Will could rebuild the session's work from the log alone. Treat it with the same weight as the
other four — always in the classification step, always in the preview, always confirmed before
writing.

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
→ DEV_LOG: [yes — which repo(s), which phase name] / [no — reason, e.g. "no code shipped"]
→ Notion: [yes — reason] / [no — reason]
→ Obsidian: [yes — candidate list] / [no]
→ HUB_STATE: [yes — which project section] / [no]
→ Tasks DB: [yes — N candidates found] / [no]
→ Task reconciliation: [yes — N contradictions found across repo TASKS.md/Notion/HUB_STATE] /
  [checked, none found] — always run this check for repo(s) touched this session, never skip
```

DEV_LOG applies whenever ANY hub-tracked repo had code shipped, a real bug found+fixed, or a
design decision made this session — this is a LOWER bar than Notion-worthiness, not the same
gate. A session can be too thin for Notion (no project-state change) but still deserve a
DEV_LOG entry (e.g. a bug fixed mid-investigation, a config value tuned with real reasoning
behind it) — don't skip DEV_LOG just because Notion was skipped. When in doubt: if reproducing
this session's changes on a fresh machine would require re-deriving something (a root cause, a
rejected alternative, a non-obvious config value), it belongs in DEV_LOG.

---

## Step 3 — Show sync preview and confirm

```
📤 Session Sync Preview

─── DEV_LOG.md ──────────────────────────
Repo: [name — e.g. terra-api-fe]
Phase heading: [## Phase N — Name, or descriptive title if not a numbered phase]
Contains: [1-line list of what sections it'll have — Goal / bugs found+fixed / decisions /
           recipe steps / known limitations]
[Repeat this block per repo if more than one was touched this session]

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

─── TASK RECONCILIATION ──────────────────
[repo]/TASKS.md → [TASK-ID]: says "[stale status]", session confirms "[real status]"
  → fix: repo TASKS.md + [Notion row / HUB_STATE section, if also stale]
[repeat per contradiction; write "Checked [repo(s)], none found." if the check ran clean —
 never omit this block silently, unlike the others above, since its absence should mean
 "checked and clean," not "forgot to check"]

─── SYNC QUEUE (if any target unreachable) ──
[target] unreachable → queued in Notion Sync Queue, will retry next sync

Sync all? (yes / edit first / skip [devlog|notion|obsidian|hubstate|tasks|reconcile])
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

**Default detail bar (standing rule, set 2026-08-08 — do not wait to be asked):** every Obsidian
note is written at full depth by default — every section below filled in substantively, not
stubbed. This is the baseline, not an escalation Will has to request. Established after a
session where he had to explicitly ask for "detailed" notes multiple times before it became the
default; it should never need asking again.

**Self-sufficiency bar (standing rule, set 2026-08-09 — do not wait to be asked): every note
for a coding/debugging/infra session must be written so a technically competent person with
ZERO session context — no access to this conversation, no access to Claude at all — could
reproduce the fix and debug the same class of problem independently from the note alone.**
Will's own framing: "if my agent is down, I could always go to my notes and do this myself."
This is a higher bar than "detailed" — detailed can still assume the reader remembers what
"the endpoint" or "the box" refers to. Self-sufficient means:
- **Every command actually run, verbatim, not paraphrased** — real file paths, real flags, real
  AWS CLI / SSM / SQL / curl invocations exactly as executed, not "then I checked the logs."
  If a command was run via a specific tool/console path (e.g. AWS Console → EC2 → Connect →
  Session Manager, not just "connected to the box"), name that exact path — a reader without
  that context can't guess which of 4 connection methods was the one that worked.
- **Every wrong turn kept, not just the final fix** — per the existing "How this was actually
  found / debugged" section below, a false lead that seemed to work but didn't is exactly as
  valuable as the real fix, because it's what the reader will also try first.
- **All prerequisite context stated inline, not assumed** — credentials/identities involved
  (by role, e.g. "an IAM user with AdministratorAccess," not assuming the reader already knows
  which user that is), account/instance IDs, exact error text and status codes, exact file
  paths and line numbers where a bug lived. A reader who has never seen this codebase should be
  able to locate the same file and see the same bug.
- **The underlying mechanism explained, not just the symptom→fix pair** — e.g. not just "add a
  newline before appending," but WHY the append corrupted the value (no trailing newline on the
  prior line + shell `>>` doesn't add one), so the reader can recognize and avoid the same
  failure mode in a completely different file/context later.
- This bar applies whenever the session involved real debugging, infra work, or a
  multi-step build (i.e., whenever the "How this was actually found / debugged" section below
  would apply) — pure concept/reference notes with no investigation story don't need this
  level of forensic command-by-command detail, just the existing full-depth bar above.

```markdown
> **What this note is:** [One sentence — what this note covers and why it was written]

#tag #tag #tag

### What is it?
[One concise paragraph]

### Why it matters
[Consequence, impact, relevance to your work]

### How it works
[Mechanism, flow, or structure — full steps/commands, not a summary]

### How this was actually found / debugged
**Include this section whenever the note originated from real debugging — a bug hunt, an
incident, an investigation with more than one step or a wrong turn. Omit entirely (don't stub
it) for pure reference notes with no investigation story — e.g. "how OAuth refresh tokens
work," written from general knowledge rather than a live session's troubleshooting.**
When included, write it as a chronological narrative, not a summary of the end state:
- The starting symptom, in the words it actually appeared (error messages, log lines)
- Each hypothesis tried, in order — including the ones that were WRONG or only partially
  right. A fix that turned out to be real-but-not-sufficient (a genuine bug that didn't fully
  explain the symptom) is exactly as valuable to record as the final root cause — it's what
  future-Will will also try first, and should know not to stop there.
- What ruled each hypothesis in or out (the actual command/log output, not just "it wasn't that")
- The final root cause, and specifically what distinguished it from the false leads

### The design principles behind it

| Principle | What it means |
|---|---|
| [name] | [1-line explanation] |

### Common misconceptions
- ["X seems true but isn't, because Y"] — include this section whenever the topic has a
  plausible-but-wrong mental model worth naming explicitly, not just for debugging-sourced notes.

### Troubleshooting table (symptom → cause → fix)
[Include when the note documents a setup/config process with identifiable failure modes —
a table of exact error text → root cause → fix, scannable for a future fast lookup.]

### Key insight
[One sentence that would make future-Will immediately recall why this mattered]

## Related Notes
- [[Note Title]] — [one-line description of relationship]
```

Sections without a bracketed placeholder above (What is it / Why it matters / How it works /
Design principles / Key insight / Related Notes) are always included. "How this was actually
found," "Common misconceptions," and "Troubleshooting table" are included whenever they apply
per their own inline guidance — the default is to include them when in doubt, not to skip them
for brevity.

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
5. If this session produced a dev-log-worthy phase or decision, this is NOT optional —
   proceed to Step 4E and actually write the DEV_LOG.md entry before considering the
   sync complete. HUB_STATE only ever gets the resulting Next Step / Status, never the
   narrative — the narrative's real destination is DEV_LOG.md, not a "maybe later."

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

## Step 4D-2 — Existing task reconciliation (runs every sync, not just on request)

**Why this exists (added 2026-08-31):** Step 4D above only ever creates NEW task rows from
session chatter — it has no mechanism for catching an EXISTING task row that's gone stale
against a repo's own `TASKS.md`. That gap was real: on 2026-08-30, a manual pass found
`terra-api/TASKS.md` and `terra-hq-site/TASKS.md` both had status labels contradicted by their
own repos' git history (one said "Planned" for work closed 3 weeks earlier; thirteen rows said
"Done — pending commit" for a batch that had been merged and pushed for a week) — and nothing
about a normal `sync` would ever have caught or fixed that, because reconciliation wasn't a step.
This step is the fix: a lightweight check, scoped to whatever this session actually touched,
run automatically as part of every sync — not a separate thing Will has to remember to ask for.

**Scope — deliberately narrow, not the full ecosystem:** only the repo(s)/project(s) this
session actually worked in. A full cross-repo sweep (every hub-tracked repo, live Notion Tasks
DB pull, `ALL_TASKS.md` regeneration) is a bigger, slower operation — that's a separate explicit
trigger ("reconcile all tasks" / "audit tasks ecosystem-wide"), not something every routine sync
pays the cost of. Most sessions touch one or two repos; check only those.

### Procedure
1. For each repo touched this session that has a `TASKS.md`: re-read the specific task ID
   row(s) this session's work relates to (not the whole file — just what's relevant to what
   was done). Compare that row's Status against what actually happened this session.
2. Cross-check the same task ID (or its Notion-row equivalent, if one exists — not every repo
   task ID has a matching Notion row) against:
   - The Notion Tasks DB, if a row references this task (search by title/ID substring).
   - `HUB_STATE.md`'s section for this project, if it makes a claim about the same task.
3. If any of the three (repo TASKS.md / Notion / HUB_STATE) disagrees with what this session
   confirmed actually happened, that's a reconciliation candidate — surface it in the Step 3
   preview under a new `─── TASK RECONCILIATION ───` block (format below), don't fix it
   silently. This is a "did the docs catch up to reality" check, not a full audit — don't go
   hunting for staleness in rows unrelated to this session's work.
4. On confirmation, fix the stale side(s) directly:
   - Repo `TASKS.md` — local file edit via Filesystem tools, same as any other repo write this
     skill makes. Note it in Step 5's post-sync confirmation as uncommitted, same treatment as
     DEV_LOG.md.
   - Notion row — `notion-update-page` on the Status/relevant property, same call shape as
     Step 4A-props.
   - HUB_STATE.md — same overwrite-in-place rule as Step 4C; don't accumulate history here.
5. If the session's active project is `terra-initiative-home` specifically (or this session
   touched 3+ hub-tracked repos), also refresh `ALL_TASKS.md` at that repo's root: re-pull the
   live Notion Tasks DB, re-read each repo's `TASKS.md` directly (not from a prior snapshot),
   and rewrite the file per its own "What changed" convention (see the file's own header
   comment for the expected shape). This is the heavier ecosystem-wide op referenced in Scope
   above — only pay for it when the session's own footprint already justifies it, or Will asks
   for the full pass explicitly.

### Task reconciliation preview block (added to Step 3)
```
─── TASK RECONCILIATION ─────────────────
[repo]/TASKS.md → [TASK-ID]: says "[stale status]", session confirms "[real status]"
  → fix: repo TASKS.md + [Notion row / HUB_STATE section, if also stale]
[repeat per contradiction found; omit this block entirely if none found]
```

### What this step is NOT
Not a full-ecosystem audit on every sync (that's the separate "reconcile all tasks" trigger,
scoped like the 2026-08-30 `ALL_TASKS.md` regeneration). Not a substitute for Step 4D's
new-task-candidate scan — both run every sync, they catch different things (4D: new items never
recorded anywhere; 4D-2: existing items whose recorded status is now wrong).

### Separate trigger — full ecosystem-wide reconciliation ("reconcile all tasks" / "audit tasks")
Not part of a routine `sync` — this is the heavier operation Step 4D-2 above deliberately stays
narrow to avoid paying for on every sync. Trigger explicitly on phrases like "reconcile all
tasks," "audit tasks ecosystem-wide," or "make sure everything's aligned with Notion" (not just
"sync"). Procedure, matching the 2026-08-30 session that established this pattern:
1. Confirm which hub-tracked repos are actually present/cloned on this machine (don't assume
   from a prior session's snapshot — `git status`/directory-list each one directly; the
   2026-08-30 pass itself got this wrong once, assuming `oms` and `terra-hq-site` weren't
   cloned locally when they were, nested under `terra-initiative-home/`).
2. For each present repo: `git fetch`, check for local/origin divergence, fast-forward if clean
   and behind (flag, don't force, if diverged with local changes).
3. Read each repo's `TASKS.md` directly, in full — not from HUB_STATE or a prior `ALL_TASKS.md`
   snapshot, both of which can themselves be stale.
4. Re-pull the live Notion Tasks DB (Terra-domain or project-relevant rows).
5. Cross-reference all three (repo TASKS.md × Notion × HUB_STATE) per task ID; for every
   contradiction, fix the stale side(s) — repo file edit + commit + push, Notion property
   update, or HUB_STATE overwrite, per Step 4D-2's fix procedure above.
6. Regenerate `ALL_TASKS.md` (or the equivalent cross-reference doc for a non-Terra project, if
   one exists) with a "What changed since last pass" section at the top, not a silent overwrite.
7. Preview every fix before writing (same confirmation bar as everything else in this skill) —
   this is a bigger diff than routine reconciliation, so batch the preview by repo, not as one
   undifferentiated wall of changes.

---

## Step 4E — DEV_LOG.md sync (per repo)

The full narrative — the ONE target with the mandate and the room to be thorough enough that
Will could reproduce this session's work from the log alone, per HUB_GUIDE.md's Documentation
Protocol quality bar: "WHY not just WHAT · non-obvious flags commented · alternatives named +
rejected · root cause not just fix · reproducible on a fresh machine from the log alone."
Everything else in this sync (Notion's 2-3 bullet log entry, HUB_STATE's ≤3-line Context field)
is a compressed pointer TO this — never a substitute for it.

### Procedure

1. Identify every hub-tracked repo touched this session (code changed, a bug fixed, a decision
   made — see Step 2's DEV_LOG classification bar, which is lower than Notion-worthiness).
2. For each repo, read its existing `DEV_LOG.md` to confirm the current phase-numbering/heading
   convention that repo actually uses (some use `## Phase N — Name`, some use a plain descriptive
   title) — match it, don't impose a different one.
3. Write a full entry using the Phase Log schema from HUB_GUIDE.md's Documentation Protocol:
   `## Phase N — [Name]`, `**Date:**`/`**Status:**`, then `### Goal` / `### Key Design Decision`
   (or per-bug `### Files Created / Modified` sections for a bugfix-heavy session) /
   `### Setup / Recipe` / `### Build / Test Result` / `### Known Limitations / Next`. For each
   real bug found and fixed this session, include: **Root cause** (not just the fix), **Why not
   [alternative]** for any rejected approach, and enough concrete detail (file, line-level
   mechanism, exact values changed) that the fix could be independently re-derived without
   re-reading the whole session transcript.
4. PREPEND the new phase block at the point in the file where the existing convention puts new
   entries (check whether the repo's convention is newest-first or newest-last — do not assume;
   `terra-api-fe/DEV_LOG.md` as of 2026-08-04 appends newest-last, chronological).
5. Show the DEV_LOG preview (Step 3) and get confirmation before writing — same bar as every
   other target. This is a local file write via Filesystem tools, executed directly (not a
   supplied command) — DEV_LOG.md is ordinary repo content, not a credential-bearing or
   destructive file, so it doesn't need the git-command-supply treatment HUB.md/HUB_STATE.md get.
6. DEV_LOG.md is NOT auto-committed — mention its modified-but-uncommitted state in the Step 5
   post-sync confirmation, same as any other locally-written file this session touched.

---

## Step 5 — Post-sync confirmation

```
✅ Session sync complete

DEV_LOG.md → [repo]: [Phase heading] written, uncommitted (or: skipped — reason)
Notion     → [project] content + properties (Status/Last Synced) updated (or: queued in Sync Queue, target unreachable)
Obsidian   → [note title] written to [vault path] (or: queued)
HUB_STATE  → [project] section overwritten (claude-skills/skills/ai-control/HUB_STATE.md)
Tasks DB   → [N] task(s) created ([sources]) / none this session (or: queued)
Reconcile  → [N] stale task status(es) fixed ([repo TASKS.md / Notion / HUB_STATE]) / checked, none found

Remind: git add skills/ai-control/HUB_STATE.md && git commit && git push if not done.
Remind: DEV_LOG.md change(s) in [repo(s)] also uncommitted — same repo, Will's call when to commit.
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
| Repo TASKS.md not reachable (repo not cloned/present on this machine) | Skip reconciliation for that repo silently — don't guess its status from HUB_STATE or an old ALL_TASKS.md snapshot; note it as "not checked this pass," same as Step 4D-2's own procedure |
