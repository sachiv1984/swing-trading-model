**Owner:** API Contracts & Documentation Owner
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-07-29
**Cycle:** 2026-07-28__release-v7.10 (ST-12 — BLG-QA-128)

---

# Consumer-Driven Contract Check — First Run and Triage

## Purpose

ST-12 (BLG-QA-128): implement a lightweight, scripted check comparing frontend API call sites against the response fields documented in `docs/specs/api_contracts/*.md`, to catch drift between what the frontend actually depends on and what the contract says it can depend on.

## Implementation

`scripts/check_consumer_contract_drift.js` (Node, no new dependencies):

1. Parses `src/api/base44Client.js`'s central `api` object (the primary consumer surface — see Scope below) into `{category}.{method} -> HTTP path template` entries.
2. Parses every `## METHOD /path` heading in `docs/specs/api_contracts/*.md`, finds the first ` ```json ` block after a `### Response` sub-heading, and collects its top-level (+ one level of nested `data`) keys as "documented fields."
3. Scans `src/pages/**/*.js` and `src/components/**/*.js` for call sites, handling the two dominant consumption patterns in this codebase: direct `await` (with destructuring or later `.field` access) and `@tanstack/react-query`'s `useQuery({ queryFn: () => api.x.y(), select: ... })` (tracking the destructured alias, or the `select` transform's own parameter).
4. Diffs consumed fields against documented fields per endpoint and reports mismatches.

**Scope (deliberately bounded, per this story's "lightweight" qualifier):** only covers call sites through the central `api` object. Components that construct `fetch()` calls directly (`API_BASE_URL` usage bypassing `api.js`) are a separate, already-tracked concern — out of scope for this first pass.

## First run — results and triage

25 call sites analysed. Raw output: 11 OK, 12 field mismatches, 2 "no contract doc found." Every mismatch was individually triaged against the actual contract doc and/or handler code (not just re-reading the script's own characterization) — full findings below.

### Genuine gap found and fixed (1)

**`GET /portfolio`** — `src/pages/RiskDashboard.js` reads `portfolioData?.portfolio_heat_percent` and `portfolioData?.position_risks`, both genuinely returned by `services/portfolio_service.py::get_portfolio_summary()` (confirmed by reading the service code), but neither field appeared anywhere in `portfolio_endpoints.md`'s `GET /portfolio` section. **Fixed in this story**: both fields added to the JSON response example and field notes (`portfolio_endpoints.md` v2.5.0 → v2.5.1).

### False positives — script limitation, not real gaps (11)

The script only parses the first JSON example block after a `### Response` heading, and does not parse markdown field-reference tables. Several contract docs document additional fields either in a *second* example (an alternate response shape, e.g. an error branch or a gate-not-met branch) or in a field table below the example — both invisible to this first-pass script. Verified genuinely documented elsewhere, not real gaps:

- `POST /ai/daily-briefing` (`error` field) — documented in `ai_endpoints.md`'s field reference table (`| error | string or null | Error message when LLM unavailable |`), just not shown in the success-path JSON example the script parsed.
- `GET /portfolio/sector-regime-trend` (`weeks_available`) — documented in both a second JSON example (the "insufficient history" branch) and a field table in `portfolio_endpoints.md`.
- `GET /trade-plans/setup-quality-score` (`score`, `matching_trades`, `win_rate`, `average_pnl_pct`) — documented in both a second JSON example (the "gate met" branch) and a field table in `trade_plan_endpoints.md`.
- `GET /ai/spend-trend` (`total_cost_usd`) — script cross-contamination: `Settings.js` has two adjacent `useQuery` calls (`monthlyCostData` for `GET /ai/monthly-cost`, `spendTrendData` for `GET /ai/spend-trend`); the script's backward-search for the destructured alias attributed `monthlyCostData.total_cost_usd` (correct, real usage) to the wrong (`spendTrendData`) call site. `GET /ai/spend-trend`'s actual documented and consumed shape (`data[].version`, `data[].spend_usd`) is correct and matches.
- `GET /portfolio` via `src/components/dashboard/home/PortfolioHeatCard.js` (`portfolio`, `data`) and `GET /settings`/`GET /trades` via `src/pages/PerformanceAnalytics.js` (`data`) — both are defensive optional-chaining fallback patterns (`data?.portfolio ?? data?.data ?? data`) checking for multiple possible envelope shapes, not a hard dependency on an undocumented field.
- `src/pages/Reports.js` (`totalClosedTrades`, `gateCondition1Met`, etc., x2) — these are **locally-computed derived variables** (`const totalClosedTrades = tradesRes?.total_trades ?? 0;`), not fields read directly off the API response; the script's file-wide field-access window incorrectly attributed them to the API call site.
- `src/pages/StrategyBenchmark.js` (`detail`) — from a `.catch()` error-handling block reading `err.response?.data?.detail`, not the success-path response shape.
- `src/components/dashboard/home/RecentActivityCard.js` (`data`) — same envelope-fallback pattern as above.

### "No contract doc found" — script path-matching bug, not real gaps (2)

`api.analytics.metrics` (`analytics_endpoints.md` §GET /analytics/metrics) and `api.portfolio.redFlagJournal` (`red_flag_journal.md` §GET /portfolio/red-flag-journal, also cross-documented in `portfolio_endpoints.md`) are both genuinely documented — but for two different script bugs, not one: `redFlagJournal`'s path template contains an unresolved `${qs ? ...}` fragment (a query-string-bearing template literal the path extraction doesn't fully resolve); `analytics.metrics`'s failure is separate — `analytics_endpoints.md`'s JSON response example uses schema-placeholder syntax (e.g. `"summary": { ... }`) that fails strict `JSON.parse`, silently producing an empty documented-fields set for that endpoint. Both are script parsing limitations (see below), not real documentation gaps — neither was worth fixing for a first "lightweight" pass given every other mismatch this run turned out to already be a false positive or already fixed.

## Known limitations of the script (for future extension, not fixed this story)

- Does not parse markdown field-reference tables — only the first JSON example block per endpoint. This produced the majority of this run's false positives.
- Contract JSON examples using schema-placeholder syntax (e.g. `"summary": { ... }` instead of a concrete literal) fail strict `JSON.parse` and silently produce an empty documented-fields set for that endpoint (`analytics_endpoints.md`'s `GET /analytics/metrics` example hits this) — surfaces as a false "no contract doc found," not a true undocumented-field mismatch.
- Query-string-bearing path templates (e.g. `` `/portfolio/red-flag-journal${qs ? '?' + qs : ''}` ``) aren't fully resolved by the path-template extraction, also surfacing as a false "no contract doc found" for `api.portfolio.redFlagJournal` — a separate bug from the placeholder-JSON one above.
- Does not disambiguate between multiple `useQuery` calls with similarly-named nearby variables in the same file (spend-trend/monthly-cost cross-contamination).
- Does not distinguish locally-computed derived variables from direct API field access.
- Covers only the central `api` object, not direct `fetch()`/`API_BASE_URL` call sites.

None of these are blocking for this story's AC ("lightweight," "first run's findings triaged") — the triage above is the deliverable, and it found and fixed one genuine, real spec-debt gap.

## Sign-off

**API Contracts & Documentation Owner:** Confirmed — script implemented and run; all 14 raw findings triaged individually against actual contract/handler code; 1 genuine gap found and fixed (`GET /portfolio`); 13 confirmed false positives from documented script limitations. 2026-07-29.
