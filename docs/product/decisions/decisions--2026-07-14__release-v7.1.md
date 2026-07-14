Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v7.1
Cycle: 2026-07-14__release-v7.1
Last Updated: 2026-07-14

## Planning Decisions — v7.1 Nightly Backtest Data Integrity

### Scope decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Anchor scope fixed to `BLG-BE-59`, `BLG-BE-60`, `BLG-FE-107` per roadmap §3 mandatory naming | STEP 8.0 Production Correctness Fast-Track named these directly at the 2026-07-13 rebalance; Release Planning does not alter roadmap-named scope | Product Owner | 2026-07-14 |
| Add 4 capacity-filling items (`BLG-BE-61`, `BLG-QA-106`, `BLG-SPEC-83`, `BLG-SPEC-84`) as firm scope | All are ready, effort-estimated, `Provisional-Target: v7.1` v7.0 post-ship hardening items; total scope (~11–13.5d) fits the ~12–14d capacity band; applies the v7.0 carry-forward lesson on capacity-filling selection (see `run_manifest.md` §Scope Decision) | Product Owner | 2026-07-14 |
| Defer `BLG-BE-62`, `BLG-SPEC-85` | Both carry `Provisional-Target: TBD`, not v7.1-targeted; `BLG-BE-62` is a broader cross-job audit better scoped independently | Product Owner | 2026-07-14 |

### Sequencing decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-02 (`BLG-FE-107`) sequenced after Design Gate passes | Item explicitly requires a design-gate decision between spec-compliance fix and formal acceptance of shipped amber treatment; not a same-sprint code-only fix | Head of Specs Team | 2026-07-14 |
| EPIC-01's two items may run in parallel or tightly sequenced PRs | No hard dependency declared in backlog; RISK-02 mitigation (regression check for deterministic backtest output) applies regardless of ordering | Backend Engineering Patterns Owner | 2026-07-14 |

### Accepted risks
None.

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-07-14__release-v7.1
