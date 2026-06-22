# Sprint Planning Notes — 2026-06-22__release-v6.1

**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-06-22
**Cycle:** 2026-06-22__release-v6.1

---

## Backlog Slice Source

Original — `claude/cycles/2026-06-22__release-v6.1/stage4_backlog_slice.md`

No amendment sealed. `amended_backlog_slice_path` is empty in `.claude_current_state.json`.

---

## Carry-Forward Items

Carry-forward reviewed from `claude/cycles/2026-06-19__release-v6.0/lessons_learnt_closure.md`. 3 items from prior cycle.

| # | Item | Status |
|---|------|--------|
| CF-1 | PT-04 gate re-check (≥20 closed trades) | Resolved at planning — PO confirmed firm inclusion with graceful degradation (see EPIC-04 scope decision below) |
| CF-2 | `execution_prompt.md` STEP 5.3A write+verify patch | ✅ Resolved — v3.46→v3.47 applied 2026-06-22 (AUD-2026-06-22-001, prompt_change_log.md confirmed) |
| CF-3 | BLG-QA-60 no-further-deferral | ✅ Resolved — included as firm scope ST-04 in EPIC-02 |

---

## Capacity WARN Acknowledgement

**Capacity check outcome:** WARN (phasing required)
**Firm effort:** ~17 hrs (EPIC-01, EPIC-02, EPIC-03 firm stories)
**Total with EPIC-04:** ~29 hrs
**Available window:** ~20–45 hrs across 2-sprint window (~12–14 days/sprint × 2)

**Product Owner acknowledgement:** Confirmed 2026-06-22. Two-sprint phasing accepted. `capacity_warn_acknowledged = true`.

---

## EPIC-04 Scope Decision

**Context:** EPIC-04 (ST-08, ST-09) was classified conditional at release planning (gate: ≥20 closed trades; last known count 13 at 2026-06-16).

**PMO Lead gate re-check at sprint planning (2026-06-22):** Current count = 15 trades. Gate not met (< 20).

**Product Owner decision:** Include EPIC-04 as firm scope. Rationale: the stories themselves handle the gate_not_met case gracefully — ST-08 AC-03 returns `{"gate_not_met": true, "min_trades_required": 20}` and ST-09 AC-03 displays "Insufficient trade history (<20 trades)". These are fully testable states in CI. The score path activates automatically when trades ≥20 (~2026-07-02). Deferral would be the 9th consecutive cycle for PT-04; PO elected to ship with built-in degradation.

**Score path testing:** Gate_not_met path testable in CI immediately. Score path (score > 0) verifiable only with ≥20 closed trades or synthetic staging data. QA to sign off gate_not_met path at sprint close; score path validation documented as staging-only advisory (no backlog item required — AC-03 explicitly covers this as a designed state, not a gap).

---

## ST-06 Delegation Class Reclassification

**Original class in backlog slice:** `delegated_frontend`
**Reclassified to:** `autonomous`
**Basis:** BLG-GOV-72 fast-path (c) — new component implemented against a locked frontend spec where Playwright feasibility is confirmed.
- Locked spec: `docs/design/2026-06-22__release-v6.1/sector-heatmap/ux_spec.md` v1.0 (design gate cleared 2026-06-22, Head of UX & Design + Product Owner)
- Playwright feasibility: confirmed per ST-06 AC-05 (coverage scenario specified in AC)
- Original `delegated_frontend` classification was written before design gate passed; BLG-GOV-72 (c) now applies.

---

## Deferred Items

No items deferred at planning. All 9 stories included as firm scope.

| Item | Reason | Next Sprint Candidate? |
|------|--------|----------------------|
| — | — | — |

---

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-09 | ST-08 | Internal (backend endpoint must exist before frontend integration) | Resolved — ST-08 in Sprint 1, ST-09 in Sprint 2 |
| ST-06 | Design gate | External prerequisite | ✅ Resolved — design gate passed 2026-06-22 |
| ST-07 | GET /portfolio/gate-metrics (v5.5, BLG-BE-34) | External API | ✅ Resolved — endpoint live since v5.5 |
| ST-05 | PATCH /trades/{trade_id}/costs live in production | External API | ✅ Resolved — endpoint confirmed v6.0 |
| ST-08 | ≥20 closed trades for score path | Runtime gate | Advisory only — gate_not_met path testable in CI; no execution blocker |

No circular dependencies detected.

---

## Execution Sequence

### Sprint 1 — Governance Correctness + User Value (5 stories)

Order within sprint (parallel where noted):

1. **ST-01** (EPIC-01) — Release planning: Design Gate Required flag *(autonomous; prompt edit)*
2. **ST-02** (EPIC-01) — Sprint planning: Design Gate hard gate at preflight *(autonomous; prompt edit; parallel with ST-01)*
3. **ST-06** (EPIC-03) — Portfolio sector heat-map visualization *(autonomous; M effort; new component against locked spec)*
4. **ST-07** (EPIC-03) — Trade gate proximity indicator on dashboard *(autonomous; S effort; reads existing endpoint; parallel with ST-06 after design review)*
5. **ST-08** (EPIC-04) — Setup Quality Score backend engine *(autonomous; S effort; must complete before ST-09)*

### Sprint 2 — Governance Proposal + CI + PT-04 Frontend (4 stories)

Order within sprint (parallel where noted):

1. **ST-03** (EPIC-01) — Governance overhead ceiling metric proposal *(autonomous; proposal doc + draft amendment)*
2. **ST-04** (EPIC-02) — Register spec files in playwright.yml *(autonomous; XS; CI file edit; parallel with ST-03)*
3. **ST-05** (EPIC-02) — API performance baseline update *(autonomous; XS; doc update; parallel with ST-03/04)*
4. **ST-09** (EPIC-04) — Setup Quality Score frontend display *(autonomous; S effort; depends ST-08 from Sprint 1)*

---

## Multi-EPIC Execution Notes

**Execution_state.json owner:** EPIC-01 (first EPIC in execution order). The EPIC-01 branch creates `execution_state.json`. All other EPIC branches must check for existence before creating their own — if found, read it and append their EPIC's section rather than overwrite.

**EPICs spanning both sprints:**
- EPIC-01 branch: ST-01 + ST-02 in Sprint 1; ST-03 in Sprint 2. Branch remains open across both sprints. PR opened after all 3 stories complete (Sprint 2).
- EPIC-04 branch: ST-08 in Sprint 1; ST-09 in Sprint 2. Branch remains open across both sprints. PR opened after ST-09 completes (Sprint 2).

**EPICs in single sprint:**
- EPIC-02 branch: ST-04 + ST-05 in Sprint 2 only.
- EPIC-03 branch: ST-06 + ST-07 in Sprint 1 only.

**Recommended merge order:** EPIC-03 → EPIC-01 → EPIC-02 → EPIC-04
- EPIC-03 (Sprint 1 close): no shared-file conflicts; merge first
- EPIC-01 (Sprint 2 close): merges after EPIC-03; no shared files
- EPIC-02 (Sprint 2 close): after EPIC-01; CI-only changes, no shared files
- EPIC-04 (Sprint 2 close): merges last; shares `openapi.yaml` and `backend/routers/test.py` with EPIC-03 — must rebase on `main` after EPIC-03 merges before finalising

**Shared files across EPICs:**

| File | EPICs | Owner | Advisory |
|------|-------|-------|---------|
| `docs/reference/openapi.yaml` | EPIC-03 (ST-06 new endpoint), EPIC-04 (ST-08 new endpoint) | EPIC-03 (first to merge) | EPIC-04 must rebase on `main` after EPIC-03 merges; take union of all path additions |
| `backend/routers/test.py` | EPIC-03 (ST-06 AC-06), EPIC-04 (ST-08 AC-05) | EPIC-03 (first to merge) | EPIC-04 must rebase on `main` after EPIC-03 merges; take union of test registrations |
| `src/pages/SystemStatus.js` | EPIC-03 (ST-06 adds endpoint → count +1), EPIC-04 (ST-08 adds endpoint → count +1) | EPIC-03 (first to merge) | EPIC-04 must rebase; update fallback count to reflect cumulative total after both EPICs |

---

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 (ST-01, ST-02, ST-03) | Valid — governance edit checklist (CLAUDE.md §6) must run for each prompt file modified; all 4 steps in same commit |
| RISK-02 | EPIC-02 (ST-04) | Valid — full CI suite must pass after playwright.yml change; confirm pre-existing specs still execute |
| RISK-03 | EPIC-03 (ST-06) | Valid — design gate passed; locked spec available; mitigated. New backend endpoint for sector weights must be specced in api_contracts/ before implementation |
| RISK-04 | EPIC-04 (ST-08, ST-09) | Acknowledged — PT-04 gate (≥20 trades) not yet met at planning (15 trades). PO accepted firm inclusion; gate_not_met path is primary testable state. Score path validation deferred to staging or post-sprint verification |

---

## Pre-Sprint Vulnerability Scan

`pip-audit` not installed in the local environment. Command unavailable.

Advisory: PO and Head of Engineering acknowledge `pip-audit` unavailability as a documented risk. Recommendation: install `pip-audit` before Sprint 1 execution begins.

---

## Prompt Change Log Hygiene

- `sprint_planning_prompt.md`: current v3.10, last logged v3.9→v3.10 (2026-06-16) ✅ No gap
- `release_planning_prompt.md`: current v2.37, last logged v2.36→v2.37 (2026-06-17) ✅ No gap

---

## Skill-Silo Ceiling Advisory

**Release-level G+D+P ratio:** 5/9 = 55.6% (above 40% ceiling across all 9 stories)

**Per-sprint:**
- Sprint 1: 2G / 5 stories = 40% — at ceiling ✅
- Sprint 2: 3G+D / 4 stories = 75% — above ceiling ⚠ (structural; no compliant arrangement possible for Sprint 2 given remaining story composition)

Sprint 2 ceiling advisory does not block planning. Recorded for post-ship retrospective and future roadmap balancing.

---

## Outstanding Actions

| Action | Owner | Blocker? |
|--------|-------|---------|
| Install pip-audit before Sprint 1 execution | Head of Engineering | No |
| BLG-GOV-134 and BLG-QA-62 disposition: confirm v6.2 target or unscheduled | Product Owner | No — advisory for next release planning |
| EPIC-04 score path validation: confirm ≥20 closed trades reached before sprint close (or accept staging-only QA for score path) | PMO Lead; Director of Quality | No — gate_not_met path sufficient for sprint sign-off |
