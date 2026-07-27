# Engineering Hub State
<!-- Freshness: 2026-07-26 (rev 37) | v1.3 | Snapshots only — overwritten in place. History lives in DEV_LOGs. -->
<!-- New project? Copy the template from HUB_GUIDE.md → HUB_STATE Section Template. -->

## Terra API                                        <!-- prefix: TAPI -->
- **Status:** Active — Local Docker orchestration verified end-to-end 2026-07-26 (3rd session), but
  **found a real production bug while pushing that fix live**: `~/terra-api-prod` on the EC2 box
  was checked out on `phase-6-cicd`, not `master` — every prior "Deploy to Prod" run had silently
  deployed the wrong branch. Fixed (`git checkout master && git pull`, box now correctly on
  `master`), but the actual deploy is **still incomplete** — session ended mid-retry. Full
  root-cause writeup in `terra-api/DEV_LOG.md`. Notion project page + `terra-api/CLAUDE.md` both
  updated to match.
- **Active Task:** Still no formal TAPI-0XX ID (last is TAPI-012) — flagged four times now, worth
  opening one. This session: fixed the Postgres/Redis credential-duplication bug (docker.env now
  the single source of truth for containerized runs), wired terra-api-fe into the local dev
  compose stack, fixed a terra-api-fe Dockerfile bug (redundant runtime-stage `npm install`,
  doubled build time/network exposure), found + fixed the prod wrong-branch bug above, hard-rebooted
  the EC2 box after a deploy hung it unresponsive for ~50 min. All code committed + pushed to both
  `origin` and `bitbucket`: `terra-api` @ `bc3df10`, `terra-api-fe` @ `4ee36c4`.
- **Next Step:** **On the EC2 box** (`ssh -i terra-api/terra-api-key.pem ubuntu@100.60.61.209`,
  already confirmed on `master`): retry the interrupted deploy —
  `docker-compose-v2 -p terra-api-prod -f docker-compose.prod.yml pull/down/up -d` (last attempt
  stalled on a redis image layer, network flakiness, not a config problem — check
  `ps aux | grep docker` first for a stray process from the killed session before retrying). Also
  re-trigger the `phase-6-cicd` "Deploy to Staging" job — it was killed by the same EC2 reboot.
  After both are confirmed up: terra-api-fe local full-stack rebuild (Dockerfile fix applied, not
  yet re-verified clean) → resume TFE-101/102/103.
- **Blockers:** Prod deploy incomplete as of session end (see Next Step) — old prod containers are
  presumed still running/serving (deploy never reached `down`), but not yet confirmed on this sync.
- **Context:** Jenkins multibranch pipeline audited this session (read the job's `config.xml`
  directly): already does what was asked — all branches auto-trigger CI, only `master`/`phase-*`
  push/deploy. Uses 60s polling, not a webhook (can't switch yet — Jenkins runs locally, not on a
  publicly reachable server; matches the repo's own documented future-migration plan). Two
  pre-existing issues flagged, not fixed: missing `feature-flags.yaml`; Spring Security generated a
  default in-memory password at boot (`SecurityConfig` may not fully override the default
  `UserDetailsService`). Redis intentionally left unauthenticated on the local/CI compose file
  (never deployed) — prod/staging have their own separate, still-unfixed no-auth-Redis gap.
  `HUB.md`'s Machine Paths table still stale (`New folder\` → should be `terra-api-home\`).
  `terra-api-key.pem` gitignore decision pending.

## terra-api-fe                                     <!-- prefix: TFE -->
- **Status:** Active — Dockerfile fixed and stack-integrated 2026-07-26 (3rd session): `npm install`
  run (regenerated `package-lock.json`, was missing `react-router-dom`), a real Dockerfile bug
  fixed (redundant runtime-stage `npm install`, was doubling build time), and the service wired
  into `terra-api/docker-compose.dev.yml` (key renamed `frontend` → `terra-api-fe`).
- **Active Task:** All local changes committed + pushed to **both** `origin` and `bitbucket` @
  `4ee36c4` — correction to the prior entry below: `origin` does in fact have
  `phase-1-auth-shell` now (was stale info), not bitbucket-only.
- **Next Step:** Re-run the full local stack build (`docker compose --env-file docker.env up
  --build` from `terra-api-home/`) to confirm terra-api-fe's image now builds clean end-to-end —
  last attempt progressed further after the Dockerfile fix but wasn't confirmed complete before
  the session ended (attention was on the terra-api prod-deploy incident, see TAPI). Then resume
  TFE-101/102/103 — login flow + JWT storage/attach against terra-api endpoints.
- **Blockers:** None
- **Context:** CRA (React 19, plain JS — no TypeScript). Sibling to terra-api + terra-jenkins under
  `terra-api-home` (its own git repo, `will55555/terra-api-home`, not a bare folder).

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

