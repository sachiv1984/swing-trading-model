**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Superseded
**Release:** v4.9
**Cycle:** 2026-06-02__release-v4.9
**Last Updated:** 2026-06-02 (post-ship closure)

---

## Decisions Record — v4.9

### Scope Decisions

| Decision | Rationale | Owner | Authority |
|----------|-----------|-------|-----------|
| Include BLG-GOV-78 (roadmap_prompt STEP 8.1 strengthening) as EPIC-03 | LL-RP-v4.8-01 deferred action; natural v4.9 fit; prevents recurring -1.2 advisory at each release planning | Head of Specs Team + PMO Lead | Product Owner |
| Exclude BLG-GOV-74 (AI quarterly review) from v4.9 | Gate date 2026-08-29 is post v4.9 ship; Provisional-Target: v4.9 tag was incorrect; deferred to first cycle after 2026-08-29 | PMO Lead | Product Owner |
| Include SI-05 Phase 1 (BLG-GOV-67) as conditional EPIC-04 | Gate clears 2026-06-21; OA-3 from v4.8 closure explicitly requires v4.9 prioritisation; conditional on gate confirmation at sprint planning | Product Owner | Product Owner |

### Sequencing Decisions

| Decision | Rationale |
|----------|-----------|
| EPIC-01 (security) executes first | P1 HIGH CVE item requires earliest resolution; no dependencies on other EPICs |
| EPIC-02 (CI) executes in parallel with EPIC-01 | Independent scope; Phase B CI wiring is a standalone infrastructure change |
| EPIC-03 (governance) executes independently | Governance prompt edit is a ~0.5d item; can execute in any order |
| EPIC-04 (conditional) executes last | Gate confirmation required before sprint planning seals; sequenced after firm scope |

### Accepted Risks

None — no escalations raised in this planning cycle.

### Supersession note

Superseded by: v4.9 ship — 2026-06-02
Changelog: docs/product/changelog.md#v4.9
Verification report: claude/cycles/2026-06-02__release-v4.9/verification_report.md
Cycle: 2026-06-02__release-v4.9
