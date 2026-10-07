Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-10-07
Cycle: 2026-10-06__release-v9.10

---

# Sprint Close Record — 2026-10-06__release-v9.10

## Sprint Goal

Make every live stop come from one §11 parameter source, and show the ATR, multiplier, recalculation source and already-known exit conditions behind each position (BLG-BE-138, BLG-FE-193, BLG-FE-198), while clearing v9.10's lifecycle/gap-risk rulings and AI-governance, ops and QA hygiene items.

## Items Done

All 21 in-scope ST items reached `done` and are merged to `main` across 4 EPICs and 4 PRs. Commit SHAs are each story's recorded `commit_sha` in `execution_state.json`.

### EPIC-01 — Stop-Parameter Correctness & ATR Integrity (PR #1915, merged 2026-10-06T21:00:45Z)

| ST | Title | Commit SHA | Spec reference(s) |
|----|-------|------------|--------------------|
| ST-01 | One source for §11 stop parameters across the on-load and nightly stop paths | `333e9d00` | `claude/strategy/strategy_rules.md#11. Current production parameters`; `backend/utils/strategy_parameters.py`; `docs/specs/frontend/pages/settings.md#Strategy Parameter Presentation`; `docs/specs/data_model.md#DS-26`; `tests/test_strategy_parameter_parity.py`; `tests/e2e/settings-strategy-parameters-fixed.spec.js` |
| ST-02 | Remove silent ATR fallbacks and record ATR provenance | `333e9d00` | `docs/specs/data_model.md#DS-25`; `docs/specs/api_contracts/position_endpoints.md#GET /positions`; `docs/reference/openapi.yaml`; `tests/test_atr_provenance.py` |
| ST-03 | Contract corrections: losing-stop formula, analyze side effects, settings-change effect | `37f4cbfd` | `docs/specs/api_contracts/position_endpoints.md`; `docs/specs/api_contracts/settings_endpoints.md` |
| ST-04 | Unit-test the live exit decision and grace-period behaviour | `f9aa7f57` | `claude/strategy/strategy_rules.md`; `docs/testing/strategy_rule_test_traceability_matrix.md`; `tests/test_live_exit_decision.py` |
| ST-05 | Rule on strategy-version registry coverage and enforce it with a test | `60f77f91` | `docs/specs/data_model.md#DS-11`; `docs/specs/api_contracts/strategy_version_comparison_contract.md`; `tests/test_strategy_version_registry.py` |

### EPIC-02 — Stop & Exit Transparency (PR #1916, merged 2026-10-07T06:59:46Z)

| ST | Title | Commit SHA | Spec reference(s) |
|----|-------|------------|--------------------|
| ST-06 | Show ATR, active multiplier and recalculation source in the stop-loss cell | `b1921fd1` | `docs/specs/frontend/pages/positions.md#Stop Provenance Line and Per-Row Stop Details`; `docs/design/2026-10-06__release-v9.10/stop-cell-provenance/decision_record.md`; `tests/e2e/stop-cell-provenance.spec.js` |
| ST-07 | Trade Entry shows the stop and risk the system will actually store | `e5df8e65` | `docs/specs/frontend/components/position_form.md#Initial Stop (set by system)`; `docs/design/2026-10-06__release-v9.10/trade-entry-system-stop/decision_record.md`; `tests/e2e/trade-entry-system-stop.spec.js`; `tests/test_add_position_stop_handling.py` |
| ST-08 | Exit dialog pre-selects the exit reason the system already knows | `1d7b7a24` | `docs/specs/frontend/pages/positions.md#Exit Dialog Pre-Selection and Deep Link`; `tests/e2e/exit-condition-surfacing.spec.js` |
| ST-09 | Morning briefing card for §8 exit recommendations | `1d7b7a24` | `docs/specs/frontend/pages/dashboard.md#Exit Conditions Met Row`; `tests/e2e/exit-condition-surfacing.spec.js` |
| ST-10 | Recent Trades badge shows a neutral glyph for a break-even trade | `89f16aa4` | `tests/e2e/recent-trades-zero-pnl-badge.spec.js` |

### EPIC-03 — Lifecycle & Gap-Risk Strategy Boundary (PR #1917, merged 2026-10-07T08:06:08Z)

| ST | Title | Commit SHA | Spec reference(s) |
|----|-------|------------|--------------------|
| ST-11 | Reconcile the lifecycle-state registry with strategy_rules.md §9 | `05ad3ecf` | `docs/specs/position_lifecycle_states_registry.md#Relationship to strategy_rules.md §9`; `claude/strategy/strategy_rules.md#9. Position states`; `docs/specs/data_model.md#Position Lifecycle`; `docs/specs/api_contracts/position_endpoints.md#GET /positions`; `tests/test_position_lifecycle.py`; `tests/e2e/lifecycle-badge-grace-calendar-days.spec.js` |
| ST-12 | Positions lifecycle badge agrees with the §6 grace window, in calendar days | `0e8a431b` | `docs/specs/frontend/pages/positions.md#Grace Precedence and UNKNOWN Reasons`; `docs/specs/api_contracts/position_endpoints.md#GET /positions`; `docs/specs/api_contracts/grace_period_alert_endpoint.md`; `tests/e2e/lifecycle-badge-grace-calendar-days.spec.js` |
| ST-13 | Gap Risk Flag §13.3 ruling on UK-ticker earnings flags and day-0 timing | `05ad3ecf` | `docs/product/decisions/decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md#Addendum — v9.10 Rulings`; `claude/strategy/strategy_rules.md#4.2.3`; `claude/strategy/strategy_rules.md#13.3`; `tests/test_gap_risk.py` |
| ST-14 | Gap risk flag: disposition the standalone weekend-hold trigger and align trigger-timing label/spec with code | `05ad3ecf` | `docs/specs/api_contracts/position_endpoints.md#GET /positions/{position_id}/gap-risk`; `docs/reference/openapi.yaml`; `docs/specs/frontend/pages/positions.md#Gap Risk Reason Labels`; `docs/design/2026-07-10__release-v6.9/gap-risk-flag/ux_spec.md`; `docs/design/2026-10-06__release-v9.10/gap-risk-trigger-label-alignment/decision_record.md`; `tests/test_gap_risk.py`; `tests/e2e/gap-risk-flag.spec.js` |

### EPIC-04 — AI Governance, Ops & QA Hygiene (PR #1918, merged 2026-10-07T10:31:10Z)

| ST | Title | Commit SHA | Spec reference(s) |
|----|-------|------------|--------------------|
| ST-15 | AI chat advisory §13 quarterly self-audit checklist | `b84b12fb` | `docs/ops/ai_chat_section13_quarterly_self_audit_checklist.md` |
| ST-16 | AI model output logging completeness audit | `ef167325` | `docs/ops/ai_output_logging_completeness_audit_2026-10-06.md`; `tests/test_claude_audit_entry_failure_logging.py` |
| ST-17 | Quarterly dependency update review | `05600e77` | `docs/security/dependency_update_review_2026-10-06.md` |
| ST-18 | Confirm the stale-staging-deploy alert fires on a real stale-staging condition | `51269188` | `scripts/staging_smoke_test.py`; `.github/workflows/staging-smoke-test.yml`; `tests/test_staging_smoke_test.py` |
| ST-19 | Add the Reports and Notifications pages to the axe accessibility scan | `b8ced55f` | `tests/e2e/accessibility-axe-scan.spec.js` |
| ST-20 | Correct the PO-05 pre-assessment and replay page spec wording | `50dc7154` | `docs/product/decisions/po05_section13_preassessment.md#v9.10 Corrections`; `docs/specs/frontend/pages/replay_mode.md#§13 Boundary`; `docs/product/decisions/po05_replay_scope_confirmation.md`; `claude/roadmap/current_roadmap.md`; `tests/e2e/replay-mode.spec.js` |
| ST-21 | Sign-off single-point-of-failure matrix | `d87aa8d1` | `docs/ops/sign_off_single_point_of_failure_matrix.md` |

## Items Returned to Backlog

None. All 21 in-scope items reached `done`.

## Items Delegated and Outstanding

None outstanding. There were four delegation records this cycle, and all are terminal:

- **DEL-20261006-01** (ST-01/EPIC-01, production read): `Unblocked`, in-session (2026-10-06T17:34:46Z). The user supplied both production query outputs. The settings row equals §11 (10/14/5.00/2.00), and none of the 4 open positions has a diverged stop, so no AC 6 correction is owed.
- **DEL-20261006-02** (ST-02/EPIC-01, `delegated_backend`): `Unblocked`, in-session (2026-10-06T17:38:42Z). The user applied DS-25 (`atr_source`) on staging, then production. Verified live.
- **DEL-20261006-03** (ST-18/EPIC-04, live fire): `Unblocked`, in-session (2026-10-07T09:45:20Z). The user, acting for the Infrastructure & Operations Owner, set the missing `STAGING_API_URL` secret (BLG-OPS-180) and ran the live fire. Failing run 37598457966 and passing run 37602589130.
- **DEL-20261006-04** (ST-01/EPIC-01, `delegated_backend`): `Unblocked`, in-session (2026-10-06T17:38:42Z). The user applied DS-26 (`stop_calculation_source`) on staging, then production. Verified live.

## QA Evidence Logs Produced

- `claude/cycles/2026-10-06__release-v9.10/qa_evidence_EPIC-01.md`: agent-mediated (Director of Quality role, §5.3), 2026-10-06
- `claude/cycles/2026-10-06__release-v9.10/qa_evidence_EPIC-02.md`: agent-mediated (Director of Quality role, §5.3), 2026-10-07
- `claude/cycles/2026-10-06__release-v9.10/qa_evidence_EPIC-03.md`: agent-mediated (Director of Quality role, §5.3), 2026-10-07
- `claude/cycles/2026-10-06__release-v9.10/qa_evidence_EPIC-04.md`: agent-mediated (Director of Quality role, §5.3), 2026-10-07. The first pass was Blocked; it was approved with comments on retry 1.

All four sign-off `Date:` fields are non-blank, and `qa_signed_off: true` is set for all four EPICs. Each was signed on the user's explicit direction and is labelled "pending human confirmation". A human merged every PR.

## Process Notes

Rolled up from `execution_state.json.process_notes` (26 entries, 2026-10-06 to 2026-10-07):

- **Strategy rulings unblocked the sprint inside one day.** Six escalations were raised (five Strategy, one Lifecycle). ST-01 and ST-05 were ruled directly by the user on 2026-10-06. ST-11, ST-13/ST-14 and ST-20 were ruled on 2026-10-07 through agent-mediated Strategy Rules & System Intent Owner rulings on the user's direction. ST-15 was approved by the human Product Owner. ST-06/ST-07 were held as `blocked_decision` on ST-01's ruling, then resumed as `autonomous`. Every escalation was resolved before its SLA.
- **ST-18 exposed a long-standing ops gap.** The `STAGING_API_URL` secret had never been set, so all 126 prior `staging-smoke-test.yml` runs had failed at the env check without anyone noticing (BLG-OPS-180, P1). The first live run then reported a false-positive `STALE STAGING DEPLOY`, because the check compared staging against `main`'s tip and a governance-only commit never redeploys staging. The engine changed the comparison target to the latest staging-deploying commit (`23c6810f`). ST-18 AC 1 is narrowed and tracked: the failing run diverged staging from the EPIC-04 branch, not from `main` (BLG-OPS-182). The hook deploy that never went live is BLG-OPS-181.
- **ST-19's own axe test failed in real CI.** It failed (`scrollable-region-focusable`) on every EPIC-04 code commit. The STEP 3.2.A real-CI check caught it, it was fixed in `b8ced55f`, and all 8 workflows went green before the PR opened.
- **EPIC-04 DoQ first pass was Blocked.** The ST-18 and ST-20 evidence rows over-stated their results. Both were regraded `Pass_with_deviation` with tracking items (BLG-OPS-182, BLG-GOV-377), and retry 1 was approved with comments.
- **Cross-EPIC commit pre-PR check (v3.82, BLG-GOV-368).** It ran for PR #1918 and found no foreign commits. No cross-EPIC commits reached `main` this cycle.
- **Post-merge sibling sync.** After PR #1917 merged, `main` was merged into EPIC-04 per CLAUDE.md §8. The `execution_state.json`, `backlog.md` and `execution_escalations.md` conflicts were all additive, and no shared-field shape drift was found (2b).
- **Resume/mid-session syncs.** All four PRs were merged by the human. Each merge was picked up by the STEP 4 resume or mid-session sync, and the orphaned post-merge commit check (LL-v6.8-P3-01) found nothing on any of the four branches.
- **Agent-mediated sign-offs.** All four DoQ sign-offs, all PR review comments and the merge-gate QA/PO comments were agent-mediated on the user's explicit direction, labelled as such (OA-6). No PR was merged by the engine.
- **Sprint-close metadata correction (LL-v9.0-P4-02 backstop).** `test_scenarios` was missing three test files named in the QA evidence logs. EPIC-01 gained `tests/test_strategy_version_registry.py` and `tests/test_strategy_version_at_entry.py`; EPIC-03 gained `tests/test_position_lifecycle_states_registry.py`. EPIC-04's missing `merged_utc` (2026-10-07T10:31:10Z) was also backfilled.
- **STEP 5.1 checks.** All 21 stories have `acceptance_verified: true`, `deviations_filed: true` and populated `spec_references`, so no correction was needed. The item count matches: 21 declared in `sprint_backlog.md` ("All 21 slice items are in scope") and 21 in `execution_state.json`. All four EPIC branches have no unpushed or orphaned commits.
- **System Status Report corrections.** None were needed. `docs/System_status_report.md` has no SC-* scenario-count cells or execution-prompt version reference that this sprint made stale. A new Sprint section was added (STEP 5.3A).

## Deviations Filed This Sprint

No new canonical-spec `DEV-*` records were filed. Every `done` story's deviation check finished with `deviations_filed = true`.

Two stories are graded `Pass_with_deviation` in `qa_evidence_EPIC-04.md`. Both are narrowed ACs, disclosed and tracked, and neither is P0 or P1. The severity here matches the DoQ assessment:

| Story | Gap | Priority | Backlog ID |
|-------|-----|----------|------------|
| ST-18 | AC 1 narrowed: the failing live fire diverged staging from the EPIC-04 branch rather than from `main`. The new comparison target has not yet run from `main` against a deliberate divergence | P3 | `BLG-OPS-182` |
| ST-20 | AC 2 partly met: `strategy_rules.md` §13.5's PO-05 roster row still states the IT-06 paper-trading premise. That file is outside this routine's write scope | P3 | `BLG-GOV-377` |

Backlog follow-ups filed this cycle are listed below. These are out-of-scope findings, not spec deviations:

| Backlog ID | Filed by | Reason |
|------------|----------|--------|
| `BLG-BE-143`, `BLG-BE-144`, `BLG-BE-145`, `BLG-QA-214` | PR #1915 DoQ review (EPIC-01) | Grace-period stop recalculation; first-save NULL strategy columns; US NULL `fill_price` crash; grace-warning `min_hold_days` test |
| `BLG-API-07`, `BLG-FE-201`, `BLG-FE-202` | PR #1915 PO review (EPIC-01) | Settings API still accepts fixed strategy fields; Settings helper text; positions with no ATR are never shown |
| `BLG-BE-146`, `BLG-FE-203`, `BLG-QA-215`, `BLG-FE-204` | EPIC-02 pre-PR review | ATR preview on Trade Entry; ATR field units/validation; non-UTC tooltip assertion; £0.00 rounding break-even |
| `BLG-BE-147`, `BLG-BE-148`, `BLG-BE-149` | EPIC-03 pre-PR review | Grace alert day basis; gap-risk holiday/US-date calendar; Risk page `display_status` basis |
| `BLG-GOV-376` | ST-13/ST-14 | `strategy_rules.md` §13.3 text after `weekend_hold` removal |
| `BLG-GOV-377` | ST-20 | `strategy_rules.md` §13.5 PO-05 roster row |
| `BLG-AI-08` | ST-16 | `claude_audit_log` gains `prompt_hash`/`response_length` and failed-call logging |
| `BLG-AI-09` | ST-15 | Daily briefing system prompt lacks an advisory statement |
| `BLG-TECH-22`, `BLG-TECH-23` | ST-17 | Batch patch/minor bumps; assess major upgrades |
| `BLG-FE-200` | ST-19 | Reports and Notifications light-theme colour contrast |
| `BLG-OPS-180`, `BLG-OPS-181`, `BLG-OPS-182` | ST-18 | Missing `STAGING_API_URL` secret; hook deploy never went live; live fire from `main` |
| `BLG-QA-216` | PR #1918 review (ST-19) | Assert the applied theme in every light-theme axe scan |

## Open Escalations

None open at sprint close. All six escalations raised this cycle were resolved before their SLA:

| Escalation | Item | Owning authority | Disposition |
|------------|------|-------------------|-------------|
| `ESC-EXEC-20261006-01` | ST-01/EPIC-01 | Strategy Rules & System Intent Owner | Resolved 2026-10-06T17:30:09Z (SLA 2026-10-09). Ruling (a), by the user directly |
| `ESC-EXEC-20261006-02` | ST-05/EPIC-01 | Strategy Rules & System Intent Owner | Resolved 2026-10-06T17:40:37Z (SLA 2026-10-09). Behaviour-only, by the user directly |
| `ESC-EXEC-20261006-03` | ST-11/EPIC-03 | Strategy Rules & System Intent Owner | Resolved 2026-10-07T07:22:44Z (SLA 2026-10-09). Agent-mediated, user-directed |
| `ESC-EXEC-20261006-04` | ST-13/EPIC-03 (gates ST-14) | Strategy Rules & System Intent Owner | Resolved 2026-10-07T07:22:44Z (SLA 2026-10-09). Agent-mediated, user-directed |
| `ESC-EXEC-20261006-05` | ST-20/EPIC-04 | Strategy Rules & System Intent Owner | Resolved 2026-10-07T07:36:55Z (SLA 2026-10-09). Agent-mediated, user-directed |
| `ESC-EXEC-20261006-06` | ST-15/EPIC-04 | Product Owner | Resolved 2026-10-07T08:16:06Z (SLA 2026-10-07T16:04:53Z). Human Product Owner, in session |

**Backlog cross-reference check (AUD-2026-08-21-006):** none of these escalations carry forward past this close, so no `Source:` backfill is needed.

## Net Outcome vs Sprint Goal

The goal was met. Both live stop paths (on-load and nightly) now read §11 parameters from one source (ST-01, ruling (a)). The silent ATR fallbacks are gone, and ATR and stop-calculation provenance are persisted (DS-25, DS-26, live on staging and production) and exposed on `GET /positions` (ST-02). The Positions stop-loss cell shows the ATR, the active multiplier and the recalculation source (ST-06, BLG-FE-193). Trade Entry shows the system-set stop and risk (ST-07). Exit conditions the system already knows are surfaced in the exit dialog and on the morning briefing (ST-08, ST-09, BLG-FE-198). The lifecycle and gap-risk rulings landed (ST-11–ST-14): the `weekend_hold` trigger was removed, and the earnings window is US-only and runs to the next trading session. The AI-governance, ops and QA hygiene items (ST-15–ST-21) are complete. ST-18 and ST-20 are complete with narrowed ACs, tracked as BLG-OPS-182 and BLG-GOV-377. All 21 items from the sealed `stage4_backlog_slice.md` merged, with no deferrals.

## Verification Readiness Statement

| Field | Status |
|-------|--------|
| All spec references populated in execution_state.json | Yes |
| All P1–P3 deviations filed and backlog references updated | Yes |
| QA evidence logs complete and DoQ sign-off non-blank for all EPICs | Yes |
