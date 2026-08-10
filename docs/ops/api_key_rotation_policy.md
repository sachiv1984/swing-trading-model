**Owner:** Cybersecurity & Trust Lead
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.2
**Last Updated:** 2026-08-10 (ST-05, BLG-SEC-16, v8.5 — Application X-API-Key added to Scope/Rotation Schedule/Credential-Specific Notes; it was formally registered in v6.8 (BLG-OPS-99) and gained a detailed rotation procedure in its own register entry at v8.2 (ST-06, BLG-SEC-27), but this policy document's own scope table and schedule never referenced it); prior — 2026-05-29 (ST-15, BLG-GOV-36 — initial policy)
**Cycle:** 2026-08-08__release-v8.5 (ST-05 — BLG-SEC-16)

---

# API Key Rotation Policy

## Purpose

This document defines the mandatory rotation schedule and procedure for all external API credentials used by the Momentum Trading Assistant. Regular rotation limits the blast radius of a compromised key.

For the single-credential external API key security register (key names, storage locations, rotation cadence, last rotation dates), see: `docs/security/api_key_security_register.md`.

For the Alpaca API key specifically (rotation steps, trigger conditions), see: `docs/ops/alpaca_key_rotation_policy.md`.

---

## Scope

This policy covers all external API credentials listed in `docs/security/api_key_security_register.md`:

| Credential | Env Var | Rotation Cadence |
|-----------|---------|------------------|
| Alpaca API Key ID | `APCA_API_KEY_ID` | Annual minimum (12 months) |
| Alpaca API Secret | `APCA_API_SECRET_KEY` | Annual minimum (12 months) |
| Anthropic API Key | `ANTHROPIC_API_KEY` | Annual minimum (12 months) |
| News API Key | `NEWS_API_KEY` | Annual minimum (12 months) |
| Supabase DB Connection | `DATABASE_URL` | On suspected compromise only |
| Application X-API-Key | `API_KEY` (backend/Render), `REACT_APP_API_KEY` (frontend build-time) | Annual minimum (12 months) |

---

## Rotation Schedule

### Routine Rotation

| Credential | Cadence | Trigger |
|-----------|---------|---------|
| Alpaca API Key + Secret | Annual (12 months) | Calendar schedule; first rotation due 12 months from last recorded rotation |
| Anthropic API Key | Annual (12 months) | Calendar schedule; first rotation due 2026-08-25 (90 days from first inventory) |
| News API Key | Annual (12 months) | Calendar schedule |
| Supabase DB Connection | Not scheduled — see emergency trigger table | Rotate only on suspected breach |
| Application X-API-Key | Annual (12 months) | Calendar schedule; last rotated 2026-08-04 (ST-06, BLG-SEC-27, v8.2), next due 2026-08-04 + 12 months |

### Emergency Rotation Triggers (All Credentials)

| Trigger | Response |
|---------|---------|
| Credential appears in any public repository, log file, or error message | Immediate rotation — within 1 hour of detection |
| Unexpected API calls observed in provider account (unknown IP, unusual activity) | Immediate rotation — within 1 hour |
| Render environment variables are exposed or the Render account is compromised | Immediate rotation — within 1 hour |
| Team member offboarding who had access to key material | Rotate within 24 hours |

---

## Rotation Procedure

### General Procedure (All Credentials)

1. **Generate a new credential** in the provider's console (Alpaca / Anthropic / news provider / Supabase dashboard).
2. **Update Render staging env first** — update the relevant `env var` in Render → staging service → Environment tab. Save changes (triggers redeploy).
3. **Verify on staging** — confirm the relevant endpoint responds correctly after redeploy (e.g. `GET /health/detailed` for Alpaca, `POST /trade-plans/{plan_id}/generate-thesis` for Anthropic).
4. **Update Render production env** — repeat Step 2 for the production service.
5. **Verify on production** — spot-check the same endpoint in production.
6. **Revoke the old credential** in the provider's console.
7. **Update the security register** — update `last_rotated` in `docs/security/api_key_security_register.md`.
8. **Commit the register update:** `[GOVERNANCE] <service> API key rotated YYYY-MM-DD`

### Credential-Specific Notes

**Alpaca API Key + Secret:**
- Full step-by-step procedure: `docs/ops/alpaca_key_rotation_policy.md`
- Secret is shown only once at generation in the Alpaca dashboard. If the secret is lost, generate a new key pair.
- Revoke the old key only after verifying the new key is functional (Step 6 comes after Steps 3–5).

**Anthropic API Key:**
- Generate in Anthropic Console → Settings → API Keys.
- The platform does not support key-level scope restrictions — full API access is granted to all keys.
- Application-level controls apply; see `docs/security/anthropic_api_key_scope_review.md`.

**Supabase DB Connection (`DATABASE_URL`):**
- Rotate by generating a new Supabase project password or connection string from the Supabase dashboard.
- The connection string includes the password inline — treat as a secret.
- Staging and production use separate Supabase projects; rotate independently.
- Only rotate on suspected compromise — routine rotation is not scheduled.

**Application X-API-Key (`API_KEY` / `REACT_APP_API_KEY`):** (ST-05, BLG-SEC-16, v8.5)

This credential does not follow the General Procedure above unchanged — staging and production hold two **distinct** values (since the 2026-08-04 rotation, ST-06/BLG-SEC-27), and the frontend bundle bakes the key in at build time, so a rotation is incomplete until the frontend is rebuilt. Full step-by-step procedure and the last-rotation verification evidence are maintained in the register entry itself (single source of truth, not duplicated here): `docs/security/api_key_security_register.md` §6 Application X-API-Key.

- **Owner:** Cybersecurity & Trust Lead (policy); Infrastructure & Operations Owner (executes, per the Responsibility table below)
- **Steps (summary — see register entry #6 for the full procedure):**
  1. Generate two new distinct values (one for staging, one for production — do not reuse a single value across environments).
  2. Update `API_KEY` on each Render service independently (production backend, staging backend) and `REACT_APP_API_KEY` on the staging frontend service.
  3. Trigger a redeploy on each service — env var changes via the Render API do not auto-restart the running process.
  4. Update the `API_KEY` / `REACT_APP_API_KEY` GitHub Actions repo secrets to the new production value.
  5. Rebuild and redeploy the production frontend (`gh workflow run deploy.yml`) with the new key **before** revoking the old one — the already-deployed GH Pages bundle has the old key baked in and will start failing auth otherwise.
  6. Update `STAGING_API_KEY` GitHub Actions repo secret (consumed by `api-key-cross-environment-check.yml`) to the new staging value.
  7. Update the local `RENDER_API_KEY` copy in `~/.api_keys`.
  8. Revoke old values only after step 5 completes.
- **Verification checklist (all must pass before considering the rotation complete):**
  - [ ] Old shared/previous value returns `401` against production.
  - [ ] Old shared/previous value returns `401` against staging.
  - [ ] New production value returns `200` against production.
  - [ ] New production value returns `401` against staging (confirms genuine per-environment distinctness, not a synchronized rotation).
  - [ ] New staging value returns `200` against staging.
  - [ ] New staging value returns `401` against production.
  - [ ] `api-key-cross-environment-check.yml`'s next scheduled run (daily, 06:00 UTC) completes without a `[CROSS-WIRED]` finding.
  - [ ] Production GH Pages frontend rebuilt and redeployed with the new key (confirm via a manual authenticated request through the live frontend, not just the API directly).
- **Update the register:** `last_rotated` in `docs/security/api_key_security_register.md` §6, same as the General Procedure step 7.

---

## Responsibility

| Role | Responsibility |
|------|---------------|
| Infrastructure & Operations Owner | Executes rotation procedure for all credentials; updates `last_rotated` in security register |
| Cybersecurity & Trust Lead | Policy owner; confirms rotation completion; handles breach escalation |

---

## Storage Rules (All Credentials)

- **Never** store any credential value (key, secret, token, password) in source code, `.env` files committed to git, or any file in the repository.
- **Only** store credentials in Render environment variables.
- Credential IDs (e.g. Alpaca key ID — not the secret) may appear in logs only if they are non-sensitive public identifiers.
- Do not pass credentials in URL query parameters.

---

## Escalation

If a credential is suspected compromised and the rotation procedure cannot be completed within 1 hour:
1. **Revoke the credential immediately** in the provider's console (Step 6 first) to cut off access.
2. **Notify the Cybersecurity & Trust Lead** and Infrastructure & Operations Owner immediately.
3. **Assess impact** — review provider audit logs for any unauthorised use during the exposure window.

---

## Acceptance

- Accepted by: Cybersecurity & Trust Lead
- Accepted by: Infrastructure & Operations Owner
- Date: 2026-05-29
