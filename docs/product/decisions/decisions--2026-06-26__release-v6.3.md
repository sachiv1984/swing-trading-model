Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v6.3
Cycle: 2026-06-26__release-v6.3
Last Updated: 2026-06-26

## Planning Decisions — v6.3 Strategy Benchmark, AI Security & Quality Infrastructure

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Include BLG-BE-39 and BLG-FE-79 (P1 correctness fixes) as mandatory firm scope | Rebalance 2026-06-26__scheduled STEP 8.0 Production Correctness Mandate — non-negotiable before any other v6.3 items. Both user-reported 2026-06-25 post-v6.2 ship. | Product Owner | 2026-06-26 |
| Include BLG-OPS-81 (AI rate limiting) and BLG-GOV-146 (injection risk assessment) as mandatory firm scope | Both are P1 security items for live AI endpoints shipped in v6.2 — POST /ai/daily-briefing and POST /ai/chat carry direct Anthropic API cost exposure. Rebalance cycle_summary.md lists as mandatory v6.3 inputs. | Cybersecurity & Trust Lead | 2026-06-26 |
| Include BLG-QA-65/66 (nightly stop CI simulation + spec) as mandatory firm scope | P1 test infrastructure — v6.2 shipped nightly computations with zero CI coverage. Silent regression risk on trailing stop, rebalance exit, and inv-vol sizing is unacceptable. Rebalance mandatory input. | Director of Quality | 2026-06-26 |
| Include BLG-FEAT-53 (Strategy Benchmark page) as firm scope in v6.3 | Filed 2026-06-26 with explicit Provisional-Target: v6.3 by Product Owner; directly addresses "am I trading this strategy?" visibility gap. L effort — placed in Sprint 2 to isolate from Sprint 1 correctness/security work. | Product Owner | 2026-06-26 |
| Include BLG-FE-80 (morning briefing progressive disclosure) as firm scope | Mandatory pull-forward from rebalance PVR advisory (ratio=0.37) — v6.3 must include meaningful U-content. S effort (0.5d) pairs with Sprint 2. | Product Owner | 2026-06-26 |
| Classify BLG-GOV-147/148, BLG-QA-67/68, BLG-OPS-79/78/80 as conditional | All 7 items are P2–P3 with Provisional-Target: v6.3; include in sprint planning based on Sprint 1/2 velocity. Firm item load (~9.0d) is sufficient for a 2-sprint plan without conditional padding. | PMO Lead | 2026-06-26 |
| Defer BLG-FEAT-52 (Trade tagging) | Gate-conditional: Arc 4 PO-02 (6+ months AI journal entries). AI journals only started 2026-06-25 — gate clears ~2026-12. L effort; low priority at current data density. | Product Owner | 2026-06-26 |
| Defer SI-02 frontend | Gate not met: ~15 closed trades, gate requires 20; estimated ~2026-09. | Product Owner | 2026-06-26 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01 (correctness + security) and EPIC-02 (test infrastructure) run Sprint 1 in parallel | Both EPICs are P1 priority and independent of each other and of EPIC-03. Sprint 1 firm effort ~3.5d combined — leaves room for conditional S2-05/06 and S2-09/10 in Sprint 1. | PMO Lead | 2026-06-26 |
| EPIC-03 (Strategy Benchmark + UX) runs Sprint 2 | BLG-FEAT-53 (5.0d flagship) fills most of Sprint 2. No dependency on Sprint 1 outcomes. Conditional EPIC-03 items (S2-13/14/15) fill remaining Sprint 2 capacity. | PMO Lead | 2026-06-26 |
| BLG-FEAT-53 schema first within EPIC-03 | backtest_trades and backtest_yearly_performance table migrations must complete before POST /strategy/benchmark/import or GET endpoints can be implemented. Frontend gates on API. | Head of Engineering | 2026-06-26 |
| BLG-OPS-79 requires architecture review before endpoint design | Gate condition: v6.2 scheduler architecture must be reviewed before GET /health/scheduler is designed. Review can commence Sprint 1; implementation Sprint 2 conditional. | Infrastructure & Operations Owner | 2026-06-26 |

### Accepted risks

None — no escalations raised in this planning cycle.

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-06-26__release-v6.3
