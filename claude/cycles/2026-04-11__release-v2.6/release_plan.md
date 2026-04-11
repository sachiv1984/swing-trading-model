**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v2.6
**Cycle:** 2026-04-11__release-v2.6
**Last Updated:** 2026-04-11

---

# Release Plan — v2.6 Backend Integration Completion, Test Automation & Governance Hardening

---

## Readiness

**Assessed by:** PMO Lead + Head of Specs Team
**Date:** 2026-04-11

### Lifecycle Guard

- Prior cycle status: `Closed` ✅
- `post_ship_complete`: `true` ✅
- `next_cycle_unblocked`: `true` ✅
- Lifecycle Guard: **PASS**

### Backlog Readiness

Active backlog items targeting v2.6: **14 items** with `Provisional-Target: v2.6` plus 3 governance deferred patches from v2.5 (no Provisional-Target field — sourced from lessons_learnt_closure.md carry-forward).

- P1 items: 3 (BLG-BE-08-GAP-01, BLG-BE-09-GAP-01, BLG-QA-09) + 1 governance CF-1 patch
- P2 items: 3 (BLG-BE-09-GAP-02, BLG-QA-07/08/10, BLG-GOV-15) + 1 governance CF-2 patch
- P3 items: 8 (FE, QA-11, SPEC, GOV remaining)

### Advisory Checks

**Backlog Age Advisory:** BLG-GOV-08 aged 4+ cycles without story assignment. PO decision: defer to v2.7 (L effort, lower priority vs. P1/P2 items). ⚠ Advisory logged.

**Provisional-Target:** 14 items carry `Provisional-Target: v2.6`. 3 governance patches from carry-forward have no Provisional-Target field. ℹ Noted.

**Design Dependency Scan:** 3 items flagged — BLG-FE-11, BLG-FE-12, BLG-FE-13 all require "Head of UX review before implementation". Design dependency scan: 3 item(s) flagged. Surfaced in Pre-sprint Required Decisions checklist.

### Readiness Verdict

Backlog is ready for scope extraction. No hard blockers. Design dependencies noted for EPIC-03 (require UX pre-sprint decision).

---

## Scope

### S2 Scope Items

| S2-ID | Epic | Description | Backlog Source | Priority |
|-------|------|-------------|----------------|----------|
| S2-01 | EPIC-01 | Backend Integration Completion — migrate Reports Performance tab to FastAPI; wire Signals page to FastAPI; replace Base44 cash balance | BLG-BE-08-GAP-01, BLG-BE-09-GAP-01, BLG-BE-09-GAP-02 | P1/P2 |
| S2-02 | EPIC-02 | Test Automation & CI Hardening — fix pytest collection errors; add CI workflow; fee drag Playwright spec; fee drag backend pytest tests | BLG-QA-09, BLG-QA-10, BLG-QA-07, BLG-QA-08 | P1/P2 |
| S2-03 | EPIC-03 | Frontend UX Polish — StatsCard tooltip prop; Trade History bar layout; column header styling; flexible column sorting | BLG-FE-10, BLG-FE-11, BLG-FE-12, BLG-FE-13 | P3 |
| S2-04 | EPIC-04 | Governance & Spec Debt — execution_prompt STEP 5.1 unpushed-commit check; §6 edit reminders for 3 engines; decision_log.md hard gate; frontend performance budget spec | CF-1, CF-2, BLG-GOV-15, BLG-FE-09 | P1/P2/P3 |

### Items Explicitly Deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-TECH-05 | P3 — multi-user prerequisite; no current operational need | v2.7 or when multi-user |
| BLG-QA-11 | P3 — System Status Playwright spec; lower priority vs. active test gaps | v2.7 |
| BLG-GOV-08 | P3 — L effort engine compression; would dominate sprint capacity | v2.7 |
| BLG-GOV-11 | P3 — large artefact inventory scope; deprioritised vs. P1/P2 items | v2.7 |
| BLG-GOV-14 | P3 — governance health score formula definition; complex; deprioritised | v2.7 |
| BLG-SPEC-D17 | P3 — spec dependency map; deprioritised vs. higher-priority items | v2.7 |
| CF-3 (exec_state schema) | Low priority — execution_state.json test_scenarios field ambiguity | v2.7 |

---

## Execution Plan

### EPIC Table

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01 | Head of Engineering | RISK-01 (Base44 API contract divergence — untested paths) | None (self-contained) |
| EPIC-02 | S2-02 | QA & Testing Owner | RISK-02 (CI env configuration complexity) | EPIC-02 ST-05 depends on ST-04 (collection errors fixed first) |
| EPIC-03 | S2-03 | Frontend Specifications & UX Owner | RISK-03 (UX design decisions required before implementation) | EPIC-03 requires UX design pre-sprint decisions for ST-09/ST-10/ST-11 |
| EPIC-04 | S2-04 | Head of Specs Team | RISK-04 (§6 checklist compliance for 3-engine patch) | None (governance-only; no code changes) |

**EPIC-03 note:** ST-09 (bar layout), ST-10 (column headers), ST-11 (flexible sorting) require Head of UX design decisions before sprint execution. ST-08 (tooltip prop) is self-contained and may proceed independently. Pre-sprint required decisions checklist in cycle_summary.md.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | Reports Performance tab and Signals page depend on Base44 SDK for data that may not fully map to FastAPI endpoints — untested integration paths could reveal data model gaps | Medium | ST-01/ST-02 include integration review; GAP docs (reports_integration_review.md, signals_integration_review.md) already document known gaps; any new gaps to be filed as backlog items | null |
| RISK-02 | EPIC-02 | CI test runner workflow (ST-05) requires GitHub Actions environment with correct Python version and dependencies — configuration errors may stall CI setup | Low | Phase A (clean tests only) does not require DATABASE_URL secret; start minimal and expand | null |
| RISK-03 | EPIC-03 | ST-09/ST-10/ST-11 require Head of UX design decisions before implementation — if decisions are not made pre-sprint, stories cannot proceed | Medium | Checklist in cycle_summary.md pre-sprint required decisions; Head of UX to resolve before sprint seal | null |
| RISK-04 | EPIC-04 | 3-engine §6 edit reminder patch (ST-13) requires governance file edit checklist compliance across design_gate_prompt.md, amendment_cycle_prompt.md, roadmap_prompt.md — risk of missing version bumps or prompt_change_log.md entries | Low | Use CLAUDE.md §6 checklist; commit-check skill before committing | null |

---

## Integrity Validation — 3.5 Local Model Integrity

**Assessed by:** Head of Specs Team + Challenger

### S2 → EPIC Mapping Check

| S2-ID | Mapped EPIC | Status |
|-------|-------------|--------|
| S2-01 | EPIC-01 | ✅ |
| S2-02 | EPIC-02 | ✅ |
| S2-03 | EPIC-03 | ✅ |
| S2-04 | EPIC-04 | ✅ |

All 4 S2 scope items have exactly 1 EPIC mapping. No orphaned scope items.

### RISK → EPIC Mapping Check

All 4 RISK-IDs referenced in the EPIC table appear in the Risk Register Summary. All have `escalation_ref: null` (no escalations raised).

### Design Dependency Consistency

3 design dependencies flagged in readiness (BLG-FE-11/12/13 → ST-09/ST-10/ST-11). RISK-03 covers this. Pre-sprint required decisions checklist will enforce resolution before sprint seal.

### Model Integrity Verdict: **PASS**

- No S2 items without EPIC assignment ✅
- No EPIC without S2 mapping ✅
- No RISK-IDs missing from register ✅
- No open escalations ✅

---

## Capacity Check

**Assessed by:** FinOps & Resource Architect + PMO Lead

### Effort Band Lookup

scored_initiatives.md: no Effort Band column present. All EPICs fall to Tier 3 (inline estimate). No advisory required.

### Effort Estimates

| EPIC-ID | Stories | Effort (Low) | Effort (High) | Mid |
|---------|---------|-------------|--------------|-----|
| EPIC-01 | 3 | 32h | 56h | 44h |
| EPIC-02 | 4 | 15h | 27h | 21h |
| EPIC-03 | 4 | 13h | 20h | 17h |
| EPIC-04 | 4 | 12h | 20h | 16h |
| **Total** | **15** | **72h** | **123h** | **98h** |

### Capacity Assumption

Solo developer with AI engine assistance. Based on prior cycle velocity (v2.4: 1.00, v2.5: 1.00), 2-sprint delivery is the target. Estimated availability: ~50–60 hours per sprint (engine-assisted velocity).

- 2-sprint capacity estimate: ~100–120h
- Mid-point total: 98h → within 2-sprint capacity ✅
- High-end total: 123h → marginally above — acceptable given AI assistance and velocity 1.00

### Phasing Recommendation

Sprint 1 (higher-effort, higher-priority EPICs):
- EPIC-01: Backend Integration (44h mid) — P1 items, largest effort, ship first
- EPIC-02: Test Automation (21h mid) — P1/P2 items, enables CI gates

Sprint 1 total (mid): 65h — within a sprint of ~60–70h.

Sprint 2 (lower-effort, polish/governance EPICs):
- EPIC-03: Frontend UX Polish (17h mid) — P3, UX-gated stories
- EPIC-04: Governance & Spec Debt (16h mid) — P2/P3, governance patches

Sprint 2 total (mid): 33h — within a sprint of ~40–50h.

Ordering rationale: EPIC-01/02 deliver P1 user-facing and infra value before polish/governance. EPIC-03 requires UX pre-sprint decisions which can be obtained between planning and sprint start. EPIC-04 governance patches are low-effort and can be front-loaded or back-loaded flexibly.

### Capacity Verdict: **PASS**

Mid-point total (98h) is within 2-sprint capacity envelope. Proceed.

---

## Integrity Validation — 5.5 Cross-Stage Integrity

**Assessed by:** Director of Quality + Head of Specs Team

### Checks

| Check | Result | Notes |
|-------|--------|-------|
| All S2-IDs have EPIC assignments | ✅ PASS | S2-01→EPIC-01, S2-02→EPIC-02, S2-03→EPIC-03, S2-04→EPIC-04 |
| All EPICs have S2 back-references | ✅ PASS | All 4 EPICs declare Maps to S2-xx |
| All RISK-IDs in EPIC table appear in Risk Register | ✅ PASS | RISK-01 through RISK-04 all present |
| No open escalations blocking publish | ✅ PASS | open_escalations = [] |
| Backlog items for all S2 items confirmed in backlog.md | ✅ PASS | BLG IDs confirmed present |
| Deferred items documented with rationale | ✅ PASS | 7 items deferred with reasons |
| Design dependencies surfaced | ✅ PASS | 3 items in run_manifest + RISK-03 + pre-sprint checklist |

### Cross-Stage Integrity Verdict: **PASS**

---

## Integrity Validation — 5.7 Decision Record Integrity

**Assessed by:** Director of Quality

### Check

Decision record `docs/product/decisions/decisions--2026-04-11__release-v2.6.md` present: ✅

Accepted risk escalations: 0 — accepted risks section in decisions record is "None" — no AR records required.

### Decision Record Integrity Verdict: **PASS** (no AR records required)
