**Owner:** Infrastructure & Operations Owner
**Status:** Canonical
**Version:** 1.0.0
**Last Updated:** 2026-03-05

# Unavailability Policy — System Failure Modes and Manual Fallback Procedures

## Purpose

This document defines how the swing-trading system behaves when components are unavailable, what actions the user must take in each failure scenario, and how data integrity is preserved. It is the canonical reference for operational resilience.

---

## 1. System Component Overview

The swing-trading system has two independently deployable components:

| Component | Role | Failure impact |
|-----------|------|----------------|
| Backend API (`http://localhost:8000`) | All calculations, data persistence, live price fetching | Frontend renders error states |
| Frontend (Base44 app) | User interface only | Trade decisions made without tool |

The system has no redundant deployment. Single-instance, single-user design.

---

## 2. Failure Scenarios

---

### 2.1 Backend Down

**Symptom:** All frontend pages display API error states or fail to load data. HTTP requests to `localhost:8000` time out or return connection refused.

**System state:** Frontend is accessible but all data panels show error state. No reads or writes are possible.

**User required actions:**
1. Check the backend process (e.g. `uvicorn main:app --reload` or equivalent runner).
2. Check application logs for startup errors (missing environment variables, port conflict).
3. If `DATABASE_URL` is not set: set the environment variable and restart the backend.
4. Restart the backend. Confirm health at `GET /health` returns `{"status": "healthy"}`.
5. Do not attempt to trade using stale browser data — prices displayed before the outage are invalid.

**Manual fallback procedure:**
- All stop-loss levels and position sizing must be looked up in the brokerage platform directly.
- Use `strategy_rules.md` §Stop Loss and §Position Sizing formulas manually if an exit decision is required during the outage.
- Log any trades executed manually; enter them via the frontend once the backend is restored.

**Data integrity implications:**
- No data is lost during a backend-down event (database is unaffected).
- Trades executed manually during outage must be entered retroactively; holding_days and grace period status will be calculated correctly from the entry_date.
- If a position is exited manually without recording in the system, `GET /portfolio` will show the position as open until exit is recorded. Manually update after restoration.

---

### 2.2 Market Data Feed Unavailable

**Symptom:** `GET /positions`, `GET /portfolio`, and `GET /positions/analyze` return stale prices or fail with an error related to price fetching. Signals generation fails.

**System state:** Backend is running. Price refresh calls to the external market data provider fail. Cached or last-known prices may be returned, or price fields may be absent.

**User required actions:**
1. Confirm the market data provider API key is valid and not rate-limited.
2. Check backend logs for the specific error (timeout, 429, invalid API key).
3. If rate-limited: wait for the rate-limit window to reset (typically 1 minute for free tier providers).
4. If API key expired: renew key, update environment variable, restart backend.
5. Do not execute new positions based on stale prices — verify current prices via brokerage platform before acting.

**Manual fallback procedure:**
- All buy/sell decisions requiring current prices must use brokerage platform prices directly.
- Signal generation (`POST /signals/generate`) will fail or return incomplete results — do not rely on it during this state.
- Portfolio heat and drawdown calculations depend on live prices; treat displayed values as unreliable until prices are refreshed.

**Data integrity implications:**
- No data is written during price fetch failures (read-only failure mode).
- Stop-loss levels stored in the database are unaffected.
- Once the feed is restored, the next call to `GET /positions` will refresh all prices.

---

### 2.3 Partial Degradation — Single Service Unavailable

Partial degradation occurs when the backend starts but one service module fails (e.g., analytics service, portfolio service, signals service).

**Symptom:** Some pages work normally; others show error states. `GET /health/detailed` may show `degraded` status.

**System state:** Backend is running at reduced capability. Unaffected pages are fully operational.

**User required actions:**
1. Call `GET /health/detailed` to identify which components are degraded.
2. Call `POST /test/endpoints` to identify which specific endpoints are failing.
3. Check backend logs for the failing service module.
4. Common causes: database connection timeout for a specific query, external API failure scoped to one data type.
5. Restart the backend if the service module is stuck; otherwise investigate the specific endpoint failure.

**Manual fallback procedure:**
- Use functioning pages normally (e.g., if analytics is down but portfolio is working, continue monitoring positions).
- Do not use the signals page during signal service degradation.
- Record any decisions made during degradation in the trade journal once the service is restored.

**Data integrity implications:**
- Partial degradation does not affect data already in the database.
- Writes to the degraded service will fail with an error response — the frontend will display the error rather than silently dropping data.
- Analytics calculations depend on trade history records, which are persisted independently. Once analytics service is restored, metrics will reflect the full trade history.

---

## 3. General Data Integrity Principles

- **All trades and positions are persisted at write time.** Failures after a successful HTTP 200 response from the backend mean the data is safely stored.
- **Price data is ephemeral.** Current prices are fetched on demand; they are not stored as business data. Price staleness does not corrupt persistent records.
- **Analytics are computed on demand.** Metric values are never stored; they are recomputed from `trade_history` and `portfolio_history` on every call. An outage during an analytics call has no data integrity impact.
- **Cash transactions are transactional.** If a `POST /cash/transaction` call returns an error, the transaction was not recorded. Do not assume a partial write occurred.
- **Signal status updates are idempotent.** The `PATCH /signals/{signal_id}` endpoint may be safely retried if the initial call fails.

---

## 4. Recovery Checklist

After any availability event, confirm the following before resuming normal operations:

- [ ] `GET /health` returns `{"status": "healthy"}`
- [ ] `GET /portfolio` returns current positions with live prices
- [ ] `GET /positions/analyze` completes without error
- [ ] Any manually executed trades during the outage have been entered retroactively
- [ ] `POST /validate/calculations` passes (all 14 metrics: `total: 14, failed: 0`)

---

## Change Log

| Version | Date | Change |
|---------|------|--------|
| 1.0.0 | 2026-03-05 | Initial version. Covers backend down, market data feed unavailable, and partial degradation scenarios. Created for v1.8 sprint (ST-11, S2-09). |
