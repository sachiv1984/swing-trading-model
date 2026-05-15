**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v3.5
**Cycle:** 2026-05-15__release-v3.5
**Last Updated:** 2026-05-15

---

# Backlog Slice — v3.5 Arc 3 Completion + Arc 4 Foundation

---

## EPIC-01 — Arc 3 Completion: Alpaca Paper Trading Integration (IT-06)

**Maps to:** S2-01
**Owner:** Head of Engineering
**Sprint:** Sprint 1 (§13 review ST-01) + Sprint 2 (implementation ST-02/03, conditional)
**Risk:** RISK-01 (§13 gate — implementation conditional on §13 PASS)

**Description:** Complete Arc 3 by delivering IT-06 — mirroring US market positions to Alpaca paper account for tracking against real market conditions without real capital. §13 compliance review is mandatory prerequisite before any implementation begins. If §13 review yields FAIL, EPIC-01 scope reduces to ST-01 only.

---

### ST-01 — §13 Compliance Review: Alpaca Paper Trading

**EPIC:** EPIC-01
**Sprint:** Sprint 1 (must be first story in EPIC-01)
**Effort:** XS (~0.25 day)
**Owner:** Strategy Rules & System Intent Owner
**Gate:** This story must complete (PASS or FAIL) before any IT-06 implementation story begins.

**Description:** Conduct a formal §13 compliance review to determine whether IT-06 (Alpaca Paper Trading Integration) is within system bounds per `claude/strategy/strategy_rules.md §13`. Paper trading connects to Alpaca execution infrastructure and must not constitute an automated trading capability.

**Acceptance Criteria:**
- AC-1: Review conducted against `strategy_rules.md §13.1` (what the system is), §13.2 (what it is not), and §13.3 (boundary rationale).
- AC-2: Written determination produced: "PASS — paper trading is within §13 bounds because [rationale]" OR "FAIL — paper trading violates §13 because [rationale]".
- AC-3: Determination filed as `docs/product/decisions/decisions--2026-05-15__release-v3.5--IT-06-section13-review.md`.
- AC-4: If PASS: determination document notes specific §13 conditions that apply (e.g., no automated order execution, positions created only by human action, paper account is tracking-only not execution-capable).
- AC-5: If FAIL: EPIC-01 implementation stories (ST-02, ST-03) are removed from scope; closure note added to IT-06 roadmap entry; backup scope confirmed with PMO Lead.
- AC-6: Strategy Rules & System Intent Owner sign-off recorded in determination document.

---

### ST-02 — IT-06 Backend: Alpaca Paper Trading Sync Service

**EPIC:** EPIC-01
**Sprint:** Sprint 2
**Effort:** M (~2–3 days)
**Owner:** Head of Engineering
**Prerequisite:** ST-01 PASS
**Conditional:** Story active only if ST-01 yields PASS determination.

**Description:** Backend service to mirror US market positions to an Alpaca paper trading account. Positions are created in the paper account when a US market position is opened in the system (user action). Positions are updated/closed in the paper account when the system position is updated/closed.

**Acceptance Criteria:**
- AC-1: New service `backend/services/alpaca_paper_sync_service.py` handles paper account sync for US market positions.
- AC-2: `POST /positions` and `PATCH /positions/{id}` and position close operations trigger paper account sync for US-market tickers only.
- AC-3: Sync is best-effort — failure to sync to Alpaca does not block the primary position operation; errors logged but not surfaced as blocking errors to user.
- AC-4: Alpaca credentials managed via environment variable (`ALPACA_PAPER_API_KEY`, `ALPACA_PAPER_SECRET_KEY`); paper account endpoint distinct from live account endpoint.
- AC-5: `GET /portfolio/paper-positions` endpoint returns current Alpaca paper account positions with P&L comparison vs system positions.
- AC-6: Integration test covers: US position creation → paper sync; non-US position creation → no sync; sync failure → position created anyway.
- AC-7: `docs/reference/openapi.yaml` updated with `GET /portfolio/paper-positions` in same commit.
- AC-8: New endpoint added to `backend/routers/test.py` and `SystemStatus.js` fallback count updated (+1) with `SC-SS-01b` updated in same commit.
- AC-9: §13 compliance note added to service file: "Paper trading integration is §13 compliant — positions created by human action only; no automated order execution."

---

### ST-03 — IT-06 Frontend: Paper Positions Display Panel

**EPIC:** EPIC-01
**Sprint:** Sprint 2
**Effort:** M (~2 days)
**Owner:** Head of Engineering
**Prerequisite:** ST-02
**Conditional:** Story active only if ST-01 yields PASS determination.

**Description:** Frontend panel displaying Alpaca paper account positions alongside system positions for US market tickers. Surfaces hypothetical P&L tracking against real market conditions.

**Acceptance Criteria:**
- AC-1: Paper positions panel visible on Positions page (US market positions section) when `ALPACA_PAPER_API_KEY` is configured.
- AC-2: Panel displays: ticker, paper entry price, current market price, paper P&L ($ and %), date opened, position size.
- AC-3: Panel header labels clearly as "Paper Account" to distinguish from real positions.
- AC-4: When Alpaca paper credentials not configured, panel is hidden (no empty error state visible to user).
- AC-5: When sync is active but paper data unavailable (Alpaca API error), panel shows "Paper tracking temporarily unavailable" — does not break Positions page.
- AC-6: UX spec `docs/ux_specs/paper-trading/ux_spec.md` created and signed off by Head of UX & Design before this story begins.
- AC-7: Playwright E2E test covers: panel visible with mock data; panel hidden when not configured.

---

## EPIC-02 — Arc 4 Foundation: Plan vs Reality Analysis (PO-01)

**Maps to:** S2-02
**Owner:** Head of Engineering
**Sprint:** Sprint 2
**Risk:** RISK-02 (capacity — H effort alongside IT-06), RISK-03 (data density — PO-01 most useful once trade plan data exists)

**Description:** Begin Arc 4 by delivering: (a) Arc 4 data requirements capture document (BLG-GOV-21) as prerequisite, then (b) PO-01 Plan vs Reality Analysis — structured comparison of trade plan vs actual outcome, displayed at trade close. Requires PT-01 live (✅ v3.1) and position lifecycle data (✅ v3.3–v3.4).

---

### ST-04 — BLG-GOV-21: Arc 4 Data Requirements Capture

**EPIC:** EPIC-02
**Sprint:** Sprint 2 (first story in EPIC-02; must precede ST-05)
**Effort:** S (~0.5 day)
**Owner:** Head of UX & Design + Product Owner

**Description:** Lightweight document capturing data points not currently stored in the system that Arc 4 features (PO-01 through PO-05) will require. This is a data needs capture only — not a feature specification, UX design, or implementation commitment.

**Acceptance Criteria:**
- AC-1: Document `docs/product/arc4_data_requirements.md` created.
- AC-2: Each entry specifies: field name, purpose, data type, source (user input / calculated / external), and why it cannot be derived from existing data.
- AC-3: Document covers: AI context inputs, qualitative annotations (user-authored), pre-entry state snapshots, plan vs reality comparison fields.
- AC-4: Document explicitly notes: "This document is not a feature specification or implementation commitment. It is a reference input for Arc 4 sprint planning."
- AC-5: Product Owner + Head of UX & Design sign-off recorded in document.
- AC-6: BLG-GOV-21 marked as resolved in backlog.

---

### ST-05 — PO-01 Backend: Plan vs Reality Calculation Service

**EPIC:** EPIC-02
**Sprint:** Sprint 2
**Effort:** M–H (~3–4 days)
**Owner:** Head of Engineering
**Prerequisite:** ST-04

**Description:** Backend calculation service comparing trade plan (PT-01) against actual trade outcome for closed positions. Produces a structured `plan_vs_reality` record attached to each closed position that has a trade plan.

**Acceptance Criteria:**
- AC-1: New data model field `plan_vs_reality` (JSONB) added to `trades` table via migration; linked to `trade_plans` via `trade_id`.
- AC-2: Calculation service `backend/services/plan_vs_reality_service.py` computes comparison on position close (or on-demand via endpoint).
- AC-3: Comparison fields calculated: entry timing accuracy (actual entry vs planned entry zone), R achieved vs R target, exit reason alignment (actual vs planned exit conditions), lifecycle state at exit.
- AC-4: `GET /trades/{id}/plan-vs-reality` endpoint returns comparison record for a closed trade with a plan; returns 404 with `{"detail": "No trade plan found for this trade"}` if no plan exists.
- AC-5: `GET /trades/{id}/plan-vs-reality` returns 200 with `{"status": "trade_open"}` if position is still open.
- AC-6: `docs/reference/openapi.yaml` updated with new endpoint in same commit.
- AC-7: New endpoint added to `backend/routers/test.py` and `SystemStatus.js` + `SC-SS-01b` updated in same commit.
- AC-8: `docs/data_model.md` updated to reflect new `plan_vs_reality` field in same commit.

---

### ST-06 — PO-01 Frontend: Plan vs Reality Comparison View

**EPIC:** EPIC-02
**Sprint:** Sprint 2 (phase to v3.6 if Sprint 2 capacity exceeded after IT-06)
**Effort:** M (~2 days)
**Owner:** Head of Engineering
**Prerequisite:** ST-05

**Description:** Frontend display of the plan vs reality comparison, surfaced at trade close in the trade detail view. Empty state graceful when no trade plan exists.

**Acceptance Criteria:**
- AC-1: `PlanVsReality` component renders on closed trade detail page when a plan vs reality record exists.
- AC-2: Component displays: entry timing (planned zone vs actual), R achieved vs R target (with colour coding: green ≥ target, amber within 20%, red < target - 20%), exit alignment (matched / partially matched / diverged), lifecycle state at exit.
- AC-3: When no trade plan exists for a closed trade, component is hidden (no error, no empty placeholder visible).
- AC-4: When trade is still open, component is hidden.
- AC-5: UX spec `docs/ux_specs/plan-vs-reality/ux_spec.md` created and signed off by Head of UX & Design before this story begins.
- AC-6: Playwright E2E test covers: component visible with mock plan vs reality data; component hidden for trade with no plan.

---

## EPIC-03 — Spec & QA Debt

**Maps to:** S2-03
**Owner:** Head of Specs Team
**Sprint:** Sprint 1

**Description:** Clear v3.4 delivery deviation spec corrections and QA documentation debt. All items are documentation/spec only — no implementation changes required for BLG-SPEC-29/30/31.

---

### ST-07 — BLG-SPEC-29: Correct grace-period-alert ux_spec.md sessionStorage

**EPIC:** EPIC-03
**Sprint:** Sprint 1
**Effort:** XS (~0.25 day)
**Owner:** Head of UX & Design

**Acceptance Criteria:**
- AC-1: `docs/ux_specs/grace-period-alert/ux_spec.md` §5 updated to reference `sessionStorage` (not `localStorage`) for dismiss persistence.
- AC-2: §5 note added: "Dismiss resets on tab close; alert reappears in a new browser session."
- AC-3: No implementation change required.
- AC-4: BLG-SPEC-29 marked as resolved in backlog (COMPLETE v3.5).

---

### ST-08 — BLG-SPEC-30: Correct stop-management-workflow ux_spec.md HTTP verb

**EPIC:** EPIC-03
**Sprint:** Sprint 1
**Effort:** XS (~0.25 day)
**Owner:** Head of UX & Design

**Acceptance Criteria:**
- AC-1: `docs/ux_specs/stop-management-workflow/ux_spec.md` §4.4 updated to reference `PATCH /positions/{id}` (not `PUT /positions/{id}`).
- AC-2: No implementation change required.
- AC-3: BLG-SPEC-30 marked as resolved in backlog (COMPLETE v3.5).

---

### ST-09 — BLG-SPEC-31: React Query v5 onSuccess Codebase Scan

**EPIC:** EPIC-03
**Sprint:** Sprint 1
**Effort:** S (~0.5 day)
**Owner:** Head of Engineering

**Acceptance Criteria:**
- AC-1: All `useQuery` calls in `src/` scanned for `onSuccess` usage.
- AC-2: Any `useQuery` calls with `onSuccess` identified and assessed: Is the callback still needed? Has it been silently dropped by React Query v5?
- AC-3: All affected patterns either fixed (refactored to `useEffect` with data dependency) or confirmed as no-ops (documented in a closure note).
- AC-4: If no affected patterns found: closure note filed in backlog entry and BLG-SPEC-31 marked COMPLETE.
- AC-5: If patterns fixed: unit/E2E test coverage added for each fixed component.
- AC-6: BLG-SPEC-31 marked as resolved in backlog.

---

### ST-10 — BLG-QA-19: Research View Regression Test Protocol

**EPIC:** EPIC-03
**Sprint:** Sprint 1
**Effort:** S (~0.5 day)
**Owner:** QA Lead

**Acceptance Criteria:**
- AC-1: `docs/qa/acceptance_protocols/research_view_regression_protocol.md` created.
- AC-2: Protocol defines the canonical list of Playwright test scenarios that must pass after any modification to `GET /research/{ticker}` or research view components.
- AC-3: Protocol covers: PT-02 base fields (ticker, price, ATR, regime, signal), PT-03 entry condition overlay, PT-05 entry checklist UX, null/degraded state handling (SC-RV-18, SC-RV-19).
- AC-4: Protocol explicitly references existing test IDs from `tests/e2e/` that constitute the regression gate.
- AC-5: Protocol cross-referenced in `docs/specs/api_contracts/research_endpoint.md` as regression anchor.
- AC-6: QA Lead sign-off recorded in document.
- AC-7: BLG-QA-19 marked as resolved in backlog (COMPLETE v3.5).

---

## EPIC-04 — Governance Patches

**Maps to:** S2-04
**Owner:** Head of Specs Team
**Sprint:** Sprint 1 (first EPIC — governance patches shipped before execution begins)

**Description:** Deliver all governance prompt patches deferred from v3.4 lessons learnt: sprint_planning_prompt.md execution_state.json ownership rule (BLG-GOV-22), execution_prompt.md deviation-filing advisory patches, and sprint_close / lessons_learnt formatting improvements.

---

### ST-11 — BLG-GOV-22: sprint_planning_prompt.md Shared Ownership Patch

**EPIC:** EPIC-04
**Sprint:** Sprint 1
**Effort:** S (~0.5 day)
**Owner:** Head of Specs Team

**Description:** Patch sprint_planning_prompt.md with shared execution_state.json ownership rule and multi-EPIC Positions.js merge guidance to prevent cross-EPIC merge conflict recurrence (v3.3 + v3.4 recurrence).

**Acceptance Criteria:**
- AC-1: `sprint_planning_prompt.md` updated with rule: "First EPIC branch in execution order creates `execution_state.json`; all subsequent EPIC branches check for file existence before creating — if found, read it and append their EPIC's section rather than overwrite."
- AC-2: `sprint_planning_prompt.md` version bumped; change log entry added to `claude/system/prompt_change_log.md` in same commit.
- AC-3: `OPERATIONAL_GUIDE.md` §14 sprint_planning_prompt.md version updated in same commit.
- AC-4: Sprint backlog template (or sprint_planning_prompt.md §sprint_backlog section) includes: merge order note and explicit shared file ownership advisory for pages shared across EPICs (e.g., `Positions.js`).
- AC-5: Head of Specs Team sign-off recorded.
- AC-6: BLG-GOV-22 marked as resolved in backlog (COMPLETE v3.5).

---

### ST-12 — execution_prompt.md: Deviation Filing Advisory Patches

**EPIC:** EPIC-04
**Sprint:** Sprint 1
**Effort:** S (~0.5 day)
**Owner:** Head of Specs Team

**Description:** Three advisory improvements to execution_prompt.md §3.1.A deviation filing guidance, from v3.4 lessons learnt items #3, #4, #5.

**Acceptance Criteria:**
- AC-1 (LL item #3): `execution_prompt.md` §3.1.A step 10 adds advisory: "Before filing a deviation, verify implementation matches spec *intent*, not just literal draft wording. If spec and implementation agree on intent, record as an implementation note only — do not file a deviation."
- AC-2 (LL item #4): `execution_prompt.md` §3.1.A step 10 adds advisory: "When filing a deviation, also add a Known Deviations section to the canonical spec in the same commit. This shifts work to execution time and reduces verification overhead."
- AC-3 (LL item #5): `execution_prompt.md` §3.3 (or lessons_learnt step for new backlog IDs) adds check: "Before filing new backlog IDs in lessons_learnt Phase 3, verify the ID is unoccupied in `backlog.md`. Query existing IDs before assigning."
- AC-4: `execution_prompt.md` version bumped; change log entry added in same commit.
- AC-5: `OPERATIONAL_GUIDE.md` §14 execution_prompt.md version updated in same commit.
- AC-6: Head of Specs Team sign-off recorded.

---

### ST-13 — Sprint Close / LL Formatting Improvements

**EPIC:** EPIC-04
**Sprint:** Sprint 1
**Effort:** S (~0.5 day)
**Owner:** Head of Specs Team (ST-13a) + PMO Lead (ST-13b)

**Description:** Two governance formatting improvements from v3.4 lessons learnt carry-forward items #6 and #7.

**Acceptance Criteria:**
- AC-1 (LL-v3.3 CF-01 — item #6): Sprint close prompt or execution_prompt.md updated with rule: "Deviations Filed table priority must match DoQ assessment — verify deviation severity consistency between sprint_close.md and DoQ sign-off before closing."
- AC-2 (LL-v3.3 CF-02 — item #7): Sprint close or execution_prompt.md updated with protocol checkbox: "Verify all deviations filed as backlog items have BLG IDs recorded in sprint_close.md before closing. 'Backlog item filed' without a BLG ID is incomplete."
- AC-3: If changes are to execution_prompt.md: version bumped and change log entry added in same commit; OPERATIONAL_GUIDE.md §14 updated in same commit.
- AC-4: If changes are to a different prompt (e.g., post_ship_closure.md): same version/changelog/OG update rules apply.
- AC-5: Head of Specs Team + PMO Lead sign-off recorded.
