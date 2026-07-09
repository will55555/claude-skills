# Engineering Hub State
<!-- Freshness: 2026-07-09 | Snapshots only — overwritten in place. History lives in DEV_LOGs. -->
<!-- New project? Copy the template from HUB_GUIDE.md → HUB_STATE Section Template. -->

## Terra API                                        <!-- prefix: TAPI -->
- **Status:** Active — primary build
- **Active Task:** TAPI-001 — Phase 3 JWT auth implementation
- **Next Step:** Build TokenIssuer → SelfTokenIssuer + TokenValidator seams with versioned claims
- **Blockers:** None
- **Context:** Spring Boot 3.5.1 / Java 21 / Gradle Kotlin. Phase 2 static-key COMPLETE
  (phase-2-auth). Phase 3 branch = resilience + JWT workstreams. Reuse shouldNotFilter bypass
  for /actuator/** and /api/webhooks/** (ApiKeyFilter gotcha).

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
- **Status:** Active — hub deployed, path fix + push pending
- **Active Task:** SKILLS-007 — commit + push path-reference fix (ai-control/ → skills/ai-control/)
- **Next Step:** `sync skills` to commit and push; then SKILLS-005 (CLAUDE.md pointers) and SKILLS-006 (dogfood)
- **Blockers:** None
- **Context:** Hub v1 + satellite edits live at `skills/ai-control/`. dev-log archived. Path refs
  were pointing at wrong location (`ai-control/` vs actual `skills/ai-control/`) — fixed in place
  2026-07-09, not yet committed/pushed. Remaining tasks tracked in `skills/ai-control/TASKS.md`.
