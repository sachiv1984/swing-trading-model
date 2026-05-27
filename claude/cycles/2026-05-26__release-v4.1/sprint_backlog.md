**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-05-27
**Cycle:** 2026-05-26__release-v4.1
**Release:** v4.1
**Sprint Goal:** Resolve 2nd-recurrence governance failures in execution, planning, and verification prompts; clear API contract spec debt for four undocumented v4.0 endpoints; and deliver Arc 5 P&L integration, Gemini cost alerting, and SI-02 pre-planning artefacts to unlock position drift monitoring sprint planning.
**Backlog Slice Source:** claude/cycles/2026-05-26__release-v4.1/stage4_backlog_slice.md (original)

---

# Sprint Backlog — 2026-05-26__release-v4.1

---

## Merge Order

**Sprint 1:** EPIC-01 → EPIC-02

**Sprint 2:** EPIC-04 → EPIC-03

**Overall sequence:** EPIC-01 → EPIC-02 → EPIC-04 → EPIC-03

**execution_state.json owner:** EPIC-01 creates `execution_state.json`; all subsequent EPICs (EPIC-02, EPIC-04, EPIC-03) must check for existence before creating their own version — if found, append. Do not overwrite.

**Shared file advisory:**
- `docs/reference/openapi.yaml`: EPIC-02 owns; EPIC-03 must rebase onto `origin/main` after EPIC-02 merges
- `claude/system/delivery_verification_prompt.md`: EPIC-01 owns; EPIC-04 must rebase after EPIC-01 merges
- `claude/system/OPERATIONAL_GUIDE.md`: EPIC-01 owns; EPIC-04 must rebase after EPIC-01 merges
- `claude/system/prompt_change_log.md`: EPIC-01 owns; EPIC-04 must rebase after EPIC-01 merges and append, not conflict

---

## Sprint Scope

---

### EPIC-01 — Governance Prompt Hardening

**Maps to:** S2-01
**Owner:** Head of Specs Team
**Estimated effort:** ~3 days
**Risk IDs:** RISK-01 (2nd recurrence escalation — must not slip)
**Execution sequence:** 1 (Sprint 1, first)
**Branch:** `exec/2026-05-26__release-v4.1/EPIC-01`

---

#### ST-01 — execution_prompt.md: Add merge-gate re-invocation as hard gate (OA-01)

**Owner:** Head of Specs Team
**Estimated effort:** S (~1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None

**Notes:** 2nd-recurrence escalation (v3.9 + v4.0). Must be actioned in v4.1 — if missed again, CLAUDE.md §2 mandate required. OA-03 investigation (sprint_close_reminder.yml) is AC-04 of this story.

**Staging-only ACs:** None

---

#### ST-02 — sprint_planning_prompt.md + sprint_backlog.md template: Staging-only AC designation at planning (OA-02)

**Owner:** Head of Specs Team
**Estimated effort:** S (~1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Notes:** 2nd-recurrence escalation (v3.9 + v4.0). Must be actioned in v4.1 — if missed again, CLAUDE.md §2 mandated rule required.

**Staging-only ACs:** None

---

#### ST-03 — delivery_verification_prompt.md: STEP 5.0A pr_number null guard (OA-04)

**Owner:** Head of Specs Team
**Estimated effort:** S (~1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Notes:** First occurrence; straightforward null guard implementation. EPIC-04 ST-14 also modifies delivery_verification_prompt.md — EPIC-04 must rebase after EPIC-01 merges.

**Staging-only ACs:** None

---

### EPIC-02 — API Contract Spec Debt Batch 1

**Maps to:** S2-02
**Owner:** API Contracts Documentation Owner
**Estimated effort:** ~3 days
**Risk IDs:** RISK-02 (overdue by 1 cycle; BLG-SPEC-33 blocks ST-07)
**Execution sequence:** 2 (Sprint 1, concurrent with EPIC-01)
**Branch:** `exec/2026-05-26__release-v4.1/EPIC-02`

---

#### ST-04 — SI-03 Red Flag Journal API contract document (BLG-SPEC-33)

**Owner:** API Contracts Documentation Owner
**Estimated effort:** S (~1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None (but ST-07 in EPIC-03 gates on this — satisfies gate for Sprint 2)

**Notes:** Contract for `GET /portfolio/red-flag-journal`. Endpoint heading must be `##` level per CLAUDE.md §2 OpenAPI drift gate.

**Staging-only ACs:** None

---

#### ST-05 — SI-01 Pre-Entry Validation API contract document (BLG-SPEC-34)

**Owner:** API Contracts Documentation Owner
**Estimated effort:** S (~1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Notes:** Contract for `GET /portfolio/pre-entry-validation`. Endpoint heading must be `##` level.

**Staging-only ACs:** None

---

#### ST-06 — Arc 5 analytics endpoint API contract (BLG-SPEC-40)

**Owner:** API Contracts Documentation Owner
**Estimated effort:** S (~1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None

**Notes:** Contract for `GET /analytics/arc5-compliance`. Advisory dependency: ST-08 P&L integration benefits from this contract for field verification.

**Staging-only ACs:** None

---

### EPIC-03 — Feature Integration + Quality

**Maps to:** S2-03, S2-04, S2-05, S2-06, S2-07
**Owner:** Head of Engineering; QA Lead
**Estimated effort:** ~10 days
**Risk IDs:** RISK-03 (Sprint 2 capacity-tight; staging bundle + M-effort items combined)
**Execution sequence:** 4 (Sprint 2, second — after EPIC-04 initiates)
**Branch:** `exec/2026-05-26__release-v4.1/EPIC-03`

---

#### ST-07 — Gemini thesis endpoint API contract (BLG-SPEC-38)

**Owner:** API Contracts Documentation Owner; Head of Specs Team
**Estimated effort:** S (~1 day)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** ST-04 (BLG-SPEC-33) must be closed — gate condition per AC-01. Satisfied by sprint ordering (ST-04 Sprint 1, ST-07 Sprint 2).

**Notes:** Contract for `POST /trade-plans/{plan_id}/generate-thesis`. Verify ST-04 closed (BLG-SPEC-33 merged to main) before commencing. Must rebase `openapi.yaml` after EPIC-02 merges.

**Staging-only ACs:** None

---

#### ST-08 — Arc 5 compliance metrics P&L integration (BLG-FEAT-40 + BLG-FEAT-42)

**Owner:** Metrics Definitions & Analytics Owner; Financial Reporting & Records Owner
**Estimated effort:** M (~3 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** ST-06 advisory (arc5-compliance contract for field verification — not a hard gate)

**Notes:** Two bundled items: FEAT-40 (composite score formula in metrics_definitions.md) + FEAT-42 (P&L report compliance section). AC-02 and AC-06 require Owner review — engine produces draft for review sign-off.

**Staging-only ACs:** None

---

#### ST-09 — Gemini API daily cost threshold alert via Telegram (BLG-OPS-34)

**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Estimated effort:** M (~2–3 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None

**Notes:** Backend implementation with configurable env var threshold. AC-04 unit test coverage verifiable in CI. AC-05 staging verification is [staging-only evidence] — human QA Lead must perform staging check; if deferred post-merge, file BLG-QA-xx before PR opens.

**Staging-only ACs:** AC-05 (threshold alert fires on staging with test data) `[staging-only evidence]`

---

#### ST-10 — Frontend: Research view signal_type + Arc5ComplianceSection spec (BLG-FE-44 + BLG-FE-48)

**Owner:** Head of Engineering; Frontend Specs & UX Documentation Owner
**Estimated effort:** S (~1.5 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** ST-06 advisory (arc5-compliance contract for FE-48 spec field mapping)

**Notes:** Two bundled items: FE-44 (signal_type column in Research view — frontend code change) + FE-48 (Arc5ComplianceSection spec document). AC-02 requires Playwright test coverage for the signal_type column (AC-02 condition: "human staging sign-off or Playwright test coverage" — Playwright path selected, no staging-only evidence needed). Per CLAUDE.md §2, Playwright test must be included in the same commit as the frontend change.

**Staging-only ACs:** None (AC-02 resolved via Playwright test coverage)

---

#### ST-11 — Staging Verification Bundle (BLG-QA-28, BLG-QA-29, BLG-QA-30, BLG-OPS-28)

**Owner:** QA Lead; Infrastructure & Operations Owner
**Estimated effort:** S (~2 days)
**Delegation class:** delegated_qa

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** ST-07/08/09/10 should complete first (verifies their staging behaviour)

**Notes:** Closes four deferred v4.0 staging ACs. AC-01 (QA-28 Playwright) is engine-implementable; ACs 02-04 require human staging verification. This story IS the backlog item for BLG-QA-28/29/30 and BLG-OPS-28 — no additional items required. Lowest-risk Sprint 2 deferral to v4.2 if capacity is constrained. Discretionary deferral authorised by PO (see sprint_planning_notes.md).

**Staging-only ACs:** AC-02 (Gemini thesis staging with GEMINI_API_KEY) `[staging-only evidence]`, AC-03 (Yahoo Finance live rejection) `[staging-only evidence]`, AC-04 (Render deploy hook verification) `[staging-only evidence]`

---

### EPIC-04 — SI-02 Pre-Planning + Security + Ops

**Maps to:** S2-08, S2-09, S2-10, S2-11
**Owner:** Strategy Rules & System Intent Owner; Infrastructure & Operations Owner
**Estimated effort:** ~6.5 days
**Risk IDs:** RISK-04 (documentation/review only — low risk)
**Execution sequence:** 3 (Sprint 2, first — can run in parallel with EPIC-03 implementation)
**Branch:** `exec/2026-05-26__release-v4.1/EPIC-04`

---

#### ST-12 — SI-02 data model gap analysis (BLG-SPEC-39)

**Owner:** Data Model & Domain Schema Owner; Head of Specs Team
**Estimated effort:** M (~2 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None

**Notes:** Engine reads current schema files and produces gap analysis document. AC-03 requires review by 3 owners before SI-02 sprint planning.

**Staging-only ACs:** None

---

#### ST-13 — SI-02 pre-planning: §13 criteria + data audit + query performance (BLG-GOV-44 + BLG-GOV-46 + BLG-GOV-51)

**Owner:** Strategy Rules & System Intent Owner; Challenger; Head of Engineering
**Estimated effort:** S (~1.5 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None

**Notes:** Three SI-02 pre-planning documents. AC-02 review by Strategy Rules owner; AC-04 review by Challenger + PO; AC-06 review by Head of Engineering + Head of Backend Engineering.

**Staging-only ACs:** None

---

#### ST-14 — Security review + governance patches (BLG-GOV-49 + BLG-GOV-54 + BLG-GOV-56)

**Owner:** Cybersecurity & Trust Lead; Product Owner; Head of Specs Team
**Estimated effort:** S (~1.5 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** EPIC-01 must merge first — both ST-03 (EPIC-01) and ST-14 GOV-56 modify `delivery_verification_prompt.md`. EPIC-04 branch must rebase onto `origin/main` after EPIC-01 merges before finalising delivery_verification_prompt.md changes.

**Notes:** Three governance items: GOV-49 (Gemini API key scope review), GOV-54 (SI-05 Phase 1 roadmap annotation), GOV-56 (delivery_verification_prompt.md STEP 12.1 artefact presence check). OPERATIONAL_GUIDE.md and prompt_change_log.md updates required per CLAUDE.md §6 for GOV-56.

**Staging-only ACs:** None

---

#### ST-15 — Operational reviews: API performance baseline + Gemini usage + P&L attribution (BLG-OPS-29 + BLG-OPS-30 + BLG-OPS-32)

**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect; Financial Reporting & Records Owner
**Estimated effort:** S (~1.5 days)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** ST-07 advisory (Gemini thesis endpoint in performance baseline — ST-07 contract available from Sprint 2 sequencing)

**Notes:** Three operational reviews. OPS-29 updates api_performance_baseline.md (closes OA-07/BLG-OPS-29 from v4.0). OPS-30 is the first monthly Gemini usage review. OPS-32 checks P&L trade attribution before Arc 5 compliance integration.

**Staging-only ACs:** None

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity (2 sprints) | ~16–20 days |
| Total estimated effort (in-scope) | ~23 days |
| Utilisation | ~115–145% |
| Over-allocation | Yes — accepted by PO with EPIC-04 parallelisation note and discretionary deferral of ST-09/ST-11 if needed |

---

## Items Deferred This Sprint

No items deferred. All 15 stories from `stage4_backlog_slice.md` are included in scope.

---

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| OA-05: Rejected-but-strong register gaps (3 ideas) | PMO Lead | No |
| OA-06: Ambiguous ideas register rows (2 rows) | PMO Lead | No |
| ST-09 AC-05 staging: if deferred post-merge, file BLG-QA-xx before PR opens | QA Lead | No (conditional) |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed — 2026-05-27
**Scope confirmed:** Confirmed — all 15 stories, 4 EPICs, 2 sprints — 2026-05-27
**Capacity confirmed:** Confirmed — WARN acknowledged; over-allocation accepted with EPIC-04 parallelisation note; discretionary deferral of ST-09/ST-11 to v4.2 authorised if Sprint 2 capacity constrained — 2026-05-27
**Deferred execution blockers accepted:** N/A (none)
**PT-04 written rationale:** PT-04 gate not met (< 20 closed trades). Insufficient trade history for meaningful performance analytics. Parked until gate confirmed met. Recorded 2026-05-27.
**Signed off by:** Product Owner
**Date:** 2026-05-27
