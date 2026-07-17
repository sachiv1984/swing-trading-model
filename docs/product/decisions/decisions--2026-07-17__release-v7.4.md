Owner: Product Owner
Class: Planning Document (Class 4)
Status: Superseded
Release: v7.4
Cycle: 2026-07-17__release-v7.4
Last Updated: 2026-07-17

## Planning Decisions — v7.4 UI Feature Expansion

### Scope decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Firm scope = 5 items (`BLG-SPEC-95`, `BLG-FE-115/116/117/118`), no additions/deferrals from roadmap anchor | All 5 named in roadmap `2026-07-17__scheduled` STEP 8.1 anchor scope; PO pre-emptively committed all 4 FE items (exceeding the ≥2-item Skill-Silo pull-forward guidance) | Product Owner (via roadmap rebalance) | 2026-07-17 |
| `BLG-FE-120` (shared toast primitive) deferred, not added to scope | Carries `Provisional-Target: v7.4` but was not named in the STEP 8.1 anchor disposition; PO did not commit it alongside the 4 named items | Head of Specs Team (release planning engine), pending PO confirmation | 2026-07-17 |

### Sequencing decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Split into 5 EPICs (1 per feature item + 1 for the readiness bundle), resolving `BLG-GOV-248` | `BLG-GOV-248` (FinOps & Resource Architect) requested this exact cost/benefit call ahead of this invocation; no note was pre-produced, so the release planning engine performed the analysis directly. The 4 feature items share no data-model dependency and touch largely disjoint files/components (command palette, alerts, bulk-select, saved-filters/calendar). Bundling into 1 EPIC would force one large PR across 4 unrelated surfaces, serialize otherwise-parallel work, and raise review/merge risk. Splitting enables parallel execution, smaller PR surfaces per item, and matches the EPIC-per-item pattern already used for `BLG-SPEC-91–94` in v7.3. Lower governance overhead (the argument for bundling, per `roadmap_prompt.md` §7.1) is outweighed here because none of the coordination cost that bundling saves (shared data model, shared sequencing) actually exists between these 4 items. | Head of Specs Team (release planning engine), resolving `BLG-GOV-248` | 2026-07-17 |
| EPIC-01 (readiness bundle) sequenced first, gating EPIC-02/03/04/05 | `BLG-SPEC-95` delivers the npm dependency additions (`cmdk`, `react-day-picker`) and UX/design-review artefacts that EPIC-02/04/05 need before implementation can start cleanly | Head of Specs Team | 2026-07-17 |

### Accepted risks
| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|--------------|-----------|
| None | — | No escalations raised this cycle; no risk required Accepted-Risk disposition | — | — |

### Governance-input items addressed (not scope, not escalations)
- `BLG-GOV-248` — resolved above (split decision).
- `BLG-GOV-249` (confirm DL-069 capacity baseline reflected in next `sprint_capacity.md`) — cannot be verified within release planning (targets `plan sprint`); flagged forward in `cycle_summary.md` for the Sprint Planning Engine to action.
- `BLG-GOV-250` (confirm §13 applicability for `BLG-FE-115`/`BLG-FE-118`) — added as RISK-05 (High, must-resolve-before-sprint-planning-seal) and to the Pre-sprint Planning Required Decisions checklist in `cycle_summary.md`.

### Supersession note
Superseded by: v7.4 ship — 2026-07-17
Changelog: docs/product/changelog.md#v7.4
Verification report: claude/cycles/2026-07-17__release-v7.4/verification_report.md
Cycle: 2026-07-17__release-v7.4
