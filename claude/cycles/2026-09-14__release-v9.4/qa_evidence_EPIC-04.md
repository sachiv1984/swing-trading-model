Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-15

---

## Consolidation Block

**EPIC:** EPIC-04 — Spec, Documentation & Financial Reporting Debt
**Cycle:** 2026-09-14__release-v9.4
**Sprint goal:** Clear the full v9.4 debt-reduction scope — 28 items across 6 EPICs — at the top of confirmed sprint capacity, including standing up the AI-output boundary-language sampling hook (`BLG-AI-06`/ST-23). See `sprint_goal.md`.
**Test scenarios used:** None — this EPIC is entirely documentation/decision-record work, no application code changed.

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|-----------------|----------------------|--------|------------|
| ST-13 | `docs/specs/frontend/design_system.md#Accessibility (v1.12, v1.14)` | Pre-met finding: the design gate commit (`fffbc231`) already documents delay-based stagger explicitly and fixes a target release (v9.5) + per-component remediation for all 4 listed components, before this story's own execution began. | Both AC bullets pre-met, verified by document re-read. | Pass | None |
| ST-14 | `docs/specs/frontend/design_system.md#Currency-Basis Correctness Pattern for US-Market Positions` | New §Consistency Rules subsection naming two opposite currency-basis failure modes (Trail Stop tile: GBP-converted value mislabelled native; R at Risk: value needing conversion had none), each with its correct fix, keyed by which applies. 1st-pass agent-mediated review Blocked (falsely claimed both precedents converged on one fix) — corrected same-session, 2nd pass Approved. | Both AC bullets met — pattern documented, both precedents cross-referenced accurately. | Pass | None |
| ST-15 | `docs/product/decisions/decisions--2026-09-14__release-v9.4--ST-15-appendix-f-governance-metrics-placement.md`, `docs/specs/metrics_definitions.md#Appendix F` | Placement decision resolved (acting as Product Owner + Metrics Definitions & Analytics Canonical Owner, on explicit user direction, after being correctly escalated per STEP 3.1.D — `ESC-EXEC-20260915-01`): governance-process metrics stay in `metrics_definitions.md` Appendix F, no relocation to `docs/governance/`. Full reasoning recorded; existing v9.2 scope note gains a cross-reference. | AC bullet 1 met — explicit decision recorded. AC bullet 2 not triggered — decision was to keep, not move. | Pass | None |
| ST-16 | `docs/specs/pnl_export_reconciliation.md#8. Journal-Derived P&L vs Broker-Statement Import Reconciliation` | New §8: reconciliation calculation and tolerance (£1.00 or 0.5%, whichever larger) for journal-derived vs. broker-statement P&L totals, with an explicit dependency note against `BLG-QA-122`'s blocked status. Spec/dependency-mapping only per AC — not implementable until that gate clears. | Both AC bullets met. | Pass | None |
| ST-17 | `docs/specs/frontend/pages/reports.md#Tax Year Summary Bar (v0.17)` | Pre-met finding: the design gate commit (`fffbc231`) already added the Carried Forward Loss field, explicitly labelled "Design Only — Implementation Pending" with field mapping locked — satisfies the AC's informational-only-status clause. | Both AC bullets pre-met, verified by document re-read. | Pass | None |

**QA test coverage:**
- Scenarios run: N/A — no application code touched by any story in this EPIC (all 5 are spec/documentation/decision-record work).
- Regression areas checked: N/A for the same reason. `check_local_openapi_contract_completeness.py` and `check_api_performance_baseline_drift.py` re-verified clean on every commit (no new endpoint added by this EPIC).
- Known deviations: None found — all 5 stories' deviation checks completed (`deviations_filed: true`).

---

## Sign-Off Block

**Mixed-Class EPIC** (ST-15 `delegated_decision`; ST-13/ST-14/ST-16/ST-17 `autonomous`) — per `qa_evidence_template.md` "Mixed-Class EPIC Signer Format Note", the BLG-GOV-19 autonomous class is unavailable (Criterion 1: not all stories are `autonomous`) and this uses the agent-mediated/human named-role format instead.

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] N/A — no frontend component in this EPIC making direct URL construction
- Signed off by: Sprint Execution Engine (agent-mediated, Frontend Specifications & UX Documentation Owner role — §5.3)
- Signed off by: Product Owner
- Signed off by: Metrics Definitions & Analytics Canonical Owner
- Date: 2026-09-15
- Comments: ST-14's sign-off (Frontend Specifications & UX Documentation Owner) cleared after 1 Blocked-then-fixed retry — see its `sign_off_record.findings_applied`. ST-15's Product Owner + Metrics Definitions & Analytics Canonical Owner sign-off was completed with those roles acted in on explicit user direction (per `execution_prompt.md` §5), after the item was correctly escalated per STEP 3.1.D rather than resolved without authorisation — see `ESC-EXEC-20260915-01`'s resolution entry in `execution_escalations.md`. ST-13/ST-16/ST-17 required no additional sign-off beyond the deviation check (ST-13/ST-17 pre-met; ST-16 no named sign-off role in its own AC).
