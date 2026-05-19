**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Published
**Version:** 1.0
**Release:** v3.8
**Cycle:** 2026-05-19__release-v3.8
**Last Updated:** 2026-05-19
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Decisions Record — v3.8

---

## Scope Decisions

| Decision | Rationale | Authority |
|----------|-----------|-----------|
| Include SI-01 (Pre-Entry Rule Validation Gate) as primary arc feature for v3.8 | Highest-priority unshipped item by scored_initiatives.md weighted score (Strat=5, Risk=5, Rev=5, SPS=4). Pull-forward candidate for Arc 5 — high standalone value. §13 review required via gate story in Sprint 1. | Product Owner |
| Defer SI-03 (Red Flag Journal) to v3.9 | SI-03 depends on SI-01 being operational (it logs SI-01 override events). Attempting both SI-01 and SI-03 in same release risks SI-01 delivery quality. SI-01 must be live and validated before SI-03 is meaningful. | Product Owner |
| Include BLG-FEAT-22, BLG-FEAT-23, BLG-FEAT-24, BLG-FE-36 as EPIC-03/04 scope | All carry Provisional-Target: v3.8; all authored by user in 2026-05-19 session. Collectively enhance the trade plan creation workflow — high daily-use value. Form a natural dependency chain: setup type (S2-03) → news panel (S2-03) → AI thesis (S2-03). | Product Owner |
| PT-04 carried as conditional EPIC-02 scope | Two consecutive conditional defers (v3.6, v3.7). Product Owner decision due 2026-05-22 — park as "pending gate" or carry conditional again. Gate condition (20+ closed trades) must be confirmed before sprint planning seals. | Product Owner |
| Defer PO-02/03/04/05 and SI-02/04/05 | Data density gates not met. SPS=1 across all items. No value in planning until respective gates clear. | Product Owner |

---

## Sequencing Decisions

| Decision | Rationale | Authority |
|----------|-----------|-----------|
| Merge order: EPIC-04 → EPIC-03 → EPIC-01 → EPIC-02 | EPIC-04 (governance/platform) first — fewest shared files; lowest risk. EPIC-03 (trade plan enhancements) second — self-contained. EPIC-01 (SI-01 — Arc 5) third — shares trade plan form with EPIC-03; merge after EPIC-03 to avoid conflicts. EPIC-02 (PT-04 conditional) last — independent if included. | PMO Lead |
| EPIC-01 uses §13 gate pattern | SI-01 touches pre-entry validation — must confirm §13 compliance before implementing. Delegated_decision gate story (ST-01) in Sprint 1; implementation (ST-02, ST-03) in Sprint 2 after PASS. Established pattern from v3.5 IT-06. | Strategy Rules & System Intent Owner |
| EPIC-02 conditional on PO gate confirmation before sprint planning | PT-04 gate (20+ closed trades) not confirmed. If PO confirms gate met at sprint planning: EPIC-02 scope added. If not confirmed: EPIC-02 removed and sprint sealed without it. Sprint planning must record the gate decision explicitly. | Product Owner |

---

## Accepted Risks

None. All risks addressed via scope decisions or sprint sequencing.

---

## Supersession note

*(To be completed at Post-Ship Closure — Step 4)*
