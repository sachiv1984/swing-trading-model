**Owner:** Cybersecurity & Trust Lead
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-04-30
**Cycle:** 2026-04-29__release-v3.1 (ST-12)

---

# Alpaca API Key Rotation Policy

## Purpose

This document defines the mandatory rotation schedule and procedure for the Alpaca API key used by the Momentum Trading Assistant to retrieve live market data and manage brokerage operations. Regular rotation limits the blast radius of a compromised key.

---

## Rotation Schedule

| Trigger | Action Required |
|---------|----------------|
| Routine rotation | Every **90 days** from the date of last rotation |
| Suspected compromise | Immediate rotation — within 1 hour of detection |
| Team member offboarding | Rotate within 24 hours if the individual had access to key material |
| Render environment breach | Rotate within 1 hour |

The rotation date must be recorded in the **External API Credential Inventory** (`docs/ops/external_api_credential_inventory.md`) after each rotation.

---

## Trigger Conditions for Immediate Rotation

- Alpaca key appears in any public repository, log file, or error message
- Unexpected API calls observed in Alpaca account activity log (login from unknown IP, unusual order activity)
- Render environment variables are exposed or the Render account is compromised
- Suspicious trading activity not initiated by the system

---

## Step-by-Step Rotation Procedure

### Step 1 — Generate a new key in Alpaca

1. Log in to [https://app.alpaca.markets](https://app.alpaca.markets)
2. Navigate to **Paper Trading** or **Live Trading** (whichever is in use) → **API Keys**
3. Click **Generate New Key**
4. Copy both `API Key ID` and `API Secret Key` — the secret is shown only once
5. Do **not** revoke the old key yet

### Step 2 — Update Render environment variables

1. Log in to [https://dashboard.render.com](https://dashboard.render.com)
2. Navigate to the `swing-trading-model` service → **Environment** tab
3. Update `ALPACA_API_KEY` with the new key ID
4. Update `ALPACA_API_SECRET` with the new secret
5. Save changes — Render will trigger a redeploy automatically

### Step 3 — Verify the new key is working

1. Wait for the Render redeploy to complete (typically 2–3 minutes)
2. Confirm the health endpoint responds: `GET /health/detailed`
3. Confirm Alpaca data is flowing: check a live price via the positions page or `GET /positions`
4. If any errors appear referencing `ALPACA_API_KEY` or authentication: do not proceed to Step 4 — diagnose first

### Step 4 — Revoke the old key

1. Return to Alpaca → **API Keys**
2. Revoke the old key ID
3. Confirm the system continues to function normally after revocation

### Step 5 — Update the credential inventory

1. Open `docs/ops/external_api_credential_inventory.md`
2. Update the `last_rotated` field for the Alpaca entry to today's date
3. Commit the change: `[GOVERNANCE] Alpaca API key rotated YYYY-MM-DD`

---

## Storage Rules

- **Never** store the Alpaca API secret in source code, `.env` files committed to git, or any file in the repository
- **Only** store credentials in Render environment variables
- The key ID may appear in logs only if it is a public identifier (not the secret)
- Do not pass credentials in URL query parameters

---

## Escalation

If a key is suspected compromised and the rotation procedure cannot be completed within 1 hour, escalate to the Infrastructure & Operations Owner immediately. Revoke the key in Alpaca first (Step 4) before rotating to minimise exposure window.

---

## Acceptance

- Accepted by: Cybersecurity & Trust Lead
- Date: 2026-04-30
