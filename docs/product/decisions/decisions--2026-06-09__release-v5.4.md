**Owner:** Head of Specs Team
**Class:** Planning Record (Class 3)
**Status:** Superseded
**Version:** 1.0
**Release:** v5.4
**Cycle:** 2026-06-09__release-v5.4
**Last Updated:** 2026-06-10
**Supersession note:** Superseded by: v5.4 ship — 2026-06-10
Changelog: docs/product/changelog.md#v5.4
Verification report: claude/cycles/2026-06-09__release-v5.4/verification_report.md
Cycle: 2026-06-09__release-v5.4

---

# Decisions Record — v5.4

## Release

v5.4 — Ops Monitoring, UX Debt Clearance & Governance Patches

## Scope Decisions

| Decision | Authority | Rationale |
|----------|-----------|-----------|
| BLG-GOV-91 deferred — SI-04 security review excluded | Product Owner | Gate requires SI-04 sprint planning to be imminent; SI-04 is in Later horizon; no timeline trigger |
| BLG-FE-68/70 deferred — compliance score sparkline/widget excluded | Product Owner | Gate requires BLG-FE-45 (expandability review) complete first; BLG-FE-45 not scheduled |
| BLG-FE-69/71 deferred — SI-05 in-app digest excluded | Product Owner | Gate requires BLG-GOV-92 Phase 2 channel decision first; BLG-GOV-92 is in-sprint (ST-04); deferred to v5.5 after ST-04 produces the decision |
| BLG-FE-64 included as firm Sprint 1 story | Product Owner | Gate (2026-06-21) clears 12 days from release planning; execution timing ensures gate will be met before story executes |
| S2-05/S2-06/S2-07 conditional Sprint 2 | PMO Lead | All three gated to 2026-07-04 effectiveness review; included as conditional scope — Sprint 2 proceeds only if gate clears on schedule |
| DP-2 excluded | Head of Specs Team | Already applied in roadmap_prompt.md v6.9 (2026-06-09__scheduled rebalance); no story required |

## Sequencing Decisions

| Decision | Authority | Rationale |
|----------|-----------|-----------|
| EPIC-03 ST-04 in Sprint 1 | PMO Lead | BLG-GOV-92 has no gate and enables BLG-FE-69/71 gate assessment; earlier is better |
| Sprint 2 gate-conditional on 2026-07-04 | PMO Lead | All Sprint 2 stories (ST-05, ST-06, ST-07) depend on SI-05 effectiveness review completing; PO confirms go/no-go before Sprint 2 seals |
| Merge order: EPIC-01 → EPIC-02 → EPIC-03 | PMO Lead | EPICs independent; simplest to fewest shared files first; EPIC-03 governance docs last |

## Accepted Risks

None — no Accepted Risk escalations raised in this cycle.

## Supersession Note

(To be completed at Post-Ship Closure)
