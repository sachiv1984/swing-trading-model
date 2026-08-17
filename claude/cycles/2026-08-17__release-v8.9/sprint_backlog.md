**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-08-17
**Cycle:** 2026-08-17__release-v8.9
**Release:** v8.9
**Sprint Goal:** Ship v8.9: eliminate the two live risk-management stop-price defects on open positions (breakeven-floor ratchet, currency-basis mismatch) and deliver the sector-aware position sizing, pre-commit risk simulator, AI post-trade debrief, and in-app backtesting foundations of the Trade Intelligence Expansion — while clearing this cycle's reliability, QA, ops, and governance debt.
**Backlog Slice Source:** Original — `stage4_backlog_slice.md`

---

# Sprint Backlog — v8.9

**Theme:** Live Risk-Management Correctness & Trade Intelligence Expansion

---

## Sprint Scope

### Merge Order (Multi-EPIC)

Sprint 1: **EPIC-01 → EPIC-02 (Sprint-1 subset) → EPIC-03 → EPIC-04 → EPIC-05 → EPIC-06**
Sprint 2 (gated on ST-23 reaching `done` with PASS/CONDITIONAL): **EPIC-02 (Sprint-2 subset — ST-06 only)**

### Execution State Owner

**EPIC-01** owns `execution_state.json` for this sprint (first in execution order; leads capacity allocation). EPIC-02 through EPIC-06 must check for `execution_state.json` existence before initialising their own — if found, read and append their EPIC's section rather than overwrite.

### Shared Files Advisory

No shared source files identified across EPIC-01 through EPIC-06 this cycle. Each EPIC's data-model and spec touches are scoped to independent files — see `sprint_planning_notes.md § Shared File Ownership Advisory`.

### Multi-Sprint Gate Note

ST-06 (EPIC-02) is design-gate-conditional (per `design_gate.md`, Gate Status: PASSED, ST-06 Conditionally Cleared) on a §13 System Boundary Review. **ST-23**, a new `delegated_decision` gate story scoped directly by `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-gate-story-scoping.md` (not sourced from `stage4_backlog_slice.md` — its acceptance criteria are reproduced in full below, per that decision record §2), runs in Sprint 1. ST-06 does not open for execution until ST-23 reaches `status: done` with a PASS or CONDITIONAL determination. If ST-23 is not resolved by end of Sprint 1: escalate and defer ST-06 to the next cycle (decision record §2 fallback clause).

---

## Sprint 1

### EPIC-01 — Live Risk-Management Correctness

**Maps to:** S2-01
**Owner:** Backend Engineering Patterns Owner; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 3.25d
**Risk IDs:** RISK-01
**Execution sequence:** 1

---

#### ST-01 — Fix nightly trailing-stop ratchet to apply breakeven floor for profitable positions

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** M
**Delegation class:** `delegated_backend`

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None (sequence first within EPIC-01 — ST-02 shares its data path)

**Notes:** RISK-01 — add the regression test specified in the item's own AC before changing production behaviour; backfill/recompute existing open positions' `current_stop` only after the calculation-path fix is verified correct.

**Staging-only ACs:** "No open profitable position has `current_stop` below its own `entry_price`" — requires a live-position data query to confirm; not fully CI-reproducible.

---

### EPIC-02 — Trade Sizing & Post-Trade Intelligence (Sprint 1 subset)

**Maps to:** S2-02
**Owner:** Head of Engineering; Backend Engineering Patterns Owner; Strategy Rules & System Intent Owner
**Estimated effort:** 8.00d (Sprint 1 subset: ST-04, ST-05, ST-07) + ~1d (ST-23)
**Risk IDs:** RISK-02
**Execution sequence:** 2

---

#### ST-04 — Correlation/sector-concentration-aware position sizing

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** M
**Delegation class:** `delegated_backend`

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** Design gate cleared — `docs/design/2026-08-17__release-v8.9/correlation-sector-concentration-sizing/decision_record.md`; frontend spec `trade_plan.md` v1.7 §10.7 (locked).

**Staging-only ACs:** None — all ACs CI-verifiable (regression test comparing sized outputs; visible-reason rendering covered by Playwright at execution time per CLAUDE.md's frontend-visible-change rule).

---

#### ST-05 — Pre-commit "what-if" sizing/risk simulator on the trade-plan form

**Owner:** Backend Engineering Patterns Owner; Head of Engineering
**Estimated effort:** M
**Delegation class:** `delegated_frontend`

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Notes:** Design gate cleared — `docs/design/2026-08-17__release-v8.9/what-if-sizing-risk-simulator/ux_spec.md`; frontend spec `trade_plan.md` v1.7 §5d (locked).

**Staging-only ACs:** None — all ACs CI-verifiable (Playwright: live-update preview, no-DB-write-on-preview check; preview-vs-save-value parity test).

---

#### ST-07 — In-app backtesting engine for strategy rule changes

**Owner:** Strategy Rules & System Intent Owner; Head of Engineering
**Estimated effort:** L
**Delegation class:** `delegated_backend`

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None (soft: Head of Engineering reuse-feasibility confirmation, RISK-02 — advisory, not blocking)

**Notes:** RISK-02 — largest single item this cycle (~3-5d); confirm `production_strategy.py` simulation-logic reuse feasibility early. If infeasible, scope may narrow to a smaller candidate-comparison surface. Design gate cleared — `docs/design/2026-08-17__release-v8.9/in-app-backtesting-engine/ux_spec.md`; frontend spec `strategy_benchmark.md` v0.6 §7.6 (locked).

**Staging-only ACs:** None — deterministic calculation over historical data, CI-testable with fixture data; persisted-run audit detail is a DB-level assertion, CI-testable.

---

#### ST-23 — §13 System Boundary Review: Automated AI Post-Trade Debrief *(new — gate story, not in `stage4_backlog_slice.md`)*

**Owner:** Strategy Rules & System Intent Owner
**Estimated effort:** S
**Delegation class:** `delegated_decision`

**Acceptance Criteria:** (reproduced in full from `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-gate-story-scoping.md` §2 — this story has no `stage4_backlog_slice.md` entry)
1. A §13 pre-assessment document is produced at `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md`, following the same structure as `arc6_ps03_section13_preassessment.md` (§13 Boundary Criteria, Compliance Assessment against all four criteria, Critical Boundary Questions, Binding Conditions if PASS/CONDITIONAL, Determination, Sign-Off).
2. The assessment addresses determinism, own-data-only, non-predictive-output, and decision-support-only criteria specifically against ST-06's "one suggested focus area" output — the boundary risk area most likely to draw a CONDITIONAL rather than a clean PASS.
3. Binding conditions are documented if PASS/CONDITIONAL.
4. An explicit Determination is recorded: PASS / CONDITIONAL / FAIL.
5. Strategy Rules & System Intent Owner sign-off.

**Dependencies:** None. Gates ST-06 (Sprint 2) — must reach `status: done` with PASS or CONDITIONAL before ST-06 opens for execution.

**Notes:** Sequence early in Sprint 1 (unblocks Sprint 2 planning). If Determination is FAIL: ST-06 is re-parked to the backlog with a blocking §13 objection (decision record §2). If not resolved by end of Sprint 1: escalate and defer ST-06 to the next cycle.

**Staging-only ACs:** None — deliverable is a document; sign-off is a governance action, not a CI-verified behaviour.

---

### EPIC-03 — Backend Reliability & Performance

**Maps to:** S2-03
**Owner:** Backend Engineering Patterns Owner; Head of Engineering
**Estimated effort:** 3.375d
**Risk IDs:** RISK-03
**Execution sequence:** 3

---

#### ST-08 — Investigate GET /trade-plans/tags ~10s p50 latency

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** S
**Delegation class:** `delegated_backend`

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None

**Staging-only ACs:** "Re-measured p50 within the same order of magnitude as `GET /positions/tags`" — requires production/staging latency measurement, not CI-reproducible.

---

#### ST-09 — Verify ST-11 duration logging against a real post-merge invocation

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** XS
**Delegation class:** `delegated_backend`

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None

**Staging-only ACs:** Entire item — verification requires a real Render production log invocation; not CI-reproducible. `[staging-only evidence]`.

---

#### ST-10 — Wrap audit-trail writes in the same transaction as the primary state update

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** S
**Delegation class:** `autonomous`

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Staging-only ACs:** None — transaction-rollback behaviour is CI-testable.

---

#### ST-11 — Confirm trade_csv_service.py::build_trade_history_csv is dead code and remove, or document coexistence

**Owner:** Head of Engineering
**Estimated effort:** S
**Delegation class:** `autonomous`

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None

**Staging-only ACs:** None.

---

### EPIC-04 — Test Coverage & QA Hardening

**Maps to:** S2-04
**Owner:** QA & Testing Owner; Director of Quality; Product Owner
**Estimated effort:** 3.375d
**Risk IDs:** RISK-04
**Execution sequence:** 4

---

#### ST-13 — Decide and apply treatment for trade_plans.setup_type with no default/required guarantee

**Owner:** Product Owner
**Estimated effort:** S
**Delegation class:** `delegated_decision`

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None

**Notes:** RISK-04 — sequence this decision early within EPIC-04, ahead of any dependent implementation work. Design gate: Design Pre-Approved (PO-confirmed downgrade) — if implementation surfaces a UI-visible change not already in use on this form, return to `design_gate.md` before merge (per its own note).

**Staging-only ACs:** None.

---

#### ST-12 — Add test coverage for screener_refresh/risk_off_alerts job-registration wiring

**Owner:** QA & Testing Owner
**Estimated effort:** XS
**Delegation class:** `autonomous`

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None

**Staging-only ACs:** None.

---

#### ST-14 — Add direct unit tests for cash_service, compliance_service, news_service, validation_service

**Owner:** QA & Testing Owner
**Estimated effort:** S
**Delegation class:** `autonomous`

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** None

**Staging-only ACs:** None.

---

#### ST-15 — Add Playwright coverage for WhatsNewCard's changelog User Impact rendering

**Owner:** QA & Testing Owner
**Estimated effort:** S
**Delegation class:** `autonomous`

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None

**Staging-only ACs:** None — Playwright test runs in CI.

---

### EPIC-05 — Operations & Spec Currency

**Maps to:** S2-05
**Owner:** Infrastructure & Operations Owner; API Contracts & Documentation Owner; Head of Specs Team
**Estimated effort:** 2.375d
**Risk IDs:** RISK-05
**Execution sequence:** 5

---

#### ST-16 — Local dev venv version-pin enforcement; confirm PUBLIC_URL parity on production

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S
**Delegation class:** `delegated_backend`

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** None

**Staging-only ACs:** "Production `PUBLIC_URL` status confirmed and documented" — requires a live production check, not CI-reproducible.

---

#### ST-17 — Archive window_summary_IW-*.md files older than 90 days

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S
**Delegation class:** `autonomous`

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** None

**Staging-only ACs:** None.

---

#### ST-18 — Document screener_refresh and risk_off_alerts jobs in health_endpoints.md

**Owner:** API Contracts & Documentation Owner
**Estimated effort:** XS
**Delegation class:** `autonomous`

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** None

**Staging-only ACs:** None.

---

### EPIC-06 — Governance Process Debt Closure

**Maps to:** S2-06
**Owner:** Head of Specs Team
**Estimated effort:** 2.75d
**Risk IDs:** RISK-06
**Execution sequence:** 6

---

#### ST-19 — Fix post_ship_closure.md to actually write last_post_ship_cycle/last_post_ship_utc

**Owner:** Head of Specs Team
**Estimated effort:** XS
**Delegation class:** `autonomous`

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

**Dependencies:** None

**Notes:** Standard CLAUDE.md §6 governance file edit checklist applies (version bump, `OPERATIONAL_GUIDE.md` §14, `prompt_change_log.md` entry).

**Staging-only ACs:** None.

---

#### ST-20 — Root-cause and correct execution_state.json timestamp drift from actual git commit dates

**Owner:** Head of Specs Team
**Estimated effort:** S
**Delegation class:** `autonomous`

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`

**Dependencies:** None

**Staging-only ACs:** None.

---

#### ST-21 — Physically place the Displacement Debt Register and wire it into roadmap_prompt.md STEP 8

**Owner:** Head of Specs Team
**Estimated effort:** XS
**Delegation class:** `autonomous`

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`

**Dependencies:** None

**Notes:** RISK-06 — must follow the full CLAUDE.md §6 Governance File Edit Checklist in the same commit as the `roadmap_prompt.md` STEP 8 edit; do not land the register file without the paired prompt edit or vice versa.

**Staging-only ACs:** None.

---

#### ST-22 — Define a pruning rule for stale RA: roadmap-annotation markers older than 3 releases

**Owner:** Head of Specs Team
**Estimated effort:** S
**Delegation class:** `autonomous`

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-22`

**Dependencies:** None

**Staging-only ACs:** None.

---

## Sprint 2 (Gated — opens when ST-23 reaches `done` with PASS/CONDITIONAL)

### EPIC-02 — Trade Sizing & Post-Trade Intelligence (Sprint 2 subset)

**Maps to:** S2-02
**Owner:** Head of Engineering; Backend Engineering Patterns Owner; AI Compliance & Governance Officer
**Estimated effort:** 3.00d
**Risk IDs:** RISK-02
**Execution sequence:** 7

---

#### ST-06 — Automated AI post-trade debrief

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** M
**Delegation class:** `delegated_backend`

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** ST-23 (must complete first, `status: done` with PASS/CONDITIONAL — Sprint 1 gate story)

**Status at sprint open: conditional — gate ST-23 completion (not a fixed calendar date)**

**Notes:** Design gate: Conditionally Cleared (see `design_gate.md`). AI Compliance & Governance Officer sign-off required per standing AI-generated-content governance policy — generation must be logged to `claude_audit_log`.

**Staging-only ACs:** "Every newly-closed trade has an AI-generated debrief available shortly after close (real-time generation, or on-demand if real-time isn't feasible)" — real-time generation timing behaviour on a live trade-close event is not fully CI-reproducible; verify via staging run or document the on-demand fallback path if real-time timing cannot be staged.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | 24-28d |
| Total estimated effort (in-scope, 23 items across both sprints) | ~27.125d |
| Utilisation | ~97-113% of band (upper/lower bound respectively) |
| Over-allocation | No — within confirmed 24-28d band; buffer-floor advisory (STEP 1.5) acknowledged by Product Owner, proceed at full scope (see `sprint_capacity.md`) |

## Items Deferred This Sprint

None.

## Deferred Execution Blockers Accepted

*(section omitted — `deferred_execution_blockers` is empty in `state.json`)*

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Confirm `production_strategy.py` reuse feasibility for ST-07 (RISK-02) | Head of Engineering | No |
| Sequence PO/Frontend Specs decision for ST-13 early in EPIC-04 (RISK-04) | Product Owner; Frontend Specifications & UX Documentation Owner | No |
| Full CLAUDE.md §6 checklist accompanying ST-21's `roadmap_prompt.md` STEP 8 edit (RISK-06) | Head of Specs Team | No |
| File P3 Spec Debt backlog item for `PositionSizingWidget` baseline documentation | PMO Lead / Head of Specs Team | No |
| Escalate 2 carried-forward Phase 4 deferred patches (§6.4 threshold now crossed) | Head of Specs Team | No |

No outstanding action is marked `Blocker? Yes`.

---

## Director of Quality Readiness

QA criteria reviewed for all 7 EPIC scopes (6 backlog EPICs + ST-23 gate story under EPIC-02). Autonomous and delegated_backend items with CI-verifiable ACs (ST-04, ST-05 Playwright, ST-10 through ST-22 except staging-flagged items) are CI-verifiable. Staging-only ACs are explicitly designated per story above (ST-01, ST-02, ST-08, ST-09, ST-16, ST-06) — each is either a live-data/production-measurement check or, for ST-06, real-time generation timing. No test coverage gap identified that would block sign-off. Director of Quality confirms QA criteria are sufficient to produce `qa_evidence_EPIC-0x.md` at sprint close for each EPIC.

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed, 2026-08-17
**Scope confirmed:** Confirmed, 2026-08-17 — 22 backlog-slice items + ST-23 gate story, split Sprint 1 (22 items) / Sprint 2 (ST-06, gated)
**Capacity confirmed:** Confirmed, 2026-08-17 — proceed at full ~27.125d scope against the 24-28d band (buffer-floor advisory acknowledged, see `sprint_capacity.md`)
**Deferred execution blockers accepted (if any):** N/A — none present
**Signed off by:** Product Owner
**Date:** 2026-08-17
