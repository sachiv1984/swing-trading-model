# Sprint Backlog — 2026-06-22__release-v6.1

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-06-22
**Cycle:** 2026-06-22__release-v6.1
**Release:** v6.1
**Sprint Goal:** Correct the governance engine deficiencies that allowed the design gate to be bypassed, and deliver the user-facing visualisation and analytics features — sector heat-map, gate proximity indicator, and Setup Quality Score — that make the trading system more transparent and actionable.
**Backlog Slice Source:** original `claude/cycles/2026-06-22__release-v6.1/stage4_backlog_slice.md`

---

## Sprint Scope

### Merge Order

**EPIC-03 → EPIC-01 → EPIC-02 → EPIC-04**

- EPIC-03 merges first (Sprint 1 close); establishes `openapi.yaml` and `backend/routers/test.py` baseline
- EPIC-01 merges second (Sprint 2 close, after ST-03 complete)
- EPIC-02 merges third (Sprint 2 close); CI-only changes
- EPIC-04 merges last (Sprint 2 close); must rebase on `main` after EPIC-03 merges to resolve `openapi.yaml` and `backend/routers/test.py` shared-file additions

**Execution_state.json owner:** EPIC-01 (first in execution order). All other EPIC branches must check for existence before creating their own.

**EPICs spanning both sprints:** EPIC-01 (ST-01/02 Sprint 1; ST-03 Sprint 2) and EPIC-04 (ST-08 Sprint 1; ST-09 Sprint 2). Branches remain open across sprints; PRs open after all stories in each EPIC complete.

---

## Sprint 1 — Governance Correctness + User Value

*Stories: ST-01, ST-02, ST-06, ST-07, ST-08 | G+D+P%: 40% (at Skill-Silo ceiling)*

---

### EPIC-01 — Governance Prompt Correctness (Sprint 1 stories)

**Maps to:** S2-01 (BLG-GOV-132), S2-02 (BLG-GOV-133)
**Owner:** Head of Specs Team; PMO Lead
**Risk IDs:** RISK-01
**Execution sequence:** 1st (Correctness Fast-Track)
**Branch:** `exec/2026-06-22__release-v6.1/EPIC-01`

#### ST-01 — Release planning: Design Gate Required flag

**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Sprint:** 1
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None

**Notes:** Prompt edit to `release_planning_prompt.md`. Governance edit checklist (CLAUDE.md §6) mandatory: bump version, update OPERATIONAL_GUIDE §14, update §6B source prompt header, append prompt_change_log.md row — all in same commit per RISK-01.

**Staging-only ACs:** None

---

#### ST-02 — Sprint planning: Design Gate hard gate at preflight

**Owner:** Head of Specs Team; PMO Lead
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Sprint:** 1
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None (can execute in parallel with ST-01)

**Notes:** Prompt edit to `sprint_planning_prompt.md`. Governance edit checklist (CLAUDE.md §6) mandatory in same commit per RISK-01. Note: this story patches the engine that is currently running — the patch benefits future invocations of `plan sprint`.

**Staging-only ACs:** None

---

### EPIC-03 — User Value Features (Sprint 1 stories)

**Maps to:** S2-04 (BLG-FE-76), S2-06 (BLG-FE-78)
**Owner:** Head of UX & Design; Frontend Specs & UX Documentation Owner
**Risk IDs:** RISK-03
**Execution sequence:** 3rd (after EPIC-01)
**Branch:** `exec/2026-06-22__release-v6.1/EPIC-03`

#### ST-06 — Portfolio sector heat-map visualization

**Owner:** Product Owner; Frontend Specs & UX Documentation Owner; Head of UX & Design
**Estimated effort:** M (~2–3 days)
**Delegation class:** autonomous *(reclassified from delegated_frontend — BLG-GOV-72 fast-path (c): locked spec `docs/design/2026-06-22__release-v6.1/sector-heatmap/ux_spec.md` v1.0; Playwright feasibility confirmed per AC-05; see sprint_planning_notes.md)*
**Sprint:** 1
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Spec reference:** `docs/design/2026-06-22__release-v6.1/sector-heatmap/ux_spec.md` v1.0 (locked; design gate cleared 2026-06-22)

**Dependencies:** Design gate (passed 2026-06-22 ✅)

**Notes:** New `SectorHeatMap.js` component. New backend endpoint required for sector weights — endpoint spec must be in api_contracts/ before implementation (RISK-03 mitigation; CLAUDE.md non-negotiable). AC-06 requires endpoint registered in `backend/routers/test.py` and `openapi.yaml` in same commit.

**Staging-only ACs:** None

---

#### ST-07 — Trade gate proximity indicator on dashboard

**Owner:** Head of Frontend Engineering; Head of UX & Design
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Sprint:** 1
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Spec reference:** `docs/design/2026-06-22__release-v6.1/gate-proximity-indicator/ux_spec.md` v1.0 (locked; design gate cleared 2026-06-22); `docs/specs/frontend/pages/dashboard.md` v2.2

**Dependencies:** GET /portfolio/gate-metrics (v5.5, BLG-BE-34, confirmed live ✅); Design gate cleared for Dashboard placement ✅

**Notes:** Display-only. Reads existing endpoint. No new backend changes. Error from gate-metrics must be hidden silently per design gate spec.

**Staging-only ACs:** None

---

### EPIC-04 — Setup Quality Score / PT-04 (Sprint 1 story)

**Maps to:** S2-08 (BLG-FEAT-25)
**Owner:** Head of Backend Engineering; Head of UX & Design; Metrics & Analytics Owner
**Risk IDs:** RISK-04
**Execution sequence:** 4th (Sprint 1: backend only; Sprint 2: frontend)
**Branch:** `exec/2026-06-22__release-v6.1/EPIC-04`

#### ST-08 — Setup Quality Score — backend engine (PT-04)

**Owner:** Head of Backend Engineering; Metrics & Analytics Owner
**Estimated effort:** S (~1–2 days)
**Delegation class:** autonomous
**Sprint:** 1
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None

**Notes:** Current closed trade count = 15 (2026-06-22); gate_not_met response (AC-03) is primary testable state at implementation time. Score path (AC-02) activates automatically when trades ≥20 (~2026-07-02). AC-05 endpoint registration in `backend/routers/test.py` and `openapi.yaml` mandatory in same commit (CLAUDE.md non-negotiable). ST-09 depends on this story — must complete before Sprint 2 ST-09.

**Staging-only ACs:** None (gate_not_met path fully CI-testable; score path testable with synthetic data or real trades — advisory, not a seal blocker)

---

## Sprint 2 — Governance Proposal + CI Quality + PT-04 Frontend

*Stories: ST-03, ST-04, ST-05, ST-09 | G+D+P%: 75% — above Skill-Silo ceiling (structural; see sprint_planning_notes.md)*

---

### EPIC-01 — Governance Prompt Correctness (Sprint 2 story)

**Maps to:** S2-05 (BLG-GOV-131)
*(continuing from Sprint 1 — same branch `exec/2026-06-22__release-v6.1/EPIC-01`)*

#### ST-03 — Governance overhead ceiling metric and accountability mechanism

**Owner:** PMO Lead; Head of Specs Team
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** autonomous
**Sprint:** 2
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None (no dependency on ST-01 or ST-02 beyond being in same EPIC branch)

**Notes:** Produces proposal document at `docs/product/decisions/gov_overhead_ceiling_proposal_v6.1.md`. Draft amendment to `roadmap_prompt.md` STEP 2 included in proposal doc. Actual prompt modification requires Head of Specs Team sign-off per CLAUDE.md §6 before any prompt file is modified — ST-03 does not itself modify prompts. Prior 5-cycle G+D+P% data required for AC-04.

**Staging-only ACs:** None

---

### EPIC-02 — CI Quality & Baseline Hygiene

**Maps to:** S2-03 (BLG-QA-60), S2-07 (BLG-OPS-73)
**Owner:** Director of Quality; Infrastructure & Operations Owner
**Risk IDs:** RISK-02
**Execution sequence:** 2nd (Sprint 2; no hard dependency on EPIC-01)
**Branch:** `exec/2026-06-22__release-v6.1/EPIC-02`

#### ST-04 — Register morning-briefing.spec.js and screener-quality.spec.js in playwright.yml

**Owner:** Director of Quality; Head of Engineering
**Estimated effort:** XS (<1 hour)
**Delegation class:** autonomous
**Sprint:** 2
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** None

**Notes:** CI file edit to `.github/workflows/playwright.yml`. AC-04 requires CI `Playwright E2E Acceptance Tests` job to pass — confirm via CI run after change. Full CI suite must pass; confirm pre-existing specs still execute (RISK-02 mitigation).

**Staging-only ACs:** None

---

#### ST-05 — Add PATCH /trades/{id}/costs to api_performance_baseline.md

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** XS (<1 hour)
**Delegation class:** autonomous
**Sprint:** 2
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** PATCH /trades/{trade_id}/costs live in production (v6.0 confirmed ✅)

**Notes:** Doc update to `docs/ops/api_performance_baseline.md`. Measurement from Render internal logs or live test per §19 methodology. Entry format must match existing baseline rows.

**Staging-only ACs:** AC-02 (measurement from Render internal logs or live endpoint — requires staging/production access; cannot be reproduced in CI)

---

### EPIC-04 — Setup Quality Score / PT-04 (Sprint 2 story)

*(continuing from Sprint 1 — same branch `exec/2026-06-22__release-v6.1/EPIC-04`)*
*(Must rebase on `main` after EPIC-03 merges — shared files: `openapi.yaml`, `backend/routers/test.py`)*

#### ST-09 — Setup Quality Score — frontend display (PT-04)

**Owner:** Head of UX & Design; Head of Frontend Engineering
**Estimated effort:** S (~1–2 days)
**Delegation class:** autonomous
**Sprint:** 2
**Status at sprint open: ready**

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Spec reference:** `docs/design/2026-05-21__release-v3.9/setup-quality-score-v2/ux_spec.md` (pre-approved); `pre_trade_research.md` v0.3 §5; `trade_plan.md` v0.7 §7a/7b

**Dependencies:** ST-08 (backend endpoint must exist — ✅ Sprint 1); design pre-approved from v3.9 design gate

**Notes:** At Sprint 2 start, ST-08 will have delivered the endpoint. AC-03 ("Insufficient trade history" message) is primary state at implementation time. Score badge (AC-02) activates when trades ≥20. AC-06 Playwright coverage must include both score-renders and gate-not-met states.

**Staging-only ACs:** None (gate_not_met path CI-testable; score badge testable with synthetic data)

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~20–45 hrs (2-sprint window) |
| Total estimated effort (Sprint 1) | ~5–7 hrs |
| Total estimated effort (Sprint 2) | ~3–5 hrs |
| Total estimated effort (all) | ~17–29 hrs |
| Over-allocation | No — within 2-sprint window; WARN acknowledged by PO 2026-06-22 |

---

## Items Deferred This Sprint

None — all 9 stories included as firm scope.

---

## Deferred Execution Blockers Accepted

No deferred execution blockers present in `state.json`.

---

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Install pip-audit before Sprint 1 execution | Head of Engineering | No |
| BLG-GOV-134 / BLG-QA-62 disposition (v6.2 or unscheduled) | Product Owner | No |
| EPIC-04 score path validation: confirm trades ≥20 reached or accept staging-only for score path | PMO Lead; Director of Quality | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed
**Scope confirmed:** Confirmed — 9 stories (EPIC-01 ST-01/02/03, EPIC-02 ST-04/05, EPIC-03 ST-06/07, EPIC-04 ST-08/09); 2-sprint phasing
**Capacity confirmed:** Confirmed — WARN acknowledged; 2-sprint window (~20–45 hrs available)
**Deferred execution blockers accepted:** N/A
**Signed off by:** Product Owner
**Date:** 2026-06-22
