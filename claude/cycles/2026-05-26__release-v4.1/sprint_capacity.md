Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-05-27
Cycle: 2026-05-26__release-v4.1

---

# Sprint Capacity — 2026-05-26__release-v4.1

## Capacity Inputs

```
Sprint duration:    2 sprints (~8–10 working days available per sprint, evenings/weekends)
Available FTE:      1 (solo developer)
Total capacity:     ~16–20 days across both sprints
Skill constraints:  None — all EPICs within solo-developer skill set
```

Sources: `release_plan.md ## Capacity Check`; `workforce_capacity.md`

---

## Item Effort Mapping

### Sprint 1

| EPIC | Story | Title | Effort estimate |
|------|-------|-------|-----------------|
| EPIC-01 | ST-01 | execution_prompt.md merge-gate hard gate | S (~1 day) |
| EPIC-01 | ST-02 | sprint_planning_prompt.md + sprint_backlog.md staging-only AC | S (~1 day) |
| EPIC-01 | ST-03 | delivery_verification_prompt.md pr_number null guard | S (~1 day) |
| EPIC-02 | ST-04 | SI-03 Red Flag Journal API contract | S (~1 day) |
| EPIC-02 | ST-05 | SI-01 Pre-Entry Validation API contract | S (~1 day) |
| EPIC-02 | ST-06 | Arc 5 analytics endpoint API contract | S (~1 day) |
| **Sprint 1 total** | | | **~6 days** |

Sprint 1 vs capacity (~8–10 days): **Within capacity ✅**

### Sprint 2

| EPIC | Story | Title | Effort estimate |
|------|-------|-------|-----------------|
| EPIC-04 | ST-12 | SI-02 data model gap analysis | M (~2 days) |
| EPIC-04 | ST-13 | SI-02 pre-planning: §13 criteria + data audit + query performance | S (~1.5 days) |
| EPIC-04 | ST-14 | Security review + governance patches | S (~1.5 days) |
| EPIC-04 | ST-15 | Operational reviews: API perf baseline + Gemini usage + P&L attribution | S (~1.5 days) |
| EPIC-03 | ST-07 | Gemini thesis endpoint API contract | S (~1 day) |
| EPIC-03 | ST-08 | Arc 5 compliance metrics P&L integration | M (~3 days) |
| EPIC-03 | ST-09 | Gemini API daily cost threshold alert | M (~2–3 days) |
| EPIC-03 | ST-10 | Frontend: Research view signal_type + Arc5ComplianceSection spec | S (~1.5 days) |
| EPIC-03 | ST-11 | Staging Verification Bundle | S (~2 days) |
| **Sprint 2 total** | | | **~17 days** |

Sprint 2 vs capacity (~8–10 days): **Over-allocated ⚠ (~7–9 days over)**

**Grand total: ~23 days vs ~16–20 days available**

---

## Total Effort vs Capacity

| Sprint | Estimated | Available | Status |
|--------|-----------|-----------|--------|
| Sprint 1 | ~6 days | ~8–10 days | ✅ Within capacity |
| Sprint 2 | ~17 days | ~8–10 days | ⚠ Over-allocated |
| **Total** | **~23 days** | **~16–20 days** | ⚠ Over-allocated |

---

## Capacity WARN Acknowledgement

> ⚠ **Capacity WARN (inherited from release planning — `capacity_feasible: "warn"`):** Sprint 2 estimated effort (~17 days) exceeds solo-developer sprint capacity (~8–10 days). The release plan recommends EPIC-04 (reviews/docs, ~6.5 days) can run in parallel with EPIC-03 implementation, reducing effective sequenced load. If capacity is constrained mid-Sprint 2, lowest-risk deferrals to v4.2 are: ST-11 (staging bundle, S effort — verification-only) and/or ST-09 (Gemini cost alerting, M effort — no blocking downstream dependency).
>
> **Product Owner acknowledgement:** Product Owner has explicitly acknowledged the over-capacity risk and accepts inclusion of all 15 stories, noting that EPIC-04 parallelisation with EPIC-03 and discretionary deferral of ST-09/ST-11 is available mid-sprint without a formal amendment. Recorded: 2026-05-27.

---

## Conditional (Deferred)

No items are conditionally deferred at planning. All 15 stories from `stage4_backlog_slice.md` are included in the sealed sprint backlog.

> **Gate re-invocation:** If a gate condition is met during the sprint requiring scope addition (e.g. PT-04 trade count gate clears), do not add items informally. Invoke the amendment cycle (`amend cycle --cycle 2026-05-26__release-v4.1 --reason "<gate met>"`) to add the item to the sprint backlog. The amendment cycle is the only authorised path for post-seal scope addition.
