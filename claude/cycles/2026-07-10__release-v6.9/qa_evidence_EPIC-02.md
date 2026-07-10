Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-10

# QA Evidence — EPIC-02 (Overnight/Weekend Gap Risk Flag)

**EPIC:** EPIC-02 — Overnight/Weekend Gap Risk Flag
**Cycle:** 2026-07-10__release-v6.9
**Sprint goal:** Give traders on-demand visibility into whether an open position still passes its original SI-01 entry rules and whether it carries overnight/weekend gap risk, closing out both named Product Value Alert pull-forward anchors from the 2026-07-10 rebalance.
**Test scenarios used:** `tests/test_gap_risk.py`, `tests/e2e/gap-risk-flag.spec.js`

## ST Item Summary

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-02 | `docs/design/2026-07-10__release-v6.9/gap-risk-flag/ux_spec.md`; `docs/specs/frontend/pages/positions.md#Gap Risk Badge`; `docs/specs/api_contracts/position_endpoints.md#GET /positions/{position_id}/gap-risk` | `GET /positions/{position_id}/gap-risk` combines the DS-04 earnings calendar (`services/earnings_service.py`) with historical OHLCV gap statistics (`services/gap_risk_service.py`) to flag earnings-before-next-session and Friday-close weekend-hold positions; new "Alerts" Table View column (RISK OFF badge relocated into it, GAP RISK badge added, stacked); Grid View GAP RISK badge near ticker; `useGapRisk.js` hook mirrors the existing per-ticker `useEarnings.js` lazy-fetch pattern | AC-01 (earnings-before-next-session flag) — Covers AC-01. AC-02 (weekend-hold flagged at Friday close) — Covers AC-02. AC-03 (historical average gap magnitude / insufficient-history state) — Covers AC-03. AC-04 (§13 sign-off) — see Strategy Rules & System Intent Owner sign-off below. | Pass | None |

## QA Test Coverage

- **Scenarios run:**
  - `tests/test_gap_risk.py` (9 unit/integration tests, backend, all mocked — no live DB/network/yfinance): 404 when position not found; not flagged when no earnings and not Friday; flagged for earnings before next session; not flagged when earnings too far out; flagged for weekend hold on Friday; both reasons stack when earnings and weekend coincide; insufficient-history flag still shown; `_compute_gap_stats` insufficient-below-threshold gate (direct exercise against a mocked yfinance history frame); endpoint returns the gap_risk object via the service.
  - `tests/e2e/gap-risk-flag.spec.js` (8 Playwright scenarios, AC-01–03): no flag shows a dash; earnings-flagged badge with amber-600 (`#D97706`) background; weekend-hold-flagged badge; tooltip/aria-label exposes reason + historical average; insufficient-history badge still shown; both reasons present in tooltip; RISK OFF and GAP RISK badges stack in the same Alerts cell; Grid View badge shown on the position card.
  - Full backend suite: 599 tests passed on the EPIC-02 branch in isolation (590 pre-existing/unrelated + 9 new for this EPIC), 2 pre-existing skips unrelated to this change. [DoQ note: original text miscounted the pre-existing baseline as 596 — re-verified at 590. The cited combined figure of 605 (590 baseline + 6 EPIC-01 + 9 EPIC-02) was independently reproduced by trial-merging both EPIC branches and running the full suite: 605 passed, 2 skipped, 0 failures — confirming no interaction regression between the two EPICs' backend changes, subject to the routine EPIC-01/EPIC-02 merge-conflict resolution in `backend/main.py` and `backend/routers/test.py` required by CLAUDE.md §8 before both land on main.]
  - Full relevant e2e suite run on the EPIC-02 branch in isolation: 47 passed (8 new gap-risk-flag + 16 epic01-v62-stops-alerts + 7 compliance-panel + 16 system-status), 0 failures. [DoQ note: per-file counts corrected during sign-off review — total of 47 and 0 failures independently re-verified via `npx playwright test --list` / execution; original per-file breakdown misattributed 7 tests between epic01-v62-stops-alerts.spec.js and system-status.spec.js.]
- **Regression areas checked:** `tests/e2e/epic01-v62-stops-alerts.spec.js` (23 scenarios, including `SC-RO-*` risk-off badge tests) — confirmed the risk-off badge relocation from the Ticker cell into the new dedicated Alerts column does not break these tests, since they select by `title` attribute rather than cell position; `tests/e2e/compliance-panel.spec.js` (7 scenarios, unaffected — different endpoint/component); `tests/e2e/system-status.spec.js` (9 scenarios, updated for the new 83-endpoint count).
- **Known deviations filed:** None as a formal DEV-record. Implementation note (not a deviation): the story anticipated a `gap_risk` field embedded in `GET /positions`; a dedicated `GET /positions/{position_id}/gap-risk` endpoint was used instead, which the story notes explicitly pre-authorise ("If implementation requires a new endpoint instead, the same same-commit registration rules apply"). Intent (informational gap flag, Alerts-column display with its own defined loading state) is fully preserved — only the transport mechanism differs. Documented in `position_endpoints.md`'s Change Log entry and endpoint "Implementation note".

## Implementation Improvement (incidental, in scope for this story)

`docs/specs/frontend/pages/positions.md` has documented an "Alerts" column (v6.2 ST-05) as the canonical location for the RISK OFF badge since 2026-06-24, but `Positions.js`'s Table View never actually created a dedicated column — the badge was rendered inline in the Ticker cell instead. Since ST-02's own AC requires placing the new GAP RISK badge in "the existing Alerts column" (per design gate and stage4_backlog_slice.md), building the correctly-specified dedicated column was the minimal, spec-faithful way to deliver ST-02 — this incidentally resolves the pre-existing v6.2 placement gap as a byproduct, not as separate scope creep. Verified via the existing `SC-RO-*` Playwright tests (`epic01-v62-stops-alerts.spec.js`), which select the badge by its `title` attribute and remain green after the relocation.

## §13 Sign-Off — Strategy Rules & System Intent Owner

**AC-04:** Confirms no prediction of gap direction or magnitude — informational only.

ST-02 AC-04: Approved — `gap_risk_service.py` surfaces only a known calendar fact (earnings date proximity or Friday-close weekend hold) and a historical average of past overnight/weekend gap magnitudes, gated by a minimum-event threshold. It does not predict the direction or magnitude of the upcoming gap event, and contains no statistical or machine-learning model — purely date comparisons and an arithmetic mean over historical OHLCV data.
Signed off by: Strategy Rules & System Intent Owner (agent-mediated, §5.3)
Date: 2026-07-10

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — `useGapRisk.js` and `Positions.js` use `process.env.REACT_APP_API_URL` via the module-level `API_BASE` constant, consistent with existing codebase convention (`useEarnings.js`, `StrategyCompliancePanel.js`).
- Signed off by: Director of Quality
- Date: 2026-07-10
- Comments: Verified `tests/test_gap_risk.py` (9/9 pass) and `tests/e2e/gap-risk-flag.spec.js` (8/8 pass) exist on `exec/2026-07-10__release-v6.9/EPIC-02` and independently re-ran them, plus the full backend suite and the four relevant e2e specs (47/47 pass) — all AC-01–03 claims (earnings/weekend-hold flag logic, amber-600 badge colour, tooltip/aria-label reasons and historical average, insufficient-history handling, Alerts-column stacking with Risk-Off) match the actual component code and test assertions. Corrected two minor test-count misattributions in the evidence text (per-file e2e breakdown and backend pre-existing baseline) that did not affect the underlying pass/fail conclusions. No unresolved P0/P1 deviations found; sign-off granted.
