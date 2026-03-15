**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-15
**Cycle:** 2026-03-15__release-v1.10

---

# Sprint Planning Notes — 2026-03-15__release-v1.10

## Backlog Slice Source

Original — `claude/cycles/2026-03-15__release-v1.10/stage4_backlog_slice.md`

No amendment file present (`amended_backlog_slice_path` is empty in `.claude_current_state.json`).

---

## Deferred Items

None. All 7 stories from the backlog slice are included in sprint scope.

| Item | Reason | Next Sprint Candidate? |
|------|--------|----------------------|
| — | — | — |

---

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-02 | ST-01 | Internal — staging env must exist before CI/CD can deploy to it | Resolved (sequenced) |
| ST-03 | ST-01, ST-02 | Internal — governance docs reference staging URL; staging + auto-deploy must be live | Resolved (sequenced) |
| ST-06 | ST-05 | Internal — CI step requires tests to exist | Resolved (sequenced) |
| ST-07 | ST-01 (advisory) | External/advisory — scenario authoring is independent; staging recommended for scenario *execution* only | Noted (authoring may proceed before ST-01) |

No circular dependencies detected.

---

## Execution Sequence

Recommended execution order for a solo developer:

**Track A — EPIC-01 (P1 — start immediately):**
1. ST-01 — Provision staging environment infrastructure
2. ST-02 — Configure CI/CD auto-deploy to staging *(depends on ST-01)*
3. ST-03 — Update QA sign-off governance process *(depends on ST-01 + ST-02)*

**Track B — EPIC-02 (independent — can run in parallel with Track A):**
4. ST-04 — Refactor CohortAnalysis.js to use backend endpoint

**Track C — EPIC-03 (independent start; scenarios recommended after ST-01):**
5. ST-05 — FastAPI TestClient integration tests for portfolio endpoints
6. ST-06 — Add integration test CI step *(depends on ST-05)*
7. ST-07 — Author v1.7 missing QA test scenarios (BLG-QA-01)

**Recommended solo sequencing:** ST-01 → ST-02 → ST-03 → ST-04 → ST-05 → ST-06 → ST-07

Rationale: EPIC-01 is P1 and blocking for QA governance; complete it first. EPIC-02 (ST-04) is the shortest EPIC and independent — good to deliver early. EPIC-03 has internal dependencies (ST-06 after ST-05) and is sequenced last as all items are P2.

ST-07 may begin authoring at any point; staging environment (ST-01) is only required for scenario *execution*, not authoring. Authoring can proceed alongside EPIC-01 if the developer wants to parallelise.

---

## Risk Flags

| Risk ID | Associated Item | Mitigation Status | Notes |
|---------|----------------|------------------|-------|
| RISK-01 | EPIC-01 (ST-01) | Valid — staging scope ambiguity | Infrastructure & Operations Owner must decide and document the hosting approach (cloud service vs same-host isolation) before ST-01 implementation begins. Constrain to simplest viable approach. This is an outstanding pre-execution action — it does not block sprint planning seal. See Outstanding Actions. |
| RISK-02 | EPIC-02 (ST-04) | Valid — CohortAnalysis regression | AC explicitly requires: period toggle and cohort table output must match pre-refactor behaviour exactly. Director of Quality sign-off on regression verification before merge. Spec reference: analytics.md v1.4 (locked by Design Gate). |
| RISK-03 | EPIC-03 (ST-05) | Valid — integration test DB dependency | AC explicitly requires CI-safe design: dependency override or in-memory SQLite. Director of Quality confirms CI step present and passing on a test PR before sign-off. |

No risks have materialised since release planning (2026-03-15). All mitigations remain valid.

---

## Capacity WARN Acknowledgement (IMP-41)

**Outcome of capacity check:** WARN — no `--capacity` parameter was specified at invocation.

**Situation:** Total mid effort ~48 hrs. Feasible under full-time (1.5-week sprint, ~52–60 hrs available). Could stretch under evenings-only mode (3-week sprint, ~45–60 hrs available with low headroom). Hi estimate (74 hrs) would over-run any schedule.

**Product Owner acknowledgement:** The Product Owner has reviewed the capacity WARN and explicitly acknowledges the risk. Scope is confirmed as single-sprint (all 7 stories, all 3 EPICs). Phasing option (Sprint 1: EPIC-01; Sprint 2: EPIC-02+03) is available as a fallback if execution reveals capacity over-run mid-sprint.

*Acknowledgement recorded here; `capacity_warn_acknowledged: true` to be set in STEP 7 state write.*

---

## Pre-Sprint Vulnerability Scan

**Tool:** pip-audit
**Status:** `pip-audit` not installed in the current environment (`command not found`).

**Impact:** Vulnerability scan could not be completed pre-sprint. Recommend installing `pip-audit` before sprint execution begins:
```
pip install pip-audit
pip-audit -r backend/requirements.txt
```
Prior cycle (v1.9 Sprint 1) pip-audit result was `clean` (no high/critical CVEs). No new backend dependencies have been added since v1.9.

**Advisory:** This does not block sprint planning. The execution engine's CI gate (`quality_gate.yml`) will run pip-audit at merge time. Pre-sprint scanning is advisory per sprint_planning_prompt.md §-1.9 rationale.

---

## LL-01 Pre-Sprint Decision Note

**From lessons_learnt.md LL-01:** The sprint planning session must confirm the staging approach decision (Infrastructure & Operations Owner) is documented before sealing the sprint backlog for execution.

**Resolution at this session:** The LL-01 action was surfaced at sprint planning. The sprint backlog Outstanding Actions table records this as a pre-execution requirement (not a seal blocker). The Infrastructure & Operations Owner must document the hosting approach decision before ST-01 implementation begins. This satisfies the LL-01 action — the decision checkpoint is now formally tracked.

---

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Capacity WARN acknowledged by Product Owner | Product Owner | Yes — recorded in this document and in sprint backlog sign-off |
| Infrastructure & Operations Owner documents staging hosting approach (RISK-01 / LL-01) | Infrastructure & Operations Owner | No — required before ST-01 execution begins, not before sprint planning seals |
| Security field: all 7 stories confirmed N/A (no security surface changed) | Head of Specs Team | No — confirmed at planning; noted in sprint backlog |
