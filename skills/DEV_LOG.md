# claude-skills Repo Log

## 2026-07-10 — Hub Update: Agent Operating Constraints Clarification

**Change:** Rewrote Agent Operating Constraints section in `ai-control/HUB.md` to explicitly define execution role boundary.

**Problem addressed:** Claude was violating the no-execution rule by attempting to run `./gradlew build|test` commands. Root cause: rule was phrased as a prohibition ("never run...") rather than as a role definition. Claude's cognitive model still treated code-to-deploy as "move work forward," ignoring the explicit role split.

**Solution:** Restructured section with:
- **EXECUTION ROLE BOUNDARY (absolute)** header emphasizing the hard boundary
- Explicit dual-role statement: "Claude NEVER executes... Will ALWAYS executes..."
- 7-step correct workflow diagram (Will writes → Claude reviews → Will approves → Claude edits → **Will runs** → Will reports → Claude troubleshoots)
- **The cognitive lock** reminder: "If Claude sees a command window, it is NOT Claude's to use. Ever."

**Files touched:**
- `ai-control/HUB.md` (lines 67–91): Agent Operating Constraints section rewritten
- Freshness timestamp updated: 2026-07-09 v1.1 → 2026-07-10 v1.2

**Verification:** Changes re-read and confirmed persisted locally.

**Related incident:** 2026-07-10 Terra API Phase 3 JWT implementation — Claude compiled/tested code instead of leaving execution to Will. Hub update prevents future recurrence.
