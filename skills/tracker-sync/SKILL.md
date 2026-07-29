---
name: tracker-sync
description: Refresh command-center.html's project data from the Notion canonical Projects DB using a surgical diff-and-replace, never a full regeneration. Trigger on "sync tracker", "refresh tracker", "update command center", or on the weekly Sunday finance-review cadence. Never touches CSS, JS render functions, or nav — only the PROJECTS data array and GENERATED_AT.
---

# Tracker Sync Skill (v2)

Keeps `C:\Users\solan\OneDrive\Desktop\SDE\command-center.html` current against
the Notion canonical Projects DB (`collection://cf8f7353-f469-44bf-bbf2-56e1dfa280f3`)
without ever rewriting the file from scratch.

---

## Step 0 — Preflight (v2)

Before querying Notion, confirm the Filesystem connection can actually read
`command-center.html`. If it can't:

- Stop immediately. Do not query Notion, do not attempt any edit.
- Report plainly: "Tracker sync aborted — can't reach command-center.html on
  disk. Check the Filesystem connector in Cowork." No partial work, no
  guessing that it probably still applied.
- If the connector is flaky (times out, comes back after a retry), it's fine
  to retry the read once. Don't loop indefinitely — surface it to Will after
  one retry fails.

## Step 1 — Pull current DB state

```sql
SELECT Name, Domain, Status, Priority,
       "date:Start Date:start" as StartDate,
       "date:Last Synced:start" as LastSynced,
       Terra, url
FROM "collection://cf8f7353-f469-44bf-bbf2-56e1dfa280f3"
ORDER BY Domain, Status
```

## Step 2 — Read the existing file's PROJECTS array

Parse the `const PROJECTS = [...]` block only. Do not touch anything else.

## Step 3 — Diff by page ID, not name (v2)

Every Notion `url` embeds the page ID (the 32-char hex after the last `/`,
strip any `p/` prefix). Extract it as the match key for both sides of the
diff — DB rows keyed by their `url`'s ID, array rows keyed by their existing
`id` field. **Never match on `name`.** Names churn — one pull alone saw 11
renames (icon additions, expanded titles) that would have read as 11
deletes + 11 adds under a name-based diff, silently destroying row history.

Rows created before v2 won't have an `id` field yet. Backfill it
opportunistically: the first time a legacy row is touched for any reason
(a real field change), add its `id` alongside the edit. Don't do a
one-shot mass backfill — that's a full-file rewrite in disguise.

| Case | Action |
|---|---|
| DB row's ID not in array | Append a new object literal (with `id`) at the correct domain position |
| ID exists in both, fields differ | Edit just that object literal, refreshing `id` if it was missing |
| ID in array, no longer in DB | Don't delete. Move it to the Archive convention (see Step 3b). Never silently drop a row |
| `pfdc-loandatacorrection` / any FM-work row | Never sync detail fields. Keep the isolated placeholder as-is — name, domain, status "Active" only |
| Row has `source:"obsidian"` or `source:"manual"` | Never overwrite from the Notion query. See "Sourced rows" below |
| No changes | Skip entirely, don't touch the file |

## Step 3b — Archive convention

The dashboard has a dedicated **Archive** tab that aggregates any project
with `status:"Done"` across all domains, showing its original domain as a
column. When a project disappears from the DB or is marked Done, that's
where it lives — not as a stray "Done" row sitting inside its old domain
table. Domain tables already exclude `status:"Done"` rows automatically. No
new `Domain` value is invented; `Archive` is a view, not a schema field.

## Step 3c — HUB_STATE overlay (git-authoritative, added after this session's audit)

Six projects are also tracked in `claude-skills/skills/ai-control/HUB_STATE.md`,
which the Engineering Hub declares the SOLE AUTHORITY for these projects —
Notion is explicitly just a mirror there, never authoritative on conflict.
tracker-sync must respect that hierarchy, not quietly treat Notion as equally
true for these six:

| HUB_STATE section | command-center.html project |
|---|---|
| Terra API | Terra API |
| terra-api-fe | terra-api-fe |
| ROMS | ROMS |
| PIOS | PIOS |
| terra-hq-site | Terra HQ Site |
| claude-skills | claude-skills |
| Yahoo Mail MCP Server | Yahoo Mail MCP Server |

For these rows only, after the normal Notion diff pass:

1. Read HUB_STATE.md's section for each mapped project.
2. Populate/refresh a `hubDetail` field on that project's object — a single
   plain-language line built from Status + Next Step (e.g. "Prod EC2 down
   ~26h, diagnosing before redeploy" rather than copying the raw HUB_STATE
   bullet). Keep it under ~90 characters; it renders as subtext under the
   project name.
3. If HUB_STATE's Status materially conflicts with the Notion Status property
   (e.g. HUB_STATE says Blocked, Notion still says Active), do NOT silently
   overwrite Notion's Status property — that would invert the authority
   rule by letting a tracker-sync write flow git-derived truth into a
   Notion property that Step 4A-props of session-context-sync also writes
   to, creating two writers of the same field. Instead, surface the
   conflict in the sync summary: "HUB_STATE/Notion disagree on ROMS status
   — HUB_STATE says X, Notion says Y." Let the next real session-context-sync
   pass resolve it properly (it writes both targets in one pass, this skill
   should not).
4. HUB_STATE.md has no page property for "Last Synced" — use its own
   freshness stamp (top of file) to judge whether the six-project overlay
   itself is stale, and note that separately if the stamp is old.

## Step 4 — Update generation timestamp

Edit `GENERATED_AT` to today's date. The only non-data edit this skill
makes.

## Step 5 — Sourced rows: push toward zero

Rows tagged `source:"obsidian"` or `source:"manual"` are technical debt —
two sources of truth is the exact drift problem this tracker exists to
prevent. This skill's Notion-diff pass must never overwrite them. At the
end of every run, list any remaining sourced rows in the summary as a
nudge:

```
Still outside Notion: Terra Chain — Nkap/Njangi Coin Concept (obsidian).
Consider creating a real Projects DB entry when it's ready.
```

A separate, manually-triggered vault re-scan ("rescan obsidian for
tracker") is the only thing that should add or update `source:"obsidian"`
rows.

## Step 6 — Report, don't narrate

```
Tracker synced: +2 new (Terra Trademark Filing, Layer 2 Routing Fix),
3 field changes, 1 newly archived (Meal App), 1 newly stale (NACA, 52d).
Still outside Notion: Terra Chain concept (obsidian).
```

If nothing changed: "Tracker checked — no changes since last sync."

## Isolation rule (always enforced)

FM-work rows never get dates, priority, or a Notion URL synced into this
file, regardless of what changes in the source DB. Status label only.

## Versioning (recommendation, not yet automated)

`command-center.html` is edited unsupervised on a schedule with no
rollback path today. Recommend putting it under lightweight git tracking
(a repo separate from `claude-skills` is fine) so a bad diff has a
revert. Not yet part of this skill's automated steps — flag to Will if
ten+ syncs have happened with no versioning in place.

## Cadence

Default: weekly, aligned to the existing Sunday finance-review cadence.
Can also be triggered ad hoc with "sync tracker" or "refresh tracker".
