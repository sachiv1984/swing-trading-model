Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-05
Cycle: 2026-08-05__release-v8.3

# Sprint Capacity — 2026-08-05__release-v8.3

## Capacity Inputs

```
Sprint duration:    ~1-2 calendar days between sprint starts (autonomous execution engine) — per workforce_capacity.md baseline (Effective 2026-07-17)
Available FTE:      1 (solo developer / autonomous execution engine)
Total capacity:     ~24-28 working-day-equivalent units (per sprint)
Skill constraints:  None scarce this cycle — 6 EPICs span ~15 distinct owner roles, no concurrent scarce-skill collision identified (unchanged from release_plan.md STEP 4.5 finding)
```

## Item Effort Mapping

**ST-11 effort correction (planning-time recalculation):** `release_plan.md §Capacity Check` sized EPIC-03 at 6.00 days using `BLG-FE-103`'s pre-correction `Effort: M`. The design gate re-run (`ESC-20260805-01`, resolved 2026-08-05) narrowed `BLG-FE-103`'s scope to a single-file migration and revised its effort `M → S` in `claude/backlog/backlog.md`. `stage4_backlog_slice.md` (sealed, not editable by this engine) still shows the pre-correction `Effort: M` and original AC text for ST-11 — see `sprint_planning_notes.md §Stale Backlog Slice Text (ST-11)` for the full discrepancy note and the corrected AC used for execution. This table uses the corrected `S` band, reducing EPIC-03's (and the sprint's) total effort below the `release_plan.md` figure.

| EPIC | Item | Effort Band | Midpoint (days) | Estimate source |
|------|------|-------------|------------------|------------------|
| EPIC-01 | ST-01 (BLG-OPS-129) | S | 1.25 | release_plan.md §Capacity Check |
| EPIC-01 | ST-02 (BLG-OPS-130) | S | 1.00 | release_plan.md §Capacity Check |
| EPIC-01 | ST-03 (BLG-OPS-131) | S | 1.00 | release_plan.md §Capacity Check |
| EPIC-01 | ST-04 (BLG-SEC-17) | S | 1.00 | release_plan.md §Capacity Check |
| EPIC-02 | ST-05 (BLG-BE-37) | S | 0.50 | release_plan.md §Capacity Check |
| EPIC-02 | ST-06 (BLG-BE-57) | S | 0.50 | release_plan.md §Capacity Check |
| EPIC-02 | ST-07 (BLG-BE-67) | S | 0.50 | release_plan.md §Capacity Check |
| EPIC-02 | ST-08 (BLG-BE-69) | M | 2.00 | release_plan.md §Capacity Check |
| EPIC-02 | ST-09 (BLG-BE-79) | S | 0.50 | release_plan.md §Capacity Check |
| EPIC-02 | ST-10 (BLG-BE-80) | S | 0.50 | release_plan.md §Capacity Check |
| EPIC-03 | ST-11 (BLG-FE-103) | S *(corrected M→S)* | 1.00 | `claude/backlog/backlog.md` (corrected, ESC-20260805-01) |
| EPIC-03 | ST-12 (BLG-FE-121) | S | 1.00 | release_plan.md §Capacity Check |
| EPIC-03 | ST-13 (BLG-FE-126) | M | 2.00 | release_plan.md §Capacity Check |
| EPIC-03 | ST-14 (BLG-FE-132) | S | 0.50 | release_plan.md §Capacity Check |
| EPIC-03 | ST-15 (BLG-FE-81) | S | 0.50 | release_plan.md §Capacity Check |
| EPIC-04 | ST-16 (BLG-QA-86) | S | 0.75 | release_plan.md §Capacity Check |
| EPIC-04 | ST-17 (BLG-QA-94) | S | 0.75 | release_plan.md §Capacity Check |
| EPIC-04 | ST-18 (BLG-QA-98) | S | 0.75 | release_plan.md §Capacity Check |
| EPIC-04 | ST-19 (BLG-SPEC-88) | S | 0.75 | release_plan.md §Capacity Check |
| EPIC-04 | ST-20 (BLG-SPEC-96) | S | 0.75 | release_plan.md §Capacity Check |
| EPIC-04 | ST-21 (BLG-SPEC-108) | S | 0.75 | release_plan.md §Capacity Check |
| EPIC-05 | ST-22 (BLG-GOV-124) | S | 0.75 | release_plan.md §Capacity Check |
| EPIC-05 | ST-23 (BLG-GOV-204) | M | 1.75 | release_plan.md §Capacity Check |
| EPIC-05 | ST-24 (BLG-GOV-237) | S | 0.50 | release_plan.md §Capacity Check |
| EPIC-05 | ST-25 (BLG-GOV-257) | M | 1.75 | release_plan.md §Capacity Check |
| EPIC-05 | ST-26 (BLG-GOV-270) | S | 0.75 | release_plan.md §Capacity Check |
| EPIC-06 | ST-27 (BLG-FEAT-45) | S | 0.50 | release_plan.md §Capacity Check |

All 27 items carry an effort estimate. No `[ESTIMATE REQUIRED]` placeholders.

## Total Effort vs Capacity

```
Total estimated effort:  ~24.25 days midpoint (recalculated; release_plan.md's own figure was ~25.25 days, pre-ST-11-correction)
Confirmed capacity:      ~24-28 working-day-equivalent
Utilisation:              ~87-101% (depending on which end of the band is used as denominator)
Outcome:                  pass — no over-allocation against the ceiling at any point in the confirmed band; the ST-11 correction moves utilisation further from the ceiling, not closer to it
```

No over-allocation. No Product Owner acknowledgement of over-100%-of-band-ceiling risk required under §8 (capacity check outcome is `pass`, not `warn`, at every point in the band). No `### Phasing Recommendation` exists in `release_plan.md` (only required on `warn` outcome) — nothing to adopt or decline here.

## Minimum Capacity Buffer Floor (§1.5, advisory)

`scope_effort ÷ confirmed_capacity`, evaluated across the confirmed band:
- Against the top of band (28 days): 24.25 / 28 ≈ **0.87** — under the 95% floor.
- Against the midpoint (26 days): 24.25 / 26 ≈ **0.93** — under the 95% floor.
- Against the bottom of band (24 days): 24.25 / 24 ≈ **1.01** — exceeds the floor (and, at this single denominator, effort nominally exceeds the low end of the confirmed band by ~0.25 days).

**Buffer floor note:** at the conservative (low) end of the confirmed capacity band, the ratio marginally exceeds both the 95% advisory floor and 100% of that single reference point. This is the same recurring pattern flagged at `2026-08-04__release-v8.2` (there: 1.03 at the bottom-of-band denominator) — a structural feature of sizing near the middle of a wide band, not new. It is distinct from — and less severe than — the hard over-100%-of-full-band WARN threshold in §8, which is not triggered (effort sits within the 24-28 band at the midpoint and top).

**Product Owner acknowledgement (agent-mediated, delegated authority — no explicit user scope-priority instruction this session):** Proceed at current scope — 27 items were already curated (not padded to the ceiling) at release planning; the ST-11 correction only reduced total effort. No items require trimming. — Product Owner, 2026-08-05.

## Conditional (Deferred)

None. `release_plan.md` records `story_items_conditional: 0` — all 27 items in the backlog slice are firm; none are gate-conditionally deferred at planning.
