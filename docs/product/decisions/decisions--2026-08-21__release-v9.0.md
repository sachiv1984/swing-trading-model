Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v9.0
Cycle: 2026-08-21__release-v9.0
Last Updated: 2026-08-21

## Planning Decisions — v9.0 AI Debrief/Backtest Follow-Through, Risk-Data Integrity & Operational Resilience

### Scope decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Scope drawn directly from the ungated backlog pool (no formal roadmap Now-horizon section) | STEP -1.2 Option (b) equivalence — `2026-08-11__scheduled` rebalance's documented Option (b) defer decision, consistent with v8.5–v8.9 precedent | Release Planning Engine (delegated authority) | 2026-08-21 |
| Widen scope to the top of the confirmed ~24–28 day capacity band (27.15d) | Explicit user instruction: "use full capacity" | Product Owner | 2026-08-21 |
| `BLG-FEAT-92` excluded from firm scope | Own AC requires reconciliation against gate-conditional `BLG-FEAT-30` before scheduling; unresolved for the 2nd consecutive cycle — not resolvable unilaterally by this routine | Product Owner (delegated) | 2026-08-21 |
| `BLG-FEAT-73`/`BLG-FEAT-74` excluded from firm scope despite P1 priority | Both carry unmet content-level pre-conditions (re-check gate; §13 pre-clearance) not captured by a formal `Gate criteria:` field — manually screened per §1.3a's BLG-OPS-48 data-quality pattern | Release Planning Engine (delegated authority) | 2026-08-21 |
| `BLG-GOV-105` excluded — already closed | Confirmed ✅ CLOSED duplicate (2026-07-12); stale entry, not live scope | Release Planning Engine (delegated authority) | 2026-08-21 |
| `BLG-OPS-101`, `BLG-BE-54` added to fill remaining capacity to the top of the band | Both P3, ungated, `Gate criteria: None`, small clean hygiene items with no dependency risk | Product Owner (delegated) | 2026-08-21 |

### Sequencing decisions
| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| `BLG-BE-105` sequenced early within EPIC-02 | Touches live open-position stop values directly; must run through the existing regression-tested floor-calculation path | Product Owner (delegated) | 2026-08-21 |
| `BLG-BE-109` sequenced with its own regression test added before behaviour change | Fix changes production-consumed nightly backtest rebalance-date logic | Product Owner (delegated) | 2026-08-21 |

### Accepted risks
| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| None | — | No escalations raised this cycle | — | — |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-08-21__release-v9.0
