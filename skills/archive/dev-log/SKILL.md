---
name: dev-log-ARCHIVED
description: |
  ARCHIVED — superseded by the Engineering Hub's Documentation Protocol
  (claude-skills/skills/ai-control/HUB_GUIDE.md). Do not trigger this skill. Kept
  for schema reference only. If you are Claude and considering triggering on this
  file, stop — load the Engineering Hub instead (`load hub`) and use its
  Documentation Protocol section, which contains the same Phase Log / Repo Log
  schemas plus the hub's completion-trigger and preview rules.
---

# Dev Log Skill

Generates or updates a `DEV_LOG.md` for a project. The output is a living
engineering reference — recipe-style, decision-driven, transferable to any machine
or future collaborator. It is NOT a commit history or a task tracker.

---

## Core principle

**WHY over WHAT.** File names and git diffs already tell you what changed.
A dev log tells you:
- Why this approach was chosen over alternatives
- What constraints or tradeoffs drove the decision
- How to reproduce a setup step on a new machine
- What broke and why — root cause, not just the fix
- What the next phase looks like

If a section only describes WHAT happened and not WHY, it belongs in a commit
message, not a dev log.

---

## Two modes

### Mode 1 — Phase Log (active project)

Use for: ROMS, PIOS, or any feature-driven software project.
File location: repo root → `DEV_LOG.md`, or named per concern
(e.g. `FRONTEND_DEV_LOG.md`, `CI_CD_DEVLOG.md`).

Each entry is a **Phase** — a meaningful unit of work (not a calendar day).
Phases can span multiple sessions or multiple phases can happen in one session.

#### Phase entry schema

```markdown
## Phase N — [Phase Name]

**Date:** YYYY-MM-DD
**Status:** Complete | In Progress | Blocked

### Goal
[One paragraph: what this phase accomplishes and why it was the right next step]

### Architecture / Concept Summary (if new concepts introduced)

| Concept | What It Does | Analogy |
|---|---|---|
| [term] | [plain explanation] | [Spring Boot / familiar analogy] |

### Key Design Decision: [Decision Title]
[Why this approach over alternatives. Name the alternatives considered.]

### Files Created / Modified

**`path/to/file.ext`** *(new | updated)*
[What this file does and why it was structured this way]

### Setup / Recipe (if reproducible steps required)
[Step-by-step commands with WHY comments on non-obvious steps]

### Build / Test Result
[Pass/fail + any warnings worth noting]

### Known Limitations / Next Phase
[What's intentionally deferred and why]
```

#### Bug / error entry schema (insert within the relevant phase or as its own Phase N+1)

```markdown
### Error — [Short Description]

**Where it appeared:** [Stage / file / test]

**Full error:**
```
[paste the actual error]
```

**Root cause:**
[Explain WHY this happened — not just what the error said]

**Fix:**
[What changed and why this fix works]

**Why this approach and not [alternative]:**
[If there were other obvious fixes, explain why they were rejected]
```

---

### Mode 2 — Repo Log (tool / infrastructure repo)

Use for: claude-skills, dotfiles, infra repos, or any repo that IS the tool
rather than building a product.
File location: repo root → `DEV_LOG.md`.

Not phase-based. Sections are permanent reference entries.

#### Repo log schema

```markdown
# [Repo Name] Dev Log

## [Date] — [Session title]

### What this is and why it exists
[One paragraph: purpose, motivation, what problem it solves]

### How to [key operation 1]
[Step-by-step recipe with WHY comments]

### How to [key operation 2]
[Step-by-step recipe with WHY comments]

### [Inventory / Reference table]
| Item | Purpose / Notes |
|---|---|

### Design decisions worth knowing
**Why [decision]?**
[Rationale + tradeoffs]

**Why [decision]?**
[Rationale + tradeoffs]
```

---

## Step 1 — Determine mode and gather context

Ask (or infer from context):

1. **Mode:** Is this an active feature project (Phase Log) or a tool/repo (Repo Log)?
2. **Source material:** What's available?
   - Git log (`git log --oneline`)
   - Existing Obsidian notes for this project
   - Current session context (decisions made, errors fixed, files changed)
   - Existing `DEV_LOG.md` (update vs. create)
3. **Scope:** All phases to date, or just this session?

For Phase Logs, always read existing Obsidian project notes first — they often
contain the richest decision context (see ROMS `Projects/ROMS/` notes as reference).

---

## Step 2 — Show preview before writing

```
📋 Dev Log Preview

Mode: [Phase Log / Repo Log]
File: [path/to/DEV_LOG.md]
Action: [Create new / Prepend phase / Update section]

Content preview:
[first 10–15 lines of what will be written]
...

Proceed? (yes / edit first / skip)
```

---

## Step 3 — Write or update

**Creating new:** Write full file.

**Updating — Phase Log:** Prepend the new phase(s) above existing entries.
Never overwrite existing phases — the log is append-only going backward.

**Updating — Repo Log:** Update the relevant sections in-place.
Add a new dated session block if the session produced new decisions.

---

## Quality bar

Before writing, ask for each section:

- [ ] Does it say WHY, not just WHAT?
- [ ] If a command is included, is there a comment explaining non-obvious flags?
- [ ] If a package/library was chosen, are the alternatives named and rejected?
- [ ] If something broke, is the root cause explained (not just the fix)?
- [ ] If an analogy exists that makes the concept stick, is it included?
- [ ] Could someone reproduce this setup on a fresh machine from this log alone?

If any answer is no, fill in the missing context before writing.

---

## Analogies

When the project stack involves a technology the developer knows well, use it as
an anchor for new concepts. Examples from ROMS:

| New concept | Familiar anchor |
|---|---|
| React Router | Spring `@RequestMapping` / `DispatcherServlet` |
| Redux Store | Singleton `@Service` in ApplicationContext |
| `useEffect` | `@PostConstruct` |
| WebSocket STOMP | Kafka `@KafkaListener` |
| `useRef` | A pointer variable — holds a reference, not a value |

When writing for Will: Spring Boot / Java is the familiar anchor for frontend
concepts. Use it when introducing React, Node, or browser-native APIs.

---

## File placement

| Project type | Dev log file | Location |
|---|---|---|
| Full-stack project | `DEV_LOG.md` | repo root |
| Separate FE/BE concerns | `FRONTEND_DEV_LOG.md`, `BACKEND_DEV_LOG.md` | repo root |
| CI/CD / infra | `CI_CD_DEVLOG.md` | repo root or `Infra/` |
| Tool / skills repo | `DEV_LOG.md` | repo root |

After writing: remind Will to `git add DEV_LOG.md && git commit -m "docs: update dev log"`.
