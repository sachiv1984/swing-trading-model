Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-05-22

---

# QA Evidence — EPIC-02: Ticker Universe Management Enhancements

**EPIC:** EPIC-02 — Ticker Universe Management Enhancements
**Cycle:** 2026-05-21__release-v3.9
**Sprint goal:** Restore screener data reliability with P1/P2 bug fixes and a degraded-run warning, improve Ticker Universe management, ship the Arc 5 Red Flag Journal for persistent operator-deviation capture, and close all five v3.8 governance carry-forward patches.
**Test scenarios used:** `tests/e2e/ticker-universe.spec.js` (SC-TU-DISP-01, SC-TU-COMP-01)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-05 | `docs/specs/frontend/pages/ticker_universe.md §5` | `displayTicker()` helper strips `.L` suffix from display label only; API requests use full `.L` ticker unchanged | AC-01: LSE tickers show without `.L`; AC-02: API requests unchanged; AC-03: US tickers unaffected; AC-04: Playwright SC-TU-DISP-01 | Pass | None |
| ST-06 | `docs/specs/frontend/pages/ticker_universe.md §4`, `docs/specs/api_contracts/ticker_universe_api_contract.md` | `ensure_company_name_column()` adds `company_name TEXT` to DB; backfill from CSV at startup; `GET /ticker-universe` returns `company_name`; Company Name column added to TU page as 2nd column | AC-01: column added via `ensure_company_name_column()`; AC-02: backfill on startup; AC-03: sync_from_tickers_table populates `company_name`; AC-04: API returns `company_name`; AC-05: Company Name column visible; AC-06: null handled gracefully (empty cell); AC-07: Playwright SC-TU-COMP-01 | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/e2e/ticker-universe.spec.js` — SC-TU-DISP-01 (3 sub-tests: suffix stripped, US tickers unchanged, API request has `.L`), SC-TU-COMP-01 (3 sub-tests: column header visible, known ticker shows company name, LSE ticker shows company name)
- Regression areas checked: Ticker Universe page rendering; existing SC-TU-01 through SC-TU-06 still valid (mock data updated to `BATS.L`; testid references updated); toggle/delete requests still include `.L` suffix (confirmed by SC-TU-DISP-01c)
- Known deviations filed: None

**Frontend testing gate (LL-v3.1-EX-01) verification:**
- ST-05 AC-01 (LSE tickers without `.L` in display): Playwright SC-TU-DISP-01a ✓
- ST-05 AC-03 (US tickers unaffected): Playwright SC-TU-DISP-01b ✓
- ST-05 AC-04 (API requests unchanged): Playwright SC-TU-DISP-01c ✓
- ST-06 AC-05 (Company name column visible): Playwright SC-TU-COMP-01b ✓
- ST-06 AC-07 (Playwright verifies company name): SC-TU-COMP-01b, SC-TU-COMP-01c ✓
- All observable ACs have Playwright test coverage. No human staging run required per LL-v3.1-EX-01 criterion 1.

---

## DoQ Sign-Off

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — TickerUniverse.js uses `API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000"` directly. Confirmed consistent with existing pattern (no issue).
- [x] Frontend testing gate (LL-v3.1-EX-01): All observable ACs covered by Playwright tests SC-TU-DISP-01 and SC-TU-COMP-01
- Signed off by: Director of Quality
- Date: 2026-05-22
- Comments: ST-05 and ST-06 fully verified. displayTicker() correctly strips .L for display while preserving the full ticker in all API requests. ensure_company_name_column() adds the column idempotently and backfills from CSV. Company Name renders as the 2nd column with null handled as empty string. All observable ACs covered by Playwright tests SC-TU-DISP-01 (3 sub-tests) and SC-TU-COMP-01 (3 sub-tests) at the 1280px configured viewport. No deviations found. Approved.
- Sign-off method: agent_mediated
