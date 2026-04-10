Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-04-06

---

# QA Evidence Log — EPIC-01: System Status Reliability

**Cycle:** 2026-04-05__release-v2.5
**Sprint:** Sprint 1

---

## ST-01 — Fix auth forwarding in POST /test/endpoints

**Spec references:** `backend/services/health_service.py`, `backend/routers/test.py`

**Commits:** `230643b` (auth forwarding), `2a471e5` (React Query v5 `isPending` + `onSuccess` state fix)

**What was built:**
Extracted `X-API-Key` from the incoming `request.headers` in the `POST /test/endpoints` route (`backend/routers/test.py`). Built a `forward_headers` dict containing the key if present, and passed it to all `httpx.AsyncClient` GET and POST calls. Updated `health_service.py test_all_endpoints()` to accept an `api_key` parameter and forward it via `headers` dict. Implementation uses API key forwarding (not middleware bypass) per RISK-01.

**Acceptance criteria:**

| Dimension | Criteria | Status |
|-----------|----------|--------|
| Technical | `test_all_endpoints()` accepts and forwards API key; `POST /test/endpoints` extracts X-API-Key and passes through | Pass |
| Quality | All correctly-implemented endpoints report "pass" when system is healthy | Pass (staging — 26/26, 100%) |
| Security | API key forwarding only — no middleware bypass; key not stored or logged | Pass (code review) |
| Verification | Staging run confirming success rate improves from 1/17 to expected pass rate; code review confirming no bypass pattern | Pass — DoQ 2026-04-10 (staging: 26/26 pass) |

---

## ST-02 — Sync endpoint test list with openapi.yaml

**Spec references:** `docs/reference/openapi.yaml`, `backend/services/health_service.py`, `backend/routers/test.py`, `src/pages/SystemStatus.js`

**Commit:** `a6a74c0`

**What was built:**
Added 9 missing v2.3/v2.4 endpoints to `backend/routers/test.py` test_cases list: `/positions/compliance`, `/alerts/rules`, `/alerts/history`, `/notifications`, `/notifications/preferences`, `/digest/weekly`, `/analytics/cohort`, `/analytics/r-multiple-distribution`, `/analytics/compliance-metrics`. Added comment block referencing `docs/reference/openapi.yaml` as source of truth (router). Added same 10 endpoints (including `/health/detailed`) to `backend/services/health_service.py` endpoint list with comment block. Updated SystemStatus.js placeholder from `'17'` to `'26'`.

**Acceptance criteria:**

| Dimension | Criteria | Status |
|-----------|----------|--------|
| Technical | All 10 missing parameterless GET endpoints added to health_service.py; comment block references openapi.yaml; placeholder text updated | Pass |
| Quality | No regression to existing endpoint tests; all added endpoints correctly included | Pass (staging — 26/26; no regression to existing 17) |
| Security | N/A | N/A |
| Verification | Code review confirming all 10 missing endpoints present; comment block present; placeholder updated | Pass — DoQ 2026-04-10 (staging: 26 endpoints confirmed, all pass) |

---

## ST-03 — Fix System Status endpoint categorisation for v2.3/v2.4 routes

**Spec references:** `src/pages/SystemStatus.js`

**Commit:** `a6a74c0` (same commit as ST-02 — changes were in same file)

**What was built:**
Updated `categorizeEndpoint()` in SystemStatus.js to route `/alerts` → "Alerts", `/notifications` → "Notifications", `/digest` → "Digest" before the existing category checks. Added `categoryConfig` entries: `Alerts` (Bell icon, rose colour), `Notifications` (BellRing icon, orange colour), `Digest` (Mail icon, teal colour). Added Bell, BellRing, Mail to lucide-react imports.

**Note:** ST-03 changes were committed under the ST-02 commit (`a6a74c0`) since both touched SystemStatus.js. This is a process observation — no P1/P2 deviation. DoQ should verify both ST-02 and ST-03 AC in the same code review.

**Acceptance criteria:**

| Dimension | Criteria | Status |
|-----------|----------|--------|
| Technical | `categorizeEndpoint()` covers /alerts, /notifications, /digest routes; categoryConfig entries for Alerts, Notifications, Digest added with icons/colours | Pass |
| Quality | Alert/notification/digest endpoints appear in correct categories (not "Other"); no regression to other categories | Pass (staging) |
| Security | N/A | N/A |
| Verification | Code review confirming new category configs; staging run or screenshot evidence | Pass — DoQ 2026-04-10 (staging: Alerts/Notifications/Digest headings confirmed; no spurious categories) |

---

## EPIC-01 Consolidation

**EPIC:** EPIC-01 — System Status Reliability
**Cycle:** 2026-04-05__release-v2.5
**Sprint goal:** Establish an operational baseline for v2.5 by sealing Sprint 1 governance debt and System Status reliability.
**Test scenarios used:** `docs/testing/atr_scenarios.md`, `docs/testing/dedup_scenarios.md`, `docs/testing/stop_price_scenarios.md` (authored by ST-13 — cover v2.4 EPIC-01 correctness fixes, not v2.5 EPIC-01 System Status)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-01 | backend/routers/test.py, health_service.py | API key forwarding to downstream test calls; React Query v5 UI fix | Auth-protected endpoints tested correctly; UI renders results | Pass (staging 2026-04-10) | P3 obs: React Query v5 `isLoading`→`isPending` + `onSuccess` state pattern required (committed `2a471e5`) |
| ST-02 | openapi.yaml, health_service.py, SystemStatus.js | 10 missing endpoints added; comment block; placeholder updated | Endpoint list synced to openapi.yaml | Pass (staging 2026-04-10) | None |
| ST-03 | src/pages/SystemStatus.js | Alerts/Notifications/Digest categories in categorizeEndpoint + categoryConfig | Routes categorised correctly | Pass (staging 2026-04-10) | None |

**QA test coverage:**
- Scenarios run: Manual — code review of all three story implementations
- Regression areas checked: endpoint test list, auth key forwarding, category routing in UI
- Known deviations filed: None

**QA sign-off block:** (Director of Quality completes this)
- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A (existing apiFetch pattern used; SystemStatus.js uses API_URL env var per existing pattern)
- Signed off by: Director of Quality
- Date: 2026-04-10
- Comments: ST-01 PASS (staging). ST-02 PASS (staging — 26/26 endpoints confirmed). ST-03 PASS (staging — Alerts, Notifications, Digest headings present; no spurious categories). One P3 observation: SystemStatus.js required a React Query v5 compatibility fix (`isLoading`→`isPending`; mutation `data` → `onSuccess` + local `useState`) committed as `2a471e5` during DoQ staging run — this is a known React Query v5 breaking change pattern, not a design defect. No P0 or P1 deviations. All EPIC-01 AC verified by staging run on 2026-04-10 against Render deployment of `exec/2026-04-05__release-v2.5/EPIC-01`.
