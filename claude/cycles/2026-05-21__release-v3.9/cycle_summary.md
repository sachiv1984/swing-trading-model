Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Release: v3.9
Cycle: 2026-05-21__release-v3.9
Last Updated: 2026-05-21

---

# Cycle Summary — v3.9

**Theme:** Screener Quality & Reliability + Arc 5 Red Flag Journal (SI-03) + Governance Patches

**Cycle ID:** 2026-05-21__release-v3.9
**Published:** 2026-05-21
**Mode:** standard
**State at summary:** Validated

---

## Scope

| EPIC | Stories | Description | Sprint |
|------|---------|-------------|--------|
| EPIC-01 | ST-01–ST-04 | Screener data quality & reliability (P1/P2 bug fixes + degraded-run warning) | Sprint 1 |
| EPIC-02 | ST-05–ST-06 | Ticker Universe enhancements (.L suffix display, company_name) | Sprint 1 |
| EPIC-03 | ST-07–ST-08 | Arc 5 Red Flag Journal — backend + frontend | Sprint 2 |
| EPIC-04 | ST-09–ST-12 | Governance patches (CF-2/3/4/5, BLG-GOV-25) | Sprint 2 |
| EPIC-05 (cond.) | ST-13–ST-14 | PT-04 Setup Quality Score (gate: 20+ closed trades) | Sprint 2 (if gate met) |

**Firm stories:** 12
**Conditional:** +2 (ST-13/ST-14, EPIC-05)

**Sprint 1 merge order:** EPIC-02 → EPIC-01
**Sprint 2 merge order:** EPIC-04 → EPIC-03 → EPIC-05 (if in scope)

---

## Capacity

- **Estimated firm effort:** ~7–10 days
- **Estimated with EPIC-05:** ~9–14 days
- **Capacity check:** WARN (standard mode — within tolerance; EPIC-05 brings total close to upper bound)
- **Velocity reference:** v3.8 = 1.00; rolling 6-cycle avg = 0.97
- **Phasing:** Sprint 1 is well within capacity. Sprint 2 approach EPIC-05 gate decision at sprint planning.

---

## Key Risks

| Risk | Disposition |
|------|-------------|
| RISK-01: YF crumb fix incomplete if YF changes auth | Medium — mitigated by degraded-run warning (S2-02) as secondary signal |
| RISK-03: SI-03 Red Flag Journal — SI-01 event persistence model | Medium — verify at sprint planning; include DB migration if needed |
| RISK-05: PT-04 gate not met | High for EPIC-05 only — gate decision required at sprint planning |

---

## Pre-sprint Planning Required Decisions

The following decisions must be resolved before sprint planning seals (i.e., before `sprint_sealed = true`). Sprint Planning Engine STEP -1 must consume this checklist.

- [ ] [RISK-03] SI-03 backend prerequisite — verify SI-01 override event persistence model in v3.8 code; confirm whether a new DB table/migration is needed for ST-07 — Owner: Head of Backend Engineering
- [ ] [RISK-05] PT-04 gate — Product Owner confirms whether 20+ closed trades gate is met; if yes, EPIC-05 (ST-13/ST-14) enters sprint backlog; if no, record `deferred_at_planning` — Owner: Product Owner

---

## Carry-Forward From v3.8 (Disposition)

| Item | Disposition in v3.9 |
|------|---------------------|
| Duplicate GitHub issues audit/close | PMO Lead housekeeping during sprint execution (not a story) |
| createPageUrl map in delegation template | ST-09 (EPIC-04) |
| QA evidence pre-merge enforcement (escalated) | ST-12 (EPIC-04); DoQ must confirm active before execution begins |
| test_scenarios population guidance | ST-09 (EPIC-04) |
| Planning-deferred in execution_state.json | ST-10 (EPIC-04) |

All 5 carry-forward items addressed. ✅

---

## Outstanding Actions at Publish

| # | Action | Owner | When |
|---|--------|-------|------|
| 1 | Confirm PT-04 gate (20+ closed trades) | Product Owner | Before sprint planning seals |
| 2 | Verify SI-01 override event persistence model | Head of Backend Engineering | Before sprint planning seals |
| 3 | Confirm DoQ PR template checklist item is live (CF-3 escalation) | Director of Quality | Before v3.9 execution begins |
| 4 | Audit and close duplicate GitHub issues from v3.8 | PMO Lead | During sprint execution |

---

## Integrity Gate Results

| Gate | Result |
|------|--------|
| STEP 5.5 Cross-stage integrity | ✅ Pass |
| STEP 5.7 Decision record integrity | ✅ N/A (no escalations) |
| Stage 1–3.5 | ✅ Pass |
| Capacity check | ⚠️ WARN (within standard mode tolerance) |
| Publish gate | ✅ Eligible (standard mode; capacity warn accepted) |
