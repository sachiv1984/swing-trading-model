Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active — Signed off
Last Updated: 2026-11-06
Cycle: 2026-11-03__release-v9.15

---

# Delivery Verification Report — 2026-11-03__release-v9.15

## 1. Verification Status

```
Status: Verified_with_deviations
Sprint goal: Make every route into Trade Entry show the §4.2 pre-entry checks and pre-fill the live FX rate (BLG-FE-244, BLG-FE-245, P1). Deliver Site Structure & Usability Phase 1: navigation v2/glossary, Dashboard "Today" and Journal area specs approved, one name per page, legacy Dashboard route removed, per-page tab titles. Ship v9.15's metric-correctness, AI-check, operations, data-model and governance items alongside.
Cycle: 2026-11-03__release-v9.15
Backlog slice source: claude/cycles/2026-11-03__release-v9.15/stage4_backlog_slice.md (read with its additive stage4_backlog_slice_addendum.md; no amended_backlog_slice_path)
Verification run: 2026-11-06T14:30:00Z
Mode: standard
```

One P1 and two P2 open found defects are carried post-merge with documented Product Owner and Director of Quality acceptance: `BLG-OPS-214` (P1), `BLG-OPS-213` (P2) and `BLG-FE-271` (P2) (see §4 Acceptance Records and §9). No P0, no `Fail` result, and no traceability gap.

**Preflight (STEP -1).**
- Branch `main`.
- `execution_state.json` is `sealed: true` (2026-11-06T14:00:00Z).
- `.claude_current_state.json` status is `Sprint_Complete`.
- No amended slice. The slice pointer matches `execution_state.json.backlog_slice_source`.
- `sprint_close.md` Verification Readiness Statement: all three fields `Yes`.
- All 7 merged EPICs have a QA evidence log signed `Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)` (a compliant format), with a date, and with human DoQ/PO merge-gate confirmations.
- All 7 EPICs have a non-null `pr_number`. GitHub confirms each PR is `MERGED`.

## 2. Traceability Matrix

| ST Item | Title | Outcome | Spec Reference | Backlog Entry |
|---------|-------|---------|----------------|---------------|
| ST-01 | Show the pre-entry checks on every route into Trade Entry | merged | `position_form.md` §Pre-Entry Checks; `portfolio_endpoints.md`; `strategy_rules.md` §4.2.1/§4.2.6; `trade-entry-pre-entry-checks/decision_record.md` | N/A |
| ST-02 | Pre-fill Trade Entry's FX rate from the live rate | merged | `position_form.md` §FX Rate; `trade-entry-fx-rate/decision_record.md` | N/A |
| ST-03 | Label the FX rate the same way on entry and exit | merged | `position_form.md`; `exit_modal.md`; `trade_plan.md` | N/A |
| ST-04 | Default trade, exit and cash dates to the local date | merged | `src/lib/localDate.js`; `local-date-prefill.spec.js` | N/A |
| ST-05 | Normalise the Trade Entry ticker for ATR preview and save | merged | `portfolio_endpoints.md`; `positions.md` | N/A |
| ST-06 | Trail Stop modal ATR trail multiplier and breakeven floor | merged | `positions.md` §Trail Stop Action; `stop_trail_endpoint.md` | N/A |
| ST-07 | Signal cost incl. fees; plain-English zero-ATR reason | merged | `signals.md`; `signal_endpoints.md` | N/A |
| ST-08 | Navigation spec v2 and glossary UI-label section | merged | `navigation.md`; `glossary.md` | N/A |
| ST-09 | Dashboard spec: prioritised "Today" action list | merged | `dashboard.md` §1B | N/A |
| ST-10 | Spec for one Journal area | merged | `journal.md` | N/A |
| ST-11 | One name per page and action | merged | `glossary.md`; `navigation.md`; `src/lib/pageLabels.js` | N/A |
| ST-12 | Remove the legacy widget Dashboard route | merged | `navigation.md`; `positions.md` | N/A |
| ST-13 | Browser-tab title for each page | merged | `navigation.md` §Browser Tab Title | N/A |
| ST-14 | Three small chrome defects | merged | `navigation.md`; `dashboard.md` | N/A |
| ST-15 | Trade History counts a break-even trade as a win | merged | `metrics_definitions.md#Win Rate`; `trade_history.md#Summary Stats` | N/A |
| ST-16 | Dashboard win-rate widgets are fed from open positions only | deferred_at_planning (superseded by ST-12, PO 2026-11-03) | N/A — not executed | ✓ `BLG-FE-240` (Notes record the v9.15 deferral; the defect left with the removed page) |
| ST-17 | View Trail modal wording | merged | `positions.md#Trail Stop Action` | N/A |
| ST-18 | Strategy Benchmark Rebalance badge contrast | merged | `strategy_benchmark.md#7.3` | N/A |
| ST-19 | Price-alert duplicate fallback 500 | merged | `alerts_endpoints.md#POST /price-alerts`; `data_model.md#DS-28` | N/A |
| ST-20 | Deploy date as strategy v1.15 effective date | merged | `strategy_version_registry.py`; `strategy_rules.md` Change log | N/A |
| ST-21 | Code-written fallback when P&L summary regeneration fails | merged | `reports_endpoints.md#POST /reports/monthly-pnl/narrative`; `metrics_definitions.md` | N/A |
| ST-22 | Gap-risk weekend statistic by exchange calendar | merged | `position_endpoints.md#GET /positions/{position_id}/gap-risk`; `earnings_endpoints.md` | N/A |
| ST-23 | Open-position pnl definition aligned with code | merged | `data_model_positions_dictionary.md#5.2`; `metrics_definitions.md#Position Risk` | N/A |
| ST-24 | Review briefing ticker-caveat tokens | merged | `ai_endpoints.md#POST /ai/daily-briefing` | N/A |
| ST-25 | Journal summary advisory check: false positives and misses | merged | `ai_endpoints.md#POST /ai/journal-summary`; `ai_s13_boundary_test_suite.md` B-JS-04 | N/A |
| ST-26 | Chat stop-time focus rule: ignore non-ticker words | merged | `ai_endpoints.md#POST /ai/chat` | N/A |
| ST-27 | Journal summary check: "could/may help explain" | merged | `ai_endpoints.md#POST /ai/journal-summary`; B-JS-04 | N/A |
| ST-28 | §13 boundary clarity pass — AI journal summarisation | merged | ST-28 decision record; `strategy_rules.md` §13.2, §13.5 | N/A |
| ST-29 | ANTHROPIC_API_KEY 6-month scope audit | merged | `anthropic_api_key_scope_audit_2026-11-06.md`; `api_key_rotation_policy.md` | N/A |
| ST-30 | Rebalance-exit checks today's screener run completed | merged | `signal_endpoints.md#POST /signals/rebalance-exit`; `data_model.md#DS-39` | N/A |
| ST-31 | Skip code-test workflows on governance/docs-only pushes | merged | `detect-code-changes/action.yml`; `ci-tests.yml` | N/A |
| ST-32 | "No qualifying tickers" vs "momentum run missing" | merged | `signal_endpoints.md#POST /signals/rebalance-exit`; `data_model.md#DS-39` | N/A |
| ST-33 | Weekly market-data call-volume baseline from production | returned_to_backlog (conditional gate 2026-11-09 not cleared) | `data_model.md#DS-36`; `data_pipeline_cost_baseline.md` | ✓ `BLG-OPS-197` (Sprint return line references this cycle) |
| ST-34 | Clear the 8 success-example drifts | merged | `openapi.yaml`; `health_endpoints.md`; `reports_endpoints.md` | N/A |
| ST-35 | Re-apply NOT NULL on positions.portfolio_id/total_cost | merged | `data_model.md#DS-38` | N/A |
| ST-36 | Apply DS-17 open-position unique index to staging | merged | `data_model.md#DS-17` | N/A |
| ST-37 | Gate scan treats shipped roadmap feature ID as met | merged | `scan_backlog_gate_conditions.py`; `release_planning_prompt.md` | N/A |
| ST-38 | Consistency check counts uninitialised EPICs as pending | merged | `check_execution_state_consistency.py` | N/A |
| ST-39 | Behavioural tests for live holding days | merged | `tests/test_live_holding_days_readers.py` | N/A |
| ST-40 | Real-Postgres tests: ai_audit_log UUID[] and cost sum | merged | `test_ai_audit_uuid_and_cost_postgres.py`; `data_model.md#DS-31` | N/A |
| ST-41 | utils.* leak guard on patched attributes | merged | `tests/conftest.py` | N/A |
| ST-42 | Unique SC-TS-* Playwright scenario IDs | merged | `check_e2e_scenario_id_uniqueness.py` | N/A |
| ST-43 | Escalation SLA breach dry-run test | merged | `escalation_sla_dry_run.py`; dry-run record 2026-11-05 | N/A |
| ST-44 | Strategic exclusions review cadence | merged | ST-44 decision record | N/A |
| ST-45 | Sunset review for Priority 3 — Deferred initiatives | merged | ST-45 decision record | N/A |

Traceability gaps: 0 | Items returned: 2 (ST-33 returned in flight; ST-16 deferred at planning) | Backlog entries added this run: 0

ST-16 is recorded in `execution_state.json.deferred_at_planning` rather than as an EPIC story. Its outcome is traceable to the Product Owner decision in `sprint_backlog.md` (Items Deferred This Sprint) and to `BLG-FE-240`, so it is not counted as a gap.

## 3. QA Evidence Summary

| EPIC | Items | Pass | Fail | Sign-off | Notes |
|------|-------|------|------|----------|-------|
| EPIC-01 | 7 | 7 | 0 | ✓ DoQ (agent-mediated §5.3) 2026-11-04; human DoQ/PO 2026-11-04 | Found gap `BLG-FE-271` (P2) on ST-01, see §4 |
| EPIC-03 | 8 | 8 (ST-20 Pass_with_deviation) | 0 | ✓ DoQ 2026-11-04; human 2026-11-04T20:45Z | ST-22 found defect fixed in-sprint |
| EPIC-02 | 7 | 7 (ST-09, ST-14 Pass with notes) | 0 | ✓ DoQ 2026-11-05; human 2026-11-05T08:14Z | ST-13 found defect fixed in-sprint |
| EPIC-04 | 5 | 5 (ST-24 Pass_with_deviation) | 0 | ✓ DoQ 2026-11-05; human 2026-11-05T09:34Z (immediately after merge, `ESC-CLOSE-20261103-01`) | — |
| EPIC-06 | 3 | 3 (ST-34 Pass with notes) | 0 | ✓ DoQ 2026-11-05; human ~2026-11-05T12:48Z | ST-35 production half post-merge (seal-marked) |
| EPIC-07 | 9 | 9 (ST-40 Pass with notes; ST-42 Pass_with_deviation) | 0 | ✓ DoQ 2026-11-05; human 2026-11-05T17:40Z | ST-37 found defect fixed in-sprint; ST-45 AC 2 post-merge (seal-marked) |
| EPIC-05 | 5 (4 merged + ST-33 returned) | 4 (ST-29, ST-31 Pass_with_deviation) | 0 | ✓ DoQ 2026-11-06; human PR #2195 comment 2026-11-06T13:13:02Z | ST-33 returned (expected path) |

**STEP 2.1 / 2.3 checks.**
- Every `Result` is a recognised value.
- Each `Pass_with_deviation` names its AC gap and a confirmed backlog item. ST-31 uses the no-remainder variant: ruling `ESC-EXEC-20261105-05` exists in `execution_escalations.md` and covers ST-31 AC 1 specifically. The on-`main` confirmation is a seal-marked post-merge AC, `BLG-OPS-211`.
- Every `Pass with notes` has a substantive comment.
- All 7 sign-off blocks have every checkbox ticked.

**Found-defect rule (LL-v9.11-P4-01 / LL-v9.13-P4-01).** This was applied at every grade. `BLG-BE-206` (ST-40, Pass with notes) is P3, so it stays at the default severity. The P1/P2 found defects are in §4.

**STEP 2.2.** No AC was narrowed or omitted without a filed backlog item. The seal-marked post-merge ACs are planned remainders under LL-v9.13-P3-03 and are checked in §5, not as deviations: ST-31 AC 1 on `main` (`BLG-OPS-211`), ST-35 production (`BLG-SPEC-217`), ST-45 AC 2 (`BLG-GOV-408`) and ST-33 (`BLG-OPS-197`).

## 4. Deviation Register

No canonical-spec `DEV-*` records were filed this sprint. The register below covers every `Pass_with_deviation` gap and every found defect listed in `sprint_close.md` "Deviations Filed This Sprint". Priorities are read from `backlog.md`.

| Deviation Ref | ST Item | Priority | Description | Disposition | Backlog Item |
|---------------|---------|----------|-------------|-------------|--------------|
| PWD-ST20 | ST-20 | P3 | AC 2 partly met: v1.17 and v1.20 effective dates also need moving to deploy dates | Recorded | `BLG-BE-203` (P3) |
| PWD-ST24 | ST-24 | P3 | Production caveat-token log read not available in-sprint (`DEL-20261105-01`) | Recorded | `BLG-AI-27` (P3) |
| PWD-ST29-a | ST-29 | P3 | AC 1 not met as worded: touchpoint register omits `POST /reports/monthly-pnl/narrative` | Recorded | `BLG-SPEC-223` (P3) |
| FD-ST29-b | ST-29 | P2 | Found pre-existing defect: second key copy injected into the public GitHub Pages build as `REACT_APP_ANTHROPIC_API_KEY` | **Accepted** (PO + DoQ, 2026-11-06T10:06:48Z) | `BLG-OPS-213` (P2) |
| FD-ST29-c | ST-29 | **P1** | Found pre-existing defect: Anthropic key rotation overdue since 2026-08-25 | **Accepted** (PO + DoQ, 2026-11-06T10:06:48Z) | `BLG-OPS-214` (P1) |
| PWD-ST31 | ST-31 | P3 | AC 1 narrowed by ruling `ESC-EXEC-20261105-05` (no remainder) | Recorded (no-remainder variant) | `BLG-OPS-211` (P3, on-`main` check only) |
| PWD-ST42 | ST-42 | P3 | AC narrowed: 19 other cross-file duplicate scenario IDs remain | Recorded | `BLG-QA-250` (P3) |
| FD-ST01 | ST-01 | P2 | Found gap: plan-linked Trade Entry does not require the acknowledgement when the plan's stored checks were WARN/FAIL | **Accepted** (PO 2026-11-04; PO + DoQ re-confirmed in §9, 2026-11-06). Known Deviations: routed to Post-Ship Closure STEP 5 if the ruling applies §4.2.1 (see note) | `BLG-FE-271` (P2) |
| FD-ST22 | ST-22 | P2 | Found defect: `days_until_earnings` used server date, not US market date | Resolved in-sprint (`8861f03d`, on `main`). Carve-out, no acceptance needed | `BLG-BE-204` (P2; ✅ banner pending `groom backlog`) |
| FD-ST13 | ST-13 | P2 | Found defect: malformed Research URL blanked the app | Resolved in-sprint (`349a90d2`, on `main`). Carve-out | `BLG-FE-273` (P2; ✅ banner pending `groom backlog`) |
| FD-ST37 | ST-37 | P2 | Found defect: live PT-04 gate-scan test fails once gates clear | Resolved in-sprint (`31d5ffe2`, on `main`). Carve-out | `BLG-QA-251` (P2; ✅ banner pending `groom backlog`) |
| FD-ST40 | ST-40 | P3 | Found defect: journal-summary history returns `trade_ids` as Postgres array text | Recorded | `BLG-BE-206` (P3) |

### Hard Blocks

- P0: none.
- P1: `BLG-OPS-214`. Accepted (see below).
- P2 open: `BLG-OPS-213` is accepted. `BLG-FE-271` is accepted (PO + DoQ, §9, 2026-11-06).
- P2 resolved in-sprint: `BLG-BE-204`, `BLG-FE-273` and `BLG-QA-251`. Each fix commit was confirmed as an ancestor of `main`. Each item's own backlog entry and QA evidence log carry the resolution narrative, which is the "or equivalent" evidence under LL-v9.1-P4-01, so the Resolved-deviation carve-out (LL-v8.6-P4-03) applies.

### Acceptance Records

| Item | Priority | Accepted by | When | Rationale | Source |
|------|----------|-------------|------|-----------|--------|
| `BLG-OPS-214` | P1 | Product Owner and Director of Quality (the user, holding both roles) | 2026-11-06T10:06:48Z | Pre-existing, found by the ST-29 audit, not introduced by v9.15. The user chose to carry it past the EPIC-05 merge rather than rotate the key before merge. The item stays open and tracked as P1. | `qa_evidence_EPIC-05.md` Decisions and Escalations |
| `BLG-OPS-213` | P2 | Product Owner and Director of Quality (the user) | 2026-11-06T10:06:48Z | As above. Pre-existing second copy of the key in the Pages build secret. The remainder is tracked. | `qa_evidence_EPIC-05.md` Decisions and Escalations |
| `BLG-FE-271` | P2 | Product Owner (the user), in session, before the merge; Director of Quality and Product Owner re-confirmed in §9 | 2026-11-04; 2026-11-06 | Listed as a P2 follow-up in the EPIC-01 PO acceptance. The shipped behaviour follows the locked design record (AC 3, "not shown twice"). Whether §4.2.1 v1.23 extends to the plan-linked route needs a Strategy Rules & System Intent Owner ruling, which is `BLG-FE-271` Scope bullet 1. The DoQ confirmed it post-merge on this basis (§9). | `qa_evidence_EPIC-01.md` line 58; this report §9 |

### Known Deviations Sync (LL-v2.3-CL-03)

- The `Pass_with_deviation` rows (ST-20, ST-24, ST-29-a, ST-31, ST-42) are exempt under `ESC-CLOSE-20260930-03`. None of their comments shows shipped behaviour contradicting the cited canonical spec.
- ST-29's found defects (`BLG-OPS-213`, `BLG-OPS-214`) have no natural canonical-spec home (security audit doc and ops policy). Under `ESC-CLOSE-20260923-02`, the backlog entries, the audit doc and this register are the equivalent evidence.
- **`BLG-FE-271`: possible spec divergence, flagged to the Director of Quality.** `strategy_rules.md` §4.2.1 v1.23 (written by ST-01) says an entry "is blocked by requiring the user to acknowledge the FAIL before it can be saved". The plan-linked route does not require this. The shipped behaviour matches `position_form.md` and the locked decision record, so the divergence turns on scope: does §4.2.1 cover the plan-linked route? That is the ruling `BLG-FE-271` asks for. **Routed to Post-Ship Closure STEP 5:** if the Strategy Rules & System Intent Owner rules that §4.2.1 applies, a Known Deviations entry is needed against `strategy_rules.md` §4.2.1 / `position_form.md` §Pre-Entry Checks. This engine may not write canonical specs (§5).

## 5. Outstanding Items and Deferred Execution Blockers

### (a) Outstanding items carried to backlog

| Item | Type | Outcome | Backlog ref |
|------|------|---------|-------------|
| ST-33 | Returned to backlog (conditional, gate 2026-11-09) | Carried. The backlog entry references this cycle | `BLG-OPS-197` ✓ |
| ST-16 | Deferred at planning (superseded by ST-12) | Defect left with the removed page. The item's Notes record this. A `groom backlog` should close it | `BLG-FE-240` ✓ |
| `DEL-20261105-01` (ST-24) | Delegation in progress, carried post-merge | Tracked | `BLG-AI-27` ✓ |
| ST-31 AC 1 on `main` | Seal-marked post-merge AC | Open | `BLG-OPS-211` ✓ |
| ST-35 production half (`DEL-20261105-02`) | Seal-marked post-merge AC | Open | `BLG-SPEC-217` ✓ |
| ST-45 AC 2 | Seal-marked post-merge AC | Open | `BLG-GOV-408` ✓ |
| ST-30/ST-32 DS-39 Live Confirmation | Out-of-scope follow-up | Open | `BLG-OPS-212` ✓ |
| `ESC-EXEC-20260910-01` (cycle v9.3) | Prior-cycle Deferred escalation, non-blocking | Not from this cycle. Its trigger is still unmet | `BLG-GOV-399` ✓ |

No new `backlog.md` entries were required. Every outstanding item already has a traceable entry. `delegated_items` and `blocked_items` are empty. All ten `ESC-EXEC-*` records from this cycle are `Resolved`.

### (b) Deferred execution blocker dispositions

No deferred execution blockers. `state.json.deferred_execution_blockers` is `[]`.

### Stale parked items (STEP 4.3)

Skipped. The authoritative slice contains no `parked` items.

## 6. Test Coverage Assessment

Every EPIC has a populated `test_scenarios` list. Every listed file exists on disk and is cited in its EPIC's QA evidence log ("Scenarios run" or the per-story evidence). Frontend-visible ACs in EPIC-01, EPIC-02 and EPIC-03 have Playwright coverage. No story replaced a core algorithm, so the AUD-2026-06-22-007 advisory does not apply.

| EPIC | Scenario files | Cited as run | Status |
|------|----------------|--------------|--------|
| EPIC-01 | 10 | 10 | Covered |
| EPIC-02 | 10 | 10 | Covered |
| EPIC-03 | 9 | 9 | Covered |
| EPIC-04 | 3 | 3 | Covered |
| EPIC-05 | 4 | 4 | Covered |
| EPIC-06 | 2 | 2 | Covered |
| EPIC-07 | 7 | 7 | Covered |

### Test Scenario Gaps — Structured Register

No test scenario gaps identified. Table N/A.

Known coverage remainders are already tracked by their own backlog items and are not new gaps: `BLG-QA-250` (remaining duplicate scenario IDs) and `BLG-QA-252` / `BLG-QA-253` (CI detector fail-safe and docs-coupled selection tests).

## 7. System Status Confirmation

**Confirmed, with one minor correction.** `docs/System_status_report.md` § Sprint 2026-11-03__release-v9.15 lists all 7 merged EPICs with correct spec references. It lists ST-33 and ST-16 under "Capabilities deferred or returned" and shows every P3 and found defect against its capability row.

Corrections made this run:
1. `**Status:**` line updated from `Sprint_Complete — pending verification` to `Verified_with_deviations — 2026-11-06` (routine, BLG-GOV-170).
2. EPIC-01 Deviations cell: `BLG-FE-271` now also states that it is carried post-merge with PO acceptance, matching how EPIC-05 marks its accepted P1/P2 items.

## 9. Sign-off Block

## Director of Quality Sign-off

- [x] Traceability complete (or gaps documented with rationale)
- [x] QA evidence reviewed and accepted
- [x] Deviation register reviewed; all P0/P1/P2 dispositions confirmed
- [x] Test coverage gaps actioned (backlog items created)
- [x] System status report confirmed accurate
- [x] Deferred execution blockers dispositioned

Signed off by: Director of Quality (the user, in session)
Date: 2026-11-06
Comments: Signed off as Verified_with_deviations. `BLG-FE-271` (P2) accepted post-merge: the shipped behaviour follows the locked `trade-entry-pre-entry-checks` design record, and the item tracks the Strategy Rules & System Intent Owner ruling on whether §4.2.1 v1.23 covers the plan-linked route. `BLG-OPS-214` (P1) and `BLG-OPS-213` (P2) acceptances of 2026-11-06T10:06:48Z re-confirmed.

## Product Owner Acceptance

- [x] Outstanding items confirmed in backlog
- [x] P1/P2 deviation acceptances confirmed (if any)
- [x] Deferred execution blocker outcomes acknowledged
- [x] Next cycle cleared to open

Accepted by: Product Owner (the user, in session)
Date: 2026-11-06
Comments: Accepted. Outstanding items confirmed in backlog (`BLG-OPS-197`, `BLG-FE-240`, `BLG-AI-27`, `BLG-OPS-211`, `BLG-SPEC-217`, `BLG-GOV-408`). P1/P2 acceptances re-confirmed (`BLG-OPS-214`, `BLG-OPS-213`, `BLG-FE-271`). Next cycle cleared to open.
