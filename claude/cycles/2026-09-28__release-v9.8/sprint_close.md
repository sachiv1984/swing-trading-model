Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-09-30
Cycle: 2026-09-28__release-v9.8

---

# Sprint Close Record — 2026-09-28__release-v9.8

## Sprint Goal

Clear the full v9.8 full-capacity debt slice — 39 stories across 6 EPICs spanning frontend/UX consistency, backend reliability, QA/test coverage, operations/security hardening, spec & API contract debt, and governance/process debt — with no anchor feature, at exactly the top of the confirmed ~24–28 day sprint capacity band.

## Items Done

All 39 in-scope ST items reached `done` and are merged to `main` across 6 EPICs, 6 PRs.

### EPIC-01 — Frontend & UX Debt Clearance (PR #1843, merged 2026-09-29T07:36:47Z)

| ST | Title | Commit SHA | Spec reference(s) |
|----|-------|------------|--------------------|
| ST-01 | Migrate remaining toFixed/toLocaleString call sites to the shared formatting helper | `fb49a284` | `docs/specs/frontend/design_system.md#Number and Currency Formatting`; `docs/design/.../ST-01-formatting-migration-allowlist.md` |
| ST-02 | Drive Screener and Watchlist table body cells from shared column definitions | `050ed6ce` | `docs/design/2026-09-21__release-v9.6/screener-watchlist-csv-export/decision_record.md` |
| ST-03 | Tax Year restated-months notice links to months the Monthly tab shows | `adbc297b` | `docs/design/.../tax-year-restated-notice-year-scoped-link/decision_record.md`; `docs/specs/frontend/pages/reports.md#Monthly Financial Table Tax Year Filter`; `docs/specs/api_contracts/reports_endpoints.md#GET /reports/monthly-pnl` |
| ST-04 | SystemStatus.js categorizeEndpoint() gains a /replay case | `df0c8bcb` | `src/Layout.js#NAV_GROUPS` |
| ST-05 | Responsive-table behaviour spec for Positions, TradeHistory, TradePlans | `6c6fee0d` | `positions.md#Responsive Behavior`; `trade_history.md#Responsive Behavior`; `trade_plan.md#4.2 List Layout` |
| ST-06 | Canonical keyboard-shortcut inventory spec | `05344379` | `docs/specs/frontend/pages/navigation.md#Canonical Inventory` |

### EPIC-02 — Backend Reliability & Financial Correctness (PR #1844, merged 2026-09-29T09:06:01Z)

| ST | Title | Commit SHA | Spec reference(s) |
|----|-------|------------|--------------------|
| ST-07 | Remaining ad hoc timeout=/retry call sites migrated to the shared upstream-call helper | `ac569bb5` | `backend/utils/upstream_call.py`; `tests/test_upstream_call_helper.py` |
| ST-08 | Extend v9.7 float→Decimal fee-rounding audit to tax-year statement calculations | `1ef40035` | `docs/ops/money_arithmetic_audit_tax_year_2026-09-29.md`; `tests/test_tax_year_statement_rounding_audit.py` |

### EPIC-03 — QA & Test Coverage (PR #1845, merged 2026-09-29T11:55:55Z)

| ST | Title | Commit SHA | Spec reference(s) |
|----|-------|------------|--------------------|
| ST-09 | Golden-fixture CI regression for AI prompt templates | `1f9fe404` | `claude/strategy/strategy_rules.md#13.2` |
| ST-10 | End-to-end test confirms backend/main.py's root logger emits JSON in situ | `1f9fe404` | `docs/specs/structured_logging_standards.md#Structured Log Format` |
| ST-11 | Playwright duration-assertion coverage for 9 toast call sites (ST-42 v9.7) | `1f9fe404` | `docs/specs/frontend/design_system.md#Shared UI Components` |
| ST-12 | Regression coverage for motion-timing values (ST-41 v9.7) | `1f9fe404` | `docs/specs/frontend/design_system.md#Motion-vs-contrast guideline` |
| ST-13 | Escaped-defect and follow-on-ratio tracking per cycle | `1f9fe404` | N/A — new artefact (`docs/testing/escaped_defect_and_follow_on_ratio_tracker.md`) is itself the spec |
| ST-14 | DoQ checklist addendum for AI-touching stories | `1835907e` | `claude/system/templates/qa_evidence_template.md` |
| ST-15 | Mutation-testing pilot on sizing calculator and stop ratchet | `5af1aa71` | `strategy_rules.md#4.1`, `#7.2`, `#7.3` |
| ST-16 | Enable Playwright trace/screenshot retain-on-failure | `1f9fe404` | N/A — CI/tooling config change |

### EPIC-04 — Operations & Security Hardening (PR #1846, merged 2026-09-29T13:30:32Z)

| ST | Title | Commit SHA | Spec reference(s) |
|----|-------|------------|--------------------|
| ST-17 | Detect a merge that should have redeployed staging but did not | `78f4a991` | `docs/specs/api_contracts/health_endpoints.md`; `docs/ops/staging_deploy_notes.md` |
| ST-18 | Documented allow-list of pre-approved read-only staging-DB query patterns | `f95a4a89` | `docs/infrastructure/staging_setup.md` |
| ST-19 | Harden the non-registry dependency guard | `5e38e1c8` | `scripts/check_non_registry_dependencies.py` |

### EPIC-05 — Spec & API Contract Debt (PR #1847, merged 2026-09-30T09:01:13Z)

| ST | Title | Commit SHA | Spec reference(s) |
|----|-------|------------|--------------------|
| ST-20 | Idempotency/double-submit documentation for every mutating endpoint | `6e3f0be4` | 13 `docs/specs/api_contracts/*.md` files |
| ST-21 | Error-payload (4xx/5xx) examples for the 10 most-called endpoints | `a7042d44` | 8 `docs/specs/api_contracts/*.md` files; `scripts/check_contract_example_freshness.py` |
| ST-22 | Field-level openapi.yaml authoring pass for 20 thin data payload schemas | `65d6fcc2` | `docs/ops/contract_example_freshness_triage_2026-09-18.md`; `docs/reference/openapi.yaml` |
| ST-23 | POST /trade-plans and DELETE /trade-plans/{id} response schemas | `700ad46c` | `docs/reference/openapi.yaml` |
| ST-24 | trade_plans CREATE TABLE / DS-04 CHECK constraint documentation | `d992b8cf` | `docs/specs/data_model.md` |
| ST-25 | openapi.yaml OperationalHealthResponse.ai_journal oneOf modelling | `5da709af` | `docs/reference/openapi.yaml` |
| ST-26 | screener_results.md column list gains the Earnings column | `3f86b76f` | `docs/specs/frontend/pages/screener_results.md` |
| ST-27 | trade_reflection.md missing-R-multiple glyph (pre-met) | `c9fbdd9d` | `docs/specs/frontend/pages/trade_reflection.md` |
| ST-28 | sprint_velocity_trend_chart.md non-adjacent-reading splice fix | `48a2aa49` | `claude/cycles/sprint_velocity_trend_chart.md` |
| ST-29 | Reconcile IT-06 §13 review with mirror-write paper sync | `ecaa7ce1` | `docs/product/decisions/decisions--2026-05-15__release-v3.5--IT-06-section13-review.md` |

### EPIC-06 — Governance & Process Debt (PR #1848, merged 2026-09-30T12:59:15Z)

| ST | Title | Commit SHA | Spec reference(s) |
|----|-------|------------|--------------------|
| ST-30 | Accessible-name/heading-order rules baked into Base44 prompt template | `f3dd1648` | `docs/specs/frontend/base44_prompt_template_library.md` |
| ST-31 | PVR / Skill-Silo measurement package | `6859c4bf` | `docs/specs/metrics_definitions.md` |
| ST-32 | Delivery-flow metrics — lead time by priority band, ready-pool runway forecast | `ddbb12df` | `docs/specs/metrics_definitions.md`; `claude/system/roadmap_prompt.md` |
| ST-33 | Persist STEP 7.2 role-share tallies as structured history | `04353afe` | `claude/cycles/2026-09-28__release-v9.8/role_share_history.md` (interim location — see Deviations) |
| ST-34 | JSON Schema for .claude_current_state.json | `3b04fb34` | `claude/system/state_schema.json`; `scripts/validate_state_schema.py` |
| ST-35 | Size grep-and-fix-everywhere/verify-against-live-environment story classes a notch higher | `bb6de380` | `claude/system/release_planning_prompt.md` |
| ST-36 | strategy_rules.md §13.5 roster gains PO-05 row | `4431baa7` | `claude/strategy/strategy_rules.md` |
| ST-37 | governance_sync.yml auto-closes phased stories' GitHub issues | `820e2b8e` | `scripts/governance_sync_lib.sh`; `scripts/test_governance_sync_phased_story_logic.sh` |
| ST-38 | Trigger/owner for the 90-day post-ship AI feature usage review | `2ae716ee` | `claude/system/post_ship_closure.md` |
| ST-39 | PO-04 gains its own §13 boundary cross-reference | `4353591a` | `docs/specs/api_contracts/reflection_outcome_correlation_stub.md`; `claude/backlog/backlog.md#BLG-SPEC-156` |

## Items Returned to Backlog

None. All 39 in-scope items reached `done`.

## Items Delegated and Outstanding

None outstanding. One delegation record this cycle, terminal:

- **DEL-20260929-01** (ST-15/EPIC-03, `delegated_qa`) — Status: `Unblocked`. `BLG-QA-198` environmental blocker resolved in-session (Product Owner direction); real mutation score recorded (`calculate_trailing_stop` 100%, `_floor_4dp` 100%, `size_position` 51.6% — gap `BLG-QA-199`).

Six `delegated_decision` items were escalated and resolved in-session this cycle (ST-17, ST-18, ST-29, ST-33, ST-38 by AskUserQuestion role-mediated resolution; ST-31 by direct precedent application per `ESC-EXEC-20260930-03`) — see Open Escalations below; none carried past sprint close.

## QA Evidence Logs Produced

- `claude/cycles/2026-09-28__release-v9.8/qa_evidence_EPIC-01.md` (Director of Quality, 2026-09-29)
- `claude/cycles/2026-09-28__release-v9.8/qa_evidence_EPIC-02.md` (Sprint Execution Engine — autonomous class, 2026-09-29)
- `claude/cycles/2026-09-28__release-v9.8/qa_evidence_EPIC-03.md` (Sprint Execution Engine — agent-mediated, Director of Quality role, 2026-09-29)
- `claude/cycles/2026-09-28__release-v9.8/qa_evidence_EPIC-04.md` (Director of Quality, 2026-09-29)
- `claude/cycles/2026-09-28__release-v9.8/qa_evidence_EPIC-05.md` (Sprint Execution Engine — autonomous class, 2026-09-29)
- `claude/cycles/2026-09-28__release-v9.8/qa_evidence_EPIC-06.md` (Sprint Execution Engine — autonomous class, 2026-09-30)

## Process Notes

Rolled up from `execution_state.json.process_notes` (11 entries spanning 2026-09-28T15:48:41Z–2026-09-29T13:31:16Z):

- PR #1843 (EPIC-01) and PR #1846 (EPIC-04) were both opened with their `qa_evidence_EPIC-xx.md` sign-off `Date:` field still blank, on explicit Product Owner direction (per `BLG-GOV-18`'s own precedent-following path) rather than waiting — both were completed and signed off by a human Director of Quality before merge; STEP 4's merge gate was unaffected by the early open in either case.
- Two resume-sync gaps were found and self-corrected mid-cycle: (1) after PR #1845 (EPIC-03) merged, a prior session's STEP 4 halt had not fully persisted `merge_gate.epics_merged`/`epics_pending`/`process_notes` — corrected at the next `run sprint` invocation with no orphaned commits found; (2) the top-level `completed_items` array was found missing ST-09–ST-16 (EPIC-03's own stories) during the same correction pass — backfilled in the same commit.
- Agent-mediated Director of Quality + Product Owner reviews were posted (explicitly labelled agent-mediated/pending human confirmation per §5.3) on PR #1844 and PR #1846; both PRs still required and received human Product Owner merge acceptance — the agent-mediated reviews did not themselves satisfy the merge gate.
- **This sprint close correction (STEP 5.1 deviations-filed enforcement check):** ST-32/EPIC-06 was found with `deviations_filed: false` and no deviation record in `qa_evidence_EPIC-06.md` (Result: Pass, Deviations: None) — corrected to `true` per the enforcement rule; no deviation filing was required.
- Governance file edit checklist (CLAUDE.md §6) was applied in full for `roadmap_prompt.md` (ST-32), `release_planning_prompt.md` (ST-35), `post_ship_closure.md` (ST-38), and `strategy_rules.md` (ST-36) during this sprint; all four are confirmed synced against `OPERATIONAL_GUIDE.md` §14 and `prompt_change_log.md`.
- All 6 EPIC branches confirmed to have zero unpushed/orphaned commits at sprint close (`git log origin/main..origin/exec/<cycle>/<epic>` empty for all six).

## Deviations Filed This Sprint

None. Every `done` ST item's deviation check (STEP 3.1.A step 10) completed with `deviations_filed = true` and no canonical-spec `DEV-*` record required — no implementation was found to diverge from what a governing spec requires. Several stories filed new **backlog items** (not spec deviations) for follow-up work genuinely out of this sprint's scope; these are tracked via `claude/backlog/backlog.md`, not the spec deviation register:

| Backlog ID | Filed by | Reason |
|------------|----------|--------|
| `BLG-FE-192` | ST-01 | Icon-badge colour finding, not a toFixed call site — out of scope |
| `BLG-QA-197` | ST-03 | Pre-existing stale zero-P&L sign-convention test assertion |
| `BLG-QA-199` | ST-15 | `size_position` US-market/batch-sizing mutation-coverage gap |
| `BLG-OPS-171` | ST-17 | Staging-only evidence that the redeploy-alert fires on a real stale-staging condition |
| `BLG-OPS-172`/`173`/`174`, `BLG-API-06` | ST-20 | Undefined double-submit behaviours found while documenting idempotency |
| `BLG-SPEC-175` | ST-21 | 5 pre-existing error-envelope convention violations, other EPICs/routers |
| `BLG-SPEC-176` | ST-23 | DELETE /trade-plans/{id} envelope shape deviates from `conventions.md` §12 standard |
| `BLG-QA-203` | ST-17/ST-18 | Pre-existing test-order-dependent failure in `test_api_contracts.py` |
| `BLG-SEC-40` | ST-19 (PR review) | 2 residual non-registry-dependency guard gaps |
| `BLG-GOV-353` | ST-33 | Canonical `claude/roadmap/role_share_history.md` placement + §7.2 wiring deferred (write-scope) |
| `BLG-GOV-354` | ST-33 | `.claude_current_state.json.execution_state_path` stale pointer to prior cycle |
| `BLG-GOV-355` | ST-31 | Canonical `product_value_ratio_history.md` effort-weighted-PVR append deferred (write-scope) |
| `BLG-QA-198` | ST-15 (resolved in-session) | `mutmut` 3.x environmental blocker — resolved, see DEL-20260929-01 |

## Open Escalations

None open at sprint close. All 6 escalations raised this cycle were resolved in-session:

| Escalation | Item | Owning authority | Disposition |
|------------|------|-------------------|-------------|
| `ESC-EXEC-20260929-01` | ST-17/EPIC-04 | Infrastructure & Operations Owner | Resolved 2026-09-29 |
| `ESC-EXEC-20260929-02` | ST-18/EPIC-04 | Infrastructure & Operations Owner / Cybersecurity & Trust Lead | Resolved 2026-09-29 |
| `ESC-EXEC-20260929-03` | ST-29/EPIC-05 | Strategy Rules & System Intent Owner | Resolved 2026-09-29 |
| `ESC-EXEC-20260930-01` | ST-38/EPIC-06 | Head of Specs Team; PMO Lead | Resolved 2026-09-30 |
| `ESC-EXEC-20260930-02` | ST-33/EPIC-06 | PMO Lead | Resolved 2026-09-30 |
| `ESC-EXEC-20260930-03` | ST-31/EPIC-06 | PMO Lead | Resolved 2026-09-30 |

**Backlog cross-reference check (AUD-2026-08-21-006):** none of the above carried forward past this cycle's close, so no cross-cycle backlog `Source:` backfill is required.

## Net Outcome vs Sprint Goal

Goal fully met: all 39 items from the sealed `stage4_backlog_slice.md` across all 6 EPICs reached `done` and merged, at full declared capacity (28.00/28.00 days), with no deferrals. Debt cleared spans frontend/UX consistency (EPIC-01), backend financial-correctness reliability (EPIC-02), QA/test coverage (EPIC-03), operations/security hardening (EPIC-04), spec & API contract debt (EPIC-05), and governance/process debt (EPIC-06). Three items closed as `Pass_with_deviation` on a disclosed, non-blocking write-scope deferral (ST-17/`BLG-OPS-171` staging-only evidence; ST-31/`BLG-GOV-355` and ST-33/`BLG-GOV-353` canonical `claude/roadmap/*` placement) — in each case the AC's substance was delivered at an in-scope location and a backlog item filed for the roadmap engine to complete the canonical placement under its own write authority.

## Verification Readiness Statement

| Field | Status |
|-------|--------|
| All spec references populated in execution_state.json | Yes |
| All P1–P3 deviations filed and backlog references updated | Yes |
| QA evidence logs complete and DoQ sign-off non-blank for all EPICs | Yes |
