**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-04
**Cycle:** 2026-03-04__release-v1.8

---

# Stage 1 — Release Readiness Validation

## Release: v1.8 — Risk Dashboard

---

## 1.1 Roadmap Confirmation

| Check | Status | Evidence |
|-------|--------|----------|
| v1.8 listed on `current_roadmap.md` | ✅ Pass | §3.4 Risk Dashboard, Status: Planned |
| Release theme confirmed | ✅ Pass | "Risk Dashboard — Full risk page — heat, drawdown, grace period, position-level risk" |
| No scope change required | ✅ Pass | Roadmap item predates this engine run |

---

## 1.2 v1.7 Pre-Conditions for v1.8

The roadmap specifies one v1.8 pre-condition:

> **Pre-requisite:** Metrics Definitions (Portfolio Heat formula and thresholds) must be canonical before pre-alignment opens *(v1.7 gate)*

| Pre-condition | Status | Evidence |
|--------------|--------|----------|
| Portfolio Heat formula canonical in `metrics_definitions.md` | ✅ CLEARED | `docs/specs/metrics_definitions.md` v1.6.0 — §Portfolio Heat (line 505) and §Portfolio Heat Display Thresholds (line 540). Formula and all four thresholds present. Delivered in v1.7 EPIC-03. |

---

## 1.3 Strategy Boundary Check

| Check | Status | Notes |
|-------|--------|-------|
| `strategy_rules.md` version | ✅ v1.3 | Active, no amendments since v1.7 |
| PoG POG-20260304-01 stale condition | ✅ Not stale | POG stales if `strategy_rules.md` incremented past v1.3; currently at v1.3 |
| v1.8 scope (Risk Dashboard) — §13 boundary | ✅ No conflict | Risk Dashboard reads existing position/analytics data. No new parameters, no strategy-execution exposure. No §13 review required. |

---

## 1.4 Prior Cycle State

| Check | Status | Evidence |
|-------|--------|----------|
| Prior cycle (`2026-03-02__release-v1.7`) | ✅ Closed / Complete | `.claude_current_state.json` prior_cycle field |
| No open escalations carried forward | ✅ Confirmed | Current state: no deferred execution blockers from v1.7 |
| Backlog lock free | ✅ Pass | `claude/backlog/.lock` does not exist |

---

## 1.5 Frontend Spec Readiness

| Item | Status | Notes |
|------|--------|-------|
| `docs/specs/frontend/pages/` — Risk Dashboard spec | ⚠️ Not present | No `risk_dashboard.md` exists. Design Gate Engine (Phase 1.5) will create this before Sprint Planning. This is expected at Release Planning stage. |

> **Note (Facilitator):** Absence of the frontend spec at Release Planning is expected and normal. The Design Gate Engine runs after this plan is published and before Sprint Planning. EPIC-01 acceptance criteria must reference the Design Gate artefact, not a pre-existing spec.

---

## 1.6 Open Backlog Items Eligible for v1.8

The following items in `claude/backlog/backlog.md` are explicitly tagged for v1.8 competition (per DL-005, Roadmap Rebalance 2026-03-04__item-3.4):

| ID | Title | Priority | Effort |
|----|-------|----------|--------|
| BLG-NEW-01 | Golden Output Regression Baseline for CI | P1 | ~1 day |
| BLG-NEW-02 | Backtest vs Live Stop Reconciliation Report | P1 | ~0.5 day |
| BLG-NEW-03 | Define and Document Unavailability Failure Mode | P1 | ~0.5 day |
| BLG-NEW-04 | AI-Assisted Workflow Governance Policy | P2 | ~0.5 day |
| BLG-NEW-05 | Dependency Vulnerability Scanning in CI | P1 | ~0.5 day |
| BLG-NEW-07 | Running API Changelog Document | P1 | ~0.5 day |
| BLG-NEW-08 | Automated OpenAPI Drift Detection in CI | P1 | ~0.5 day |

Additionally eligible (P1/P2 spec debt, pre-existing):

| ID | Title | Priority | Effort |
|----|-------|----------|--------|
| BLG-SPEC-D2 | Settings endpoint method drift (P1 — decision required) | P1 | ~0.5 day |
| BLG-SPEC-D7 | openapi.yaml frozen at v1.8.1 (P2) | P2 | ~1 day |
| BLG-SPEC-D3 | GET /market/status undocumented (P2) | P2 | ~0.5 day |

---

## 1.7 Readiness Verdict

| Gate | Result |
|------|--------|
| v1.8 on roadmap | ✅ Pass |
| v1.7 pre-conditions cleared | ✅ Pass |
| Strategy boundary clear | ✅ Pass |
| No blocking prior-cycle escalations | ✅ Pass |
| Frontend spec absence | ⚠️ Expected — Design Gate Engine responsibility |

**Stage 1 Result: PASS** (frontend spec absence is expected at this stage; flagged advisory only)
