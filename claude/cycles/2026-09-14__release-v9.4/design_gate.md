**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-09-14
**Cycle:** 2026-09-14__release-v9.4

# Design Gate Record — 2026-09-14__release-v9.4

## Gate Status: PASSED

Completed: 2026-09-14
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

28 of 28 items cleared — 6 Design Required (ST-13, ST-17, ST-22, ST-25, ST-27, ST-28 — artefacts produced and frontend specs updated this run), 2 Design Pre-Approved (ST-14, ST-24 — pure spec debt / cleanup with no UI change, existing conventions govern), 20 Design Not Applicable (pure backend/CI-CD/test-coverage/governance-process/documentation/ops items with no user-visible effect). No blocked items. `sprint_planning_pre_condition` is met.

**Classification note:** the sealed backlog slice flagged 3 items (`BLG-FE-174`/ST-25, `BLG-FEAT-95`/ST-28, `BLG-AI-05`/ST-22) as `design_gate_required: true` at Release Planning. STEP 1 review found 3 additional items warranting Design Required under the §6 motion/timing special rule (BLG-FE-131) or the "new data displayed" criterion, not flagged at Release Planning time: ST-13 (motion-timing target-release assignment), ST-27 (new toast-timing standard authored this cycle), and ST-17 (new Carried Forward Loss field on the tax-year statement). All 6 were resolved within this gate rather than blocked — see Item Classification Summary.

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 | DB-level unique constraint on (ticker, entry_date) | Design Not Applicable | DB migration, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-02 | Nullable trade_plan_id FK migration path | Design Not Applicable | Migration approach documentation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-03 | CI check for inverse OpenAPI drift case | Design Not Applicable | CI/CD gate addition, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-04 | Deprecated-endpoint removal-follow-through scan | Design Not Applicable | Backend/process scan, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-05 | Investigate consolidating 3 scheduled-job runners | Design Not Applicable | Spec-only investigation, no migration, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-06 | Playwright boundary coverage — Arc5ComplianceSection low-volume advisory | Design Not Applicable | Test coverage for already-shipped advisory; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-07 | Backend pytest coverage — GET /analytics/arc5-compliance | Design Not Applicable | Backend test coverage, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-08 | Pinned regression assertion — Settings heading order / aria-labelledby | Design Not Applicable | Regression test pinning existing behaviour, no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-09 | Wire AI cost/latency anomaly check into scheduled job + alert | Design Not Applicable | Ops/scheduling wiring, no UI. §13 pre-check: monitors existing AI-invoking endpoints, does not introduce/extend an AI-provider call — pre-check does not apply. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 | Run real Q3 2026 AI cost-trend query | Design Not Applicable | Ops data query/documentation, no UI. §13 pre-check: analyses cost of existing AI-invoking endpoints — pre-check does not apply. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-11 | Rotate and scope-narrow CI service account token | Design Not Applicable | Infra/credential rotation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-12 | Automated secret-scanning pre-commit hook | Design Not Applicable | CI/tooling addition, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-13 | Framer Motion stagger-delay animations exceed 500ms ceiling | Design Required | Motion/timing-sensitive-interaction special rule (§6, BLG-FE-131) — always Design Required, even for a documentation-only pass. Target release (v9.5) and per-component remediation approach fixed this gate for all 4 known non-compliant components. | `docs/design/2026-09-14__release-v9.4/motion-timing-target-release/decision_record.md` | `design_system.md` v1.15 (bumped this run) | ✅ Cleared | Head of UX & Design |
| ST-14 | Name the GBP-basis FX-conversion display pattern | Design Pre-Approved | Pure spec debt — documents an already-live pattern in `design_system.md`, no UI/behavioural change | N/A | `design_system.md` v1.15 (locked reference at gate time — actual pattern documentation is ST-14's own execution-phase deliverable) | ✅ Cleared | Head of UX & Design |
| ST-15 | Review placement of Appendix D governance metrics | Design Not Applicable | Governance-doc placement decision, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-16 | Reconciliation check — journal-derived P&L vs broker-statement totals | Design Not Applicable | Spec/dependency-mapping only this cycle (blocked on `BLG-QA-122`), no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-17 | Carried-forward-loss field on tax-year P&L statement | Design Required | New data displayed to the user (§6 explicit Design Required criterion) | `docs/design/2026-09-14__release-v9.4/carried-forward-loss-field/decision_record.md` | `reports.md` v0.17 (bumped this run — field added as Design Only / Implementation Pending) | ✅ Cleared | Head of UX & Design |
| ST-18 | Cross-role escalation response-time tracker | Design Not Applicable | Internal governance tracker artefact, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-19 | Idea-intake/roadmap-session compute cost attribution | Design Not Applicable | Governance/process documentation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-20 | Recurring data-density gate trajectory re-estimate cadence | Design Not Applicable | Governance process cadence definition, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-21 | Quarterly automated re-scan of AI-generated copy for boundary-language drift | Design Not Applicable | Process/checklist documentation, no UI. §13 pre-check: re-scans already-shipped AI-surfaced copy for existing-boundary drift, does not introduce/extend an AI-provider call — pre-check does not apply. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-22 | In-app disclosure block — advisory-only AI outputs vs deterministic outputs | Design Required | Observable UI element (new visible badge/disclosure block), per the slice's own design-gate note. §13 pre-check: generalises an already-cleared display-only badge, does not introduce/extend an AI-provider call — pre-check does not apply. | `docs/design/2026-09-14__release-v9.4/ai-advisory-disclosure-badge/decision_record.md` | `design_system.md` v1.15, `dashboard.md` v3.5 (both bumped this run) | ✅ Cleared | Head of UX & Design |
| ST-23 | Generation-time opt-in sampling hook for AI-output boundary-language audits | Design Not Applicable | Backend instrumentation hook, opt-in/default-off, no UI. §13 pre-check: samples/audits existing AI outputs after generation, does not itself call an AI provider — pre-check does not apply. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-24 | Audit Base44 components for orphaned props | Design Pre-Approved | AC explicitly requires no visual/behavioural regression (existing Playwright coverage passes) — cleanup only | N/A | N/A (governed by existing `design_system.md` §Component Prop-Naming Conventions, v1.13 — unchanged) | ✅ Cleared | Head of UX & Design |
| ST-25 | Standardise loading-skeleton pattern (Dashboard/Screener/Journal) | Design Required | 3 divergent screens converging on one canonical pattern — layout/component-consistency change, flagged `design_gate_required: true` at Release Planning | `docs/design/2026-09-14__release-v9.4/loading-skeleton-standardisation/decision_record.md` | `screener_results.md` v1.5, `red_flag_journal.md` v1.2, `dashboard.md` v3.5 (confirmed conformant, no change) — all bumped/confirmed this run | ✅ Cleared | Head of UX & Design |
| ST-26 | Usability pass on Arc 5 compliance advisory banner | Design Not Applicable | Review-only; any recommended change filed as its own item, not fixed inline this cycle | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-27 | Standard interaction-timing rule for toast notifications | Design Required | Reclassified from an initial Pre-Approved read — toast duration is timing-sensitive interaction behaviour under the §6 motion/timing special rule (BLG-FE-131), same treatment as the `2026-09-07__release-v9.2` ST-05 guideline-authoring precedent | `docs/design/2026-09-14__release-v9.4/toast-timing-standard/decision_record.md` | `design_system.md` v1.15 (bumped this run) | ✅ Cleared | Head of UX & Design |
| ST-28 | "Trade plan required before entry" UI soft-nudge | Design Required | New non-blocking UI element on the position-entry flow, flagged `design_gate_required: true` at Release Planning | `docs/design/2026-09-14__release-v9.4/trade-plan-required-nudge/decision_record.md` | `position_form.md` v1.4 (bumped this run) | ✅ Cleared | Head of UX & Design |

## Blocked Items

None.

## Notes

- **§13 pre-check scope:** every item was checked against the mandatory §13 boundary pre-check (STEP 1). No item in this cycle's 28-item scope introduces or extends a call to an AI/LLM provider — the AI-adjacent items (ST-09, ST-10, ST-21, ST-22, ST-23) all monitor, audit, or generalise an already-shipped AI touchpoint rather than adding a new one. Flagged individually in the Rationale column above for traceability.
- **Motion/timing-sensitive interactions (§6, BLG-FE-131):** two items this cycle — ST-13 (target-release assignment for 4 known non-compliant components, `design_system.md`'s existing guideline) and ST-27 (new toast-notification-timing standard, no shipped call-site change this cycle). Both classified Design Required per the special rule regardless of the absence of a shipped-behaviour change, consistent with the `2026-09-07__release-v9.2` ST-05 precedent (a motion guideline authored with no shipped animation change was still Design Required).
- **Items reclassified above the Release Planning flag:** ST-13 and ST-17 were not flagged `design_gate_required` at Release Planning; both independently met a §6 Design Required criterion on STEP 1 review (motion/timing special rule; new-data-displayed criterion respectively) and were resolved within this gate rather than deferred or blocked. ST-27 was initially read as Design Pre-Approved (pure documentation, no UI) and reclassified to Design Required on the same basis as ST-13 before this record was finalised — see its own Rationale cell.
- **Follow-up action outside this gate's write scope:** a single consolidated backlog item to track the actual v9.5 implementation of ST-13's 4 motion-timing fixes should be filed by the Product Owner/PMO Lead — this design gate may not write to backlog documents (§5 write-scope restriction) and did not file one itself. **Filed post-gate:** `BLG-FE-175`, 2026-09-14 (Product Owner/PMO Lead action, via `/backlog-add`, outside this routine's own write scope).
- **Design artefacts produced this run:** `motion-timing-target-release`, `ai-advisory-disclosure-badge`, `loading-skeleton-standardisation`, `carried-forward-loss-field`, `toast-timing-standard`, `trade-plan-required-nudge` — all under `docs/design/2026-09-14__release-v9.4/`.
- **Frontend specs touched:** `design_system.md` v1.13→v1.15 (target-release assignment, AdvisoryBadge, Toast Notification Timing), `dashboard.md` v3.4→v3.5, `reports.md` v0.16→v0.17, `screener_results.md` v1.4→v1.5, `red_flag_journal.md` v1.1→v1.2, `position_form.md` v1.3→v1.4.
- **`reports.md`'s Carried Forward Loss field (ST-17)** ships as "Design Only — Implementation Pending", following the same convention already established in that document (v0.8, §Arc 5 Compliance Summary / §Gross vs Net Comparison) — no backend field exists yet; ST-17 is a frontend/spec story with no corresponding backend AC this cycle.
