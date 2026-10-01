**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-10-01
**Cycle:** 2026-09-30__release-v9.9
**Release:** v9.9
**Sprint Goal:** Ship a single canonical ATR/stop-recalculation implementation with timestamp visibility on `GET /positions` (this release's build-and-ship candidate, `BLG-BE-135`), while clearing the queued backend, security, QA, governance, spec, and frontend debt items that make up the rest of v9.9's full-capacity scope.
**Backlog Slice Source:** Original — `claude/cycles/2026-09-30__release-v9.9/stage4_backlog_slice.md`

# Sprint Backlog — 2026-09-30__release-v9.9

## Merge Order

**EPIC merge sequence:** EPIC-01 → EPIC-04 → EPIC-05 → EPIC-02 → EPIC-03 → EPIC-06 (front-loads EPICs carrying `delegated_decision`/`delegated_backend` items so their external dependencies are raised as early as possible).

**`execution_state.json` owner:** EPIC-01. All other EPIC branches must check for its existence before creating their own and append their own section rather than overwrite.

**Shared files across EPICs:** `strategy_rules.md` (EPIC-01 §7.1 + EPIC-04 §11/§12.3 — EPIC-01 owns canonical version, merges first; EPIC-04 must rebase onto `main` after EPIC-01 merges before finalising). `claude/system/prompt_change_log.md` (append-only across EPIC-01/04/05 — low conflict risk). `data_model.md`, `openapi.yaml`/`position_endpoints.md`, `current_roadmap.md`, `ai_endpoints.md` — each touched by exactly one EPIC this cycle, no cross-EPIC contention. Full detail: `sprint_planning_notes.md § Shared-file ownership advisory`.

## Sprint Scope

### EPIC-01 — Backend Reliability & Data Integrity

**Maps to:** S2-01–S2-05
**Owner:** Head of Engineering; Backend Engineering Patterns Owner
**Estimated effort:** 8.60 days
**Risk IDs:** RISK-01
**Execution sequence:** 1

#### ST-01 — Consolidate 4 duplicate ATR implementations; persist stop/ATR recalculation timestamp; expose atr/multiplier/timestamp on GET /positions

**Owner:** Head of Engineering; Backend Engineering Patterns Owner
**Estimated effort:** 8.00
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None (internal: ST-04 depends on this landing first — see Dependency Map)

**Notes:** RISK-01 — spec query to Strategy Rules & System Intent Owner on `strategy_rules.md` §7.1 cadence wording must be raised and resolved as an internal design-decision sub-step ahead of/alongside implementation; the story itself remains a single sealed item (not ST-ID phased). This cycle's PO Modify-recommended build-and-ship U-item candidate (`BLG-BE-135`).

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

#### ST-02 — GET /reports/monthly-pnl's year param has no bounds check, unlike its sibling GET /reports/tax-year

**Owner:** Head of Engineering; Backend Engineering Patterns Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

#### ST-03 — gemini_service.py's daily-cost Telegram alert still uses a hardcoded timeout, not utils.upstream_call

**Owner:** Head of Engineering; Backend Engineering Patterns Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

#### ST-04 — utils/pricing.py's ATR-fallback Yahoo Finance call still uses a hardcoded timeout, not utils.upstream_call

**Owner:** Head of Engineering; Backend Engineering Patterns Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** ST-01 (must complete first — both touch `backend/utils/pricing.py`; ST-01's ATR consolidation should land before this timeout-sourcing fix to avoid rework)

**Notes:** None.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

#### ST-05 — alpaca_paper_sync_service.py's 3 Alpaca calls still use hardcoded timeouts, not utils.upstream_call

**Owner:** Head of Engineering; Backend Engineering Patterns Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

---

### EPIC-02 — Operational Reliability & Security Hardening

**Maps to:** S2-06–S2-09
**Owner:** Infrastructure & Operations Owner; Cybersecurity & Trust Lead
**Estimated effort:** 0.60 days
**Risk IDs:** None
**Execution sequence:** 4

#### ST-06 — Two residual gaps in the just-hardened non-registry dependency guard

**Owner:** Infrastructure & Operations Owner; Cybersecurity & Trust Lead
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

#### ST-07 — POST /ai/check-daily-cost has no de-duplication guard against a double-submitted Telegram alert

**Owner:** Infrastructure & Operations Owner; Cybersecurity & Trust Lead
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

#### ST-08 — POST /ai/check-endpoint-anomalies has no de-duplication guard against a double-submitted Telegram alert

**Owner:** Infrastructure & Operations Owner; Cybersecurity & Trust Lead
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

#### ST-09 — POST /price-alerts has no de-duplication guard against a double-submitted duplicate alert

**Owner:** Infrastructure & Operations Owner; Cybersecurity & Trust Lead
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

---

### EPIC-03 — QA & Test Coverage

**Maps to:** S2-10–S2-18
**Owner:** Director of Quality; QA & Testing Owner
**Estimated effort:** 7.05 days
**Risk IDs:** None
**Execution sequence:** 5

#### ST-10 — GET /reports/tax-year returns HTTP 500 against its own test fixture

**Owner:** Director of Quality; QA & Testing Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

#### ST-11 — Strategy-rule → test traceability matrix for strategy_rules.md §4–§8

**Owner:** Director of Quality; QA & Testing Owner
**Estimated effort:** 2.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

#### ST-12 — Property-based tests for 'stop never decreases' and sizing validity rules

**Owner:** Director of Quality; QA & Testing Owner
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

#### ST-13 — Real-Postgres integration test for the reflection-reminder evaluation step

**Owner:** Director of Quality; QA & Testing Owner
**Estimated effort:** 0.75
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None

**Notes:** Runs in Phase B CI (real Postgres) per its own AC — not a staging-environment dependency; CI-reproducible.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

#### ST-14 — Convert remaining test files sharing test_trade_plan_audit_log.py's unrestored sys.modules["database"] swap pattern

**Owner:** Director of Quality; QA & Testing Owner
**Estimated effort:** 1.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

#### ST-15 — Add automated test coverage for the I/O-boundary functions in EPIC-04's staleness/CI-usage scripts

**Owner:** Director of Quality; QA & Testing Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

#### ST-16 — test_null_fee_trade_audit.py's inspect.getsource() call fails against the database module stub

**Owner:** Director of Quality; QA & Testing Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

#### ST-17 — Prove the non-registry dependency check fails a real PR, and confirm it is a required status check on main

**Owner:** Director of Quality; QA & Testing Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** None

**Notes:** Evidence is a recorded CI run URL — CI-reproducible, not staging-only.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

#### ST-18 — Harden the UI-copy boundary lint against obfuscation-grade and cross-node phrase splits

**Owner:** Director of Quality; QA & Testing Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

---

### EPIC-04 — Governance Process & Strategy Boundary

**Maps to:** S2-19–S2-27
**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** 8.55 days
**Risk IDs:** RISK-02, RISK-03
**Execution sequence:** 2

#### ST-19 — Conduct the overdue 90-day AI feature usage review (BLG-GOV-74/140/141/142 cluster)

**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** 1.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

**Dependencies:** None

**Notes:** RISK-03 — may require Human-Delegation for live production data; this sandboxed environment has no production credential (same structural gap as `ESC-EXEC-20260921-02/03/04`, `ESC-EXEC-20260910-01`).

**Staging-only ACs:** AC-1 (production AI feature adoption/cost review — requires live production data not reproducible in CI or this sandbox; see RISK-03). If deferred to post-merge Human-Delegation, a backlog item must be filed before the PR opens per CLAUDE.md §2.

---

**Status at sprint open: ready**

#### ST-20 — gap_risk_service.py (BLG-FEAT-65) shipped without a recorded §13 review or §13.5 roster row

**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** 1.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`

**Dependencies:** None

**Notes:** Governance §13 determination requires Head of Specs Team / Strategy Rules Owner judgement, not mechanical execution.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

#### ST-21 — Split roadmap_prompt.md into a core plus an appendix so it fits a single read

**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** 1.75
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`

**Dependencies:** None (internal: ST-25 depends on this landing first — see Dependency Map)

**Notes:** CLAUDE.md §6 governance file edit checklist applies in full (version bump, OPERATIONAL_GUIDE.md §14, source-prompt header, prompt_change_log.md entry).

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

#### ST-22 — Parameter-change ledger for strategy_rules.md §11 production parameters

**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-22`

**Dependencies:** None

**Notes:** Touches `strategy_rules.md` — shared with EPIC-01/ST-01 (§7.1). Rebase onto `main` after EPIC-01 merges, per Merge Order shared-file advisory.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

#### ST-23 — scan_backlog_gate_conditions.py date-disambiguation gap can produce false negatives

**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-23`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

#### ST-24 — Five near-duplicate "AI adoption window" gate-criteria texts should be one canonical shared reference

**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-24`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

#### ST-25 — Rebalance diagnostic tallies (STEP 2.4/7.1/7.2) are recomputed by hand each cycle

**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** 2.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-25`

**Dependencies:** ST-21 (must complete first — both touch `roadmap_prompt.md`; ST-21's core/appendix split should land before this story's script-reference addition)

**Notes:** None.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

#### ST-26 — role_share_history.md has no governance-authorized home under claude/roadmap/

**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** 0.15
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-26`

**Dependencies:** None

**Notes:** RISK-02 — routing/authority decision (formal authorisation to create a new `claude/roadmap/*` file, per `execution_prompt.md` §7 write-scope restriction) must be raised and resolved as an internal design-decision sub-step ahead of implementation.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

#### ST-27 — .claude_current_state.json's execution_state_path points to the prior cycle, not the active one

**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-27`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

---

### EPIC-05 — Spec & Data-Model Debt Clearance

**Maps to:** S2-28–S2-34
**Owner:** Data Model & Domain Schema Owner; Head of Specs Team
**Estimated effort:** 2.90 days
**Risk IDs:** None
**Execution sequence:** 3

#### ST-28 — Read-only live-schema vs data_model.md drift detector

**Owner:** Data Model & Domain Schema Owner; Head of Specs Team
**Estimated effort:** 2.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-28`

**Dependencies:** None

**Notes:** Read-only tool — no live-write access required.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

#### ST-29 — Drop 4 confirmed-orphaned, always-NULL columns from the live positions table

**Owner:** Data Model & Domain Schema Owner; Head of Specs Team
**Estimated effort:** 0.15
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-29`

**Dependencies:** None (internal: shares `data_model.md` with ST-30, ST-32 — no strict order required)

**Notes:** Requires live-DB write access (Human-Delegation), same precedent as `ESC-EXEC-20260921-04` (DS-17 migration).

**Staging-only ACs:** AC-1 (dropping columns from the live `positions` table — requires live-DB write access, not CI-reproducible). If deferred to post-merge Human-Delegation, a backlog item must be filed before the PR opens per CLAUDE.md §2.

---

**Status at sprint open: ready**

#### ST-30 — Reconcile positions.fees_paid NOT NULL constraint (re-apply live, or confirm nullable is intentional)

**Owner:** Data Model & Domain Schema Owner; Head of Specs Team
**Estimated effort:** 0.15
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-30`

**Dependencies:** None (internal: shares `data_model.md` with ST-29, ST-32 — no strict order required)

**Notes:** Requires live-DB write access (Human-Delegation), same precedent as `ESC-EXEC-20260921-04`.

**Staging-only ACs:** AC-1 (reconciling the `fees_paid` constraint on the live table — requires live-DB write access, not CI-reproducible). If deferred to post-merge Human-Delegation, a backlog item must be filed before the PR opens per CLAUDE.md §2.

---

**Status at sprint open: ready**

#### ST-31 — Cross-reference current_roadmap.md's SI-02 field to the canonical "linked trade plan" definition

**Owner:** Data Model & Domain Schema Owner; Head of Specs Team
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-31`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

#### ST-32 — data_model.md DS-19 "Verification status" still says the migration was never run against a live PostgreSQL

**Owner:** Data Model & Domain Schema Owner; Head of Specs Team
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-32`

**Dependencies:** None (internal: shares `data_model.md` with ST-29, ST-30 — no strict order required)

**Notes:** None.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

#### ST-33 — Correct the BLG-BE-128 citation to BLG-BE-129 for the latency_ms composition decision

**Owner:** Data Model & Domain Schema Owner; Head of Specs Team
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-33`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

#### ST-34 — Correct notifications.md and the alert-thresholds empty-state scenario doc to the no-trailing-period headings now shipped

**Owner:** Data Model & Domain Schema Owner; Head of Specs Team
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-34`

**Dependencies:** None

**Notes:** Resolves `DEV-v9.7-ST05-01`.

**Staging-only ACs:** None.

---

**Status at sprint open: ready**

---

### EPIC-06 — Frontend & UX Debt

**Maps to:** S2-35
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.15 days
**Risk IDs:** None
**Execution sequence:** 6

#### ST-35 — RecentTradesWidget icon-background badge uses two-way (>=0) colour logic for zero P&L

**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-35`

**Dependencies:** None

**Notes:** Design gate cleared — existing canonical rule (`design_system.md` v1.21 §Consistency Rules → Number and Currency Formatting) plus in-component precedent (`RecentTradesWidget.js`'s own P&L text already implements correct three-way logic) fully satisfies the Design Required classification; no new wireframe/decision record needed (`design_gate.md`). CLAUDE.md §2 frontend-visible-change rule satisfied by the story's own Playwright AC.

**Staging-only ACs:** None — the story's own AC requires Playwright coverage passing in CI, which is itself the CI-verifiable evidence method (CLAUDE.md §2).

---

**Status at sprint open: ready**

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24–28 working-day-equivalent units |
| Total estimated effort (in-scope) | 27.85 |
| Utilisation | 99.5% of band top edge (27.85 / 28.00) |
| Over-allocation | No (within band; Product Owner acknowledged proceeding at ceiling per `sprint_capacity.md` §1.5 buffer-floor advisory) |

## Items Deferred This Sprint

None — all 35 items from the authoritative backlog slice are in scope.

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Resolve RISK-01 spec query (strategy_rules.md §7.1 cadence wording) | Strategy Rules & System Intent Owner | No |
| Resolve RISK-02 routing/authority decision for new claude/roadmap/* file | Head of Specs Team | No |
| RISK-03 Human-Delegation disposition for ST-19 (if confirmed needed) | AI Compliance & Governance Officer / Product Owner | No |
| Live-DB write access delegation for ST-29/ST-30 | Data Model & Domain Schema Owner + Infrastructure & Operations Owner | No |

No outstanding action is marked `Blocker? Yes`.

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed, 2026-10-01 (as drafted)
**Scope confirmed:** Confirmed — all 35 items, 6 EPICs, per `stage4_backlog_slice.md`
**Capacity confirmed:** Confirmed — 27.85 / ~24–28 day band, proceed at ceiling (buffer-floor advisory acknowledged, 2026-10-01)
**Deferred execution blockers accepted (if any):** N/A — `deferred_execution_blockers` is empty in `state.json`
**Signed off by:** Product Owner
**Date:** 2026-10-01
