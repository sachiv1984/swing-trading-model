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

## ESC-EXEC-20261030-02

- **Raised at:** 2026-10-30T15:55:23Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-29__release-v9.14
- **Step:** STEP 3.1.D (EPIC-03 execution loop, first sub-step of ST-15 per `sprint_backlog.md` ST-15 Notes, RISK-05)
- **ST/EPIC item:** ST-15 / EPIC-03 (BLG-AI-20)
- **Trigger type:** Strategy
- **Blocking statement:** `journal_summary_language_failures()` (`backend/services/ai_service.py`) fails a journal summary on `scan_prescriptive` or `_TRADING_CHANGE_RE` (ruling `ESC-EXEC-20261027-03` (A): subject, then a present-tense or modal word, then a change verb). Seven advisory sentences pass both: "Consider tightening stops on volatile names.", "It may be worth revisiting position sizing.", "Stops could be tightened.", "Tighter stops could help.", "Reducing position size after losses would be prudent.", "A review of setups is warranted." and "Stop placement is something to revisit." ST-15 AC 1 needs the AI Compliance & Governance Officer to extend (A). No §13 clause names the journal summary, so the extension is a §13 determination answering §13.1 (what the system is) and §13.2 (what it is not). Proposed extension, a sibling pattern reported under the same `trading_change` category, using the same subject and change-verb lists: **(1)** imperative "consider/try" then a change verb then the subject; **(2)** "worth" then a change verb, with the subject in the sentence; **(3)** passive: subject, then a modal (could/should/might/may/would/can/must) + "be", then a change verb; **(4)** a change gerund, review noun ("a review/revision/rethink of") or comparative ("tighter/wider/smaller/larger/lower/higher") before the subject, then an evaluative phrase ("would be prudent/wise/better/sensible/helpful", "could/may/might/would help", "is/are warranted/needed/advisable/recommended"); **(5)** subject … "is something to" + change verb. Past-tense descriptive wording ("Stops were tightened after the loss.") still passes. `compliance_check_result` values, fallback text, prompt and `JOURNAL_SUMMARY_PROMPT_VERSION` are unchanged.
- **Engine recommendation (non-binding):** approve the extension as proposed.
- **Owning authority:** AI Compliance & Governance Officer
- **Unblock criteria:** a dated ruling recorded in this escalation's resolution, answering §13.1 and §13.2. The engine then implements it, adds the seven sentences as positive cases, keeps every ST-18 (v9.13) case's result, and updates `ai_s13_boundary_test_suite.md` (B-JS).
- **SLA due-by:** 2026-11-02T15:55:23Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-10-30T16:49:32Z):** AI Compliance & Governance Officer ruling, given in-session by the user acting in that role, dated 2026-10-30: **Approved as proposed** — extension (A′) of `ESC-EXEC-20261027-03` (A). §13.1: the journal summary stays a description of what the notes record; no AI authority is added. §13.2: wording that suggests changing stops, sizing or setups is the advisory risk §13.2 excludes, so all five forms fail the summary: (1) imperative "consider/try" + change verb + subject; (2) "worth" + change verb with the subject in the sentence; (3) passive subject + modal + "be" + change verb; (4) change gerund, review noun or comparative before the subject, then an evaluative phrase; (5) subject … "is something to" + change verb. Same subject and change-verb lists as (A), reported as `trading_change`; past-tense descriptive wording passes; `compliance_check_result` values, fallback, prompt and `JOURNAL_SUMMARY_PROMPT_VERSION` unchanged. ST-15 reclassified `autonomous`.

## ESC-EXEC-20261030-03

- **Raised at:** 2026-10-30T15:55:23Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-29__release-v9.14
- **Step:** STEP 3.1.D (EPIC-03 execution loop, first sub-step of ST-17 per `sprint_backlog.md` ST-17 Notes, RISK-05)
- **ST/EPIC item:** ST-17 / EPIC-03 (BLG-AI-22)
- **Trigger type:** Strategy
- **Blocking statement:** Ruling `ESC-EXEC-20261027-01` (B) condition 3 attributes a chat stop sentence to the held focus ticker when the sentence names no *held* ticker. With focus `MU`, "TSLA's stop was hit last week." (TSLA not held) therefore gets "(MU stop last recalculated …)", which reads as if it were about TSLA. ST-17 AC 1 needs the AI Compliance & Governance Officer to amend condition 3. Proposed amendment: **attribute to the focus ticker only when the sentence names no ticker-like token other than the focus ticker itself**, where a ticker-like token is a `_TICKER_TOKEN_RE` match not in `_NON_TICKER_WORDS` (the briefing caveat's definitions, extended by ST-16), compared in ST-15 normalised form. A sentence naming another token is left unattributed (`[STOP-TIME-MISSING]` / `stop_time_missing_unattributed`), as before v9.13 ST-16. Conditions 1, 2 and 4–7 are unchanged; briefing actions keep `own_ticker`. As a §13 determination: §13.2 (the system does not present AI text as a decision about a position it is not about), and §13.5's "BLG-FEAT-50/51 (AI Advisory Layer — daily briefing + chat)" roster row: the amendment narrows a code-written note, adds no AI authority, and stays within that clearance.
- **Engine recommendation (non-binding):** approve the amendment as proposed.
- **Owning authority:** AI Compliance & Governance Officer
- **Unblock criteria:** a dated ruling recorded in this escalation's resolution, answering §13.2 and the §13.5 roster row. The engine then implements it after ST-16 and ST-20, adds the TSLA/MU test, and keeps every `tests/test_ai_stop_time_focus_attribution.py` test passing.
- **SLA due-by:** 2026-11-02T15:55:23Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-10-30T16:49:32Z):** AI Compliance & Governance Officer ruling, given in-session by the user acting in that role, dated 2026-10-30: **Approved as proposed** — `ESC-EXEC-20261027-01` (B) condition 3 amended: a chat stop sentence is attributed to the held focus ticker only when it names no ticker-like token (`_TICKER_TOKEN_RE` match not in `_NON_TICKER_WORDS`, compared in ST-15 normalised form) other than the focus ticker; otherwise it is left unattributed (`stop_time_missing_unattributed`). §13.2: the system does not present a code-written note as being about a position the sentence is not about. §13.5 "BLG-FEAT-50/51 (AI Advisory Layer — daily briefing + chat)": the amendment narrows a code-written note, adds no AI authority and stays within that clearance. Conditions 1, 2 and 4–7 unchanged. ST-17 reclassified `autonomous`.
