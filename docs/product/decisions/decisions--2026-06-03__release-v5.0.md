**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Published
**Release:** v5.0
**Cycle:** 2026-06-03__release-v5.0
**Last Updated:** 2026-06-03
**Published:** 2026-06-03

---

# Decisions Record — v5.0

## Scope Decisions

| Decision | Rationale | Authority |
|----------|-----------|-----------|
| BLG-GOV-79/80/81/82/83 all as firm (not conditional) | All are AUD-2026-06-02 open items with explicit P2/P3 priority; governance debt from identified gaps must not be deferred a second cycle | Product Owner + Head of Specs Team |
| BLG-FEAT-43 (allocation_insufficient) and BLG-BE-25 (regime gate fix) as firm | Both slipped v4.9 with explicit v5.0 Provisional-Target; product correctness issues erode user trust; must not defer further | Product Owner |
| BLG-OPS-52 (Anthropic SDK staging verification) as firm | Staging-only AC deferred from v4.9 per CLAUDE.md §2; must be cleared before next cycle touching AI endpoints | Infrastructure & Operations Owner |
| BLG-GOV-67 (SI-05 Phase 1 impl) as conditional only | Gate clears 2026-06-21; sprint 1 would complete before gate date; conditional sprint 2 story is the correct placement | Product Owner |
| BLG-BE-26 as firm (assessment item) | Assessment scope is bounded (0.5–1 day); unconditional since assessment can run independently of gate | Product Owner |

## Sequencing Decisions

| Decision | Rationale |
|----------|-----------|
| Merge order: EPIC-01 → EPIC-02 → EPIC-03 → EPIC-04 | EPIC-01/02 are pure governance patches; EPIC-02 depends on EPIC-01's prompt_change_log.md append landing first. EPIC-03 is independent product code. EPIC-04 is spec/document output only |
| ST-09 before ST-10 within EPIC-04 | BLG-FE-60 (notification channel decision) must complete before BLG-GOV-86 (Telegram format spec) can be authored; format spec depends on channel decision |
| Sprint 2 gated on 2026-06-21 | BLG-GOV-67 gate is date-based; if gate clears, sprint 2 opens; otherwise EPIC-04 closes with ST-09–ST-13 |

## Accepted Risks

None — no Accepted Risk escalations raised in this planning cycle.

## Supersession Note

*(To be completed at Post-Ship Closure.)*
