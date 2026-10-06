Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-10-06
Cycle: 2026-09-30__release-v9.9

---

# Sprint Close Record — 2026-09-30__release-v9.9

## Sprint Goal

Ship a single canonical ATR/stop-recalculation implementation with timestamp visibility on GET /positions (BLG-BE-135), while clearing queued backend, security, QA, governance, spec, and frontend debt items.

## Items Done

All 35 in-scope ST items reached `done` and are merged to `main` across 6 EPICs, 6 PRs. Commit SHAs are the story's recorded `commit_sha` in `execution_state.json`.

### EPIC-01 — Backend Reliability & Data Integrity (PR #1884, merged 2026-10-01T14:29:50Z)

| ST | Title | Commit SHA | Spec reference(s) |
|----|-------|------------|--------------------|
| ST-01 | Consolidate 4 duplicate ATR implementations; persist stop/ATR recalculation timestamp; expose atr/multiplier/timestamp on GET /positions | `94c75fe7` | `claude/strategy/strategy_rules.md#7.1`; `docs/specs/data_model.md#DS-22`; `docs/specs/api_contracts/position_endpoints.md#GET /positions`; `docs/reference/openapi.yaml`; `docs/product/decisions/st01_atr_consolidation_ruling.md` |
| ST-02 | GET /reports/monthly-pnl's year param has no bounds check, unlike its sibling GET /reports/tax-year | `56a56d6a` | `docs/specs/api_contracts/reports_endpoints.md#GET /reports/monthly-pnl` |
| ST-03 | gemini_service.py's daily-cost Telegram alert still uses a hardcoded timeout, not utils.upstream_call | `ec1a5199` | — (Case E: config/timeout-sourcing consistency fix (pattern already established by prior ST-07 migration), no prior canonical spec — verified via tests/test_upstream_call_helper.py::TestST03GeminiDailyCostAlertUsesConfiguredTimeout) |
| ST-04 | utils/pricing.py's ATR-fallback Yahoo Finance call still uses a hardcoded timeout, not utils.upstream_call | `9cdfc2c6` | — (Case E: config/timeout-sourcing consistency fix (pattern already established by prior ST-07 migration), no prior canonical spec — verified via tests/test_upstream_call_helper.py::TestST04CalculateAtrYahooFallbackUsesConfiguredTimeout) |
| ST-05 | alpaca_paper_sync_service.py's 3 Alpaca calls still use hardcoded timeouts, not utils.upstream_call | `ec1a5199` | — (Case E: config/timeout-sourcing consistency fix (pattern already established by prior ST-07 migration), no prior canonical spec — verified via tests/test_upstream_call_helper.py::TestST05AlpacaPaperSyncUsesConfiguredTimeout) |

### EPIC-02 — Operational Reliability & Security Hardening (PR #1886, merged 2026-10-05T07:26:30Z)

| ST | Title | Commit SHA | Spec reference(s) |
|----|-------|------------|--------------------|
| ST-06 | Two residual gaps in the just-hardened non-registry dependency guard | `0f950f5a` | `scripts/check_non_registry_dependencies.py`; `tests/test_non_registry_dependency_check.py` |
| ST-07 | POST /ai/check-daily-cost has no de-duplication guard against a double-submitted Telegram alert | `2cc1c14e` | `backend/services/gemini_service.py`; `backend/database.py` |
| ST-08 | POST /ai/check-endpoint-anomalies has no de-duplication guard against a double-submitted Telegram alert | `3ea83dbc` | `backend/services/ai_endpoint_anomaly_service.py` |
| ST-09 | POST /price-alerts has no de-duplication guard against a double-submitted duplicate alert | `554efcd6` | `backend/services/alerts_service.py`; `docs/specs/api_contracts/alerts_endpoints.md#POST /price-alerts` |

### EPIC-03 — QA & Test Coverage (PR #1888, merged 2026-10-05T09:25:32Z)

| ST | Title | Commit SHA | Spec reference(s) |
|----|-------|------------|--------------------|
| ST-10 | GET /reports/tax-year returns HTTP 500 against its own test fixture | `eff1ea98` | `tests/test_api_contracts.py` |
| ST-11 | Strategy-rule -> test traceability matrix for strategy_rules.md S4-S8 | `7af317f6` | `docs/testing/strategy_rule_test_traceability_matrix.md` |
| ST-12 | Property-based tests for 'stop never decreases' and sizing validity rules | `e160a8d8` | `tests/test_strategy_invariants_property.py`; `claude/strategy/strategy_rules.md#7.3`; `claude/strategy/strategy_rules.md#4.1.4` |
| ST-13 | Real-Postgres integration test for the reflection-reminder evaluation step | `d1312ca5` | `tests/test_reflection_reminder_postgres.py` |
| ST-14 | Convert remaining test files sharing test_trade_plan_audit_log.py's unrestored sys.modules swap pattern | `c2ab1ea1` | `tests/_real_database.py`; `tests/conftest.py` |
| ST-15 | Add automated test coverage for the I/O-boundary functions in EPIC-04's staleness/CI-usage scripts | `f98732cd` | `tests/test_ci_scripts_io_boundary.py` |
| ST-16 | test_null_fee_trade_audit.py's inspect.getsource() call fails against the database module stub | `86612f9f` | `tests/test_null_fee_trade_audit.py` |
| ST-17 | Prove the non-registry dependency check fails a real PR, and confirm it is a required status check on main | `8a1db624` | `docs/ops/non_registry_dependency_check_live_fire_2026-10-05.md`; `.github/workflows/non-registry-dependency-check.yml` |
| ST-18 | Harden the UI-copy boundary lint against obfuscation-grade and cross-node phrase splits | `7ef43618` | `scripts/check_ui_copy_forbidden_phrases.py`; `tests/test_ui_copy_forbidden_phrases.py`; `scripts/ui_copy_lint_babel_differential.py` |

### EPIC-04 — Governance Process & Strategy Boundary (PR #1891, merged 2026-10-06T09:35:25Z; ST-21/22/23/25/27 first reached `main` via PR #1886 — retroactive gate)

| ST | Title | Commit SHA | Spec reference(s) |
|----|-------|------------|--------------------|
| ST-19 | Conduct the overdue 90-day AI feature usage review (BLG-GOV-74/140/141/142 cluster) | `979f0126` | `docs/ops/ai_feature_usage_review_2026-09-24.md` |
| ST-20 | gap_risk_service.py (BLG-FEAT-65) shipped without a recorded S13 review or S13.5 roster row | `90b43b53` | `docs/product/decisions/decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md`; `claude/strategy/strategy_rules.md#13.3`; `claude/strategy/strategy_rules.md#13.5` |
| ST-21 | Split roadmap_prompt.md into a core plus an appendix so it fits a single read | `94de0a0b` | `claude/system/roadmap_prompt.md`; `claude/system/roadmap_prompt_appendix.md` |
| ST-22 | Parameter-change ledger for strategy_rules.md S11 production parameters | `ae17d5de` | `docs/governance/strategy_parameter_change_ledger.md`; `claude/strategy/strategy_rules.md#12.3` |
| ST-23 | scan_backlog_gate_conditions.py date-disambiguation gap can produce false negatives | `d260e98b` | `scripts/scan_backlog_gate_conditions.py` |
| ST-24 | Five near-duplicate 'AI adoption window' gate-criteria texts should be one canonical shared reference | `64e7525c` | `claude/backlog/backlog.md#Shared Gate References` |
| ST-25 | Rebalance diagnostic tallies (STEP 2.4/7.1/7.2) are recomputed by hand each cycle | `57de1411` | `scripts/compute_rebalance_diagnostics.py`; `claude/system/roadmap_prompt.md#STEP 2.4`; `claude/system/roadmap_prompt.md#7.1` |
| ST-26 | role_share_history.md has no governance-authorized home under claude/roadmap/ | `3e0f61e8` | `claude/roadmap/role_share_history.md`; `claude/system/roadmap_prompt.md#7.2 Cross-Role Workload Balance Check` |
| ST-27 | .claude_current_state.json's execution_state_path points to the prior cycle, not the active one | `018f5c1c` | `claude/schemas/state_field_owners.json#execution_state_path` |

### EPIC-05 — Spec & Data-Model Debt Clearance (PR #1892, merged 2026-10-06T10:06:33Z; ST-28/32/33/34 first reached `main` via PR #1886 — retroactive gate)

| ST | Title | Commit SHA | Spec reference(s) |
|----|-------|------------|--------------------|
| ST-28 | Read-only live-schema vs data_model.md drift detector | `aba5e44b` | `scripts/check_data_model_drift.py` |
| ST-29 | Drop 4 confirmed-orphaned, always-NULL columns from the live positions table | `bd89ed49` | `docs/specs/data_model.md#DS-24` |
| ST-30 | Reconcile positions.fees_paid NOT NULL constraint (re-apply live, or confirm nullable is intentional) | `425dcd89` | `docs/specs/data_model.md#DS-23`; `docs/specs/data_model_positions_dictionary.md#fees_paid` |
| ST-31 | Cross-reference current_roadmap.md's SI-02 field to the canonical 'linked trade plan' definition | `13e33563` | `docs/specs/metrics/si02_drift_score.md#2.4 Canonical "Linked Trade Plan" Count`; `claude/roadmap/current_roadmap.md#SI-02 gate confirmation status` |
| ST-32 | data_model.md DS-19 'Verification status' still says the migration was never run against a live PostgreSQL | `62eebdd8` | `docs/specs/data_model.md#DS-19` |
| ST-33 | Correct the BLG-BE-128 citation to BLG-BE-129 for the latency_ms composition decision | `3677d86e` | `docs/specs/api_contracts/ai_endpoints.md`; `docs/ops/external_api_dependency_register.md` |
| ST-34 | Correct notifications.md and the alert-thresholds empty-state scenario doc to the no-trailing-period headings now shipped | `ebc23c14` | `docs/specs/frontend/pages/notifications.md`; `docs/testing/alert_thresholds_empty_state_scenarios.md` |

### EPIC-06 — Frontend & UX Debt (PR #1889, merged 2026-10-05T09:05:04Z)

| ST | Title | Commit SHA | Spec reference(s) |
|----|-------|------------|--------------------|
| ST-35 | RecentTradesWidget icon-background badge uses two-way (>=0) colour logic for zero P&L | `7013c331` | `docs/specs/frontend/design_system.md#Data States`; `tests/e2e/recent-trades-zero-pnl-badge.spec.js` |

## Items Returned to Backlog

None. All 35 in-scope items reached `done`.

## Items Delegated and Outstanding

None outstanding. Three delegation records this cycle, all terminal:

- **DEL-20261001-01** (ST-01/EPIC-01): Status `Unblocked` (2026-10-01T12:29:32Z). The Data Model & Domain Schema Owner applied the DS-22 migration (`stop_calculated_at`, `atr_calculated_at`, `active_atr_multiplier`) to staging and production. The session re-confirmed it on staging.
- **DEL-20261001-02** (ST-29/EPIC-05, `delegated_backend`): Status `Unblocked`, in-session (2026-10-05T12:45:37Z). The user dropped the 4 orphaned `positions` columns on staging, then production, and the verification query returned 0 rows. Recorded as `data_model.md` DS-24, commit `bd89ed49`.
- **DEL-20261001-03** (ST-30/EPIC-05, `delegated_backend`): Status `Unblocked`, in-session (2026-10-05T12:55:48Z). The user re-applied `positions.fees_paid NOT NULL` on staging, then production, after a 0-row NULL pre-check. Recorded as `data_model.md` DS-23, commit `425dcd89`.

## QA Evidence Logs Produced

- `claude/cycles/2026-09-30__release-v9.9/qa_evidence_EPIC-01.md`: agent-mediated (Strategy Rules & System Intent Owner; Data Model & Domain Schema Owner roles), 2026-10-01
- `claude/cycles/2026-09-30__release-v9.9/qa_evidence_EPIC-02.md`: Sprint Execution Engine (autonomous class), 2026-10-05
- `claude/cycles/2026-09-30__release-v9.9/qa_evidence_EPIC-03.md`: agent-mediated (Director of Quality role), 2026-10-05
- `claude/cycles/2026-09-30__release-v9.9/qa_evidence_EPIC-04.md`: agent-mediated (Director of Quality role), 2026-10-05. Retroactive gate; Product Owner acceptance by merging PR #1891
- `claude/cycles/2026-09-30__release-v9.9/qa_evidence_EPIC-05.md`: agent-mediated (Director of Quality role), 2026-10-05. Retroactive gate; Product Owner acceptance by merging PR #1892
- `claude/cycles/2026-09-30__release-v9.9/qa_evidence_EPIC-06.md`: agent-mediated (Director of Quality role), 2026-10-05

All six sign-off `Date:` fields are non-blank, and `qa_signed_off: true` is set for all six EPICs.

## Process Notes

Rolled up from `execution_state.json.process_notes` (9 entries, 2026-10-01 to 2026-10-06):

- **Cross-EPIC commits merged through PR #1886 (largest process deviation this cycle).** EPIC-02's branch was cut on top of the EPIC-04/EPIC-05 linear history. Merging PR #1886 therefore also merged 19 other-EPIC commits into `main` (12 `[EPIC-04]`, 7 `[EPIC-05]`) without their own STEP 4 merge gate, which breaks the CLAUDE.md §2 branch-matching rule. The user directed a retroactive gate. `qa_evidence_EPIC-02/04/05.md` record the deviation. EPIC-04 and EPIC-05 then got agent-mediated DoQ sign-off, and the Product Owner accepted them by merging PRs #1891 and #1892. Both are now `merged_via.retroactive_gate: complete`. Root-cause prevention filed as `BLG-GOV-368`.
- **Summary-state staleness found by resume backstops.** EPIC-03 (PR #1888) and EPIC-05 (PR #1892) were each merged by a human between sessions and still showed `pr_status: open` at the next `run sprint`. ST-33 and ST-34 were still `not_started` even though their commits were on `main`. The STEP 4 resume-sync and the new §10 step 3a pushed-commit reconciliation (v3.81) corrected all of them. No orphaned post-merge commits were found on any of the six EPIC branches.
- **Session-start divergence.** Local `main` was 20 commits behind `origin/main` (2026-10-05) and then 19 behind (2026-10-06) at session start. It was pulled before state was read (LL-v7.2-P3-01).
- **PR #1884 (EPIC-01) waited on human gates.** All CI checks were green, but DoQ and Product Owner acceptance were outstanding, so the engine moved on to other EPICs instead of stalling.
- **Agent-mediated sign-offs.** Claude Code's auto-mode classifier refused the first EPIC-05 DoQ subagent launch as self-approval. The user then explicitly chose agent-mediated sign-offs, and the review was re-run with their approval. Every agent-mediated PR review was labelled as agent-mediated, and every EPIC merge was performed by a human.
- **Governance PR #1890** (execution_prompt.md v3.81, ESC-CLOSE rulings) merged mid-cycle. Both open EPIC branches then conflicted with `main`, and each was resolved per CLAUDE.md §8 (`3ea9d78f`, `4b452da9`, `05481c48`).
- **Sprint-close metadata correction.** EPIC-01's `test_scenarios` was missing `tests/test_atr_consolidation.py` and `tests/test_position_atr_timestamp_persistence.py`, which are named in `qa_evidence_EPIC-01.md`. Both were added under the LL-v9.0-P4-02 backstop.
- **STEP 5.1 checks.** All 35 stories have `acceptance_verified: true` and `deviations_filed: true`, so no correction was needed. The item count matches (35 declared in `sprint_backlog.md`'s "Scope confirmed", 35 in `execution_state.json`). All six EPIC branches have no unpushed or orphaned commits.
- **System Status Report corrections.** None needed. `docs/System_status_report.md` has no SC-* scenario-count cells or execution-prompt version reference that this sprint made stale. A new Sprint section was added (STEP 5.3A).

## Deviations Filed This Sprint

No new canonical-spec `DEV-*` records were filed. Every `done` story's deviation check finished with `deviations_filed = true`.

- **ST-01** is `Pass_with_deviation` in `qa_evidence_EPIC-01.md`. `BLG-BE-135` literally asks for "1 canonical source across all 4 files", and that is intentionally not met for `pricing.py`/`screener_engine.py`. The AC allows this ("engineering constrained to match the documented cadence, per the Owner's ruling"), and the RISK-01 ruling (`docs/product/decisions/st01_atr_consolidation_ruling.md`) provides that ruling. The result matches the spec's intent, so no spec deviation was filed (LL-v3.4-P3-03). Severity matches the DoQ assessment.
- **ST-34 closed a pre-existing deviation.** `DEV-v9.7-ST05-01` (`docs/specs/frontend/pages/notifications.md`) is marked closed in the same commit (`ebc23c14`), per the resolving-commit discipline.

Backlog follow-ups filed this cycle are listed below. These are out-of-scope findings, not spec deviations:

| Backlog ID | Filed by | Reason |
|------------|----------|--------|
| `BLG-QA-204` | PR #1884 review (ST-01) | ATR timestamp persistence test does not mock `get_settings()` |
| `BLG-OPS-175`, `BLG-OPS-176` | PR #1886 review (ST-09, ST-08) | No DB-level unique constraint behind the price-alert dedup; anomaly dedup-clear path ignores `send_alert` |
| `BLG-QA-205`–`BLG-QA-208` | ST-11 | Strategy-rule → test traceability gaps (FX/insufficient cash, sizing widget, live exit decision, entry required fields) |
| `BLG-OPS-177` | ST-17 | Make the Non-Registry Dependency Check a required status check on `main` |
| `BLG-QA-209` | ST-14 | `utils.*` stubs leak in `sys.modules`; a reordered run fails 32 tests |
| `BLG-QA-210`, `BLG-QA-211`, `BLG-OPS-178` | PR #1888 review (ST-12, ST-14) | Sizing property checks only an upper bound; real-DB module binding persists; test deps in the production build |
| `BLG-FE-194` | PR #1889 review (ST-35) | Break-even trade badge still shows an up-trend glyph |
| `BLG-GOV-361`, `BLG-GOV-362` | ST-24 / ESC-EXEC-20261001-01 ruling | Stale sixth AI-adoption gate copy; standing write-scope rule for plan-named files |
| `BLG-BE-136`, `BLG-SPEC-179`, `BLG-GOV-359`, `BLG-GOV-360` | ST-20 (§13 retroactive review) | Gap Risk Flag remediation items |
| `BLG-QA-212`, `BLG-GOV-365`, `BLG-BE-137`, `BLG-GOV-366`, `BLG-GOV-367`, `BLG-SPEC-182` | PR #1891 reviews (EPIC-04) | Role-share script tests; §13.3 UK/day-0 ruling; strategy version registry drift; next AI review tracking; Skill-Silo formula mix; decision-record refresh |
| `BLG-SPEC-178` | ST-28 | New live-vs-doc divergences found by the drift detector |
| `BLG-SPEC-180`, `BLG-SPEC-181` | ST-30, ST-29 | `metrics_definitions.md` NULL fee-leg claim; action-rate spec still cites the dropped `stop_price` |
| `BLG-QA-213`, `BLG-SPEC-183`, `BLG-SPEC-184` | PR #1892 review (EPIC-05) | `fees_paid NOT NULL` regression guard; `entry_price` currency mismatch; drift detector to compare defaults |
| `BLG-GOV-368` | Sprint close | Pre-PR check that an EPIC branch carries no other EPIC's commits (PR #1886 root cause) |

## Open Escalations

None open at sprint close. All 5 escalations raised this cycle were resolved in-session on 2026-10-05, each after its SLA had passed (non-blocking, so advisory only per `shared_standards.md` §16.4.1):

| Escalation | Item | Owning authority | Disposition |
|------------|------|-------------------|-------------|
| `ESC-EXEC-20261001-01` | ST-24/EPIC-04 | Head of Specs Team | Resolved 2026-10-05 (SLA 2026-10-02) |
| `ESC-EXEC-20261001-02` | ST-19/EPIC-04 | Head of Specs Team; PMO Lead | Resolved 2026-10-05 (SLA 2026-10-04): Product Owner supplied production data |
| `ESC-EXEC-20261001-03` | ST-20/EPIC-04 | Head of Specs Team; Strategy Rules & System Intent Owner | Resolved 2026-10-05 (SLA 2026-10-04): CONDITIONAL |
| `ESC-EXEC-20261001-04` | ST-26/EPIC-04 | Head of Specs Team | Resolved 2026-10-05 (SLA 2026-10-02) |
| `ESC-EXEC-20261001-05` | ST-31/EPIC-05 | Head of Specs Team | Resolved 2026-10-05 (SLA 2026-10-02) |

**Backlog cross-reference check (AUD-2026-08-21-006):** none of these escalations carry forward past this close, so no `Source:` backfill is needed.

## Net Outcome vs Sprint Goal

The goal was met. The anchor item `BLG-BE-135` (ST-01) shipped: one canonical ATR/stop-recalculation path, persisted `stop_calculated_at`/`atr_calculated_at`/`active_atr_multiplier` (DS-22, live on staging and production), and those fields exposed on `GET /positions`. All 35 items from the sealed `stage4_backlog_slice.md` across all 6 EPICs reached `done` and merged, with no deferrals. The debt cleared covers backend reliability (EPIC-01), operational/security hardening (EPIC-02), QA/test coverage (EPIC-03), governance process and the strategy boundary (EPIC-04), spec and data-model debt including 2 live schema changes (EPIC-05), and frontend/UX (EPIC-06). The one material process deviation was the cross-EPIC merge through PR #1886. It was closed with retroactive gates, and its root cause is filed as `BLG-GOV-368`.

## Verification Readiness Statement

| Field | Status |
|-------|--------|
| All spec references populated in execution_state.json | Yes |
| All P1–P3 deviations filed and backlog references updated | Yes |
| QA evidence logs complete and DoQ sign-off non-blank for all EPICs | Yes |
