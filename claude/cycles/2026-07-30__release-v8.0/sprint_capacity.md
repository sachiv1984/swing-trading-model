Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-30
Cycle: 2026-07-30__release-v8.0

# Sprint Capacity — 2026-07-30__release-v8.0

## Capacity Inputs

```
Sprint duration:    ~1-2 calendar days between sprint starts (autonomous execution engine cadence, Effective 2026-07-17 per workforce_capacity.md)
Available FTE:      1 (solo developer / autonomous execution engine)
Total capacity:     ~24-28 working-day-equivalent units
Skill constraints:  None scarce this cycle — 6 EPICs span 8 distinct owner roles, no concurrent scarce-skill collision identified (per release_plan.md Capacity Check)
```

## Item Effort Mapping

| EPIC | Item | Effort Band | Midpoint (days) | Owner |
|------|------|-------------|------------------|-------|
| EPIC-01 | ST-01 (BLG-SPEC-78) | M | 2.0 | Data Model & Domain Schema Owner |
| EPIC-01 | ST-02 (BLG-SPEC-79) | S | 1.0 | Financial Reporting & Records Owner |
| EPIC-01 | ST-03 (BLG-SPEC-107) | S | 1.0 | Financial Reporting & Records Owner |
| EPIC-02 | ST-04 (BLG-SEC-25) | S | 1.0 | Head of Engineering |
| EPIC-02 | ST-05 (BLG-SEC-23) | S | 1.0 | Cybersecurity & Trust Lead |
| EPIC-02 | ST-06 (BLG-FE-135) | S | 1.0 | Head of UX & Design |
| EPIC-02 | ST-07 (BLG-FE-136) | S | 1.0 | Head of UX & Design |
| EPIC-02 | ST-08 (BLG-SEC-24) | S | 1.0 | Cybersecurity & Trust Lead |
| EPIC-02 | ST-09 (BLG-SEC-26) | S | 1.0 | Cybersecurity & Trust Lead |
| EPIC-03 | ST-10 (BLG-QA-97) | S | 1.0 | QA Lead |
| EPIC-03 | ST-11 (BLG-QA-120) | M | 2.0 | QA & Testing Owner |
| EPIC-03 | ST-12 (BLG-QA-121) | M | 2.0 | QA & Testing Owner |
| EPIC-04 | ST-13 (BLG-OPS-114) | M | 2.0 | Infrastructure & Operations Owner |
| EPIC-04 | ST-14 (BLG-OPS-115) | XS | 0.25 | Infrastructure & Operations Owner |
| EPIC-04 | ST-15 (BLG-OPS-109) | S | 1.0 | Infrastructure & Operations Owner |
| EPIC-04 | ST-16 (BLG-OPS-124) | S | 1.0 | FinOps & Resource Architect |
| EPIC-04 | ST-17 (BLG-OPS-126) | S | 1.0 | Infrastructure & Operations Owner |
| EPIC-05 | ST-18 (BLG-FE-124) | M | 2.0 | Base44 Frontend Prompt Owner |
| EPIC-06 | ST-19 (BLG-GOV-263) | L (~3-5 days) | 4.0 | Head of Engineering |

All 19 items carry an effort estimate (inherited from `release_plan.md ## Capacity Check`). No `[ESTIMATE REQUIRED]` placeholders.

## Total Effort vs Capacity

```
Total estimated effort:  ~26.25 days midpoint
Confirmed capacity:      ~24-28 working-day-equivalent
Utilisation:             ~94-109% (depending on which end of the band is used as denominator)
Outcome:                 pass — no over-allocation against the confirmed ceiling
```

Capacity check outcome inherited from `release_plan.md ## Capacity Check` = `pass`. No WARN acknowledgement required; no Phasing Recommendation subsection present or needed.

## Conditional (Deferred)

None. All 19 ST items in the authoritative backlog slice (`stage4_backlog_slice.md`) enter this sprint's scope — no items are held back under a `deferred_at_planning` / `gate_condition` status. (Items excluded at Release Planning — `BLG-OPS-48`, `BLG-FEAT-73/74`, the Arc 5 UX cluster, and the ~145-item P2/P3 pool — were never part of the authoritative backlog slice and therefore are release-planning deferrals, not sprint-planning deferrals; they carry no `execution_state.json` entry from this engine.)

**Gate re-invocation:** If a gate condition above is met during the sprint, do not add deferred items informally. Invoke the amendment cycle (`amend cycle --cycle 2026-07-30__release-v8.0 --reason "<gate met>"`) to add the item to the sprint backlog. The amendment cycle is the only authorised path for post-seal scope addition.
