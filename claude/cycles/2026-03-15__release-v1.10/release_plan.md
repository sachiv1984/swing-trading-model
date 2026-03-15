**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v1.10
**Cycle:** 2026-03-15__release-v1.10
**Last Updated:** 2026-03-15

---

# Release Plan — v1.10 Operations & Quality Foundation

---

## Readiness

**Release theme:** Operations & Quality Foundation — establish the staging environment (BLG-OPS-01), resolve the CohortAnalysis architecture debt (BLG-TECH-06), and build the QA test infrastructure gaps (BLG-API-01, BLG-QA-01/TEST-GAP-EPIC-06).

| Item | Source | P | Spec ready | Dependencies | Status |
|------|--------|---|------------|--------------|--------|
| BLG-OPS-01 — Dev environment | Roadmap v1.10 | P1 | N/A (infra task) | None | ✅ Ready |
| BLG-TECH-06 — Fix CohortAnalysis | Backlog | P2 | analytics.md §15; GET /analytics/cohort endpoint exists | BLG-OPS-01 (staging) | ✅ Ready |
| BLG-API-01 — Backend integration tests | Backlog | P2 | portfolio_endpoints.md; golden baseline in place | GET /portfolio in place | ✅ Ready |
| TEST-GAP-EPIC-06 — v1.7 scenario gaps | Backlog | — | verification_report.md §6 defines gaps | BLG-API-01 CI step recommended first | ✅ Ready (advisory) |

**⚠ Advisory (STEP 1.1):** TEST-GAP-EPIC-06 has been in backlog 3 release cycles without story assignment. Promoted to ST-07 in this release's backlog slice.

---

## Scope

### Items in scope

| S2-ID | Epic | Item | Effort (Lo–Hi days) |
|-------|------|------|---------------------|
| S2-01 | EPIC-01 | BLG-OPS-01 — Provision staging/dev environment | 2–4 |
| S2-02 | EPIC-02 | BLG-TECH-06 — Fix CohortAnalysis.js client-side computation | 0.5–1 |
| S2-03 | EPIC-03 | BLG-API-01 — FastAPI TestClient integration tests + CI step | 1.5–3 |
| S2-04 | EPIC-03 | TEST-GAP-EPIC-06 — Author v1.7 missing QA scenarios (BLG-QA-01) | 0.5–1 |

**Total effort range:** 4.5–9 days (mid: ~6.5 days / ~50 hrs)

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| 3.5 Alerts & Notifications | v2.0 scope; QA gate still pending | v2.0 |
| 4.1b Tax-Year P&L Statement | v2.0 scope | v2.0 |
| 4.3 Signal Exposure Enhancement | v2.0 scope; PoG POG-20260304-01 cleared | v2.0 |
| 4.2 Watchlists & Screening | P2 — do not pull forward | v2.1+ |
| Chart Interactivity | P2 — do not pull forward | v2.1+ |
| BLG-NEW-13 — Spec Coverage Inventory | v2.0 target | v2.0 |
| BLG-FEAT-03 — Slippage Tracking | v2.1 target | v2.1 |
| BLG-TECH-05 — Prometheus metrics | v2.1 target | v2.1 |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-03-15__release-v1.10

---

## Execution Plan

### EPIC Table

| EPIC-ID | Scope items | Owner | Stories | Key risk | Sequencing constraint |
|---------|-------------|-------|---------|----------|-----------------------|
| EPIC-01 | S2-01 | Infrastructure & Operations Owner | ST-01, ST-02, ST-03 | RISK-01 | Must start first — BLG-OPS-01 is P1 prerequisite |
| EPIC-02 | S2-02 | Head of Engineering | ST-04 | RISK-02 | Independent — can run parallel to any EPIC |
| EPIC-03 | S2-03, S2-04 | QA & Testing Owner | ST-05, ST-06, ST-07 | RISK-03 | S2-04 (ST-07) recommended after S2-03 CI step in place |

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | Staging environment scope ambiguity — "provision an environment" could mean simple same-server port, separate cloud service, or Docker compose. Unconstrained scope risks over-engineering or under-delivery. | Medium | Constrain to simplest viable approach: same host, different port or subdomain, tracking main. Infrastructure & Operations Owner decides approach at STEP 0 of sprint. | null |
| RISK-02 | EPIC-02 | CohortAnalysis refactor regression — refactoring from client-side to backend endpoint may produce output differences if server response field names differ from buildCohorts() output shape. | Medium | Acceptance criteria require explicit regression check: period toggle and table display output must match pre-refactor behaviour. QA sign-off required before merge. | null |
| RISK-03 | EPIC-03 | Integration test database dependency — TestClient tests must be CI-safe (no live DB). If the endpoint implementation has unresolvable hard DB dependencies, fixture injection may be complex. | Low | Acceptance criteria explicitly require CI-safe design (dependency override or in-memory SQLite). Director of Quality confirms CI step present and passing. | null |

---

## Capacity Check

**Effort summary:**
- ST-01 (Provision environment): 1–2 days (mid: 1.5d = 12 hrs)
- ST-02 (CI/CD pipeline): 0.5–1 day (mid: 0.75d = 6 hrs)
- ST-03 (Governance update): 0.25 day (mid: 2 hrs)
- ST-04 (CohortAnalysis refactor): 0.5–1 day (mid: 0.75d = 6 hrs)
- ST-05 (Integration tests): 1–2 days (mid: 1.5d = 12 hrs)
- ST-06 (CI step for tests): 0.5 day (mid: 4 hrs)
- ST-07 (QA scenarios): 0.5–1 day (mid: 0.75d = 6 hrs)

**Total mid estimate:** ~6.5 days / ~48 hrs

**Capacity assumption:** No `--capacity` specified. Using prior cycle standard: solo developer, mixed intensity (evenings + weekends ≈ 15–20 hrs/week; full-time sprint ≈ 35–40 hrs/week).

- At full-time: ~48 hrs ÷ 35 hrs/week = ~1.4 weeks. **PASS** within a single 2-week sprint.
- At evenings: ~48 hrs ÷ 17 hrs/week = ~2.8 weeks. Manageable in standard solo cycle.

**Outcome: WARN** — no capacity parameter specified; estimate is feasible under full-time assumption but could stretch under evenings-only mode. Phasing recommendation provided below.

### Phasing Recommendation

Since no capacity was specified, sprint planning may adopt a single sprint (if full-time) or two phased sprints (if evenings/part-time):

**Phase 1 (Sprint 1 — recommended if phasing):** EPIC-01 (ST-01, ST-02, ST-03) — estimated 20 hrs (mid). Delivers the P1 prerequisite (staging environment) first. Outcome: governance gap resolved; QA can run pre-merge.

**Phase 2 (Sprint 2 — if needed):** EPIC-02 + EPIC-03 (ST-04 through ST-07) — estimated 28 hrs (mid). Delivers quality and test improvements on top of the staging foundation.

**Ordering rationale:** EPIC-01 is the P1 item and the LL-01 lesson from cycle 2026-03-15__item-5.3 requires it to enter v1.10 as Prerequisite item, not a peer feature. If capacity forces phasing, it must ship in Sprint 1.

---

## Integrity Validation — 3.5 Local Model Integrity

| Check | Result | Notes |
|-------|--------|-------|
| All scope items have S2-IDs | ✅ PASS | S2-01–S2-04 |
| All EPICs have IDs and Maps-to | ✅ PASS | EPIC-01→S2-01, EPIC-02→S2-02, EPIC-03→S2-03+S2-04 |
| All risks have IDs and EPIC references | ✅ PASS | RISK-01→EPIC-01, RISK-02→EPIC-02, RISK-03→EPIC-03 |
| All risks have escalation_ref field | ✅ PASS | All null (no escalations raised) |
| All stories covered by EPICs | ✅ PASS | ST-01–07 distributed across 3 EPICs |
| §13 strategy boundary check | ✅ PASS | No new features; all items are infrastructure, refactoring, or QA — no strategy boundary interaction |
| Roadmap scope compliance | ✅ PASS | No scope additions; all items are pre-approved backlog/roadmap items |
| Spec pre-conditions | ✅ PASS | All 4 scope items have their pre-conditions met |

**Model integrity: PASS — plan_executable = true**

---

## Integrity Validation — 5.5 Cross-Stage Integrity

| Check | Result | Notes |
|-------|--------|-------|
| S2-01 → EPIC-01 → ST-01,ST-02,ST-03 | ✅ | Chain complete |
| S2-02 → EPIC-02 → ST-04 | ✅ | Chain complete |
| S2-03 → EPIC-03 → ST-05,ST-06 | ✅ | Chain complete |
| S2-04 → EPIC-03 → ST-07 | ✅ | Chain complete |
| All backlog slice EPIC IDs match plan EPIC IDs | ✅ | EPIC-01, EPIC-02, EPIC-03 |
| No free-text EPICs in backlog slice | ✅ | All reference EPIC-xx IDs |
| Risk register complete (all EPICs have risk entry) | ✅ | RISK-01/02/03 cover all EPICs |
| Scope document present | ✅ | docs/product/scope/scope--2026-03-15__release-v1.10-operations-quality.md |
| Decisions record present | ✅ | docs/product/decisions/decisions--2026-03-15__release-v1.10.md |
| Backlog marker present | ✅ | RP:v1.10:2026-03-15__release-v1.10 |
| Roadmap annotation present | ✅ | RA:v1.10:2026-03-15__release-v1.10 |

**Cross-stage integrity: PASS**

---

## Integrity Validation — 5.7 Decision Record Integrity

No Accepted Risk escalations raised. No typed decision records (AR/SRB) required.

**Decision record integrity: NOT_APPLICABLE**
