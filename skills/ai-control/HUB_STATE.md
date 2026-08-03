# Engineering Hub State
<!-- Freshness: 2026-08-02 (rev 39) | v1.3 | Snapshots only — overwritten in place. History lives in DEV_LOGs. -->
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
- **Status:** Active — prod healthy (recovered 2026-07-29 under TAPI-013; the "prod DOWN ~26h"
  text above was already stale before today). 2026-08-01: found + fully remediated a credential
  leak in terra-api's git history (see Context).
- **Active Task:** **ADR-009 Phase 3 + ADR-003 Tier 1 both shipped 2026-08-02.**
  Phase 3 (`5e79627`+`e590c92` on `master`): `GET /api/v1/ecosystem/health` — the customer-facing
  twin of `/actuator/ecosystem-health`, on the API port because the management port is
  deliberately unpublished. New DTO, not a filtered copy: the operator shape splits services
  across `services`/`quarantined` without carrying tier, and cannot express a service that is
  entitled but has never sent a heartbeat.
  Tier 1 (`51040a1` on **`phase-8-customer-identity`**, pushed both remotes, NOT yet merged):
  `customers` + `customer_identities` tables, BCrypt local login, ADR-010's `role` claim threaded
  end-to-end but enforced nowhere, dev-only seed. **Verified end-to-end against live Postgres**,
  not just unit-tested: login returns `sub=cust_dev_001` / `role=customer`, and the health
  endpoint returns both entitled services as `running:false` with `tier` omitted — exactly the
  grey/navy off-state ADR-009's visualizer expects. 74 tests green.
  Earlier: TAPI-013 DONE (`dcf7d6a`), TFE-201 DONE (FE wired into Jenkins CI).
- **Next Step:** (a) **Merge `phase-8-customer-identity` → `master`** — note that merging master
  is itself the prod-deploy trigger per the Jenkinsfile's "merge IS the approval" gate, and this
  one carries a schema change (two new tables) that will run against the prod database;
  (b) **ADR-009 Phase 4** — the visualizer, on `phase-4-visualizer` in terra-api-fe (branch cut,
  empty). Now has a real contract to mock against rather than a guess; (c) ADR-003 Tier 2
  (Google sign-in via `POST /api/auth/social`) whenever a customer actually wants it.
- **Blockers:** None. Two carried items, neither blocking: `docker-prod.env` /
  `docker-staging.env` on the EC2 box still need `SPRING_PROFILES_ACTIVE=prod`/`staging` (until
  then the dev seed is kept out of prod by `application-dev.yaml` being gitignored — safe, but by
  file-absence rather than by declaration); and Phase 3's work went **straight to `master`**
  without a branch/PR, contrary to the project's own convention — Tier 1 corrected that by using
  `phase-8-customer-identity`.
- **Context:** **Credential incident (2026-08-01):** a Notion API key was committed live in
  terra-api's `.env` since 2026-07-05 and copied into `DEV_LOG.md` 2026-07-26. Rotated by Will;
  scrubbed from git history via two `git-filter-repo` passes (2nd pass needed for a 1-char-shorter
  historic variant the 1st missed), force-pushed to `origin`+`bitbucket`, verified clean via full
  local (incl. unreachable loose objects) + remote history scans. Pre-scrub backup bundle:
  `terra-api-home/terra-api-backup-before-history-scrub-2026-08-01.bundle`.
  Jenkins runs on the `solan` machine (port 8090) until the ADR-010 EC2 migration — not scheduled.
  `terra-api-fe` npm peer-conflict fix verified: `rm -rf node_modules package-lock.json && npm
  install`. Never `npm audit fix --force` there (guts `react-scripts`).
  Still unfixed: missing `feature-flags.yaml`; Spring Security default in-memory password at boot;
  prod/staging no-auth-Redis gap.

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
- **Next Step:** Three gaps, none of them TFE tasks, ranked: (1) **the deploy has never run** —
  ADR-009 Phase 2 wired Jenkins to copy the CRA build into Spring's `static/`, marked done but
  never executed, so nobody can reach this dashboard except locally; (2) **a 401 leaves the user
  on a broken page** rather than redirecting to login (hit twice on 2026-08-02); (3) **10 of 12
  modules have no tests** — only `healthColors` and `domainConfig` (the pure logic) are covered,
  18 tests. Also note the dashboard is feature-complete for a customer base that does not exist
  yet: ADR-011's amendment established there is no real customer identity, so `cust_dev_001` is a
  dev fixture. Deliberate sequencing, but it means shipping has no urgency behind it.
  Deferred by Will 2026-08-02: the ADR-012 admin dashboard.
  (superseded) Confirm the FE image builds clean end-to-end via `docker compose --env-file
  docker.env up --build` from `terra-api-home/` — this has never actually been verified green, only
  the CI-side `npm ci`/build. Then start repurposing the `design-reference/` static HTML into real
  JSX components (dashboard shell, product launchpad card, Nkap tier card, activity ledger).
- **Blockers:** None. Standing caution: **never run `npm audit fix --force`** here — it downgrades
  `react-scripts` to `0.0.0` (empty stub), stripping ~1280 packages and the whole build toolchain
  (hit and reverted 2026-07-28). Still unexamined: stray `package-lock.json;C` / `package.json;C`
  directories in the repo root — harmless so far, worth deleting when someone is in there.
- **Context:** CRA (React 19, plain JS — no TypeScript). Sibling to terra-api + terra-jenkins under
  `terra-api-home` (its own git repo, `will55555/terra-api-home`, dual remote: GitHub + Bitbucket
  `terra-inc-dev/terra-api-fe`). ⚠️ Stack drift flagged 2026-08-01: the 2026-07-16 decision says
  "stays React (Vite)" but the actual repo runs CRA/react-scripts, not Vite — unresolved, not
  re-litigated here.
  **2026-08-01 — UI design direction accepted:** Concept AB "The Command Matrix" — top row: 60/40
  split, scoped 3D topology visualizer (left) + Nkap tier/balance card (right); middle: contextual
  product launchpad (active products full-detail, locked products dashed with status pills);
  bottom: cross-product activity ledger. Nkap 5-tier color mapping: Silver #E2E8F0, Gold
  var(--gold), Platinum var(--teal), Diamond var(--purple), Sapphire var(--blue). Built via Gemini
  iteration as static HTML reference: `terra_dashboard_state_a.html` (today's single-product
  state), `terra_dashboard_state_b.html` (3-product future state), `terra_nkap_tiers.html` (tier
  comparison). Light-mode pass requested, not yet returned — dark is default. Moved into
  `terra-api-fe/design-reference/` (2026-08-01), kept out of `src/`/`public/` so CRA's build
  doesn't touch them. Repurposing into real JSX components (dashboard shell, product launchpad
  card, Nkap tier card, activity ledger + extracted styles/hooks) is a real coding task,
  deliberately deferred until the lockfile blocker is fixed — better done in Claude Code with a
  running dev server than generated blind in chat.

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
- **Reference Links:** Method lives in the hub, not a project doc: HUB_GUIDE → DSA Methodology
  (3-phase flow). Obsidian vault notes under `Learn/Software Development/`. Notion: (none
  recorded — add when confirmed).
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
  agent). **Status: DONE 2026-08-02** — alarm + SNS topic created and confirmed under TAPI-013
  (`dcf7d6a`). This is the first piece of gap (1) actually built; the rest (DB backups, OS
  patching, domains + TLS) remains deferred.

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

