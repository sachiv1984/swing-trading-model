Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-14
Cycle: 2026-09-14__release-v9.4
Release: v9.4

# Release Plan — v9.4

Invocation: `plan release --version "v9.4" --capacity "full capacity"`

---

## Readiness

Preflight (STEP -1) passed in full on this (second) invocation — see `run_manifest.md`. No formal `## v9.4` roadmap section exists; cleared via the STEP -1.2 Option(b)-equivalence rule against the `2026-09-14__scheduled` rebalance's documented "defer again" decision (12th consecutive release cycle relying on this equivalence, extending the v8.5–v9.3 pattern). `post_ship_complete`/`next_cycle_unblocked` both `true` for prior cycle `2026-09-09__release-v9.3`. All required agent roles present. Write test passed.

**First invocation of this session halted at STEP -1.6's SLA-breach carry-forward hard gate** (`AUD-2026-09-14-001`): `ESC-EXEC-20260910-01` (ST-22/EPIC-05, cycle `2026-09-09__release-v9.3`) was `Open` and ~26 hours past its SLA due-by. Resolved by the AI Compliance & Governance Officer (owning-authority match) before this re-invocation: dispositioned `Deferred` (not `Resolved` — genuine live-production sample remains structurally blocked in this environment; not `Accepted Risk` — prohibited for Strategy-boundary trigger-type escalations per `shared_standards.md` §4), with concrete remediation filed as `BLG-AI-06`. See `docs/ops/ai_output_boundary_sample_audit_20260910.md` Addendum (2026-09-14), commit `8cad2428`. `open_escalations` is now empty; gate clears.

Advisory checks (§1.1–§1.4, full detail in `run_manifest.md`):
- Backlog Age Advisory: no 2+ cycle carried spec/documentation debt item in scope — all 28 selected items enter `stage4_backlog_slice.md` for the first time.
- Provisional-Target Advisory: no item carries `Provisional-Target: v9.4` (no horizon signal pre-existed); all 28 selected items carry `TBD`/`Unscheduled`.
- Design-Gate Language Scan: 3 selected items (`BLG-FE-174`, `BLG-FEAT-95`, `BLG-AI-05`) carry an observable UI acceptance criterion → **`design_gate_required: true`** — the first release with design-gate-triggering scope since v9.0.
- Gate-Condition Proximity Scan: Arc 4/Arc 5 data-density metrics unchanged since the last rebalance (0/11 linked trade plans; SI-02/PO-02/PO-04 gates NOT MET). No item in this cycle's scope touches that gate family. No ungated P0/P1 item exists this cycle — ready pool is 8 P2 items (7 selected), 1 P4 item (not selected), remainder P3.

```yaml
artifacts.stage1_readiness: pass
```

---

## Scope

Scope document: `docs/product/scope/scope--2026-09-14__release-v9.4-full-capacity-debt-clearance-ii.md`

| S2-ID | Scope theme | Items | Effort (days) |
|-------|-------------|-------|----------------|
| S2-01 | Backend & Platform Engineering Debt | 5 | 8.50 |
| S2-02 | QA & Test Coverage Debt | 3 | 0.45 |
| S2-03 | Operations & Security Debt | 4 | 1.65 |
| S2-04 | Spec, Documentation & Financial Reporting Debt | 5 | 5.45 |
| S2-05 | Governance Process & AI Compliance Debt | 6 | 7.00 |
| S2-06 | Frontend, UX & Product Debt | 5 | 4.50 |
| **Total** | | **28** | **27.55** |

**Items explicitly deferred (not entering v9.4 scope):**
- `BLG-GOV-178` — literal AC already shipped at ST-22/v9.3; retained un-archived only for escalation-tracking purposes (`ESC-EXEC-20260910-01`, now `Deferred`); its concrete remediation (`BLG-AI-06`) is selected into scope on its own merits instead.
- `BLG-FEAT-73`, `BLG-FEAT-74`, `BLG-FEAT-76`, `BLG-SPEC-56`, `BLG-SPEC-57`, `BLG-QA-59` — data-quality-flagged (embedded gate-like free text in `Provisional-Target`, no formal `Gate` field); treated as not-ready, consistent with v9.3's treatment of 3 of these same 6 items.
- 130 formally gated/conditional items — no clearance evidence this cycle (unchanged data-density/AI-adoption/§13-review gates).
- 46 further ungated P3/P4 items, ~37.50 estimated days, left unselected purely on capacity grounds — see `run_manifest.md` for the full ready-pool accounting; available for a future release cycle.

No scope reprioritisation performed beyond selection from the ungated pool — this routine does not alter strategy boundaries.

```yaml
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

**Format note (IMP-08):** full acceptance criteria live in `stage4_backlog_slice.md`; this section is the compact sequencing/risk view.

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-01 | Backend Engineering Patterns Owner; Data Model & Domain Schema Owner; API Contracts & Documentation Owner; Head of Engineering | RISK-01 | No UI ACs; independent of other EPICs |
| EPIC-02 | S2-02 | QA Testing Owner; Director of Quality | RISK-02 | No UI ACs; independent of other EPICs |
| EPIC-03 | S2-03 | Infrastructure & Operations Owner; FinOps & Resource Architect; Cybersecurity & Trust Lead | RISK-03 | No UI ACs; independent of other EPICs |
| EPIC-04 | S2-04 | Frontend Specifications & UX Documentation Owner; Metrics Definitions & Analytics Canonical Owner; Financial Reporting & Records Owner | RISK-04 | No UI ACs; independent of other EPICs |
| EPIC-05 | S2-05 | PMO Lead; AI Compliance & Governance Officer; FinOps & Resource Architect; Director of HR | RISK-05 | `BLG-AI-05` carries an observable UI AC (disclosure badge) — sequence after `BLG-AI-06` if both touch the same AI-response call sites, to avoid the badge component and the sampling hook colliding on the same shared wrapper |
| EPIC-06 | S2-06 | Base44 Frontend Prompt Owner; Head of UX & Design; Product Owner | RISK-06 | **Design-gate-triggering** (`BLG-FE-174`, `BLG-FEAT-95`) — `run design-gate --cycle 2026-09-14__release-v9.4` must pass before `plan sprint` can seal (`sprint_planning_pre_condition`) |

**Design-gate-triggering EPICs this cycle:** EPIC-06 (primary — 2 items) and, secondarily, `BLG-AI-05` within EPIC-05 (1 item; its own AC needs a Playwright/staging method added before execution, see `run_manifest.md`). First release since v9.0 with observable-UI scope.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | `BLG-BE-115`'s unique-constraint migration could fail to apply if duplicate `(ticker, entry_date)` rows already exist in production; this execution environment has no live DB access to pre-check | Medium | Story author writes the pre-check as part of the migration script itself (fail loudly with a clear report of offending rows rather than a raw constraint-violation error); if a live pre-check cannot be run in this environment, the migration script is delivered and verified against synthetic/staging-shaped data, and the live application step is explicitly disclosed as pending a DB-accessible environment rather than claimed complete | null |
| RISK-02 | EPIC-02 | `BLG-QA-163` targets `get_arc5_trade_plan_adherence_rate`, whose signature may have shifted since the v9.2 PR that surfaced this gap (2026-09-07) | Low | Story author confirms current function name/signature in `backend/services/` before writing tests; if renamed, update the story's own AC text to match rather than silently testing a stale name | null |
| RISK-03 | EPIC-03 | `BLG-OPS-151`/`BLG-OPS-152` both require production DB access (`DATABASE_URL`) to fully close their "runs against real data" sub-criteria — the same constraint disclosed at ST-13/ST-21/ST-22 (v9.3) and ST-56 (v9.2), unresolved again this cycle (re-confirmed unset this session) | Medium | Implement/wire the mechanism fully regardless (the code-level deliverable does not require live DB access); explicitly disclose — not fabricate — if the final "run against real production data" sub-criterion cannot execute in this environment, following the same honest-disclosure precedent as `ESC-EXEC-20260910-01`/`ST-22` rather than claiming completion | null |
| RISK-04 | EPIC-04 | `BLG-FR-02` depends on `BLG-QA-122` (blocked — no broker-statement import mechanism exists); its own AC already scopes this cycle's work to spec/dependency-mapping only | Low | Story explicitly states "not blocked on implementation this cycle" in its own AC — no mitigation action needed beyond following that scoping as written | null |
| RISK-05 | EPIC-05 | `BLG-AI-06` (opt-in generation-time sampling hook) touches multiple AI-response call sites (journal-summary, daily-briefing, chat, debrief, trade-plan generation) at M (~1–2d) effort — risk of under-scoping if no single shared chokepoint exists across all 5 | Medium | Scope to the shared AI-response helper/wrapper if one exists (touch one chokepoint, not 5 call sites individually) to stay within estimate; if no shared chokepoint exists, deliver a phased implementation (highest-value call sites first) and file follow-on `BLG-AI-*` items for remaining call sites rather than overrunning the sprint | null |
| RISK-06 | EPIC-06 | Design-gate-triggering EPIC — `run design-gate` has not yet been run for this cycle; `sprint_planning_pre_condition` blocks `plan sprint` from sealing until it passes | Medium | Flagged explicitly in `cycle_summary.md`; Product Owner/Head of Specs Team must run `run design-gate --cycle 2026-09-14__release-v9.4` before invoking `plan sprint` | null |

```yaml
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

All 28 ST items in `stage4_backlog_slice.md` carry a `**Source:** BLG-xxx` reference resolving to an existing, currently-open backlog entry in `claude/backlog/backlog.md` (confirmed via the same script-driven extraction used to build the slice — no fabricated or stale IDs). All 6 EPIC IDs are internally consistent between `release_plan.md` and `stage4_backlog_slice.md`. No `[ESTIMATE REQUIRED]` or `[AC REQUIRED]` placeholders present in any of the 28 stories.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Capacity Check

**Effort Band Lookup (ST-14):** `scored_initiatives.md` has 0 active initiatives — no pre-assigned Effort Bands. All 6 EPICs sized via inline STEP 4 estimate from each item's own `**Effort:**` field in `claude/backlog/backlog.md`, using the canonical Effort Band → Days table in `workforce_capacity.md` (XS=0.15d, S=0.5d, M=2.5d, L=3.5d).

| EPIC | Items | Subtotal (days) |
|------|-------|-------------------|
| EPIC-01 — Backend & Platform Engineering Debt | 5 | 8.50 |
| EPIC-02 — QA & Test Coverage Debt | 3 | 0.45 |
| EPIC-03 — Operations & Security Debt | 4 | 1.65 |
| EPIC-04 — Spec, Documentation & Financial Reporting Debt | 5 | 5.45 |
| EPIC-05 — Governance Process & AI Compliance Debt | 6 | 7.00 |
| EPIC-06 — Frontend, UX & Product Debt | 5 | 4.50 |
| **Total** | **28** | **27.55** |

27.55 days vs the confirmed ~24–28 day band (`claude/roadmap/workforce_capacity.md`, unchanged since 2026-07-17) — within band, at its upper bound (98% of the 28-day ceiling), matching the explicit "use full capacity" instruction; ties v9.2's exact figure. **Capacity check outcome: pass, no WARN.**

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity / 5.7 Decision Record Integrity

**5.5 Cross-Stage Integrity:** All 6 S2 IDs (S2-01..S2-06) map 1:1 to EPIC-01..EPIC-06. All 6 EPIC IDs in `stage4_backlog_slice.md` match the Execution Plan table. All 6 RISK IDs in the EPIC table appear in the Risk Register Summary. No orphaned references found.

**5.7 Decision Record Integrity:** Skipped — `artifacts.escalations` is not `present` for this cycle's own run (no new escalation raised during this release-planning session; the one escalation touched, `ESC-EXEC-20260910-01`, was resolved in a prior session turn, outside this cycle's own escalation log). `decisions--2026-09-14__release-v9.4.md` is still produced per STEP 3's standing requirement (scope/sequencing decisions, not escalation-driven).

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```

---

## Change Log

| Date | Version | Change | Authority |
|------|---------|--------|-----------|
| 2026-09-14 | 1.0 | Initial publication — v9.4 release plan, 28 items / 6 EPICs / 27.55 days, full capacity; first design-gate-triggering release since v9.0 | Head of Specs Team (Release Planning Engine) |
