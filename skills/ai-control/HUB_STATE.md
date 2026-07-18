# Engineering Hub State
<!-- Freshness: 2026-07-17 (rev 6) | v1.3 | Snapshots only — overwritten in place. History lives in DEV_LOGs. -->
<!-- New project? Copy the template from HUB_GUIDE.md → HUB_STATE Section Template. -->

## Terra API                                        <!-- prefix: TAPI -->
- **Status:** Active — primary build
- **Active Task:** TAPI-011 (Phase 5: Redis + Postgres audit migration) — In
  Progress. Built on `phase-5-redis` 2026-07-17: Redis property-driven config
  (ADR-001), Postgres `schema.sql` + `AuditLogRepository` (JdbcTemplate, dual-
  write alongside the JSON audit log), insert moved off the hash-chain lock
  via a bounded `@Async` executor, profile-gated+idempotency-guarded
  `AuditLogBackfillRunner`, `docker-compose.yml` for local Redis+Postgres.
  Caught and fixed a near-miss: the Redis dependency swap briefly broke the
  unrelated `CaffeineRateLimitStore` (TAPI-002) by removing the raw Caffeine
  library entirely — restored, noted in ADR-001.
- **Next Step:** `./gradlew test` green (48/48) and committed locally at
  `f4f8bc4` — **not yet pushed** (brand new branch, no remote tracking yet)
  and not yet verified against a real running Postgres/Redis (only proven:
  app boots and existing behavior is unbroken, not that the new dual-write/
  backfill actually works end-to-end). Full context: terra-api TASKS.md →
  TAPI-011, ADR-001 + ADR-007 both amended in Notion with what's actually
  built vs. still planned.
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
- **Active Task:** THQ-001 — public pages (index.html + products.html) — ⚠️ this
  description looks stale against the repo's own CLAUDE.md (11 pages shipped,
  no products.html listed); not reconciled this session, flagged only.
- **Next Step:** THQ-002 opened 2026-07-17, Planned/notes-only — no code yet.
  New behavior: visualizer cubes color by graduated health tier (ADR-005's
  HEALTHY/YELLOW/ORANGE/RED via Terra API's `ecosystem-health` endpoint)
  instead of today's binary connected/disconnected. Full context + open design
  questions: terra-hq-site TASKS.md → THQ-002 (new file this session — repo had
  no task tracking before). Repo cloned locally this session at
  `C:\Users\test\Desktop\Programing\terra-hq-site` (machine: test) — now
  recorded in HUB.md's Machine Paths table.
- **Blockers:** None
- **Context:** Static on Cloudflare Pages; dark gold/teal system. /internal pages get TAPI Phase 2/3
  JWT protection later — site stays a client of Terra API, never merged into it.

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
