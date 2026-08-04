# Engineering Hub State
<!-- Freshness: 2026-08-04 (rev 48) | v1.3 | Snapshots only — overwritten in place. History lives in DEV_LOGs. -->
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
- **Status:** Active — prod healthy. **TAPI-013 fully closed** 2026-08-02 (`dcf7d6a`): heap caps
  verified genuinely active, CloudWatch alarm + SNS added, staging re-enabled with real headroom.
  **`phase-8-customer-identity` (ADR-003 Tier 1) and `phase-7-frontend-ci-integration` (TFE-201)
  both merged to `master` 2026-08-02** — confirmed via `git log`/`git merge-base` 2026-08-03, this
  hub's prior "pending" language was stale. **TAPI-015 shipped direct to `master`** (`ef6aa96`,
  2026-08-02): `OperatorAccess`, ADR-012's operator authorization gate, built proactively — closes
  a real gap before any endpoint uses it (role=internal alone would've let the ROMS service
  account read cross-customer operator data; now requires role=internal AND an explicit
  `ops:read` scope no service account has). Nothing calls it yet. **`master` (incl. TAPI-014)
  deployed to prod 2026-08-03** — confirmed live, not just assumed: `GET
  /api/v1/ecosystem/public-health` (an endpoint that did not exist before TAPI-014) returns `200`
  with the correct `PublicEcosystemHealthResponse` shape (`services: []`, `ecosystem_status:
  "healthy"`) from the public EC2 box. Empty `services` is expected — neither ROMS nor PIOS is
  deployed/reporting heartbeats yet.
- **Active Task:** None open. **TAPI-014 merged to `master`** (`81d4d7e`, 2026-08-03, pushed both
  remotes) — `GET /api/v1/ecosystem/public-health`, genuinely public/unauthenticated, for
  terra-hq-site's public visualizer (ADR-005's 2026-08-03 amendment). Consumer side confirmed
  working, not just assumed: terra-hq-site's `terra_api_visualizer_phase5.js` (THQ-002, `bf8d54c`)
  polls this exact endpoint, and the shape lines up field-for-field —
  `PublicEcosystemHealthResponse.services[].service_id`/`running`/`tier` against the visualizer's
  `SERVICE_ID_BY_CUBE_NAME`/`TIER_COLORS`, and `QuarantineTier`'s `HEALTHY`/`YELLOW`/`ORANGE`/`RED`
  against the visualizer's tier-color keys, verified by reading both sides rather than trusting
  the naming. No unmerged branches remain on either repo.
- **Next Step:** **TAPI-016, TFE-501, and TAPI-018 all done and live-verified 2026-08-03.**
  TAPI-018 (Postgres backup automation, whole `terra` DB): S3 bucket + 30-day lifecycle rule,
  IAM instance-profile role scoped to `s3:PutObject`+`sns:Publish` only (no `ListBucket`,
  deliberately minimized), failure alerts reuse TAPI-013's existing SNS topic
  (`terra-api-prod-alerts` — resolved the prior naming discrepancy). 5 manual test backups
  confirmed landed in S3; cron installed for daily 3am UTC runs, confirmed via `crontab -l`.
  Real bug found+fixed along the way: an apostrophe inside a `${VAR:?message}` breaks bash's
  parser even inside double quotes — confirmed via isolated repro.
  **TAPI-017 and TAPI-019 both stalled 2026-08-04, both resuming on `solan`:** TAPI-017 (ADR-012
  operator endpoints) needs the actual ADR-012 spec, which lives in Notion — the MCP connection
  was down all session despite looking fine at the account/connector level (didn't propagate into
  an already-running session; needs a fresh session, which `solan` will be). TAPI-019 (Jenkins →
  own EC2 box): researched (`terra-jenkins/docker-compose.jenkins.yml`'s own header already
  documents the migration steps) and prepared full CloudShell provisioning commands
  (`t3.medium`/30GB, sized up front to avoid TAPI-013's OOM history) — NOT yet run. Found the real
  blocker: `jenkins_home` is a named Docker volume (`infra_jenkins_home`) holding every actual job
  config, credential (`server-ssh`, `dockerhub-credentials`, GitHub App key), and plugin — it lives
  on `solan`, unreachable from a `test`-machine session. A session can provision a new box and get
  Jenkins *running* there, but the real data migration needs hands actually on `solan`. Full
  detail + prepared commands in `terra-api/TASKS.md` → TAPI-019.
  Remaining sequence, unchanged: TAPI-017 → TAPI-019 → TAPI-020 (SonarQube gate, after Jenkins's
  box is final) → TAPI-021 (EC2 right-size toward `t3.micro` — corrected scope, heap caps +
  swapfile already done via TAPI-013) → TAPI-022 (domains + TLS, last) → TAPI-023 (OS patching
  automation, last, covers Jenkins's new box too). ADR-003 Tier 2 (Google sign-in) deliberately
  NOT sequenced — stays deferred until a customer wants it.
- **Blockers:** None. Phase 3 went straight to `master` without a branch, contrary to convention
  — corrected via `phase-8-customer-identity`. Jenkins split into 4 jobs
  (`terra-api-be`/`terra-api-fe` × `main`/`branches`) instead of one flat pipeline, GitHub App
  scope extended to cover `terra-api-fe` too — factual state, not a problem. Formerly-loose items
  (env-file verification, missing `feature-flags.yaml`, default Spring Security password,
  Redis no-auth) now tracked as TAPI-016, see Next Step.
- **Context:** **Credential incident (2026-08-01):** a Notion API key was committed live in
  terra-api's `.env` since 2026-07-05 and copied into `DEV_LOG.md` 2026-07-26. Rotated by Will;
  scrubbed from git history via two `git-filter-repo` passes (2nd pass needed for a 1-char-shorter
  historic variant the 1st missed), force-pushed to `origin`+`bitbucket`, verified clean via full
  local (incl. unreachable loose objects) + remote history scans. Pre-scrub backup bundle:
  `terra-api-home/terra-api-backup-before-history-scrub-2026-08-01.bundle`.
  Jenkins on the `solan` machine (port 8090) until TAPI-019 migrates it to its own EC2 box.
  `terra-api-fe` npm peer-conflict fix verified: `rm -rf node_modules package-lock.json && npm
  install`. Never `npm audit fix --force` there (guts `react-scripts`).

## terra-api-fe                                     <!-- prefix: TFE -->
- **Reference Links:** Local spec (authoritative, verified 2026-08-02):
  `terra-api-fe/TASKS.md` — carries the full TFE phase breakdown, incl. Phase 4 visualizer work
  (TFE-401 repurpose phase5 Three.js · TFE-402 cube filtering per customer against Phase 3's
  entitlement-filtered endpoint · TFE-403 health-tier colors per terra-api-adr-009). Also read
  `terra-hq-site/CLAUDE.md` lines 39-43 for the two-visualizer scope distinction. Notion ADRs:
  see Terra API's Reference Links (shared `terra-api-adr-*` series). Own Notion page: (none
  recorded — add when confirmed).
- **Status:** **ALL 13 TFE TASKS CLOSED 2026-08-02** — feature-complete against ADR-009's Build
  Sequence, but NOT production-ready, and the distinction matters: it has only ever run on CRA's
  dev server. See Next Step.
- **Active Task:** None open. Phase 4 shipped and merged to `main` (`d1a13a4`): the visualizer
  ported from phase5 into React (`terraScene.js` — real disposal, drag-to-rotate, raycast hover),
  the Command Matrix dashboard, tier accent theming, faceted gold corners, light mode. TFE-301/302/
  303 (backend entitlement + `role` claim) also closed — they shipped as terra-api work but were
  tracked here.
  **`domainConfig.js` is now a MIRROR of terra-hq-site's phase5 `CUBE_CONFIG`**, not a
  re-derived taxonomy — an earlier hand-written version had already drifted (hq-site named
  Nkap/ROMS/PIOS as children while this had six domains `service: null`). If phase5 changes, this
  follows. Only addition is `serviceId`, which phase5 has no concept of.
- **Next Step:** **TFE-501 done and live-verified 2026-08-03** — `terra-api`'s `SecurityPaths`
  flipped from an allow-list (couldn't cover arbitrary React Router paths) to protecting
  `/api/**` by default; `GET /` now returns `200` (was `401`), public/protected endpoints
  unaffected. TFE-502/503 remain (Phase 5, `terra-api-fe/TASKS.md`): TFE-502 — a 401 leaves the
  user on a broken page instead of redirecting to login (hit twice 2026-08-02); TFE-503 — 10 of
  12 modules have no tests (only `healthColors`/`domainConfig` covered, 18 tests). Also note the
  dashboard is feature-complete for a customer base that does not exist yet: ADR-011's amendment
  established
  there is no real customer identity, so `cust_dev_001` is a dev fixture — deliberate sequencing,
  not urgency. Deferred by Will 2026-08-02: the ADR-012 admin dashboard.
  **Found 2026-08-03:** Jenkins' `phase-4-visualizer` branch job failing `npm ci` (lockfile missing
  `yaml@2.9.0`) on a run from ~3.5h prior. No local checkout of that branch remains (remote-only),
  and its work already shipped via the `d1a13a4` merge to `main` — confirmed isolated (Will:
  "everything else passing in pipeline"), so this is a stale multibranch CI check against a
  now-superseded branch, not a live problem. **Deleted from both `origin` and `bitbucket`
  2026-08-03** (confirmed fully merged into `main` first via `git merge-base --is-ancestor`) —
  recurring false-alarm build stopped.
  (superseded) Confirm the FE image builds clean end-to-end via `docker compose --env-file
  docker.env up --build` from `terra-api-home/` — this has never actually been verified green, only
  the CI-side `npm ci`/build. Then start repurposing the `design-reference/` static HTML into real
  JSX components (dashboard shell, product launchpad card, Nkap tier card, activity ledger).
- **Blockers:** None. Standing caution: **never run `npm audit fix --force`** here — it downgrades
  `react-scripts` to `0.0.0` (empty stub), stripping ~1280 packages and the whole build toolchain
  (hit and reverted 2026-07-28). Stray `package-lock.json;C` / `package.json;C` directories
  (previously flagged as unexamined) — **confirmed gone 2026-08-02**, no longer an item.
- **Context:** CRA (React 19, plain JS — no TypeScript). Sibling to terra-api + terra-jenkins under
  `terra-api-home` (its own git repo, `will55555/terra-api-home`, dual remote: GitHub + Bitbucket
  `terra-inc-dev/terra-api-fe`). ⚠️ Stack drift flagged 2026-08-01: the 2026-07-16 decision says
  "stays React (Vite)" but the actual repo runs CRA/react-scripts, not Vite — unresolved, not
  re-litigated here. A standalone CI-only `Jenkinsfile` (checkout/`npm ci`/build/test, no deploy)
  was added to this repo 2026-08-02 for independent CI feedback — verify it's still present after
  this session's merge, since the Phase 4 work landed around the same time. Concept AB's static
  HTML reference (`design-reference/terra_dashboard_state_a/b.html`, `terra_nkap_tiers.html`,
  accepted 2026-08-01) has now been superseded by Phase 4's real shipped JSX components
  (`Dashboard.js`, `NkapCard.js`, `ProductLaunchpad.js`, `TierCorners.js`) — the reference files
  can likely be deleted once someone confirms the real components fully replace them.

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
- **Active Task:** None open. **THQ-002 shipped** (`bf8d54c`, 2026-08-03): public visualizer now
  polls Terra API's `GET /api/v1/ecosystem/public-health` (TAPI-014) once per tick and colors
  ROMS/PIOS by real HEALTHY/YELLOW/ORANGE/RED tier, replacing the old binary connected/
  disconnected model against hardcoded per-domain ports. Design question resolved: single
  ecosystem-health poll, not per-cube. Domain cubes with no reporting service render as a
  distinct "unbuilt" navy, separate from "off."
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

