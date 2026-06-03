**Owner:** Strategy Rules & System Intent Owner
**Class:** Operational Record (Class 3)
**Status:** Active — PASS (formalisation of pre-assessment)
**Last Updated:** 2026-06-03
**Cycle:** 2026-06-03__release-v5.0
**Story:** ST-12 (EPIC-04, v5.0)
**Backlog ref:** BLG-GOV-88
**Pre-assessment source:** `docs/product/decisions/si04_section13_preassessment.md` (2026-05-31, PASS)
**API Contract:** `docs/specs/api_contracts/strategy_version_comparison_contract.md` (BLG-SPEC-43, v4.8)

---

# SI-04 §13 Compliance — Formal Binding Conditions Record

**Feature:** SI-04 — Strategy Version Comparison
**Review type:** Formal formalisation of §13 binding conditions (Class 3 decisions document)
**Original §13 assessment:** `docs/product/decisions/si04_section13_preassessment.md` (PASS, 2026-05-31)
**Governance reference:** `claude/strategy/strategy_rules.md §13`
**API Contract reference:** `docs/specs/api_contracts/strategy_version_comparison_contract.md` (BLG-SPEC-43)

---

## Purpose of This Document

The SI-04 §13 pre-assessment (`si04_section13_preassessment.md`) was completed in v4.7 ST-01 and recorded a **PASS** determination with 6 binding conditions. The API contract was pre-authored in v4.8 (BLG-SPEC-43). However, the 6 binding conditions existed only in the ad-hoc pre-assessment file, not in a formal Class 3 decisions record equivalent to the SI-01 and SI-02 precedents.

This document formalises the 6 binding conditions as a standalone decisions record, cross-referencing BLG-SPEC-43, so that any future SI-04 sprint planning may reference this document directly without parsing the pre-assessment.

---

## §13 Determination (from pre-assessment)

**Overall determination: PASS**

All four §13 criteria confirmed COMPLIANT. SI-04 is a retrospective, deterministic historical analysis operating on the user's own trade history, split by strategy version tags. See `si04_section13_preassessment.md` for the full per-criterion analysis.

---

## 6 Binding Conditions (Mandatory for any SI-04 Implementation Sprint)

The following conditions are reproduced verbatim from `si04_section13_preassessment.md §13 Conditions for Implementation`. Sprint planning for SI-04 may not seal without confirming all 6 conditions carry forward.

### Binding Condition 1 — Comparison output is display-only

The version comparison endpoint must be a pure read-compute-return operation. No write operations to `strategy_rules.md`, `settings`, `trade_history`, or any table except a dedicated analytics cache (if caching is implemented). No side effects.

**API contract reference:** `strategy_version_comparison_contract.md` (BLG-SPEC-43) — all SI-04 endpoints are GET-only read operations with no write side-effects.

### Binding Condition 2 — Thin-period statistical caveat required

When a strategy version period contains fewer than 10 closed trades, the frontend must display a caveat (e.g., "Insufficient sample — interpret with caution" or a visual indicator). Metrics from thin periods must not be presented equivalently to well-sampled periods.

**Sprint planning note:** Any SI-04 frontend implementation story must include this caveat as an explicit acceptance criterion.

### Binding Condition 3 — No auto-reversion affordance

The frontend display must not include any button, link, or prompt that automatically reverts `strategy_rules.md` to a prior version based on comparison output. If strategy rollback functionality is added in any future sprint, a new §13 review is required before implementation.

**Scope boundary:** Any feature that writes to `strategy_rules.md` based on SI-04 output is out-of-scope until a new §13 review is completed.

### Binding Condition 4 — No parameter optimisation extension

Any extension that uses the version comparison to recommend, suggest, or calculate optimal strategy parameter values requires a new §13 review before implementation. This pre-assessment — and this decisions record — covers display-only comparison only.

**Scope boundary:** Automatic or semi-automatic parameter recommendation based on SI-04 output requires a new §13 review.

### Binding Condition 5 — Past-tense framing throughout

Frontend display must use past-tense historical framing: "trades before the change," "outcomes during v1.x period," "win rate after update." Forward-looking language ("expected improvement," "projected performance," "recommended parameters") is prohibited.

**UX requirement:** Any SI-04 frontend story must include past-tense framing as a hard acceptance criterion.

### Binding Condition 6 — §13 compliance note in backend service

The backend version comparison service must include a code comment referencing this pre-assessment and affirming: "display-only historical analysis; no adaptive output; no write operations to strategy or settings tables; §13 PASS — docs/product/decisions/si04_section13_preassessment.md."

---

## BLG-SPEC-43 Cross-Reference

The SI-04 API contract at `docs/specs/api_contracts/strategy_version_comparison_contract.md` (BLG-SPEC-43, v4.8, completed 2026-06-02) defines the endpoint specifications for SI-04. All endpoints are GET-only read operations, consistent with Binding Condition 1 (display-only). The contract does not define any write endpoints for SI-04 — consistent with the §13 boundary.

Any future SI-04 sprint that adds endpoints to the contract must verify each new endpoint against Binding Conditions 1, 3, and 4 before the sprint plan seals.

---

## Sign-Off

**Signed off by:** Strategy Rules & System Intent Owner
**Date:** 2026-06-03
**Determination:** PASS (formalisation — original determination unchanged from 2026-05-31)
**Comments:** This document formalises the 6 binding conditions from the SI-04 §13 pre-assessment (v4.7 ST-01) as a formal Class 3 decisions record. The §13 determination (PASS) is unchanged. All 6 binding conditions are reproduced verbatim from the pre-assessment. BLG-SPEC-43 (API contract) cross-referenced — all SI-04 API endpoints are GET-only, confirming Binding Condition 1 compliance at the contract level. BLG-GOV-88 resolved.
