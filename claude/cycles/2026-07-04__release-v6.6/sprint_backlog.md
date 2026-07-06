**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-07-06
**Cycle:** 2026-07-04__release-v6.6
**Release:** v6.6
**Sprint Goal:** Complete a systematic WCAG-AA contrast audit across secondary/disclaimer text surfaces app-wide, ship Red Flag Journal filter-state persistence, resolve every true backlog-ID collision in `claude/backlog/backlog.md`, and reach a verified decision on automated derivation for the `database.py` / `_DB_STUB_FUNCTIONS` test-stub sync list.
**Backlog Slice Source:** original `stage4_backlog_slice.md`

# Sprint Backlog — 2026-07-04__release-v6.6

## Merge Order

- **EPIC merge sequence:** EPIC-02 → EPIC-01 (autonomous EPIC first; EPIC-01 sequenced second as it carries both `delegated_frontend` items).
- **`execution_state.json` owner:** EPIC-02 (first in execution order). EPIC-01's branch must check for `execution_state.json` existence before creating its own version — if found, read and append rather than overwrite.
- **Shared files across EPICs:** None identified this sprint (see `sprint_planning_notes.md` §Shared File Ownership Advisory).

## Sprint Scope

### EPIC-02 — QA & Test Infrastructure Debt

**Maps to:** S2-03, S2-04
**Owner:** Director of Quality / QA & Testing Owner
**Estimated effort:** ≈2.0 days
**Risk IDs:** RISK-02, RISK-03
**Execution sequence:** 1

#### ST-03 — Audit colliding backlog IDs (BLG-QA-72)

**Owner:** Director of Quality; Product Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Notes:** RISK-02 applies — grep all `claude/cycles/*/` and `claude/roadmap/` for any renumbered ID before finalising, per the item's own AC. Confirmed real collisions per `stage4_backlog_slice.md` context: `BLG-OPS-13`/`BLG-FE-45` (9×), `BLG-OPS-17`/`BLG-GOV-88`/`BLG-FEAT-55` (8×), `BLG-SPEC-46`/`BLG-QA-42` (7×), plus a dozen more at 4–6×. Classify prose-citation vs. true collision before renumbering anything.

**Staging-only ACs:** None — all three ACs (classification, renumbering, `groom backlog` re-verification) are verifiable via direct document/code review and the next `groom backlog` run.

---

#### ST-04 — database.py / _DB_STUB_FUNCTIONS manual-sync risk (BLG-QA-73)

**Owner:** QA & Testing Owner; Backend Engineering Patterns Owner
**Estimated effort:** M (~1–2 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** RISK-03 applies — AC-02 requires a verifying CI run before merge if automated derivation is adopted; if infeasible, resolves as a documented decision with no code change (zero regression risk). If a new `database` import is added to `backend/services/position_service.py` during this work, `tests/conftest.py`'s `_DB_STUB_FUNCTIONS` list must be updated in the same commit per CLAUDE.md.

**Staging-only ACs:** None — AC-02's "verified by a CI run" is CI-native by definition.

---

### EPIC-01 — UX & Accessibility Debt

**Maps to:** S2-01, S2-02
**Owner:** Base44 Frontend Prompt Owner / Head of UX & Design
**Estimated effort:** ≈1.5 days
**Risk IDs:** RISK-01, RISK-04 (resolved)
**Execution sequence:** 2

#### ST-01 — Colour contrast audit sweep (BLG-FE-82)

**Owner:** Head of UX & Design
**Estimated effort:** S (~1 day)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None

**Notes:** Design gate classification: Design Not Applicable — ships a findings report, not a UI change. Any contrast fixes surfaced by the audit must be filed as separate follow-up backlog items, each subject to its own future design gate classification (`design_gate.md`). RISK-01 applies — Head of UX & Design sign-off (AC-03) is the mitigation.

**Staging-only ACs:** None — this story ships an audit report, not a rendering change; no CI/staging split applies.

---

#### ST-02 — Red Flag Journal filter state persistence (BLG-FE-40)

**Owner:** Base44 Frontend; Head of UX & Design
**Estimated effort:** S (~0.5 day)
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Notes:** Design gate classification: Design Pre-Approved — persistence-only change (localStorage), no new component, no layout change, existing filter UI is pixel-identical before and after (`design_gate.md`). Gate condition ("RFJ in active use ≥30 days post-v3.9") cleared 2026-06-21, confirmed by Product Owner in `release_plan.md` §1.4b. RISK-01 applies — AC-03 already specifies the required Playwright test (set filter → reload → verify restored), satisfying CLAUDE.md's frontend-visible-change Playwright gate directly.

**Staging-only ACs:** None — AC-01 (persistence) and AC-02 (stale-state clearing) are covered by the same Playwright test named in AC-03; all three are CI-verifiable.

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~12–14 days |
| Total estimated effort (in-scope) | ≈3.5 days |
| Utilisation | ≈25–29% |
| Over-allocation | No |

## Items Deferred This Sprint

None — all 4 items from the authoritative backlog slice enter scope.

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| DF-18 recurrence threshold met (2-cycle carry-forward, `/commit-check` pathspec-diff patch still unapplied) — recommend filing a backlog item or direct prompt/skill patch outside this routine. | Head of Specs Team | No |
| Root `.claude_current_state.json` design gate fields are stale (`design_gate_status: not_started`, pointing at v6.5's record) — recommend correcting directly; the cycle-level `state.json` (authoritative) correctly shows `Passed`. | PMO Lead | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — 2026-07-06
**Scope confirmed:** Confirmed — all 4 items (EPIC-01/EPIC-02) accepted within capacity, 2026-07-06
**Capacity confirmed:** Confirmed — ≈3.5d vs ~12–14d available, no over-allocation, 2026-07-06
**Deferred execution blockers accepted (if any):** N/A — `deferred_execution_blockers` empty in `state.json`
**Signed off by:** Product Owner
**Date:** 2026-07-06
