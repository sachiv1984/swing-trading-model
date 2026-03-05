Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-03-05

# QA Evidence Log — EPIC-02: CI Quality Gates

**EPIC:** EPIC-02 — CI Quality Gates
**Cycle:** 2026-03-04__release-v1.8
**Sprint goal:** Establishing automated correctness gates (golden output CI, vulnerability scanning, OpenAPI drift detection).
**Test scenarios used:** Derived from spec + acceptance criteria (CI pipeline verification)

---

## Per-Story Evidence

*(All ST items in EPIC-02 are delegated_backend. Evidence to be completed by Head of Engineering and confirmed by Director of Quality and Cybersecurity & Trust Lead.)*

---

### ST-05 — Golden Output Regression Baseline

**Spec references:** `claude/strategy/strategy_rules.md`

**Status:** 🟡 PENDING — Delegated to Head of Engineering + QA & Testing Owner (DEL-20260305-04).

**Acceptance criteria:**
- `tests/golden_outputs.json` exists with golden test cases
- Golden values derived from `strategy_rules.md` spec (not implementation)
- Precision tolerance documented
- CI step asserts outputs match on every PR; fails on deviation
- Director of Quality confirms golden coverage sufficient

*(To be completed by Head of Engineering)*

- **Commit SHA:** _(pending)_
- **What was built:** _(pending)_
- **Deviation check:** _(pending)_

---

### ST-06 — Backtest vs Live Stop Reconciliation

**Spec references:** `tests/golden_outputs.json` (from ST-05)

**Status:** 🟡 PENDING — Delegated to Head of Engineering (DEL-20260305-05). Blocked on ST-05.

*(To be completed after ST-05)*

- **Commit SHA:** _(pending)_
- **What was built:** _(pending)_
- **Deviation check:** _(pending)_

---

### ST-07 — Dependency Vulnerability Scanning

**Spec references:** (CI tooling — no canonical spec; approach documented in workflow file)

**Status:** 🟡 PENDING — Delegated to Head of Engineering (DEL-20260305-06).

**Acceptance criteria:**
- CI step scanning Python deps for CVEs on every PR
- Tool and severity threshold documented in workflow
- Cybersecurity & Trust Lead acknowledges approach
- Director of Quality confirms CI integration

*(To be completed by Head of Engineering; Cybersecurity & Trust Lead to acknowledge)*

- **Commit SHA:** _(pending)_
- **What was built:** _(pending)_
- **Cybersecurity & Trust Lead acknowledgement:** _(pending)_

---

### ST-08 — Automated OpenAPI Drift Detection

**Spec references:** `docs/reference/openapi.yaml` (v1.9.0 after ST-10 merge)

**Status:** 🟡 PENDING — Delegated to Head of Engineering (DEL-20260305-07). Coordinate with ST-10 merge.

**Acceptance criteria:**
- CI step detects drift between openapi.yaml and markdown contracts
- Approach documented; merge blocked on drift
- Passes on clean post-ST-10 state; fails on synthetic drift
- Director of Quality confirms CI integration

*(To be completed after EPIC-03 / ST-10 is merged to main)*

- **Commit SHA:** _(pending)_
- **What was built:** _(pending)_
- **Deviation check:** _(pending)_

---

## EPIC-Level Consolidation

*(To be completed when all ST items are done)*

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|---------------|----------------|--------------------|---------|----|
| ST-05 | `strategy_rules.md` | _(pending)_ | Golden outputs CI; spec-derived values | _(pending)_ | _(pending)_ |
| ST-06 | ST-05 baseline | _(pending)_ | Backtest vs live reconciliation check | _(pending)_ | _(pending)_ |
| ST-07 | (CI tooling) | _(pending)_ | Dependency CVE scanning; threshold documented | _(pending)_ | _(pending)_ |
| ST-08 | `openapi.yaml` | _(pending)_ | OpenAPI drift detection CI | _(pending)_ | _(pending)_ |

**QA test coverage:**
- Scenarios run: _(to be completed — CI pipeline verification)_
- Regression areas checked: CI workflow correctness, golden output coverage, dependency scanning
- Known deviations filed: _(to be completed)_

**QA sign-off block:** (Director of Quality completes this)
- [ ] All acceptance criteria verified against canonical spec
- [ ] No unresolved P0 or P1 deviations
- [ ] Regression areas checked
- [ ] Cybersecurity & Trust Lead sign-off on ST-07 (dependency scanning approach)
- [ ] CI pipeline verified end-to-end (golden outputs, reconciliation, CVE scan, drift detection)
- Signed off by: Director of Quality
- Date:
- Comments:
