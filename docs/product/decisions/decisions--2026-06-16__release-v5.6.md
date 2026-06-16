**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Superseded
**Release:** v5.6
**Cycle:** 2026-06-16__release-v5.6
**Last Updated:** 2026-06-16
**Supersession note:** Superseded by v5.6 ship — 2026-06-16. Changelog: docs/product/changelog.md#v5.6. Cycle: 2026-06-16__release-v5.6
**Last Updated:** 2026-06-16

---

# Decisions Record — v5.6

## Scope Decisions

| Decision | Rationale | Authority |
|----------|-----------|-----------|
| Include BLG-OPS-63, BLG-OPS-64 beyond roadmap candidate list | Product Owner directive to "clear as much backlog as possible"; both are S-effort P3 latency investigations from the same v5.5 baseline run; high efficiency gain | Product Owner |
| Classify BLG-FE-64 as conditional (not firm Sprint 2) | Applying LL-P3-03-v55 lesson: item deferred twice due to gate; treat as conditional at planning; gate clears 2026-06-21 — sprint planning picks it up if/when gate clears | PMO Lead |
| No governance prompt patches as separate EPIC | LL-RP-02 already applied at rebalance 2026-06-16 (roadmap_prompt.md v7.0→v7.1); LL-P3-03-v55/LL-P4-01-v55 applied as guidance at this planning; no further prompt edits required | Head of Specs Team |
| No design gate required | 0 items flagged for design dependency; all items are performance fixes, UX copy changes, governance docs, QA docs, or pre-brief docs | Head of UX & Design + Product Owner |

## Sequencing Decisions

| Decision | Rationale |
|----------|-----------|
| EPIC-02 (performance) sequenced last (Sprint 2 if needed) | S2-03 (research caching) is the M-effort item; investigations (S2-04/05/06) should run first; Sprint 1 priority is P1 gate check (S2-07) and P2 UX/QA items |
| EPIC-03 first in Sprint 1 | Contains P1 item BLG-GOV-106; PT-04 gate re-verification should not be deferred further |

## Accepted Risks

None. No escalations raised.

## OA-1 Resolution (v5.5 carry-forward)

OA-1 (LL-RP-02: roadmap_prompt.md candidate list pruning) — **Resolved** at rebalance 2026-06-16__scheduled. roadmap_prompt.md updated v7.0→v7.1 with STEP 8.0.5 strengthened to mandatory prune before STEP 8.1. No further action required.
