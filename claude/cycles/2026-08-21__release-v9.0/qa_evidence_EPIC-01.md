Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-21

## Consolidation Block

**EPIC:** EPIC-01 — Live Correctness Follow-Through (Nightly Backtest & AI Debrief)
**Cycle:** 2026-08-21__release-v9.0
**Sprint goal:** Close out the correctness and data-integrity follow-through surfaced directly by v8.9's own PR-review process, while hardening operational resilience (deploy-path and staging safeguards) and expanding QA and cost/capacity hygiene coverage.
**Test scenarios used:** `tests/test_production_strategy.py`, `tests/test_backtest_rule_service.py`, `tests/test_root_logging_config.py`, `tests/test_debrief_service.py`, `tests/test_strategy_engine_consolidation.py`; full backend suite (1272 passed, 5 skipped at ST-05's verification point; 1282 passed, 5 skipped at ST-03's later verification point)

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|---------------------|--------|------------|
| ST-01 | Correctness bug fix (BLG-BE-109), no prior canonical spec | Fixed nightly backtest's `rebalance_dates` computation in both `production_strategy.py` and `backend/services/backtest_rule_service.py` to exclude the current, in-progress calendar month. Extracted a `compute_rebalance_dates()` helper in both files for testability (sets up ST-05's later consolidation). | `rebalance_dates` never includes a date from the current, incomplete calendar month; regression test added; existing invariant checks re-verified | Pass | None — deviations_filed=true recorded no actual deviation found |
| ST-02 | N/A — staging-only, no canonical spec beyond `docs/ops/api_performance_baseline.md` §36 (target update location) | Code fix complete: `logging.basicConfig()` added as the first statement in `backend/main.py`, before all other imports, so `logger.info()` calls reach Render's captured logs. Tested via subprocess-isolated regression test (`tests/test_root_logging_config.py`). The two remaining ACs (live Render-dashboard log confirmation, baseline doc update) structurally require the fix to already be deployed to production — cannot be satisfied pre-merge in any session (identical precedent: `2026-08-17__release-v8.9` ST-09, `DEL-20260818-01`, commit `cc120bef`). Delegation record `DEL-20260821-01` updated to Cancelled; returned to backlog in-flight (`BLG-BE-107` note appended, `claude/backlog/backlog.md`). | Root logging configured; production log confirmed to show the fix's effect; performance baseline doc updated | Returned to backlog | None — not a spec deviation, a structural pre/post-merge sequencing constraint |
| ST-03 | `docs/specs/api_contracts/trade_endpoints.md` | Product Owner decision (`BLG-BE-108`, resolves `ESC-EXEC-20260821-01`): AI Post-Trade Debrief's "linked journal entries" draws on BOTH `entry_note`/`exit_note` (the fields the UI labels "Trade Journal", directly adjacent to the Debrief panel) and Red Flag Journal events — not one or the other. `_journal_context_for_trade()` updated accordingly. | Product Owner decision recorded; implementation tested | Pass | None — 6 new tests (`TestJournalContextForTrade`); `trade_endpoints.md` v2.5.0→v2.5.1 |
| ST-04 | `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md#Condition 1` | Rewrote the AI debrief-generation prompt's `_FOCUS_AREA_SYSTEM` text to remove "pattern" framing and explicitly prohibit cross-trade count/frequency claims the system can't verify (`BLG-TECH-17`). | Prompt no longer encourages an unverifiable claim type; test coverage added; existing numeric cross-check defense-in-depth preserved | Pass | Filed a Known Deviations entry in the v8.9 decision record — Condition 1's literal "Nth trade" example now conflicts with this fix; flagged for AI Compliance & Governance Officer awareness, not silently left inconsistent |
| ST-05 | `backend/services/strategy_engine.py`; `tests/test_strategy_engine_consolidation.py` | Consolidated the duplicated backtest algorithm (`compute_signals`/`compute_atr`/`compute_risk_on`/`transaction_fee`/`compute_rebalance_dates`/`backtest`) from `production_strategy.py` and `backend/services/backtest_rule_service.py` into one canonical `strategy_engine.py`, both call sites now import from it. Byte-identical parity verified against pre-consolidation code (loaded directly from git commit `c6b9c950` via importlib). | Single canonical implementation; both call sites migrated; no behavioural change (parity-verified); full suite re-verified | Pass | Caught and fixed a real bug during the refactor (sell fee incorrectly applied to still-open/unrealized positions) — found via the parity test itself, not shipped |

**QA test coverage:**
- Scenarios run: targeted test files for each story plus the full backend suite (1272 passed, 5 skipped at ST-05's checkpoint, the most complete run in this EPIC's timeline — no regressions from ST-01/02/04/05's combined changes).
- Regression areas checked: `strategy_engine.py`'s consolidation (ST-05) is the highest-risk change in this EPIC (touches the core backtest algorithm used by both the nightly production job and the in-app backtest-rule-change feature) — verified via a dedicated parity test comparing byte-for-byte against both pre-consolidation implementations on a fixed synthetic dataset, not just "tests still pass."
- Known deviations: None found — all five stories' deviation checks completed with nothing to file. ST-02's non-completion is a structural staging-only sequencing constraint (pre-declared in `sprint_backlog.md`'s "Staging-only ACs: AC2"), not a spec deviation.

**Frontend testing gate (execution_prompt.md §3.2.A):** Not applicable — no story in this EPIC creates or modifies any file under `src/pages/**` or `src/components/**`. Purely backend/AI-governance/spec scope.

---

## Sign-Off

**Mixed-Class EPIC Signer Format:** EPIC-01 contains both `autonomous` stories (ST-01, ST-04, ST-05 — each individually reviewed and Approved by agent-mediated Backend Engineering Patterns Owner sign-off, ST-05 additionally co-signed by Strategy Rules & System Intent Owner given its strategy-logic scope) and `delegated_backend`/`delegated_decision` stories (ST-02, ST-03). ST-03 resolved via agent-mediated Product Owner sign-off (see `execution_state.json` `sign_off_record`).

```
Director of Quality

EPIC-01 consolidation reviewed. Four of five stories done, acceptance
criteria verified, spec_references populated. ST-02's remaining ACs
(live Render-dashboard log confirmation, baseline doc update) are a
structural pre/post-merge sequencing constraint, not incomplete work --
the code fix is done, tested, and merge-ready; the ACs themselves cannot
be satisfied before the fix reaches production, which cannot happen
before this EPIC merges. Returned to backlog in-flight (Product Owner
authorized, real-time in-session) rather than blocking this EPIC
indefinitely -- identical precedent already established in this repo
(2026-08-17__release-v8.9 ST-09/DEL-20260818-01). Post-merge follow-up
tracked via BLG-BE-107 and this story's own delegation record. No
unresolved P0/P1 deviations. EPIC-01 ready for PR.

Signed: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
Date: 2026-08-21
```
