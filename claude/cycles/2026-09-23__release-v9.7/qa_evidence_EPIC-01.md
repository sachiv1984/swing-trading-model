Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-25

# QA Evidence — EPIC-01 (PO-05 Lightweight Replay Mode) — 2026-09-23__release-v9.7

**EPIC:** EPIC-01 — PO-05 Lightweight Replay Mode
**Cycle:** 2026-09-23__release-v9.7
**Sprint goal:** Ship PO-05 Lightweight Replay Mode end-to-end and clear the full-capacity, category-balanced debt-clearance slice across 7 EPICs, 29 stories.
**Test scenarios used:** `tests/test_replay_service.py` (30, service-layer), `tests/test_replay_router.py` (19, HTTP-layer), `tests/test_strategy_engine_backtest_regression.py` (4, golden-file F3 regression), 2 added to `tests/test_router_error_envelope_conformance.py`, `tests/e2e/replay-mode.spec.js` (13, Playwright)

**Frontend-visible-change note:** ST-01c changes rendered UI (`src/pages/Replay.js`, `src/Layout.js`, `src/pages.config.js`), so the Autonomous DoQ sign-off class is unavailable for this EPIC (BLG-GOV-135 detection rule). The Standard Sign-Off Block below applies. Every observable AC has Playwright coverage — no AC relies on "code review only" and no deferred-to-staging backlog item is needed.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-01a | `docs/product/decisions/po05_replay_scope_confirmation.md` | Scope-confirmation note (rev 3) answering the three questions `decision_record.md` §2.7 deferred and locking the `POST /replay/run` wire contract, traced against all six §13 binding conditions. Three independent review passes (Blocked, Blocked, Approved) before ST-01b/c were built against it. | AC (`sprint_backlog.md`): request/response shape, output field names, Trade Set mixing rule all answered and locked before implementation began. | Pass | None |
| ST-01b | `po05_replay_scope_confirmation.md`; `docs/specs/api_contracts/replay_endpoints.md`; `po05_section13_preassessment.md` | `POST /replay/run` (router → service → database): per-trade day-by-day exit simulation in ratio space anchored at the trade's own entry price, using the current strategy engine's stop/risk-off rules (F3 extraction from `strategy_engine.py`, golden-file-regression-tested); bounds, warm-up checks, FX conversion, SHA-256 determinism fingerprint; manual request validation (no `RequestValidationError` handler exists, so a pydantic model would return FastAPI's default 422 instead of this repo's envelope). No Alpaca call, no persistence. | **AC-1** user can select a date range or trade set and run it through the current strategy rules — `POST /replay/run`, both modes, `test_replay_service.py`. **AC-2** output labelled retrospective/deterministic — `retrospective_notice` server constant, notice-equality test. **AC-3** §13 pre-clearance completed before sprint planning — `po05_section13_preassessment.md` (prior cycle) + this EPIC's own binding-condition trace (scope note §3). | Pass | None |
| ST-01c | `decision_record.md`; `docs/specs/frontend/pages/replay_mode.md` v0.2 | `src/pages/Replay.js`: Date Range / Trade Set selector, "Run Replay" gating, retrospective banner rendered from the API response with a hard-coded fallback, summary row, independence note, skipped-trades notice, FX-basis caption, badged results table, running/failure states. Registered in `pages.config.js`/`utils/index.js`/`Layout.js` (Analytics nav group, route `/Replay`). | Same AC-1/AC-2 as ST-01b, from the UI side — `tests/e2e/replay-mode.spec.js` SC-REP-01..12, all passing, 2 mutation-checked (SC-REP-05 banner wording, SC-REP-06 badge colour) against a deliberately broken implementation. | Pass | None |

**Observable-AC coverage map (CLAUDE.md §2 frontend-visible-change rule):**

| Story | Observable AC | Playwright scenario(s) |
|-------|---------------|------------------------|
| ST-01c | Nav item present, routes to the page | SC-REP-01 |
| ST-01c | Selector tabs mutually exclusive, own controls each | SC-REP-02 |
| ST-01c | "Run Replay" disabled until valid selection, both modes | SC-REP-03, SC-REP-03b |
| ST-01c | Running state: spinner, disabled | SC-REP-04 |
| ST-01c | Retrospective banner: presence, exact wording, non-dismissible | SC-REP-05 |
| ST-01c | Populated success: summary, independence note, FX caption, badged table | SC-REP-06 |
| ST-01c | 0-trade success, with and without skips | SC-REP-07, SC-REP-08, SC-REP-09 |
| ST-01c | Failure state wording; selector remains usable | SC-REP-10 |
| ST-01c | No write-capable control in the output view (negative) | SC-REP-11 |
| ST-01c | Trade Set checkbox list (ticker, exit date, toggling) | SC-REP-12 |

**QA test coverage:**
- Scenarios run: the 5 files above. New tests added by this EPIC: 29 (`test_replay_service.py`) + 19 (`test_replay_router.py`) + 4 (`test_strategy_engine_backtest_regression.py`) + 2 (added to `test_router_error_envelope_conformance.py`) = **54**, all passing. The agent-mediated code reviewer separately ran all four files together (including that file's ~22 pre-existing, unrelated router classes) and reported 74 passed, 0 failed. Full backend suite: 1855 passed, 5 skipped (unrelated pre-existing DB-opt-in skips). `replay-mode.spec.js`: 13/13 passed locally; the 47 sibling nav/system-status Playwright scenarios re-run alongside it with no regression.
- Regression areas checked: `strategy_engine.py`'s `backtest()` (golden-file byte-identical across 3 stop modes, 29 trades, independently regenerated from pre-refactor code by the reviewer); the sidebar nav groups; System Status endpoint count; the full backend suite.
- Known deviations: None. Both stories' deviation checks completed with nothing to file.

**Independent review record (agent-mediated, not this EPIC's own author reviewing itself):**
1. **Wire contract (ST-01a), 3 passes:** Pass 1 Blocked (8 findings — price basis, exit-rule fidelity, warm-up/calendar, rule fidelity, FX, determinism wording, error-envelope mechanism, scope disclosure). Pass 2 Blocked (2 findings — the `Body(dict)` mechanism's actual FastAPI behaviour, yfinance `end`-exclusivity). Pass 3 Approved.
2. **Implementation (ST-01b/c), 1 pass:** Approved, with one non-blocking gap (fetched series not sorted ascending per D6) — fixed same-session (commit `cc284457`) with 2 new tests confirmed to fail without the fix. Two further minor/theoretical notes accepted as-is (negative `holding_days` for an unreachable pathological date case; no defensive non-finite check mid-loop beyond the entry-time checks already present).

Both reviews independently regenerated or hand-verified financial-correctness claims (the golden fixture; the ATR/regime warm-up boundary math; the Stop/Risk-Off trigger scenarios; the D4 rounding-order worked example) rather than trusting the code's or the tests' own claims.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, `Replay.js` uses `fetch` directly against a local `API_BASE` constant, the same pattern every sibling page (`TradePlan.js`, etc.) uses
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-09-25
- Comments: [Agent-mediated Director of Quality sign-off, performed on the user's explicit direction ("carry on with ST-01b and c") — pending human Director of Quality confirmation; the merge-gate QA sign-off remains an always-human gate (execution_prompt.md §5.3).] Three independent review passes across the wire contract (2 Blocked, 1 Approved) and one independent review of the implementation itself (Approved, one gap fixed same-session). CI confirmation: PENDING_CI — to be filled once the PR's checks complete (see the Post-PR-open CI addendum below).

**Post-PR-open CI addendum:** to be appended after this EPIC's PR checks (including the full Playwright suite) have run.
