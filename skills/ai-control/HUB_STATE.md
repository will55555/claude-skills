# Engineering Hub State
<!-- Freshness: 2026-07-17 (rev 4) | v1.3 | Snapshots only — overwritten in place. History lives in DEV_LOGs. -->
<!-- New project? Copy the template from HUB_GUIDE.md → HUB_STATE Section Template. -->

## Terra API                                        <!-- prefix: TAPI -->
- **Status:** Active — primary build
- **Active Task:** None in progress — **TAPI-009 (post-Phase-4 codebase audit) +
  TAPI-010 (runtime/build performance pass) both closed 2026-07-17:** full
  file-by-file correctness pass across all 7 `src/main/java` packages, followed by a
  throughput/build/startup pass. `./gradlew test` green after all fixes both times.
- **Next Step:** TAPI-011 (Phase 5: Redis + Postgres audit migration) opened
  2026-07-17, Planned/notes-only — no code yet. Both ADR triggers look unmet
  (dashboard deleted so Redis's ">10 concurrent users" gate is moot; Postgres
  audit migration's "query/reporting need" hasn't materialized) but Will's call
  is to build it anyway as forward-looking prep. Full context: terra-api
  TASKS.md → TAPI-011. Also still open: no real build/startup timing numbers
  taken yet (TAPI-010 flagged this).
- **Blockers:** None
- **Context:** TAPI-009 real fixes: `CacheConfig`/`EnvConfig` replaced with
  property-driven config (`spring.cache.*` YAML, `DotenvEnvironmentPostProcessor`);
  `TerraAuthProperties`/`QuarantinePolicyProperties` now `@Validated` (was 5 scattered
  `@Value` injections / 8 redundant Java defaults); new `SecurityPaths` consolidates a
  bypass-path list that had already drifted twice; `QuarantineService` per-record
  updates now `synchronized` (volatile fields don't compose atomically across
  `recordHeartbeat`'s request threads and the scheduled missed-heartbeat check);
  `Heartbeat.status` now `@Pattern`-validated (was failing open to HEALTHY on any
  unrecognized value); dead `EventBusController` + unused webflux/reactor-test
  removed. Also fixed 2 pre-existing bugs (401-vs-403, `actuator/health` 404-via-
  MockMvc) surfaced by a live test run, both already flagged in the TAPI-007 commit
  message but never fixed until now. Full writeup: terra-api/DEV_LOG.md → TAPI-009
  (concept-heavy — Java field-init ordering, volatile-vs-synchronized, Spring's
  separate management-port child context, EnvironmentPostProcessor SPI). Machine:
  `test`, single-nested path (see Machine Paths table).

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
