**Owner:** Cybersecurity & Trust Lead
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-07-31
**Cycle:** 2026-07-28__release-v7.10 (ST-07 — BLG-SEC-18); 2026-07-30__release-v8.0 (ST-08 — BLG-SEC-24 resolution)

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

## Part 3 — BLG-SEC-24 live verification result (ST-08, EPIC-02, v8.0)

Part 2 above (2026-07-29) flagged as unverified whether `request.client.host` reflects the true client IP behind Render's proxy, or collapses all callers to Render's own edge IP (which would defeat per-IP rate limiting entirely). This was resolved via a live production test, automated via a two-job GitHub Actions `workflow_dispatch` (`.github/workflows/st08-proxy-ip-verification.yml`), run `30611215629`:

- **Job A** (runner public IP `135.232.227.144`) burst `GET /health` and was rate-limited on attempt 61 — consistent with the documented 60/min limit (`backend/main.py:1097`), confirming the limiter itself works correctly for a single real client.
- **Job B** (a separate GitHub-hosted runner, genuinely different public IP `172.182.243.52`) made a single probe request immediately after Job A's block and received `HTTP 200` — **not** rate-limited.

**Result: no proxy-IP collapse.** `request.client.host` correctly distinguishes real per-client IPs in production; two genuinely distinct clients get genuinely independent rate-limit buckets. No `uvicorn --proxy-headers`/`--forwarded-allow-ips` configuration change is needed — the theoretical risk named in Part 2 and filed as `BLG-SEC-24` did not materialize in practice, most likely because Render's edge for this service type passes through the real peer connection rather than terminating and re-proxying it internally in a way that would substitute its own address as `request.client.host`.

`BLG-SEC-24` is resolved as **no code change required**; the finding above (confirmed-correct behavior, with reproducible run evidence) is the closing action per the story's acceptance criteria ("confirmed accurate, no change needed" outcome).

## Disposition

- Part 1 (application-level refresh): no new P0/P1 gap. 3 new endpoints since 2026-07-26 confirmed to fall into the existing accepted-risk bucket (C3).
- Part 2 (Render platform-level): no platform-level rate-limit configuration exists in this repo to audit directly; the one confirmed, actionable cross-cutting risk (proxy-header/`request.client.host` reliability) is already filed as `BLG-SEC-24` (P1) — not duplicated here.
- Part 3 (BLG-SEC-24 resolution): live-verified 2026-07-31 — no proxy-IP collapse, no config change needed. See run `30611215629` above.
- No new backlog item filed by this story specifically; `BLG-SEC-24` (filed under ST-06) is the operative follow-up for both stories' overlapping finding, now resolved.

## Sign-off

**Cybersecurity & Trust Lead:** Confirmed — application-level audit refreshed against all 131 current endpoints (3 new since 2026-07-26, no new gap); Render platform-level posture documented to the extent verifiable from this repository, with the one cross-cutting actionable risk correctly cross-referenced to `BLG-SEC-24` rather than duplicated. 2026-07-29.

**Cybersecurity & Trust Lead (Part 3 addendum):** Confirmed — `BLG-SEC-24` live-verification methodology and evidence reviewed (GitHub Actions run `30611215629`, job logs independently inspected). Job ordering was `needs`-gated and the observed gap between Job A's HTTP 429 (06:58:11.57 UTC) and Job B's probe (06:58:17.14–17.80 UTC) was ~6 seconds — comfortably inside the 60s sliding window, ruling out a window-expiry false negative. Job A's block on attempt 61 matches the configured `_HEALTH_LIMIT = 60` exactly. `request.client.host` extraction is identical (transport-layer property, not per-route) across all four rate-limited call sites (`main.py` `/health`, `ai.py` journal-summary/daily-briefing/chat, `trade_plans.py` generate-plan/generate-thesis), so this single verification of the underlying primitive generalizes to all of them. `BLG-SEC-24` is resolved: no proxy-IP collapse, no code change required. 2026-07-31.
