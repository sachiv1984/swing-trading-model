**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v6.3
**Cycle:** 2026-06-26__release-v6.3
**Last Updated:** 2026-06-26

---

# Release Plan — v6.3 Strategy Benchmark, AI Security & Quality Infrastructure

---

## Readiness

**Roadmap authority:** §-1.2 cleared via STEP 8.1 Option(b) decision from rebalance 2026-06-26__scheduled. cycle_summary.md records: "Now horizon: intentionally empty (PO STEP 8.1 Option b — defer to `plan release v6.3`)". `**Next planned release:** v6.3` confirmed in roadmap §1 header.

**Context:** v6.2 (Production Strategy Parity & AI Intelligence) shipped 2026-06-25 with full velocity (13/13 stories). v6.3 opens with two mandatory production correctness fixes surfaced post-v6.2 ship (BLG-BE-39, BLG-FE-79) alongside a P1 security hardening cluster (BLG-OPS-81 rate limiting, BLG-GOV-146 injection threat model), P1 test infrastructure (BLG-QA-65/66 nightly computation CI simulation), and the flagship feature: Strategy Benchmark page (BLG-FEAT-53 — compare live trades against backtest). Product Value Ratio (0.37, advisory) and Skill-Silo (51.5%, advisory) both improved from v6.1; v6.3 must sustain the U-heavy mix with BLG-FEAT-53 and BLG-FE-80.

**Advisories from STEP 1:**
- ℹ No perennial-return items; no within-sprint date gates (§1.4a/b).
- ⚠ Advisory (§1.2): BLG-BE-39 and BLG-FE-79 carry stale `Provisional-Target: v6.2` — mandatory v6.3 per rebalance STEP 8.0 mandate; update in backlog.md post-publish.
- ⚠ Advisory (§1.3): Design dependencies on BLG-FE-79 (R-multiple rendering), BLG-FEAT-53 (new 3-panel page), BLG-FE-80 (expand/collapse interaction). Design Gate required — 3 items classified as UI-facing.
- ℹ Carry-forward: FI-P3-01 (Playwright strict mode template fix — 2nd occurrence), FI-P3-02 (frontend testing gate clarification), FI-P4-01 (CI spec_references convention) — governance improvement items; action during sprint execution.
- ℹ Arc 4 data density: AI journals started v6.2 2026-06-25; PO-02 gate ~2026-12; PO-04 gate trajectory unknown; SI-02 gate ~2026-09.

---

## Scope

| S2-ID | Backlog Item | Description | Priority | Effort | Type | Class |
|-------|-------------|-------------|----------|--------|------|-------|
| S2-01 | BLG-BE-39 | Fix AI journal summary on Trade History tab (silent failure) | P1 | S | Bug | Firm |
| S2-02 | BLG-FE-79 | Fix R-multiple not displaying on Reflection page (shows "—") | P1 | S | Bug | Firm |
| S2-03 | BLG-OPS-81 | AI endpoint per-endpoint rate limiting hardening (POST /ai/*) | P1 | S | Operations/Security | Firm |
| S2-04 | BLG-GOV-146 | AI response injection risk assessment (threat model) | P1 | S | Governance/Security | Firm |
| S2-05 | BLG-GOV-147 | AI feature advisory disclaimer visibility assessment (§13) | P2 | S | Governance/§13 | Conditional |
| S2-06 | BLG-GOV-148 | API contract review checklist for AI advisory endpoints | P2 | S | Governance/Spec | Conditional |
| S2-07 | BLG-QA-65 | Nightly stop computation CI simulation tests | P1 | S | QA/Test Coverage | Firm |
| S2-08 | BLG-QA-66 | Strategy signal regression test specification | P1 | S | QA/Spec | Firm |
| S2-09 | BLG-QA-67 | AI chat response schema validation tests | P2 | S | QA/Test Coverage | Conditional |
| S2-10 | BLG-QA-68 | §13 boundary test suite for AI advisory endpoints | P2 | S | QA/Spec | Conditional |
| S2-11 | BLG-FEAT-53 | Strategy Benchmark page: compare live trades against backtest | P2 | L | Feature | Firm |
| S2-12 | BLG-FE-80 | Morning briefing progressive disclosure (expand/collapse sections) | P2 | S | Frontend/UX | Firm |
| S2-13 | BLG-OPS-79 | Background scheduler health monitoring endpoint (GET /health/scheduler) | P2 | S | Operations | Conditional |
| S2-14 | BLG-OPS-78 | Measure live latency for POST /ai/daily-briefing and POST /ai/chat | P3 | XS | Operations | Conditional |
| S2-15 | BLG-OPS-80 | Render deployment rollback procedure documentation | P3 | XS | Operations/Runbook | Conditional |

**Items explicitly deferred:** BLG-FEAT-52 (Trade tagging — Arc 4 PO-02 gate: ~2026-12). BLG-QA-63 (a11y testing — Arc 5 not fully stabilised). BLG-OPS-76/77 (gate-conditional: BLG-OPS-25/71 not complete). BLG-GOV-137/138/139 (gate-conditional: tooling/velocity_metrics.md path resolution not confirmed). BLG-GOV-149 (AI caching evaluation — Provisional-Target: Unscheduled). All backlog items below P2 or gate-blocked not listed in v6.3 provisional target.

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01, S2-02, S2-03, S2-04, S2-05, S2-06 | Head of Backend Engineering; Cybersecurity & Trust Lead | RISK-02 | Sprint 1 first — P1 correctness + security hardening before feature work |
| EPIC-02 | S2-07, S2-08, S2-09, S2-10 | QA Lead; Director of Quality | RISK-03 | Sprint 1 alongside EPIC-01 — test infrastructure is independent |
| EPIC-03 | S2-11, S2-12, S2-13, S2-14, S2-15 | Product Owner; Head of Engineering | RISK-01 | Sprint 2 — BLG-FEAT-53 (L effort) leads; UX/ops items fill capacity |

**EPIC-01 note:** P1 mandatory cluster. BLG-BE-39 (AI journal summary silent failure) and BLG-FE-79 (R-multiple display) are non-negotiable correctness fixes per rebalance STEP 8.0 mandate. BLG-OPS-81 (rate limiting) and BLG-GOV-146 (injection threat model) are P1 security items for the live AI endpoints shipped in v6.2. S2-05/06 (GOV-147/148 — §13 disclaimer assessment and API contract checklist) are conditional P2 governance items; include in Sprint 1 if EPIC-01 firm items complete early.

**EPIC-02 note:** P1 test infrastructure. BLG-QA-65 (nightly stop CI simulation) and BLG-QA-66 (regression test specification) fill the zero-coverage gap on nightly computation services introduced in v6.2. BLG-QA-67/68 (conditional) add AI endpoint schema validation and §13 boundary test suite; include in Sprint 1 if capacity allows alongside EPIC-01. EPIC-02 items are independent of both EPIC-01 and EPIC-03.

**EPIC-03 note:** BLG-FEAT-53 (Strategy Benchmark page — L effort) is the flagship feature requiring new DB schema, import mechanism, 3 API endpoints, and a full 3-panel frontend page. Leads Sprint 2. BLG-FE-80 (morning briefing expand/collapse, S effort) is a mandatory UX pull-forward from the rebalance PVR advisory; pair with Sprint 2 if Sprint 1 capacity is full. BLG-OPS-79/78/80 are conditional — include at sprint planning based on Sprint 1 velocity. BLG-FEAT-53 schema migration (backtest_trades, backtest_yearly_performance) must complete before API work begins.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-03 | BLG-FEAT-53 is L-effort (~5 days): new DB schema (2 tables), 3 API endpoints, import mechanism, 3-panel frontend page. Schema complexity may undermine Sprint 2 estimate; frontend panel scope may expand. | High | Sequence: DB schema first → API → frontend. Gate frontend on API completion. Import script is standalone (parallel-able). If Sprint 2 overflows, conditional EPIC-03 items (S2-13, S2-14, S2-15) deferred. | null |
| RISK-02 | EPIC-01 | BLG-GOV-146 (AI injection risk assessment) may surface open risks requiring immediate remediation. A high-severity finding would require an emergency backlog item outside current v6.3 scope. | Medium | GOV-146 is assessment-only; any remediation items will be filed as new backlog items targeting v6.4 unless P0 critical severity. Accept at current threat posture. | null |
| RISK-03 | Release-level | Total estimated effort ~9.0 days firm + ~2.75 days conditional = ~11.75 days. Solo dev 2-sprint capacity ~10–14 days. Conditional items may overflow Sprint 2 if BLG-FEAT-53 fills capacity. | Medium | Conditional items (S2-05, S2-06, S2-09, S2-10, S2-13, S2-14, S2-15) confirmed at sprint planning. Sprint 1 velocity will inform Sprint 2 conditional scope. | null |

---

## Integrity Validation — 3.5 Local Model Integrity

**S2 → EPIC mapping check:**
- S2-01, S2-02, S2-03, S2-04, S2-05, S2-06 → EPIC-01 ✅
- S2-07, S2-08, S2-09, S2-10 → EPIC-02 ✅
- S2-11, S2-12, S2-13, S2-14, S2-15 → EPIC-03 ✅

**RISK → EPIC mapping check:**
- RISK-01 → EPIC-03 ✅
- RISK-02 → EPIC-01 ✅
- RISK-03 → Release-level ✅

**Dependency chain integrity:** EPIC-01 and EPIC-02 are independent and can run Sprint 1 in parallel. EPIC-03 follows Sprint 2; no circular dependencies.

**Model integrity: PASS**

---

## Capacity Check

**Effort estimates (inline — no scored_initiatives.md match; Tier 3 per §16.7):**

| EPIC | Stories | Effort (days) | Firm/Conditional | Notes |
|------|---------|--------------|------------------|-------|
| EPIC-01 | ST-01 to ST-06 | 2.75 | 2.0 firm + 0.75 conditional | S2-01 (0.5d) + S2-02 (0.5d) + S2-03 (0.5d) + S2-04 (0.5d) + S2-05 (<0.5d ≈ 0.25d conditional) + S2-06 (0.5d conditional) |
| EPIC-02 | ST-07 to ST-10 | 2.5 | 1.5 firm + 1.0 conditional | S2-07 (1.0d) + S2-08 (0.5d) + S2-09 (0.5d conditional) + S2-10 (0.5d conditional) |
| EPIC-03 | ST-11 to ST-15 | 6.5 | 5.5 firm + 1.0 conditional | S2-11 (5.0d) + S2-12 (0.5d) + S2-13 (0.5d conditional) + S2-14 (<0.5d ≈ 0.25d conditional) + S2-15 (<0.5d ≈ 0.25d conditional) |
| **Total** | **15** | **11.75** | **9.0 firm + 2.75 conditional** | — |

**Capacity assumption:** ~10–15 hrs/week solo dev (consistent with v6.1/v6.2); 2 sprints = ~20–30 hrs/sprint ≈ 10–14 dev-days total.

**Assessment:** 9.0 days firm effort is achievable across 2 sprints. 11.75 total days (firm + conditional) at upper bound of capacity range. EPIC-03 flagship (BLG-FEAT-53, 5.0d) is the dominant risk item; Sprint 2 must be sequenced around it.

**Outcome: WARN** — Total estimated effort at upper bound of 2-sprint capacity; 2-sprint plan required with conditional items subject to capacity confirmation at sprint planning.

### Phasing Recommendation

| Phase | EPICs | Estimated effort | Rationale |
|-------|-------|-----------------|-----------|
| Sprint 1 | EPIC-01 (firm) + EPIC-02 (firm) + EPIC-01/02 conditionals if capacity | ~3.5 firm + up to 1.75 conditional | P1 correctness + P1 security + P1 test infrastructure. All independent. EPIC-01 and EPIC-02 firm items ~3.5d — leaves substantial Sprint 1 runway for conditional items. |
| Sprint 2 | EPIC-03 (BLG-FEAT-53 + BLG-FE-80) + EPIC-03 conditionals if capacity | ~5.5 firm + up to 1.0 conditional | Strategy Benchmark page leads Sprint 2. BLG-FE-80 (0.5d) pairs cleanly. EPIC-03 conditional items (scheduler monitoring, latency baseline, rollback runbook) fill remaining capacity. |

**Ordering rationale:** EPIC-01/02 in Sprint 1 because: P1 mandates, no dependencies on EPIC-03, and clearing correctness/security/test-infrastructure debt creates a stable foundation for the L-effort feature work in Sprint 2. EPIC-03 in Sprint 2 because: BLG-FEAT-53 (5.0d) fills most of Sprint 2 capacity on its own and has no Sprint 1 dependencies.

---

## Integrity Validation — 5.5 Cross-Stage Integrity

**5.5 Cross-Stage Integrity:**
- All S2 IDs (S2-01 through S2-15) map to EPICs in stage3 ✅
- All EPIC IDs in stage4_backlog_slice.md (EPIC-01, EPIC-02, EPIC-03) match stage3 ✅
- All RISK IDs in EPIC table (RISK-01, RISK-02, RISK-03) appear in Risk Register ✅
- No orphaned S2/EPIC/RISK references ✅

**5.7 Decision Record Integrity:** No escalations raised (`artifacts.escalations = none`) — 5.7 not applicable.

**Cross-stage integrity: PASS**
