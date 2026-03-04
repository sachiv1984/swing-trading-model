**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-04
**Cycle:** 2026-03-04__release-v1.8

---

# Sprint Planning Notes — 2026-03-04__release-v1.8

---

## Deferred Items

No items deferred from the backlog slice. All 12 ST items included in sprint scope.

Items deferred at release planning stage (not re-evaluated here — carry forward to v1.9):

| Item | Reason | v1.9 Candidate? |
|------|--------|----------------|
| BLG-NEW-04 AI Governance Policy | Capacity / P2 priority | Yes |
| BLG-SPEC-D1, D3, D4, D8, D9 | P2/P3 spec debt | Yes |
| BLG-SPEC-G1–G5 | P2/P3 spec gaps | Yes |

---

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-01 | Design Gate artefact | Spec | ✅ Resolved — Design Gate passed 2026-03-04 |
| ST-03 | ST-01 (frontend spec locked) | Internal | ✅ Resolved — ST-01 complete |
| ST-03 | ST-02 (heat endpoint confirmed) | Internal | Must complete before ST-03 UI wiring |
| ST-04 | ST-03 (implementation to test) | Internal | ST-04 scenario authoring can begin in parallel; execution of scenarios requires ST-03 |
| ST-06 | ST-05 (golden baseline required) | Internal | Hard dependency — ST-05 must complete first |
| ST-08 | ST-10 (openapi.yaml updated) | Coordination | ST-08 CI check must pass after ST-10 update; ship together |
| ST-12 | ST-10 (coordinate) | Advisory | API changelog should reflect same version as ST-10 update |
| ST-09 | ESC-20260304-01 decision | External | ✅ Resolved — option (a) declared 2026-03-04 |

No circular dependencies detected. ✅

---

## Execution Sequence

### Wave 1 — Immediate (no dependencies, start in parallel)

1. **ST-02** — Backend: Confirm heat calculation availability
2. **ST-05** — Golden output regression baseline
3. **ST-07** — Dependency vulnerability scanning
4. **ST-09** — Settings endpoint method drift (spec update, option a)
5. **ST-10** — Update openapi.yaml to v1.9.0
6. **ST-11** — Unavailability failure mode documentation

### Wave 2 — After Wave 1 prerequisites met

7. **ST-06** — Backtest vs live stop reconciliation *(after ST-05)*
8. **ST-08** — Automated OpenAPI drift detection CI *(alongside / after ST-10)*
9. **ST-12** — Running API changelog *(coordinate with ST-10)*
10. **ST-03** — Risk Dashboard page implementation *(after ST-02)*

### Wave 3 — After implementation

11. **ST-04** — QA acceptance test scenarios *(after ST-03 ready for testing)*

### Already complete

- **ST-01** — Frontend spec: Risk Dashboard Page *(completed at Design Gate 2026-03-04)*

---

## Risk Flags

| Risk ID | Associated Item | Mitigation Status |
|---------|----------------|------------------|
| RISK-01 | EPIC-01 | ✅ Mitigated — metrics_definitions.md v1.6.0 confirmed canonical |
| RISK-02 | EPIC-03 / ST-09 | ✅ Resolved — ESC-20260304-01 decision made (option a) |
| RISK-03 | Release-level | ⚠️ Active — capacity WARN; accepted by PO; milestone-based delivery |
| RISK-04 | EPIC-01 / ST-01 | ✅ Mitigated — Design Gate passed; risk_dashboard.md v0.1.0 locked |
| RISK-05 | EPIC-03 / ST-10 | Active — API Contracts owner to review all contract files before update; approach in pre-alignment |

---

## Outstanding Actions at Planning Seal

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Confirm heat endpoint availability (ST-02 pre-alignment) | Head of Engineering | No — confirmed at execution start |
| Confirm prospective heat calculation endpoint approach | Head of Engineering | No — confirmed at execution start |
| RISK-05 ST-10 approach confirmation | API Contracts & Documentation Owner | No — confirmed at execution of ST-10 |

No outstanding actions marked as blockers. Sprint may be sealed. ✅
