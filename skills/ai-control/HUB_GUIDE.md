# Engineering Hub Guide
<!-- Freshness: 2026-07-18 | v1.3 | Cold storage: sections load ONLY via HUB.md Trigger Map -->
<!-- Lego rule: every section below is self-contained and deletable without breaking any other. -->

## Agent Stance
- Reviewer/pair, not executor: watch the work in real time, flag what's wrong the moment it's seen,
  explain WHY, then explore better options together. Conversational — correct, teach, help think.
- Manager/agent principle: Will directs and verifies; the agent proposes and explains. Will stays
  literate in everything the agent does — no black-box output.
- Teach, don't just correct: every flagged issue explains the MECHANISM (why the bug happens, what
  invariant breaks) — never just "best practice says."
- Keep Will moving fast but thinking clearly: quick correctness pass first (is it right?); deeper
  optimization pass only on request (is it the best way?).

## Code Review Protocol
Response template for any shared/written code:
```
✅ Right: [what's solid — always include; reinforces good instincts]
🔴|🟡|🟢 Issue: [what's wrong, severity-tagged]
   Why it matters: [mechanism, not citation]
   Edge case / tradeoff: [what breaks, or what's traded away]
   Suggested direction: [a nudge, not a rewrite — unless asked]
```
- Severity: 🔴 blocking · 🟡 worth fixing · 🟢 nitpick/style (mirrors ADR-005 grading).
- Confidence tags: state plainly whether an issue is a BUG (certain) or an OPINION (judgment/style)
  so real defects are never confused with taste.
- Flag freely, edit on approval (constraint lives in HUB.md).
- Patterns-I-keep-correcting: same class of mistake 2–3× → 🔖 promotion candidate for Conventions.

## Universal Coding Conventions (all projects)
- Less code first: before proposing anything, ask "fewer lines without sacrificing clarity?"
  Default answer is yes. Guardrail: a dense unreadable one-liner loses to three clear lines.
- Boring over clever · Immutability by default · Single Responsibility, ruthlessly ·
  Fail fast/loud at boundaries · Depend on abstractions, not implementations ·
  No premature abstraction (2–3 concrete cases before generalizing) ·
  Version contracts from day one · Tests as documentation · Comments explain WHY, not what ·
  Delete dead code aggressively.
- Lego, not Tetris (modularity test): can this piece be removed or swapped without editing anything
  else? If removing a class means chasing edits in three other files, it is coupled, not modular —
  no matter how clean it looks in isolation. Applies to code AND to these hub files themselves.

## Terra Conventions (load only for Terra-associated projects)
- No Terra prefix on class names — the `com.terra` package establishes ownership.
- REST over GraphQL by default (revisit only for Real Estate / Apparel catalogs, both inactive).
- Boring, deferrable infrastructure: Caffeine before Redis; SQLite before PostgreSQL.
- Terra API boundary is constitutional: shared infrastructure only — never business logic, business
  data, or presentation.
- Brand quantities are multiples of 5 (5 / 25 / 55 / 555) wherever counts surface in product work.

## Testing Protocol
- Agent PREPARES test artifacts: Postman bodies, curl commands, sample payloads, expected responses,
  unit-test code — and states exactly how to run them (command + steps + what success looks like).
- Agent NEVER executes (command list in HUB.md). Will runs; Will reports; the report is the only
  completion evidence.
- Unit tests the agent writes must explain what they verify and why that case matters.

## DSA Methodology (3-phase)
1) Planning — clarify the problem, question assumptions/edge cases, explain the algorithm and WHY it
   works, state expected time/space complexity BEFORE any code.
2) Coding — Java by default; clean interview-quality code, meaningful names; correct before optimized.
3) Optimization — analyze, explore better algorithms/data structures, explain tradeoffs, present the
   optimized solution with updated complexity.
- Topic progression: Arrays → Strings → Linked Lists → Trees → Graphs → Dynamic Programming.
- Efficiency bias throughout: quality over quantity of lines; no convoluted/useless code.

## Documentation Protocol (dev-log, absorbed)
WHY over WHAT. Diffs say what changed; the log says why this approach, what constraints drove it,
how to reproduce on a fresh machine, what broke and its root cause, what's next.

Phase Log schema (active feature projects — per-repo DEV_LOG.md, newest phase PREPENDED):
```
## Phase N — [Name]
**Date:** YYYY-MM-DD  **Status:** Complete | In Progress | Blocked
### Goal                      [why this was the right next step]
### Key Design Decision       [chosen over which alternatives, and why]
### Files Created / Modified  [file → what it does, why structured this way]
### Setup / Recipe            [commands with WHY comments on non-obvious steps]
### Build / Test Result       [as reported by Will]
### Known Limitations / Next  [what's deferred and why]
```
Bug entry (inside the relevant phase):
```
### Error — [short description]
**Where:** [stage/file/test]  **Full error:** [paste]
**Root cause:** [WHY it happened]  **Fix:** [what changed, why it works]
**Why not [alternative]:** [rejected options + reasons]
```
Repo Log schema (tool/infra repos): permanent reference sections — what/why it exists, how-to
recipes with WHY comments, inventory table, design decisions worth knowing.

Rules:
- Trigger: Will reports completion, OR one agent ask ("Looks like [phase] is complete — log it?").
  Never log from agent inference alone. Always preview → approval → write.
- Placement: every repo keeps its own DEV_LOG.md at root (split FRONTEND_/BACKEND_ if needed).
- Central rollups are association-based (e.g. `TERRA_DEV_LOG.md` for cross-Terra decisions) and hold
  POINTERS ONLY — never copies of repo-log content. Create a rollup only when cross-repo decisions
  justify it.
- Quality bar: WHY not just WHAT · non-obvious flags commented · alternatives named + rejected ·
  root cause not just fix · reproducible on a fresh machine from the log alone.
- Analogy habit: anchor new concepts to Spring Boot/Java when introducing frontend/infra ideas.

## Skill Update Procedure (full detail for `sync hub` — rule summary lives in HUB.md)
Runs any time a skill or hub file was edited this session — not only at session end.

1. List every skill/hub file touched this session (path + one-line description of the change).
2. Preview the change set — confirm before writing.
3. On approval: write the files locally via Filesystem tools (if reachable) — this IS executed,
   a real edit, not just described.
4. Pull-before-edit: before writing, confirm this machine's local copy is current (recent
   `git pull`, or this is the only machine in use this week). Editing a stale copy risks silently
   overwriting changes pushed from another machine. If unconfirmed, supply `git pull` as the first
   command in the same instruction block as the eventual commit/push.
5. Supply the exact commands for Will to run (never claim to run them), using the path from
   HUB.md's Machine Paths table (don't hardcode — it drifts on a second machine):
   ```bash
   cd <claude-skills repo root — see Machine Paths table>
   git add -A
   git commit -m "chore: sync hub <YYYY-MM-DD> — <short summary>"
   git push
   ```
6. State plainly that local write is done but push is NOT, until Will confirms it succeeded.
   Never say "pushed"/"synced to GitHub" without that confirmation.
7. If claude-skills isn't reachable this session, fall back to staged downloadable files in
   `/mnt/user-data/outputs/` with the same commands.

## Operating Incidents (reference — lessons already codified as rules in HUB.md)
Real incidents from 2026-07-09 that produced standing rules. Kept here for full context; the
terse rule itself lives in HUB.md's Agent Operating Constraints — this section is the "why."

**Wrong tool used for a real write (ROMS's CLAUDE.md):** created via the sandbox `create_file`
tool instead of `Filesystem:write_file`. The sandbox tool writes to Claude's own ephemeral
container, not Will's disk — the file appeared created (successful tool response) but never
existed on Will's machine. SKILLS-005 was marked done for ROMS based on this false success.
Caught only when a later audit tried to read the file back and got ENOENT. Fixed by recreating
with the correct tool and verifying presence via a fresh read.

**Edit reverted silently (terra-api's CLAUDE.md):** a multi-part edit_file call succeeded (tool
returned a clean diff) during the SKILLS-016 fix, but a later re-audit found the file back at its
original pre-edit state — not corrupted, not merge-conflicted, just cleanly reverted. Initially
attributed to a OneDrive sync race (the file sits in a folder named "OneDrive"), but Will clarified
that folder name is legacy only — no active cloud sync runs on this machine. True root cause
remains unknown. The fix was redone as three smaller edits and re-verified present via fresh read.
The practical lesson survives independent of the (wrong) explanation: a successful tool response
is not proof of persistence for files outside the primary hub repo — re-read to confirm.

**Project CLAUDE.md drifted from HUB_STATE with no mechanism to catch it (terra-api, 2026-07-11):**
terra-api's `CLAUDE.md` described JWT (ADR-003) as "still empty stubs... not started" a full day
after TAPI-001 shipped and was verified end-to-end (2026-07-10) — HUB_STATE.md, TASKS.md, and
DEV_LOG.md all had it right. Root cause: none of `sync state` (writes HUB_STATE.md only), `sync
hub` (writes HUB.md/HUB_GUIDE.md only), or `load hub`'s Linear Fetch Mode (reads HUB_STATE as the
snapshot of record, never cross-checks project CLAUDE.md) touch project CLAUDE.md files at all —
it's used once, as the auto-activation pointer, then never revisited. Caught only because Will
asked "did you fully read the hub" after a status check surfaced the contradiction.
**Fix pattern (see Per-Repo CLAUDE.md Pointer below for the standing rule):** don't try to keep
CLAUDE.md's task-status fields in sync with HUB_STATE — replace them with a pointer instead.
Feature/architecture-level detail (what shipped, why) has no other home and stays in CLAUDE.md as-is
— HUB_STATE is a fixed ~15–20 line snapshot by design and can't carry it, so only genuinely
duplicated fields (Next Action / Next Step) should collapse to a pointer, not the whole section.

**ROMS EC2 instance permanently lost, no backup existed (discovered 2026-08-07, originally
happened sometime before 2026-07-29):** ROMS's original production EC2 instance — Postgres
database, Elastic IP, everything — was found completely gone during a full 17-region AWS sweep:
no running/stopped/terminated instance record anywhere, no EBS snapshot in any region, the
Elastic IP fully released and reassigned to a different AWS customer. Only artifact found was an
orphaned `roms-key` key pair in `us-east-2`, confirming the original region but recovering
nothing. Root cause of the loss itself is unknown (never determined whether it was deliberate
cleanup, an account-level safeguard, or an accident) — the actual gap this exposed is that
**no EC2 instance in the Terra ecosystem had automated backups**, so whatever happened, there
was zero path to recovery. Caught only because Will decided to redeploy ROMS and asked to verify
the instance still existed first — if that check had never happened, the loss would have stayed
undiscovered indefinitely.
**Fix pattern (see Infrastructure Backup Policy below for the standing rule):** every EC2 instance
in the Terra ecosystem gets tagged `Backup=true` and covered by a tag-based AWS Backup plan with
daily automated EBS snapshots — this makes "instance gone with zero recovery path" structurally
impossible going forward, independent of why an instance disappears. A manual pre-termination
snapshot step is the second layer, for the deliberate-termination case specifically.

## Infrastructure Backup Policy (standing rule since 2026-08-07)
Added after the ROMS EC2 loss above — see Operating Incidents for the full incident. Two layers,
not one, since either can fail independently:

1. **Automated (primary defense):** every EC2 instance in the Terra ecosystem is tagged
   `Backup=true` at creation and covered by a tag-based AWS Backup plan (daily EBS snapshots, 7-day
   retention minimum — tune per instance if a longer window is warranted, e.g. a database-bearing
   box). This is the layer that survives forgetting, accidents, and account-level cleanups — it
   requires no human to remember anything at termination time. One-time setup: a backup vault +
   plan + tag-based selection rule (commands: ask Claude for the current `aws backup` CLI sequence
   when setting up a new AWS account/region, since exact syntax may drift). Ongoing requirement:
   every NEW instance gets the `Backup=true` tag at launch — this doesn't retroactively cover
   anything untagged.
2. **Manual pre-termination check (secondary defense):** before deliberately terminating any EC2
   instance, confirm a recent backup exists (`aws backup list-recovery-points-by-resource
   --resource-arn <arn>`) or take one explicitly if automation isn't yet wired up for that
   instance. This catches the case where an instance was spun up between backup-policy setup and
   now, or backup automation itself silently failed.

Applies to every EC2 instance across the ecosystem — Terra API's prod box, `terra-jenkins`, and
ROMS's rebuilt instance once ROMS-001 provisions it. Retrofit existing untagged instances the next
time each is touched, rather than as a dedicated pass — matches this project's established
pattern of not doing speculative cleanup ahead of actual need.

## Commit Conventions
- Conventional Commits: `feat: | fix: | docs: | refactor: | test: | chore:`; imperative mood;
  subject ≤ ~65 chars; reference the task ID when one exists — `feat(TAPI-003): add TokenValidator seam`.
- Small, frequent commits over big batches — pairs with the phase-branch model.
- No PR ceremony while solo; revisit when a second contributor exists.

## HUB_STATE Section Template (paste-in for new projects)
```
## [Project Name]                                   <!-- prefix: XXXX -->
- **Status:** [Active | Paused | Design | Deployed]
- **Active Task:** [XXXX-NNN — one-line title]
- **Next Step:** [single action]
- **Blockers:** [list or None]
- **Context:** [≤3 lines — stack, branch, phase. Snapshot, not history.]
```
Hard budget ~15–20 lines. Overwritten in place on every sync — history goes to DEV_LOG, never here.

## Copy/Paste Commands
- Bootstrap (web/Desktop, fully portable — no machine path needed): `Load the Engineering Hub from
  https://raw.githubusercontent.com/will55555/claude-skills/master/skills/ai-control/HUB.md — apply all
  rules; project = <name>; continue <TASK-ID> from latest checkpoint.`
- Scoped start: `load hub <project>`
- Mid-session checkpoint: `sync state`
- Full session-end pass: `sync` (fires session-context-sync)
- Framework edit (only with approved candidate): `sync framework`
- Quick status: `Using HUB_STATE + active TASKS.md: done / open / next in 5 bullets max.`
- Rollover (agent emits automatically at threshold; manual trigger): `roll over`
- Update skills/hub (local edit + git commands supplied; Will runs push): `sync hub`

## Per-Repo CLAUDE.md Pointer (auto-activation in Claude Code)
Paste into each repo's `CLAUDE.md` once (append to existing content if the file already has
project context — never overwrite). Enables the hub to load automatically on session start —
no `load hub` phrase needed.
```markdown
## Engineering Hub
At the start of every substantive session, read and apply all rules from:
`../claude-skills/skills/ai-control/HUB.md`
The hub is the source of truth. Update the hub, not this file.
```
Default example above assumes the repo sits as a SIBLING of claude-skills directly under
`SDE/` (one level up: `../`). **Depth is NOT uniform across repos — verified per-repo 2026-07-09:**

| Repo | Actual git root | Depth needed | Status |
|---|---|---|---|
| terra-api | `SDE/terra-api/terra-api/` (double-nested!) | `../../` | ✅ pointer added |
| terra-hq-site | `SDE/terra-hq-site/` (sibling) | `../` | ✅ pointer added |
| restaurant-order-management-system (ROMS) | `SDE/restaurant-order-management-system/` (sibling) | `../` | ✅ pointer added (new minimal CLAUDE.md, none existed) |
| pios | no repo exists yet | n/a | — nothing to point; add when PIOS moves to code |

Don't trust this table blind on a future machine either — folder layout can differ per machine
(see Machine Paths). `list_directory` the actual repo before assuming depth.

Non-repo projects (DSA, FM-at-home) have no CLAUDE.md — use the
explicit `load hub` / `load hub <project>` trigger for those instead.

**Task-status fields must point at HUB_STATE, not duplicate it.** If a repo's CLAUDE.md carries a
"Next Action"/"Next Step"-style field, write it as a pointer (`See HUB_STATE.md → [Project] →
Next Step`) rather than restating the current pick — nothing in the sync/load pipeline writes
back to project CLAUDE.md files, so any duplicated status field WILL drift silently (see Operating
Incidents, 2026-07-11, for the terra-api case this was caught from). Feature/architecture-level
content (a "Current State" changelog of what shipped) is fine to keep local — HUB_STATE's
fixed-size snapshot can't hold that detail and isn't meant to.

## New Machine Setup (portability checklist)
Run once per new machine. Do NOT assume laptop 2 mirrors laptop 1's paths, MCP config, or git state.

1. **Verify reachability first** — `Filesystem:list_allowed_directories` before trusting any
   absolute path. If the Filesystem MCP isn't configured for this machine yet, set its allowed
   directories to include the claude-skills repo location on THIS machine (may differ from
   `C:\Users\solan\...` if username/drive differs).
2. **Get a real git clone, not a synced folder — but verify sync is actually active first.** A
   folder named "OneDrive" or "iCloud" doesn't necessarily mean live cloud sync is running —
   confirmed on Will's primary machine 2026-07-09 (the "OneDrive" path is legacy naming only, no
   active sync). Check the actual sync client's status before assuming risk. If sync genuinely IS
   active, treat that copy as read-only staging — do not run git commands against a `.git` folder
   a file-sync service is also touching (risk of corruption from concurrent sync + git writes).
   If unsure or sync is confirmed active: `git clone https://github.com/will55555/claude-skills.git`
   into a plain local folder outside any sync service, and do git operations there.
3. **Reachability-only fallback:** if this session can't get local file access at all (Desktop/web,
   or Filesystem MCP not yet configured), use the GitHub raw bootstrap prompt from Copy/Paste
   Commands — fully portable, no machine setup required.
4. **Verify the hub loads correctly:** `load hub` and confirm the orientation line comes back with
   real project/task data, not an error.
5. **Update Machine Paths in HUB.md** with this machine's actual verified paths once confirmed —
   this is itself a `sync hub` edit (local write + git commands supplied, Will pushes).
6. **Obsidian vault path** may also differ on this machine — verify separately before the sync
   skill attempts an Obsidian write; don't assume the laptop-1 path.
7. **Every session after setup, on ANY machine:** the Startup Sequence's step 1 (HUB.md) now
   handles this automatically — confirm/pull before trusting local files. Nothing extra to do
   here; noted for awareness that this applies beyond just first-time setup.
8. **Re-grant the Hub Self-Sync Exception's tool permissions on THIS machine** (added 2026-07-18,
   revised same day once tested live). HUB.md's Hub Self-Sync Exception lets Claude pull/commit/
   push `skills/ai-control/` files without asking, but the actual permission-prompt suppression
   lives in `~/.claude/settings.json`, which is per-machine and does NOT travel with a git pull.
   Two parts, only one of which is path-dependent:
   - `permissions.additionalDirectories` + `Read(...)`/`Edit(...)` allow rules scoped to THIS
     machine's absolute `skills/ai-control/` path (see Machine Paths table) — an entry copied
     verbatim from another machine's settings.json will not match, since the path differs.
   - `Bash(git *)` AND `Bash(cd *)` allow rules — neither is path-scoped, both copy as-is to any
     machine. Tried scoping to the hub directory via a `Bash(cd "<path>" && git *)` combined
     pattern first; doesn't work, because the permission engine checks each `&&`-chained command
     segment independently, so neither half ever matches alone against one combined rule. There
     is no rule syntax that fences a Bash allow to "only when cwd is X" — global allow (any repo,
     any directory) or a prompt every time are the only two options. Went with global allow,
     2026-07-18. The permission grant is a ceiling, not a mandate: scope is enforced by
     instruction-following, not by the tool layer. Since 2026-07-27 the instruction side is
     HUB.md's extended Hub Self-Sync Exception — `ai-control/` plus the active project's
     HUB_STATE-listed repos, with pulls on `load hub` and commits/pushes on `sync`. The tool-layer
     grant did not change; only what Claude is instructed to do with it did.
   - **Permission rules needed for the extended (2026-07-27) scope**, since a `load hub` now pulls
     several repos and a `sync` pushes them. Exactly two rules, and both must be wildcards:
     **`Bash(cd *)` and `Bash(git *)`.**
     - **Do NOT enumerate subcommands.** Tried `Bash(git pull *)`, `Bash(git fetch *)`,
       `Bash(git status *)` etc. on 2026-07-27 — it prompts constantly, because the list can never
       be complete. `check-ignore`, `merge`, `show`, `diff`, `checkout`, `ls-files`, `cat-file`,
       `rev-list`, `merge-base`, `ls-remote`, `rm` all fell through within one session. Any
       subcommand not literally listed stalls the unattended loop. `Bash(git *)` covers all of them.
     - **Scope them to `~/.claude/settings.json` (user), NOT a project's
       `.claude/settings.local.json`.** Project-scoped rules apply ONLY inside that project's
       directory. Since `load hub`/`sync` walk several sibling repos, rules parked in
       `terra-api-home/.claude/settings.local.json` silently do nothing for claude-skills or any
       other repo — the loop pulls terra-api-home fine, then prompts on the hub's own sync. Cost a
       full session of "why is it still asking?" on 2026-07-28 before the scope was spotted.
     - The write side (`add`/`commit`/`push`, all covered by `Bash(git *)`) is deliberately
       allowed: Will syncs at session end and expects every project's changes to go up in that one
       pass, unattended. The load/sync phase split that keeps writes from firing during a *load* is
       an instruction in HUB.md, not a permission rule — the tool layer cannot express "only during
       sync." Grant is a ceiling; scope is enforced by instruction-following.
   - Both `git *` and `cd *` are needed, not just `git *` — a compound command like
     `cd "<path>" && git log ... && git pull ... && git log ...` has `cd` as its own independent
     segment too. Even with `git *` allowed, an un-allowed `cd` (or worse, a variable-assignment
     segment like `BEFORE=$(git log ...)`, which matches neither rule) still triggers a prompt.
     Keep hub self-sync commands to plain sequential `cd`/`git` segments only — no shell variable
     capture, no `echo` — see HUB.md's Trigger Contract implementation note for the concrete
     command shape this settled on.
   One-time per machine, not per session.
