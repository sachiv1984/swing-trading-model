Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-04

# Execution Escalations — 2026-11-03__release-v9.15

## ESC-EXEC-20261104-01

- **Raised at:** 2026-11-04T10:56:15Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-11-03__release-v9.15
- **Step:** STEP 3.1.D (EPIC-01 execution loop, raised at sprint start per `sprint_backlog.md` ST-01 Notes and `stage4_backlog_slice_addendum.md` ST-01, RISK-07)
- **ST/EPIC item:** ST-01 / EPIC-01 (BLG-FE-244)
- **Trigger type:** Strategy
- **Blocking statement:** ST-01 AC 2 says that with a risk-off or unknown regime "save requires the acknowledgement". `strategy_rules.md` §4.2.6 (binding) says the advisory panel "must never prevent, gate, or auto-reject" a submission and that any hard submission gate needs a new §13 review. §4.2.1 (v1.20) says new entries in an unknown-regime market "are blocked". The Trade Plan path's acknowledgement does not disable Save today. A dated ruling is needed: **Branch A (acknowledge to proceed)** — Submit is disabled until a WARN/FAIL is acknowledged; the ruling states that a one-click, user-passable acknowledgement is not a "hard submission gate" under §4.2.6 (and, if needed, clarifies §4.2.1's "are blocked" wording), applied as a case (c) `strategy_rules.md` write confirmed at seal; or **Branch B (advisory only)** — Submit stays enabled as on the plan path, and AC 2 is met by the regime check showing FAIL/unknown with the acknowledgement offered. Both are designed in `docs/design/2026-11-03__release-v9.15/trade-entry-pre-entry-checks/decision_record.md` §2.3.
- **Engine recommendation (non-binding):** see the in-session question; this is a strategy call.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** a dated ruling, Branch A or Branch B, recorded in this escalation's resolution and in ST-01's QA evidence. Under Branch A with a text clarification, the engine applies the case (c) `strategy_rules.md` write with its Change Log row and `STRATEGY_VERSION_REGISTRY` entry in the same commit.
- **SLA due-by:** 2026-11-07T10:56:15Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-11-04T11:00:36Z):** Strategy Rules & System Intent Owner ruling, given in-session by the user acting in that role, dated 2026-11-04: **Branch A, acknowledge to proceed.** On Trade Entry, when any pre-entry check is WARN or FAIL (including a risk-off or unknown regime), Submit is disabled until the user ticks the acknowledgement. A one-click, user-passable acknowledgement is not a "hard submission gate" under §4.2.6, and §4.2.1's "are blocked" for an unknown regime means the entry cannot be saved until the FAIL is acknowledged (or the regime is measured). The engine recommended Branch A: it carries out v1.20's fail-closed intent while keeping the decision with the user, as §3 requires. Applied by ST-01 as a case (c) `strategy_rules.md` write (§4.2.1, §4.2.6) with a Change Log row and a `STRATEGY_VERSION_REGISTRY` entry. ST-01 reclassified `autonomous`.

## ESC-EXEC-20261104-02

- **Raised at:** 2026-11-04T14:51:24Z (raised and ruled in the same in-session exchange)
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-11-03__release-v9.15
- **Step:** §5.3 agent-mediated Director of Quality review of EPIC-01, finding 2 (Blocked)
- **ST/EPIC item:** ST-06 / EPIC-01 (BLG-BE-173)
- **Trigger type:** Strategy
- **Blocking statement:** ST-06 AC 1 says `atr_trail_stop` "equals the value `calculate_trailing_stop` would produce from the same inputs". The endpoint passes `current_stop = -inf`, so it reports the §7.2 candidate without ratcheting against the stored stop. Example: entry 100, price 130, ATR 4, stored stop 125 gives 122 and "no action required", where `calculate_trailing_stop` with the stored stop returns 125. A ruling is needed on whether the un-ratcheted candidate is the intended value.
- **Engine recommendation (non-binding):** rule the un-ratcheted candidate as intended. A ratchet would make `trail_difference` always ≥ 0 and the "below current stop — no action required" branch unreachable.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** a dated ruling recorded here and cited in ST-06's QA evidence Deviations cell.
- **SLA due-by:** 2026-11-07T14:51:24Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-11-04T14:51:24Z):** Strategy Rules & System Intent Owner ruling, given in-session by the user acting in that role, dated 2026-11-04: **the Trail Stop modal's `atr_trail_stop` is the un-ratcheted §7.2 candidate** — `calculate_trailing_stop` with the §11 multipliers and the breakeven floor, but not raised to the stored `current_stop`. `trail_difference` stays signed so the modal can say when the candidate is below the current stop. ST-06 AC 1 is met under this reading; no code change and no backlog remainder. No `strategy_rules.md` text change is needed: §7.2's ratchet governs the stored stop, which this read-only endpoint does not write.

## ESC-EXEC-20261104-03

- **Raised at:** 2026-11-04T19:29:15Z (raised and ruled in the same in-session exchange)
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-11-03__release-v9.15
- **Step:** STEP 3.1.D (EPIC-03 execution loop, raised at EPIC start per `sprint_backlog.md` ST-20 Notes)
- **ST/EPIC item:** ST-20 / EPIC-03 (BLG-BE-171)
- **Trigger type:** Strategy
- **Blocking statement:** ST-20's first sub-step needs a ruling: is a behavioural strategy version's effective date the ruling date or the date its code reaches production? `strategy_version_at_entry` is stamped by `get_current_strategy_version()` from the registry in the live code. v1.15 was ruled 9 October 2026, but PR #1970 merged to `main` (and deployed) on 12 October 2026 (`e07d2a04`, 12:58Z), so positions entered 9–11 October were stamped "1.4" while their `entry_date` falls in the v1.15 window. The same one-day lag exists for v1.17 (Change Log 16 October, PR #2071 merged 17 October) and v1.20 (29 October, PR #2131 merged 30 October); v1.21 and v1.23 reached `main` on their Change Log dates.
- **Engine recommendation (non-binding):** the deploy date. The stamp switches when the code deploys, so a deploy-date window agrees with the stamps by construction.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** a dated ruling recorded here; under the deploy date, ST-20 applies the case (c) `strategy_rules.md` Change Log row 1.15 Date write (confirmed at seal) with the matching registry `effective_date`.
- **SLA due-by:** 2026-11-07T19:29:15Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-11-04T19:29:15Z):** Strategy Rules & System Intent Owner ruling, given in-session by the user acting in that role, dated 2026-11-04: **a behavioural version's effective date is the date its code reaches production (merges to `main`, which deploys).** ST-20 records the rule in the `strategy_version_registry.py` docstring and moves v1.15's registry `effective_date` and Change Log row 1.15 Date to 12 October 2026 (case (c), confirmed at seal). The v1.17 and v1.20 one-day lags fall outside the seal's authorisation (row 1.15 only) and are filed as a follow-up backlog item. ST-20 reclassified `autonomous`.

## ESC-EXEC-20261104-04

- **Raised at:** 2026-11-04T19:29:15Z (raised and ruled in the same in-session exchange)
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-11-03__release-v9.15
- **Step:** STEP 3.1.D (EPIC-03 execution loop, raised at EPIC start per `sprint_backlog.md` ST-23 Notes, RISK-07)
- **ST/EPIC item:** ST-23 / EPIC-03 (BLG-SPEC-198)
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-23's first sub-step needs a ruling on the canonical open-position `pnl` basis. The live computation (`calculate_position_pnl()`, used by `get_positions_with_prices()` and `portfolio_service.py`) is `(current_price − native_entry) × shares ÷ live_fx_rate` for US positions, with no `fees_paid` deduction. `data_model_positions_dictionary.md` v0.6 §5.2 and the `pnl` row say entry-time `fx_rate` and `− fees_paid`. Closed-trade realised P&L is `exit_proceeds_gbp − total_cost_gbp` (fees deducted, currency movement included), so neither matches it exactly.
- **Engine recommendation (non-binding):** the spec follows the code. This is a doc-only change, no displayed figure changes, and it fits the 0.5d estimate. The basis difference from realised P&L gets its own follow-up item.
- **Owning authority:** Data Model & Domain Schema Owner
- **Unblock criteria:** a dated ruling recorded here and in `data_model_positions_dictionary.md`'s decision record.
- **SLA due-by:** 2026-11-05T19:29:15Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-11-04T19:29:15Z):** Data Model & Domain Schema Owner ruling, given in-session by the user acting in that role, dated 2026-11-04: **the spec follows the code.** Open-position `pnl` is native P&L converted at the live GBP/USD rate (US) and is not net of `fees_paid`. Rationale: it is the figure every surface displays today, and changing it would change displayed P&L on several pages, which needs a design pass and more than the 0.5d budget. The difference from the realised (closed-trade) basis, which is fee-netted and includes currency movement on the principal, is recorded in the dictionary and filed as a follow-up backlog item. ST-23 reclassified `autonomous`.

## ESC-EXEC-20261104-05

- **Raised at:** 2026-11-04T21:03:58Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-11-03__release-v9.15
- **Step:** STEP 3.1.A → 3.1.D (EPIC-02 execution loop, found while mapping ST-12's "components used only by the legacy page")
- **ST/EPIC item:** ST-12 / EPIC-02 (BLG-FE-247)
- **Trigger type:** Scope
- **Blocking statement:** ST-12 removes `src/pages/Dashboard.js` and "components used only by the legacy page" (slice Scope bullet 3; `site-structure-phase1/decision_record.md` §3.3). `MonitorModal.js` (the Daily Position Monitor, with the v9.13 exit queue and v9.14 grace-aware suggestions) is opened only from that page's Quick Actions widget (`QuickActions.js` "Daily Monitor"), and `positions.md` §Daily Position Monitor Exit Queue names "Dashboard → Quick Actions → Run Monitor" as its entry point. No other page opens it. Applied literally, ST-12 deletes a live feature and 7 Playwright scenarios (`monitor-exit-queue.spec.js` SC-MEQ-01..04, `monitor-grace-aware-suggestions.spec.js` SC-MGS-01..03). Neither the design brief nor the slice addendum mentions the Monitor. Moving its entry point to another page is new UI that the engine may not add on its own authority (§5.2: no scope extension).
- **Engine recommendation (non-binding):** (a) move the Monitor's entry point to a "Daily Monitor" button in the Positions page header, carrying over `MonitorModal`, the exit queue and the pre-select logic unchanged, retarget the 7 monitor scenarios to `/#/Positions`, and update `positions.md` §Daily Position Monitor's entry-point line in the same commit. Positions is where exits are recorded, `positions.md` already owns the Monitor spec, and the Dashboard home is about to be redesigned by ST-09/`BLG-FE-254`. Other options: (b) the same move onto the Dashboard home; (c) defer ST-12 to v9.16 and keep the legacy page this sprint; (d) remove the Monitor with the page (not recommended: feature loss).
- **Owning authority:** Product Owner (scope), with the Head of UX & Design on placement
- **Unblock criteria:** a dated Product Owner ruling naming option (a), (b), (c) or (d), recorded here and in ST-12's QA evidence. Under (a) or (b), the Head of UX & Design confirms the placement (agent-mediated per §5.3 permitted).
- **SLA due-by:** 2026-11-05T21:03:58Z (24h — lifecycle/scope)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-11-04T21:04:56Z):** Product Owner ruling, given in-session by the user acting in that role, dated 2026-11-04: **option (a), move the Monitor to Positions.** ST-12 adds a "Daily Monitor" button to the Positions page header that opens `MonitorModal` with the exit queue and pre-select logic unchanged, retargets the 7 monitor scenarios (`monitor-exit-queue.spec.js`, `monitor-grace-aware-suggestions.spec.js`) to `/#/Positions`, and updates `positions.md` §Daily Position Monitor's entry-point line in the same commit (Known Deviation standard does not apply: the spec is updated to the ruled placement). The Head of UX & Design confirms the placement (agent-mediated, §5.3) in ST-12's QA evidence. ST-12 reclassified `autonomous`.

## ESC-EXEC-20261105-01

- **Raised at:** 2026-11-05T08:26:16Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-11-03__release-v9.15
- **Step:** STEP 3.1.D (EPIC-04 execution loop, first sub-step of ST-25 per `sprint_backlog.md` ST-25 Notes; covers ST-27 per its Notes)
- **ST/EPIC item:** ST-25 / EPIC-04 (BLG-AI-24); ST-27 / EPIC-04 (BLG-AI-26)
- **Trigger type:** Strategy
- **Blocking statement:** `journal_summary_language_failures()` applies ruling `ESC-EXEC-20261027-03` (A) and its extension (A′) `ESC-EXEC-20261030-02`. Checked on this branch (cut from `7a749bcf`): two descriptive sentences fail as `trading_change` — "Stops can be moved only upward under the system." (form (3)'s "can") and "The trader wrote that a review of setups is warranted." (reported speech, form (4)); two more fail through form (4)'s "could/may help" — "Moving stops to breakeven after a 2R gain could help explain the lower drawdown." and "Smaller position size in May may help explain why losses were lower." (BLG-AI-26). Six advisory sentences pass: "Consider a tighter stop.", "Perhaps revisit stop placement.", "It could help to tighten stops.", "Think about tightening stops.", "Your sizing is worth a second look." and "Stops would benefit from tightening." Each change alters the ruling's forms, so it is a §13 determination answering §13.1 and §13.2. Proposed amendment (A″): **(i)** drop "can" from form (3)'s modals (a statement of what the system permits is descriptive); **(ii)** a match inside past-tense reported speech of the notes or trader ("wrote/noted/recorded/said/mentioned/commented/felt/thought/believed/concluded that …") passes; **(iii)** form (4)'s "could/may/might/would help" does not match when "help" is followed by an explanatory verb (explain, account for, show) — ST-27; **(iv)** new advisory forms, same subject and change-verb lists, reported as `trading_change`: form (1) also takes "think about" and a comparative + subject ("Consider a tighter stop."); a sentence-initial imperative change verb, optionally after "perhaps/maybe", before the subject ("Perhaps revisit stop placement."); "could/may/might/would help to" + change verb + subject; subject … "worth a (second/another) look"; subject … "would/could/might/may benefit from" + change gerund. Past tense still passes; `compliance_check_result` values, fallback, prompt and `JOURNAL_SUMMARY_PROMPT_VERSION` unchanged.
- **Engine recommendation (non-binding):** approve (A″) as proposed.
- **Owning authority:** AI Compliance & Governance Officer
- **Unblock criteria:** a dated ruling recorded in this escalation's resolution, answering §13.1 and §13.2, before the code change (ST-25 AC 1). The engine then implements it, adds each BLG-AI-24 and BLG-AI-26 sentence as a test with the ruled result, keeps every ST-15 (v9.14) and v9.13 ST-18 case's result, and updates `ai_s13_boundary_test_suite.md` B-JS-04.
- **SLA due-by:** 2026-11-08T08:26:16Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-11-05T08:50:24Z):** AI Compliance & Governance Officer ruling, given in-session by the user acting in that role, dated 2026-11-05: **(A″) approved as proposed**, amending (A) `ESC-EXEC-20261027-03` and (A′) `ESC-EXEC-20261030-02`. §13.1: the journal summary stays a description of what the notes record; no AI authority is added. §13.2: a statement of what the system permits ("can be moved"), the trader's own past-tense words reported as such, and "could/may help explain/account for/show" are descriptive and pass; the six missed sentences suggest changing stops or sizing, which is the advisory risk §13.2 excludes, so the new forms fail as `trading_change`. Parts: (i) "can" dropped from form (3); (ii) past-tense reported speech of the notes or trader passes; (iii) "help" + explanatory verb excluded from form (4) (ST-27, BLG-AI-26); (iv) new forms — "think about" and comparative + subject in form (1), sentence-initial imperative change verb (optionally after "perhaps/maybe"), "could/may/might/would help to" + change verb, subject … "worth a (second/another) look", subject … modal + "benefit from" + change gerund. Past tense passes; `compliance_check_result` values, fallback, prompt and `JOURNAL_SUMMARY_PROMPT_VERSION` unchanged. ST-25 reclassified `autonomous`; ST-27 proceeds under this ruling.

## ESC-EXEC-20261105-02

- **Raised at:** 2026-11-05T08:26:16Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-11-03__release-v9.15
- **Step:** STEP 3.1.D (EPIC-04 execution loop, first sub-step of ST-28 per `sprint_backlog.md` ST-28 Notes, RISK-03)
- **ST/EPIC item:** ST-28 / EPIC-04 (BLG-GOV-194)
- **Trigger type:** Strategy
- **Blocking statement:** ST-28 needs the Strategy Rules & System Intent Owner's dated re-read of `strategy_rules.md` §13 (v1.24) against the AI journal summary (`POST /ai/journal-summary`, BLG-AI-20, v9.14 ST-15), recorded in `docs/product/decisions/`. Engine reading for the owner to confirm or correct: no §13 clause names the journal summary. §13.1 ("deterministic decision-support engine", "human-in-the-loop") holds: the summary is a read-only description of the user's own notes, writes nothing but audit rows, and makes no decision. §13.2 ("not … a discretionary or adaptive rule system", "not … an AI-driven prediction system") holds: it predicts nothing, and the output check withholds wording that suggests changing stops, sizing or setups. But §13's text says nothing about AI-written narrative advising a change to the strategy's parameters. Three rulings (`ESC-EXEC-20261027-03`, `ESC-EXEC-20261030-02`, and `ESC-EXEC-20261105-01` now open) have each had to infer that exclusion from §13.2's "discretionary or adaptive rule system". The journal summary is not on §13.5's re-attestation roster, which lists the briefing/chat, debrief and monthly narrative. Outcomes: **(1) clarify** — a case (c) write (authorised at seal, confirmed 2026-11-03): one §13.2 sentence stating that AI-written text describing the user's data (briefing, chat, debrief, monthly narrative, journal summary) must not suggest changing stops, position sizing, setups or other strategy parameters, plus a §13.5 roster row for the journal summary citing the new decision record; documentation-only version 1.25 in `DOCUMENTATION_ONLY_VERSIONS`; **(2) confirmed unambiguous**, journal summary added to §13.5 by a follow-up backlog item (the seal authorises a roster row only with a clarification); **(3) confirmed unambiguous**, not added to the roster.
- **Engine recommendation (non-binding):** outcome (1). Three rulings inferring the same exclusion is the evidence that the language is not explicit, and the roster gap leaves the summary out of the 2027-02-06 re-attestation.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** a dated outcome (1), (2) or (3) recorded in this escalation's resolution. The engine then writes the decision record under `docs/product/decisions/` answering each clause it cites, and under (1) applies the case (c) write with its §16 Change Log row, registry entry and §15 re-run in one commit.
- **SLA due-by:** 2026-11-08T08:26:16Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-11-05T08:50:24Z):** Strategy Rules & System Intent Owner ruling, given in-session by the user acting in that role, dated 2026-11-05: **outcome (1), clarify.** The re-read finds §13.1 and §13.2 hold for the journal summary but that §13's text does not state the exclusion three rulings have inferred, so the boundary language is not explicit enough. ST-28 applies the case (c) write confirmed at seal (2026-11-03): one §13.2 sentence stating that AI-written text describing the user's data must not suggest changing stops, position sizing, setups or other strategy parameters, and a §13.5 roster row for the journal summary citing the new decision record; documentation-only version 1.25 with its §16 Change Log row, `DOCUMENTATION_ONLY_VERSIONS` entry and §15 re-run. ST-28 reclassified `autonomous`.

## ESC-EXEC-20261105-03

- **Raised at:** 2026-11-05T13:56:47Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-11-03__release-v9.15
- **Step:** STEP 3.1.D (EPIC-07 execution loop)
- **ST/EPIC item:** ST-44 / EPIC-07 (BLG-GOV-195)
- **Trigger type:** Strategy
- **Blocking statement:** ST-44 needs a dated decision by the Strategy Rules & System Intent Owner with the Product Owner that re-confirms or flags each of the four product-scope exclusions in `current_roadmap.md` §2 (broker API integration (execution), real-time streaming prices, social/community features, options and futures support), with a reason for each, and sets a re-confirmation cadence. The engine cannot make this scope determination.
- **Engine recommendation (non-binding):** re-confirm all four. Broker execution would cross §13's "not an automated trading bot" boundary in practice, and IT-06's Alpaca mirror is read-only paper trading. Real-time streaming adds cost and noise to a daily/swing ATR strategy whose signals and stops recalculate on close. Social features contradict the single-user scope in §2 "This system is". Options and futures fall outside the equities momentum strategy `strategy_rules.md` defines. Cadence: re-confirm every 10 completed cycles (next due at completed_cycle_count 101), recorded in the decision only, so no governance prompt change. `current_roadmap.md` §2 unchanged.
- **Owning authority:** Strategy Rules & System Intent Owner (with the Product Owner)
- **Unblock criteria:** a dated ruling per exclusion (re-confirm or flag, with reason) and a cadence, recorded in this escalation's resolution. The engine then writes `docs/product/decisions/strategic-exclusions-reconfirmation--2026-11-05.md`.
- **SLA due-by:** 2026-11-08T13:56:47Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-11-05T14:38:30Z):** Strategy Rules & System Intent Owner with the Product Owner, ruling given in-session by the user acting in both roles, dated 2026-11-05: engine recommendation accepted as drafted. All four product-scope exclusions re-confirmed with the reasons above; re-confirm every 10 completed cycles (next at completed_cycle_count 101), recorded in the decision only (no governance prompt change); `current_roadmap.md` §2 unchanged. Record: `docs/product/decisions/decisions--2026-11-03__release-v9.15--ST-44-strategic-exclusions-reconfirmation.md`.

## ESC-EXEC-20261105-04

- **Raised at:** 2026-11-05T13:56:47Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-11-03__release-v9.15
- **Step:** STEP 3.1.D (EPIC-07 execution loop)
- **ST/EPIC item:** ST-45 / EPIC-07 (BLG-GOV-196)
- **Trigger type:** Scope
- **Blocking statement:** ST-45 needs a dated Product Owner decision that re-confirms each of the seven Priority 3 — Deferred initiatives in `initiative_register.md` as deliberately deferred, or flags it for review, with a reason for each. The engine cannot make this scope determination.
- **Engine recommendation (non-binding):** re-confirm Multi-Portfolio Support, Mobile App and BLG-TECH-05 Prometheus (single-user scale and a web-only product are unchanged; no operational need has arisen). Flag four for review at the next `run roadmap`: Position Correlation Analysis (partly overlapped by Market Correlation Analysis, shipped v2.7); Backtesting Module (overlaps PO-05 Lightweight Replay Mode on the roadmap); Full Compliance Scoring (the Arc 5 composite compliance score shipped v4.1, so the item may be done or need redefining); Customisable Dashboard Layout (the Site Structure & Usability programme is redesigning the Dashboard, the right point to decide). `initiative_register.md` unchanged; the decision record is the next `run roadmap`'s input (AC 2 post-merge, BLG-GOV-408).
- **Owning authority:** Product Owner
- **Unblock criteria:** a dated ruling per initiative (re-confirm or flag, with reason) recorded in this escalation's resolution. The engine then writes `docs/product/decisions/priority3-deferred-sunset-review--2026-11-05.md`.
- **SLA due-by:** 2026-11-06T13:56:47Z (24h — lifecycle/scope)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-11-05T14:38:30Z):** Product Owner ruling, given in-session by the user, dated 2026-11-05: engine recommendation accepted as drafted. Re-confirmed deferred: Multi-Portfolio Support, Mobile App, BLG-TECH-05 Prometheus. Flagged for the next `run roadmap`: Position Correlation Analysis, Backtesting Module, Full Compliance Scoring, Customisable Dashboard Layout. `initiative_register.md` unchanged; AC 2 carry-forward tracked by BLG-GOV-408. Record: `docs/product/decisions/decisions--2026-11-03__release-v9.15--ST-45-priority3-deferred-sunset-review.md`.
