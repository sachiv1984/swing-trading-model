Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v8.1
Cycle: 2026-08-03__release-v8.1
Last Updated: 2026-08-03

## Planning Decisions — v8.1 User-Feature Push & Governance Debt Clearance

### Scope decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Include `BLG-FE-137` as the sole firm user-facing item this cycle | Exhaustive scan of all `BLG-FEAT-*`/`BLG-FE-*` candidates found every other item gate-blocked on a substantive (not just labelled) unmet precondition — see `run_manifest.md` | Product Owner | 2026-08-03 |
| Defer `BLG-FEAT-73`/`BLG-FEAT-74` and the Arc 5 UX-prep cluster for a 2nd consecutive cycle — Option (a), keep conditional with updated per-item gate evidence | STEP 1.4a Perennial-Return Check mandates an explicit active disposition at N≥2 consecutive returns; gates remain genuinely unmet (SI-02 data density, Arc 6 unscoped, §13 pre-clearance not run) but several (AI-adoption date gates, `BLG-FEAT-44`) are demonstrably closer to clearing than at v8.0, so Option (b) kill/remove would be premature | Product Owner | 2026-08-03 |
| Exclude `BLG-FEAT-45` from firm scope despite its 2026-08-05 gate date falling inside this cycle's likely execution window | STEP 1.4b (mandatory): within-sprint date gates may never be classified firm regardless of proximity | Product Owner | 2026-08-03 |
| Size scope to ~25.75 days midpoint, top of the confirmed ~24-28 day capacity band | Explicit user instruction this session: "Use full capacity" | Product Owner | 2026-08-03 |
| Fill remaining ~25.25 days with highest-priority ready (ungated) Governance/QA/Spec/Backend items across EPICs 02–07 | No further ungated user-facing scope exists; filling capacity with the next-most-valuable ready work (including two items — `BLG-GOV-280`, `BLG-GOV-268` — that directly address the structural cause of this cycle's thin user-value finding) is preferable to leaving capacity unused | Product Owner | 2026-08-03 |

### Sequencing decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-07 (`BLG-GOV-284`) may proceed directly to implementation with no further design step | Design was already reviewed and signed off by Head of Engineering and Head of Specs Team at `2026-07-30__release-v8.0` delivery verification (`ESC-EXEC-20260731-01`); re-litigating it here would be redundant | Product Owner | 2026-08-03 |
| EPIC-03's 7 items carry no cross-dependency and may execute in any order | Each is an independent governance-process document/checklist change with a distinct owner role | Product Owner | 2026-08-03 |

### Accepted risks
| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| None | — | No escalations were raised this cycle (capacity outcome `pass`, no gate failures requiring risk acceptance) | — | — |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-08-03__release-v8.1
