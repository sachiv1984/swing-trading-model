**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-04-11
**Cycle:** 2026-04-11__release-v2.6
**Release:** v2.6
**Sprint Goal:** Ship v2.6: eliminate Base44 SDK dependencies in Reports and Signals, stand up a runnable CI pytest suite with fee drag coverage, deliver Trade History UX polish per locked design spec, and close carry-forward governance debt patches CF-1 and CF-2 from v2.5.
**Backlog Slice Source:** original `claude/cycles/2026-04-11__release-v2.6/stage4_backlog_slice.md`

---

## Sprint Scope

### Sprint 1

---

#### EPIC-01 — Backend Integration Completion

**Maps to:** S2-01
**Owner:** Head of Engineering + Frontend Specifications & UX Owner
**Estimated effort:** 44h (mid) | 32–56h (range)
**Risk IDs:** RISK-01 (Base44 API contract divergence)
**Execution sequence:** 1

##### ST-01 — Migrate Reports Performance Tab to FastAPI Backend

**Owner:** Head of Engineering
**Estimated effort:** L (~3–5 days)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`
**Dependencies:** None
**Notes:** Integration review in scope — any new Base44/FastAPI gaps discovered during implementation to be filed as backlog items per RISK-01 mitigation.

---

##### ST-02 — Wire Signals Page Dismissal and Position Creation to FastAPI

**Owner:** Head of Engineering
**Estimated effort:** M (~1–2 days)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`
**Dependencies:** None (ST-01 integration pattern may inform approach; not a hard dependency)
**Notes:** Signal state and positions must reach the authoritative database — no Base44 mutation calls may remain for these operations.

---

##### ST-03 — Replace Base44 Cash Balance on Signals Page with GET /cash/summary

**Owner:** Head of Engineering
**Estimated effort:** XS (<1 hour)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`
**Dependencies:** None
**Notes:** XS item — may be bundled with ST-02 commit where appropriate.

---

#### EPIC-02 — Test Automation & CI Hardening

**Maps to:** S2-02
**Owner:** QA & Testing Owner + Infrastructure & Operations Owner
**Estimated effort:** 21h (mid) | 15–27h (range)
**Risk IDs:** RISK-02 (CI env configuration complexity)
**Execution sequence:** 2

##### ST-04 — Fix 4 Pytest Collection Errors

**Owner:** QA & Testing Owner
**Estimated effort:** S (~2–3 hours)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`
**Dependencies:** None — prerequisite for ST-05 Phase B
**Notes:** Must complete before ST-05 Phase B and before ST-06/ST-07 CI validation. Three specific fixes defined in AC: `API_TITLE`, `update_position` stub, `tests/conftest.py` DATABASE_URL.

---

##### ST-05 — Add CI Test Runner Workflow

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S (~1 hour)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`
**Dependencies:** ST-04 (for Phase B); Phase A runnable immediately
**Notes:** Phase A (clean tests only) unblocked. Phase B (all tests) requires ST-04 collection errors fixed first. Deliberate failure test required in AC.

---

##### ST-06 — Fee Drag Playwright Spec

**Owner:** QA & Testing Owner
**Estimated effort:** M (~1–2 days)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`
**Dependencies:** None (mock pattern from `slippage-tracking.spec.js` is the template)
**Notes:** SC-FEE-01 through SC-FEE-04. `fee-drag-scenarios.md` must be updated with spec file path.

---

##### ST-07 — Fee Drag Backend Pytest Unit Tests

**Owner:** QA & Testing Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`
**Dependencies:** None (run after ST-04 for clean CI integration)
**Notes:** SC-FEE-05 and SC-FEE-06. `sys.modules` stub pattern required — no live DB calls.

---

### Sprint 2

---

#### EPIC-03 — Frontend UX Polish

**Maps to:** S2-03
**Owner:** Frontend Specifications & UX Owner + Head of UX & Design
**Estimated effort:** 17h (mid) | 13–20h (range)
**Risk IDs:** RISK-03 (resolved — design gate cleared 2026-04-11)
**Execution sequence:** 3
**Spec lock:** `docs/specs/frontend/pages/trade_history.md` v1.6 (design gate 2026-04-11)

##### ST-08 — StatsCard Tooltip Prop

**Owner:** Frontend Specifications & UX Owner
**Estimated effort:** XS (<1 hour)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`
**Dependencies:** None — foundational; Avg Fee Drag tooltip wiring in ST-09 builds on this
**Notes:** Tooltip text for Avg Fee Drag defined in `trade_history.md` v1.6 §Avg Fee Drag. No regression to existing StatsCard usage.

---

##### ST-09 — Trade History StatsCard Bar Layout (6-Card Width)

**Owner:** Frontend Specifications & UX Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`
**Dependencies:** ST-08 (Avg Fee Drag card needs tooltip wiring before layout is tested)
**Notes:** Design decision resolved — `grid-cols-7` at `xl` (≥1280px), `grid-cols-4` at `md`. Spec: `trade_history.md` v1.6 §Summary Stats Bar Layout.

---

##### ST-10 — Trade History Column Header Styling and Formatting

**Owner:** Frontend Specifications & UX Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`
**Dependencies:** None
**Notes:** Trade History-specific override only. Target: `text-xs font-semibold text-slate-300 uppercase tracking-wide`. Spec: `trade_history.md` v1.6 §Column Header Styling.

---

##### ST-11 — Flexible Column Sorting Across Trade History Table

**Owner:** Frontend Specifications & UX Owner
**Estimated effort:** M (~1–2 days)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`
**Dependencies:** None (sort infrastructure fixed in v2.5)
**Notes:** 8 sortable columns; Exit Date descending as default sort. Non-sortable: Ticker, Market flag, Shares, Entry/Exit price, Exit reason. Spec: `trade_history.md` v1.6 §Sortable Columns.

---

#### EPIC-04 — Governance & Spec Debt

**Maps to:** S2-04
**Owner:** Head of Specs Team
**Estimated effort:** 16h (mid) | 12–20h (range)
**Risk IDs:** RISK-04 (§6 compliance for 3-engine patch)
**Execution sequence:** 4

##### ST-12 — execution_prompt.md STEP 5.1 Unpushed-Commit Check

**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`
**Dependencies:** None
**Notes:** CF-1 from v2.5 lessons_learnt_closure. CLAUDE.md §6 checklist applies — version bump, OPERATIONAL_GUIDE §14 update, prompt_change_log.md entry required in same commit.

---

##### ST-13 — Prompt Log Hygiene: §6 Edit Reminders for 3 Engines

**Owner:** Head of Specs Team
**Estimated effort:** M (~1–2 days)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`
**Dependencies:** None (logically independent; sequencing after ST-12 recommended as ST-13 patches design_gate_prompt.md which this cycle used)
**Notes:** CF-2 from v2.5 lessons_learnt_closure. Touches 3 governance files: design_gate_prompt.md, amendment_cycle_prompt.md, roadmap_prompt.md. CLAUDE.md §6 checklist applies to all 3.

---

##### ST-14 — Upgrade decision_log.md Hard Gate in roadmap_prompt.md

**Owner:** Head of Specs Team
**Estimated effort:** M (~0.5–1 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`
**Dependencies:** None
**Notes:** BLG-GOV-15. Hard gate upgrade (halt on line count decrease) — not just an assertion. CLAUDE.md §6 checklist applies to roadmap_prompt.md + OPERATIONAL_GUIDE.md.

---

##### ST-15 — Frontend Performance Budget Spec

**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`
**Dependencies:** None
**Notes:** BLG-FE-09. Documentation-only spec at `docs/specs/frontend/performance_budget.md`. No code instrumentation in scope. Targets aligned to BLG-OPS-05 API latency floor.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~110h (mid, 2-sprint) |
| Total estimated effort (in-scope) | 98h (mid) |
| Utilisation | ~89% |
| Over-allocation | No |

## Items Deferred This Sprint

None — all 15 items from the backlog slice are included.

## Deferred Execution Blockers Accepted

N/A — `deferred_execution_blockers` was empty at release plan publish.

## Outstanding Actions at Planning Seal

None.

---

## Product Owner Sign-Off

**Sprint goal confirmed:** confirmed — 2026-04-11
**Scope confirmed:** confirmed — all 15 items, 4 EPICs, within 2-sprint capacity ✅
**Capacity confirmed:** confirmed — mid 98h / ~110h capacity, PASS ✅
**Deferred execution blockers accepted:** N/A
**Signed off by:** Product Owner
**Date:** 2026-04-11
