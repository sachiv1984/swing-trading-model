Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-08-20
Cycle: 2026-08-17__release-v8.9

# Sprint Close — 2026-08-17__release-v8.9

## Sprint Goal

Ship v8.9: eliminate the two live risk-management stop-price defects on open positions (breakeven-floor ratchet, currency-basis mismatch) and deliver the sector-aware position sizing, pre-commit risk simulator, AI post-trade debrief, and in-app backtesting foundations of the Trade Intelligence Expansion — while clearing this cycle's reliability, QA, ops, and governance debt.

## Items Done

All 23 in-scope stories reached `done`/`merged` status. All 6 EPICs merged to `main` (EPIC-02 across two PRs — see below).

### EPIC-01 — Live Risk-Management Correctness (PR #1452)
| ST | Title | Commit | Spec reference |
|----|-------|--------|-----------------|
| ST-01 | Fix nightly trailing-stop ratchet to apply breakeven floor for profitable positions | `616dab28` | `backend/utils/calculations.py#calculate_trailing_stop`; `tests/test_trailing_stop_breakeven_floor.py` |
| ST-02 | Fix currency basis of current_trailing_stop/stop_price for US-market positions | `275b6e4f` | `docs/specs/api_contracts/position_endpoints.md#Field notes`; `docs/specs/frontend/pages/positions.md#Trailing Stop Column` |
| ST-03 | Add trailing_stop_action_rate spec entry with validation tolerances | `92080113` | `docs/specs/metrics_definitions.md#Trailing Stop Action Rate` |

### EPIC-02 — Trade Sizing & Post-Trade Intelligence (PR #1453 Sprint 1 + PR #1460 Sprint 2)
| ST | Title | Commit | Spec reference |
|----|-------|--------|-----------------|
| ST-23 | §13 System Boundary Review: Automated AI Post-Trade Debrief | `cdc27936aa2f` | `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md` |
| ST-04 | Correlation/sector-concentration-aware position sizing | `97e6c407e4a2` | `docs/design/2026-08-17__release-v8.9/correlation-sector-concentration-sizing/decision_record.md`; `backend/services/concentration_service.py` |
| ST-05 | Pre-commit "what-if" sizing/risk simulator on the trade-plan form | `86cfc07895b9` | `docs/design/2026-08-17__release-v8.9/what-if-sizing-risk-simulator/ux_spec.md`; `docs/specs/frontend/pages/trade_plan.md#5d` |
| ST-07 | In-app backtesting engine for strategy rule changes | `0b0a8caf2ff7` | `docs/design/2026-08-17__release-v8.9/in-app-backtesting-engine/ux_spec.md`; `docs/specs/frontend/pages/strategy_benchmark.md#7.6` |
| ST-06 | Automated AI post-trade debrief (Sprint 2 — gated on ST-23) | `53286f6c6e95` | `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md`; `docs/specs/data_model.md#DS-16`; `docs/specs/api_contracts/trade_endpoints.md#GET /trades/{trade_id}/debrief` |

### EPIC-03 — Backend Reliability & Performance (PR #1454)
| ST | Title | Commit | Spec reference |
|----|-------|--------|-----------------|
| ST-08 | Investigate `GET /trade-plans/tags` ~10s p50 latency | `373f606b` | `docs/ops/db_index_audit_arc4_2026-08-06.md` |
| ST-09 | Verify ST-11 duration logging against a real post-merge invocation | N/A — staging-only verification, no code commit | N/A — `spec_reference_not_applicable: true` |
| ST-10 | Wrap audit-trail writes in the same transaction as the primary state update | `20a6fc33` | `docs/specs/data_model.md#DS-13` |
| ST-11 | Confirm `trade_csv_service.py::build_trade_history_csv` is dead code and remove | `3fb46a6c` | `docs/specs/api_contracts/trade_endpoints.md` |

### EPIC-04 — Test Coverage & QA Hardening (PR #1455)
| ST | Title | Commit | Spec reference |
|----|-------|--------|-----------------|
| ST-12 | Add test coverage for `screener_refresh`/`risk_off_alerts` job-registration wiring | `3ff90706` | `backend/routers/screener.py`; `backend/main.py#risk_off_alerts_endpoint` |
| ST-13 | Decide and apply treatment for `trade_plans.setup_type` with no default/required guarantee | `bdf8fee2` | `docs/specs/api_contracts/trade_plan_endpoints.md#Request Body Fields` |
| ST-14 | Add direct unit tests for `cash_service`, `compliance_service`, `news_service`, `validation_service` | `c2bc74b0` | `docs/ops/backend_service_layer_test_coverage_report_2026-08-16.md` |
| ST-15 | Add Playwright coverage for `WhatsNewCard`'s changelog User Impact rendering | `96790ec5` | `tests/e2e/whats-new-panel.spec.js`; `docs/specs/frontend/pages/dashboard.md#§6A` |

### EPIC-05 — Operations & Spec Currency (PR #1456)
| ST | Title | Commit | Spec reference |
|----|-------|--------|-----------------|
| ST-16 | Local dev venv version-pin enforcement; confirm PUBLIC_URL parity on production | `5f80e301` | `docs/ops/test_environment_parity_check_2026-08-16.md#§2.1` |
| ST-17 | Archive `window_summary_IW-*.md` files older than 90 days | `d41d8adb` | `claude/backlog/backlog.md#BLG-OPS-113` |
| ST-18 | Document `screener_refresh` and `risk_off_alerts` jobs in `health_endpoints.md` | `dc3f3eaa` | `docs/specs/api_contracts/health_endpoints.md#GET /health/scheduler` |

### EPIC-06 — Governance Process Debt Closure (PR #1457)
| ST | Title | Commit | Spec reference |
|----|-------|--------|-----------------|
| ST-19 | Fix `post_ship_closure.md` to actually write `last_post_ship_cycle`/`last_post_ship_utc` | `4a5ee87c` | `claude/system/post_ship_closure.md#STEP 10`; `claude/schemas/state_field_owners.json` |
| ST-20 | Root-cause and correct `execution_state.json` timestamp drift from actual git commit dates | `2220b84e` | `claude/system/execution_prompt.md#3.1` |
| ST-21 | Physically place the Displacement Debt Register and wire it into `roadmap_prompt.md` STEP 8 | `2220b84e` | `claude/system/roadmap_prompt.md#STEP 8` |
| ST-22 | Define a pruning rule for stale `RA:` roadmap-annotation markers older than 3 releases | `be94ba81` | `claude/system/roadmap_management_prompt.md#STEP 5.2` |

## Items Returned to Backlog

None — all 23 in-scope stories reached `done`. (ST-09 held a temporary in-flight `returned_to_backlog` status from 2026-08-18 to 2026-08-20 while genuinely blocked on EPIC-03's own merge — see `DEL-20260818-05` addenda — and reached `done` once the post-merge invocation became possible.)

## Items Delegated and Outstanding

All 12 delegated-item tracking entries (10 `DEL-*` delegation log entries + 2 `ESC-EXEC-*` escalations, for the 2 `delegated_decision`-classified items which route through the escalation subroutine instead of the delegation log) reached a terminal state — none outstanding:

| Delegation ID | ST Item | Outcome |
|---------------|---------|---------|
| DEL-20260817-01 | ST-01 | Unblocked — engine-completed in-session |
| DEL-20260817-02 | ST-02 | Unblocked — engine-completed in-session |
| DEL-20260818-01 | ST-23 | Unblocked — engine-completed in-session, 3 sign-off review passes |
| DEL-20260818-02 | ST-04 | Unblocked — engine-completed in-session |
| DEL-20260818-03 | ST-05 | Unblocked — reclassified engine-completed (LL-v2.3-CL-01), 1 sign-off retry |
| DEL-20260818-04 | ST-07 | Unblocked — engine-completed in-session |
| DEL-20260818-05 (renumbered from EPIC-03's own `-01`) | ST-09 | Complete — genuinely blocked pre-merge; resolved post-merge 2026-08-20 via real production invocation + Product Owner-directed interim proxy (`DEV-EPIC03-ST09-01`) |
| DEL-20260818-06 (renumbered from EPIC-03's own `-02`) | ST-08 | Unblocked — engine-completed in-session, 2 sign-off retries (vacuous-test-assertion bugs found and fixed) |
| DEL-20260818-07 (renumbered from EPIC-05's own `-03`) | ST-16 | Unblocked — engine-completed in-session |
| DEL-20260820-01 | ST-06 | Unblocked — engine-completed in-session (Sprint 2, picked up 2026-08-20 after EPIC-02's Sprint 1 PR had already merged; own PR #1460) |
| ESC-EXEC-20260818-01 | ST-13 | Resolved same-session — Product Owner decision (option b), well within 24h SLA |
| ESC-EXEC-20260818-02 | ST-21 | Open, non-blocking — file-creation sub-item architecturally outside Sprint Execution's write scope, handed to the Roadmap Rebalance Engine; prompt-wiring sub-item (the achievable half) is done |

## QA Evidence Logs Produced

- `claude/cycles/2026-08-17__release-v8.9/qa_evidence_EPIC-01.md`
- `claude/cycles/2026-08-17__release-v8.9/qa_evidence_EPIC-02.md` (updated 2026-08-20 with ST-06's Sprint 2 pass and AI Compliance & Governance Officer sign-off)
- `claude/cycles/2026-08-17__release-v8.9/qa_evidence_EPIC-03.md`
- `claude/cycles/2026-08-17__release-v8.9/qa_evidence_EPIC-04.md`
- `claude/cycles/2026-08-17__release-v8.9/qa_evidence_EPIC-05.md`
- `claude/cycles/2026-08-17__release-v8.9/qa_evidence_EPIC-06.md`

## Process Notes

- **Session-resume merge-gate state sync (STEP 4, LL-v3.9-P3-1/LL-v6.4-P3-01):** The closing session began on an unrelated branch (`governance/backlog-additions-20260819`), 69 commits behind `origin/main`. All 6 EPIC PRs had already merged on GitHub (last: EPIC-06 PR #1457) but `execution_state.json`'s `merge_gate` block was stale — EPIC-06 was omitted from both `epics_merged` and `epics_pending`, and EPIC-03–06's per-EPIC `status`/`pr_status` fields still read `done`/`open`. Corrected via `git fetch` + `gh pr view` re-check on all 6 PR numbers, committed directly to `main` (`e112f553`, `[GOVERNANCE]`).
- **Scope gap found post-sync: ST-06 was genuinely unbuilt.** Cross-checking `sprint_backlog.md`'s own 23-item count (22 Sprint 1 + ST-23 gate story, ST-06 gated to Sprint 2) against `execution_state.json`'s 22 recorded stories surfaced that ST-06 (Automated AI Post-Trade Debrief, EPIC-02 Sprint 2 subset) had been unblocked since 2026-08-18 (ST-23 reached `done`/CONDITIONAL) but never picked up — `execution_state.json` had no entry for it at all. User confirmed: implement it in this same session rather than deferring.
- **EPIC-02 required a second, separate PR (#1460) for its Sprint 2 subset**, since its Sprint 1 PR (#1453) had already merged and closed by the time ST-06 was picked up. Tracked via a new `execution_state.json.epics.EPIC-02.sprint2` sub-object rather than overwriting the Sprint 1 subset's accurate historical PR record.
- **Two-agent PR review performed on PR #1460 at explicit user request**, posted as a GitHub PR comment (agent-mediated, on behalf of Director of Quality and Product Owner, per the OA-6 labeling convention — not a substitute for the actual human sign-offs). Surfaced 2 non-blocking findings: (1) the debrief-generation prompt encourages cross-trade pattern language ("this is the Nth trade where X occurred") that no computed data currently backs, so `numeric_cross_check` will reject such claims more often than the design intends; (2) "linked journal entries" was implemented via `red_flag_events` rather than `trade_history.entry_note`/`exit_note` (the fields this codebase already labels "Trade Journal" in the same UI section) — a plausible but debatable reading of ST-06's AC. Neither blocked merge; both are worth a follow-up backlog item.
- **Orphaned post-merge commit check (LL-v6.8-P3-01):** `git log origin/main..origin/exec/<cycle_id>/EPIC-xx` returned empty for all 6 EPIC branches at both sync points (initial 5-EPIC sync and the later EPIC-02 Sprint 2 sync) — nothing orphaned, no reconciliation needed.
- **Cross-EPIC merge conflict resolution (CLAUDE.md §8), applied for EPIC-05 and EPIC-06:** EPIC-05's PR required a `delegation_log.md` DEL-ID collision resolution (`DEL-20260818-03` renumbered to `DEL-20260818-07`, commit `981e5fd1`). EPIC-06's PR required an add/add reconciliation on `execution_escalations.md`.
- **DEL-ID collision pattern recurred twice this cycle** (EPIC-03's independently-filed `DEL-20260818-01`/`02` colliding with EPIC-02's own, renumbered to `DEL-20260818-05`/`06`; EPIC-05's `DEL-20260818-03` colliding with EPIC-02's own, renumbered to `DEL-20260818-07`) — consistent with the same class of parallel-EPIC ID-namespace collision seen in prior cycles.
- **Self-referential governance EPIC (EPIC-06):** all 4 stories modified `execution_prompt.md`, `post_ship_closure.md`, and/or `roadmap_prompt.md`/`roadmap_management_prompt.md`. Handled via agent-mediated Head of Specs Team review for all 4 stories and one in-session write-scope self-correction (ST-21 — file-creation reverted before commit once `claude/roadmap/*`'s hard write-scope exclusion was confirmed).
- **Pre-existing documentation gap self-corrected while touching the same file (shared_standards.md §9.1):** `docs/ops/api_performance_baseline.md`'s Document History table was found missing ST-09's own v2.29 row (§36.5 addition) — the header already read 2.29 but the table's newest row was still 2.28. Added in the same commit as this cycle's own next bump (2.29→2.30, ST-06's §41).

## Deviations Filed This Sprint

| Spec file | Deviation ref | Priority | Status |
|-----------|---------------|----------|--------|
| `docs/specs/frontend/pages/positions.md#Known Deviations` | `DEV-EPIC01-ST02-01` | — | Resolved same-story |
| `docs/specs/frontend/pages/trade_plan.md` | `DEV-v8.9-ST05-01` | — | Resolved same-story |
| `docs/specs/frontend/pages/trade_plan.md` | `DEV-v8.9-ST05-02` | — | Resolved same-story |
| `docs/ops/api_performance_baseline.md#§36.5` | `DEV-EPIC03-ST09-01` | P3 | Open — interim GitHub Actions timing-proxy adopted; `BLG-BE-107` tracks the underlying production logging-config fix |

None found for ST-06 — the on-demand-vs-real-time generation choice is an AC-offered option, not a divergence.

Non-deviation backlog items filed mid-sprint as out-of-scope discoveries: `BLG-GOV-311` (strategy_rules.md §13.5 roster-table row, outside execution_prompt.md's write scope), `BLG-TECH-13`, `BLG-TECH-14`, `BLG-FE-164`, `BLG-TECH-15` (algorithm-port-sync debt), `BLG-BE-107` (production logging-config gap).

**Follow-up recommended (not filed as formal backlog items in this record — see Open Escalations / this record's own Process Notes for the two-agent PR review findings):** (1) either compute real cross-trade pattern counts to back ST-06's encouraged "Nth trade" phrasing, or remove that phrasing from the prompt; (2) confirm with Product Owner whether ST-06's "linked journal entries" should also draw on `trade_history.entry_note`/`exit_note`.

## Open Escalations

- `ESC-EXEC-20260818-02` (ST-21/EPIC-06) — Open, non-blocking (Workforce/Capacity class, no fixed SLA). File-creation half of ST-21 handed to the Roadmap Rebalance Engine; will close on the next live `run roadmap`/`manage roadmap` invocation per `roadmap_prompt.md` STEP 8.

## Net Outcome vs Sprint Goal

Both live risk-management stop-price defects closed (ST-01 breakeven-floor confirmed already-correct-and-now-regression-tested; ST-02 currency-basis mismatch genuinely fixed). Full Trade Intelligence Expansion foundation shipped: §13-gated AI post-trade debrief scoping and implementation (ST-23 CONDITIONAL gate, ST-06 built under its 9 binding conditions), sector-concentration-aware sizing, pre-commit what-if simulator, and in-app backtesting engine. Reliability/QA/ops/governance debt cleared across EPIC-03–06, including a structural fix for the recurring `execution_state.json` timestamp-drift bug (ST-20) discovered and corrected within this same cycle. Sprint goal fully met — all 23 in-scope stories done, all 6 EPICs merged (EPIC-02 via two PRs, Sprint 1 + Sprint 2 as designed by the Multi-Sprint Gate Note). No scope carried forward except the pre-authorized `DEV-EPIC03-ST09-01` interim-proxy split (post-merge platform gap, not this cycle's fault) and `ESC-EXEC-20260818-02`'s architecturally-out-of-scope file creation, both cleanly handed off with explicit unblock criteria rather than silently dropped.

## Verification Readiness Statement

| Field | Status |
|-------|--------|
| All spec references populated in execution_state.json | Yes |
| All P1–P3 deviations filed and backlog references updated | Yes |
| QA evidence logs complete and DoQ sign-off non-blank for all EPICs | Yes |
