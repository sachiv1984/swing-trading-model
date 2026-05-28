**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect; Director of Quality
**Class:** QA Evidence Log (Class 3)
**Status:** Active
**Last Updated:** 2026-05-28
**Cycle:** 2026-05-27__release-v4.2
**EPIC:** EPIC-02 — Claude API Operational Baselines
**Branch:** exec/2026-05-27__release-v4.2/EPIC-02

---

# QA Evidence Log — EPIC-02

---

## ST-04 — API Performance Baseline Update (OA-3)

**Classification:** delegated_backend (unblocked by live environment timing run 2026-05-28)
**Commit SHA:** 0f847c69

### Acceptance Criteria Evidence

| AC | Criterion | Evidence | Status |
|----|-----------|----------|--------|
| AC-01 | `POST /ai/check-daily-cost` documented in `docs/ops/api_performance_baseline.md` | `docs/ops/api_performance_baseline.md` §14 added: p50=205ms, p95=518ms (5 samples, staging environment, warm service) | Pass |
| AC-02 | Live environment timing run completed | 5 samples collected from Render staging service (`trading-assistant-api-staging.onrender.com`). Warm service confirmed (requests after initial wake-up). Baseline: p50=205ms, p95=518ms | Pass |
| AC-03 | Infrastructure & Operations Owner sign-off | Infrastructure & Operations Owner APPROVED (agent-mediated) 2026-05-28. DEL-20260528-03 status: Unblocked. BLG-OPS-35 closed. | Pass |

**Delegation record:** DEL-20260528-03 (resolved)

---

## ST-05 — Claude API First Monthly Cost Review

**Classification:** delegated_decision (unblocked by production data query 2026-05-28)
**Commit SHA:** 46a8a3b3

### Acceptance Criteria Evidence

| AC | Criterion | Evidence | Status |
|----|-----------|----------|--------|
| AC-01 | Actual API call volume and cost data from live logging | `gemini_audit_log` query results provided by Infrastructure & Operations Owner 2026-05-28: 6 calls, 1,372 input tokens, 1,203 output tokens, $0.007387 total (2026-05-25 to 2026-05-26) | Pass |
| AC-02 | Monthly review report produced | `docs/ops/claude_cost_review_2026-05.md` v1.0 produced. Covers call volume, cost breakdown, cost rate confirmation (Claude Haiku 4.5: $1.00/1M input, $5.00/1M output), projection analysis | Pass |
| AC-03 | Monthly monitoring cadence defined | Cadence: first Thursday of each month. First review: 2026-06-05. Defined in `docs/ops/claude_cost_review_2026-05.md` §5 | Pass |
| AC-04 | Cost alert threshold defined | Daily alert threshold: $1.00/day (existing, confirmed in `gemini_service.py`). Monthly escalation threshold: $5.00/month (new — ~680× current run rate). Defined in §5 | Pass |

**Delegation record:** DEL-20260528-04 (resolved)

---

## ST-06 — Claude API Thesis Generation Latency Baseline

**Classification:** delegated_backend (unblocked by live production timing run 2026-05-28)
**Commit SHA:** cdae90b5

### Acceptance Criteria Evidence

| AC | Criterion | Evidence | Status |
|----|-----------|----------|--------|
| AC-01 | ≥10 sample calls from live environment | 10 warm production calls to `POST /trade-plans/{plan_id}/generate-thesis` on `trading-assistant-api-c0f9.onrender.com` (plan `66d6dda6-15de-447d-969e-4a0d8c548825`). Sample times (ms): 4008, 3556, 3563, 3565, 3819, 3543, 3473, 3776, 3481, 3487 | Pass |
| AC-02 | p50/p95 latency baseline recorded in `docs/ops/api_performance_baseline.md` | §15 added: p50=3,560ms, p95=3,923ms, min=3,473ms, max=4,008ms, mean=3,627ms. Note: staging excluded (ANTHROPIC_API_KEY not configured on staging). | Pass |
| AC-03 | Regression threshold defined | p95 > 7,846ms (2× baseline p95=3,923ms) triggers performance review. Defined in §15. | Pass |

**Delegation record:** DEL-20260528-05 (resolved)

---

## Consolidation Block

**EPIC:** EPIC-02 — Claude API Operational Baselines
**Cycle:** 2026-05-27__release-v4.2
**Sprint goal:** Establish Claude API operational baselines — performance, cost, and latency — needed for SI-02 observability sprint planning.
**Test scenarios used:** None (operational baseline/documentation scope — AC verifiable by live environment measurements and document review)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-04 | `docs/ops/api_performance_baseline.md` | `POST /ai/check-daily-cost` baseline: p50=205ms, p95=518ms (5 staging samples). §14 added to api_performance_baseline.md v1.6 | AC-01: endpoint documented; AC-02: live timing run; AC-03: sign-off | Pass | None |
| ST-05 | `docs/ops/claude_cost_review_2026-05.md` | First monthly Claude API cost review: 6 calls, $0.007387, monthly cadence + $5.00/month threshold defined | AC-01: actual data; AC-02: report produced; AC-03: cadence defined; AC-04: threshold defined | Pass | None |
| ST-06 | `docs/ops/api_performance_baseline.md` | Thesis generation latency baseline: p50=3,560ms, p95=3,923ms (10 production samples), regression threshold 2× p95. §15 added to api_performance_baseline.md v1.7 | AC-01: ≥10 samples; AC-02: baseline recorded; AC-03: regression threshold defined | Pass | None |

**QA test coverage:**
- Scenarios run: Live environment measurements + document review (operational baseline scope)
- Regression areas checked: Performance baseline document completeness; cost review data integrity; latency measurement methodology
- Known deviations filed: None

---

## DoQ Sign-Off

**Director of Quality:** Confirmed — agent-mediated, 2026-05-28
- Date: 2026-05-28

**Scope confirmed:**
- ST-04: All 3 ACs passed. Live staging timing run (5 samples) confirmed. `POST /ai/check-daily-cost` baseline documented.
- ST-05: All 4 ACs passed. Actual `gemini_audit_log` data used. First monthly review report produced with cadence and threshold defined.
- ST-06: All 3 ACs passed. 10 warm production samples collected. p50/p95 baseline and regression threshold documented.

**Note on sign-off class:** All 3 stories were `delegated_backend` or `delegated_decision` — standard agent-mediated DoQ sign-off applied.

**Deviations:** None.

- [x] All acceptance criteria verified against canonical spec (ST-04, ST-05, ST-06 all done)
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] No frontend component changes (documentation-only EPIC)
