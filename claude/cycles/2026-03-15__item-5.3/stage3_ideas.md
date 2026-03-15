**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-03-15

---

# Stage 3 — Ideas Pool Review

**Cycle:** 2026-03-15__item-5.3
**Date:** 2026-03-15

---

## Intake Status

**STEP -1.6 result:** Idea intake skipped — 30 open ideas (Status: Parked) found in `claude/ideas/submissions/`. Count ≥ 20 threshold. No new intake window opened this cycle.

**Last intake window:** IW-20260304-01 (2026-03-04 — 44 submissions, 22 agents)

---

## Ideas Pool State

### Status Breakdown

| Status | Count | Notes |
|--------|-------|-------|
| Parked (old format — `Status: Parked`) | 30 | Prior to Parked-cycle-N format adoption; treated as Parked-cycle-1 for expiry tracking |
| Advancing / Promoted (stale label) | 12 | Ideas promoted in prior cycles with label not updated; to be corrected to Promoted-Added |
| Rejected | 2 | No action required |
| Active / Window summary | 1 | ideas_window.json or window_summary file |
| **Total files** | **45+** | Including window_summary_IW-20260304-01.md |

---

## Key Ideas for STEP 4 Consideration

### IDEA-head-of-specs-20260304-02 — Spec Coverage Inventory

**Submitter:** Head of Specs Team
**Original window:** IW-20260304-01
**Status:** Parked
**Summary:** Systematic audit of canonical spec sections against implementation coverage. Produces a living inventory identifying coverage gaps.
**STEP 4 recommendation:** **Advance to backlog as BLG-NEW-13**. Strong alignment with governance quality goals; low effort (analysis/documentation work); complements BLG-NEW-11 (Canonical Terms Glossary). No displacement required — backlog-level addition.

---

### IDEA-ai-compliance-20260304-02 — AI Compliance Tracking / Workflow Governance Metrics

**Submitter:** (AI/compliance agent)
**Original window:** IW-20260304-01
**Status:** Parked
**Summary:** Track governance compliance metrics for AI-assisted workflows; audit trail for AI-generated artefact provenance.
**STEP 4 recommendation:** **Re-park (Parked-cycle-2)**. BLG-NEW-04 (AI-Assisted Workflow Governance Policy) covers the intent at the policy level. STEP 8.6 guardrail applies — advancing both would expand governance workload beyond current capacity bounds. Re-park pending clearer distinction from BLG-NEW-04.

---

### All Other Parked Ideas (30 items — bulk disposition)

The 30 remaining Parked ideas from IW-20260304-01 were reviewed at the pool level. All are ideas that were parked in the prior cycle (2026-03-06__item-3.4 or earlier). None meet the criteria for roadmap-level promotion this cycle (v2.0 capacity is committed to 3.5, 4.1b, 4.3, BLG-OPS-01; no roadmap slots available without additional kills).

**Bulk disposition:** Re-park all 30 as Parked-cycle-2 (or increment existing cycle count by 1).

**Note on old-format Parked ideas:** Ideas with `Status: Parked` (no cycle suffix) are treated as first-cycle parks for expiry purposes. Their status will be updated to `Parked-cycle-2` in STEP 8 bulk update to normalise to the current format. This does not count as an expiry cycle — they were already parked once.

**Stale idea expiry check:** No ideas have reached Parked-cycle-3 or above this cycle (all are at Parked-cycle-1 or equivalent). No Product Owner disposition required for cycle-3 expiry.

---

### Stale Advancing/Promoted Ideas (12 items — status correction)

12 files carry the label `Status: Advancing` or `Status: Promoted` from prior cycles where the label was not updated post-promotion. These are ideas that were advanced to the roadmap or backlog in prior roadmap runs (IW-20260304-01 → cycles 2026-03-04__item-3.4 and 2026-03-06__item-3.4).

**Disposition:** Correct status to `Promoted-Added` in STEP 8 bulk update. These ideas served their purpose; their outputs are live roadmap/backlog items.

---

## Ideas Not Advancing to Roadmap This Cycle

No new roadmap-level additions from the idea pool this cycle. The STEP 8 Add (BLG-OPS-01) originates from the backlog (operational observation), not from the idea pool.

One backlog-level addition (BLG-NEW-13) advances from the idea pool. This does not require a roadmap-level Kill.

---

## STEP 4 Summary

| Idea | Disposition | Action |
|------|------------|--------|
| IDEA-head-of-specs-20260304-02 | Advance → BLG-NEW-13 (backlog) | Add to backlog.md |
| IDEA-ai-compliance-20260304-02 | Re-park (Parked-cycle-2) | Update status in file |
| 30 Parked (old format) | Re-park (Parked-cycle-2) | Bulk status update |
| 12 Advancing/Promoted (stale) | Correct → Promoted-Added | Bulk status update |
