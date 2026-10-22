---
name: notion-space-audit
description: |
  Structural integrity audit for any Notion space (Engineering Hub, NACA Hub, Finance
  Hub, Terra Operations, or any other hub/root page). Use whenever Will asks to "audit
  Notion," "clean up my Notion," "check for broken links / orphans / duplicates,"
  "is anything misfiled," "did the last cleanup actually work," or wants a health
  check on a hub's structure. Also trigger proactively if a session surfaces signs of
  drift — duplicate pages, dead links, pages that don't roll up to any hub — even if
  Will didn't explicitly ask for an audit. Also use for whole-workspace coverage
  requests — "go through my entire Notion," "index everything," "what did you miss,"
  "update the Page Registry" — which run the Full-Workspace Crawl mode (deterministic
  tree crawl + Page Registry + page markers), not a search sweep. Runs read-only first: never moves, archives,
  or deletes anything without an explicit approval step. Not for routine session-state
  syncing (see session-context-sync) — this is a structural audit, not a state snapshot.
  Also not for reading or summarizing note content ("what did I write about X," "pull
  up my notes on Y") — see note-reader for that; this skill only checks structure
  (links, orphans, duplicates, filing), never content meaning.
---

# Notion Space Audit

Structural health check for a Notion hub-and-spoke space. Three-phase contract:
inventory (read-only) → findings report → approval → one batched execution pass with
a full sync log. Never writes anything in Phase 1 or 2, no matter how obvious a fix
looks — that's the whole point of the gate.

Notion-generic: takes a target hub/root page as a parameter each run. Do not hardcode
a specific hub's page ID into this file — look it up in Claude memory (userMemories)
or ask Will which hub to audit if it's not already named in the request.

---

## Modes

| Mode | When | Phase 1 inventory method |
|---|---|---|
| **Hub audit** (default) | One named hub/space | 1a–1c below (link walk + DB query + reconciliation) |
| **Full-Workspace Crawl** | "Whole Notion," "everything," "index," "what did you miss," Registry refresh | Section 1F below replaces 1a/1b; 1c still runs |

Both modes share Phases 2–4 and every guardrail. If the request is ambiguous ("audit
Notion" with no hub named), ask which mode before starting.

**Why the crawl mode exists (added 2026-10-22):** past "go through the entire space"
runs missed pages because `notion-search` is relevance-ranked and result-capped — it
cannot enumerate a workspace. Coverage has to come from a deterministic tree crawl;
search is only a final cross-check.

---

## Phase 1 — Read-only inventory

No writes of any kind in this phase. Three sub-passes, all required — don't stop at
just following links, that's how orphans get missed (see Traps).

### 1a. Walk the structure
Starting from the target hub page, follow every visible link outward via
`notion-fetch`. Build a map of what's reachable and how many clicks from the hub.

### 1b. Query databases directly
Don't rely on link-following alone — orphaned pages hide inside databases that
nothing links to directly. Use `notion-query-data-sources` (or `notion-search`
scoped to the workspace) against every DB associated with this hub — Projects,
Strategy Docs, or whatever the hub's own DBs are — and cross-reference against the
map from 1a. Anything in a DB that isn't reachable from the hub map is a candidate
orphan.

Also run a broad `notion-search` pass (not scoped to any one DB) for the hub's own
name/topic — this catches pages that are neither linked from the hub nor sitting in
one of its known DBs.

### 1c. Reconciliation check
Before producing new findings, verify the *previous* run didn't silently fail.

1. Look for a prior sync log — either one this skill wrote on an earlier run, or any
   other trace of manual cleanup in the space (dated Safe-to-Delete why-notes, an
   Archive-adjacent log page, or ad hoc comments). For the comment case, check
   `notion-get-comments` on candidate Archive/Safe-to-Delete pages — that's where a
   "moved X because Y" note left as a page comment (rather than page content) would
   actually live, and following links alone won't surface it. Check both log-page and
   comment traces; don't assume only this skill's own log format counts.
2. If no such history exists anywhere in this hub, skip this check cleanly and move
   to Phase 2 — first run on a hub has nothing to reconcile against.
3. If history exists, walk Archive and any Safe-to-Delete area and diff claimed-moved
   items against what's actually there. In Full-Workspace Crawl mode, the Page
   Registry (see 1F) also counts as prior history: diff its rows against this crawl.
   Classify each claimed item as:
   - **Confirmed** — present where the log says it should be. No action.
   - **Missing** — logged as moved but isn't there. This is a failed/silent execution
     from a prior run, not a new orphan — report it separately in Phase 2, don't
     re-triage it as if it were newly discovered.
   - **Present but unlogged** — sitting in Archive/Safe-to-Delete with no matching log
     entry. Flag as drift (moved outside this skill's process, e.g. manually).

### 1F. Full-Workspace Crawl (crawl mode only — replaces 1a/1b)

Still read-only. Present the crawl plan (seeds, exclusions, estimated scope) and get
the go-ahead before starting, per the plan → approve → execute contract.

**Scope**
- In: projects, routines, strategies, hubs, plans, ADRs, governance pages, and every
  database holding them.
- Excluded: Deal Digests and other auto-generated pages (scanner outputs, digests,
  logs). Each excluded tree is recorded once in the Registry as `Excluded` and never
  re-flagged as missing or orphaned on later runs.

**Crawl method**
1. Seed list: every top-level page and teamspace root — Terra Inc hub, Finance Hub
   root, homepage, plus private and shared sidebar pages via
   `notion-list-private-pages` / `notion-list-shared-pages`.
2. Breadth-first: `notion-fetch` each page by UUID; enqueue every child page, child
   database, and linked page ID found in its content.
3. Databases: query each data source (`notion-query-data-sources`) and enqueue every
   row page. Page through results until `has_more` is false — a first page is not a
   full DB.
4. Deduplicate by page ID. Stop only when the queue is empty — never on a page or
   time budget without saying so in the report.
5. Final cross-check only: broad `notion-search` passes for orphans the crawl didn't
   reach. Anything search finds that the crawl missed is an orphan finding, not proof
   the crawl is complete.
6. Record per page: title, ID, parent, space, type, last-edited time (from fetch),
   and whether it carries a page marker (see below) and with what date.

**Page Registry (Notion database)** — source of truth for page count and coverage.
One row per page. Properties: Title · Page ID · Parent (relation or text) · Space
(Terra, Finance, Personal, Work, …) · Type (Hub, Project, Routine, Strategy,
Database, Reference, Excluded) · Last reviewed by Claude (date) · Last edited in
Notion (date) · Status (Reviewed / Needs review / Excluded). Claude memory stores
only the Registry's database ID, never page lists. If no Registry exists yet, search
for one first; only then propose creating it in the Phase 2 report (creation is a
write — it waits for the Phase 3 gate).

**Page marker** — one faint gray line at the very bottom of each reviewed page, e.g.
`Claude indexed · 2026-10-22`.
- Later runs review only pages that are missing from the Registry, unmarked, or
  edited after their marker date. Everything else is counted, not re-reviewed.
- Re-review updates the marker date in place — never stack a second marker.
- Pilot markers on one hub before rolling out workspace-wide.
- Markers and Registry rows are writes: they're applied in Phase 4, after approval,
  never during the crawl itself.

**Execution-layer intake** — while crawling, flag pages containing actionable items
(deadlines, purchases, to-dos) for intake into the canonical Routines DB (extend it;
no separate Execution DB) using the standard intake format: **Task, Deadline, Cost,
Source, Space**. Flagging only — intake rows are written in Phase 4 after approval.
Each space gets a filtered Routines view; the homepage gets the global view grouped
by Space, sorted by deadline.

**Transfer-queue sweep** — pages titled "Obsidian Queue," "Sync Queue," "Task Queue"
or marked `DRAINED` are transfer buffers, not knowledge. Report them separately:
confirmed-drained ones are proposed for a move to Archive (leaving an index of where
their content landed on the parent page); undrained ones are reported with their
target (vault path, HUB_STATE, repo file) so nothing is archived before it's
transferred.

---

## Phase 2 — Findings report

Group findings by type, not by page. Each finding gets a one-line reason. Reconciliation
results from 1c get their own section, separate from newly-discovered items — a missing
logged item is a different problem than a new duplicate and Will needs to triage them
differently.

```
📋 Notion Space Audit — [Hub name]

─── RECONCILIATION (prior run) ──────────────────
⚠️ Missing (logged moved, not found): [N] — [list or "None"]
⚠️ Unlogged drift (found, no log entry): [N] — [list or "None"]
[Skip this section entirely if 1c found no prior history]

─── BROKEN LINKS ────────────────────────────────
[page] → links to [target] which no longer resolves

─── ORPHANS ──────────────────────────────────────
[page] — found via [DB query / broad search], not reachable from hub within N clicks

─── DUPLICATES ────────────────────────────────────
[page A] / [page B] — [why they look like duplicates; which looks Canonical]

─── MISFILED ───────────────────────────────────────
[page] — currently under [location], structurally belongs under [location]

─── COVERAGE (crawl mode only) ─────────────────────
Pages found: [N] — by space: [...] — by type: [...]
New since last Registry run: [N] · Changed (edited after marker): [N] · Unreached by crawl, found by search: [N]
Excluded (logged once): [list of excluded trees]

─── ACTIONABLE ITEMS FOR ROUTINES DB (crawl mode only) ───
[Task] · [Deadline] · [Cost] · [Source page] · [Space]

─── TRANSFER QUEUES ───────────────────────────────
Drained (propose archive): [list] · Undrained (target): [list]

Proposed actions: [N] items — archive / tag Canonical-Superseded / move / merge / Registry rows / markers / Routines intake
```

Stop here. Do not act on anything yet.

---

## Phase 3 — Approval gate

Present the findings report and wait for explicit approval before any write. Will can
approve all, approve a subset, or send items back for more triage. No batched execution
starts until this gate clears — this includes items that look unambiguous (e.g. an
obviously dead link); "obvious" is not the same as "approved."

---

## Phase 4 — Batched execution

One pass, batched — not item-by-item back-and-forth. Two different tools cover the
"move" and "edit" cases below — don't conflate them, they fail in different ways.

**Relocating a page (archive, re-file, un-orphan)** — use `notion-move-pages`.
Moving a page moves its entire subtree with it, which is usually correct but not
always what you want. Before calling it on a parent page, `notion-fetch` the parent
and look at its children, then decide per child: move with the parent, or re-parent
elsewhere first. Decide before you move, not after — once moved, a child that
shouldn't have come along has to be moved twice.

**Editing a page's content** (retagging Canonical/Superseded, adding a why-note,
consolidating a duplicate) — use `notion-update-page`:
1. **Re-fetch immediately before calling it with `command: "update_content"`.**
   Never reuse content fetched during Phase 1 — `content_updates`' `old_str` must
   exactly match current page content, and a stale fetch either fails outright or,
   worse, matches text that changed underneath you.
2. Escape `$` as `\$` (single backslash) in any `old_str`/`new_str` passed.
3. **Never use `command: "replace_content"` on a page with child pages/databases
   without re-including them** as `<page url="...">` / `<database url="...">` tags
   inside `new_str`. This isn't a hub convention, it's an API guardrail: the call
   fails and lists what would be deleted unless `allow_deleting_content: true` is
   set. Never set that flag to force it through — if the call fails with a deletion
   list, show Will the list and get explicit confirmation before retrying with the
   flag, exactly as the tool's own guidance requires. Prefer `update_content`
   (targeted search-and-replace) over `replace_content` whenever the edit doesn't
   need to touch the whole page — it sidesteps this risk entirely.
4. Before creating anything (e.g. a replacement for a "duplicate"), search once more
   via `notion-search` — a duplicate found in Phase 1 may already have been handled,
   or what looked like a gap may not be one.
5. Apply Safe-to-Delete convention via `update_properties` or a content note:
   anything archived/deleted gets a dated why-note, not a bare move.

**Archiving vs. deleting** — the default "archive" is a `notion-move-pages` into the
workspace's Archive page (Global → Archive), which is reversible and keeps the page
searchable. `notion-delete-pages` exists (moves to Notion Trash, restorable for a
limited time) but is used only when Will names the exact pages to delete — never as
cleanup on Claude's own initiative. If the delete tool is unavailable in a session,
deprecate with a title prefix and log in Safe to Delete instead of leaving the page
in place indefinitely.

**Crawl-mode writes** (after approval, same batch): upsert Registry rows, write or
update page markers (in place, one per page), and create approved Routines DB intake
rows. Re-fetch each page immediately before adding/updating its marker.

### Sync log
Write one log entry covering the whole batch — not one per item:

```markdown
---
### YYYY-MM-DD — Notion Space Audit: [Hub name]
- Archived: [page] → [Safe-to-Delete location] — why: [reason]
- Tagged Superseded: [page] (canonical: [page])
- Moved: [page] from [old location] to [new location]
- Merged: [page A] + [page B] → [surviving page]
- Reconciliation carried forward: [N] items still missing from prior run, re-flagged
- Registry: [N] rows added, [N] updated · Markers: [N] written/updated · Routines intake: [N] rows
```

After the batch: run a memory correction pass (Registry DB ID only — no page lists)
and a session sync with links to every page created or updated.

Link every item in the log to the actual page. This log is what the *next* audit's
Phase 1c reconciliation check will read — keep it in the format above so it stays
machine-diffable, not just human-readable.

---

## Traps to avoid

These came from real near-misses — don't relearn them:

- **`notion-move-pages` moves the whole subtree, not just the page.** Always check
  for sub-pages before relocating a parent. Triage children first — decide which
  move with it and which get re-parented elsewhere before the call, not after.
- **`replace_content` can silently take children down with it.** This is a separate
  mechanism from moving pages — it's about content editing, not relocation. Any
  child page/database embedded in a page you `replace_content` on must be
  re-included as a `<page url>` / `<database url>` tag or the operation either fails
  (good) or, if `allow_deleting_content: true` is set, deletes them (bad). Never set
  that flag without showing Will the affected list first.
- **Search before creating.** A "gap" is often not a gap — search before assuming
  something needs to be created.
- **Orphans hide in two places you won't find by clicking around:** the Archive, and
  inside databases nothing links to directly. Query the DBs; don't just follow links.
- **Search can't enumerate a workspace.** `notion-search` is relevance-ranked and
  capped; a "full sweep" built on search silently misses pages. Crawl the tree;
  use search only to catch orphans.
- **Drained queues linger when nobody archives them.** Terra API's Obsidian queues
  sat marked "drained — delete me" for months because earlier sessions assumed no
  delete/archive path existed. Move confirmed-drained queues to Archive in the same
  batch that confirms them.
- **Stale fetches break `update_content`.** Re-fetch immediately before every edit —
  exact-string matching (`old_str` must match exactly) means content fetched even one
  step earlier can mismatch.

---

## Structural conventions enforced

| Convention | What it means here |
|---|---|
| Hub-and-spoke | Everything should trace back to the hub; flag anything that doesn't |
| 2-clicks-from-hub | Findings should note click-depth for misfiled/orphaned pages |
| Canonical / Superseded tagging | Duplicates get one tagged Canonical, the other Superseded — not deleted outright unless approved |
| Static tables → live DB views | Flag static markdown tables that duplicate what a live DB view could show |
| Safe-to-Delete with dated why-note | Never a bare archive/delete — always a reason and a date |
| Batch pushes | Execution is one pass per approved batch, not incremental item-by-item writes |
| Sync log with links | Every batch produces one linked, diffable log entry (see Phase 4) |
| Page Registry | One row per page; the Registry, not search, defines coverage (crawl mode) |
| Page marker | One faint `Claude indexed · date` line per reviewed page, updated in place |
| Execution intake | Actionable items flagged into the Routines DB as Task / Deadline / Cost / Source / Space |

---

## Error handling

| Error | Action |
|---|---|
| No prior sync log or manual-cleanup trace found | Skip Phase 1c cleanly, proceed to Phase 2 |
| `update_content` fails on exact-string match | Re-fetch the page fresh and retry once; if it fails again, surface to Will rather than guessing at the string |
| Parent page has unarchived children at execution time | Stop, do not relocate the parent via `notion-move-pages`, report which children need triage first |
| `replace_content` fails with a would-delete-children list | Stop. Do not set `allow_deleting_content: true` to force it. Show Will the exact list and get confirmation before retrying — or switch to `update_content` if the edit doesn't need the whole page replaced |
| Ambiguous duplicate (no clear Canonical candidate) | Include in findings report but don't propose an action — ask Will to pick |
| Target hub not specified | Ask which hub/space before starting Phase 1 — never guess |
| DB query returns nothing for a hub that should have DBs | Note it in findings rather than silently treating the hub as DB-less |
| No Page Registry found (crawl mode) | Search for it once more; if absent, propose creating it in Phase 2 — don't create during the crawl |
| Crawl can't finish in one session | Stop at a clean queue boundary, report pages done vs. still queued, and record the remaining seeds so the next run resumes — never report partial coverage as complete |
| Page fetch fails mid-crawl | Record it as Unreached with the error, keep crawling, list it in the Coverage section |
