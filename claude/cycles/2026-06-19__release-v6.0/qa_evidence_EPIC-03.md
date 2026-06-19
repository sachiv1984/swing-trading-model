Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-06-19

---

# QA Evidence — EPIC-03: Screener Data Quality Telemetry

**EPIC:** EPIC-03 — Screener data quality telemetry
**Cycle:** 2026-06-19__release-v6.0
**Sprint goal:** Ship the P0 signal correctness fix and deliver the Trader's Morning Briefing and net-of-costs features to resolve the Product Value Alert, complete Screener data quality telemetry, and advance SI-05 effectiveness reviews as within-sprint gates clear.
**Test scenarios used:** tests/e2e/screener-quality.spec.js (SC-SQ-01 to SC-SQ-05)

---

## ST-04 — Screener data quality telemetry

| AC | Spec AC | Evidence method | Result |
|----|---------|-----------------|--------|
| AC-01 | GET /screener/results includes tickers_requested, tickers_loaded, tickers_failed, last_full_run_utc, run_quality | New fields added to get_screener_results(); backed by tickers_requested + failed_tickers JSONB columns added to screener_runs; run_quality derived from degraded_run + tickers_loaded | Pass |
| AC-02 | Screener page shows structured quality panel for all three run_quality values | ScreenerQualityPanel component replaces DegradedRunBanner; data-testid="screener-quality-panel" data-quality="FULL/DEGRADED/FAILED" | Pass |
| AC-03 | FULL state: green badge + loaded ratio (e.g. "500 / 500") | SC-SQ-01: "Full run" + "500 / 500" visible; panel has data-quality="FULL" | Pass |
| AC-04 | DEGRADED state: amber badge + loaded ratio + expandable failed ticker list + incomplete message | SC-SQ-02: amber panel visible with "375 / 500" and "3 tickers failed to load"; SC-SQ-03: expand button reveals ticker list | Pass |
| AC-05 | FAILED state: red badge + retry prompt | SC-SQ-04: "Screener run failed" + retry button visible | Pass |
| AC-06 | Stale advisory renders when last_full_run_utc > 24 hours ago | SC-SQ-05: data-testid="stale-advisory" + "Last full run: N hours ago" visible | Pass |
| AC-07 | Playwright: all three quality states render correctly; failed ticker count shown in DEGRADED state; retry prompt shown in FAILED state | tests/e2e/screener-quality.spec.js — 5 scenarios covering all 3 states + ticker list expansion + stale advisory | Pass |

**Schema changes:** screener_runs table gets `tickers_requested INTEGER` and `failed_tickers JSONB` columns via `ensure_screener_results_table()` (idempotent ADD IF NOT EXISTS).
**Spec changes:** screener_api_contract.md v1.1→v1.2 with new field documentation; openapi.yaml /screener/results schema updated.
**Note:** EPIC-03 branch must rebase onto main after EPIC-02 merges before PR is opened (per ST-04 notes and CLAUDE.md §8 merge conflict resolution guidance). No PR opened until post-rebase.

**ST-05 (Conditional):** Gate ~2026-06-23 (SI-05 Telegram digest delivery after FRONTEND_URL set). All ACs are staging-only. Not started — awaiting gate confirmation.

**Deviations:** None

---

## EPIC-03 Consolidation Block

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-04 | stage4_backlog_slice.md#ST-04, screener_api_contract.md v1.2 | screener_batch_service.py: failed_ticker tracking in run_screener(), tickers_requested + failed_tickers columns in screener_runs, get_screener_results() returns 5 new fields; Screener.js: ScreenerQualityPanel replaces DegradedRunBanner; screener_api_contract.md v1.2; openapi.yaml updated; 5 Playwright scenarios | All 7 ACs verified; Playwright AC-07 satisfied | Pass | None |
| ST-05 | stage4_backlog_slice.md#ST-05 | Conditional — gate ~2026-06-23. Not started. Awaiting SI-05 digest delivery confirmation | N/A (gate pending) | Not applicable | None |

**QA test coverage:**
- Scenarios run: tests/e2e/screener-quality.spec.js (5 tests — FULL, DEGRADED (badge+ratio), DEGRADED (expandable list), FAILED, stale advisory)
- Regression areas checked: GET /screener/results response shape (degraded_run, failure_rate fields preserved), DegradedRunBanner → ScreenerQualityPanel replacement (backward-compatible via runQuality null-check), openapi.yaml drift gate
- Known deviations filed: None

---

## BLG-GOV-19 Autonomous DoQ Sign-Off

Classification: Autonomous — ST-04 is `classification: autonomous`. DoQ sign-off is agent-mediated per BLG-GOV-19. ST-05 not started (conditional gate pending).

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec (ST-04)
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] Playwright coverage confirmed for all frontend-visible observable ACs (AC-07)
- Signed off by: Director of Quality (agent-mediated, BLG-GOV-19)
- Date: 2026-06-19
- Comments: ST-04 Screener quality telemetry — 5 Playwright scenarios covering all 3 run_quality states (FULL/DEGRADED/FAILED), expandable failed ticker list, and stale advisory. Frontend testing gate satisfied. OpenAPI drift gate requirements met (same-commit openapi.yaml update). ST-05 deferred pending gate 2026-06-23 — no PR impact until gate confirmed. EPIC-03 branch requires rebase onto main after EPIC-02 merges before PR can be opened.
