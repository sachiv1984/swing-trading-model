Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v3.6
Cycle: 2026-05-16__release-v3.6
Last Updated: 2026-05-16

# Backlog Slice — v3.6 Arc 4 Data Integrity + Arc 2 Quality Score + Debt Clearance

---

## EPIC-01 — Arc 4 Data Capture Foundation

**Maps to:** S2-01
**Owner:** Head of Engineering
**Risk IDs:** RISK-01
**Sprint:** Sprint 1 (ST-01), Sprint 2 (ST-02)
**Estimated effort:** M (~1.5–2 days total)

Arc 4 Plan vs Reality Analysis (PO-01, shipped v3.5) deferred `entry_delta_pct` because `planned_entry_price` is not captured at position creation. This EPIC closes that data gap and surfaces the metric in the UI.

---

### ST-01 — Capture planned_entry_price at trade entry

**Owner:** Head of Engineering
**Estimated effort:** S–M (~1 day)
**Delegation class:** autonomous
**Sprint:** 1
**Dependencies:** None

**Objective:** When a position is created with a linked trade plan, snapshot `planned_entry_price` from the trade plan's `entry_price` field onto the trade record. Compute `entry_delta_pct` in the plan-vs-reality service and return it in the GET /trades/{id}/plan-vs-reality response.

**Acceptance Criteria:**

| AC-ID | Criterion | Verification |
|-------|-----------|-------------|
| AC-01 | `planned_entry_price` field added to trades table (nullable; existing records default null) | Schema migration present; GET /trades returns field |
| AC-02 | On POST /positions, if a trade plan is linked (trade_plan_id present), `planned_entry_price` is populated from the trade plan's `entry_price` field | Integration test: create position with linked trade plan → verify field populated |
| AC-03 | plan_vs_reality_service computes `entry_delta_pct = (actual_entry_price - planned_entry_price) / planned_entry_price * 100` when `planned_entry_price` is not null | Unit test on service computation |
| AC-04 | GET /trades/{id}/plan-vs-reality returns `entry_delta_pct` (float or null) in response body | API test: trade with planned_entry_price → non-null entry_delta_pct returned |
| AC-05 | Existing trades without planned_entry_price: GET /trades/{id}/plan-vs-reality returns `entry_delta_pct: null` with no error | Regression test: existing trade → null entry_delta_pct |
| AC-06 | openapi.yaml updated to reflect `planned_entry_price` field and `entry_delta_pct` in plan-vs-reality response | Drift detection gate passes |
| AC-07 | Backend route registered in backend/routers/test.py; endpoint test suite count updated | Test suite count check passes |

**Spec references:** `docs/specs/arc4/arc4_data_requirements.md §3.1`

---

### ST-02 — Update PlanVsReality component to display entry_delta_pct

**Owner:** Head of Engineering
**Estimated effort:** XS–S (~0.5 day)
**Delegation class:** autonomous
**Sprint:** 2
**Dependencies:** ST-01 (backend field and API response required)

**Objective:** Update the PlanVsReality frontend component to display `entry_delta_pct` when available. Historical trades (null value) show a "historical trade — data not captured" placeholder.

**Acceptance Criteria:**

| AC-ID | Criterion | Verification |
|-------|-----------|-------------|
| AC-01 | PlanVsReality component displays entry_delta_pct row when value is non-null: format "+X.X%" / "-X.X%" with green/red colouring | Playwright test |
| AC-02 | When entry_delta_pct is null, row shows "Entry delta: data not available for historical trades" in muted style | Playwright test |
| AC-03 | No regression in other PlanVsReality rows (entry timing, R achieved vs R target, exit alignment, lifecycle state at exit) | Playwright regression test |

**Spec references:** `docs/specs/frontend/pages/trade_history.md §Expandable Journal Row — Plan vs Reality`

---

## EPIC-02 — Arc 2 Completion: PT-04 Setup Quality Score

**Maps to:** S2-02
**Owner:** Head of Specs Team (spec) + Head of Engineering (implementation)
**Risk IDs:** RISK-02
**Sprint:** Sprint 1 (ST-03 spec), Sprint 2 (ST-04, ST-05) — conditional on gate
**Estimated effort:** M–L (~2–3 days total, if gate confirmed)

**GATE CONDITION:** Product Owner must confirm 20+ closed trades before sprint planning seals. If not confirmed, this entire EPIC defers to v3.7. Sprint Planning Engine STEP -1 must check this condition.

PT-04 is the last remaining Arc 2 feature. It provides a deterministic score (0–100) against the user's own historical win conditions — no ML, calculated from own trade history.

---

### ST-03 — PT-04 spec authoring and gate confirmation

**Owner:** Head of Specs Team + Product Owner
**Estimated effort:** XS (~0.5 day)
**Delegation class:** delegated_decision
**Sprint:** 1
**Dependencies:** Product Owner gate confirmation (20+ closed trades)

**Objective:** Author the canonical PT-04 spec: scoring algorithm (regime match %, signal alignment, ATR zone, entry timing relative to signal); scoring bands (0–39 weak, 40–69 acceptable, 70–100 strong); API contract for GET /trades/setup-quality-score; frontend display spec. Gate confirmation must be recorded before this story closes.

**Acceptance Criteria:**

| AC-ID | Criterion | Verification |
|-------|-----------|-------------|
| AC-01 | Product Owner confirms gate: 20+ closed trades in system (can check via GET /portfolio/analytics or equivalent) | Written confirmation in delegation log |
| AC-02 | `docs/specs/arc2/setup_quality_score_spec.md` authored: scoring algorithm, bands (0–39/40–69/70–100), input fields (regime status at entry, signal score, ATR proximity, entry timing) | File exists, Head of Specs Team sign-off |
| AC-03 | API contract for GET /research/{ticker}/setup-quality-score documented in `docs/specs/api_contracts/setup_quality_score_endpoint.md` | File exists; endpoint added to openapi.yaml |
| AC-04 | Frontend display spec appended to `docs/specs/frontend/pages/pre_trade_research.md`: quality score badge with band label, tooltip with factor breakdown | Spec section present |

**Spec references:** `docs/roadmap/current_roadmap.md §4 Arc 2 PT-04` (indicative)

---

### ST-04 — Setup Quality Score backend endpoint

**Owner:** Head of Engineering
**Estimated effort:** M (~1–1.5 days)
**Delegation class:** autonomous
**Sprint:** 2
**Dependencies:** ST-03 (spec must be complete and gate confirmed)

**Objective:** Implement `GET /research/{ticker}/setup-quality-score` per ST-03 spec. Score is computed deterministically from closed trade history where regime/signal/ATR conditions at entry are known.

**Acceptance Criteria:**

| AC-ID | Criterion | Verification |
|-------|-----------|-------------|
| AC-01 | GET /research/{ticker}/setup-quality-score returns `{score: int, band: str, factors: {regime_match_pct: float, signal_alignment: float, atr_proximity: float, entry_timing: float}, trade_count: int, gate_met: bool}` | API test with real/mock trade data |
| AC-02 | When trade_count < 20: `gate_met: false`, score: null, response status 200 with advisory message | API test: insufficient history → gate_met false |
| AC-03 | Score is deterministic: same trade history always produces same score | Unit test: run twice with same input |
| AC-04 | openapi.yaml updated for new endpoint; registered in backend/routers/test.py | Drift detection + test suite count |
| AC-05 | Falls back gracefully when no trade history: `gate_met: false, trade_count: 0` | Test with empty trade history |

**Spec references:** `docs/specs/arc2/setup_quality_score_spec.md` (authored in ST-03)

---

### ST-05 — Setup Quality Score frontend display

**Owner:** Head of Engineering
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous
**Sprint:** 2
**Dependencies:** ST-04 (API endpoint), ST-03 (display spec)

**Objective:** Integrate Setup Quality Score into the Pre-Trade Research View. Display score badge, band label, and factor breakdown per ST-03 spec.

**Acceptance Criteria:**

| AC-ID | Criterion | Verification |
|-------|-----------|-------------|
| AC-01 | Score badge visible in Pre-Trade Research View when gate_met: true — shows score (0–100) and band (Weak/Acceptable/Strong) with colour coding | Playwright test |
| AC-02 | Tooltip on score badge shows factor breakdown (regime_match_pct, signal_alignment, atr_proximity, entry_timing) | Playwright test |
| AC-03 | When gate_met: false or score null: advisory message "Setup Quality Score requires 20+ closed trades" shown in place of score | Playwright test |
| AC-04 | No regression in other Pre-Trade Research View sections | Playwright regression |

**Spec references:** `docs/specs/frontend/pages/pre_trade_research.md §Setup Quality Score` (authored in ST-03)

---

## EPIC-03 — QA, Spec & UX Debt Clearance

**Maps to:** S2-03
**Owner:** QA & Testing Owner (ST-06), API Contracts & Documentation Owner (ST-07), Head of UX & Design (ST-08)
**Risk IDs:** RISK-03
**Sprint:** Sprint 1
**Estimated effort:** S (~1 day total)

Three aged backlog items (2–3 cycles deferred) cleared in one focused EPIC.

---

### ST-06 — SC-RV-18 and SC-RV-19 Playwright coverage

**Owner:** QA & Testing Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Sprint:** 1
**Dependencies:** None
**Closes:** BLG-FE-32, TEST-GAP-EPIC-03-v33

**Objective:** Add explicit Playwright tests for research view null state scenarios SC-RV-18 (regime field null) and SC-RV-19 (all fields null — degraded mode). Update scenario library and regression protocol.

**Acceptance Criteria:**

| AC-ID | Criterion | Verification |
|-------|-----------|-------------|
| AC-01 | SC-RV-18 added to `docs/qa/test_scenarios/research_view_scenarios.md`: GET /research/{ticker} returns regime=null → regime panel shows "unavailable" state; no crash | Playwright test in tests/e2e/pre-trade-research.spec.js |
| AC-02 | SC-RV-19 added: all data fields null (all sources failed) → degraded mode; all sections show placeholders; no crash; user-visible error state per UX spec | Playwright test in tests/e2e/pre-trade-research.spec.js |
| AC-03 | `docs/qa/acceptance_protocols/research_view_protocol.md §2.3` updated to reference both scenarios as filed | Protocol file updated; staging caveat removed |
| AC-04 | `docs/qa/acceptance_protocols/research_view_regression_protocol.md §2.2` updated to reflect Playwright coverage (remove staging-only caveat) | Protocol file updated |
| AC-05 | Both new tests pass in CI | CI green |

**Spec references:** `docs/specs/api_contracts/research_endpoint.md`, `docs/qa/test_scenarios/research_view_scenarios.md`

---

### ST-07 — Research endpoint HTTP error code differentiation

**Owner:** API Contracts & Documentation Owner + Head of Engineering
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Sprint:** 1
**Dependencies:** None
**Closes:** BLG-SPEC-27

**Objective:** Update GET /research/{ticker} to return 404 when ticker does not exist in any source, and 503 when a critical external source (Yahoo Finance) is entirely unavailable. Current implementation always returns 200 with null sub-fields.

**Acceptance Criteria:**

| AC-ID | Criterion | Verification |
|-------|-----------|-------------|
| AC-01 | GET /research/{ticker} returns 404 when ticker lookup fails across all data sources | Integration test with non-existent ticker |
| AC-02 | GET /research/{ticker} returns 503 when Yahoo Finance (critical source) is entirely unavailable (not partial field-level failure) | Mock test: Yahoo source timeout/error → 503 |
| AC-03 | Partial source failure (one source down, others up) still returns 200 with null sub-fields for failed source — no change to existing partial-failure behaviour | Regression test |
| AC-04 | `docs/specs/api_contracts/research_endpoint.md §Error Responses` updated to reflect new HTTP codes | Spec file updated; Head of Specs Team review |
| AC-05 | openapi.yaml 4xx/5xx response entries updated for this endpoint | openapi.yaml updated in same commit |
| AC-06 | No regression in frontend research view (404 and 503 handled gracefully — show appropriate error state) | Playwright test |

**Spec references:** `docs/specs/api_contracts/research_endpoint.md §Error Responses`

---

### ST-08 — Research page UX fix: regime lozenge and font consistency

**Owner:** Head of UX & Design
**Estimated effort:** XS (~0.25 day)
**Delegation class:** autonomous
**Sprint:** 1
**Dependencies:** None
**Closes:** BLG-FE-26

**Objective:** Fix research page UX issues identified in v3.2 staging: regime lozenge wrapping to two lines; font inconsistency against design system.

**Acceptance Criteria:**

| AC-ID | Criterion | Verification |
|-------|-----------|-------------|
| AC-01 | Regime lozenge constrained to single line (max-width or text truncation applied); no two-line wrapping at standard viewport widths (1280px, 1440px) | Playwright visual check or human staging |
| AC-02 | Font usage on Research page conforms to `docs/frontend/design_system.md` typography scale — weights and sizes match documented spec | Human staging: side-by-side comparison with design_system.md |
| AC-03 | No regression in other Research page sections | Playwright regression |

**Spec references:** `docs/frontend/design_system.md`

---

## EPIC-04 — Governance Maintenance

**Maps to:** S2-04
**Owner:** Head of Specs Team
**Risk IDs:** None
**Sprint:** Sprint 1 (priority)
**Estimated effort:** XS–S (~0.5 day total)

Four execution_prompt.md patches deferred from v3.5 lessons learnt (all owned by Head of Specs Team, all targeted v3.6). Plus 4 missing prompt_change_log.md entries (OA-RP-01–04).

---

### ST-09 — execution_prompt.md §13 gate story pattern formalisation

**Owner:** Head of Specs Team
**Estimated effort:** XS (~0.25 day)
**Delegation class:** autonomous
**Sprint:** 1
**Dependencies:** None

**Objective:** Formalise the §13 gate story pattern in execution_prompt.md (or release_planning_prompt.md): "When an arc feature requires §13 review, scope the review as a Sprint 1 story (delegated_decision) gating implementation stories in Sprint 2." This pattern was proven effective in v3.5 ST-01 (IT-06).

**Acceptance Criteria:**

| AC-ID | Criterion | Verification |
|-------|-----------|-------------|
| AC-01 | execution_prompt.md (or release_planning_prompt.md) contains explicit guidance for §13 gate story pattern — Sprint 1 delegated_decision story scoping rule documented | File updated; section present |
| AC-02 | Prompt version bumped; OPERATIONAL_GUIDE.md §14 updated to match | Version + guide updated |
| AC-03 | prompt_change_log.md entry appended for the bumped prompt | Change log entry present |
| AC-04 | Missing change log entries for OA-RP-01–04 added to prompt_change_log.md: sprint_planning_prompt.md v3.0→v3.1, execution_prompt.md v3.18→v3.20, delivery_verification_prompt.md v2.1→v2.2, backlog_management_prompt.md v1.6→v1.7 | 4 entries added |

**Spec references:** v3.5 lessons_learnt_closure.md deferred action #1; run manifest OA-RP-01–04

---

### ST-10 — execution_prompt.md metadata + sprint_close + Phase 3 patches

**Owner:** Head of Specs Team
**Estimated effort:** XS–S (~0.25 day)
**Delegation class:** autonomous
**Sprint:** 1
**Dependencies:** ST-09 (same file — must be same commit or sequential)

**Objective:** Apply three remaining execution_prompt.md patches from v3.5 LL deferred actions 2–4:
1. §3.1.A: Add guidance to set `deviations_filed = true` after step 10 deviation check regardless of findings (true = check completed; false = check not yet run)
2. §5.3 sprint close template: add three-field verification readiness block (`All spec references populated: Yes/No`, `All deviations filed: Yes/No`, `QA evidence logs complete: Yes/No`)
3. §5.4: Add explicit reference to `lessons_learnt_cycle.md` Phase 3 section append as mandatory pre-sprint-close step

**Acceptance Criteria:**

| AC-ID | Criterion | Verification |
|-------|-----------|-------------|
| AC-01 | execution_prompt.md §3.1.A: guidance added — `deviations_filed = true` means "check completed"; story completion template updated | File updated; guidance present |
| AC-02 | execution_prompt.md §5.3 sprint_close template: three-field verification readiness block present — `All spec references populated: Yes/No`, `All deviations filed: Yes/No`, `QA evidence logs complete: Yes/No` | Block present in template |
| AC-03 | execution_prompt.md §5.4 (or equivalent): explicit reference to lessons_learnt_cycle.md Phase 3 section append as mandatory pre-sprint-close step | Reference present |
| AC-04 | Prompt version bumped (coordinated with ST-09 — single version bump if same commit); OPERATIONAL_GUIDE.md §14 updated | Version + guide consistent |
| AC-05 | prompt_change_log.md entry appended (coordinated with ST-09) | Entry present |

**Spec references:** v3.5 lessons_learnt_closure.md deferred actions #2, #3, #4
