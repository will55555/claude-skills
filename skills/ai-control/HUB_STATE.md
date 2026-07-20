# Engineering Hub State
<!-- Freshness: 2026-07-19 (rev 13) | v1.3 | Snapshots only — overwritten in place. History lives in DEV_LOGs. -->
<!-- New project? Copy the template from HUB_GUIDE.md → HUB_STATE Section Template. -->

## Terra API                                        <!-- prefix: TAPI -->
- **Status:** Active — TAPI-012 CI/CD on its own branch `phase-6-cicd` now (moved off
  `phase-5-redis`, which is TAPI-011-only again, verified clean at `03bc7bf` on both remotes).
  EC2 box is live; Jenkins itself + the compose files are what's left.
- **Active Task:** TAPI-012 (Ecosystem CI/CD, terra-api-adr-010) — in progress
- **Next Step:** Create `docker-compose.staging.yml`/`docker-compose.prod.yml`, uncomment the
  two Deploy stages, stand up Jenkins (`terra-jenkins/docker-compose.jenkins.yml`) and do its
  setup (SSH Agent plugin, `server-ssh`/`dockerhub-credentials`/GitHub credentials,
  `DOCKERHUB_USERNAME` global env var, Pipeline job). `terra-shared-lib` deliberately not built
  yet — ADR's own ordering extracts it once both services' pipelines exist, not before.
- **Blockers:** None (SEC-001 done)
- **Context:** EC2 live — `t3.micro`, Ubuntu 24.04, Elastic IP `100.60.61.209`, security group
  SSH-only (staging kept internal-only on purpose, no public port; prod's port TBD). Docker +
  Compose v2 installed, SSH deploy key on GitHub (read-only). `~/terra-api-prod` (tracks
  `master`) and `~/terra-api-staging` (currently on old `phase-5-redis` checkout — needs
  `git checkout phase-6-cicd` next) both cloned on the box. `Jenkinsfile` live through Push to
  Docker Hub (Gradle, single-module, image `terra-api-be`, branch-tiered); Deploy/Frontend
  stages commented out with explanatory headers. Committed as `3b46754` on `phase-6-cicd`,
  pushed to both remotes.

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
