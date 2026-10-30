Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-30

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
- **Disposition:** Resolved
- **Resolution summary (2026-10-29T15:00:25Z):** Strategy Rules & System Intent Owner ruling, given in-session by the user acting in that role, dated 2026-10-29: **(a) Block entries.** (1) §4.2.1: while a market's regime is unknown (its index data could not be measured from any source), the pre-entry regime check FAILs for that market, and new entries there are blocked until it is measured. (2) §8.2: an unknown regime never triggers the market risk-off exit; open positions stay protected by their stops (§8.1). The engine recommended (a) when asked: fail-closed for entries without exiting the book on a data outage; (b) would need a persisted last-good result with a staleness limit, and (c) keeps an unmeasured reading counting as a pass. Applied by ST-03 as a case (c) `strategy_rules.md` write (§4.2.1 and §8.2) with a Change Log row and a `STRATEGY_VERSION_REGISTRY` entry. ST-03 reclassified `autonomous`.

## ESC-EXEC-20261030-01

- **Raised at:** 2026-10-30T08:26:37Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-29__release-v9.14
- **Step:** STEP 3.1.D (EPIC-02 execution loop, first sub-step of ST-09 per `sprint_backlog.md` ST-09 Notes, RISK-05)
- **ST/EPIC item:** ST-09 / EPIC-02 (BLG-BE-190)
- **Trigger type:** Strategy
- **Blocking statement:** `size_position()` (`backend/services/sizing_service.py`) computes US shares as `RiskAmount / (StopDistance × FX)`, where `FX` is GBP/USD quoted as USD per £1 (e.g. 1.27). Every other conversion in the same function (estimated cost, fees, concentration price, `MaxAffordableShares`, heat impact) divides a USD amount by `FX` to get GBP. §4.1.3 writes `RawShares = RiskAmount / StopDistance` without saying which currency the stop distance is in, and §4.1.5 says only that "the system uses an effective FX rate". AC 1 needs a dated Strategy Rules & System Intent Owner confirmation of the convention: **FX is USD per £1; a USD stop distance converts to GBP as `StopDistance / FX`; so for a US position `RawShares = RiskAmount × FX / StopDistance`** (£100 risk, $10 stop distance, FX 1.27 → 12.7 shares), and whether §4.1.3 should state the US formula explicitly.
- **Engine recommendation (non-binding):** confirm the convention above and state the US formula in §4.1.3. It matches §4.1.5's Known Deviation's canonical requirement (v1.19) and every other conversion in the codebase.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** a dated confirmation recorded in this escalation's resolution and in ST-09's QA evidence. The engine then applies the case (c) `strategy_rules.md` write (§4.1.5 Known Deviation closed; §4.1.3 US formula if ruled ambiguous) with its Change Log row and `STRATEGY_VERSION_REGISTRY` entry.
- **SLA due-by:** 2026-11-02T08:26:37Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-10-30T08:29:17Z):** Strategy Rules & System Intent Owner ruling, given in-session by the user acting in that role, dated 2026-10-30: **FX is GBP/USD quoted as USD per £1. A native USD stop distance converts to GBP as `StopDistance / FX`, so for a US position `RawShares = RiskAmount × FX / StopDistance`** (£100 risk, $10 stop distance, FX 1.27 → 12.7 shares). §4.1.3 is ambiguous and must state the US formula. Applied by ST-09 as a case (c) `strategy_rules.md` write (§4.1.3 US formula; §4.1.5 Known Deviation closed) with a Change Log row and a `STRATEGY_VERSION_REGISTRY` entry. ST-09 reclassified `autonomous`.
