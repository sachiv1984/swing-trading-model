**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect
**Class:** Supporting Document (Class 2) — Living Reference
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-10-27 (agent-mediated review findings applied: false-healthy Yahoo check, cost basis for §4, Alpaca feed condition); prior — 2026-10-27 (created)
**Source:** ST-33 (`BLG-OPS-77`), EPIC-05, cycle `2026-10-16__release-v9.13`
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Data Provider Risk Assessment

## Purpose

All market data comes from two providers, Alpaca and Yahoo Finance, and there is no documented failover if either is unavailable for a long period. This document lists every active external data provider, what fails and what that does to the system when each one is lost, the failover paths that are cheap to add, and the conditions under which the accepted risk must be reassessed.

It covers **market-data providers**: the services that supply prices, bars, FX, news and reference data. Supabase, Render, Anthropic and Telegram are infrastructure or advisory dependencies; their failure modes are in `docs/ops/external_api_dependency_register.md` and `docs/operations/external_api_risk_register.md` and are not repeated here.

Findings are from the code at `exec/2026-10-16__release-v9.13/EPIC-05`, read on 2026-10-27.

---

## 1. Active Data Providers

| Provider | Access | Cost | Used for |
|----------|--------|------|----------|
| Alpaca Market Data API (`data.alpaca.markets`) | REST, key and secret | Free tier, while `ALPACA_DATA_FEED` is unset or `iex` (`alpaca_service.py:41-43`); `sip` is a paid feed | US prices, US daily bars (ATR, screener), US news headlines |
| Alpaca Paper Trading API (`paper-api.alpaca.markets`) | REST, key and secret | Free | Mirroring opened and closed **US** positions to a paper account; the Paper Trading page |
| Yahoo Finance chart API (`query1.finance.yahoo.com/v8/finance/chart`) | Undocumented REST, no key | None | UK prices; US price and bar fallback; GBP/USD FX; SPY and FTSE 200-day regime |
| Yahoo Finance via the `yfinance` package | Undocumented, no key | None | Earnings dates, sector and industry, company names, watchlist details, gap risk, backtests and replay |

**Present in the code but not active:**

- **Stooq** and **Twelve Data:** `screener_data_service.py` has fetchers for both (`_stooq_fetch_ohlcv`, `_twelve_data_fetch_ohlcv`), but nothing calls them. `fetch_ohlcv` notes that Stooq times out from Render's IP range and that Twelve Data needs a paid plan for LSE symbols (`screener_data_service.py:545-548`). The Stooq claim rests on that code comment only; the Twelve Data claim was confirmed against the vendor's site on 2026-10-27 (§4). `external_api_dependency_register.md` MIT-08 still lists them as screener fallback tiers; that is out of date (§6).
- **newsapi.org:** the register's "News API" entry describes newsapi.org, but news comes from Alpaca's news endpoint (`news_service.py`). No newsapi.org call exists.
- **Wikipedia:** `backend/generate_ticker_lists.py` reads the S&P 500 and FTSE 100 lists. It is a manual script, not a runtime dependency.

---

## 2. Failure Modes and Impact

### Alpaca Market Data API

| Failure mode | What the system does | Impact |
|--------------|----------------------|--------|
| Outage, timeout or 5xx | US price (`get_current_price`), US ATR (`calculate_atr`) and US screener bars (`fetch_ohlcv`) fall back to Yahoo Finance after the bounded retry. | Low while Yahoo works: slower, with a different source. |
| Rate limit (free tier) | Same fallback to Yahoo per call. | Low; bulk screener runs move load onto Yahoo, which raises Yahoo's risk (YFM-02). |
| Credentials missing, revoked or expired | `_credentials_configured()` is false, so every US call goes straight to Yahoo. | Low for prices and bars. **US news shows no headlines** — there is no fallback. |
| News endpoint fails | `get_news_headlines` returns `[]`. UK tickers always return `[]` (Alpaca has no UK news). | Low: news is context only and feeds no rule. |
| Alpaca changes or ends the free tier | All of the above at once, permanently. | Medium: everything US moves onto Yahoo, which has no SLA. |

### Alpaca Paper Trading API

| Failure mode | What the system does | Impact |
|--------------|----------------------|--------|
| Outage or credential failure | For US positions only, position open and close in `main.py` (`:663-668`, `:702-707`) call `sync_open_paper_position` / `sync_close_paper_position`; a failure is logged and the real position is still recorded. The Paper Trading page cannot load positions. | Low: the paper account is a mirror and is not the system of record. It can drift from the real portfolio until re-synced. |

### Yahoo Finance (chart API and `yfinance`)

Yahoo is the larger risk. It has no contract, no SLA and no key, and can block Render's shared egress IPs. It is also the **only** source for several things:

| Failure mode | What the system does | Impact |
|--------------|----------------------|--------|
| UK price unavailable | `get_current_price` returns `None`; the position view uses the last stored `current_price`, or the entry price. | **High for UK positions:** P&L and stop-distance shown from a stale price, with no stale marker on that path. |
| FX (GBP/USD) unavailable | `get_live_fx_rate` serves the 5-minute cache, then falls back to the constant `DEFAULT_FX_RATE = 1.27` (`utils/pricing.py:25`, `:184-189`; `config.py:47`). | **High for US positions:** GBP P&L, portfolio value and sizing use a fixed rate that can be far from the market. |
| SPY or FTSE 200-day data unavailable | `check_market_regime` **defaults that market to risk-on**, with price and 200-day MA set to 0, and caches the result for 5 minutes (`utils/pricing.py:300-311`, `:325-326`). | **High:** this fails open. During an outage, new entries are allowed and the nightly risk-off job raises no risk-off exit alerts, whatever the market is doing. This is the most consequential single failure. |
| UK screener bars unavailable | `fetch_ohlcv` returns `None` for UK tickers (no other source). | Medium: UK tickers drop out of the screener and the momentum ranking, which can also trigger rebalance-exit alerts for held UK positions that are missing from the ranking. |
| US fallback unavailable while Alpaca is also down | `fetch_ohlcv` and pricing return `None` for US tickers. | High: no US data at all (a double failure). |
| Schema or shape drift (YFM-01) | Calls return empty or malformed data rather than an error. | Medium: looks like missing data, so it degrades as the rows above, often without a clear error. |
| Rate limit or IP block (YFM-02) | Empty responses or 429s; the crumb-based path shares a cooldown with earnings lookups. | As the rows above, intermittently. |
| `yfinance` reference data unavailable | Earnings dates, sectors, company names, watchlist details and gap-risk checks return nothing or an error. | Low to medium: pre-entry checks have less context (no earnings date, no gap risk), but no price or rule depends on them. |
| Monitoring reports Yahoo healthy during an outage | The System Status Yahoo Finance check calls `get_live_fx_rate()` and reports healthy unless it raises (`health_service.py:310-320`). `get_live_fx_rate()` never raises: it returns 1.27 on failure (`utils/pricing.py:184-189`). The rolling `yahoo_finance` call metrics are fed only by screener calls and are reset on restart (`health_service.py:63-80`). | **High:** an outage is invisible on System Status, so the fail-open regime and frozen FX above go unnoticed. |

### Impact if a provider is lost for an extended period

| Provider lost | Core trading function | Summary |
|---------------|----------------------|---------|
| Alpaca (data) | Keeps working on Yahoo | US prices, ATR and screener continue on Yahoo; US news disappears. No user-visible failure apart from news. |
| Alpaca (paper) | Unaffected | The paper mirror stops and drifts. |
| Yahoo Finance | **Degraded, partly unsafe** | US data continues on Alpaca. UK prices and UK screener stop. FX is frozen at 1.27. The market regime reads risk-on for both markets regardless of conditions. Earnings, sector and gap-risk context disappear. |
| Both | **Stopped** | No live prices or bars for any market; regime reads risk-on; FX frozen. |

---

## 3. Quick-Win Failover Paths

Each item is small, uses only providers already in place, and needs no new account or cost.

| # | Failover | Covers | Effort |
|---|----------|--------|--------|
| QW-1 | Compute the **SPY** 200-day regime from Alpaca daily bars when Yahoo fails (`get_ohlcv_bars("SPY", limit=210)`). | US half of the fail-open regime | S |
| QW-2 | When regime data is missing, mark the regime **unknown** and show it, instead of silently defaulting to risk-on. What the rules do on "unknown" (block entries, keep current state, or risk-on with a warning) is a strategy decision for the Strategy Rules & System Intent Owner; the visible marker is not. | Both markets' fail-open regime | S, plus a strategy ruling |
| QW-3 | Keep the last good FX rate (with its timestamp) in the database and use it before the 1.27 constant; show its age when it is older than a trading day. | Frozen FX | S |
| QW-4 | Mark a position's price as stale on the positions view when the live fetch fails and the stored price is shown. | Silent stale UK prices | S |
| QW-6 | Make the System Status Yahoo Finance check fail when the FX fetch falls back to the constant (or the regime fetch fails), so an outage is visible. | False-healthy monitoring | XS |
| QW-5 | Correct `external_api_dependency_register.md` and `external_api_credential_inventory.md`: news comes from Alpaca, and Stooq and Twelve Data are not active fallbacks. Then either delete the two unused fetchers or document why they are kept. | Out-of-date failover record | XS |

No quick win exists for UK prices or UK bars: Alpaca has no LSE data, Stooq times out from Render, and Twelve Data needs a paid plan for LSE. A second UK source is a cost decision (§5).

QW-1 to QW-4 and QW-6 are filed as backlog items (§6). Under QW-2, the strategy question stays open until the owner rules; only the visible marker is in scope.

---

## 4. Accepted Risk

**Statement.** The system accepts reliance on Yahoo Finance as the sole source for UK prices and bars, GBP/USD FX, the FTSE regime and reference data (earnings, sectors, gap risk), and on Alpaca's free tier as the primary US source. The reason is cost. Both sources are free. The cheapest second source with UK daily bars is Twelve Data's Grow plan: **$79 per month**, which lists the London Stock Exchange (XLON) at end-of-day level for Grow and above (twelvedata.com/pricing and /exchanges?level=grow, checked 2026-10-27). That is about $950 a year. Current external spend is far below it: Anthropic API spend is estimated at $0.05 – $0.25 a month (`docs/ops/anthropic_api_cost_trend_2026.md`), the staging services are $0 (`render.yaml`), and production runs on Render Starter. Paying $79 a month to cover UK data for a single-user system with a handful of UK positions is not justified while the outage risk can be reduced for free (§3).

The fail-open regime (§2), frozen FX and false-healthy monitoring are **not** accepted as permanent behaviour: QW-1 to QW-4 and QW-6 are filed to close them. Until they ship, the System Status Yahoo Finance check cannot be trusted to show an outage. The operator should treat the regime as unconfirmed whenever System Status shows a GBP/USD rate of exactly 1.27 (in the expanded Yahoo Finance check's details), because that value only appears when the FX fetch has failed. It can lag an outage by up to 5 minutes, while the cached rate is still served (`utils/pricing.py:153-155`). The Dashboard regime cards show only risk-on or risk-off, so they give no sign of a failed fetch.

**Sign-off.**

| Role | Decision | Date | Method |
|------|----------|------|--------|
| Infrastructure & Operations Owner | Accepted (agent-mediated, Infrastructure & Operations Owner role — §5.3) | 2026-10-27 | Agent-mediated review against the role charter; first pass Blocked (false-healthy Yahoo monitoring), Approved on retry 1 after §2, §3 QW-6, §4 and §5 were corrected. Pending human confirmation. |
| FinOps & Resource Architect | Accepted (agent-mediated, FinOps & Resource Architect role — §5.3) | 2026-10-27 | Agent-mediated review against the role charter; first pass Blocked (no cost basis for §4), Approved on retry 1 after §4 named the $79/month alternative and §1 and §5 were corrected. Open note: §4 gives no dollar figure for Render Starter, which no repo document records; it does not change the conclusion. Pending human confirmation. |

---

## 5. Re-evaluation Conditions

Reassess this document, and whether to pay for a second data source, when any of these happens:

1. Yahoo Finance is unavailable or blocked for more than 1 trading day in a row, or on 3 or more days in a calendar month. Until QW-6 ships, detect this from a GBP/USD rate of exactly 1.27 in System Status's Yahoo Finance details, or from the Render log lines "Could not fetch SPY data" / "Could not fetch FTSE data" (`utils/pricing.py:302`, `:310`).
2. Alpaca changes, limits or removes the free market-data tier, or the account's credentials are revoked.
3. The portfolio holds more than 10 open positions at once, or UK positions exceed half of portfolio value, so a UK data loss affects more capital.
4. The system moves from manual, advisory use to placing live orders automatically from signals.
5. A risk-on regime is recorded during a provider outage and a position is entered or held that the real regime would have blocked or flagged.
6. QW-1 to QW-4 have not shipped by the end of v9.15.
7. A data source with daily LSE bars becomes available for under $20 a month (a quarter of the current $79 alternative). Re-check vendor prices at each annual review.
8. At the annual review of this document (next due 2027-10-27).

---

## 6. Follow-up Items Filed

- `BLG-BE-192`: compute the SPY regime from Alpaca bars when Yahoo fails (QW-1)
- `BLG-BE-193`: show an unknown regime instead of silently defaulting to risk-on, with a Strategy Rules & System Intent Owner ruling on entries (QW-2)
- `BLG-BE-194`: keep the last good GBP/USD rate and show its age before falling back to the constant (QW-3)
- `BLG-FE-234`: mark stale prices on the positions view (QW-4)
- `BLG-OPS-194`: make the System Status Yahoo Finance check detect an outage (QW-6)
- `BLG-SPEC-209`: correct `external_api_dependency_register.md` and `external_api_credential_inventory.md` for Alpaca news and the inactive Stooq and Twelve Data fetchers (QW-5)
