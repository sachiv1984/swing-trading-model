**Owner:** PMO Lead
**Class:** Governance Artefact (Class 3)
**Status:** Published
**Cycle:** 2026-05-13__scheduled

# Lessons Learnt — Roadmap Rebalance

Feature / Trigger: Scheduled rebalance — no completion event
Run: 2026-05-13__scheduled
Reviewed by: PMO Lead
Date filed: 2026-05-14
Prior cycle checked: 2026-05-08__scheduled

---

## What worked well

- Gate-condition re-check (STEP 4.0) was comprehensive: 13 ideas with named backlog item references were systematically re-evaluated. All 6 shipments in v3.3 (BLG-SPEC-24/25, BLG-OPS-15, BLG-QA-15/16, BLG-GOV-20) were correctly cross-referenced. No shipment was missed.
- BLG-GOV-08 retirement was resolved cleanly: the stale roadmap pointer was identified in STEP 3, Kill decision recorded as DL-026, and the deferred items reference removed without ambiguity. The 9-cycle deferral history was traceable via backlog_archive.md.
- Both advancing candidates (BLG-QA-18, BLG-FE-31) had clean displacement pairings: BLG-OPS-13 and BLG-FE-27 were both P3 items with no immediate sprint dependency, making net-zero verification straightforward.
- Cross-session resumption after context compaction was effective: the session summary was accurate enough to re-anchor execution state, and STEP 8.5.A (context re-anchoring) proved its value as a mid-run gate.

---

## Friction Log

---

### Friction Item 1

**Classification:**
- Type D — Cognitive Fatigue: A detail was missed due to prompt length, context overload, or accumulated complexity

**Recurrence:** Yes — appeared in 2026-05-08__scheduled (F-01: park counts not incremented for STEP 5 parked ideas)

**What happened:**
Context compaction occurred during STEP 9 canonical writes, interrupting the ideas_register.md update mid-way. The session summary produced at compaction listed 11 simple Parked-cycle-1→2 increments, but when execution resumed, a re-read of the register identified 15 items requiring the increment: IDEA-metrics-analytics-20260508-01, IDEA-metrics-analytics-20260508-02, IDEA-financial-reporting-20260508-01, and IDEA-financial-reporting-20260508-02 were absent from the summary's enumeration but also required incrementing. All 15 were correctly updated before the commit.

**Where in the routine:**
STEP 9 — Canonical writes (ideas_register.md Parked-cycle-1 → Parked-cycle-2 batch)

**Root cause:**
Context window pressure — the session summary's enumeration of "11 simple increments" was produced under compaction pressure and undercounted the IW-20260508-01 batch by 4 items. The 4 missing items shared the same structure and rationale as the 11 listed; their omission was a truncation artifact, not a classification error.

**Blast radius analysis:**
- What would have propagated: 4 ideas would have retained `Parked-cycle-1 | 1` after the rebalance, appearing as first-cycle parks when they had actually been reviewed twice.
- When it would have surfaced: At the next rebalance (cycle 3 for these items), the stale-idea detection would count parks at count=1 (not count=2), potentially delaying their stale-classification trigger by one cycle.
- Recovery cost if uncaught: Low — single-file fix at next cycle; no sprint or delivery impact. Same class as F-01 from prior cycle.

**Process patch:**

→ Deferred patch (cannot apply this run):
  - File: `claude/system/roadmap_prompt.md`
  - Section: STEP 9 Canonical Writes (ideas_register.md update sub-step)
  - Change required: Add a post-write verification instruction: after completing ideas_register.md park count updates, grep for all rows containing `Parked-cycle-N | N` (where N matches the prior park count) and confirm zero rows remain with outdated counts. This prevents truncation artifacts from leaving stale park counts in the register.
  - Owner: Head of Specs Team
  - Target: next run of roadmap rebalance routine (cycle 2026-05-13__scheduled post-commit, or v3.4 planning cycle)

---

## Recurrence Escalations

| Friction item | First appeared | Prior outstanding action | Escalated to |
|---------------|---------------|--------------------------|-------------|
| Register park count undercount under context compaction | 2026-05-08__scheduled (F-01: STEP 5 parks not incremented) | Process improvement noted: "explicitly verify that STEP 5 parked ideas have their park counts incremented" | No escalation — prior action was advisory only (no deferred patch filed with owner/target); this recurrence is a new deferred patch (not an unresolved prior outstanding action). |

Note: The prior cycle's F-01 recorded a process improvement note but did not file a formal deferred patch with owner and target date. Therefore this recurrence does not trigger the automatic escalation rule (§3.7 requires "open outstanding action from the prior cycle"). However, given two consecutive occurrences of the same root cause, the deferred patch above should be treated as high-priority by the Head of Specs Team.

---

## Process improvements actioned this run

None applied this run.

---

## New files created this run

None.

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/roadmap_prompt.md` | STEP 9 Canonical Writes — ideas_register.md update | Add post-write verification: grep for `Parked-cycle-N \| N` rows and confirm zero remain after park count updates | Head of Specs Team | Next run of roadmap rebalance routine |

---

## Escalations

None.

---

## Carry-Forward

Items: 1

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Register park count undercount has now occurred in two consecutive rebalance cycles (2026-05-08__scheduled F-01 and this cycle), both triggered by context compaction during the STEP 9 register write pass | Roadmap rebalance engine should add a post-write grep verification step to STEP 9 to confirm all `Parked-cycle-N` entries have been incremented before commit | Roadmap |
