**Owner:** Cybersecurity & Trust Lead
**Class:** Supporting Document (Class 2) — Living Reference
**Status:** Active
**Version:** 1.1
**Last Updated:** 2026-10-15 (ST-27, EPIC-04, v9.12, BLG-SEC-42 — `REACT_APP_API_KEY` reclassified: full write scope, public bundle; Product Owner accept-risk recorded, ESC-EXEC-20261015-01); prior — 2026-05-06 (initial version)
**Source:** BLG-SEC-05 (v3.2 ST-15)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Credential Policy

**Purpose:** Inventory of all production API credentials, their storage locations, rotation policy, and incident response procedures.

**Maintenance Obligation:** This document is a mandatory living reference. Updating it is a required step whenever a credential is added, rotated, or retired. This update obligation applies to all contributors — do not rotate or retire a credential without updating this document in the same commit/PR. The rotation procedure in §3 references this obligation explicitly.

---

## 1. Credential Inventory

| Credential | Environment Variable | Service | Storage | Scope | Last Rotation |
|------------|---------------------|---------|---------|-------|--------------|
| Alpaca API Key | `APCA_API_KEY_ID` | Alpaca Markets | Render environment variables | Market data + paper trading | Unknown (pre-v3.0) |
| Alpaca Secret Key | `APCA_API_SECRET_KEY` | Alpaca Markets | Render environment variables | Paired with API Key | Unknown (pre-v3.0) |
| Anthropic API Key | `ANTHROPIC_API_KEY` | Anthropic Claude API | Render environment variables | AI analysis (weekly digest, live assistant) | Unknown (pre-v3.0) |
| Telegram Bot Token | `TELEGRAM_BOT_TOKEN` | Telegram Bot API | Render environment variables | Alert delivery | Unknown (pre-v3.0) |
| Telegram Chat ID | `TELEGRAM_CHAT_ID` | Telegram Bot API | Render environment variables | Alert delivery (destination chat) | Unknown (pre-v3.0) |
| Frontend API Key | `REACT_APP_API_KEY` | Internal backend | CI/build environment; embedded in the public GitHub Pages bundle | Frontend → backend auth header. **Full read and write scope:** the same value as the backend `API_KEY`, accepted on every route except `OPTIONS` and `GET /health` (see §1.1) | Unknown |

### Storage Notes

All backend secrets are stored as Render environment variables (encrypted at rest by Render). They are never committed to source code or `.env` files in the repository.

Frontend secrets (`REACT_APP_API_KEY`) are embedded in the built JS bundle, which is served publicly from GitHub Pages, so the key is readable by anyone who loads the app. It is **not** a low-sensitivity token (the v1.0 wording): it carries the backend's full write scope. See §1.1.

### 1.1 Frontend API Key: Write Scope and Accepted Risk

**Classification (v1.1, ST-27, BLG-SEC-42, 2026-10-15):** full-write-scope credential, publicly exposed by design.

**Write scope (verified 2026-10-15 against `backend/main.py` `api_key_middleware`):** the backend checks a single `API_KEY` on every request except `OPTIONS` (CORS preflight) and `GET /health`. The frontend sends that same value, so `REACT_APP_API_KEY` authorises all 150 routes, of which 61 are writes (`POST`/`PUT`/`PATCH`/`DELETE`). These include:
- settings writes (`POST /settings`, `PATCH /settings/{settings_id}`)
- position entry and exit, and cash transactions
- stop recomputation (`GET /positions/analyze`, which writes stops; `POST /positions/nightly-stop-update`)
- signal generation, alert evaluation and backtest import
- `POST /ops/purge-audit-logs`

**Decision: Product Owner accept-risk (option (b) of ESC-EXEC-20261015-01), 2026-10-15.** The Product Owner (human, in-session) accepted the risk rather than scoping a narrower frontend key (option (a)).
- **Reason:** single-user app with no other users' data at risk. Option (a) needs a second key, a route allowlist and new secrets on Render, GitHub Pages and GitHub Actions, beyond this story's scope.
- **What the acceptance covers:** anyone who reads the bundle can call any authenticated route, including the writes above. Settings writes are audit-logged in `settings_change_log` (DS-33, BLG-SEC-41) with `request_source` `api` for non-UI callers, so a settings change made outside the Settings page is visible.
- **Review triggers:** revisit this decision, and treat option (a) as required, if any of these occurs: a second user or shared access; a live (non-paper) broker or real-money integration; any sign of calls not made by the owner (unexpected settings-log `api` rows, unexplained positions or cash transactions, Render logs from unknown clients); or at each quarterly dependency/security review.
- **Rotation note:** the §2 trigger "public exposure" cannot apply literally to a key that is public by design. Read it as "evidence of use by anyone other than the owner", one of the review triggers above.

---

## 2. Rotation Policy

| Credential | Rotation Frequency | Trigger-Based Rotation |
|------------|-------------------|-----------------------|
| Alpaca API Key + Secret | Every 12 months minimum | Immediately on: suspected compromise, staff departure with access, any security incident |
| Anthropic API Key | Every 12 months minimum | Immediately on: suspected compromise, billing anomaly |
| Telegram Bot Token | On demand (no fixed schedule) | Immediately on: suspected compromise |
| Frontend API Key | Per major release or on compromise | Immediately on: public exposure |

---

## 3. Alpaca Key Rotation Procedure

This is the step-by-step procedure for rotating Alpaca API credentials. Follow in order.

**Pre-rotation checklist:**
- [ ] Confirm new key has been generated in Alpaca dashboard (do not revoke old key yet)
- [ ] Confirm no active live trading jobs are running

**Steps:**

1. Log in to the [Alpaca dashboard](https://alpaca.markets) and generate a new API key pair.
2. Copy the new `API Key ID` and `Secret Key` — the secret is shown only once.
3. In Render dashboard: go to **Environment** for the backend service.
4. Update `APCA_API_KEY_ID` and `APCA_API_SECRET_KEY` with the new values.
5. Trigger a manual redeploy of the backend service on Render.
6. Validate (see §4 Validation).
7. Once validation passes, revoke the old key in the Alpaca dashboard.
8. Update this document:
   - Set **Last Rotation** for Alpaca credentials to today's date.
   - Note who performed the rotation and why.
9. Commit the updated `credential_policy.md` (no secrets in the commit — only the date/metadata update).

---

## 4. Validation After Rotation

After rotating any credential, validate before revoking the old key:

| Credential | Validation Step |
|------------|----------------|
| Alpaca | Hit `GET /screener/results` and confirm data loads; check `GET /market/status` returns regime data |
| Anthropic | Trigger `POST /digest/generate` (weekly digest) and confirm AI content is generated |
| Telegram | Send a test alert; confirm it appears in the configured chat |
| Frontend API Key | Load app in browser; confirm pages load without 401/403 errors |

---

## 5. Incident Response

If a credential is suspected compromised:

1. **Immediately rotate** — do not wait for a scheduled window. Follow the rotation procedure for the affected credential.
2. **Revoke the old key** immediately after confirming the new one works.
3. **Check audit logs** — review Render access logs and Alpaca/Anthropic usage dashboards for anomalous calls in the 48h window before discovery.
4. **Document** — record the incident, timeline, and response in `docs/operations/` or the appropriate governance record.
5. **Notify** — inform the Product Owner and relevant team leads.

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 1.1 | 2026-10-15 | ST-27 (BLG-SEC-42, EPIC-04, v9.12): `REACT_APP_API_KEY` reclassified from low-sensitivity to full write scope (all 150 routes, 61 writes, one shared `API_KEY`), exposed in the public bundle. New §1.1 records the scope, the Product Owner accept-risk decision (ESC-EXEC-20261015-01 option (b)), and review triggers. |
| 1.0 | 2026-05-06 | Initial credential policy document. v3.2 ST-15 (BLG-SEC-05). All known production credentials inventoried. |
