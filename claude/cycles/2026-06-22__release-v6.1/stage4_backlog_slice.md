Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Release: v6.1
Cycle: 2026-06-22__release-v6.1
Last Updated: 2026-06-22

<!-- release-plan-marker: RP:v6.1:2026-06-22__release-v6.1 -->

---

# Stage 4 Backlog Slice — v6.1 Governance Correctness, CI Quality & User Value Foundation

---

## EPIC-01 — Governance Prompt Correctness (Correctness Fast-Track)

**Maps to:** S2-01 (BLG-GOV-132), S2-02 (BLG-GOV-133), S2-05 (BLG-GOV-131)
**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** ~5 hrs (3×S)
**Risk IDs:** RISK-01
**Execution sequence:** 1st — Correctness Fast-Track; governance prompt patches must precede sprint planning for this cycle

**Epic description:** Patch the release planning and sprint planning engines to enforce design gate detection and hard gate enforcement, closing the process gaps exposed in v6.0. Also deliver the governance overhead ceiling metric proposal to surface Skill-Silo and Product Value Alert patterns before they compound across cycles.

---

### ST-01 — Release planning: Design Gate Required flag

**BLG-ID:** BLG-GOV-132
**EPIC:** EPIC-01
**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous (prompt edit; well-defined scope)
**Dependencies:** None
**Staging-only ACs:** None (all ACs verifiable by inspection and manual trigger of release planning engine)

**Acceptance Criteria:**
- AC-01: STEP 4 of release_planning_prompt.md scans backlog slice items for UI-facing scope (delegated_frontend, autonomous with observable UI ACs) and classifies cycle as design_gate_required = true or false
- AC-02: design_gate_required = true → release planning output includes prominent advisory "⚠ DESIGN GATE REQUIRED before plan sprint — N items classified as UI-facing. Run: run design-gate --cycle <cycle_id>"
- AC-03: design_gate_required = false → output includes "Design Gate: Not Required — proceed directly to plan sprint"
- AC-04: cycle/state.json and .claude_current_state.json updated with design_gate_required field at STEP 4 completion
- AC-05: cycle_summary.md header includes design_gate_required status line
- AC-06: release_planning_prompt.md version bumped; §14 OPERATIONAL_GUIDE.md and prompt_change_log.md updated in same commit per §6 governance edit checklist

**Spec references:** release_planning_prompt.md (current v2.37); CLAUDE.md §6 governance edit checklist; docs/specs/api_contracts/ (none required)

---

### ST-02 — Sprint planning: Design Gate hard gate at preflight

**BLG-ID:** BLG-GOV-133
**EPIC:** EPIC-01
**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous (prompt edit; well-defined scope)
**Dependencies:** None (can execute in parallel with ST-01 or after; no runtime dependency)
**Staging-only ACs:** None

**Acceptance Criteria:**
- AC-01: STEP -1.3 of sprint_planning_prompt.md checks design_gate_status when entering from Release_Planning_Complete with design_gate_required = true; if design_gate_status ≠ Passed AND bypass fields empty → hard gate fires, halt report output, status = Blocked
- AC-02: Bypass path: design_gate_bypass_authority + design_gate_bypass_reason both populated → proceeds with bypass acknowledgement appended to sprint planning notes (not silent)
- AC-03: Pass path: design_gate_status = Passed → proceeds normally; gate check logged as "Design gate: Passed"
- AC-04: design_gate_required = false → gate check skipped; noted "Design gate: Not Required for this cycle"
- AC-05: sprint_planning_prompt.md version bumped; §14 OPERATIONAL_GUIDE.md and prompt_change_log.md updated in same commit per §6 checklist

**Spec references:** sprint_planning_prompt.md (current v3.10); shared_standards.md §10.1; CLAUDE.md §6

---

### ST-03 — Governance overhead ceiling metric and accountability mechanism

**BLG-ID:** BLG-GOV-131
**EPIC:** EPIC-01
**Owner:** PMO Lead; Head of Specs Team
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous (proposal document + draft amendment; no prompt patch without sign-off)
**Dependencies:** None
**Staging-only ACs:** None

**Acceptance Criteria:**
- AC-01: Governance overhead ceiling metric defined: G+D+P% over a rolling 5-cycle window (matching STEP 2.4 window), alert threshold ≥ 60% as initial proposal
- AC-02: Proposal document produced at `docs/product/decisions/gov_overhead_ceiling_proposal_v6.1.md` for Head of Specs Team and PMO Lead review
- AC-03: Draft amendment to roadmap_prompt.md STEP 2 included in proposal document (implementation requires Head of Specs Team sign-off per §6 before any prompt file is modified)
- AC-04: Proposal document includes prior 5-cycle G+D+P% data to establish baseline

**Spec references:** roadmap_prompt.md §2.4 (rolling-window rebalance gate); CLAUDE.md §6 governance edit checklist

---

## EPIC-02 — CI Quality & Baseline Hygiene

**Maps to:** S2-03 (BLG-QA-60), S2-07 (BLG-OPS-73)
**Owner:** Director of Quality; Infrastructure & Operations Owner
**Estimated effort:** ~2 hrs (2×XS)
**Risk IDs:** RISK-02
**Execution sequence:** 2nd — no hard dependency on EPIC-01; advisory ordering

**Epic description:** Register two missing Playwright spec files in the CI playwright.yml workflow (closing a CI gap exposed in v6.0 EPIC-04 merge gate), and add the missing PATCH /trades/{id}/costs baseline entry to api_performance_baseline.md (post-ship ops hygiene from v6.0 delivery).

---

### ST-04 — Register morning-briefing.spec.js and screener-quality.spec.js in playwright.yml

**BLG-ID:** BLG-QA-60
**EPIC:** EPIC-02
**Owner:** Director of Quality; Head of Engineering
**Estimated effort:** XS (<1 hour)
**Delegation class:** autonomous (CI file edit; well-defined)
**Dependencies:** None
**Staging-only ACs:** None

**Acceptance Criteria:**
- AC-01: `tests/e2e/morning-briefing.spec.js` added to the `npx playwright test` command in `.github/workflows/playwright.yml`
- AC-02: `tests/e2e/screener-quality.spec.js` added to the same command in playwright.yml
- AC-03: Spec inventory comment block in playwright.yml updated to list both new files (total spec count updated)
- AC-04: CI `Playwright E2E Acceptance Tests` job passes with new specs included (confirmed via CI run or PR check)

**Spec references:** `.github/workflows/playwright.yml`; `tests/e2e/morning-briefing.spec.js`; `tests/e2e/screener-quality.spec.js`

---

### ST-05 — Add PATCH /trades/{id}/costs to api_performance_baseline.md

**BLG-ID:** BLG-OPS-73
**EPIC:** EPIC-02
**Owner:** Infrastructure & Operations Owner
**Estimated effort:** XS (<1 hour)
**Delegation class:** autonomous (ops measurement + doc update)
**Dependencies:** PATCH /trades/{trade_id}/costs endpoint live in production (v6.0, confirmed)
**Staging-only ACs:** None (measurement from live endpoint; doc update verifiable by inspection)

**Acceptance Criteria:**
- AC-01: PATCH /trades/{id}/costs entry added to `docs/ops/api_performance_baseline.md` with p50, p95, and measurement date
- AC-02: Measurement taken from Render internal logs or live test per §19 methodology in api_performance_baseline.md
- AC-03: Entry format consistent with existing baseline rows

**Spec references:** `docs/ops/api_performance_baseline.md`; `docs/reference/openapi.yaml` line 1571 (endpoint reference)

---

## EPIC-03 — User Value Features

**Maps to:** S2-04 (BLG-FE-76), S2-06 (BLG-FE-78)
**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Estimated effort:** ~10 hrs (M + S)
**Risk IDs:** RISK-03
**Execution sequence:** 3rd — After Design Gate passes (hard gate for BLG-FE-76)

**Epic description:** Deliver two user-facing features: a portfolio sector heat-map to surface sector concentration risk visually, and a trade gate proximity indicator to make the PT-04/SI-02 gate count visible on the dashboard without SQL queries.

---

### ST-06 — Portfolio sector heat-map visualization

**BLG-ID:** BLG-FE-76
**EPIC:** EPIC-03
**Owner:** Product Owner; Frontend Specs & UX Documentation Owner; Head of UX & Design
**Estimated effort:** M (~2–3 days)
**Delegation class:** delegated_frontend (new component; requires design gate sign-off before implementation)
**Dependencies:** Design Gate sign-off (head of UX & Design + Product Owner) — hard gate; EPIC-03 may not start before Design Gate passes
**Staging-only ACs:** None (all ACs verifiable in CI via Playwright)

**Acceptance Criteria:**
- AC-01: `SectorHeatMap.js` component visible on Portfolio or Dashboard page (placement determined by Design Gate)
- AC-02: Each sector displays: name, position count, exposure % of portfolio
- AC-03: Concentration alert (> 40% in one sector) highlighted visually (colour/threshold per design gate sign-off)
- AC-04: Backend endpoint delivers sector weights derived from existing positions data + ticker sector_name field (no new data provider)
- AC-05: Playwright E2E coverage: at least one sector concentration scenario (≥1 position per sector) renders correctly; empty portfolio state handled
- AC-06: New backend endpoint registered in backend/routers/test.py and openapi.yaml in same commit per CLAUDE.md non-negotiables

**Spec references:** Design Gate record (to be created by run design-gate); `GET /portfolio/sector-weights` (endpoint spec TBD at Design Gate)

---

### ST-07 — Trade gate proximity indicator on dashboard

**BLG-ID:** BLG-FE-78
**EPIC:** EPIC-03
**Owner:** Head of Frontend Engineering; Head of UX & Design
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous (reads existing endpoint; display-only)
**Dependencies:** GET /portfolio/gate-metrics endpoint live (v5.5, BLG-BE-34, confirmed); placement decision via Design Gate (advisory — BLG-FE-78 may proceed autonomously if design decision is display-only)
**Staging-only ACs:** None

**Acceptance Criteria:**
- AC-01: Dashboard or system status page shows current closed-trade count vs 20-trade gate threshold (format: `[N]/20 trades (PT-04/SI-02 gate)`)
- AC-02: Display updates on page refresh using existing GET /portfolio/gate-metrics endpoint
- AC-03: Shows "Gate cleared" state when count ≥ 20
- AC-04: Playwright coverage: indicator renders with at least one trade count; "Gate cleared" state tested

**Spec references:** `GET /portfolio/gate-metrics` (BLG-BE-34, v5.5 contract)

---

## EPIC-04 — Conditional: Setup Quality Score (PT-04)

**Maps to:** S2-08 (BLG-FEAT-25)
**Owner:** Head of Backend Engineering; Head of UX & Design; Metrics & Analytics Owner
**Estimated effort:** ~12 hrs (M conditional)
**Risk IDs:** RISK-04
**Execution sequence:** 4th — conditional; sprint planning gate check required before entering firm capacity

**Epic description:** Deliver the Setup Quality Score (PT-04) — a 0–100 deterministic score derived from own trade history matching current regime/signal/ATR conditions. Backend endpoint + frontend display in Pre-Trade Research View and Trade Plan form. Conditional on ≥20 closed trades confirmed by PMO Lead at sprint planning.

**Gate condition:** ≥20 closed trades in production (trade_history WHERE pnl IS NOT NULL). Current count: 13 (2026-06-16). Projected clear: ~2026-07-02. PMO Lead must re-verify at sprint planning before EPIC-04 enters firm capacity. If gate not met, EPIC-04 is returned to backlog without sprint impact.

---

### ST-08 — Setup Quality Score — backend engine (PT-04)

**BLG-ID:** BLG-FEAT-25 (backend scope)
**EPIC:** EPIC-04
**Owner:** Head of Backend Engineering; Metrics & Analytics Owner
**Estimated effort:** S (~1–2 days)
**Delegation class:** autonomous (backend; well-specced)
**Classification:** Conditional — gate: ≥20 closed trades (gate clearing estimate ~2026-07-02). May not be included as firm capacity at sprint planning if gate not met.
**Dependencies:** Gate condition met (PMO Lead verification at sprint planning)
**Staging-only ACs:** None

**Acceptance Criteria:**
- AC-01: `GET /trade-plans/setup-quality-score?ticker={ticker}` endpoint implemented
- AC-02: Score (0–100) computed from closed trade history matching current regime/signal/ATR conditions
- AC-03: Gate response: `{"gate_not_met": true, "min_trades_required": 20}` when fewer than 20 closed trades
- AC-04: Score factors included in response: matching_trades, win_rate, average_R, score_explanation
- AC-05: Endpoint registered in backend/routers/test.py and openapi.yaml in same commit (per CLAUDE.md non-negotiable)
- AC-06: Unit tests cover gate_not_met case, gate_met with mixed history, and perfect-history case

**Spec references:** BLG-FEAT-25 scope (Backend — ST-04 original spec); strategy_rules.md §4.1; docs/specs/api_contracts/

---

### ST-09 — Setup Quality Score — frontend display (PT-04)

**BLG-ID:** BLG-FEAT-25 (frontend scope)
**EPIC:** EPIC-04
**Owner:** Head of UX & Design; Head of Frontend Engineering
**Estimated effort:** S (~1–2 days)
**Delegation class:** autonomous (frontend; existing patterns)
**Classification:** Conditional — gate: ≥20 closed trades (gate clearing estimate ~2026-07-02). May not be included as firm capacity at sprint planning if gate not met.
**Dependencies:** ST-08 (backend endpoint must exist before frontend integration); gate condition met
**Staging-only ACs:** None (Playwright-verifiable in CI once endpoint is live)

**Acceptance Criteria:**
- AC-01: Setup Quality Score displayed in Pre-Trade Research View and Trade Plan form
- AC-02: Score badge with numeric value (0–100) and qualitative label (Excellent ≥80 / Good ≥60 / Fair ≥40 / Low <40)
- AC-03: "Insufficient trade history (< 20 trades)" message clearly displayed when gate not met
- AC-04: Tooltip or expandable detail shows: matching_trades, win_rate, average_R
- AC-05: Score updates when ticker changes (no stale data across tickers)
- AC-06: Playwright coverage: score renders; gate-not-met message renders; score updates on ticker change

**Spec references:** BLG-FEAT-25 scope (Frontend — ST-05 original spec); Pre-Trade Research View existing component patterns
