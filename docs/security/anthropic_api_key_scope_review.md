**Owner:** Cybersecurity & Trust Lead
**Class:** Operational Policy (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-27
**Cycle:** 2026-05-26__release-v4.1 (ST-14, BLG-GOV-49)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Anthropic API Key Scope Minimization Review

## 1. Background

This review was originally scoped for `GEMINI_API_KEY` (BLG-GOV-49, filed 2026-05-25). As of v4.1, the project has migrated from the Google Gemini API to the Anthropic Claude API for thesis generation (`POST /trade-plans/{plan_id}/generate-thesis`, shipped v4.0 ST-12). The credential under review is therefore `ANTHROPIC_API_KEY`.

The Gemini API key (`GEMINI_API_KEY`) is no longer used in the codebase. See §5 for the Gemini key disposition record.

---

## 2. Scope

This review covers:
- `ANTHROPIC_API_KEY` — used by `backend/services/gemini_service.py` (legacy filename; now implements Claude API calls via the Anthropic SDK) and `backend/services/ai_service.py`
- Usage context: `POST /trade-plans/{plan_id}/generate-thesis` endpoint generates a pre-trade thesis using Claude claude-haiku-4-5

---

## 3. API Key Scope Analysis

### 3.1 Anthropic API Key Characteristics

Unlike Google Cloud credentials, Anthropic API keys are **not scoped to specific services or operations at the key level**. An Anthropic API key grants access to:

| Access Granted | Notes |
|---------------|-------|
| All Claude model tiers accessible to the account | Key does not restrict which models can be called |
| `/v1/messages` — text generation | Primary endpoint used for thesis generation |
| `/v1/models` — model listing | Not used by this application |
| Batch API endpoints | Not used by this application |
| Files API | Not used by this application |

**Assessment:** Anthropic does not currently support key-level scope restriction (as of 2026-05-27). The key grants broad API access. Scope minimization at the key level is not technically feasible with the current Anthropic platform.

### 3.2 Application-Level Scope Enforcement

Since key-level scope restriction is not available, application-level controls are the primary risk mitigation:

| Control | Status | Notes |
|---------|--------|-------|
| API key stored in environment variable only | ✅ Confirmed | `ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")` in `gemini_service.py:20` |
| API key not logged | ✅ Confirmed | No key value appears in log statements |
| API key not committed to source control | ✅ Confirmed | `.env` files in `.gitignore`; no key in repo |
| Only one model called (`claude-haiku-4-5`) | ✅ Confirmed | `ai_service.py` and `gemini_service.py` both call `claude-haiku-4-5` only |
| Graceful degradation when key absent | ✅ Confirmed | Functions return `{"available": False, "error": "ANTHROPIC_API_KEY not configured"}` when key is missing |
| Cost audit logging | ✅ Confirmed | `gemini_audit_log` table captures `model_version`, `prompt_tokens`, `completion_tokens`, `estimated_cost_usd` per call |
| Monthly cost threshold defined | ✅ Confirmed | $5.00/month threshold documented in `docs/ops/gemini_cost_tracking.md` |

### 3.3 Rate Limiting and Cost Controls

| Control | Status | Notes |
|---------|--------|-------|
| Rate limiting at API layer | ⚠️ No application-level rate limit on thesis endpoint | The endpoint relies on Anthropic's server-side rate limiting and account quotas |
| Cost threshold enforcement | ⚠️ Advisory only | The $5.00/month threshold in `gemini_cost_tracking.md` is advisory; no automated block exists |
| Per-user key isolation | N/A | Single-user application; single shared key |

**Risk assessment:** No application-level rate limit on `POST /trade-plans/{plan_id}/generate-thesis` means a malformed request loop (bug or abuse) could generate unexpected API costs. Since this is a single-user application with `X-API-Key` authentication, the practical risk is low.

**Recommendation (P3 — low priority):** Add a per-portfolio daily call limit (e.g. max 50 thesis generations per portfolio per day) to the thesis generation endpoint as a cost guard. File as backlog item.

---

## 4. Findings and Disposition

| Finding | Severity | Disposition |
|---------|----------|-------------|
| Anthropic API key scope restriction not available at platform level | ℹ️ Informational | Accepted — platform limitation; application-level controls are the primary mitigation |
| No application-level rate limit on thesis endpoint | P3 Low | Accepted with advisory — file P3 backlog item for daily call limit |
| Key stored securely in environment variables | ✅ Pass | No action needed |
| Cost audit logging active | ✅ Pass | No action needed |
| Legacy `gemini_service.py` filename may cause confusion | P4 Cosmetic | Accepted — rename deferred to avoid breaking changes; file as P4 backlog item |

---

## 5. Gemini API Key Disposition

The Google `GEMINI_API_KEY` environment variable was previously documented as used for thesis generation. As of v4.0/v4.1:

- `GEMINI_API_KEY` is **no longer referenced** in any backend service or router
- `backend/services/gemini_service.py` has been updated to use `ANTHROPIC_API_KEY` (kept the filename for backward compatibility with import paths)
- `GEMINI_API_KEY` should be removed from Render environment variables for both staging and production environments

**Action required:** Product Owner or Infrastructure & Operations Owner to remove `GEMINI_API_KEY` from Render environment variables. This is a cleanup action with no functional impact.

---

## 6. External API Keys Register Update

The `docs/ops/external_api_credential_inventory.md` has been updated in this commit to add the `ANTHROPIC_API_KEY` entry. See that document for the full inventory.

---

## 7. Sign-Off

| Role | Status | Date | Notes |
|------|--------|------|-------|
| Cybersecurity & Trust Lead | Confirmed | 2026-05-28 | Key controls verified against §4.2 Security Governance in charter: env var storage, no log exposure, cost audit logging all confirmed (§3.2) |
| AI Compliance & Governance Officer | Confirmed | 2026-05-28 | AC-01: charter scope sufficiency confirmed (§4.1 API Provider Coverage note added); AC-02: key security posture verified against §3 |
| Director of HR | Confirmed | 2026-05-28 | AC-04: governance role accountability confirmed — AI Compliance & Governance Officer role is assigned and accountable for Anthropic API oversight |
