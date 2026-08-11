**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-08-11
**Cycle:** 2026-08-11__release-v8.6
**Release:** v8.6
**Sprint Goal:** Ship all 26 scoped v8.6 stories — trade-plan completion-rate tracking and an AI-assisted order-placement thesis digest, trade-plan-to-position linkage enforced with a DB-level integrity safeguard, the remaining shadcn design-token and secondary-text drift debt closed, and the financial-correctness, QA-coverage, and governance-debt carryover from v8.5 fully resolved — see `sprint_goal.md`
**Backlog Slice Source:** original `stage4_backlog_slice.md`

# Sprint Backlog — 2026-08-11__release-v8.6

## Merge Order

EPIC merge sequence: **EPIC-01 → EPIC-02 → EPIC-03 → EPIC-04 → EPIC-05 → EPIC-06** (per `sprint_planning_notes.md` Execution Sequence; EPIC-01 leads per the Skill-Silo rotation guideline named in `release_plan.md`'s Execution Plan; EPIC-03's internal ST-04 → ST-05 sequencing applies within that EPIC).

`execution_state.json` owner: **EPIC-01** (first in execution order). All other EPIC branches must check for `execution_state.json` existence before creating their own version — if found, read it and append their EPIC's section rather than overwrite.

Shared files across EPICs (see `sprint_planning_notes.md` Multi-EPIC Execution Notes for full detail):
- `docs/specs/frontend/pages/analytics.md` — EPIC-01 (ST-01) owns the canonical §21 addition; EPIC-03 (ST-10) references §15 as an unchanged locked reference.
- `docs/specs/frontend/pages/trade_plan.md` — EPIC-01 (ST-02) owns the canonical §10.5 addition; EPIC-02 (ST-03) references §10 as an unchanged locked reference.
- `docs/specs/frontend/design_system.md` — EPIC-03 only (ST-04, ST-06, ST-07); no cross-EPIC collision.
- `execution_state.json` — all 6 EPICs.

---

## Sprint Scope

### EPIC-01 — User-Facing Product Features

**Maps to:** S2-01
**Owner:** Product Owner
**Estimated effort:** 2.75
**Risk IDs:** RISK-01
**Execution sequence:** 1

#### ST-01 — Trade plan completion rate tracking

**Owner:** Product Owner
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None

**Notes:** Priority P2 (escalated from P3, 2026-08-11 rebalance). Design cleared — `docs/specs/frontend/pages/analytics.md` v2.1 §21.

**Staging-only ACs:** None

---

#### ST-02 — AI-assisted setup thesis digest at order placement

**Owner:** Product Owner
**Estimated effort:** 1.75
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Notes:** RISK-01 — gate condition (AI adoption window + established usage patterns) resolved via explicit Product Owner disposition, `decisions--2026-08-11__release-v8.6.md`. Reuses the existing Claude thesis generation service (v4.0 infrastructure) — no fresh §13 review required (design gate note). Design cleared — `docs/specs/frontend/pages/trade_plan.md` v1.4 §10.5.

**Staging-only ACs:** None

---

### EPIC-02 — Trade-Plan Data Integrity Foundation

**Maps to:** S2-02
**Owner:** Data Model, Domain & Schema Owner; Backend Engineering Patterns Owner
**Estimated effort:** 1.75
**Risk IDs:** RISK-02
**Execution sequence:** 2

#### ST-03 — Enforce trade-plan linkage at position entry + DB-level safeguard against orphaned trade_plans rows

**Owner:** Data Model, Domain & Schema Owner; Backend Engineering Patterns Owner
**Estimated effort:** 1.75
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Notes:** RISK-02 — named structural response to the 2026-08-11 rebalance's mandatory Skill-Silo pull-forward finding; targets the 0/11-linked-trade-plans fact blocking `BLG-FEAT-73`'s gate. DB-level safeguard risks blocking a legitimate edge-case position-creation flow if scoped too strictly — staging verification required before merge; Data Model, Domain & Schema Owner + Product Owner sign-off required per AC.

**Staging-only ACs:** AC-01 ("Entry-flow linkage confirmed enforced (staging-verified)") — the AC is explicitly staging-verified, not CI-reproducible via unit/integration test alone.

---

### EPIC-03 — Frontend Design Consistency & Correctness Carryover

**Maps to:** S2-03
**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 6.25
**Risk IDs:** RISK-03
**Execution sequence:** 3

#### ST-04 — Register remaining unregistered shadcn design tokens in tailwind.config.js

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 1.75
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None (ST-05 depends on this item — see below)

**Notes:** Should land before/alongside ST-05 — coverage needs the tokens registered first. Identical root cause to v8.5 ST-06's `-muted` fix (design gate note).

**Staging-only ACs:** None

---

#### ST-05 — Playwright coverage for the remaining -muted/-muted-foreground call sites left untested by v8.5/ST-06

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** ST-04 (must complete first)

**Notes:** Test-coverage-only story for already-shipped tokens; no UI change (design gate note, mirrors v8.5 ST-09 audit precedent).

**Staging-only ACs:** None

---

#### ST-06 — Fix 6 drift instances against the v6.7 canonical secondary-text token

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None

**Notes:** Corrective work restoring an already-canonical token (`design_system.md` §Color Usage, v6.7).

**Staging-only ACs:** None

---

#### ST-07 — Design decision: should modals/dialogs support light theme?

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** Design decision already produced at design gate — `docs/design/2026-08-11__release-v8.6/modal-light-theme-support/decision_record.md`. Follow-up implementation item `BLG-FE-156` filed separately (not this story's scope) per `design_gate.md`'s notes.

**Staging-only ACs:** None

---

#### ST-08 — Switch Layout.js's dark-class document.documentElement sync to useLayoutEffect

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None

**Notes:** Design gate classified Design Not Applicable — lifecycle-hook timing choice, not an interaction-timing parameter under BLG-FE-131's clause. AC itself permits a code-comment-only outcome.

**Staging-only ACs:** None

---

#### ST-09 — Correct st15_nav_bar_redesign_exploration.md's nav group/page counts against live NAV_GROUPS

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None

**Notes:** Documentation correction only; no live UI change.

**Staging-only ACs:** None

---

#### ST-10 — Migrate CohortAnalysis.js from client-side computation to GET /analytics/cohort

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Notes:** Corrective architecture fix against `analytics.md` §15's existing hard rule (`DEV-EPIC02-ST03-01`); AC states no visual change expected. Uses the existing `GET /analytics/cohort` endpoint — no new endpoint.

**Staging-only ACs:** None

---

### EPIC-04 — Backend & Financial Correctness

**Maps to:** S2-04
**Owner:** Financial Reporting & Records Owner; Cybersecurity & Trust Lead
**Estimated effort:** 4.75
**Risk IDs:** RISK-04
**Execution sequence:** 4

#### ST-11 — get_regime_distribution's NULL-exclusion documented behaviour is dead code

**Owner:** Financial Reporting & Records Owner
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None

**Notes:** Backend documentation/behaviour correctness fix; no UI.

**Staging-only ACs:** None

---

#### ST-12 — Multi-currency cost-basis rounding consistency check

**Owner:** Financial Reporting & Records Owner
**Estimated effort:** 1.75
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None

**Notes:** RISK-04 — audit-first scope ("fix any inconsistency found"); may surface a real historical-data discrepancy requiring a data fix, not just a code fix. Financial Reporting & Records Owner sign-off required per AC.

**Staging-only ACs:** None

---

#### ST-13 — Closed-trade export completeness check against tax-year boundary edge cases

**Owner:** Financial Reporting & Records Owner
**Estimated effort:** 1.00
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None

**Notes:** Financial Reporting & Records Owner sign-off required per AC.

**Staging-only ACs:** None

---

#### ST-14 — check_dependency_vuln_rescan.py silently treats a failed audit tool as "zero findings"

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** None

**Notes:** CI/CD tool robustness fix; no UI.

**Staging-only ACs:** None

---

### EPIC-05 — QA Test-Coverage Debt Closure

**Maps to:** S2-05
**Owner:** Director of Quality
**Estimated effort:** 3.00
**Risk IDs:** RISK-05
**Execution sequence:** 5

#### ST-15 — Add endpoint-level regression test for GET /analytics/tag-performance's ensure_trade_plans_table call

**Owner:** Director of Quality
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None

**Notes:** Test only; no UI.

**Staging-only ACs:** None

---

#### ST-16 — Add Playwright coverage for setNarrativeField AI-draft-badge clearing on the 3 non-setup_thesis fields

**Owner:** Director of Quality
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** None

**Notes:** Test-coverage-only story for already-shipped behaviour; no UI change.

**Staging-only ACs:** None

---

#### ST-17 — Add unit tests for scripts/check_dependency_vuln_rescan.py

**Owner:** Director of Quality
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** None

**Notes:** Test only; no UI.

**Staging-only ACs:** None

---

#### ST-18 — Document one-directional limitation of test_alerts_service.py's sys.modules restore fixture

**Owner:** Director of Quality
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** None

**Notes:** Test-infrastructure documentation; no UI.

**Staging-only ACs:** None

---

### EPIC-06 — Operations & Governance Debt Closure

**Maps to:** S2-06
**Owner:** Head of Specs Team
**Estimated effort:** 5.25
**Risk IDs:** RISK-06
**Execution sequence:** 6

#### ST-19 — Align api-key-cross-environment-check.yml's alert-step grep with the skip-guard's ::error:: prefix

**Owner:** Head of Specs Team
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

**Dependencies:** None

**Notes:** CI/CD workflow fix; no UI.

**Staging-only ACs:** None

---

#### ST-20 — Document CVE-2026-4539 ignore rationale in dependency-vuln-rescan.yml

**Owner:** Head of Specs Team
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`

**Dependencies:** None

**Notes:** CI/CD documentation; no UI.

**Staging-only ACs:** None

---

#### ST-21 — Confirm dependency-vuln-rescan.yml runs successfully post-merge

**Owner:** Head of Specs Team
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`

**Dependencies:** None (timing note — see `sprint_planning_notes.md`; execute after this sprint's PRs merge)

**Notes:** Closes v8.5/ST-04's originally-deferred AC. Requires observing a real post-merge workflow run — sequenced last within EPIC-06.

**Staging-only ACs:** None

---

#### ST-22 — File retroactive DEV record for the dark-mode/Radix-portal Layout.js fix

**Owner:** Head of Specs Team
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-22`

**Dependencies:** None

**Notes:** Governance record only; matches `DEV-REPORTS-ST01-02`'s format.

**Staging-only ACs:** None

---

#### ST-23 — shared_standards_changelog.md missing v3.27 entry

**Owner:** Head of Specs Team
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-23`

**Dependencies:** None

**Notes:** Governance document fix; no UI.

**Staging-only ACs:** None

---

#### ST-24 — execution_state.json's deviations_filed field is used as "check performed" not literally "filed"

**Owner:** Head of Specs Team
**Estimated effort:** 1.75
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-24`

**Dependencies:** None

**Notes:** Head of Specs Team sign-off required per AC.

**Staging-only ACs:** None

---

#### ST-25 — Annotate BLG-FE-146/BLG-FE-139 with 2026-08-10 trigger-condition re-check

**Owner:** Head of Specs Team
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-25`

**Dependencies:** None

**Notes:** Governance document annotation; no UI.

**Staging-only ACs:** None

---

#### ST-26 — Correct BLG-GOV-288's Acceptance Criteria text (says STEP 0, actual fix is STEP 7)

**Owner:** Head of Specs Team
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-26`

**Dependencies:** None

**Notes:** Governance document correction; no UI.

**Staging-only ACs:** None

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24-28 days |
| Total estimated effort (in-scope) | 23.75 days |
| Utilisation | ~85-99% (84.8% of the 28-day upper bound; 98.96% of the 24-day lower bound) |
| Over-allocation | No |

## Items Deferred This Sprint

None. All 26 items from `stage4_backlog_slice.md` are in scope.

## Deferred Execution Blockers Accepted

*(omitted — `deferred_execution_blockers` in `state.json` is empty)*

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Install `pip-audit` in the execution environment before sprint execution begins | Head of Engineering | No |
| Verify `dependency-vuln-rescan.yml` post-merge run once EPIC-06's PR lands (ST-21's own AC) | Director of Quality | No |

No outstanding action is marked `Blocker? Yes`.

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — see `sprint_goal.md`
**Scope confirmed:** Confirmed — all 26 items, 6 EPICs, within confirmed capacity
**Capacity confirmed:** Confirmed — 23.75 days vs ~24-28 day band; buffer-floor advisory (§1.5) acknowledged, proceed with full scope per the explicit "use full capacity" instruction carried into this cycle (`sprint_capacity.md`)
**Deferred execution blockers accepted (if any):** N/A — none present
**Signed off by:** Product Owner
**Date:** 2026-08-11
