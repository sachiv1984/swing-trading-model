**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-29
**Cycle:** 2026-05-29__release-v4.3

---

# Sprint Capacity — v4.3 Governance Consolidation, QA Debt Clearance & Ops Hardening

---

## Capacity Inputs

| Field | Value |
|-------|-------|
| Sprint duration | 2 sprints (solo-dev evenings) |
| Available FTE | 1 (solo developer) |
| Per-sprint capacity | ~10–12 hrs (12–14 evening sessions × ~0.75–1 hr/session) |
| Total capacity (2 sprints) | ~20–24 hrs |
| Warn threshold | >14 hrs/sprint sustained |
| Skill constraints | Base44 frontend delegation required for ST-16/17/18; human staging access required for ST-06/07/08/13/14 |

*Baseline source: `claude/roadmap/workforce_capacity.md` §Sprint Capacity Baseline (effective 2026-05-27). Revised upward from 8–10 days → 12–14 days/sprint to reflect actual sustained pace.*

---

## Item Effort Mapping

### Sprint 1

#### EPIC-01 — Governance Patch Resolution

| Story | Title | Effort Band | Hrs (mid) |
|-------|-------|-------------|-----------|
| ST-01 | execution_prompt.md STEP 3.2.A: qa_signed_off advisory patch | XS | 0.5 |
| ST-02 | execution_prompt.md STEP 5.3/STEP 8: sprint close branch safety advisory | XS | 0.5 |
| ST-03 | qa_evidence_template.md: AC mapping 1:1 advisory | XS | 0.5 |
| ST-04 | Staging-only AC pre-designation reference table | S | 1.0 |
| ST-05 | AI feature inventory document | S | 0.5 |
| **EPIC-01 total** | | | **~3.5 hrs** |

*Release plan mid-point estimate: 4 hrs. Variance within XS rounding.*

#### EPIC-04 — Frontend Polish & Arc 5 Feature

| Story | Title | Effort Band | Hrs (mid) |
|-------|-------|-------------|-----------|
| ST-16 | Pre-entry check entry price bug fix | XS | 0.25 |
| ST-17 | Claude thesis generation UI copy audit | S | 0.5 |
| ST-18 | Arc 5 compliance score in monthly P&L report | M | 2.0 |
| **EPIC-04 total** | | | **~2.75 hrs** |

*Release plan mid-point estimate: 4 hrs. ST-18 is the effort anchor.*

**Sprint 1 total estimated effort: ~6.25–8 hrs**
**Sprint 1 confirmed capacity: ~10–12 hrs**
**Sprint 1 utilisation: ~52–80% — within capacity ✅**

---

### Sprint 2

#### EPIC-03 — Operations & Security Hardening

| Story | Title | Effort Band | Hrs (mid) |
|-------|-------|-------------|-----------|
| ST-13 | Staging environment parity audit | M | 2.0 |
| ST-14 | claude-audit-log performance baseline | XS | 0.25 |
| ST-15 | API key rotation policy and external API key security register | S | 1.0 |
| **EPIC-03 total** | | | **~3.25 hrs** |

*Release plan mid-point estimate: 4 hrs.*

#### EPIC-02 — QA Debt & Test Coverage

| Story | Title | Effort Band | Hrs (mid) |
|-------|-------|-------------|-----------|
| ST-06 | Staging verification: Claude thesis generation | XS | 0.5 |
| ST-07 | Staging verification: ticker validation live Yahoo Finance rejection path | XS | 0.5 |
| ST-08 | Staging verification: Claude API daily cost threshold alert | XS | 0.5 |
| ST-09 | Playwright E2E coverage for Arc5ComplianceSection | S | 0.5 |
| ST-10 | Arc 5 end-to-end integration test specification | M | 2.0 |
| ST-11 | CI pipeline execution time baseline measurement | XS | 0.25 |
| ST-12 | Playwright scenario coverage matrix and Arc 5 coverage audit | M | 2.0 |
| **EPIC-02 total** | | | **~6.25 hrs** |

*Release plan mid-point estimate: 8 hrs. ST-06/07/08 are human-delegate staging tasks with minimal engine effort.*

**Sprint 2 total estimated effort: ~9.5–12 hrs**
**Sprint 2 confirmed capacity: ~10–12 hrs**
**Sprint 2 utilisation: ~79–120% — AT UPPER BOUND ⚠ WARN**

---

## Total Effort vs Capacity

| Sprint | Capacity | Estimated Effort | Variance | Status |
|--------|----------|-----------------|----------|--------|
| Sprint 1 | ~10–12 hrs | ~6.25–8 hrs | +2–6 hrs buffer | ✅ Within capacity |
| Sprint 2 | ~10–12 hrs | ~9.5–12 hrs | 0–0.5 hrs buffer | ⚠ WARN — at limit |
| **Total** | **~20–24 hrs** | **~15.75–20 hrs** | **~0–8 hrs buffer** | **⚠ WARN — at upper bound** |

**Outcome:** ⚠ WARN — effort at upper bound of confirmed capacity. Sprint 1 has adequate buffer. Sprint 2 is tight; staging verification stories (ST-06/07/08/13/14) are human-delegate tasks that reduce engine effort significantly. Feasible if staging environment is configured before Sprint 2 begins.

**Capacity WARN Acknowledgement:** Product Owner issued `plan sprint` with awareness of the WARN from release planning. Risk accepted: "feasible over 2 sprints; staging verifications are human-delegate tasks with minimal code effort." Record: `capacity_warn_acknowledged = true`.

---

## Merge Order and Sprint Phasing

| Sprint | EPICs | Merge Order |
|--------|-------|------------|
| Sprint 1 | EPIC-01, EPIC-04 | EPIC-01 → EPIC-04 |
| Sprint 2 | EPIC-03, EPIC-02 | EPIC-03 → EPIC-02 |

**execution_state.json owner:** EPIC-01 (first EPIC in execution order across the release). All subsequent EPICs must check for `execution_state.json` existence before creating their own section — read and append, do not overwrite.

> **Gate re-invocation:** If a gate condition is met during the sprint, do not add deferred items informally. Invoke the amendment cycle (`amend cycle --cycle 2026-05-29__release-v4.3 --reason "<gate met>"`) to add the item to the sprint backlog. The amendment cycle is the only authorised path for post-seal scope addition.
