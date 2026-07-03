**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-07-03
**Cycle:** 2026-07-02__release-v6.5
**Release:** v6.5
**Sprint Goal:** Clear all 10 remaining AUD-2026-07-01 audit findings, resolve the 3-cycle-stagnant BLG-QA-61 carry-forward and the two v6.5-provisional-target backlog debt items, and ship the Claude thesis feedback mechanism together with its adoption-rate metric.
**Backlog Slice Source:** original `stage4_backlog_slice.md`

# Sprint Backlog — 2026-07-02__release-v6.5

## Merge Order

- **EPIC merge sequence:** EPIC-01 → EPIC-02 → EPIC-03 (autonomous EPICs first; EPIC-03 sequenced last as it carries the one `delegated_frontend` item).
- **`execution_state.json` owner:** EPIC-01 (first in execution order). EPIC-02 and EPIC-03 branches must check for `execution_state.json` existence before creating their own version — if found, read and append rather than overwrite.
- **Shared files across EPICs:** None identified this sprint (see `sprint_planning_notes.md` §Shared File Ownership Advisory).

## Sprint Scope

### EPIC-01 — Audit Remediation Cluster

**Maps to:** S2-06, S2-07, S2-08
**Owner:** Head of Specs Team
**Estimated effort:** ≈0.7 day
**Risk IDs:** RISK-01
**Execution sequence:** 1

#### ST-01 — Lifecycle/prompt/state wording and consistency fixes (BLG-GOV-157 as labelled in slice — see Outstanding Actions re: ID cross-reference defect)

**Owner:** Head of Specs Team
**Estimated effort:** XS (<1 hour)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None

**Notes:** RISK-01 applies — apply the CLAUDE.md §6 Governance File Edit Checklist in the same commit for any Class 6 prompt or OPERATIONAL_GUIDE.md touch made while resolving this item. See Outstanding Actions for a BLG-ID cross-reference defect affecting this item's backlog-ref label only (content/AC unaffected).

**Staging-only ACs:** None — all three ACs (staging-only AC protocol wording, `FRICTION_LOAD` wording, state-file reconciliation) are verifiable via direct document/code review in CI or code review.

---

#### ST-02 — README.md document hygiene sweep (BLG-GOV-158)

**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Notes:** Wording/documentation-only item per CLAUDE.md's FI-P3-02 exception — code review of the static text may substitute for staging sign-off (no visual rendering/colour/layout claim).

**Staging-only ACs:** None.

---

#### ST-03 — OPERATIONAL_GUIDE/prompt version-sync drift (BLG-GOV-159 as labelled in slice — see Outstanding Actions re: ID cross-reference defect)

**Owner:** Head of Specs Team
**Estimated effort:** XS (<1 hour)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Notes:** RISK-01 applies — apply the CLAUDE.md §6 Governance File Edit Checklist in the same commit. See Outstanding Actions for a BLG-ID cross-reference defect affecting this item's backlog-ref label only (content/AC unaffected).

**Staging-only ACs:** None.

---

### EPIC-02 — Backlog Debt Clearance

**Maps to:** S2-01, S2-02, S2-03
**Owner:** Infrastructure & Operations Owner; QA & Testing Owner
**Estimated effort:** ≈0.6 day
**Risk IDs:** RISK-02
**Execution sequence:** 2

#### ST-04 — Add v6.4 endpoint to `api_performance_baseline.md` (BLG-OPS-83)

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** XS (<1 hour)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** Follow the §22.2/§22.3 dynamic-2x regression-threshold pattern (precedent: BLG-OPS-82). Per the BLG-OPS-82 precedent, measure against staging (`https://trading-assistant-api-staging.onrender.com`), falling back to production only if staging is unavailable (404).

**Staging-only ACs:** AC-01 (measured p50/p95 against a live staging/production environment, minimum 5 warm requests — CI cannot reproduce deployed-environment latency measurements).

---

#### ST-05 — Playwright coverage for Strategy Benchmark Panel 0 rendering (TEST-GAP-EPIC-03-v64)

**Owner:** QA & Testing Owner
**Estimated effort:** XS (<0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Notes:** RISK-02 applies — follow the existing BLG-QA-37 mock/error-injection strategy for AC-03 (API-error state) to avoid flakiness.

**Staging-only ACs:** None — all four ACs are CI-verifiable Playwright test additions to `tests/e2e/strategy-benchmark.spec.js`.

---

#### ST-06 — Review `signals_scenarios.md` against ST-01 signal sizing model changes (BLG-QA-61)

**Owner:** QA & Testing Owner; Director of Quality
**Estimated effort:** XS (<1 hour)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None

**Notes:** 3-cycle carry-forward item (v6.2→v6.3→v6.4) — promoted to firm scope per `release_plan.md` §1.4a active disposition. Resolves the recurring Carry-Forward flag (see `sprint_planning_notes.md` §Carry-Forward Items row 1).

**Staging-only ACs:** None.

---

### EPIC-03 — AI Thesis Feedback Loop

**Maps to:** S2-04, S2-05
**Owner:** Base44 Frontend; Head of UX & Design; Metrics Definitions & Analytics Owner
**Estimated effort:** ≈1.5 day
**Risk IDs:** RISK-03
**Execution sequence:** 3

#### ST-07 — Claude thesis generation user feedback mechanism (BLG-FE-46)

**Owner:** Base44 Frontend; Head of UX & Design
**Estimated effort:** S (~1 day)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None (design gate pre-condition already satisfied — see below)

**Notes:** Design gate cleared 2026-07-02 (`design_gate.md`) — Design Required classification, UX spec `docs/design/2026-07-02__release-v6.5/thesis-feedback-mechanism/ux_spec.md` v1.0, `trade_plan.md` v0.8. Build-time correction required per the design artefact: the feedback control must gate on a Claude-specific signal, not the shared `isAiDraft` flag (which is also set by the non-AI "Generate thesis" template button) — feedback must never be solicited for non-AI template content. Recommended (non-binding) persistence approach: `thesis_feedback` field on `claude_audit_log`, exposed via `POST /trade-plans/{plan_id}/thesis-feedback` — Sprint Execution remains bound only by AC-02 itself. **Per LL-v2.0-P4-2 (new user-facing control, no Playwright AC defined at planning): Sprint Execution must add Playwright coverage for AC-01 or file a `/backlog-add` item before the PR opens if staging sign-off is deferred (CLAUDE.md observable-AC Playwright gate).** Set EPIC-03 `test_scenarios = "pending — QA & Testing Owner to author before next sprint on this domain"` in `execution_state.json` at STEP 0.

**Staging-only ACs:** None flagged at planning time — AC-01 (UI rendering) and AC-02 (persistence) are expected to be CI-verifiable via Playwright/integration test once authored per the note above; if Sprint Execution determines otherwise, file per CLAUDE.md's observable-AC Playwright gate before the PR opens.

---

#### ST-08 — Claude thesis adoption rate metric (BLG-FEAT-41)

**Owner:** Metrics Definitions & Analytics Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None

**Notes:** Backend metric-definition item with no UI acceptance criterion — Design Not Applicable (confirmed at design gate).

**Staging-only ACs:** None.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~12–14 days |
| Total estimated effort (in-scope) | ≈2.8 days |
| Utilisation | ≈20–23% |
| Over-allocation | No |

## Items Deferred This Sprint

None — all 8 items from the authoritative backlog slice enter scope.

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| BLG-ID cross-reference defect: ST-01/ST-03 backlog-ref labels are swapped relative to actual `backlog.md` entries (content/AC unaffected) | Head of Specs Team | No |
| LL-v2.0-P4-2 test scenario gap: ST-07 new user-facing control has no Playwright AC yet; set `execution_state.json` EPIC-03 `test_scenarios = pending` at Sprint Execution STEP 0 | QA & Testing Owner | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — 2026-07-03
**Scope confirmed:** Confirmed — all 8 items (EPIC-01/02/03) accepted within capacity, 2026-07-03
**Capacity confirmed:** Confirmed — ≈2.8d vs ~12–14d available, no over-allocation, 2026-07-03
**Deferred execution blockers accepted (if any):** N/A — `deferred_execution_blockers` empty in `state.json`
**Signed off by:** Product Owner
**Date:** 2026-07-03
