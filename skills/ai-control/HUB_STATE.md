# Engineering Hub State
<!-- Freshness: 2026-08-23 (rev 70) | v1.3 | Snapshots only — overwritten in place. History lives in DEV_LOGs. -->
<!-- Last Audit: 2026-08-02 | Monthly Hub Audit (HUB.md) fires from Startup Sequence step 7 when this is >30 days old. Update this line after each audit. -->
<!-- New project? Copy the template from HUB_GUIDE.md → HUB_STATE Section Template. -->

## Terra API                                        <!-- prefix: TAPI -->
- **Machine Reference (added 2026-08-08, port corrected same day):** `terra-api-server`
  (`i-044e35066f956d506`, us-east-1) — private IP `172.31.21.172:8080`, public IP
  `100.60.61.209:8080` (**port moved 8081→8080 2026-08-08**, security group has both open during
  transition, 8081 not yet removed). **Real HTTPS now live: `https://api.terra-hq.com`** —
  Cloudflare-proxied (Flexible SSL/TLS mode) + an Origin Rule rewriting destination port to 8080
  (required: Cloudflare's free tier only proxies to a fixed origin-port allowlist, 8081 wasn't on
  it). This is TAPI-022's actual scope (domains + TLS) becoming real for the first time, though
  only this one public endpoint has been verified through the HTTPS path so far — not a full
  TAPI-022 close.
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
- **Status:** Active — prod healthy. **TAPI-020 (SonarQube quality gate) fully closed 2026-08-07:**
  `jacoco` plugin added, `sonar-token` Jenkins credential created, SonarCloud Automatic Analysis
  disabled (was conflicting with CI-based analysis), GitHub webhook wired — full pipeline green on
  every push to `master`. **Jenkins given public IP access 2026-08-07** (Elastic IP `3.211.62.86` +
  security group `sg-0a811821f4b2739bf` opened on 8090, no longer SSM-only) — but this is NOT
  TAPI-022 closing: **TAPI-022's real scope is domains + TLS** (everything, ROMS included, is still
  raw IP:port), corrected 2026-08-07 after being wrongly marked closed earlier the same session.
  **TAPI-017 fully closed 2026-08-04** — the operator page's open ⚠️ (never actually rendered
  against live data) is resolved: `/internal` confirmed rendering live on `solan`, 26 backend tests
  confirmed green. **Port 8082 (management/actuator) fixed**: `application.yaml`'s
  `management.server.address: localhost` broke when containerized (Docker's host port-forward had
  nothing to connect to — Tomcat bound the container's own loopback only, confirmed via `curl`
  returning "Empty reply from server" despite Tomcat logging it as started). Fixed via
  `${MANAGEMENT_ADDRESS:localhost}` + an env override in `docker-compose.dev.yml` — host/`bootRun`
  default unchanged. **New ADR-013 (Customer Identity & Login Strategy) created 2026-08-07** —
  Proposed, unscheduled; resolves ADR-011's open question (new ADR, not an ADR-003 amendment);
  sequenced last, after TAPI-021/023, blocked on pending frontend rework + a design pass on
  `/internal` and the customer visualizer (tied to queued terra-hq-site design work, TBD).
  **2026-08-08: ROMS's visualizer confirmed rendering live in a real browser** (not just via
  `curl`) — required finding and fixing 3 layered bugs: (1) Terra API had zero CORS config, fixed
  with a deliberately narrow `CorsConfigurationSource` scoped to `/api/v1/ecosystem/public-health`
  + `https://terra-hq.com` only, documented as an explicit exception to the 2026-06-06 "CORS not
  in API layer" decision (that decision solved terra-api-fe's problem via same-origin, which isn't
  available to a separately-deployed Cloudflare Pages site); (2) mixed-content blocking (browser
  policy, separate from CORS, blocks any plain-HTTP fetch from an HTTPS page before CORS is even
  evaluated) — real root cause of "CORS fixed but browser still fails," found by scrolling up in
  DevTools Console for a separate browser-native warning; (3) Cloudflare's free-tier proxy only
  forwards to a fixed origin-port allowlist, which didn't include Terra API's old port — resolved
  by the 8081→8080 move above plus a Cloudflare Origin Rule. Full chronological debugging writeup,
  including the false leads (522 initially looked like a firewall problem, wasn't): Obsidian
  `cloudflare-https-proxy-for-non-standard-port-origin`. Separately, terra-hq-site's own Cloudflare
  Pages deploy was ALSO found silently broken since mid-July (bot-generated `wrangler.jsonc` never
  merged from its own branch into `main`) — fixed same session, see terra-hq-site's devlog.
  **2026-08-09: TAPI-025 closed, TAPI-024 still open.** Root cause was no prod DB access
  existing at all (SSH/SSM/Serial Console all failed) — fixed by attaching
  `AmazonSSMManagedInstanceCore` to `terra-api-server`'s IAM role (`terra-api-backup-role`,
  previously S3/SNS-only from the backup-automation work, SSM was simply never in scope).
  SSM now works on `terra-api-server` AND `roms-server` (latter had NO instance profile at all —
  created `roms-server-ssm-role`/`roms-server-ssm-profile` from scratch, same additive pattern).
  New prod operator account created directly via SSM (`admin@terra-hq.com`, `role=internal`,
  `ops:read`) — no registration endpoint exists in this codebase, account creation has always
  been an undocumented manual DB step. A self-inflicted bug during this fix (a `docker-prod.env`
  append landed on the same line as `TERRA_AUTH_PASSWORD` with no newline, corrupting it and
  breaking ROMS's heartbeat auth with 401s) was found and fixed same session. Full
  command-by-command tutorial, including a 6-attempt Jenkinsfile detour (3 distinct Groovy
  pitfalls: GString-interpolated secrets get masked/blanked by `withCredentials`, declarative
  `steps{}` rejects plain Groovy statements, multi-line `+` concatenation across pipeline lines
  fails to parse) that was abandoned once SSM access was fixed properly: Obsidian
  `ec2-ssm-access-provisioning-and-jenkins-groovy-secret-pitfalls`. Full narrative + root causes:
  `terra-api/DEV_LOG.md`, "TAPI-024/025 Resolved" (2026-08-09).
  **2026-08-09: Jenkins outage + recovery.** `terra-jenkins` (`3.211.62.86:8090`,
  `i-04ef85c382ac39269`) hung after 3-4 near-simultaneous pipeline triggers from this session's
  push wave — TCP connected, zero HTTP response. An SSM-issued `reboot` did NOT clear it (still
  hung ~8 min later); a full AWS Console reboot did (confirmed via `curl` → `403`). Root cause
  unconfirmed — no `free -h`/`docker ps` data was ever captured before the box was rebooted.
  Collateral: ROMS-Pipeline's Build Frontend stage was killed mid-run by the reboot (not a real
  code bug) — retriggered same session, confirmed running cleanly (a stage-replay reproduced the
  same stuck symptom once; a fresh full pipeline run succeeded). Full writeup: `terra-api/
  DEV_LOG.md`, "Jenkins Outage" entry; Obsidian `jenkins-hung-instance-ssm-reboot-vs-console-
  reboot`. Two new, unscoped forward-looking asks now in Notion Tasks DB: "Scope a Jenkins
  capacity/scaling session" and "Scope a service-load learning session (ROMS under high
  concurrency, etc.)" — Will's explicit sequencing: learning/design pass first, review before
  any implementation.
  **2026-08-09: ApiDashboard + terra-hq-site content accuracy audit.** Ported HTML text (both
  `terra-api-fe`'s `/` `ApiDashboard.js`, 9 tabs, and `terra-hq-site`'s 11 static pages) checked
  against current Notion/hub state via two read-only background-agent passes, then corrected.
  Real bug found, not just staleness: AdrsTab.js's ADR-010 card described a completely different
  ADR (CI/CD content, mislabeled) than the actual `terra-api-adr-010` (Tier/Role Claim
  Separation, Proposed) — fixed, plus "9 ADRs Accepted" miscounts, ADR-011/012/013 cards added
  (were missing entirely), and ADR-012 itself amended in Notion (its own text said no operator
  identity exists — stale since TAPI-025 provisioned one same session). terra-hq-site: fixed a
  repeated false claim (Terra API "EVENT BUS" — no such capability exists, only an ADR-007 audit
  log) across 4 spots in `terra_initiative.html`, plus 2 minor staleness fixes. Full writeup:
  `terra-api/DEV_LOG.md` and `terra-api-fe/DEV_LOG.md`. Some lower-severity findings (Build
  Sequence tab framing, a few overclaimed-capability lines) flagged but not yet fixed — follow-up
  pass, not urgent.
- **Active Task:** **TAPI-021 — EC2 right-size.** TAPI-019 (Jenkins EC2 data restore) and TAPI-020
  (SonarQube) both closed. TAPI-019 recap: the dedicated Jenkins EC2 `i-04ef85c382ac39269` restored
  the real `infra_jenkins_home` data and completed a fresh `master` pipeline green through
  production deploy; deploy target uses prod's private VPC IP `172.31.21.172`; prod SSH permits the
  Jenkins security group via `sgr-05b94280fb11d357d`. Old local Jenkins confirmed already off.
- **Next Step:** Scope TAPI-021 (EC2 right-size). Remaining sequence: → TAPI-021 (EC2 right-size) →
  TAPI-023 (OS patching) → TAPI-022 (domains+TLS — one real endpoint now live via
  `api.terra-hq.com`, per above; NOT a full close, most of the ecosystem is still raw IP:port,
  including ROMS's own address) → ADR-013 (customer identity/login, blocked on frontend + design
  rework, TBD). Also open, not yet scheduled: remove the old 8081 security-group rule once
  confident nothing references it. Confirmed NOT a new ROMS→Jenkins task: that's already
  `ROMS-002` (migrate ROMS's own separate Jenkins to the shared Terra Jenkins EC2) — CLOSED
  2026-08-08, see ROMS section below, not duplicated here.
- **Blockers:** None. A dedicated `will-cli` IAM identity now exists for local AWS work; narrow its
  AdministratorAccess policy or move to IAM Identity Center as a separate security follow-up.
  **2026-08-09: this access was used directly for real prod writes** (IAM policy attach on 2
  instances, direct SQL via SSM against prod Postgres) — fast and effective, but a same-session
  self-inflicted bug (the `docker-prod.env` corruption above) is a concrete example of what broad
  admin access can do wrong when a single command is slightly off. Narrowing this remains open
  and unscheduled.
- **Context:** **Credential incident (2026-08-01):** a Notion API key was committed live in
  terra-api's `.env` since 2026-07-05 and copied into `DEV_LOG.md` 2026-07-26. Rotated by Will;
  scrubbed from git history via two `git-filter-repo` passes, force-pushed, verified clean.
  Pre-scrub backup bundle: `terra-api-home/terra-api-backup-before-history-scrub-2026-08-01.bundle`.
  `terra-api-fe` npm peer-conflict fix verified: `rm -rf node_modules package-lock.json && npm
  install`. Never `npm audit fix --force` there (guts `react-scripts`).
  **2026-08-04: port 8082 fix committed and pushed** (`5b281cc`) — `application.yaml`,
  `docker-compose.dev.yml`, `DEV_LOG.md` all landed on `master`, nothing left uncommitted.
  **2026-08-07: CLAUDE.md decision log corrected** — the 2026-07-26 entry claiming terra-api-fe
  Jenkins CI was "deferred" was stale; TFE-201 (2026-08-02) actually shipped it live (both a
  standalone terra-api-fe Jenkinsfile and four frontend stages inside terra-api's own Jenkinsfile,
  per the same-origin deploy model in adr-009). Entry marked superseded, not deleted.

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
  Feature-complete against ADR-009's Build Sequence. **CORRECTED 2026-08-08 — this WAS live
  in production the whole time**, contrary to the "not production-ready" note previously here:
  same-origin embed (ADR-009) means terra-api's own Jenkinsfile checks out terra-api-fe,
  builds/tests it, and copies the CRA build into `src/main/resources/static/` inside the
  terra-api jar — there is no separate terra-api-fe deploy pipeline or Docker image, so the
  commented-out `terra-api-fe` service in terra-api's `docker-compose.prod.yml` (mirroring
  ROMS's separate-container frontend shape) was never the right model and stays commented out
  correctly. Verified via `curl https://api.terra-hq.com/` returning the CRA shell
  (`main.054491d5.js`), `Last-Modified` same-day as this correction — confirms current build is
  live, not stale cached HTML. The prior "not production-ready" framing conflated dev-only
  *testing* against real ROMS/PIOS data (still true — no live integration test done) with
  deployment status (false — deployment has been live since at least TFE-201, 2026-08-02).
- **Active Task:** **SonarQube-related cleanup on `sonarqube-quality-gate` — RESOLVED 2026-08-08**
  (was flagged dirty 2026-08-07: modified `App.css`, `ProtectedRoute.js`, `Login.js`; new
  `ProtectedRoute.test.js`, `Login.test.js`; untracked `.vscode/`). Committed via `198f591`
  ("refinements") same day; working tree confirmed clean via `git status`. Separately, this
  branch's Jenkinsfile gained a `post { always {} }` cleanup stage 2026-08-08 — considered
  mirroring terra-api's `docker image prune -f` exactly, but landed on `npm cache verify`
  instead (an earlier draft used `npm cache clean --force`): the hub's standing disk-cleanup
  rule (HUB_GUIDE.md, from the ROMS incident) is deliberately unconditional because gradual
  silent accumulation was the failure mode, but that rule targets Docker image layers
  specifically — npm's cache is content-addressed and self-managing, no unbounded-growth
  problem to justify a full wipe. `verify` prunes corrupted/unreachable entries only. Considered
  and rejected: a `du`-based size-threshold gate — new precedent (no existing pipeline gates the
  standing rule on a threshold) solving a problem that doesn't apply to npm's cache. Not yet
  committed, pending Will's approval. Distinct from terra-api's own TAPI-020 (SonarQube quality
  gate), which IS fully closed and verified green — this was terra-api-fe-specific, unrelated
  status, now also resolved.
  **3 real bugs found and fixed in the port, 2026-08-04:**
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
- **Next Step:** **2026-08-09 — `terra_api_strategy.html` ported into this app as a real page,
  now the app's DEFAULT LANDING ROUTE.** Full writeup: `terra-api-fe/DEV_LOG.md`, "Terra API
  Internal Surface — HTML-to-React Port, /internal (ApiDashboard), Root Route Swap" (long
  entry — covers the initial scaffold, a full redo after the first pass drifted from the HTML's
  actual CSS values instead of copying them, 4 distinct visual bugs found only by Will looking
  at the rendered page, new UI with no HTML equivalent, and the final route swap). Short version:
  new `ApiDashboard.js` at `/` (moved off `/internal` in the same session — Will: this is his
  own internal tool right now, not a live customer product, so root should land here, not on
  the customer dashboard) — 9 tabs: the HTML's original 8 (Overview/Core Services/Health &
  Isolation/Build Sequence/ADRs/Ecosystem Public/Ecosystem Architecture/For Partners, migrated
  as a near-verbatim CSS+markup copy) plus a 9th "Operator" tab absorbing the old standalone
  `/internal` route (`OperatorDashboard.js`, now deleted). Customer dashboard moved to
  `/dashboard` behind the same `ProtectedRoute`; `OperatorRoute`'s non-operator fallback updated
  to `/dashboard` (was `/`, would have infinite-looped once `/` became the same gated route).
  Also ported: `HeartbeatBackdrop.js`, a React port of the HTML's animated procedural
  circuit-trace canvas (not a static image — random-walk PCB trace generator + scroll parallax +
  heartbeat-interval flash propagation). `EcosystemVisualizer`/`terraScene.js` gained an opt-in
  `transparent` prop (default `false`, zero behavior change for existing callers) so the
  Overview/Operator tabs' visualizer can show the circuit backdrop through it — the one
  deliberate exception to "identical to the HTML," per Will: the live React visualizer itself
  stays, only its background treatment needed to match. TFE-602 opened for two placeholder-
  branding slots pending Will's own designs (nav logo, browser favicon) — see terra-api-fe/
  TASKS.md. TFE-502/503 (401 redirect UX, 10/12 modules untested) remain untouched, still open
  from prior sessions.
- **Blockers:** **Everything above is UNCOMMITTED** (confirmed via `git status`/`git log`
  before this note was written — nothing pushed, nothing committed this session). Also:
  mobile/narrow-viewport rendering for this new page has NOT been visually verified — no browser
  automation tool was available; claims are based on a careful CSS read against the HTML
  source's own breakpoints, not an actual screenshot. See DEV_LOG's "Known Limitations" for
  specifics. Standing caution unchanged: never run `npm audit fix --force` here.
  **2026-08-04: `package-lock.json` regenerated** via `rm -rf node_modules package-lock.json &&
  npm install` — fixed a `react-router`/`react-router-dom` version mismatch (stale lockfile had
  pulled a v7 `react-router` under a v6 `react-router-dom`) plus a `caniuse-lite` submodule gap
  that broke the Docker build's CSS/PostCSS step. Confirmed fixed via clean container rebuild.
  **2026-08-08: Jenkinsfile gained a post-build `npm cache verify` stage** (`8b9ae71`, superseding
  an initial `clean --force` draft `813959a` — full reasoning in DEV_LOG). GitHub webhook payload
  URL identified for push-triggered builds: `http://3.211.62.86:8090/github-webhook/` (same
  global receiver as terra-api's) — not yet confirmed added on GitHub, and not yet confirmed the
  `terra-api-fe-main`/`-branches` jobs have "GitHub hook trigger for GITScm polling" enabled.
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

## ROMS repo, product name Ha'bem (OMS)        <!-- prefix: ROMS -->
- **Naming (corrected 2026-08-10):** Product acronym is **OMS** (Order Management System), not
  ROMS — "ROMS" is only the literal legacy repo/package name in the codebase (short for the
  original "Real-time Order Management System"). Product docs now say "Ha'bem (OMS)"
  consistently. Notion (main project page, all 5 ADRs, Resort Deployment Tracker) and Obsidian
  (notes 01, 02, 12) all updated same day.
- **Reference Links:** Notion ADRs `roms-adr-001`–`005`. Repo: `terra-api-home/
  restaurant-order-management-system/` (gitignored there). Design ref: `roms-expansion-sketch.md`
  (Claude-generated, not yet in repo) · Obsidian `Projects/ROMS/12 - Habem Expansion & Brand
  Design`. **ROMS ADR-005 and terra-api-adr-010 still need a follow-up amendment** (stale
  "found stopped, recoverable in place" text, superseded by actual migration).
- **Status:** Live in prod, single property, verified end-to-end (heartbeat → Terra API public
  health). **2026-08-10: guest-facing brand renamed ROMS → "Ha'bem"** — ROMS stays the internal/
  engineering codename (repo, packages, ADRs unchanged). Full pre-implementation design pass
  done this session: `Property`-scoped multi-tenancy + multi-category data model sketched
  (`CatalogCategory`/`CatalogItem`/`Booking`/`ServiceRequest`/`PaymentMethod`, adapter pattern
  for African mobile money); Phase 2 conceptual framework for an eventual Africa-wide open
  delivery network (provisioning-only, nothing built); brand/icon system (wordmark + per-category
  tab badges) drafted, palette not finalized. **Frontend page mockup built** (`habem-pages.jsx`
  + companion `habem-pages-tutorial.md`, both Claude-generated, not yet in repo): functional
  React mockup of the browse grid/sidebar/hero/cart flow, themed via a single `THEME` object and
  a shared `CategoryGlyph` image-or-icon component for one-place color/asset swapping.
  **Currency generalized**: replaced hardcoded XAF formatting with a `CURRENCIES` registry
  (XAF/KES/NGN/USD) + a `PROPERTY` object + `formatPrice()`, mirroring `Property.currency` —
  adding a new region's currency is now one registry entry. **Portability layer completed
  2026-08-10:** added `APP_IDENTITY` (product naming — `Logo` renders from it dynamically
  instead of hardcoding "Ha'/bem") and `DESIGN_TOKENS` (corner radius scale + typeface) —
  four total swap points now (`THEME`/`APP_IDENTITY`/`DESIGN_TOKENS`/`CURRENCIES`+`PROPERTY`).
  Matching §0 Naming Registry added to `roms-expansion-sketch.md` as the prose-side source of
  truth for future renames. **2026-08-11: §13 conceptual cross-vertical sourcing link drafted**
  — Ha'bem's Food & Beverage catalog sourcing from Terra Agriculture (mirrors the existing Terra
  Apparel/bamboo off-take pattern). Explicitly not build-ready: Terra Agriculture is
  planning-only, no active ops, only defined scope is a Ghana bamboo/calabash pilot — nothing
  about produce yet. Geography mismatch flagged (Ghana pilot vs. Cameroon-only Ha'bem property).
  One real thread: both sides independently already plan to use Terra Nkap. Cross-linked from
  the Terra Agriculture Notion page; open question (Cameroon-only vs. standing principle) not
  yet decided.
- **Active Task:** None blocking prod. **2026-08-13: real prod login bug found and fixed same
  session** — `POST /api/users/login` was returning `500` for any login typed with different
  username casing than at signup (registration lowercases, login lookup didn't — two separate
  un-normalized `findByUsername()` call sites). Compounded by `GlobalExceptionHandler`'s catch-all
  masking the real exception as an opaque `500` with zero logging. Both fixed, committed (`8c7d7e0`),
  deployed. Full debugging narrative (3 false leads before the real root cause, confirmed live with
  Will): `oms/DEVLOG.md`, "Login 500 Root-Caused" entry.
- **Next Step:** Decide final Ha'bem wordmark palette; verify domain + OAPI (Cameroon/CEMAC)
  trademark availability before brand commit; decide Grocery category's real fulfillment model
  before building it as a separate tab; pin `CatalogItem` price to a currency on the backend
  (frontend pattern now exists as reference); replace placeholder 8% Nkap discount rate once
  Terra Chain settlement design is real; build Spa/Tours/Housekeeping category pages once
  `Booking`/`ServiceRequest` entities exist. Unrelated/still open: disable SonarCloud Automatic
  Analysis for ROMS project; amend ADR-005 with final migration outcome; terminate/delete old
  us-east-2 instance once confident. New: OMS-018 (favicon/touch-icon needs tighter cropping,
  blocked on a real source image — binary asset, not a code fix); OMS-015 (Redis health-check
  race/config bug, root cause still genuinely uncertain, needs a dedicated investigation session).
- **Blockers:** None technical.
- **Context:** Spring Boot + React, single 2GB EC2 instance (us-east-1, `oms-server` /
  `i-04f3abfb579f2bd1d`, public IP `100.60.7.24`). Data model extension is non-breaking (5-step
  migration path drafted, not run). Full brand/data-model reference: Obsidian note 12 in
  `Projects/ROMS/`. SSM access confirmed working on this box (used directly 2026-08-13 to pull
  container logs and query prod Postgres for the login-bug investigation).

## PIOS                                             <!-- prefix: PIOS -->
- **Reference Links:** Notion ADRs `pios-adr-011`–`015` — URLs not recorded, add when confirmed.
  Strategy page: `terra-hq-site/pios_strategy.html` (architecture, event model, capital
  governance).
- **Status:** CORRECTED 2026-08-07, REVISED 2026-08-08 after checking PIOS's own Notion project
  page (not just the ADR index). **ADR-013 (event schema versioning, upcasting at the repository
  layer) is Accepted and resolved**, not gating — verified via the ADR's own text ("flagged as the
  most critical unresolved design decision before coding could begin; now resolved"). ADRs 011,
  012, 014 also all Accepted. ADR-015 (Consumer Capital Layer) is design-level-accepted only,
  correctly deferred until PIOS MVP + Terra API's WebSocket relay both exist. **However — the
  2026-08-07 correction was incomplete: PIOS has a SEPARATE, real, still-standing blocker that has
  nothing to do with ADRs.** Per PIOS's own project page (last synced 2026-05-30, itself possibly
  stale but the gate condition should be re-verified with Will, not assumed cleared): a
  **learning-stack prerequisite gate** — CS50P + Karpathy Zero to Hero (Python) → Angular → DSA —
  is required before any PIOS coding begins, and as of that page's last sync had **not been
  started**. Design phase (no PIOS code exists yet) is accurate for BOTH reasons: no code has
  started, and the learning gate was still open as of the last real check.
- **Active Task:** None — PIOS coding cannot start until the learning-stack gate clears (or Will
  explicitly decides to waive/reorder it), independent of the ADR sequence being fully resolved.
- **Next Step:** Confirm with Will whether the learning-stack gate (CS50P/Karpathy → Angular → DSA)
  has progressed since 2026-05-30 — this project page hasn't been touched since, same staleness
  risk as everything else in this ecosystem. If cleared, PIOS is ready to start on the
  event-sourced write path (ADR-011/012/013). If not, it remains genuinely blocked, not just
  deprioritized.
- **Blockers:** Learning-stack prerequisite (Python/CS50P+Karpathy → Angular → DSA), NOT any ADR —
  status of that gate unconfirmed as of this correction, needs a direct check, not inference.
- **Context:** Event-sourced. FastAPI/Python reserved. Rules-engine-gated AI signals. Two Notion
  pages exist for the same ADR-013 decision (an early 2026-05-12 draft under a superseded
  "Investment System App" page, and the formal 2026-07-13 `pios-adr-013` filed under PIOS itself) —
  both Accepted, same decision, not a real conflict — worth eventually archiving the older
  duplicate but not urgent.

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
  **2026-08-13: terra_africa_strategy.html gained a new "FARM RENDERS" tab (THQ-004, committed
  locally, not yet pushed)** — 21 Gemini-generated images for the Terra Agriculture Cameroon
  pilot (beehive field, approved wide site mockup, the 11-panel modular-shell schematic sheet,
  and realistic component/configuration renders for the shell system) added under
  `Assets/agriculture/`, each with its exact generation prompt inline via a show/hide toggle +
  click-to-enlarge lightbox (new `.render-*` CSS block + `toggleRenderPrompt`/
  `openRenderLightbox` JS, none of it colliding with existing page classes). A new "Pilot Status"
  section (00) precedes the gallery: a 6-phase budget grid pulled from this session's Notion sync
  (Beekeeping $1,200–3,700 · Chickens $500–2,000 · Crops $200–700/cycle · Hydroponics $150–3,000 ·
  Pigs & Cattle $2,000–5,000+ · Agrivoltaics not yet scoped), plus two callouts: the open hive/
  living-fence security gate (Flow Hive explicitly ruled out as a security fix) and the modern-hive
  pricing comparison that reaffirmed the top-bar build decision. The BRAND & STRUCTURE tab's Terra
  Agriculture card was also rewritten to match (was a stale generic "AgTech platform" blurb).
  3 draft images intentionally excluded (in-progress schematic duplicate + 2 rejected coop
  iterations missing a foundation) — flagged inline on the page, not deleted from disk. No roof-
  only realistic render exists yet (schematic-only) — flagged inline too.
- **Next Step:** Commit + push `terra_africa_strategy.html` (THQ-004, currently uncommitted on
  disk only). Also unrelated/still open — **THQ-003, found 2026-08-04, uncommitted**: live-testing THQ-002 against a real
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
- **Folder rename completed 2026-08-20: `terra-api-home` → `terra-initiative-home`** (final name
  differs from the earlier-planned `terra-home` — see Claude memory `terra-api-home-future-
  rename`). All Machine Paths / local-path references across this hub, CLAUDE.md files, and
  Notion should use the new name going forward; `terra-api-home` in older HUB_STATE entries
  above is historical and hasn't been retroactively edited. Local Claude memory (project-scoped,
  not git-tracked) was migrated file-for-file from the old project path to the new one same day.
  The 🌍 Terra Inc Notion page (`39289370d49780178d44c4e2c87c5488`) now carries a "Local machine"
  note pointing at the new folder path, added directly under its intro paragraph.
- **New `ALL_TASKS.md` at the `terra-initiative-home` root (2026-08-21):** cross-references the
  canonical Notion Tasks DB (Terra-domain rows) against oms/terra-api/terra-api-fe/terra-hq-site's
  own local `TASKS.md` files. Found 4 Notion rows that read as stale against more current/detailed
  repo TASKS.md entries (TAPI-020 SonarQube gate, JVM heap caps "not yet applied," ADR-012/
  operator-account provisioning, ROMS EC2/Phase D). This file is a manually-regenerated snapshot,
  not a live sync — re-pull Notion + re-read each TASKS.md each session that needs it current. The
  terra-hq-site "~13 items pending commit" (THQ-005–017) risk this file flagged turned out to
  describe the `solan` machine's session state specifically — the `test` machine's own
  `terra-hq-site` clone has always had a clean working tree and only ever tracked THQ-001/002/003;
  re-check on `solan` directly rather than trusting this note for that machine (found 2026-08-22).
- **All 4 stale-Notion-row contradictions above resolved 2026-08-23**, via live Notion MCP access
  (finally connected in a Claude Code/VSCode session, not just claude.ai): (1) TAPI-020 had no
  standalone Notion row to correct — only referenced inside Phase A's title and the meta-correction
  task, nothing to close. (2) JVM heap caps task marked Done, referencing TAPI-013's verified
  `-XX:+PrintFlagsFinal` confirmation. (3) Phase B (ADR-012) marked Done — operator account +
  endpoints both live; ADR-012's own Notion page Status field also flipped Proposed→Accepted,
  since its 2026-08-09 update note already documented live verification. (4) Phase D (ROMS EC2)
  marked Done, per Ha'bem (OMS)'s own Notion page confirming ROMS-001/002 closed 2026-08-08 — one
  real fragment survives, undone: disabling SonarCloud Automatic Analysis for the OMS project,
  which that same page's log still lists as an open manual step. Also fixed in the same pass: the
  terra-api-fe Notion project page wrongly said its own repo was `will55555/terra-api-home` (should
  be `will55555/terra-api-fe`, confirmed via `git remote -v`). Two meta-tasks this uncovered were
  also closed: "Correct stale Notion Tasks DB rows" (this work) and "Confirm whether a Machine
  Paths table exists in Notion" (confirmed via search: it does not — Machine Paths is a
  `claude-skills`-only artifact, never built in Notion). **Left open, not closed** (a scope call,
  not a factual correction): "Phase A: Terra API branch consolidation" — its Notion page is blank
  and names branches (`frontend-CI`, `public-health`, `customer-identity`) that don't exist under
  those names in `terra-api`'s current branch list; the underlying work looks done via
  differently-named merges, but confirm with Will before closing it.
- **HUB.md's Machine Paths table was stale against the 2026-08-20 folder rename — fixed 2026-08-23.**
  All `(machine: test)` rows for terra-api/terra-api-fe/terra-jenkins/terra-hq-site previously
  pointed at a "New folder\" sibling layout that no longer exists on this machine; corrected to
  `terra-initiative-home\<repo>\`, matching the real structure (one outer git repo,
  `origin=will55555/terra-api-home` — not yet renamed on GitHub to match the local folder — with
  each of the four as a gitignored nested-repo subdirectory, confirmed via direct `ls`/`git
  remote -v` checks). The `terra-hq-site (machine: test)` row was doubly wrong: it pointed at a
  standalone clone path (`Programing\terra-hq-site\`) that hasn't existed since the rename either.
- **`terra-hq-site/TASKS.md`'s THQ-003 row corrected 2026-08-23**: previously said "uncommitted,
  local to `test` machine only" — false on this machine (the fix IS committed, `43805a9a`,
  2026-08-03). The real finding: the commit only half-applies the fix — the child tube's
  `cube1`/`cube2` assignment is live code, but the parent extension tube's matching fix is
  literally commented out (`// tube.userData.cube1 = cube;`), so the bug THQ-003 was opened for
  still reproduces on the parent tube specifically. TASKS.md updated to describe this precisely;
  **the file edit itself is uncommitted on `terra-hq-site`** — Will's call whether/when to commit
  a docs-only change.
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
- **Future heartbeat model refinement — pull, not push (noted 2026-08-08, explicitly NOT for now,
  save for a dedicated refinement session):** Will's proposal to eventually replace ADR-005's
  current sidecar PUSH model (each service independently sends a heartbeat payload — including raw
  metrics like `latency_p95_ms`/`error_rate_1m` — to Terra API on its own schedule) with a PULL
  model instead: Terra API initiates a query to each service; each service runs its own
  continuously-updated internal health-evaluation class (constantly comparing actual state against
  expected state); when queried, the service responds with a minimal, pre-digested tri-state
  signal (roughly yes/no/maybe — healthy/unhealthy/degraded), not raw metrics. **Rationale
  (security-driven):** the current push model means N services can each send arbitrary payloads
  *into* Terra API — a compromised service has a wide, structured inbound surface to exploit. A
  pull model narrows this dramatically: each service only ever answers one fixed, narrow question
  when asked, nothing unsolicited ever arrives at Terra API. This is a real architectural shift
  (inverts ADR-005 Section 1's "push over pull" decision and its own stated rationale — "Terra API
  stays passive... does not need to know each service's internal health endpoint URL or schema" —
  a pull model requires exactly that knowledge) and deserves its own ADR amendment/dedicated
  session when Will returns to it, not a quick retrofit. Not started, not scoped further than this
  note.

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
