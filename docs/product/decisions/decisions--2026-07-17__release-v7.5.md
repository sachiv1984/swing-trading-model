Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v7.5
Cycle: 2026-07-17__release-v7.5
Last Updated: 2026-07-17

## Planning Decisions — v7.5 UI Feature Expansion Continuation

### Scope decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Carry forward `BLG-FE-115/116/117/118` as v7.5 scope, all 4 classified **conditional** (not firm) | Same 4 items removed pre-seal from v7.4 by `AMD-20260717-01` (Design Gate blocked, no artefacts). Per STEP 1.4a Perennial-Return disposition, kept conditional with a materially different gate condition this time: design artefacts must be produced and Design Gate must PASS **before** Sprint Planning seals, sequenced outside sprint-execution scope (structural fix vs. the v7.4 error). | Product Owner (delegated authority, this session) | 2026-07-17 |
| No new idea intake / rebalance scope added | This session is a direct `plan release` invocation, not a scheduled rebalance — no fresh backlog candidates were surfaced or considered. | Product Owner | 2026-07-17 |

### Sequencing decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| 4 EPICs (EPIC-01–04), one per feature item, no readiness-bundle EPIC | Matches the EPIC-per-item split already ratified for these same items at v7.4 (resolving `BLG-GOV-248`: no shared data-model dependency, disjoint files/components). `BLG-SPEC-95`'s readiness scaffolding (`cmdk`/`react-day-picker` deps) already shipped in v7.4 — no repeat needed. | Head of Specs Team (release planning engine, applying the v7.4-established analysis) | 2026-07-17 |
| Design-artefact production sequenced as a precursor to `run design-gate`, not inside any EPIC's sprint-execution scope | Root-cause fix for the v7.4 `AMD-20260717-01` blocker — see RISK-01. | Head of UX & Design; Product Owner | 2026-07-17 |

### Accepted risks
| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| None | — | No escalations raised this cycle; no risk required Accepted-Risk disposition. RISK-01 is mitigated (precursor artefact production), not accepted. | — | — |

### Governance-input items addressed (not scope, not escalations)
- `BLG-GOV-249` (confirm DL-069 capacity baseline reflected in `sprint_capacity.md`) — still targets `plan sprint`, not release planning; flagged forward again in `cycle_summary.md`.
- `BLG-GOV-250` / RISK-05 §13 applicability for `BLG-FE-115`/`BLG-FE-118` — already confirmed PASS at the v7.4 Design Gate run (`claude/cycles/2026-07-17__release-v7.4/design_gate.md`); carried forward as cleared evidence, not re-litigated. A fresh Design Gate pass is still required this cycle per RISK-01 (artefact currency, not §13 applicability).

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-07-17__release-v7.5
