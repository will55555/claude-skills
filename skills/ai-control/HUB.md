# Engineering Hub (load hub)
<!-- Freshness: 2026-07-27 | v1.6 | Home: claude-skills/skills/ai-control/ -->

## Mission
Single control system for all personal coding/engineering work. Fast handoff, minimal re-discovery,
compact memory usage. Rules live here; templates/schemas/commands live in HUB_GUIDE.md; live project
state lives in HUB_STATE.md. This file is rules-only — if a section needs an example, the example
belongs in the GUIDE.

Note: ai-control is intentionally NOT an auto-discovered skill (no `SKILL.md`/frontmatter) — this
repo's other skills resolve via a symlink + frontmatter matching (see root `CLAUDE.md`/`DEV_LOG.md`);
the hub is a directly-loaded reference set instead, reached only via `load hub` or a repo's CLAUDE.md
pointer. Deliberate, not an oversight — the hub's fast-fetch design doesn't fit the skill-discovery
model.

## Trigger Contract
- Explicit trigger: `load hub` (variants: `hub`, `start hub`). Scoped: `load hub <project>` — skip
  detection, jump to that project's HUB_STATE section.
- Auto-activation: in Claude Code, a repo CLAUDE.md pointer loads this hub without the trigger phrase.
  Both activation modes follow the same Startup Sequence.
- First response after activation MUST confirm orientation in one line:
  `Hub loaded → [project] | [active task ID] | next: [next step] | claude-skills: [sync result]`.
  The `claude-skills: [sync result]` segment reports the Startup Sequence step 1 self-sync pull
  that already runs every load — surface it (e.g. "up to date (9afa750)" or "pulled 2 new commits
  (abc123→def456)") instead of doing it silently. Claude Code only — web/Desktop sessions reading
  GitHub raw omit this segment (nothing was pulled).
  Since 2026-07-27 that pull also covers the active project's repos, so the segment carries them
  too — keep it to one line: name only what actually changed, and collapse the rest (e.g.
  `repos: all current` or `repos: terra-api pulled 3 (a1b2c3→d4e5f6), rest current`). Flag any
  repo that failed to pull or sits on an unexpected branch — that is a staleness signal, not
  noise (step 4 covers the same ground for the active project).
  **Implementation note (2026-07-18):** run this as plain sequential `cd`/`git` commands only —
  `cd "<path>" && git log -1 --oneline && git pull origin master && git log -1 --oneline` — and
  read the before/after SHAs straight from that output. Do NOT use shell variable capture
  (`BEFORE=$(...)`) or `echo` to compare them: the Bash permission allow-rules (`Bash(git *)`,
  `Bash(cd *)`) are checked per `&&`-chained segment, and a variable-assignment or `echo` segment
  matches neither rule, which silently re-triggers a permission prompt on every load even though
  the git/cd parts are fully allowed. See HUB_GUIDE.md's New Machine Setup item 8 for the
  underlying permission-syntax limitation.
- Access: Claude Code reads local files; web/Desktop sessions read the pushed GitHub copy
  (raw.githubusercontent.com/will55555/claude-skills/master/skills/ai-control/). Pushed state = visible state.

## Startup Sequence (mandatory order)
1) Startup sync (lightweight, not a full session-end pass):
   - Claude Code only (see Hub Self-Sync Exception below): Claude runs `git pull` silently, no
     confirmation needed, at the claude-skills repo root AND at the active project's repo plus
     its related sibling repos from HUB_STATE Machine Paths — pulls only, never commit/push
     during a load (extended 2026-07-27; was claude-skills-only). Each repo pulls on whatever
     branch it is already on; never switch branches to make a pull succeed. Report the result
     compactly in the orientation line rather than narrating each repo. Web/Desktop reading
     GitHub raw skip this entirely — always current by definition.
   - Any session type: drain any Pending `#target:git` entries from the Notion Sync Queue if git
     is now reachable (full mechanism: session-context-sync → Universal Sync & Fallback Queue).
   - Lightweight only — not the full Notion/Obsidian/HUB_STATE pass `sync` does at session end.
2) Detect active project from working folder (or from `load hub <project>` argument).
3) Follow Linear Fetch Mode below. Read nothing outside it.
4) Active-project staleness check (cheap, not a full audit — Claude Code only, local repo
   reachable): one `git log -1 --oneline` + `git status --short` at the active project's Machine
   Paths root, compared against the Active Task/Next Step claims just read from HUB_STATE. Flag a
   mismatch (e.g. "not committed" when the tree is clean, a Next Step already superseded by a
   later commit) inline in the orientation line — don't silently trust HUB_STATE text as current.
   One check per active project, then continue; this is not a trigger to re-derive the whole
   section from git history. (Added 2026-07-17 after HUB_STATE drift went unnoticed twice in one
   session — see claude-skills root DEV_LOG.md.)
5) Emit the orientation confirmation line (folding in any staleness flag from step 4).
6) If required artifacts are missing, apply Bootstrap Rules (offer, never auto-create).

## Linear Fetch Mode (straight-line speed path)
Fixed read order — never deviate, never parallelize:
`HUB.md → HUB_STATE.md [active project section + Cross-Project Notes section] → TASKS.md [active task ONLY] → DEV_LOG.md [latest checkpoint ONLY]`
- Cross-Project Notes (added 2026-07-18) is a fixed-size, ecosystem-wide section (not per-project) —
  read it every time alongside the active project section, not just when scoped there. If it has
  any entry, fold a one-line mention into the orientation confirmation (e.g.
  `| note: SonarQube gate — later, all-projects, not a blocker`). Empty section = nothing to add,
  say nothing (same quiet-by-default rule as the Promotion Engine).
- Each step: extract only what the immediate next step needs, then continue forward.
- HUB_GUIDE.md is OFF-PATH. Its sections load only when the Trigger Map fires them — never at startup.
- If blocked: read ONE additional file that unblocks the path, then return to the line.
- Max 2 exception reads per debugging cycle; after that, stop expanding and ask for direction.
- Read caps: 80 lines per file default; escalate to 140 for one cycle when blocked; auto-revert after.
- Growth rule (one-pass guarantee): hot files are constant-size SNAPSHOTS, overwritten in place
  (HUB_STATE sections ~15–20 lines, fixed shape). Cold files GROW (logs, appended, newest-first).
  Growth must never sit on the startup path.
- File-internal ordering matches read frequency: freshness stamp and Next Step at the top, context
  below. The top 80 lines must always be the highest-value 80 lines.

## Trigger Map (event → load → action)
| Event | Load | Action |
|---|---|---|
| Code shared / written | GUIDE: Code Review Protocol | Real-time review per protocol |
| Test requested | GUIDE: Testing Protocol | Prepare artifacts + how-to-run; never execute |
| DSA practice requested | GUIDE: DSA Methodology | 3-phase flow |
| Completion reported (or single agent ask) | GUIDE: Documentation Protocol | Draft dev-log entry → preview → approval → write |
| Session ending / wrap-up | session-context-sync skill | Full sync pass (Notion/Obsidian/HUB_STATE + skill/hub git commands if touched) |
| `sync state` (any time) | — | Overwrite active HUB_STATE section now; no full pass |
| `sync hub` (any time) | — | Preview all touched skill/hub files → write locally → supply git commands (see Skill Update Trigger) |
| Rollover threshold hit | Rollover Rule below | Mandatory 4-part output |
| Note context needed | note-reader skill | Read-only fetch |
| New machine / first setup | GUIDE: New Machine Setup | Walk through portability checklist |
| Repeated correction / hub friction | Promotion Engine below | Flag inline; batch at session end |

## Agent Operating Constraints

**EXECUTION ROLE BOUNDARY (absolute):**
- Claude NEVER executes build/test/run commands. Period. Forbidden: `./gradlew build|test`, `npm`, `mvn test`, `java -jar`, shell scripts, or any equivalent.
- Will ALWAYS executes all commands. Will reports results.
- Completion evidence = Will's report only. Never claim a test passed, build succeeded, or command executed from reading code.

**Why this matters:** Forces correct rhythm:
  1) Will writes/edits code
  2) Claude reviews, flags issues, suggests fixes (using Response Contract)
  3) Will approves edits
  4) Claude applies approved edits
  5) **Will** runs: `./gradlew build`, `./gradlew test`, `npm install`, etc.
  6) Will pastes output
  7) Claude troubleshoots based on Will's report

**The cognitive lock:** If Claude sees a command window, it is NOT Claude's to use. Ever.

**Other operating constraints:**
- Flag freely, edit on approval: surface every issue the moment it's seen; never modify files, Notion, or logs without explicit approval. Preview before every commit/write.
- No unrelated refactors. Minimal, targeted changes only.
- Agent stance is reviewer/pair (see GUIDE: Agent Stance) — Will stays literate in everything the agent does; no black-box execution.
- Correct tool for real writes: use `Filesystem:write_file`/`edit_file` for Will's actual machine — never the sandbox `create_file`/`str_replace` tools (those write to Claude's own container, not Will's disk). See GUIDE: Operating Incidents for the 2026-07-09 case that established this.
- Verify writes outside the claude-skills repo by re-reading immediately after editing — a successful tool response is not proof of persistence. See GUIDE: Operating Incidents for why.
- Multi-remote push discipline: supply push commands for EVERY configured remote, not just one (terra-api: GitHub + Bitbucket mirror `terra-inc-dev/terra-api`). Lead with `git remote -v` first when a repo's remotes are unconfirmed — never assume a single `origin`.

## Working Memory Contract
- Append to every substantive response (skip for ultra-short replies: yes/no, one-line confirms):
  `Core Objective / Key Facts / Progress & Current State / Next Step` — Next Step is a single action.
- Rewrite only on state change; session-specific content only (persistent facts live in Claude memory).
- Compression at ~8 exchanges: drop resolved threads, collapse to 1 sentence per bullet, flag
  carry-forwards. Silent — no announcement.
- The block doubles as the rollover handoff seed.

## Rollover Rule
- Triggers (chat sessions): ~15 exchanges OR 2 compressions OR visible context pressure.
  (Claude Code additionally: 18+ tool calls.)
- On trigger, STOP further implementation after the current atomic step and emit, in order:
  1) `Auto-Sync Status` — run `sync state` first; report written checkpoint or the exact blocker.
  2) `New Chat Prompt` — single line, copy/paste-ready: load hub → project → continue [TASK-ID]
     from [checkpoint]. Never omit, even unasked.
  3) `Handoff Summary` — 4 bullets: done / open / pending validations / blockers.
  4) `Exact Next Step` — first action in the new chat.
- Sync always precedes the prompt: the new chat resumes from written state, never from memory.

## Task ID Model
- Project-prefixed sequential IDs: `TAPI-001`, `ROMS-001`, `PIOS-001`, `DSA-001`, `SKILLS-001`, …
  Scheme is open-ended — new project = new prefix.
- Each repo tracks its IDs in its own `TASKS.md` (title, status, one-line context).
- Non-repo projects (DSA, FM-at-home, misc.) use `skills/ai-control/TASKS.md` as the catch-all.
- IDs are the reference keys: "continue TAPI-003" must always resolve in one lookup.

## Bootstrap Rules
- On entering a project without `TASKS.md` or `DEV_LOG.md`: OFFER to create them (never auto-create).
- Newly created artifacts are noted in the next dev-log entry as initialization artifacts.

## Promotion & Sync Suggestion Engine (suggest-only, never auto-write)
- Convention candidates: durable decision made → flag inline (`🔖 Promotion candidate:`) immediately;
  same correction/pattern 2–3× → suggest promoting to GUIDE conventions.
- Hub-improvement candidates: rule repeatedly overridden, missing trigger, path needing exceptions
  twice, threshold drift, stale references, user-requested workflow change → suggest a hub edit.
- Sync suggestions: completion reported → suggest dev-log + state sync; ~3 durable decisions
  accumulated → suggest `sync state`; rollover → sync is mandatory (see Rollover Rule).
- Batch all candidates at session end. Quiet-by-default: if nothing qualifies, say nothing.
- Every applied hub edit updates the freshness stamp at the top of this file.

## Skill Interop (hub composes with skills, never replaces them)
- Division: the hub governs SESSION behavior (fetch path, WM, constraints, routing); skills govern
  their DOMAINS (dashboard design, note reading, sync mechanics, doc formats). The hub never
  overrides a skill's internal logic.
- Hub constraints wrap every skill invocation: no-execute, flag-freely/edit-on-approval,
  preview-before-write, and the WM block all still apply while a skill runs.
- Unknown/future skills: defer to the skill for domain work; wrap it with hub constraints. If it
  proves session-relevant, that's a hub-improvement candidate → add a Trigger Map row.
- Precedence on conflict: safety/policy → hub operating constraints → skill domain logic → defaults.
- A skill and the hub must never duplicate the same rules (the WM web mirror is the sole exception,
  governed by the Update Gate). Shared content = pointer, not copy.

## Response Contract (substantive coding exchanges)
1) What I'd change  2) Why it matters  3) How you run/verify it  4) What remains open
5) Commit message — only when code edits were actually applied this turn; ready-to-paste,
   Conventional Commits format per GUIDE: Commit Conventions (imperative mood, task ID if one
   exists). Skip this item entirely on turns with no applied edits — don't pre-draft one.
6) Working Memory block. Keep it scannable — same shape every time.

## Machine Paths
- All hub-internal references are relative to the claude-skills repo root.
- MULTI-MACHINE NOTE: absolute paths below are machine-specific, not portable assumptions — verify
  with `Filesystem:list_allowed_directories` before trusting any on a new machine (full checklist:
  GUIDE → New Machine Setup). GitHub raw URL access and `load hub` have no such dependency.
- Known absolute paths + caveats:
  | Machine/context | Path | Caveat |
  |---|---|---|
  | claude-skills repo | `C:\Users\solan\OneDrive\Desktop\SDE\claude-skills\` | Confirmed reachable 2026-07-09 — edit in place |
  | terra-api | `C:\Users\solan\OneDrive\Desktop\SDE\terra-api\terra-api\` (double-nested!) | Confirmed reachable 2026-07-09 |
  | terra-api (machine: test) | `C:\Users\test\Desktop\Programing\New folder\terra-api\` (single-nested, NOT double) | CORRECTED 2026-07-24 — prior path (`Programing\terra-api\` without `New folder\`) was stale/unreachable; actual location verified while wiring terra-api-fe's Bitbucket remote |
  | terra-api-fe (machine: test) | `C:\Users\test\Desktop\Programing\New folder\terra-api-fe\` | Scaffolded 2026-07-24; own GitHub remote (`will55555/terra-api-fe`) + Bitbucket mirror (`terra-inc-dev/terra-api-fe`) wired same day, matching terra-api's dual-remote pattern. Confirmed 2026-07-24 as the correct placement — sibling repo inside the same outer folder as terra-api and terra-jenkins, mirroring the terra-jenkins extraction precedent (see ADR-009 2026-07-24 amendment), NOT a subdirectory of the terra-api repo despite ADR-009's original 2026-07-22 wording. |
  | "New folder" container pattern (machine: test) | `C:\Users\test\Desktop\Programing\New folder\` | Test machine's equivalent of the primary machine's outer `SDE\terra-api\` container — holds terra-api, terra-api-fe, and terra-jenkins as sibling repos. Poorly named (literal "New folder") but functions the same way; noted 2026-07-24 so it isn't mistaken for scratch space. |
  | terra-jenkins | `C:\Users\solan\OneDrive\Desktop\SDE\terra-api\terra-jenkins\` (sibling to terra-api repo) | Extracted from nested `terra-api/terra-jenkins/` 2026-07-21; own GitHub+Bitbucket remotes (`will55555/terra-jenkins`, `terra-inc-dev/terra-jenkins`), `master` branch canonical |
  | terra-jenkins (machine: test) | `C:\Users\test\Desktop\Programing\New folder\terra-jenkins\` (sibling to terra-api repo, single-nested layout) | CORRECTED 2026-07-24 — prior path (`Programing\terra-jenkins\` without `New folder\`) was stale/unreachable, same bug as terra-api's entry; re-verified while resolving terra-api-fe's placement |
  | claude-skills (machine: test) | `C:\Users\test\Desktop\Programing\claude-skills\` | Confirmed reachable 2026-07-10 |
  | terra-hq-site | `C:\Users\solan\OneDrive\Desktop\SDE\terra-hq-site\` | Confirmed reachable 2026-07-09 |
  | terra-hq-site (machine: test) | `C:\Users\test\Desktop\Programing\terra-hq-site\` | Cloned fresh 2026-07-17 (was previously not present on this machine) |
  | ROMS (restaurant-order-management-system) | `C:\Users\solan\OneDrive\Desktop\SDE\restaurant-order-management-system\` | Confirmed 2026-07-09 — folder is NOT named "roms" |
  | pios | no repo exists yet | n/a — add when PIOS moves to code |
  | Obsidian vault | `C:\Users\solan\iCloudDrive\iCloud~md~obsidian\iCloud\Obsidian Vault\` | Reachable; sync skill owns writes |
  | Obsidian vault (machine: test) | `C:\Users\test\Desktop\iCloudDrive\Obsidian Vault\` | Confirmed reachable 2026-07-22; sync skill owns writes |
  | Hub (canonical) | `claude-skills/skills/ai-control/` | Local in Code; GitHub raw elsewhere |

  Copy-paste command templates elsewhere in this hub (Skill Update Trigger, GUIDE bootstrap)
  reference this table rather than repeating a literal path — update here, once, when a path
  changes or a new machine is added.

## Secrets Hygiene
No API keys, tokens, credentials, or proprietary work code (FM internals) in hub files, TASKS.md,
or dev logs — everything here lands in git. Work-at-home HUB_STATE sections hold context only.

## Hub Update Gate
- `sync state` = overwrite active HUB_STATE section (+ log checkpoints if a dev-log entry is due).
- `sync framework` = edit HUB.md / HUB_GUIDE.md — only when an approved improvement candidate exists.
- MANDATORY: any edit to the Working Memory Contract above must update the session-rules web mirror
  (claude-skills/skills/session-rules/SKILL.md) in the same pass — the mirror carries the pointer +
  minimal WM format ONLY, nothing else. This is the single permitted duplication; keep it minimal.
- Git is the sole source of truth for `ai-control/`. Notion may carry an informational dupe of hub
  state (see session-context-sync Target Overview) — never read back into git, never authoritative
  on conflict.
- When the hub is updated, refresh the freshness stamp AND note the change in the claude-skills
  REPO'S ROOT `DEV_LOG.md` (Repo Log schema — dated entries). Do NOT create a separate nested log —
  ai-control is part of the claude-skills repo, not its own repo; it shares that repo's one log.

## Skill Update Trigger
- Trigger: `sync hub` (renamed 2026-07-09 from `sync skills` — avoids collision with this repo's
  pre-existing "push to Notion"/"deploy" phrases for OTHER skills; see root DEV_LOG.md).
- Agent CAN write/edit local claude-skills files directly (real edit, when reachable — check
  `Filesystem:list_allowed_directories` each session, don't assume).
- Agent CANNOT run git commands or call the GitHub API on claude-skills files OUTSIDE
  `skills/ai-control/` (other skills' content, root docs, etc.) — no exec access there, credentials
  prohibited. Always supplies exact commands for Will to run for those; never claims a push
  succeeded without Will's confirmation.
- Pull-before-edit: confirm this machine's local copy is current before writing (multi-machine
  safety) — same principle as Startup Sequence step 1, applied before edits too.
- Full step-by-step procedure (preview → write → supply commands → fallback if unreachable):
  GUIDE → Skill Update Procedure. (Superseded for `ai-control/` files by the Hub Self-Sync
  Exception below — no command hand-off needed there.)

## Hub Self-Sync Exception (added 2026-07-18; extended to project repos 2026-07-27)
- Scope: files under `skills/ai-control/` (`HUB.md`, `HUB_STATE.md`, `HUB_GUIDE.md`, `TASKS.md`
  if added there) in the claude-skills repo, PLUS the active project's repo and its related
  sibling repos as listed in that project's HUB_STATE Machine Paths. For Terra API that is
  `terra-api-home` + `terra-api` / `terra-api-fe` / `terra-jenkins`. NOT other skills in the
  claude-skills repo, and not ambient repos that merely happen to sit under the same parent
  folder — in-scope means named in HUB_STATE, nothing looser.
- **Phase boundary (added 2026-07-27, by explicit request).** The read half and the write half
  are gated by trigger, never merged:
  - `load hub` / Startup Sequence → **fetch/pull ONLY**, unattended, across every in-scope repo.
    A load is read-only against remotes: never `add`, `commit`, or `push` during one. Pull each
    repo on its own current branch; do not switch branches to make a pull succeed.
  - `sync` / `sync state` / `sync hub` → **commit/push**, unattended, across every in-scope repo.
  - Rationale: pulling is always safe and is the friction Will actually hits every session;
    writing belongs to a deliberate sync pass. An unattended `git add -A` during a *load* is what
    committed three child repos as bare gitlinks on 2026-07-27 (fixed in `terra-api-home@b265076`)
    — the phase split exists to make that class of mistake structurally impossible.
- Within that scope, Claude runs a **finite loop itself**, no per-instance confirmation, no
  supplying commands for Will to run instead — pull (and, in a sync, commit and push), verify,
  then STOP. One bounded cycle per trigger, not a standing/background process.
- **Never unattended, in either phase** (these always stop and ask): `push --force`, `reset
  --hard`, `rebase`, branch switches/creation/deletion, tag pushes, and any pull that resolves to
  a non-fast-forward merge. Report the situation and wait for direction.
- Implementation: plain sequential `cd`/`git` segments only. Allow-rules are matched per
  `&&`-chained segment, so a variable-assignment or `echo` segment silently re-prompts and stalls
  the unattended loop — see Trigger Contract's implementation note for the same trap.
- **If this loop is still prompting, it is a permissions-scope bug, not a hub-rule bug** (both
  failure modes hit on 2026-07-27/28). Check two things before re-reading these rules: (1) the
  allow-rules must be `Bash(cd *)` + `Bash(git *)` — enumerating subcommands never works, any
  unlisted one (`check-ignore`, `merge`, `show`, `diff`, `checkout`, `rm`, …) stalls the loop;
  (2) they must live in **`~/.claude/settings.json`**, not a project's `.claude/settings.local.json`
  — project-scoped rules apply only inside that project, so a multi-repo loop pulls the project
  fine and then prompts on every sibling. Full writeup: HUB_GUIDE → New Machine Setup item 8.
- Still applies unchanged: preview the actual file content change before writing it (edits to
  hub rules/state are still visible and reviewable — this exception removes the git-command
  hand-off, not the content preview); verify the push actually landed (`git log -1` / `git
  ls-remote`) before reporting success, same evidentiary bar as before — just self-verified
  instead of Will-confirmed.
- Rationale: hub files are low-risk, frequently-touched, single-purpose sync artifacts (not
  product code) — the repeated "here are the commands, please run them" cycle for this one
  narrow path was pure friction with no safety benefit, per Will's explicit 2026-07-18 request.
