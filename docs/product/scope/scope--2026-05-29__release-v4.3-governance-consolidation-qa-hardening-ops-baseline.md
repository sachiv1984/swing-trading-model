**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Superseded
**Release:** v4.3
**Cycle:** 2026-05-29__release-v4.3
**Last Updated:** 2026-05-29 (post-ship closure — Superseded)
**Supersession note:** *(completed at Post-Ship Closure)*

---

# Scope Document — v4.3 Governance Consolidation, QA Debt Clearance & Ops Hardening

---

## Items in Scope

| S2-ID | Description | Backlog source(s) | Priority | EPIC |
|-------|-------------|-------------------|---------|------|
| S2-01 | Governance Prompt Patches — 3 OA items from v4.2 closure (execution_prompt.md STEP 3.2.A qa_signed_off advisory; execution_prompt.md STEP 5.3/8 branch safety advisory; qa_evidence_template.md AC mapping 1:1 advisory) | OA-1/2/3 (v4.2 closure_record.md §6) | P1 | EPIC-01 |
| S2-02 | Governance Hardening — staging-only AC pre-designation reference table; AI feature inventory | BLG-GOV-42, BLG-GOV-47 | P1/P2 | EPIC-01 |
| S2-03 | QA Debt Clearance — 8 QA backlog items: 3 staging verifications, Playwright for Arc5ComplianceSection, Arc 5 E2E integration test spec, CI pipeline baseline, Playwright coverage matrix, Arc 5 coverage audit | BLG-QA-28/29/30/32/33/35/36/38 | P2 | EPIC-02 |
| S2-04 | Operations & Security Hardening — staging environment parity audit; claude-audit-log performance baseline; API key rotation policy; external API key security register | BLG-OPS-33, BLG-OPS-42, BLG-GOV-36, BLG-GOV-50 | P2 | EPIC-03 |
| S2-05 | Frontend Polish & Arc 5 Feature — pre-entry check entry price bug fix; Claude thesis UI copy audit; Arc 5 compliance score in monthly P&L report | BLG-FE-50, BLG-FE-51, BLG-FE-38 | P2 | EPIC-04 |

**Total scope:** 5 scope items → 4 EPICs → 18 stories

---

## Items Explicitly Deferred

| Item | Description | Reason |
|------|-------------|--------|
| SI-02 pre-planning cluster (7 items) | BLG-SPEC-37/41, BLG-BE-17/23, BLG-FE-52/53, BLG-GOV-39 | Gate: <20 closed trades; SI-02 sprint planning not imminent |
| BLG-GOV-67 (SI-05 Phase 1) | Weekly digest via SI-01+SI-03 data only | Gate: SI-01+SI-03 live ≥30 days; clears 2026-06-21 — deferred to v4.4 |
| BLG-GOV-33, BLG-GOV-34 | Arc 4 data density assessments | Advisory; lower urgency than sprint items |
| BLG-FE-25 (PT-04) | Setup Quality Score | Gate: ≥20 closed trades — not met |
| BLG-QA-31 | SI-02 Playwright pre-design | Gate: SI-02 sprint planning imminent |

---

## Supersession Note

Superseded by: v4.3 ship — 2026-05-29
Changelog: docs/product/changelog.md#v4.3
Verification report: claude/cycles/2026-05-29__release-v4.3/verification_report.md
Cycle: 2026-05-29__release-v4.3
