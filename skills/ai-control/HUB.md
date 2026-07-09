# Engineering Hub (load hub)
<!-- Freshness: 2026-07-09 | v1.0 | Home: claude-skills/skills/ai-control/ -->

## Mission
Single control system for all personal coding/engineering work. Fast handoff, minimal re-discovery,
compact memory usage. Rules live here; templates/schemas/commands live in HUB_GUIDE.md; live project
state lives in HUB_STATE.md. This file is rules-only — if a section needs an example, the example
belongs in the GUIDE.

## Trigger Contract
- Explicit trigger: `load hub` (variants: `hub`, `start hub`). Scoped: `load hub <project>` — skip
  detection, jump to that project's HUB_STATE section.
- Auto-activation: in Claude Code, a repo CLAUDE.md pointer loads this hub without the trigger phrase.
  Both activation modes follow the same Startup Sequence.
- First response after activation MUST confirm orientation in one line:
  `Hub loaded → [project] | [active task ID] | next: [next step]`.
- Access: Claude Code reads local files; web/Desktop sessions read the pushed GitHub copy
  (raw.githubusercontent.com/will55555/claude-skills/master/skills/ai-control/). Pushed state = visible state.

## Startup Sequence (mandatory order)
1) Detect active project from working folder (or from `load hub <project>` argument).
2) Follow Linear Fetch Mode below. Read nothing outside it.
3) Emit the orientation confirmation line.
4) If required artifacts are missing, apply Bootstrap Rules (offer, never auto-create).

## Linear Fetch Mode (straight-line speed path)
Fixed read order — never deviate, never parallelize:
`HUB.md → HUB_STATE.md [active project section ONLY] → TASKS.md [active task ONLY] → DEV_LOG.md [latest checkpoint ONLY]`
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
| Session ending / wrap-up | session-context-sync skill | Full sync pass (Notion/Obsidian/HUB_STATE) |
| `sync state` (any time) | — | Overwrite active HUB_STATE section now; no full pass |
| Rollover threshold hit | Rollover Rule below | Mandatory 4-part output |
| Note context needed | note-reader skill | Read-only fetch |
| New machine / first setup | GUIDE: New Machine Setup | Walk through portability checklist |
| Repeated correction / hub friction | Promotion Engine below | Flag inline; batch at session end |

## Agent Operating Constraints
- NO EXECUTION: never run `mvn test`, `./gradlew build|test`, `ng test`, `npm test|start`,
  `java -jar`, scripts, or any program/test — nor any equivalent in tools not listed. Will runs
  everything; agent supplies the exact command and expected result.
- Completion evidence = Will's report only. Never claim a test passed or a build succeeded from
  reading code.
- Flag freely, edit on approval: surface every issue the moment it's seen; never modify files,
  Notion, or logs without explicit approval. Preview before every commit/write.
- No unrelated refactors. Minimal, targeted changes only.
- Agent stance is reviewer/pair (see GUIDE: Agent Stance) — Will stays literate in everything the
  agent does; no black-box execution.

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
5) Working Memory block. Keep it scannable — same shape every time.

## Machine Paths
- All hub-internal references are relative to the claude-skills repo root.
- MULTI-MACHINE NOTE: absolute paths below are machine-specific, not portable assumptions. On any
  new machine, verify with `Filesystem:list_allowed_directories` before trusting a path — do not
  assume laptop 2 mirrors laptop 1's username or drive layout. GitHub raw URL access and the
  `load hub` trigger have no such dependency and are the reliable cross-machine fallback.
- Known absolute paths + caveats:
  | Machine/context | Path | Caveat |
  |---|---|---|
  | claude-skills repo | `C:\Users\solan\OneDrive\Desktop\SDE\claude-skills\` | Filesystem MCP CAN reach directly (verified 2026-07-09) — edit in place |
  | Other SDE repos (terra-api, roms, etc.) | `C:\Users\solan\OneDrive\Desktop\SDE\<repo>\` | Reachability unconfirmed — check `Filesystem:list_allowed_directories` each session; fall back to downloadables if absent |
  | Obsidian vault | `C:\Users\solan\iCloudDrive\iCloud~md~obsidian\iCloud\Obsidian Vault\` | Reachable; sync skill owns writes |
  | Hub (canonical) | `claude-skills/skills/ai-control/` | Local in Code; GitHub raw elsewhere |

## Secrets Hygiene
No API keys, tokens, credentials, or proprietary work code (FM internals) in hub files, TASKS.md,
or dev logs — everything here lands in git. Work-at-home HUB_STATE sections hold context only.

## Hub Update Gate
- `sync state` = overwrite active HUB_STATE section (+ log checkpoints if a dev-log entry is due).
- `sync framework` = edit HUB.md / HUB_GUIDE.md — only when an approved improvement candidate exists.
- MANDATORY: any edit to the Working Memory Contract above must update the session-rules web mirror
  (claude-skills/skills/session-rules/SKILL.md) in the same pass — the mirror carries the pointer +
  minimal WM format ONLY, nothing else. This is the single permitted duplication; keep it minimal.
- When the hub is updated, refresh the freshness stamp and note the change in ai-control's own DEV_LOG (create `skills/ai-control/DEV_LOG.md` on first use, per Bootstrap Rules).

## Skill Update Trigger
- Trigger: `sync skills` (variants: `push skills`, `update skills`). Runs any time a skill or hub
  file was edited this session — not only at session end (session-end sync still covers this via
  the Trigger Map row, but `sync skills` lets it fire on demand mid-session).
- What the agent CAN do directly: write/edit the local files in the claude-skills repo via the
  Filesystem tool, when that repo is reachable (verified for `claude-skills/` itself; check
  `Filesystem:list_allowed_directories` each session — don't assume). This is a real file edit,
  not a preview.
- PULL-BEFORE-EDIT (multi-machine safety): before editing any hub/skill file locally, ask Will to
  confirm this machine's local copy is current (`git pull` run recently, or this is the only
  machine in use this week). Editing a stale local copy risks overwriting changes pushed from
  another machine, silently. If Will can't confirm, supply `git pull` as the first command in the
  same instruction block as the eventual commit/push — pull before write, not just before push.
- What the agent CANNOT do: run git commands or call the GitHub API. No exec access on Will's
  machine, and entering credentials/tokens is prohibited outright — same rule as the no-execute
  constraint above, extended to git.
- On trigger:
  1) List every skill/hub file touched this session (path + one-line description of the change).
  2) Preview the change set — confirm before writing.
  3) On approval: write the files locally via Filesystem tools (if reachable) — this IS executed,
     not just described.
  4) Supply the exact commands for Will to run (never claim to run them):
     ```bash
     cd C:\Users\solan\OneDrive\Desktop\SDE\claude-skills
     git add -A
     git commit -m "chore: sync skills <YYYY-MM-DD> — <short summary>"
     git push
     ```
  5) State plainly that local write is done but push is NOT — Will must run the commands above
     before web/Desktop sessions see the update. Never say "pushed" or "synced to GitHub" unless
     Will has reported back that the push succeeded.
- If the claude-skills repo isn't reachable this session (Filesystem MCP doesn't list it), fall
  back to staged downloadable files in `/mnt/user-data/outputs/` with the same commands, same as
  any other unreachable-path scenario.
