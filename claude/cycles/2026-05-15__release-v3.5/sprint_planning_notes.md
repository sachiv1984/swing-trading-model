**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-15
**Cycle:** 2026-05-15__release-v3.5

---

# Sprint Planning Notes — 2026-05-15__release-v3.5

---

## Backlog Slice Source

Original — `claude/cycles/2026-05-15__release-v3.5/stage4_backlog_slice.md`

No amendment active (`amended_backlog_slice_path` absent from `.claude_current_state.json`).

---

## Deferred Items

| Item | Reason | Next Sprint Candidate? |
|------|--------|----------------------|
| ST-02, ST-03 (conditional) | §13 determination pending (RISK-01) — included as conditional Sprint 2 items; deferred to v3.6 only if §13 FAIL | Yes (Sprint 2, if §13 PASS) |
| ST-06 (conditional) | Capacity WARN — PO-01 frontend phaseable to v3.6 if Sprint 2 capacity exceeded after IT-06 | Yes (Sprint 2 if capacity allows; v3.6 fallback) |

---

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-02 | ST-01 (§13 PASS) | Internal — gate | Conditional: ST-01 must complete with PASS outcome |
| ST-03 | ST-02 | Internal — implementation | Resolved (ST-02 in scope before ST-03) |
| ST-05 | ST-04 | Internal — prerequisite | Resolved (ST-04 first in EPIC-02) |
| ST-06 | ST-05 | Internal — API | Resolved (ST-05 before ST-06) |
| ST-03 | UX spec at `docs/ux_specs/paper-trading/ux_spec.md` | Spec dependency | ✅ Resolved — design gate created spec v1.0 |
| ST-06 | UX spec at `docs/ux_specs/plan-vs-reality/ux_spec.md` | Spec dependency | ✅ Resolved — design gate created spec v1.0 |

---

## Execution Sequence

### Sprint 1

1. **EPIC-04** (governance patches — first per convention):
   - ST-11 → ST-12 → ST-13 (sequential; each prompt edit owned by Head of Specs Team)
2. **EPIC-03** (spec/QA debt — parallelisable with EPIC-01 ST-01):
   - ST-07, ST-08 (XS, parallelisable)
   - ST-09 (codebase scan, autonomous)
   - ST-10 (QA protocol doc, requires QA Lead sign-off)
3. **EPIC-01 ST-01** (§13 compliance review — can run in parallel with EPIC-03; must complete before Sprint 2 EPIC-01 begins):
   - ST-01: Strategy Rules & System Intent Owner sign-off required

### Sprint 2

4. **EPIC-01** (conditional on ST-01 PASS):
   - ST-02 (backend sync service) → ST-03 (frontend panel)
5. **EPIC-02**:
   - ST-04 (data requirements capture — Head of UX & Design + PO sign-off) → ST-05 (backend calculation service) → ST-06 (frontend comparison view, capacity permitting)

**Merge order:** EPIC-04 → EPIC-03 → EPIC-01 → EPIC-02 (per cycle_summary.md recommendation)

---

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 (ST-02, ST-03) | Valid — §13 review as ST-01 in Sprint 1; EPIC-01 implementation conditional on PASS; if FAIL, EPIC-01 reduces to ST-01 only; EPIC-02 absorbs freed capacity |
| RISK-02 | EPIC-02 (ST-05, ST-06) | Valid — PO-01 H effort; ST-06 phaseable to v3.6 as safety valve; capacity WARN acknowledged (pending PO sign-off) |
| RISK-03 | EPIC-02 (ST-05, ST-06) | Valid — graceful degradation designed in (empty state); no gate on data volume; low risk to implementation |

---

## Pre-Sprint Vulnerability Scan

pip-audit result: **CLEAN** — no known vulnerabilities in `backend/requirements.txt`.
Scan completed: 2026-05-15. No CVEs identified. No PO acceptance required.

---

## Carry-Forward Items

From cycle `2026-05-14__release-v3.4` lessons_learnt_closure.md (6 items reviewed):

| # | Carry-Forward Item | Resolution in v3.5 |
|---|-------------------|-------------------|
| 1 | BLG-GOV-22 — sprint_planning_prompt.md shared execution_state.json ownership rule | ✅ ST-11 (EPIC-04) |
| 2 | BLG-GOV-22 — sprint_backlog.md template merge order + Positions.js advisory | ✅ ST-11 (EPIC-04) |
| 3 | execution_prompt.md — before filing deviation, verify spec intent (not literal wording) | ✅ ST-12 (EPIC-04) |
| 4 | execution_prompt.md — when filing deviation, add Known Deviations to canonical spec same commit | ✅ ST-12 (EPIC-04) |
| 5 | execution_prompt.md / lessons_learnt — ID uniqueness check before filing backlog IDs | ✅ ST-12 (EPIC-04) |
| 6 | LL-v3.3 CF-01 — Deviations Filed table priority consistency check | ✅ ST-13 (EPIC-04) |
| 7 | LL-v3.3 CF-02 — Protocol checkbox: BLG ID required for backlog item claims | ✅ ST-13 (EPIC-04) |

All 7 carry-forward items from v3.4 are in scope as v3.5 EPIC-04 stories. Full resolution expected this sprint.

---

## Capacity WARN Acknowledgement

**Source:** `release_plan.md ## Capacity Check` → outcome = `warn`

**Summary:**
- Total estimated effort Scenario A (§13 PASS): ~13–16 days
- Total estimated effort Scenario B (§13 FAIL): ~9–11 days
- Confirmed capacity: ~10–12 days (solo dev, evenings)
- Over-allocation (Scenario A): ~2–4 days
- Release valves: (a) §13 FAIL removes ~4–5 days Sprint 2 scope; (b) ST-06 deferral removes ~2 days

**Product Owner acknowledgement:** Confirmed — Product Owner accepts Scenario A over-allocation with release valves in place (2026-05-15)

---

## Pre-Sprint Required Decisions

| Decision | Source | Status | Notes |
|----------|--------|--------|-------|
| [RISK-01] §13 compliance review for IT-06 | cycle_summary.md Pre-sprint Required Decisions | Conditional OA | ST-01 IN Sprint 1 is the resolution mechanism. Determination doc required at `docs/product/decisions/decisions--2026-05-15__release-v3.5--IT-06-section13-review.md`. Blocker? Conditional (blocks EPIC-01 ST-02/03 execution only — not Sprint 1 execution). |

---

## Prompt Change Log Gaps (Advisory)

The following Class 6 prompts have current versions exceeding the last logged entry in `claude/system/prompt_change_log.md`. Entries from the modular changelogs (introduced 2026-05-09) were not mirrored to `prompt_change_log.md`.

| Prompt | Current Version | Last Logged Version | Gap |
|--------|----------------|---------------------|-----|
| `sprint_planning_prompt.md` | v3.0 | v2.8 (2026-05-10) | v2.8→v2.9, v2.9→v3.0 not in prompt_change_log.md (recorded in sprint_planning_changelog.md) |
| `shared_standards.md` | v3.0 | v2.7 (2026-03-23) | v2.7→v3.0 not in prompt_change_log.md |
| `execution_prompt.md` | v3.18 | v3.17 (2026-05-10) | v3.17→v3.18 not in prompt_change_log.md |
| `OPERATIONAL_GUIDE.md` | v3.81 | v3.78 (2026-05-15) | v3.78→v3.81 not in prompt_change_log.md |

Advisory only — does not block sprint planning. Recommend backfilling `prompt_change_log.md` entries in a future governance cycle.

---

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Product Owner confirm or replace sprint goal | Product Owner | Yes |
| Product Owner acknowledge capacity WARN (Scenario A over-allocation) | Product Owner | Yes |
| Product Owner accept conditional scope for EPIC-01 ST-02/03 (conditional on ST-01 §13 outcome) | Product Owner | Yes |
| §13 compliance determination document filed (`docs/product/decisions/decisions--2026-05-15__release-v3.5--IT-06-section13-review.md`) | Strategy Rules & System Intent Owner (via ST-01) | Conditional — blocks EPIC-01 ST-02/03 execution; does not block Sprint 1 |
