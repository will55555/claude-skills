# Engineering Hub State
<!-- Freshness: 2026-08-02 (rev 39) | v1.3 | Snapshots only — overwritten in place. History lives in DEV_LOGs. -->
<!-- New project? Copy the template from HUB_GUIDE.md → HUB_STATE Section Template. -->

## Terra API                                        <!-- prefix: TAPI -->
- **Status:** Active — prod healthy. TAPI-013 fully closed 2026-08-02: heap caps verified
  actually active (not just committed), CloudWatch alarm + SNS monitoring added, staging
  re-enabled with confirmed real headroom. TFE-201 (same-origin frontend deploy wiring)
  live-verified same day — full Jenkins pipeline green through Deploy to Staging.
- **Active Task:** None blocking. `phase-7-frontend-ci-integration` (TFE-201's Jenkinsfile
  changes) built and deployed successfully but not yet merged to `master`.
- **Next Step:** Merge `phase-7-frontend-ci-integration` → `master` when ready. Confirm the new
  CloudWatch alarm's SNS email subscription was actually clicked (asked, not yet confirmed —
  alarm fires into nothing without it).
- **Blockers:** None.
- **Context:** Jenkins split into 4 jobs (`terra-api-be-main`/`-branches`,
  `terra-api-fe-main`/`-branches`) instead of one flat pipeline; GitHub App scope extended to
  also cover `terra-api-fe`. Still unfixed (reconfirmed live 2026-08-02): missing
  `feature-flags.yaml`, Spring Security default in-memory password at boot, prod/staging
  no-auth-Redis gap. Full detail: `DEV_LOG.md` → TAPI-013.

## terra-api-fe                                     <!-- prefix: TFE -->
- **Status:** Active — Phase 1 (auth shell, TFE-101/102/103) done, merged to `main` 2026-08-02.
  Phase 2 (TFE-201, Jenkins CI + same-origin deploy wiring) done, live-verified same day. The
  lockfile regression (tailwindcss/yaml conflict, then typescript floated to an incompatible
  major) is fully fixed — no longer a blocker, and the stray `package-lock.json;C`/`package.json;C`
  directories are also gone (confirmed absent post-fix).
- **Active Task:** None blocking. Concept AB dashboard UI (accepted 2026-08-01) still not
  started — no longer blocked behind the lockfile fix, since that's resolved now.
- **Next Step:** Repurpose the accepted Concept AB static HTML (`design-reference/`) into real
  JSX components (dashboard shell, product launchpad card, Nkap tier card, activity ledger) — or
  Phase 3 backend work (TFE-301/302/303) if prioritized first.
- **Blockers:** None. **Never run `npm audit fix --force`** here — still downgrades
  `react-scripts` to an empty stub (unrelated to the now-fixed lockfile issue).
- **Context:** New standalone CI-only `Jenkinsfile` added (checkout/build/test, no deploy —
  same-origin means no independent artifact); `docker-compose.dev.yml` service re-enabled.
  ⚠️ Stack drift still unresolved, not re-litigated here: repo runs CRA/react-scripts, not the
  2026-07-16 "stays React (Vite)" decision. Full detail: `DEV_LOG.md` → Phase 2/TFE-201.

## ROMS                                             <!-- prefix: ROMS -->
- **Status:** ⚠️ "Deployed but static" is now DOUBTFUL — **the ROMS EC2 instance may no longer
  exist.** Noticed 2026-07-29: the us-east-1 console listed "Instances (1)", `terra-api-server`
  only, no ROMS box. Deliberately not chased — Will's call to resolve it when ROMS integration
  actually starts, not before. Otherwise unchanged: not being redeployed until needed (call first
  made 2026-07-07, reconfirmed 2026-07-22), effectively maintenance mode.
- **Active Task:** ROMS-001 — first real integration target for Terra API shared services, once live
- **Next Step:** Blocked on Will's decision to actually redeploy ROMS — TAPI-001 (JWT auth) makes the
  eventual integration technically unblocked, but there's no live target to integrate against yet.
  Don't scope integration details further until that trigger fires.
- **Blockers:** ROMS not redeployed — deliberate, no timeline
- **Context:** Spring Boot + React. First potential revenue source, once actually integrated.
  **When ROMS integration does start, check this FIRST** (deferred from 2026-07-29): is the
  instance gone, or just in another region? Cheapest check is EC2 → **AWS Global View**, which
  lists resources across all regions at once — the console was on N. Virginia (us-east-1) when the
  absence was spotted, and a box launched elsewhere simply wouldn't appear. Also worth checking
  EBS **Snapshots** (is there anything to restore from?) and **Elastic IPs** (an unassociated one
  both confirms the box existed and quietly bills). Low stakes either way: the ROMS repo is intact
  locally and on both remotes, so what's potentially lost is the deployment, not the code — and
  ROMS-001 assumes a redeploy regardless.

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
- **EC2 right-sizing back to `t3.micro` (noted 2026-07-29, TAPI):** Resized `t3.micro`→`t3.small`
  (~$7.50→$15/mo) to stop the repeated OOM freezes, explicitly as a stabilizer — Will's call is to
  engineer the footprint back down to `micro` later. Root cause measured, not guessed: the box runs
  BOTH prod and staging stacks (6 containers, per TAPI-012's one-box design), two Spring Boot JVMs
  at ~231MB RSS each, leaving **28Mi available of 911Mi with no swap** — i.e. at capacity while
  idle, before any load. Ranked options to get back to `micro`: (1) **staging on-demand** — biggest
  win, `down` by default and `up` only when a `phase-*` build deploys, reclaims ~250–300MB that two
  idle JVMs hold 24/7 for a tier only used during deploys; (2) **cap JVM heaps** (`-Xmx256m`) —
  nothing bounds them today, each reserves 2.7GB virtual and would grow until the kernel intervenes
  (still true on `small`, just slower); (3) 2GB swapfile — free, removes the OOM cliff, worth doing
  regardless; (4) Alpine JRE base instead of `jammy`, ~20–40MB/container; (5) trim snapd/SSM,
  ~30–50MB. No task ID yet.
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
  **Gap (1) stopped being hypothetical on 2026-07-27:** terra-api prod was down ~40h and surfaced
  only because Will went looking. AWS *knew* — the EC2 instance-status check failed at 03:35
  GMT-4 — there was simply no alarm wired to say so. Concrete fix, ~10 min of console work, first
  actually-warranted piece of this gap: CloudWatch alarm on **`StatusCheckFailed`** for
  `i-044e35066f956d506` (Maximum, 1-min period, threshold ≥1, 2-of-2 datapoints to avoid
  single-blip noise) → SNS topic `terra-api-alerts` → email. **The SNS email subscription must be
  confirmed from the inbox or the alarm fires into nothing.** Worth pairing with a free
  `CPUUtilization > 90% for 15 min` alarm on the same topic, which would catch a thrash spiral
  before a hard freeze (host memory isn't available as a CloudWatch metric without installing the
  agent). Status: walked through 2026-07-29, not yet confirmed created.

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

