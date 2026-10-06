**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-10-06
**Cycle:** 2026-10-06__release-v9.10
**Release:** v9.10
**Sprint Goal:** Make every live stop come from one §11 parameter source, and show the ATR, multiplier, recalculation source and already-known exit conditions behind each position (BLG-BE-138, BLG-FE-193, BLG-FE-198), while clearing v9.10's lifecycle/gap-risk rulings and AI-governance, ops and QA hygiene items.
**Backlog Slice Source:** Original — `claude/cycles/2026-10-06__release-v9.10/stage4_backlog_slice.md`

# Sprint Backlog — 2026-10-06__release-v9.10

## Merge Order

**EPIC merge sequence:** EPIC-01 → EPIC-03 → EPIC-04 → EPIC-02. EPICs carrying `delegated_decision` rulings and Human-Delegation go first, so their external dependencies are raised early. EPIC-02, which depends on ST-01's ruling, merges last.

**`execution_state.json` owner:** EPIC-01. Every other EPIC branch must check whether the file exists before creating its own. If it exists, the branch appends its own section and does not overwrite.

**Shared files across EPICs:**
- `strategy_rules.md` (EPIC-01, EPIC-03): EPIC-01 owns it. EPIC-03 rebases after EPIC-01 merges.
- `strategy_version_registry.py` (EPIC-01 ST-05; EPIC-03 if a qualifying Change Log row is added).
- `position_endpoints.md` and `openapi.yaml` (EPIC-01 ST-01/02/03; EPIC-03 ST-12/14): EPIC-01 owns them. Take the union of field additions and the highest version.
- `positions.md`, `Positions.js` and `PositionCard.js` (EPIC-03 ST-12/14; EPIC-02 ST-06/08): EPIC-03 owns them. EPIC-02 rebases after EPIC-03 merges.
- `position_service.py` (EPIC-01; EPIC-03 ST-12 if routed there): EPIC-01 owns it.
- `prompt_change_log.md`: append-only.
- `current_roadmap.md`: EPIC-04 ST-20 only.

Full detail: `sprint_planning_notes.md § Shared-File Ownership Advisory`.

## Sprint Scope

### EPIC-01 — Stop-Parameter Correctness & ATR Integrity

**Maps to:** S2-01–S2-05
**Owner:** Head of Engineering; Strategy Rules & System Intent Owner (ruling); Backend Engineering Patterns Owner
**Estimated effort:** 8.50 days
**Risk IDs:** RISK-01, RISK-02
**Execution sequence:** 1

#### ST-01 — One source for §11 stop parameters across the on-load and nightly stop paths

**Owner:** Head of Engineering; Strategy Rules & System Intent Owner (ruling); Infrastructure & Operations Owner (production read)
**Estimated effort:** 4.00
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None (ST-02, ST-03, ST-05, ST-06 and ST-07 depend on it, see Dependency Map)

**Notes:** RISK-01. P1 Correctness Fast-Track. The parameter-authority ruling (AC 2) is the first sub-step, and the production-read Human-Delegation is raised at sprint start. ST-01 should also write the on-load/nightly source field (`stop_calculation_source`) that ST-06 needs (design gate obligation). The Settings fallback values are an observable UI change (design gate: Design Required), but the slice AC does not name a Playwright assertion for them. Add Playwright coverage, or file a backlog item before the PR opens (RISK-05). If ruling (b) or (c) is chosen, `strategy_rules.md` §12 changes under RISK-02.

**Staging-only ACs:** AC 1 (production `settings` read; the governed environment has only a staging `DATABASE_URL`, so this needs Human-Delegation). AC 6 (correction decision depends on the production open-position data from AC 1).

**Status at sprint open: ready**

---

#### ST-02 — Remove silent ATR fallbacks and record ATR provenance

**Owner:** Head of Engineering; Backend Engineering Patterns Owner
**Estimated effort:** 2.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** ST-01 (same `position_service.py` paths)

**Notes:** Adds `positions.atr_source`. `data_model.md`, `position_endpoints.md` and `openapi.yaml` change in the same commit (CLAUDE.md §2).

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-03 — Contract corrections: losing-stop formula, analyze side effects, settings-change effect

**Owner:** API Contracts & Documentation Owner; Head of Engineering
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** ST-01 (AC 2 ruling)

**Notes:** No new endpoints.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-04 — Unit-test the live exit decision and grace-period behaviour

**Owner:** QA & Testing Owner; Head of Engineering
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** Can run in parallel while the ST-01 ruling is pending.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-05 — Rule on strategy-version registry coverage and enforce it with a test

**Owner:** Strategy Rules & System Intent Owner (ruling); Backend Engineering Patterns Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** ST-01 (if its ruling bumps `strategy_rules.md`)

**Notes:** See `sprint_planning_notes.md` Dependency Map note 1. Any qualifying `strategy_rules.md` Change Log row added by ST-11 or ST-13 after this story lands must add its registry entry in the same commit.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

### EPIC-03 — Lifecycle & Gap-Risk Strategy Boundary

**Maps to:** S2-11–S2-14
**Owner:** Strategy Rules & System Intent Owner; Head of Specs Team; Head of Engineering; Head of UX & Design
**Estimated effort:** 4.50 days
**Risk IDs:** RISK-02, RISK-05
**Execution sequence:** 2

#### ST-11 — Reconcile the lifecycle-state registry with strategy_rules.md §9

**Owner:** Strategy Rules & System Intent Owner (ruling); Head of Specs Team
**Estimated effort:** 1.00
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None

**Notes:** RISK-02. If the overlay becomes canonical, §9 is amended under §16, and the registry coupling to ST-05 applies.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-12 — Positions lifecycle badge agrees with the §6 grace window, in calendar days

**Owner:** Head of UX & Design; Head of Engineering
**Estimated effort:** 1.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** ST-11 (post-grace copy only; in-grace work is unblocked)

**Notes:** Locked spec `positions.md` v2.11. Needs a backend `lifecycle_reason` field. `position_endpoints.md` and `openapi.yaml` change in the same commit (design gate obligation). Playwright per the decision record §5.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-13 — Gap Risk Flag §13.3 ruling on UK-ticker earnings flags and day-0 timing

**Owner:** Strategy Rules & System Intent Owner (ruling)
**Estimated effort:** 0.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None

**Notes:** RISK-02. The ruling is an addendum to the v9.9 §13 review record. Tests may land in ST-14's commit.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-14 — Gap risk flag: disposition the standalone weekend-hold trigger and align trigger-timing label/spec with code

**Owner:** Head of Engineering; Head of UX & Design; Strategy Rules & System Intent Owner (sign-off)
**Estimated effort:** 1.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** ST-13

**Notes:** Default disposition is to remove `weekend_hold` (BLG-BE-136 scope). May shrink the `reasons` enum, in which case the contract and OpenAPI change in the same commit. Must also update the prior-cycle `ux_spec.md` §5, which its AC 3 names. Playwright for the label.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

### EPIC-04 — AI Governance, Ops & QA Hygiene

**Maps to:** S2-15–S2-21
**Owner:** AI Compliance & Governance Officer; Infrastructure & Operations Owner; QA & Testing Owner; Head of Specs Team
**Estimated effort:** 5.00 days
**Risk IDs:** RISK-03, RISK-04
**Execution sequence:** 3

#### ST-15 — AI chat advisory §13 quarterly self-audit checklist

**Owner:** AI Compliance & Governance Officer; Product Owner and Strategy Rules & System Intent Owner (sign-off)
**Estimated effort:** 0.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None

**Notes:** AC restated: the first review is a dated slot after sprint close.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-16 — AI model output logging completeness audit

**Owner:** AI Compliance & Governance Officer (sign-off); Head of Engineering
**Estimated effort:** 0.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** None

**Notes:** RISK-04. The code-path audit proceeds regardless. The silent-failure path in `database.create_claude_audit_entry()` is either fixed or filed as a remediation item.

**Staging-only ACs:** None. A live `claude_audit_log` read is only needed if the code-path audit cannot confirm completeness. If it is needed, it is Human-Delegation, and the AC 3 evidence is recorded as staging-only.

**Status at sprint open: ready**

---

#### ST-17 — Quarterly dependency update review

**Owner:** Infrastructure & Operations Owner; Cybersecurity & Trust Lead
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** None

**Notes:** Reuses `docs/security/npm_audit_rescan_triage_2026-10-06.md`. `react-scripts`-pinned findings are referred to `BLG-TECH-21`. Pre-sprint pip-audit is clean (60 deps).

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-18 — Confirm the stale-staging-deploy alert fires on a real stale-staging condition

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.50
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** None

**Notes:** RISK-04. Needs live Render/GitHub Actions control. Raise the Human-Delegation at sprint start.

**Staging-only ACs:** AC 1 (failing CI run against a real, deliberately introduced staging/main divergence). AC 2 (passing run after staging is restored).

**Status at sprint open: ready**

---

#### ST-19 — Add the Reports and Notifications pages to the axe accessibility scan

**Owner:** QA & Testing Owner
**Estimated effort:** 0.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

**Dependencies:** None

**Notes:** Design pre-approved. Fixes must use existing `design_system.md` tokens.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-20 — Correct the PO-05 pre-assessment and replay page spec wording

**Owner:** Head of Specs Team; Strategy Rules & System Intent Owner (acknowledgement)
**Estimated effort:** 0.50
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`

**Dependencies:** `ESC-CLOSE-20261006-01` ruling (resolved 2026-10-06)

**Notes:** RISK-03, resolved at planning by the named-file rule. ST-20 may edit `claude/roadmap/current_roadmap.md`'s PO-05 wording directly, in-sprint, within sealed AC 2, citing the Head of Specs Team ruling recorded in `sprint_planning_notes.md`. It does not route through the Roadmap Rebalance Engine. The caption change is wording-only (FI-P3-02 exception).

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-21 — Sign-off single-point-of-failure matrix

**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** 1.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`

**Dependencies:** None

**Notes:** Filed under `docs/ops/` (restated AC).

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

### EPIC-02 — Stop & Exit Transparency (build-and-ship)

**Maps to:** S2-06–S2-10
**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design; Product Owner
**Estimated effort:** 9.90 days
**Risk IDs:** RISK-05
**Execution sequence:** 4

#### ST-06 — Show ATR, active multiplier and recalculation source in the stop-loss cell

**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design
**Estimated effort:** 5.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** ST-01 (ruling and `stop_calculation_source`); ST-02 optional

**Notes:** RISK-05. Largest single item. Locked spec `positions.md` v2.11, Playwright per the decision record §5. Roadmap-committed (`BLG-FE-193`). May ship the false "daily" tooltip-claim removal as a first increment.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-07 — Trade Entry shows the stop and risk the system will actually store

**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Estimated effort:** 2.50
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** ST-01 (single fallback-multiplier source)

**Notes:** Locked spec `position_form.md` v1.7. AC 1 is to be covered by Playwright, not a staging run.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-08 — Exit dialog pre-selects the exit reason the system already knows

**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design
**Estimated effort:** 1.00
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None

**Notes:** Roadmap-committed (`BLG-FE-198`). Defines the shared exit-condition predicate used by ST-09. Adds the `?exit=` deep link. Playwright.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-09 — Morning briefing card for §8 exit recommendations

**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design
**Estimated effort:** 1.25
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** ST-08 (shared predicate)

**Notes:** §13: display-only, deterministic, no AI call. Locked spec `dashboard.md` v3.7. Playwright.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

#### ST-10 — Recent Trades badge shows a neutral glyph for a break-even trade

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Notes:** Extends `tests/e2e/recent-trades-zero-pnl-badge.spec.js`.

**Staging-only ACs:** None.

**Status at sprint open: ready**

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24-28 days (top edge 28.00) |
| Total estimated effort (in-scope) | 27.90 days |
| Utilisation | 99.6% (above the §1.5 95% buffer floor; Product Owner: proceed at ceiling, 2026-10-06) |
| Over-allocation | No |

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| — | — | None. All 21 slice items are in scope. |

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Record `ESC-CLOSE-20261006-01` as Resolved in `closure_escalations.md` and `.claude_current_state.json` `open_escalations` (outside Sprint Planning's write scope) | Head of Specs Team | No |
| Ship `BLG-GOV-362` prompt patches with the CLAUDE.md §6 checklist | Head of Specs Team | No |
| Raise Human-Delegation for the ST-01 production read and the ST-18 live fire (ST-16 if needed) at sprint start | Infrastructure & Operations Owner | No |
| Rulings for ST-01, ST-05, ST-11 and ST-13, raised at sprint start | Strategy Rules & System Intent Owner | No |
| Add Playwright for ST-01's Settings fallback values, or file a backlog item before EPIC-01's PR opens | QA & Testing Owner | No |

## Product Owner Sign-Off

Sprint goal: Confirmed (as drafted), 2026-10-06
Buffer floor (99.6%): Proceed at ceiling, 2026-10-06
Sprint backlog: Confirmed, 2026-10-06
