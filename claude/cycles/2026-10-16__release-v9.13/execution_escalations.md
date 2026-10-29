Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-16

# Execution Escalations — 2026-10-16__release-v9.13

## ESC-EXEC-20261016-01

- **Raised at:** 2026-10-16T11:05:32Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-16__release-v9.13
- **Step:** STEP 3.1.D (EPIC-01 execution loop, raised at sprint start per `sprint_backlog.md` ST-05 Notes)
- **ST/EPIC item:** ST-05 / EPIC-01 (BLG-GOV-391)
- **Trigger type:** Strategy
- **Blocking statement:** Since v6.2 (`BLG-FEAT-47`), `signal_service.py::generate_rebalance_exit_signals` recommends exiting every open position outside the current top-5 momentum ranking on the last trading day of each month, and `rebalance-exit.yml` runs it. `strategy_rules.md` §8 allows "exactly three" exit conditions (stop-loss, market risk-off, manual), and rebalancing is not one of them. ST-05's AC 1 needs a dated Strategy Rules & System Intent Owner determination: **(A)** the rebalance exit enters §8 under §12.3 change control, written under the RISK-02 route (named `strategy_rules.md` write authorised for ST-05) with a Change Log row, and the interim label is removed in the same change; or **(B)** the signal is withdrawn: `rebalance-exit.yml` and the signal path are retired, and the `exit_rebalance` card state with them.
- **Engine recommendation (non-binding):** none on the branch, which is a strategy-boundary call. The interim "Outside §8 — informational" label (AC 2, `rebalance-exit-interim-label/decision_record.md`) proceeds regardless and is removed under either outcome.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** a dated determination, (A) or (B), recorded in this escalation's resolution and in ST-05's QA evidence. The engine then applies it: (A) the §8 amendment with its Change Log row and the label removal; (B) retiring `rebalance-exit.yml`, the signal path and the label.
- **SLA due-by:** 2026-10-19T11:05:32Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-10-16T12:16:18Z):** Strategy Rules & System Intent Owner ruling, agent-mediated per `execution_prompt.md` §5.3 (user-directed: the user chose an agent-mediated ruling in-session on 2026-10-16), dated 2026-10-16: **(A) Approved — the month-end rebalance exit enters §8 as §8.4.** Grounds, spot-checked by the engine: the production backtest already rebalances monthly (`strategy_engine.py:69` `rebalance_freq: "ME"`; `:339-345` exits holdings no longer in the top-n on rebalance dates, with no grace check), and BLG-FEAT-47 came from a `production_strategy.py` gap analysis, so §8 omitted a validated rule; withdrawing (B) would move live further from the backtest (charter §1, §9-§10; `strategy_rules.md` §11, §12.3). Binding conditions, as applied by ST-05: (1) §8.4 text added after §8.3; (2) §8 lead-in "exactly four"; (3) §6.3, §10, §11, §12.2 consequential edits; (4) live code: ranking independent of signal status, risk-off positions skipped (§8.2 precedence), no signals and an alert (HTTP 503 failing `rebalance-exit.yml`) when today's run is missing, with pytest RX-06..RX-09; (5) the holiday deviation recorded in §8.4 and filed as BLG-BE-187; (6) seventh exit reason filed as BLG-SPEC-206 (backlog option); (7) interim label retired before shipping (`signals.md` v0.6, Playwright SC-RB-04); (8) v1.17 under RISK-02 with a §16-format Change log row, registered in `strategy_version_registry.py`, parameter ledger rows added, §15 grep re-run (33 citations, all dated; 0 actionable); (9) nothing in the do-not-remove list was removed. One wording correction by the engine: the ruling said "that day's completed screener run", but the ranking `generate_rebalance_exit_signals` reads is written by `POST /signals/generate` (the entry-signal run in `daily-snapshot.yml`), so §8.4 says "momentum signal run". ST-05 reclassified `autonomous` and continued.

## ESC-EXEC-20261017-01

- **Raised at:** 2026-10-17T15:21:52Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-16__release-v9.13
- **Step:** STEP 3.1.D (EPIC-06 execution loop)
- **ST/EPIC item:** ST-40 / EPIC-06 (BLG-GOV-387)
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-40 corrects the v9.8–v9.10 rolling-aggregate line in `claude/roadmap/role_share_history.md`. It says 19 of v9.10's 21 Owner values are compound strings. `scripts/compute_role_share_history.py claude/cycles/2026-10-06__release-v9.10/sprint_backlog.md` (re-run 2026-10-17) lists 21 Owner values, and 4 of them have no `"; "` separator (`Strategy Rules & System Intent Owner (ruling)`, `Infrastructure & Operations Owner`, `QA & Testing Owner`, `Frontend Specifications & UX Documentation Owner`), so 17 are compound. The write is authorised by the §7 plan-authorised named-file rule (case a, `sprint_backlog.md` Named-file writes). The story stays `delegated_decision` as the slice states (`ESC-CLOSE-20261006-01`), so its owner must approve the corrected line before it lands. The proposed edit changes only that line's figure, adding an inline correction note, plus the file's `Last Updated` header. No other row, figure or method changes.
- **Engine recommendation (non-binding):** approve the correction as staged.
- **Owning authority:** PMO Lead
- **Unblock criteria:** A dated PMO Lead approval (agent-mediated per §5.3 permitted), recorded in this escalation's resolution. The engine then commits ST-40.
- **SLA due-by:** 2026-10-18T15:21:52Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-10-17T15:23:13Z):** PMO Lead approval, agent-mediated per `execution_prompt.md` §5.3, dated 2026-10-17: **Approved**, first pass. Charter grounds: `pmo_lead.md` §5.1, §5.2, GI-3, GI-5. The count was checked independently and the working is shown: the script gives 19 distinct Owner strings covering 21 stories (one string has 3 stories, 18 have 1 each). 4 have no `"; "` separator (`Strategy Rules & System Intent Owner (ruling)`, `Infrastructure & Operations Owner`, `QA & Testing Owner`, `Frontend Specifications & UX Documentation Owner`, 1 each), so 21 − 4 = 17 are compound. The old "19" appears to be the number of distinct strings, which is a different measure. The diff touches only that line's figure, with an inline note, and the `Last Updated` header. The header holds the current entry plus 2 prior entries (CLAUDE.md §2). The write records a figure and decides nothing (named-file rule, case a). ST-40 is reclassified `autonomous` and committed.

## ESC-EXEC-20261017-02

- **Raised at:** 2026-10-17T16:06:04Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-16__release-v9.13
- **Step:** STEP 3.1.D (EPIC-02 execution loop, raised at EPIC start per `sprint_backlog.md` ST-06 Dependencies: "ruling: reject with 400 or floor (first sub-step)")
- **ST/EPIC item:** ST-06 / EPIC-02 (BLG-BE-180)
- **Trigger type:** Strategy
- **Blocking statement:** `add_position()` rejects a *typed* ATR when 5 × ATR ≥ entry (v9.12 ST-18), but a *fetched* or 2%-fallback ATR has no such check: `calculate_initial_stop()` can return a stop at or below zero and save stores it, and Trade Entry's preview shows the negative stop. ST-06 AC 1 needs a Strategy Rules & System Intent Owner ruling: **(A) reject** — `POST /portfolio/position` returns 400 when entry − 5 × (fetched or fallback) ATR ≤ 0; Trade Entry shows "No valid stop" and disables Submit (`initial-stop-at-or-below-zero/decision_record.md` §2.1); no `strategy_rules.md` change, since §5 already gives no stop for such an entry; or **(B) floor** — store a floored stop (the ruling must state the floor rule, e.g. "1% of the entry price") and record it in `strategy_rules.md` §5 under the RISK-02 route with a Change Log row; Trade Entry shows the floored value and caption (§2.2).
- **Engine recommendation (non-binding):** none on the branch; it decides stop behaviour, which is a strategy call. Note for the Owner: (A) needs no rule change and matches the typed-ATR path; (B) introduces a new stop rule not in the backtest.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** a dated ruling, (A) or (B) with the floor wording, recorded in this escalation's resolution. The engine then implements it with the backend test and Playwright scenario the AC names.
- **SLA due-by:** 2026-10-20T16:06:04Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-10-17T16:16:44Z):** Strategy Rules & System Intent Owner ruling, agent-mediated per `execution_prompt.md` §5.3 (user-directed: the user chose an agent-mediated ruling in-session on 2026-10-17), first pass: **Approved (A) — reject, no floor.** Grounds: §5 gives no stop when 5 × ATR ≥ entry, so rejecting adds no rule, while a floor would be a new §12.3 rule (charter §2, §7); the same outcome whatever the ATR source, matching v9.12's typed-ATR 400 (charter §3); such an entry has ATR ≥ 0.2 × entry, outside the strategy; neither branch is in the backtest (`strategy_engine.py` takes the unfloored stop), and (A) adds no new mechanism (charter §9–§10). Arithmetic shown: fallback ATR 0.02E gives stop E − 5 × 0.02E = 0.90E > 0, so only a fetched ATR can trigger it. Binding conditions, as applied by ST-06: (1) one guard in `add_position()` after the ATR is final, covering fetched and fallback, `INITIAL_ATR_MULTIPLIER`, `>=`; (2) 400 message names the ATR and source, states 5 × ATR ≥ entry so §5 gives no stop, quotes the entry, and omits the pence/cents hint; (3) typed-ATR guard unchanged; (4) Trade Entry per decision record §2.1 ("No valid stop", `initial-stop-invalid`, `role=status`, Submit disabled, Risk "—", no stop to sizing, save 400 shown), Branch B deleted from `position_form.md`; (5) backend tests incl. the equality boundary and the fallback 0.9 × E case; (6) Playwright; (7) no `strategy_rules.md` change (the RISK-02 write authorisation for ST-06 is not used). Finding (non-blocking): the backtest still takes an unfloored ≤ 0 stop for such entries; not changed by this ruling. ST-06 reclassified `autonomous`.

## ESC-EXEC-20261017-03

- **Raised at:** 2026-10-17T16:06:04Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-16__release-v9.13
- **Step:** STEP 3.1.D (EPIC-02 execution loop, raised at EPIC start per `sprint_backlog.md` ST-07 Dependencies)
- **ST/EPIC item:** ST-07 / EPIC-02 (BLG-BE-161)
- **Trigger type:** Strategy
- **Blocking statement:** `strategy_rules.md` §6.3 (v1.15+) says the stored stop is not recalculated or ratcheted during the 10-day grace period. The live paths follow it; the legacy standalone tool `backend/position_manager.py` still applies `max(current_stop, current_price − 5 × ATR)` in grace. It is off the live path and already a named exception for §7.2's multipliers. ST-07's AC needs the Owner's choice: **(A) align** — `position_manager.py` stops trailing during grace, with a unit test; no strategy change (the sprint plan's default, RISK-03); or **(B) exception** — `strategy_rules.md` names it as an exception next to the §7.2 one, with the Owner's sign-off, under the RISK-02 route.
- **Engine recommendation (non-binding):** (A). It removes a divergence rather than documenting one, needs no `strategy_rules.md` bump, and the tool is not on the live path.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** a dated choice, (A) or (B), recorded in this escalation's resolution.
- **SLA due-by:** 2026-10-20T16:06:04Z (72h — Strategy)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-10-17T16:11:36Z):** User decision for the Strategy Rules & System Intent Owner (human, in-session, 2026-10-17, via the engine's ruling question): **(A) align the code.** `backend/position_manager.py` no longer recalculates or ratchets the stop while `holding_days < min_hold_days` (§6.3); the stop trails as before after grace. No `strategy_rules.md` change. Unit tests `tests/test_stop_reconciliation.py::TestPositionManagerGracePeriodStop` (in-grace frozen, last grace day frozen, post-grace trails, in-grace price below stop holds); the two in-grace tests fail against the previous code. ST-07 reclassified `autonomous`.

## ESC-EXEC-20261017-04

- **Raised at:** 2026-10-17T16:06:04Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-16__release-v9.13
- **Step:** STEP 3.1.D (EPIC-02 execution loop, raised at EPIC start per `sprint_backlog.md` ST-08 Dependencies)
- **ST/EPIC item:** ST-08 / EPIC-02 (BLG-API-07)
- **Trigger type:** Lifecycle
- **Blocking statement:** `POST /settings` and `PATCH /settings/{settings_id}` still accept and store `min_hold_days`, `atr_period`, `atr_multiplier_initial` and `atr_multiplier_trailing`, which no stop path reads since v9.10 (§11 fixed source). A caller gets a 200 and cannot tell the change was ignored. ST-08 AC 1 needs the API Contracts & Documentation Owner's choice: **(A) 400** naming the §11 rule when a write includes any of the four fields (the sprint plan's default, RISK-03); or **(B) deprecation warning** — the write succeeds and the response carries a warning field listing the ignored fields. Either way `settings_endpoints.md` and `openapi.yaml` change in the same commit. Engine finding for the Owner: the Settings page already holds these four as `FIXED_STRATEGY_FIELDS` (`src/pages/Settings.js:19`) and seeds them with the §11 constants (lines 48–51); under (A) the engine will confirm whether the page sends them on save and stop it doing so in the same story (design gate: a defect, not a design change).
- **Engine recommendation (non-binding):** (A), the planned default: it makes an ignored write impossible to miss.
- **Owning authority:** API Contracts & Documentation Owner
- **Unblock criteria:** a dated choice, (A) or (B), recorded in this escalation's resolution.
- **SLA due-by:** 2026-10-18T16:06:04Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-10-17T16:16:44Z):** API Contracts & Documentation Owner ruling, agent-mediated per `execution_prompt.md` §5.3 (user-directed, in-session 2026-10-17), first pass: **Approved (A) — 400 naming §11.** Grounds: a 200 that silently ignores a write is neither accurate nor developer-friendly (charter §1); no success response in `docs/specs/api_contracts/` carries a request-warnings field, while `conventions.md` already maps invalid input to 400, so (A) needs no new convention; no first-party caller breaks (charter §4): the Settings page strips `FIXED_STRATEGY_FIELDS` before saving (`src/pages/Settings.js:19`, `:129-133`, asserted by `settings-strategy-parameters-fixed.spec.js`), and no script or workflow posts them. Binding conditions, as applied by ST-08: (1) both handlers return `JSONResponse` 400 `{status, message}` before the `try`; (2) message names `strategy_rules.md §11` and §12.3 and lists the offending fields in the order min_hold_days, atr_period, atr_multiplier_initial, atr_multiplier_trailing; (3) a field counts only when in `model_fields_set` and non-null; (4) check in the handlers, no pydantic validator, fields kept in `SettingsRequest`, a mixed body rejected whole; (5) `settings_endpoints.md` v1.6.0; (6) `openapi.yaml` descriptions and version; (7) no frontend change; (8) new backend tests; (9) `tests/test_main_500_no_raw_exception_text.py` and `tests/test_settings_create_and_plan_snapshot.py` updated. ST-08 reclassified `autonomous`.

## ESC-EXEC-20261027-01

- **Raised at:** 2026-10-27T08:48:35Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-16__release-v9.13
- **Step:** STEP 3.1.D (EPIC-03 execution loop, raised at EPIC start per `sprint_backlog.md` ST-16 Notes)
- **ST/EPIC item:** ST-16 / EPIC-03 (BLG-AI-18)
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-16 AC 1 needs the AI Compliance & Governance Officer to sign off extending the `ESC-EXEC-20261013-01` stop-time ruling to chat: `ai_chat()` passes `context_opts.ticker` as `own_ticker` to `_append_missing_stop_times`, so a ticker-focused reply such as "Your stop is at £450" is attributed to the focused position and gets its code-written recalculation note, instead of being counted `unattributed` with no note. The same story case-normalises `own_ticker` (upper case, `.L` folded per ST-15) against the position tickers. Choice: **(A) extend** — attribute a stop sentence with no named ticker to the focused ticker, but only when that ticker is an open position (a non-held focus ticker adds nothing); a sentence that names another held ticker is attributed to that ticker as today, plus the focused one. **(B) extend narrowly** — attribute to the focused ticker only when the sentence names no held ticker at all. **(C) decline** — keep chat as `unattributed`. ST-16 AC 4 (Head of UX & Design answer on visible "system-added" styling) is asked separately.
- **Engine recommendation (non-binding):** (B). It covers the common case the item names without attributing a sentence about another holding to the focused one.
- **Owning authority:** AI Compliance & Governance Officer
- **Unblock criteria:** a dated choice, (A), (B) or (C), recorded in this escalation's resolution.
- **SLA due-by:** 2026-10-28T08:48:35Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-10-27T08:54:27Z):** AI Compliance & Governance Officer ruling, agent-mediated per `execution_prompt.md` §5.3, first pass: **Approved (B) — extend narrowly.** Grounds: charter §4.1 (no silent expansion of AI authority) and §7 (explainability); (A) could attach the focused ticker's note to a sentence about another holding. Binding conditions: (1) the focus ticker is normalised with ST-15's helper and compared to normalised position tickers; the note uses the position's stored ticker and `_stop_recalculated_label()`; (`_CONTEXT_TICKER_PATTERN` already rejects a lower-case focus with 422, so for chat normalisation matters for `.L` folding); (2) held positions only — a non-held focus ticker behaves as today; (3) a sentence is attributed to the focus ticker only when it names no held ticker; (4) briefing actions keep their `own_ticker` behaviour, only case/`.L`-normalised (ST-16 AC 3); (5) the warning line adds `attribution=focus` when the focus rule supplied the ticker, never response text; (6) `compliance_check_result` values unchanged; (7) no prompt change from ST-16 (ST-19's separate v1.2 bump is for the cash wording); `ESC-EXEC-20261013-01` conditions 1, 2, 4 and 8 still apply; `ai_endpoints.md` describes the focus rule. ST-16 AC 4 (Head of UX & Design, agent-mediated, same pass): **Yes** — the appended note needs visible "system-added" styling, filed as a separate backlog item (P3, provisional; the `[STOP-TIME-MISSING]` rate, not queried here because a live DB query needs the user's permission, sets its priority before planning). ST-16 reclassified `autonomous`.

## ESC-EXEC-20261027-02

- **Raised at:** 2026-10-27T08:48:35Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-16__release-v9.13
- **Step:** STEP 3.1.D (EPIC-03 execution loop, raised at EPIC start per `sprint_backlog.md` ST-17 Notes)
- **ST/EPIC item:** ST-17 / EPIC-03 (BLG-AI-16)
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-02 (v9.12) drops briefing actions naming a ticker outside the context, but the `summary` prose is returned unchecked. ST-17 scans the summary for upper-case ticker-like tokens not among the open positions or context signals (normalised per ST-15; known non-ticker words such as SPY, FTSE, MA200, UK, US, EXIT, ENTER, MONITOR, HOLD, P&L excluded). AC 1 needs the AI Compliance & Governance Officer to choose the action on a hit: **(A) log and count** — summary returned unchanged, result recorded; **(B) code-written caveat** — append "(Note: <TICKER> is not in your portfolio or today's signals.)" after the model text, the same form as the stop-time note; **(C) regenerate once**, then (A) or (B) if the retry also fails. Whichever is chosen, the result is recorded alongside the stop-time result in `claude_audit_log.compliance_check_result` (AC 4).
- **Engine recommendation (non-binding):** (B). It tells the reader at the point of use, follows the ruled stop-time pattern (code-authored, model text never edited), and costs no extra model call.
- **Owning authority:** AI Compliance & Governance Officer
- **Unblock criteria:** a dated choice, (A), (B) or (C), recorded in this escalation's resolution.
- **SLA due-by:** 2026-10-28T08:48:35Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-10-27T08:54:27Z):** AI Compliance & Governance Officer ruling, agent-mediated per `execution_prompt.md` §5.3, first pass: **Approved (B) — code-written caveat, also logged and counted.** Same pattern as the stop-time ruling: the reader is told at the point of use, model text is never edited, no extra model call. Binding conditions: (1) ticker-like token regex `(?<![A-Za-z0-9_.&$£])[A-Z][A-Z0-9_]{1,14}(?:\.[A-Z]{1,2})?(?![A-Za-z0-9_&])` over the raw summary; (2) a token is known if, after ST-15 normalisation, it is an open position or a top signal passed in, or appears as a whole word in the context sent to the model, or is in a tested module constant `_NON_TICKER_WORDS` (at least UK, US, USD, GBP, GBX, EXIT, ENTER, MONITOR, HOLD, ATR, MA, ETF, AI, UTC); (3) caveat after any stop-time notes, once per token in first-appearance order: `(Note: <TICKER> is not one of your open positions or today's top signals.)`, or for several `(Note: <T1>, <T2> are not among your open positions or today's top signals.)`; (4) `summary` only; (5) `compliance_check_result`: unchanged on no hit; `ticker_outside_context_appended` when stop-time is `pass`; otherwise `<stop value>+ticker_outside_context_appended`; scan error `<stop value>+ticker_check_error`; (6) one warning per hit (endpoint, field, token, `action=caveat_appended`, prompt version), never response text; (7) fails open; (8) sampling hook gets raw output; no prompt change (`BRIEFING_PROMPT_VERSION` stays v1.3); docstring and contract describe the caveat. ST-17 reclassified `autonomous`.

## ESC-EXEC-20261027-03

- **Raised at:** 2026-10-27T08:48:35Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-16__release-v9.13
- **Step:** STEP 3.1.D (EPIC-03 execution loop, raised at EPIC start per `sprint_backlog.md` ST-18 Notes)
- **ST/EPIC item:** ST-18 / EPIC-03 (BLG-AI-15)
- **Trigger type:** Lifecycle
- **Blocking statement:** `POST /ai/journal-summary` runs no output-language check; its staging output once ended "...or if stop placements need adjustment". ST-18 adds a post-generation check reusing the debrief's `scan_prescriptive` plus a pattern for wording that suggests changing stops, sizing or setups. AC 1 needs the AI Compliance & Governance Officer to choose the failure action: **(A) regenerate once, then a code-written fallback** (summary `null` with an explanatory `message`, the debrief / monthly-narrative pattern); **(B) return the text with the result logged**. Either way each call's result goes in `claude_audit_log.compliance_check_result`, and `JOURNAL_SUMMARY_PROMPT_VERSION` is bumped if the prompt text is tightened.
- **Engine recommendation (non-binding):** (A). It matches the two other AI narrative features, so text suggesting stop or sizing changes never reaches the user.
- **Owning authority:** AI Compliance & Governance Officer
- **Unblock criteria:** a dated choice, (A) or (B), recorded in this escalation's resolution.
- **SLA due-by:** 2026-10-28T08:48:35Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-10-27T08:54:27Z):** AI Compliance & Governance Officer ruling, agent-mediated per `execution_prompt.md` §5.3, first pass: **Approved (A) — regenerate once, then a code-written fallback.** Grounds: charter §4.3 consistency with the debrief and monthly narrative; wording suggesting stop or sizing changes is the §13 risk the check exists for. Binding conditions: (1) fail on `scan_prescriptive` or a new `_TRADING_CHANGE_RE` — subject (stops, stop-loss, stop placement/level/distance, position size/sizing, setups) then within 40 characters a present-tense or modal word (needs, should, ought, requires, warrants, may/might need, could use) then within 25 characters a change verb (adjust, change, tighten, widen, loosen, revise, revisit, reconsider, rethink, review, modify, refine, move, reduce, increase, cut, lower, raise), case-insensitive, within one sentence; past-tense needed/required excluded on purpose; (2) categories `prescriptive`, `trading_change`; `compliance_check_result` per model call: `pass`, `pass_on_regenerate`, `fail_regenerate:<cats>`, `fail_fallback:<cats>`; `model_call_failed` unchanged; (3) fallback `{"summary": null, "model": null, "message": "The AI summary was withheld because it did not pass the advisory-language check. Your journal notes are unchanged; please try again later."}`; (4) sampling hook gets each attempt's raw output; logs carry categories only; (5) prompt adds "Describe what the notes record; do not suggest changing stops, position sizing or setups." and `JOURNAL_SUMMARY_PROMPT_VERSION` v1.0 → v1.1; (6) `ai_endpoints.md` and `ai_s13_boundary_test_suite.md` updated; tests cover the staging sentence, a prescriptive one, a descriptive pass, pass on regeneration and the fallback. The ruling's own sentence-classification claim is re-verified by the ST-18 tests, not relied on alone (LL-v8.6-P3-01). ST-18 reclassified `autonomous`.

## ESC-EXEC-20261027-04

- **Raised at:** 2026-10-27T21:17:56Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-16__release-v9.13
- **Step:** STEP 3.1.D (EPIC-05 execution loop)
- **ST/EPIC item:** ST-33 / EPIC-05 (BLG-OPS-77)
- **Trigger type:** Lifecycle
- **Blocking statement:** ST-33 AC 3 needs the accepted-risk statement in `docs/operations/data_provider_risk_assessment.md` §4 signed off by the Infrastructure & Operations Owner and the FinOps & Resource Architect. The statement accepts Yahoo Finance as the sole source for UK prices and bars, GBP/USD FX, the FTSE regime and reference data, and Alpaca's free tier as the primary US source, on cost grounds. It does not accept the fail-open regime or frozen FX as permanent; follow-ups BLG-BE-192/193/194 and BLG-FE-234 are filed.
- **Engine recommendation (non-binding):** accept as drafted.
- **Owning authority:** Infrastructure & Operations Owner; FinOps & Resource Architect
- **Unblock criteria:** both roles' decisions, dated, recorded in §4 of the assessment and in this escalation's resolution.
- **SLA due-by:** 2026-10-28T21:17:56Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-10-27T21:21:14Z):** Infrastructure & Operations Owner and FinOps & Resource Architect, each agent-mediated per `execution_prompt.md` §5.3. First pass: both Blocked (I&O: the System Status Yahoo check reports healthy during an outage, so §4's interim guidance and §5 condition 1 could not be acted on; FinOps: §4 gave no cost basis). Findings applied in the working tree, then retry 1: both **Approved — accept as drafted**. §2 gains the false-healthy monitoring row, §3 QW-6 and BLG-OPS-194; §4 names Twelve Data Grow at $79/month (XLON EOD, vendor site checked 2026-10-27) against current spend; §5 gains a price trigger. Non-blocking notes applied: BLG-OPS-194 covers the regime case; §4 notes the 5-minute FX cache lag. Open note: no repo document records Render Starter's dollar fee. Recorded in the assessment's §4 sign-off table at `afcd8906`. Human confirmation by either role may supersede.

## ESC-EXEC-20261028-01

- **Raised at:** 2026-10-28T21:05:55Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-10-16__release-v9.13
- **Step:** STEP 3.1.D (EPIC-04 execution loop, raised at EPIC start per `sprint_backlog.md` ST-27 Dependencies)
- **ST/EPIC item:** ST-27 / EPIC-04 (BLG-QA-211)
- **Trigger type:** Lifecycle
- **Blocking statement:** `real_database_imports()` (`tests/_real_database.py`, ST-14 v9.9) restores `sys.modules["database"]` after its block, and the conftest leak guard enforces that. But `main`, the routers and the services imported inside the block stay in `sys.modules`, bound to the real `database` module, for the rest of the pytest session. A later file importing one of those services gets the real-bound copy. The suite passes because tests patch at the service level, but the guard does not detect this coupling. ST-27's AC needs the Director of Quality to choose: **(A) accept and document** — record the decision in `tests/_real_database.py` (what persists, why eviction is not done: other files' string `patch()` targets resolve against the cached modules, and how a later test stays safe: patch the service-level name, never rely on `database` being the stub inside a real-bound service) and state in the conftest guard's comment what it does not cover; **(B) eliminate** — move every Category B file to a pattern that does not populate the shared cache (e.g. one session-scoped app fixture shared by every TestClient file, or evict and re-import per file), so no real-bound module survives past the importing file.
- **Engine recommendation (non-binding):** (A). The story is P4 and sized at 0.5 day; (B) touches every Category B test file and their `patch()` targets, which is well beyond that budget and risks the collection-order fragility ST-14 removed. (A) makes the known limit visible where a test author will read it.
- **Owning authority:** Director of Quality (with QA & Testing Owner)
- **Unblock criteria:** a dated choice, (A) or (B), recorded in this escalation's resolution; for (A), the reviewed wording in `tests/_real_database.py` and the conftest guard comment.
- **SLA due-by:** 2026-10-29T21:05:55Z (24h — Lifecycle)
- **Blocks execution:** No
- **Disposition:** Resolved
- **Resolution summary (2026-10-28T21:21:09Z):** Director of Quality ruling, agent-mediated per `execution_prompt.md` §5.3. First pass: **Blocked**. Choice (A) was approved, on charter §4.5 (trade-offs explicit and documented) and §4.1 (no normalisation of undocumented behaviour); per §5, (B) would be a 31-file architecture change, out of proportion for a P4 item. Two factual errors in the draft were blocking. (1) The first importer at collection is `tests/test_api_call_attribution.py`, not `tests/test_api_contracts.py`; this blocking statement and BLG-QA-211's Problem make the same error and are corrected by this record. (2) The session holds a mix: 22 main/router/service modules real-bound and 17 stub-bound after collection (probe run with a stub `DATABASE_URL`). The 67 function-level `from database import` statements in `backend/` resolve to the stub at call time. Findings 1–3, 5 and 6 were applied. Retry 1: **Approved**, plus an optional clarification ("first block run at collection"), which was applied. Evidence: 31 Category B files; `routers/strategy_benchmark.py:17` uses `import database`. The reviewed wording is in `tests/_real_database.py` ("Known limit") and the `conftest.py` leak-guard comment ("Not covered"). ST-27 reclassified `autonomous`.
