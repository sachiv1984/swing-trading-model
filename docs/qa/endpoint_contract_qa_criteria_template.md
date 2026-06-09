**Owner:** Director of Quality
**Class:** Operational Reference (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-06-09
**Sprint:** 2026-06-08__release-v5.3 (ST-03, BLG-QA-51)

---

# QA Acceptance Criteria Template — Endpoint Contract Gap Stories

This template defines what constitutes a "complete" API contract for endpoint gap stories (BLG-SPEC-49–52 and future contract gap items). Applied to EPIC-01 v5.3 and reusable for future sprints.

---

## What Constitutes a "Complete" Endpoint Contract

An endpoint contract is complete when ALL of the following conditions are true:

### 1. Contract Document Heading (required)

- A `## METHOD /path` heading exists at exactly the `##` level (not `###` or deeper) in a file in `docs/specs/api_contracts/`
- The heading format is: `## GET /path`, `## POST /path`, `## PUT /path`, `## DELETE /path`, `## PATCH /path`
- Using `###` or deeper causes the OpenAPI Drift Detection gate (`openapi-drift.yml`) to miss the endpoint — this is a hard requirement

### 2. openapi.yaml Entry (required)

- A corresponding path entry exists in `docs/reference/openapi.yaml` under the `paths:` key
- Minimum required fields: `summary`, at least one response (200), response schema or description
- The path must match the contract heading exactly (case-sensitive, parameter format: `{param}`)

### 3. test.py Entry (required when applicable)

- When the endpoint is in `backend/routers/` (not `backend/main.py`), a corresponding entry must exist in `backend/routers/test.py`
- Entry format: `{"name": "METHOD /path", "method": "METHOD", "url": f"{base_url}/path", "critical": False}`
- For parameterised routes (e.g. `/{ticker}`), use a representative safe value (e.g. `AAPL`)

### 4. SystemStatus.js + Playwright Test Count (required when test.py count changes)

- If the total test.py endpoint count changes, update the fallback count in `src/pages/SystemStatus.js` (`Tests {totalTests || 'N'}`)
- Update `SC-SS-01b` in `tests/e2e/system-status.spec.js` to match the new fallback value
- Both must be updated in the same commit as the test.py change

---

## Application to BLG-SPEC-49–52

| BLG-SPEC ID | Endpoint | Contract File | openapi.yaml | test.py | SystemStatus count |
|-------------|----------|---------------|--------------|---------|-------------------|
| BLG-SPEC-49 | GET /ai/journal-summary/history | ai_endpoints.md | Required | Already present (line ~96) | No change |
| BLG-SPEC-50 | GET /analytics/compliance-metrics | analytics_endpoints.md | Required | Already present (line ~96) | No change |
| BLG-SPEC-51 | GET /news/{ticker} | news_endpoints.md (new) | Required | Already present (GET /news/AAPL) | No change |
| BLG-SPEC-52 | GET /watchlist | watchlist_endpoints.md (new) | Required | Must add | +3 endpoints |
| BLG-SPEC-52 | POST /watchlist | watchlist_endpoints.md (new) | Required | Must add | (counted above) |
| BLG-SPEC-52 | DELETE /watchlist/{entry_id} | watchlist_endpoints.md (new) | Required | Must add | (counted above) |

---

## Reusability for Future Sprints

This template applies to any story labelled `BLG-SPEC-*` with the pattern "endpoint contract gap" or "missing contract". At sprint planning, QA verifies all four completeness conditions above. A story with AC referencing this template is complete when all conditions check out.

---

## Sign-Off

- Director of Quality: approved (agent-mediated, 2026-06-09, ST-03 execution)
