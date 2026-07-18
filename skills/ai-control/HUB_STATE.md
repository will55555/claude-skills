# Engineering Hub State
<!-- Freshness: 2026-07-18 (rev 8) | v1.3 | Snapshots only — overwritten in place. History lives in DEV_LOGs. -->
<!-- New project? Copy the template from HUB_GUIDE.md → HUB_STATE Section Template. -->

## Terra API                                        <!-- prefix: TAPI -->
- **Status:** Active — primary build
- **Active Task:** None in progress — **TAPI-011 (Phase 5: Redis + Postgres
  audit migration) Done, live-verified 2026-07-18.** Built on `phase-5-redis`:
  Redis property-driven config (ADR-001), Postgres `schema.sql` +
  `AuditLogRepository` (JdbcTemplate, dual-write alongside the JSON audit
  log), insert moved off the hash-chain lock via a bounded `@Async` executor,
  profile-gated+idempotency-guarded `AuditLogBackfillRunner`,
  `docker-compose.yml` for local Redis+Postgres. `docker-compose up` +
  a real request confirmed an actual row landed in `audit_log` end-to-end —
  not just test-suite-clean. Two real bugs found only by live-running it:
  `schema.sql`'s `CREATE INDEX` statements weren't idempotent (fixed to match
  the table's `IF NOT EXISTS`), and a native Windows `postgres.exe` service
  was competing for port 5432 with the Docker container (moved the
  container's mapping to 5433 in both `docker-compose.yml` and
  `application.yaml`). Also caught and fixed a near-miss: the Redis
  dependency swap briefly broke the unrelated `CaffeineRateLimitStore`
  (TAPI-002) — restored, noted in ADR-001.
- **Next Step:** No next-phase task selected yet. `phase-5-redis` fully
  committed (`03bc7bf`) and pushed to both `origin` and `bitbucket`; no PR
  opened/merged yet — that's the one remaining step before this could be
  considered fully shipped. Full context: terra-api TASKS.md → TAPI-011,
  ADR-001 + ADR-007 both amended in Notion with the complete build+verify
  writeup.
- **Blockers:** None
- **Context:** Phase 4 (TAPI-009/010) closed 2026-07-17 before Phase 5
  started same day — full writeup terra-api/DEV_LOG.md → TAPI-009 (concept-
  heavy: Java field-init ordering, volatile-vs-synchronized, Spring's
  separate management-port child context, EnvironmentPostProcessor SPI).
  Machine: `test`, single-nested path (see Machine Paths table).

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
