**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-05-22
**Cycle:** 2026-05-22__scheduled

---

# Lessons Learnt — 2026-05-22__scheduled

## Summary

| Friction count | Deferred patches | Action-now items |
|---------------|-----------------|-----------------|
| 2 | 0 | 2 |

---

## Frictions

### Friction #1 (Type B): P1 spec debt items accumulating from shipped features

**Observed:** Two P1 spec debt items created this cycle (BLG-SPEC-33 for SI-03 API contract, BLG-SPEC-34 for SI-01 API contract). Both endpoints shipped (v3.9 and v3.8 respectively) without formal API contract documents. Pattern: new Arc 5 endpoints ship, spec debt is filed as backlog items, but sprint planning does not proactively include spec debt clearing for recently shipped endpoints.

**Root cause:** Sprint planning currently does not have an explicit check for "has the previous sprint's shipped endpoints generated spec debt that should be included in this sprint?" The API contracts for SI-01 and SI-03 should ideally have been included in the sprints that shipped those features.

**Recommendation:** At sprint planning, the Head of Specs Team should explicitly scan for spec debt from the immediately prior release before finalising sprint scope. This complements BLG-GOV-30/31 process improvements.

**Owner:** Head of Specs Team

**Status:** Deferred — governance improvement for v4.0 sprint planning. No action-now required (not blocking).

---

### Friction #2 (Type A): SI-05 scope ambiguity surfaced during idea debate

**Observed:** IDEA-product-owner-20260522-01 proposed shipping SI-05 without SI-02. The Challenger correctly identified that SI-05's documented scope explicitly requires SI-02 drift signals as a named component — partial delivery would create product definition confusion. The idea was correctly parked.

**Root cause:** SI-05 roadmap entry has a dependency note ("depends on SI-02 + SI-03") but this is not written as a hard gate. Ambiguity in dependency language allows optimistic re-interpretation.

**Recommendation:** At v4.0 release planning, when SI-05 is scoped, the dependency on SI-02 should be recorded as an explicit hard gate (not an advisory note) in the release plan. If PO wishes to deliver a partial digest, a formal roadmap scope change (DL entry) must be made first.

**Owner:** Product Owner (at v4.0 release planning)

**Status:** Deferred — governance note for v4.0 release planning. No action-now required.

---

## Action-Now Items (STEP 11)

### OA-01: Action BLG-GOV-30 and BLG-GOV-31 before next sprint planning

**Owner:** Head of Specs Team
**Due:** Before v4.0 sprint planning seals

Both BLG-GOV-30 (sprint planning staging-only AC designation flag) and BLG-GOV-31 (merge gate re-invocation advisory) are P1 governance process improvements that directly address the two carry-forward advisories from v3.9 post-ship closure. They should be actioned in the same governance commit before v4.0 sprint planning begins.

**Scope:**
- BLG-GOV-30: Add `staging_only_evidence` field notation to sprint_backlog.md schema documentation and update sprint_planning_prompt.md to prompt for designation when an AC references external live service behaviour.
- BLG-GOV-31: Add a re-invocation advisory to the sprint capacity template noting that the execution engine must be re-invoked after each EPIC GitHub merge to keep `merge_gate.epics_merged` current.

**Note:** Both items require governance file edits → CLAUDE.md §6 checklist applies (version bump, OPERATIONAL_GUIDE.md update, prompt_change_log.md append, §14 table update). Head of Specs Team sign-off required.

---

### OA-02: Address spec debt BLG-SPEC-33 and BLG-SPEC-34 before SI-04/SI-05 sprint planning

**Owner:** API Contracts Documentation Owner
**Due:** Before SI-04 or SI-05 sprint planning seals

BLG-SPEC-33 (SI-03 Red Flag Journal API contract) and BLG-SPEC-34 (SI-01 Pre-Entry Validation API contract) are P1 spec debt items. SI-04 and SI-05 will extend or reference both endpoints; having no formal API contracts for them creates implementation risk.

**Scope:**
- Author `docs/specs/api_contracts/red_flag_journal.md` for `GET /portfolio/red-flag-journal` — filter parameters, pagination schema, error codes, SI-01 write path.
- Author `docs/specs/api_contracts/pre_entry_validation.md` for `GET /portfolio/pre-entry-validation` — rule enumeration, response schema, override acknowledgement path.
- Each contract must be registered in `docs/reference/openapi.yaml` per CLAUDE.md §2.

---

## Deferred Patches

None. Both action-now items are scoped as sprint planning or sprint execution work, not prompt patches. No governance prompt changes are warranted from this cycle's frictions.

---

## Carry-Forward Advisory (from this cycle)

| # | Item | Owner | Implication |
|---|------|-------|-------------|
| 1 | Spec debt from shipped features (BLG-SPEC-33, BLG-SPEC-34) | API Contracts Documentation Owner | Future sprints should proactively include API contract authoring for newly shipped endpoints |
| 2 | SI-05 scope dependency hardening | Product Owner | At v4.0 release planning, record SI-02 as a hard gate for SI-05, not an advisory dependency |
