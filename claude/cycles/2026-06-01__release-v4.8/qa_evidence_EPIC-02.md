Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-06-01

---

# QA Evidence Log — EPIC-02 (Operations, Security & QA Debt)

**Cycle:** 2026-06-01__release-v4.8

---

## Consolidation Block

**EPIC:** EPIC-02 — Operations, Security & QA Debt (S2-02)
**Cycle:** 2026-06-01__release-v4.8
**Sprint goal:** Resolve all firm v4.8 governance and operations debt items — closing the §13 OPERATIONAL_GUIDE register gap, remediating agent charter header non-compliance, establishing build minutes monitoring policy, completing the post-v4.7 dependency audit, and updating the QA coverage matrix — clearing the decks ahead of the SI-05 Phase 1 gate window (2026-06-21).
**Test scenarios used:** Derived from spec + AC (all ACs verifiable by code review and document inspection; no automated test scenarios)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-04 | `docs/operations/build_minutes_monitoring_policy.md` | Created build minutes monitoring policy v1.0: monthly allocation (400 min), v4.6/v4.7 consumption history, 80% threshold (320 min), billing reset (1st of month), double-capacity sprint assessment. | AC-01: monthly allocation documented ✓; AC-02: consumption history documented ✓; AC-03: 80% threshold defined ✓; AC-04: billing reset date documented ✓; AC-05: double-capacity assessment documented ✓; AC-06: FinOps & Resource Architect sign-off ✓ | Pass | None |
| ST-05 | `docs/security/security_register.md` | Created security_register.md v1.0: pip-audit (clean), npm audit (45 vulns, 0 critical, 21 HIGH in devDeps — all react-scripts chain), Anthropic SDK check (0.40.0 → 0.105.2 available). BLG-OPS-49 filed (npm HIGH, P1), BLG-OPS-50 filed (Anthropic SDK upgrade, P2). | AC-01: pip-audit run + documented ✓; AC-02: npm audit run + documented ✓; AC-03: HIGH findings filed as BLG-OPS-49 P1 (no CRITICAL) ✓; AC-04: Anthropic SDK checked, BLG-OPS-50 filed ✓; AC-05: findings documented in security_register.md ✓; AC-06: Cybersecurity & Trust Lead sign-off ✓ | Pass | None — note: 21 HIGH npm CVEs are all devDependencies (react-scripts build chain), not production runtime. Filed P1 per security policy. |
| ST-06 | `docs/qa/playwright_coverage_matrix.md`, `docs/specs/api_contracts/reports_endpoints.md#GET /reports/monthly-pnl` | Updated coverage matrix v1.1: added v4.3–v4.7 sections, compliance_summary field as regression point (SC-REP-05 reference). Verified GET /reports/monthly-pnl v0.6 schema present in reports_endpoints.md (line 482). No contract gaps found. | AC-01: compliance_summary in coverage matrix ✓; AC-02: SC-REP-05 regression test reference ✓; AC-03: v0.6 contract confirmed in reports_endpoints.md ✓; AC-04: no contract gaps found ✓; AC-05: QA Lead sign-off ✓ | Pass | None |
| ST-07 | `docs/specs/api_contracts/strategy_version_comparison_contract.md` | Created strategy_version_comparison_contract.md v0.1.0 (GET /analytics/strategy-version-comparison contract pre-sprint draft). Added openapi.yaml placeholder entry. Response schema, query params, error cases, §13 binding conditions documented. | AC-01: contract file created ✓; AC-02: response schema with version_comparison fields ✓; AC-03: query parameters defined ✓; AC-04: error cases (404, 422) defined ✓; AC-05: openapi.yaml placeholder added ✓; AC-06: §13 binding conditions owner acknowledged in contract header ✓; AC-07: Head of Specs Team sign-off ✓ | Pass | None |

**QA test coverage:**
- Scenarios run: Code review and document inspection (all ACs verifiable without staging or live system interaction)
- Regression areas checked: Render build minutes policy; npm/pip dependency security; Playwright coverage matrix; GET /reports/monthly-pnl v0.6 contract; openapi.yaml integrity
- Known deviations filed: None

---

## Autonomous Class Sign-Off (BLG-GOV-19)

**Autonomous class eligibility check (BLG-GOV-19):**
- [x] Criterion 1: All stories in this EPIC have `delegation_class: autonomous` — ✓
- [x] Criterion 2: All AC verifiable by code review alone — no observable UI behaviour, no staging run required — ✓
- [x] Criterion 3: No frontend-visible change — confirm no React page or UI component was created or modified (checked src/pages/ and src/components/) — ✓
- [x] Criterion 4: Engine signer field populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-06-01
- Comments: Autonomous class sign-off — all four qualifying criteria met. All 4 stories are documentation/policy creation (build minutes policy, security register, coverage matrix update, SI-04 pre-sprint contract). All ACs verifiable by code review and document inspection. No frontend-visible changes. ST-05 filed BLG-OPS-49 (P1) and BLG-OPS-50 (P2) per security policy for HIGH npm vulns and Anthropic SDK upgrade gap.
