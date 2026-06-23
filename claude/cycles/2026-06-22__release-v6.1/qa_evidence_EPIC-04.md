**Owner:** Director of Quality
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-23

---

# QA Evidence — EPIC-04: Setup Quality Score / PT-04

**EPIC:** EPIC-04 — Setup Quality Score / PT-04 (Sprint 1 backend, Sprint 2 frontend)
**Cycle:** 2026-06-22__release-v6.1
**Sprint goal:** Deliver the Setup Quality Score backend engine (ST-08) to enable PT-04 gate progress measurement once ≥20 closed trades exist.
**Test scenarios used:** Unit tests: tests/test_setup_quality_score.py (gate_not_met, mixed history, perfect history cases)

---

## ST-08 — Setup Quality Score — backend engine (PT-04)

**Spec reference:** `docs/specs/api_contracts/trade_plan_endpoints.md` v0.5; `claude/strategy/strategy_rules.md`
**Commit SHA:** 302046d8
**Delegation class:** autonomous

**What was built:**
- `GET /trade-plans/setup-quality-score?ticker={ticker}` endpoint in `backend/routers/trade_plans.py`.
- Gate check: returns `{"gate_not_met": true, "min_trades_required": 20, "current_trades": N}` when closed trade count < 20.
- Score computation when gate met: win_rate × 0.6 + max(avg_pnl_pct, 0) × 0.4, clamped 0–100.
- Response includes: `score`, `matching_trades`, `win_rate`, `average_pnl_pct`, `score_explanation`, `ticker`.
- Endpoint added to `backend/routers/test.py` (68 pre-rebase total) and `docs/reference/openapi.yaml` in same commit.
- `docs/specs/api_contracts/trade_plan_endpoints.md` v0.5 with full spec for GET /trade-plans/setup-quality-score.
- `tests/test_setup_quality_score.py` — unit tests covering all three AC-06 cases.
- `src/pages/SystemStatus.js` fallback updated 67→68 (pre-rebase).
- `tests/e2e/system-status.spec.js` SC-SS-01b updated 67→68 (pre-rebase).

**Note on rebase:** Sprint backlog requires EPIC-04 to rebase on main after EPIC-03 merges to resolve `openapi.yaml` and `backend/routers/test.py` shared-file additions. After rebase: test count becomes 69, SystemStatus.js and SC-SS-01b must be updated to `69`.

**Acceptance criteria verification:**
- [x] AC-01: `GET /trade-plans/setup-quality-score?ticker={ticker}` endpoint implemented in trade_plans.py router before the `/{plan_id}` parameterized route (routing order preserved).
- [x] AC-02: Score (0–100) computed from closed trade history using win_rate and avg_pnl_pct. Formula documented in response `score_explanation` field.
- [x] AC-03: Gate response `{"gate_not_met": true, "min_trades_required": 20, "current_trades": N}` returned when trade count < 20. Verified as primary testable state at implementation time (15 trades in production as of 2026-06-22).
- [x] AC-04: Score factors included: `matching_trades`, `win_rate`, `average_pnl_pct`, `score_explanation`. `ticker` echoed uppercase.
- [x] AC-05: Endpoint registered in `backend/routers/test.py` (68 entries pre-rebase) and `docs/reference/openapi.yaml` in same commit as endpoint.
- [x] AC-06: Unit tests in `tests/test_setup_quality_score.py` cover: gate_not_met (0 trades, 15 trades, trades with null pnl excluded), gate_met mixed history (50% win rate), perfect history (100% win, high score), ticker echoed uppercase, no portfolio.

**Deviations:** None

---

## EPIC-level consolidation

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|---------------------|--------|------------|
| ST-08 | trade_plan_endpoints.md v0.5 | GET /trade-plans/setup-quality-score + unit tests | AC-01..06 verified (gate response, score computation, Playwright suite not required — AC-06 unit tests + no observable UI ACs) | Pass | None |
| ST-09 | BLG-FEAT-25 (Frontend); ux_spec.md v3.9 | SetupQualityScorePanel in Research.js and TradePlan.js | AC-01..06 verified (score badge, gate-not-met message, detail expansion, ticker change, Playwright SC-SQS-01..06) | Pass | None |

**QA test coverage:**
- Scenarios run: tests/test_setup_quality_score.py (ST-08 backend); tests/e2e/setup-quality-score.spec.js SC-SQS-01..06 (ST-09 frontend)
- Regression areas checked: GET /trade-plans/{plan_id} routing order confirmed unaffected; Research.js and TradePlan.js existing panels unaffected by panel insertion
- Known deviations filed: None

---

## ST-09 — Setup Quality Score — frontend display (PT-04)

**Spec reference:** `docs/design/2026-05-21__release-v3.9/setup-quality-score-v2/ux_spec.md`; BLG-FEAT-25 Frontend scope
**Commit SHA:** 2ab3a6f0
**Delegation class:** autonomous

**What was built:**
- `src/components/trades/SetupQualityScorePanel.js` — new React component using `useQuery`
- Score badge (0–100) with qualitative label: Excellent (≥80) / Good (≥60) / Fair (≥40) / Low (<40)
- Gate-not-met message when insufficient trade history (`gate_not_met = true`)
- Expandable detail showing: matching_trades, win_rate, average_pnl_pct
- Score updates on ticker change (query key includes ticker)
- Silent error hide (returns null on error)
- `data-testid` attributes for Playwright targeting
- Integrated into `src/pages/Research.js` (Pre-Trade Research View, before Trade Plan section)
- Integrated into `src/pages/TradePlan.js` (after Setup Type field)
- `api.tradePlans.setupQualityScore(ticker)` added to `src/api/base44Client.js`
- `tests/e2e/setup-quality-score.spec.js` — SC-SQS-01..06 Playwright tests
- `.github/workflows/playwright.yml` updated 23→24 spec files; setup-quality-score.spec.js registered

**Acceptance criteria verification:**
- [x] AC-01: Panel displayed in Pre-Trade Research View (`Research.js`) and Trade Plan form (`TradePlan.js`)
- [x] AC-02: Score badge with numeric value and qualitative label (Excellent ≥80 / Good ≥60 / Fair ≥40 / Low <40)
- [x] AC-03: "Insufficient trade history (< 20 trades)" message when gate_not_met = true; uses `data-testid="setup-quality-gate-not-met"`
- [x] AC-04: Expandable detail section shows matching_trades, win_rate, average_pnl_pct (Avg Return %)
- [x] AC-05: Query key includes ticker — new query per ticker, no stale data across ticker changes
- [x] AC-06: SC-SQS-01..06 Playwright tests cover: panel renders (Research + TradePlan), score badge value/label, gate-not-met message, expanded detail values, ticker change score update

**Note on rebase:** EPIC-04 must rebase on main after EPIC-03 merges. After rebase: test.py count 68→69, SystemStatus.js `'68'`→`'69'`, SC-SS-01b "68"→"69". playwright.yml will need conflict resolution with EPIC-02's additions (23→25 → combined 26 spec files).

---

## Autonomous class eligibility check

- [x] Criterion 1: Both ST-08 and ST-09 have `delegation_class: autonomous` — ✓
- [x] Criterion 2: All ACs verifiable by code review + Playwright tests. ST-08 has no observable UI ACs (backend-only). ST-09 observable UI ACs covered by SC-SQS-01..06 Playwright tests — ✓
- [x] Criterion 3: Frontend changes (ST-09) have Playwright coverage (option-a per CLAUDE.md) — ✓
- [x] Criterion 4: Engine signer populated as "Sprint Execution Engine (autonomous class)" — ✓

- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-06-23
- Comments: ST-08 (backend) and ST-09 (frontend) both complete. Rebase requirement noted: EPIC-04 must rebase on main after EPIC-03 merge to resolve shared-file conflicts (test.py, openapi.yaml, playwright.yml). SystemStatus.js and SC-SS-01b will require updating at rebase time.
