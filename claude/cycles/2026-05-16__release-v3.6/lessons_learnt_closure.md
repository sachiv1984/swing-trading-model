Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-05-17
Cycle: 2026-05-16__release-v3.6

---

# Lessons Learnt Closure Record — 2026-05-16__release-v3.6

**Invoking routine:** post_ship_closure.md v2.7
**Phase:** Post-Ship
**Cycle:** 2026-05-16__release-v3.6
**Prior cycle checked:** 2026-05-15__release-v3.5 (lessons_learnt_closure.md present — recurrence check complete)

---

## Records Reviewed

| Record | Location | Status |
|--------|----------|--------|
| Release Planning lessons | claude/cycles/2026-05-16__release-v3.6/lessons_learnt.md | Read |
| Phase 3 (Sprint Execution) | claude/cycles/2026-05-16__release-v3.6/lessons_learnt_cycle.md §Phase 3 | Read |
| Phase 4 (Delivery Verification) | claude/cycles/2026-05-16__release-v3.6/lessons_learnt_cycle.md §Phase 4 | Read |
| Amendment sections | N/A — no amendments this cycle | N/A |

---

## Closure-Phase Observations

1. **Carry-forward resolution (v3.5 → v3.6):** All 4 v3.5 deferred governance patches delivered in EPIC-04 (ST-09/ST-10). §13 gate story pattern formalised; deviations_filed semantics guidance added; three-field readiness block confirmed; Phase 3 section present. The governance patch EPIC approach is proving reliable — 4 items cleared in 2 stories with no sprint friction.

2. **Document location (STEP 4):** Both scope document (`scope--2026-05-16__release-v3.6-arc-4-data-integrity.md`) and decisions document (`decisions--2026-05-16__release-v3.6.md`) located on first read. Both Superseded without friction.

3. **Backlog reconciliation (STEP 3):** 3 items marked COMPLETE (BLG-FE-26, BLG-FE-32, BLG-SPEC-27). BLG-FE-33 pre-confirmed present from delivery verification. No returns-to-backlog. No stale parked items (per verification report §5c). Clean backlog state.

4. **Specs Index (STEP 7):** TSG-v33-03 (SC-RV-18/SC-RV-19) resolved after 3 cycles open. TSG-v36-01 (ST-08 AC-02 font staging) added as new gap. One item resolved; one added — net zero open TSG items post-v3.6.

5. **Endpoint coverage drift (STEP 6):** No new backend routes in v3.6 (sprint_close confirmed no new `@router` decorators). Endpoint count unchanged at 57. No BLG-OPS advisory required.

6. **scored_initiatives.md staleness (OA-RP-05, continuing):** Identified in v3.5 release planning as "8+ cycles" stale. Now at 9+ cycles. Still carries an open advisory from v3.5 closure. Becoming a carry-forward escalation risk — see Recurrence Check.

---

## Consolidated Action Summary

### Immediate Actions Applied: 0

None applied in this closure run.

*All v3.5 carry-forward items were delivered during sprint execution (EPIC-04/ST-09/ST-10), not during this post-ship run. BLG-FE-33 was actioned during delivery verification. No template or prompt changes can be applied here without ambiguity — all are deferred to v3.7 with named owners.*

---

### Deferred to v3.7: 5

| # | Action | Source | Owner | Target |
|---|--------|--------|-------|--------|
| 1 | execution_prompt.md §3.1.A: add sub-step 10a — "Immediately after step 10 deviation check: write `deviations_filed: true` to execution_state.json for this ST item. Do not defer." Make the flag write atomic with the deviation check. | LL Phase 3 item 1 (recurrence from v3.5 deferred action) | Head of Specs Team | v3.7 |
| 2 | qa_evidence_template.md BLG-GOV-19 section: add explicit criterion 3 fail-path — "If any story has observable AC → autonomous class does not apply regardless of Playwright coverage. Use standard DoQ sign-off block and record Playwright test file references in DoQ comments." | LL Phase 3 item 2 | Director of Quality | v3.7 |
| 3 | PMO Lead to confirm STEP 5.4 (Phase 3 lessons append) is in every sprint close pre-seal checklist. No retroactive fix — enforcement going forward. | LL Phase 3 item 3 | PMO Lead | v3.7 |
| 4 | execution_prompt.md §3.1.A story completion checklist: add guidance — "When filing a mandatory backlog item for a deferred staging AC, verify the item appears in backlog.md before closing the story (file read or grep check)." | LL Phase 4 item 1 | Head of Specs Team | v3.7 |
| 5 | execution_prompt.md §3.1.A story completion checklist: add guidance — "When populating spec_references in execution_state.json, verify each path exists using a file read or ls check before recording." | LL Phase 4 item 2 | Head of Specs Team | v3.7 |

---

### Escalated for Decision: 0

None.

---

## Recurrence Check

**Prior cycle (v3.5) lessons_learnt_closure.md checked:** Present.

| v3.5 Carry-Forward Item | v3.6 Status |
|------------------------|-------------|
| §13 gate story pattern formalised in execution_prompt.md | ✅ RESOLVED — ST-09 v3.22 (2026-05-16) |
| deviations_filed semantics guidance (§3.1.A step 10) | ✅ RESOLVED structurally — ST-10 v3.22 (2026-05-16) — but execution discipline gap recurred (4 items still missed flag despite guidance) — deferred patch sub-step 10a (item #1 above) |
| sprint_close.md three-field verification readiness block | ✅ RESOLVED — ST-10 v3.22; confirmed in sprint_close.md ✅ |
| Phase 3 lessons section in lessons_learnt_cycle.md | ✅ RESOLVED — Phase 3 section present in v3.6 ✅ |
| scored_initiatives.md refresh (OA-RP-05) | ⚠ OPEN — 2nd consecutive cycle not addressed (advisory only; no hard gate) |

**Recurrence flag:** `deviations_filed = false` despite guidance — second consecutive cycle. Guidance was patched in v3.6 EPIC-04 but execution still missed the flag for 4 items. Sub-step 10a deferred to v3.7 (item #1). Not yet an escalation threshold per shared_standards.md §3.7 (threshold = 3 consecutive cycles).

**scored_initiatives.md staleness:** Confirmed 2 consecutive cycles open without action. OA-RP-05 remains open. If unresolved at v3.7 release planning, treat as escalation to Facilitator.

---

## Process Improvements Actioned This Run

None applied this run.

---

## New Files Created This Run

None.

---

## Outstanding Deferred Patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| claude/system/execution_prompt.md | §3.1.A story completion checklist | Add sub-step 10a: atomic deviations_filed = true write after deviation check | Head of Specs Team | v3.7 |
| docs/qa/templates/qa_evidence_template.md | BLG-GOV-19 criteria section | Add criterion 3 fail-path: observable AC disqualifies autonomous class regardless of Playwright coverage | Director of Quality | v3.7 |
| — (enforcement, not file) | Sprint close pre-seal checklist | PMO Lead to confirm STEP 5.4 Phase 3 LL append is included every sprint | PMO Lead | v3.7 |
| claude/system/execution_prompt.md | §3.1.A story completion checklist | Add guidance: verify backlog item appears in backlog.md before closing story with deferred staging AC | Head of Specs Team | v3.7 |
| claude/system/execution_prompt.md | §3.1.A story completion checklist | Add guidance: verify spec_references paths exist before recording in execution_state.json | Head of Specs Team | v3.7 |

---

## Escalations

None.

---

## Carry-Forward

Items: 3

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `deviations_filed = false` recurred in v3.6 despite guidance patch applied in EPIC-04. Flag-set is atomic with deviation check in principle but execution still defers it. Sub-step 10a (make write explicit) is the proposed fix. | Sprint Execution engine should confirm sub-step 10a is present in execution_prompt.md before execution begins; flag if absent. | Sprint Planning |
| 2 | BLG-GOV-19 autonomous class misapplied in two EPICs (EPIC-03 and EPIC-01) — observable frontend changes present in both. Playwright coverage was good; the classification failure was in the sign-off form. qa_evidence_template.md update deferred to v3.7 (Director of Quality). | Sprint Execution should flag BLG-GOV-19 class selection against observable AC list before signing off; delivery verification should check class eligibility at STEP -1.3. | Sprint Execution |
| 3 | scored_initiatives.md 9+ cycles stale; OA-RP-05 open 2 consecutive cycles. If not addressed before v3.7 roadmap, treat as escalation to Facilitator. | Roadmap engine should surface staleness advisory at STEP 1.1 and block DL advancement if OA-RP-05 still open. | Roadmap |
