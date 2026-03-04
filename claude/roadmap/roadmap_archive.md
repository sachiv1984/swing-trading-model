**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-04

# Roadmap Archive — Momentum Trading Assistant

This document is the permanent record of completed and killed roadmap items retired from `claude/roadmap/current_roadmap.md`. Items are listed in retirement order, most recent first.

Entries are append-only. Do not edit existing entries.

---

## §3.3 — Foundation & Governance (v1.7)

**Original roadmap location:** §3 Delivery Plan — §3.3
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-03-04
**Shipped version:** v1.7
**Cycle reference:** 2026-03-02__release-v1.7
**Verification report:** `claude/cycles/2026-03-02__release-v1.7/verification_report.md`
**Decision log reference:** N/A
**Retirement confirmed by:** Product Owner

### Original Roadmap Entry

### 3.3 Foundation & Governance (v1.7)

**Status:** ✅ Complete — Shipped 2026-03-03
**Cycle:** 2026-03-02__release-v1.7
**Verification:** Verified — `claude/cycles/2026-03-02__release-v1.7/verification_report.md`
**Changelog:** `docs/product/changelog.md` — v1.7 entry

This release delivered the technical and governance foundations that de-risk everything that follows. It was non-user-facing but a hard dependency for several v1.8+ features.

#### BLG-TECH-04 — CI/CD GitHub Actions Validation Workflow
**Status:** ✅ Complete — 2026-03-03 (EPIC-01)
`.github/workflows/validate-analytics.yml` merged. Triggers on PR/push to main/develop. Blocks merge on `critical_failed > 0`. Posts severity breakdown as PR comment. PR #11 merged.

#### Strategy Rules §13 Boundary Review
**Status:** ✅ Complete — 2026-03-03 (EPIC-02)
Three features reviewed: Signal Params COMPLIANT, AI Journal CONDITIONALLY COMPLIANT, New Indicators COMPLIANT if canonical. §13-gated features cleared to proceed. Decision record: `docs/product/decisions/SRB-v1.7-2026-03-02__release-v1.7.md`.

#### Metrics Definitions — Portfolio Heat Formula & Thresholds *(pre-work gate for v1.8)*
**Status:** ✅ Complete — 2026-03-03 (EPIC-03)
`metrics_definitions.md` v1.6.0: Position Risk (GBP-adjusted), Portfolio Heat formula, explicit display thresholds. v1.8 pre-alignment gate cleared.

#### Structured Logging / Observability Standards
**Status:** ✅ Complete — 2026-03-03 (EPIC-04)
`docs/specs/structured_logging_standards.md` v0.1.0 created (Class 1 Canonical Specification). Log levels, JSON format, correlation IDs, async observability. v2.0 pre-alignment gate (logging) cleared.

#### API Versioning Strategy Decision Record
**Status:** ✅ Complete — 2026-03-03 (EPIC-05)
`docs/product/decisions/api-versioning-v1.7.md` filed. URL path versioning deferred to first breaking change; 60-day deprecation; webhooks versioned from inception. v2.0 pre-alignment gate (API versioning) cleared.

#### Spec Debt Resolution (BLG-TECH-06, BLG-TECH-08, BLG-TECH-09)
**Status:** ✅ Complete — 2026-03-03 (EPIC-06)
`analytics_endpoints.md` v1.9.0 (14 metrics, OBS-01 resolved); `portfolio_endpoints.md` v1.9.0 (corrected to live API, OBS-QWB-R1-01 resolved); `trade_endpoints.md` v1.9.0 (`holding_days` added, OBS-QWB-R3-01 resolved).

---

## v1.6.1 — Correctness & Quick Wins

**Original roadmap location:** §3 Delivery Plan — v1.6.1 section
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-03-04
**Shipped version:** v1.6.1
**Cycle reference:** N/A (pre-cycle governance)
**Verification report:** `docs/product/verification/QWB-quick-wins-bundle-verification.md` v1.0
**Decision log reference:** N/A
**Retirement confirmed by:** Product Owner

### Original Roadmap Entry

### v1.6.1 — Correctness & Quick Wins *(new)*

This release is inserted immediately after v1.6. It exists to resolve known correctness issues and ship a cluster of small, high-value backlog items before any new feature investment begins. No new feature work opens until this release is complete.

#### BLG-TECH-01 — Fix Sharpe Variance + Capital Efficiency *(promoted from backlog — P0)*
**Status:** ✅ Complete — 2026-02-21
**Closed:** Canonical Owner sign-off granted 2026-02-21. Validation confirmed 13/13 pass at 2026-02-21T00:24:41Z. `metrics_definitions.md` updated to v1.5.7 (Appendix E both items resolved). `analytics_endpoints.md` updated to v1.8.1. No regressions.

Fix `_calculate_sharpe()` to use sample variance (n−1) for portfolio and trade-level Sharpe. Fixed capital efficiency to use `total_cost (GBP)` from `trade_history` instead of `entry_price × shares`. `validation_data.py` expected values updated accordingly. v1.6 quality gate satisfied.

#### BLG-TECH-02 + BLG-TECH-03 — Validation Severity Model + Service Layer Consolidation (promoted from backlog — P1)
**Status:** ✅ Complete — 2026-02-21
**Closed:** Director of Quality sign-off 2026-02-21T21:30:00Z. 14/14 validation results pass with severity model. Phase Gate Documents filed.

Severity field added to every validation result (critical / high / medium / low) per analytics_endpoints.md v1.8.1
by_severity aggregation added to summary — all four tiers always present
All validation logic consolidated into services/validation_service.py per backend_engineering_patterns.md §3
Router thinned to HTTP in/out only — delegates entirely to ValidationService.validate_all()
Delivered co-delivered on single branch: fix/blg-tech-02-03-severity-service-consolidation
Phase Gate Documents: docs/product/phase_gates/BLG-TECH-02-validation-severity-model-phase-gate.md, docs/product/phase_gates/BLG-TECH-03-validationservice-consolidation-phase-gate.md
BLG-TECH-04 (CI/CD gate) dependency now unblocked ✅

#### Quick Wins Bundle *(promoted from backlog --- P2)*

**Status:** ✅ Complete --- 2026-03-01 **Estimated total effort:** ~8--10.5 hours (revised from ~6--8 hours to account for spec authoring --- A-S05, 2026-02-25) **Scope document:** `docs/product/scope/scope--QWB-quick-wins-bundle.md` **Decisions record:** `docs/product/decisions/QWB-quick-wins-bundle.md` **Phase Gate Document:** `docs/product/phase_gates/QWB_quick_wins_bundle_phase_gate.md` **Value:** Visible, tangible user-facing improvements. All decisions closed. All specs locked and QA-signed.

| Item | Effort | Status |
| --- | --- | --- |
| BLG-FEAT-01 --- Current Drawdown Widget | ~30 min | ✅ Complete — Shipped v1.6.1, 2026-03-01 |
| BLG-FEAT-02 --- R-Multiple Column in Trade History | ~1 hour | ✅ Complete — Shipped v1.6.1, 2026-03-01 |
| BLG-FEAT-04 --- Best / Worst Trades Widget | ~1 hour | ✅ Complete — Shipped v1.6.1, 2026-03-01 |
| BLG-FEAT-05 --- Win Rate by Month Chart | ~1 hour | ✅ Complete — Shipped v1.6.1, 2026-03-01 |
| BLG-FEAT-06 --- Grace Period Indicator | ~1 hour | ✅ Complete — Shipped v1.6.1, 2026-03-01 |
| BLG-FEAT-07 --- CSV Export of Trade History | ~1 hour | ✅ Complete — Shipped v1.6.1, 2026-03-01 |

**Locked canonical specs (implementation source of truth):**

| Spec | Version |
| --- | --- |
| `docs/specs/metrics_definitions.md` | v1.5.8 |
| `docs/specs/api_contracts/portfolio_endpoints.md` | v1.8.2 |
| `docs/specs/api_contracts/position_endpoints.md` | v1.8.3 |
| `docs/specs/api_contracts/trade_endpoints.md` | v1.8.4 |
| `docs/specs/api_contracts/analytics_endpoints.md` | v1.8.1 |
| `docs/specs/data_model.md` | v1.7 |
| `docs/specs/frontend/pages/dashboard.md` | v1.1 |
| `docs/specs/frontend/pages/trade_history.md` | v1.1 |
| `docs/specs/frontend/pages/analytics.md` | v1.2 |
| `docs/specs/frontend/pages/positions.md` | v1.2 |
| `docs/specs/api_dependencies.md` | v1.2 |
| `docs/reference/openapi.yaml` | current |

Verification: docs/product/verification/QWB-quick-wins-bundle-verification.md v1.0
Director of Quality sign-off: 2026-03-01 — Pass with logged deferrals (F-17, F-27)
Changelog: docs/product/changelog.md — v1.6.1 entry
Last Updated: 2026-03-01

---

## 3.2 — Position Sizing Calculator

**Original roadmap location:** §3 Delivery Plan — §3.2
**Status at retirement:** ✅ Complete
**Retired from active roadmap:** 2026-03-04
**Shipped version:** v1.6
**Cycle reference:** N/A (pre-cycle governance)
**Verification report:** `docs/product/verification/3.2-position-sizing-calculator-verification.md` (v1.4)
**Decision log reference:** N/A
**Retirement confirmed by:** Product Owner

### Original Roadmap Entry

**3.2 Position Sizing Calculator (Primary Feature)**
**Status:** ✅ Complete (shipped v1.6)
**Effort:** Low–Medium (2–3 days) (revised from 1–2 days — see scope note below)
**Value:** High (daily workflow improvement)
Always-visible widget inside the position entry form, directly above the shares field. User provides risk percentage (pre-populated from settings default) and stop price; system calculates suggested share count. Auto-fills the shares field when empty; shows a "use this" affordance when the user has already entered a value. Validates against available cash in real time via debounced calculation (300ms).

**Scope note (revised 2026-02-19):** Scope expanded during pre-alignment to include default_risk_percent field in the settings table, settings endpoint, and settings page UI. This is required to support widget pre-population and is in scope for v1.6 — not deferred. The original 1–2 day estimate did not account for the settings field, database migration, and additional spec updates across four documents. Revised estimate: 2–3 days. Full decision rationale: docs/product/decisions/3.2-position-sizing-calculator.md.

**Canonical specifications:** Sizing formula, validity rules, FX handling, and cash constraint behaviour are canonicalised in docs/specs/strategy_rules.md §4.1. Endpoint contract at docs/specs/api_contracts/portfolio_endpoints.md (POST /portfolio/size). Data model at docs/specs/data_model.md §6. Settings field at docs/specs/api_contracts/settings_endpoints.md.

**Shipped:** Director of Quality sign-off 2026-02-20. Verification report: docs/product/verification/3.2-position-sizing-calculator-verification.md (v1.4). Changelog: v1.6 entry. Scope and decisions documents superseded.

---

## 4.1a — CSV Export of Trade History

**Original roadmap location:** §3 Delivery Plan — v2.0 section
**Status at retirement:** ❌ Killed
**Retired from active roadmap:** 2026-03-04
**Shipped version:** N/A — killed
**Cycle reference:** 2026-03-01__item-3.2
**Verification report:** N/A
**Decision log reference:** DL-001 (2026-03-01)
**Retirement confirmed by:** Product Owner

### Original Roadmap Entry

#### 4.1a — CSV Export of Trade History
**Status:** ❌ Killed — superseded by BLG-FEAT-07 (shipped v1.6.1, 2026-03-01)

BLG-FEAT-07 (CSV Export) was delivered as part of the QWB Quick Wins Bundle and shipped in v1.6.1. This planning item is closed. Decision log: 2026-03-01__item-3.2.
