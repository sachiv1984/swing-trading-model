**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-08-09
**Cycle:** 2026-08-08__release-v8.5
**Release:** v8.5
**Sprint Goal:** Clear the full ready frontend-correctness, design-consistency, and security-hardening slate across all 25 scoped stories — see `sprint_goal.md`
**Backlog Slice Source:** original `stage4_backlog_slice.md`

# Sprint Backlog — 2026-08-08__release-v8.5

## Merge Order

EPIC merge sequence: **EPIC-01 → EPIC-03 → EPIC-04 → EPIC-02 → EPIC-05 → EPIC-06** (per `sprint_planning_notes.md` Execution Sequence; EPIC-03 must land before EPIC-04's ST-09/ST-13 per RISK-01).

`execution_state.json` owner: **EPIC-01** (first in execution order). All other EPIC branches must check for `execution_state.json` existence before creating their own version — if found, read it and append their EPIC's section rather than overwrite.

Shared files across EPICs (see `sprint_planning_notes.md` Multi-EPIC Execution Notes for full detail):
- `docs/specs/frontend/design_system.md` — EPIC-03 (ST-06), EPIC-04 (ST-09/ST-10/ST-13) — EPIC-03 owns canonical version, EPIC-04 rebases after EPIC-03 merges.
- `docs/specs/frontend/pages/reports.md` — EPIC-03 (ST-08) only.
- `docs/specs/frontend/pages/screener_results.md` — EPIC-06 (ST-21) only.
- `release_planning_prompt.md` / `CLAUDE.md` — EPIC-06 (ST-23, ST-24) — both within the same EPIC, no cross-EPIC collision.

---

## Sprint Scope

### EPIC-01 — Production Correctness Fixes

**Maps to:** S2-01
**Owner:** Head of Backend Engineering; Infrastructure & Operations Owner
**Estimated effort:** 1.0
**Risk IDs:** RISK-03
**Execution sequence:** 1

#### ST-01 — Fix GET /analytics/tag-performance 500 on staging (missing trade_tags column ensure)

**Owner:** Head of Backend Engineering
**Estimated effort:** 0.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None

**Notes:** RISK-03 — either candidate fix (narrow endpoint-level ensure vs. broader startup-sequence `ensure_trade_plans_table()`) is acceptable; AC requires an explicit no-regression confirmation against existing `trade_plans.py` endpoints before merge regardless of approach.

**Staging-only ACs:** None

---

#### ST-02 — Confirm api-key-cross-environment-check.yml is genuinely running, not silently skipping

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.5
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Notes:** Requires inspecting a real workflow run's log (not just the YAML source) to confirm the comparison step actually executes; the skip-guard hardening decision should be recorded explicitly either way.

**Staging-only ACs:** None

---

### EPIC-02 — Security Hardening

**Maps to:** S2-02
**Owner:** Cybersecurity & Trust Lead; Metrics Definitions & Analytics Owner
**Estimated effort:** 2.75
**Risk IDs:** RISK-06
**Execution sequence:** 4

#### ST-03 — Security fix false-positive rate assessment (BLG-SEC-02)

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** 1.0
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Notes:** Gate condition (30-day production observation window) confirmed cleared 2026-08-08 — 37 days in production since v6.4 with no incident on record. Coordinate with `BLG-QA-70`'s own equivalent finding per the AC.

**Staging-only ACs:** None

---

#### ST-04 — Recurring dependency vulnerability re-scan cadence (consolidated)

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** 1.0
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** Covers both `pip-audit` and `npm audit`; combined cadence (sprint planning + scheduled interval) must be documented alongside the scheduled job itself.

**Staging-only ACs:** None

---

#### ST-05 — API key rotation runbook

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** 0.75
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Staging-only ACs:** None

---

### EPIC-03 — Frontend Correctness Fixes

**Maps to:** S2-03
**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 2.25
**Risk IDs:** RISK-01
**Execution sequence:** 2

#### ST-06 — Register muted/muted-foreground (and other dead -muted classes) in tailwind.config.js

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 1.25
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None — but must land first within the sprint, ahead of EPIC-04/ST-09 and ST-13 (RISK-01)

**Notes:** Design Pre-Approved (`design_gate.md`) — restores an already-canonical token, no new visual design decision. Frontend-visible change: Playwright coverage or staging sign-off required per CLAUDE.md.

**Staging-only ACs:** None — Playwright coverage is the expected CI-verifiable path.

---

#### ST-07 — Frontend wiring to populate trade_plans.thesis_model_version/thesis_prompt_version on save

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.3
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** `Provisional-Target: v8.5` already carried on this item — horizon-planned for this release. Hidden metadata fields, not displayed in any UI — Design Not Applicable.

**Staging-only ACs:** None

---

#### ST-08 — Reconcile Monthly P&L vs Tax Year table's exact-zero P&L colour convention

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.7
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None

**Notes:** Design Required — colour-convention decision already resolved at Design Gate (`docs/design/2026-08-08__release-v8.5/exact-zero-pnl-colour-convention/decision_record.md`); this story implements the decided convention. Resolves `DEV-REPORTS-ST01-02`. Frontend-visible change: Playwright coverage or staging sign-off required per CLAUDE.md.

**Staging-only ACs:** None — Playwright coverage is the expected CI-verifiable path.

---

### EPIC-04 — Design System & Contrast Consistency Audit

**Maps to:** S2-04
**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design
**Estimated effort:** 8.5
**Risk IDs:** RISK-01, RISK-02
**Execution sequence:** 3

#### ST-09 — Design token audit: v6.7 contrast fix consistency

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 1.0
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** EPIC-03/ST-06 (must complete first — RISK-01)

**Notes:** Audit-only completion is a valid, complete outcome (RISK-02) — any drift found is filed as a follow-up backlog item, not fixed in-story.

**Staging-only ACs:** None

---

#### ST-10 — Empty-state illustration/microcopy consistency pass

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 2.0
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Notes:** Design Required — microcopy pattern decision already resolved at Design Gate (`docs/design/2026-08-08__release-v8.5/empty-state-microcopy-pattern/decision_record.md`); AC ships a live fix (`TradePlans.js`) plus pattern applied to ≥3 pages total.

**Staging-only ACs:** None

---

#### ST-11 — Confirm theme-toggle persistence across sessions

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.75
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None

**Notes:** Verification of already-established behaviour; any gap found is fixed or filed as a follow-up, not a new design decision.

**Staging-only ACs:** None

---

#### ST-12 — Mobile responsive audit for PerformanceAnalytics page

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 1.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None

**Notes:** Design Pre-Approved — audits/fixes against the page's already-approved layout spec (`analytics.md` v2.0); corrective only. Frontend-visible change if any fix ships: Playwright coverage or staging sign-off required per CLAUDE.md.

**Staging-only ACs:** None — Playwright coverage is the expected CI-verifiable path for any shipped fix.

---

#### ST-13 — Dark/light theme contrast audit follow-up

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 1.25
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** EPIC-03/ST-06 (must complete first — RISK-01)

**Notes:** Audit-only completion is a valid, complete outcome (RISK-02) — targeted follow-up scoped to confirm no further gaps remain beyond BLG-FE-87/88/89's known fixes.

**Staging-only ACs:** None

---

#### ST-14 — Ad hoc component inventory: candidates for shared design-system extraction

**Owner:** Head of UX & Design
**Estimated effort:** 2.0
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** None

**Notes:** AC explicitly requires Head of UX & Design sign-off on the inventory/ranking deliverable. Audit-only completion is a valid, complete outcome (RISK-02).

**Staging-only ACs:** None

---

### EPIC-05 — Frontend UX Review & Documentation

**Maps to:** S2-05
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 7.35
**Risk IDs:** RISK-02
**Execution sequence:** 5

#### ST-15 — Nav bar redesign exploration

**Owner:** Head of UX & Design
**Estimated effort:** 2.0
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None

**Notes:** Design Not Applicable (no live UI change this cycle) — exploration/recommendation document. If redesign recommended, the resulting implementation item is filed and gated in a future cycle, not built this sprint.

**Staging-only ACs:** None

---

#### ST-16 — User journey map: SI-05 Telegram digest to app action

**Owner:** Head of UX & Design
**Estimated effort:** 1.25
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** None

**Notes:** AC explicitly requires Head of UX & Design sign-off. Documentation deliverable only, no live UI change this cycle.

**Staging-only ACs:** None

---

#### ST-17 — Reusable empty-state component spec for Base44 prompts

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.75
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** Draws on EPIC-04/ST-10's decision record (reference only, not a hard block)

**Notes:** Spec-writing deliverable for future reference; no component ships or is applied this cycle.

**Staging-only ACs:** None

---

#### ST-18 — Reports page information hierarchy review

**Owner:** Head of UX & Design
**Estimated effort:** 1.25
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** None

**Notes:** AC explicitly requires Head of UX & Design review. Expected path is "findings documented, fix filed as follow-up if not resolved in-story" — deferral is the expected outcome, not a shortfall.

**Staging-only ACs:** None

---

#### ST-19 — Rework ChartStyle to drop style-src 'unsafe-inline' dependency, if/when a consumer adopts ChartContainer

**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Estimated effort:** 1.8
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

**Dependencies:** None (in-story condition: `ChartContainer` consumer adoption — unresolved as of planning)

**Notes:** Conditional/deferred scope — `chart.js` has zero live consumers today; most likely closes as "confirmed still unused, no action needed." If a consumer is adopted during execution, re-classify as needing a fresh design pass before implementing (per `design_gate.md` Notes) — do not proceed on the pre-cleared Design Not Applicable outcome. Apply LL-v2.0-P4-2's `test_scenarios` roll-up backstop if triggered (see `sprint_planning_notes.md` Outstanding Actions).

**Staging-only ACs:** None — if triggered, Playwright coverage is the expected CI-verifiable path.

---

#### ST-20 — Playwright/staging visual verification of calendar.js when a real consumer is added

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.3
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`

**Dependencies:** None (in-story condition: `ui/calendar.js` consumer adoption — unresolved as of planning)

**Notes:** Deferred-trigger item — zero live consumers today; closes when a consumer ships with its own Playwright coverage or staging sign-off, referencing that story/PR.

**Staging-only ACs:** None

---

### EPIC-06 — Analytics & Governance Process Fixes

**Maps to:** S2-06
**Owner:** Metrics Definitions & Analytics Owner; Head of Specs Team; QA & Testing Owner
**Estimated effort:** 5.3
**Risk IDs:** RISK-04
**Execution sequence:** 6

#### ST-21 — Regime distribution metric over screener history

**Owner:** Metrics Definitions & Analytics Owner
**Estimated effort:** 1.25
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`

**Dependencies:** None

**Notes:** Gate condition (screener live ≥ 60 days) confirmed cleared 2026-08-08 — 103 days live. Design Required — placement/control/colour decision already resolved at Design Gate (`docs/design/2026-08-08__release-v8.5/regime-distribution-panel/decision_record.md`); implements against the system's actual binary risk-on/risk-off regime model (see `design_gate.md` ST-21 taxonomy correction note), not the illustrative four-way taxonomy in the original idea-intake wording.

**Staging-only ACs:** None

---

#### ST-22 — Product Value Ratio historical trend chart

**Owner:** Metrics Definitions & Analytics Owner
**Estimated effort:** 1.0
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-22`

**Dependencies:** None

**Notes:** Internal governance-tooling deliverable, not customer-facing product UI (Design Not Applicable, out of Head of UX & Design scope per `design_gate.md`).

**Staging-only ACs:** None

---

#### ST-23 — Release Planning does not reset root sprint_sealed to false on new-cycle publish

**Owner:** Head of Specs Team
**Estimated effort:** 0.9
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-23`

**Dependencies:** None

**Notes:** Governance-file patch (`release_planning_prompt.md` STEP 0) — CLAUDE.md §6 Governance File Edit Checklist (version bump, `OPERATIONAL_GUIDE.md` §14 sync, `prompt_change_log.md` entry) applies in the same commit (RISK-04). This is the exact gap observed live in this cycle's own `.claude_current_state.json` (`sprint_sealed: true` carried stale from `v8.4`'s seal) — see that file's own `_sprint_sealed_note`.

**Staging-only ACs:** None

---

#### ST-24 — CLAUDE.md §8 sibling-vs-sibling union clause for execution_state.json array fields

**Owner:** Head of Specs Team
**Estimated effort:** 0.9
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-24`

**Dependencies:** None

**Notes:** Governance-file patch (`CLAUDE.md` §8) — CLAUDE.md §6 checklist applies in the same commit (RISK-04).

**Staging-only ACs:** None

---

#### ST-25 — Fix unrestored sys.modules stubbing in test_alerts_service.py (cross-file test pollution)

**Owner:** QA & Testing Owner
**Estimated effort:** 1.25
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-25`

**Dependencies:** None

**Notes:** Matches the guarded pattern already used in `test_trade_service.py` — mechanically verifiable via a full suite run.

**Staging-only ACs:** None

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24-28 days |
| Total estimated effort (in-scope) | 27.15 days |
| Utilisation | ~97-113% of band (top of band, per `sprint_capacity.md §1.5`) |
| Over-allocation | No — within confirmed band; buffer-floor advisory acknowledged (see below) |

## Items Deferred This Sprint

None — all 25 items included.

## Deferred Execution Blockers Accepted

*(section omitted — `deferred_execution_blockers` was empty in `state.json`)*

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Install `pip-audit` before sprint execution so the pre-sprint vulnerability scan can run with real results | Infrastructure & Operations Owner | No |
| `OPERATIONAL_GUIDE.md` header (`4.147`) is 2 versions behind its own §14 table / `prompt_change_log.md` (`4.149`) — file a backlog item | Head of Specs Team | No |
| `DEV-EPIC02-ST03-01` re-triage (carried from `v8.4` closure) remains unresolved — surface again at this cycle's Post-Ship Closure if still open | Head of Specs Team | No |
| If a `ChartContainer` consumer is adopted during ST-19 execution, apply LL-v2.0-P4-2's `test_scenarios` roll-up backstop and re-classify the rendering/colour question as needing a fresh design pass | EPIC-05 owner | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed (agent-mediated, delegated authority) — see `sprint_goal.md`
**Scope confirmed:** Confirmed — all 25 items from `stage4_backlog_slice.md` included, 0 deferred, 0 over-allocation beyond the band ceiling
**Capacity confirmed:** Confirmed — ~27.15 days against the ~24-28 day band; buffer-floor (95%) advisory acknowledged as an intentional top-of-band sizing consistent with this session's standing "full capacity" instruction, not a fresh over-allocation requiring trimming (capacity check outcome is `pass`, not `warn` — see `sprint_capacity.md §1.5`)
**Deferred execution blockers accepted (if any):** N/A — none present
**Signed off by:** Product Owner (agent-mediated, delegated authority)
**Date:** 2026-08-09
