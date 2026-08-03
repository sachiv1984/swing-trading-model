# Sprint Backlog — 2026-08-03__release-v8.1

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-08-03
**Cycle:** 2026-08-03__release-v8.1
**Release:** v8.1
**Sprint Goal:** Ship v8.1's operational-safety, governance-process, QA-debt, spec-debt, and backend-hardening scope — including the cross-EPIC execution-state structural fix and the release's one ready user-facing accessibility fix.
**Backlog Slice Source:** original `stage4_backlog_slice.md`

## Merge Order

**EPIC merge sequence:** EPIC-07 → EPIC-01 → EPIC-03 → EPIC-06 → EPIC-04 → EPIC-02 → EPIC-05 (see `sprint_planning_notes.md §Execution Sequence` for full rationale — EPIC-07 leads because it implements the new per-EPIC `execution_state.json` mechanism that all other EPICs should adopt from the start of their own branches).

**`execution_state.json` owner:** EPIC-07 (structural-transition owner — see `sprint_planning_notes.md §Multi-EPIC Execution Notes`). Once EPIC-07 merges, each subsequent EPIC branch creates its own `execution_state/EPIC-xx.json` rather than writing to a shared file.

**Shared files across EPICs:** `execution_state.json` (all 7), `shared_standards.md` (EPIC-07 §12 retirement; possibly EPIC-03/ST-09 §17 extension), `OPERATIONAL_GUIDE.md` §14 and `prompt_change_log.md` (EPIC-07 and any EPIC-03 item bumping a governance prompt version). Full ownership table: `sprint_planning_notes.md §Multi-EPIC Execution Notes`. EPICs opening after EPIC-07 must rebase onto `main` after EPIC-07 merges before finalising changes to these files.

---

## Sprint Scope

### EPIC-07 — Cross-EPIC Execution State Structural Fix

**Maps to:** S2-19
**Owner:** Head of Engineering
**Estimated effort:** 4.0 days (L)
**Risk IDs:** RISK-02
**Execution sequence:** 1

#### ST-19 — Implement per-EPIC `execution_state.json` files (Option 1)

**Owner:** Head of Engineering
**Estimated effort:** 4.0 (L)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-19`

*(The Execution Engine reads AC from `stage4_backlog_slice.md` directly via `spec_references`. Do not duplicate the full AC table here — the sprint backlog is a sequencing and ownership document.)*

**Dependencies:** None — sequenced first as the structural prerequisite for the other 6 EPICs' `execution_state.json` handling (see Merge Order above)

**Notes:** Design already reviewed and signed off (`ESC-EXEC-20260731-01`); this EPIC is implementation-only. Head of Engineering sign-off required before the new mechanism is used live (RISK-02).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-01 — User-Facing Accessibility Fix

**Maps to:** S2-01
**Owner:** Base44 Frontend Prompt Owner; Head of UX & Design
**Estimated effort:** 0.5 days (XS)
**Risk IDs:** RISK-01
**Execution sequence:** 2

#### ST-01 — Trade Plan tag-suggestion buttons use `onMouseDown`, not keyboard-operable

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** 0.5 (XS)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

*(The Execution Engine reads AC from `stage4_backlog_slice.md` directly via `spec_references`. Do not duplicate the full AC table here — the sprint backlog is a sequencing and ownership document.)*

**Dependencies:** None

**Notes:** Design Gate PASSED (Design Pre-Approved — `journal_components.md` §4 already mandates keyboard-navigable suggestions; `TradeEntry.js` already implements the correct `onClick` pattern to model the fix and its Playwright test on).

**Staging-only ACs:** None — the observable UI interaction AC is Playwright-verifiable in CI (per CLAUDE.md §2's general observable-AC rule, not the staging-only-evidence exception).

**Status at sprint open: ready**

---

### EPIC-03 — Governance Process Hardening

**Maps to:** S2-03, S2-04, S2-05, S2-06, S2-07, S2-08, S2-09
**Owner:** Product Owner; Challenger; FinOps & Resource Architect; Head of Engineering; Director of HR; AI Compliance & Governance Officer; Head of Specs Team
**Estimated effort:** 9.0 days (S+S+S+M+M+M+S)
**Risk IDs:** None
**Execution sequence:** 3

#### ST-03 — Formal sunset criteria for perennially-returning gated backlog items

**Owner:** Product Owner
**Estimated effort:** 1.0 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Notes:** None

**Staging-only ACs:** None

**Status at sprint open: ready**

#### ST-04 — Escalation path for Product Value Ratio's persistent Advisory tier

**Owner:** Head of Specs Team
**Estimated effort:** 1.0 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** If adopted, touches `roadmap_prompt.md` STEP 2.4 — apply the standard governance file edit checklist (CLAUDE.md §6) in the same commit.

**Staging-only ACs:** None

**Status at sprint open: ready**

#### ST-05 — Minimum capacity buffer floor recommendation for sprint planning

**Owner:** FinOps & Resource Architect
**Estimated effort:** 1.0 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Notes:** Requires FinOps & Resource Architect + PMO Lead sign-off per its own AC.

**Staging-only ACs:** None

**Status at sprint open: ready**

#### ST-06 — Technical debt registry (consolidated cross-cycle view)

**Owner:** Head of Engineering
**Estimated effort:** 2.5 (M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None

**Notes:** None

**Staging-only ACs:** None

**Status at sprint open: ready**

#### ST-07 — Skill-Silo mitigation: rotate execution-heavy story assignment pattern

**Owner:** Director of HR
**Estimated effort:** 2.0 (M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** Tied explicitly to the STEP 7.1 Skill-Silo alert as its trigger condition; document in `release_planning_prompt.md` or a referenced companion doc per its own AC.

**Staging-only ACs:** None

**Status at sprint open: ready**

#### ST-08 — Automated PII scan gate for new backend endpoints

**Owner:** AI Compliance & Governance Officer
**Estimated effort:** 2.5 (M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None

**Notes:** Must be confirmed to fire on a deliberately-introduced PII-shaped field in a test PR per its own AC — self-verifiable by the execution engine.

**Staging-only ACs:** None

**Status at sprint open: ready**

#### ST-09 — Governed write path for a non-empty, unversioned Now-horizon carry-forward

**Owner:** Head of Specs Team
**Estimated effort:** 1.0 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None

**Notes:** Two alternative remediation paths named in the item's own AC (§17 extension vs. STEP 8.1 amendment) — resolve the choice at execution kickoff (see `sprint_planning_notes.md §Risk Flags`, LP-14 check). If the §17 path is chosen, this branch touches `shared_standards.md` and must rebase onto `main` after EPIC-07 merges (see Merge Order above). Apply the standard governance file edit checklist (version bump, `OPERATIONAL_GUIDE.md` §14 update, `prompt_change_log.md` entry) regardless of which path is chosen.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-06 — Backend Hardening

**Maps to:** S2-17, S2-18
**Owner:** Backend Engineering Patterns Owner; Data Model & Domain Schema Owner
**Estimated effort:** 3.75 days (M+S)
**Risk IDs:** None
**Execution sequence:** 4

#### ST-17 — Standardise pagination pattern across list endpoints (consolidated)

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 2.5 (M)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** None

**Notes:** Not required to retrofit all existing endpoints in one pass, per its own AC — only the canonical pattern doc, shared helper, one reference migration, and the next 2 new/modified list endpoints.

**Staging-only ACs:** None

**Status at sprint open: ready**

#### ST-18 — `trade_plans.position_id` historical backfill design

**Owner:** Data Model & Domain Schema Owner
**Estimated effort:** 1.25 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-18`

**Dependencies:** None

**Notes:** Scoping document only — not an implementation of the backfill itself. Recorded as an explicit trade-off alongside `BLG-BE-52`'s original "no backfill" resolution per its own AC.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-04 — QA Process & Debt Closure

**Maps to:** S2-10, S2-11, S2-12, S2-13
**Owner:** Director of Quality; QA Lead; QA & Testing Owner
**Estimated effort:** 3.5 days (XS+S+S+S)
**Risk IDs:** None
**Execution sequence:** 5

#### ST-10 — Staging sign-off: custom price alert live delivery firing

**Owner:** Director of Quality
**Estimated effort:** 0.5 (XS)
**Delegation class:** delegated_qa

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Notes:** This backlog item (`BLG-QA-115`) is itself a staging-only verification task. The staging run must be dated in the ST-02 (EPIC-02, v7.5) DoQ sign-off block (`qa_evidence_EPIC-02.md`) per its own AC, and the backlog item closed/archived once recorded.

**Staging-only ACs:** AC-01/AC-02 (staging alert trigger + Telegram delivery confirmation) — `[staging-only evidence]`, no CI-reproducible equivalent. This story is the backlog filing itself, so no additional pre-PR backlog item is required per CLAUDE.md §2.

**Status at sprint open: ready**

#### ST-11 — Recurring pre-sprint-planning endpoint test coverage audit

**Owner:** QA & Testing Owner
**Estimated effort:** 1.0 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None

**Notes:** Run once against current state this sprint with results recorded (pass, or gaps filed) per its own AC.

**Staging-only ACs:** None

**Status at sprint open: ready**

#### ST-12 — Cross-EPIC deviation (DEV-*) consolidation review across cycles

**Owner:** Director of Quality
**Estimated effort:** 1.0 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None

**Notes:** First consolidation review performed this sprint per its own AC.

**Staging-only ACs:** None

**Status at sprint open: ready**

#### ST-13 — Post-parallelization Playwright shard balance audit

**Owner:** QA Lead
**Estimated effort:** 1.0 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None

**Notes:** REC-CI-01 follow-up.

**Staging-only ACs:** None

**Status at sprint open: ready**

---

### EPIC-02 — Operational Safety

**Maps to:** S2-02
**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.5 days (S)
**Risk IDs:** None
**Execution sequence:** 6

#### ST-02 — Recurring manual `pg_dump` backup schedule for production Supabase

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.5 (S)
**Delegation class:** delegated_backend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Notes:** Requires live production Supabase infrastructure access — not implementable by the execution engine alone. `database_backup_disaster_recovery_runbook.md` must be updated in the same commit per its own AC.

**Staging-only ACs:** None (the AC calls for a dry-run restore test against a non-production target, not a staging-only evidence gap — this is achievable and verifiable directly, not CI-unreproducible)

**Status at sprint open: ready**

---

### EPIC-05 — Spec Debt: SI-02 Definitional Clarity

**Maps to:** S2-14, S2-15, S2-16
**Owner:** Product Owner; Strategy Rules & System Intent Owner; Head of UX & Design
**Estimated effort:** 2.5 days (S+S+S)
**Risk IDs:** None
**Execution sequence:** 7

#### ST-14 — Revisit SI-02 Gate Status Condition 2/3 threshold definitions

**Owner:** Product Owner
**Estimated effort:** 0.5 (S)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** None

**Notes:** No HoST design-session artefact exists for this threshold decision (advisory, `sprint_planning_notes.md`). AC-02's conditional UI update (`SI02GateStatusSection`) reuses an already-approved display pattern (Design Pre-Approved, `design_gate.md`) — only required if the product review actually changes threshold values.

**Staging-only ACs:** None

**Status at sprint open: ready**

#### ST-15 — Explicit §13 continuity note for v6.9 on-demand recheck

**Owner:** Strategy Rules & System Intent Owner
**Estimated effort:** 1.0 (S)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None

**Notes:** None

**Staging-only ACs:** None

**Status at sprint open: ready**

#### ST-16 — Formally define SI-02 condition-3 "sufficient data" threshold

**Owner:** Strategy Rules & System Intent Owner
**Estimated effort:** 1.0 (S)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** None

**Notes:** No HoST design-session artefact exists for this threshold decision (advisory, `sprint_planning_notes.md`).

**Staging-only ACs:** None

**Status at sprint open: ready**

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~24-28 days |
| Total estimated effort (in-scope) | ~25.75 days |
| Utilisation | ~92-107% |
| Over-allocation | No |

## Items Deferred This Sprint

None — all 19 items in the authoritative backlog slice entered the sprint.

## Deferred Execution Blockers Accepted

*(omitted — `deferred_execution_blockers` was empty in `state.json`)*

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Install `pip-audit` in the execution environment | Infrastructure & Operations Owner | No |
| Log the `sprint_planning_prompt.md` v3.12→v3.13 transition in `prompt_change_log.md` (retroactive) | Head of Specs Team | No |
| Schedule a Product Owner + Strategy Rules & System Intent Owner decision session for ST-14/ST-16 before those items execute | Product Owner | No |
| Resolve ST-09's two-vehicle remediation choice at execution kickoff | Head of Specs Team | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — Product Owner, 2026-08-03
**Scope confirmed:** Confirmed — all 19 items across 7 EPICs accepted within capacity; no items deferred — Product Owner, 2026-08-03
**Capacity confirmed:** Confirmed — ~25.75 days against ~24-28 day band, `pass` outcome, no WARN acknowledgement required — Product Owner, 2026-08-03
**Deferred execution blockers accepted (if any):** N/A — none present
**Signed off by:** Product Owner
**Date:** 2026-08-03
