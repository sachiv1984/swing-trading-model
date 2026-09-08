**Owner:** API Contracts & Documentation Owner
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-09-08 (ST-43, EPIC-05, v9.2, BLG-SPEC-119 — tracker created)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Deprecated / Superseded Endpoint Sunset Tracker

## 1. Purpose

Single live register of every API endpoint currently inside its deprecation-notice window (per `conventions.md` §14), and a historical log of endpoints already fully removed or superseded. `conventions.md` §14 defines *how* an endpoint is deprecated and removed; this document tracks *which* endpoints are currently in that process, so a reader doesn't have to scan `api_changelog.md` and every contract file to find out what's actually pending sunset right now.

This tracker is updated as part of the same commit that marks an endpoint `deprecated: true` in `docs/reference/openapi.yaml` (§14.3), and again when the endpoint is actually removed (§14.5).

## 2. Currently Active Deprecations (Notice Window Open)

| Endpoint | Marked deprecated | Notice window | Earliest removal | Replacement | Status |
|----------|-------------------|----------------|-------------------|-------------|--------|
| — | — | — | — | — | None currently active |

**Confirmed 2026-09-08 (ST-43):** `grep -i "deprecat" docs/reference/openapi.yaml` returns 0 matches — no endpoint in the live contract is currently marked `deprecated: true`. This matches `conventions.md` §14's own note that no endpoint has ever been formally deprecated under the §14 process (the process was written ahead of the first real deprecation, v8.3).

## 3. Historical Register — Superseded or Removed Before §14 Existed

These predate the `conventions.md` §14 deprecation-window policy (added v8.3, 2026-08-06) and were handled as direct contract-file supersession/rename rather than the formal `deprecated: true` + notice-window process. Recorded here for completeness, not because the §14 process applies retroactively.

| Endpoint / Contract | Outcome | Replacement | Reference |
|----------------------|---------|-------------|-----------|
| `docs/specs/api_contracts/gemini_thesis_generation.md` (`POST /trade-plans/{plan_id}/generate-thesis`, Gemini-backed implementation) | Contract file renamed/superseded in place, not removed | `docs/specs/api_contracts/ai_thesis_generation.md` v2.1.0 | v4.2 ST-08 / BLG-SPEC-42 |
| `GET /settings`, `PUT /settings` (v1.0.0 settings contract) | Replaced by `PATCH /settings/{settings_id}` + `POST /settings` to match live implementation | `docs/specs/api_contracts/settings_endpoints.md` v1.1.0+ | ESC-20260304-01 option (a); v1.8 ST-09 |

No endpoint in either row above remains live under its old shape — both are fully resolved, listed for audit-trail completeness only.

## 4. Process Reference

See `conventions.md` §14 for the full deprecation-window policy (30-day minimum for internally-consumed endpoints, 90-day minimum for externally-consumed ones, sign-off requirements for exceptions). This tracker does not restate that policy — it is the live register §14.4 points to.

## 5. Sign-Off

**API Contracts & Documentation Owner:** Confirmed — tracker created, §2 register verified empty against the current `openapi.yaml` (0 `deprecated: true` entries), §3 historical entries cross-checked against their source contract files. 2026-09-08.

---

## Change Log

| Date | Version | Summary |
|---|---|---|
| 2026-09-08 | 1.0 | Tracker created (ST-43, EPIC-05, v9.2, BLG-SPEC-119). |
