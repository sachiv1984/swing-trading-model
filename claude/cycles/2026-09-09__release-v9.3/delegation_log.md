Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-10

---

## DEL-20260910-01

- **ST Item:** ST-27 — API key rotation drill
- **EPIC:** EPIC-05
- **Classification:** delegated_backend
- **Assigned to:** Cybersecurity & Trust Lead
- **GitHub Issue:** #1627
- **Branch:** exec/2026-09-09__release-v9.3/EPIC-05
- **Delegated at:** 2026-09-10T11:00:00Z
- **What is needed:** Exercise `docs/ops/api_key_rotation_policy.md`'s rotation runbook end-to-end for one non-critical key. **Recommended candidate: News API Key (`NEWS_API_KEY`)** — of the 7 credentials in scope, this is the only one with no dedicated Credential-Specific Notes subsection (unlike Alpaca, Anthropic, Supabase, Application X-API-Key, and Telegram, which each have one), meaning it follows the bare 8-step General Procedure untested by any prior drill. This makes it both genuinely non-critical (a brief misconfiguration affects only `GET /news/{ticker}`, no trading/financial-data path) and the highest-value choice for a drill specifically intended to surface runbook gaps — a credential whose procedure is already detailed and well-exercised (e.g. Application X-API-Key, which has its own explicit multi-step verification checklist) would be less likely to reveal anything new.
  1. Generate a new News API key in the provider's console.
  2. Update Render staging `NEWS_API_KEY`; verify via `GET /news/{ticker}` on staging (e.g. a liquid US ticker with recent news coverage).
  3. Update Render production `NEWS_API_KEY`; verify via `GET /news/{ticker}` on production.
  4. Revoke the old key in the provider's console.
  5. Update `last_rotated` in `docs/security/api_key_security_register.md` for this credential.
  6. Commit: `[GOVERNANCE] News API key rotated YYYY-MM-DD`.
  7. **Drill-specific step (not in the General Procedure — this is the actual AC):** record findings — did every General Procedure step work as written for this credential? Any step that failed, was ambiguous, or needed a News-API-specific addition should be corrected directly in `docs/ops/api_key_rotation_policy.md` (adding a Credential-Specific Notes subsection for News API Key, following the existing pattern used for the other 5 credentials), with the correction itself as part of this drill's evidence.
- **Spec reference:** `docs/ops/api_key_rotation_policy.md` §Rotation Procedure (General Procedure, lines 62-73); `docs/security/api_key_security_register.md` (News API Key entry, `last_rotated` field to update); `docs/security/external_api_credential_inventory.md` (background)
- **Unblock criteria:** Runbook exercised end-to-end against a live News API key rotation (staging + production Render env updates, verified via a real `GET /news/{ticker}` call against each environment, old key revoked); findings documented — either "runbook worked as written, no correction needed" or the specific correction applied to `api_key_rotation_policy.md`; `last_rotated` updated in the security register.
- **Commit format required:** `[EPIC-05][ST-27] <description>` pushed to `exec/2026-09-09__release-v9.3/EPIC-05`
- **Status:** Pending
