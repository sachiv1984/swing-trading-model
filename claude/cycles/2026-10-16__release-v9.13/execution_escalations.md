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
