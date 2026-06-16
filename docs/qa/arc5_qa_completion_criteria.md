**Owner:** Director of Quality; QA Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-16
**Source:** ST-09 / BLG-QA-45 — v5.6 sprint execution

---

# Arc 5 QA Completion Criteria

## Purpose

This document defines the canonical "Arc 5 fully complete" criteria that trigger BLG-QA-26 (Arc 5 E2E QA protocol). It resolves the ambiguity noted in BLG-QA-45: BLG-QA-26 gated on "all five Arc 5 features shipped" but "fully complete" was undefined.

## Arc 5 Feature Inventory and Status

| Feature ID | Feature Name | Status | Notes |
|-----------|--------------|--------|-------|
| SI-01 | Pre-Entry Rule Validation Gate | ✅ Complete (v3.8) | 5 strategy checks + override acknowledgement |
| SI-02 | Behavioural Drift Detection | ⏸ Partial (backend ✅ v4.6; frontend gated) | Frontend gated on 20+ closed trades (~Q1 2027 at current rate) |
| SI-03 | Red Flag Journal | ✅ Complete (v3.9) | Full CRUD + Playwright coverage |
| SI-04 | Strategy Version Comparison | ❌ Not planned | Requires Arc 2 (PT-04) version-tagged trade history; itself gated on 20+ closed trades |
| SI-05 | Weekly Strategy Integrity Digest | ✅ Phase 1 Complete (v5.0–v5.5) | Phase 1: Red Flag + compliance score via Telegram; Phase 2 adds SI-02 drift signal (gated on SI-02 frontend) |

## Ambiguity Resolution

### Question 1: Does SI-05 Phase 2 count as a separate Arc 5 requirement?

**Decision:** SI-05 Phase 2 counts as a **separate, gate-conditional extension** of SI-05. Phase 1 is sufficient for the purposes of the BLG-QA-26 trigger. Phase 2 (drift signal integration) is dependent on SI-02 frontend, which is itself gated on 20+ closed trades. Making BLG-QA-26 conditional on SI-05 Phase 2 would create an indefinite dependency on the trade count gate.

**Rationale:** SI-05 Phase 1 delivers the primary user value (weekly digest covering Red Flag Journal summary + compliance score trend). Phase 2 adds an incremental drift signal layer. The arc-level QA protocol should cover the shipped feature set, not wait for an indefinitely gated extension.

### Question 2: Does SI-02 frontend count separately from SI-02 backend?

**Decision:** For the BLG-QA-26 trigger, SI-02 is treated as **complete at the point where its primary behavioural signal is accessible to users**. The backend (v4.6) computes drift scores; the frontend activation is gated on 20+ closed trades. Therefore: SI-02 backend is **in scope for the BLG-QA-26 trigger**; SI-02 frontend (when it ships) will require a BLG-QA-26 update/addendum, not a full re-trigger.

### Question 3: Does SI-04 block BLG-QA-26?

**Decision:** SI-04 (Strategy Version Comparison) is **not required** for the BLG-QA-26 trigger. SI-04 depends on Arc 2 (PT-04) which is itself gated on 20+ closed trades (~28 months). Including SI-04 as a BLG-QA-26 gate condition would create a multi-year blocker on an otherwise ready QA initiative.

## Canonical "Arc 5 Fully Complete" Criteria for BLG-QA-26

BLG-QA-26 (Arc 5 E2E QA protocol) may enter sprint planning when **all of the following** are true:

| # | Criterion | Met? | Evidence |
|---|-----------|------|----------|
| C-01 | SI-01 shipped and passing Playwright coverage (SC-TP-17–20) | ✅ Met (v3.8) | qa_evidence_EPIC-01.md v3.8 |
| C-02 | SI-03 shipped and passing Playwright coverage (SC-RFJ-01/02/03) | ✅ Met (v3.9) | qa_evidence_EPIC-03.md v3.9 |
| C-03 | SI-05 Phase 1 shipped and digest delivery verified | ✅ Met (v5.0–v5.5) | Multiple qa_evidence files |
| C-04 | SI-02 backend shipped (drift score computation endpoints live) | ✅ Met (v4.6) | BLG-BE-27 complete |
| C-05 | Arc 5 Playwright test coverage assessment complete (BLG-QA-49) | 🔄 In progress (ST-10 v5.6) | This sprint |

**C-05 completion (ST-10) is the final remaining criterion.** Upon ST-10 completion and DoQ sign-off, BLG-QA-26 may enter sprint planning.

**Not required for BLG-QA-26 trigger:**
- SI-02 frontend (gated on 20+ closed trades — expected ~Q1 2027)
- SI-04 Strategy Version Comparison (gated on Arc 2 / PT-04 — expected ~Oct 2028+)
- SI-05 Phase 2 (gated on SI-02 frontend)

**Post-trigger scope updates:** When SI-02 frontend ships and/or SI-04 ships, BLG-QA-26 should be extended with an addendum covering those features, not re-triggered.

## Impact on BLG-QA-26 Gate Condition

The BLG-QA-26 gate condition field should be updated to:

> **Arc 5 fully complete (for BLG-QA-26 purposes):** SI-01 ✅, SI-02 backend ✅, SI-03 ✅, SI-05 Phase 1 ✅, BLG-QA-49 coverage assessment ✅ (C-01 through C-05 above met). SI-02 frontend, SI-04, and SI-05 Phase 2 are explicitly excluded from this trigger — they are deferred extensions requiring separate gate conditions.

## Sign-Off

**Product Owner sign-off required:** Confirm resolution of Q1 (SI-05 Phase 2 excluded), Q2 (SI-02 backend sufficient), and Q3 (SI-04 excluded) before BLG-QA-26 enters planning.

**Director of Quality sign-off required:** Confirm C-01 through C-05 criteria are sufficient for a meaningful arc-level QA protocol.

| Role | Decision | Date |
|------|----------|------|
| Director of Quality | Approved — C-01/05 sufficient; exclusions appropriate; C-05 as final gate correct; BLG-FE-54/63 gate conditions noted for future sprint | 2026-06-16 |
| Product Owner | Approved — SI-05 Phase 2 excluded (Phase 1 sufficient; Phase 2 is incremental extension gated on SI-02 frontend); SI-02 backend sufficient (frontend a visibility gap, not correctness; addendum when shipped); SI-04 excluded (not in sprint planning; addendum when it ships). BLG-QA-26 should validate what is live and stable. | 2026-06-16 |
