Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v9.0
Cycle: 2026-08-21__release-v9.0
Last Updated: 2026-08-21

# Release Plan — v9.0

## Readiness

Preflight PASS (see `run_manifest.md` STEP -1). Release cleared for planning via STEP -1.2 Option (b) equivalence — no formal `## v9.0` roadmap section exists; `2026-08-11__scheduled` rebalance recorded a documented Option (b) defer decision (4th consecutive firing), which this routine treats as authorization to draw scope directly from the ungated backlog pool for `plan release`, consistent with the precedent already relied on for v8.5–v8.9.

**Anchor scope:** 4 items carry `Provisional-Target: v9.0`, horizon-signalled directly out of v8.9's own PR review process (2026-08-18/20): `BLG-BE-109` (nightly backtest month-end rebalance-date bug — found live 2026-08-21 investigating unexpected INTC/WDC trade behaviour), `BLG-BE-107` (root logger never configured — INFO-level logs silently dropped in production), `BLG-BE-108` (Product Owner decision needed on the AI Post-Trade Debrief's "linked journal entries" data source), `BLG-TECH-17` (debrief prompt encourages unverifiable cross-trade pattern claims).

**Capacity assumption (Product Owner decision, 2026-08-21 — explicit user instruction: "use full capacity"):** Confirmed capacity band: ~24–28 working-day-equivalent units (`claude/roadmap/workforce_capacity.md`, unchanged since 2026-07-17). Scope widened to the top of the band — see Capacity Check below.

Advisories (full detail in `run_manifest.md`):
- Backlog Age Advisory: no `BLG-SPEC`/documentation-debt item found aged 2+ cycles without a story assignment in the P1/P2 ungated pool.
- Provisional-Target Advisory: 4 items carry `Provisional-Target: v9.0`; 23 items have no v9.0-specific signal, drawn from the ungated P1–P3 pool.
- Design-Gate Language Scan: `BLG-FE-164` offers an optional new UI field as one of two acceptance paths — flagged for STEP 4.1.
- Gate-Detection Procedure (`scripts/scan_backlog_gate_conditions.py`): 267 items scanned, 170 gated/conditional. All 27 selected items confirmed ungated. `BLG-FEAT-73`/`BLG-FEAT-74` manually excluded despite no formal Gate field (see `run_manifest.md` — BLG-OPS-48-pattern data-quality note). `BLG-FEAT-92` shortlisted then dropped — same unresolved `BLG-FEAT-30` reconciliation dependency as `2026-08-17__release-v8.9`, now flagged as overdue for a standing PO/Head of Specs Team decision. `BLG-GOV-105` shortlisted then dropped — already ✅ CLOSED, pending `groom backlog` archival.
- Perennial-Return Check / Within-Sprint Date Gate: not applicable — no gate-conditional items in scope.

```yaml
artifacts.stage1_readiness: pass
```

---

## Scope

Scope document: `docs/product/scope/scope--2026-08-21__release-v9.0.md`

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | AI post-trade debrief & backtest correctness follow-through (nightly month-end rebalance-date fix, production log-visibility fix, debrief journal-source decision, debrief prompt verifiability fix, shared strategy-algorithm consolidation) |
| S2-02 | EPIC-02 | Live risk-management & trade-plan data-integrity closure (breakeven-floor stop audit/backfill, setup_type default disambiguation, table-init lock hardening, migration rollback tests, FX-override sizing gap, UK-market stop Playwright coverage) |
| S2-03 | EPIC-03 | Operational resilience & deploy-path safeguards (DB backup/restore drill, automated staging smoke test, staging drift detector, production PUBLIC_URL confirmation, GitHub Pages asset-path CI safeguard) |
| S2-04 | EPIC-04 | QA coverage & process hardening (Arc 5 QA protocol, visual regression baselines, R-multiple regression test, Arc5ComplianceSection coverage audit, axe-core accessibility scan, backend coverage PR reporting) |
| S2-05 | EPIC-05 | Backend architecture & cost/capacity hygiene (service-layer boundary review, DB connection pool tuning review, Render hosting tier review, Render cost trend dashboard, dependency upgrade cadence policy) |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| `BLG-FEAT-92` | Own item text requires "Reconciliation with `BLG-FEAT-30` completed and documented... before either item is scheduled"; `BLG-FEAT-30` remains gate-conditional. Not resolvable unilaterally by this routine. Dropped from firm scope for the 2nd consecutive cycle. | Next cycle, after PO/Head of Specs Team reconciliation |
| `BLG-FEAT-73` (SI-02 frontend) | PO disposition (2026-08-17) sets re-check no earlier than 2026-11-09 or 10 new linked `trade_plans`, whichever first. Neither condition met. | Next re-check trigger (2026-11-09 or milestone) |
| `BLG-FEAT-74` (PO-05 Replay Mode) | §13 determinism pre-clearance review not yet scheduled or run. | After §13 pre-clearance |
| `BLG-GOV-105` | Already ✅ CLOSED (confirmed duplicate, 2026-07-12); stale entry pending archival, not live scope. | `groom backlog` archival |

Remaining ungated P2/P3 pool not selected (well over 100 items) remains available in `backlog.md` for future release cycles; none were displaced from a committed scope.

```yaml
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

**Format note:** full acceptance criteria live in `stage4_backlog_slice.md`. This table is sequencing/ownership/risk only.

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-01 | Backend Engineering Patterns Owner; Strategy Rules & System Intent Owner; AI Compliance & Governance Officer | RISK-01 | Leads capacity allocation — closes out v8.9's own PR-review-originated follow-through items, including one live production data-correctness bug (`BLG-BE-109`). |
| EPIC-02 | S2-02 | Backend Engineering Patterns Owner; Product Owner; Frontend Specifications & UX Documentation Owner; Director of Quality | RISK-02 | `BLG-BE-105` touches live open-position stop values — sequence its regression-tested code path first within the EPIC. |
| EPIC-03 | S2-03 | Infrastructure & Operations Owner; Director of Quality | RISK-03 | Design gate not required (no observable UI AC) |
| EPIC-04 | S2-04 | Director of Quality; QA Lead; QA & Testing Owner; Financial Reporting & Records Owner | RISK-04 | Design gate not required — audits/tests only |
| EPIC-05 | S2-05 | Head of Engineering; Backend Engineering Patterns Owner; FinOps & Resource Architect | RISK-05 | None |

**EPIC-01:** All 5 items trace directly to agent-mediated review findings on v8.9's own EPIC-02 stories (ST-06 AI debrief, ST-07 backtesting engine), plus one live production bug (`BLG-BE-109`, found 2026-08-21 investigating anomalous nightly-backtest trade behaviour on INTC/WDC). This is genuine correctness/follow-through work, not new build-and-ship feature scope — no qualifying ungated build-and-ship U-item was found in the backlog this cycle (both P1 build candidates, `BLG-FEAT-73`/`BLG-FEAT-74`, remain gate-blocked; `BLG-FEAT-92`, the nearest P2 feature candidate, remains blocked on the `BLG-FEAT-30` reconciliation). Flagged here rather than silently omitted, per the Skill-Silo mitigation guideline (`release_planning_prompt.md` §3) — this release's EPIC table cannot lead with build-and-ship scope this cycle because no ready candidate exists; the standing `BLG-FEAT-92` reconciliation gap is the most direct path to changing that next cycle.

**EPIC-02:** `BLG-BE-105` closes a deferred AC from v8.9's own `BLG-BE-102` (ST-01) — the live-DB backfill that story's delivery explicitly could not verify in CI. Grouped with 5 further data-integrity/correctness items surfaced by the same v8.9 PR-review cycle plus one QA-coverage companion (`BLG-QA-153`).

**EPIC-03:** `BLG-OPS-148` and `BLG-OPS-147` both trace to the 2026-08-21 GitHub Pages white-page incident and its `BLG-OPS-146` (v8.9 ST-16) remainder — grouped with the pre-existing staging-resilience items (`BLG-OPS-103`, `BLG-OPS-25`, `BLG-OPS-90`) as one operational-resilience theme.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | `BLG-BE-109`'s fix changes the nightly-scheduled backtest rebalance-date computation directly consumed by the production backtest history table; `BLG-TECH-15`'s consolidation touches the same shared strategy-algorithm surface | High | Add the regression test specified in `BLG-BE-109`'s own AC before changing production behaviour; verify `BLG-TECH-15`'s consolidation against a fixed historical run before replacing either call site | null |
| RISK-02 | EPIC-02 | `BLG-BE-105`'s backfill directly modifies live open positions' `current_stop` values | High | Apply only via the existing, regression-tested `calculate_trailing_stop()` floor logic through the existing nightly recompute path — no bespoke one-off script, per the item's own scope note | null |
| RISK-03 | EPIC-03 | `BLG-OPS-90` and `BLG-OPS-25` both add automated gating to the CI/deploy pipeline; a false positive could block a legitimate deploy | Medium | Confirm each check fails correctly on a deliberately-broken dry run before enabling as a blocking gate, per each item's own AC | null |
| RISK-04 | EPIC-04 | None material — all 6 items are additive test/audit/documentation scope with no production behaviour change | Low | Standard review | null |
| RISK-05 | EPIC-05 | `BLG-BE-54`'s connection-pool tuning, if misapplied, could affect production DB connection availability | Low | Measure before adjusting; apply as a configuration change only, no code-path change | null |

```yaml
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

All 27 in-scope items map to the existing data model or introduce straightforward, precedented extensions. `BLG-BE-109`/`BLG-TECH-15` modify existing computation logic (`production_strategy.py`/`backend/services/backtest_rule_service.py`) — no schema change. `BLG-BE-105` writes through the existing `positions` table via the existing `calculate_trailing_stop()` path — no new column. `BLG-FEAT-93` and `BLG-BE-108` are decision-and-apply items against the existing `trade_plans` schema — any resulting change (a new `setup_type_source`-style field, or an extended prompt-context source) follows the existing migration convention. `BLG-BE-106` adds a `threading.Lock`, no schema impact. No item in EPIC-03/04/05 touches the data model. Plan is executable as scoped.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Capacity Check

**Effort Band Lookup (ST-14):** No active roadmap initiatives (CPS = N/A) — no pre-assigned effort bands in `scored_initiatives.md`. All EPICs sized via inline STEP 4 estimate.

**Estimation convention:** Where a backlog item states an explicit day range (e.g. "S (~0.5–1d)"), its midpoint is used. `BLG-OPS-147` ("<1h") is estimated at 0.15d. Where an item carries a bare effort label with no explicit range, the following defaults apply: XS = 0.375d, S = 1d, M = 2d, L = 4d.

Confirmed capacity band: **~24–28 working-day-equivalent units** (`claude/roadmap/workforce_capacity.md`, unchanged since 2026-07-17).

| EPIC | Subtotal (days) |
|------|------------------|
| EPIC-01 | 4.00 |
| EPIC-02 | 3.75 |
| EPIC-03 | 5.90 |
| EPIC-04 | 8.25 |
| EPIC-05 | 5.25 |
| **Total** | **27.15** |

Total estimated effort (27.15 days) sits within the confirmed 24–28 day band, near its upper bound (~97–113% of the range) — matches the Product Owner's explicit "use full capacity" instruction for this invocation. No WARN triggered (WARN applies only when estimated effort exceeds the band's upper bound); PASS.

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity / 5.7 Decision Record Integrity

**5.5 Cross-Stage Integrity:** All S2-01..S2-05 map to EPIC-01..EPIC-05 (1:1). All EPIC IDs in `stage4_backlog_slice.md` match this document's Execution Plan table. All RISK-01..RISK-05 appear in the Risk Register above with no orphaned references. Pass.

**5.7 Decision Record Integrity:** Skipped — `artifacts.escalations` not present this cycle (no escalations raised; 0 open, 0 deferred, 0 accepted-risk). Not applicable.

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```
