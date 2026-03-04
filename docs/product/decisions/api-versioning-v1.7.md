**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Superseded
**Superseded by:** v1.7 ship — 2026-03-03
**Changelog:** docs/product/changelog.md#v1.7
**Verification report:** claude/cycles/2026-03-02__release-v1.7/verification_report.md
**Cycle:** 2026-03-02__release-v1.7
**Version:** 0.1.0
**Last Updated:** 2026-03-04
**Cycle:** 2026-03-02__release-v1.7
**Maps to:** S2-05 (EPIC-05)

---

# Decision Record — API Versioning Policy (v1.7)

## Context

v2.0 Alerts will introduce webhook and async callback patterns. A versioning policy must be established before v2.0 pre-alignment opens to:

1. Determine if and how API endpoints are versioned.
2. Define the deprecation notice period.
3. Define how webhook/async patterns are handled under the policy.
4. Clarify the status of existing endpoints.

This decision record answers the four questions defined in EPIC-05 (stage4_backlog_slice.md).

---

## Decision Questions and Answers

### Q1 — Do we version API endpoints? If yes, what approach?

**Decision: Yes — URL path versioning, deferred until a breaking change is introduced.**

**Rationale:**
- The current API (`/portfolio`, `/trades`, `/analytics/metrics`, etc.) has no version prefix. There are no external consumers other than the first-party frontend (`sachiv1984.github.io`).
- Introducing a version prefix today (`/v1/`) with no breaking changes is unnecessary overhead.
- URL path versioning (e.g. `/v2/alerts`) is chosen as the versioning approach when needed because:
  - It is explicit, human-readable, and cacheable.
  - It is consistent with the conventions of the existing `/api_contracts/` specs.
  - Header versioning (`Accept: application/vnd.api+json;version=2`) adds client complexity with no benefit for this system's use case.
- **Trigger rule:** A new version prefix (`/v2/`) is introduced only when a breaking change is necessary and cannot be avoided via additive extension. Additive changes (new fields, new endpoints) do not require a version bump.

**Breaking change definition (canonical):**
- Removing or renaming a field from a response object.
- Changing the type of an existing response field.
- Removing an endpoint.
- Changing the semantics of an existing field (same name, different meaning).
- Changing required query parameters to required body parameters.

**Non-breaking change definition (additive — no version bump required):**
- Adding a new field to a response object.
- Adding a new optional query parameter.
- Adding a new endpoint.
- Expanding an enum with a new value (when clients are expected to handle unknown values gracefully).

---

### Q2 — Deprecation notice period?

**Decision: Minimum 60-day notice before removing or breaking a versioned endpoint.**

**Rationale:**
- The primary consumer is the first-party frontend. 60 days is sufficient for coordinated changes within a solo/small-team development cycle.
- Deprecation procedure:
  1. Add a `Deprecation` response header to all responses from the affected endpoint: `Deprecation: true; date="YYYY-MM-DD"`.
  2. Add a `Sunset` response header indicating the removal date: `Sunset: YYYY-MM-DDT00:00:00Z`.
  3. Log a WARNING on every call to the deprecated endpoint from the deprecation date.
  4. Update the relevant `api_contracts/*.md` spec with a `⚠️ Deprecated` notice and removal date.
  5. Remove the endpoint no earlier than 60 days after the deprecation date.
- For the current v1 API (which has no version prefix and no external consumers), breaking changes are managed by coordinating the backend and frontend deployments within the same release cycle rather than by the formal deprecation procedure above. The formal procedure applies from v2 onwards.

---

### Q3 — How are webhook/async patterns handled?

**Decision: Webhooks introduced in v2.0 follow URL path versioning from inception (`/v2/webhooks/...`) and are subject to the same 60-day deprecation policy from their first stable release.**

**Rationale:**
- Webhooks are consumer-driven (the consumer registers an endpoint to receive callbacks). Breaking a webhook contract forces the consumer to update their handler. The same versioning and deprecation rules therefore apply.
- v2.0 Alerts webhooks will be introduced under `/v2/webhooks/alerts` (or equivalent). The exact path will be defined in the v2.0 API contracts spec.
- Async job status endpoints (e.g. `GET /v2/jobs/{job_id}`) follow the same URL versioning rules.
- **Webhook payload versioning:** Webhook payloads will include a `schema_version` field in the body (e.g. `"schema_version": "2.0"`). This allows consumers to handle multiple payload versions independently of the URL version.

```json
{
  "schema_version": "2.0",
  "event": "alert.triggered",
  "alert_id": "...",
  "triggered_at": "2026-03-02T10:00:00Z",
  "payload": { ... }
}
```

---

### Q4 — Are existing endpoints grandfather-exempted?

**Decision: Yes — all existing v1 endpoints are grandfather-exempted from the URL versioning requirement.**

**Rationale:**
- The existing endpoints (`/portfolio`, `/positions`, `/trades`, `/analytics/metrics`, `/validate/calculations`, `/signals`, `/cash`, `/health`) are treated as "v1" by convention even without a `/v1/` prefix.
- They will not be renamed to `/v1/...` unless a breaking change requires a new version, at which point the new version will be introduced as `/v2/...` and the old unversioned path will be deprecated per the 60-day policy above.
- **Exception:** If a breaking change is required for an existing endpoint before v2.0, the endpoint will be versioned at that point (e.g. `/v2/portfolio`). The old path will remain accessible for 60 days with deprecation headers.

---

## Summary Table

| Question | Decision |
|----------|----------|
| Versioning approach | URL path versioning (`/v2/`), deferred until first breaking change |
| Deprecation notice | 60 days minimum, with `Deprecation` and `Sunset` response headers |
| Webhook/async handling | URL path versioning from inception + `schema_version` field in payload |
| Existing endpoints | Grandfather-exempted; versioned only if a breaking change is introduced |

---

## Gate Cleared

✅ v2.0 pre-alignment gate (API versioning) is cleared by this decision record.

v2.0 pre-alignment may proceed subject to all other gate conditions (EPIC-04 structured logging standards also required).

---

## Review Sign-offs

**TASK-18 — API Contracts & Documentation Owner Review** (Delegated Authority, 2026-03-02)

Reviewed against current endpoint design and v2.0 Alerts scope:
- Q1 (URL path versioning, deferred to first breaking change): consistent with current unversioned endpoints and avoids premature version churn ✅
- Q2 (60-day deprecation + response headers): sufficient notice period for the current single-consumer system; `Deprecation`/`Sunset` headers are the industry standard and add no overhead ✅
- Q3 (webhooks use URL path versioning from inception): correct — webhooks are new surface area and should not inherit the grandfather exemption ✅
- Q4 (grandfather exemption for existing endpoints): appropriate — retrofitting version segments to existing routes would break all current consumers with zero benefit ✅

**Review: APPROVED.** No changes required to the policy draft.

**TASK-20 — Head of Specs Team Lifecycle Sign-off** (Delegated Authority, 2026-03-02)

Lifecycle compliance review:
- Class 4 (Planning Document): correct — decision records under `docs/product/decisions/` are Class 4 ✅
- Header complete: Owner, Class, Status, Version, Cycle, Maps-to all present ✅
- Status set to Active ✅
- All four mandated decision questions explicitly answered ✅
- v2.0 pre-alignment gate cleared statement present ✅

**Sign-off: GRANTED.** v2.0 pre-alignment gate (API versioning) is cleared.

---

## Changelog

| Version | Date | Change | Author |
|---------|------|--------|--------|
| 0.1.0 | 2026-03-02 | Initial draft — TASK-17 and TASK-19 complete. Four versioning questions answered. v2.0 gate cleared pending TASK-18/20. | Product Owner |
| 0.1.0 | 2026-03-02 | TASK-18 API Contracts review: APPROVED. TASK-20 Head of Specs Team sign-off: GRANTED. Status Draft → Active. All EPIC-05 acceptance criteria met. | API Contracts & Documentation Owner + Head of Specs Team |
