Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v9.1
Cycle: 2026-09-03__release-v9.1
Last Updated: 2026-09-03

# Release Plan — v9.1

## Readiness

Preflight PASS (see `run_manifest.md` STEP -1). Release cleared for planning via STEP -1.2 Option (b) equivalence — no formal `## v9.1` roadmap section exists; `2026-08-11__scheduled` rebalance recorded a documented Option (b) defer decision (4th consecutive firing at that rebalance), which this routine treats as authorization to draw scope directly from the ungated backlog pool for `plan release`, consistent with the precedent relied on for v8.5–v9.0 (now 6 consecutive release cycles).

**Anchor scope:** None. No item carries `Provisional-Target: v9.1` (no horizon signal existed before this session). All 15 P1 items remain Arc 5/SI-02/SI-05/PO-02 gate-conditional; the sole ungated P2 feature candidate (`BLG-FEAT-92`) was reconciled this session as a `BLG-FEAT-30` sub-scope (see Scope below) and excluded.

**Capacity assumption (Product Owner decision, 2026-09-03 — explicit user instruction: "use full capacity"):** Confirmed capacity band: ~24–28 working-day-equivalent units (`claude/roadmap/workforce_capacity.md`, unchanged since 2026-07-17). Scope widened to the top of the band — see Capacity Check below.

Advisories (full detail in `run_manifest.md`):
- Backlog Age Advisory: `BLG-SPEC-132` carries a passed `Provisional-Target: v8.10` (a release label never reached); reassigned into this release's scope rather than re-deferred (see Scope decisions in `decisions--2026-09-03__release-v9.1.md`).
- Provisional-Target Advisory: `BLG-GOV-74` and `BLG-GOV-311` also carry passed provisional targets (`v4.10 or first cycle after 2026-08-29` and `v8.9 or next cycle touching strategy_rules.md`, respectively) — both reassigned into scope, resolving all 3 items named in `backlog_health_20260903.md`'s outstanding Product Owner decision.
- Design-Gate Language Scan: EPIC-01 (`BLG-FE-165`–`BLG-FE-169`) is directly UI-facing (colour-contrast, accessible-name/label fixes) — classified `design_gate_required: true` at STEP 4.1.
- Gate-Detection Procedure (`scripts/scan_backlog_gate_conditions.py`): 251 items scanned. All 41 selected items confirmed ungated. 6 data-quality warnings (embedded gate language, no formal Gate field) manually excluded per the BLG-OPS-48 pattern. `BLG-FEAT-92` reconciled and excluded (see Scope). `BLG-GOV-105`/`BLG-GOV-315` shortlisted then dropped — both stale-but-resolved, pending `groom backlog` archival.
- Perennial-Return Check / Within-Sprint Date Gate: not formally triggered (no gate-conditional item in scope); `BLG-FEAT-92`/`BLG-GOV-105` given an explicit active disposition anyway, in the spirit of §1.4a, given their 3-cycle recurrence.

```yaml
artifacts.stage1_readiness: pass
```

---

## Scope

Scope document: `docs/product/scope/scope--2026-09-03__release-v9.1.md`

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | Frontend accessibility & UI consolidation (5 axe-core violation fixes, debounce-hook consolidation, keyboard-navigation spec section) |
| S2-02 | EPIC-02 | Backend reliability & technical debt (npm build regression, fail-open logging, sector-lookup consolidation, raw-SQL extraction) |
| S2-03 | EPIC-03 | QA & test coverage (3 Arc5ComplianceSection Playwright gaps, quality trend index, DoD/DoQ spot-checks, regression suite budget) |
| S2-04 | EPIC-04 | Governance process debt & overdue dispositions (auto-close bug fix, 3 passed-target resolutions, recurrence-check fix, Displacement Debt Register, 2 spec-debt fixes, Specs_Index changelog) |
| S2-05 | EPIC-05 | Spec & knowledge debt / AI governance register (spec consolidation, AI touchpoint register, effort-band/PVR metric structuring, terminology definitions) |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| `BLG-FEAT-92` | Reconciled as `BLG-FEAT-30` sub-scope this session; inherits its gate (screener live ≥60 days AND ≥60 closed trades with attribution), currently NOT MET. | After `BLG-FEAT-30`'s gate clears |
| `BLG-FEAT-73` (SI-02 frontend) | PO disposition (2026-08-17): re-check no earlier than 2026-11-09 or 10 new linked `trade_plans`. Neither met. | Next re-check trigger |
| `BLG-FEAT-74` (PO-05 Replay Mode) | §13 determinism pre-clearance not yet run. | After §13 pre-clearance |
| `BLG-GOV-105` | Already ✅ CLOSED (duplicate of `BLG-GOV-45`); stale, pending archival. 3rd consecutive cycle flagged. | `groom backlog` archival |
| `BLG-GOV-315` | Underlying fix already applied same-day (`execution_prompt.md` v3.71); item itself pending archival. | `groom backlog` archival |

Remaining ungated P2/P3 pool (well over 150 items) remains available for future release cycles; none were displaced from a committed scope.

```yaml
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

**Format note:** full acceptance criteria live in `stage4_backlog_slice.md`. This table is sequencing/ownership/risk only.

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-01 | Frontend Specifications & UX Documentation Owner; Director of Quality | RISK-01 | Sequenced first — only EPIC with observable UI ACs; design gate must clear before this EPIC enters sprint execution. |
| EPIC-02 | S2-02 | Backend Engineering Patterns Owner; Head of Engineering | RISK-02 | ST-08 (`BLG-TECH-18`, npm build regression) sequenced first within the EPIC — currently-reproducible build-breaking bug. |
| EPIC-03 | S2-03 | Director of Quality; QA & Testing Owner | RISK-03 | Design gate not required — tests/audits only |
| EPIC-04 | S2-04 | Head of Specs Team; PMO Lead; Strategy Rules & System Intent Owner | RISK-04 | ST-21 (`BLG-GOV-311`) requires write access to `claude/strategy/strategy_rules.md` under Strategy Rules & System Intent Owner authority — outside standard Sprint Execution write scope; flag for delegated/agent-mediated sign-off per `execution_prompt.md` §5.3. |
| EPIC-05 | S2-05 | Head of Specs Team; AI Compliance & Governance Officer | RISK-05 | None |

**EPIC-01:** All 5 axe-core fixes trace to `tests/e2e/accessibility-axe-scan.spec.js`'s existing `KNOWN_VIOLATIONS` allowlist entries — each fix's AC is removing its own allowlist entry once the underlying violation is fixed, giving this EPIC a mechanically verifiable completion signal. `BLG-TECH-14` and `BLG-SPEC-99` are grouped here as the same frontend-consolidation/spec theme.

**EPIC-04:** This is the largest EPIC by item count (10) but modest by effort (3.90d) — reflects the release's overdue-disposition clearing theme: 3 passed-provisional-target items, 1 live operational bug (`governance_sync.yml` auto-close gap, found live at v9.0's own sprint execution), 1 half-achieved carried item (`BLG-GOV-264`), and 5 smaller process/spec-debt fixes.

**No build-and-ship U-item found ready — same finding as v9.0.** No qualifying ungated build-and-ship U-item exists in the backlog this cycle (all P1 candidates remain gate-blocked; the nearest P2 candidate, `BLG-FEAT-92`, was reconciled and excluded this session — see Scope). Flagged here rather than silently omitted, per the Skill-Silo mitigation guideline (`release_planning_prompt.md` §3). Unlike v9.0, this cycle also carries no live-production-bug anchor scope — it is entirely backlog-driven hygiene/debt-clearance work. The `BLG-FEAT-92`/`BLG-FEAT-30` gate (screener trade-volume threshold) remains the most direct path to a real build-and-ship candidate in a future cycle.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | Colour-contrast/label fixes could shift visual design-token usage in ways not confirmed by the design gate | Low | Design gate scoped as `design_gate_required: true`; each fix's own AC (KNOWN_VIOLATIONS entry removal) is Playwright-verifiable in CI | null |
| RISK-02 | EPIC-02 | `BLG-BE-110`'s raw-SQL extraction touches `backend/routers/analytics.py`/`digest.py` production analytics/digest code paths (32 combined call sites) | Medium | Structural move only, no query rewrite; full existing test suite for both routers must pass unchanged, per the item's own AC | null |
| RISK-03 | EPIC-03 | None material — all 7 items are additive test/audit/documentation scope with no production behaviour change | Low | Standard review | null |
| RISK-04 | EPIC-04 | `BLG-GOV-311`'s `strategy_rules.md` §13.5 roster edit requires write access outside standard Sprint Execution scope (`claude/strategy/*` is governance-file-restricted per CLAUDE.md §2) | Medium | Route through delegated/agent-mediated Strategy Rules & System Intent Owner sign-off, per `execution_prompt.md` §5.3's existing pattern for this exact restriction | null |
| RISK-05 | EPIC-05 | None material — all 13 items are documentation/register/retrospective scope with no production behaviour change | Low | Standard review | null |

```yaml
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

None of the 41 in-scope items introduce a new database table or column. `BLG-BE-110` (raw SQL extraction) and `BLG-TECH-13` (sector-lookup consolidation) restructure existing query call sites through the existing `database.py` layer — no schema change. `BLG-TECH-18`, `BLG-TECH-16`, `BLG-TECH-14` are build-tooling/logging/frontend-hook changes with no data-model surface. All EPIC-03/04/05 items are test/documentation/register/retrospective scope — no data model touched. Plan is executable as scoped.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Capacity Check

**Effort Band Lookup (ST-14):** No active roadmap initiatives (CPS = N/A) — no pre-assigned effort bands in `scored_initiatives.md`. All EPICs sized via inline STEP 4 estimate.

**Estimation convention:** Where a backlog item states an explicit day range (e.g. "S (~0.5–1d)"), its midpoint is used. Items marked "<1h" or "~15min" are estimated at 0.1d. Where an item carries a bare effort label with no explicit range, the following defaults apply: XS = 0.1d, S = 0.5d, M = 1.5d, L = 4d.

Confirmed capacity band: **~24–28 working-day-equivalent units** (`claude/roadmap/workforce_capacity.md`, unchanged since 2026-07-17).

| EPIC | Subtotal (days) |
|------|------------------|
| EPIC-01 | 3.70 |
| EPIC-02 | 6.10 |
| EPIC-03 | 3.30 |
| EPIC-04 | 3.90 |
| EPIC-05 | 10.50 |
| **Total** | **27.50** |

Total estimated effort (27.50 days) sits within the confirmed 24–28 day band, at its upper bound (~98–115% of the range) — matches the Product Owner's explicit "use full capacity" instruction for this invocation, consistent with v9.0's 27.15d, v8.9's 26.1d, and v8.7's 25.25d. No WARN triggered (WARN applies only when estimated effort exceeds the band's upper bound); PASS.

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
