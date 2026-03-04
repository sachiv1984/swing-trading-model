**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-04
**Cycle:** 2026-03-04__release-v1.8

---

# Stage 3.5 — Local Model Integrity Check

## Release: v1.8 — Risk Dashboard

---

## 3.5.1 S2 → EPIC Mapping Integrity

| S2 ID | Title | Maps to EPIC | EPIC has Maps-to declared | Pass? |
|-------|-------|-------------|--------------------------|-------|
| S2-01 | Risk Dashboard Page | EPIC-01 | ✅ EPIC-01 Maps to: S2-01 | ✅ |
| S2-02 | Golden Output Regression Baseline | EPIC-02 | ✅ EPIC-02 Maps to: S2-02, S2-03, S2-04, S2-05 | ✅ |
| S2-03 | Backtest vs Live Stop Reconciliation | EPIC-02 | ✅ | ✅ |
| S2-04 | Dependency Vulnerability Scanning | EPIC-02 | ✅ | ✅ |
| S2-05 | Automated OpenAPI Drift Detection | EPIC-02 | ✅ | ✅ |
| S2-06 | Settings Endpoint Method Drift | EPIC-03 | ✅ EPIC-03 Maps to: S2-06, S2-07 | ✅ |
| S2-07 | Update openapi.yaml to v1.9.0 | EPIC-03 | ✅ | ✅ |
| S2-08 | Running API Changelog | EPIC-04 | ✅ EPIC-04 Maps to: S2-08, S2-09 | ✅ |
| S2-09 | Unavailability Failure Mode Documentation | EPIC-04 | ✅ | ✅ |

**Every S2 item maps to exactly one EPIC. Every EPIC declares its S2 mappings. ✅**

---

## 3.5.2 EPIC → Risk Mapping

| EPIC | Related Risks |
|------|--------------|
| EPIC-01 | RISK-01 (mitigated), RISK-04 (Design Gate) |
| EPIC-02 | RISK-03 (capacity) |
| EPIC-03 | RISK-02 (settings decision — ESC-20260304-01), RISK-05 (openapi conflicts) |
| EPIC-04 | RISK-03 (capacity) |

All 5 risks have RISK-xx IDs and declare `Relates to: EPIC-xx` or `Release-level`. ✅

---

## 3.5.3 Dependency Integrity

| Dependency | Declared in Stage 3 | Consistent? |
|------------|--------------------|-----------:|
| ST-06 depends on ST-05 | ✅ Yes | ✅ |
| ST-01 depends on Design Gate artefact | ✅ Yes | ✅ |
| ST-03 depends on ST-01 | ✅ Yes | ✅ |
| ST-09 gated on ESC-20260304-01 | ✅ Yes — escalation being raised | ✅ |

---

## 3.5.4 Scope Containment Check

**Challenger review:** Does any item in the execution plan represent a new initiative not on the approved roadmap or DL-005 backlog pool?

| Item | Roadmap/DL-005 Source | Cleared? |
|------|-----------------------|---------|
| EPIC-01 Risk Dashboard | Roadmap §3.4 | ✅ |
| EPIC-02 CI Quality Gates | DL-005 → BLG-NEW-01, 02, 05, 08 | ✅ |
| EPIC-03 Spec Debt | Pre-existing BLG-SPEC-D2, D7 (in backlog) | ✅ |
| EPIC-04 Governance Docs | DL-005 → BLG-NEW-03, 07 | ✅ |

No initiative added. No roadmap mutation. ✅

---

## 3.5.5 Strategy Boundary Check

**Strategy Rules & System Intent Owner review:** Any items that touch signal generation, calculation logic, or execution parameters?

- EPIC-01 (Risk Dashboard): Reads from existing endpoints. No new strategy parameters. No §13 impact. ✅
- EPIC-02 (CI): Tests golden values against `strategy_rules.md` — this is verification, not modification. ✅
- EPIC-03 (Spec Debt): Documentation and spec updates only. ✅
- EPIC-04 (Governance): Policy documents only. ✅

**No §13 boundary issue found. ✅**

---

## 3.5.6 Escalation Flag

**ESC-20260304-01** — Product Owner decision required for BLG-SPEC-D2 (settings endpoint method). Escalation being raised. EPIC-03/ST-09 is gated. Other EPICs are unblocked.

This escalation will be recorded in `escalations.md` with disposition: Deferred, Blocks execution: No (EPIC-01, 02, 04 can proceed; only EPIC-03/ST-09 is blocked).

---

## 3.5.7 Model Integrity Verdict

| Check | Result |
|-------|--------|
| S2 → EPIC complete mapping | ✅ Pass |
| EPIC → Risk mapping | ✅ Pass |
| Dependency chain consistency | ✅ Pass |
| Scope containment (no new initiatives) | ✅ Pass |
| Strategy boundary clear | ✅ Pass |
| ESC-20260304-01 (settings decision) | ⚠️ Conditional — gated EPIC-03/ST-09 only; deferred with Blocks execution: No |

**Stage 3.5 Result: PASS** (conditional on ESC-20260304-01 being recorded and correctly dispositioned as Deferred/Blocks execution: No)
