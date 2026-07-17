# Engineering Hub State
<!-- Freshness: 2026-07-15 | v1.3 | Snapshots only — overwritten in place. History lives in DEV_LOGs. -->
<!-- New project? Copy the template from HUB_GUIDE.md → HUB_STATE Section Template. -->

## Terra API                                        <!-- prefix: TAPI -->
- **Status:** Active — primary build
- **Active Task:** None in progress — **Phase 4 (governance) fully closed 2026-07-15:**
  TAPI-002/003/004/006/007/008 Done, TAPI-005 resolved Not Needed (re-evaluated after
  TAPI-002/003/004 shipped; none needed custom exceptions).
- **Next Step:** `phase-4-governance` branch, 14 commits ahead of Phase 3 close, not
  pushed — held until Will decides to push/merge. No next-phase task selected yet;
  candidates are Phase 5 (Redis + PostgreSQL migration, ADR-001/007) or resuming ROMS
  integration testing (JWT auth ready since TAPI-001).
- **Blockers:** None
- **Context:** Phase 4 shipped rate limiting, audit log bus, feature flags, Notion
  removal — plus 2 real bugs found only via live smoke-testing (not caught by
  `MockMvc`): audit log JSON casing (camelCase vs. ADR-007's snake_case schema) and a
  Spring Security `/error` permitAll gap that silently overwrote real HTTP statuses
  with `403` app-wide (TAPI-008, general fix, not heartbeat-specific). Full writeup:
  terra-api/DEV_LOG.md (7 dated entries this session). Machine: `test`, single-nested
  path (see Machine Paths table).

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
- **Active Task:** THQ-001 — public pages (index.html + products.html)
- **Next Step:** Continue building public pages in VS Code
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
