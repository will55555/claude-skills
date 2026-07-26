# Engineering Hub State
<!-- Freshness: 2026-07-26 (rev 36) | v1.3 | Snapshots only — overwritten in place. History lives in DEV_LOGs. -->
<!-- New project? Copy the template from HUB_GUIDE.md → HUB_STATE Section Template. -->

## Terra API                                        <!-- prefix: TAPI -->
- **Status:** Active — Docker orchestration verified end-to-end 2026-07-26 (3rd session) via a live
  `docker compose --env-file docker.env up --build` run: Postgres/Redis start clean, Hikari
  connects with no auth error, app reaches `Started TerraApiApplication in 95.077 seconds`.
  `include:` confirmed working. TAPI-012/Phase 5 EC2 live-verification (2026-07-20) unaffected.
- **Active Task:** Still no formal TAPI-0XX ID (last is TAPI-012) — flagged three times now, worth
  opening one. Found + fixed a real bug during verification: `terra-api/docker-compose.yml`
  hardcoded Postgres's password, which only worked by coincidence because it matched
  `terra-api/.env`'s `DATASOURCE_PASSWORD` — a future rotation would've silently broken auth. Fixed
  in `docker-compose.yml` (postgres) + `docker-compose.dev.yml` (terra-api-be): both now read
  `${DATASOURCE_USERNAME}`/`${DATASOURCE_PASSWORD}`/`${REDIS_PASSWORD}`/`${TERRA_AUTH_*}` via
  interpolation from `docker.env`, replacing a hardcoded value + a separately-synced `env_file`
  copy. `terra-api/.env` untouched — stays scoped to host-mode (`gradle bootRun`) only, per its
  existing header comment.
- **Next Step:** Commit + push the credential fix (2 files, still uncommitted:
  `terra-api/docker-compose.yml` + `docker-compose.dev.yml`; commit message already drafted this
  session). Then terra-api-fe: `npm install` → uncomment frontend service → full stack verify →
  TFE-101/102/103.
- **Blockers:** None
- **Context:** Two pre-existing issues flagged during verification, not fixed (out of scope):
  missing `feature-flags.yaml` (empty flag set served); Spring Security generated a default
  in-memory password at boot, suggesting `SecurityConfig` may not fully override the default
  `UserDetailsService` — worth checking later. Redis intentionally left unauthenticated (this
  compose file is dev/CI-only, never deployed — prod/staging have their own separate, also-unfixed
  no-auth-Redis gap). `HUB.md`'s Machine Paths table still stale (says `New folder\`, should say
  `terra-api-home\` — hub-improvement candidate, not yet applied). Jenkins webhook auto-trigger
  still unresolved. `terra-api-key.pem` gitignore decision pending.

## terra-api-fe                                     <!-- prefix: TFE -->
- **Status:** Active — Dockerfile now actually present locally (was an unmerged orphan commit as
  of the last sync; corrected 2026-07-26 2nd session).
- **Active Task:** TFE-001 — the `efe1cb1` Dockerfile commit existed on `origin/main` but was never
  pulled locally and predated `phase-1-auth-shell` (the active branch, cut from `main` before
  `efe1cb1`). Fixed: fetched + fast-forwarded local `main` (`41c5ebd`→`efe1cb1`), then merged `main`
  into `phase-1-auth-shell` (clean merge, no conflicts, commit `8f38475`). Dockerfile now on the
  active branch's working tree.
- **Next Step:** Push `8f38475` to `bitbucket/phase-1-auth-shell` (this branch has NO `origin`
  counterpart — GitHub only ever had `main`). Then `npm install` locally, uncomment the frontend
  service in `terra-api/docker-compose.dev.yml`, verify the full stack actually builds (untested).
  Then resume TFE-101/102/103 — login flow + JWT storage/attach against terra-api endpoints.
- **Blockers:** npm dependencies not yet installed locally (docker build will fail until resolved)
- **Context:** CRA (React 19, plain JS — no TypeScript). Dual-remote repo overall, but
  `phase-1-auth-shell` specifically only exists on `bitbucket`, not `origin` — don't assume both
  remotes have every branch. Sibling to terra-api + terra-jenkins under `terra-api-home` (now
  confirmed to be its own git repo, `will55555/terra-api-home`, not a bare folder).

## ROMS                                             <!-- prefix: ROMS -->
- **Status:** Deployed but static — not being redeployed until actually needed (Will's call,
  reconfirmed 2026-07-22; first made 2026-07-07). Effectively maintenance mode in practice, though
  not officially declared as such.
- **Active Task:** ROMS-001 — first real integration target for Terra API shared services, once live
- **Next Step:** Blocked on Will's decision to actually redeploy ROMS — TAPI-001 (JWT auth) makes the
  eventual integration technically unblocked, but there's no live target to integrate against yet.
  Don't scope integration details further until that trigger fires.
- **Blockers:** ROMS not redeployed — deliberate, no timeline
- **Context:** Spring Boot + React. First potential revenue source, once actually integrated.

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
- **"Launch and forget" production-hardening goal (noted 2026-07-20):** End-state goal across
  every deployed service — running reliably without needing to babysit it (Will's own framing:
  "like a site like apple"). Already in place per-service via TAPI-012's pattern: container
  `restart: unless-stopped`, CI/CD auto-deploy on merge, `/actuator/health`-style endpoints.
  Genuinely missing, ecosystem-wide, none built yet: (1) monitoring/alerting — nothing currently
  notifies if a service goes down, has to be noticed manually; (2) automated database backups;
  (3) OS-level security patching automation; (4) domain names + TLS (everything is raw
  IP:port right now — ROMS included, which has had zero domain since its own 2026-05-04 deploy).
  Deliberately not being built now — same "don't build ahead of the actual need" pattern as
  everything else here. No task ID yet.

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

## Yahoo Mail MCP Server                            <!-- prefix: YMCP -->
- **Status:** Active — OAuth persistence fix deployed 2026-07-26, live-verified via Render deploy logs
- **Active Task:** YMCP-002 — reconnect Yahoo Mail MCP connector once in Claude to pick up token under new signing scheme
- **Next Step:** After reconnect, confirm token holds across a natural idle/spin-down period without forcing re-auth
- **Blockers:** None
- **Context:** Repo `willtchouente/yahoo-mail-mcp-server` (fork of `jtokib/yahoo-mail-mcp-server`),
  deployed on Render free tier. Session 1 (2026-06-22, YMCP-001) fixed IMAP-layer instability
  (connection pooling, retry-with-backoff, SSE heartbeat) — necessary but not sufficient, since
  reconnect complaints persisted. Session 2 (2026-07-26) found the actual root cause: OAuth
  `validTokens`/`authCodes` were in-memory Set/Map, wiped every Render spin-down (~15min idle +
  ephemeral filesystem). Fixed by making tokens stateless (HMAC-signed via Node `crypto`, no
  jsonwebtoken dep, 30-day TTL via `ACCESS_TOKEN_TTL_SECONDS`). Added `.github/workflows/keep-alive.yml`
  (10min health ping) as secondary defense against spin-down itself. Full history in repo's own
  `DEV_LOG.md` (Phase 1 + Phase 2). Notion: PAI subproject page `📨 Yahoo Mail MCP Server`.

