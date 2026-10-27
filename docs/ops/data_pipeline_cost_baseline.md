**Owner:** Infrastructure & Operations Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-10-27 (created; weekly call volumes pending the first full week of attribution data)
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
| Alpaca data (`alpaca_data`) | Pending | Pending | $0.00 |
| Alpaca news (`alpaca_news`) | Pending | Pending | $0.00 |
| Alpaca paper (`alpaca_paper`) | Pending | Pending | $0.00 |
| Yahoo Finance (`yahoo`) | Pending | Pending | $0.00 |
| **Combined** | **Pending** | **Pending** | **$0.00** |

**Measurement window:** the first full 7 days of production data after the deploy that ships DS-36. The volumes are filled in from `GET /ops/api-call-attribution?window=weekly` run on production at the end of that week, with the date and the report's `top_contributors` recorded here. That measurement is delegated to the Infrastructure & Operations Owner (needs production API access).

**Expected shape (estimate, not a baseline):** most calls come from the nightly screener run, which fetches each active ticker's bars once, from Alpaca for US and from Yahoo for UK, falling back to Yahoo for US. Next come the nightly stop update and position views (prices, ATR, FX and regime). News calls only happen when news is viewed.

## 5. Advisory Threshold

An advisory is raised when, for any source, the last 7 days exceed **2× the baseline**:

1. **Volume:** weekly calls to a source more than 2× its baseline calls per week, or combined weekly calls more than 2× the combined baseline.
2. **Cost:** combined weekly estimated cost more than 2× the baseline cost. While the baseline is $0.00, this means **any non-zero estimated cost**, which only happens if a unit cost in `UNIT_COST_USD` is set because a source has started charging.
3. **Failures:** the volume rule above, applied to failures. A sudden rise in failures usually means a provider is throttling or down, and the risk assessment's fail-open regime and frozen FX follow.

An advisory is a prompt to check the attribution report's `by_feature` breakdown for the feature that grew, not an automatic action. Until an automated check exists, compare at the monthly cost review. Automating it (a scheduled call to the report and a Telegram message over threshold, as `ai-daily-cost-check.yml` does for AI spend) is filed as `BLG-OPS-195`.

The threshold is reviewed when a baseline is first recorded, and whenever the active ticker universe grows by more than 25% (screener volume scales with it).

## 6. Sign-Off

- [x] Combined cost baseline across Alpaca, Yahoo Finance and the news API: $0.00 per week, with the basis for each source (§2)
- [ ] Weekly call-volume baseline per source: pending one week of production attribution data (§4, delegated)
- [x] Advisory threshold defined: more than 2× baseline volume, cost or failures (§5)
- [x] Gate (`BLG-OPS-17`) verified at Release Planning 2026-10-16
- Prepared by: Sprint Execution Engine (ST-30)
- Date: 2026-10-27
