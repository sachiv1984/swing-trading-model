**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-07-02
**Cycle:** 2026-07-02__release-v6.4
**Release:** v6.4
**Sprint Goal:** Deliver v6.4's mandatory production correctness fix, AI prompt-injection security hardening, full AUD-2026-07-01 lifecycle-audit remediation, and the Strategy Benchmark Open Positions panel (with accessibility contrast and Playwright coverage fixes) in a single sealed sprint.
**Backlog Slice Source:** original `claude/cycles/2026-07-02__release-v6.4/stage4_backlog_slice.md`

# Sprint Backlog — 2026-07-02__release-v6.4

## Merge Order

- **EPIC merge sequence:** EPIC-01 → EPIC-02 → EPIC-03
- **`execution_state.json` owner:** EPIC-01 (first in execution order). EPIC-02 and EPIC-03 must check for its existence before creating their own and append rather than overwrite.
- **Shared files across EPICs:** None identified this sprint (see `sprint_planning_notes.md` Multi-EPIC Execution Notes for the full file-ownership breakdown by EPIC). No cross-EPIC rebase-before-merge requirement beyond the standard sequence above.

## Sprint Scope

### EPIC-01 — Backend Correctness & Security Hardening

**Maps to:** S2-01, S2-02, S2-03
**Owner:** Backend Engineering Patterns Owner; Cybersecurity & Trust Lead
**Estimated effort:** 0.90 days (ST-01 0.15 + ST-02 0.25 + ST-03 0.5)
**Risk IDs:** RISK-01, RISK-02
**Execution sequence:** 1

#### ST-01 — Signal generation reads deprecated `tickers` table instead of `ticker_universe` (BLG-BE-40)

**Owner:** Backend Engineering Patterns Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None

**Status at sprint open: ready**

**Notes:** P1 mandatory STEP 8.0 fast-track item (rebalance 2026-07-01__scheduled). RISK-01 (ticker source divergence) applies — verify parity via Ticker Universe Management before merge.

**Staging-only ACs:** AC-02 (live signal generation output change verified against a real Ticker Universe Management action — not CI-reproducible as a pure unit test; see `sprint_planning_notes.md` Staging-Only AC Assessment).

---

#### ST-02 — Sanitise `context_opts.ticker` before system prompt injection (BLG-SEC-01)

**Owner:** Cybersecurity & Trust Lead; Backend Engineering Patterns Owner
**Estimated effort:** 0.25
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Status at sprint open: ready**

**Notes:** RISK-02 (validation regex could reject legitimate international formats) — test against full current `ticker_universe` active list before deploy.

**Staging-only ACs:** None — AC-01/02/03 are unit-testable; AC-04 is a Cybersecurity & Trust Lead sign-off, not a live-environment evidence requirement.

---

#### ST-03 — Validate ticker/market strings at signal write time (BLG-SEC-02)

**Owner:** Cybersecurity & Trust Lead; Backend Engineering Patterns Owner
**Estimated effort:** 0.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Status at sprint open: ready**

**Notes:** RISK-02 applies here too (shared validation regex risk with ST-02). AC-02 (review existing signals for anomalous values) is a one-time manual data-cleanup task, not CI-testable and not staging — track as a manual execution step.

**Staging-only ACs:** None.

---

### EPIC-02 — Governance & Audit Remediation

**Maps to:** S2-04, S2-05, S2-06, S2-07
**Owner:** Head of Specs Team
**Estimated effort:** 3.25 days (ST-04 0.5 + ST-05 0.5 + ST-06 1.75 + ST-07 0.5)
**Risk IDs:** RISK-03, RISK-04
**Execution sequence:** 2

#### ST-04 — Fix governance version-sync drift (BLG-GOV-150)

**Owner:** Head of Specs Team
**Estimated effort:** 0.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Status at sprint open: ready**

**Notes:** RISK-04 applies (4 governance-file-editing stories in this EPIC) — run `/governance-drift` before this commit.

**Staging-only ACs:** None — all text/version verification, CI/manual-review testable.

---

#### ST-05 — Document hygiene cleanup (BLG-GOV-151)

**Owner:** Head of Specs Team
**Estimated effort:** 0.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None

**Status at sprint open: ready**

**Notes:** RISK-04 applies. AC-04 touches this very file's own header — apply last, after this sprint backlog is sealed, to avoid mutating an in-flight governed artefact.

**Staging-only ACs:** None.

---

#### ST-06 — Close structural reliability gaps (BLG-GOV-152 + FI-P3-01/FI-P3-02/FI-P4-01 re-target)

**Owner:** Head of Specs Team
**Estimated effort:** 1.75
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None (sequence before ST-07 within this EPIC — both touch `shared_standards.md`, different sections; see `sprint_planning_notes.md`)

**Status at sprint open: ready**

**Notes:** RISK-03 (FI-P3-01 folded in without a dedicated backlog ID) and RISK-04 apply. DF-10 carry-forward (2-cycle escalation risk) is resolved by AC-02 in this story. Run `/governance-drift` before commit.

**Staging-only ACs:** None — all governance-prompt text changes, verifiable by review/grep.

---

#### ST-07 — Audit & governance process fixes (BLG-GOV-153)

**Owner:** Head of Specs Team
**Estimated effort:** 0.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** ST-06 (sequence after — same-file section, `shared_standards.md`)

**Status at sprint open: ready**

**Notes:** RISK-04 applies. Run `/governance-drift` before commit.

**Staging-only ACs:** None.

---

### EPIC-03 — Strategy Benchmark Enhancement & UX/QA Polish

**Maps to:** S2-08, S2-09, S2-10, S2-11, S2-12, S2-13
**Owner:** Head of UX & Design; Backend Engineering Patterns Owner; QA & Testing Owner
**Estimated effort:** 3.65 days (ST-08 1.5 + ST-09 0.25 + ST-10 0.25 + ST-11 0.15 + ST-12 0.5 + ST-13 1.0)
**Risk IDs:** RISK-05, RISK-06 (closed — see below)
**Execution sequence:** 3

**Design Gate:** Passed 2026-07-02 (`design_gate.md`) — all 13 items cleared, 0 blocked. ST-08/09/10 were the 3 UI-facing items requiring clearance (RISK-06); all confirmed.

#### ST-08 — Add Open Positions panel to Strategy Benchmark page (BLG-FEAT-54)

**Owner:** Head of UX & Design; Backend Engineering Patterns Owner
**Estimated effort:** 1.5
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None (merges first within EPIC-03 — see `sprint_planning_notes.md` Dependency Map re: ST-13)

**Status at sprint open: ready**

**Notes:** Design artefact: `docs/design/2026-07-02__release-v6.4/open-positions-panel/ux_spec.md` v1.0. New `GET /strategy/benchmark/open-positions` endpoint — RISK-05 applies: sequence backend endpoint → `openapi.yaml`/contract doc → `backend/routers/test.py` registration → frontend panel work, within this story, using `/commit-check` before each commit. 4 ACs — below the ≥5 threshold that mandates a Playwright scenario stub per DF-06, but one is recommended given RISK-05/RISK-06 profile (advisory, not required).

**Staging-only ACs:** AC-01 (Panel 0 rendering — no Playwright test scoped for Panel 0 this sprint; ST-13 covers Panels 1/3 only). If staging sign-off is deferred to post-merge for AC-01, a backlog item must be filed via `/backlog-add` before the PR opens (CLAUDE.md §2).

---

#### ST-09 — Improve AI daily briefing disclaimer text contrast (BLG-UX-01)

**Owner:** Head of UX & Design; AI Compliance & Governance Officer
**Estimated effort:** 0.25
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None

**Status at sprint open: ready**

**Notes:** Design artefact: `docs/specs/qa/ai_disclaimer_visibility_assessment.md` v1.0 (pre-existing, confirmed current at design gate).

**Staging-only ACs:** AC-01 (contrast ratio), AC-02 (no visual regression) — visual/rendering checks; precedent (v6.3 BLG-GOV-147) used human visual QA sign-off. If deferred to post-merge staging, a backlog item must be filed before the PR opens (CLAUDE.md §2).

---

#### ST-10 — Improve AI chat widget footer disclaimer contrast and add test coverage (BLG-UX-02)

**Owner:** Head of UX & Design; AI Compliance & Governance Officer
**Estimated effort:** 0.25
**Delegation class:** delegated_frontend

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Status at sprint open: ready**

**Notes:** Design artefact: `docs/specs/qa/ai_disclaimer_visibility_assessment.md` v1.0 (shared with ST-09). AC-03's Playwright test (visibility + "advisory" keyword) satisfies the CLAUDE.md Playwright-coverage hard gate for AC-02/AC-03; AC-01 (contrast) remains unverified by that test.

**Staging-only ACs:** AC-01 (contrast ratio — not covered by AC-03's Playwright test, which checks visibility/text content, not computed contrast). If deferred to post-merge staging, a backlog item must be filed before the PR opens (CLAUDE.md §2).

---

#### ST-11 — Add v6.3 endpoints to `api_performance_baseline.md` (BLG-OPS-82)

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** 0.15
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None

**Status at sprint open: ready**

**Notes:** None.

**Staging-only ACs:** AC-01 (5 warm requests measured against a live API to produce p50/p95 — inherently a staging/production measurement, not CI-reproducible).

---

#### ST-12 — Playwright coverage for ST-01 observable UI ACs, AI journal summary error states (TEST-GAP-EPIC-01)

**Owner:** QA & Testing Owner
**Estimated effort:** 0.5
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None

**Status at sprint open: ready**

**Notes:** Closes TSG-v63-01 (v6.3 delivery verification test gap).

**Staging-only ACs:** None — these ACs are the Playwright tests themselves, CI-executable.

---

#### ST-13 — Playwright scenario coverage for Strategy Benchmark page (TEST-GAP-EPIC-03)

**Owner:** QA & Testing Owner
**Estimated effort:** 1.0
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** ST-08 (merge after — see `sprint_planning_notes.md` Dependency Map; Panel 0 addition should land before these tests are authored/finalised to avoid DOM/selector rework)

**Status at sprint open: ready**

**Notes:** Closes TSG-v63-02 (v6.3 delivery verification test gap).

**Staging-only ACs:** None — these ACs are the Playwright tests themselves, CI-executable.

---

## Sign-Off

**Sprint Goal confirmed:** Yes — see `sprint_goal.md`.

**Capacity check:** PASS — 7.8 days estimated vs ~12–14 day baseline. No `warn`, no over-allocation, no Product Owner acceptance-of-risk required.

**All `[AC REQUIRED]` placeholders resolved:** Yes — none existed; all 13 items sourced ACs directly from `stage4_backlog_slice.md` (defined at release planning).

**All `[ESTIMATE REQUIRED]` placeholders resolved:** Yes — none existed; all 13 items carry effort estimates from `release_plan.md ## Capacity Check`.

**Outstanding actions marked `Blocker? Yes`:** None (see `sprint_planning_notes.md` Outstanding Actions — all resolved or advisory-only).

**Deferred execution blockers:** None (`state.json deferred_execution_blockers = []`).

**Staging-only AC check (OA-02, 2nd recurrence):** Complete — every story's `**Staging-only ACs:**` field above reflects the assessment in `sprint_planning_notes.md`.

**Design Gate:** Passed 2026-07-02 (`design_gate.md`) — required precondition for ST-08/09/10 satisfied.

Product Owner: Confirmed — sprint scope (all 13 items), sprint goal, and capacity outcome accepted as planned. Date: 2026-07-02
Head of Specs Team: Confirmed — acceptance criteria for all 13 items reviewed as testable, observable, and sufficiently specific. Date: 2026-07-02
Director of Quality: Confirmed — QA criteria across all 3 EPICs are sufficient to produce `qa_evidence_EPIC-xx.md` at sprint close; no coverage gaps identified beyond those already flagged as staging-only. Date: 2026-07-02
FinOps & Resource Architect: Confirmed — capacity outcome PASS, no workforce constraint. Date: 2026-07-02
PMO Lead: Confirmed — dependency map, execution sequence, and multi-EPIC merge order recorded in `sprint_planning_notes.md`. Date: 2026-07-02
