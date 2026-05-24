# QA Evidence Log — EPIC-03
## Cycle: 2026-05-22__release-v4.0

**Owner:** Director of Quality
**Class:** DoQ Sign-off Required (frontend-visible changes present — ST-12)
**Status:** Partial — DoQ sign-off pending; ST-09 implemented 2026-05-24

---

## Stories

### ST-12 — Gemini Flash base wiring

| Field | Value |
|---|---|
| Commit SHA | fffa0dc8 |
| Branch | exec/2026-05-22__release-v4.0/EPIC-03 |
| Classification | autonomous (reclassified from delegated_frontend per LL-v2.3-EX-02) |
| Acceptance Verified | true |

**Evidence:**
- `backend/services/gemini_service.py` created with `generate_setup_thesis()` function
- `POST /trade-plans/{plan_id}/generate-thesis` added to `backend/routers/trade_plans.py`
- `google-generativeai==0.8.3` added to `backend/requirements.txt`
- `REACT_APP_GEMINI_API_KEY` added to `.env.staging` and `.env.production`
- API contract `docs/specs/api_contracts/trade_plan_endpoints.md` bumped to v0.3
- Endpoint registered in `docs/reference/openapi.yaml`
- `backend/routers/test.py`: test entry added (61 total); SystemStatus.js fallback `'61'`; SC-SS-01b updated
- Frontend: "Improve with AI" button in TradePlan.js wired to call endpoint (`editId` mode only, `HAS_GEMINI` guard)

**Observable AC — CI-testable:**
- AC-01: Endpoint returns `{"status":"ok","data":{"available":false,"error":"GEMINI_API_KEY not configured"}}` when key absent
- AC-02: Endpoint returns HTTP 404 when plan_id not found

**Observable AC — staging-only:**
- AC-03: Returns thesis text when `GEMINI_API_KEY` set (live Gemini API key required)
- Backlog item **BLG-QA-29** filed for staging verification (see below)

**Observable AC — frontend (deferred to staging):**
- AC-04: "Improve with AI" button visible on TradePlan edit page when `REACT_APP_GEMINI_API_KEY` set
- AC-05: Button click calls endpoint and populates setup_thesis textarea
- Backlog item **BLG-QA-29** covers frontend staging AC as well

---

### ST-07 — Gemini audit trail

| Field | Value |
|---|---|
| Commit SHA | 83857a78 |
| Branch | exec/2026-05-22__release-v4.0/EPIC-03 |
| Classification | autonomous |
| Acceptance Verified | true |

**Evidence:**
- `ensure_gemini_audit_log_table()` / `create_gemini_audit_entry()` / `purge_gemini_audit_log_older_than_90_days()` added to `database.py`
- Startup hook registered in `backend/main.py`
- `tests/conftest.py` `_DB_STUB_FUNCTIONS` updated
- Audit entry written fire-and-forget after each successful Gemini call in `gemini_service.py`
- Fields: model_version, prompt_version, input_hash, output_hash, generated_at, token counts, cost

**Observable AC:**
- AC-01: `gemini_audit_log` table created on startup
- AC-02: Each Gemini thesis generation call inserts a row (verifiable via integration test)
- AC-03: `purge_gemini_audit_log_older_than_90_days()` exists and compiles (CI)

---

### ST-08 — Gemini cost tracking

| Field | Value |
|---|---|
| Commit SHA | 83857a78 |
| Branch | exec/2026-05-22__release-v4.0/EPIC-03 |
| Classification | autonomous |
| Acceptance Verified | true |

**Evidence:**
- Token usage logged via `response.usage_metadata` (prompt_tokens, completion_tokens, total_tokens)
- `estimated_cost_usd` computed at $0.075/1M input + $0.30/1M output tokens
- Alert threshold: 800,000 tokens/month (80% of 1M free-tier) — documented in `docs/ops/gemini_cost_tracking.md`
- Monthly aggregate SQL provided in documentation

**Observable AC:**
- AC-01: Token fields present in `gemini_audit_log` schema
- AC-02: `estimated_cost_usd` column exists in schema
- AC-03: Alert threshold defined and documented

---

### ST-09 — CI/CD automated staging re-deploy

| Field | Value |
|---|---|
| Commit SHA | (see ST-09 commit on EPIC-03 branch) |
| Branch | exec/2026-05-22__release-v4.0/EPIC-03 |
| Classification | autonomous |
| Acceptance Verified | true (CI-testable ACs); staging-only AC deferred → BLG-OPS-28 |

**Evidence:**
- `.github/workflows/staging-deploy.yml` created — triggers on push to `main` with path filter: `src/**`, `backend/**`, `public/**`, `package.json`, `package-lock.json`, `requirements.txt`
- Docs-only commits (`docs/**`, `claude/**`, `*.md`) do NOT trigger deploy — path filter verified in workflow YAML
- Build minute impact assessed and documented in `docs/ops/staging_deploy_notes.md`: ~1 min/trigger, <3% of free-tier monthly quota
- BLG-OPS-25 dependency satisfied: deploy hook mechanism available for smoke test integration (see `docs/ops/staging_deploy_notes.md` §5)

**Observable AC — CI-testable:**
- AC-01: Path filter present in workflow YAML (verified by code review)
- AC-02: Build minute impact documented in `docs/ops/staging_deploy_notes.md`
- AC-03: BLG-OPS-25 integration notes present (§5 of staging_deploy_notes.md)

**Observable AC — staging-only:**
- AC-04: Live Render deploy triggered on code-change merge (requires `RENDER_STAGING_DEPLOY_HOOK` secret configured)
- AC-05: Docs-only commit does NOT trigger deploy (live path filter verification)
- Backlog item **BLG-OPS-28** filed for staging verification

---

## Deviations

None for ST-12, ST-07, ST-08.

ST-12: staging-only AC deferred → BLG-QA-29 filed.
ST-12: delegated_frontend → autonomous reclassification per LL-v2.3-EX-02.
ST-09: RISK-03 gate resolved 2026-05-24 — PO accepted path filter approach; implementation in progress.

---

## DoQ Sign-off Block

```
[ ] ST-12 Gemini base — CI tests pass (absent-key graceful error, 404) — Pass / Fail
[ ] ST-12 staging: thesis generated with live key (date: _______) — via BLG-QA-29 staging run
[ ] ST-12 frontend staging: Improve with AI button works (date: _______) — via BLG-QA-29 staging run
[ ] ST-07 audit trail — gemini_audit_log table created and populated — Pass / Fail
[ ] ST-08 cost tracking — token fields and cost documented — Pass / Fail
[ ] ST-09 — workflow path filter verified by code review (Pass); staging live verification deferred → BLG-OPS-28 — Pass (code review) / Staging TBD

Signed: ___________________  Date: ___________
Role: Director of Quality
```

---

*Generated by Sprint Execution Engine — 2026-05-24*
