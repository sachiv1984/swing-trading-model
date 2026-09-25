Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Active — LOCKED on Product Owner acceptance (the merge of the PR that carries this document)
Last Updated: 2026-09-24 (rev 3 — revised after two independent review passes; rev 1 was returned Blocked with 8 blocking findings and rev 2 with 2, all verified against the source and applied)
Cycle: 2026-09-23__release-v9.7
Story: ST-01a (EPIC-01) — PO-05 scope-confirmation sub-story
Backlog ref: BLG-FEAT-74
Escalation ref: ESC-EXEC-20260924-01

---

# PO-05 Lightweight Replay Mode — Scope Confirmation and Locked Wire Contract

**Purpose.** This is the deliverable of ST-01a (`sprint_backlog.md`, RISK-01's own resolution mechanism). It answers the three questions `decision_record.md` §2.7 deferred, locks the backend wire contract that the backend and frontend implementation stories build against, and records — per Binding Condition 6 of `po05_section13_preassessment.md` — how the result satisfies all six binding conditions. It does not change the V1 UI shape in `docs/design/2026-09-23__release-v9.7/po05-replay-mode/decision_record.md` except for the additions §7 names for the Head of UX & Design / Product Owner to confirm.

**Authority and sign-off.** Head of Specs Team role, exercised by the Sprint Execution Engine (agent-mediated, `execution_prompt.md` §5.3) on the user's explicit direction, 2026-09-24. Independent review: §9. **Product Owner acceptance — including of the scope decision in §7 item 1 — is a human decision and is recorded by the Product Owner's merge of the PR that carries this document; no agent records it. Implementation of the backend story must not start before that merge.**

**This document takes precedence for the build** over the wording in `sprint_backlog.md` (ST-01b), `docs/specs/frontend/pages/replay_mode.md` §13 item 5, `po05_section13_preassessment.md` and `current_roadmap.md` (PO-05) that says the replay "reuses IT-06's paper-trading mechanics" or requires IT-06 — see F1. The sealed `sprint_backlog.md` and the other documents are not edited here; correcting the pre-assessment and roadmap wording is pending the owning authorities' acknowledgement (§7).

---

## 1. Findings that shape the decisions (each verified in the source, 2026-09-24)

**F1 — "The existing paper-trading mechanics" cannot replay history.** IT-06 in code is `backend/services/alpaca_paper_sync_service.py`: a best-effort, real-time mirror of user-initiated position open/close events to Alpaca's paper account (network calls, credentials, current positions only, no history). It cannot replay a past period and it is not deterministic. `alpaca_service.py` is a market-data client, and no other paper-trading mechanics exist in `backend/`, `production_strategy.py` or `scripts/`. The deterministic simulation engine that does exist is `backend/services/strategy_engine.py`, shared by the nightly backtest and the in-app "Backtest Rule Change" feature.
**Decision:** in this feature "paper" means *simulated*. The replay is an in-process deterministic simulation built on `strategy_engine.py`. **It makes no Alpaca call and reads or writes no Alpaca data.** Binding Condition 5 is therefore satisfied by construction.

**F2 — The determinism claim must be restated.** The pre-assessment says the same inputs give byte-identical output, unconditionally. The output depends on the price series (`yfinance`, `auto_adjust=True`, a network fetch whose history can be revised), on the rule values, on the selected trade rows, and — for a float pipeline — on the runtime's pandas/numpy versions. See D6 for the exact guarantee and the fingerprint that makes it checkable. The §13-relevant property is unchanged and unconditional: **no randomness, no model, no adaptive state.**

**F3 — The per-position exit logic is inline in `backtest()`'s portfolio loop** (`strategy_engine.py`: the stop block, the risk-off block, the initial-stop computation at entry, and the `is_risk_on` closure). Re-implementing it would create a third copy of the algorithm — the burden `BLG-TECH-15` removed. See §5.

**F4 — The engine is not identical to the live rule set (rule fidelity).** `strategy_engine.py` differs from `strategy_rules.md` §7.2 and the live position logic in four ways: (1) it has **no breakeven floor** on a profitable position's stop (§7.2 v1.10 requires `max(price − ProfitATR×ATR, EntryPrice)`); (2) its ATR is **close-only** (`compute_atr` sets high = low = close, so true range is |Δclose|; live ATR uses OHLC); (3) it evaluates the **stop before risk-off**, while the live logic checks risk-off first; (4) it charges the buy fee inside the entry price, whereas `trade_history.entry_price` is the raw price with fees held separately. This is existing, documented-elsewhere engine behaviour and is not changed here; the replay follows the engine so it stays consistent with the backtest tool. The consequence — "the current rules" in the approved banner is slightly loose — is disclosed in D1 and §7 item 4.

**F5 — The roadmap defines PO-05 more broadly than V1 delivers.** `current_roadmap.md` (PO-05): *"Replay historical signals against your own strategy rules on your own trade history … a replay of what the system would have signalled, compared to what you actually did."* `BLG-FEAT-74`'s acceptance text says "run it through paper-trading mechanics under current strategy rules". V1 (D1) satisfies the backlog text but **not** the roadmap description in full: it replays exits only, reads no signals or candidates, and does not compare against the actual outcome. See §7 item 1.

---

## 2. Scope decisions

### D1 — What is replayed: each of the user's own closed trades, independently, under the engine's exit rules

- **Input (own-data only, §13 Criterion 2):** rows of the user's `trade_history`, scoped to the current portfolio (`get_portfolio()` → `portfolio_id`, as every other query does). Nothing else is a trade source. Market data is read only as price history for those trades' tickers, plus the SPY and ^FTSE regime series.
- **Entry facts are fixed as recorded:** `ticker`, `entry_date`, `entry_price`, `shares`. **Market is derived from the ticker** (`.L` → UK, otherwise US), exactly as the engine does; the `market` column (nullable) is not used. Entry selection, ranking, sizing and rebalancing are **not** replayed.
- **Price basis — the simulation runs in ratio space.** Recorded prices and the yfinance `auto_adjust` series are on different bases (splits, dividend adjustment, and UK pence). Let `ref` be the series close on `entry_date` (the last bar on or before it). For every later day D, `sim_price(D) = entry_price × close(D) / ref`. The ATR series is scaled by the same factor `entry_price / ref`. The stop, the profit test and every output price are computed on `sim_price`, in the trade's recorded unit. `entry_price` and `shares` are never compared with a raw series value.
- **Day-by-day rule evaluation.** For each calendar day D strictly after `entry_date` and up to and including the trade's actual `exit_date`, using each ticker's own trading calendar:
  1. **Stop (only when `(D − entry_date).days ≥ min_hold_days` and ATR(D) is defined).** The initial stop, set at entry, is `entry_price − initial_atr_mult × ATR(entry)` (`atr_mult` in `simple` mode). It is **not** evaluated during the hold window. From the first eligible day the stop ratchets: `stop = max(stop, sim_price(D) − active_mult × ATR(D))`, with `active_mult` per the engine: `simple` → `atr_mult`; `tiered` → `initial_atr_mult` while `holding_days < 2 × min_hold_days`, else `atr_mult`; `profit_lock` → `profit_atr_mult` if `sim_price(D) > entry_price`, else `initial_atr_mult`. If `sim_price(D) ≤ stop`, exit with reason `"Stop"`.
  2. **Risk-off (no hold-period exemption — the engine applies none).** If the ticker's market regime is not risk-on on D (`risk_off_mode`, as `is_risk_on` in the engine: `.L` uses ^FTSE, otherwise SPY, for `single`), exit with reason `"Risk-Off"`.
  3. `entry_date` itself is never evaluated. The first rule that fires ends the simulation.
- **Exit price is always that day's `sim_price`** — a gap through the stop exits at the day's close, never at the stop level.
- **`holding_days` and `min_hold_days` are calendar days**, `(D − entry_date).days`.
- **No rule fires by the actual exit date →** the simulated exit is the actual exit date's `sim_price` with reason `"Actual Exit"`. The replay never looks past the user's own exit. If `exit_date` is not a bar date, use the last bar on or before it; if `entry_date == exit_date` the trade is a 0-day `"Actual Exit"`.
- **Rule set = the current `LIVE_PARAMS` at run time (Binding Condition 4).** The client cannot supply or override any rule value. The values used are echoed as `run.rule_set` (display-only).
- **Fees and comparability.** The engine's sell fee (`transaction_fee(ticker, "sell")`: 0.15% US, 0% UK) is applied to the simulated exit; **no entry cost is applied** (the recorded `entry_price` is raw). `simulated_pnl_*` is therefore **not comparable with recorded `pnl`**, which uses the real fee schedule.
- **Rule fidelity (F4) and design-induced differences.** The four engine-versus-live differences in F4 apply to the replay unchanged. Differences from the *engine* that follow from this design: (a) the profit test is relative to the entry-day close, not to the engine's fee-inflated entry; (b) because the series is dividend-adjusted, the ratio path is total-return based, so `simulated_exit_price` can exceed any price actually traded; (c) rules are evaluated on each ticker's own calendar, not the SPY calendar with forward-filled prices. Measured against the real `backtest()` in a 60-path synthetic probe (not a population statistic), with fees zeroed the exit day and reason match on every path; with the engine's real fees the exit day or reason differed on 1–3 of 60 paths per stop mode (the fee moves the profit-test threshold and can flip `profit_lock` between its tight and wide stop). Flat or halted series: ATR = 0 gives `stop = price`, an immediate `"Stop"` on the first eligible day, as in the engine. Exit reasons are `"Stop"`, `"Risk-Off"` (both in the frontend's `EXIT_REASON_BADGE`) and `"Actual Exit"` (not in the badge map; the existing component renders an unknown reason as plain text, which is the intended V1 treatment).

### D2 — Request shape: one endpoint, two mutually exclusive modes, no parameters

`POST /replay/run` accepts **exactly one** of:

```json
{ "date_from": "2026-03-01", "date_to": "2026-06-30" }
```
```json
{ "trade_ids": ["<uuid>", "<uuid>"] }
```

- These map one-to-one to the two UI tabs. Both, neither, an empty `trade_ids`, any other field, a malformed UUID, `date_from > date_to`, or a `date_to` after today (UTC) is a validation error (D5).
- **The route must parse and validate the body itself.** It is `async def replay_run(request: Request)`: it reads `await request.body()`, parses it with `json.loads` inside try/except, requires a `dict`, and returns `400 validation_error` (D5 envelope) for a missing body, malformed JSON or a non-object; it then validates each field manually and runs the blocking service via `run_in_threadpool`. **`body: dict = Body(...)` is not sufficient, and neither is a pydantic model with `extra="forbid"`:** the backend has no `RequestValidationError` handler, so FastAPI returns `422 {"detail": [...]}` for a missing, malformed or non-object body (verified) — breaking the envelope and `tests/test_router_error_envelope_conformance.py`, which asserts `"detail" not in body`. This is also how Binding Condition 4 is enforced at the wire.
- **Date Range mode selects the user's closed trades whose `exit_date` is in `[date_from, date_to]` inclusive** — the field the Trade Set list displays and the monthly report uses.
- **Trade Set mode:** duplicate ids are de-duplicated and `requested_trade_count` is counted after de-duplication; an id that does not exist or belongs to another portfolio (or has a NULL `portfolio_id`) is skipped with `trade_not_found`.
- **Evaluation order:** validation → resolve trades → bounds (evaluated on resolved trades).
- **Bounds (no silent truncation):** at most **100** trades and **25** distinct tickers per run (SPY and ^FTSE are not counted). Beyond either, the request is rejected (D5) and the client narrows the selection.
- **Read-only, no persistence.** V1 adds **no table and no write path** (Binding Condition 1). It is a `POST` only because it carries a body. The existing `X-API-Key` authentication is inherited.

### D3 — "Trade Set" mode: any mix of tickers and dates; no contiguity constraint

Each trade is replayed **independently** (D1): no shared cash, position cap, concentration limit or chronology between trades, so mixing tickers and non-contiguous dates is well-defined. A position closed in several partial exits appears as several `trade_history` rows and is replayed as separate trades. The independence is a documented V1 limitation and is surfaced to the user (§7 item 3).

### D4 — Response shape (success)

`HTTP 200`, the standard envelope `{"status": "ok", "data": { ... }}`:

```json
{
  "status": "ok",
  "data": {
    "retrospective_notice": "Retrospective result — shows what the current rules would have produced over this past period. Not a prediction of future performance.",
    "run": {
      "mode": "date_range",
      "date_from": "2026-03-01",
      "date_to": "2026-06-30",
      "requested_trade_count": 12,
      "replayed_trade_count": 11,
      "skipped": [ { "trade_id": "…", "reason": "price_data_unavailable" } ],
      "rule_set": {
        "stop_loss_mode": "profit_lock", "atr_mult": 2, "initial_atr_mult": 5,
        "profit_atr_mult": 2, "min_hold_days": 10, "risk_off_mode": "single"
      },
      "price_data_source": "yfinance",
      "price_data_fingerprint": "sha256:…"
    },
    "summary": {
      "trade_count": 11, "win_count": 7, "win_rate_pct": 63.64,
      "total_simulated_pnl_gbp": 412.55, "excluded_from_gbp_total": 0
    },
    "trades": [
      {
        "trade_id": "…", "ticker": "NVDA", "market": "US", "currency": "USD",
        "entry_date": "2026-03-04", "entry_price": 121.5, "shares": 10.0,
        "initial_stop": 110.2,
        "simulated_exit_date": "2026-05-12", "simulated_exit_price": 133.1,
        "simulated_exit_reason": "Stop", "holding_days": 69,
        "simulated_pnl_native": 114.0, "simulated_pnl_gbp": 89.63,
        "fx_basis": "entry_fx_rate"
      }
    ]
  }
}
```

- **`retrospective_notice`** is a **server-supplied constant** equal to the design record's §2.3 wording verbatim. The frontend renders it as the retrospective banner (`data-testid="replay-retrospective-banner"`) and keeps an identical hard-coded fallback literal so a missing field can never silently drop the Binding-Condition-2 banner. A backend test asserts the constant equals the approved string (`scripts/check_ui_copy_forbidden_phrases.py` scans `src/` only, so this test is the guard for the server-side copy).
- **Echoes:** `run.mode` is `"date_range"` or `"trade_set"`; in `trade_set` mode `run.date_from` and `run.date_to` are `null`.
- **Ordering:** `trades` by `simulated_exit_date` ascending, then `trade_id` ascending — a total order.
- **P&L definition.** `simulated_pnl_native = (simulated_exit_price × (1 − sell_fee) − entry_price) × shares`. `simulated_exit_price` and `initial_stop` are the ratio-space prices (D1), **not** fee-adjusted, in the trade's recorded unit. The worked example above: `(133.1 × 0.9985 − 121.5) × 10 = 114.0035`, shown as `114.0`; the GBP figure is computed from the **unrounded** native value, `114.0035 / 1.272 = 89.6253`, shown as `89.63` (dividing the rounded `114.00` would give `89.62` — do not).
- **GBP conversion.** `simulated_pnl_gbp = simulated_pnl_native / entry_fx_rate` for US trades (`entry_fx_rate` is native units per £1, as `trade_service.py` divides); UK trades use 1.0. `currency` ∈ {`USD`, `GBP`}. `fx_basis` ∈ {`entry_fx_rate`, `not_applicable_gbp`, `unavailable`}. If a US trade's `entry_fx_rate` is NULL or ≤ 0: `simulated_pnl_gbp: null`, `fx_basis: "unavailable"`, the trade is excluded from `summary.total_simulated_pnl_gbp` and counted in `summary.excluded_from_gbp_total`. FX movement after entry is deliberately ignored (no FX series exists for a date the user did not trade on) and must be disclosed in the UI (§7 item 2). UK `entry_price` is taken as recorded and assumed to be in pounds (`utils/calculations.py`: "UK: already in GBP"; `position_service.py` normalises pence the same way).
- **Rounding and non-finite values.** Prices (`entry_price`, `initial_stop`, `simulated_exit_price`) are rounded to 4 dp (the `trade_history` precision, so sub-£1 UK prices survive) and P&L amounts to 2 dp; a **win** is decided on the unrounded `simulated_pnl_native`; `summary` sums are computed from unrounded per-trade values and rounded once; `win_rate_pct` is 2 dp and `null` when `trade_count` is 0; `total_simulated_pnl_gbp` is `0.0` when there is nothing to sum. Any non-finite value is emitted as `null`; a trade whose ATR or initial stop is non-finite at entry is skipped as `insufficient_history` (the engine's own NaN behaviour, where `max(nan, x)` is `nan`, is preserved in `backtest()` and not copied here).
- **Skipped trades are reported, never silently dropped.** `skipped[].reason` ∈ `trade_not_found`, `price_data_unavailable`, `insufficient_history`. `requested_trade_count − replayed_trade_count = len(skipped)`; `summary` and `trades` cover replayed trades only.
- **0 trades replayed** is a normal success (`trades: []`, `trade_count: 0`, `retrospective_notice` still present). If `skipped` is non-empty the UI must show the skipped notice as well, so the 0-trade text is not misleading.

### D5 — Errors

Envelope per `conventions.md` §13.3 — `{"status": "error", "message": "<human-readable>", "code": "<snake_case>"}` (`code` is the additive field already used in `analytics.py`). Status codes follow the canonical mapping in `conventions.md` §13.2 (validation and business-rule violations are `400`; backend or external-API failure is `500`). The repository also contains `422` usages for validation (`ai.py`, `analytics.py`); this contract deliberately follows the canonical document, not those precedents, and the contract file must say so.

| HTTP | `code` | When |
|------|--------|------|
| 400 | `validation_error` | any request problem listed in D2 |
| 400 | `replay_scope_too_large` | over 100 resolved trades or 25 distinct tickers; the message names the limit |
| 500 | `price_data_unavailable` | the price provider returned nothing usable for **every** requested ticker, **or** for a regime series the run requires under `risk_off_mode` (D6: `single` needs only each trade's own market series; `dual` and `dual_strict` need both). A yfinance frame that is empty or all-NaN counts as failed, and a partial failure is `skipped`, not an error |
| 500 | `replay_failed` | any unexpected server error |

The frontend maps every non-2xx to the single failure state in `decision_record.md` §2.5 ("Couldn't run the replay. Try again.").

### D6 — Data window, calendar and the determinism guarantee

- **Fetch window.** Each ticker, SPY and ^FTSE, from `min(entry_date) − 420 calendar days` to **`max(exit_date) + 1 day`** (yfinance's `end` is exclusive — passing the latest `exit_date` itself drops that day's bar), with `auto_adjust=True`, sorted, the upstream timeout used by `utils/upstream_call.py`'s `yfinance_history` (15 s), and **no `bfill`** (the backtest service's `.reindex(spy.index).ffill().bfill()` fabricates history for late-listed tickers and must not be copied). Rows with a NaN close are dropped per ticker (yfinance returns union-date frames).
- **Fetch only when needed:** the fetch happens only if at least one trade survives resolution and the today-boundary skip below (so a request whose trades all resolve to `trade_not_found`, or all exit today or later, makes no network call); the tickers and window are those of the surviving trades. The regime series required depend on `risk_off_mode`: `single` needs the trade's own market series; `dual` and `dual_strict` need both. `LIVE_PARAMS` is `single`, but the shared function must handle all three.
- **Calendar.** Each ticker uses its own trading calendar (the engine instead puts every ticker on the SPY calendar with forward-filled prices — a named divergence, see D1). A regime value for a ticker's date is the last regime bar on or before it (forward-fill only). A regime series is risk-on only once at least 200 rows exist; a trade with fewer than 200 regime rows or fewer than 14 ticker rows before its `entry_date` is skipped `insufficient_history` — never evaluated against the engine's warm-up `False`, which would manufacture a spurious `Risk-Off` exit.
- **"Today".** Evaluated in UTC (the repository precedent, `BLG-BE-125`). A trade with `exit_date` on or after today is skipped `price_data_unavailable` (no final bar exists).
- **`price_data_fingerprint`** is the SHA-256 of one canonical JSON document, all lists sorted: (a) `rule_set`; (b) for each replayed trade, `(trade_id, ticker, entry_date, exit_date, entry_price, shares, entry_fx_rate)`; (c) the **full fetched close series** for each ticker (including warm-up rows), as `(ticker, date, repr(float))`; (d) the full fetched regime series the run required.
- **Guarantee.** *Same request, same code and dependency versions, and the same `price_data_fingerprint` ⇒ byte-identical `data.trades` and `data.summary`.* Nothing stronger is claimed.

---

## 3. Binding-condition trace (`po05_section13_preassessment.md`, Binding Condition 6)

| # | Condition | How this specification satisfies it |
|---|-----------|--------------------------------------|
| 1 | Read-only against real data; no parameter writes | Reads `trade_history` only; **no table, no write path, no persistence** (D2). The implementation test asserts that no `INSERT`/`UPDATE`/`DELETE` is issued, not only that row counts are unchanged. |
| 2 | Explicitly retrospective-labelled | `retrospective_notice` is a server constant with the approved wording verbatim, backed by a frontend fallback literal and a backend constant test (D4). |
| 3 | No auto-remediation affordance | The response has no actionable field and the request has no parameter to act on. UI obligations unchanged (`decision_record.md` §2.3). |
| 4 | Rule set fixed to "current" | Rule values are read server-side from the current `LIVE_PARAMS`; the manually-validated request rejects any extra field (D2); values are echoed for audit only. **"Current" is inexact — see F4 and §7 item 4.** |
| 5 | IT-06 paper-data isolation | **Satisfied by construction (F1):** no Alpaca call, credential, read or write. |
| 6 | Spec checked against the pre-assessment | This section. **Corrections, not contradictions:** the IT-06 reuse premise (F1), the unconditional determinism wording (F2), and the engine-versus-live rule divergences (F4). Each makes the feature more conservative or more precisely described, and none weakens conditions 1–5. Recorded for the Strategy Rules & System Intent Owner's acknowledgement (§7 item 4). |

**§13.2 check.** No ML or inference; no random sampling; no adaptive parameters; no broker or streaming component; no forecast — every input is a fact already on record (a recorded trade, a realised price). No path exists for replay output to reach real signals, sizing, screening or stops: nothing is persisted or linked out. The one shared-code risk is the F3 refactor of `backtest()`, which the regression test in §5 guards.

---

## 4. Out of scope for V1 (each would need its own scoping and, where noted, its own §13 review)

Entry, selection, sizing and rebalance replay; reading signals or candidates; portfolio-level interaction between replayed trades; any user-supplied rule or parameter (**needs a new §13 review**, Binding Condition 4); comparison with the actual outcome or with any benchmark; persistence or history of replay runs; export; a "Replay this period" shortcut from Trade History.

---

## 5. Hand-over to backend and frontend implementation

**Backend implementation (Head of Engineering).** Build exactly the contract in §2, in one commit set that includes (`CLAUDE.md` §2):
- Router + service (router → service → database pattern).
- **The F3 extraction:** move the per-position stop logic, the initial-stop-at-entry computation and the `is_risk_on` closure into shared functions in `strategy_engine.py`, and have `backtest()` call them. **A golden-file regression test proves `backtest()`'s trade output is unchanged; the golden file is generated from the pre-refactor code on `main`, not from the refactored code.** `backtest()`'s existing NaN-ATR behaviour is preserved, not silently changed.
- `docs/specs/api_contracts/replay_endpoints.md` with a `## POST /replay/run` heading (exactly `##`), the matching `docs/reference/openapi.yaml` entry, an `api_changelog.md` entry, a `docs/specs/Specs_Index.md` entry (`check_specs_index_freshness.py`; `replay_mode.md` is also absent from it today), a router class in `tests/test_router_error_envelope_conformance.py` (a 500 with an additive `code` passes its `_assert_canonical_error`), keeping `check_local_openapi_contract_completeness.py` (heading lint plus the router/contract/openapi three-way sweep) green, and a `docs/ops/api_performance_baseline.md` row (expect a high-latency, multi-second profile by design; precedent: the existing backtest-rule-change endpoint's row). The contract file records the deliberate 400-not-422 choice (D5).
- `backend/routers/test.py` registration (the entry name must be exactly `POST /replay/run`) — **with the body `{"trade_ids": ["00000000-0000-0000-0000-000000000000"]}`**, which returns 200 with `skipped: trade_not_found` and makes no network call (the existing backtest-rule-change registration uses `{}` and runs a real backtest on every System Status test — do not copy it); the `SystemStatus.js` fallback endpoint count updated; and `SC-SS-01b` in `tests/e2e/system-status.spec.js` matched. **Re-derive the count fresh immediately before the commit and again before the PR** — it is currently 124 in both `SystemStatus.js` and `test.py`'s `test_cases`, counted by AST as the CI Endpoint Count Drift Check does, **not** by grepping `"name":` (which over-counts).
- Tests: determinism (same fixture twice → identical output; the fingerprint changes when one price changes); the read-only assertion (no write statement issued); **Alpaca isolation as "patch Alpaca's HTTP entry points to raise, run the replay, assert none was called"** (an import-based check is brittle because `utils/pricing.py` imports `alpaca_service` transitively); manual-validation envelope for every D2 rejection, **including a missing body, malformed JSON and a non-object body**; bounds; every error code; every skip reason including `insufficient_history` at the 14-row and 200-row boundaries; the 0-trade success; **a trade exiting on the latest date in the set uses that date's bar** (fetch `end` is exclusive); the notice-constant equality test; a `LIVE_PARAMS` drift test tying `backtest_rule_service.LIVE_PARAMS` to `production_strategy.py`'s constants (no test does today). Importing `LIVE_PARAMS` from `backtest_rule_service` also imports the write function `create_backtest_rule_run` at module level; it is never called, so the no-write assertion still holds — or move `LIVE_PARAMS` into `strategy_engine.py` and re-export it.
- **Measure and record the synchronous run time at the bounds** (100 trades, 25 tickers). If it cannot complete comfortably inside a normal request timeout, raise an escalation rather than silently lowering the bounds. Note that yfinance multi-ticker downloads are not thread-safe across concurrent requests, an exposure the backtest feature already shares.

**Frontend implementation.** Build `decision_record.md` §2.1–§2.6 against the contract above (it depends on the backend story), plus the additions in §7 items 2–4; correct `replay_mode.md` §13 item 5 (the IT-06 premise) in the same change (a Class 2 document owned by the Frontend Specifications & UX Documentation Owner); render the banner from `data.retrospective_notice` with the hard-coded fallback; `replay_mode.md` v0.1 moves from "Design Only" once the contract lands. Every observable AC needs Playwright coverage (`CLAUDE.md` §2), including the 0-trade-with-skipped state.

---

## 6. Sequencing note

The Product Owner's decision on D1 (§7 item 1) gates the backend story, because a different scope would waste its effort. That decision is the Product Owner's, recorded by the merge of the PR carrying this document. Only after that merge does the backend story start.

---

## 7. Items for other authorities (raised here; not decided here except where stated)

1. **Product Owner — scope interpretation (D1, F5).** V1 replays the *exits* of the user's own trades under the engine's rules. It does not read signals or candidates, does not re-select trades, and does **not compare with what the user actually did** — which is part of the roadmap's own definition of PO-05. It satisfies `BLG-FEAT-74`'s acceptance text, not the roadmap sentence in full. Recommended because it is deterministic, own-data-only, the cleanest §13 case, and buildable inside the sized effort; a per-trade actual-versus-simulated comparison is the most natural next increment. **Accept (by merge), or direct a different scope before the backend story starts.**
2. **Head of UX & Design / Product Owner — FX-basis caption.** GBP figures use the recorded entry rate (D4). The results view should show a muted caption, e.g. *"GBP figures use each trade's recorded entry exchange rate."*
3. **Head of UX & Design / Product Owner — independence and skipped-trade notices.** The results view should show (a) a muted line that trades are replayed independently (no shared cash or position limits) and (b) when `run.skipped` is non-empty, a notice naming how many trades could not be replayed and why. Neither changes the approved layout.
4. **Strategy Rules & System Intent Owner — acknowledgement of F1, F2 and F4** (the IT-06 premise, the determinism wording, and the engine-versus-live divergences), and a decision on caption wording such as *"Simulated with the strategy backtest engine's exit rules."*, since the approved banner says "the current rules". This note finds no contradiction with any of the six conditions; `po05_section13_preassessment.md` itself is outside this role's write scope and is not edited here. A follow-up backlog item records the corrections (filed with this document).
5. **Strategy Rules & System Intent Owner — separate observation (not part of this contract).** The IT-06 §13 review states the Alpaca sync is GET-only with no orders placed, but `alpaca_paper_sync_service.py` POSTs orders and DELETEs positions on user position open/close. That discrepancy predates this feature; a backlog item records it (filed with this document).

---

## 8. Sign-off

**Signed off by:** Sprint Execution Engine (agent-mediated, Head of Specs Team role — §5.3), on the user's explicit direction, 2026-09-24
**Date:** 2026-09-24
**Determination:** Wire contract LOCKED on Product Owner acceptance. `ESC-EXEC-20260924-01`'s unblock criterion — the backend wire contract for the replay run is defined — is met by this document once merged.
**Comments:** The three deferred questions are answered (D2 request shape, D4 output field names, D3 Trade Set mixing) and the contract is specified to the level the backend story needs: price basis, exit-rule order and semantics, calendar and warm-up rules, FX conversion and NULL handling, fingerprint, error mapping. Every design decision rests on a repository fact verified in code (F1–F5). Rev 1 of this document was returned *Blocked* by an independent review that found it would have led the backend story to build the wrong thing; the corrections are in this revision.

---

## 9. Independent review record

- **Pass 1 (rev 1) — Blocked.** 8 blocking findings, each verified against the source before being applied: price-basis mismatch (B1); the exit-rule description not matching the engine — min-hold gates only the stop, the initial stop is set at entry and inactive during the hold window, exits fill at the day's close, ATR is close-only, day-0 and NaN-ATR semantics (B2); unspecified warm-up, regime and calendar rules (B3); rule-fidelity divergences from the live rule set (B4); FX direction and NULL handling (B5); an over-claiming determinism guarantee and NaN serialisation (B6); an error envelope that default FastAPI validation cannot produce (B7); an incomplete scope disclosure that omitted the roadmap's own PO-05 definition (B8). Non-blocking findings (N1–N8) were also applied, including the separate IT-06 observation.
- **Pass 2 (rev 2) — Blocked, 2 narrow findings**, both verified before applying: the prescribed `body: dict = Body(...)` mechanism returns FastAPI's default `422 {"detail": [...]}` for a missing, malformed or non-object body, so it could not deliver the D5 envelope (P2-1); and yfinance's `end` is exclusive, so fetching "to the latest `exit_date`" drops that day's bar (P2-2). Pass 2 also confirmed the ratio-space price basis by running it against the real `backtest()` on 60 random paths in three stop modes (0 mismatches with fees off). Its non-blocking findings (N-a to N-h) were applied.
- **Pass 3 (rev 3) — Approved.** Confirmed both fixes (the manual-parse mechanism re-probed under stacked HTTP middleware, returning the 400 envelope for missing, malformed and non-object bodies), all pass-2 items, the count and rounding statements, and the two filed backlog items. One internal contradiction (D5 versus D6 on which regime series a failure applies to), the fetch-skip wording, several text tidy-ups and the quantification wording were applied in this revision. No question remains that the backend story would have to ask.
