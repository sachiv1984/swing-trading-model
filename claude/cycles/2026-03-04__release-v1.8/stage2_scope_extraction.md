
**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-04
**Cycle:** 2026-03-04__release-v1.8

---

# Stage 2 — Scope Extraction

## Release: v1.8 — Risk Dashboard

> **Constraint:** This engine may not add, replace, defer, or kill roadmap initiatives. Scope items are extracted from the approved roadmap and the backlog pool authorised for v1.8 by DL-005 (Roadmap Rebalance 2026-03-04__item-3.4).

---

## 2.1 Primary Roadmap Scope

### S2-01 — Risk Dashboard Page
**Source:** `current_roadmap.md` §3.4
**Status:** Planned → In scope for v1.8
**Effort:** Medium (3–4 days)
**Value:** High — daily risk visibility for active trader

**Scope items (from roadmap):**
- Portfolio Heat Gauge — total capital at risk across open positions as % of portfolio value
- Current Drawdown summary — from peak equity, days underwater
- Grace Period status panel — positions in grace period with days remaining
- Position-level risk table — stop distance, ATR, position state (GRACE / LOSING / PROFITABLE) per open position
- Prospective heat indicator — integration with Position Sizing Calculator to show heat impact before entry

**Data dependencies:**
- `GET /portfolio` — positions, heat calculation, grace period data
- `GET /analytics/metrics` — drawdown, peak equity
- Portfolio Heat formula: canonical in `metrics_definitions.md` v1.6.0 ✅
- No new backend data dependencies confirmed by roadmap

**Constraints:**
- Frontend spec must be produced by Design Gate Engine (Phase 1.5) before Sprint Planning opens
- Heat endpoint: confirm whether `GET /portfolio` response already includes `portfolio_heat_percent` or whether a dedicated calculation call is needed (to be resolved in pre-alignment)

---

## 2.2 Backlog Pool — v1.8 Candidates (DL-005)

**Selection criteria applied:**
1. P1 items: included unless dependency or effort precludes v1.8 timebox
2. P2 items: included if effort ≤ 1 day and no unresolved blocker
3. Items with unresolved decisions: include with conditional gate notation
4. Items deferred: listed with rationale

### Included in v1.8 Scope

**S2-02 — Golden Output Regression Baseline for CI**
**Source:** BLG-NEW-01
**Priority:** P1
**Effort:** ~1 day
**Rationale:** Foundational quality gate. Stop/sizing calculation integrity directly underpins the Risk Dashboard correctness. Included in v1.8 as a quality pre-requisite.
**Constraint:** Golden values must be derived from canonical `strategy_rules.md` spec, not from implementation.

**S2-03 — Backtest vs Live Stop Reconciliation Report**
**Source:** BLG-NEW-02
**Priority:** P1
**Effort:** ~0.5 day
**Dependency:** Must follow S2-02 (BLG-NEW-01 golden baseline must exist first)
**Rationale:** Prevents silent divergence between backtest and live stop logic. CI assertion only; no UI surface.

**S2-04 — Dependency Vulnerability Scanning in CI**
**Source:** BLG-NEW-05
**Priority:** P1
**Effort:** ~0.5 day
**Rationale:** Security hygiene; 0.5-day CI step. No dependencies. Include.

**S2-05 — Automated OpenAPI Drift Detection in CI**
**Source:** BLG-NEW-08
**Priority:** P1
**Effort:** ~0.5 day
**Rationale:** Prevents recurrence of BLG-SPEC-D7 (openapi.yaml drift). CI gate. Include alongside S2-07.

**S2-06 — Settings Endpoint Method Drift Resolution**
**Source:** BLG-SPEC-D2
**Priority:** P1
**Effort:** ~0.5 day (spec update); potentially more if option (b) chosen
**Condition:** Requires Product Owner + API Contracts owner decision on option (a) vs (b) before execution can begin.
**Included:** Yes — EPIC-03. Execution is gated on that decision. Conditional gate recorded in escalations.

**S2-07 — Update openapi.yaml to v1.9.0**
**Source:** BLG-SPEC-D7
**Priority:** P2
**Effort:** ~1 day
**Rationale:** P2 spec debt directly related to CI gate (S2-05). Include together.

**S2-08 — Running API Changelog Document**
**Source:** BLG-NEW-07
**Priority:** P1
**Effort:** ~0.5 day
**Rationale:** Governance documentation; low effort, high governance value. Include.

**S2-09 — Unavailability Failure Mode Documentation**
**Source:** BLG-NEW-03
**Priority:** P1
**Effort:** ~0.5 day
**Rationale:** Operational safety documentation. P1 designation. Include.

---

### Deferred from v1.8 (to v1.9 or later)

| ID | Title | Priority | Deferral Rationale |
|----|-------|----------|--------------------|
| BLG-NEW-04 | AI-Assisted Workflow Governance Policy | P2 | P2 governance doc; lower urgency than P1 items. Defer to v1.9 governance bundle. |
| BLG-SPEC-D3 | GET /market/status undocumented | P2 | Effort competes with higher-priority CI items. Defer to v1.9 spec debt wave. |
| BLG-SPEC-D1 | API Contracts README version frozen | P3 | P3 doc housekeeping. Defer. |
| BLG-SPEC-D4 | GET /positions/search/tags undocumented | P3 | P3. Defer. |
| BLG-SPEC-D8 | System_status_report.md lifecycle header | P3 | P3. Defer. |
| BLG-SPEC-D9 | process_index.md / Specs_Index.md wrong path | P3 | P3. Defer. |
| BLG-SPEC-G1 | settings_model.md missing | P2 | Blocked on D2 decision. Defer until D2 resolved. |
| BLG-SPEC-G2 | Error Response Standard not defined | P2 | Significant scope; separate initiative required. Defer to v1.9 spec wave. |
| BLG-SPEC-G3 | structured_logging_standards.md not in index | P3 | P3. Defer. |
| BLG-SPEC-G4 | ADR-002 in wrong location | P3 | P3. Defer. |
| BLG-SPEC-G5 | validation_system.md owner non-compliant | P3 | P3. Defer. |

---

## 2.3 Final v1.8 Scope Summary

| S2 ID | Title | Source | Priority | Effort est. |
|-------|-------|--------|----------|-------------|
| S2-01 | Risk Dashboard Page | Roadmap §3.4 | Primary | 3–4 days |
| S2-02 | Golden Output Regression Baseline | BLG-NEW-01 | P1 | ~1 day |
| S2-03 | Backtest vs Live Stop Reconciliation | BLG-NEW-02 | P1 | ~0.5 day |
| S2-04 | Dependency Vulnerability Scanning CI | BLG-NEW-05 | P1 | ~0.5 day |
| S2-05 | Automated OpenAPI Drift Detection CI | BLG-NEW-08 | P1 | ~0.5 day |
| S2-06 | Settings Endpoint Method Drift | BLG-SPEC-D2 | P1 | ~0.5 day* |
| S2-07 | Update openapi.yaml to v1.9.0 | BLG-SPEC-D7 | P2 | ~1 day |
| S2-08 | Running API Changelog Document | BLG-NEW-07 | P1 | ~0.5 day |
| S2-09 | Unavailability Failure Mode Documentation | BLG-NEW-03 | P1 | ~0.5 day |

*S2-06 effort contingent on Product Owner decision; execution gated.

**Total estimated effort: 7–8.5 days**

**Capacity note:** No timebox or capacity provided in invocation. Standard assumption applied: 2 weeks, solo-dev evenings. This estimate will be assessed in Stage 4.5.
