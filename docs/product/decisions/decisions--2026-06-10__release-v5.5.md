**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Published
**Last Updated:** 2026-06-10
**Cycle:** 2026-06-10__release-v5.5

---

# Decisions Record — v5.5

**Release:** v5.5
**Cycle:** 2026-06-10__release-v5.5
**Last Updated:** 2026-06-10

---

## Scope Decisions

| Decision | Rationale | Authority |
|----------|-----------|-----------|
| All three v5.4 LL carry-forwards (GOV-116/117/118) included in Sprint 1 | Second-occurrence risk if deferred again (LL-P3-03 was already a second recurrence at v5.4) | Product Owner |
| BLG-BE-34 (gate-monitoring view) paired with BLG-GOV-120 (trade density tracker) in EPIC-02 | Backend view enables frontend display; natural dependency | Head of Backend Engineering |
| BLG-OPS-13 (24 endpoint baseline) included despite M effort | Long-outstanding (v2.9 post-ship 2026-04-24 original source); deferring further degrades ops visibility | Infrastructure & Operations Owner |
| BLG-OPS-54 included as distinct story from OPS-61 | Different targets: OPS-54 adds the digest endpoint with live measurement; OPS-61 adds v5.1–v5.4 routes | Infrastructure & Operations Owner |
| BLG-FE-64 in Sprint 2 only (not Sprint 1) | Gate (2026-06-21) does not clear until after Sprint 1 is likely to be underway; safe to start only after gate date confirmed | Product Owner |
| BLG-GOV-115 included despite gate-conditional classification | Gate (2026-07-04 review) is the trigger to produce the actionability metrics — this is the natural deliverable from that review | Product Owner |
| GOV-119 / GOV-121 / GOV-122 deferred | Hard gate conditions not met; would not deliver value without underlying data | Product Owner |

---

## Sequencing Decisions

| Decision | Rationale |
|----------|-----------|
| Sprint 1 first; Sprint 2 post-2026-07-04 | Sprint 2 gate items require 2026-07-04 SI-05 review; no benefit to starting Sprint 2 earlier |
| EPIC-02: S2-04 before S2-05 | Backend `get_gate_metrics()` view must exist before frontend display can query it |
| EPIC-03: S2-06 (OPS-13) is separable | Can shift to Sprint 2 if Sprint 1 capacity is tight without blocking gated items |
| EPIC-01 stories independent | GOV-116/117/118 modify different prompts; can be parallelised in sprint |

---

## Accepted Risks

None. All risks have active mitigations; no escalations raised.

---

## Supersession Note

*(Completed at Post-Ship Closure)*
