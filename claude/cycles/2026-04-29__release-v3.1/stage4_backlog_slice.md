**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v3.1
**Cycle:** 2026-04-29__release-v3.1
**Last Updated:** 2026-04-29

---

# Backlog Slice — v3.1 Arc 2 Start: Trade Plan Object & Pre-Trade Research Foundation

**Sprints:** 2 | **Stories:** 14 | **EPICs:** 4

---

## EPIC-01 — Arc 2 Foundation: Trade Plan Object

**Maps to:** S2-01
**Sprint:** Sprint 1 (ST-01, ST-02) + Sprint 2 (ST-03)
**Owner:** Head of Specs Team + Data Model Domain & Schema Owner
**Theme:** Deliver the Trade Plan data model, backend CRUD, and frontend creation/detail flow. Foundation for all remaining Arc 2 work.

### ST-01 — Trade Plan spec authoring: data model schema + API contract

**Type:** Spec authoring
**Effort:** S (~1 day)
**Sprint:** Sprint 1
**Depends on:** nothing
**Blocks:** ST-02, ST-03

**Acceptance Criteria:**
- `docs/specs/data_model.md` updated with Trade Plan schema: fields include `id`, `position_id` (nullable — plan may exist before position), `ticker`, `market`, `created_at`, `setup_thesis`, `entry_rationale`, `regime_context_at_entry`, `r_target`, `early_exit_conditions`, `confirmation_criteria`, `checklist_completed` (bool), `checklist_items` (JSON), `status` (draft/active/closed)
- New API contract doc `docs/specs/api_contracts/trade_plan_endpoints.md` authored covering: `POST /trade-plans`, `GET /trade-plans`, `GET /trade-plans/{id}`, `PUT /trade-plans/{id}`, `DELETE /trade-plans/{id}`, `GET /trade-plans/by-position/{position_id}`
- All endpoints added to `docs/reference/openapi.yaml`
- Data Model Domain & Schema Owner and Head of Specs Team sign-off recorded

---

### ST-02 — Trade Plan backend: migration, CRUD endpoints, test registration

**Type:** Backend implementation
**Effort:** M (~2.5 days)
**Sprint:** Sprint 1
**Depends on:** ST-01
**Blocks:** ST-03, ST-04 (indirectly)

**Acceptance Criteria:**
- Database migration creates `trade_plans` table matching ST-01 schema
- `backend/routers/trade_plans.py` implements all 6 endpoints per ST-01 API contract
- All 6 endpoints registered in `backend/routers/test.py`
- `SystemStatus.js` hardcoded endpoint count updated to reflect new total
- `docs/reference/openapi.yaml` entries match ST-01 contract
- Unit tests pass; existing endpoints unaffected
- Migration is reversible (down migration included)

---

### ST-03 — Trade Plan frontend: creation flow and detail view

**Type:** Frontend implementation
**Effort:** M (~2.5 days)
**Sprint:** Sprint 2
**Depends on:** ST-02 (backend live) + design gate pass
**Blocks:** nothing

**Acceptance Criteria:**
- Trade Plan creation form accessible from positions list and watchlist (entry point TBD by design gate)
- Form fields: setup thesis (textarea), entry rationale (textarea), regime context (auto-populated from current regime status), R target (numeric), early exit conditions (textarea), confirmation criteria (textarea)
- Saved trade plan displays on position detail with all fields
- `GET /trade-plans/by-position/{position_id}` used to associate trade plan with open position
- No regression to positions list or watchlist pages

---

## EPIC-02 — Pre-Trade Research View Foundation

**Maps to:** S2-02
**Sprint:** Sprint 2
**Owner:** Head of Specs Team + API Contracts & Documentation Owner
**Theme:** Spec and backend foundation for the Pre-Trade Research View. Frontend delivery (PT-02 UI) deferred to v3.2 pending design gate.

### ST-04 — Pre-Trade Research View API contract spec authoring

**Type:** Spec authoring
**Effort:** S (~0.75 day)
**Sprint:** Sprint 2
**Depends on:** ST-02 (Trade Plan data model available as context)
**Blocks:** ST-05

**Acceptance Criteria:**
- `docs/specs/api_contracts/pre_trade_research_endpoints.md` authored
- New endpoint `GET /research/{ticker}` (or `GET /trade-plans/research/{ticker}`) documented: aggregates signal strength, market correlation (v2.7 backend), regime status, sector context (DS-03), earnings proximity (DS-04, if available), prospective heat (`GET /portfolio/prospective-heat`)
- Response schema defined: all fields documented with types and nullability
- Endpoint added to `docs/reference/openapi.yaml`
- API Contracts Documentation Owner sign-off recorded

---

### ST-05 — Pre-Trade Research View backend: aggregation endpoint

**Type:** Backend implementation
**Effort:** M (~2.5 days)
**Sprint:** Sprint 2
**Depends on:** ST-04
**Blocks:** nothing (frontend deferred to v3.2)

**Acceptance Criteria:**
- `backend/routers/research.py` (or equivalent) implements `GET /research/{ticker}` per ST-04 contract
- Endpoint registered in `backend/routers/test.py`
- `SystemStatus.js` hardcoded endpoint count updated
- Response aggregates from: signal service, portfolio service (prospective heat), market correlation service, sector data (DS-03 enrichment), earnings data (DS-04 if available in v3.1)
- Graceful nulls for data not yet available (earnings if DS-04 not complete at time of ST-05 implementation)
- `docs/reference/openapi.yaml` entry matches ST-04 contract
- No regression to existing endpoints

---

## EPIC-03 — Arc 1 Completion & Screener Quality

**Maps to:** S2-03, S2-04
**Sprint:** Sprint 1 (ST-06, ST-07, ST-09) + Sprint 2 (ST-08, ST-10)
**Owner:** Backend Engineering Patterns Owner + QA & Testing Owner
**Theme:** Complete Arc 1 with Earnings Calendar integration; fix P1 screener bug; deliver screener QA documentation.

### ST-06 — Fix screener UK ticker display and watchlist promotion (BLG-FE-20)

**Type:** Bug fix + UX
**Effort:** S (~0.5 day)
**Sprint:** Sprint 1 (Priority: P1 — first story in sprint)
**Depends on:** nothing
**Blocks:** nothing

**Acceptance Criteria:**
- `src/pages/Screener.js`: UK tickers display without `.L` suffix in the results table (strip when `result.market === "UK"`)
- `WatchlistPopover.handleAdd`: strips `.L` from ticker before posting to `POST /watchlist` for UK tickers
- "Add X to Watchlist" popover header also strips `.L` from the label
- Ticker column font treatment reviewed and confirmed (monospace vs `font-semibold`)
- US ticker display and watchlist promotion unaffected
- No regression to Market badge, signal scores, ATR, or news panel

---

### ST-07 — Earnings Calendar backend + OpenAPI (DS-04)

**Type:** Spec authoring + Backend implementation
**Effort:** M (~2.0 days)
**Sprint:** Sprint 1
**Depends on:** nothing
**Blocks:** ST-08

**Acceptance Criteria:**
- `docs/specs/api_contracts/earnings_endpoints.md` (or extension of screener_api_contract.md) authored: `GET /earnings/{ticker}` returns `{ ticker, next_earnings_date, days_until_earnings, fiscal_quarter, data_source }` or null if unavailable
- `GET /earnings/bulk` (optional, for screener batch) documented if needed
- All new endpoints added to `docs/reference/openapi.yaml`
- Backend implementation fetches earnings date from Yahoo Finance (existing yfinance dependency); returns null gracefully if unavailable
- Endpoints registered in `backend/routers/test.py`
- `SystemStatus.js` endpoint count updated
- Data freshness validated: Yahoo Finance earnings dates are generally reliable 2–4 weeks out; spec documents known limitations

---

### ST-08 — Earnings Calendar frontend (DS-04)

**Type:** Frontend implementation
**Effort:** M (~2.0 days)
**Sprint:** Sprint 2
**Depends on:** ST-07 + design gate pass (earnings display is a new UI element on 3 pages)
**Blocks:** nothing

**Acceptance Criteria:**
- Earnings date displayed on screener results table (new column or inline badge): `{N} days` or `N/A` if unavailable
- Earnings date displayed on watchlist page for each watchlisted ticker
- Earnings date displayed on open positions page (proximity warning if within 5 days)
- Earnings dates sourced from `GET /earnings/{ticker}` endpoint
- Null/unavailable gracefully hidden (no empty column or broken display)
- No regression to screener results, watchlist, or positions page rendering

---

### ST-09 — Screener accuracy test protocol (BLG-QA-11)

**Type:** QA documentation
**Effort:** S (~0.75 day)
**Sprint:** Sprint 1
**Depends on:** nothing
**Blocks:** BLG-QA-10 (ST-10 references this protocol)

**Acceptance Criteria:**
- Written protocol document `docs/qa/screener_accuracy_protocol.md` created
- Protocol covers: frequency (weekly for first month post-live, then monthly), sample size (minimum 10 results per run), comparison methodology (compare screener output against manually computed filters for 3 known tickers), pass/fail thresholds (≤5% discrepancy on ATR-based scores, 0 discrepancy on regime gate)
- Protocol references BLG-QA-10 scenario library (ST-10) where applicable
- Director of Quality sign-off recorded

---

### ST-10 — Screener scenario library (BLG-QA-10)

**Type:** QA documentation
**Effort:** M (~1.5 days)
**Sprint:** Sprint 2
**Depends on:** ST-09 (protocol as reference)
**Blocks:** nothing

**Acceptance Criteria:**
- Scenario library document `docs/qa/screener_scenarios.md` created with ≥10 scenarios
- Scenarios cover: normal results (mixed UK/US), zero results (all filters too tight), max results (all filters open), single-sector sweep, conflicting filter combinations, ticker with missing data, UK-only market filter, US-only market filter
- Each scenario has: name, input filters, expected behaviour, pass/fail criteria
- Library serves as reference for both manual QA and future automation
- QA & Testing Owner sign-off recorded

---

## EPIC-04 — Operations, Governance & Quick Wins

**Maps to:** S2-05, S2-06, S2-07
**Sprint:** Sprint 1
**Owner:** Infrastructure & Operations Owner + Financial Reporting & Records Owner + PMO Lead
**Theme:** Security policy docs, monthly P&L feature, and governance prompt patches from carry-forward.

### ST-11 — Monthly P&L summary report (BLG-FEAT-19)

**Type:** Product feature (reporting)
**Effort:** S (~0.75 day)
**Sprint:** Sprint 1
**Depends on:** nothing
**Blocks:** nothing

**Acceptance Criteria:**
- New endpoint `GET /reports/monthly-pnl` or extension of existing reports endpoint returns month-by-month realised P&L for current and prior year
- Response: `[{ year, month, realised_pnl_gbp, trade_count }]` sorted descending
- Endpoint registered in `backend/routers/test.py`; `docs/reference/openapi.yaml` updated; `reports_endpoints.md` updated
- Frontend: monthly breakdown table displayed in the financial reporting section, consistent with existing P&L formatting
- No regression to annual tax-year P&L report

---

### ST-12 — External API security policy docs & dependency risk register (BLG-SEC-03, BLG-SEC-04, BLG-GOV-17)

**Type:** Security documentation + Governance documentation
**Effort:** S (~0.75 day combined — three XS/S documents)
**Sprint:** Sprint 1
**Depends on:** nothing
**Blocks:** nothing

**Acceptance Criteria:**
- `docs/ops/alpaca_key_rotation_policy.md` created: rotation schedule (every 90 days or on suspected compromise), trigger conditions, step-by-step rotation procedure referencing Render environment variables, accepted by Cybersecurity & Trust Lead
- `docs/ops/external_api_credential_inventory.md` created: lists all external credentials (Alpaca API key, news API key), each entry has service, credential type, scope, storage location reference, rotation policy reference; no sensitive values stored; accepted by Cybersecurity & Trust Lead
- `docs/ops/external_api_dependency_register.md` created: Alpaca and news API entries; each entry: service, failure modes identified (Alpaca null bars crash — v3.0 incident; hyphenated ticker handling), mitigations in place, monitoring approach; accepted by PMO Lead

---

### ST-13 — execution_prompt.md §3.1.A reclassification backfill instruction (CF-01)

**Type:** Governance prompt patch
**Effort:** S (~0.5 day)
**Sprint:** Sprint 1
**Depends on:** nothing
**Blocks:** nothing

**Acceptance Criteria:**
- `claude/system/execution_prompt.md` §3.1.A updated: instruction added — "If stories are reclassified from `delegated_frontend` to `autonomous` mid-sprint, the accepting engine must backfill `test_scenarios` in `execution_state.json` at the time of reclassification. `test_scenarios` must be populated with the test file paths before the story's QA evidence log entry is written."
- `execution_prompt.md` version bumped per §6 checklist
- `OPERATIONAL_GUIDE.md` §8 source prompt header and §14 entry updated
- `claude/system/prompt_change_log.md` entry appended
- All 4 §6 governance checklist steps verified complete

---

### ST-14 — execution_prompt.md STEP 8.5 output target fix (CF-02)

**Type:** Governance prompt patch
**Effort:** S (~0.5 day)
**Sprint:** Sprint 1
**Depends on:** nothing
**Blocks:** nothing

**Acceptance Criteria:**
- `claude/system/execution_prompt.md` STEP 8.5 updated: explicit note added — "Output target is `lessons_learnt_cycle.md` — do NOT append to `lessons_learnt.md` (Release Planning artefact). Create `lessons_learnt_cycle.md` if absent."
- `execution_prompt.md` version bumped (can be combined with ST-13 into a single version bump if committed together)
- `OPERATIONAL_GUIDE.md` §8 source prompt header and §14 entry updated
- `claude/system/prompt_change_log.md` entry appended
- All 4 §6 governance checklist steps verified complete
- Optional: include Playwright `waitFor` pattern advisory (CF-03) as a brief note in `claude/system/execution_prompt.md` E2E testing guidance section — advisory only, non-blocking

---

## Sprint Assignment Summary

| Sprint | EPICs | Stories | Estimated Effort |
|--------|-------|---------|-----------------|
| Sprint 1 | EPIC-01 (ST-01, ST-02), EPIC-03 (ST-06, ST-07, ST-09), EPIC-04 (ST-11, ST-12, ST-13, ST-14) | 9 stories | ~9.0 days |
| Sprint 2 | EPIC-01 (ST-03), EPIC-02 (ST-04, ST-05), EPIC-03 (ST-08, ST-10) | 5 stories | ~9.75 days |
| **Total** | 4 EPICs | **14 stories** | **~18.75 days** |

**Capacity note (WARN):** Both sprints exceed solo dev evening/weekend capacity estimate (~5–6 days each). Sprint Planning Engine must review and defer ST-10 or ST-05 if capacity tight.
