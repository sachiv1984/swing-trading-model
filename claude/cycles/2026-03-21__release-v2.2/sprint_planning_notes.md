**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-22
**Cycle:** 2026-03-21__release-v2.2

---

# Sprint Planning Notes — 2026-03-21__release-v2.2

## Backlog Slice Source

Original — `claude/cycles/2026-03-21__release-v2.2/stage4_backlog_slice.md`

No amendment file in use (`amended_backlog_slice_path` is empty in `.claude_current_state.json`).

---

## Deferred Items

No items deferred from the backlog slice. All 15 stories are included across the 3-sprint phased delivery. The over-capacity WARN is resolved by the 3-sprint phasing plan (Product Owner acceptance on record — see sprint_capacity.md).

| Item | Reason | Next Sprint Candidate? |
|------|--------|----------------------|
| (none) | — | — |

---

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-04 (Alert Threshold Customisation) | ST-03 (Alert Scheduling Design) | Internal — spec + design decision gates implementation | Must resolve before ST-04 begins |
| ST-05 (Alert History Table) | ST-03 (Alert Scheduling Design) | Internal — scheduling design confirms evaluation frequency and what to record | Must resolve before ST-05 begins |
| ST-12 (Traceability Matrix) | ST-11 (Automation Readiness) | Internal — readiness assessment confirms scope of traceability matrix | Should complete before ST-12 (same EPIC, natural ordering) |
| ST-04 | Design gate (design_gate.md) | Spec — notifications.md v0.2 locked | Cleared — notifications.md v0.2 is the locked spec reference |
| ST-05 | Design gate (design_gate.md) | Spec — notifications.md v0.2 locked | Cleared — notifications.md v0.2 is the locked spec reference |
| ST-07 (Slippage StatsCard) | Design gate (design_gate.md) | Spec — trade_history.md v1.3 locked | Cleared — trade_history.md v1.3 is the locked spec reference |
| ST-12 | ST-17 (Spec Coverage Inventory — v2.1) | External — inventory must exist before matrix is built | Cleared — ST-17 shipped v2.1 |

---

## Execution Sequence

### Sprint 1 — Security + Quick Wins + Alert Design

**Priority 1 (highest):** EPIC-01
1. ST-01 — API Key Authentication (backend middleware + frontend env-var wiring; single EPIC-01 branch, both sides in same or back-to-back PRs)
2. ST-02 — Content Security Policy Headers (can bundle with ST-01 PR or follow immediately)

**Priority 2:** EPIC-03 (independent; can run in parallel with EPIC-01)
3. ST-06 — Fix CSV Export Function Name Bug
4. ST-07 — Fix Slippage StatsCard Gradient Key
5. ST-08 — Health Check Endpoint
   *(ST-06 + ST-07 + ST-08 bundled into single EPIC-03 PR)*

**Priority 3:** EPIC-02 — ST-03 only (design decision; does not block EPIC-01 or EPIC-03)
6. ST-03 — Alert Scheduling: Define Trigger Mechanism and Rule Behaviour

### Sprint 2 — Alert Maturity + QA Coverage

**Gate: ST-03 must be complete (decisions documented, spec updated) before ST-04 or ST-05 begin**

EPIC-02:
7. ST-04 — Alert Threshold Customisation (backend schema + frontend threshold input UI; EPIC-02 branch)
8. ST-05 — Alert History Table (backend evaluation table + `GET /alerts/history` + frontend history view; EPIC-02 branch)
   *(ST-04 and ST-05 may run in parallel within EPIC-02 branch if the scheduling spec confirms independent schema changes)*

EPIC-04 (no dev dependency — can run concurrently with EPIC-02):
9. ST-11 — Test Automation Readiness Assessment (before ST-12)
10. ST-09 — Execute Notification Scenarios on Staging
11. ST-10 — Create Watchlist Test Scenarios

### Sprint 3 — Governance + QA Traceability

EPIC-04:
12. ST-12 — Spec-to-Test Traceability Matrix (after ST-11 complete)

EPIC-05 (governance items; can run concurrently with ST-12):
13. ST-13 — Roadmap Engine: Provisional-Target Field
14. ST-14 — Release Planning: scored_initiatives.md Handoff
15. ST-15 — Structured Lessons Learnt Carry-Forward Block

*(ST-13, ST-14, ST-15 are logically paired but each is an independent §6 checklist operation — sequence within Sprint 3 is at owner's discretion)*

---

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 (ST-01) | Valid — ST-01 AC covers both backend middleware and frontend env-var; DoQ must confirm no regression and no unprotected endpoint |
| RISK-02 | EPIC-02 (ST-03→ST-04/ST-05) | Valid — ST-03 AC requires a concrete scheduler decision (option selected, documented); if PO defers to v2.3, ST-04/ST-05 implementation options must be explicitly stated in ST-03 output. RISK-02 is the most critical mid-sprint dependency. |
| RISK-03 | EPIC-03 (ST-06) | Valid — AC requires regression confirmation: incorrect import name confirmed present before fix, correct after. |
| RISK-04 | EPIC-04 (ST-09) | Valid — partial execution acceptable if test data setup is infeasible for 3 open-position scenarios. Blockers must be documented per ST-09 AC-3. |
| RISK-05 | EPIC-05 (ST-13, ST-14, ST-15) | Valid — §6 checklist enforced; each story requires Head of Specs Team self-sign-off + DoQ review of prompt diffs. |

---

## Pre-Sprint Vulnerability Scan

**pip-audit not installed on this environment.** Tool is not available at `$(which pip-audit)` (command not found).

Recommendation: Install `pip-audit` before Sprint 1 execution begins (`pip install pip-audit`). The CI gate already includes pip-audit; this is a local tooling gap.

Flag: advisory — does not block sprint planning. No known CVEs from prior scan results in backlog. ST-01 (API Key Auth) is the P1 security item for this sprint; dependency vulnerability scanning is separate.

---

## Test Scenario Gap Flags (LL-v2.0-P4-2)

The following `delegated_frontend` items introduce new pages or new user-facing controls. The `test_scenarios` field for their EPICs is flagged as pending:

| Item | New UI Surface | Flag |
|------|---------------|------|
| ST-04 (Alert Threshold Customisation) | New threshold input fields on alert creation/edit UI; threshold display on alert list | `EPIC-02 test_scenarios: pending — QA & Testing Owner to author threshold customisation scenarios before Sprint 2 close or next sprint on this domain` |
| ST-05 (Alert History Table) | New alert history view (`/notifications/history`) | `EPIC-02 test_scenarios: pending — QA & Testing Owner to author alert history scenarios before Sprint 2 close or next sprint on this domain` |

These flags surface the coverage gap at planning time. QA & Testing Owner should prepare scenario files during Sprint 2 alongside ST-04/ST-05 implementation.

---

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| pip-audit: install and run before Sprint 1 execution | Head of Engineering | No (advisory) |
| QA & Testing Owner: author alert threshold customisation test scenarios | QA & Testing Owner | No (before Sprint 2 delivery verification) |
| QA & Testing Owner: author alert history test scenarios | QA & Testing Owner | No (before Sprint 2 delivery verification) |

*No outstanding actions are marked Blocker? Yes. Sprint backlog may be sealed.*
