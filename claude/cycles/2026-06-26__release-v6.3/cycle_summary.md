**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Cycle:** 2026-06-26__release-v6.3
**Last Updated:** 2026-06-26
**Design Gate Required:** true

---

# Cycle Summary — Release Planning v6.3

## Release Identity

**v6.3 — Strategy Benchmark, AI Security & Quality Infrastructure**

**Context:** v6.2 (Production Strategy Parity & AI Intelligence) shipped 2026-06-25 with full velocity (13/13 stories). v6.3 opens with two mandatory P1 correctness fixes (BLG-BE-39, BLG-FE-79 per rebalance STEP 8.0 mandate), P1 security hardening for live AI endpoints (rate limiting + injection threat model), P1 test infrastructure for the v6.2 nightly computation services (zero CI coverage → fixture-based simulation), and the flagship feature: Strategy Benchmark page comparing live trades against the production_strategy.py backtest.

---

## Plan Overview

| Attribute | Value |
|-----------|-------|
| Cycle ID | 2026-06-26__release-v6.3 |
| Release | v6.3 |
| Date | 2026-06-26 |
| Mode | standard |
| Sprints planned | 2 |
| Capacity assessment | WARN (total ~11.75d; firm ~9.0d; 2-sprint plan) |
| EPICs | 3 (EPIC-01, EPIC-02, EPIC-03) |
| Total stories | 15 (8 firm, 7 conditional) |
| Design Gate Required | true — 3 UI-facing stories (ST-02, ST-11, ST-12) |

---

## Scope Summary

### EPIC-01 — Production Correctness & AI Security Hardening (Sprint 1)

| ST-ID | Description | BLG-ID | Class |
|-------|-------------|--------|-------|
| ST-01 | Fix AI journal summary on Trade History tab | BLG-BE-39 | Firm |
| ST-02 | Fix R-multiple not displaying on Reflection page | BLG-FE-79 | Firm |
| ST-03 | AI endpoint per-endpoint rate limiting hardening | BLG-OPS-81 | Firm |
| ST-04 | AI response injection risk assessment | BLG-GOV-146 | Firm |
| ST-05 | AI feature advisory disclaimer visibility assessment | BLG-GOV-147 | Conditional |
| ST-06 | API contract review checklist for AI advisory endpoints | BLG-GOV-148 | Conditional |

### EPIC-02 — Test Infrastructure & Quality Coverage (Sprint 1)

| ST-ID | Description | BLG-ID | Class |
|-------|-------------|--------|-------|
| ST-07 | Nightly stop computation CI simulation tests | BLG-QA-65 | Firm |
| ST-08 | Strategy signal regression test specification | BLG-QA-66 | Firm |
| ST-09 | AI chat response schema validation tests | BLG-QA-67 | Conditional |
| ST-10 | §13 boundary test suite for AI advisory endpoints | BLG-QA-68 | Conditional |

### EPIC-03 — Strategy Benchmark & UX Enhancement (Sprint 2)

| ST-ID | Description | BLG-ID | Class |
|-------|-------------|--------|-------|
| ST-11 | Strategy Benchmark page: compare live trades against backtest | BLG-FEAT-53 | Firm |
| ST-12 | Morning briefing progressive disclosure (expand/collapse sections) | BLG-FE-80 | Firm |
| ST-13 | Background scheduler health monitoring endpoint | BLG-OPS-79 | Conditional |
| ST-14 | Measure live latency for POST /ai/daily-briefing and POST /ai/chat | BLG-OPS-78 | Conditional |
| ST-15 | Render deployment rollback procedure documentation | BLG-OPS-80 | Conditional |

---

## Key Risks

| RISK-ID | Description | Priority | Mitigation |
|---------|-------------|----------|------------|
| RISK-01 | BLG-FEAT-53 (L-effort, ~5 days) — schema + 3 endpoints + 3-panel frontend page may underestimate Sprint 2 | High | Schema first → API → frontend; conditional EPIC-03 items defer if Sprint 2 overflows |
| RISK-02 | GOV-146 injection risk assessment may surface open items requiring remediation | Medium | Assessment-only; remediation items target v6.4 unless P0/critical |
| RISK-03 | Capacity WARN — conditional items (~2.75d) may overflow Sprint 2 capacity | Medium | Conditional items confirmed at sprint planning based on Sprint 1 velocity |

---

## Design Gate

**Design Gate Required: true**

⚠ DESIGN GATE REQUIRED before plan sprint.

3 stories classified as UI-facing with observable rendering/interaction ACs:
- ST-02 (BLG-FE-79): R-multiple numeric display on Reflection page
- ST-11 (BLG-FEAT-53): Strategy Benchmark page — full 3-panel page with toggle modes, filter bar, stat cards
- ST-12 (BLG-FE-80): Morning briefing expand/collapse with localStorage state persistence

**Required next step:** `run design-gate --cycle 2026-06-26__release-v6.3`

---

## Carry-Forward Advisories (from v6.2 closure)

| ID | Description | Owner | Action |
|----|-------------|-------|--------|
| FI-P3-01 | Add Playwright strict mode advisory to Base44 prompt draft §6 (2nd occurrence — template change required) | Director of Quality | Action during v6.3 sprint execution |
| FI-P3-02 | Clarify frontend testing gate: code review vs staging sign-off criteria for wording-only vs visual ACs | Head of Specs Team | Action during v6.3 sprint execution |
| FI-P4-01 | Add CI/infrastructure spec_references convention to execution_prompt.md §3.1.A | Head of Specs Team | Action during v6.3 sprint execution |

---

## Phasing Recommendation

| Phase | EPICs | Effort | Rationale |
|-------|-------|--------|-----------|
| Sprint 1 | EPIC-01 (firm) + EPIC-02 (firm) + EPIC-01/02 conditionals if capacity | ~3.5d firm + up to 1.75d conditional | P1 correctness + P1 security + P1 test infrastructure. All independent. Leaves substantial runway for conditional items. |
| Sprint 2 | EPIC-03 (BLG-FEAT-53 + BLG-FE-80) + EPIC-03 conditionals if capacity | ~5.5d firm + up to 1.0d conditional | Strategy Benchmark page leads Sprint 2. BLG-FE-80 (0.5d) pairs cleanly. Conditional ops items fill remaining capacity. |

---

## Outstanding Actions Before Sprint Planning

| Action | Owner | Blocking? |
|--------|-------|-----------|
| Run design gate | Head of UX & Design | YES — hard gate at sprint planning STEP -1.3 |
| Update BLG-BE-39 and BLG-FE-79 Provisional-Target from `v6.2` → `v6.3` in backlog.md | Product Owner | No — advisory |
| BLG-OPS-79 architecture review before ST-13 implementation | Infrastructure & Operations Owner | No — advisory at release planning; confirmed at sprint planning |
| Action carry-forward items FI-P3-01, FI-P3-02, FI-P4-01 | Director of Quality / Head of Specs Team | No — during sprint execution |

---

## Recommended Next Action

Run: `run design-gate --cycle 2026-06-26__release-v6.3`

Then: `plan sprint --cycle 2026-06-26__release-v6.3`
