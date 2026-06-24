Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v6.2
Cycle: 2026-06-24__release-v6.2
Last Updated: 2026-06-24

## Planning Decisions — v6.2 Production Strategy Parity & AI Intelligence

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Include all 4 P1 strategy parity items (BLG-FEAT-46–49) in v6.2 | Now-horizon confirmed by rebalance 2026-06-24__scheduled (STEP 8.2 PASS); close critical gap between live system and production_strategy.py backtest logic | Product Owner | 2026-06-24 |
| Include BLG-FEAT-50/51 (AI intelligence) as conditional scope in v6.2 | High user value (P2); depends on P1 cluster completing first; phased to Sprint 2 to manage capacity | Product Owner | 2026-06-24 |
| Include BLG-GOV-135/136 (governance debt) and BLG-OPS-75/BLG-QA-62 in v6.2 | All were explicitly targeted v6.2 from v6.1 lessons learnt (BLG-GOV-135/136, BLG-OPS-75) or are carry-forward (BLG-QA-62, priority recommendation from v6.1 closure) | Head of Specs Team | 2026-06-24 |
| Defer BLG-FEAT-52 (Trade tagging) | Gate-conditional: Arc 4 PO-02 (Journal Pattern Recognition) not imminent; L effort; low priority at current data density | Product Owner | 2026-06-24 |
| Defer SI-02 frontend | Gate not met: ~15 closed trades, gate requires 20; estimated ~2–3 months away | Product Owner | 2026-06-24 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01 (strategy parity) runs Sprint 1; EPIC-02 (AI intelligence) runs Sprint 2 | EPIC-02 (daily briefing, chat) requires live trailing stop, rebalance exit, and risk-off data from EPIC-01; dependency is absolute | Product Owner | 2026-06-24 |
| EPIC-03 (governance debt) runs Sprint 1 alongside EPIC-01 | All EPIC-03 items (XS–S effort) are independent of EPIC-01/02; batching minimises sprint overhead | Head of Specs Team | 2026-06-24 |
| RISK-01 §13 review for BLG-FEAT-50/51 required before sprint planning seal | AI endpoints (daily briefing, chat) must be confirmed advisory-only per strategy_rules.md §13 before implementation proceeds | Strategy Rules & System Intent Owner | 2026-06-24 |

### Accepted risks

None — no escalations raised in this planning cycle.

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-06-24__release-v6.2
