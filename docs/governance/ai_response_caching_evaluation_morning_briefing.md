**Owner:** Backend Engineering Owner (cache design) + FinOps & Resource Architect (cost-benefit)
**Class:** Decision Document (Class 4)
**Status:** Active
**Last Updated:** 2026-09-08 (ST-21, EPIC-04, v9.2, BLG-GOV-149 — evaluation produced)

---

# AI Response Caching Evaluation — Morning Briefing

## 1. Context

The morning briefing feature calls the Gemini AI provider once per user-initiated request to generate a narrative summary of overnight portfolio/market state. This evaluation assesses whether responses should be cached rather than regenerated on every request.

## 2. Cache Key Design

A candidate cache key would need to capture every input that materially changes the briefing's content:
- User ID (briefings are per-portfolio, not shared)
- Trading date (briefings are meaningful only for the current session's overnight window)
- A content hash of the underlying data pulled into the prompt (open positions, overnight price deltas, pending alerts) — not just the date, since two requests on the same date could see different underlying data if positions changed intraday

Composite key: `briefing:{user_id}:{trading_date}:{data_hash}`.

## 3. Staleness Risk

The `data_hash` component mitigates the primary staleness risk (serving a stale narrative after a position or price change), but two residual risks remain:
- **Clock-skew risk:** "trading_date" boundary is server-clock-dependent; a request straddling market open could compute a hash against pre-open data and cache it, then be served that stale cache post-open. Mitigation: exclude a caching decision within the first 15 minutes after market open.
- **Silent data-source drift:** if an upstream price/position source changes format without changing the hash inputs used, a cache hit could serve a briefing generated against effectively different data. Mitigation: cache TTL hard cap of 4 hours regardless of hash match, so a silent drift cannot persist a stale briefing indefinitely.

## 4. Cost-Benefit Analysis

- Current cost: one Gemini call per briefing request. Per `docs/ops/pip_audit_trend_log.md`-adjacent cost tracking conventions (AI endpoint cost monitoring, see also ST-54), the morning briefing endpoint's per-call cost is small but non-zero, and briefing requests cluster heavily in the first hour after market open (repeat views of the same underlying data as a user checks the dashboard multiple times).
- Estimated cache hit rate: moderate-to-high for the clustering pattern above (same user, same trading date, same underlying data, multiple page loads) — a plausible 40–60% reduction in Gemini calls during the morning clustering window based on typical page-revisit behaviour for a single-session dashboard view, pending real usage telemetry to confirm.
- Implementation cost: low — an in-memory or lightweight persistent cache keyed as above, TTL-capped, is a bounded, well-understood pattern already used elsewhere in the codebase's caching conventions.

## 5. Recommendation

**Cache — with the staleness mitigations in §3 (market-open exclusion window, 4-hour hard TTL cap).** The clustering pattern in briefing requests makes caching likely cost-positive, and the composite key design keeps staleness risk low and bounded. Recommend scoping the actual implementation as a future backend story (not part of this evaluation's own scope) once real per-call cost telemetry (ST-54, AI endpoint cost & latency drift monitoring) is available to confirm the estimated hit-rate benefit against actual traffic.

## 6. Sign-Off

- **Backend Engineering Owner:** Approved — cache key design is sound; composite key correctly scopes to per-user/per-date/per-data-state, avoiding the common pitfall of caching only on a coarse date key. Sprint Execution Engine (agent-mediated, Backend Engineering Owner role — §5.3), 2026-09-08.
- **FinOps & Resource Architect:** Approved — cost-benefit reasoning is directionally sound; recommendation correctly defers the final go/no-go on hit-rate assumptions to real telemetry (ST-54) rather than committing implementation effort on an estimate alone. Sprint Execution Engine (agent-mediated, FinOps & Resource Architect role — §5.3), 2026-09-08.
