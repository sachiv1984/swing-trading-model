**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-08-12
**Cycle:** 2026-08-12__release-v8.7
**Release:** v8.7
**Sprint Goal:** Deliver v8.7's user-facing feature and theme-consistency completion work while closing the mandatory trade-plan data-integrity carryover from v8.6, backed by expanded test, security, reliability, and governance coverage across the release's remaining six EPICs — see `sprint_goal.md`
**Backlog Slice Source:** original `stage4_backlog_slice.md`

# Sprint Backlog — 2026-08-12__release-v8.7

## Merge Order

EPIC merge sequence: **EPIC-01 → EPIC-02 → EPIC-03 → EPIC-04 → EPIC-05 → EPIC-06 → EPIC-07** (per `sprint_planning_notes.md` Execution Sequence; EPIC-01 leads per the explicit user "user features to be prioritised" capacity directive; EPIC-03 sequenced after EPIC-01 because ST-08 depends on ST-06's shipped token usage).

`execution_state.json` owner: **EPIC-01** (first in execution order). All other EPIC branches must check for `execution_state.json` existence before creating their own version — if found, read it and append their EPIC's section rather than overwrite.

Shared files across EPICs (see `sprint_planning_notes.md` Multi-EPIC Execution Notes for full detail):
- `docs/specs/frontend/design_system.md` — EPIC-01 (ST-06, Modal / Dialog Theming) and EPIC-07 (ST-21, new "Gated variant" subsection). EPIC-01 merges first; EPIC-07 must rebase onto `main` after EPIC-01 merges before finalising its `design_system.md` changes.
- `docs/specs/data_model.md` — EPIC-01 (ST-03, new `is_ai_draft` migration block) and EPIC-02 (ST-07, DS-12 verification note, same `trade_plans` table). EPIC-01 merges first; EPIC-02 must rebase onto `main` after EPIC-01 merges before finalising any `data_model.md` note it adds.
- `execution_state.json` — all 7 EPICs (EPIC-01 owns the canonical file; all others append their own section).

---

## Sprint Scope

### EPIC-01 — User-Facing Product Features & UX Completion

**Maps to:** S2-01
**Owner:** Product Owner; Head of UX & Design
**Estimated effort:** 6.25
**Risk IDs:** RISK-01
**Execution sequence:** 1

#### ST-01 — Thesis pre-mortem / invalidation-condition capture at trade-plan entry

**Owner:** Product Owner; Head of UX & Design
**Estimated effort:** M
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None

**Notes:** Design cleared — `docs/specs/frontend/pages/trade_plan.md` v1.5 §5.1 (`decision_record.md`, Design Gate). Classified autonomous per `sprint_planning_prompt.md` §3.1 fast-path (c) — new field implemented against a locked frontend spec, Playwright feasibility confirmed at Design Gate.

**Status at sprint open:** ready

**Staging-only ACs:** None

---

#### ST-02 — Consume trade_plan_linked/trade_plan_id in the position-entry flow

**Owner:** Product Owner; Head of UX & Design
**Estimated effort:** XS
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Notes:** Design cleared — `docs/specs/frontend/pages/trade_plan.md` v1.5 §10.6. Backend response fields (`trade_plan_linked`/`trade_plan_id`) already shipped in v8.6 (ST-03) — this item is frontend consumption only.

**Status at sprint open:** ready

**Staging-only ACs:** None

---

#### ST-03 — Persist isAiDraft flag on trade_plans for AI-origin display badges

**Owner:** Product Owner; Head of UX & Design
**Estimated effort:** S
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Notes:** Badge display already fully specified (`trade_plan.md` §10.5, v1.4, v8.6; referenced in known deviation `DEV-v8.6-ST02-01`) — this item only persists the flag server-side. New DB migration required (`trade_plans.is_ai_draft`) — see `data_model.md` shared-file advisory above.

**Status at sprint open:** ready

**Staging-only ACs:** None

---

#### ST-04 — SI-02 Gate Status section (Reports.js) light/dark theme fix

**Owner:** Product Owner; Head of UX & Design
**Estimated effort:** S
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** Design Pre-Approved — same dark-only-token-pairing defect class as established `design_system.md` precedent (`BLG-FE-87/88/95` lineage); corrective, not new design.

**Status at sprint open:** ready

**Staging-only ACs:** None

---

#### ST-05 — Unrealised P&L card (Reports.js) light/dark theme fix

**Owner:** Product Owner; Head of UX & Design
**Estimated effort:** S
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Notes:** Design Pre-Approved — identical root cause and precedent as ST-04 (sibling backlog item, same discovery pass).

**Status at sprint open:** ready

**Staging-only ACs:** None

---

#### ST-06 — Convert 4 hardcoded dark-only modals to theme-aware tokens

**Owner:** Product Owner; Head of UX & Design
**Estimated effort:** S
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** Depends on `BLG-FE-147` (v8.6, shipped — tokens already registered). ST-08 (EPIC-03) depends on this item completing first (RISK-03).

**Notes:** Design Pre-Approved — exact 4 files already named at `design_system.md` v1.9 (Modal / Dialog Theming, v8.6). Must land before ST-08's Playwright authoring — see Execution Sequence.

**Status at sprint open:** ready

**Staging-only ACs:** None

---

### EPIC-02 — Trade-Plan Data Integrity Closure

**Maps to:** S2-02
**Owner:** Head of Engineering; Data Model, Domain & Schema Owner
**Estimated effort:** 1.00
**Risk IDs:** RISK-02
**Execution sequence:** 2

#### ST-07 — Staging verification of ST-03's (v8.6) trade-plan-linkage enforcement, and legacy orphaned-row audit

**Owner:** Head of Engineering; Data Model, Domain & Schema Owner
**Estimated effort:** S
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** P1, mandatory — PO risk-acceptance condition from v8.6 ("do not defer further"). Staging/live-Postgres access re-confirmed unavailable in this sandbox at sprint planning (see `sprint_planning_notes.md` Pre-sprint Planning Required Decisions) — Product Owner (agent-mediated) re-confirmed proceeding via best-available proxy, with the standing condition that any of the 11 known legacy rows found `status='active'` escalates to its own P0 immediately, not folded into this item's timeline.

**Status at sprint open:** ready

**Staging-only ACs:** AC-01 ("On staging (or production, read-only): confirm `POST /portfolio/position` links a trade plan by default..."), AC-02 ("Live query confirms 0 rows... matching `status='active' AND position_id IS NULL`"), AC-03 ("DS-12 CHECK constraint... confirmed present and `NOT VALID` on the live table") — all three require live staging/production database access that CI cannot reproduce; see planning-time resolution above. A backlog item covering the residual gap already exists (`BLG-BE-96` — this story itself); no new backlog filing required.

---

### EPIC-03 — Test Coverage for Shipped UI & Financial Correctness

**Maps to:** S2-03
**Owner:** QA & Testing Owner
**Estimated effort:** 1.50
**Risk IDs:** RISK-03
**Execution sequence:** 3

#### ST-08 — Playwright coverage for the remaining shadcn token call-site families left untested by v8.6/ST-04

**Owner:** QA & Testing Owner
**Estimated effort:** S
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** ST-06 (EPIC-01) must complete first — selectors depend on ST-06's shipped token conversion remaining stable (RISK-03).

**Notes:** Sequenced after EPIC-01 in Execution Sequence to satisfy this dependency.

**Status at sprint open:** ready

**Staging-only ACs:** None — CI-runnable Playwright coverage against real computed styles.

---

#### ST-09 — End-to-end integration assertion for tax-year boundary trade rows

**Owner:** QA & Testing Owner
**Estimated effort:** XS
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None

**Notes:** Backend unit/integration test only; no UI.

**Status at sprint open:** ready

**Staging-only ACs:** None

---

### EPIC-04 — Backend Reliability & Performance Hardening

**Maps to:** S2-04
**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 4.50
**Risk IDs:** RISK-04
**Execution sequence:** 4

#### ST-10 — Extend the BLG-BE-57 retry/backoff audit pattern to Gemini API call sites

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** M
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Notes:** Applies an already-established pattern (`BLG-BE-57`); no new design decision. Design Gate: no §13 review required (non-functional reliability wrapper, no new AI-provider call semantics).

**Status at sprint open:** ready

**Staging-only ACs:** None — failure modes (timeout, rate-limit, transient 5xx) are testable via mocked call sites in CI.

---

#### ST-11 — N+1 query audit across trade/position list endpoints

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** M
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None

**Notes:** Scope explicitly bounded (RISK-04) — audit + fix of clearly-attributable cases only; anything requiring broader refactor filed as a follow-up backlog item rather than expanded in-cycle.

**Status at sprint open:** ready

**Staging-only ACs:** None

---

#### ST-12 — SI-04 schema requirements pre-design

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** S
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None

**Notes:** Schema-only pre-work, no SI-04 feature implementation — documentation judgment call, classified `delegated_decision`.

**Status at sprint open:** ready

**Staging-only ACs:** None

---

### EPIC-05 — Security Hardening

**Maps to:** S2-05
**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** 3.50
**Risk IDs:** RISK-05
**Execution sequence:** 5

#### ST-13 — Prompt-injection resistance test for the Gemini thesis-generation endpoint

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** M
**Delegation class:** delegated_qa

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None

**Notes:** Design Gate: no §13 review required (test suite exercising an already-shipped endpoint, no new AI-provider call). Run against staging/test environment only, per RISK-05 mitigation — no production traffic generation.

**Status at sprint open:** ready

**Staging-only ACs:** None — test suite is CI/test-environment runnable; not literally a live-staging-deploy dependency.

---

#### ST-14 — Rate-limit audit on unauthenticated/low-auth endpoints

**Owner:** Cybersecurity & Trust Lead
**Estimated effort:** M
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** None

**Notes:** Inventory + config audit; gaps documented, trivial fixes done in-cycle, others filed as follow-ups (per AC).

**Status at sprint open:** ready

**Staging-only ACs:** None

---

### EPIC-06 — Operations & Infrastructure Debt

**Maps to:** S2-06
**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 3.00
**Risk IDs:** RISK-06
**Execution sequence:** 6

#### ST-15 — Render Starter-tier headroom reassessment

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None

**Notes:** Analysis/recommendation deliverable, no code change.

**Status at sprint open:** ready

**Staging-only ACs:** None (not a testable AC in the CI sense — infra dashboard research/reporting deliverable).

---

#### ST-16 — Render dashboard-only build/deploy path filter — canonical documentation + onboarding note

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** None

**Notes:** Documentation only — closes the root cause behind `BLG-OPS-82`/`BLG-OPS-90`.

**Status at sprint open:** ready

**Staging-only ACs:** None

---

#### ST-17 — Fix substring-match false negatives in check_api_performance_baseline_drift.py's find_missing_endpoints()

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** None

**Notes:** Closes the fix carried across 3 consecutive Post-Ship Closures (v8.4→v8.5→v8.6) — see `sprint_planning_notes.md` Carry-Forward Items.

**Status at sprint open:** ready

**Staging-only ACs:** None — regression test is CI-runnable.

---

### EPIC-07 — Governance & Spec Debt

**Maps to:** S2-07
**Owner:** Head of Specs Team
**Estimated effort:** 5.50
**Risk IDs:** RISK-07
**Execution sequence:** 7

#### ST-18 — CLAUDE.md §8 rule for shared JSON schema drift mid-sprint between sibling EPIC branches

**Owner:** Head of Specs Team
**Estimated effort:** S
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** None

**Notes:** Governance rule authorship — requires Head of Specs Team judgment on wording/placement.

**Status at sprint open:** ready

**Staging-only ACs:** None

---

#### ST-19 — Roadmap Unlock Tracker — consolidated view of all gated features and their conditions

**Owner:** Head of Specs Team
**Estimated effort:** M
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

**Dependencies:** None

**Notes:** Mechanical aggregation task, sourced from `scripts/scan_backlog_gate_conditions.py` output per the AC's own instruction.

**Status at sprint open:** ready

**Staging-only ACs:** None

---

#### ST-20 — §13 policy question: are confidence-interval-qualified "preview" analytics compatible with the deterministic/non-predictive boundary?

**Owner:** Head of Specs Team
**Estimated effort:** S
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-20`

**Dependencies:** None

**Notes:** Inherently a Strategy Rules & System Intent Owner policy determination — cannot be produced without that role's judgment. Per LL-v2.2-SP-01: no HoST design session artefact exists for this item beyond the AC itself; advisory only, does not block planning (this is a policy-authorship item, not a UX design item).

**Status at sprint open:** ready

**Staging-only ACs:** None

---

#### ST-21 — Canonical "gated" DataState variant and visual/interaction spec for not-yet-unlocked feature surfaces

**Owner:** Head of Specs Team
**Estimated effort:** M
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-21`

**Dependencies:** None

**Notes:** Design cleared at Design Gate — `decision_record.md`, `design_system.md` v1.10 new "Gated variant" subsection already scoped. Classified autonomous per fast-path (c) — implemented against a locked spec.

**Status at sprint open:** ready

**Staging-only ACs:** None

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24-28 day-equivalent units |
| Total estimated effort (in-scope) | 25.25 day-equivalent units |
| Utilisation | ~90-105% (band-dependent) |
| Over-allocation | No — within confirmed band; buffer-floor advisory noted and accepted (see `sprint_capacity.md` §1.5) |

## Items Deferred This Sprint

None. All 21 items in `stage4_backlog_slice.md` enter the sprint.

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Confirm ST-07 best-available-proxy execution approach and residual-gap documentation at delivery verification | Head of Engineering | No |
| Rebase `design_system.md` (EPIC-07 onto EPIC-01) and `data_model.md` (EPIC-02 onto EPIC-01) after EPIC-01 merges | EPIC-07 / EPIC-02 branch owners | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — see `sprint_goal.md`
**Scope confirmed:** Confirmed — all 21 items from `stage4_backlog_slice.md` enter the sprint, no deferrals
**Capacity confirmed:** Confirmed — 25.25 days within the ~24-28 day band; buffer-floor advisory accepted (proceed, no trim)
**Deferred execution blockers accepted (if any):** N/A — `deferred_execution_blockers` empty in `state.json`
**Signed off by:** Product Owner (agent-mediated, no counter-instruction raised)
**Date:** 2026-08-12
