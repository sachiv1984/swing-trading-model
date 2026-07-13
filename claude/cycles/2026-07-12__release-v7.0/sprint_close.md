Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-13
Cycle: 2026-07-12__release-v7.0

# Sprint Close — 2026-07-12__release-v7.0

## Sprint Goal

Close the Grid View/Table View position-risk badge and trailing-stop parity gap, resolve the v6.9-carried spec-reconciliation and data-correctness debt, and ship three new reporting and position-review features (tax-year P&L CSV export, realized/unrealized P&L split, and position review-cadence nudge) — fully utilising this cycle's ~12–14 day capacity per the Product Owner's scope-maximisation directive.

## Items Done

### EPIC-01 — Positions Grid View Parity (PR #968, merged)

| ST | Title | Commit SHA | Spec References |
|----|-------|-----------|-------------------|
| ST-01 | `positions.md` Grid View badge placement subsection (BLG-SPEC-80) | `f5c0962c` | `docs/specs/frontend/pages/positions.md#Alerts Column` |
| ST-02 | Positions Grid View missing RISK OFF badge (BLG-FE-102) | `2d4eaa57` | `docs/specs/frontend/pages/positions.md#Alerts Column` |
| ST-03 | Positions Grid View missing trailing-stop value and breach indicator (BLG-FE-97) | `2d4eaa57` | `docs/specs/frontend/pages/positions.md#Trailing Stop Column` |
| ST-04 | Positions Grid View badge parity Playwright coverage (BLG-QA-95) | `19d2d5ba` | `tests/e2e/epic01-v70-grid-badge-parity.spec.js` |
| ST-05 | GAP RISK / RISK OFF combined-badge visual differentiation review (BLG-FE-104) | `4242fecb` | `docs/design/2026-07-12__release-v7.0/combined-badge-differentiation/decision_record.md`; `docs/specs/frontend/pages/positions.md#Alerts Column` |

### EPIC-02 — v6.9 Carryover Fixes & Reconciliation (PR #969, merged)

| ST | Title | Commit SHA | Spec References |
|----|-------|-----------|-------------------|
| ST-06 | Reports.js Tax Year P&L tab spec reconciliation (BLG-SPEC-71) | `7f414052` | `docs/specs/frontend/pages/reports.md` |
| ST-07 | Instrument trailing-stop recommendation capture for `trailing_stop_action_rate` metric (BLG-BE-50) | `9683319c` | `docs/specs/metrics_definitions.md#Trailing Stop Action Rate` |
| ST-08 | Dashboard/StrategyBenchmark page-title light-theme contrast gap (BLG-FE-95) | `62e2721f` | `docs/design/2026-07-12__release-v7.0/heading-light-theme-contrast/decision_record.md` |
| ST-09 | Positions Table View breach badge does not match approved spec colour/label (BLG-FE-96) | `479c005a` | `docs/specs/frontend/pages/positions.md#Trailing Stop Column` |
| ST-10 | Gate Progress Indicator copy divergence (BLG-SPEC-73) | `cd97af1d` | `docs/specs/frontend/pages/dashboard.md#6` |
| ST-11 | Add endpoint and date-range filters to `GET /ai/claude-audit-log` (BLG-BE-51) | `95c2a0e4` | `docs/specs/api_contracts/ai_endpoints.md` |
| ST-12 | Sector Concentration: join `ticker_universe` for sector data (BLG-BE-38) | `e5ae2802` | `docs/specs/frontend/pages/risk_dashboard.md#8a. Component: Sector Concentration Heat Map` |

### EPIC-03 — User-Facing Feature Enhancements (PR #970, merged)

| ST | Title | Commit SHA | Spec References |
|----|-------|-----------|-------------------|
| ST-13 | Tax-year P&L CSV export (BLG-FEAT-69) | `3b364084` | `docs/design/2026-07-12__release-v7.0/tax-year-csv-export/ux_spec.md`; `docs/specs/frontend/pages/reports.md` |
| ST-14 | Realized vs. unrealized gain distinction in monthly P&L (BLG-FEAT-70) | `ca04901e` | `docs/design/2026-07-12__release-v7.0/realized-unrealized-split/ux_spec.md`; `docs/specs/frontend/pages/reports.md` |
| ST-15 | Position review cadence nudge (BLG-FEAT-68) | `633fad41` | `docs/design/2026-07-12__release-v7.0/position-review-cadence-nudge/ux_spec.md`; `docs/specs/frontend/pages/positions.md#Last Reviewed Column` |

All 15 in-scope ST items across all three EPICs are `done`, with `acceptance_verified = true` and `deviations_filed = true`.

## Items Returned to Backlog

None — all 15 ST items in the sealed backlog slice were completed within the sprint.

## Items Delegated and Outstanding

None — every story was classified `autonomous` and completed by the engine; no delegation records were created (`delegation_log.md` was not needed).

## QA Evidence Logs Produced

- `claude/cycles/2026-07-12__release-v7.0/qa_evidence_EPIC-01.md` — agent-mediated Director of Quality sign-off (standard sign-off block; autonomous class did not qualify per BLG-GOV-135 — `PositionCard.js` modified), dated 2026-07-13
- `claude/cycles/2026-07-12__release-v7.0/qa_evidence_EPIC-02.md` — Director of Quality sign-off, dated 2026-07-13
- `claude/cycles/2026-07-12__release-v7.0/qa_evidence_EPIC-03.md` — Director of Quality sign-off, dated 2026-07-13

## Process Notes

- **execution_state.json state-tracking gap (ST-04, EPIC-01):** ST-04 was implemented and pushed (commit `19d2d5ba`) and QA-signed-off as Pass in `qa_evidence_EPIC-01.md`, but `execution_state.json` was never updated from `not_started` at the time — left as a silent inconsistency inside an already-merged EPIC. Corrected at this sprint-close resume session (2026-07-13): status set to `done`, `acceptance_verified = true`, `commit_sha` and `spec_references` backfilled (Case C test-authoring — the test file itself is the deliverable), `sign_off_record` populated from the QA evidence log. No re-work was required; this was a bookkeeping correction only.
- ST-09 (EPIC-02) changed the `Positions.js` breach badge title text and added `data-testid="breach-badge"`, replacing the fragile title-text selector used by both `tests/e2e/epic01-v62-stops-alerts.spec.js` (fixed in the same commit, `479c005a`) and `tests/e2e/epic01-v70-grid-badge-parity.spec.js` SC-GVP-09 (EPIC-01, not yet merged to main at the time EPIC-02 was authored). SC-GVP-09's selector could not be fixed from the EPIC-02 branch since that file didn't exist there yet — it was fixed during EPIC-03's rebase onto post-merge `main` instead (see below), verified passing.
- EPIC-01 (PR #968) merged 2026-07-13T11:55:32Z, EPIC-02 (PR #969) merged 2026-07-13T12:01:00Z. EPIC-03's branch was rebased onto post-merge `main`; the one real conflict was in `src/components/positions/PositionCard.js` (EPIC-01's `RiskOffCardBadge`/`PositionCardAlertsRow` vs EPIC-03's `getReviewCadenceState`/`LastReviewedRow`), resolved by keeping both feature sets — verified via syntax check and presence-check of all merged functions. All other files (`backend/database.py`, `backend/main.py`, `docs/reference/openapi.yaml`, `positions.md`, `src/pages/Positions.js`) auto-merged cleanly. The SC-GVP-09 selector fix flagged in EPIC-02's process notes was not auto-resolved by the merge (still referenced the pre-ST-09 title text) — fixed manually during this rebase (`data-testid="breach-badge"` + `"⚠ BREACH"` text), verified passing.
- No orphaned post-merge commits found on any of the three EPIC branches at STEP 4 resume (`git log origin/main..origin/exec/<cycle_id>/<epic_id>` empty for all three).

## Deviations Filed This Sprint

| Spec File | Deviation Ref | Priority | Backlog Reference |
|-----------|---------------|----------|--------------------|
| `docs/specs/frontend/pages/positions.md` | DEV-EPIC01-ST05-01 (Table View RISK OFF badge colour/label diverges from canonical spec — pre-existing since v6.2, unrelated to this sprint's stacking/order work) | P2 | BLG-FE-107 (target v7.1) |

All other stories: no deviation (implementation confirmed to match spec intent).

## Open Escalations

None.

## Net Outcome vs Sprint Goal

All three EPICs shipped and merged to `main` within the sprint, matching the sprint goal in full:

- **Grid View/Table View parity (EPIC-01):** RISK OFF badge, trailing-stop value + breach indicator, and combined-badge stacking are now consistent between Grid View and Table View, with dedicated Playwright coverage (9 scenarios) confirming parity.
- **v6.9 carryover debt (EPIC-02):** Spec reconciliation (Tax Year P&L tab, Gate Progress Indicator copy), a data-correctness fix (Sector Concentration heat map now joins `ticker_universe` instead of using stale/missing sector data), a new metrics-capture instrumentation point (`trailing_stop_action_rate`), a light-theme contrast accessibility fix, and expanded audit-log filtering were all resolved.
- **New features (EPIC-03):** Tax-year P&L CSV export (fixed a pre-existing button-order spec deviation in the process), realized/unrealized P&L split in the Monthly P&L view, and the position review-cadence nudge (new `last_reviewed_at` tracking + `PATCH /positions/{id}/mark-reviewed` endpoint) all shipped.

One P2 deviation (DEV-EPIC01-ST05-01) was discovered as a byproduct of the ST-05 stacking review — pre-existing, unrelated to this sprint's changes, filed to backlog (BLG-FE-107) for v7.1. No scope was deferred; all 15 sealed backlog-slice items were delivered.

## Verification Readiness Statement

| Field | Status |
|-------|--------|
| All spec references populated in execution_state.json | Yes |
| All P1–P3 deviations filed and backlog references updated | Yes |
| QA evidence logs complete and DoQ sign-off non-blank for all EPICs | Yes |
