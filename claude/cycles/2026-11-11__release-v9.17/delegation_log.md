Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-13

# Delegation Log — 2026-11-11__release-v9.17

## DEL-20261113-01

- **ST Item:** ST-15 — Find out why most on-demand Yahoo calls fail on production (earnings, positions, gap risk, research)
- **EPIC:** EPIC-06
- **Classification:** delegated_backend (production `api_call_log` read, Human-Delegation — `sprint_backlog.md` ST-15 Notes and Staging-only ACs, RISK-03; LL-v8.0-P3-01 infra/ops pattern). AC 1 needs this read in-sprint. AC 2 and AC 3 are seal-marked `post-merge` and tracked by `BLG-OPS-217`.
- **Assigned to:** Infrastructure & Operations Owner (production read); Head of Engineering (code fixes, engine-implemented)
- **GitHub Issue:** #2250
- **Branch:** exec/2026-11-11__release-v9.17/EPIC-06
- **Delegated at:** 2026-11-13T13:06:31Z
- **What is needed:** The sandbox `DATABASE_URL` is staging, and the engine has no production database access. `api_call_log` (DS-36) stores `service`, `endpoint` (the provider URL path, without the query string), `feature`, `success` and `called_at`. A failure is an exception or an HTTP status of 400 or more; the status code itself is not stored. Run these read-only queries on **production** and paste the output, or grant the engine a one-off read:

  ```sql
  -- Q1: failures by feature and provider path family (ticker removed from the path)
  SELECT feature,
         regexp_replace(endpoint, '/(chart|quoteSummary|timeseries)/[^/]+$', '/\1/{symbol}') AS path,
         COUNT(*) AS calls,
         COUNT(*) FILTER (WHERE NOT success) AS failures
  FROM api_call_log
  WHERE service = 'yahoo'
    AND called_at >= now() - interval '7 days'
    AND feature IN ('GET /earnings/{ticker}', 'GET /positions',
                    'GET /positions/{position_id}/gap-risk', 'GET /research/{ticker}',
                    'POST /screener/run', 'POST /signals/generate')
  GROUP BY 1, 2
  ORDER BY 1, failures DESC;

  -- Q2: failing symbols, for the paths that carry one
  SELECT feature, endpoint, COUNT(*) AS calls, COUNT(*) FILTER (WHERE NOT success) AS failures
  FROM api_call_log
  WHERE service = 'yahoo' AND called_at >= now() - interval '7 days'
    AND feature IN ('GET /earnings/{ticker}', 'GET /positions',
                    'GET /positions/{position_id}/gap-risk', 'GET /research/{ticker}')
  GROUP BY 1, 2
  HAVING COUNT(*) FILTER (WHERE NOT success) > 0
  ORDER BY failures DESC
  LIMIT 60;

  -- Q3: are failures bursty (throttling) or steady (a broken call)? Calls and failures per minute.
  SELECT date_trunc('minute', called_at) AS minute, feature, COUNT(*) AS calls,
         COUNT(*) FILTER (WHERE NOT success) AS failures
  FROM api_call_log
  WHERE service = 'yahoo' AND called_at >= now() - interval '7 days'
    AND feature IN ('GET /earnings/{ticker}', 'GET /positions',
                    'GET /positions/{position_id}/gap-risk', 'GET /research/{ticker}')
  GROUP BY 1, 2
  HAVING COUNT(*) FILTER (WHERE NOT success) > 0
  ORDER BY failures DESC
  LIMIT 30;
  ```

  Q1 includes the two nightly features, which call the same Yahoo paths and rarely fail, as a control. Q2's symbols separate ETFs, `.L` tickers and delisted symbols from a general fault. In Q3, failures that cluster in a few minutes point to throttling of page-load bursts; a steady rate points to a call that always fails.
- **What the engine has found so far (sandbox, 2026-11-13, public Yahoo endpoints, no database):** the four features take three different HTTP paths. `GET /earnings/{ticker}` and `GET /research/{ticker}` use yfinance `Ticker.info` (curl_cffi): `getcrumb`, then `quoteSummary`, `v7/finance/quote` and `fundamentals-timeseries`. `GET /positions` UK prices use plain `requests` to `v8/finance/chart/<symbol>` (`utils/pricing.py`). Gap risk uses yfinance `history()` (`v8/finance/chart`). From this sandbox's IP every call returned 200, except `quoteSummary` for an ETF (SPY), which returns **404 "No fundamentals data found"** twice per earnings lookup and is recorded as two provider failures. yfinance's cookie step requests `https://fc.yahoo.com` (`yfinance/data.py` `_get_cookie_basic`), which answers **404 while setting the `A3` cookie** (checked 2026-11-13 with both curl_cffi and requests); every cookie bootstrap is therefore recorded as a failure under path `/`, although it worked. In this sandbox yfinance reused a cached cookie, so the request did not appear in the probe. Neither explains 87% on its own, so the production path breakdown is needed.
- **Workflow viability (LL-v9.10-P3-01):** Not a workflow dispatch. A production database read only.
- **Spec reference:** `docs/ops/data_pipeline_cost_baseline.md` §4 (failures paragraph); `docs/specs/api_contracts/ops_endpoints.md#GET /ops/api-call-attribution` (failure definition); `stage4_backlog_slice.md#ST-15`
- **Unblock criteria:** Q1–Q3 output for production (or "no rows"), supplied in session or in this record. The engine then records a cause per feature (AC 1), fixes what is broken or documents expected failures, and commits on the EPIC-06 branch.
- **Commit format required:** `[EPIC-06][ST-15] <description>` on `exec/2026-11-11__release-v9.17/EPIC-06` (engine commits)
- **Result (supplied in session by the user, Infrastructure & Operations Owner, 2026-11-13):** production Q1–Q3 output. Q1: calls needing Yahoo's crumb failed almost every time (`getcrumb` 105/111, `quoteSummary` 250/268, `v7/finance/quote` 136/154), calls not needing it did not (`v8/finance/chart` 3/3,569, `fundamentals-timeseries` 0/60). Q2: failures spread over about 55 US and UK symbols, all with `.L` where UK; none are funds or delisted. Q3: 418 of the four features' 488 failures (86%) came in one burst, 2026-11-09 15:37–15:38 (471 calls); gap risk's came in three clusters; quiet Positions loads failed only on the cookie request. Cause per feature recorded in `docs/ops/data_pipeline_cost_baseline.md` §4 (v1.3). Fixes: `5cc4e8bd` (UK symbol, cookie 404, next earnings date, fund calendar skip) and `c313bc90` (shared 12 h `Ticker.info` cache, 4-lookup cap). Follow-up filed: `BLG-FE-294`.
- **Sign-off:** sign_off_cleared — production data supplied by the Infrastructure & Operations Owner in session, 2026-11-13.
- **Commit SHA:** c313bc900bf3093198fe3d39864ddc7d3e99ccf8
- **Status:** Unblocked (2026-11-13T13:41:30Z) — Unblocked in-session — production api_call_log Q1–Q3 output, supplied by the user (Infrastructure & Operations Owner), same session as delegation.
