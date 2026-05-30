Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-05-30

---

# Execution Escalations — 2026-05-30__release-v4.5

---

## ESC-EXEC-20260530-01

- **Raised at:** 2026-05-30T14:30:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-05-30__release-v4.5
- **Step:** STEP 3 — EPIC-03 ST-06
- **ST/EPIC item:** EPIC-03 / ST-06 — SI-02 §13 formal boundary review
- **Trigger type:** Human-Delegation
- **Blocking statement:** ST-06 requires the Strategy Rules & System Intent Owner to conduct a formal §13 boundary review for the SI-02 drift detection feature set. This review must determine whether the proposed drift detection output is: deterministic, display-only, and non-automated (no automated position management). The review must produce an explicit PASS/FAIL determination with binding conditions documented. ST-07 cannot begin until ST-06 returns PASS.
- **Owning authority:** Strategy Rules & System Intent Owner
- **Unblock criteria:** §13 review document produced with explicit PASS/FAIL determination; binding conditions documented (e.g., "drift alerts are informational only; no automated position management"); sign-off recorded and committed to `exec/2026-05-30__release-v4.5/EPIC-03` with commit format `[EPIC-03][ST-06] SI-02 §13 boundary review — PASS/FAIL`
- **SLA due-by:** 2026-06-02T14:30:00Z (72 hours — strategy boundary SLA)
- **Blocks execution:** Yes (ST-07 and ST-08 gated on PASS result; EPIC-03 cannot close without ST-06)
- **Disposition:** Open
- **Resolution summary:** —

---

## ESC-EXEC-20260530-02

- **Raised at:** 2026-05-30T14:30:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-05-30__release-v4.5
- **Step:** STEP 3 — EPIC-03 ST-07
- **ST/EPIC item:** EPIC-03 / ST-07 — SI-02 drift detection score metric definition
- **Trigger type:** Human-Delegation
- **Blocking statement:** ST-07 requires the Metrics Definitions & Analytics Canonical Owner (with Head of Specs Team) to define the drift detection score metric for SI-02. This definition must cover: user-facing format (% deviation vs raw count vs index), rolling window length, threshold bands (green/amber/red states), warning state triggers, and SI-05 weekly digest integration points. The resulting document must be filed at `docs/specs/metrics/si02_drift_score.md`. ST-07 cannot begin until ST-06 returns PASS.
- **Owning authority:** Metrics Definitions & Analytics Canonical Owner (co-signed: Head of Specs Team)
- **Unblock criteria:** (1) ESC-EXEC-20260530-01 resolved with PASS; (2) metric definition document produced and committed to `exec/2026-05-30__release-v4.5/EPIC-03` at `docs/specs/metrics/si02_drift_score.md`, covering all AC-01–04 from `stage4_backlog_slice.md#ST-07`; (3) signed off by Metrics Definitions & Analytics Canonical Owner and Head of Specs Team
- **SLA due-by:** 72 hours after ESC-EXEC-20260530-01 resolved with PASS
- **Blocks execution:** Yes (part of EPIC-03 critical path)
- **Disposition:** Open
- **Resolution summary:** —

---

## ESC-EXEC-20260530-03

- **Raised at:** 2026-05-30T14:30:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-05-30__release-v4.5
- **Step:** STEP 3 — EPIC-03 ST-08
- **ST/EPIC item:** EPIC-03 / ST-08 — SI-02 data schema pre-definition
- **Trigger type:** Human-Delegation
- **Blocking statement:** ST-08 requires the Data Model & Domain Schema Owner (with Head of Specs Team) to conduct a gap analysis of current trade, position, and trade plan schemas and produce a data schema pre-definition document for SI-02. The document must enumerate missing fields with data types, tables affected, and migration complexity estimates. It should be informed by ST-07 metric definitions (not hard-blocked, but benefits from metric context). The document must be filed at `docs/specs/data_model/si02_data_schema.md`.
- **Owning authority:** Data Model & Domain Schema Owner (co-signed: Head of Specs Team)
- **Unblock criteria:** (1) ESC-EXEC-20260530-01 resolved with PASS; (2) data schema pre-definition document produced and committed to `exec/2026-05-30__release-v4.5/EPIC-03` at `docs/specs/data_model/si02_data_schema.md`, covering all AC-01–05 from `stage4_backlog_slice.md#ST-08`; (3) signed off by Data Model & Domain Schema Owner and Head of Specs Team. Note: can be started in parallel with ST-07 after ST-06 PASS — not hard-blocked on ST-07, but metric definition context is valuable.
- **SLA due-by:** 72 hours after ESC-EXEC-20260530-01 resolved with PASS
- **Blocks execution:** Yes (part of EPIC-03 critical path)
- **Disposition:** Open
- **Resolution summary:** —
