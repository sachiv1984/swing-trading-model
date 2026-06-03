Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-06-03

---

# QA Evidence — EPIC-03: Product Correctness & Ops

**EPIC:** EPIC-03 — Product Correctness & Ops
**Cycle:** 2026-06-03__release-v5.0
**Sprint goal:** Close all five AUD-2026-06-02 governance open items, ship the two v4.9 slipped product correctness fixes (FEAT-43, BE-25), and deliver the full SI-05 Phase 1 pre-work documentation suite.
**Test scenarios used:** Code review (ST-06, ST-07) + staging verification (ST-08 — pending Infrastructure & Operations Owner)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-06 | `docs/specs/api_contracts/signal_endpoints.md` | Backend: `allocation_insufficient` status + `reason` field when price_gbp > allocation_gbp; DB: `reason` column + extended status constraint; Frontend: `SignalCard` orange "Cannot Size" badge + reason inline; openapi.yaml updated; test.py + SC-SS-01b updated | All AC items: new status set correctly, reason string present, frontend displays visually distinct, openapi/test.py updated | Pass | None |
| ST-07 | `docs/specs/api_contracts/pre_entry_validation.md` | 5-minute module-level cache added to `check_market_regime()` in `position_manager.py`; all callers (dashboard, pre-entry validation, signal generation) share one result per window; new unit tests added covering cache hit/miss paths | `_check_regime()` uses shared cache; no independent `yf.download` from pre-entry validation; dashboard and pre-entry agree within session | Pass | None |
| ST-08 | `docs/specs/api_contracts/ai_thesis_generation.md`, `docs/specs/api_contracts/ai_endpoints.md` | Verification-only — no code to write. Requires Infrastructure & Operations Owner staging run. | ST-08-AC-01: POST /trade-plans/{plan_id}/generate-thesis HTTP 200 + non-null thesis on staging; ST-08-AC-02: POST /ai/check-daily-cost HTTP 200 + expected cost structure on staging | **Pending staging sign-off** (DEL-20260603-01) | None expected |

**QA test coverage:**
- Scenarios run: code review (ST-06, ST-07); staging verification pending (ST-08)
- Regression areas checked: signal generation logic (status assignment), pre-entry validation (regime gate), Anthropic SDK endpoints
- Known deviations filed: None

---

## ST-08 Staging Verification (To be completed by Infrastructure & Operations Owner)

**Instructions for Infrastructure & Operations Owner:**

Please run the following staging checks and complete the sign-off block below:

**Check 1 (ST-08-AC-01):** On the staging environment, call `POST /trade-plans/{plan_id}/generate-thesis` with a valid plan_id. Confirm HTTP 200 response with a non-null `thesis` field.
- Date checked: _______
- HTTP status: _______
- thesis field non-null: Yes / No
- Notes: _______

**Check 2 (ST-08-AC-02):** On the staging environment, call `POST /ai/check-daily-cost`. Confirm HTTP 200 response with expected cost structure (fields: daily_cost, limit, within_limit).
- Date checked: _______
- HTTP status: _______
- Cost structure correct: Yes / No
- Notes: _______

---

## Sign-Off Block (Pending)

> **Note:** This sign-off block cannot be completed until ST-08 staging checks are done by Infrastructure & Operations Owner. Once ST-08 is signed off, Director of Quality counter-sign is required to open the EPIC-03 PR.

- [ ] All acceptance criteria verified against canonical spec (ST-06 and ST-07: code review ✓; ST-08: staging pending)
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked

**Staging verification sign-off (Infrastructure & Operations Owner):**
- Signed off by: _(Infrastructure & Operations Owner)_
- Date: _(fill in — must be non-blank before PR opens)_
- Comments:

**DoQ consolidation (Director of Quality):**
- Signed off by: _(Director of Quality)_
- Date: _(fill in after staging sign-off received)_
- Comments: ST-06 + ST-07 autonomous code-review pass; ST-08 staging sign-off by Infrastructure & Operations Owner per DEL-20260603-01.
