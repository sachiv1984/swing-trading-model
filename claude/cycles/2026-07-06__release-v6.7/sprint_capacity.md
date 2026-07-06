Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-07-06
Cycle: 2026-07-06__release-v6.7

---

# Sprint Capacity — 2026-07-06__release-v6.7

## 1.1 Capacity Inputs

```
Sprint duration:    ~10-12 working days (single sprint; solo developer, evenings/weekends)
Available FTE:      1 (solo operator — Backend Engineering, Frontend/Base44, QA execution, Spec authoring, Governance all performed by same operator across roles)
Total capacity:     ~12-14 working days (per workforce_capacity.md Sprint Capacity Baseline, effective 2026-05-27)
Skill constraints:  None scarce for this scope — EPIC-01 requires Head of UX & Design + Head of Engineering (frontend/contrast); EPIC-02 requires Head of Specs Team (governance prompt edits). No overlapping scarce-skill contention between the two EPICs.
Warn threshold:     Effort > 14 days
```

## 1.2 Item Effort Mapping

| EPIC | Story | Effort estimate (source: release_plan.md Execution Plan / Capacity Check) |
|------|-------|------|
| EPIC-01 | ST-01 (BLG-FE-87) | L (~2–3 days, mid-point 2.5) |
| EPIC-01 | ST-02 (BLG-FE-88) | L (~3–4 days, mid-point 3.5) |
| EPIC-01 | ST-03 (BLG-FE-89) | M (~1–2 days, mid-point 1.5) |
| EPIC-02 | ST-04 (BLG-GOV-167) | M (~1–2 days, mid-point 1.5) |
| EPIC-02 | ST-05 (BLG-GOV-168) | M (~1–2 days, mid-point 1.5) |
| EPIC-02 | ST-06 (BLG-GOV-169) | XS (<1 hour, mid-point 0.1) |
| EPIC-02 | ST-07 (BLG-GOV-170) | XS (<1 hour, mid-point 0.1) |

No item is missing an effort estimate. No `[ESTIMATE REQUIRED]` placeholders.

## 1.3 Total Effort vs Capacity

```
EPIC-01 total:  ~7.5 days
EPIC-02 total:  ~3.2 days
Grand total:    ~10.7 days
Capacity:       ~12-14 days
Outcome:        PASS — within confirmed capacity, no over-allocation. Matches release_plan.md Capacity Check outcome (PASS, not WARN). capacity_warn_acknowledged = false (not applicable — no WARN was issued).
```

Both EPICs fit within a single sprint. EPIC-02 (3.2 days, no dependency) runs fully in parallel with EPIC-01's sequential chain (ST-01 → ST-02 → ST-03), as anticipated in release_plan.md's Capacity Check advisory note. No scope split across two sprints is required.

## 1.4 Gate-Conditional Deferred Items

None. All 7 items from the authoritative backlog slice (`stage4_backlog_slice.md`) are firm scope, ungated, and included in this sprint. No `## Conditional (Deferred)` section required.
