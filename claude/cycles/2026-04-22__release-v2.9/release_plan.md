Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v2.9
Cycle: 2026-04-22__release-v2.9
Last Updated: 2026-04-22

---

# Release Plan — v2.9 Arc 1 Foundation

## Readiness

| Check | Outcome | Notes |
|-------|---------|-------|
| Velocity (v2.8) | 1.00 | Rolling 6-cycle avg: 0.99 |
| Backlog age advisory | ⚠ 2 items | BLG-FEAT-13 (2 cycles no ST), BLG-GOV-08 (5 deferrals — retirement review) |
| Provisional-Target: v2.9 candidates | ℹ 20 items | 15 in scope, 5 deferred |
| Design dependency scan | ✅ 0 | BLG-FE-17 is the design work itself |
| Prior cycle post-ship | PASS | post_ship_complete=true, next_cycle_unblocked=true |

---

## Scope

**Theme:** Arc 1 Foundation — Spec, Governance, QA Infrastructure, and first Arc 1 implementations (DS-03, DS-05, DS-06).

| S2-ID | Item | Priority | Effort | Epic |
|-------|------|----------|--------|------|
| S2-01 | DS-03 — Sector & Industry Classification | Roadmap | S | EPIC-02 |
| S2-02 | DS-05 — Alpaca US Market Data Integration | Roadmap | M | EPIC-02 |
| S2-03 | DS-06 — Alpaca News Panel | Roadmap | S | EPIC-02 |
| S2-04 | BLG-SPEC-21 — Screener results schema spec | P1 | S | EPIC-01 |
| S2-05 | BLG-SPEC-22 — Alpaca API integration contract | P1 | S | EPIC-01 |
| S2-06 | BLG-SPEC-23 — Screener internal API contract | P1 | S | EPIC-01 |
| S2-07 | BLG-FE-17 — Screener results page UX spec | P1 | M | EPIC-01 |
| S2-08 | BLG-GOV-16 — §13 review record for DS-06 | P1 | S | EPIC-03 |
| S2-09 | BLG-QA-08 — External API mock harness for CI | P1 | M | EPIC-03 |
| S2-10 | BLG-QA-09 — Screener test data library | P1 | M | EPIC-03 |
| S2-11 | BLG-GOV-14 — execution_prompt.md §3.2 patches | P2 | S | EPIC-04 |
| S2-12 | BLG-GOV-15 — execution_prompt.md STEP 5.1.B | P2 | S | EPIC-04 |
| S2-13 | BLG-FE-15 — SystemStatus.js /ai prefix fix | P3 | S | EPIC-04 |
| S2-14 | BLG-AI-01 — AI Journal summary audit log | P2 | S | EPIC-04 |
| S2-15 | TEST-GAP-EPIC-04 — AI Journal test coverage | P3 | S | EPIC-04 |

**Explicitly deferred:**

| Item | Reason | Target |
|------|--------|--------|
| DS-01 — Strategy-Rules Screener Engine | Requires BLG-SPEC-21/23 specs (in this sprint) as prerequisites; H effort | v3.0 |
| DS-02 — Screener Results Page | Requires DS-01 + BLG-FE-17; defer until DS-01 ships | v3.0 |
| DS-04 — Earnings Calendar Integration | M effort; no blocking dependency; defer to keep scope manageable | v3.0 |
| DS-07 — Watchlist Promotion Flow | Depends on DS-02 | v3.0 |
| BLG-GOV-08 — Engine prompt compression | 5 consecutive deferrals; retirement review triggered; recommend retire at next groom | Retire |
| BLG-GOV-11 — Cycle artefact inventory | P3, M effort; deferred again pending Arc 1 focus | v3.0 |
| BLG-FEAT-13 — Feature flag rollout | P3, M effort; no Arc 1 dependency | v3.0 |
| BLG-FEAT-18 — Consecutive losing streak metric | P2, S; not Arc 1 prerequisite | v3.0 |
| BLG-FEAT-19 — Monthly P&L summary | P2, S; not Arc 1 prerequisite | v3.0 |
| BLG-OPS-12 — External API health check | P2, S; useful but defer to keep scope | v3.0 |
| BLG-FE-16 — React component inventory | P3, M; useful Arc 1 reference but deferrable | v3.0 |
| BLG-AI-02 — Model version contract | P3, S; BLG-AI-01 (in scope) covers the urgent gap | v3.0 |
| BLG-SPEC-20 — Spec front-matter standard | P3, S; apply inline when creating Arc 1 specs | v3.0 |

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-04, S2-05, S2-06, S2-07 | Head of Specs Team + Frontend Specs Owner | RISK-01 | Sprint 1; before EPIC-02 |
| EPIC-02 | S2-01, S2-02, S2-03 | Backend Engineering Patterns Owner | RISK-02 | Sprint 2; DS-05 after EPIC-01 S2-05; DS-06 after EPIC-03 S2-08 |
| EPIC-03 | S2-08, S2-09, S2-10 | Strategy Rules Owner + Director of Quality | RISK-04 | Sprint 1; S2-08 before EPIC-02 S2-03 |
| EPIC-04 | S2-11, S2-12, S2-13, S2-14, S2-15 | Head of Specs Team + Backend | — | ST-11/12/13 Sprint 1; ST-14/15 Sprint 2 |

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01, EPIC-02 | BLG-SPEC-22 (Alpaca API contract) authoring may reveal constraints that affect DS-05 scope or endpoint choices | High | Author BLG-SPEC-22 (ST-02) in Sprint 1 before DS-05 (ST-06) is scheduled; ST-06 ACs must reference the contract | null |
| RISK-02 | EPIC-02, EPIC-03 | BLG-GOV-16 §13 review may add display-only scope conditions to DS-06 that require ST-07 AC updates | Medium | BLG-GOV-16 (ST-08) in Sprint 1; DS-06 (ST-07) in Sprint 2 with condition-aware ACs drawn from sign-off | null |
| RISK-03 | EPIC-02 | Alpaca API may change between contract authoring (ST-02) and implementation (ST-06) | Low | Pin API version in BLG-SPEC-22; document version in ST-06 ACs | null |
| RISK-04 | EPIC-03 | External API mock harness complexity may exceed M estimate if Alpaca API response shapes are complex | Low | Scope BLG-QA-08 to request/response mocking only; defer auth flow testing to v3.0 | null |

---

## Integrity Validation — 3.5 Local Model Integrity

| Check | Result |
|-------|--------|
| All S2 items map to exactly one EPIC | PASS — 15 items, 4 EPICs, no orphans |
| All EPICs have S2 mappings | PASS |
| Dependency flow correct | PASS — EPIC-01 precedes EPIC-02 (DS-05/06); EPIC-03 S2-08 precedes EPIC-02 S2-03 |
| No circular dependencies | PASS |
| All RISKs have EPIC references | PASS |
| S2 IDs are stable and unique | PASS |

**Status: PASS** — plan_executable = true

---

## Capacity Check

**Effort summary (no scored_initiatives.md data; inline estimates used):**

| Sprint | Stories | S items | M items | Est. effort |
|--------|---------|---------|---------|-------------|
| Sprint 1 | 10 | 7 | 3 | ~9.75 days |
| Sprint 2 | 5 | 4 | 1 | ~4.5 days |
| **Total** | **15** | **11** | **4** | **~14.25 days** |

No H or L effort items. Velocity reference: 0.99 (6-cycle avg). Prior releases at 15 stories: v2.6 (1.00 velocity), v2.3 (0.94 velocity). This scope is within the demonstrated delivery range.

No --capacity specified. Default assumption: consistent with prior release cadence.

**Status: PASS** — capacity_feasible = pass

---

## Integrity Validation — 5.5 Cross-Stage Integrity

| Check | Result |
|-------|--------|
| All S2 items assigned to ST stories (stage4_backlog_slice.md) | PASS — 15 S2 → 15 ST |
| All EPICs reference S2 IDs | PASS |
| All ST stories reference source backlog/roadmap items | PASS |
| Sprint assignment respects sequencing (EPIC-01 Sprint 1, EPIC-02 Sprint 2) | PASS |
| Backlog marker present in backlog.md | PASS |
| Roadmap annotation marker present | PASS |

**Status: PASS** — cross_stage_integrity = pass

---

## Integrity Validation — 5.7 Decision Record Integrity

`docs/product/decisions/decisions--2026-04-22__release-v2.9.md` created. No accepted risk escalations (no open escalations this cycle).

**Status: PASS (not_applicable for accepted risks)** — decisions_validated = pass
