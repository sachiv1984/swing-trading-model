**Owner:** Cybersecurity & Trust Lead
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-29
**Cycle:** 2026-05-29__release-v4.3 (ST-15 — BLG-GOV-36)

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
| Alpaca API Key ID | `ALPACA_API_KEY` | Annual minimum (12 months) |
| Alpaca API Secret | `ALPACA_API_SECRET` | Annual minimum (12 months) |
| Anthropic API Key | `ANTHROPIC_API_KEY` | Annual minimum (12 months) |
| News API Key | `NEWS_API_KEY` | Annual minimum (12 months) |
| Supabase DB Connection | `DATABASE_URL` | On suspected compromise only |

---

## Rotation Schedule

### Routine Rotation

| Credential | Cadence | Trigger |
|-----------|---------|---------|
| Alpaca API Key + Secret | Annual (12 months) | Calendar schedule; first rotation due 12 months from last recorded rotation |
| Anthropic API Key | Annual (12 months) | Calendar schedule; first rotation due 2026-08-25 (90 days from first inventory) |
| News API Key | Annual (12 months) | Calendar schedule |
| Supabase DB Connection | Not scheduled — see emergency trigger table | Rotate only on suspected breach |

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
