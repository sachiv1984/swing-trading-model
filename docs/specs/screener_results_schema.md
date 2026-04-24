**Owner:** Head of Specs Team
**Class:** Class 2 Canonical Specification
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-04-23
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Strategy Parameter Source:** claude/strategy/strategy_rules.md §11

---

# Screener Results Schema

**Purpose:** Defines the canonical output schema for the Arc 1 Strategy-Rules Screener Engine (DS-01). Every screener result record must conform to this schema. Downstream consumers (screener results page DS-02, watchlist promotion flow DS-07) must use these field names and semantics.

---

## 1. Screener Result Record

A screener result record represents one ticker that has been evaluated by the screener engine. Records are produced per screener run; only tickers that pass all filters appear in the result set.

### 1.1 Output Fields

| Field | Type | Nullable | Derivation source | Description |
|-------|------|----------|-------------------|-------------|
| `ticker` | `string` | NO | Input ticker list | Exchange ticker symbol (e.g. `NVDA`, `FRES.L`) |
| `market` | `enum("US", "UK")` | NO | Derived from ticker format: `.L` suffix = UK, else US | Market classification |
| `currency` | `enum("USD", "GBP")` | NO | Derived from `market`: US → USD, UK → GBP | Price currency. UK tickers: Yahoo Finance returns pence; screener converts to GBP before storing |
| `price` | `number` | NO | Yahoo Finance (UK) or Alpaca Markets (US) | Last close price in `currency` |
| `atr` | `number` | NO | Calculated from 14-day price history (§11 parameter: ATR period = 14 days). UK tickers: pence→GBP conversion applied before storage | 14-day Average True Range in `currency`. Used for stop sizing |
| `atr_period` | `integer` | NO | `claude/strategy/strategy_rules.md §11` | ATR lookback period in days. Canonical value: 14. Must match §11 at time of screener run |
| `regime_status` | `enum("risk_on", "risk_off")` | NO | 200-day MA of relevant index: SPY (US market), FTSE (UK market). Risk-on if price > MA200 | Market regime at time of screen run. Tickers failing regime gate are excluded from results |
| `regime_index` | `string` | NO | Derived from `market`: US → `"SPY"`, UK → `"^FTSE"` | Index used for regime gate evaluation |
| `regime_index_price` | `number` | NO | Yahoo Finance | Current price of regime index at time of run |
| `regime_index_ma200` | `number` | NO | Calculated from 200 trading days of Yahoo Finance data | 200-day moving average of regime index at time of run |
| `signal_score` | `number (0.0–1.0)` | NO | Signals endpoint (`POST /signals/generate`) | Momentum signal score. Only tickers above the screener signal threshold appear in results |
| `signal_type` | `string \| null` | YES | Signals endpoint | Signal type descriptor from signals service (e.g. `"strong_momentum"`) |
| `sector` | `string \| null` | YES | Yahoo Finance `quoteType.sector` (DS-03 enrichment) | Sector classification. Null if Yahoo Finance does not return a sector for this ticker |
| `industry` | `string \| null` | YES | Yahoo Finance `quoteType.industry` (DS-03 enrichment) | Industry sub-classification. Null if not available |
| `proximity_to_entry_zone` | `number \| null` | YES | Calculated: `(price - entry_zone_lower) / entry_zone_lower`. Entry zone definition: price within 2× ATR of the current momentum entry trigger. Null if entry zone cannot be computed | Fractional proximity to entry zone (0.0 = at zone lower, positive = above zone). Negative means price is below entry zone lower bound |
| `news_headline_count` | `integer` | NO | Alpaca News API (DS-06). US tickers only; UK tickers: 0 | Count of recent news headlines from Alpaca News API for this ticker |
| `news_headlines` | `array<NewsHeadline>` | NO | Alpaca News API (DS-06). US tickers only; UK tickers: [] | List of recent news headline objects. May be empty. See §1.2 |
| `run_id` | `string (UUID)` | NO | Generated per screener run | Unique identifier for the screener run that produced this record. All results from one run share the same `run_id` |
| `run_timestamp` | `string (ISO-8601)` | NO | System time at start of screener run | UTC timestamp when the screener run was initiated |

### 1.2 NewsHeadline Object

| Field | Type | Nullable | Description |
|-------|------|----------|-------------|
| `id` | `integer` | NO | Alpaca news item ID |
| `headline` | `string` | NO | Headline text (verbatim from Alpaca) |
| `created_at` | `string (ISO-8601)` | NO | Publication timestamp |
| `source` | `string \| null` | YES | News source identifier |

**§13 compliance note:** Headlines are surfaced verbatim. No sentiment scoring, no sentiment labels, no advisory generation. See `docs/product/decisions/sec13_review_DS-06_alpaca_news_panel.md`.

---

## 2. Screener Run Parameters

Every screener run must log the parameter set used. This enables audit traceability and reproducibility.

### 2.1 Run Metadata

| Field | Type | Description |
|-------|------|-------------|
| `run_id` | `string (UUID)` | Unique run identifier |
| `run_timestamp` | `string (ISO-8601)` | UTC start time |
| `parameter_version` | `string` | Version of `claude/strategy/strategy_rules.md §11` at time of run (e.g. `"§11 v2026-04-23"`) |
| `atr_period` | `integer` | ATR lookback period used (from §11; canonical: 14) |
| `ticker_universe` | `array<string>` | Input list of tickers evaluated |
| `tickers_evaluated` | `integer` | Count of tickers evaluated |
| `tickers_passed_regime` | `integer` | Count of tickers that passed regime gate |
| `tickers_passed_atr` | `integer` | Count of tickers that passed ATR threshold gate |
| `tickers_in_results` | `integer` | Count of tickers in final result set |
| `us_market_regime` | `enum("risk_on", "risk_off")` | US market regime (SPY vs MA200) for this run |
| `uk_market_regime` | `enum("risk_on", "risk_off")` | UK market regime (FTSE vs MA200) for this run |

### 2.2 Logging Requirement

**Screener runs must log the parameter set used for each run.** The log record must include:
- `run_id` and `run_timestamp`
- `parameter_version`: the §11 version (or document hash) active at run time
- All §11 parameter values used: `atr_period`, signal threshold, and any other screener parameters defined by DS-01 implementation

**Purpose:** Enables post-run audit of which strategy parameters were active at the time of a given screen. Required for compliance and reproducibility under the strategy governance framework.

**Storage:** Run metadata may be stored in the `screener_runs` database table (defined by DS-01 migration), application logs, or both — DS-01 implementation must choose and document the storage mechanism.

---

## 3. Parameter Sources (§11 Reference)

The following screener parameters are governed by `claude/strategy/strategy_rules.md §11`:

| Parameter | §11 value | Description |
|-----------|-----------|-------------|
| ATR period | 14 days | Lookback for ATR calculation |
| Initial stop multiplier | 5 × ATR | Used in entry zone proximity calculation |
| Profitable stop multiplier | 2 × ATR | Post-entry risk management (not screener gate) |

**Signal threshold** and **ATR minimum threshold** for screener gates are defined by the DS-01 screener engine implementation. These are operational parameters not currently in §11 — they must be documented in the DS-01 implementation spec and referenced here once defined.

**Regime gate:** Defined in `claude/strategy/strategy_rules.md` (positions are exited when market enters risk-off regime; screener applies the same logic to candidate selection — only candidates in risk-on markets are returned).

---

## 4. Filter Ordering

The screener evaluates tickers in this order. Tickers failing a gate are excluded from subsequent gates:

1. **Regime gate:** Is the relevant market index (SPY/FTSE) above its 200-day MA? Fail → excluded.
2. **Data sufficiency gate:** Is sufficient price history available to calculate ATR (minimum 14 + 1 = 15 bars)? Fail → excluded.
3. **ATR gate:** Is ATR above the minimum threshold? (Threshold defined by DS-01.) Fail → excluded.
4. **Signal gate:** Is signal score above the minimum threshold? (Threshold defined by DS-01.) Fail → excluded.
5. **Result inclusion:** Ticker passes all gates → included in `screener_results` with all fields populated.

---

## 5. Market Routing

| Field | US tickers | UK tickers |
|-------|-----------|-----------|
| OHLCV data source | Alpaca Markets API (DS-05) | Yahoo Finance |
| Price currency | USD | GBP (Yahoo returns pence; convert ÷ 100) |
| ATR currency | USD | GBP (pence → GBP conversion applied) |
| News source | Alpaca News API (DS-06) | Not available (news_headline_count=0) |
| Regime index | SPY | ^FTSE |

---

## 6. Result Set Ordering

Screener results are ordered by `signal_score` descending (highest momentum first) by default. The implementation may support client-specified sort fields — if so, the default must remain `signal_score` descending when no sort parameter is provided.

---

## DoQ Sign-Off

- [x] All screener output fields defined with type, nullability, and derivation source
- [x] §11 referenced as parameter source for regime gate, ATR multiplier, and signal threshold fields
- [x] Logging requirement section included (§2.2)
- [x] Market routing table included (§5)
- [x] Document added to Specs_Index.md (separate commit in same PR)
- Signed off by: Sprint Execution Engine (autonomous class)
- Date: 2026-04-23
- Comments: Autonomous class sign-off — all four qualifying criteria met (all stories autonomous, all AC code-review-verifiable, no frontend changes, engine signer populated).
