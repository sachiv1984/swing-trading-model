Owner: Strategy Rules & System Intent Owner
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-11-05 (initial decision, ESC-EXEC-20261105-03)
Cycle: 2026-11-03__release-v9.15
Story: ST-44 (EPIC-07, BLG-GOV-195)
Escalation ref: ESC-EXEC-20261105-03

---

# Product-Scope Exclusions: Re-Confirmation and Cadence

**Decision date:** 2026-11-05
**Decided by:** Strategy Rules & System Intent Owner with the Product Owner (the user, in session, acting in both roles), accepting the engine's recommendation as drafted in `ESC-EXEC-20261105-03`
**Subject:** the four product-scope exclusions in `claude/roadmap/current_roadmap.md` §2 "Product scope exclusions (deferred, not strategically excluded)". They had not been re-confirmed since they were first recorded (`BLG-GOV-195`).
**Not in scope:** the three strategic exclusions in the same section. They are system boundaries in `strategy_rules.md` §13, which has its own review and re-attestation path.
**AC reference:** `claude/cycles/2026-11-03__release-v9.15/stage4_backlog_slice.md#ST-44`

---

## Ruling per Exclusion

| Exclusion | Ruling | Reason |
|-----------|--------|--------|
| Broker API integration (execution) | **Re-confirmed** | Placing orders through a broker would cross the §13 boundary "not an automated trading bot" in practice, since all exits require manual confirmation. IT-06's Alpaca integration (v3.5) mirrors US positions to a paper account and places no live orders, so it does not change this. |
| Real-time streaming prices | **Re-confirmed** | The strategy is a daily/swing ATR momentum strategy: signals, trailing stops and regime checks are recalculated on close. Streaming would add data cost and intraday noise without changing any decision the rules make. |
| Social / community features | **Re-confirmed** | The system is "a single-user portfolio tracker" (§2 "This system is"). Shared or community features have no user to serve at this scale. |
| Options and futures trading support | **Re-confirmed** | `strategy_rules.md` defines an equities momentum strategy (UK and US shares), with ATR stops and position sizing for shares. Derivatives would need a different strategy contract, not an extension. |

All four remain deliberate product-scope choices, not un-revisited defaults.

## Re-Confirmation Cadence

- Re-confirm these four exclusions **every 10 completed cycles**. This review is at `completed_cycle_count` 91, so the next is due at **101**.
- The cadence is recorded in this decision only. No governance prompt is changed, so the CLAUDE.md §6 checklist does not apply. If a later run wants the cadence enforced by an engine, that is a separate governance change.
- The next review re-reads each exclusion against what has shipped since, and records a dated ruling in `docs/product/decisions/`.

## Effect

- `current_roadmap.md` §2 is unchanged. Under `sprint_backlog.md` ST-44 Notes, any change to §2 would be left to the next `run roadmap` (BLG-GOV-408); none is needed.
- `BLG-GOV-195` is met by this record once ST-44 merges.
