Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v8.8
Cycle: 2026-08-14__release-v8.8
Last Updated: 2026-08-14

# Release Plan — v8.8

## Readiness

Preflight PASS (see `run_manifest.md` STEP -1). Release cleared for planning via STEP -1.2 Option (b) equivalence — no formal `## v8.8` roadmap section exists; `2026-08-11__scheduled` rebalance recorded a documented Option (b) defer decision (4th consecutive firing), which this routine treats as authorization to draw scope directly from the ungated backlog pool for `plan release`.

**Capacity assumption (Product Owner decision, 2026-08-14):** Presented with a tight 7-item scope (~5.25 days, all `Provisional-Target: v8.8` items) vs. widening toward the confirmed ~24–28 working-day capacity band, the Product Owner chose to widen scope. Confirmed capacity band: ~24–28 working-day-equivalent units (`claude/roadmap/workforce_capacity.md`, unchanged since 2026-07-17).

Advisories (full detail in `run_manifest.md`):
- Backlog Age Advisory: `BLG-SPEC-118` (api_changelog.md stale since v7.8.0, ≥5 releases without story assignment) promoted into scope per this advisory's recommendation.
- Provisional-Target Advisory: 7 items carry `Provisional-Target: v8.8` (`BLG-FE-161`, `BLG-FE-162`, `BLG-FE-163`, `BLG-OPS-143`, `BLG-OPS-144`, `BLG-OPS-145`, `BLG-BE-97`); 22 items have no Provisional-Target signal, drawn from the ungated P3 pool.
- Design-Gate Language Scan: no explicit design-pending language found.
- Gate-Detection Procedure (`scripts/scan_backlog_gate_conditions.py`): 275 items scanned, 170 gated + 6 data-quality warnings. All 29 selected items confirmed ungated. (`BLG-GOV-292` was shortlisted then dropped — its `Provisional-Target` field showed it already resolved 2026-08-11, pending archival, not live scope.)
- Perennial-Return Check / Within-Sprint Date Gate: not applicable — no gate-conditional items in scope.

```yaml
artifacts.stage1_readiness: pass
```

---

## Scope

Scope document: `docs/product/scope/scope--2026-08-14__release-v8.8.md`

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Live data-integrity & scheduled job coverage (screener refresh workflow, risk-off-alerts workflow, backtest import investigation, 3 performance-baseline completions) |
| S2-02 | EPIC-02 | Backend engineering hardening (regime-check consolidation, position lifecycle history, alert-to-trade linkage, digest logging fixes, query-latency review) |
| S2-03 | EPIC-03 | Frontend UX & dead-code cleanup (changelog user-facing copy, status badge fix, ticker universe filtering, dead-code mount points, shadcn variant remapping) |
| S2-04 | EPIC-04 | Quality & test-coverage debt (Arc 6 field audit, service-layer coverage report, test-environment parity, test.py completeness re-audit) |
| S2-05 | EPIC-05 | Security hardening (Claude prompt role separation, license compliance scan, npm audit review, Telegram token rotation policy gap) |
| S2-06 | EPIC-06 | API & spec debt closure (api_changelog.md backfill, stale field anchor fix) |
| S2-07 | EPIC-07 | Governance correctness fixes (CLAUDE.md §8 commit-template self-violation, prior_cycle field ownership gap) |

### Items explicitly deferred

None. This cycle draws directly from the ungated backlog pool (no formal roadmap Now-horizon scope exists to defer from — see Readiness). Remaining ungated P3 items not selected (70 of the 92 ungated P3 pool) remain available in `backlog.md` for future release cycles; none were displaced from a committed scope.

```yaml
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

**Format note:** full acceptance criteria live in `stage4_backlog_slice.md`. This table is sequencing/ownership/risk only.

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-01 | Infrastructure & Operations Owner | RISK-01 | None — leads capacity allocation; closes 2 live P1 data-integrity gaps |
| EPIC-02 | S2-02 | Backend Engineering Patterns Owner | RISK-02 | None |
| EPIC-03 | S2-03 | Frontend Specifications & UX Documentation Owner; Product Owner | RISK-03 | None — design gate required (see STEP 4.1) |
| EPIC-04 | S2-04 | Director of Quality; QA & Testing Owner | RISK-04 | None |
| EPIC-05 | S2-05 | Cybersecurity & Trust Lead | RISK-05 | None |
| EPIC-06 | S2-06 | API Contracts & Documentation Owner; Head of Specs Team | RISK-06 | None |
| EPIC-07 | S2-07 | Head of Specs Team; PMO Lead | RISK-07 | None |

**EPIC-01:** Leads the table — both `BLG-OPS-144` and `BLG-OPS-145` are live data-integrity issues (screener results 24 days stale; `RISK OFF` badge structurally incapable of reflecting real market regime), each `Provisional-Target: v8.8` and P1. `BLG-OPS-143` (backtest import investigation) and the 3 performance-baseline completions round out the operations pool.

**EPIC-02:** Includes `BLG-BE-97` (consolidate two divergent `check_market_regime()` implementations — found while investigating `BLG-OPS-145`) alongside 5 further ungated backend debt items (largest single subtotal this cycle — Skill-Silo mitigation rotation, per §3 guidance, weights this release toward execution-heavy scope).

**EPIC-03:** All 5 items carry observable UI acceptance criteria — `design_gate_required = true` (see STEP 4.1 below). `BLG-FE-161`/`BLG-FE-162`/`BLG-FE-163` are `Provisional-Target: v8.8`; `BLG-FE-159`/`BLG-FE-160` are ungated dead-code/token-remapping cleanup pulled in to widen scope.

**EPIC-06:** `BLG-SPEC-118` selected per the Backlog Age Advisory (stale since `v7.8.0`, ≥5 releases without a story assignment).

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | `BLG-OPS-143`'s root cause is unconfirmed pending live GitHub Actions/Render log review (not visible from a static code read) | Medium | Sequence the investigation first within the EPIC; if root cause requires scope beyond a single-cycle fix, file follow-up backlog item rather than extending this story indefinitely | null |
| RISK-02 | EPIC-02 | `BLG-BE-84`'s effort estimate is explicitly marked advisory/not fully scoped (schema + backend + frontend trade-creation wiring) | Medium | Confirm scope boundaries at sprint planning before commitment; trim to alert-to-trade linkage only if frontend wiring proves out of band | null |
| RISK-03 | EPIC-03 | `BLG-FE-161` requires a new curated user-facing description field sourced into `changelog_service.py` — touches the changelog authoring convention documented in release/post-ship prompts | Low | Scope the authoring-convention documentation update as part of this story's acceptance criteria, not a separate follow-up | null |
| RISK-04 | EPIC-04 | None material — all 4 items are audit/report-generation scoped, no runtime behaviour change | Low | Standard review | null |
| RISK-05 | EPIC-05 | Security testing/scans (`BLG-SEC-32`, `BLG-SEC-18`) must not disrupt CI or introduce new required-check failures against existing dependency baselines | Low | Run as read-only audits first; any remediation action filed as follow-up if it requires a version bump beyond simple review | null |
| RISK-06 | EPIC-06 | None material — both items are documentation-only | Low | Standard review | null |
| RISK-07 | EPIC-07 | `BLG-GOV-293`'s `prior_cycle` field fix touches `.claude_current_state.json` ownership — must not conflict with STEP 9's own authoritative write to that file this same cycle | Low | Sequence `BLG-GOV-293`'s fix as a scoped, single-field prompt/engine-ownership clarification, not a live state-file edit outside this routine's own STEP 9 write | null |

```yaml
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

All 30 in-scope items map to the existing data model or existing schema with no unresolved model ambiguity. `BLG-BE-58` (position lifecycle state-transition history table) and `BLG-BE-85` (`telegram_message_id` population) are the only items touching schema, and both extend existing tables (`positions`, `si05_digest_log`) — no new entity introduced without a mapped precedent. `BLG-BE-97`'s consolidation operates on existing endpoints/patterns only. Frontend items (EPIC-03) consume existing API response fields. No new database migrations required beyond straightforward column/table additions already scoped in the source backlog items. Plan is executable as scoped.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Capacity Check

**Effort Band Lookup (ST-14):** No active roadmap initiatives (CPS = N/A) — no pre-assigned effort bands in `scored_initiatives.md`. All EPICs sized via inline STEP 4 estimate.

Confirmed capacity band: **~24–28 working-day-equivalent units** (`claude/roadmap/workforce_capacity.md`, unchanged since 2026-07-17).

| EPIC | Subtotal (days) |
|------|------------------|
| EPIC-01 | 2.75 |
| EPIC-02 | 7.25 |
| EPIC-03 | 3.00 |
| EPIC-04 | 3.00 |
| EPIC-05 | 2.50 |
| EPIC-06 | 1.00 |
| EPIC-07 | 1.00 |
| **Total** | **20.50** |

Total estimated effort (20.50 days) sits below the confirmed 24–28 day band (~73–85% of the range) — comfortably within capacity with headroom, and a substantial increase over the tight-scope alternative (~5.25 days, ~20% of the band). No WARN triggered (WARN applies only when estimated effort exceeds the band's upper bound); PASS.

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity / 5.7 Decision Record Integrity

**5.5 Cross-Stage Integrity:** All S2-01..S2-07 map to EPIC-01..EPIC-07 (1:1). All EPIC IDs in `stage4_backlog_slice.md` match this document's Execution Plan table. All RISK-01..RISK-07 appear in the Risk Register above with no orphaned references. Pass.

**5.7 Decision Record Integrity:** Skipped — `artifacts.escalations` not present this cycle (no escalations raised; 0 open, 0 deferred, 0 accepted-risk). Not applicable.

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```
