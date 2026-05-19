**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-19
**Cycle:** 2026-05-19__release-v3.8

---

# Sprint Planning Notes — 2026-05-19__release-v3.8

---

## Backlog Slice Source

Original — `claude/cycles/2026-05-19__release-v3.8/stage4_backlog_slice.md`

`amended_backlog_slice_path` is null in state.json — no amendment in effect.

---

## Carry-Forward Items

From `claude/cycles/2026-05-18__release-v3.7/lessons_learnt_closure.md §Carry-Forward` (4 items reviewed):

| Item | Owner | Status in v3.8 |
|------|-------|----------------|
| PT-04 gate decision (park vs conditional) | Product Owner | **Resolved** — parked 2026-05-19: gate not met (< 20 closed trades) |
| DoQ sign-off date enforcement before PR merge | Director of Quality | **Addressed** — covered by ST-10 (governance debt clearance) |
| Smoke-tests.yml timeout review | QA & Testing Owner | Advisory — no action unless recurrence observed |
| v3.6 changelog entry reconstruction | PMO Lead | **Outstanding** — must be completed before v3.8 closes |

---

## Capacity WARN Acknowledgement

The release planning capacity check was `warn` (triggered by PT-04 inclusion: total mid ~12 days). EPIC-02 (ST-04, ST-05) has been removed from sprint scope by Product Owner decision 2026-05-19: PT-04 gate not met (< 20 closed trades), formally parked. Effective scope without PT-04: 6–10 days (mid ~8 days) — within comfortable range. Capacity WARN is resolved by virtue of scope reduction. Product Owner acknowledged by parking decision.

`capacity_warn_acknowledged = true` set in global state.

---

## Pre-Sprint Required Decisions

| Decision | Owner | Resolution |
|---------|-------|-----------|
| [RISK-01] PT-04 gate (20+ closed trades) | Product Owner | **Resolved 2026-05-19** — gate not met; EPIC-02 removed; PT-04 parked in backlog |

All pre-sprint required decisions resolved. Sprint planning may proceed to seal.

---

## Deferred Items

| Item | EPIC | Reason | Next Sprint Candidate? |
|------|------|--------|-----------------------|
| ST-04 — PT-04 Backend Setup Quality Score | EPIC-02 | PO decision 2026-05-19: gate not met (< 20 closed trades); PT-04 formally parked in backlog | No — gate condition required before re-entry |
| ST-05 — PT-04 Frontend Setup Quality Score Display | EPIC-02 | Depends on ST-04 (removed); same gate applies | No — gate condition required |
| ST-02 — SI-01 Backend Validation Service | EPIC-01 | Sprint 2 — gated by ST-01 §13 PASS (Sprint 1 gate story) | Yes — Sprint 2 |
| ST-03 — SI-01 Frontend Validation Panel | EPIC-01 | Sprint 2 — gated by ST-01 §13 PASS and ST-02 | Yes — Sprint 2 |

---

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-07 (News Context Panel) | Alpaca News API integration (existing) | External (already available) | Resolved — same endpoint as screener news panel |
| ST-08 (AI-Assisted Thesis Generation) | ST-06 (setup type dropdown) | Internal — Sprint 1 | Resolved — ST-06 before ST-08 within EPIC-03 |
| ST-08 (AI-Assisted Thesis Generation) | ST-07 (news context panel) | Internal — Sprint 1 | Resolved — ST-07 before ST-08 within EPIC-03 |
| ST-02 (SI-01 Backend) | ST-01 §13 PASS decision | Cross-sprint gate | Resolved at planning — ST-01 Sprint 1, ST-02 Sprint 2 |
| ST-03 (SI-01 Frontend) | ST-02 (backend service) | Internal — Sprint 2 | Resolved — ST-02 before ST-03 within EPIC-01 Sprint 2 |
| ST-03 (SI-01 Frontend) | ST-01 §13 PASS decision | Cross-sprint gate | Resolved at planning — same gate as ST-02 |

No circular dependencies detected.

---

## Execution Sequence

### Sprint 1

**EPIC-04** (merge 1st — fewest shared file conflicts):
1. ST-10 — Governance Debt Clearance (autonomous; fastest delivery; no dependencies)
2. ST-09 — Ticker Universe Management Page (delegated_frontend; largest frontend story in EPIC-04)

**EPIC-03** (merge 2nd — after EPIC-04 lands on main):
3. ST-06 — Setup Type Classification Field (delegated_frontend; DB migration + API + form dropdown; must precede ST-08)
4. ST-07 — News Context Panel (delegated_frontend; uses existing news endpoint; must precede ST-08)
5. ST-08 — AI-Assisted Thesis Generation (delegated_frontend; depends on ST-06 + ST-07)

**EPIC-01 Sprint 1** (merge 3rd — after EPIC-03 lands on main; gate story only):
6. ST-01 — §13 Review Gate (delegated_decision; blocks Sprint 2 ST-02/ST-03)

### Sprint 2

**EPIC-01 Sprint 2** (continues on same exec branch):
7. ST-02 — SI-01 Backend Validation Service (autonomous; requires ST-01 §13 PASS)
8. ST-03 — SI-01 Frontend Validation Panel (delegated_frontend; requires ST-02)

---

## Multi-EPIC Execution Notes

**execution_state.json owner:** EPIC-04 (first in execution order). All other EPIC branches (EPIC-03, EPIC-01) must check for `execution_state.json` existence before creating their own version — if found, read and append their EPIC's section rather than overwrite.

**EPIC-03:** Must rebase onto `main` after EPIC-04 merges before finalising any shared file changes.

**EPIC-01:** Must rebase onto `main` after EPIC-03 merges before finalising any shared file changes.

### Shared Files Across EPICs

| Shared File | Owner EPIC | Used by | Advisory |
|------------|-----------|---------|---------|
| `docs/reference/openapi.yaml` | EPIC-04 (first merge) | EPIC-03 (news endpoint), EPIC-01 (pre-entry endpoint) | EPIC-03 and EPIC-01 must rebase onto main after EPIC-04 merges |
| `backend/routers/test.py` | EPIC-04 (first merge) | EPIC-03 (potentially), EPIC-01 (pre-entry route) | Same rebase requirement |
| `docs/specs/data_model.md` | EPIC-04 (ticker_universe changes) | EPIC-03 (setup_type migration), EPIC-01 (potentially) | Rebase required after EPIC-04 |

---

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-02 | **Resolved** — EPIC-02 removed; PT-04 parked |
| RISK-02 | EPIC-01 | **Valid** — ST-01 §13 gate in Sprint 1 mitigates scope restriction risk; binding conditions documented in decisions record |
| RISK-03 | EPIC-03 | **Valid** — ST-06 → ST-07 → ST-08 sequencing enforced within EPIC-03; ST-08 Phase 1 template-only approach avoids external API dependency |
| RISK-04 | EPIC-04 | **Valid** — ST-09 AC requires ticker_universe seeded before sync removal; Playwright coverage required for screener/signal correctness |

---

## Pre-Sprint Vulnerability Scan

**pip-audit result: CLEAN** — No vulnerabilities detected in `backend/requirements.txt` (run 2026-05-19, pre-sprint).

---

## Prompt Change Log Advisory

Latest entries in `claude/system/prompt_change_log.md` reviewed:
- `execution_prompt.md`: last logged v3.23→v3.24 (2026-05-18)
- `sprint_planning_prompt.md`: last logged v3.1→v3.2 (2026-05-16)
- `OPERATIONAL_GUIDE.md`: last logged v3.90→v3.91 (2026-05-18)

No Class 6 prompt version gaps detected against last logged entries.

---

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| v3.6 changelog entry reconstruction (`docs/product/changelog.md`) | PMO Lead | No — due before v3.8 closes |
| Smoke-tests.yml timeout review (if CI timeout recurs) | QA & Testing Owner | No — advisory; trigger is recurrence |
| design_gate.md present only on hotfix branch, not yet on main | PMO Lead | No — advisory; design gate passed per state.json; file will land via hotfix merge |

---

## LL-v2.2-SP-01 Design Artefact Check

- ST-01 (`delegated_decision`): §13 review process is a documented governance gate per `strategy_rules.md §13` and `execution_prompt.md §5.1`. Design artefact = the §13 review decision record produced by ST-01 itself. No prior HoST design session required — the ST-01 delivery IS the design artefact.
- All other items: no `delegated_decision` classification. Check not applicable.

---

## LL-v2.0-P4-2 Test Scenario Gap Check

Items introducing new pages / new user-facing controls:
- ST-09 (Ticker Universe Management Page): new page. Playwright scenarios required per AC. No test_scenarios gap — AC specifies Playwright coverage for add/toggle/delete/filter.
- ST-06, ST-07, ST-08 (Trade Plan Form enhancements): new controls on existing page. Playwright scenarios specified in AC for each item.
- ST-03 (Pre-Entry Validation Panel): new panel. Playwright coverage specified in AC.

No `test_scenarios = "pending"` flag required — all delegated_frontend items have specified Playwright scenarios in their AC.
