# Engineering Hub State
<!-- Freshness: 2026-07-11 | v1.2 | Snapshots only — overwritten in place. History lives in DEV_LOGs. -->
<!-- New project? Copy the template from HUB_GUIDE.md → HUB_STATE Section Template. -->

## Terra API                                        <!-- prefix: TAPI -->
- **Status:** Active — primary build
- **Active Task:** TAPI-001 Done (2026-07-10) — Phase 3 JWT auth verified end-to-end
  (login → 200 + token → GET /api/dashboard → 200). No active task assigned yet.
- **Next Step:** TAPI-006 (delete superseded `health/HealthIndicator.java` stub) is
  small/standalone, available now. The bigger pick is starting the Phase 4 branch
  (TAPI-002/003/004: rate limit, audit log, feature flags — reassigned from Phase 3
  2026-07-11) with `client/`+`exception/` package realignment (TAPI-005) done JIT as
  part of it, not standalone. None started yet.
- **Blockers:** None
- **Context:** ApiKeyFilter actually deleted 2026-07-11 (previously only de-annotated
  despite docs claiming full deletion — caught and fixed same session). ADR-006/007/008
  reassigned Phase 3 → Phase 4 in Notion (dated amendments, originals preserved); Redis
  formally Phase 5 (was informal `phase-4-redis` branch name). Full writeup:
  terra-api/DEV_LOG.md → Phase Renumbering. New machine in use this session (user
  `test`, single-nested path), now in Machine Paths table.

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
