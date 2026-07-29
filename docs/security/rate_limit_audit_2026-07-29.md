**Owner:** Cybersecurity & Trust Lead
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-07-29
**Cycle:** 2026-07-28__release-v7.10 (ST-07 — BLG-SEC-18)

---

# Rate-Limiting Posture Audit — Render Platform-Level and Application-Level (Refresh)

## Purpose

ST-07 (BLG-SEC-18) audits current rate-limiting posture — both Render platform-level and application-level — against all public-facing endpoints, ahead of any future authentication model change. A comprehensive application-level audit already exists (`docs/security/rate_limit_audit_2026-07-26.md`, ST-08/BLG-SEC-21, v7.8) covering all endpoints as of 2026-07-26; this story (a) refreshes that audit against endpoints added since, and (b) adds the Render platform-level analysis the prior audit's scope did not cover.

## Part 1 — Refresh of the 2026-07-26 application-level audit

**Endpoint count check:** `grep -c '@router\.\(get\|post\|put\|delete\|patch\)('` across `backend/routers/*.py` (23 files, excluding `test.py`) now returns 85 (was 82); `backend/main.py` unchanged at 46. New total: 131 (was 128).

**Correction (found during Cybersecurity & Trust Lead sign-off review):** the first draft of this audit misidentified `GET /reports/monthly-pnl` as new — it was actually added 2026-04-30, well before the 2026-07-26 baseline, and was already counted in the original 128. The genuinely new, previously-unaudited endpoint accounting for the 82→85 router-file growth is `GET /ai/spend-trend` (`routers/ai.py`, added 2026-07-26 in the v7.9 cycle, after the prior audit was written). Corrected list below.

**3 new endpoints since 2026-07-26**, all shipped in the intervening v7.9 cycle (2026-07-27__release-v7.9):
- `GET /portfolio/sector-regime-trend` (`portfolio_risk.py`) — pure DB read (`sector_regime_history` table), no external API call.
- `GET /ai/spend-trend` (`ai.py`) — pure DB read via `services.ai_spend_trend_service` (queries `claude_audit_log`), no external API call. Note: despite living in the AI router, this endpoint itself does not call Claude — it reports on *past* Claude spend already recorded by other, separately-rate-limited endpoints (`journal-summary`, `daily-briefing`, `chat`) — so it is not a duplicate cost-amplification surface.
- `GET /changelog/latest` (`changelog.py`) — reads a local file (`changelog.md`), no DB, no external API call.

All 3 are gated by the existing global `X-API-Key` middleware (`backend/main.py::api_key_middleware`) with no exemption (the only exemptions are `OPTIONS` requests and `GET /health`), and none calls a metered external API (Alpaca, Yahoo Finance, Claude, Telegram, News API). Per the prior audit's bucket taxonomy, all 3 fall into **Bucket C3 — authenticated, no external API call, accepted risk (key-compromise threat model)** — the same disposition as the other 116/128 previously-audited endpoints in that bucket. **No new P0/P1 gap found in this refresh.** Buckets A/B/C1/C2 from the 2026-07-26 audit are unchanged (no new AI/metered-API-calling endpoint was added).

## Part 2 — Render platform-level posture (new scope, not covered by the 2026-07-26 audit)

The 2026-07-26 audit's method section explicitly scoped to application-level checks only (app-level rate-limiter usage, `X-API-Key` middleware coverage, external-API-call classification). This story's acceptance criteria additionally names "Render platform-level" posture.

**What is verifiable from this repository:** `render.yaml` provisions the staging API as a Render Web Service on the **free plan**, with `startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT` — no platform-level rate-limiting configuration is declared anywhere in this repo (Render does not expose a declarative rate-limit config in `render.yaml`; any platform-level throttling is Render's own edge/infrastructure behaviour, not something this codebase configures or can override).

**What is not verifiable from a static repo checkout (requires live Render dashboard/support access):** Render's specific edge-level DDoS/abuse-protection thresholds, and whether the free-tier plan's connection/request ceilings differ from paid tiers. This audit does not fabricate specifics that cannot be confirmed without production access.

**Directly relevant cross-reference (BLG-SEC-24, filed during ST-06 this same cycle):** the application-level per-IP limiters (`_ai_limiter`, `services/rate_limiter.py`) key on `request.client.host`, and `render.yaml`'s uvicorn command has no `--proxy-headers` flag — meaning `request.client.host` may reflect Render's own proxy connection rather than the true client IP in production. This is the single most consequential finding for this story's "Render platform-level and application-level" framing: if confirmed, it means the platform-level proxy layer and the application-level limiter interact in a way that defeats the latter's per-IP intent entirely (collapsing to one shared bucket), independent of whatever Render's own edge-level protections may or may not provide. This is not re-filed here — `BLG-SEC-24` already covers it and names the exact remediation (verify live, configure `--proxy-headers`/`--forwarded-allow-ips` if confirmed).

## Disposition

- Part 1 (application-level refresh): no new P0/P1 gap. 3 new endpoints since 2026-07-26 confirmed to fall into the existing accepted-risk bucket (C3).
- Part 2 (Render platform-level): no platform-level rate-limit configuration exists in this repo to audit directly; the one confirmed, actionable cross-cutting risk (proxy-header/`request.client.host` reliability) is already filed as `BLG-SEC-24` (P1) — not duplicated here.
- No new backlog item filed by this story specifically; `BLG-SEC-24` (filed under ST-06) is the operative follow-up for both stories' overlapping finding.

## Sign-off

**Cybersecurity & Trust Lead:** Confirmed — application-level audit refreshed against all 131 current endpoints (3 new since 2026-07-26, no new gap); Render platform-level posture documented to the extent verifiable from this repository, with the one cross-cutting actionable risk correctly cross-referenced to `BLG-SEC-24` rather than duplicated. 2026-07-29.
