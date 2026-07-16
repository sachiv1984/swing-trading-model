**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-07-16
**Cycle:** 2026-07-16__release-v7.3
**Release:** v7.3
**Sprint Goal:** Ship the three carried-forward v7.2 UI implementation stories (Start Trade from Plan, dashboard empty/first-run state coverage, dashboard briefing visual hierarchy) and complete all four v7.4-candidate pre-implementation readiness passes (command palette, custom price alerts incl. §13 pre-check, bulk actions, saved filters/calendar view), so v7.4's next release plan can scope `BLG-FE-115/116/117/118` from a fully de-risked backlog.
**Backlog Slice Source:** original `stage4_backlog_slice.md`

- **EPIC merge sequence:** EPIC-01 → EPIC-02 → EPIC-03 → EPIC-04 → EPIC-05
- **`execution_state.json` owner:** EPIC-01 (first in execution order — EPIC-02/EPIC-03/EPIC-04/EPIC-05 branches must check for existence and append rather than overwrite)
- **Shared files across EPICs:** None identified — see `sprint_planning_notes.md §Multi-EPIC Execution Notes` for the full per-EPIC file ownership breakdown

## Sprint Scope

### EPIC-01 — Dashboard & Trade-Plan UX Implementation (carried from v7.2)

**Maps to:** S2-01, S2-02, S2-03
**Owner:** Head of UX & Design; Base44 Frontend Prompt Owner
**Estimated effort:** 2.75 days (1.5 + 0.75 + 0.5)
**Risk IDs:** RISK-01
**Execution sequence:** 1

#### ST-01 — Trade-plan-to-execution linkage UX ("Start Trade from Plan")

**Owner:** Head of UX & Design; Base44 Frontend Prompt Owner
**Estimated effort:** 1.5 (M)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

*(The Execution Engine reads AC from `stage4_backlog_slice.md` directly via `spec_references`. Do not duplicate the full AC table here — the sprint backlog is a sequencing and ownership document.)*

**Dependencies:** None

**Shared Playwright Spec:** `tests/e2e/v7.2-dashboard-tradeplan-ux-hardening.spec.js` — per `docs/specs/frontend/blg_qa_111_combined_design_review_shared_playwright_plan.md` §3, this story's observable ACs (AC-01) populate the `describe("Start Trade from Plan")` group in this shared file (v7.2 lessons-learnt carry-forward #1, closed this run — see `sprint_planning_notes.md`).

**Notes:** Design gate cleared 2026-07-16 (`design_gate.md`) — classified Design Pre-Approved, prior v7.2 Passed record cited directly, `trade_plan.md` confirmed unchanged since.

**Staging-only ACs:** AC-01 (visible/functional action, element presence/interaction).

---

#### ST-02 — Dashboard empty/first-run state coverage

**Owner:** Head of UX & Design; Base44 Frontend Prompt Owner
**Estimated effort:** 0.75 (S–M)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None (shares `DashboardHome.js` with ST-03 — sequence this story first within EPIC-01 to minimise merge friction, see `sprint_planning_notes.md`)

**Shared Playwright Spec:** `tests/e2e/v7.2-dashboard-tradeplan-ux-hardening.spec.js` — populates the `describe("Dashboard empty states")` group (v7.2 carry-forward #1).

**Notes:** Design gate cleared 2026-07-16 — Design Pre-Approved, `dashboard.md` v3.1 §4A confirmed unchanged since v7.2 gate.

**Staging-only ACs:** AC-01/AC-02 (empty-state rendering, colour/iconography).

---

#### ST-03 — Dashboard briefing visual hierarchy

**Owner:** Head of UX & Design
**Estimated effort:** 0.5 (S)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None (shares `DashboardHome.js` with ST-02 — sequence after ST-02 within EPIC-01, see `sprint_planning_notes.md`)

**Shared Playwright Spec:** `tests/e2e/v7.2-dashboard-tradeplan-ux-hardening.spec.js` — populates the `describe("Dashboard briefing hierarchy")` group (v7.2 carry-forward #1).

**Notes:** Design gate cleared 2026-07-16 — Design Pre-Approved, `dashboard.md` v3.1 §1A/§5 confirmed unchanged since v7.2 gate.

**Staging-only ACs:** AC-01/AC-03 (visual distinction, dual-theme layout).

---

### EPIC-02 — Command Palette Readiness Pass

**Maps to:** S2-04
**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Estimated effort:** 2.5 days
**Risk IDs:** RISK-02
**Execution sequence:** 2

#### ST-04 — Command Palette (BLG-FE-115) pre-implementation spec, prompt template & discoverability/adoption pass

**Owner:** Frontend Specs & UX Documentation Owner; Head of UX & Design
**Estimated effort:** 2.5 (M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** Design gate cleared — Design Pre-Approved (spec-only pass, no UI change; implementing `BLG-FE-115` itself deferred to v7.4).

**Staging-only ACs:** None — documentation/spec pass, no UI to verify visually.

---

### EPIC-03 — Custom Price Alerts Readiness Pass

**Maps to:** S2-05
**Owner:** Data Model & Domain Schema Owner; Backend Engineering Patterns Owner
**Estimated effort:** 3.5 days
**Risk IDs:** RISK-03
**Execution sequence:** 3

#### ST-05 — Custom Price Alerts (BLG-FE-116) pre-implementation readiness pass

**Owner:** Data Model & Domain Schema Owner; Backend Engineering Patterns Owner
**Estimated effort:** 3.5 (L)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Notes:** Highest-priority readiness gate this release (RISK-03). AC-05's §13 pre-check must record PASS or a named follow-up; if a genuine §13 concern surfaces, `BLG-FE-116` may require PO/Strategy Rules Owner scoping before it can enter any future release. Sequenced 3rd (not last) to leave runway for that escalation path within this sprint. Design gate cleared — Design Pre-Approved (spec-only pass, no UI change; implementing `BLG-FE-116` itself deferred to v7.4).

**Staging-only ACs:** None — documentation/design pass, no UI to verify visually.

---

### EPIC-04 — Bulk Actions Readiness Pass

**Maps to:** S2-06
**Owner:** Backend Engineering Patterns Owner; Director of Quality
**Estimated effort:** 2.0 days
**Risk IDs:** RISK-04
**Execution sequence:** 4

#### ST-06 — Bulk Actions (BLG-FE-117) pre-implementation readiness pass

**Owner:** Backend Engineering Patterns Owner; Director of Quality
**Estimated effort:** 2.0 (M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None

**Notes:** Design gate cleared — Design Pre-Approved (spec-only pass, no UI change; implementing `BLG-FE-117` itself deferred to v7.4).

**Staging-only ACs:** None — documentation/design pass, no UI to verify visually.

---

### EPIC-05 — Saved Filters & Calendar View Readiness Pass

**Maps to:** S2-07
**Owner:** Data Model & Domain Schema Owner; Frontend Specs & UX Documentation Owner
**Estimated effort:** 2.5 days
**Risk IDs:** RISK-05
**Execution sequence:** 5

#### ST-07 — Saved Filters & Calendar View (BLG-FE-118) pre-implementation spec pass

**Owner:** Data Model & Domain Schema Owner; Frontend Specs & UX Documentation Owner
**Estimated effort:** 2.5 (M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** AC-01's JSON-column-vs-dedicated-table schema decision must be made and recorded with rationale during this pass, not deferred to execution kickoff (RISK-05, LP-14 check applied at planning — see `sprint_planning_notes.md`). Named first candidate to phase into a second sprint via amendment cycle if capacity tightens — sequenced last for that reason. Design gate cleared — Design Pre-Approved (spec-only pass, no UI change; implementing `BLG-FE-118` itself deferred to v7.4).

**Staging-only ACs:** None — documentation/spec pass, no UI to verify visually.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~12–14 days |
| Total estimated effort (in-scope) | 13.25 days (midpoint) |
| Utilisation | ~95–110% of band (thin buffer — 0.75d to 14d warn threshold) |
| Over-allocation | No (outcome: PASS) |

## Items Deferred This Sprint

None — all 7 backlog-slice items are in scope.

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Add 5 missing prompt-change-log rows (see `sprint_planning_notes.md`) | Head of Specs Team | No |
| Monitor `BLG-SPEC-92`/`BLG-SPEC-94` effort trend; phase `BLG-SPEC-94` via amendment cycle if capacity tightens | PMO Lead | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed
**Scope confirmed:** Confirmed — 7 items, 5 EPICs, within capacity (PASS)
**Capacity confirmed:** Confirmed — PASS at 13.25d midpoint vs. ~12-14d band; thin-buffer monitoring note accepted, no phasing action required at seal
**Deferred execution blockers accepted (if any):** N/A — none present (`state.json deferred_execution_blockers` empty)
**Signed off by:** Product Owner
**Date:** 2026-07-16
