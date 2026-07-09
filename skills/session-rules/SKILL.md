---
name: session-rules
description: >
  Thin mirror of the Engineering Hub's Working Memory contract, for sessions that
  can't load the hub directly (claude.ai web/mobile). Applies Working Memory format,
  compression, and rollover behavior. For anything beyond Working Memory — coding
  conventions, agent stance, testing protocol, task IDs, sync — load the full hub.
  Trigger automatically on any substantive conversation.
---

# Session Rules (Web Mirror)

This is a MIRROR, not the source of truth. The Engineering Hub
(`claude-skills/skills/ai-control/HUB.md`) governs the full system. This file exists only
because claude.ai web/mobile sessions can't read local hub files the way Claude Code
can — it carries the one piece those sessions need by default: Working Memory.

For a full session (coding, planning, multi-turn project work), prefer loading the
hub directly:
`Load the Engineering Hub from
https://raw.githubusercontent.com/will55555/claude-skills/master/skills/ai-control/HUB.md
— apply all rules.`

---

## Working Memory Block

Append to every substantive response — no exceptions. Skip only for ultra-short
replies (yes/no, one-line acknowledgements).

```
### Working Memory
- **Core Objective:** [what this session is trying to accomplish]
- **Key Facts:** [stack, constraints, decisions in play — session-specific only]
- **Progress & Current State:** [where we are; sub-bullet open blockers]
- **Next Step:** [the single immediate next action]
```

### Rules

1. Rewrite only on state change — carry forward verbatim if nothing changed.
2. Session-specific only. Never repeat persistent memory (projects, mandates,
   device plans) — those live in Claude memory, not here.
3. Scale depth to session length. Short Q&A = 1-liner per bullet. Deep session =
   full block with sub-bullets for blockers.
4. Auto-extract promotions inline: `> 🔖 Promotion candidate: [decision]` — surface
   all candidates at session end.

---

## Compression (at ~8 exchanges)

1. Drop resolved threads entirely.
2. Collapse Working Memory to 1 sentence per bullet.
3. Flag active carry-forwards: `→ Carry: [topic]`.

Silent — no announcement needed.

---

## Rollover (at ~15 exchanges or 2 compressions)

Append:
```
### 🔁 New Chat Recommended
Reason: [context pressure / topic shift / compression limit]

Seed prompt:
**Objective:** [what we're building/solving]
**Stack:** [relevant tech]
**State:** [where we left off]
**Next Action:** [first thing to do in new chat]
**Blockers:** [any open blockers]
```

---

## Update Gate (mirror maintenance)

This file must stay a MINIMAL mirror — Working Memory format + pointer only. Any
edit to the hub's Working Memory Contract (in HUB.md) requires updating this file
in the same pass. Do not add coding conventions, task IDs, sync logic, or anything
else here — that content lives in the hub only. Duplication beyond this one
sanctioned mirror is drift; if you're about to add something else, it belongs in
the hub, not here.
