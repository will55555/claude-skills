# Engineering Hub State
<!-- Freshness: 2026-07-18 (rev 10) | v1.3 | Snapshots only — overwritten in place. History lives in DEV_LOGs. -->
<!-- New project? Copy the template from HUB_GUIDE.md → HUB_STATE Section Template. -->

## Terra API                                        <!-- prefix: TAPI -->
- **Status:** Active — Phase 5 complete, pivoting to CI/CD infrastructure (terra-api-adr-010)
- **Active Task:** TAPI-012 — Ecosystem CI/CD & Deployment Infrastructure (terra-api-adr-010)
- **Next Step:** (On different machine per user request) Set up Jenkinsfile in terra-api repo
  mirroring ROMS's pipeline; extract terra-jenkins (move Jenkins server config from ROMS repo
  into neutral home); define thin shared library (buildAndPushImage + deploySSH). Blocked on
  SEC-001 (plaintext GitHub PAT + AWS keys at SDE root → password manager).
- **Blockers:** SEC-001 must resolve before credential setup
- **Context:** TAPI-011 (Phase 5: Redis + Postgres audit migration) complete 2026-07-18,
  pushed to both origin + bitbucket (branch: phase-4-governance, 12 commits ahead locally).
  Local machine (`solan`) has clean working tree. Work continues on different machine.
  Full context: terra-api/TASKS.md → TAPI-011, terra-api/DEV_LOG.md → Phase 4/5 writeups.
  terra-api-adr-010 finalized in Notion + terra_api_strategy.html (domain-prefixed naming
  formalized 2026-07-18).

## ROMS                                             <!-- prefix: ROMS -->
- **Status:** Deployed
- **Active Task:** ROMS-001 — first real integration target for Terra API shared services
- **Next Step:** Define integration point — TAPI-001 (JWT auth) done 2026-07-10, unblocked
- **Blockers:** None
- **Context:** Spring Boot + React. First potential revenue source.

## PIOS                                             <!-- prefix: PIOS -->
- **Status:** Design phase — no coding until ADR-013 resolves
- **Active Task:** PIOS-001 — resolve ADR-013 (event schema versioning)
- **Next Step:** Draft ADR-013 options + tradeoffs
- **Blockers:** ADR-013 is the gating decision; ADRs 012–014 pending
- **Context:** Event-sourced. FastAPI/Python reserved. Rules-engine-gated AI signals.

## terra-hq-site                                    <!-- prefix: THQ -->
- **Status:** Active — parallel track
- **Active Task:** THQ-002 (Visualizer health-tier coloring) opened 2026-07-17, Planned/notes-only.
- **Next Step:** Implement color model (HEALTHY/YELLOW/ORANGE/RED tiers from Terra API
  `ecosystem-health` endpoint) to replace binary connected/disconnected. Open design question:
  per-cube polling vs. single Terra API ecosystem-health endpoint poll.
- **Blockers:** None
- **Context:** 2026-07-18 session completed: (1) Clarified dual-visualizer architecture (terra-hq-site
  public + terra-api-fe scoped both read from Terra API ecosystem-health endpoint — single source
  of truth); (2) Refactored terra_api_strategy.html (removed 430 lines embedded WebGL, added
  domain-prefixed ADRs terra-api-adr-001–010, linked to build phases); (3) Fixed product pages
  (ROMS/PIOS using domain-prefixed ADRs roms-adr-001–005, pios-adr-011–015); (4) Cleaned up Notion
  CI/CD pages (renamed ADR-009→terra-api-adr-010, updated status/references). All changes staged for
  commit. CLAUDE.md, TASKS.md, terra_api_strategy.html modified locally; ready to commit.

## DSA Practice                                     <!-- prefix: DSA -->
- **Status:** Active — recurring
- **Active Task:** DSA-001 — Arrays (start of progression)
- **Next Step:** First Arrays problem via 3-phase methodology
- **Blockers:** None
- **Context:** Java default. Arrays → Strings → Linked Lists → Trees → Graphs → DP.

## Cross-Project Notes                              <!-- no prefix — ecosystem-wide, not project-scoped -->
- **SonarQube gate (noted 2026-07-18):** Ecosystem-wide code-quality pass planned across all
  projects, once, before full deployment — not a per-project or per-PR blocker. Intent: keep
  developing/adding functionality now, run it later, likely wired into the CI/CD pipeline being
  built under Terra API's TAPI-012. No task ID yet — too early to scope.

## claude-skills                                    <!-- prefix: SKILLS -->
- **Status:** Active — hub v1.1 complete, pointers placed, both open decisions resolved
- **Active Task:** SKILLS-006 — dogfood: run `load hub tapi` in a fresh Claude Code session
- **Next Step:** Open a real Claude Code session in terra-api, confirm the CLAUDE.md pointer
  auto-activates the hub, verify orientation line, log any friction
- **Blockers:** None
- **Context:** Hub v1.1 committed and pushed 2026-07-09 (first round); second round of fixes
  (CLAUDE.md pointers, `sync skills`→`sync hub` rename, session-context-sync excluded from
  Notion flow, TAPI/ADR-003 correction) applied on disk, not yet committed. Git = sole source of
  truth for ai-control; Notion = informational dupe only.
