# Engineering Hub State
<!-- Freshness: 2026-10-31 (rev 79) | v1.3 | Snapshots only — overwritten in place. History lives in DEV_LOGs. -->
<!-- Last Audit: 2026-10-22 | Monthly Hub Audit (HUB.md) fires from Startup Sequence step 7 when this is >30 days old. Update this line after each audit. 5 findings this pass, 1 resolved same day: terra-api-fe's Bitbucket mirror was 8 commits behind — Will ran `git push bitbucket` directly, re-verified 0/0 divergence, RESOLVED. Still open: the odd 4th "all" remote pushing to both GitHub+Bitbucket, separate from the plain origin/bitbucket pair, is still there and is likely why origin-only pushes keep drifting — worth remembering to push `all` (or both remotes) going forward, not a one-time fix; terra-api-fe's stale "Everything above is UNCOMMITTED" claim (tree is clean at 4874f91); ~~Agent Operating Constraints (NEVER execute build/test/run) sits past HUB.md's own 80-line read cap~~ — RESOLVED same day: the section was pure restatement of Prime Directives 1–2 (already inside the cap), deduplicated to a pointer + the genuinely new content (multi-remote push discipline, backup policy, write-verification rules), HUB.md v2.1→v2.2; terra-api's HUB_STATE text doesn't cite a comparable SHA to its current a4590a5, can't fully verify drift there. -->
<!-- Last Notion Task Pull: 2026-10-31 | Startup Sequence step 2b checks the live Tasks DB for rows created after this date, every load. Update this line every time step 2b runs, regardless of whether anything new was found. 81 new rows since 2026-10-22 (9 already Done/superseded, 72 open), mix of Terra-domain and personal/finance; Terra rows now listed in ACTION_PLAN/ALL_TASKS.md, not individually verified; a full `reconcile all tasks` pass is still separate. -->
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
- **Status:** **PROD STOPPED (checked via AWS 2026-10-31):** root stopped `terra-api-server`, `oms-server` and
  `terra-jenkins` 2026-10-06 20:47 ET; `api.terra-hq.com` and Jenkins time out. Root also detached
  `terra-api-server`'s only volume (`vol-0095d9b52a1d3ffaa`) 2026-10-29 19:18 ET, after snapshot
  `snap-022af6a744bfe2724`; it now reads as "unattached". Newest Postgres dump in S3: 2026-10-06 03:00 UTC. No AWS
  Backup plan exists, despite the backup policy. Earlier text below describes the system when running. **TAPI-020 (SonarQube quality gate) fully closed 2026-08-07:**
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
- **Next Step:** Run the AWS audit scripts (Notion rows from 2026-10-30), then scope TAPI-021 (EC2 right-size) from the output. Remaining sequence: → TAPI-021 (EC2 right-size) →
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
- **Blockers:** Working tree clean at `4874f91` (checked 2026-10-31). Still true: mobile/narrow-viewport rendering for this
  new page has NOT been visually verified — no browser
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

## Ha'bem (OMS)                                      <!-- prefix: OMS (was ROMS, renamed 2026-10-03) -->
- **Status:** Shipped — Enhancements Queued. **`oms-server` stopped since 2026-10-06** (see Terra API), so the temp links are down. Mobile-first + store-readiness rules adopted 2026-09-28.
- **Active Task:** Mobile audit (absorbs parked Phase F UX pass).
- **Next Step:** Fix phone layout: sidebar → ☰ drawer under tablet width, icon-only header actions under ~480px, single-column grid; then verify menu data loads over a real domain.
- **Chain:** mobile audit → guest-facing Ha'bem domain → Location (room/table) entity via §8 migration → per-room/table QR codes → app store readiness.
- **Blockers:** QR printing blocked on (1) guest-facing domain (not terra-hq.com — stealth), (2) no room/table concept in backend.
- **Context:** QRs will encode a redirect path (`/r/{property}/{room}`) so targets can change without reprints. Store publisher identity is trigger-gated → entity that owns Ha'bem, not personal name. Likely store path: Capacitor + native push. Full notes: Obsidian `Projects/ROMS/13 - Habem Mobile-First, QR & Store Readiness`.
  Box: `oms-server` / `i-04f3abfb579f2bd1d` (us-east-1), public IP `100.60.7.24`, root EBS 20GB
  (resized from 6.8GB 2026-10-03); SSM and EC2 Instance Connect both confirmed working (Instance
  Connect is the fallback if SSM dies). Internal dashboard temp link:
  `http://100.60.7.24/internal/dashboard` (raw IP, no Ha'bem domain yet).
- **Reference Links:** Notion ADRs `roms-adr-001`–`005` (Notion names not yet renamed) · design
  ref `oms/assets/oms-expansion-sketch.md` · Obsidian `Projects/ROMS/12 - Habem Expansion & Brand
  Design` (brand/data-model reference).
- **Carried forward (open, outside the mobile chain):** (1) no migration file for the manual prod
  `user_role_check` `INTERNAL` addition — a from-scratch DB rebuild loses it; (2) confirm a clean,
  fully automated green Jenkins deploy since the builder-prune fix + EBS resize (last deploy
  needed manual SSM/Instance Connect help); (3) amend ROMS ADR-005 + terra-api-adr-010 with the
  final migration outcome; (4) terminate old us-east-2 instance; (5) disable SonarCloud Automatic
  Analysis for OMS; (6) OMS-018 favicon/touch-icon (blocked on a real source image); (7) brand/
  product decisions: wordmark palette, domain + OAPI (Cameroon/CEMAC) trademark check, Grocery
  fulfillment model, pin `CatalogItem` price to a currency, replace placeholder 8% Nkap discount
  rate; Spa/Tours/Housekeeping pages once `Booking`/`ServiceRequest` entities exist.

## PIOS                                             <!-- prefix: PIOS -->
- **Reference Links:** Repo `terra-initiative-home\pios` (local, no remote). ADRs 001-020 in
  `pios/docs/adr` (Notion is the source for 001-019; the ADR-019 copy omits personal values). Notion page
  `36f89370d4978140a5a9d14f76ddaefd`. Doc 24, Finance strategy → PIOS map:
  `3fc89370d497814180aada37d64ff686`. Travel open item: `3da89370d4978198ab71cef2ad7aa37c`. 6-layer
  schema summary: Obsidian `Knowledge/Projects/PIOS/02-event-sourcing-schema.md`. Strategy page:
  `terra-hq-site/pios_strategy.html`.
- **Status:** Scaffolded 2026-10-31 (`9cc314a`): one package per schema layer, repository interface
  with SQLite and Postgres stubs, modular empty migrations, CI (GitHub Actions + dormant Jenkinsfile
  on one `scripts/check.sh`). Will reran the checks from the new location on Python 3.15.2: 25 tests,
  ruff, mypy strict all green. **Scaffold only: no event types, projectors, rules engine, routes or
  tables** (ADR-020). Finance strategies stay in the Notion Finance space with their values; PIOS gets
  templates only (ADR-016, doc 24).
- **Active Task:** None. **Paused by Will 2026-10-31.** PIOS-001 done; feature work waits for the gate.
- **Next Step:** On resuming: PIOS-008, write the travel layer ADR (next free number, 021) and add its doc 24 row.
  Design work, so the gate doesn't block it. PIOS-005 (pios-algo joins by `git subtree` at `pios/algo`)
  comes later and doesn't hold up algo steps 3-9.
- **Blockers:** Learning-stack prerequisite (CS50P + Karpathy → Angular → DSA), kept on purpose by Will
  2026-10-31. Last recorded as not started 2026-10-06. pios-algo counts as the Python practice track
  (E6) but PIOS itself isn't let through. Notion's `Current Phase` "Blocked — Needs Decision" is this
  same gate, not a separate design question. No remotes set up, by choice, for `pios`, `pios-algo` or
  `will-strategies`: the Terra GitHub org doesn't exist yet.
- **Context:** ADR-020 (Accepted 2026-10-31): PIOS owns its envelope, algo events cross through a
  repo-layer translator (designed, not built), and PIOS never imports `pios_algo`. No DDL for
  `pios_schema_v1.0.0` exists anywhere found, so tables arrive with their features (PIOS-002). ADRs
  016, 017, 019 are still Proposed; ADR-015 stays deferred until after MVP + Terra API's WebSocket
  relay. An older duplicate ADR-013 page sits under the superseded "Investment System App" page:
  worth archiving, not urgent.

## pios-algo                                        <!-- prefix: ALGO -->
- **Reference Links:** Repo `terra-initiative-home\pios-algo` (local, no remote). Design docs in its
  `docs/`; private state and planning notes in `terra-initiative-home\will-strategies\docs` (index
  `README.md`, decisions E1-E15). Notion build page `3a989370-d497-81a6-90db-fb0abf02af5b`. Doctrine page
  `37089370-d497-8130-936b-c5cb7de79dbf` is never edited. Merge rules:
  `docs/adr/ADR-003-merge-ready-brick.md`. Obsidian: `Knowledge/Projects/PIOS/07-pios-algo-build-state.md`.
- **Status:** In build. Steps 1-2 and pre-step-3 done and committed (`pios-algo` `a83ab5f`+,
  `will-strategies` `c1fc3b7`+): chain IDs, unknown versions refused on read and append, `tzdata`, Python
  targets, `StrEnum`. Will ran the checks on Python 3.15.2: 81 + 9 tests, ruff clean, mypy strict clean on
  `core`, `events`, `tenancy` (`will-strategies` has no mypy). Python 3.14 itself hasn't been run. Claude
  Code owns the build; bundles retired. Live trading stays in Cowork scheduled tasks: MOM-01 v1.1 and
  VOL-01 at L2 with in-app confirmation, paper set at L0.
- **Active Task:** None. **Build paused by Will 2026-10-31**; live scheduled trading continues. Step 3 is next on resuming (Webull adapter on paperTrade keys).
- **Next Step:** Will generates the paperTrade keys and checks scopes, then step 3. Keys go in the password
  manager only.
- **Blockers:** Waiting on Will: paperTrade keys + scope check, Advanced Quotes price, AWS audit outputs,
  root MFA, MOM-01 `expected_signals_per_week` then approval (the rate is in `param_hash`), VOL-01 monthly
  loss cap, Trading Log CRX #2 row. `pios-algo` and `will-strategies` stay local for now, like `pios`.
  `will-strategies/docs` has the account number committed locally (`5c563a1`): decide before it ever gets a
  remote.
- **Context:** Terra-owned platform, Will = tenant #1; `will-strategies` is Will's own, adjacent to PIOS but
  never merged into it. Python in pios-algo, Java for Terra API/PIOS integration (ADR-001). Envelope stays v1
  while no event database exists; after that, changes need a version bump and upcast (ADR-013). Runs in Will's
  personal AWS account, ≈ $8-10/mo (E1, E11). Engine and watchdog never share PIOS's process (ADR-003, PIOS
  ADR-020).

## Terra Agriculture                                <!-- no repo, no prefix yet — planning, Terra Africa -->
- **Reference Links:** Notion `38189370d497816daa98ce7dc961b099` (phase and research pages stay live there;
  Phase 0 `3bb89370d49781599304f6cf1943481b` is the fence source). Operational summary is maintained on
  `terra-hq-site/terra_africa_strategy.html` → Agriculture and Farm Renders tabs.
- **Status:** Planning, no operations or capital yet. Likely Terra's first live real-world service. Site and
  Notion compared 2026-10-31 and aligned: Phase 0 design, Parcel B numbers (planning 235 × 180 m, ~830 m),
  order 0 → 1 → then 2/3/5 in parallel. Pilot rollup with the re-costed fence: ~$7,900-$16,600, planning-stage.
- **Active Task:** Phase 0 prep. The dry-season window runs mid-Nov → mid-Mar; first rains ~Mar 2027.
- **Next Step:** Land title formalization (lead blocker), then GPS corner walk + altitude (altitude decides the
  post species), IRAD questions, ~330 grafted citrus order, 5 local quotes, boundary eucalyptus count.
- **Blockers:** Land title before capital goes into permanent structures. Local operator is open, in parallel.
  Public brand name undecided. All figures stay planning-stage until Cameroon ground truth replaces them.
- **Context:** Tasks live in the Notion Tasks DB, listed in `ACTION_PLAN/ALL_TASKS.md`. Old-fence renders
  stay as they are (Will, 2026-10-31); 12 unused `Gemini_Generated_Image_*` files in
  `Assets/agriculture` are unused. Africa, including this line, is family-owned and outside US tax scope. Future
  full-stack domain service, no code yet.

## terra-hq-site                                    <!-- prefix: THQ -->
- **Reference Links:** Local specs (verify freshness before trusting detail — this section had
  drifted months stale before the 2026-10-03 rewrite below): `terra-hq-site/CLAUDE.md` — page
  inventory + Cloudflare Access/visualizer status (now corrected, see Status) ·
  `terra-hq-site/TASKS.md` (THQ-001 through THQ-019) · `terra-hq-site/devlog.md`. The repo's own
  Three.js visualizer is ARCHIVED (`Assets/archive/terra_api_visualizer_phase5.js/.html`,
  2026-08-09) — the live/maintained visualizer is terra-api-fe's own
  (`terra-api-fe/src/visualizer/`), see that section. Notion: (none recorded — add when
  confirmed).
- **Status — rewritten 2026-10-03, this whole section was stale since ~August.** THQ-001/002/003
  all CLOSED 2026-10-04 per Will's direct confirmation — superseded, not built-in-place: the
  visualizer migration THQ-001 was tracking already happened (lives in `terra-api-fe/src/
  visualizer/`, live at `api.terra-hq.com`); THQ-002 (health-tier coloring) and THQ-003
  (pipeline-tube refresh bug) both already shipped in that terra-api-fe copy instead of this
  repo's own archived one. **Cloudflare Access plan abandoned, superseded** — CLAUDE.md's old
  "NOT enabled, setup pending" language was stale; that plan was dropped in favor of JWT-based
  route gating via Terra API (`OperatorRoute`, ADR-012), which already shipped. `terra-hq.com`
  itself stays intentionally public; only operator-gated pages (now on `api.terra-hq.com`, not
  this repo) require auth. **2026-10-03: index.html's standalone Terra API puzzle piece
  removed** (commit `5de8ea6`) — corrected an earlier misread of "fold Terra API into Terra
  Tech" (an agent had read it as a content/link question, already resolved; the real ask was
  removing a redundant top-level card, since Terra Tech's own card already listed "Terra API
  Shipped"). Hero stat + section-count copy updated to match (now "Terra Inc + 5 divisions",
  not "+ API platform"). **2026-10-03: terra_tech.html's Products & Infrastructure cards all
  made clickable** (commit `97dd2d8`) — Terra API Visualizer card now links to the local
  archived copy, Terra CI/CD card links to the Jenkins temp URL (`http://3.211.62.86:8090`,
  plaintext HTTP + raw IP, will break on IP change — same caveat as Ha'bem's temp link below).
  **2026-10-03: Ha'bem (OMS) card repointed** (commit `3919b96`) from the static
  `roms_gtm_strategy.html` page to the new OMS-fe internal dashboard
  (`http://100.60.7.24/internal/dashboard`, temp raw IP, no Ha'bem domain yet — see Claude
  memory `habem-domain-pending`).
- **2026-10-03/04/06 follow-on work.** `terra_tech.html` Overview tab reordered — the embedded
  prototype visualizer moved from section 05 to section 01 (top), per Will's direct ask
  (`36ec6ae`). **Visualizer cube taxonomy fixed in BOTH copies** (terra-api-fe's live
  `domainConfig.js` AND this repo's embedded `Assets/archive/terra_api_visualizer_phase5.js`,
  commit `b851c5b`) — stale Hospitality/Africa cube names replaced per Will's confirmed
  2026-09-28 model (Tech, Fabrication, Finance, Ventures, Real Estate, Agriculture, Apparel,
  Solar); also discovered `Assets/archive/` was fully gitignored so this fix wouldn't have
  deployed — added a precise `.gitignore` exception for just these 2 files (full reasoning
  inline in `.gitignore` itself). `terra_initiative.html`'s Org Chart child-service cards
  (Ha'bem/PIOS/Terra API under Terra Tech's expanded panel) linked to their real destinations,
  matching `terra_tech.html`'s own choices (`b901119`). **Repo-wide broken-image-path sweep**
  (`4d16f3e`, `2ce6945`) — found a systemic bug: `cards/`, `coins/`, `apparel/`, `resort/`, and
  `Tech/` (JS-constructed, missed by the first static-grep pass) were all referenced without
  their real `Assets/` parent directory across 5 pages (`resortConcept.html`,
  `terra_apparel.html`, `terra_nkap.html`, `terra_ventures.html`, `terra_tech.html`'s Gallery
  tab) — fixed all of them. Also found/fixed a stale `terra-roms-windbreaker.png` filename
  (HTML already said `terra-habem-windbreaker.png`, asset file was never renamed to match).
  **2 images remain genuinely missing, not a path bug** — `resortConcept.html`'s two
  `Gemini_Generated_Image_*` files don't exist anywhere in the repo; need new assets, not a
  code fix.
- **Active Task: Notion → HQ migration (started 2026-10-17).** Settled Notion content moves to its
  HQ home, which becomes the live place to update it; Notion source gets a dated "🚀 Live on
  Terra HQ" freeze callout (stamped 2026-10-28 on Terra Inc hub, Finance Quick Stats, Terra
  Entities, Compliance Calendar, Terra Agriculture, Terra Apparel). Done so far: REGISTER tab on
  `terra_initiative.html` (status, quick stats, entity register, compliance calendar) + holdco
  stale-fact fixes (Rung 2 pending, Rung 1 checklist, Mercury→Chase, WY report Terra Inc only);
  AGRICULTURE tab on `terra_africa_strategy.html`; Brand Governance on `terra_apparel.html`;
  Finance≠Ventures callout on `terra_ventures.html`; orphan `terra_africa.html` merged in as a
  Convergence tab + `_redirects`; `#tab` deep links. Tasks DB stays in Notion permanently.
  Protocol: future HQ data layer = own service, append-only revisions, per-home read feeds.
- **Earlier: THQ-004 CLOSED, 2026-10-17/18** — confirmed via `git log`, not
  trust-without-checking: `terra_africa_strategy.html`'s Farm Renders tab shipped a Security
  Perimeter section (14 renders, `32552a6`), a Full Ecosystem/hypothetical-completion section (8
  renders, `e527441`), and a Parcel A pond water-source update (`fdd22a3`) — all pushed to
  `origin/main`, nothing local-only. The prior "unconfirmed since 2026-08-13" framing was stale.
- **2026-10-18/19: full-site cross-link audit + fixes, 3 commits (`39e5778`, `fc4bf29`, plus the
  Nkap/Apparel decision-sync commit `cb5504e`).** Background-agent audit found cross-page
  references (Ha'bem/PIOS/Terra API/Nkap mentioned by name but not linked across
  `terra_africa_strategy.html`, `roms_gtm_strategy.html`, `pios_strategy.html`,
  `terra_ventures.html`, `terra_nkap.html`) and same-page anchor gaps (every page except
  `index.html` lacked `id` attributes on section headers, so "see X above" text had no real
  target). Fixed: added `id="pilot-status"`/`id="land-water-ops"` anchors + linked the
  Security-Perimeter-section callout's two "see above" references; linked first substantive
  Ha'bem/PIOS/Terra API/Nkap mention per section across 6 files; fixed a real bug in
  `terra_initiative.html` where Nkap entity notes said "see callout below" but the actual detail
  lives on `terra_ventures.html` (now links directly + the real callout got `id="nkap-callout"`);
  linked the private GitHub repo (same self-facing-link precedent as the gated `api.terra-hq.com`
  links elsewhere on that page); fixed the only unlinked card in `terra_initiative.html`'s Tech
  org-chart drill-down (`TERRA ASSEMBLY` was a plain `<div>`, now links to `terra_tech.html`'s
  Fabrication Lab tab, matching the other 3 linked cards in that row).
- **Separately, Nkap/Apparel decisions synced Notion↔site, 2026-10-18 (`cb5504e`).** Nkap: coin
  name confirmed final (not a placeholder); Diamond AND Sapphire tiers now show round-only on
  `terra_nkap.html` (oval variants retired from display, kept in `Assets/coins/`, not deleted) —
  matches a Notion decision originally scoped to Diamond only, extended same-day to Sapphire for
  consistency. Apparel: first drop decided as a mixed-pillar, light-garment (t-shirts/dress
  shirts) 5–25-piece test batch (not the full 55-piece run); social-brand positioning decided as
  a recruitment+audience-building mix, not a single goal — both now reflected in
  `terra_apparel.html`'s callout instead of listed as open next actions.
- **2026-10-31:** Agriculture Phase 0 gate and Phase 1 apiary renders shipped (`e5df489`), verified live. An unused 30.5 MiB WhatsApp video stays untracked: over Cloudflare's 25 MiB limit.
- **Next Step:** (1) Generic wording done 2026-10-31 (`0c1d915`, `72ba2ca`): client and financing names and a named relative are off the live pages; a gated home is still later. Git history keeps the old text.
  (2) Migrate the non-sensitive remainder: Tech product status, Ha'bem resort tracker, a Terra
  Finance page taking the PIOS tabs off `terra_ventures.html`. (3) Mark SEC-001 resolved on the
  Register. (4) Move embedded images out of `resortConcept.html` (4.1 MB, mobile). Still open
  from before: 2 missing `resortConcept.html` Gemini images; Jenkins/Ha'bem temp links;
  `terra_nkap.html` pre-existing div imbalance (267/268, not visibly breaking).
- **Blockers:** **terra-hq.com is public** — Cloudflare Access was abandoned (JWT gating covers
  only `api.terra-hq.com/internal`). The migration assumed a gate: Register names Snorkel/NACA
  and Africa family-owned wording stays by Will's choice (2026-10-31). Ops DBs (Contacts,
  Hires, OMS CRM) + Business Banking stay unmigrated until a gated home exists. Pilot home and
  HQ data stack (D1/Workers vs Postgres) undecided.
- **Context:** Full page inventory and page-by-page detail live in `terra-hq-site/CLAUDE.md` —
  this section intentionally stays a pointer rather than re-duplicating page-by-page content
  that already drifted once before (see the Monthly Hub Audit item 3 pattern: duplicated detail
  rots quietly between sessions). THQ-019 (the Terra API card-removal task) and its ALL_TASKS.md
  counterpart were corrected in the same 2026-10-03 pass — the entry previously said "already
  done in substance, no new work needed," which was wrong; both now reflect the actual fix.

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
- **2026-10-31:** `ALL_TASKS.md` moved to `ACTION_PLAN/`. The home repo's GitHub name is now
  `terra-initiative-home` (Bitbucket's is still `terra-api-home`). `pios`, `pios-algo` and
  `will-strategies` now live in the home folder, gitignored, no remotes. Bitbucket blocks this machine's
  Git Credential Manager version (2.6.1, bundled with Git 2.51.2) on 2026-11-30 (Notion task). terra-api, terra-api-fe
  and terra-jenkins Bitbucket mirrors were 0/0 with their branches on 2026-10-31. Git is now 2.56.0 but GCM only 2.9.1;
  needs 3.0.0+ (`winget install --id Git.GCM -e`). `test` machine is behind this one (Will): pull there; pios repos have
  no remotes. Credential CSVs sit in the laptop's Drive-synced `Programing` folder, unopened: SEC-001 isn't closed.
- **Terra Finance vs. Terra Ventures — confirmed distinct, 2026-10-06 (re-checked Notion directly
  after Will asked "was Terra Finance retired?").** They are NOT the same entity and neither
  supersedes the other: **Terra Finance** = live, active — PIOS, trading, capital governance
  (via Investment Hub); **Terra Ventures** = separate, not-yet-formed Rung 3 placeholder for
  external investing/acquisitions, Nkap sits under it. A 2026-06-18 Notion edit had briefly
  renamed "Terra Finance" → "Terra Ventures" as if they were one thing — that merge was
  superseded 2026-08-30 (reaffirmed 2026-09-28), per Notion's own "Terra Ventures" page history.
  The visualizer's `Finance` cube (plain label, no "Terra" prefix, matching every other cube's
  naming convention) already correctly represents Terra Finance — confirmed correct as-is,
  no rename needed. Will separately considered folding Solar into Tech and using that freed
  8th cube slot for something else, but explicitly held off — **current 8-cube list (Tech,
  Real Estate, Finance, Ventures, Agriculture, Apparel, Fabrication, Solar) stays as-is.**
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
  committed since; `terra-hq-site`'s tracked files are clean as of 2026-10-31.
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
- **Status:** Active — hub v2.4; `load hub` and `sync` both exercised in Claude Code 2026-10-31.
- **Active Task:** SKILLS-006 — dogfood the CLAUDE.md pointer's auto-activation (not re-checked here; this
  session used the explicit `load hub` trigger).
- **Next Step:** Open a fresh Claude Code session in a repo with the pointer and confirm it activates.
- **Blockers:** None
- **Context:** Rewritten 2026-10-31: the old text still said hub v1.1 with uncommitted fixes. Git =
  sole source of truth for ai-control; Notion = informational dupe only.

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
