**Owner:** API Contracts & Documentation Owner
**Class:** Canonical Specification (Class 2)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-05-30
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# External API Integration Contract — Template

This template defines the required sections and minimum content for all external API integration contracts in this project. All new external API integration contracts must conform to this structure.

**Current integrations using this template:**
- `alpaca_integration_contract.md` — Alpaca Markets Data API v2 (conformance: partial; see §AC-03 advisory below)
- `ai_thesis_generation.md` — Anthropic Claude API (conformance: partial; see §AC-03 advisory below)
- `gemini_thesis_generation.md` — Legacy (superseded by ai_thesis_generation.md v2.1.0)

**Gate:** ≥2 external API integrations confirmed at time of authoring (Alpaca, Yahoo Finance, Anthropic = 3 integrations).

---

## Template Usage

Copy this document. Replace all `<placeholder>` values. Delete this Template Usage section. Set Status to `Active`. The document name should use the integration name, e.g. `<provider>_integration_contract.md`.

---

## 1. API Identification

| Field | Value |
|-------|-------|
| Provider | `<Provider name>` |
| API name | `<API product name>` |
| API version | `<version pinned — e.g. v2, v1beta1>` |
| Base URL | `<https://api.provider.com>` |
| SDK | `<SDK name and version, if applicable — e.g. anthropic Python SDK v0.x>` |
| Documentation URL | `<https://docs.provider.com — use authoritative docs, not cached URL>` |
| Contract authored | `<YYYY-MM-DD>` |
| Contract version | `<1.0>` |

**Version pin:** This contract is pinned to the version above. Migration to a future API version requires a new contract version and Head of Specs Team sign-off before deployment.

---

## 2. Authentication Model

**Authentication method:** `<API Key | OAuth 2.0 | Bearer Token | Basic Auth | other>`

| Credential | Environment variable | Rotation policy |
|-----------|---------------------|-----------------|
| `<key name>` | `<ENV_VAR_NAME>` | `<rotation frequency and policy doc reference>` |

**Rules:**
- Credentials must be read from environment variables at runtime. They must never be hard-coded or committed to version control.
- Credential storage and rotation follow `docs/ops/api_key_rotation_policy.md`.
- Failed authentication (401/403) must be logged and surfaced as a service error — never silently swallowed.

---

## 3. Rate Limits

| Tier | Limit | Window | Applies to |
|------|-------|--------|------------|
| `<Free/Basic/Pro>` | `<N requests>` | `<per minute/hour/day>` | `<which endpoints>` |

**Rate limit handling:**
- On `429 Too Many Requests`: apply exponential backoff starting at `<N>` seconds; maximum `<M>` retries.
- Log rate limit events to `<log file or table name>`.
- If rate limit cannot be cleared within the retry window: surface as a service error with `<error code or status>`.

**Current plan:** `<plan name — e.g. Free, Starter, Pro>`

---

## 4. Error Taxonomy

| HTTP status | Provider error code | Meaning | System handling |
|-------------|---------------------|---------|-----------------|
| `400` | `<code>` | Bad request — malformed input | Log; raise `400` to caller with sanitised message |
| `401` | `<code>` | Authentication failed | Log; alert via `<notification channel>`; raise `503` to caller |
| `403` | `<code>` | Authorisation denied | Log; raise `403` to caller |
| `404` | `<code>` | Resource not found | Log; raise `404` or `200` with `null` per endpoint contract |
| `429` | `<code>` | Rate limit exceeded | Apply retry policy (§3); log |
| `500` | `<code>` | Provider internal error | Apply retry policy (§3); log; raise `502` to caller after max retries |
| `503` | `<code>` | Provider unavailable | Apply retry policy (§3); log; surface graceful degradation per §7 |

**Error response shape:** Describe the provider's error response JSON shape here — field names for error code, message, and request ID.

**Never expose raw provider error messages to the frontend.** All provider errors must be mapped to a system error code and a sanitised message before returning to callers.

---

## 5. Cost Attribution

| Dimension | Unit | Rate | Notes |
|-----------|------|------|-------|
| `<API calls>` | `<per request>` | `<$X.XX per N>` | `<e.g. first N free>` |
| `<Input tokens>` | `<per 1M tokens>` | `<$X.XX>` | `<if applicable>` |
| `<Output tokens>` | `<per 1M tokens>` | `<$X.XX>` | `<if applicable>` |

**Cost logging:** All billable calls must be logged to `<table or file name>` with: timestamp, endpoint, units consumed, estimated cost.

**Cost monitoring:** `<Link to cost monitoring dashboard or policy doc>`.

**Monthly budget ceiling:** `<$X.XX or "not set">`. If set, document the alerting mechanism.

---

## 6. Data Model Mapping

For each data entity returned by this API, map provider field names to internal schema names:

| Provider field | Internal field | Table/model | Notes |
|---------------|----------------|-------------|-------|
| `<provider_field>` | `<internal_field>` | `<table.column>` | `<any transformation required>` |

If the provider returns nested objects, document the de-nesting logic. If provider field types differ from internal types (e.g. string vs numeric), document the conversion.

---

## 7. Retry Policy

| Scenario | Retry | Backoff | Max retries | Fallback |
|----------|-------|---------|-------------|---------|
| `429 Rate limit` | Yes | Exponential, start `<N>`s | `<M>` | Log + surface error |
| `500 Server error` | Yes | Exponential, start `<N>`s | `<M>` | Log + surface error |
| `503 Unavailable` | Yes | Exponential, start `<N>`s | `<M>` | Graceful degradation (see below) |
| `401/403 Auth` | No | — | 0 | Alert + raise to caller |
| `400 Bad request` | No | — | 0 | Log + raise to caller |
| Network timeout | Yes | Linear, `<N>`s | `<M>` | Log + surface error |

**Graceful degradation:** When this API is unavailable beyond the retry window, the system must `<describe graceful degradation behaviour — e.g. return cached data, return empty response with status "unavailable", disable feature>`. No feature may fail silently.

**Circuit breaker:** `<Document if a circuit breaker pattern is implemented and where>`

---

## 8. Known Limitations and Constraints

- `<Document any known API limitations relevant to this integration — e.g. no bulk endpoints, no webhook support, UK market data excluded>`
- `<Document any §13 compliance constraints if applicable — e.g. output is display-only, no automated decisions>`

---

## Known Deviations

*None at template authoring. Conformance gaps in existing integrations noted under §Conformance Advisory.*

---

## Conformance Advisory (BLG-SPEC-32 AC-03)

Existing sealed contracts were reviewed against this template. Gaps are noted as advisory only — sealed artefacts are not modified retroactively.

**`alpaca_integration_contract.md` v1.0:**
- ✅ Authentication model documented
- ✅ Error taxonomy partially documented (provider-specific errors noted)
- ⚠ Rate limits: documented qualitatively but no formal limit table
- ⚠ Cost attribution: no section (Alpaca free tier for standard data — zero direct cost; implicit cost is acceptable omission)
- ⚠ Data model mapping: not present as a formal section (field mappings are implicit in endpoint responses)
- ⚠ Retry policy: referenced in code comments but not formally documented in contract

**`ai_thesis_generation.md` v2.1.0:**
- ✅ Authentication model: environment variables documented
- ✅ Cost attribution: token rates documented in overview
- ✅ Data model mapping: response fields documented per endpoint
- ⚠ Rate limits: no formal rate limit table (Anthropic rate limits depend on account tier — document when tier is confirmed)
- ⚠ Error taxonomy: no formal error code table (error handling is in service layer only)
- ⚠ Retry policy: not documented in contract (retry logic is in service layer)

Remediation of these gaps is recommended at the next version bump of the respective contracts.
