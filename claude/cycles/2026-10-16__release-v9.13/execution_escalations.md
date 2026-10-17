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
- **Disposition:** Open

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
- **Disposition:** Open
