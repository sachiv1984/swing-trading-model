**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-03-24
**Cycle:** 2026-03-24__release-v2.3
**Release:** v2.3
**Sprint Goal:** Establish a reproducible QA automation layer, deliver user-facing compliance and metrics features, and resolve all outstanding frontend polish and operational spec debt for v2.3.
**Backlog Slice Source:** Original `claude/cycles/2026-03-24__release-v2.3/stage4_backlog_slice.md`

---

# Sprint Backlog — 2026-03-24__release-v2.3

---

## Sprint 1 — Operational Readiness + QA Foundation Prerequisites + Governance Quick Win

*Estimated effort: ~5–8 days*

---

### EPIC-05 — Governance & QA Process

**Maps to:** S2-05
**Owner:** Head of Specs Team + QA Lead
**Estimated effort:** XS–S items from this EPIC in Sprint 1
**Risk IDs:** RISK-05 (GOV-08 conditional stretch — Sprint 3 only)
**Execution sequence:** 1

#### ST-14 — BLG-GOV-07: Reinforce Backend Branch Discipline

**Owner:** Head of Specs Team
**Estimated effort:** XS (<1 hour)
**Delegation class:** autonomous
**Sprint:** 1

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-14`

**Dependencies:** None

**Notes:** §6 checklist (CLAUDE.md) must be applied — version bump, OPERATIONAL_GUIDE §14, phase section header, prompt_change_log.md entry. One commit per checklist.

---

#### ST-15 — BLG-QA-03: Canonical Test Execution Report Template

**Owner:** QA Lead
**Estimated effort:** S (~0.5 day)
**Delegation class:** delegated_qa
**Sprint:** 1

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-15`

**Dependencies:** None

**Notes:** Template stored in `docs/testing/` or `docs/governance/`. Enables consistent DoQ sign-off evidence from Sprint 2 onwards.

---

### EPIC-03 — Operational Readiness & Spec Debt

**Maps to:** S2-03
**Owner:** API Contracts Owner + FinOps & Resource Architect + Infrastructure & Operations Owner
**Estimated effort:** ~1–2 days
**Risk IDs:** RISK-03 (SPEC-D14 must precede OPS-07)
**Execution sequence:** 2

#### ST-07 — BLG-SPEC-D14: Update health_endpoints.md to v1.1

**Owner:** API Contracts Documentation Owner
**Estimated effort:** XS (<1 hour)
**Delegation class:** autonomous
**Sprint:** 1

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None (but gates ST-09)

**Notes:** openapi.yaml OperationalHealthResponse schema must be updated in same commit. Commit must include both health_endpoints.md v1.1 and openapi.yaml changes.

---

#### ST-08 — BLG-OPS-09: Database Size Monitoring Alert

**Owner:** FinOps & Resource Architect + Backend Engineering
**Estimated effort:** S (~0.5 day)
**Delegation class:** delegated_backend
**Sprint:** 1

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None

**Notes:** §3 compliance: alert is notification-only, no automated cleanup. openapi.yaml updated if new endpoint or field added.

---

#### ST-09 — BLG-OPS-07: System Health Check Playbook

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Sprint:** 1

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** ST-07 (references health_endpoints.md v1.1)

**Notes:** RISK-03 mitigated by ordering ST-07 first. Playbook must reference v1.1 schema.

---

### EPIC-02 — QA Automation Foundation (Sprint 1 portion)

**Maps to:** S2-02
**Owner:** QA & Testing Owner + Infrastructure & Operations Owner
**Estimated effort (Sprint 1 items):** ~1.5–3.5 days
**Risk IDs:** RISK-02 (OPS-08 gates QA-06 + QA-05 in Sprint 2)
**Execution sequence:** 3

#### ST-03 — BLG-OPS-08: Staging Data Reset Script

**Owner:** Infrastructure & Operations Owner + Backend Engineering
**Estimated effort:** S (~0.5 day)
**Delegation class:** delegated_backend
**Sprint:** 1

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None (but gates ST-04 and ST-05 in Sprint 2)

**Notes:** RISK-02 — must complete Sprint 1. ST-04 and ST-05 are blocked until this is merged.

---

#### ST-06 — BLG-QA-01: Playwright E2E for Chart Interactivity

**Owner:** QA & Testing Owner
**Estimated effort:** M (~1–2 days)
**Delegation class:** delegated_qa
**Sprint:** 1

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None (independent of OPS-08 dependency chain)

**Notes:** Covers SC-CHART-IX-01 through SC-CHART-IX-06 (16 sub-scenarios). Run against per-PR preview URL.

---

## Sprint 2 — User Features + QA Automation Completion

*Estimated effort: ~8–13 days*

---

### EPIC-02 — QA Automation Foundation (Sprint 2 portion)

**Maps to:** S2-02
**Owner:** QA & Testing Owner + Infrastructure & Operations Owner
**Estimated effort (Sprint 2 items):** ~3 days
**Risk IDs:** RISK-02
**Execution sequence:** 1

#### ST-04 — BLG-QA-06: Test Data Seed Script Library

**Owner:** QA & Testing Owner + Backend Engineering
**Estimated effort:** S–M (~1 day)
**Delegation class:** delegated_qa
**Sprint:** 2

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** ST-03 (OPS-08 staging reset complete)

**Notes:** Seeds for alerts, watchlists, portfolio/trades. Stored in `scripts/seeds/` or equivalent.

---

#### ST-05 — BLG-QA-05: Critical-Path Smoke Test (Playwright)

**Owner:** QA & Testing Owner
**Estimated effort:** M (~2 days)
**Delegation class:** delegated_qa
**Sprint:** 2

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** ST-03 (OPS-08) + ST-04 (QA-06 seeds)

**Notes:** 3 critical paths: add trade, view portfolio, view alerts. Playwright pass = supporting evidence for non-visual AC only; visual AC remains DoQ manual review. Flaky failures advisory only.

---

### EPIC-01 — User Features: Compliance & Metrics

**Maps to:** S2-01
**Owner:** Strategy Rules & System Intent Owner + Backend Engineering + Base44 Frontend
**Estimated effort:** ~4–7 days
**Risk IDs:** RISK-01 (BLG-FEAT-11 SPS=4 sign-off required)
**Execution sequence:** 2

#### ST-01 — BLG-FEAT-11: Strategy Compliance Score (Display-Only)

**Owner:** Strategy Rules & System Intent Owner + Backend Engineering + Base44 Frontend
**Estimated effort:** M–L (~3–5 days)
**Delegation class:** delegated_frontend
**Sprint:** 2

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

**Dependencies:** None (independent of QA automation chain)

**Notes:** RISK-01 — Strategy Rules & System Intent Owner DoQ sign-off required at delivery verification. §13.3 display-only constraint must be explicitly in implementation (no automated actions). Test scenario gap flag: EPIC-01 test_scenarios pending — QA & Testing Owner to author before next sprint on this domain.

---

#### ST-02 — BLG-FEAT-09: Metrics Staleness Indicator

**Owner:** Backend Engineering + Base44 Frontend
**Estimated effort:** S–M (~1–2 days)
**Delegation class:** delegated_frontend
**Sprint:** 2

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Notes:** Indicator on analytics and portfolio pages. Design source: `docs/design/2026-03-24__release-v2.3/staleness-indicator/ux_spec.md`. Frontend spec: `docs/specs/frontend/pages/analytics.md` v1.6. Test scenario gap flag: EPIC-01 test_scenarios pending (shared with ST-01 flag above).

---

## Sprint 3 — Frontend Polish + QA Coverage + Conditional Stretch

*Estimated effort: ~5–8 days (plus ST-17 conditional)*

---

### EPIC-04 — Frontend Polish

**Maps to:** S2-04
**Owner:** Base44 Frontend Prompt Owner + Product Owner
**Estimated effort:** ~3–5 days
**Risk IDs:** RISK-04 (resolved — Product Owner design decision issued 2026-03-24)
**Execution sequence:** 1

#### ST-11 — BLG-FE-04: Alert Thresholds Empty State CTA Button

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** XS (<1 hour)
**Delegation class:** delegated_frontend
**Sprint:** 3

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None

**Notes:** Closes known deviation DEV-EPIC02-ST04-01 from `notifications.md`. Pre-approved spec: `notifications.md §Section 2` (v0.3).

---

#### ST-10 — BLG-FE-05: Alert Notification Badge in Nav

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** delegated_frontend
**Sprint:** 3

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** None

**Notes:** Design source: `docs/design/2026-03-24__release-v2.3/alert-nav-badge/ux_spec.md`. Frontend spec: `docs/specs/frontend/pages/notifications.md` v0.3 §Nav Alert Badge. Badge propagates to collapsed Tools group header (ST-13 integration). Test scenario gap flag: EPIC-04 test_scenarios pending — QA & Testing Owner to author before next sprint on this domain.

---

#### ST-12 — BLG-FE-02: Loading State Standardisation

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** M (~1–2 days)
**Delegation class:** delegated_frontend
**Sprint:** 3

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None (independent; sequenced before ST-13 to avoid nav refactor conflict)

**Notes:** Design source: `docs/design/2026-03-24__release-v2.3/loading-states/ux_spec.md`. Pattern spec: `docs/specs/frontend/patterns/loading_states.md` v1.0. Pages in scope: Portfolio, Positions, Watchlist, Alerts, Analytics.

---

#### ST-13 — BLG-UX-01: Sidebar Navigation Overflow

**Owner:** Base44 Frontend Prompt Owner
**Estimated effort:** M (~1–2 days)
**Delegation class:** delegated_frontend
**Sprint:** 3

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None (design decision resolved; RISK-04 closed)

**Notes:** Product Owner design decision: collapsible section groups — 4 groups: Trading, Analytics, Tools, System. Design source: `docs/design/2026-03-24__release-v2.3/sidebar-nav-groups/ux_spec.md`. Frontend spec: `docs/specs/frontend/pages/navigation.md` v1.0. Badge propagation to collapsed Tools group header integrates with ST-10 — ST-13 should be sequenced after ST-10 to confirm integration. Test scenario gap flag: EPIC-04 test_scenarios pending (shared with ST-10 flag above).

---

### EPIC-05 — Governance & QA Process (Sprint 3 portion)

**Maps to:** S2-05
**Owner:** Head of Specs Team + QA Lead
**Estimated effort (Sprint 3 items):** ~1–4 days (QA-04 ~1 day; GOV-08 conditional ~2–3 days)
**Risk IDs:** RISK-05 (GOV-08 conditional)
**Execution sequence:** 2

#### ST-16 — BLG-QA-04: Integration Test Coverage Report

**Owner:** QA & Testing Owner + CI Engineering
**Estimated effort:** M (~1 day)
**Delegation class:** delegated_qa
**Sprint:** 3

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-16`

**Dependencies:** None

**Notes:** CI-generated coverage report against openapi.yaml endpoints. Report format: either machine-readable or human-readable. Coverage gaps visible to DoQ during sign-off.

---

#### ST-17 — BLG-GOV-08: Engine Prompt Compression (Conditional)

**Owner:** Head of Specs Team
**Estimated effort:** L (~2–3 days)
**Delegation class:** delegated_decision
**Sprint:** 3 (conditional — executes only if residual capacity permits after ST-13 + ST-16 complete)

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-17`

**Dependencies:** ST-13 complete + ST-16 complete (Sprint 3 capacity gate)

**Notes:** RISK-05 — conditional stretch. Does not block the v2.3 release publish gate. If Sprint 3 capacity is consumed by ST-10–ST-16, ST-17 carries to v2.4. §6 checklist applies to both modified files. HoST design session recommended before Sprint 3 start to define compression criteria (LL-v2.2-SP-01 advisory).

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~18–24 days (3 sprints) |
| Total estimated effort (all 17 items incl. GOV-08) | ~15–26 days |
| Total estimated effort (GOV-08 conditional excluded) | ~13–23 days |
| Utilisation (mid-point, GOV-08 excluded) | ~75% |
| Over-allocation | No — within capacity when GOV-08 treated as conditional stretch. WARN acknowledged by Product Owner 2026-03-24. |

## Items Deferred This Sprint

None — all 17 items included. ST-17 (GOV-08) is conditional within Sprint 3 scope, not deferred.

## Deferred Execution Blockers Accepted

N/A — `deferred_execution_blockers` was empty in state.json.

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| EPIC-01 test_scenarios: QA & Testing Owner to author scenario file before next sprint on compliance/staleness domain | QA & Testing Owner | No |
| EPIC-04 test_scenarios: QA & Testing Owner to author scenario file before next sprint on alert badge / nav groups domain | QA & Testing Owner | No |
| ST-17 GOV-08: HoST design session recommended before Sprint 3 (advisory — LL-v2.2-SP-01) | Head of Specs Team | No |
| Delegation log update discipline: entries updated at merge point, not batched at sprint close | PMO Lead (Phase 3) | No |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** confirmed
**Scope confirmed:** confirmed — all 17 items in scope; ST-17 conditional stretch accepted
**Capacity confirmed:** confirmed — WARN acknowledged; GOV-08 conditional resolves upper-bound risk
**Deferred execution blockers accepted (if any):** N/A
**Signed off by:** Product Owner
**Date:** 2026-03-24
