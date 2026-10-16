**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Version:** 1.0
**Last Updated:** 2026-10-16 (created by a Head of Specs Team action-now patch, user-directed, at roadmap rebalance `2026-10-16__scheduled` STEP -1.5 to clear an OVERDUE deferred patch, BLG-GOV-374; backfilled v9.3–v9.12)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Ready-Pool History

This file holds one row per release for the ready (ungated) backlog pool at Release Planning. Release Planning §1.4c appends the row when it records its selection (`release_planning_prompt.md`). `roadmap_prompt.md` STEP 7.3 reads this file for the gap trend and the runway reading. It does not re-read release run manifests unless a row is missing. `docs/specs/metrics_definitions.md` Appendix F ("Ready-Pool Runway Forecast") defines the runway metric, and this file is its data source from v9.8 onward.

## Column definitions

- **Pool / Selected / Leftover:** items and estimated days, as recorded on the release `run_manifest.md` Scope Construction `**Result:**` line. Leftover days are the recorded figure. Where the manifest states a calibrated figure, that figure is used here, so leftover can differ slightly from pool minus selected.
- **Ceiling:** the upper bound of the confirmed capacity band, in days.
- **Gap:** pool days minus ceiling (STEP 7.3 step 2).
- **Δ leftover:** leftover days minus the prior release's leftover days.
- **Rolling Δ:** the mean of up to the last 3 Δ leftover values (Appendix F).
- **Runway:** leftover days ÷ |Rolling Δ| when Rolling Δ < 0; otherwise "N/A — pool growing".

## History

| Release | Release cycle | Pool (items / days) | Selected (items / days) | Leftover (items / days) | Ceiling | Gap | Δ leftover | Rolling Δ | Runway | Source |
|---------|---------------|---------------------|-------------------------|-------------------------|---------|-----|------------|-----------|--------|--------|
| v9.3 | `2026-09-09__release-v9.3` | 61 / ~41.0 | 27 / 27.50 | 34 / 13.10 | 28 | 13.00 | — | N/A | N/A — insufficient trend data | Appendix F backfill; `roadmap_prompt_appendix.md` §STEP 7.3 (no `**Result:**` line in this manifest) |
| v9.4 | `2026-09-14__release-v9.4` | 74 / ~65.05 | 28 / 27.55 | 46 / 37.50 | 28 | 37.05 | +24.40 | +24.40 | N/A — pool growing | run_manifest.md "Ready pool" line; Appendix F |
| v9.5 | `2026-09-15__release-v9.5` | 62 / 44.79 | 43 / 27.99 | 19 / 16.80 | 28 | 16.79 | −20.70 | +1.85 | N/A — pool growing | run_manifest.md `**Result:**` (Appendix F shows ~43.79 pool days; 27.99 + 16.80 = 44.79) |
| v9.6 | `2026-09-21__release-v9.6` | 76 / 61.75 | 32 / 28.00 | 44 / 33.75 | 28 | 33.75 | +16.95 | +6.88 | N/A — pool growing | run_manifest.md `**Result:**` |
| v9.7 | `2026-09-23__release-v9.7` | 68 / 61.35 | 29 / 28.00 | 39 / 21.35 | 28 | 33.35 | −12.40 | −5.38 | ≈4.0 cycles | run_manifest.md `**Result:**` |
| v9.8 | `2026-09-28__release-v9.8` | 65 / 46.7 | 39 / 28.00 | 26 / 18.7 | 28 | 18.70 | −2.65 | +0.63 | N/A — pool growing | run_manifest.md `**Result:**` |
| v9.9 | `2026-09-30__release-v9.9` | 53 / 36.20 | 35 / 27.85 | 18 / 8.35 | 28 | 8.20 | −10.35 | −8.47 | ≈1.0 cycle | run_manifest.md `**Result:**` |
| v9.10 | `2026-10-06__release-v9.10` | 82 / 61.80 | 21 / 27.90 | 61 / ~34.25 | 28 | 33.80 | +25.90 | +4.30 | N/A — pool growing | run_manifest.md `**Result:**` (selected days include +0.35d calibration) |
| v9.11 | `2026-10-08__release-v9.11` | 97 / 61.67 | 43 / 27.975 | 54 / ~34.55 | 28 | 33.67 | +0.30 | +5.28 | N/A — pool growing | run_manifest.md `**Result:**` (raw days) |
| v9.12 | `2026-10-12__release-v9.12` | 101 / 54.70 | 48 / 27.95 | 53 / 26.75 | 28 | 26.70 | −7.80 | +6.13 | N/A — pool growing | run_manifest.md `**Result:**` (calibrated) |

**Backfill note:** the v9.8–v9.12 Δ, Rolling Δ and Runway values were computed when this file was created, from the recorded figures only, using the Appendix F method with no look-ahead. The v9.3–v9.7 values match Appendix F's backfill table.
