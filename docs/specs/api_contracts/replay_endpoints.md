**Owner:** Backend Engineering Patterns Owner; Product Owner
**Class:** API Contract (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-25 — ST-01b, EPIC-01, v9.7, BLG-FEAT-74 (new file)
**Story:** ST-01b (EPIC-01, v9.7, BLG-FEAT-74)

---

# Replay API Contract

Endpoint supporting PO-05 Lightweight Replay Mode — replays each of the user's own
closed trades, independently, through the current strategy engine's exit rules
(stop / risk-off), producing a retrospective, deterministic simulation of what those
rules would have done to trades the user already took.

Wire contract locked in: `docs/product/decisions/po05_replay_scope_confirmation.md`
(rev 3) — read that document for the full design rationale (D1–D6) and the §13
binding-condition trace. This file states the wire contract itself.

**§13 compliance:** deterministic simulation over the user's own historical trades and
market data (no ML model, no random sampling, no adaptive state). Makes no Alpaca call
and reads/writes no Alpaca data — the feature's "paper" replay is an in-process
simulation built on the same engine as the existing Backtest Rule Change feature, not
IT-06's Alpaca paper-trading integration (see the scope note's Finding F1). Read-only:
no table is created, no row is written anywhere. See `po05_section13_preassessment.md`
Binding Conditions 1–6.

**Error convention (deliberate departure from the 422 precedent in `ai.py`/`analytics.py`):**
this contract follows `conventions.md` §13.2's canonical HTTP status mapping (validation
and business-rule violations are `400`, not `422`) and adds a `code` field to the
standard `{"status": "error", "message": ...}` envelope, the same additive pattern
`analytics.py` already uses. The backend has no `RequestValidationError` handler, so a
pydantic-model-based request would return FastAPI's default `422 {"detail": [...]}` for
a malformed body — this endpoint parses and validates its body manually instead, so
every rejection returns this contract's own envelope regardless of what was wrong with
the request.

All endpoints require `X-API-Key` header authentication.

---

## POST /replay/run

Replays a date range or an explicit set of the user's own closed trades. Synchronous —
a run over the full 100-trade / 25-ticker bound is expected to take several seconds
(dominated by `yfinance` network I/O, the same profile as `POST
/strategy/backtest-rule-change/run`); the frontend shows an inline spinner for the
duration. Read-only and persists nothing — repeated identical requests are safe to retry.

**Request body (application/json):** exactly one of the two shapes below. Any other
combination (both, neither, an extra field, an empty `trade_ids` array, a malformed
UUID, `date_from` after `date_to`, or `date_to` in the future) is a `400
validation_error`.

```json
{ "date_from": "2026-03-01", "date_to": "2026-06-30" }
```
```json
{ "trade_ids": ["3f1b2c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d"] }
```

| Field | Type | Notes |
|-------|------|-------|
| `date_from` / `date_to` | string (ISO date) | Both required together. Selects the user's closed trades whose `exit_date` falls in `[date_from, date_to]` inclusive. `date_to` may not be after today (UTC). |
| `trade_ids` | array of string (UUID) | Non-empty. Duplicate ids are de-duplicated before counting. An id that does not exist, or belongs to another portfolio, is reported in `run.skipped` with reason `trade_not_found` rather than failing the request. |

**Bounds:** at most 100 resolved trades and 25 distinct tickers per run (evaluated
after trade resolution, before the price/regime fetch). Exceeding either returns `400
replay_scope_too_large` naming the limit — the client narrows the selection; there is
no silent truncation.

**Response (200):**

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
      "skipped": [
        { "trade_id": "3f1b2c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d", "reason": "price_data_unavailable" }
      ],
      "rule_set": {
        "stop_loss_mode": "profit_lock",
        "atr_mult": 2,
        "initial_atr_mult": 5,
        "profit_atr_mult": 2,
        "min_hold_days": 10,
        "risk_off_mode": "single"
      },
      "price_data_source": "yfinance",
      "price_data_fingerprint": "sha256:5f2c...e91a"
    },
    "summary": {
      "trade_count": 11,
      "win_count": 7,
      "win_rate_pct": 63.64,
      "total_simulated_pnl_gbp": 412.55,
      "excluded_from_gbp_total": 0
    },
    "trades": [
      {
        "trade_id": "9a1b...",
        "ticker": "NVDA",
        "market": "US",
        "currency": "USD",
        "entry_date": "2026-03-04",
        "entry_price": 121.5,
        "shares": 10.0,
        "initial_stop": 110.2,
        "simulated_exit_date": "2026-05-12",
        "simulated_exit_price": 133.1,
        "simulated_exit_reason": "Stop",
        "holding_days": 69,
        "simulated_pnl_native": 114.0,
        "simulated_pnl_gbp": 89.63,
        "fx_basis": "entry_fx_rate"
      }
    ]
  }
}
```

### Field notes

- **`retrospective_notice`** — a server-supplied constant, always present, equal to
  `docs/design/2026-09-23__release-v9.7/po05-replay-mode/decision_record.md` §2.3's
  approved wording verbatim. The frontend renders this string as the retrospective
  banner (`data-testid="replay-retrospective-banner"`) and keeps an identical
  hard-coded fallback literal so a missing/renamed field can never silently drop the
  banner. Never varies with the request or the result.
- **`run.mode`** — `"date_range"` or `"trade_set"`, echoing which request shape was
  used. In `"trade_set"` mode, `run.date_from`/`run.date_to` are `null`.
- **`run.requested_trade_count`** vs **`run.replayed_trade_count`** — the former is the
  count after de-duplication (trade_set mode) or the raw resolved count (date_range
  mode); the difference is exactly `len(run.skipped)`.
- **`run.skipped[].reason`** — one of `trade_not_found` (trade_set mode only — the id
  doesn't exist or belongs to another portfolio), `price_data_unavailable` (the
  trade's `exit_date` is today or later, or its ticker's own price history could not
  be fetched), `insufficient_history` (fewer than 14 trading days of the ticker's own
  price history, or fewer than 200 trading days of the regime series it depends on,
  exist before the trade's `entry_date` — never silently evaluated against an
  unwarmed-up value).
- **`run.rule_set`** — the current live strategy parameters used for this run,
  echoed for audit only. The request cannot supply, override, or vary any of these
  values (§13 Binding Condition 4) — an extra field anywhere in the request body is a
  validation error precisely to enforce this at the wire.
- **`run.price_data_fingerprint`** — a SHA-256 hash over the rule set, every replayed
  trade's own identifying fields, and the exact price/regime data used. Two runs of
  the same request (same code and dependency versions) that produce the same
  fingerprint are guaranteed to produce byte-identical `trades` and `summary`; a
  changed price anywhere in the window changes the fingerprint. `null` when zero
  trades were replayed (no fetch occurred).
- **Price basis.** Every trade is simulated in "ratio space" anchored at its own
  recorded `entry_price` — the simulation never compares a recorded price against a
  raw `yfinance` value directly (dividend adjustment, stock splits, and UK pence make
  the two bases incompatible). `initial_stop` and `simulated_exit_price` are therefore
  in the trade's own recorded price unit, not `yfinance`'s adjusted-series unit.
- **P&L.** `simulated_pnl_native = (simulated_exit_price × (1 − sell_fee) − entry_price) × shares`,
  where `sell_fee` is the same 0.15% (US) / 0% (UK) rate the strategy engine already
  uses. No entry fee is applied (the recorded `entry_price` is used as-is) — this
  figure is **not comparable** with a trade's recorded `pnl` in `trade_history`, which
  uses the real, full fee schedule.
- **GBP conversion.** `simulated_pnl_gbp = simulated_pnl_native / entry_fx_rate` for a
  US trade (the trade's own recorded entry-time rate); a UK trade's native value
  already is its GBP value (`fx_basis: "not_applicable_gbp"`). If a US trade's
  `entry_fx_rate` was never recorded (`fx_basis: "unavailable"`), its `simulated_pnl_gbp`
  is `null` and it is excluded from `summary.total_simulated_pnl_gbp` (counted in
  `summary.excluded_from_gbp_total`) rather than silently treated as zero. FX movement
  after the trade's entry is deliberately not modelled — no historical FX series exists
  for a date the user did not trade on.
- **`summary.win_rate_pct`** — `null` when `summary.trade_count` is 0 (never a
  fabricated 0%). `summary.total_simulated_pnl_gbp` is `0.0`, not `null`, when there is
  nothing to sum (0 trades, or every trade excluded from the GBP total).
- **0 trades replayed is a normal 200 response**, not an error — `trades: []`,
  `summary.trade_count: 0`, `retrospective_notice` still present.
- **Exit reasons** (`simulated_exit_reason`): `"Stop"`, `"Risk-Off"` (both already
  rendered by the frontend's `StrategyBenchmark.js` `EXIT_REASON_BADGE` map), and
  `"Actual Exit"` — no rule fired before the trade's own real exit date, so the
  simulated exit is that date's own price (not in the badge map; rendered as plain
  text, the intended treatment for an unbadged reason).
- **Independence.** Each trade in a `trade_ids` batch is replayed independently — there
  is no shared cash, position cap, or chronology between trades in a batch. Mixing
  tickers and non-contiguous dates in one `trade_ids` request is well-defined and
  supported.

**Errors:**

| HTTP | `code` | When |
|------|--------|------|
| `400` | `validation_error` | Any request-shape problem — see the bullet list above the request body. |
| `400` | `replay_scope_too_large` | Resolved trades exceed 100, or distinct tickers exceed 25. |
| `500` | `price_data_unavailable` | The price provider returned no usable data at all for every requested ticker, or for a regime series (SPY / ^FTSE) this run required. Distinct from a per-trade `skipped` entry of the same name, which covers one trade's own individually-missing data without failing the whole request. |
| `500` | `replay_failed` | Any unexpected server error. |

---

*Contract authored by Sprint Execution Engine — agent-mediated governance protocol, ST-01b, cycle 2026-09-23__release-v9.7.*
