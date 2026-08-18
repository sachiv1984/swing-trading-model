Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-18

# QA Evidence Log — EPIC-02 (Trade Sizing & Post-Trade Intelligence, Sprint 1 subset)

**EPIC:** EPIC-02 — Trade Sizing & Post-Trade Intelligence (Sprint 1 subset)
**Cycle:** 2026-08-17__release-v8.9
**Sprint goal:** Ship v8.9: eliminate the two live risk-management stop-price defects on open positions (breakeven-floor ratchet, currency-basis mismatch) and deliver the sector-aware position sizing, pre-commit risk simulator, AI post-trade debrief, and in-app backtesting foundations of the Trade Intelligence Expansion — while clearing this cycle's reliability, QA, ops, and governance debt.
**Test scenarios used:** tests/test_sizing_concentration.py (9 scenarios); tests/e2e/position-sizing-concentration.spec.js (3 scenarios, V-SIZE-01/02/03); tests/test_sizing_heat_impact.py (5 scenarios); tests/e2e/what-if-sizing-preview.spec.js (4 scenarios, V-WHATIF-01/02/02b/03); tests/test_backtest_rule_service.py (11 scenarios); tests/e2e/backtest-rule-change.spec.js (5 scenarios, V-BACKTEST-01..05)

**Scope note:** ST-06 (Automated AI Post-Trade Debrief, BLG-FEAT-90) is a Sprint 2 subset of this EPIC per sprint_backlog.md's Multi-Sprint Gate Note — gated on ST-23 reaching `done` with a PASS/CONDITIONAL determination, which it has. ST-06 is out of scope for this PR and this QA evidence log; it will be evaluated under its own EPIC-02 Sprint 2 execution pass.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-23 | `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md` | §13 System Boundary Review for ST-06 (AI Post-Trade Debrief) — Determination: CONDITIONAL, 9 binding conditions, including a Condition 9 requiring output-side (not just prompt-instruction) enforcement of the "pattern-surfacing, not prescriptive" focus-area constraint, added after a first-pass agent-mediated review caught the gap. | §13 pre-assessment document produced; assessment addresses determinism/own-data-only/non-predictive/decision-support-only against the "suggested focus area" output specifically; binding conditions documented; explicit Determination recorded; Strategy Rules & System Intent Owner sign-off | Pass | None |
| ST-04 | `docs/design/2026-08-17__release-v8.9/correlation-sector-concentration-sizing/decision_record.md`; `backend/services/concentration_service.py`; `backend/services/sizing_service.py#_apply_concentration_adjustment` | `POST /portfolio/size` reduces or flags suggested size based on the user's existing open-position sector concentration, reusing (not redefining) `strategy_rules.md §4.2.2`'s canonical 30% threshold; `concentration_adjusted`/`concentration_reason` fields added; amber inline note in `PositionSizingWidget.js`. | Sizing reflects existing open-position sector concentration, not just the candidate ticker's own volatility; visible reason when reduced or flagged; regression test confirms two same-sector positions produce a smaller second size than two uncorrelated ones would; Backend Engineering Patterns Owner sign-off | Pass | None |
| ST-05 | `docs/design/2026-08-17__release-v8.9/what-if-sizing-risk-simulator/ux_spec.md`; `docs/specs/frontend/pages/trade_plan.md#5d`; `src/components/trades/WhatIfSizingPreview.js` | New "What-If Sizing Preview" panel on the Trade Plan form, reusing `POST /portfolio/size` (same endpoint as `PositionSizingWidget`); extracted `calculate_prospective_heat` from `prospective_heat.py` into `portfolio_service.py`, shared to add `heat_impact_percent`. Filed and resolved same-story: `DEV-v8.9-ST05-01` (§5d.1 presence-gate self-contradiction) and `DEV-v8.9-ST05-02` (R at Risk missing FX conversion, caught by sign-off review). | User can adjust stop distance/entry price and see position size, R at risk, portfolio heat impact update live before saving; preview value matches what is saved (same endpoint, by construction); no DB write occurs from interacting with the preview alone | Pass | DEV-v8.9-ST05-01, DEV-v8.9-ST05-02 (both resolved same-story) |
| ST-07 | `docs/design/2026-08-17__release-v8.9/in-app-backtesting-engine/ux_spec.md`; `docs/specs/frontend/pages/strategy_benchmark.md#7.6`; `backend/services/backtest_rule_service.py` | New "Backtest Rule Change" tab on Strategy Benchmark page — runs a candidate `strategy_rules.md` parameter change against a bounded historical window (20 tickers, 4 years) entirely in-app, compares against the live rule set over the identical universe/window, persists each run. RISK-02's contingency exercised: full `production_strategy.py` reuse (100+ tickers/8yr/90min CI budget) found infeasible for a synchronous request; algorithm ported (not imported, for concurrency safety) instead. | Candidate rule change runs against historical data from inside the app, no external script step; output includes win rate, R-multiple distribution, drawdown vs. live rule set; each run persisted with audit detail; Strategy Rules & System Intent Owner sign-off | Pass | None |

**QA test coverage:**
- Scenarios run: `tests/test_sizing_concentration.py` (9/9 pass), `tests/test_sizing_heat_impact.py` (5/5 pass), `tests/test_backtest_rule_service.py` (11/11 pass, including a full end-to-end run against synthetic price data) — full backend suite `backend/.venv/bin/python3 -m pytest tests/` 1195 passed / 5 skipped, 0 failed, 0 regressions (run repeatedly across all 3 stories' commits). `tests/e2e/position-sizing-concentration.spec.js` (3/3), `tests/e2e/what-if-sizing-preview.spec.js` (4/4), `tests/e2e/backtest-rule-change.spec.js` (5/5) — all run live against `npm start`, all passing.
- Regression areas checked: `backend/services/sizing_service.py::size_position()` response shape (additive fields only — `concentration_adjusted`, `concentration_reason`, `heat_impact_percent`); `PositionSizingWidget.js` existing auto-fill behaviour (pre-existing `smoke-critical-paths.spec.js`, 3/3 re-verified); `GET /portfolio/prospective-heat`'s response shape after the `calculate_prospective_heat` extraction (pre-existing `test_fx_audit_trail_completeness.py`, `test_api_contracts.py`, `test_portfolio_integration.py` patch-target migrations, 95 tests re-verified passing); `TradePlan.js` existing form behaviour (pre-existing `trade-plan.spec.js` 52 tests + `entry-checklist.spec.js` 11 tests re-verified passing); `StrategyBenchmark.js` existing Benchmark/Version Comparison tabs (pre-existing `strategy-benchmark.spec.js` 23 tests + `si04-version-comparison.spec.js` 5 tests re-verified passing).
- Known deviations: DEV-v8.9-ST05-01, DEV-v8.9-ST05-02 (`trade_plan.md#Known Deviations`) — both filed and resolved in the same story. No other deviations found — ST-23, ST-04, and ST-07 deviation checks completed with nothing to file.

**Frontend testing gate (execution_prompt.md §3.2.A):** ST-04, ST-05, and ST-07 all introduce frontend-visible changes (`PositionSizingWidget.js`, `WhatIfSizingPreview.js` (new), `StrategyBenchmark.js`). Each is covered by dedicated Playwright scenarios (V-SIZE-01..03, V-WHATIF-01..03, V-BACKTEST-01..05 respectively), all run live against a real `npm start` instance and passing — not merely code-reviewed. The BLG-GOV-19 autonomous class sign-off does not apply to this EPIC (criterion 3 unmet — multiple `src/components/**`/`src/pages/**` files modified) — Standard Sign-Off Block with Mixed-Class Signer Format used below.

**Governance self-consistency check (execution_prompt.md §3.2.A, LL-v8.5-P3-01):** No story in this EPIC bumped `OPERATIONAL_GUIDE.md`'s version — not applicable this EPIC.

---

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object — N/A, all new frontend code uses the `api.*` wrapper (`api.portfolio.size`, `api.backtestRuleChange.*`)

> **Mixed-Class EPIC Signer Format (ST-11 / LL-v5.2-P4-01):** EPIC-02 contains `delegated_decision` (ST-23), `delegated_backend` (ST-04, ST-07), and `delegated_frontend`-reclassified-to-engine (ST-05, per LL-v2.3-CL-01) stories — agent-mediated format required.

- Signed off by: Sprint Execution Engine (agent-mediated, Strategy Rules & System Intent Owner role — §5.3)
  Sprint Execution Engine (agent-mediated, Backend Engineering Patterns Owner role — §5.3)
  Sprint Execution Engine (agent-mediated, Head of Engineering role — §5.3)
  Sprint Execution Engine (agent-mediated, Frontend Specifications & UX Documentation Owner role — §5.3)
- Date: 2026-08-18
- Comments: Story-level sign-offs provided by Strategy Rules & System Intent Owner (ST-23, ST-07 AC-04), Backend Engineering Patterns Owner (ST-04), Head of Engineering (ST-05, ST-07), and Frontend Specifications & UX Documentation Owner (ST-05), agent-mediated per §5.3 — see below. ST-23 and ST-04 Approved on first pass; ST-05's Frontend Specifications & UX Documentation Owner review required 1 retry (R at Risk FX-conversion bug, fixed same-day); ST-07 Approved on first pass by both required reviewers. All acceptance criteria met, no unresolved P0/P1 gaps.

### Story-level authority sign-off (BLG-GOV-14 — required in addition to, not instead of, the EPIC-level block above)

**Strategy Rules & System Intent Owner** (ST-23, ST-07 AC-04):
- Signed off by: Sprint Execution Engine (agent-mediated, Strategy Rules & System Intent Owner role — §5.3)
- Date: 2026-08-18
- Comments: ST-23 Approved after 2 retries (within the 2-retry cap) — Pass 1 Blocked (Conditions 1/2 prompt-instruction-only, no output-side verification for the "suggested focus area" risk); fixed by adding Condition 9 (output-side enforcement). Pass 2 Blocked (Condition 9 sound but Determination section still said "eight conditions" after Condition 9 was added — internal inconsistency); fixed same-day. Pass 3 Approved — count consistency and regenerate-then-recheck sequencing confirmed. ST-07 Approved on first pass — `LIVE_PARAMS` independently re-verified field-for-field against `production_strategy.py`'s `OPTIMAL_PARAMS` and cross-checked against `strategy_rules.md §11`'s canonical prose, no drift; §13 boundary confirmed in code; scope-reduction disclosure confirmed adequate including in the rendered UI; R-multiple formula matches `metrics_definitions.md`'s canonical formula exactly.
- Known deviations: None found.

**Backend Engineering Patterns Owner** (ST-04):
- Signed off by: Sprint Execution Engine (agent-mediated, Backend Engineering Patterns Owner role — §5.3)
- Date: 2026-08-18
- Comments: Approved on first pass. Threshold reuse verified (30% correctly imported from `concentration_service.py`, matching `strategy_rules.md §4.2.2`, not redefined). Reduction math hand-traced against 2 test cases (partial reduction, full saturation) — cap formula correctly lands allocation at/under 30%, floors conservatively, `final_shares` never increases. Backward-compatibility short-circuit confirmed by reading the code path directly. AC-03 test confirmed not question-begging — corroborated by independent threshold-math tests.
- Known deviations: None found.

**Head of Engineering** (ST-05, ST-07):
- Signed off by: Sprint Execution Engine (agent-mediated, Head of Engineering role — §5.3)
- Date: 2026-08-18
- Comments: ST-05 Approved on first pass — `prospective_heat.py` extraction confirmed genuinely behaviour-preserving (line-by-line diff against pre-extraction commit); `_calculate_heat_impact`'s fail-open except fixed to log per the codebase's own sibling convention. 2 non-blocking findings filed as BLG-TECH-14/BLG-FE-164. ST-07 Approved on first pass — port fidelity confirmed line-by-line against `production_strategy.py` (no unintentional drift); concurrency safety confirmed (`is_risk_on` nested per-call, no shared mutable state); `initial_stop_price` tracking confirmed correct and consistent across all 4 exit paths; RISK-02's scope-reduction and synchronous-request judgment calls confirmed reasonable. 2 minor fast-follow items found and applied same-day (commit `0b0a8caf`): API contract error-code documentation corrected (500→400 for the two `BacktestRuleChangeError` business-rule cases), dead `_floor_4dp` function removed.
- Known deviations: None found.

**Frontend Specifications & UX Documentation Owner** (ST-05):
- Signed off by: Sprint Execution Engine (agent-mediated, Frontend Specifications & UX Documentation Owner role — §5.3)
- Date: 2026-08-18
- Comments: Required 1 retry (within the 2-retry cap). First pass Blocked — `WhatIfSizingPreview.js`'s "R at Risk" had no FX conversion for US-market plans, contradicting `trade_plan.md §5d.3`'s own "FX-converted for US market" wording; the new Playwright test had locked in the bug by asserting the unconverted value as correct — same class of currency-basis bug as ST-02/BLG-BE-103 earlier this cycle. Fixed same-day: reads `fx_rate_used` from the response, divides for US-market plans matching `TradeEntry.js`'s `costs.totalRisk` convention exactly, £ symbol added, `DEV-v8.9-ST05-02` filed, spec Format column corrected. Second pass Approved — FX math verified structurally identical to the real precedent (entry/stop/shares/fx_rate hand-traced to the exact expected value), UK no-conversion path confirmed correct via a dedicated test case, no stray old-wording references remain in the spec.
- Known deviations: DEV-v8.9-ST05-01 (§5d.1 presence-gate self-contradiction — diagnosis confirmed correct, no alternate reading rescues the literal wording; Stop-Level-only gating is the only sensible resolution), DEV-v8.9-ST05-02 (see above). Both resolved same-story.
