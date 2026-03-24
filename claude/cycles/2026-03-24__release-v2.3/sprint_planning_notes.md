**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-24
**Cycle:** 2026-03-24__release-v2.3

---

# Sprint Planning Notes — 2026-03-24__release-v2.3

## Backlog Slice Source

Original — `claude/cycles/2026-03-24__release-v2.3/stage4_backlog_slice.md`

No amendment in effect. `amended_backlog_slice_path` absent from `.claude_current_state.json`.

---

## Carry-Forward Advisory (from cycle 2026-03-21__release-v2.2)

3 carry-forward items reviewed from `claude/cycles/2026-03-21__release-v2.2/lessons_learnt_closure.md §Carry-Forward`:

| # | Item | Applicable this sprint |
|---|------|------------------------|
| 1 | Sprint planning should surface advisory when blocked_decision items scheduled with no design artefact | Addressed: ST-13 (UX-01) design artefact was produced in design gate. ST-17 (GOV-08) advisory raised below. |
| 2 | Delegation log entries must be updated at point of merge, not batched at sprint close | Carried to execution phase — reminder noted for Phase 3 |
| 3 | Backlog grooming engine should run ID uniqueness scan (LL-RP-v22-01) | Carried to next `groom backlog` run — not in sprint scope |

---

## Pre-Sprint Required Decisions Status

| Decision | Status | Evidence |
|----------|--------|---------|
| [RISK-04] BLG-UX-01 sidebar navigation design decision (collapsible sections / grouping pattern) | **Resolved** — Product Owner selected collapsible section groups (4 groups: Trading, Analytics, Tools, System) in design gate session 2026-03-24 | `claude/cycles/2026-03-24__release-v2.3/design_gate.md` §Notes — RISK-04 resolved |

---

## Pre-Sprint Vulnerability Scan

pip-audit result: **clean** — no known vulnerabilities found across all 57 packages in `backend/requirements.txt` (scan date: 2026-03-24).

---

## Capacity WARN Acknowledgement

Capacity check outcome: WARN (~15–26 days total, 3 sprints at ~18–24 days capacity).
Product Owner acknowledged 2026-03-24. Rationale: ST-17 (GOV-08) is a conditional/stretch item; excluding it, mid-point estimate (~18 days) is within capacity. ST-17 executes only if Sprint 3 residual capacity permits after ST-13 and ST-16 complete.

---

## Delegation Class Assignments

| Item | Delegation Class | Justification |
|------|----------------|--------------|
| ST-01 BLG-FEAT-11 | delegated_frontend | New compliance panel (backend + frontend); UX change; SPS=4 DoQ sign-off required |
| ST-02 BLG-FEAT-09 | delegated_frontend | New staleness indicator UI element + backend response field |
| ST-03 BLG-OPS-08 | delegated_backend | Infrastructure/backend scripting; no UX change |
| ST-04 BLG-QA-06 | delegated_qa | QA domain — seed script authoring |
| ST-05 BLG-QA-05 | delegated_qa | Playwright E2E authoring + CI wiring |
| ST-06 BLG-QA-01 | delegated_qa | Playwright E2E authoring + CI wiring |
| ST-07 BLG-SPEC-D14 | autonomous | Spec doc update + openapi.yaml; no UX change; fully defined change; no mid-task sign-off |
| ST-08 BLG-OPS-09 | delegated_backend | Backend implementation (DB monitoring + alert); no UX change |
| ST-09 BLG-OPS-07 | autonomous | Documentation only (playbook); no UX change; content fully defined by health_endpoints.md v1.1 |
| ST-10 BLG-FE-05 | delegated_frontend | New nav badge UI element |
| ST-11 BLG-FE-04 | delegated_frontend | Frontend fix (CTA button in empty state) |
| ST-12 BLG-FE-02 | delegated_frontend | Multi-component refactor + shared pattern — design spec locked; no new page (refactor of existing) |
| ST-13 BLG-UX-01 | delegated_frontend | Nav restructure; design decision resolved; UX spec locked |
| ST-14 BLG-GOV-07 | autonomous | Governance prompt update; fully defined change (add specific guidance to §9 invariants); §6 checklist applies |
| ST-15 BLG-QA-03 | delegated_qa | Template document authoring — QA domain |
| ST-16 BLG-QA-04 | delegated_qa | CI tooling + coverage report; QA domain |
| ST-17 BLG-GOV-08 | delegated_decision | L effort prompt compression; requires HoST + PMO Lead review before applying; conditional stretch |

---

## Test Scenario Gap Flags (LL-v2.0-P4-2)

Items classified `delegated_frontend` introducing new pages or new user-facing controls:

| Item | Gap | Flag |
|------|-----|------|
| ST-01 BLG-FEAT-11 | New compliance panel on Positions page | EPIC-01 `test_scenarios`: pending — QA & Testing Owner to author before next sprint on this domain |
| ST-02 BLG-FEAT-09 | New staleness indicator on Analytics/Portfolio pages | EPIC-01 `test_scenarios`: pending — QA & Testing Owner to author before next sprint on this domain |
| ST-10 BLG-FE-05 | New alert badge on Alerts nav item | EPIC-04 `test_scenarios`: pending — QA & Testing Owner to author before next sprint on this domain |
| ST-13 BLG-UX-01 | Sidebar nav restructured with collapsible groups | EPIC-04 `test_scenarios`: pending — QA & Testing Owner to author before next sprint on this domain |

Items ST-11 (CTA fix), ST-12 (loading state refactor of existing components) — existing UI refactor, not new page/control → no flag required.

---

## Blocked-Decision Advisory (LL-v2.2-SP-01)

**ST-17 BLG-GOV-08 (delegated_decision):** No HoST design artefact exists for the prompt compression approach. Advisory: "A HoST design session should be scheduled before Sprint 3 start to define the compression criteria and identify which sections of `roadmap_prompt.md` and `release_planning_prompt.md` can safely be extracted/compressed — to reduce mid-sprint design overhead." Advisory only — does not block planning or scope selection.

---

## Deferred Items

None — all 17 items included in sprint scope.

ST-17 (GOV-08) is conditional within Sprint 3 (stretch), not deferred. It remains in scope; execution is contingent on residual Sprint 3 capacity.

---

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-04 BLG-QA-06 | ST-03 BLG-OPS-08 | Internal sequential | Resolved — ST-03 Sprint 1, ST-04 Sprint 2 |
| ST-05 BLG-QA-05 | ST-03 BLG-OPS-08 + ST-04 BLG-QA-06 | Internal sequential chain | Resolved — ST-03 Sprint 1, ST-04 Sprint 2, ST-05 Sprint 2 |
| ST-09 BLG-OPS-07 | ST-07 BLG-SPEC-D14 | Internal sequential (spec reference) | Resolved — ST-07 Sprint 1, ST-09 Sprint 1 |
| ST-17 BLG-GOV-08 | ST-13 BLG-UX-01 complete + ST-16 BLG-QA-04 complete | Internal sequential (conditional) | Resolved — both Sprint 3; ST-17 executes only if capacity remains |

No circular dependencies detected.

---

## Execution Sequence

### Sprint 1 — Operational Readiness + QA Foundation Prerequisites + Governance Quick Win

| Order | Item | EPIC | Rationale |
|-------|------|------|-----------|
| 1 | ST-14 BLG-GOV-07 | EPIC-05 | XS governance quick win; no dependencies; fastest unblock |
| 2 | ST-15 BLG-QA-03 | EPIC-05 | S documentation item; no dependencies; enables QA reporting standard from Sprint 2 onwards |
| 3 | ST-07 BLG-SPEC-D14 | EPIC-03 | XS; must precede ST-09 (health playbook); early sequencing clears RISK-03 |
| 4 | ST-08 BLG-OPS-09 | EPIC-03 | S; independent of other EPIC-03 items; pairs naturally with spec update sprint |
| 5 | ST-09 BLG-OPS-07 | EPIC-03 | S; depends on ST-07; references health_endpoints.md v1.1 |
| 6 | ST-03 BLG-OPS-08 | EPIC-02 | S; prerequisite for ST-04 and ST-05 in Sprint 2 — must complete Sprint 1 |
| 7 | ST-06 BLG-QA-01 | EPIC-02 | M; independent of OPS-08 chain; chart E2E tests can run in parallel with above |

### Sprint 2 — User Features + QA Automation Completion

| Order | Item | EPIC | Rationale |
|-------|------|------|-----------|
| 1 | ST-04 BLG-QA-06 | EPIC-02 | S-M; gated on ST-03 complete; seeds prerequisite for ST-05 |
| 2 | ST-05 BLG-QA-05 | EPIC-02 | M; gated on ST-03 + ST-04; smoke test confirms QA automation layer is operational |
| 3 | ST-01 BLG-FEAT-11 | EPIC-01 | M-L; main feature item; SPS=4 DoQ sign-off required at sprint close |
| 4 | ST-02 BLG-FEAT-09 | EPIC-01 | S-M; paired with EPIC-01; independent of FEAT-11 but same EPIC |

### Sprint 3 — Frontend Polish + QA Coverage + Conditional Stretch

| Order | Item | EPIC | Rationale |
|-------|------|------|-----------|
| 1 | ST-11 BLG-FE-04 | EPIC-04 | XS; fastest frontend win; fixes known deviation |
| 2 | ST-10 BLG-FE-05 | EPIC-04 | S; alert badge; independent quick win |
| 3 | ST-12 BLG-FE-02 | EPIC-04 | M; loading state standardisation; refactor before UX-01 (which restructures nav) |
| 4 | ST-13 BLG-UX-01 | EPIC-04 | M; sidebar nav groups; design resolved; sequences after ST-12 to avoid nav refactor conflict |
| 5 | ST-16 BLG-QA-04 | EPIC-05 | M; integration test coverage report; independent of EPIC-04 |
| 6 | ST-17 BLG-GOV-08 | EPIC-05 | L; conditional stretch — executes only if Sprint 3 capacity permits after ST-13 + ST-16 complete |

---

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 ST-01 | Valid — Strategy Rules & System Intent Owner DoQ sign-off at delivery verification remains required; §13.3 display-only constraint in AC |
| RISK-02 | EPIC-02 ST-03/04/05 | Valid — OPS-08 in Sprint 1 (item 6); QA-06+QA-05 in Sprint 2 items 1–2; chain is correctly sequenced |
| RISK-03 | EPIC-03 ST-07/09 | Valid — SPEC-D14 Sprint 1 item 3; OPS-07 follows in same sprint; confirmed ordered |
| RISK-04 | EPIC-04 ST-13 | **Resolved** — Product Owner issued design decision in design gate session 2026-03-24 (collapsible section groups). ST-13 is no longer conditional. |
| RISK-05 | EPIC-05 ST-17 | Valid — GOV-08 remains conditional/stretch in Sprint 3; does not block release |

---

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| EPIC-01 test_scenarios flag: QA & Testing Owner to author scenario file before next sprint on compliance/staleness domain | QA & Testing Owner | No |
| EPIC-04 test_scenarios flag: QA & Testing Owner to author scenario file before next sprint on alert badge / nav groups domain | QA & Testing Owner | No |
| ST-17 GOV-08: HoST design session recommended before Sprint 3 to define compression criteria (advisory — LL-v2.2-SP-01) | Head of Specs Team | No |
| Carry-forward item 2: delegation log must be updated at merge point, not batched at sprint close | PMO Lead (Phase 3 reminder) | No |
