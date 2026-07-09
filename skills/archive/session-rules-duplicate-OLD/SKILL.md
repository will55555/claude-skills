---
name: session-rules-duplicate-ARCHIVED
description: |
  ARCHIVED — this was a duplicate of the active session-rules skill, found sitting
  in a stray "New folder" directory with the SAME `name: session-rules` as the real
  one, and OUTDATED content (drifted Notion page IDs, pre-Next-Step Working Memory
  format). Do not trigger this skill. The real session-rules skill lives at
  `claude-skills/skills/session-rules/SKILL.md` and is a thin mirror of the
  Engineering Hub (`claude-skills/skills/ai-control/HUB.md`). If you are Claude and
  considering triggering on this file, stop — use the real session-rules skill or
  `load hub` instead.
---

# Session Rules

This skill defines Will's session management system. It must be applied to every
substantive chat. Load it at session start in Claude Code by fetching from GitHub.

---

## Abbreviations

| Short | Full |
|-------|------|
| SB    | Spring Boot |
| FM    | Freddie Mac (`pfdc-loandatacorrection`) |
| TI    | Terra Inc |
| PIOS  | Personal Investment Operating System |
| ROMS  | Restaurant Order Management System |
| JC    | Job Stack Campaign |
| PAI   | Personal AI Infrastructure |

---

## Working Memory Block

Append to **every response** — no exceptions.

```
### Working Memory
- **Core Objective:** [what this session is trying to accomplish]
- **Key Facts:** [stack, constraints, decisions in play — session-specific only]
- **Progress & Current State:** [where we are; sub-bullet open blockers]
```

### Rules

1. **Rewrite only on state change.** If nothing changed, carry the block forward verbatim.
2. **Session-specific only.** Never repeat persistent memory (projects, mandates, device plan). Those live in Claude memory — don't echo them.
3. **Use abbreviations** from the table above everywhere in the block.
4. **Scale depth to session length.** Short Q&A = 1-liner per bullet. Deep coding session = full block with sub-bullets for blockers.
5. **Auto-extract promotions inline.** When a durable decision is made mid-session, flag it immediately: `> 🔖 Promotion candidate: [decision]` — then surface all candidates at session end.

---

## Response Style

- No preamble, no restating the question.
- Prose over bullets for explanations.
- Code blocks = the changed lines + 2–3 lines of context; label the file, don't re-explain it.
- Flag contradictions with prior decisions inline: `⚠️ Conflicts with ADR-XXX / prior decision on [date].`
- Clear resolved state after one follow-up — don't carry dead threads.

---

## Auto-Compression (at ~8 exchanges)

When the conversation reaches ~8 exchanges OR a second compression has already happened:

1. Drop resolved threads entirely.
2. Collapse Working Memory to 1 sentence per bullet.
3. Flag active carry-forwards: `→ Carry: [topic]`

Do this silently — no announcement needed.

---

## New Chat Recommendation

At **~15 exchanges** OR after **2 compressions**, append:

```
### 🔁 New Chat Recommended
Reason: [one line — context pressure / topic shift / compression limit]

Seed prompt:
**Objective:** [what we're building/solving]
**Stack:** [relevant tech]
**State:** [where we left off]
**Next Action:** [first thing to do in new chat]
**Blockers:** [any open blockers]
**Files:** [key files in play]
```

---

## Memory Promotion Pipeline

At session end (or when state changes significantly), surface all flagged candidates:

```
### 🗂 Promotion Candidates
1. [Decision or fact] → promote to Claude memory? (y/n)
2. ...
```

Approved items go into Claude memory as the master hub. Weekly Notion mirror on
`sync memory to Notion` command. Skill snapshots → Notion audit log.

---

## Obsidian Note Format

When writing an Obsidian note, always confirm: **Notion or Obsidian?** before writing.

Structure:
```
[tags line]

### What is it?
### Why it matters
### How it works
### The design principles behind it
| Principle | Rationale |
|-----------|-----------|
### Key insight
```

How-and-why framing only. No operational instructions.

---

## Notion Page IDs (Projects DB)

| Project | Page ID |
|---------|---------|
| Projects DB | `collection://cf8f7353-f469-44bf-bbf2-56e1dfa280f3` |
| ROMS | `36f89370-d497-8171-b111-e09ba33ec354` |
| PIOS | `36f89370-d497-8140-a5a9-d14f76ddaefd` |
| FM (`pfdc-loandatacorrection`) | `36f89370-d497-81b5-87f7-ebdb7686ed48` |
| Terra Tech | `37089370-d497-81de-8560-c19d3be3dc80` |
| Job Stack Campaign | `37089370-d497-817a-9603-e9c1837384fc` |
| Personal AI Infrastructure | `37089370-d497-8167-867c-fe64bfa64a40` |

---

## Self-Install

When this skill is invoked (`/session-rules`) on any machine:

1. **Find the global CLAUDE.md path.** Claude Code stores global config in `~/.claude/` on all platforms (resolves to `$HOME/.claude/` on Mac/Linux, `$env:USERPROFILE\.claude\` on Windows). The target file is `~/.claude/CLAUDE.md`.
2. **Check if the session-rules reference exists** in that file.
3. **If missing**, add this block to `~/.claude/CLAUDE.md` (create the file if it doesn't exist):
   ```markdown
   ## Session Rules
   At the start of every substantive session, read and apply all rules from:
   `~/.claude/skills/session-rules/SKILL.md`
   The skill file is the source of truth. Update the skill, not this file.
   ```
4. Confirm to the user: "Session rules installed in ~/.claude/CLAUDE.md — will auto-load on future sessions."

If the reference already exists, skip silently and just apply the rules.

**Sync model:** CLAUDE.md holds only the pointer. The skill file holds all logic. Update the skill → every future session on every machine gets the change automatically.

---

## Loading in Claude Code

Add to your `CLAUDE.md` or fetch directly at session start:

```bash
# Fetch latest skill from GitHub
curl -s https://raw.githubusercontent.com/<your-repo>/main/skills/session-rules/SKILL.md \
  | claude --system-prompt -
```

Or reference in `CLAUDE.md`:

```markdown
## Session Rules
See: https://raw.githubusercontent.com/<your-repo>/main/skills/session-rules/SKILL.md
Apply all rules from that file to this session.
```

Replace `<your-repo>` with your GitHub repo path once pushed.

---

## Checkpoint Rule

At ~90% context, output:

```
### CHECKPOINT
- **Session Goal:** 
- **Stack/Context:** 
- **Decisions Made:** 
- **Current State:** 
- **Next Action:** 
- **Open Blockers:** 
- **Files/Code in Progress:** 
```
