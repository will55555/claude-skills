# Engineering Hub State
<!-- Freshness: 2026-07-26 (rev 37) | v1.3 | Snapshots only — overwritten in place. History lives in DEV_LOGs. -->
<!-- New project? Copy the template from HUB_GUIDE.md → HUB_STATE Section Template. -->

## Terra API                                        <!-- prefix: TAPI -->
- **Status:** Active — **prod has been DOWN ~26h** (confirmed, not presumed: EC2 instance-status
  check failed 2026-07-27 03:35 GMT-4 and the box never recovered). Local dev stack, by contrast,
  is verified healthy 2026-07-28: `terra-api-be` + Postgres + Redis all `Up`, app boots in 24.5s,
  `/actuator/health` returns `{"status":"UP"}` from inside the container.
- **Active Task:** Still no formal TAPI-0XX ID (last is TAPI-012) — flagged five times now.
  2026-07-28 session: merged `phase-6-cicd` → `master` (`54efe14`, the step TAPI-012 never
  completed — Jenkinsfile states "merge IS the approval" for prod deploy); merged the two divergent
  `docker.env` copies (this machine was missing `TERRA_AUTH_*`/`REDIS_PASSWORD`, the other laptop's
  copy was missing the Notion keys + Docker networking overrides — now complete and verified, zero
  unset-variable warnings); commented out `terra-api-fe` in dev compose (`1c4adda`) with the
  blocker documented inline.
- **Next Step:** **Diagnose the EC2 box before redeploying anything.** It has now frozen TWICE in
  26h, the second time with Docker STOPPED and nothing running — which rules out the container
  stack, Jenkins, and any deploy loop as the cause. Check `CloudWatch → CPUCreditBalance` first
  (read-only, may answer it outright — a credit-exhausted `t3.micro` throttles to ~5% of a vCPU and
  goes unresponsive while idle, which fits "froze doing nothing" far better than memory does), and
  try **EC2 Serial Console** to reach it *while* frozen rather than restarting and losing the
  evidence again. Only after that: stop→start, `sudo systemctl start docker`, assess inherited
  containers, then deploy.
- **Blockers:** EC2 box unresponsive (port 22 closed as of session end) — needs a stop→start to
  return. Root cause of both freezes still UNKNOWN.
- **Context:** ⚠️ **Two 2026-07-26 claims were disproven 2026-07-28 — do not trust them:** (1) the
  "wrong branch on prod" fix was backwards — `master` was 71 commits BEHIND and lacked
  `docker-compose.prod.yml` entirely; `phase-6-cicd` had the working files. Switching the box to
  `master` moved it onto broken ones. Now moot: the merge landed. (2) "old prod containers presumed
  still running/serving" — false; the box was fully down.
  Jenkins runs LOCALLY (not on EC2), 60s polling, prod deploy auto-gated with no approval step —
  so starting it deploys `master` immediately. Deliberately left un-started this session.
  `terra-api-fe` blocked on a real peer conflict: lockfile records `tailwindcss@3.4.19` (a leftover
  — NOT in `package.json`) needing `yaml@^2.4.2` while `react-scripts@5.0.1` pins `yaml@1.10.3`, so
  `npm ci` refuses it. Fix verified: `rm -rf node_modules package-lock.json && npm install`.
  **Never run `npm audit fix --force` there** — it downgrades `react-scripts` to `0.0.0` (empty
  stub), removing ~1280 packages and the whole build toolchain (hit and reverted this session).
  `terra-api-key.pem` gitignore decision was already resolved (`.gitignore:41` `*.pem`) — HUB_STATE
  was stale. Key now on this machine too, ACL locked to `solan:(R)`.
  `HUB.md`'s Machine Paths table still stale (`New folder\` → should be `terra-api-home\`).
  Still unfixed: missing `feature-flags.yaml`; Spring Security default in-memory password at boot;
  prod/staging no-auth-Redis gap.

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

