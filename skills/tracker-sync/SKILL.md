---
name: tracker-sync
description: Refresh command-center.html's project data from the Notion canonical Projects DB using a surgical diff-and-replace, never a full regeneration. Trigger on "sync tracker", "refresh tracker", "update command center", or on the weekly Sunday finance-review cadence. Never touches CSS, JS render functions, or nav — only the PROJECTS data array and GENERATED_AT.
---

# Tracker Sync Skill

Keeps `C:\Users\solan\OneDrive\Desktop\SDE\command-center.html` current against
the Notion canonical Projects DB (`collection://cf8f7353-f469-44bf-bbf2-56e1dfa280f3`)
without ever rewriting the file from scratch.

---

## Step 1 — Pull current DB state

Run this exact query against the canonical Projects DB:

```sql
SELECT Name, Domain, Status, Priority,
       "date:Start Date:start" as StartDate,
       "date:Last Synced:start" as LastSynced,
       Terra, url
FROM "collection://cf8f7353-f469-44bf-bbf2-56e1dfa280f3"
ORDER BY Domain, Status
```

## Step 2 — Read the existing file's PROJECTS array

Read `command-center.html` from the path above. Parse the
`const PROJECTS = [...]` block only. Do not touch anything else in the file.

## Step 3 — Diff, don't replace

Compare DB rows against the parsed array by `Name`:

| Case | Action |
|---|---|
| New row in DB, not in array | Append a new object literal at the correct domain position |
| Row exists in both, fields differ (Status/Priority/dates) | Edit just that object literal |
| Row in array, no longer in DB | Flag for removal, don't auto-delete — surface in the run summary and wait for confirmation |
| `pfdc-loandatacorrection` / any FM-work row | Never sync detail fields. Keep the isolated placeholder exactly as-is — name, domain, status "Active" only |
| Row has `source:"obsidian"` | Never overwrite from the Notion query — these are vault-only entries. Only touch them via a manual Obsidian re-scan, not this skill |
| No changes | Skip entirely, don't touch the file |

Always keep `TOP_OF_MIND` untouched — that section is session-curated, not
DB-sourced, and this skill has no authority to edit it. If it looks stale,
flag it in the summary; don't rewrite it.

## Step 4 — Update generation timestamp

Edit the `GENERATED_AT` constant to today's date. This is the only
non-data-array edit this skill is allowed to make.

## Step 5 — Report, don't narrate

After a sync, give a compact summary, not a play-by-play:

```
Tracker synced: +2 new (Terra Trademark Filing, Layer 2 Routing Fix),
3 status changes, 1 newly stale (NACA search, 52d). No removals.
```

If nothing changed: "Tracker checked — no changes since last sync."

## Isolation rule (always enforced)

FM-work rows never get dates, priority, or a Notion URL synced into this
file, regardless of what changes in the source DB. Status label only.

## Obsidian-sourced rows

Rows tagged `source:"obsidian"` (e.g. Terra Chain, Outlier.AI) come from
`C:\Users\solan\iCloudDrive\iCloud~md~obsidian\iCloud\Obsidian Vault`, not
Notion. This skill's Notion-diff pass must never touch them. A separate,
manually-triggered vault re-scan is the only thing that should update them —
run one periodically ("rescan obsidian for tracker") to catch new project
folders/notes the Notion DB will never see.

## Cadence

Default: weekly, aligned to the existing Sunday finance-review cadence.
Can also be triggered ad hoc with "sync tracker" or "refresh tracker".
