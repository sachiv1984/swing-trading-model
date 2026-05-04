**Owner:** PMO Lead
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-04-30
**Cycle:** 2026-04-29__release-v3.1 (ST-12)

---

# External API Dependency Register

## Purpose

This register documents all external API dependencies of the Momentum Trading Assistant, their known failure modes, mitigations, and monitoring approach. It is used for incident management, risk review, and onboarding.

---

## Dependencies

### 1. Alpaca Markets API

| Field | Value |
|-------|-------|
| Service | Alpaca Markets |
| Type | Brokerage & market data API |
| Usage | Live price fetching (positions P&L update), bar data (ATR calculation), paper/live order management |
| Endpoint(s) | `https://paper-api.alpaca.markets` (paper) or `https://api.alpaca.markets` (live) |
| Auth | API key + secret (see `external_api_credential_inventory.md`) |
| SLA/uptime | Alpaca publishes a status page; no formal SLA for paper trading tier |

#### Known Failure Modes

| ID | Mode | Description | Introduced |
|----|------|-------------|------------|
| AFM-01 | Null bars crash | When Alpaca returns `null` for a bars response (e.g. non-trading hours, halted ticker, or paper account with no data), the system previously raised an unhandled `AttributeError` or `NoneType` error in the price-fetching layer. | v3.0 incident |
| AFM-02 | Hyphenated ticker handling | Alpaca uses hyphens in some ticker symbols (e.g. `BRK-B`). If the system sends a dot-format or un-normalised ticker to Alpaca, the request fails silently or returns empty data. | v3.0 identified |
| AFM-03 | Rate limiting | Alpaca enforces rate limits on the data API. Bulk operations (e.g. screener enrichment) can exhaust rate limits if not throttled. | Operational observation |

#### Mitigations in Place

| ID | Mode Addressed | Mitigation |
|----|---------------|------------|
| MIT-01 | AFM-01 | `get_current_price` in `utils/pricing.py` wraps Alpaca bar responses with null-guards. If bars is null or empty, returns a fallback price of 0.0 and logs a warning rather than raising. Deployed v3.0 hotfix. |
| MIT-02 | AFM-02 | Ticker normalisation applied at the screener ingestion layer — hyphenated tickers are converted before external API calls. |
| MIT-03 | AFM-03 | Screener batch service uses sequential processing with per-request delays. Bulk enrichment is rate-limited at the service layer. |

#### Monitoring Approach

- `GET /health/detailed` checks Alpaca connectivity and records last successful price fetch
- `GET /health` returns degraded state if Alpaca is unreachable
- Render logs capture all Alpaca API errors with ticker and response body
- Alert: if more than 3 consecutive position price-fetch failures occur, the positions page will display stale-price warnings (controlled by `last_updated` timestamp)

---

### 2. News API

| Field | Value |
|-------|-------|
| Service | News API (newsapi.org or equivalent) |
| Type | Financial news aggregation API |
| Usage | Fetching ticker-specific news for `GET /news/{ticker}` |
| Auth | API key (see `external_api_credential_inventory.md`) |
| SLA/uptime | No formal SLA; free tier enforces 100 requests/day cap |

#### Known Failure Modes

| ID | Mode | Description | Introduced |
|----|------|-------------|------------|
| NFM-01 | Rate limit exhaustion | Free tier cap of 100 requests/day. Under active use, limit can be reached during the trading day. | Operational observation |
| NFM-02 | Ticker with no news | Some tickers return no articles; API returns empty `articles` array rather than an error. | Operational observation |
| NFM-03 | API key expiry / plan downgrade | If the news API key is revoked or the account plan is downgraded, all news requests return 401. | Operational risk |

#### Mitigations in Place

| ID | Mode Addressed | Mitigation |
|----|---------------|------------|
| MIT-04 | NFM-01 | `GET /news/{ticker}` endpoint handles 429 gracefully — returns empty array with a `source_note` field explaining rate limit. Frontend displays "News temporarily unavailable" rather than an error state. |
| MIT-05 | NFM-02 | Empty `articles` array is handled by the frontend — shows "No recent news" state rather than a spinner or error. |
| MIT-06 | NFM-03 | Credential inventory tracks key status. Rotation policy in `external_api_credential_inventory.md` covers provider key renewal. |

#### Monitoring Approach

- News API failures are logged at WARNING level in Render logs
- The `/health/detailed` endpoint does not currently probe the news API (non-critical path)
- Manual monitoring: check Render logs if users report missing news

---

## Register Maintenance

This register must be updated when:
- A new external API dependency is added to the system
- A new failure mode is identified (e.g. during an incident postmortem)
- A mitigation is deployed or removed
- A dependency is decommissioned

Commit updates with: `[GOVERNANCE] Update external API dependency register — <reason>`

---

## Acceptance

- Accepted by: PMO Lead
- Date: 2026-04-30
