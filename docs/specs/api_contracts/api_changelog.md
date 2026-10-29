**Owner:** API Contracts & Documentation Owner
**Class:** Class 2
**Status:** Canonical
**Version:** 1.27.0
**Last Updated:** 2026-10-29 (ST-06, EPIC-01, v9.14, BLG-OPS-194 — v9.14.0 entry: GET /health/detailed's Yahoo Finance check reports fallbacks); prior — 2026-10-29 (ST-04/ST-05, EPIC-01, v9.14, BLG-BE-194/BLG-BE-169 — v9.14.0 entry: GET /portfolio, GET /positions and GET /market/status gain fx_rate_source and fx_rate_as_of); prior — 2026-10-29 (ST-03, EPIC-01, v9.14, BLG-BE-193 — v9.14.0 entry: GET /market/status and GET /market/regime report an unknown regime); prior history retained — see prior entries in version control
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

# API Changelog

## Entry Template (ST-23, EPIC-04, v9.2, BLG-GOV-205)

Every release entry in this changelog follows this structure — documented here as the canonical template rather than left as an unstated convention:

```markdown
## vX.Y.0 (YYYY-MM-DD — Release vX.Y)

### <api_contracts_file>.md — vA.B (NEW | UPDATED)

**EPIC:** EPIC-xx
**ST:** ST-xx

| Change | Details |
|--------|---------|
| New endpoint: METHOD /path | One-sentence description of what it does and why (BLG-xx if applicable). |
| Updated endpoint: METHOD /path | What changed and why, if this is an UPDATED entry rather than NEW. |
```

Rules:
- One `## vX.Y.0` heading per release that changed the API surface — omit releases with no API changes entirely (do not add an empty heading).
- One `### <file>.md — vA.B` subsection per contract file touched in that release, even if multiple contract files changed in the same release (see `v8.5.0`'s single-file example above for the common case; multi-file releases add one subsection per file).
- `NEW` marks a contract file's first appearance in this changelog; `UPDATED` marks a subsequent revision to an already-listed file.
- The Change/Details table uses one row per endpoint added or materially changed — not one row per release. A release adding 3 endpoints to the same contract file gets 3 table rows under one subsection, not 3 subsections.
- Every entry must be traceable to a governing story: `**EPIC:**`/`**ST:**` fields are mandatory, matching `execution_prompt.md` §5.1's `spec_references` traceability discipline for the story itself.

**Conformance check (this story):** reviewed all existing entries in this file (`v8.9.0` down through the backfilled `v7.9.0`/`v8.2.0` entries) against the template above. **All existing entries already conform** — no migration note required. This is expected: the template above is a formalisation of the structure every entry already used ad hoc, not a new structure being retrofitted.

**Sign-off:** Head of Specs Team — Approved. Formalising an already-consistently-used structure (rather than introducing a new one requiring migration) is the right scope for this story — the conformance check confirms there was nothing to migrate. Sprint Execution Engine (agent-mediated, Head of Specs Team role — §5.3), 2026-09-08.

---

## v9.14.0 (2026-10-29 — Release v9.14)

### market_endpoints.md — v0.4 (UPDATED)

**EPIC:** EPIC-01
**ST:** ST-03

| Change | Details |
|--------|---------|
| Updated endpoint: GET /market/status | Each index adds `regime_status` (`risk_on`, `risk_off` or `unknown`). When the index data is unavailable from every source, `price`, `ma200` and `is_risk_on` are `null` and `regime_status` is `unknown`, instead of a defaulted risk-on with price 0 (BLG-BE-193). |
| Updated endpoint: GET /market/regime | `data[].status` adds `unknown` for an unmeasured market (BLG-BE-193). |

### market_endpoints.md — v0.5 (UPDATED)

**EPIC:** EPIC-01
**ST:** ST-04, ST-05

| Change | Details |
|--------|---------|
| Updated endpoint: GET /market/status | Adds `fx_rate_source` (`live` / `last_known` / `constant`) and `fx_rate_as_of`; on a fetch failure `fx_rate` is the last good rate before the 1.27 constant (BLG-BE-194/BLG-BE-169). |

### portfolio_endpoints.md — v2.14.0 (UPDATED)

**EPIC:** EPIC-01
**ST:** ST-04, ST-05

| Change | Details |
|--------|---------|
| Updated endpoint: GET /portfolio | Adds `fx_rate_source` and `fx_rate_as_of` describing `live_fx_rate`, which falls back to the last good rate before the 1.27 constant (BLG-BE-194/BLG-BE-169). |

### position_endpoints.md — v2.18.0 (UPDATED)

**EPIC:** EPIC-01
**ST:** ST-04, ST-05

| Change | Details |
|--------|---------|
| Updated endpoint: GET /positions | Each position adds `fx_rate_source` and `fx_rate_as_of` describing `live_fx_rate` (BLG-BE-194/BLG-BE-169). |

### health_endpoints.md — v1.9 (UPDATED)

**EPIC:** EPIC-01
**ST:** ST-06

| Change | Details |
|--------|---------|
| Updated endpoint: GET /health/detailed | `checks.yahooFinance` is `degraded` or `unhealthy`, with `details.reason`, when the FX rate or a regime index fell back; it adds `fx_rate_source`, `fx_rate_as_of`, `spy_regime_source` and `ftse_regime_source` to `details` (BLG-OPS-194). |

## v9.13.0 (2026-10-16 — Release v9.13)

### position_endpoints.md — v2.16.1 (UPDATED)

**EPIC:** EPIC-01
**ST:** ST-02

| Change | Details |
|--------|---------|
| Updated endpoint: POST /positions/{position_id}/exit | Enforces the documented `exit_reason` list: an unlisted value, an empty string or a legacy snake-case spelling returns `400` before anything is written; omitted or `null` still means `Manual Exit` (BLG-SPEC-186). The list matches `data_model.md` DS-34's CHECK constraints. |

### signal_endpoints.md — v1.9 (UPDATED)

**EPIC:** EPIC-01
**ST:** ST-05

| Change | Details |
|--------|---------|
| Updated endpoint: POST /signals/rebalance-exit | Implements `strategy_rules.md` §8.4 (v1.17): the ranking is every ticker today's momentum signal run wrote, whatever its status; `risk_off_exit` positions and positions at their stop are skipped; with no run recorded today it creates nothing and returns 503 (BLG-GOV-391, BLG-OPS-190). |

### red_flag_journal.md — v1.1.0 (UPDATED)

**EPIC:** EPIC-01
**ST:** ST-04

| Change | Details |
|--------|---------|
| Updated endpoint: GET /portfolio/red-flag-journal | Can now return `checklist_skipped` events, written when `POST /trade-plans` or `PUT /trade-plans/{id}` saves a non-empty, incomplete checklist; context `source`, `plan_id`, `unchecked_items`, `total_items` (BLG-BE-182). Response shape unchanged. |

### reports_endpoints.md — v0.18 (UPDATED)

**EPIC:** EPIC-02
**ST:** ST-09

| Change | Details |
|--------|---------|
| Updated endpoint: GET /reports/monthly-pnl | A failure to read or write `monthly_pnl_snapshots` no longer fails the request: it returns `200` with realised P&L for every month and none of the four restatement fields, and logs the failure with `exc_info` (BLG-BE-156). Success shape unchanged. |

### position_endpoints.md — v2.17.0 (UPDATED)

**EPIC:** EPIC-02
**ST:** ST-10

| Change | Details |
|--------|---------|
| New endpoint: GET /positions/stop-freshness | Median and maximum age of `stop_calculated_at` across open positions, with the oldest stop's ticker and the never-recalculated count, for System Status (BLG-SPEC-188). Read-only. |

### portfolio_endpoints.md — v2.13.0 (UPDATED)

**EPIC:** EPIC-02
**ST:** ST-06

| Change | Details |
|--------|---------|
| Updated endpoint: POST /portfolio/position | A fetched (or fallback) ATR where `5 × ATR ≥ entry_price` is rejected with `400` before anything is stored: `strategy_rules.md` §5 gives no stop for the entry (BLG-BE-180; Strategy Rules & System Intent Owner ruling (A)). |

### settings_endpoints.md — v1.6.0 (UPDATED)

**EPIC:** EPIC-02
**ST:** ST-08

| Change | Details |
|--------|---------|
| Updated endpoint: POST /settings | Behavioural change: a body that sets `min_hold_days`, `atr_period`, `atr_multiplier_initial` or `atr_multiplier_trailing` to a non-null value returns `400` naming `strategy_rules.md` §11; nothing is written (was stored and ignored). Absent or `null` is a no-op (BLG-API-07). |
| Updated endpoint: PATCH /settings/{settings_id} | Same rule as `POST /settings`; a mixed body is rejected whole (BLG-API-07). |

### ai_endpoints.md — v1.32 (UPDATED)

**EPIC:** EPIC-05
**ST:** ST-28

| Change | Details |
|--------|---------|
| Updated endpoint: POST /ai/check-daily-cost | Response gains `status: "ok"`. A failed cost query now returns `503` with `status: "error"`, `error: "cost_query_failed"` and no totals (was a 200 reporting $0 spend), so the scheduler's step fails and sends a Telegram message (BLG-OPS-187). |

### health_endpoints.md — v1.8 (UPDATED)

**EPIC:** EPIC-05
**ST:** ST-29

| Change | Details |
|--------|---------|
| Updated endpoint: GET /health/detailed | Response gains `render_service_id` (Render's `RENDER_SERVICE_ID`, `null` off Render), so the staging smoke test can confirm the host behind `STAGING_API_URL` is the staging backend (BLG-OPS-189). |

### ops_endpoints.md — v1.4 (UPDATED)

**EPIC:** EPIC-05
**ST:** ST-31

| Change | Details |
|--------|---------|
| New endpoint: GET /ops/api-call-attribution | Market-data provider calls over the last day or week, grouped by the route or job that triggered them and by provider, with an estimated cost (every unit cost is 0.0 today) and the top 3 features; 503 if the query fails (BLG-OPS-19). |

### screener_api_contract.md — v1.6 (UPDATED)

**EPIC:** EPIC-05
**ST:** ST-32

| Change | Details |
|--------|---------|
| Updated endpoint: GET /screener/history | Each run gains `duration_seconds`, the run's time from start to persistence; `null` for runs before v9.13 (BLG-OPS-23). |

## v9.12.0 (2026-10-13 — Release v9.12)

### market_endpoints.md — v0.3 (UPDATED)

**EPIC:** EPIC-03
**ST:** ST-17

| Change | Details |
|--------|---------|
| New endpoint: GET /market/atr/{ticker} | Returns a ticker's 14-day ATR in native currency (or `null`), fetched as `POST /portfolio/position` fetches it, so Trade Entry can show the system stop, risk and suggested shares before save (BLG-BE-146). Read-only. |

## v9.11.0 (2026-10-09 — Release v9.11)

### reports_endpoints.md — v0.17 (UPDATED)

**EPIC:** EPIC-04
**ST:** ST-25

| Change | Details |
|--------|---------|
| New endpoint: GET /reports/monthly-pnl/narrative | Returns the stored AI summary of one tax year's Monthly P&L figures if it was written from the current figures; never calls the model (BLG-FEAT-59). |
| New endpoint: POST /reports/monthly-pnl/narrative | Returns the stored summary or generates one: output checks, regenerate once, code-written fallback, 10/min/IP rate limit, 40-call daily cap (429), fail-closed 503, `advisory: true`. §13 CONDITIONAL (BLG-FEAT-59). |

## v9.7.0 (2026-09-25 — Release v9.7)

### replay_endpoints.md — v1.0 (NEW)

**EPIC:** EPIC-01
**ST:** ST-01b

| Change | Details |
|--------|---------|
| New endpoint: POST /replay/run | Replays a date range or an explicit set of the user's own closed trades, independently, through the current strategy engine's stop/risk-off exit rules -- a deterministic, retrospective simulation (BLG-FEAT-74). Makes no Alpaca call, persists nothing. |

## v9.6.0 (2026-09-21 — Release v9.6)

### alerts_endpoints.md — v0.8 (UPDATED)

**EPIC:** EPIC-01
**ST:** ST-04

| Change | Details |
|--------|---------|
| Updated endpoint: POST /alerts/evaluate | Evaluates a new `reflection_reminder` step (closed trade, no saved reflection, ≥ 48 h; at most one per trade). Response gains `reflection_reminders` (BLG-FEAT-98). |
| Updated endpoint: GET /notifications/preferences | Now returns five preference types; `reflection_reminder` is backfilled for already-seeded portfolios and defaults to `email_enabled: false`. |
| Updated endpoint: PATCH /notifications/preferences | Accepts the `reflection_reminder` key (a preference type, not a rule type). |
| Updated endpoint: GET /notifications | `alert_type` gains `reflection_reminder`; `context` is `{trade_id, ticker, exit_date}` for that type. |

### reports_endpoints.md — v0.13 (UPDATED)

**EPIC:** EPIC-02
**ST:** ST-07, ST-08

| Change | Details |
|--------|---------|
| Updated endpoint: GET /reports/monthly-pnl | Per-month `data[]` objects gain `null_fee_trade_count` — count of that month's closed trades with `entry_fees` or `exit_fees` NULL in `trade_history` (BLG-FR-04). Audit signal only; does not change `realised_pnl_gbp`. |
| Updated endpoint: GET /reports/monthly-pnl | Per-month `data[]` objects gain `snapshotted`/`restated`/`snapshot_realised_pnl_gbp`/`restated_diff_gbp` — month-end immutable baseline + restatement diff, backed by new table `monthly_pnl_snapshots` (BLG-FR-05, `data_model.md` DS-20). |
| Updated endpoint: GET /reports/tax-year | `summary` gains `restated_month_count`/`restated_months_notice`, derived from the same snapshot table for months overlapping the tax year (BLG-FR-05). No separate tax-year snapshot. |

None of the above fields are added to either endpoint's `format=csv` export.

### strategy_benchmark_endpoints.md — v1.3 (UPDATED)

**EPIC:** EPIC-03
**ST:** ST-10

| Change | Details |
|--------|---------|
| Updated endpoint: GET /strategy/backtest-rule-change/runs | Gains `offset` query param for paging. A negative `limit` or `offset` now returns HTTP 400 `INVALID_PARAMS` instead of a 500 (BLG-BE-118). |

---

## v8.9.0 (2026-08-18 — Release v8.9)

### strategy_benchmark_endpoints.md — v1.2 (NEW)

**EPIC:** EPIC-02
**ST:** ST-07

| Change | Details |
|--------|---------|
| New endpoint: POST /strategy/backtest-rule-change/run | Runs a candidate `strategy_rules.md` parameter change against a bounded historical window (first 20 active `ticker_universe` tickers, trailing 4 years), entirely in-app, and compares it against the live rule set over the identical universe/window (BLG-FEAT-89). Persists the run for audit. |
| New endpoint: GET /strategy/backtest-rule-change/runs | Run history, most recent first (AC-03). |
| New endpoint: GET /strategy/backtest-rule-change/runs/{run_id} | Re-view a prior run's stored output without re-running (AC-03). |

## v8.5.0 (2026-08-10 — Release v8.5)

### screener_api_contract.md — v1.3 (UPDATED)

**EPIC:** EPIC-06
**ST:** ST-21

| Change | Details |
|--------|---------|
| New endpoint: GET /screener/regime-distribution | Returns the aggregate risk-on/risk-off market regime distribution over screener run history for a rolling 30d/60d/all window (BLG-FEAT-29). Sourced from `screener_runs.regime_us`/`regime_uk` (one row per run), not `screener_results` (one row per ticker). |

**Note (this entry, corrected by ST-26/EPIC-06/v8.8, BLG-SPEC-118):** this changelog had not been updated between `v7.8.0` and this entry — the `v7.9`–`v8.4` gap flagged here has since been backfilled below (`v8.2.0`, `v7.9.0`), based on a full re-derivation of every `docs/specs/api_contracts/*.md` Changelog table entry dated within that window, not just the products changelog's higher-level "Spec sections updated" column (which cites section references, not necessarily new-endpoint additions — cross-checking against the actual contract file text caught one false positive, `PATCH /watchlist/{entry_id}`, cited in `v7.9`'s product changelog row but confirmed pre-existing since `v5.3`).

## v8.2.0 (2026-08-05 — Release v8.2)

### reports_endpoints.md — v0.11 (NEW)

**EPIC:** EPIC-01
**ST:** ST-01

| Change | Details |
|--------|---------|
| New endpoint: GET /reports/reconciliation | P&L / tax record reconciliation report (BLG-FEAT-88) — compares the Tax Year report's system-computed realised P&L total against an independently re-derived export-side sum for the same tax year, and surfaces a pass/fail match indicator to the user. |

## v7.9.0 (2026-07-28 — Release v7.9)

### portfolio_endpoints.md — v2.5.0 (NEW)

**EPIC:** EPIC-02
**ST:** ST-02

| Change | Details |
|--------|---------|
| New endpoint: GET /portfolio/sector-regime-trend | Weekly-bucketed sector concentration + regime status trend (BLG-FEAT-67), backed by a new `sector_regime_history` table (going-forward capture only — no prior historical sector/regime data existed to aggregate). |

**Note (this entry):** the remaining 5 releases in the backfilled `v7.9`–`v8.4` window — `v7.10`, `v8.0`, `v8.1`, `v8.3`, `v8.4` — shipped no new endpoints (confirmed via a full scan of every contract file's own Changelog table for entries dated within each release's ship window; all changes in that period were field additions to existing endpoints, response-example corrections, or documentation backfill of already-shipped-but-undocumented routes — e.g. `v8.4`'s `GET /test/quick-health`/`POST /test/rate-limit-scenarios`, which `health_endpoints.md`'s own changelog states "both routes existed in `backend/routers/test.py` but were undocumented," not newly shipped). No entries added for those 5 releases — an empty release is not silently missing, it is confirmed empty.

## v7.8.0 (2026-07-27 — Release v7.8)

### changelog_endpoints.md — v1.0 (NEW)

**EPIC:** EPIC-01
**ST:** ST-01

| Change | Details |
|--------|---------|
| New endpoint: GET /changelog/latest | Returns the most recent release's version label and changes-shipped descriptions, parsed server-side from docs/product/changelog.md. Backs the in-app "What's New" panel (dashboard.md §6A). `data` is null if no parseable version section exists. |

### reports_endpoints.md — v0.10 (UPDATED)

**EPIC:** EPIC-05
**ST:** ST-05

| Change | Details |
|--------|---------|
| New query param: GET /reports/monthly-pnl?format=csv | Returns a CSV file download of the month rows (Year, Month, Realised P&L (GBP), Trades) instead of JSON — mirrors the existing GET /reports/tax-year?format=csv handler. Invalid format values return 400. |

### ai_endpoints.md — v1.8 (UPDATED)

**EPIC:** EPIC-06
**ST:** ST-06

| Change | Details |
|--------|---------|
| New endpoint: GET /ai/spend-trend | Returns Claude API spend for the last 6 release cycles, oldest to newest, bucketed by date windows parsed from docs/product/changelog.md version headings. Sourced from existing claude_audit_log data. |

## v6.1.0 (2026-06-23 — Release v6.1)

### portfolio_endpoints.md — v2.4.0 (UPDATED)

**EPIC:** EPIC-03
**ST:** ST-06

| Change | Details |
|--------|---------|
| New endpoint: GET /portfolio/sector-weights | Returns open-position sector breakdown by market value: sectors array (sector_name, position_count, exposure_pct), total_positions, concentration_alert (true when ≥40% in single sector). Positions without sector field grouped as "Unclassified". Silent graceful degradation on error. |

### trade_plan_endpoints.md — v0.5 (UPDATED)

**EPIC:** EPIC-04
**ST:** ST-08

| Change | Details |
|--------|---------|
| New endpoint: GET /trade-plans/setup-quality-score | Returns 0-100 setup quality score from closed trade history. Gate: returns gate_not_met=true when <20 closed trades. Score = clamp(win_rate×0.6 + max(avg_pnl_pct,0)×0.4, 0, 100). Response includes: score, matching_trades, win_rate, average_pnl_pct, score_explanation. |

**Sign-off:** Sprint Execution Engine (autonomous class) — 2026-06-23

---

## v2.9.0 (2026-04-23 — Release v2.9)

### alpaca_integration_contract.md — v1.0 (NEW)

**EPIC:** EPIC-01 (Arc 1 Specification Foundation)
**ST:** ST-02 (BLG-SPEC-22)

| Change | Details |
|--------|---------|
| New contract: Alpaca Markets API integration | External API contract for Alpaca Data API v2. Documents GET /v2/stocks/{symbol}/bars (OHLCV bars, DS-05) and GET /v1beta1/news (news headlines, DS-06). Includes rate limits, error codes, retry strategy, and explicit fallback strategy (Yahoo Finance for OHLCV; empty panel for news). US tickers only. API version pinned. |

**Sign-off:** Sprint Execution Engine (autonomous class) — 2026-04-23

---

### screener_api_contract.md — v1.0 (NEW)

**EPIC:** EPIC-01 (Arc 1 Specification Foundation)
**ST:** ST-03 (BLG-SPEC-23)

| Change | Details |
|--------|---------|
| New endpoint: GET /screener/results | Returns screener result records from the latest (or specified) completed screener run. Offset-based pagination. Filter by market. Results ordered by signal_score descending. |
| New endpoint: POST /screener/run | Triggers an async screener run. Returns run_id (UUID) immediately. Results retrievable via GET /screener/results?run_id={run_id}. Returns 409 if a run is already in progress. |

**Sign-off:** Sprint Execution Engine (autonomous class) — 2026-04-23

---

## v2.1.2 (2026-03-20 — Release v2.1)

### trade_endpoints.md — v2.1.0

**EPIC:** EPIC-05 (Financial Reporting Exports & Enhancements)
**ST:** ST-14

| Change | Details |
|--------|---------|
| New field: `fill_price` per trade | Actual fill price in native currency. `null` for trades entered before v2.1 (Fill Price capture not yet active). Source: `positions.fill_price`. |
| New field: `slippage_pct` per trade | Computed server-side: `(fill_price − entry_price) / entry_price * 100`. Negative = favourable (filled below market). Positive = unfavourable. `null` when `fill_price` is `null`. Rounded to 2dp. |
| New field: `avg_slippage_pct` (top-level) | Portfolio average slippage across all trades with `fill_price` recorded. `null` when no trades have `fill_price`. |
| Data model gate | `fill_price` was pre-existing in `data_model.md` v1.2 (`positions` table, nullable `DECIMAL(10,4)`). Gate cleared: Data Model & Domain Schema Owner + Head of Specs Team countersigned 2026-03-20. |

**Sign-off:** Data Model & Domain Schema Owner + Head of Specs Team (gate) — 2026-03-20

---


## v2.1.1 (2026-03-20 — Release v2.1)

### reports_endpoints.md — v0.3

**EPIC:** EPIC-05 (Financial Reporting Exports & Enhancements)
**ST:** ST-13

| Change | Details |
|--------|---------|
| New format: `GET /reports/tax-year?format=csv` | CSV download of tax-year P&L report. `Content-Type: text/csv`. `Content-Disposition: attachment; filename="tax-year-{year}-pnl.csv"`. |
| CSV structure | 5-row metadata block (Tax Year, Generated At, Total Realised P&L, Total Closed Trades, Win Rate %), blank row, 17-column trades table with human-readable headers. |
| Column headers | Trade ID, Ticker, Market, Entry Date, Exit Date, Holding Days, Entry Price (Native), Exit Price (Native), Entry FX Rate (GBP/USD), Exit FX Rate (GBP/USD), Shares, Total Cost (GBP), Exit Proceeds (GBP), Realised P&L (GBP), P&L %, Currency, Tags. |
| `format` validation tightened | Unknown `format` values now return `400 — "format must be one of: pdf, csv"`. Previously unspecified. |
| No schema migration | Pure format conversion of existing endpoint data. |

**Sign-off:** Head of Engineering (implementation) — 2026-03-20

---

## v2.1.0 (2026-03-20 — Release v2.1)

### alerts_endpoints.md — v0.1 (new file)

**EPIC:** EPIC-02 (Alerts & Notifications)
**ST:** ST-02
**ADR:** ADR-003 (FastAPI BackgroundTasks delivery architecture)

| Change | Details |
|--------|---------|
| New endpoint: `GET /alerts/rules` | List alert rules for portfolio. Seeds 4 defaults on first call. Returns array with `id`, `type`, `enabled`, `threshold_percent`. |
| New endpoint: `POST /alerts/rules` | Create alert rule (used to restore after deletion). Returns `400` if type already exists. |
| New endpoint: `PATCH /alerts/rules/{rule_id}` | Update rule `enabled` or `threshold_percent`. |
| New endpoint: `DELETE /alerts/rules/{rule_id}` | Delete alert rule. Standard DELETE envelope. |
| New endpoint: `POST /alerts/evaluate` | Evaluate all enabled rules against current portfolio state. Enqueues email delivery as FastAPI BackgroundTask. Returns `notifications_created`, `delivery_tasks_enqueued`, `redelivery_tasks_enqueued`. |
| New endpoint: `GET /notifications` | Notification feed, newest first. Page-based pagination (50/page). Returns `notifications[]`, `total`, `page`, `per_page`, `has_more`. |
| New endpoint: `PATCH /notifications/{id}` | Mark one notification as read. Idempotent. |
| New endpoint: `POST /notifications/mark-all-read` | Mark all unread as read. Returns `marked_read_count`. |
| New endpoint: `GET /notifications/preferences` | Per-type email preferences. Seeds defaults on first call. |
| New endpoint: `PATCH /notifications/preferences` | Update preferences for one or more alert types. Map body: `{ alert_type_key: { email_enabled: bool } }`. |
| Architecture | Delivery via FastAPI `BackgroundTasks` — no Redis/Celery. Retry: re-enqueue on next evaluation if `delivered = false` and `delivery_attempts < 3`. |

**Data model:** `data_model.md` v1.9 — 3 new tables: `alert_rules`, `notifications` (with delivery tracking), `notification_preferences`.

**Sign-off:** Head of Specs Team — 2026-03-20

---


## v2.0.0 (2026-03-17 — Release v2.0)

### reports_endpoints.md — v0.1 (new file)

**EPIC:** EPIC-02 (4.1b Tax-Year P&L)
**ST:** ST-03

| Change | Details |
|--------|---------|
| New endpoint: `GET /reports/tax-year` | Tax-year P&L statement for UK tax years. Attribution by `exit_date`. `year` query parameter = start year of UK tax year (e.g. `year=2025` = 6 Apr 2025 to 5 Apr 2026). |
| Response shape | Top-level: `tax_year_start`, `tax_year_end`, `tax_year_label`, `generated_at`. Summary: `total_realised_pnl`, `total_gross_profit`, `total_gross_loss`, `win_count`, `loss_count`, `win_rate`, `estimated_unrealised_pnl`, `unrealised_note`. Trades array: full per-trade breakdown including FX rates, GBP costs/proceeds, tags. |
| Validation | Future year returns 400. Absent or non-integer `year` returns 400. Empty tax year returns 200 with zero summary and empty trades array. |
| Scope | UK-based accounts only (6 April to 5 April boundary). Not a substitute for qualified tax advice. |

**Sign-off:** Head of Specs Team + Financial Reporting & Records Owner — 2026-03-17

---

## Purpose

This document is the running changelog for all API contract versions. It must be updated alongside every contract version bump.

**Maintenance obligation:** Whenever an `*_endpoints.md` contract file is incremented (major or minor version), a corresponding entry must be added here. This document is the single place to trace what changed between API versions.

---

## v1.9.0 (2026-03-05 — Release v1.8)

### analytics_endpoints.md — v1.9.0

**EPIC:** EPIC-06 (Release v1.7) — Spec Debt
**ST:** ST-06 (v1.7)

| Change | Details |
|--------|---------|
| Added `sharpe_ratio_trade_method` as 14th validated metric | `POST /validate/calculations` now validates 14 metrics total. `sharpe_ratio_trade_method` is severity `critical`. The method field on the Sharpe result distinguishes `portfolio`, `trade`, or `insufficient_data` calculation paths. |
| Total metric count | `summary.total: 14` (was 13). Severity distribution: critical: 4, high: 3, medium: 6, low: 1. |

### portfolio_endpoints.md — v1.9.0

**EPIC:** EPIC-06 (Release v1.7) — Spec Debt
**ST:** ST-07 (v1.7)

| Change | Details |
|--------|---------|
| Spec corrected to match live API | Position summary objects in `GET /portfolio` confirmed to include: `current_value`, `current_stop`, `pnl_pct`, `fx_rate`, `live_fx_rate`. Field `pnl_pct` is the canonical field name for position P&L percentage (not `pnl_percent` — that appears in trade history only for backward compatibility). |

### trade_endpoints.md — v1.9.0

**EPIC:** EPIC-06 (Release v1.7) — Spec Debt
**ST:** ST-08 (v1.7)

| Change | Details |
|--------|---------|
| Added `holding_days` to changelog | `GET /trades` trade objects include `holding_days` (integer, calendar days from `entry_date` to `exit_date` inclusive). Field was present in the implementation and added to the spec changelog. |

---

## v1.9.0 — settings_endpoints.md (2026-03-05 — Release v1.8)

**EPIC:** EPIC-03 (Release v1.8) — API & Spec Debt
**ST:** ST-09 (v1.8)

| Change | Details |
|--------|---------|
| Replaced `PUT /settings` with `PATCH /settings/{settings_id}` and `POST /settings` | The live backend implementation uses `PATCH /settings/{settings_id}` for updating an existing settings record and `POST /settings` for creating a new one. The spec previously documented `PUT /settings` which was never the live behaviour. ESC-20260304-01 option (a) — spec updated to follow implementation. |
| Added lifecycle header | `settings_endpoints.md` now has a canonical lifecycle header. Version incremented to 1.1.0. |

---

## v1.8.1 (prior to Release v1.8)

### openapi.yaml — v1.8.1

**EPIC:** BLG-TECH-02 (pre-v1.8 technical debt)

| Change | Details |
|--------|---------|
| Added severity model to ValidationResponse | Each `POST /validate/calculations` result now includes a `severity` field (critical \| high \| medium \| low). Summary includes `by_severity` breakdown. |

---

## v1.8.0 (Release v1.7 — prior history)

### settings_endpoints.md — v1.8.0 (approximate)

| Change | Details |
|--------|---------|
| Added `default_risk_percent` field | `GET /settings` response includes `default_risk_percent` (float, > 0, ≤ 100). Used to pre-populate the Position Sizing Calculator widget. Default: `1.00`. |

---

## Maintenance Notes

- This changelog covers contract versions from v1.8.0 onward. Earlier history was not captured in this document.
- For pre-v1.8.0 changes, refer to individual `*_endpoints.md` file history.
- All future API contract version bumps must include an entry here before the PR is merged.

---

## Change Log (this document)

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-03-05 | Initial version. Backfilled v1.9.0 changes from EPIC-06 (v1.7) and EPIC-03 (v1.8). ST-12, S2-08. |
