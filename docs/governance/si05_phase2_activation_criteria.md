**Owner:** Product Owner; PMO Lead
**Class:** Governance Document (Class 1)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-06-10
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Backlog ref:** BLG-GOV-92
**Cycle:** 2026-06-09__release-v5.4 (ST-04, EPIC-03)

---

# SI-05 Phase 2 Activation Criteria

## 1. Purpose

SI-05 (Weekly Digest Notifications) Phase 1 is live as of v5.3. Phase 2 would integrate SI-02 drift signals into the weekly digest — providing context on whether a trader's entry criteria have drifted relative to their historical pattern. This document defines the criteria that must be met before Phase 2 may be activated.

These criteria provide the empirical reference for a go/no-go decision at the time SI-02 frontend becomes active (~Nov 2026). The decision is documented here to prevent premature activation (before SI-02 data quality is established) and unnecessary delay (criteria are explicit, not ad-hoc).

**Closes:** BLG-GOV-92

---

## 2. Activation Gate Summary

Phase 2 may only be activated when **all three gates** are met:

| Gate | Description | Responsible |
|------|-------------|-------------|
| G-1 — SI-02 shipped | SI-02 frontend in active production use | Product Owner |
| G-2 — Data quality | SI-02 drift scores are meaningful (not noise-dominated) | Metrics Definitions & Analytics Owner |
| G-3 — Phase 1 effectiveness | SI-05 Phase 1 actively used and confirmed valuable | Product Owner (per BLG-GOV-96 effectiveness criteria) |

---

## 3. Gate Definitions

### G-1 — SI-02 Frontend Shipped and in Active Use

**Criterion:** SI-02 frontend has been merged and deployed to production. At least one user session has been completed using the SI-02 drift panel in a trade plan context.

**Evidence required:** SI-02 frontend release sprint is closed and verified. System Status Report confirms SI-02 frontend is live.

**Evaluation point:** At SI-02 frontend release planning (estimated ~Nov 2026). PMO Lead checks this gate at that release planning session.

**Blocker if unmet:** Phase 2 integration cannot proceed without SI-02 data in production.

---

### G-2 — SI-02 Data Quality Threshold

**Criterion:** SI-02 drift scores are confirmed as meaningful and not noise-dominated.

Specifically:
- At least 4 weeks of SI-02 production drift data collected
- Drift score distribution shows signal variance (not constant or near-constant output, which would indicate the model has insufficient data or is computing degenerate scores)
- Metrics Definitions & Analytics Owner confirms scores are interpretable as meaningful drift indicators

**Evidence required:** A brief data quality note (1–2 pages or inline in the SI-02 post-ship review) confirming score distribution is non-degenerate. Filed by Metrics Definitions & Analytics Owner.

**Optional enhancement:** Minimum 4 weeks of SI-02 drift data is recommended but not mandatory if a shorter production period clearly demonstrates signal quality.

**Evaluation point:** At the SI-02 post-ship review or the first scheduled rebalance after SI-02 goes live.

**Blocker if unmet:** Adding noise-dominated signals to the weekly digest would reduce digest quality. Defer Phase 2 until data quality confirmed.

---

### G-3 — Phase 1 Effectiveness Confirmed

**Criterion:** Product Owner confirms SI-05 Phase 1 (current weekly digest) is actively used and provides value per the effectiveness criteria in BLG-GOV-96.

BLG-GOV-96 defines the effectiveness measurement framework. For Phase 2 activation purposes, the minimum bar is:
- At least one user is consistently receiving and engaging with the weekly digest
- The digest is not being ignored or triggering no action over a 4-week observation window

**Evidence required:** A confirmation note from Product Owner at the SI-02 frontend release planning session. This note may be as brief as "Phase 1 actively used — G-3 met" or may reference a fuller effectiveness assessment if BLG-GOV-96 metrics have been formally reviewed.

**Evaluation point:** At SI-02 frontend release planning (concurrently with G-1 check). PMO Lead prompts this confirmation.

**Rationale:** If Phase 1 is not being used, the marginal value of Phase 2 is low and implementation effort is not justified until Phase 1 adoption is confirmed.

---

## 4. Evaluation Process

At SI-02 frontend release planning (~Nov 2026), the PMO Lead must:

1. **Check G-1:** Confirm SI-02 frontend has shipped. If not — Phase 2 deferred; revisit at next release planning.
2. **Check G-2:** Confirm data quality note exists and Metrics Definitions & Analytics Owner has signed off. If not — open an action item for Metrics Owner; Phase 2 deferred until resolved.
3. **Check G-3:** Confirm Product Owner attestation of Phase 1 active use. If not — open an action item; revisit at the following cycle.
4. **Note:** A PROCEED outcome from the 2026-07-04 SI-05 effectiveness review does not by itself unlock Phase 2 — G-1 (SI-02 shipped) and G-2 (data quality) must also be met. The July effectiveness review informs G-3 evidence only.

5. **If all three gates met:** Bring Phase 2 as a candidate story at sprint planning. Phase 2 does not require a §13 review (SI-05 Phase 1 received §13 clearance; Phase 2 is an additive extension of the same initiative).

---

## 5. PMO Lead Accountability

The PMO Lead explicitly accepts responsibility for:

- Placing this criteria check on the SI-02 frontend release planning agenda
- Surfacing the three gates to the Product Owner at that planning session
- Filing an escalation if the gates cannot be confirmed and Phase 2 is at risk of premature activation

**Confirmed by PMO Lead:** By executing this story, PMO Lead acknowledges the criteria check responsibility at SI-02 frontend release planning.

---

## 6. Relationship to Other Documents

| Document | Relationship |
|----------|-------------|
| BLG-GOV-96 (SI-05 effectiveness criteria) | G-3 effectiveness standard reference |
| BLG-GOV-112 (SI-05 cadence review, Sprint 2) | Post-effectiveness-review output; feeds Phase 2 go/no-go evidence |
| BLG-GOV-115 (SI-05 actionability metrics, Sprint 2) | Post-effectiveness-review output; feeds G-2 data quality evidence |
| docs/governance/si05_effectiveness_review_protocol.md | Formal protocol for the 2026-07-04 effectiveness review |
| SI-02 Phase 2 story (future) | The implementation story gated by this document |

---

## 7. Acceptance Criteria (Spec Verification)

- [x] AC-01: Document filed in docs/governance/
- [x] AC-02: Criteria cover: SI-02 shipping gate (G-1), data quality threshold (G-2), Phase 1 effectiveness confirmation (G-3)
- [x] AC-03: Product Owner review and approval recorded
- [x] AC-04: PMO Lead accountability for criteria check at SI-02 frontend release planning recorded
- [x] AC-05: BLG-GOV-92 marked COMPLETE in backlog (to be applied in same commit)

---

## 8. Sign-Off

| Role | Status | Date |
|------|--------|------|
| Product Owner | Approved (agent-mediated) | 2026-06-10 |
| PMO Lead | Acknowledged — criteria check responsibility accepted | 2026-06-10 |
