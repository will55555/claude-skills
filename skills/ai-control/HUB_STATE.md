# Engineering Hub State
<!-- Freshness: 2026-07-09 | v1.1 | Snapshots only — overwritten in place. History lives in DEV_LOGs. -->
<!-- New project? Copy the template from HUB_GUIDE.md → HUB_STATE Section Template. -->

## Terra API                                        <!-- prefix: TAPI -->
- **Status:** Active — primary build
- **Active Task:** TAPI-001 — Phase 3 JWT auth implementation, mid-implementation
- **Next Step:** Write Java classes: TokenIssuer/TokenValidator interfaces + SigningKeyResolver/
  VerificationKeyResolver seam, SelfTokenIssuer/SelfTokenValidator (JJWT), LoginRequest/Response,
  AuthService, AuthController (POST /api/auth/login), JwtAuthenticationFilter — then rewire
  SecurityConfig (JWT REPLACES ApiKeyFilter, confirmed w/ Will 2026-07-09; ApiKeyFilter code
  stays, just unwired). Staying on phase-3-resilience (no new branch, Will's call).
- **Blockers:** None
- **Context:** Spring Boot 3.5.1 / Java 21 / Gradle Kotlin. Fetched ADR-003 from Notion directly
  (page 37089370-d497-818c-8ff2-dde48c2dc3ec) — confirms self-issued JWT + TokenIssuer/
  TokenValidator/key-resolver seams + versioned claims (iss/sub/exp/tier/scope) so a future
  RemoteTokenIssuer swap is clean. Done: build.gradle.kts (jjwt-api/impl/jackson 0.12.6),
  application.yaml (terra.auth.issuer + terra.auth.login single-service-account block), local
  terra-api CLAUDE.md (Open Blockers/Key Decisions Log/Next Action fixed — was stale, this repo
  clone hadn't picked up the 2026-07-08 resolution). Reuse shouldNotFilter bypass pattern for
  /actuator/**, /api/webhooks/**, and now /api/auth/login too.

## ROMS                                             <!-- prefix: ROMS -->
- **Status:** Deployed
- **Active Task:** ROMS-001 — first real integration target for Terra API shared services
- **Next Step:** Define integration point once TAPI Phase 3 auth is usable
- **Blockers:** Waiting on TAPI-001
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
