**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Published
**Cycle:** 2026-05-15__scheduled

# Lessons Learnt — Roadmap Rebalance

Feature / Trigger: Scheduled rebalance — no completion event
Run: 2026-05-15__scheduled
Reviewed by: PMO Lead
Date filed: 2026-05-15
Prior cycle checked: 2026-05-13__scheduled

---

## What worked well

- Action-now patch application was clean: the deferred patch from 2026-05-13__scheduled (STEP 9 post-write park count verification) was confirmed by Head of Specs Team and applied this run without friction. The carry-forward mechanism worked as intended — the patch target was correctly identified as "this run".
- Gate-condition re-checks (STEP 4.0) were efficient: 3 ideas evaluated against shipped backlog items in one pass. All three resolutions were unambiguous (BLG-FE-22 ✅ v3.4, PT-03 ✅ v3.2, BLG-QA-15+PT-03+PT-05 ✅).
- ideas_register.md updates were completed cleanly via a single Python script pass — 35 row updates with no missed increments and no truncation artifacts.
- STEP 8.5.B write plan documented in run_manifest.md before any canonical writes began; all 13 files were executed in order against the plan.

---

## Friction Log

---

### Friction Item 1

**Classification:**
- Type D — Cognitive Fatigue: A detail was missed due to prompt length, context overload, or accumulated complexity

**Recurrence:** Yes — appeared in 2026-05-13__scheduled (deferred patch: STEP 9 post-write park count grep); and in 2026-05-08__scheduled (F-01: park counts not incremented for STEP 5 parked ideas)

**What happened:**
The deferred patch from 2026-05-13__scheduled identified a recurring problem: context compaction during STEP 9 ideas_register.md writes could leave stale park counts. The patch was deferred in that cycle with target "next run of roadmap rebalance routine." This cycle the patch was confirmed action-now by Head of Specs Team and applied to roadmap_prompt.md STEP 9 (v6.0 → v6.1). The session resumed after context compaction in the prior session and successfully applied all 35 row updates using a Python script approach that is inherently resistant to truncation artifacts.

**Where in the routine:**
STEP 9 — Canonical writes (ideas_register.md park count updates); STEP 11 — action-now patch application

**Root cause:**
Context window pressure during extended STEP 9 write passes. Root cause addressed by the STEP 9 post-write grep verification instruction now in roadmap_prompt.md v6.1.

**Blast radius analysis:**
- What would have propagated: If the deferred patch had not been applied, another cycle of potential stale park counts under context compaction.
- When it would have surfaced: At the subsequent roadmap rebalance (third consecutive occurrence).
- Recovery cost if uncaught: Low — single-file fix at next cycle; but third occurrence would trigger mandatory escalation (§3.7 two-cycle deferred patch rule).

**Process patch:**

→ Immediate patch applied this run:
  - File: `claude/system/roadmap_prompt.md`
  - Section: STEP 9 Canonical Write — after Decision log append-only enforcement block
  - Change: Added **Post-write park count verification** instruction: after completing ideas_register.md park count updates, grep for rows with prior cycle's `Parked-cycle-N | N` values and confirm zero rows remain with outdated counts.
  - Version: v6.0 → v6.1
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Yes — appended to claude/system/prompt_change_log.md

---

## Recurrence Escalations

| Friction item | First appeared | Prior outstanding action | Escalated to |
|---------------|---------------|--------------------------|-------------|
| Register park count undercount under context compaction | 2026-05-08__scheduled (F-01) | 2026-05-13__scheduled: deferred patch with owner + target filed | No escalation — deferred patch resolved this run (action-now applied); recurrence chain closed |

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/roadmap_prompt.md` | STEP 9 — after decision log enforcement block | Post-write park count verification instruction added | v6.0 → v6.1 | Yes |

---

## New files created this run

None.

---

## Outstanding deferred patches

None.

---

## Escalations

None.

---

## Carry-Forward

Items: 0

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| — | — | — | — |

---

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-05-15__scheduled",
  "phase": "Roadmap",
  "filed_utc": "2026-05-15T00:00:00Z",
  "friction_item_count": 1,
  "action_now_count": 1,
  "deferred_count": 0,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
