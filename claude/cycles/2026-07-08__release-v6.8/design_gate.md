**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-08
**Cycle:** 2026-07-08__release-v6.8

# Design Gate Record — 2026-07-08__release-v6.8

## Gate Status: PASSED

Completed: 2026-07-08
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 | Investigate `trade_plans.position_id` never populated (BLG-BE-46) | Design Pre-Approved | Backend correctness fix (data linkage); no new UI, no layout change. Existing Reports/Dashboard displays unchanged in structure — only underlying values corrected. | N/A | No frontend spec change required | ✅ Cleared | Head of UX & Design |
| ST-02 | Unvalidated dict keys as SQL column names (BLG-SEC-08) | Design Pre-Approved | Purely backend security fix (allowlist validation); no UI change. | N/A | No frontend spec change required | ✅ Cleared | Head of UX & Design |
| ST-03 | Manual review of signals for anomalous values (BLG-SEC-07) | Design Not Applicable | Manual data review/audit activity; no code or UI shipped. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-04 | Provision application `X-API-Key` (BLG-OPS-99) | Design Not Applicable | Infrastructure/credential provisioning; no user-visible effect. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-05 | Trade tagging and tag-based performance filtering (BLG-FEAT-52) | Design Required | New user-facing capability: tag add/remove on trade plans, new filter controls on PerformanceAnalytics. | `docs/design/2026-07-08__release-v6.8/trade-tagging/ux_spec.md` v1.0 | `docs/specs/frontend/pages/trade_plan.md` v0.9; `docs/specs/frontend/pages/analytics.md` v2.0 | ✅ Cleared | Head of UX & Design |
| ST-06 | SI-02 gate visibility indicator, Reports page (BLG-FEAT-71) | Design Required | New user-facing section on Reports page (gate condition breakdown, distinct from existing Dashboard strip). | `docs/design/2026-07-08__release-v6.8/si02-gate-visibility-indicator/ux_spec.md` v1.0 | `docs/specs/frontend/pages/reports.md` v0.6 | ✅ Cleared | Head of UX & Design |
| ST-07 | Dashboard homepage visual hierarchy review post-v6.2 (BLG-SPEC-58) | Design Not Applicable | Review/documentation activity owned by Head of UX & Design; no UI shipped this sprint — any resulting change is filed as a follow-up item and design-gated separately. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-08 | R-multiple cross-currency normalization specification (BLG-SPEC-59) | Design Not Applicable | Canonical spec-authoring only; no UI ships this sprint. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-09 | Trailing stop visual indicator frontend specification (BLG-SPEC-60) | Design Not Applicable | Deliverable is the frontend specification document itself (states/colours/placement); implementation not in this sprint's scope — no product UI ships. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 | Trailing stop effectiveness metric definition (BLG-SPEC-61) | Design Not Applicable | Metric definition documentation only; no UI. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-11 | Fix 12 dark spec files (BLG-QA-64) | Design Not Applicable | Test/spec wiring remediation (register or delete); no new or changed UI. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-12 | CI inline OpenAPI drift detection (BLG-GOV-134) | Design Not Applicable | CI/CD tooling; no user-visible effect. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-13 | Log Anthropic API token usage/cost per briefing call (BLG-OPS-74) | Design Not Applicable | Backend logging/observability; no UI. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-14 | Refactor `Watchlist.js` to ESLint compliance (BLG-FE-77) | Design Not Applicable | Pure refactor; AC-02 explicitly requires no functional or visual behaviour change. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-15 | v5.1–v5.4 endpoint baseline extension (BLG-OPS-61) | Design Not Applicable | Documentation of API latency baselines; no UI. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-16 | Extract Playwright test standard to `shared_standards.md` (BLG-GOV-123) | Design Not Applicable | Governance document reorganisation; no UI. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-17 | System threat model document (BLG-OPS-71) | Design Not Applicable | Security documentation; no UI. | N/A | N/A | ✅ Cleared | Head of UX & Design |

## Blocked Items (if any)

None.

## Notes

- Only ST-05 and ST-06 (EPIC-02, Product Value Pull-Forward) classified as Design Required. Both artefacts produced and approved same-day; both frontend specs updated and confirmed compliant by Head of Specs Team.
- ST-05 scope decision: trade-plan tags (`trade_tags`) are a new, data-independent field from the existing position/journal tags already documented in `journal_components.md` — same UI components reused for visual consistency only, per ST-05 AC-04's no-dependency-on-trade_annotations/PO-02 confirmation.
- ST-06 scope decision: new Reports-page section is additive to, not a replacement of, the existing Dashboard "Gate Progress" strip (`dashboard.md` §6) — the two serve different levels of detail.
- ST-09 (trailing stop visual indicator frontend spec) and ST-07 (visual hierarchy review) were the two items closest to the Design Required boundary, since both are UX-adjacent in subject matter. Classified Design Not Applicable because the story deliverable in both cases is a document (spec / review findings), not a shipped UI change — consistent with §6's "no user-visible effect" test. Any UI change resulting from either story's findings will be design-gated in a future cycle when it is actually scheduled for implementation.
- No disagreements between Product Owner and Head of UX & Design were raised on any item.

## Design-Required Items — Detail

### ST-05
- **2.1/2.2:** No existing artefact; new artefact produced — `docs/design/2026-07-08__release-v6.8/trade-tagging/ux_spec.md` v1.0
- **2.3:** Product Owner approved 2026-07-08
- **3:** `trade_plan.md` v0.8→v0.9 (§5c added, §5.1/§7 updated), `analytics.md` v1.9→v2.0 (§14a added). Head of Specs Team confirmed lifecycle compliance (Class 2 / Class 1 respectively, version incremented, Last Updated set).

### ST-06
- **2.1/2.2:** No existing artefact; new artefact produced — `docs/design/2026-07-08__release-v6.8/si02-gate-visibility-indicator/ux_spec.md` v1.0
- **2.3:** Product Owner approved 2026-07-08
- **3:** `reports.md` v0.5→v0.6 (new "SI-02 Gate Status" section). Head of Specs Team confirmed lifecycle compliance (Class 2, version incremented, Last Updated set).
