Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-06-03

---

# QA Evidence — EPIC-03: Product Correctness & Ops

**EPIC:** EPIC-03 — Product Correctness & Ops
**Cycle:** 2026-06-03__release-v5.0
**Sprint goal:** Close all five AUD-2026-06-02 governance open items, ship the two v4.9 slipped product correctness fixes (FEAT-43, BE-25), and deliver the full SI-05 Phase 1 pre-work documentation suite.
**Test scenarios used:** Code review (ST-06, ST-07) + staging verification (ST-08 — complete 2026-06-03)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-06 | `docs/specs/api_contracts/signal_endpoints.md` | Backend: `allocation_insufficient` status + `reason` field when price_gbp > allocation_gbp; DB: `reason` column + extended status constraint; Frontend: `SignalCard` orange "Cannot Size" badge + reason inline; openapi.yaml updated; test.py + SC-SS-01b updated | All AC items: new status set correctly, reason string present, frontend displays visually distinct, openapi/test.py updated | Pass | None |
| ST-07 | `docs/specs/api_contracts/pre_entry_validation.md` | 5-minute module-level cache added to `check_market_regime()` in `position_manager.py`; all callers (dashboard, pre-entry validation, signal generation) share one result per window; new unit tests added covering cache hit/miss paths | `_check_regime()` uses shared cache; no independent `yf.download` from pre-entry validation; dashboard and pre-entry agree within session | Pass | None |
| ST-08 | `docs/specs/api_contracts/ai_thesis_generation.md`, `docs/specs/api_contracts/ai_endpoints.md` | Verification-only — no code to write. Staging run completed 2026-06-03 by Infrastructure & Operations Owner acting via Sprint Execution Engine. | ST-08-AC-01: POST /trade-plans/{plan_id}/generate-thesis HTTP 200 + non-null thesis ✅; ST-08-AC-02: POST /ai/check-daily-cost HTTP 200 + cost structure confirmed ✅ | Pass | None |

**QA test coverage:**
- Scenarios run: code review (ST-06, ST-07); staging verification complete (ST-08 — 2026-06-03)
- Regression areas checked: signal generation logic (status assignment), pre-entry validation (regime gate), Anthropic SDK endpoints
- Known deviations filed: None
- Frontend testing gap: ST-06 SignalCard orange badge has no Playwright coverage — code review only; **BLG-FE-61 filed** for Playwright E2E coverage

---

## ST-08 Staging Verification — Complete

**Check 1 (ST-08-AC-01):** `POST /trade-plans/{plan_id}/generate-thesis`
- Date checked: 2026-06-03
- HTTP status: 200
- thesis field non-null: **Yes** — `"Apple breaks above prior resistance at 185 with volume expansion, confirming institutional accumulation and establishing a higher high structure…"` (model: claude-haiku-4-5, prompt_version: v3.0)
- Notes: Response shape: `{"status":"ok","data":{"thesis":"...","model_version":"claude-haiku-4-5","prompt_version":"v3.0","input_hash":"...","output_hash":"...","available":true}}`

**Check 2 (ST-08-AC-02):** `POST /ai/check-daily-cost`
- Date checked: 2026-06-03
- HTTP status: 200
- Cost structure correct: **Yes** — `{"total_cost_usd":0.000468,"request_count":1,"threshold_usd":1.0,"threshold_exceeded":false,"alert_sent":false}`
- Notes: All expected cost fields present; threshold not exceeded; alert_sent false (correct — below threshold)

---

## Sign-Off Block

- [x] All acceptance criteria verified against canonical spec (ST-06 and ST-07: code review ✓; ST-08: staging verification ✓ 2026-06-03)
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked

**Staging verification sign-off (Infrastructure & Operations Owner):**
- Signed off by: Infrastructure & Operations Owner (acting via Sprint Execution Engine — user-authorised)
- Date: 2026-06-03
- Comments: Both AC-01 and AC-02 confirmed on staging (trading-assistant-api-staging.onrender.com). Anthropic SDK 0.105.2 endpoints functional. BLG-OPS-52 closed. ST-06 frontend badge: code review only — BLG-FE-61 filed for Playwright E2E coverage (LL-v3.1-EX-01 gate).

**DoQ consolidation (agent-mediated sign-off — Director of Quality):**
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-06-03
- Comments: ST-06 code review pass — backend logic correct, spec_references populated, no deviations; frontend observable AC (orange badge) has no Playwright coverage, BLG-FE-61 filed before PR opens per LL-v3.1-EX-01 hard gate. ST-07 code review pass — shared cache correct, unit tests added. ST-08 staging verification complete — both endpoints HTTP 200, thesis non-null, cost structure present. No P0 or P1 deviations across EPIC-03. Merge gate PR comment from Director of Quality still required before merge (always-human gate per §5.3).
