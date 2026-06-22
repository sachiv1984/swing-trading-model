Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Published
Release: v6.1
Cycle: 2026-06-22__release-v6.1
Last Updated: 2026-06-22

---

# Release Plan — v6.1 Governance Correctness, CI Quality & User Value Foundation

---

## Readiness

**Prior cycle:** 2026-06-19__release-v6.0 — Closed_with_actions (post_ship_complete = true, next_cycle_unblocked = true).
**Lifecycle guard:** status = Closed → Release Planning permitted. ✓
**post_ship_complete:** true ✓
**next_cycle_unblocked:** true ✓

### Readiness Advisories

**1.1 Backlog Age:** No spec/documentation debt items aged 2+ cycles without story assignment in scope.

**1.2 Provisional-Target:** 7 items carry `Provisional-Target: v6.1`. 1 item (BLG-FEAT-25) carries `Provisional-Target: v4.0+` gate-conditional — included as conditional per rebalance.

**1.3 Design-Gate Language Scan:** ⚠ Design dependency detected on BLG-FE-76 (SectorHeatMap component — page placement + concentration alert design required) and BLG-FE-78 (badge/counter — placement decision required). Design gate required before sprint planning seals. `design_gate_required = true`.

**1.4a Perennial-Return:** BLG-FEAT-25/PT-04 has been deferred 8+ consecutive cycles under gate condition. PO active disposition on file (advance when ≥20 closed trades confirmed, re-verified v6.0 2026-06-16 at 13 trades). Proceed.

**1.4b Within-Sprint Date Gate:** BLG-FEAT-25/PT-04 gate clearing estimate ~2026-07-02 falls within the projected sprint execution window. **Mandatory classification: conditional.** Cannot be firm capacity.

**1.4 Gate Proximity:**

| Item | Gate condition | Current trajectory | Projected clear date |
|------|---------------|-------------------|---------------------|
| BLG-FEAT-25/PT-04 | ≥20 closed trades | 13 at 2026-06-16 (~1.5/wk) | ~2026-07-02 |
| SI-02 frontend | ≥20 closed trades | Same | ~2026-07-02 |
| PO-02 (Arc 4) | 6+ months AI journals | Unknown | ~Oct 2026 est. |

Arc 4 data density: closed trade count = 13 (2026-06-16); AI journal count = not available (PO to surface at sprint planning).

---

## Scope

### S2 Scope Items

| S2-ID | BLG ID | Title | Priority | Effort | Type | Classification |
|-------|--------|-------|----------|--------|------|----------------|
| S2-01 | BLG-GOV-132 | Release planning: Design Gate Required flag | P1 | S | G | Firm |
| S2-02 | BLG-GOV-133 | Sprint planning: Design Gate hard gate at preflight | P1 | S | G | Firm |
| S2-03 | BLG-QA-60 | Register morning-briefing.spec.js and screener-quality.spec.js in playwright.yml | P2 | XS | D | Firm |
| S2-04 | BLG-FE-76 | Portfolio sector heat-map visualization | P2 | M | U | Firm |
| S2-05 | BLG-GOV-131 | Governance overhead ceiling metric and accountability mechanism | P2 | S | G | Firm |
| S2-06 | BLG-FE-78 | Trade gate proximity indicator on dashboard | P3 | S | U | Firm |
| S2-07 | BLG-OPS-73 | Add PATCH /trades/{id}/costs to api_performance_baseline.md | P3 | XS | D | Firm |
| S2-08 | BLG-FEAT-25 | Setup Quality Score — backend + frontend (PT-04) | P1 | M | U | **Conditional — gate: ≥20 closed trades (~2026-07-02)** |

**Firm scope:** 7 items (S2-01 through S2-07)
**Conditional scope:** 1 item (S2-08)
**Total:** 8 scope items

### Items Explicitly Deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-GOV-134 — CI OpenAPI/baseline drift detection | Provisional-Target v6.1 but not in rebalance Now section table; advisory deferred per STEP 2 scope-lock rule | v6.2 candidate |
| BLG-QA-62 — Playwright glob auto-registration | Provisional-Target v6.1 but not in rebalance Now table; structural follow-on to BLG-QA-60 | v6.2 candidate |
| BLG-FE-77 — Watchlist.js ESLint compliance | Provisional-Target v6.1 but not in rebalance Now table | v6.2 candidate |
| BLG-OPS-74 — Log morning briefing API cost | Provisional-Target v6.1 but not in rebalance Now table | Unscheduled |
| BLG-QA-61 — signals_scenarios.md review | v6.1 provisional but not in rebalance Now table | Before next signal sprint |
| SI-02 frontend | Gate condition same as PT-04; assess at sprint planning if gate clears | v6.2+ |

---

## Execution Plan

### EPIC Table

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01, S2-02, S2-05 | Head of Specs Team; PMO Lead | RISK-01 | First — governance patches must precede sprint planning of this very cycle |
| EPIC-02 | S2-03, S2-07 | Director of Quality; Infrastructure & Operations Owner | RISK-02 | After EPIC-01; no hard dependency but CI item easiest after GOV patches |
| EPIC-03 | S2-04, S2-06 | Head of UX & Design; Frontend Specs & UX Documentation Owner | RISK-03 | After Design Gate; BLG-FE-76 requires design sign-off before implementation |
| EPIC-04 | S2-08 | Head of Backend Engineering; Head of UX & Design | RISK-04 | Conditional — sprint planning gate check required; may run parallel to EPIC-03 |

**EPIC-01 note:** GOV-132 patches release_planning_prompt.md; GOV-133 patches sprint_planning_prompt.md. These are Correctness Fast-Track items (STEP 8.0 of rebalance). They directly affect the engine running this and the next phase. Highest-priority EPIC.

**EPIC-03 note:** BLG-FE-76 is a new data visualisation component requiring design gate sign-off (Head of UX & Design + Product Owner). BLG-FE-78 is smaller (badge/counter reading existing gate-metrics endpoint) and may be autonomous.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | Governance prompt patches (STEP 1.4b mandatory, GOV-132/133) require versioned edits to release_planning_prompt.md and sprint_planning_prompt.md per §6 checklist — missed checklist step would leave prompts in non-compliant state | High | Run governance edit checklist (§6) explicitly for each file; verify prompt_change_log.md entry + OPERATIONAL_GUIDE §14 update in same commit | null |
| RISK-02 | EPIC-02 | CI changes to playwright.yml could inadvertently exclude existing specs or cause test order issues | Medium | Run full CI suite after playwright.yml change; verify all pre-existing specs still execute | null |
| RISK-03 | EPIC-03 | BLG-FE-76 (sector heat-map) requires new backend endpoint for sector weight aggregation — spec must be clear before implementation; design gate must pass first | High | Design gate required (run design-gate --cycle 2026-06-22__release-v6.1) before EPIC-03 sprint planning. BLG-FE-78 reads existing GET /portfolio/gate-metrics endpoint — lower risk | null |
| RISK-04 | EPIC-04 | PT-04 gate (≥20 closed trades) may not clear by sprint seal date — conditional item has high perennial-return risk | Medium | Classify as conditional; PMO Lead re-verifies trade count at sprint planning; if gate not met, EPIC-04 returned to backlog without sprint impact | null |

---

## Integrity Validation — 3.5 Local Model Integrity

### Cross-Reference Check
- S2-01 → EPIC-01 ✓
- S2-02 → EPIC-01 ✓
- S2-03 → EPIC-02 ✓
- S2-04 → EPIC-03 ✓
- S2-05 → EPIC-01 ✓
- S2-06 → EPIC-03 ✓
- S2-07 → EPIC-02 ✓
- S2-08 → EPIC-04 ✓

All S2 IDs map to EPICs. All EPIC IDs reference valid scope items. All RISK IDs in EPIC table appear in Risk Register. No orphaned references.

**Stage 3.5 Local Model Integrity: PASS**

---

## Capacity Check

### Effort Estimates

| EPIC | Stories | Effort (mid-point hrs) | Notes |
|------|---------|----------------------|-------|
| EPIC-01 | 3 (ST-01, ST-02, ST-03) | ~5 hrs | 2×S (~2h each) + 1×S (~1h) — governance prompt edits; well-defined scope |
| EPIC-02 | 2 (ST-04, ST-05) | ~2 hrs | 2×XS — CI file edit + one baseline row |
| EPIC-03 | 2 (ST-06, ST-07) | ~10 hrs | S2-04 (M, ~2-3 days = 8h) + S2-06 (S, ~2h) — frontend new component + badge |
| EPIC-04 | 2 (ST-08, ST-09) | ~12 hrs | M conditional — backend + frontend for PT-04 (~2-3 day estimate) |

**Firm effort total (EPIC-01 + EPIC-02 + EPIC-03):** ~17 hrs
**Conditional addition (EPIC-04):** ~12 hrs
**Grand total (firm + conditional):** ~29 hrs

### Available Capacity
No explicit --capacity or --timebox provided. Standard assumption: solo-dev evenings, ~2-3 hrs/day × 5 days/wk → ~10-15 hrs/week. Two-sprint window (~2-3 weeks) → ~20-45 hrs available.

### Assessment
**Firm scope (17 hrs):** Comfortably within 1 sprint (~10-15 hrs) with some buffer. **PASS**

**With conditional (29 hrs):** Exceeds comfortable single-sprint capacity but fits a 2-sprint window. **WARN (phasing required)**

### Phasing Recommendation

Given the Skill-Silo ceiling (40% G+D+P stories per sprint) and the EPIC-03 design gate dependency:

**Sprint 1:** EPIC-01 (3 stories, all G) + EPIC-02 (2 stories, D) = 5 stories total; G+D = 5/5 = 100% — exceeds ceiling. Sprint planning must phase EPIC-01 carefully.

**Revised Sprint Phasing Recommendation:**

| Sprint | Stories | G+D+P% | Notes |
|--------|---------|---------|-------|
| Sprint 1 | ST-01 (G), ST-02 (G), ST-06 (U), ST-07 (U) | 2/4 = 50% | Design gate must pass first for EPIC-03 |
| Sprint 2 | ST-03 (G), ST-04 (D), ST-05 (D), [ST-08, ST-09 conditional] | 3/4 = 75% (or 3/6 = 50% with conditional) | GOV-131 metric proposal + CI items |

⚠ Sprint 1 G+D+P = 50% (exceeds 40% ceiling). Sprint planning engine must further subdivide or resequence to stay within ceiling. Recommendation: move ST-01 + ST-02 to their own EPIC-01 mini-sprint or batch with at minimum 2 U stories. Alternative: split into 3 sprints of ~3 stories each with ceiling respected per sprint.

Sprint planning is authoritative on phasing — this is indicative guidance only.

**`artifacts.stage4_5_capacity_check`: warn**

---

## Integrity Validation — 5.5 Cross-Stage Integrity

### 5.5 Cross-Stage Integrity Check

**S2 → EPIC mapping:** All 8 S2 IDs map to exactly one EPIC:
- S2-01, S2-02, S2-05 → EPIC-01 ✓
- S2-03, S2-07 → EPIC-02 ✓
- S2-04, S2-06 → EPIC-03 ✓
- S2-08 → EPIC-04 ✓

**EPIC IDs in backlog slice match stage3 plan:** EPIC-01 through EPIC-04 all present in stage4_backlog_slice.md ✓

**RISK IDs in EPIC table appear in Risk Register:** RISK-01 through RISK-04 all present ✓

**No orphaned references:** ✓

**5.7 Decision Record Integrity:** `artifacts.escalations = not_started` (no escalations raised) → STEP 5.7 not applicable (skipped per conditional gate rule).

**Stage 5.5 Cross-Stage Integrity: PASS**
**Stage 5.7 Decision Record Integrity: not_applicable**
