Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v8.9
Cycle: 2026-08-17__release-v8.9
Last Updated: 2026-08-17

# Release Plan — v8.9

## Readiness

Preflight PASS (see `run_manifest.md` STEP -1). Release cleared for planning via STEP -1.2 Option (b) equivalence — no formal `## v8.9` roadmap section exists; `2026-08-11__scheduled` rebalance recorded a documented Option (b) defer decision (4th consecutive firing), which this routine treats as authorization to draw scope directly from the ungated backlog pool for `plan release`, consistent with the precedent already relied on for v8.5–v8.8.

**Anchor scope:** Two brand-new P0 (Critical) live risk-management correctness bugs were filed today (2026-08-17), both explicitly `Provisional-Target: TBD (next release)` — named for v8.9 — found during a real production investigation: `BLG-BE-102` (nightly trailing-stop ratchet skips the breakeven floor for profitable positions) and `BLG-BE-103` (stop values returned/rendered in the wrong currency basis, already caused user confusion on a live position).

**Capacity assumption (Product Owner decision, 2026-08-17):** Presented with the 2-item P0 anchor scope alone (~2.25 days) against the confirmed ~24–28 working-day capacity band, the Product Owner chose to widen scope to fill capacity (option (b) of 3 presented: tight / widen / moderate). Confirmed capacity band: ~24–28 working-day-equivalent units (`claude/roadmap/workforce_capacity.md`, unchanged since 2026-07-17).

Advisories (full detail in `run_manifest.md`):
- Backlog Age Advisory: no additional spec/documentation debt item found aged 2+ cycles without a story assignment beyond items already selected.
- Provisional-Target Advisory: 2 items carry `Provisional-Target: TBD (next release)` naming v8.9 (`BLG-BE-102`, `BLG-BE-103`); 20 items have no v8.9-specific signal, drawn from the ungated P2/P3 pool.
- Design-Gate Language Scan: no explicit design-pending language found; observable-UI-AC classification (STEP 4.1, independent check) applies to several EPIC-02 items and `BLG-BE-103`.
- Gate-Detection Procedure (`scripts/scan_backlog_gate_conditions.py`): 268 items scanned, 170 gated + 6 data-quality warnings. All 22 selected items confirmed ungated. `BLG-GOV-105` was shortlisted then dropped — already ✅ CLOSED (confirmed duplicate), pending archival, not live scope. `BLG-FEAT-92` was shortlisted then dropped — its own item text names an unresolved scope-overlap dependency on gated `BLG-FEAT-30` requiring PO/Head of Specs Team reconciliation before it may enter sprint planning; not resolvable unilaterally by this routine.
- Perennial-Return Check / Within-Sprint Date Gate: not applicable — no gate-conditional items in scope.

```yaml
artifacts.stage1_readiness: pass
```

---

## Scope

Scope document: `docs/product/scope/scope--2026-08-17__release-v8.9.md`

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Live risk-management correctness (trailing-stop breakeven-floor ratchet fix, stop-field currency-basis display fix, supporting metrics spec entry) |
| S2-02 | EPIC-02 | Trade sizing & post-trade intelligence (correlation/sector-concentration-aware sizing, pre-commit what-if sizing simulator, automated AI post-trade debrief, in-app backtesting engine) |
| S2-03 | EPIC-03 | Backend reliability & performance (trade-plan tags latency investigation, duration-logging verification, audit-trail transaction wrapping, dead-code confirmation) |
| S2-04 | EPIC-04 | Test coverage & QA hardening (job-registration wiring tests, setup_type data-quality decision, service-layer unit test gaps, changelog Playwright coverage) |
| S2-05 | EPIC-05 | Operations & spec currency (local dev venv version-pin enforcement, idea window-summary archival, health-endpoint job-list spec currency) |
| S2-06 | EPIC-06 | Governance process debt closure (state-field ownership registry fix, execution_state.json timestamp drift, Displacement Debt Register wiring, stale roadmap-annotation-marker pruning rule) |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| `BLG-FEAT-92` | Own item text names an unresolved scope-overlap dependency on gated `BLG-FEAT-30` requiring explicit PO/Head of Specs Team reconciliation before entering sprint planning — not resolvable unilaterally by this routine. | Next cycle, after reconciliation |
| `BLG-GOV-105` | Already ✅ CLOSED (confirmed duplicate, 2026-07-12); stale entry pending archival, not live scope. | `groom backlog` archival |

Remaining ungated P3 pool not selected (60 of the 82 ungated-and-not-closed P3 items) remain available in `backlog.md` for future release cycles; none were displaced from a committed scope.

```yaml
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

**Format note:** full acceptance criteria live in `stage4_backlog_slice.md`. This table is sequencing/ownership/risk only.

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-01 | Backend Engineering Patterns Owner; Frontend Specifications & UX Documentation Owner | RISK-01 | Leads capacity allocation — closes 2 live P0 risk-management-correctness gaps. ST-02 sequenced after ST-01 (same position-data path). |
| EPIC-02 | S2-02 | Head of Engineering; Backend Engineering Patterns Owner; Strategy Rules & System Intent Owner | RISK-02 | Design gate required (see STEP 4.1) — largest subtotal, execution-heavy product scope |
| EPIC-03 | S2-03 | Backend Engineering Patterns Owner; Head of Engineering | RISK-03 | None |
| EPIC-04 | S2-04 | QA & Testing Owner; Director of Quality; Product Owner | RISK-04 | None |
| EPIC-05 | S2-05 | Infrastructure & Operations Owner; API Contracts & Documentation Owner; Head of Specs Team | RISK-05 | None |
| EPIC-06 | S2-06 | Head of Specs Team | RISK-06 | None |

**EPIC-01:** Leads the table — both `BLG-BE-102` and `BLG-BE-103` are live P0 risk-management-correctness bugs found during a real production investigation (a live WDC position's stop-loss discrepancy), each `Provisional-Target: TBD (next release)`. `BLG-SPEC-85` (the `trailing_stop_action_rate` metrics-tolerance spec entry) is grouped in as directly related supporting documentation for the corrected behaviour, not because it shares the same bug.

**EPIC-02:** All 4 items were filed in the same 2026-08-17 Product Owner feature-vision session and are P2/execution-heavy (3 Product Feature, 1 Backend/Risk) — largest single subtotal this cycle, satisfying the Skill-Silo mitigation rotation guidance (§3) by weighting this release toward build-and-ship scope rather than governance/debt-heavy scope. `BLG-FEAT-92` (5th item from the same session) explicitly excluded — see Scope § Items explicitly deferred.

**EPIC-04:** `BLG-QA-150` requires a Product Owner + Frontend Specifications & UX Documentation Owner decision on treatment (required field vs. default value vs. accept-as-is) before implementation — scoped as "decide and implement/document" per its own acceptance criteria, not a pure implementation item.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | `BLG-BE-102`'s fix touches the nightly-scheduled trailing-stop path directly enforced on live open positions — an incorrect fix could itself misprice a live stop | High | Add the regression test specified in the item's own AC *before* changing production behaviour; backfill/recompute existing open positions' `current_stop` only after the calculation-path fix is verified correct | null |
| RISK-02 | EPIC-02 | `BLG-FEAT-89` (in-app backtesting engine) is the largest single item (L, ~3–5d) and touches §13-governed `strategy_rules.md` change-review tooling; feasibility of reusing `production_strategy.py`'s simulation logic is explicitly unscoped pending Head of Engineering review | Medium | Head of Engineering to confirm reuse feasibility early in the EPIC; if reuse proves infeasible, scope may need to narrow to a smaller candidate-comparison surface rather than a full historical simulation engine | null |
| RISK-03 | EPIC-03 | None material — all 4 items are investigation/hardening/dead-code-confirmation scoped, no live-position-affecting behaviour change | Low | Standard review | null |
| RISK-04 | EPIC-04 | `BLG-QA-150` requires an explicit PO/Frontend Specs decision before implementation, not pure execution — could stall mid-sprint if the decision isn't made promptly | Low | Sequence the decision early in the EPIC, ahead of any implementation work depending on it | null |
| RISK-05 | EPIC-05 | None material — all 3 items are dev-environment/documentation/housekeeping scoped, no production runtime change | Low | Standard review | null |
| RISK-06 | EPIC-06 | `BLG-GOV-264` requires editing `roadmap_prompt.md` STEP 8 — must follow the full CLAUDE.md §6 Governance File Edit Checklist (version bump, `OPERATIONAL_GUIDE.md` §14, `prompt_change_log.md` entry) in the same commit, per the item's own scope note | Low | Apply the standard checklist; do not land the register file without the paired prompt edit or vice versa | null |

```yaml
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

All 22 in-scope items map to the existing data model or introduce straightforward, precedented schema extensions. `BLG-BE-104` (sector-concentration sizing) reads existing ticker-metadata/portfolio-composition fields — no new entity. `BLG-FEAT-90` (AI post-trade debrief) writes to the existing `claude_audit_log` table per standing AI-governance convention — no new table. `BLG-FEAT-89` (backtesting engine) persists backtest runs — the item's own AC requires "enough detail to audit later" but does not mandate a specific new table; if a new table proves necessary at implementation time it follows the existing migration convention with no structural ambiguity. `BLG-FEAT-91` (what-if sizing preview) is explicitly scoped as a non-committing, no-DB-write preview endpoint reusing the existing `sizing_service` calculation — no schema impact. No item in EPIC-03/04/05/06 touches the data model. Plan is executable as scoped.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Capacity Check

**Effort Band Lookup (ST-14):** No active roadmap initiatives (CPS = N/A) — no pre-assigned effort bands in `scored_initiatives.md`. All EPICs sized via inline STEP 4 estimate.

**Estimation convention:** Where a backlog item states an explicit day range (e.g. "M (~2–3d)"), its midpoint is used. Where an item carries a bare effort label with no explicit range (the majority of P3 items), the following defaults apply: XS = 0.375d, S = 1d, M = 2d, L = 4d.

Confirmed capacity band: **~24–28 working-day-equivalent units** (`claude/roadmap/workforce_capacity.md`, unchanged since 2026-07-17).

| EPIC | Subtotal (days) |
|------|------------------|
| EPIC-01 | 3.25 |
| EPIC-02 | 11.00 |
| EPIC-03 | 3.375 |
| EPIC-04 | 3.375 |
| EPIC-05 | 2.375 |
| EPIC-06 | 2.75 |
| **Total** | **26.125** |

Total estimated effort (26.125 days) sits within the confirmed 24–28 day band (~93–109% of the range, near its midpoint) — matches the Product Owner's explicit widen-to-full-capacity decision. No WARN triggered (WARN applies only when estimated effort exceeds the band's upper bound); PASS.

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity / 5.7 Decision Record Integrity

**5.5 Cross-Stage Integrity:** All S2-01..S2-06 map to EPIC-01..EPIC-06 (1:1). All EPIC IDs in `stage4_backlog_slice.md` match this document's Execution Plan table. All RISK-01..RISK-06 appear in the Risk Register above with no orphaned references. Pass.

**5.7 Decision Record Integrity:** Skipped — `artifacts.escalations` not present this cycle (no escalations raised; 0 open, 0 deferred, 0 accepted-risk). Not applicable.

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```
