# claude-skills Dev Log

## 2026-05-30 — Repo initialized and skills library deployed

### What this is and why it exists
This repo is the canonical source of truth for all Claude Code skills. Skills live here (not on individual machines) so they can be versioned, synced, and deployed to any machine from a single place. Notion mirrors the skills for readability and authoring, but this repo is what Claude Code actually reads.

The key insight: Claude Code resolves skills from a symlink. `setup.py` creates that symlink on each machine, pointing Claude Code's skill directory at this repo. From that point on, pulling this repo = deploying new/updated skills instantly — no manual copy-paste.

---

### How to set up a new machine

```bash
git clone <repo-url> ~/claude-skills
cd ~/claude-skills
python setup.py
```

That's all. The symlink is created once; every subsequent `git pull` automatically updates available skills.

---

### How to deploy skills (Notion → repo)

When Notion has the latest version and you want to push it into the repo:

1. For each skill in the Known Skills table in `CLAUDE.md`, fetch the Notion page via the Notion MCP
2. Extract the raw `SKILL.md` content (frontmatter + body, strip Notion metadata wrapper)
3. Write to `skills/<skill-name>/SKILL.md`
4. Commit: `git add -A && git commit -m "chore: deploy skills from Notion $(date +%Y-%m-%d)"`

Trigger phrase: "deploy", "sync from Notion", or "pull skills"

---

### How to push skills (repo → Notion)

When the repo has changes that Notion doesn't reflect yet:

1. For each skill, read `skills/<skill-name>/SKILL.md`
2. Update the corresponding Notion page content via the Notion MCP
3. Commit any local changes: `git add -A && git commit -m "chore: sync skills $(date +%Y-%m-%d)"`

Trigger phrase: "push to Notion" or "sync skills to Notion"

---

### Skill inventory

| Skill | Purpose |
|-------|---------|
| `session-context-sync` | End-of-session sync → Notion, Obsidian, HUB_STATE.md. EXCLUDED from the Notion deploy/push flow as of 2026-07-09 — too tightly coupled to hub-specific design to dual-author; edit directly in-repo |
| `consolidate-memory` | Deduplicate and prune memory files |
| `docx` | Word document creation and editing (.docx) |
| `note-reader` | Read notes from Notion / Obsidian |
| `pdf` | PDF read, fill, merge, split, OCR |
| `personal-os-dashboard` | Single-file HTML personal command-center dashboards |
| `pptx` | PowerPoint deck creation and editing (.pptx) |
| `schedule` | Scheduled remote agent cron jobs |
| `session-rules` | ARCHIVED as full skill 2026-07-09 — gutted to a thin Working Memory mirror; full system now lives in the Engineering Hub |
| `setup-cowork` | Cowork onboarding and plugin setup |
| `skill-creator` | Skill authoring framework with evals and benchmarks |
| `xlsx` | Excel workbook read/write/recalc (.xlsx) |
| ~~`dev-log`~~ | ARCHIVED 2026-07-09 — absorbed into the Engineering Hub's Documentation Protocol; frontmatter neutralized, kept for schema reference only |

Note: `skills/ai-control/` (the Engineering Hub) is NOT in this table — it's intentionally not a
frontmattered, auto-discovered skill (see its own `HUB.md` Mission section for why), and it is NOT
part of the Notion deploy/push flow above (see the 2026-07-09 entry below for why).

---

### Design decisions worth knowing

**Why `docx`, `pptx`, and `xlsx` each duplicate the OOXML schema bundle?**
Each skill is intentionally self-contained — no cross-skill dependencies. Duplication is the tradeoff for portability and isolation. If one skill's schema needs updating, it doesn't break the others.

**Why `skill-creator` has multi-agent evaluators?**
Building a new skill reliably requires iterative testing against real benchmarks. `skill-creator` includes `analyzer.md`, `comparator.md`, and `grader.md` agents plus a benchmark runner so new skills can be scored before being added to the library.

**Why Notion as the authoring surface?**
Notion is easier to read and edit than raw markdown for non-code content. The repo is the deploy target, not the authoring surface — that's why the deploy flow goes Notion → repo, not the other way around by default.

---

## 2026-07-09 — Engineering Hub v1.1 built and deployed

### What this is and why it exists
Personal (not Terra-specific) session/behavior control system, adapted from Will's work
Engineering Hub. Lives at `skills/ai-control/` as four plain docs (HUB.md, HUB_GUIDE.md,
HUB_STATE.md, TASKS.md) — deliberately NOT a frontmattered skill, reached via `load hub` or a
repo's CLAUDE.md pointer, not the symlink/auto-discovery mechanism described above.

### Key design decisions
- **Git is sole source of truth for `ai-control/`**; Notion may hold an informational dupe of hub
  state, never authoritative. This is the deliberate exception to this repo's Notion-authored-skills
  pattern above — the hub's fast local-edit design (Linear Fetch, `sync state`) needs one writer.
- **Linear Fetch Mode + snapshot-vs-log growth rule**: hot files (HUB_STATE sections) stay
  constant-size and overwritten in place; only cold files (DEV_LOGs) grow — guarantees single-pass
  retrieval regardless of how much history accumulates.
- **dev-log and session-rules skills absorbed** into the hub (Documentation Protocol, Working
  Memory Contract respectively); session-rules kept only as a thin WM-only mirror for web/mobile
  sessions that can't read local hub files.
- **Universal Sync & Fallback Queue**: Notion doubles as an informational dupe AND a drainable
  queue for content that missed its real target (git/Obsidian) when unreachable, tagged
  `#SyncQueue` and retried on next sync.
- **`sync skills` trigger** (git-only, local write + supplied commands, never auto-pushed) is
  deliberately distinct from this file's "push to Notion"/"deploy" phrases above — dropped the
  `push skills` variant specifically to reduce collision risk; full resolution still open.

### Files created/modified
- `skills/ai-control/HUB.md`, `HUB_GUIDE.md`, `HUB_STATE.md`, `TASKS.md` — new
- `skills/session-rules/SKILL.md` — gutted to WM-only mirror
- `skills/session-context-sync/SKILL.md` — Step 4C rewritten (HUB_STATE write, not CLAUDE.md);
  Target Overview updated with git-authority rule + Universal Sync & Fallback Queue
- `skills/archive/dev-log/SKILL.md` — neutralized (absorbed into hub Documentation Protocol)
- `skills/archive/session-rules-duplicate-OLD/SKILL.md` — found and neutralized; had been sitting
  in a stray "New folder/" with a colliding `name: session-rules` and drifted Notion IDs from
  before this session's ID-table cleanup

### Error — path references pointed at the wrong location
**Where:** HUB.md, HUB_GUIDE.md, session-rules, session-context-sync — all referenced
`claude-skills/ai-control/` when the real deployed location is `claude-skills/skills/ai-control/`.
**Root cause:** written before the files were actually placed on disk; assumption never verified
against the real deploy path.
**Fix:** corrected every reference across all four files.
**Why not leave it:** the GitHub raw URL, CLAUDE.md pointer template, and git reminder commands
would all have pointed at a path that doesn't exist.

### Known limitations / next
- CLAUDE.md pointers not yet placed in terra-api, roms, pios, terra-hq-site (SKILLS-005) — verify
  actual relative folder depth before pasting (default template assumes siblings under SDE/)
- Trigger-name collision between `sync skills` and this repo's "sync skills to Notion"/"deploy"
  phrases — partially mitigated, not fully resolved; needs Will's decision
- This repo's Notion mirror of session-context-sync is stale relative to tonight's edits — risk if
  "deploy"/"pull skills" runs before Notion is updated to match (SKILLS-014)
- Not yet dogfooded: first real test is `load hub tapi` in a fresh Claude Code session (SKILLS-006)

### Addendum (same day) — SKILLS-005, SKILLS-013, SKILLS-014, SKILLS-016 resolved
- **SKILLS-005:** CLAUDE.md pointers placed in terra-api (`../../`, double-nested — verified by
  reading actual folder structure, not assumed), terra-hq-site (`../`), and ROMS/
  restaurant-order-management-system (`../`, new minimal CLAUDE.md — none existed). PIOS skipped,
  no repo exists yet. Depth table recorded in HUB_GUIDE.md going forward.
- **SKILLS-013 (naming collision) — resolved, not just mitigated:** `sync skills` renamed to
  `sync hub`. Reasoning: a bare-vs-qualified phrase distinction is something someone has to
  remember (same failure class as the page-ID drift and duplicate-skill issues found earlier
  tonight) — better to make the collision structurally impossible. `sync hub` matches this hub's
  existing verb-first pattern (`sync state`, `sync framework`) and has zero overlap with "sync
  skills to Notion"/"deploy"/"push to Notion."
- **SKILLS-014 (stale Notion mirror) — resolved via permanent exclusion, not a one-time refresh:**
  `session-context-sync` excluded from the Notion deploy/push flow going forward (see Skill
  inventory table above and the skill's own file). A one-time Notion refresh would only reset the
  clock until the next independent edit on either side; exclusion removes the dual-authorship
  problem structurally instead.
- **SKILLS-016:** resolved earlier same day — fetched ADR-003 directly from Notion, confirmed
  self-issued JWT + provisioned-not-built Terra Auth is the real, current, Accepted decision.
  terra-api's local CLAUDE.md was stale (2026-07-07 blocker never updated after the 2026-07-08
  resolution); corrected to match.

---

## 2026-07-11 — HUB.md v1.3: Execution Role Boundary strengthened

### What changed
`## Agent Operating Constraints` in `skills/ai-control/HUB.md` was edited directly by Will
(mid-session, terra-api) to add an explicit **EXECUTION ROLE BOUNDARY (absolute)** subsection —
stronger, more literal language than the prior "NO EXECUTION" bullet: names the forbidden
commands (`./gradlew build|test`, `npm`, `mvn test`, `java -jar`, shell scripts), spells out the
7-step edit/run/report rhythm, and adds the "cognitive lock" framing (if Claude sees a command
window, it is not Claude's to use).

### Why this matters
The edit landed on disk without a stamp refresh or a log entry — a live Hub Update Gate gap
caught mid-session when Will asked "did you fully read the hub" after a `load hub` + status
check in terra-api. Freshness stamp still read `2026-07-10 | v1.2` despite the substantive
rewrite.

### Fix
- Freshness stamp bumped to `2026-07-11 | v1.3`.
- This entry closes the gate: content edit + stamp + log now all agree.

### Known limitations / next
- No functional rule change (the underlying no-execution policy was already in force) — this was
  a specificity/emphasis upgrade plus a process-hygiene fix, not a new constraint.

### Correction (same day) — OneDrive sync misdiagnosis
A later re-audit found terra-api's CLAUDE.md fix from the SKILLS-016 entry above had reverted
silently despite the edit tool confirming success (and, separately, that ROMS's CLAUDE.md was
never actually written — wrong tool used, sandbox `create_file` instead of the real
`Filesystem:write_file`). Both were fixed and re-verified present via fresh reads. The revert was
initially attributed to a "OneDrive sync race" — Will clarified the "OneDrive" folder name on
this machine is legacy naming only, with no actual active cloud sync running. That causal theory
was wrong; true root cause remains unconfirmed. HUB.md and HUB_GUIDE.md corrected to remove the
false attribution while keeping the practical rule (re-read after editing to confirm persistence,
regardless of cause) — the observed symptom was real even though the explanation wasn't.

---

## 2026-07-11 — HUB_GUIDE.md v1.2: project CLAUDE.md pointer convention codified

### What changed
Same terra-api session that caught the HUB.md v1.3 gap above also surfaced a second one: terra-api's
`CLAUDE.md` had described JWT (ADR-003) as "still empty stubs... not started" a full day after
TAPI-001 shipped and was verified end-to-end (2026-07-10) — HUB_STATE.md, TASKS.md, and DEV_LOG.md
all had it right, CLAUDE.md alone was stale. Traced the cause: none of `sync state`, `sync hub`, or
`load hub`'s Linear Fetch Mode ever write to or cross-check project CLAUDE.md files — it's read
once as the auto-activation pointer, then never revisited.

### Fix
- terra-api's `CLAUDE.md` corrected (JWT status, Next Action) and its own Key Decisions Log given
  a 2026-07-11 entry explaining the change.
- `HUB_GUIDE.md` → `Operating Incidents`: new entry recording the drift and root cause.
- `HUB_GUIDE.md` → `Per-Repo CLAUDE.md Pointer`: standing rule added — any "Next Action"/"Next
  Step"-style field in a project CLAUDE.md must be a pointer to `HUB_STATE.md`, never a duplicate,
  since nothing rewrites it. Feature/architecture-level "Current State" content stays local —
  HUB_STATE's fixed ~15–20 line snapshot shape can't hold it by design.
- Freshness stamp bumped to `2026-07-11 | v1.2`.

### Why not fix it by wiring CLAUDE.md into the sync pipeline instead
Considered (add CLAUDE.md as a fourth `sync` write target, or have `load hub` diff it against
HUB_STATE). Will chose the pointer approach instead — smaller, matches the hub's existing "shared
content = pointer, not copy" principle (Skill Interop, HUB.md), and removes the drift surface
structurally rather than adding another thing that has to stay synchronized.

### Known limitations / next
- Only terra-api's CLAUDE.md was corrected this session (ROMS, PIOS, terra-hq-site aren't
  reachable from this machine — see Machine Paths). Their CLAUDE.md files carry the same
  duplication risk and should get the same pointer treatment next time they're touched from a
  machine that can reach them.

---

## 2026-07-17 — HUB.md: Startup Sequence gets an active-project staleness check

### What changed
A terra-api session hit the same failure twice independently: HUB_STATE.md's claims about the
active project didn't match reality. First, Terra API's Next Step said `phase-4-governance` was
"not pushed/committed" when `git log`/`git status` showed it already committed and pushed at
`e05a1db`. Second, terra-hq-site's Active Task (THQ-001, "building public pages") was several
shipped phases out of date against that repo's own CLAUDE.md (11 pages + a Three.js visualizer
already live). Both were only caught by manually running local git checks against HUB_STATE text
mid-session — the Startup Sequence itself never did this.

### Fix
`HUB.md` → `Startup Sequence`: new step 4 (renumbering the old 4/5 to 5/6) — after Linear Fetch
Mode reads the active project's HUB_STATE section, run one cheap local check (`git log -1
--oneline` + `git status --short` at that project's Machine Paths root) and compare against the
Active Task/Next Step claims just read. Fold any mismatch into the orientation confirmation line
rather than silently trusting HUB_STATE text. Explicitly scoped as one check per active project,
not a trigger to re-derive the whole section from git history — the Linear Fetch Mode read-order
discipline still holds. Freshness stamp bumped to `2026-07-17`.

### Why not a broader HUB_STATE audit instead
Considered making `load hub` diff the entire active section against DEV_LOG/TASKS.md every time.
Rejected — that's exactly the "growth must never sit on the startup path" rule this hub already
follows for Linear Fetch Mode; a full audit is `sync state`'s job (on explicit trigger), not
something every `load hub` should pay for. The staleness check added here is deliberately narrow:
one git log + one git status, nothing else.

### Known limitations / next
- Scoped to Claude Code sessions with the active project's repo reachable locally — web/Desktop
  sessions reading GitHub raw have no local git to check, so they skip this the same way step 1's
  `git pull` is already Claude-Code-only.
- Only catches drift that shows up in `git log -1`/`git status` (e.g. "not committed" claims, or a
  Next Step already superseded by a later commit). Drift in prose *content* accuracy (like
  THQ-001's stale description, which was still a "clean" git state) needs a human or a deeper read
  to catch — this check would not have caught THQ-001 on its own, only the Terra API case. Worth
  revisiting if prose-level drift keeps recurring.

## 2026-07-18 — HUB.md v1.4: Hub Self-Sync Exception (Claude runs hub's own git loop)

### What changed
A terra-api session surfaced real friction: every HUB_STATE.md edit meant Claude drafting the
change, then handing back `git add`/`commit`/`push` commands for Will to paste, every single
time — the "Agent CANNOT run git commands" rule in Skill Update Trigger applied uniformly across
all of claude-skills, hub included. Will explicitly asked for a standing exception, scoped to just
the hub, that removes this back-and-forth entirely — no permission needed per instance, run it as
a loop.

### Fix
`HUB.md` gets a new `## Hub Self-Sync Exception` section: for files under `skills/ai-control/`
ONLY (`HUB.md`, `HUB_STATE.md`, `HUB_GUIDE.md`), Claude runs a bounded pull → commit → push cycle
itself (self-verified via `git log -1`/`git ls-remote`, then stops — not a background/standing
loop). `Skill Update Trigger`'s existing "Agent CANNOT run git commands" language narrowed to
apply only OUTSIDE `skills/ai-control/` (other skills, root docs, etc.), which still hand off
commands as before. `Startup Sequence` step 1 updated to match: Claude pulls the claude-skills
repo itself at hub load, silently: General git-remote-ops boundary (no fetch/pull/push without
being asked) is explicitly preserved for every OTHER repo, including terra-api — this exception is
intentionally narrow. Freshness stamp bumped to `2026-07-18`, version to `v1.4`.

### Why scoped this narrowly
Hub files are low-risk, frequently-touched, single-purpose sync artifacts, not product code — the
repeated command hand-off had no safety benefit there. The same logic doesn't extend to project
repos (terra-api, etc.): those pushes are visible/shared-state changes on real product work, where
the existing confirm-first default still holds. Content preview before writing is unchanged either
way — this exception removes the git-command hand-off, not the review step.

## 2026-07-26 — HUB.md v1.5: Response Contract gains a commit-message step

### What changed
A terra-api-home session (fixing a Postgres/Redis credential-duplication bug across
`docker-compose.yml`/`docker-compose.dev.yml`) surfaced a gap: the Response Contract had no step
for supplying a commit message after code edits were applied, so Will had to ask for one by hand.

### Fix
`HUB.md`'s Response Contract gets a new item 5 — after code edits are actually applied in a turn,
supply a ready-to-paste commit message (Conventional Commits format, per GUIDE: Commit
Conventions — imperative mood, task ID if one exists). Explicitly skipped on turns with no applied
edits, so it doesn't get pre-drafted speculatively. Working Memory block shifts to item 6.
Freshness stamp bumped to `2026-07-26`, version to `v1.5`.

### Why
Small, mechanical, easy to codify once — same pattern as other Response Contract items (state it
once as a standing step instead of Will re-requesting it per session).

---

## 2026-08-02 — HUB.md v1.7: Prime Directives hoisted; ADR Reference Links added

### The problem: a compliant read never reached the rules
Will flagged, after a long session of repeated violations, that the agent was
neither following hub rules nor checking project ADRs. Both turned out to be
structural rather than attentional.

**Rules.** Linear Fetch Mode caps reads at 80 lines per file. The Execution Role
Boundary — "Claude NEVER executes build/test/run commands. Period." — sat at line
102 of a 287-line HUB.md. So reading HUB.md *exactly as the protocol specifies*
never reached the single most-broken rule in it. This is also a violation of the
hub's own Growth Rule: "the top 80 lines must always be the highest-value 80
lines." Note the 2026-07-11 entry above already strengthened this same boundary
once; strengthening wording at line 102 could not fix a problem caused by
position.

**ADRs.** HUB_STATE.md contained zero URLs. terra-api's ADRs live in Notion, not
the repo, so "check the ADR" had no path — the agent inferred design intent from
code instead and got it confidently wrong: it treated terra-api-fe's planned
visualizer as a fork of terra-hq-site's, when terra-hq-site/CLAUDE.md lines 39-43
document them as deliberately different scopes (public 9-cube ecosystem vs.
per-customer entitlement-filtered), sharing one endpoint and one Three.js
reference implementation per terra-api-adr-009.

### Changes
- **Prime Directives** block at the very top of HUB.md — five non-negotiables
  (execution boundary, flag-freely/edit-on-approval, read-the-spec-first,
  pulls-on-load/writes-on-sync, ask-when-it-changes-the-work). Everything below
  elaborates; nothing overrides. Placement is the entire point.
- **Two Trigger Map rows**: "designing against an existing spec" → read the ADR
  before proposing; "about to run a build/test command" → stop, hand it to Will.
  The second deliberately duplicates Prime Directive 1 because the Trigger Map is
  what gets consulted per-action.
- **HUB_STATE gains a `Reference Links` field**, starting with Terra API: the
  Notion System Design doc and project page, plus the local specs that are
  authoritative and were being missed (terra-api-fe/TASKS.md's TFE phases,
  terra-hq-site/CLAUDE.md's two-visualizer architecture). Other projects get the
  field as links are confirmed — deliberately not backfilled with guesses.

### Honest limitation
None of this is enforcement. It is still instruction-following, and the rules
being broken were already written down. What changed is position: they now sit
inside the window the read protocol guarantees, on every load, instead of in a
section a compliant read skips.
