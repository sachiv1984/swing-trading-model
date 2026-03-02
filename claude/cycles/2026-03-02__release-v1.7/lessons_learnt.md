**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Cycle:** 2026-03-02__release-v1.7
**Last Updated:** 2026-03-02

---

# Lessons Learnt — v1.7 Release Planning

## Process Observations

### LL-01 — Spec Debt Items Benefit From Explicit Release Assignment
**Observation:** BLG-TECH-06, BLG-TECH-08, and BLG-TECH-09 all arrived in the v1.7 backlog with explicit target release assignments made in prior cycles (OBS-01 from BLG-TECH-02/03 cycle; OBS-QWB-R1-01 and OBS-QWB-R3-01 from the QWB cycle). This meant they were immediately plannable in v1.7 without requiring re-triage.

**Lesson:** The practice of assigning priority, target release, and owner at observation time (per document_lifecycle_guide.md §9) directly accelerates release planning. Observations without these fields cause friction and delay. Continue enforcing §9 at every observation point.

**Action:** None required — existing practice is working well. Reinforce at verification phases.

---

### LL-02 — Pre-Condition Decisions Should Have Named Decision Owners and Expected Dates
**Observation:** BLG-TECH-08 (S2-07) and BLG-TECH-09 (S2-08) arrived in v1.7 planning with "Decision required: Product Owner + API Contracts owner to decide" but no documented deadline or joint session scheduled. This creates a stall risk during execution (RISK-02).

**Lesson:** When a backlog item documents a pre-condition decision, the backlog entry should also record:
- The named decision owners
- The expected decision date or trigger (e.g., "before v1.7 execution begins")

This would allow release planning to pick up these items without having to re-state the decision requirement as a RISK.

**Action:** Consider adding a "Decision Owner" and "Decision Target Date" field to future backlog observations that require a pre-condition decision.

---

### LL-03 — Foundation Releases Are Worth Protecting From Feature Creep
**Observation:** v1.7 is scoped to eight items, all non-user-facing governance and foundation tasks. There was no pressure to add user-facing features to this release.

**Lesson:** Explicitly framing a release as "Foundation" in the roadmap provides useful protection against scope creep during planning. When the release theme is governance/infrastructure, user-facing items are easy to identify and reject.

**Action:** Continue using explicit release themes in the roadmap. Consider a similar protection note for any future foundation-type releases.

---

### LL-04 — §13 Boundary Reviews Should Be Proactive, Not Reactive
**Observation:** The §13 boundary review (S2-02, EPIC-02) is needed because four features are now gated behind a formal boundary confirmation. The features (signal exposure, AI journal summarisation, new technical indicators) have been in the gated features table for some time.

**Lesson:** §13 boundary reviews work better as proactive governance events scheduled independently of release planning, rather than reactive gates that block feature pre-alignment. A quarterly or release-triggered §13 review cadence would prevent gated features from accumulating.

**Action:** Consider adding a standing §13 governance review to the Roadmap Rebalance Engine cadence so boundaries are reviewed each cycle rather than only when features queue up.

---

### LL-05 — Metrics Definitions Owner Concurrency Must Be Monitored Actively
**Observation:** RISK-03 captures that the Metrics Definitions & Analytics Owner is required for both EPIC-03 (v1.7) and BLG-FEAT-08 (v1.9). This constraint is documented in workforce_capacity.md but must be actively checked before v1.9 pre-alignment opens.

**Lesson:** Shared scarce-resource constraints documented in workforce_capacity.md need an explicit "check at" trigger — typically when the later-dependent release begins pre-alignment. The FinOps & Resource Architect should confirm capacity before v1.9 pre-alignment opens, not only during v1.7 planning.

**Action:** Add a note to v1.9 pre-alignment triggering events: confirm Metrics Definitions owner is available and EPIC-03 is complete before BLG-FEAT-08 is scheduled.

---

### LL-06 — Clean Runs Are Worth Documenting
**Observation:** This planning cycle ran to completion with no escalations, no blockers, and no conditional gate failures. All hard gates passed first time.

**Lesson:** Clean runs demonstrate that the governance framework is working correctly when documentation and observations are being maintained well (per LL-01). They should be noted as evidence of process health.

**Action:** None required.

---

## Summary

| Lesson | Category | Priority |
|--------|----------|----------|
| LL-01 — Spec debt observation fields at time of discovery | Process / Governance | Low — already doing this; reinforce |
| LL-02 — Pre-condition decisions need named owner + date | Backlog hygiene | Medium — small process change |
| LL-03 — Foundation releases worth protecting | Release framing | Low — continue current practice |
| LL-04 — Proactive §13 reviews vs reactive gates | Governance cadence | Medium — consider roadmap engine enhancement |
| LL-05 — Shared resource constraint monitoring | Capacity management | Medium — add trigger to v1.9 pre-alignment |
| LL-06 — Clean run as process health signal | Process health | Low — record and note |
