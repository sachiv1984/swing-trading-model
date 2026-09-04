**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-09-04
**Cycle:** 2026-09-03__release-v9.1
**Release:** v9.1
**Sprint Goal:** Ship all 41 backlog-driven hygiene items in the v9.1 scope — frontend accessibility fixes, backend reliability/tech-debt cleanup, QA/test coverage, and governance/spec-process debt — so that every axe-core violation in `KNOWN_VIOLATIONS`, the npm build regression, and all 3 outstanding passed-target backlog items close clean with zero deviations.
**Backlog Slice Source:** Original — `claude/cycles/2026-09-03__release-v9.1/stage4_backlog_slice.md`

# Sprint Backlog — 2026-09-03__release-v9.1

## Merge Order

1. EPIC-01 → 2. EPIC-02 → 3. EPIC-03 → 4. EPIC-04 → 5. EPIC-05

**`execution_state.json` owner:** EPIC-01 (first in merge order). EPIC-02/03/04/05 branches must check for its existence before creating their own version — if found, append rather than overwrite.

**Shared files across EPICs:** `claude/strategy/strategy_rules.md` (EPIC-04/ST-21, EPIC-05/ST-34 — additive, non-colliding sections; EPIC-05 must rebase onto `main` after EPIC-04 merges before finalising ST-34, per CLAUDE.md §8 step 1). Full detail: `sprint_planning_notes.md` §Multi-EPIC Execution Notes.

---

## Sprint Scope

### EPIC-01 — Frontend Accessibility & UI Consolidation

**Maps to:** S2-01
**Owner:** Frontend Specifications & UX Documentation Owner; Director of Quality
**Estimated effort:** 3.70 days
**Risk IDs:** RISK-01
**Execution sequence:** 1

#### ST-01 — Fix DashboardHome "AI Advisory" badge colour-contrast violation

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.1
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None

**Notes:** Design already cleared at design gate (Design Required → colour decision recorded, `docs/design/2026-09-03__release-v9.1/dashboardhome-ai-advisory-badge-contrast/decision_record.md`; `dashboard.md` v3.4). Implementation applies the already-approved token change only.

**Staging-only ACs:** None

---

#### ST-02 — Add accessible names to TradePlan select elements

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Notes:** Design Pre-Approved — semantic-attribute addition only, no layout change.

**Staging-only ACs:** None

---

#### ST-03 — Add discernible text to Settings page combobox buttons

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Notes:** Design Pre-Approved — `aria-label` addition only.

**Staging-only ACs:** None

---

#### ST-04 — Add labels to Settings page form inputs

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** Design Pre-Approved (Product Owner downgrade from default Design Required — reuse-only, no new visible copy). If implementation surfaces genuinely new visible label text, return to design gate before merging.

**Staging-only ACs:** None

---

#### ST-05 — Fix Settings page subtitle colour-contrast violation

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.1
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Notes:** Design Pre-Approved — verification against already-approved token, not a new colour decision; finding is non-reproducing across repeated axe runs.

**Staging-only ACs:** None

---

#### ST-06 — Consolidate PositionSizingWidget.js / WhatIfSizingPreview.js debounced-fetch boilerplate

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None

**Notes:** Design Not Applicable — pure internal refactor; existing Playwright coverage must pass unchanged (debounce behaviour not altered).

**Staging-only ACs:** None

---

#### ST-07 — Add keyboard-navigation requirements section for table-based page specs

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 1.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** Documentation-only; no code ships this cycle. Targets Positions, Trade History, and Red Flag Journal specs at minimum (per backlog slice AC — "at least").

**Staging-only ACs:** None

---

### EPIC-02 — Backend Reliability & Technical Debt

**Maps to:** S2-02
**Owner:** Backend Engineering Patterns Owner; Head of Engineering
**Estimated effort:** 6.10 days
**Risk IDs:** RISK-02
**Execution sequence:** 2

#### ST-08 — Fix npm dependency tree production-build regression after routine npm update

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 1.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None — but must execute first within this EPIC (currently-reproducible build-breaking bug; release plan sequencing constraint)

**Notes:** Sequenced first within EPIC-02 per `release_plan.md ## Execution Plan`.

**Staging-only ACs:** None

---

#### ST-09 — Log sector-concentration adjustment's fail-open exception handler

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 0.1
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None

**Notes:** No change to fail-open return behaviour.

**Staging-only ACs:** None

---

#### ST-10 — Consolidate 4 independent sector-lookup implementations

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 0.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Notes:** All 4 existing test suites must pass unchanged in behaviour.

**Staging-only ACs:** None

---

#### ST-11 — Move raw SQL execution out of analytics.py/digest.py routers into the database layer

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 4.0
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None

**Notes:** RISK-02 (Medium) — structural move only, no query rewrite; full existing test suite for both routers must pass unchanged; no new raw SQL introduced anywhere outside `database.py`.

**Staging-only ACs:** None

---

### EPIC-03 — QA & Test Coverage

**Maps to:** S2-03
**Owner:** Director of Quality; QA & Testing Owner
**Estimated effort:** 3.30 days
**Risk IDs:** RISK-03
**Execution sequence:** 3

#### ST-12 — Add Playwright coverage for Arc5ComplianceSection's events_per_week value formatting

**Owner:** QA & Testing Owner
**Estimated effort:** 0.1
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None

---

#### ST-13 — Add Playwright coverage for Arc5ComplianceSection's top_rule_breach text formatting

**Owner:** QA & Testing Owner
**Estimated effort:** 0.1
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None

---

#### ST-14 — Add Playwright coverage for Arc5ComplianceSection's null-value handling

**Owner:** QA & Testing Owner
**Estimated effort:** 0.1
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None

---

#### ST-15 — Build a quality trend index aggregating DEV-* records over time

**Owner:** Director of Quality
**Estimated effort:** 1.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None

**Notes:** Backfill from available cycle history required.

**Staging-only ACs:** None

---

#### ST-16 — Definition-of-Done compliance spot-check across the last 5 cycles

**Owner:** Director of Quality
**Estimated effort:** 0.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None

---

#### ST-17 — Spot-check Tier 1/Tier 2 DoQ severity-labelling consistency

**Owner:** Director of Quality
**Estimated effort:** 0.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None

---

#### ST-18 — Define regression suite runtime budget & reporting

**Owner:** QA & Testing Owner
**Estimated effort:** 0.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None

---

### EPIC-04 — Governance Process Debt & Overdue Dispositions

**Maps to:** S2-04
**Owner:** Head of Specs Team; PMO Lead; Strategy Rules & System Intent Owner
**Estimated effort:** 3.90 days
**Risk IDs:** RISK-04
**Execution sequence:** 4

#### ST-19 — Fix governance_sync.yml auto-close gap for split work/completion commits

**Owner:** PMO Lead
**Estimated effort:** 0.75
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

**Dependencies:** None

**Notes:** Must preserve existing `BLG-GOV-285` anti-premature-closure protection.

**Staging-only ACs:** None

---

#### ST-20 — Document convention for "Signed off by: PENDING" placeholders in Class 3 docs

**Owner:** Head of Specs Team
**Estimated effort:** 0.1
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None

---

#### ST-21 — Add ST-06 §13 CONDITIONAL clearance to strategy_rules.md §13.5 roster

**Owner:** Strategy Rules & System Intent Owner
**Estimated effort:** 0.1
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`

**Dependencies:** None

**Notes:** RISK-04 — `claude/strategy/strategy_rules.md` is outside standard Sprint Execution write scope (`execution_prompt.md §7`). Route through delegated/agent-mediated Strategy Rules & System Intent Owner sign-off per `execution_prompt.md §5.3`. If `strategy_rules.md`'s version is bumped: CLAUDE.md §6 checklist applies in the same commit. Coordinate with ST-34 (EPIC-05) — see Merge Order shared-file note.

**Staging-only ACs:** None

---

#### ST-22 — Fix recurrence-check false positive — require reading the named target file directly

**Owner:** Head of Specs Team
**Estimated effort:** 0.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-22`

**Dependencies:** None

**Notes:** Standard CLAUDE.md §6 governance file edit checklist applies (`lessons_learnt_prompt.md` version bump, OPERATIONAL_GUIDE.md §14, prompt_change_log.md entry).

**Staging-only ACs:** None

---

#### ST-23 — AI feature usage quarterly review (BLG-GOV-63 mandate)

**Owner:** AI Compliance & Governance Officer
**Estimated effort:** 0.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-23`

**Dependencies:** None

**Notes:** Next review date to record: 2026-11-29.

**Staging-only ACs:** None

---

#### ST-24 — Correct trade_plan.md §5.1 stale "Risk/Reward Notes" field reference

**Owner:** Head of Specs Team
**Estimated effort:** 0.1
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-24`

**Dependencies:** None — but must execute before ST-25 (same file, `trade_plan.md`)

**Notes:** See Dependency Map (`sprint_planning_notes.md`).

**Staging-only ACs:** None

---

#### ST-25 — Document PositionSizingWidget baseline in trade_plan.md

**Owner:** Frontend Specifications & UX Documentation Owner
**Estimated effort:** 0.75
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-25`

**Dependencies:** ST-24 (must complete first — same file)

**Notes:** See Dependency Map (`sprint_planning_notes.md`).

**Staging-only ACs:** None

---

#### ST-26 — Physically create the Displacement Debt Register and close ESC-EXEC-20260727-02

**Owner:** PMO Lead
**Estimated effort:** 0.1
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-26`

**Dependencies:** None

**Notes:** `claude/roadmap/*` is outside standard Sprint Execution write scope (`execution_prompt.md §7`). Route through delegated/agent-mediated PMO Lead / Head of Specs Team write authority per the pattern already carried via `ESC-EXEC-20260818-02`. Must also close `ESC-EXEC-20260727-02` and `ESC-EXEC-20260818-02`.

**Staging-only ACs:** None

---

#### ST-27 — Scope governed-vs-ad-hoc backlog scope visibility tally

**Owner:** PMO Lead
**Estimated effort:** 0.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-27`

**Dependencies:** None

**Notes:** First data point to be recorded retroactively for v7.1/this cycle where determinable.

**Staging-only ACs:** None

---

#### ST-28 — Give Specs_Index.md a proper Changelog table

**Owner:** Head of Specs Team
**Estimated effort:** 0.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-28`

**Dependencies:** None

**Notes:** Must convert existing `**Last Updated:**` chaining to a single-line summary per `shared_standards.md §16.14`.

**Staging-only ACs:** None

---

### EPIC-05 — Spec & Knowledge Debt / AI Governance Register

**Maps to:** S2-05
**Owner:** Head of Specs Team; AI Compliance & Governance Officer
**Estimated effort:** 10.50 days
**Risk IDs:** RISK-05
**Execution sequence:** 5

#### ST-29 — Consolidate duplicate empty-state pattern specs

**Owner:** Head of Specs Team
**Estimated effort:** 1.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-29`

**Dependencies:** None

**Notes:** `design_system.md` remains the single source; remove duplicates from at least 3 page specs.

**Staging-only ACs:** None

---

#### ST-30 — Build canonical AI feature touchpoint register with per-feature §13 classification

**Owner:** AI Compliance & Governance Officer
**Estimated effort:** 1.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-30`

**Dependencies:** None

**Notes:** Must cover all currently-shipped AI touchpoints.

**Staging-only ACs:** None

---

#### ST-31 — Spec-to-backlog traceability audit

**Owner:** Head of Specs Team
**Estimated effort:** 1.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-31`

**Dependencies:** None

**Notes:** Orphans found must be resolved, not just listed.

**Staging-only ACs:** None

---

#### ST-32 — Quarterly retrospective: estimated vs. actual effort bands

**Owner:** FinOps & Resource Architect
**Estimated effort:** 0.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-32`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None

---

#### ST-33 — Automated Specs_Index.md freshness check against live spec files

**Owner:** Head of Specs Team
**Estimated effort:** 0.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-33`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None

---

#### ST-34 — Add worked example of the ATR-based sizing edge case to strategy_rules.md

**Owner:** Strategy Rules & System Intent Owner
**Estimated effort:** 0.5
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-34`

**Dependencies:** None

**Notes:** Planning-time catch (not named in `release_plan.md`'s risk register) — same restricted-file class as ST-21/RISK-04: `claude/strategy/strategy_rules.md` is outside standard Sprint Execution write scope. Route through the same delegated/agent-mediated Strategy Rules & System Intent Owner sign-off pattern as ST-21. Documentation only — no functional/behavioural change.

**Staging-only ACs:** None

---

#### ST-35 — Formalise minimum-interval guideline between scheduled rebalances

**Owner:** Director of HR
**Estimated effort:** 0.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-35`

**Dependencies:** None

**Notes:** Documented in `claude/charter/team_charter.md` or `CLAUDE.md §5` — Director of HR + Head of Specs Team sign-off, both agent-mediated per established precedent (e.g. `team_charter.md` v1.6→v1.7, Sprint Execution ST-07).

**Staging-only ACs:** None

---

#### ST-36 — Base44 generation failure-mode log

**Owner:** Head of Specs Team
**Estimated effort:** 0.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-36`

**Dependencies:** None

**Notes:** Backfill at least the known recurring modes (dark-mode class pairs, contrast).

**Staging-only ACs:** None

---

#### ST-37 — Canonical "win rate" vs "hit rate" definitions

**Owner:** Head of Specs Team
**Estimated effort:** 0.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-37`

**Dependencies:** None

**Notes:** Reconcile at least Performance Analytics and Reports specs.

**Staging-only ACs:** None

---

#### ST-38 — Formal definition for the "90-day trade window" cited in SI-02 gate readings

**Owner:** Metrics Definitions & Analytics Canonical Owner
**Estimated effort:** 0.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-38`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None

---

#### ST-39 — Effort-band accuracy retrospective

**Owner:** Head of Specs Team
**Estimated effort:** 0.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-39`

**Dependencies:** None

**Notes:** Process must be documented for repeat use.

**Staging-only ACs:** None

---

#### ST-40 — Extract PVR and Skill-Silo metrics from rebalance prose into structured state fields

**Owner:** Head of Specs Team
**Estimated effort:** 0.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-40`

**Dependencies:** None

**Notes:** Deliverable is a `roadmap_prompt.md` edit (adds the two fields at its next `run roadmap` write) plus `state_field_owners.json` documentation — standard `claude/system/` agent-mediated authority applies (not a restricted-file case like ST-21/ST-26/ST-34). Existing `last_rebalance_outcome` prose must remain unchanged in content.

**Staging-only ACs:** None

---

#### ST-41 — Canonical glossary consolidation

**Owner:** Head of Specs Team
**Estimated effort:** 1.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-41`

**Dependencies:** None

**Notes:** None.

**Staging-only ACs:** None

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24–28 working-day-equivalent units |
| Total estimated effort (in-scope) | 27.50 days |
| Utilisation | ~98.2% of the 28-day ceiling (within band) |
| Over-allocation | No — within confirmed band; buffer-floor advisory (95%) exceeded and acknowledged by Product Owner as an extension of the explicit "use full capacity" instruction (see `sprint_capacity.md`) |

## Items Deferred This Sprint

None.

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| File `OPERATIONAL_GUIDE.md` v4.171 prompt-change-log gap row | Head of Specs Team | No |
| Coordinate ST-21/ST-34 `strategy_rules.md` edits (rebase after EPIC-04 merges) | PMO Lead / Strategy Rules & System Intent Owner | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed as drafted, 2026-09-04 (`sprint_goal.md`)
**Scope confirmed:** Confirmed — all 41 items from `stage4_backlog_slice.md`, no deferrals
**Capacity confirmed:** Confirmed — 27.50d within the 24–28d band; buffer-floor advisory (98.2%) acknowledged as extension of "use full capacity"
**Deferred execution blockers accepted (if any):** N/A — `state.json.deferred_execution_blockers` empty
**Signed off by:** Product Owner
**Date:** 2026-09-04
