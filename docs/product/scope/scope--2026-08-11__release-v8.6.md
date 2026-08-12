Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v8.6
Cycle: 2026-08-11__release-v8.6
Last Updated: 2026-08-12

## Release Scope — v8.6 User Features, Data-Integrity Foundation & Correctness Carryover

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | User-facing product features: trade-plan completion-rate tracking (`BLG-FEAT-32`), AI-assisted setup-thesis digest at order placement (`BLG-FEAT-56`) |
| S2-02 | EPIC-02 | Trade-plan data-integrity foundation: enforce linkage at position entry + DB-level safeguard (`BLG-BE-91`) |
| S2-03 | EPIC-03 | Frontend design-consistency & correctness carryover from v8.5 PR-review findings (`BLG-FE-147/148/149/150/153/154/155`) |
| S2-04 | EPIC-04 | Backend & financial correctness (`BLG-BE-88/92/93`, `BLG-SEC-29`) |
| S2-05 | EPIC-05 | QA test-coverage debt closure from v8.5 PR-review findings (`BLG-QA-136/137/138/139`) |
| S2-06 | EPIC-06 | Operations & governance debt closure from v8.5 PR-review findings (`BLG-OPS-136/137/138`, `BLG-GOV-294/295/296/297/298`) |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| `BLG-FEAT-73` (SI-02 frontend build) | Gate not met (0/20 linked trade plans) | Re-check next cycle, after `BLG-BE-91` ships |
| `BLG-FEAT-74` (PO-05 Replay Mode) | Gated; VH effort exceeds single-cycle sizing | Unscheduled — needs phasing decision |
| `BLG-FEAT-44` (Arc 5 low-volume advisory) | Gate not met until 2026-08-27 (3mo post-v4.1) | Next cycle |
| `BLG-SPEC-124` (canonical "gated" DataState spec) | Ungated but deprioritised behind capacity-filling scope | Next cycle |
| Remaining 175 gated backlog items | Gate conditions not met | Per individual gate conditions |

### Supersession note

Superseded by: v8.6 ship — 2026-08-12
Changelog: docs/product/changelog.md#v8.6
Verification report: claude/cycles/2026-08-11__release-v8.6/verification_report.md
Cycle: 2026-08-11__release-v8.6
