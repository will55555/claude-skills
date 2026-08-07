# Non-Repo Task Catch-All
<!-- For projects with no repo of their own (no per-project TASKS.md home). -->
<!-- Repo projects (Terra API, ROMS, PIOS, terra-hq-site) keep TASKS.md at their own root. -->

## DSA
- [ ] DSA-001 — Arrays: first problem (3-phase methodology, Java default)

## SKILLS (claude-skills / Engineering Hub)
- [x] SKILLS-001 — Draft Engineering Hub v1 (HUB.md, HUB_GUIDE.md, HUB_STATE.md)
- [x] SKILLS-002 — Draft satellite edits (session-rules mirror, session-context-sync Step 4C)
- [x] SKILLS-003 — Deploy: place all files in claude-skills repo (done — placed at skills/ai-control/)
- [x] SKILLS-004 — Archive dev-log skill to `claude-skills/skills/archive/dev-log/` (done)
- [x] SKILLS-007 — Fix path refs (ai-control/ → skills/ai-control/ throughout) (done)
- [x] SKILLS-008 — Neutralize dev-log frontmatter (prevent trigger collision) (done)
- [x] SKILLS-009 — Found + archived duplicate session-rules skill (was in "New folder/", same
      `name: session-rules` as active skill, drifted Notion IDs, old WM format) (done)
- [x] SKILLS-010 — Applied Patches 1–4 + Findings A–H: Sync Queue, git-authority rule,
      CLAUDE.md pointer depth fix, dev-log-location fix, hardcoded-path genericization,
      freshness stamps bumped to v1.1, trigger naming partial mitigation (done — pushed 2026-07-09)
- [x] SKILLS-011 — Append the 2026-07-09 entry to claude-skills root DEV_LOG.md (done)
- [x] SKILLS-012 — Commit + push everything above (`sync skills`) (done — pushed 2026-07-09)
- [x] SKILLS-005 — Add CLAUDE.md pointer block to terra-api, roms, pios, terra-hq-site (done
      2026-07-09 — terra-api: `../../` (double-nested, appended to existing rich CLAUDE.md);
      terra-hq-site: `../` (appended to existing rich CLAUDE.md); ROMS
      (restaurant-order-management-system): `../` (NEW minimal CLAUDE.md created, none existed);
      PIOS skipped, no repo exists yet)
- [ ] SKILLS-006 — Dogfood: run `load hub tapi` in a fresh Claude Code session, log friction
- [x] SKILLS-016 — RESOLVED 2026-07-09: fetched ADR-003 directly from Notion — confirms
      self-issued JWT on master, Terra Auth provisioned-not-built, activates on 2nd identity
      consumer ("Issuer Model — Resolved 2026-07-08"). Memory was correct; terra-api's local
      CLAUDE.md was stale (2026-07-07 blocker never updated). Fixed CLAUDE.md (Open Blockers,
      Key Decisions Log, Next Action) and HUB_STATE's TAPI section to match ADR-003.
- [x] SKILLS-017 — RESOLVED 2026-07-09 (found during re-audit): two real operational bugs caught
      by re-reading files after editing them, not just trusting tool success:
      (a) ROMS's CLAUDE.md was created with the wrong tool (sandbox `create_file`, not
      `Filesystem:write_file`) — file never actually existed on Will's machine despite SKILLS-005
      marking it done. Recreated correctly, verified present.
      (b) terra-api's SKILLS-016 CLAUDE.md fix reverted silently sometime after the edit tool
      confirmed success — root cause unconfirmed (initially misattributed to OneDrive sync race;
      Will clarified the "OneDrive" folder name is legacy only, no active cloud sync on this
      machine, so that theory is wrong — corrected in HUB.md/HUB_GUIDE.md). Redone in 3 smaller
      edits, re-verified present this time. Added both lessons as standing rules to HUB.md's Agent
      Operating Constraints (correct tool for real writes; verify-by-reread regardless of cause).
- [x] SKILLS-013 — RESOLVED 2026-07-09: renamed `sync skills` → `sync hub` (structural fix, not
      a managed bare-vs-qualified distinction — zero phrase overlap with "sync skills to
      Notion"/"deploy"/"push to Notion"). Updated HUB.md (trigger, Trigger Map row, commit
      message example) and HUB_GUIDE.md (Copy/Paste Commands).
- [x] SKILLS-014 — RESOLVED 2026-07-09: `session-context-sync` permanently excluded from the
      Notion deploy/push flow (too tightly coupled to hub-specific design to dual-author safely).
      Updated root DEV_LOG.md's Skill inventory table and the skill's own SKILL.md with explicit
      exclusion notes. "deploy"/"pull skills" will no longer touch this file.
- [x] SKILLS-015 — Update root DEV_LOG.md's "Skill inventory" table: dev-log + session-rules
      rows marked ARCHIVED, footnote added explaining ai-control's exclusion (done)

## FM (work-at-home thinking — context only, no proprietary code/internals)
(none yet)

## Queued for later sync / Notion
- [ ] ROMS-001 — Expand the ROMS integration task into a full deploy-and-heartbeat checklist for Terra API / public visualizer integration.
- [ ] ROMS-002 — Migrate ROMS Jenkins to the shared Terra Jenkins EC2 before ROMS redeployment.

## Security (not project-specific — general hygiene follow-ups)
- [ ] SEC-001 — Move exposed plaintext credentials into a password manager (Bitwarden or Proton
      Pass — both free-tier viable, Bitwarden slightly favored for CLI/dev workflow fit), then
      delete the plaintext copies:
      - `C:\Users\solan\OneDrive\Desktop\SDE\Github PAT key.txt`
      - `C:\Users\solan\OneDrive\Desktop\SDE\s3-ROMS-local_accessKeys.csv`
      - `C:\Users\solan\OneDrive\Desktop\SDE\s3-ROMS-local_credentials.csv`
      (Note: the copies of these files INSIDE `restaurant-order-management-system\` are already
      gitignored — lower urgency there. These three are the ones sitting unprotected at bare
      SDE root, outside any repo.)
