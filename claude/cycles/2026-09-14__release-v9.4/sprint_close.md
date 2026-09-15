**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-09-15
**Cycle:** 2026-09-14__release-v9.4
**Release:** v9.4

---

# Sprint Close — v9.4 Full-Capacity Debt Clearance II

## Sprint Goal

Clear the full v9.4 debt-reduction scope — 28 items across 6 EPICs — at the top of confirmed sprint capacity, including standing up the AI-output boundary-language sampling hook (`BLG-AI-06`/ST-23). See `sprint_goal.md`.

**Outcome: Goal met in full.** All 28/28 scoped items delivered and merged to `main` across 6 EPICs. The sampling hook (ST-23) shipped with all 5 real AI-generation call sites wired, opt-in/default-off/rate-bounded as required; the 2 ACs explicitly out of session scope (genuine ≥10-output live sample, closing `ESC-EXEC-20260910-01`) were disclosed as staging-only at sprint planning and remain correctly disclosed, not fabricated.

## Items Done

### EPIC-01 — Backend & Platform Engineering Debt (PR #1662)

| ST | Title | Commit SHA | Spec Reference |
|----|-------|------------|-----------------|
| ST-01 | DB-level unique constraint on (ticker, entry_date) for open positions | `13597aed` | `data_model.md#DS-17` |
| ST-02 | Nullable trade_plan_id FK migration path | `3242cd88` | `data_model.md#Migration approach` |
| ST-03 | CI check for the inverse OpenAPI drift case | `6859b921` | `tests/test_openapi_drift_inverse_case.py`; `.github/workflows/openapi-drift.yml` |
| ST-04 | Deprecated-endpoint removal-follow-through scan | `b612e453` | `deprecated_endpoint_sunset_tracker.md` |
| ST-05 | Investigate consolidating the 3 scheduled-job runners into one orchestrator | `682cdcd5` | `docs/ops/scheduled_job_runner_consolidation_investigation.md` |

### EPIC-02 — QA & Test Coverage Debt (PR #1664)

| ST | Title | Commit SHA | Spec Reference |
|----|-------|------------|-----------------|
| ST-06 | Boundary-condition Playwright coverage for Arc5ComplianceSection low-trade-volume advisory | `b62a6f9e` | `tests/e2e/arc5-compliance-section.spec.js` |
| ST-07 | Backend pytest coverage for GET /analytics/arc5-compliance total_closed_trades field | `e6845cbe` | `tests/test_arc5_total_closed_trades_null_vs_zero.py` |
| ST-08 | Pinned regression assertion — Settings heading-order fix / TradePlan aria-labelledby swap | `63a24c1a` | `tests/e2e/settings-heading-order-and-aria-labelledby-regression.spec.js` |

### EPIC-03 — Operations & Security Debt (PR #1665)

| ST | Title | Commit SHA | Spec Reference |
|----|-------|------------|-----------------|
| ST-09 | Wire the AI endpoint cost/latency anomaly check into a scheduled job and alert channel | `952ac326` | `ai_endpoints.md#POST /ai/check-endpoint-anomalies` |
| ST-10 | Run real Q3 2026 AI cost-trend query against production data | `409fbb34` | `docs/ops/ai_feature_cost_trend_2026_q3.md#3` |
| ST-11 | Rotate and scope-narrow the CI service account token | `f74bd7a5` | `docs/security/ci_service_account_token_scope_audit_2026-09-14.md` |
| ST-12 | Automated secret-scanning pre-commit hook | `38bedacf` | `.githooks/README.md#Secrets-scanning false-positive override procedure` |

### EPIC-04 — Spec, Documentation & Financial Reporting Debt (PR #1668)

| ST | Title | Commit SHA | Spec Reference |
|----|-------|------------|-----------------|
| ST-13 | Framer Motion stagger-delay entrance animations — 500ms motion-vs-contrast ceiling | `fffbc231` | `design_system.md#Accessibility` (v1.12, v1.14) |
| ST-14 | Name the GBP-basis FX-conversion display pattern in design_system.md | `cdb70434` | `design_system.md#Currency-Basis Correctness Pattern` |
| ST-15 | Review placement of Appendix D governance metrics in metrics_definitions.md | `ec38517a` | `decisions--...--ST-15-appendix-f-governance-metrics-placement.md`; `metrics_definitions.md#Appendix F` |
| ST-16 | Reconciliation check: journal-derived P&L vs broker-statement import totals | `56cdeca0` | `pnl_export_reconciliation.md#8` |
| ST-17 | Carried-forward-loss field on the tax-year P&L statement | `fffbc231` | `reports.md#Tax Year Summary Bar` (v0.17) |

### EPIC-05 — Governance Process & AI Compliance Debt (PR #1666)

| ST | Title | Commit SHA | Spec Reference |
|----|-------|------------|-----------------|
| ST-18 | Cross-role escalation response-time tracker | `e066a5a5` | `docs/governance/escalation_response_time_tracker.md` |
| ST-19 | Idea-intake / roadmap-session compute cost attribution | `1a75850a` | `docs/ops/governance_session_cost_attribution.md` |
| ST-20 | Recurring data-density gate trajectory re-estimate cadence | `cb04c6bc` | `arc4_data_density_trajectory_v4.6.md#10` |
| ST-21 | Quarterly automated re-scan of AI-generated copy for boundary-language drift | `89875a04` | `docs/ops/quarterly_ai_copy_boundary_scan_cadence.md` |
| ST-22 | In-app disclosure block: advisory-only AI outputs vs deterministic outputs | `01425ff7` | `tests/e2e/epic02-v62-ai-briefing-chat.spec.js#SC-AB-05` |
| ST-23 | Generation-time opt-in sampling hook for AI-output boundary-language audits | `4d02f9ed` | `data_model.md#DS-18`; `ai_endpoints.md#AI Output Boundary-Language Sampling Hook` |

### EPIC-06 — Frontend, UX & Product Debt (PR #1667)

| ST | Title | Commit SHA | Spec Reference |
|----|-------|------------|-----------------|
| ST-24 | Audit Base44 components for orphaned props | `c1981417` | `decisions--...--ST-24-base44-orphaned-props-audit.md` |
| ST-25 | Standardise the loading-skeleton pattern across screens | `216210c1` | `screener_results.md#10. Progressive Loading Pattern` |
| ST-26 | Usability pass on the Arc 5 compliance advisory banner | `40257339` | `decisions--...--ST-26-arc5-advisory-banner-usability-review.md` |
| ST-27 | Standard interaction-timing rule for toast notifications | `b8ec4510` | `design_system.md#Toast Notification Timing` (v1.15/v1.17) |
| ST-28 | Minimal "trade plan required before entry" UI soft-nudge | `fac91a28` | `position_form.md#Trade Plan Linkage Advisory` |

## Items Returned to Backlog

None — all 28 items delivered within the sprint.

## Items Delegated and Outstanding

All delegation records reached terminal state before sprint close — none outstanding.

| Delegation ID | ST Item | Role | Outcome |
|----------------|---------|------|---------|
| DEL-20260914-01 | ST-01 (EPIC-01) | Data Model & Domain Schema Owner (agent-mediated) | Unblocked — sign-off cleared after 1 Blocked retry |
| DEL-20260914-02 | ST-11 (EPIC-03) | Cybersecurity & Trust Lead (agent-mediated) + human (fine-grained PAT rotation) | Unblocked — sign-off cleared |
| DEL-20260914-03 | ST-23 (EPIC-05) | Head of Engineering | Unblocked (partial) — AC 1/2/3/5 met and sign-off cleared; AC 4/6 disclosed staging-only, not met, per sprint-planning-time scoping |

## QA Evidence Logs Produced

- `qa_evidence_EPIC-01.md` — Director of Quality equivalent sign-off (Data Model & Domain Schema Owner, agent-mediated), 2026-09-14
- `qa_evidence_EPIC-02.md` — autonomous class, 2026-09-14
- `qa_evidence_EPIC-03.md` — mixed-class, agent-mediated named-role sign-offs, 2026-09-14
- `qa_evidence_EPIC-04.md` — mixed-class, agent-mediated + human (Product Owner/Metrics Definitions Owner for ST-15), 2026-09-15
- `qa_evidence_EPIC-05.md` — mixed-class, agent-mediated named-role sign-offs, 2026-09-15
- `qa_evidence_EPIC-06.md` — mixed-class (autonomous stories, 0 sign-off-requiring roles named), 2026-09-15

## Process Notes

- **2026-09-15T07:42:30Z (EPIC-05):** A commit-msg hook rejection (missing ST tag on a QA-evidence-consolidation commit) left a failed attempt on top of already-pushed commit `7b4866e7`. Recovery correctly reached for a fresh commit rather than `git commit --amend` on the pushed commit (per LL-v9.1-P3-02/LL-v9.2-P3-02) — caught before push via `git log` comparison, recovered cleanly with `git reset --soft 7b4866e7` + a new commit (`b8cc78b4`), no force-push, no origin history rewrite.
- **CI failure caught and fixed pre-merge (EPIC-05, ST-23):** `test_ai_output_sampling_service.py`'s original module-level `sys.modules.pop("database", None); import database` permanently overwrote the shared stub for the rest of the pytest session, leaking a real Postgres connection attempt into `test_alerts_service.py` (alphabetical collection-order dependency). Root-caused and fixed via the isolated-copy (`importlib.util.spec_from_file_location`) + scoped `patch.dict` pattern already established by `test_position_audit_log.py`. Same latent pattern found and filed separately for `test_trade_plan_audit_log.py` (`BLG-QA-178`).
- **CI failure caught and fixed pre-merge (EPIC-06, ST-28):** Shard 4/8 failed on `position-sizing-concentration.spec.js::V-SIZE-02` post-push — the new Trade Plan Linkage Advisory banner's `AlertTriangle` icon collided with `PositionSizingWidget.js`'s pre-existing concentration-warning icon, breaking that unrelated test's icon-count assertion. Fixed by swapping to the `Info` icon; documented as a live-CI finding in `position_form.md`'s changelog.
- **Merge-gate human-review handoff (EPIC-05, EPIC-06):** Both PRs reached 100% green CI and a correctly-labeled agent-mediated two-agent advisory review (Director of Quality + Product Owner personas) before the actual human merge decision — consistent with the always-human merge gate (CLAUDE.md §2 / execution_prompt.md §5.3). Neither PR was merged by the engine.
- **Post-merge state-sync required for both EPIC-05 and EPIC-06:** Both PRs were merged directly by the human via GitHub rather than through the engine's own STEP 4 flow, so the state-sync steps (EPIC status/pr_status → `merged`, `merge_gate` update) had to be applied retroactively on `main` in a follow-up session turn each time, per the "mid-session re-sync on every PR merged report" rule (AUD-2026-08-21-010). No orphaned post-merge commits were found on either branch.

## Deviations Filed This Sprint

None — all 28 stories' deviation checks completed (`deviations_filed: true` across every EPIC); zero spec-level `DEV-*` records required. Process-debt / disclosed-gap backlog items were filed where relevant instead (not AC-shortfall deviations): `BLG-SPEC-D18`, `BLG-OPS-160`, `BLG-OPS-161`, `BLG-QA-178`, `BLG-FE-176`, `BLG-UX-05`.

## Open Escalations

None. `ESC-EXEC-20260915-01` (ST-15/EPIC-04 — Appendix D/F governance metrics placement) was raised and resolved within this sprint on explicit user direction acting as Product Owner + Metrics Definitions & Analytics Canonical Owner; disposition: Resolved, decision recorded at `docs/product/decisions/decisions--2026-09-14__release-v9.4--ST-15-appendix-f-governance-metrics-placement.md`.

`ESC-EXEC-20260910-01` (from prior cycle `2026-09-09__release-v9.3`, ST-22/EPIC-05 boundary-language sample) remains `Deferred` — not part of this cycle's open escalations, correctly not closed by ST-23 per its own disclosed staging-only ACs (see EPIC-05 QA evidence).

## Net Outcome vs Sprint Goal

**Goal fully met.** 28/28 scoped items delivered, merged to `main` across 6 EPICs, 0 items returned to backlog, 0 open escalations, 0 spec-level deviations. The sprint goal's named centrepiece (BLG-AI-06/ST-23 sampling hook) shipped functionally complete and unit-tested; its two staging-only ACs remain correctly disclosed rather than fabricated, consistent with sprint-planning-time scoping.

## Verification Readiness Statement

| Field | Status |
|-------|--------|
| All spec references populated in execution_state.json | Yes |
| All P1–P3 deviations filed and backlog references updated | Yes |
| QA evidence logs complete and DoQ sign-off non-blank for all EPICs | Yes |

## System Status Report Corrections

Reviewed `docs/System_status_report.md` for stale SC-* scenario-count cells and the `execution_prompt.md` version reference (STEP 5.1.B / BLG-GOV-15 advisory). No single stale summary-count cell was found — the report structures scenario references per-sprint-section (dated to when each was true), not as a running total that this sprint's additions could make stale. `execution_prompt.md` was not modified this sprint (remains v3.75); no version-reference correction needed. This sprint's new section (added below at §5.3A) carries its own accurate scenario references.
