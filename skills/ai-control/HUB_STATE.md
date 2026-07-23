# Engineering Hub State
<!-- Freshness: 2026-07-23 (rev 26) | v1.3 | Snapshots only — overwritten in place. History lives in DEV_LOGs. -->
<!-- New project? Copy the template from HUB_GUIDE.md → HUB_STATE Section Template. -->

## Terra API                                        <!-- prefix: TAPI -->
- **Status:** Active — TAPI-012 (Ecosystem CI/CD) Done, live-verified 2026-07-20. Full
  pipeline green end-to-end on `phase-6-cicd`: Checkout → Build → Test → Build Docker Image
  → Push to Docker Hub → Deploy to Staging, containers confirmed `Up` on the real EC2 box.
  Phase 5 (TAPI-011, Redis+Postgres audit log) also Done, live-verified 2026-07-18 on
  `phase-5-redis`.
- **Active Task:** **PR #1 merged 2026-07-23** — `phase-6-cicd-prepr` → `master` (TAPI-011+012
  combined), SonarQube clean beforehand (one justified/suppressed `java:S2143` finding). `master`
  now in sync at `534dd1b` across local, `origin` (GitHub), and `bitbucket` — confirmed identical on
  all three. `phase-6-cicd-prepr` retired everywhere (local + both remotes); `phase-6-cicd` (original,
  untouched) stays per the pre-PR convention.
- **Next Step:** **Resolved 2026-07-23** — `master` didn't auto-trigger `terra-api-pipeline` on the
  merge push because it was genuinely new to that job's branch list (Jenkins was set up entirely on
  phase branches while `master` sat stale); a one-time manual "Scan Multibranch Pipeline Now" picked
  it up. Not a webhook/polling gap — future `master` pushes should trigger normally like the phase
  branches already do. **No automatic next feature is queued** — re-scope with Will; terra-api-fe
  scaffolding (monorepo subdirectory + same-origin EC2 deploy, architecture resolved 2026-07-22) is
  the leading candidate, not gated on ROMS. PIOS/ROMS integration stay deferred until ROMS is
  actually redeployed. Other open items, none blocking: prod EC2 security-group port (TBD),
  `terra-shared-lib` extraction (deferred), GitHub App `Pull requests`/`Commit statuses` permissions
  (deferred). Full context: terra-api/TASKS.md → TAPI-011/TAPI-012, terra-api/DEV_LOG.md.
- **Blockers:** None
- **Context:** Pre-PR branch convention adopted 2026-07-20 — before merging any phase/feature branch
  to master, cut a separate pre-PR branch first, run SonarQube + cleanup there, keep the original
  phase branch untouched with full history. Applies to all future phase/feature merges. EC2 live —
  `t3.micro`, Ubuntu 24.04, Elastic IP `100.60.61.209`, security group SSH-only (staging
  deliberately internal-only, SSH-tunnel-verified). Jenkins running locally (`localhost:8090`),
  Multibranch Pipeline job `terra-api-pipeline`, GitHub App (`github-app-terra-api`, Contents:
  Read-only) used for checkout instead of a PAT. `Jenkinsfile` fully live (Gradle, single-module,
  image `terra-api-be`, branch-tiered `when` gates, Deploy-to-Staging/Prod both live); only
  frontend stages stay commented out (`terra-api-fe` doesn't exist yet). Full history on
  `phase-6-cicd`, pushed to both remotes. ROMS/Terra Solar status cross-checked against Notion
  2026-07-20, confirmed accurate. **Unresolved, flagged 2026-07-21:** `terra-api-key.pem` sitting
  untracked and un-gitignored in the terra-api repo root (test machine) — awaiting Will's call on
  whether to gitignore it or whether it belongs in the repo at all.

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
