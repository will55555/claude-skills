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
      freshness stamps bumped to v1.1, trigger naming partial mitigation (done — uncommitted)
- [x] SKILLS-011 — Append the 2026-07-09 entry to claude-skills root DEV_LOG.md (done)
- [ ] SKILLS-012 — Commit + push everything above (`sync skills`)
- [ ] SKILLS-005 — Add CLAUDE.md pointer block to terra-api, roms, pios, terra-hq-site
      (VERIFY actual relative path depth first — see HUB_GUIDE Per-Repo Pointer note)
- [ ] SKILLS-006 — Dogfood: run `load hub tapi` in a fresh Claude Code session, log friction
- [ ] SKILLS-013 — Still-open decision: resolve `sync skills` vs "sync skills to Notion"/
      "deploy" naming collision (partial mitigation applied — dropped `push skills` variant)
- [ ] SKILLS-014 — Still-open risk: Notion's copy of session-context-sync is stale vs tonight's
      edits — update the Notion page, or exclude this skill from the Notion deploy/push flow,
      before anyone runs "deploy"/"pull skills"
- [x] SKILLS-015 — Update root DEV_LOG.md's "Skill inventory" table: dev-log + session-rules
      rows marked ARCHIVED, footnote added explaining ai-control's exclusion (done)

## FM (work-at-home thinking — context only, no proprietary code/internals)
(none yet)
