**Owner:** Infrastructure & Operations Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.3
**Last Updated:** 2026-11-13 (ST-15, EPIC-06, v9.17, BLG-OPS-217 — §4 causes of the on-demand Yahoo failures recorded from a production api_call_log read, with the fix per feature); prior — 2026-11-13 (ST-16, EPIC-06, v9.17, BLG-OPS-195 — §5 is now checked weekly by `market-data-volume-check.yml`, which reads the §4 table); prior — 2026-11-11 (ST-13, EPIC-04, v9.16, BLG-OPS-197 — §4 weekly calls and failures recorded from one production report; §6 volume line ticked); prior history retained — see prior entries in version control
**Source:** ST-30 (`BLG-OPS-18`), EPIC-05, cycle `2026-10-16__release-v9.13`

# Data Pipeline Cost Baseline

## 1. Purpose

A combined weekly baseline for the market-data pipeline's three external sources (Alpaca, Yahoo Finance and the news API), so that a change in cost or usage can be noticed. It also defines the advisory threshold: more than 2× baseline.

The gate for this item, Alpaca call instrumentation (`BLG-OPS-17`), shipped in v9.3 and was verified at Release Planning on 2026-10-16.

## 2. What Each Source Costs

| Source | Service names in `api_call_log` | Plan | Price per call | Limit that matters |
|--------|-------------------------------|------|----------------|--------------------|
| Alpaca Market Data API (bars, prices) | `alpaca_data` | Free, IEX feed (`ALPACA_DATA_FEED` unset or `iex`; `sip` is paid) | $0 | 200 requests per minute (`alpaca_service.py`) |
| Alpaca News API (the "news API") | `alpaca_news` | Included with the free data plan | $0 | Same 200 per minute |
| Alpaca Paper Trading API | `alpaca_paper` | Free | $0 | — |
| Yahoo Finance (chart API and `yfinance`) | `yahoo` | No account, no key | $0 | Unpublished; throttles or blocks at high volume |

There is no newsapi.org account: news comes from Alpaca (`news_service.py`; `docs/operations/data_provider_risk_assessment.md` §1). Stooq and Twelve Data fetchers exist in the code but are not called.

**The combined weekly cost baseline is therefore $0.00.** Every source is free at current usage, so dollars cannot show a change. The baseline that can is **call volume**. Volume is what free tiers limit and what Yahoo blocks on, and it is what any future per-call price would multiply.

## 3. How Volume Is Measured

Since v9.13 every HTTP request to a market-data provider is written to `api_call_log` with its provider and the feature that triggered it (ST-31, DS-36, `backend/utils/api_attribution.py`). Each HTTP attempt is one row, so retries count, matching how providers count quota.

`GET /ops/api-call-attribution?window=weekly` returns the last 7 days' calls by provider (`by_service`) and by feature (`by_feature`), with the estimated cost from `UNIT_COST_USD`. This document's baseline is the `by_service` totals from that report.

Before v9.13 only Alpaca bar calls were counted (`service = 'alpaca'`, `GET /ops/alpaca-call-report`). Yahoo and news calls were not recorded anywhere, so no earlier volume baseline can be reconstructed.

## 4. Weekly Baseline

| Source | Calls per week | Failures per week | Cost per week |
|--------|---------------|-------------------|---------------|
| Alpaca data (`alpaca_data`) | 2,616 | 0 | $0.00 |
| Alpaca news (`alpaca_news`) | 1 | 0 | $0.00 |
| Alpaca paper (`alpaca_paper`) | 0 | 0 | $0.00 |
| Yahoo Finance (`yahoo`) | 4,488 | 665 | $0.00 |
| **Combined** | **7,105** | **665** | **$0.00** |

**Recorded:** 2026-11-11, from one production `GET /ops/api-call-attribution?window=weekly` report (the last 7 days, about 2026-11-04 to 2026-11-11), supplied by the user (Infrastructure & Operations Owner) in session (ST-13, EPIC-04, v9.16, `DEL-20261111-02`; closes `DEL-20261027-06`). `top_contributors`: `POST /screener/run` (3,074 calls: 2,535 Alpaca data, 539 Yahoo; 13 failures), `POST /signals/generate` (3,035 Yahoo; 0 failures), `GET /earnings/{ticker}` (427 Yahoo; 373 failures). No call was made to `alpaca_paper`, `alpaca_trading`, `twelve_data` or `stooq` in the window. DS-36 reached production with v9.13 EPIC-05 (merged 2026-10-28), not on 2026-11-02 as planning assumed (see `api_performance_baseline.md` §53.2 window note), so this is a later week than the first full one, and all of it is after DS-36 shipped.

**Failures in this baseline.** All 665 failures are Yahoo calls, and 652 of them come from four on-demand features: `GET /earnings/{ticker}` (373 of 427), `GET /positions` (201 of 331), `GET /positions/{position_id}/gap-risk` (57 of 64) and `GET /research/{ticker}` (21 of 24). The nightly jobs fail rarely (screener 13 of 3,074; signal generation, stop update and alerts 0). This is the measured state, not an expected one. It is tracked by `BLG-OPS-217`. While it stands, §5's failure rule (more than 2× baseline) only fires at about 1,330 Yahoo failures a week.

**Causes (ST-15, `BLG-OPS-217`, v9.17, recorded 2026-11-13).** From a production `api_call_log` read for the 7 days to 2026-11-13, supplied by the user (Infrastructure & Operations Owner) in session (`DEL-20261113-01`; queries Q1–Q3 in that record), with a read-only staging read and a sandbox probe of the live calls. In that week the four features had 488 failed Yahoo calls. Yahoo calls that need its session token ("crumb": `getcrumb`, then `quoteSummary` and `v7/finance/quote`) failed almost every time, while calls that do not need it (`v8/finance/chart`: 3 failures in 3,569; `fundamentals-timeseries`: 0 in 60) did not. The time breakdown shows why: **418 of the 488 failures (86%) came in one two-minute burst on 2026-11-09 15:37–15:38** (471 calls), when a page fired one earnings lookup per row at about four Yahoo calls each, and Yahoo stopped issuing the token. Quiet page loads succeeded apart from the cookie request below.

| Feature | Cause | Share in the burst or a burst-like cluster | Fix (v9.17, ST-15) |
|---|---|---|---|
| `GET /earnings/{ticker}` | Page-load burst: one lookup per row, each a `Ticker.info` fetch needing the token | 344 of 366 in the 2026-11-09 burst | `Ticker.info` cached 12 h per symbol and at most 4 Yahoo lookups at once (`backend/utils/yahoo_info.py`); funds skip the calendar lookup |
| `GET /positions/{position_id}/gap-risk` | Each position's gap-risk request runs an earnings lookup, so a Positions page load is itself a burst | 29 of 30 in three clusters (09:29, 11:32, 15:37) | Same cache and cap (shares `get_earnings()`) |
| `GET /positions` | The per-position sector/industry lookup (`Ticker.info`) failing during bursts; on quiet loads the only failure was the cookie request | 44 of 71 in the burst; the cookie request was 6 more | Same cache and cap; the cookie request is no longer counted as a failure |
| `GET /research/{ticker}` | Three `Ticker.info` fetches per symbol (sector, market cap, earnings), all in the burst | 21 of 21 | One shared, cached fetch per symbol |

Two further findings, also fixed in ST-15: yfinance's cookie request to `fc.yahoo.com` is answered 404 while setting the cookie, and was counted as a failure every time (it now counts as a success); and on staging, UK positions stored without `.L` were priced as US tickers (`chart/BARC` 31 of 31 failed; production UK rows carry `.L`). A separate defect found while checking what the user sees, also fixed: the earnings lookup returned the last report date rather than the next one. While earnings lookups fail, the earnings badge and the gap-risk warning show nothing, the same as "no upcoming earnings"; that display gap is filed as `BLG-FE-294`. The post-fix production weekly report (ST-15 AC 2) and the re-recorded §4 failure column (AC 3) follow once the fix has run for 7 days in production, tracked by `BLG-OPS-217`.

**Measurement window:** the first full 7 days of production data after the deploy that ships DS-36. The volumes are filled in from `GET /ops/api-call-attribution?window=weekly` run on production at the end of that week, with the date and the report's `top_contributors` recorded here. That measurement is delegated to the Infrastructure & Operations Owner (needs production API access).

**Expected shape (estimate, not a baseline):** most calls come from the nightly screener run, which fetches each active ticker's bars once, from Alpaca for US and from Yahoo for UK, falling back to Yahoo for US. Next come the nightly stop update and position views (prices, ATR, FX and regime). News calls only happen when news is viewed.

## 5. Advisory Threshold

An advisory is raised when, for any source, the last 7 days exceed **2× the baseline**:

1. **Volume:** weekly calls to a source more than 2× its baseline calls per week, or combined weekly calls more than 2× the combined baseline.
2. **Cost:** combined weekly estimated cost more than 2× the baseline cost. While the baseline is $0.00, this means **any non-zero estimated cost**, which only happens if a unit cost in `UNIT_COST_USD` is set because a source has started charging.
3. **Failures:** the volume rule above, applied to failures. A sudden rise in failures usually means a provider is throttling or down, and the risk assessment's fail-open regime and frozen FX follow.

An advisory is a prompt to check the attribution report's `by_feature` breakdown for the feature that grew, not an automatic action.

**Automated check (ST-16, `BLG-OPS-195`, v9.17).** `.github/workflows/market-data-volume-check.yml` runs every Monday at 08:00 UTC. It runs `scripts/check_market_data_volume.py`, which calls `GET /ops/api-call-attribution?window=weekly` on production and compares the result with the §4 table. When any figure is more than 2× its baseline, it sends a Telegram message naming the source, the figure, the baseline and the source's top 3 features by calls. A failed report call, missing secrets or an unreadable §4 table fail the run and send a failure message, as `ai-daily-cost-check.yml` does; a failed call is never read as zero.

- **The §4 table is the only copy of the baseline.** The script reads it at run time, so re-recording §4 changes the check. Keep its layout: one row per source with the service name in backticks, and a **Combined** row. The script fails loudly if it cannot read them.
- **Exactly 2× is not an advisory**; the rule is "more than".
- **A zero baseline exceeds on any non-zero figure.** This applies to the $0.00 cost baseline (rule 2), to a source whose §4 calls or failures are 0 (for example one Alpaca data failure), and to a source not in §4 at all (`alpaca_trading`, `twelve_data`, `stooq`). Those are sources this baseline expects to be idle, so any use is worth a look.
- Per-source failures are compared per source; the combined row compares the sum across sources.

The threshold is reviewed when a baseline is first recorded, and whenever the active ticker universe grows by more than 25% (screener volume scales with it).

## 6. Sign-Off

- [x] Combined cost baseline across Alpaca, Yahoo Finance and the news API: $0.00 per week, with the basis for each source (§2)
- [x] Weekly call-volume baseline per source: recorded 2026-11-11 from one production weekly report (§4; ST-13, v9.16)
- [x] Advisory threshold defined: more than 2× baseline volume, cost or failures (§5)
- [x] Gate (`BLG-OPS-17`) verified at Release Planning 2026-10-16
- Prepared by: Sprint Execution Engine (ST-30)
- Date: 2026-10-27
