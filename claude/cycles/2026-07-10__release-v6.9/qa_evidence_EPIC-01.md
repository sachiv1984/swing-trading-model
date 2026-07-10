Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-10

# QA Evidence — EPIC-01 (On-Demand Pre-Entry (SI-01) Compliance Recheck)

**EPIC:** EPIC-01 — On-Demand Pre-Entry (SI-01) Compliance Recheck
**Cycle:** 2026-07-10__release-v6.9
**Sprint goal:** Give traders on-demand visibility into whether an open position still passes its original SI-01 entry rules and whether it carries overnight/weekend gap risk, closing out both named Product Value Alert pull-forward anchors from the 2026-07-10 rebalance.
**Test scenarios used:** `tests/test_compliance_recheck.py`, `tests/e2e/compliance-recheck.spec.js`

## ST Item Summary

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-01 | `docs/design/2026-07-10__release-v6.9/on-demand-compliance-recheck/ux_spec.md`; `docs/specs/frontend/pages/positions.md#Compliance Recheck Panel`; `docs/specs/api_contracts/position_endpoints.md#GET /positions/{position_id}/compliance-recheck` | `GET /positions/{position_id}/compliance-recheck` re-applies the 5 SI-01 pre-entry checks against a position's current state (not entry-time snapshot); `ComplianceRecheckModal.js` reuses the `PreEntryValidationPanel` pass/warn/fail visual pattern; "Recheck Compliance" action added to Table View Actions column and Grid View card footer | AC-01 (backend re-check against current state) — Covers AC-01. AC-02 (frontend rendering, pass/warn/fail/override states) — Covers AC-02. AC-03 (on-demand only, no polling) — Covers AC-03. AC-04 (§13 sign-off) — see Strategy Rules & System Intent Owner sign-off below. | Pass | None |

## QA Test Coverage

- **Scenarios run:**
  - `tests/test_compliance_recheck.py` (6 unit/integration tests, backend, all mocked — no live DB/network): 404 when position not found; 404 when position not open; all 5 rule keys returned with minimal `{rule_key, status, detail}` shape; overall_status aggregation (fail when regime off); sector concentration excludes the rechecked position from its own baseline (regression guard against the double-count a literal reuse of the prospective-entry formula would produce); sizing validity uses the current effective stop, not the entry-time stop.
  - `tests/e2e/compliance-recheck.spec.js` (8 Playwright scenarios, AC-02): action visible in Table View Actions column; modal opens with loading state; Pass result (badge + 5 rule rows, no override checkbox); Warn result (badge + override checkbox); Fail result (badge + toggleable override checkbox); API failure (error state + retry); close button dismisses modal; Grid View action present on card footer.
  - Full backend suite: 596 tests passed on the EPIC-01 branch in isolation (590 pre-existing/unrelated + 6 new for this EPIC), 2 pre-existing skips unrelated to this change. [DoQ note: original text miscounted the pre-existing baseline as 596 — re-verified at 590. The cited combined figure of 605 (590 baseline + 6 EPIC-01 + 9 EPIC-02) was independently reproduced by trial-merging both EPIC branches and running the full suite: 605 passed, 2 skipped, 0 failures — confirming no interaction regression between the two EPICs' backend changes, subject to the routine EPIC-01/EPIC-02 merge-conflict resolution in `backend/main.py` and `backend/routers/test.py` required by CLAUDE.md §8 before both land on main.]
  - Full relevant e2e suite run on the EPIC-01 branch in isolation: 47 passed (8 new compliance-recheck + 16 epic01-v62-stops-alerts + 7 compliance-panel + 16 system-status), 0 failures. [DoQ note: per-file counts corrected during sign-off review — total of 47 and 0 failures independently re-verified via `npx playwright test --list` / execution; original per-file breakdown misattributed 7 tests between epic01-v62-stops-alerts.spec.js and system-status.spec.js.]
- **Regression areas checked:** `tests/e2e/epic01-v62-stops-alerts.spec.js` (23 scenarios covering trailing stop / risk-off badges — unaffected since this EPIC does not touch the Ticker or Stop cells), `tests/e2e/compliance-panel.spec.js` (7 scenarios covering the existing Strategy Compliance Panel — unaffected, different endpoint/component), `tests/e2e/system-status.spec.js` (9 scenarios, updated for the new 83-endpoint count).
- **Known deviations filed:** None. No spec deviation — implementation matches ux_spec.md and stage4_backlog_slice.md AC-01–03 intent. The sector-concentration formula adaptation (excluding self from the baseline sum) is a necessary correctness adaptation for the recheck-of-an-existing-position use case, documented in `compliance_recheck_service.py`'s module docstring and in `position_endpoints.md`'s "Current-state adaptation notes" — not a divergence from any stated AC.

## Observation (non-blocking, filed for future backlog consideration)

While implementing ST-02's Alerts column (EPIC-02), it was discovered that `docs/specs/frontend/pages/positions.md`'s Grid View section (§Alert badges, v6.2 changelog line 167) documents Trail Stop breach and RISK OFF badges as appearing on the Grid View position card, but `PositionCard.js` has never actually rendered them (pre-existing gap from v6.2 ST-01/ST-05, unrelated to this sprint's stories). Not corrected here — out of scope for ST-01/ST-02's acceptance criteria. Recommend a future backlog item to align Grid View with the documented spec or update the spec to reflect Table-View-only scope for those two badge types.

## §13 Sign-Off — Strategy Rules & System Intent Owner

**AC-04:** Confirms re-running existing deterministic rules on demand introduces no new automation/prediction surface.

ST-01 AC-04: Approved — `compliance_recheck_service.py` re-applies the existing SI-01 checks (`_check_regime`, `_check_cash_constraint`, `_check_earnings_proximity`, `_check_sizing_validity`) verbatim, with only a deterministic double-counting fix for sector concentration on an already-open position. The endpoint is invoked solely by the user-triggered "Recheck Compliance" action with no polling/background job, and does not touch or duplicate SI-02 (drift detection). No new scoring, statistical model, or prediction is introduced.
Signed off by: Strategy Rules & System Intent Owner (agent-mediated, §5.3)
Date: 2026-07-10

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — `ComplianceRecheckModal.js` and `Positions.js` use `process.env.REACT_APP_API_URL` via the module-level `API_BASE` constant, consistent with existing codebase convention (`useEarnings.js`, `StrategyCompliancePanel.js`).
- Signed off by: Director of Quality
- Date: 2026-07-10
- Comments: Verified `tests/test_compliance_recheck.py` (6/6 pass) and `tests/e2e/compliance-recheck.spec.js` (8/8 pass) exist on `exec/2026-07-10__release-v6.9/EPIC-01` and independently re-ran them, plus the full backend suite and the four relevant e2e specs (47/47 pass) — all AC-02 rendering/state claims (pass/warn/fail badges, override checkbox, loading, error+retry, Grid View) match the actual component code and test assertions. Corrected two minor test-count misattributions in the evidence text (per-file e2e breakdown and backend pre-existing baseline) that did not affect the underlying pass/fail conclusions. No unresolved P0/P1 deviations found; sign-off granted.
