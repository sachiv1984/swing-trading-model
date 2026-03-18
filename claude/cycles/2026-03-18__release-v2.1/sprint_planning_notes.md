**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-18
**Cycle:** 2026-03-18__release-v2.1
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Sprint Planning Notes — 2026-03-18__release-v2.1

## Backlog Slice Source

Original — `claude/cycles/2026-03-18__release-v2.1/stage4_backlog_slice.md`
No amendment file in effect (`amended_backlog_slice_path` = "").

---

## Deferred Items

No items deferred from the release scope. All 19 stories included across 3 sprints.

| Item | Sprint | Status |
|------|--------|--------|
| ST-10 (Watchlist frontend) | Sprint 3 / stretch → Sprint 4 | Included as stretch; may defer to Sprint 4 if Sprint 3 runs long. Product Owner accepts. |

Items explicitly deferred at **release planning** (not sprint planning — recorded here for traceability):

| Item | Reason | Target |
|------|--------|--------|
| BLG-TECH-05 Prometheus | P3, below priority threshold | v2.2 |
| BLG-GOV-03/04/05/06 | Governance improvements | v2.2 |

---

## Capacity WARN Acknowledgement

**Outcome:** WARN — 3-sprint release; ~129 hrs mid vs ~120 hrs capacity.
**Product Owner acknowledgement (2026-03-18):** Explicitly accepted. Phasing plan adopted. Sprint 3 stretch (ST-10) may defer to Sprint 4 without blocking release — ST-09 (backend) is the delivery prerequisite for watchlist feature acceptance.

---

## Pre-Sprint Required Decision — RISK-01 (standard mode — outstanding action)

**Decision:** BLG-TECH-08 ADR (ST-01) must be marked Complete with Head of Engineering sign-off before any EPIC-02 story (ST-02–ST-07) can be sealed in the sprint backlog.

**Status at sprint planning time:** ST-01 not yet started (sprint execution has not begun).

**Standard mode handling:** EPIC-02 stories (ST-02–ST-07) are included in the sprint backlog for Sprint 2/3 with an explicit **conditional seal status**. They may not be sealed by the Execution Engine until ST-01 is confirmed Complete with Head of Engineering sign-off. This condition is recorded in the sprint backlog and must be verified by the PMO Lead before any EPIC-02 story execution begins.

---

## Dependency Map

| Item | Depends On | Dependency Type | Status |
|------|-----------|-----------------|--------|
| ST-02 (Alerts spec) | ST-01 (ADR Complete + HoE sign-off) | Hard gate | ⚠ Pending — RISK-01 |
| ST-03 (Alert rules engine) | ST-02 (spec signed off) | Internal spec gate | Resolvable during Sprint 2 |
| ST-04 (Notification delivery) | ST-01 (architecture decision), ST-02 (spec) | Hard gate (two) | ⚠ Pending — RISK-01 + ST-02 |
| ST-05 (Notification preferences FE) | ST-02 (preference model defined in spec) | Internal spec gate | Resolvable during Sprint 2/3 |
| ST-06 (In-app notification feed) | ST-02 (notification feed schema) | Internal spec gate | Resolvable during Sprint 2/3 |
| ST-07 (QA notification scenarios) | ST-03, ST-04, ST-05, ST-06 implementation | Sequential completion | Sprint 3 close |
| ST-09 (Watchlist backend) | ST-08 (spec + data model signed off) | Internal spec gate | Resolvable during Sprint 3 |
| ST-10 (Watchlist frontend) | ST-08 (spec), ST-09 (backend live in staging) | Internal + staging gate | Sprint 3 / stretch |
| ST-12 (PDF export BE+FE) | ST-12 is self-contained | None | — |
| ST-14 (Slippage tracking) | data_model.md Fill Price spec (within ST-14 scope) | Internal spec gate — embedded in story | Self-resolving within ST-14 |
| ST-17 (BLG-SPEC-G6) | analytics_endpoints.md update | Internal spec work | Within ST-17 scope |

**No circular dependencies detected.**

---

## Execution Sequence

### Sprint 1 (target: ~39 hrs mid)

**Execution order:**

1. **ST-01** — BLG-TECH-08 ADR (must be first; unlocks EPIC-02)
2. **ST-11** — Chart Interactivity (CHART-IX) [independent, quick win]
3. **ST-12** — PDF Export backend + frontend [independent]
4. **ST-16** — Bulk lifecycle header remediation [parallel track]
5. **ST-17** — Spec maintenance batch (D13, G6, D10, D11) [parallel track]
6. **ST-18** — Test scenario docs (signals + reports) [parallel track]
7. **ST-19** — Cross-EPIC branch compliance check [sprint close gate — PMO Lead reviews commit history at sprint close]

**Sprint 1 gate:** ST-01 must be Complete with Head of Engineering sign-off before Sprint 2 opens.

### Sprint 2 (target: ~37 hrs mid; conditional on ST-01 Complete)

**Execution order:**

1. Verify ST-01 Complete — PMO Lead confirms Head of Engineering sign-off recorded
2. **ST-02** — Alerts endpoint spec (gates ST-03, ST-04, ST-05, ST-06)
3. **ST-03** — Alert rules engine backend
4. **ST-13** — CSV export [independent, complete EPIC-05]
5. **ST-15** — Render PR preview environments [independent]
6. **ST-14** — Slippage tracking (data model spec embedded in story — Data Model Owner + Head of Specs Team sign-off required before implementation begins)
7. ST-04/05 as **stretch** if Sprint 2 bandwidth allows

### Sprint 3 (target: ~43 hrs core / ~53 hrs with ST-10 stretch; conditional on ST-02 signed off)

**Execution order:**

1. Verify ST-02 Complete — Head of Specs Team sign-off confirmed
2. **ST-04** — Notification delivery (email) backend
3. **ST-05** — Notification preferences frontend
4. **ST-06** — In-app notification feed frontend
5. **ST-08** — Watchlist spec + data model (can start parallel to ST-04/05)
6. **ST-09** — Watchlist backend (gates ST-10)
7. **ST-07** — QA: notification delivery test scenarios [after ST-04/05/06 complete]
8. **ST-10** — Watchlist frontend [stretch — requires ST-09 backend live in staging]

---

## Risk Flags

| RISK-ID | Associated Items | Description | Mitigation Status |
|---------|-----------------|-------------|------------------|
| RISK-01 | EPIC-01, EPIC-02 | BLG-TECH-08 ADR not authored — EPIC-02 cannot proceed | Mitigation: ST-01 first in Sprint 1; conditional seal gate on all EPIC-02 stories |
| RISK-02 | EPIC-02 | EPIC-02 large effort (~47 hrs mid) | Mitigation: phasing plan adopted; Sprint 2–3 allocation; stretch policy for ST-04/05 in Sprint 2 |
| RISK-03 | EPIC-03 | Watchlists requires new data model tables | Mitigation: ST-08 is first EPIC-03 story; gates ST-09/10 |
| RISK-04 | EPIC-04 | Chart Interactivity scope boundary — no client-side re-derivation | Mitigation: scope constraint in AC and design artefact; enforced at code review + DoQ sign-off |
| RISK-05 | EPIC-05 | BLG-FEAT-03 requires Fill Price field in data model | Mitigation: ST-14 scoped as spec + implementation; embedded gate in AC |

All risk mitigations are valid as of sprint planning date. No risks have materialised.

---

## Pre-Sprint Vulnerability Scan

pip-audit not available in execution environment. **Recommendation:** Install pip-audit (`pip install pip-audit`) before sprint execution begins. Run `pip-audit -r backend/requirements.txt` before first commit to an exec branch to ensure no known high/critical CVEs in dependencies.

Pre-sprint pip-audit: **tool unavailable — flag for installation before execution**.

---

## Test Scenario Gap Flags (LL-v2.0-P4-2)

Per sprint planning prompt §3.1, delegated_frontend items introducing new pages or new user-facing controls are flagged for QA & Testing Owner to author test scenario documents before sprint close on that domain.

| EPIC | Items introducing new pages/controls | Existing scenario coverage | Gap flag |
|------|--------------------------------------|---------------------------|----------|
| EPIC-02 | ST-05 (notifications pref page), ST-06 (notification feed page) | ST-07 covers full notification feature | ⚠ ST-07 must be authored before Sprint 3 closes on EPIC-02. Flag: EPIC-02 test_scenarios = pending authoring (ST-07 is the vehicle) |
| EPIC-03 | ST-10 (watchlist page) | None | ⚠ EPIC-03 test_scenarios = pending. QA & Testing Owner to author watchlist_scenarios.md before Sprint 3 closes on EPIC-03 |
| EPIC-04 | ST-11 (new interactions: tooltip, zoom, drill-down) | None | ⚠ EPIC-04 test_scenarios = pending. QA & Testing Owner to author chart_interactivity_scenarios.md before Sprint 1 closes on EPIC-04 |
| EPIC-05 | ST-12 (PDF download control), ST-14 (slippage column) | ST-18 covers signals + reports (existing). Slippage and PDF UI interactions not covered. | ⚠ EPIC-05 (slippage, PDF) test_scenarios = pending. QA & Testing Owner to author coverage for slippage display and PDF export UX before Sprint 2/3 closes on these items |

These flags are surfaced at planning time. QA & Testing Owner must act before the respective sprint closes. Director of Quality has been notified.

---

## Outstanding Actions

| Action | Owner | Blocker? | Required Before |
|--------|-------|----------|-----------------|
| RISK-01: ST-01 (BLG-TECH-08 ADR) must be Complete with Head of Engineering sign-off before EPIC-02 stories (ST-02–ST-07) are sealed | Head of Engineering + Backend Engineering Patterns Owner | Yes — EPIC-02 seal | Sprint 2 EPIC-02 execution |
| pip-audit: install pip-audit before sprint execution begins | Head of Engineering | No | Before first exec branch commit |
| EPIC-04 test scenarios (chart_interactivity_scenarios.md) | QA & Testing Owner | Yes — Sprint 1 EPIC-04 close | Sprint 1 close on EPIC-04 |
| EPIC-03 test scenarios (watchlist_scenarios.md) | QA & Testing Owner | Yes — Sprint 3 EPIC-03 close | Sprint 3 close on EPIC-03 |
| EPIC-05 slippage + PDF export test scenarios | QA & Testing Owner | Yes — Sprint 2/3 EPIC-05 close | Before respective sprint closes |
| ST-14 data_model.md Fill Price spec: Data Model Owner + Head of Specs Team sign-off required before implementation | Data Model & Domain Schema Owner + Head of Specs Team | Yes — ST-14 implementation | Sprint 2, before ST-14 implementation begins |
| ST-19 cross-EPIC compliance check: PMO Lead to review commit history at Sprint 1 close | PMO Lead | Yes — ST-19 acceptance | Sprint 1 close |
