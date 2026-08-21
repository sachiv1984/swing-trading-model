Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-21

## Consolidation Block

**EPIC:** EPIC-01 — Live Correctness Follow-Through (Nightly Backtest & AI Debrief)
**Cycle:** 2026-08-21__release-v9.0
**Sprint goal:** Close out the correctness and data-integrity follow-through surfaced directly by v8.9's own PR-review process, while hardening operational resilience (deploy-path and staging safeguards) and expanding QA and cost/capacity hygiene coverage.
**Test scenarios used:** `tests/test_production_strategy.py`, `tests/test_backtest_rule_service.py`, `tests/test_root_logging_config.py`, `tests/test_debrief_service.py`, `tests/test_strategy_engine_consolidation.py`; full backend suite (1272 passed, 5 skipped at ST-05's verification point)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-01 | Correctness bug fix (BLG-BE-109), no prior canonical spec | Fixed nightly backtest's `rebalance_dates` computation in both `production_strategy.py` and `backend/services/backtest_rule_service.py` to exclude the current, in-progress calendar month. Extracted a `compute_rebalance_dates()` helper in both files for testability (sets up ST-05's later consolidation). | `rebalance_dates` never includes a date from the current, incomplete calendar month; regression test added; existing invariant checks re-verified | Pass | None — deviations_filed=true recorded no actual deviation found |
| ST-02 | `docs/ops/api_performance_baseline.md#36.5` | Code fix complete: `logging.basicConfig()` added as the first statement in `backend/main.py`, before all other imports, so `logger.info()` calls reach Render's captured logs. Tested via subprocess-isolated regression test. | Root logging configured; production log confirmed to show the fix's effect; performance baseline doc updated | **Blocked (delegated)** — code portion done, tested, pushed; the two remaining ACs (live Render-dashboard log confirmation, baseline doc update with the real value) require production dashboard access unavailable in this sandbox | Delegated via `DEL-20260821-01` to Infrastructure & Operations Owner |
| ST-03 | — | Requires a Product Owner decision (`BLG-BE-108`) on the AI Post-Trade Debrief's "linked journal entries" data source before any implementation can proceed | Product Owner decision recorded; implementation (if changed) tested | **Blocked (escalated)** — genuinely a product decision, not an engineering task; no code to write until decided | Escalated via `ESC-EXEC-20260821-01`, SLA due 2026-08-24 |
| ST-04 | `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md#Condition 1` | Rewrote the AI debrief-generation prompt's `_FOCUS_AREA_SYSTEM` text to remove "pattern" framing and explicitly prohibit cross-trade count/frequency claims the system can't verify (`BLG-TECH-17`). | Prompt no longer encourages an unverifiable claim type; test coverage added; existing numeric cross-check defense-in-depth preserved | Pass | Filed a Known Deviations entry in the v8.9 decision record — Condition 1's literal "Nth trade" example now conflicts with this fix; flagged for AI Compliance & Governance Officer awareness, not silently left inconsistent |
| ST-05 | `backend/services/strategy_engine.py`; `tests/test_strategy_engine_consolidation.py` | Consolidated the duplicated backtest algorithm (`compute_signals`/`compute_atr`/`compute_risk_on`/`transaction_fee`/`compute_rebalance_dates`/`backtest`) from `production_strategy.py` and `backend/services/backtest_rule_service.py` into one canonical `strategy_engine.py`, both call sites now import from it. Byte-identical parity verified against pre-consolidation code (loaded directly from git commit `c6b9c950` via importlib). | Single canonical implementation; both call sites migrated; no behavioural change (parity-verified); full suite re-verified | Pass | Caught and fixed a real bug during the refactor (sell fee incorrectly applied to still-open/unrealized positions) — found via the parity test itself, not shipped |

**QA test coverage:**
- Scenarios run: targeted test files for each story plus the full backend suite (1272 passed, 5 skipped at ST-05's checkpoint, the most complete run in this EPIC's timeline — no regressions from ST-01/02/04/05's combined changes).
- Regression areas checked: `strategy_engine.py`'s consolidation (ST-05) is the highest-risk change in this EPIC (touches the core backtest algorithm used by both the nightly production job and the in-app backtest-rule-change feature) — verified via a dedicated parity test comparing byte-for-byte against both pre-consolidation implementations on a fixed synthetic dataset, not just "tests still pass."
- Known deviations: two genuine blockers correctly delegated/escalated rather than worked around (ST-02 needs live production dashboard access; ST-03 needs a Product Owner product decision) — neither is an engineering shortfall, both are the correct disposition per CLAUDE.md's always-human-gate rules.

---

## Sign-Off

**Not yet complete.** ST-02 (`DEL-20260821-01`, blocked on Infrastructure & Operations Owner Render dashboard access) and ST-03 (`ESC-EXEC-20260821-01`, blocked on Product Owner decision, SLA due 2026-08-24) remain open — per `execution_prompt.md` §3.2 ("An EPIC is `done` (not yet `merged`) when all of its ST items are `done`"), EPIC-01 is not done and the EPIC-level sign-off block below is deferred until both resolve. This file is maintained incrementally per STEP 3.1.C (each completed story's disposition recorded as it finishes) — the per-story table above is current and accurate for ST-01/04/05; it does not imply the EPIC as a whole is ready for PR.

**Mixed-Class EPIC Signer Format (to be completed once ST-02/ST-03 resolve):** EPIC-01 contains both `autonomous` stories (ST-01, ST-04, ST-05 — each individually reviewed and Approved by agent-mediated Backend Engineering Patterns Owner sign-off, ST-05 additionally co-signed by Strategy Rules & System Intent Owner given its strategy-logic scope) and `delegated_backend`/`delegated_decision` stories (ST-02, ST-03). Individual story sign-offs already on record: ST-01/ST-04/ST-05 each independently reviewed and Approved by agent-mediated sign-off (see each story's own commit message and `execution_state.json` `sign_off_record` for detail).

- Signed off by: <pending — do not open the EPIC-01 PR until this is completed>
- Date: <pending>
- Comments: <pending>
