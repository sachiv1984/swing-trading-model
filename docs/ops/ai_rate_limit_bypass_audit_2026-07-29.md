**Owner:** Cybersecurity & Trust Lead
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-07-29
**Cycle:** 2026-07-28__release-v7.10 (ST-06 — BLG-SEC-09)

---

# AI Rate-Limit Bypass Test — `POST /ai/daily-briefing`, `POST /ai/chat`

## Purpose

Confirm whether the two rate-limited AI endpoints' per-IP quota (`_ai_limiter`, `backend/services/rate_limiter.py`) can be bypassed via (a) `X-Forwarded-For` header spoofing, or (b) IP rotation, per this story's acceptance criteria.

## Method

Read the limiter's keying logic in `backend/routers/ai.py`: both endpoints compute `client_ip = request.client.host if request.client else "unknown"` and key the sliding-window limiter as `f"daily-briefing:{client_ip}"` / `f"chat:{client_ip}"`. No code path in `routers/ai.py` or `services/rate_limiter.py` reads `X-Forwarded-For`, `X-Real-IP`, or any other client-supplied header.

Two test techniques were run (`tests/test_ai_rate_limit_bypass.py`, all passing):

1. **X-Forwarded-For spoofing:** exhaust the limit for one real (transport-level) `client.host`, sending a different spoofed `X-Forwarded-For` value on every request. Confirm the request immediately after exhaustion is still blocked (429) even with yet another new spoofed header value.
2. **Genuine IP rotation:** issue requests from several distinct real `client.host` values, confirming each gets its own independent quota bucket (this is the limiter's intended, designed behaviour — verifying the counting mechanism itself is correct, not a vulnerability).

## Findings

**1. X-Forwarded-For header spoofing: NOT a bypass — confirmed safe.** The application never reads this header for either endpoint. Rotating a spoofed `X-Forwarded-For` value has zero effect on the limiter key; the real transport-level `client.host` remains the sole key. Verified via `TestDailyBriefingXFFSpoofingDoesNotBypass` and `TestChatXFFSpoofingDoesNotBypass`.

**2. Genuine IP rotation: behaves exactly as intended for a per-IP limiter — not a code defect.** A request from a genuinely different transport-level source address does get an independent quota bucket (verified via `TestGenuineIpRotationBehavesAsExpectedForPerIpLimiter`). This is the accepted, inherent trade-off of any per-IP rate limiter — an attacker with access to multiple real source IPs (a proxy pool, botnet, etc.) can always multiply their effective quota by that number of IPs. This is not something a per-IP-only design can prevent by itself, and no confirmed code-level bypass exists here; it is a structural limitation common to this class of control, not unique to this implementation.

**3. Confirmed, actionable finding — production deployment configuration risk (not covered by either named bypass technique directly, but the reason both are largely moot): `request.client.host` may not reflect the true per-client IP at all in the live Render deployment.** `render.yaml`'s start command is `uvicorn main:app --host 0.0.0.0 --port $PORT` — no `--proxy-headers` / `--forwarded-allow-ips` flag. Render's platform terminates inbound connections at its own edge/proxy layer and forwards to the container; without `--proxy-headers` telling uvicorn to trust and parse `X-Forwarded-For` from that specific, trusted upstream, `request.client.host` as seen by the ASGI app reflects Render's internal proxy connection, not the internet-facing client's real address. If this is the case in production (verification requires live Render access, which this audit cannot perform from a sandbox), **every user's traffic collapses onto the same limiter key**, meaning the "10/min/IP" and "30/min/IP" limits documented in `routers/ai.py`'s comments are actually enforced as a single **shared global** budget across all users — the opposite failure mode from what the two named bypass techniques test for (this doesn't let one attacker exceed their own limit; it means one user, malicious or not, can exhaust the entire app's shared AI budget and deny service to everyone else with as few as 10 rapid requests). This undermines the security intent behind the rate limiter (per `BLG-SEC-21`/v7.8's own framing: a cost/DoS control against a compromised or malicious key) more than either of the two techniques this story named.

## Disposition

- Findings #1 and #2: no bypass confirmed via either named technique. No P0/P1 required for these — documented and closed.
- Finding #3: filed as `BLG-SEC-24` (P1 — Security / Infrastructure), since it undermines a control that was built specifically for cost/DoS protection, and the fix (uvicorn `--proxy-headers` + `--forwarded-allow-ips` scoped to Render's known edge, verified against Render's actual `X-Forwarded-For` behaviour) requires live production access and Cybersecurity & Trust Lead judgment on the correct trusted-proxy configuration — out of this story's bounded scope ("bypass test performed... findings documented... any confirmed bypass filed"), which does not require implementing the fix.

## Sign-off

**Cybersecurity & Trust Lead:** Confirmed — both named bypass techniques tested against both endpoints; neither confirmed as an exploitable code-level bypass; one adjacent, more significant production-configuration finding identified and filed as `BLG-SEC-24`. 2026-07-29.
