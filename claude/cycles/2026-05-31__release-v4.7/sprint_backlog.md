**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-05-31
**Cycle:** 2026-05-31__release-v4.7
**Release:** v4.7
**Sprint Goal:** Complete the SI-04 §13 pre-assessment, resolve all outstanding staging verifications inherited from prior cycles, add Arc 5 compliance data to the monthly P&L report, and close aged operational and UX assessment items — establishing a clean foundation for Arc 5 completion delivery in v4.8+.
**Backlog Slice Source:** Original — `claude/cycles/2026-05-31__release-v4.7/stage4_backlog_slice.md`

---

# Sprint Backlog — 2026-05-31__release-v4.7

---

## Sprint Scope

### Merge Order (Multi-EPIC)

**Sprint 1 merge order:** EPIC-03 → EPIC-04 → EPIC-02 → EPIC-01

**execution_state.json owner:** EPIC-03 (first in merge order). EPIC-04, EPIC-02, EPIC-01 branches must check for `execution_state.json` existence before creating their own; if found, read and append their EPIC section rather than overwrite.

**Shared file advisory:**
- `claude/backlog/backlog.md` — all EPICs mark BLG items complete; merge order prevents conflicts
- `docs/reference/openapi.yaml` — EPIC-02 only (compliance_summary field addition); rebasing later EPICs onto main not required (no other EPIC touches openapi.yaml)

**Sprint 2 (conditional):** EPIC-01 ST-02 only — gate: SI-01 + SI-03 live ≥30 days (2026-06-21). Activation requires `amend cycle` before Sprint 2 seals; PO must confirm gate met.

---

### EPIC-03 — Staging Verifications & Ops Housekeeping

**Maps to:** S2-03, S2-04, S2-05, S2-06
**Owner:** Infrastructure & Operations Owner; Data Model & Domain Schema Owner (ST-05, ST-06)
**Estimated effort:** ~2 days (XS+XS+XS+S)
**Risk IDs:** RISK-03 (ST-04 — Render infrastructure access)
**Execution sequence:** 1 (first in merge order; execution_state.json owner)
**Sprint:** Sprint 1 (firm)

#### ST-04 — Staging Deploy Live Verification

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** XS (~0.5 day)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** RENDER_STAGING_DEPLOY_HOOK secret must be configured before execution (Infrastructure & Operations Owner to confirm)

**Notes:** Closes v4.6 OA item BLG-OPS-28 (aged 4+ cycles). Produces `docs/ops/staging_deploy_verification.md`.

**Staging-only ACs:** AC-02 (live Render deploy trigger confirmation), AC-03 (path filter verified in Render dashboard)

---

#### ST-05 — DS-07 Migration Staging Verification

**Owner:** Infrastructure & Operations Owner; Data Model & Domain Schema Owner
**Estimated effort:** XS (~0.5 hr)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** DS-07 migration (v4.6 ST-01) must be present on staging database

**Notes:** Closes v4.6 OA item BLG-OPS-44. Produces a verification note.

**Staging-only ACs:** AC-01 (migration applied to staging with no errors), AC-02 (column presence confirmed via \d trade_plans), AC-03 (indexes confirmed)

---

#### ST-06 — Severity Field Staging Verification

**Owner:** Infrastructure & Operations Owner; Data Model & Domain Schema Owner
**Estimated effort:** XS (~0.5 hr)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** severity column migration (v4.6 ST-09) must be present on staging database

**Notes:** Closes v4.6 OA item BLG-OPS-45. Data Model & Domain Schema Owner sign-off required (AC-04).

**Staging-only ACs:** AC-01 (severity column confirmed via \d red_flag_events), AC-02 (default assignment verified), AC-03 (backfill confirmed — no nulls)

---

#### ST-07 — Render Log Retention Policy

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** Document-only story. Produces `docs/ops/render_log_retention_policy.md` (Class 3 Operational Record).

**Staging-only ACs:** None

---

### EPIC-04 — Cost & UX Assessments

**Maps to:** S2-07, S2-08
**Owner:** FinOps & Resource Architect (ST-08); Head of UX & Design (ST-09)
**Estimated effort:** ~1 day (S+S)
**Risk IDs:** None
**Execution sequence:** 2
**Sprint:** Sprint 1 (firm)

#### ST-08 — Anthropic API Tier Cost Assessment

**Owner:** FinOps & Resource Architect
**Estimated effort:** S (~0.5 day)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** BLG-OPS-36 monthly review data (completed v4.2) — usage data available

**Notes:** Document-only story. Produces `docs/ops/anthropic_api_tier_assessment.md`.

**Staging-only ACs:** None

---

#### ST-09 — Pre-Entry Validation Panel UX Assessment

**Owner:** Head of UX & Design
**Estimated effort:** S (~0.5 day)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None

**Notes:** Assessment-only — no implementation committed. Improvement candidates filed as backlog entries if warranted. Produces `docs/product/ux/pre_entry_panel_ux_assessment.md`.

**Staging-only ACs:** None

---

### EPIC-02 — User-Facing Analytics Enhancement

**Maps to:** S2-02
**Owner:** Head of Backend Engineering; Financial Reporting & Records Owner
**Estimated effort:** M (~2 days)
**Risk IDs:** RISK-02 (GET /analytics/arc5-compliance on staging)
**Execution sequence:** 3
**Sprint:** Sprint 1 (firm)

#### ST-03 — Arc 5 Compliance Score in Monthly P&L Report

**Owner:** Head of Backend Engineering; Financial Reporting & Records Owner
**Estimated effort:** M (~2 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** GET /analytics/arc5-compliance available on staging (shipped v4.0, expected stable — verify before execution)

**Notes:** Additive change to existing GET /reports/monthly-pnl endpoint. Adds `compliance_summary` field (optional). openapi.yaml must be updated in same commit as implementation. No new API endpoint — existing endpoint response schema change only.

**Staging-only ACs:** None — testable in CI with mock data

---

### EPIC-01 — Arc 5 Completion Pre-work

**Maps to:** S2-01 (Sprint 1 firm); S2-09 (Sprint 2 conditional)
**Owner:** Strategy Rules & System Intent Owner (ST-01); Head of Specs Team / Product Owner (ST-02, conditional)
**Estimated effort:** S (~1 day) Sprint 1; M (~2–3 days) Sprint 2 if gate met
**Risk IDs:** RISK-01 (ST-02 gate)
**Execution sequence:** 4 (Sprint 1); Sprint 2 (conditional)
**Sprint:** Sprint 1 (ST-01 firm); Sprint 2 (ST-02 conditional)

#### ST-01 — SI-04 §13 Formal Pre-Assessment

**Owner:** Strategy Rules & System Intent Owner
**Estimated effort:** S (~1 day)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None

**Notes:** Document-only story. Produces `docs/product/decisions/si04_section13_preassessment.md` (Class 3 Operational Record). Strategy Rules & System Intent Owner sign-off required.

**Staging-only ACs:** None — document-only story

---

#### ST-02 — SI-05 Phase 1 Implementation [DEFERRED — CONDITIONAL]

**Owner:** Head of Specs Team / Product Owner
**Estimated effort:** M (~2–3 days)
**Delegation class:** autonomous
**Status:** deferred_at_planning — gate condition not yet met

**Gate:** SI-01 + SI-03 live ≥30 days — clears 2026-06-21

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** Gate confirmation by Product Owner before Sprint 2 seals; amendment cycle required to activate

**Notes:** Execution engine must initialise `execution_state.json` with `status: deferred_at_planning, gate_condition: "SI-01 + SI-03 live ≥30 days — gate clears 2026-06-21"` for this story. Activation path: PO confirms gate → `amend cycle --cycle 2026-05-31__release-v4.7 --reason "SI-05 Phase 1 gate met"` → Sprint 2 seals.

**Staging-only ACs:** AC-05 (Telegram dispatch — requires live Telegram bot token on staging)

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24–28 days/sprint |
| Sprint 1 estimated effort (in-scope) | ~5–6 days |
| Sprint 1 utilisation | ~20–25% |
| Sprint 2 conditional effort | ~2–3 days (if gate met) |
| Over-allocation | No |
| Capacity verdict | PASS |

---

## Items Deferred This Sprint

| Item | EPIC | Reason | Deferred Status |
|------|------|--------|-----------------|
| ST-02 (SI-05 Phase 1) | EPIC-01 | Gate: SI-01 + SI-03 live ≥30 days (clears 2026-06-21) | deferred_at_planning |

---

## Deferred Execution Blockers Accepted

N/A — no deferred execution blockers were present in the release plan (`deferred_execution_blockers: []` in state.json).

---

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Prepend 4 missing prompt_change_log.md rows (advisory) | Head of Specs Team | No |
| Confirm RENDER_STAGING_DEPLOY_HOOK secret before ST-04 execution | Infrastructure & Operations Owner | No (before ST-04) |
| Confirm GET /analytics/arc5-compliance on staging before ST-03 execution | Head of Backend Engineering | No (before ST-03) |
| PO to confirm SI-01 + SI-03 gate by 2026-06-21 if Sprint 2 activates | Product Owner | No (before Sprint 2 seal) |

No outstanding actions are marked `Blocker? Yes`. Sprint may seal.

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — 2026-05-31
**Scope confirmed:** Confirmed — 8 firm stories (Sprint 1); 1 conditional (Sprint 2 gate 2026-06-21)
**Capacity confirmed:** Confirmed — PASS (~5–6 days effort vs ~24–28 day capacity; 20–25% utilisation)
**Deferred execution blockers accepted:** N/A — none present
**Signed off by:** Product Owner
**Date:** 2026-05-31
