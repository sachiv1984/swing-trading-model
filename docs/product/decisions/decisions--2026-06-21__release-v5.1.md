**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v5.1
**Cycle:** 2026-06-21__release-v5.1
**Last Updated:** 2026-06-21
**Published:** 2026-06-21

---

# Decisions Record — v5.1: SI-05 Phase 1 & Governance Debt

## Scope Decisions

| Decision | Rationale | Authority |
|----------|-----------|-----------|
| Include BLG-GOV-67 (SI-05 Phase 1) as firm scope | Gate clears 2026-06-21 (SI-01+SI-03 live ≥ 30 days); format spec (BLG-GOV-86) complete | Product Owner |
| Include LL-RP-v5.0-D-2 (delivery_verification_prompt.md §-1.3 Tier 2) | Carry-forward from v5.0 lessons_learnt_closure.md D-2; recurrent Tier 2 advisory prevents | Head of Specs Team |
| Include BLG-FE-61 as firm (not deferred backlog) | Carry-forward from v5.0 CF-1; 3rd consecutive sprint recurrence warrants firm assignment | PMO Lead |
| Defer BLG-FE-43 (SI-05 frontend spec) | SI-05 Phase 1 is Telegram-only; in-app spec relevant for Phase 2 only | Product Owner |
| Defer BLG-FE-41, BLG-FE-40 | Gates clear on release date; eligible v5.2+ | Product Owner |

## Sequencing Decisions

| Decision | Rationale |
|----------|-----------|
| EPIC-01 merges after EPIC-02 | BLG-SPEC-45 scope verification (ST-02) should confirm SI-05 format scope before ST-01 implementation begins |
| EPIC-02 and EPIC-03 merge in parallel | Both are independent of each other; no shared-file conflicts expected |
| 1-sprint delivery | 6 stories, ~4.5 days estimated — well within standard solo-dev sprint capacity |

## Design Gate Assessment

Design gate: **NOT REQUIRED**
Authority: Head of UX & Design + Product Owner
Reason: All 6 scope items are: backend service/Telegram delivery, governance patch, Playwright test, documentation/spot-check — no new UI or UX components introduced. Confirmed by STEP 1.3 design dependency scan (0 items flagged).

## §-1.2 Roadmap Section Advisory Resolution

v5.1 was not a formal roadmap section at invocation time. The roadmap metadata recorded STEP 8.1 Option(b) PO decision: "plan release v5.1 is next step; SI-05 Phase 1 gate clears 2026-06-21." This constitutes explicit PO authorization per roadmap_prompt.md v6.8 STEP 8.1 — a documented PO choice to defer section creation, knowing release planning would immediately follow. The release planning engine proceeded under advisory (not halt) and added the v5.1 section to the roadmap at STEP 5 as the authorizing annotation.

## Accepted Risks

None. All three RISK-IDs have mitigations in place; no escalations were raised.

## Supersession Note

*(To be completed at Post-Ship Closure.)*
