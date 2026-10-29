Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-29

# Execution Escalations — 2026-10-29__release-v9.14

## ESC-EXEC-20261029-01

- **Raised at:** 2026-10-29T14:55:56Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-29__release-v9.14
- **Step:** STEP 3.1.D (EPIC-01 execution loop, raised at sprint start per `sprint_backlog.md` ST-03 Notes, RISK-05)
- **ST/EPIC item:** ST-03 / EPIC-01 (BLG-BE-193)
- **Trigger type:** Strategy
- **Blocking statement:** When SPY or FTSE index data cannot be fetched, `check_market_regime()` (`backend/utils/pricing.py`) sets that market to risk-on with price and MA 0, so a regime that was never measured is used as a measured one. ST-03 returns an explicit unknown state. AC 1 needs a dated Strategy Rules & System Intent Owner ruling on what "regime unknown" means for entries (`strategy_rules.md` §4.2.1, regime gate) and the risk-off exit (§8.2): **(a)** block new entries in that market until it is measured; **(b)** keep the last measured regime (with its timestamp) for entries and the risk-off check; or **(c)** treat it as risk-on with a visible warning (today's behaviour, made explicit).
- **Engine recommendation (non-binding):** none; this is a strategy call. The unknown display (`market-regime-unknown/decision_record.md` §2) is the same under every branch.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** a dated ruling, (a), (b) or (c), recorded in this escalation's resolution and in ST-03's QA evidence. If it changes the behaviour §4.2.1 or §8.2 describes, the engine applies the case (c) `strategy_rules.md` write with its Change Log row and `STRATEGY_VERSION_REGISTRY` entry.
- **SLA due-by:** 2026-11-01T14:55:56Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Open
