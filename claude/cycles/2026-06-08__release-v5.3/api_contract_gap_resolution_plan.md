**Owner:** Head of Specs Team; API Contracts & Documentation Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-09
**Cycle:** 2026-06-08__release-v5.3
**Sprint:** 1 (ST-01, BLG-SPEC-53)

---

# API Contract Gap Resolution Plan — v5.3

## Background

BLG-GOV-100 (v5.2 endpoint coverage audit) identified 6 endpoints present in `backend/routers/` but missing from their canonical API contract files and/or `docs/reference/openapi.yaml`. This plan governs how v5.3 EPIC-01 resolves those gaps.

---

## Gap List — Priority-Ranked by Risk

| Rank | Gap ID | Endpoint | Risk | Contract File | openapi.yaml Entry | v5.3 Story |
|------|--------|----------|------|---------------|-------------------|------------|
| 1 | BLG-SPEC-49 | GET /ai/journal-summary/history | Medium — AI audit endpoint; external-facing for compliance review | ai_endpoints.md (missing `## GET /ai/journal-summary/history`) | Missing | ST-04 |
| 2 | BLG-SPEC-50 | GET /analytics/compliance-metrics | Medium — analytics endpoint used by frontend dashboard | analytics_endpoints.md (missing `## GET /analytics/compliance-metrics`) | Missing | ST-05 |
| 3 | BLG-SPEC-51 | GET /news/{ticker} | Low-Medium — display-only; no auth exposure; Alpaca news passthrough | No news_endpoints.md exists | Missing | ST-06 |
| 4 | BLG-SPEC-52 | GET /watchlist, POST /watchlist, DELETE /watchlist/{entry_id} | Low — internal portfolio management; no external exposure | No watchlist_endpoints.md exists (contract_ref in router points to non-existent file) | All 3 missing | ST-07 |

**Priority rationale:**
- BLG-SPEC-49 ranked first: audit trail endpoints are compliance-critical; missing contract reduces verifiability.
- BLG-SPEC-50 ranked second: compliance-metrics is referenced in the frontend dashboard.
- BLG-SPEC-51 and BLG-SPEC-52 are lower complexity and risk (display-only, no auth exposure on these routes).

---

## Sprint Scope Recommendation

All 6 gaps (4 BLG-SPEC items, 3 watchlist sub-endpoints) are scoped to EPIC-01 Sprint 1:

| Story | Scope | Effort |
|-------|-------|--------|
| ST-01 | This resolution plan document | M |
| ST-02 | openapi.yaml completeness audit against all 50 routes | S |
| ST-03 | QA acceptance criteria template for contract gap stories | S |
| ST-04 | GET /ai/journal-summary/history → ai_endpoints.md + openapi.yaml | XS |
| ST-05 | GET /analytics/compliance-metrics → analytics_endpoints.md + openapi.yaml | XS |
| ST-06 | GET /news/{ticker} → new news_endpoints.md + openapi.yaml | XS |
| ST-07 | GET/POST/DELETE watchlist → new watchlist_endpoints.md + openapi.yaml + test.py | S |

No additional gaps were identified during ST-02 audit beyond BLG-SPEC-49–52 (see ST-02 audit report for full findings).

---

## What Constitutes a "Complete" Contract (QA Template — ST-03)

Per ST-03, a complete endpoint contract requires:
1. `## METHOD /path` heading at exactly `##` level (not `###`) in a file in `docs/specs/api_contracts/`
2. A corresponding path entry in `docs/reference/openapi.yaml`
3. For endpoints with `@router.get`/`post`/`delete` in `backend/routers/`: a corresponding entry in `backend/routers/test.py` (watchlist only per ST-07 scope)
4. For watchlist endpoints: `SystemStatus.js` fallback count and `SC-SS-01b` in `tests/e2e/system-status.spec.js` updated

---

## Sign-Off

- Head of Specs Team: approved (agent-mediated, 2026-06-09, ST-01 execution)
- API Contracts & Documentation Owner: approved (agent-mediated, 2026-06-09, ST-01 execution)
