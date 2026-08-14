**Owner:** Head of Engineering
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-08-14
**Cycle:** 2026-08-14__release-v8.8 (ST-12 — BLG-BE-94)

---

# Pre-Trade Research View — Query-Latency Budget Review

## Purpose

`BLG-BE-94`: the Pre-Trade Research View (`GET /research/{ticker}`, PT-02, shipped v3.2) has not had a latency review since ship — "over a year of data growth and added panels (Alpaca news, drift streak metric) may have shifted its query budget." This review confirms current query latency for the endpoint's data sources and fixes or files any regression found.

## Method

1. Enumerated every data source `get_research()` (`backend/routers/research.py`) reads, cross-referenced against `docs/specs/data_provenance/research_view_provenance.md` (the canonical field-level source list) to confirm no source has silently changed since that document's v1.0 baseline.
2. For each source, read the actual call chain down to its database query (if any) or external API call, checking specifically for query shape changes that would scale with table/data growth (unbounded scans, missing `LIMIT`, missing index usage) — the class of regression the backlog item's "data growth" framing points at.
3. Cross-checked the existing `docs/ops/api_performance_baseline.md` §11/§18 entries for this endpoint's last real staging measurement (v3.1: p50=3,313ms, p95=4,601ms, gated at BLG-OPS-22/BLG-BE-15, closed by the 15-minute per-ticker TTL cache already in `research.py`).

## Data Source Inventory (cross-checked against provenance doc — unchanged)

| Source | Call | Type | Scales with growth? |
|---|---|---|---|
| Portfolio | `get_portfolio()` | DB, single row | No |
| Price + change % | `_get_price_data()` | External (Yahoo chart API) | No (external-latency-dominated) |
| Signal | `_get_signal()` → `get_signals()` (was) | DB | **Yes — see Finding 1** |
| Regime | `_get_regime()` → `check_market_regime()` | External, 5-min cache (BLG-BE-25, consolidated ST-07 this cycle) | No |
| Sector/Industry | `_get_sector()` → `get_sector_and_industry()` | External (yfinance) | No |
| Screener | `_get_screener()` → `get_screener_results(limit=500)` | DB, bounded | No — see Observation below |
| Earnings | `_get_earnings()` | External (yfinance) | No |
| Market cap | `_get_market_cap()` | External (yfinance) | No |
| News headlines | `_get_news()` | External (Alpaca/fallback) | No |

"Drift streak metric" referenced in the backlog item's problem statement does not appear in `get_research()`'s response shape, `research_view.md` (frontend page spec), or the provenance doc — not part of this endpoint. Not in scope for this review (nothing to check).

## Finding 1 (Fixed) — Unbounded per-ticker signal lookup

`_get_signal()` called `services.signal_service.get_signals()` — no ticker filter, no `LIMIT` — which runs `SELECT * FROM signals WHERE portfolio_id = %s ORDER BY signal_date DESC, rank ASC` (`database.py::get_signals()`, no ticker/date-range restriction) and returns **every signal ever generated for the portfolio across every screener run since ship**. `_get_signal()` then filtered this entire result set down to one ticker in Python. Unlike every other source in the table above, this one has no bound at all — its cost grows linearly with total signal history, which is exactly the "over a year of data growth" risk the backlog item names.

**Fix:** added `database.get_signals_for_ticker(portfolio_id, ticker)` (`WHERE portfolio_id = %s AND UPPER(ticker) = UPPER(%s)`) and `services.signal_service.get_signals_for_ticker(ticker)`; `routers/research.py::_get_signal()` now calls the targeted lookup. Selection tie-break logic (most-recent-date, `new`-status preference) is unchanged — same row selected. Commit: this story's own `[EPIC-02][ST-12]` commit. New tests: `tests/test_research_signal_lookup.py`.

**Correction (Head-of-Engineering review, agent-mediated §5.3, same day):** this review's first pass claimed the new query "uses the existing `idx_signals_ticker` and `idx_signals_portfolio` indexes." That was wrong — `idx_signals_ticker` is a plain btree index on the bare `ticker` column; it cannot serve a predicate that wraps the column in `UPPER()`, the same class of gap already documented for `trade_plans`/`red_flag_events` (ST-10, BLG-BE-82, EPIC-03, v8.4). Without a matching functional index, the fix's I/O reduction (fetching/formatting only the matched rows instead of the whole table) was real, but the database engine itself still had to scan rather than index-seek on the `UPPER(ticker)` predicate — not the fully closed gap originally claimed. **Corrected:** added `idx_signals_ticker_upper` (`database.ensure_signals_ticker_upper_index()`, registered at startup; `docs/specs/data_model.md` DS-14, v2.27→v2.28). The query now has a genuine index path for both the portfolio and ticker predicates.

## Observation (Not filed) — Screener lookup is bounded, not a regression

`_get_screener()` calls `get_screener_results(limit=500)` then filters to one ticker in Python — same shape as Finding 1, but explicitly bounded at 500 rows regardless of how large the ticker universe or screener-run history grows. This is a pre-existing, deliberate bound (not something that has "shifted" with a year of data growth — it was already capped at ship) and its worst case is fixed, small. Not a regression; not filed as a backlog item. If the ticker universe itself grows well past 500 in the future such that relevant results are ever excluded by the cap, that would be a correctness question for a different story, not a latency one.

## Conclusion

One genuine, growth-driven query-latency regression found and fixed (Finding 1). No other source in the inventory has a query shape that scales with data growth beyond what was already true at ship. The endpoint's overall external-latency-dominated profile (7 of 9 sources are external API calls) and its existing 15-minute cache (BLG-BE-15/BLG-OPS-22) remain the primary latency-budget levers — unaffected by this review, no changes needed there.

**Sign-off:**
- Head of Engineering: Blocked (first pass) — 2026-08-14 (agent-mediated, §5.3). Data-source inventory and behavior-preservation checks passed; blocked on Finding 1's index-usage claim being factually incorrect (see Correction above) — required either the functional index or a corrected/filed characterization before the story's AC ("any regression fixed or filed") was satisfied.
- Head of Engineering: Accepted (retry 1) — 2026-08-14 (agent-mediated, §5.3). `idx_signals_ticker_upper` added and Finding 1 corrected as above; re-verified the query now has an index path for both predicates, matching the accepted `trade_plans`/`red_flag_events` precedent exactly. No further action required this cycle.
