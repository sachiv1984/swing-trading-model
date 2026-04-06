Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-04-06

---

# QA Evidence Log — EPIC-03: Frontend & Operations Quick Wins

**Cycle:** 2026-04-05__release-v2.5
**Sprint:** Sprint 2

---

## ST-07 — Add --max-time to GitHub Actions curl calls

**Spec references:** `.github/workflows/alert-evaluation.yml`, `.github/workflows/daily-snapshot.yml`

**Commit:** TBD (pending)

**What was built:**
Added `--max-time 120` to all curl calls in both workflows:
- `alert-evaluation.yml`: `curl -f --max-time 120 -X POST` (1 call)
- `daily-snapshot.yml`: `curl --max-time 120 -X GET/POST` (3 calls — positions/analyze, portfolio/snapshot, signals/generate)

**Acceptance criteria:**

| Dimension | Criteria | Status |
|-----------|----------|--------|
| Technical | All curl calls in alert-evaluation.yml and daily-snapshot.yml have `--max-time 120` | Pass |
| Quality | No regression to other workflow functionality; flag added at correct position | Pass (code review) |
| Security | N/A | N/A |
| Verification | Code review confirming flag present on all curl calls; no existing flags removed | Pending DoQ |

---

## ST-08 — Fix Avg Slippage StatsCard gradient rendering

**Spec references:** `docs/testing/slippage_scenarios.md#5`

**Commit:** TBD (pending)

**What was built:**
Updated `docs/testing/slippage_scenarios.md` §5 (Known Deviations) to mark DEV-ST14-01 as RESOLVED:
- Status updated to "RESOLVED — v2.5 (2026-04-06)"
- Resolution documented: fix applied in two stages (commit 8650223 and 67d7285) in prior sprints
- SC-SLIP-03 impact note updated: deviation resolved; no longer "Pass with notes"
- Document version bumped from 1.1 to 1.2

**Note:** The underlying code fix was applied in prior sprints (commit `8650223` changed `color="cyan"` → `gradient="violet"`; commit `67d7285` added conditional emerald/rose logic). ST-08's deliverable for v2.5 is the documentation closure of DEV-ST14-01.

**Acceptance criteria:**

| Dimension | Criteria | Status |
|-----------|----------|--------|
| Technical | `slippage_scenarios.md` §5 marks DEV-ST14-01 as resolved with resolution detail | Pass |
| Quality | Existing gradient code confirmed correct (valid gradient key for all states); SC-SLIP-03 impact note updated | Pass (code review) |
| Security | N/A | N/A |
| Verification | Code review confirming gradient prop uses valid StatsCard gradient keys in all code paths | Pending DoQ |

---

## ST-09 — Fee drag metric on Trade History

**Spec references:** `docs/specs/metrics_definitions.md`, `docs/specs/frontend/pages/trade_history.md`, `docs/specs/api_contracts/trade_endpoints.md`, `docs/reference/openapi.yaml`

**Commit:** TBD (pending)

**What was built:**
Full fee drag metric implementation — backend, API contract, OpenAPI, frontend:

1. **Backend (`backend/services/trade_service.py`):**
   - Added `fee_drag_pct` per trade: `round(exit_fees / gross_proceeds * 100, 2)` — null when gross_proceeds null or zero
   - Added `avg_fee_drag_pct` aggregate: mean of non-null `fee_drag_pct` values
   - Both fields added to response; empty-trades path returns `null` for both

2. **API contract (`docs/specs/api_contracts/trade_endpoints.md`):**
   - `fee_drag_pct` and `avg_fee_drag_pct` added to response example JSON
   - Field notes added for both fields
   - Version bumped 2.1.0 → 2.2.0; changelog entry appended

3. **OpenAPI (`docs/reference/openapi.yaml`):**
   - `avg_fee_drag_pct` added to `TradeHistoryResponse` top-level properties
   - `fee_drag_pct` added to `TradeHistoryResponse.trades.items.properties`
   - Description updated with v2.2.0 note; openapi.yaml version bumped 2.4.0 → 2.5.0

4. **Frontend — table (`src/components/trades/TradeHistoryTable.js`):**
   - `feeDragSort` state + `cycleFeeSort` handler added
   - `FeeDragSortIcon` component added (amber sort arrows)
   - Fee drag sort applied in `displayTrades` useMemo
   - "Fee Drag %" column header added after Slippage (sortable, tooltip)
   - Fee drag cell added in each trade row (amber text, `+X.XX%` format)
   - Expanded row colSpan bumped 8 → 9

5. **Frontend — page (`src/pages/TradeHistory.js`):**
   - "Avg Fee Drag" StatsCard added after Avg Entry Dev. (amber gradient, `+X.XX%` format)
   - Grid cols changed from `lg:grid-cols-5` to `lg:grid-cols-3 xl:grid-cols-6`

6. **Metrics definitions (`docs/specs/metrics_definitions.md`):**
   - "Fee Drag" section added before Appendix A with canonical formula, qualifying conditions, sign convention, data source, display spec, relationship to slippage
   - Version bumped 1.8.0 → 1.9.0; changelog entry appended

**Acceptance criteria:**

| Dimension | Criteria | Status |
|-----------|----------|--------|
| Technical | `fee_drag_pct` per trade and `avg_fee_drag_pct` in GET /trades response; frontend StatsCard and column present; all 4 spec documents updated | Pass |
| Quality | Null handling correct (gross_proceeds null/zero → null); amber colour not green/red; formula matches canonical spec | Pass (code review) |
| Security | N/A (read-only metric, no new endpoints) | N/A |
| Verification | Code review confirming formula, null guard, colour treatment, column placement; staging run or screenshot confirming fee drag renders in table and StatsCard | Pending DoQ |

**Frontend DoQ verification note:** Per CLAUDE.md §2, AC requiring observable UI behaviour (column presence, amber colour rendering, StatsCard display) cannot be verified by code review alone. DoQ must record whether verification was by code review, local run, or staging.

---

## EPIC-03 Consolidation

**EPIC:** EPIC-03 — Frontend & Operations Quick Wins
**Cycle:** 2026-04-05__release-v2.5
**Sprint goal:** Close DEV-ST14-01 deviation, prevent CI workflow hangs, deliver fee drag metric.
**Test scenarios used:** `docs/testing/slippage_scenarios.md` v1.2 (ST-08 closure); no new scenario files required (ST-07 and ST-09 have no scenario file dependencies)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|-------|
| ST-07 | alert-evaluation.yml, daily-snapshot.yml | `--max-time 120` added to all curl calls | All curl calls time-limited | Pending DoQ | None |
| ST-08 | slippage_scenarios.md §5 | DEV-ST14-01 marked resolved in scenarios doc | Deviation closed; SC-SLIP-03 no longer "Pass with notes" | Pending DoQ | None |
| ST-09 | metrics_definitions.md, trade_history.md, trade_endpoints.md, openapi.yaml | fee_drag_pct backend + API contract + OpenAPI + frontend column + StatsCard | Fee drag visible in Trade History table and summary bar | Pending DoQ | See note on frontend verification |

**QA test coverage:**
- Scenarios run: Manual — code review of all three story implementations
- Regression areas checked: trade_service.py (slippage fields unaffected), TradeHistoryTable (existing sort logic preserved), openapi.yaml (existing schemas unmodified)
- Known deviations filed: None

**QA sign-off block:** (Director of Quality completes this)
- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked
- [ ] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A (fee drag display only; no new API calls)
- [ ] Frontend DoQ verification method recorded for ST-09 (code review / local run / staging)
- Signed off by: Director of Quality
- Date: <fill in — must be non-blank (LL-v2.3-EX-01)>
- Comments:
