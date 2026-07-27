Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-27

# Sprint Execution Escalations — 2026-07-24__release-v7.8

## ESC-EXEC-20260727-01

- **Raised at:** 2026-07-27T01:15:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-07-24__release-v7.8
- **Step:** STEP 3.1.D (delegated_decision handling), EPIC-11
- **ST/EPIC item:** ST-11 (EPIC-11) — Add pilot contract tests for 3 highest-traffic endpoints
- **Trigger type:** Human-Delegation
- **Blocking statement:** ST-11 is classified `delegated_decision` per RISK-03 (sprint_backlog.md, sprint_planning_notes.md): the 3 pilot endpoints for the contract-test pilot have no telemetry-backed ranking on record. Candidates named at sprint planning are positions, trades, and dashboard, but no Head of Engineering design session or equivalent artefact exists confirming this specific selection — sprint_planning_notes.md explicitly flagged this as an open item requiring Head of Engineering confirmation before implementation begins (not before sprint seal). The engine cannot resolve this itself: selecting pilot endpoints based on traffic/priority judgement is exactly the kind of scope-ambiguity decision that must be escalated rather than assumed, per execution_prompt.md's ambiguity definition (§13) and the delegated_decision classification rule.
- **Owning authority:** Head of Engineering
- **Unblock criteria:** Head of Engineering confirms the 3 pilot endpoints (from the named candidates — positions, trades, dashboard — or an alternative set) for the ST-11 contract-test pilot. Once confirmed, re-classify ST-11 to `autonomous` (or `delegated_backend` if implementation requires domain judgement beyond contract-test authoring) and resume STEP 3 execution for EPIC-11.
- **SLA due-by:** 2026-07-30T01:15:00Z (72 hours — no lifecycle/strategy/quality trigger type applies; treated as a workforce/technical-scope decision per shared_standards.md §4's SLA table, "Workforce / Capacity" row)
- **Blocks execution:** No — per execution_prompt.md §3.1.D, the engine continues to the next ST item rather than stalling the sprint on one delegated_decision item. This was the final unresolved EPIC in merge order; no further EPICs remain to continue to in this invocation.
- **Disposition:** Resolved
- **Resolution summary:** Confirmed via §5.3 agent-mediated Head of Engineering review, 2026-07-27. **Pilot endpoints: `GET /positions`, `GET /trades`, `GET /portfolio`.** Investigated the 3 named candidates (positions, trades, dashboard) against actual call-site evidence in lieu of telemetry (none exists in this app):
  - `GET /positions` (`backend/main.py`) — 6 frontend call sites (`api.positions.list()`: `Reports.js`, `CommandPalette.js`, `OpenPositionsCard.js`, `GracePeriodCard.js`, `morning/ExitZoneCard.js`, `morning/EarningsAlertCard.js`). Highest call-site count in the app — confirmed as pilot endpoint #1.
  - `GET /trades` (`backend/main.py`) — 5 frontend call sites (`api.trades.list()`: `PerformanceAnalytics.js`, `Reports.js`, `TradeHistory.js`, `Positions.js`, `RecentActivityCard.js`). Second-highest call-site count — confirmed as pilot endpoint #2.
  - **"dashboard" candidate — resolved to `GET /portfolio`, not a literal endpoint.** `DashboardHome.js` is a composition of ~12 independent queries (`DASHBOARD_QUERY_KEYS`) across many different backend endpoints — there is no single `GET /dashboard` route. Critically, 2 of those 12 dashboard queries (`home-open-positions` → `api.positions.list()`, `home-recent-activity` → `api.trades.list()`) already resolve to the exact same `GET /positions`/`GET /trades` endpoints as pilot candidates #1/#2 — so picking "dashboard" naively would have double-counted coverage rather than adding a genuinely independent third contract. Of the dashboard's remaining distinct queries, `GET /portfolio` (`PortfolioHeatCard.js` via `api.portfolio.get()`) is the one that is (a) dashboard-specific and not already covered by #1/#2, (b) fired unconditionally on every dashboard/session landing (same "loads every session" traffic profile as the other two), and (c) higher-risk than a plain DB list — its handler (`get_portfolio_summary()`, `backend/main.py` `@app.get("/portfolio")`) computes "portfolio with live prices" per open position, so a contract regression here is more failure-prone across releases (e.g. touched by any pricing/rebalance change) than a static list endpoint. Selected as pilot endpoint #3.
  - **Reclassification:** ST-11 reclassified from `delegated_decision` to `autonomous` — the remaining work (authoring 3 request/response contract tests against already-resolved endpoints, following the existing `tests/test_api_contracts.py` pattern) requires no further domain judgement beyond ordinary contract-test authoring.
  - **Evidence:** call-site greps performed 2026-07-27 against `src/` (see session record); `backend/main.py` lines 449 (`GET /positions`), 466 (`GET /portfolio`), 701 (`GET /trades`); `src/pages/DashboardHome.js` `DASHBOARD_QUERY_KEYS` composition confirmed via direct read.
