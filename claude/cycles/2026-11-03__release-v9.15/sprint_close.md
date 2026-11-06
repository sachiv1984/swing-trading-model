Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-11-06
Cycle: 2026-11-03__release-v9.15

---

# Sprint Close Record — 2026-11-03__release-v9.15

## Sprint Goal

Make every route into Trade Entry show the §4.2 pre-entry checks and pre-fill the live FX rate (BLG-FE-244, BLG-FE-245, P1). Deliver Site Structure & Usability Phase 1: navigation v2/glossary, Dashboard "Today" and Journal area specs approved, one name per page, legacy Dashboard route removed, per-page tab titles. Ship v9.15's metric-correctness, AI-check, operations, data-model and governance items alongside.

## Items Done

43 of the 44 in-scope ST items are merged to `main` across 7 EPICs and 7 PRs. ST-33 was returned to the backlog in flight (below). ST-16 was deferred at planning as superseded by ST-12 and is recorded in `execution_state.json` under `deferred_at_planning`. Each Commit SHA below is the story's recorded `commit_sha` in `execution_state.json`. For a delegated story, that is the evidence commit, and the implementation commit is in the story's notes. EPICs are listed in merge order.

### EPIC-01 — Trade Entry Integrity & Sizing (PR #2189, merged 2026-11-04T19:24:41Z)

| ST | Title | Classification | Commit SHA | Spec reference(s) |
|----|-------|----------------|------------|--------------------|
| ST-01 | Show the pre-entry checks on every route into Trade Entry, not only from a Trade Plan | autonomous | `e0a78667` | `docs/design/2026-11-03__release-v9.15/trade-entry-pre-entry-checks/decision_record.md`; `docs/specs/frontend/components/position_form.md`; `docs/specs/api_contracts/portfolio_endpoints.md`; `claude/strategy/strategy_rules.md`; `tests/e2e/trade-entry-pre-entry-checks.spec.js`; `tests/test_trade_entry_pre_entry_override.py` |
| ST-02 | Pre-fill Trade Entry's FX rate from the live rate, not a fixed 1.27 | autonomous | `41e0949e` | `docs/design/2026-11-03__release-v9.15/trade-entry-fx-rate/decision_record.md`; `docs/specs/frontend/components/position_form.md`; `tests/e2e/trade-entry-fx-rate.spec.js` |
| ST-03 | Label the FX rate the same way on entry and exit | autonomous | `4c7b10ee` | `docs/specs/frontend/components/position_form.md`; `docs/specs/frontend/components/exit_modal.md`; `docs/specs/frontend/pages/trade_plan.md`; `docs/design/2026-11-03__release-v9.15/trade-entry-fx-rate/decision_record.md` |
| ST-04 | Default trade, exit and cash dates to the user's local date, not the UTC date | autonomous | `98314abf` | `src/lib/localDate.js`; `tests/e2e/local-date-prefill.spec.js`; `tests/e2e/positions-exit-modal.spec.js` |
| ST-05 | Normalise the Trade Entry ticker the same way for the ATR preview and for save | autonomous | `e0a78667` | `docs/specs/api_contracts/portfolio_endpoints.md`; `docs/specs/frontend/pages/positions.md`; `tests/test_market_atr_preview_endpoint.py` |
| ST-06 | Trail Stop modal's ATR trail value uses a hardcoded 2.0 multiplier and no breakeven floor | autonomous | `5906bfa7` | `docs/specs/frontend/pages/positions.md`; `docs/specs/api_contracts/stop_trail_endpoint.md`; `docs/design/2026-11-03__release-v9.15/trail-stop-modal-wording/decision_record.md`; `tests/test_stop_trail_value.py` |
| ST-07 | Label signal cost as including fees, and make the zero-ATR sizing reason plain English | autonomous | `cbaaecd2` | `docs/specs/frontend/pages/signals.md`; `docs/specs/api_contracts/signal_endpoints.md`; `docs/design/2026-11-03__release-v9.15/signal-card-cost-and-sizing-reason/decision_record.md`; `tests/e2e/signal-card.spec.js` |

### EPIC-03 — Metric & Display Correctness (PR #2190, merged 2026-11-04T20:55:49Z)

| ST | Title | Classification | Commit SHA | Spec reference(s) |
|----|-------|----------------|------------|--------------------|
| ST-15 | Trade History counts a break-even trade as a win | autonomous | `b478ebd1` | `docs/specs/metrics_definitions.md#Win Rate`; `docs/specs/frontend/pages/trade_history.md#Summary Stats`; `tests/e2e/trade-history-win-rate.spec.js` |
| ST-17 | Align the View Trail modal wording with the read-only ruling | autonomous | `3888f5a3` | `docs/specs/frontend/pages/positions.md#Trail Stop Action`; `docs/design/2026-11-03__release-v9.15/trail-stop-modal-wording/decision_record.md`; `tests/e2e/epic01-v34-lifecycle.spec.js` |
| ST-18 | Fix the Strategy Benchmark Rebalance badge's contrast and settle tinted vs filled exit-reason badges | autonomous | `a2e9f875` | `docs/specs/frontend/pages/strategy_benchmark.md#7.3 Exit Reason Badges`; `docs/design/2026-11-03__release-v9.15/exit-reason-badges/decision_record.md`; `tests/e2e/strategy-benchmark.spec.js` |
| ST-19 | Price-alert duplicate fallback returns 500 when the threshold has more than 4 decimal places | autonomous | `8443628c` | `docs/specs/api_contracts/alerts_endpoints.md#POST /price-alerts`; `docs/specs/data_model.md#DS-28`; `tests/test_price_alerts_service.py`; `tests/test_price_alert_db_uniqueness.py` |
| ST-20 | Use the deploy date, not the ruling date, as strategy v1.15's effective date | autonomous | `1c133336` | `backend/strategy_version_registry.py`; `claude/strategy/strategy_rules.md#Change log`; `tests/test_strategy_version_registry.py` |
| ST-21 | Show the code-written fallback when the monthly P&L summary's regeneration call fails | autonomous | `e39f22e7` | `docs/specs/api_contracts/reports_endpoints.md#POST /reports/monthly-pnl/narrative`; `docs/specs/metrics_definitions.md#AI Monthly P&L Narrative Usage`; `docs/specs/frontend/pages/reports.md#AI Summary`; `tests/test_monthly_pnl_narrative.py`; `tests/test_monthly_pnl_narrative_db.py` |
| ST-22 | Gap-risk weekend statistic: pick it by the exchange calendar and count ordinary weekends | autonomous | `ee3460ee` | `docs/specs/api_contracts/position_endpoints.md#GET /positions/{position_id}/gap-risk`; `docs/specs/api_contracts/earnings_endpoints.md#GET /earnings/{ticker}`; `docs/product/decisions/decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md`; `tests/test_gap_risk.py` |
| ST-23 | Open-position pnl: code uses the live FX rate and does not deduct fees; the dictionary says entry-time FX, fees deducted | autonomous | `607995a6` | `docs/specs/data_model_positions_dictionary.md#5.2 pnl (GBP)`; `docs/specs/metrics_definitions.md#Position Risk` |

### EPIC-02 — Site Structure & Usability Phase 1 — Specs, Vocabulary & Quick Wins (PR #2191, merged 2026-11-05T08:21:26Z)

| ST | Title | Classification | Commit SHA | Spec reference(s) |
|----|-------|----------------|------------|--------------------|
| ST-08 | Navigation spec v2: job-based areas, plus a UI-label section in the glossary | autonomous | `32b84b68` | `docs/specs/frontend/pages/navigation.md`; `docs/reference/glossary.md`; `docs/design/2026-11-03__release-v9.15/site-structure-phase1/decision_record.md` |
| ST-09 | Dashboard spec: a prioritised "Today" action list | autonomous | `b901ce91` | `docs/specs/frontend/pages/dashboard.md`; `docs/design/2026-11-03__release-v9.15/site-structure-phase1/decision_record.md` |
| ST-10 | Spec for one Journal area combining reflections, red flags and position notes | autonomous | `ae087433` | `docs/specs/frontend/pages/journal.md`; `docs/design/2026-11-03__release-v9.15/site-structure-phase1/decision_record.md` |
| ST-11 | Use one name per page and action across sidebar, page headings and command palette | autonomous | `de1343a0` | `docs/reference/glossary.md`; `docs/specs/frontend/pages/navigation.md`; `docs/design/2026-11-03__release-v9.15/site-structure-phase1/decision_record.md`; `src/lib/pageLabels.js`; `tests/e2e/page-labels-single-source.spec.js` |
| ST-12 | Remove the legacy widget Dashboard route and its duplicate command-palette entry | autonomous | `c8523403` | `docs/specs/frontend/pages/navigation.md`; `docs/specs/frontend/pages/positions.md`; `docs/design/2026-11-03__release-v9.15/site-structure-phase1/decision_record.md`; `tests/e2e/legacy-dashboard-redirect.spec.js` |
| ST-13 | Set a browser-tab title for each page | autonomous | `b7fefee0` | `docs/specs/frontend/pages/navigation.md`; `docs/design/2026-11-03__release-v9.15/site-structure-phase1/decision_record.md`; `src/lib/pageLabels.js`; `tests/e2e/browser-tab-title.spec.js` |
| ST-14 | Fix three small chrome defects: version label, What's New heading, sidebar height | autonomous | `9de8cd20` | `docs/specs/frontend/pages/navigation.md`; `docs/specs/frontend/pages/dashboard.md`; `docs/design/2026-11-03__release-v9.15/site-structure-phase1/decision_record.md`; `tests/e2e/sidebar-chrome.spec.js` |

### EPIC-04 — AI Output Checks & §13 Boundary (PR #2192, merged 2026-11-05T09:34:02Z)

| ST | Title | Classification | Commit SHA | Spec reference(s) |
|----|-------|----------------|------------|--------------------|
| ST-24 | Review logged briefing ticker-caveat tokens for further non-tickers | delegated_backend | `aad0d041` | `docs/specs/api_contracts/ai_endpoints.md#POST /ai/daily-briefing`; `tests/test_briefing_summary_ticker_check.py` |
| ST-25 | Journal summary advisory check: remaining false positives and misses | autonomous | `e6ba8e52` | `docs/specs/api_contracts/ai_endpoints.md#POST /ai/journal-summary`; `docs/specs/qa/ai_s13_boundary_test_suite.md#Scenario B-JS-04 — No advice to change stops, sizing or setups in output`; `tests/test_journal_summary_language_check.py` |
| ST-26 | Chat stop-time focus rule: ignore common upper-case non-ticker words | autonomous | `b937a396` | `docs/specs/api_contracts/ai_endpoints.md#POST /ai/chat`; `tests/test_ai_stop_time_focus_attribution.py` |
| ST-27 | Journal summary advisory check: do not flag "could/may help explain" | autonomous | `e6ba8e52` | `docs/specs/api_contracts/ai_endpoints.md#POST /ai/journal-summary`; `docs/specs/qa/ai_s13_boundary_test_suite.md#Scenario B-JS-04 — No advice to change stops, sizing or setups in output`; `tests/test_journal_summary_language_check.py` |
| ST-28 | §13 boundary language clarity pass — AI journal summarisation | autonomous | `122619e9` | `docs/product/decisions/decisions--2026-11-03__release-v9.15--ST-28-journal-summary-section13-reread.md`; `claude/strategy/strategy_rules.md#13.2 This system is not`; `claude/strategy/strategy_rules.md#13.5 Semi-Annual Boundary Re-Attestation Cadence (ST-23, BLG-GOV-204, EPIC-05, v8.3)`; `tests/test_strategy_version_registry.py` |

### EPIC-06 — Data Model & Spec Debt (PR #2193, merged 2026-11-05T12:57:11Z)

| ST | Title | Classification | Commit SHA | Spec reference(s) |
|----|-------|----------------|------------|--------------------|
| ST-34 | Clear the 8 pre-existing success-example drifts so check_contract_example_freshness.py exits 0 | autonomous | `ff08b950` | `docs/reference/openapi.yaml`; `docs/specs/api_contracts/health_endpoints.md`; `docs/specs/api_contracts/reports_endpoints.md`; `scripts/check_contract_example_freshness.py`; `tests/test_check_contract_example_freshness.py` |
| ST-35 | Re-apply NOT NULL on positions.portfolio_id and positions.total_cost | delegated_backend | `e5a7f45f` | `docs/specs/data_model.md#DS-38` |
| ST-36 | Apply DS-17's open-position unique index to staging | delegated_backend | `dfee397b` | `docs/specs/data_model.md#DS-17` |

### EPIC-07 — QA & Governance Tooling (PR #2194, merged 2026-11-05T17:54:06Z)

| ST | Title | Classification | Commit SHA | Spec reference(s) |
|----|-------|----------------|------------|--------------------|
| ST-37 | Gate scan treats a shipped roadmap feature ID (PT-xx, SI-xx, PO-xx) as a met gate | autonomous | `ba28ae59` | `scripts/scan_backlog_gate_conditions.py`; `tests/test_scan_backlog_gate_conditions_gating_item_shipped.py`; `claude/system/release_planning_prompt.md` |
| ST-38 | Make the execution-state consistency check count EPICs not yet initialised as pending | autonomous | `7eaf4516` | `scripts/check_execution_state_consistency.py`; `tests/test_check_execution_state_consistency.py` |
| ST-39 | Behavioural tests for live holding days in the compliance and AI briefing readers | autonomous | `3133b9b2` | `tests/test_live_holding_days_readers.py` |
| ST-40 | Real-Postgres tests for the ai_audit_log UUID[] path and the claude_audit_log daily cost sum | autonomous | `7bb6e2d6` | `tests/test_ai_audit_uuid_and_cost_postgres.py`; `docs/specs/data_model.md#DS-31` |
| ST-41 | Extend the utils.* leak guard to attributes patched on the real utils modules | autonomous | `27c36319` | `tests/conftest.py`; `tests/test_utils_attribute_leak_guard.py` |
| ST-42 | Make SC-TS-* Playwright scenario IDs unique across tests/e2e | autonomous | `b0826ad3` | `scripts/check_e2e_scenario_id_uniqueness.py`; `tests/test_check_e2e_scenario_id_uniqueness.py`; `tests/e2e/epic01-v62-stops-alerts.spec.js` |
| ST-43 | Escalation SLA breach dry-run test | autonomous | `6446bb3c` | `scripts/escalation_sla_dry_run.py`; `tests/test_escalation_sla_dry_run.py`; `docs/ops/escalation_sla_breach_dry_run_2026-11-05.md` |
| ST-44 | Strategic exclusions review cadence | autonomous | `a403948a` | `docs/product/decisions/decisions--2026-11-03__release-v9.15--ST-44-strategic-exclusions-reconfirmation.md` |
| ST-45 | Sunset review for Priority 3 — Deferred initiatives | autonomous | `f7e3983d` | `docs/product/decisions/decisions--2026-11-03__release-v9.15--ST-45-priority3-deferred-sunset-review.md` |

### EPIC-05 — Operations, Security & Market-Data Monitoring (PR #2195, merged 2026-11-06T13:13:42Z)

| ST | Title | Classification | Commit SHA | Spec reference(s) |
|----|-------|----------------|------------|--------------------|
| ST-29 | ANTHROPIC_API_KEY 6-month scope audit | delegated_backend | `5e83a975` | `docs/security/anthropic_api_key_scope_audit_2026-11-06.md`; `docs/ops/api_key_rotation_policy.md` |
| ST-30 | Rebalance-exit generation should check that today's screener run completed | autonomous | `e0329f64` | `docs/specs/api_contracts/signal_endpoints.md#POST /signals/rebalance-exit`; `docs/specs/data_model.md#DS-39`; `tests/test_nightly_computations.py`; `tests/test_momentum_signal_run_marker.py` |
| ST-31 | Skip the five code-test workflows on governance-only and docs-only pushes | autonomous | `898003a9` | `.github/actions/detect-code-changes/action.yml`; `.github/workflows/ci-tests.yml`; `tests/test_ci_code_changes.py` |
| ST-32 | Tell "no qualifying tickers" apart from "momentum run missing" in the month-end rebalance job | autonomous | `e0329f64` | `docs/specs/api_contracts/signal_endpoints.md#POST /signals/rebalance-exit`; `docs/specs/data_model.md#DS-39`; `tests/test_nightly_computations.py`; `tests/test_momentum_signal_run_marker.py` |

## Items Returned to Backlog

| ST | Title | Reason | Backlog reference |
|----|-------|--------|-------------------|
| ST-33 | Record the weekly market-data call-volume baseline from production | Conditional item (`release_planning_prompt.md` §1.4b). Its gate, 7 full days of production data after the 2026-11-02 deploy, opens on 2026-11-09 and could not clear before EPIC-05 merged. Returned in flight on 2026-11-05T18:01:44Z with Product Owner authorisation (AUD-2026-05-27-003). This was the expected path in `sprint_backlog.md` ST-33 Notes, so it is not a deviation. No delegation record was raised. | `BLG-OPS-197` (stays open; return noted in the item, 2026-11-06) |

## Items Delegated and Outstanding

No story is outstanding. `delegated_items` and `blocked_items` are empty. Delegation log outcomes:

| Record | Story | Outcome |
|--------|-------|---------|
| `DEL-20261105-01` | ST-24 (EPIC-04) | In Progress — carried post-merge. The production caveat-token log read was not available in-sprint. ST-24 is graded `Pass_with_deviation` and the read is tracked by `BLG-AI-27`. |
| `DEL-20261105-02` | ST-35 (EPIC-06) | Unblocked 2026-11-05: staging pre-check, migration and verification outputs supplied in session. Production half post-merge under `BLG-SPEC-217`. |
| `DEL-20261105-03` | ST-36 (EPIC-06) | Unblocked 2026-11-05: staging DS-17 migration and verification output supplied in session. |
| `DEL-20261105-04` | ST-29 (EPIC-05) | Unblocked 2026-11-06: Anthropic console key list (names and dates only) supplied in session. AC 2 (rotation) not met; tracked by `BLG-OPS-214` (P1). |

## QA Evidence Logs Produced

Every log has a completed Standard Sign-Off Block with a non-blank date and a `## Merge Gate Confirmations` section. In every EPIC, the human Director of Quality and Product Owner (one person holding both roles) gave QA sign-off and PO acceptance explicitly, then merged the PR.

| EPIC | Log | Agent-mediated DoQ review | Human confirmation and merge |
|------|-----|---------------------------|------------------------------|
| EPIC-01 | `qa_evidence_EPIC-01.md` | Pass 1 Blocked (2), pass 2 Approved | In session 2026-11-04; merged `46307e1d` |
| EPIC-03 | `qa_evidence_EPIC-03.md` | Pass 1 Blocked (2), pass 2 Approved | In session 2026-11-04T20:45Z; merged `9df0cc9a` |
| EPIC-02 | `qa_evidence_EPIC-02.md` | Pass 1 Approved (4 record fixes) | In session 2026-11-05T08:14Z; merged `b668350b` |
| EPIC-04 | `qa_evidence_EPIC-04.md` | Pass 1 Blocked (2), pass 2 Approved | In session 2026-11-05T09:34Z, immediately after the merge; merged `ba053acf` |
| EPIC-06 | `qa_evidence_EPIC-06.md` | Pass 1 Blocked (1), pass 2 Approved | In session 2026-11-05 at about 12:48Z; merged `54c2895a` |
| EPIC-07 | `qa_evidence_EPIC-07.md` | Pass 1 Approved | In session 2026-11-05T17:40Z; merged `89157ca5` |
| EPIC-05 | `qa_evidence_EPIC-05.md` | Pass 1 Blocked (3), pass 2 Approved | PR #2195 comment 2026-11-06T13:13:02Z; merged `0e0bac2a` |

## Process Notes

Rolled up from `execution_state.json.process_notes` (15 entries, 2026-11-04 to 2026-11-06):

- **Per-EPIC initialisation.** Each EPIC initialised its own `execution_state.json` section at its STEP 0, in merge order. `merge_gate.epics_pending` listed only initialised EPICs, so `all_merged` briefly read `true` after EPIC-01 and EPIC-03 merged while later EPICs were not started. ST-38 (EPIC-07) fixed the consistency check to count uninitialised EPICs as pending.
- **Delegated decisions resolved in session.** ST-01, ST-06, ST-12, ST-20, ST-23, ST-25/ST-27, ST-28, ST-31, ST-44 and ST-45 each needed a ruling. All ten escalations (`ESC-EXEC-20261104-01` to `-05`, `ESC-EXEC-20261105-01` to `-05`) were raised and resolved in session, and the stories were reclassified autonomous where applicable.
- **EPIC-04 sign-off timing.** The human QA sign-off and PO acceptance for EPIC-04 were given immediately after the merge (2026-11-05T09:34Z), not before it. The merger holds both roles, so the merge also counts as confirmation under `ESC-CLOSE-20261103-01`.
- **ST-33 returned in flight** on 2026-11-05T18:01:44Z (see Items Returned to Backlog).
- **Orphaned post-merge commit checks (LL-v6.8-P3-01).** Run at each merge, and again at this close for all seven branches: `git log origin/main..origin/exec/2026-11-03__release-v9.15/EPIC-0{1..7}` returned no commits. Nothing to reconcile.
- **Sibling-branch sync (STEP 4 step 3c).** Recorded as not needed at each merge: no later EPIC branch existed yet when an earlier EPIC merged.
- **EPIC-05 merge recorded at resume.** PR #2195 was merged by the human at 2026-11-06T13:13:42Z between sessions. This session's resume-sync recorded it on `main` in `3c87881b`.

## Deviations Filed This Sprint

No new canonical-spec `DEV-*` records were filed. Every merged story's deviation check finished with `deviations_filed = true`.

Five stories are graded `Pass_with_deviation`. All are disclosed and tracked, and none is P0. The deviation severity is the `delivery_verification_prompt.md` STEP 2.1 P3 default, consistent with the DoQ assessments. The tracking item's own `**Priority:**` was read from `backlog.md` (LL-v9.12-P4-01). Found pre-existing defects filed at P1 or P2 are also listed (LL-v9.13-P4-01).

| Story | Grade | Gap or found defect | Deviation severity | Tracking item | Tracking item priority |
|-------|-------|---------------------|--------------------|---------------|------------------------|
| ST-20 | Pass_with_deviation | AC 2 partly met: under the deploy-date rule, strategy v1.17 and v1.20 effective dates also need moving | P3 | `BLG-BE-203` | P3 |
| ST-24 | Pass_with_deviation | Production caveat-token log read not available in-sprint (`DEL-20261105-01`) | P3 | `BLG-AI-27` | P3 |
| ST-29 | Pass_with_deviation | AC 1 not met as worded: the touchpoint register omits `POST /reports/monthly-pnl/narrative` | P3 | `BLG-SPEC-223` | P3 |
| ST-29 | Pass_with_deviation | Found defect (AC 1): a second copy of the key is injected into the public GitHub Pages build as `REACT_APP_ANTHROPIC_API_KEY` | P2 | `BLG-OPS-213` | P2 |
| ST-29 | Pass_with_deviation | Found defect (AC 2 not met): the Anthropic key rotation is overdue since 2026-08-25 | P1 | `BLG-OPS-214` | P1 |
| ST-31 | Pass_with_deviation | AC 1 narrowed by ruling `ESC-EXEC-20261105-05`; no remainder. The on-`main` check is post-merge | P3 | `BLG-OPS-211` | P3 |
| ST-42 | Pass_with_deviation | AC narrowed (Product Owner, in session): 19 other cross-file duplicate scenario IDs remain | P3 | `BLG-QA-250` | P3 |
| ST-22 | Pass | Found defect, from the PR #2190 review: `days_until_earnings` uses the server date, not the US market date. Fixed before merge in `8861f03d` | P2 | `BLG-BE-204` | P2 |
| ST-37 | Pass | Found defect, from the PR #2194 review: the live PT-04 gate-scan test fails once Release Planning clears those gates. Fixed in `31d5ffe2` | P2 | `BLG-QA-251` | P2 |
| ST-01 | Pass | Found gap, from the PR #2189 Product Owner review: plan-linked Trade Entry does not require the acknowledgement when the plan's checks were WARN/FAIL | P2 | `BLG-FE-271` | P2 |
| ST-13 | Pass | Found defect, from the PR #2191 review: a malformed Research URL blanks the app. Fixed in `349a90d2` (SC-BTT-07) | P2 | `BLG-FE-273` | P2 |

**P1 carried post-merge.** `BLG-OPS-214` (P1) and `BLG-OPS-213` (P2) are pre-existing problems that ST-29's audit found. The Product Owner and Director of Quality accepted carrying both post-merge, in session at 2026-11-06T10:06:48Z (`qa_evidence_EPIC-05.md` Decisions and Escalations). Delivery verification STEP 2.1 routes them to the §7 PO + DoQ path.

**Pass with notes.** ST-09 and ST-14 (EPIC-02), ST-34 (EPIC-06, `BLG-SPEC-222`) and ST-40 (EPIC-07, `BLG-BE-206`) are graded `Pass with notes`. All their in-sprint ACs are met.

**Fixed in-sprint but not yet marked complete in `backlog.md`.** `BLG-BE-204` (`8861f03d`), `BLG-FE-273` (`349a90d2`) and `BLG-QA-251` (`31d5ffe2`) were fixed before their EPIC PRs merged, but the items carry no ✅ COMPLETE banner. This routine may write `backlog.md` only for STEP 5.2 returns, so they are left for the next `groom backlog`.

**Post-merge ACs filed at Sprint Planning.** `BLG-OPS-211` (ST-31 AC 1), `BLG-SPEC-217` (ST-35 production half), `BLG-GOV-408` (ST-45 AC 2) and `BLG-OPS-197` (ST-33) remain open.

Backlog follow-ups filed during execution (41 items). These are out-of-scope findings, not spec deviations:

| Backlog ID | Filed by | Reason |
|------------|----------|--------|
| `BLG-FE-269`, `BLG-FE-270`, `BLG-FE-271`, `BLG-QA-244` | EPIC-01 DoQ review, PR #2189 review | Reset the acknowledgement when checks change; Trail Stop footnote at a loss; acknowledgement on plan-linked entry; ⌘K toast in Playwright |
| `BLG-BE-203`, `BLG-SPEC-218`, `BLG-SPEC-219`, `BLG-BE-204`, `BLG-QA-245`, `BLG-FE-272` | ST-20, ST-23, PR #2190 review (EPIC-03) | v1.17/v1.20 effective dates; unrealised vs realised pnl basis; `pnl_pct` definition; earnings date basis; unmapped exit-reason contrast; failed Regenerate behaviour |
| `BLG-BE-205`, `BLG-GOV-409`, `BLG-SPEC-220`, `BLG-QA-246`, `BLG-FE-273`, `BLG-FE-274` | ST-09, ST-08, ST-12, PR #2191 review (EPIC-02) | Stop-moved timestamp; IDs-in-headings clash; "Daily Monitor" button; retarget removed token tests; malformed URL tab title; removed Dashboard charts |
| `BLG-AI-27`, `BLG-AI-28`, `BLG-AI-29`, `BLG-AI-30`, `BLG-AI-31`, `BLG-AI-32`, `BLG-AI-33` | ST-24, ST-26, EPIC-04 DoQ review, PR #2192 review | Production caveat tokens; non-ticker words that are tickers; §13.2 check for briefing/chat; journal-summary check precision and coverage; linear reported-speech check |
| `BLG-SPEC-221`, `BLG-QA-247`, `BLG-SPEC-222`, `BLG-QA-248`, `BLG-QA-249` | ST-34, ST-35/ST-36, PR #2193 review (EPIC-06) | `Specs_Index.md` freshness; drift-check index regex; gate on example freshness; nested example keys; NOT NULL seed guard |
| `BLG-BE-206`, `BLG-QA-250`, `BLG-GOV-410`, `BLG-GOV-411`, `BLG-GOV-412`, `BLG-QA-251` | ST-40, ST-42, ST-43, PR #2194 review (EPIC-07) | Journal-summary `trade_ids` as UUID strings; remaining duplicate scenario IDs; SLA-breach rule for non-blocking escalations; one disposition set; exclusions re-confirmation trigger; live PT-04 test |
| `BLG-OPS-212`, `BLG-SPEC-223`, `BLG-OPS-213`, `BLG-OPS-214`, `BLG-BE-207`, `BLG-QA-252`, `BLG-QA-253` | ST-30/ST-32, ST-29, PR #2195 review (EPIC-05) | DS-39 live confirmation; touchpoint register; public-build key copy; key rotation; non-default momentum runs; detector fail-safe tests; docs-coupled test selection |

## Open Escalations

None for this cycle. All ten `ESC-EXEC-*` records raised in this cycle are `Resolved` in `execution_escalations.md` and `execution_state.json`. The only unresolved escalation in `.claude_current_state.json` is `ESC-EXEC-20260910-01` (cycle `2026-09-09__release-v9.3`, Deferred, non-blocking), which is not from this cycle.

## Net Outcome vs Sprint Goal

**Met.**
- **Trade Entry (P1).** Every route into Trade Entry now shows the §4.2 pre-entry checks (ST-01, Branch A ruling, `strategy_rules.md` v1.23). The FX rate is pre-filled from the live rate, with save validation for US trades (ST-02). Labels, local dates, ticker normalisation, the trail value and sizing wording were also corrected (ST-03 to ST-07).
- **Site Structure & Usability Phase 1.** Navigation spec v2 with a glossary UI-label section (ST-08), the Dashboard "Today" spec (ST-09) and the Journal area spec (ST-10) are approved. One name per page and action (ST-11). The legacy Dashboard route is removed, with the Daily Position Monitor moved per ruling `ESC-EXEC-20261104-05` (ST-12). Per-page tab titles (ST-13) and three chrome fixes (ST-14).
- **Alongside.** Metric and display correctness (EPIC-03), AI output checks and §13 clarity (EPIC-04), data model and spec debt (EPIC-06), QA and governance tooling (EPIC-07), and operations and security (EPIC-05) shipped, except ST-33, which is gated on production data.

The goal's commitments are delivered. The open risk is ST-29's finding that the Anthropic key rotation is overdue (`BLG-OPS-214`, P1). It is pre-existing, outside the goal, and accepted post-merge by the PO and DoQ.

## Verification Readiness Statement
| Field | Status |
|-------|--------|
| All spec references populated in execution_state.json | Yes |
| All P1–P3 deviations filed and backlog references updated | Yes |
| QA evidence logs complete and DoQ sign-off non-blank for all EPICs | Yes |
