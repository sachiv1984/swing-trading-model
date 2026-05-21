Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-05-21
Cycle: 2026-05-19__release-v3.8

---

# Lessons Learnt Closure Record — 2026-05-19__release-v3.8

**Phase:** Post-Ship Closure
**Cycle:** 2026-05-19__release-v3.8
**Generated:** 2026-05-21
**Records reviewed:** lessons_learnt.md (Release Planning), lessons_learnt_cycle.md §Phase 3 (Sprint Execution), lessons_learnt_cycle.md §Phase 4 (Delivery Verification)

---

## Closure-Phase Observations

1. **Clean document closure:** All required artefacts present and in expected state. No missing documents, no stale status fields requiring correction in STEP 6 (System_status_report.md was updated in Phase 4 to Verified_with_deviations — already current at closure). STEP 6 operational docs reconciliation was minimal (no corrections required beyond velocity_metrics.md row append).

2. **Deviation compliance complete:** One P3 deviation (DEV-EPIC04-ST09-01) — Known Deviations section already added to `docs/specs/api_contracts/ticker_universe_api_contract.md` during Phase 4 verification (LL-v2.3-CL-03). All six required fields present. No corrections needed in STEP 5.

3. **Backlog reconciliation clean:** All 5 source backlog items (BLG-FEAT-22/23/24, BLG-FE-36, BLG-GOV-24) marked ✅ COMPLETE. BLG-FEAT-25 (Phase 4 addition for ST-04/ST-05) confirmed present. No missing Phase 4 additions.

4. **SI-01 §13 decision record:** `docs/product/decisions/decisions--2026-05-19__release-v3.8--SI-01-section13-review.md` is an Operational Record (Class 3, Status: Active — PASS) — correctly NOT superseded. Confirmed filed and linked from changelog entry.

5. **PT-04 carry-forward resolved:** v3.7 carry-forward item "PT-04 gate decision (park vs conditional)" is fully resolved. PT-04 formally parked in roadmap and backlog (PO confirmed 2026-05-19). No fourth conditional deferral.

6. **v3.6 changelog carry-forward resolved:** v3.7 outstanding action to reconstruct v3.6 changelog entry — confirmed present in docs/product/changelog.md (entry for v3.6 — Arc 4 Data Integrity + Research Debt Clearance + Governance Patches — 2026-05-17). Resolved.

---

## Prior Cycle Carry-Forward Disposition (v3.7 → v3.8)

| Item | Resolution |
|------|-----------|
| PT-04 gate decision | ✅ Resolved — PT-04 formally parked 2026-05-19 (PO); roadmap + backlog updated |
| DoQ sign-off date enforcement before PR merge | 🔁 Recurrence carried — retroactive QA evidence recurred in v3.8 Phase 3 and Phase 4; now escalated per lessons_learnt_prompt §6.4; Director of Quality target v3.9 sprint start |
| Smoke-tests.yml timeout review | ✅ N/A — no CI timeout recurrence in v3.8 |
| v3.6 changelog entry reconstruction | ✅ Resolved — v3.6 entry confirmed present in changelog |

---

## Lessons Learnt Action Summary

### Records Reviewed

| Record | Actions Reviewed |
|--------|-----------------|
| lessons_learnt.md (Release Planning) | 3 action items |
| lessons_learnt_cycle.md Phase 3 (Sprint Execution) | 3 friction items (classified) |
| lessons_learnt_cycle.md Phase 4 (Delivery Verification) | 4 friction items (classified) |

---

### Immediate Actions Applied (0)

No new immediate actions required at post-ship closure. Items classified as action-now in Phase 3 and Phase 4 records were already applied during those phases:
- ST-03 reclassification (LL-v2.3-EX-02) — applied during Phase 3 execution; no template change needed
- Result column placeholder gap — resolved in practice (v3.8 QA evidence shows correct values); no further template edit required beyond the v1.2 patch applied in v3.7 post-ship closure

---

### Deferred to Next Cycle (6)

| # | Action | Owner | Target cycle | Source record |
|---|--------|-------|--------------|---------------|
| 1 | Audit and close duplicate GitHub issues created during v3.8 sprint execution (engine's gh issue create does not check for pre-existing issues with matching [ST-xx] titles) | PMO Lead | v3.9 | lessons_learnt.md #3 |
| 2 | Add createPageUrl map update requirement to delegation template for new frontend page stories | Head of Specs Team | v3.9 | Phase 3 LL item 1 |
| 3 | Add QA evidence existence check to PR template checklist; delegation recipients must create evidence before requesting merge | Director of Quality | v3.9 | Phase 3 LL item 2 |
| 4 | **[ESCALATION]** Retroactive QA evidence enforcement — deferred 2 cycles (v3.7 Phase 3 → v3.8 Phase 3 → v3.8 Phase 4). Director of Quality must implement PR template checklist item or automated check before v3.9 execution begins. | Director of Quality | v3.9 sprint start | Phase 4 LL item 1 (escalated per §6.4) |
| 5 | Update execution_prompt.md: test_scenarios should only list spec files containing scenarios exercised for that EPIC's AC (stale cross-file references inflate traceability check) | Head of Specs Team | v3.9 | Phase 4 LL item 2 |
| 6 | Update sprint_planning_prompt.md: record planning-deferred items in execution_state.json with status deferred_at_planning and gate_condition note | Head of Specs Team | v3.9 | Phase 4 LL item 3 |

---

### Decision Required (0)

No items requiring a named authority decision. PT-04 gate decision was actioned by Product Owner during sprint planning (formal park). Escalations above are enforcement actions with a named owner (Director of Quality), not decision questions.

---

## Carry-Forward

| Item | Type | Owner | Target | Notes |
|------|------|-------|--------|-------|
| Duplicate GitHub issues audit and close | Deferred | PMO Lead | v3.9 | Engine creates issues without checking for pre-existing [ST-xx] matches |
| createPageUrl map in delegation template | Deferred | Head of Specs Team | v3.9 | From DEV-EPIC04-ST09-01 root cause |
| QA evidence pre-merge enforcement (ESCALATION) | Deferred (escalated) | Director of Quality | v3.9 sprint start | 2-cycle recurrence — §6.4 escalation; PR template checklist item required before v3.9 execution opens |
| test_scenarios population guidance | Deferred | Head of Specs Team | v3.9 | execution_prompt.md update |
| Planning-deferred items in execution_state.json | Deferred | Head of Specs Team | v3.9 | sprint_planning_prompt.md update |

---

// ARTEFACT_STATUS
{
  "phase": "Post-Ship Closure",
  "cycle_id": "2026-05-19__release-v3.8",
  "status": "complete",
  "generated_utc": "2026-05-21T00:00:00Z"
}
