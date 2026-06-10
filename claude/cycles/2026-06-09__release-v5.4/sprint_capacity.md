Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-06-10
Cycle: 2026-06-09__release-v5.4

---

# Sprint Capacity — v5.4

## Capacity Inputs

| Field | Value |
|-------|-------|
| Sprint duration | Continuous delivery (solo dev, evenings/weekends) |
| Available FTE | 1 (solo developer) |
| Per-sprint capacity | ~12–14 working days |
| Warn threshold | Effort > 14 days |
| Capacity outcome | **PASS** |
| Source | `claude/roadmap/workforce_capacity.md` (revised 2026-05-27) |

Skill constraints: None. All v5.4 stories are document-creation or ops-review tasks; no scarce skill conflicts.

---

## Sprint 1 — Firm Scope

| EPIC | ST | Title | Effort | Owner |
|------|----|-------|--------|-------|
| EPIC-01 | ST-01 | Add v5.3 new endpoints to api_performance_baseline.md | S (~0.5 day) | Infrastructure & Operations Owner; Head of Engineering |
| EPIC-02 | ST-02 | Pre-entry panel: separate warn/fail override acknowledgement flow | S (~1 day) | Head of UX & Design; Frontend Specs & UX Documentation Owner |
| EPIC-02 | ST-03 | RFJ visual design review pre-brief | S (~0.5 day) | Frontend Specs & UX Documentation Owner; Head of UX & Design |
| EPIC-03 | ST-04 | SI-05 Phase 2 activation criteria definition | S (~0.5 day) | Product Owner; PMO Lead |

**Sprint 1 total effort: ~2.5 days**

---

## Sprint 2 — Conditional Scope

| EPIC | ST | Title | Effort | Owner | Gate |
|------|----|-------|--------|-------|------|
| EPIC-01 | ST-05 | SI-05 p99 production latency baseline review | S (~0.5 day) | Infrastructure & Operations Owner; Head of Engineering | ≥2026-07-04 (SI-05 ≥4 weeks production) |
| EPIC-03 | ST-06 | SI-05 digest actionability metric definition | S (~0.5–1 day) | Metrics Definitions & Analytics Owner; Infrastructure & Operations Owner | 2026-07-04 effectiveness review complete |
| EPIC-03 | ST-07 | SI-05 digest weekly cadence review | S (~0.5 day) | Product Owner; Director of Quality | 2026-07-04 effectiveness review complete; ST-06 complete |

**Sprint 2 total effort: ~1.5 days**

**Grand total: ~4 days — well within single-sprint capacity. No WARN triggered.**

---

## Conditional (Deferred)

| EPIC | ST | Effort | Gate condition |
|------|----|--------|----------------|
| EPIC-01 | ST-05 | S (~0.5 day) | SI-05 in production ≥4 weeks (≥2026-07-04) |
| EPIC-03 | ST-06 | S (~0.5–1 day) | 2026-07-04 SI-05 effectiveness review (BLG-GOV-113) complete |
| EPIC-03 | ST-07 | S (~0.5 day) | 2026-07-04 effectiveness review complete; ST-06 complete (metrics required as input) |

**Gate re-invocation:** If a gate condition above is met during the sprint, do not add deferred items informally. Invoke the amendment cycle (`amend cycle --cycle 2026-06-09__release-v5.4 --reason "<gate met>"`) to add the item to the sprint backlog. The amendment cycle is the only authorised path for post-seal scope addition.
