# Engineering Hub State
<!-- Freshness: 2026-08-05 (rev 52) | v1.3 | Snapshots only — overwritten in place. History lives in DEV_LOGs. -->
<!-- Last Audit: 2026-08-02 | Monthly Hub Audit (HUB.md) fires from Startup Sequence step 7 when this is >30 days old. Update this line after each audit. -->
<!-- New project? Copy the template from HUB_GUIDE.md → HUB_STATE Section Template. -->

## Terra API                                        <!-- prefix: TAPI -->
- **Reference Links:** (added 2026-08-02 — read these BEFORE designing against the project;
  Prime Directive 3) System Design doc: `https://app.notion.com/p/37089370d497814ab6cdf10732687fee`
  · Terra API Notion project: `https://app.notion.com/p/37789370d49781908780e2b4e7a6c480`
  · ADRs `terra-api-adr-001`–`010`, all accepted, live in Notion (NOT in the repo — grepping the
  codebase for them finds only passing mentions). Local specs that ARE authoritative and often
  missed: `terra-api-fe/TASKS.md` (TFE phase breakdown incl. TFE-401/402/403 visualizer work) and
  `terra-hq-site/CLAUDE.md` lines 39-43 (the two-visualizer architecture — hq-site is the full
  9-cube public ecosystem view, terra-api-fe is scoped to the authenticated customer's own
  entitled products; same `ecosystem-health` endpoint, different filtering. Phase 5 is the shared
  Three.js reference implementation, captured in terra-api-adr-009).
- **Status:** Active — prod healthy. **TAPI-017 fully closed 2026-08-04** — the operator page's
  open ⚠️ (never actually rendered against live data) is resolved: `/internal` confirmed rendering
  live on `solan`, 26 backend tests confirmed green. **Port 8082 (management/actuator) fixed**:
  `application.yaml`'s `management.server.address: localhost` broke when containerized (Docker's
  host port-forward had nothing to connect to — Tomcat bound the container's own loopback only,
  confirmed via `curl` returning "Empty reply from server" despite Tomcat logging it as started).
  Fixed via `${MANAGEMENT_ADDRESS:localhost}` + an env override in `docker-compose.dev.yml` —
  host/`bootRun` default unchanged.
- **Active Task:** **TAPI-020 — SonarQube quality gate in Jenkins CI/CD.** **TAPI-019 closed
  2026-08-05:** the dedicated Jenkins EC2 `i-04ef85c382ac39269` restored the real
  `infra_jenkins_home` data and completed a fresh `master` pipeline green through production
  deploy. The Jenkinsfile deploy target now uses prod's private VPC IP `172.31.21.172`; prod SSH
  permits the Jenkins security group via `sgr-05b94280fb11d357d`. The old local Jenkins was
  confirmed already off. Jenkins remains SSM-only; public access is deferred to TAPI-022.
- **Next Step:** Scope the one-time ecosystem SonarQube baseline and Jenkins quality gate. Sequence
  after TAPI-019: → TAPI-020 (SonarQube) → TAPI-021 (EC2 right-size) → TAPI-022 (domains+TLS) →
  TAPI-023 (OS patching).
- **Blockers:** None. A dedicated `will-cli` IAM identity now exists for local AWS work; narrow its
  AdministratorAccess policy or move to IAM Identity Center as a separate security follow-up.
- **Context:** **Credential incident (2026-08-01):** a Notion API key was committed live in
  terra-api's `.env` since 2026-07-05 and copied into `DEV_LOG.md` 2026-07-26. Rotated by Will;
  scrubbed from git history via two `git-filter-repo` passes, force-pushed, verified clean.
  Pre-scrub backup bundle: `terra-api-home/terra-api-backup-before-history-scrub-2026-08-01.bundle`.
  `terra-api-fe` npm peer-conflict fix verified: `rm -rf node_modules package-lock.json && npm
  install`. Never `npm audit fix --force` there (guts `react-scripts`).
  **2026-08-04: port 8082 fix committed and pushed** (`5b281cc`) — `application.yaml`,
  `docker-compose.dev.yml`, `DEV_LOG.md` all landed on `master`, nothing left uncommitted.

## terra-api-fe                                     <!-- prefix: TFE -->
- **Reference Links:** Local spec (authoritative, verified 2026-08-02):
  `terra-api-fe/TASKS.md` — carries the full TFE phase breakdown, incl. Phase 4 visualizer work
  (TFE-401 repurpose phase5 Three.js · TFE-402 cube filtering per customer against Phase 3's
  entitlement-filtered endpoint · TFE-403 health-tier colors per terra-api-adr-009). Also read
  `terra-hq-site/CLAUDE.md` lines 39-43 for the two-visualizer scope distinction. Notion ADRs:
  see Terra API's Reference Links (shared `terra-api-adr-*` series). Own Notion page: (none
  recorded — add when confirmed).
- **Status:** **TFE-401 substantially reworked 2026-08-04** — the prior "ported into React"
  visualizer (`terraScene.js`, 462 lines, a deliberately reduced dashboard-card variant) was
  replaced with a FULL copy-paste port of `terra-hq-site/terra_api_visualizer_phase5.js` per
  Will's explicit call: the reduced version was not what he wanted, full parity was. Preserves
  starfield, glass/gem materials (confirmed intentional — Will's own reference: "Infinity Stone,
  the blue one in Avengers" — an earlier matte-material pass was reverted), click-to-expand/
  release/collapse state machine, pipeline tubes with shader pulse, mouse repulsion field.
  Feature-complete against ADR-009's Build Sequence but still NOT production-ready (only ever
  run via Docker dev compose / CRA dev server, no real ROMS/PIOS deployment to test against).
- **Active Task:** None open. **3 real bugs found and fixed in the port, 2026-08-04:**
  1. Pipeline tubes visually detached from cubes on screen — phase5's per-frame sine-drift cube
     animation moved cubes but tubes were drawn once, statically. Fixed by dropping the drift
     (also stabilizes click-to-expand, which sets cube position directly).
  2. **Root cause of "some children aren't there" (Will's report, confirmed via screenshot):** 5
     of 8 placeholder child cubes in `domainConfig.js` had the EXACT SAME `name` as their parent
     domain (e.g. domain `Real Estate`, child also named `Real Estate`) — collided in the
     `cubesByName` lookup map, only one of the two meshes was ever reachable. Finance/
     Hospitality/Ventures (children Nkap/ROMS/PIOS) were unaffected — already had distinct
     names, exactly matching what Will observed working vs. not. Fixed via `<Domain> (Planned)`
     suffix on all 5 colliding names — verified all 17 cube names now unique.
  3. Anchor cube never actually turned pink (`0xaa8899`, phase5's own dead-code spec) when
     backend unreachable — `applyHealth`'s reachability check (`statusByServiceId != null`) was
     structurally always true (prop defaults to `{}`, never `null`). Fixed by threading the
     hook's real `error` value through explicitly (`EcosystemVisualizer.js` → `applyHealth`).
  Also fixed: unbuilt-child cubes were functionally invisible (opacity 0.7 + no edge outline
  against dark background) — outlines now stay attached at reduced opacity instead of removed.
  **Added, not restored** (confirmed absent in phase5's own source): idle auto-rotation, stops
  on drag, resumes on double-click — per Will's explicit request, matching hint text that had
  been promising it since an earlier version.
  **Tier colors tuned**, Will's explicit scoped exception to the colors-frozen rule:
  `healthColors.js` `ORANGE` 0xfb923c→0xe8590c (too close to YELLOW at cube scale) and `RED`
  0xf87171→0xdc2626 (read as pink, not red). `HEALTHY`/`YELLOW` untouched.
  **Dev-only test tooling added and KEPT PERMANENTLY** (not scaffolding to delete):
  `useEcosystemHealth.js` + matching `terraScene.js` override — `?mockHealth=1` (ROMS/PIOS only,
  matches production) and `?mockHealthAll=1` (all 8 domains, synthetic statuses spanning all 4
  tiers, for inspecting every cube/child pair in one pass). Opt-in via URL param only; real
  fetch/poll runs unmodified on every normal page load.
- **Next Step:** **Dashboard restyled 2026-08-04** — Montfort Group (mont-fort.com)'s markup
  used as a structural reference, explicitly scoped to layout/spacing only (Will: borrow
  structure, keep Terra's existing palette/type — consistent with colors-frozen rule):
  `.cm-grid` gap 28→40px & max-width 1400→1700px, card padding 26→34px, numbered section index
  badges (01/02/03) added to each card, corner ornaments reshaped from angular low-poly
  triangles to a soft oval/quarter-circle glow at lower opacity (Will: dashboard "looks too much
  like a game" — same complaint a family member gave independently), base font 11→13px,
  smallest labels 8/9px→9/10px, `--text-dim`/`--text-muted` brightened for contrast, light-mode
  `--border-sub` alpha 0.08→0.18 (was invisible against `--surface`). Visualizer card sizing
  tuned separately (`visualizer.css`): aspect-ratio settled at 3/2 with a `max-height: 460px`
  cap (needed once discovered the `/internal` operator page hosts it full-width, unlike the
  customer dashboard's 60/40 split — uncapped aspect-ratio alone produced a ~930px-tall card).
  **terra-hq-site explicitly DEFERRED to a fresh session** (Will's call, given session length):
  same Montfort structural pass (whitespace, numbered sections) PLUS a second pattern Will
  identified from Montfort's markup — in-page anchor-tab navigation with the site's existing
  animated section-reveal system (fade/slide/white-curtain transitions) playing during the jump,
  not an instant `#anchor` snap. 13 standalone HTML files, no shared CSS (each ~900+ lines,
  inline `<style>` blocks) — needs its own session with full context budget. TFE-502/503
  (401 redirect UX, 10/12 modules untested) remain untouched, still open from prior sessions.
- **Blockers:** None. Standing caution unchanged: never run `npm audit fix --force` here.
  **2026-08-04: `package-lock.json` regenerated** via `rm -rf node_modules package-lock.json &&
  npm install` — fixed a `react-router`/`react-router-dom` version mismatch (stale lockfile had
  pulled a v7 `react-router` under a v6 `react-router-dom`) plus a `caniuse-lite` submodule gap
  that broke the Docker build's CSS/PostCSS step. Confirmed fixed via clean container rebuild.
- **Context:** CRA (React 19, plain JS — no TypeScript). Sibling to terra-api + terra-jenkins under
  `terra-api-home`. Docker Compose stack **fixed 2026-08-04**: was scattered across two separate
  compose projects (`terra-api` vs `terra-api-home`) due to a missing explicit `-p` flag on some
  earlier invocations, causing container-name collisions (`redis`/`postgres` "already in use").
  Fixed by always invoking with `-p terra-api-home` explicitly; `terra-jenkins`/
  `infra_jenkins_home` verified untouched throughout every cleanup step. Correct full command
  (run from `terra-api-home/`):
  `docker compose --env-file docker.env -p terra-api-home -f terra-api/docker-compose.yml -f
  terra-api/docker-compose.dev.yml up -d --build`
  **2026-08-04: 8 files uncommitted on `solan`** (all of TFE-401's rework + the dashboard
  restyle — `terraScene.js`, `domainConfig.js`, `healthColors.js`, `EcosystemVisualizer.js`,
  `useEcosystemHealth.js`, `visualizer.css`, `Dashboard.js`, `dashboard.css`, plus the
  regenerated `package-lock.json`). Will's call whether/when to commit.

## ROMS                                             <!-- prefix: ROMS -->
- **Reference Links:** Notion ADRs `roms-adr-001`–`005` (domain-prefixed, per the 2026-07-18
  terra-hq-site refactor) — URLs not recorded, add when confirmed. Repo lives OUTSIDE
  `terra-api-home`: `SDE/restaurant-order-management-system/`. Strategy page:
  `terra-hq-site/roms_gtm_strategy.html`.
- **Status:** ⚠️ "Deployed but static" is now DOUBTFUL — **the ROMS EC2 instance may no longer
  exist.** Noticed 2026-07-29: the us-east-1 console listed "Instances (1)", `terra-api-server`
  only, no ROMS box. Deliberately not chased — Will's call to resolve it when ROMS integration
  actually starts, not before. Otherwise unchanged: not being redeployed until needed (call first
  made 2026-07-07, reconfirmed 2026-07-22), effectively maintenance mode.
- **Active Task:** ROMS-001 — first real integration target for Terra API shared services, once live
- **Queued for later sync / Notion:**
  - ROMS-001 — expand into a concrete deploy-and-heartbeat checklist: check old ROMS EC2/EIP/snapshots, provision a new EC2, deploy ROMS and confirm its health endpoint, configure heartbeats to Terra API, verify `/api/v1/ecosystem/public-health`, and confirm the public visualizer shifts ROMS to its live health tier.
  - ROMS-002 — migrate ROMS Jenkins to the shared Terra Jenkins EC2 before redeploying ROMS: back up the ROMS Jenkins volume, inventory jobs/plugins/credentials, import jobs without overwriting `JENKINS_HOME`, recreate or migrate credentials, run a green ROMS pipeline, then retire the old ROMS Jenkins.
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
- **Reference Links:** Notion ADRs `pios-adr-011`–`015` (ADR-013 = the gating event-schema-
  versioning decision) — URLs not recorded, add when confirmed. Strategy page:
  `terra-hq-site/pios_strategy.html` (architecture, event model, capital governance).
- **Status:** Design phase — no coding until ADR-013 resolves
- **Active Task:** PIOS-001 — resolve ADR-013 (event schema versioning)
- **Next Step:** Draft ADR-013 options + tradeoffs
- **Blockers:** ADR-013 is the gating decision; ADRs 012–014 pending
- **Context:** Event-sourced. FastAPI/Python reserved. Rules-engine-gated AI signals.

## terra-hq-site                                    <!-- prefix: THQ -->
- **Reference Links:** Local specs (authoritative, verified 2026-08-02):
  `terra-hq-site/CLAUDE.md` — page inventory + the two-visualizer architecture (lines 39-43) ·
  `terra-hq-site/TASKS.md` (THQ-001/002) · `terra-hq-site/devlog.md`. Live visualizer:
  `terra_api_visualizer_phase5.js` at the repo ROOT (1,556 lines — phases 1–4 are superseded and
  sit in `archive/`; don't port from those). Notion: (none recorded — add when confirmed).
- **Status:** Active — parallel track
- **Active Task:** None open. **Montfort structural pass shipped 2026-08-04** (`e0699aa`,
  committed and pushed): numbered section-index badges + a choreographed reveal system
  (IntersectionObserver scroll-reveal on single-scroll pages, tab-panel fade-in via double-rAF
  on tab-driven pages) ported across 11 of 13 pages — structure/spacing/animation only, zero
  color values touched anywhere (verified via diff scan across the whole commit). index.html
  built first as proof-of-concept, Will reviewed it in-browser and approved before the other 10
  ran. `home-hub.html` (iframe launcher) and `terra_api_visualizer_phase5.html` (WebGL canvas,
  no text sections) deliberately excluded — neither has content this pattern applies to.
  `terra_enterprise.html` got a lighter treatment (click-to-drill panel fade-in only, no badges
  — a tree diagram doesn't want a second numbering system). Design reference is
  `https://mont-fort.com/` itself, not just its markup — Will's framing: "final product will be
  similar," treat as the standing visual north star for future terra-hq-site work, not a one-off
  (tracked in Claude memory as `reference_montfort-design`). **THQ-002 shipped** (`bf8d54c`,
  2026-08-03): public visualizer now polls Terra API's `GET /api/v1/ecosystem/public-health`
  (TAPI-014) once per tick and colors ROMS/PIOS by real HEALTHY/YELLOW/ORANGE/RED tier,
  replacing the old binary connected/disconnected model against hardcoded per-domain ports.
  Design question resolved: single ecosystem-health poll, not per-cube. Domain cubes with no
  reporting service render as a distinct "unbuilt" navy, separate from "off."
- **Next Step:** **THQ-003, found 2026-08-04, uncommitted**: live-testing THQ-002 against a real
  ROMS heartbeat surfaced that pipeline extension tubes (created on cube expand-click) freeze
  their connected state at creation time and never refresh — `createPipelineExtension()` used
  `tube.userData.cube` (singular), which `updateCubeConnection()`'s live-refresh loop doesn't
  recognize (only `cube1`/`cube2`, the main radial tubes' naming). Candidate fix drafted
  (syntax-checked, NOT visually confirmed) — touches only tube wiring, zero color values, per
  Will's explicit constraint. **Deliberately left uncommitted, local to the `test` machine only**
  — resume there specifically (not a fresh-clone situation) to verify + commit. Full repro steps
  in `terra-hq-site/TASKS.md` → THQ-003. `local-test-proxy.js` (added alongside THQ-002) is the
  same-origin dev proxy used for this testing — may still be running on port 5500 on `test`.
- **Blockers:** None
- **Context:** 2026-07-18 session completed: (1) Clarified dual-visualizer architecture (terra-hq-site
  public + terra-api-fe scoped both read from Terra API ecosystem-health endpoint — single source
  of truth); (2) Refactored terra_api_strategy.html (removed 430 lines embedded WebGL, added
  domain-prefixed ADRs terra-api-adr-001–010, linked to build phases); (3) Fixed product pages
  (ROMS/PIOS using domain-prefixed ADRs roms-adr-001–005, pios-adr-011–015); (4) Cleaned up Notion
  CI/CD pages (renamed ADR-009→terra-api-adr-010, updated status/references). All changes staged for
  commit. CLAUDE.md, TASKS.md, terra_api_strategy.html modified locally; ready to commit.

## DSA Practice                                     <!-- prefix: DSA -->
- **Reference Links:** Method lives in the hub, not a project doc: HUB_GUIDE → DSA Methodology
  (3-phase flow). Obsidian vault notes under `Learn/Software Development/`. Notion: (none
  recorded — add when confirmed).
- **Status:** Active — recurring
- **Active Task:** DSA-001 — Arrays (start of progression)
- **Next Step:** First Arrays problem via 3-phase methodology
- **Blockers:** None
- **Context:** Java default. Arrays → Strings → Linked Lists → Trees → Graphs → DP.

## Cross-Project Notes                              <!-- no prefix — ecosystem-wide, not project-scoped -->
- **EC2 right-sizing back to `t3.micro` (noted 2026-07-29, TAPI) — now `TAPI-021`, scope
  corrected 2026-08-03:** Resized `t3.micro`→`t3.small` (~$7.50→$15/mo) to stop repeated OOM
  freezes, explicitly as a stabilizer — Will's call is to engineer the footprint back down later.
  Root cause measured, not guessed: the box runs BOTH prod and staging stacks (6 containers, per
  TAPI-012's one-box design), two Spring Boot JVMs at ~231MB RSS each, leaving **28Mi available of
  911Mi with no swap** at the time — at capacity while idle, before any load. Of the original 5
  ranked options, **two are already DONE via TAPI-013** (2026-08-02): JVM heap caps
  (`MaxRAMPercentage=50`, verified actually active, not just committed) and a 2GB swapfile
  (`/etc/fstab`-persisted). Remaining, tracked as TAPI-021: (1) staging on-demand — biggest
  remaining win, `down` by default and `up` only when a `phase-*` build deploys, reclaims
  ~250–300MB two idle JVMs hold 24/7 for a tier only used during deploys; (2) Alpine JRE base
  instead of `jammy`, ~20–40MB/container; (3) trim snapd/SSM, ~30–50MB.
- **SonarQube gate (noted 2026-07-18) — now `TAPI-020`:** Ecosystem-wide code-quality pass planned
  across all projects, once, before full deployment — not a per-project or per-PR blocker. Intent:
  keep developing/adding functionality now, run it later, wired into Jenkins once TAPI-019 gives
  it a real home (sequenced after, to avoid reconfiguring the integration post-move).
- **"Launch and forget" production-hardening goal (noted 2026-07-20):** End-state goal across
  every deployed service — running reliably without needing to babysit it (Will's own framing:
  "like a site like apple"). Already in place per-service via TAPI-012's pattern: container
  `restart: unless-stopped`, CI/CD auto-deploy on merge, `/actuator/health`-style endpoints; (1)
  monitoring/alerting done 2026-08-02 (CloudWatch alarm + confirmed SNS subscription, see Terra
  API section). Remaining, now task-ID'd 2026-08-03: (2) automated database backups — `TAPI-018`;
  (3) OS-level security patching automation — `TAPI-023`; (4) domain names + TLS (everything is
  raw IP:port right now — ROMS included, zero domain since its 2026-05-04 deploy) — `TAPI-022`.
  Jenkins getting its own EC2 box (ADR-010) is also now tracked — `TAPI-019`. Full sequencing
  rationale in `terra-api/TASKS.md`.
  **Gap (1) stopped being hypothetical on 2026-07-27:** terra-api prod was down ~40h and surfaced
  only because Will went looking. AWS *knew* — the EC2 instance-status check failed at 03:35
  GMT-4 — there was simply no alarm wired to say so. Concrete fix, ~10 min of console work, first
  actually-warranted piece of this gap: CloudWatch alarm on **`StatusCheckFailed`** for
  `i-044e35066f956d506` (Maximum, 1-min period, threshold ≥1, 2-of-2 datapoints to avoid
  single-blip noise) → SNS topic `terra-api-alerts` → email. Worth pairing with a free
  `CPUUtilization > 90% for 15 min` alarm on the same topic, which would catch a thrash spiral
  before a hard freeze (host memory isn't available as a CloudWatch metric without installing the
  agent). **Status: FULLY DONE** — alarm + SNS topic created under TAPI-013 (`dcf7d6a`,
  2026-08-02); **email subscription link clicked by Will 2026-08-02**, confirmed with him
  2026-08-03 — the alarm can actually fire into an inbox now, not just exist. This is the first
  piece of gap (1) actually built; the rest (DB backups, OS patching, domains + TLS) remains
  deferred.

## claude-skills                                    <!-- prefix: SKILLS -->
- **Reference Links:** Self-documenting — the hub IS this project's spec: `HUB.md` (rules,
  Prime Directives first), `HUB_GUIDE.md` (templates/protocols/New Machine Setup), this file.
  Change history: claude-skills ROOT `DEV_LOG.md` (one shared log — ai-control does NOT get a
  nested one, per the Hub Update Gate). Git is sole source of truth here; Notion is an
  informational dupe only, never authoritative on conflict.
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
- **Reference Links:** Repo `willtchouente/yahoo-mail-mcp-server` (fork of
  `jtokib/yahoo-mail-mcp-server`), local at `SDE/yahoo-mail-mcp-server/` — OUTSIDE
  `terra-api-home`. Full history in that repo's own `DEV_LOG.md` (Phase 1 + Phase 2). Notion:
  PAI subproject page `📨 Yahoo Mail MCP Server` — URL not recorded, add when confirmed.
  Note: this container holds host port 3000 locally, which is why terra-api-fe moved to 3001.
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

