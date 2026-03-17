**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Release:** v2.0
**Cycle:** 2026-03-17__release-v2.0
**Last Updated:** 2026-03-17

---

# Lessons Learnt — Release Planning v2.0

Feature / Trigger: v2.0 — Reporting & Alerts
Run: 2026-03-17__release-v2.0
Reviewed by: PMO Lead
Date filed: 2026-03-17
Prior cycle checked: 2026-03-15__release-v1.10

---

## What worked well

- **Prior cycle deferred items all resolved:** All 5 deferred patches from the v1.10 lessons_learnt_closure.md were applied before this cycle ran (sprint_planning_prompt.md v2.0→v2.1, backlog_management_prompt.md v1.2→v1.3, post_ship_closure.md v1.9→v2.0, roadmap_prompt.md v2.6→v2.7, roadmap_prompt.md v2.8→v3.0). STEP -1.5 required zero carry-forwards.
- **Scope consolidation:** v2.0 scope naturally consolidated 3 roadmap initiatives (4.1b, 4.3, 3.5) plus 7 backlog items targeted at v2.0. The phased vs. separate release discussion (v1.11 vs. v2.0 for BLG-BE-01) was resolved before the planning run — BLG-BE-01 guaranteed Sprint 1 item 1 with minimal overhead.
- **Conditional scope handling:** EPIC-03 (3.5 Alerts) was cleanly separated as conditional scope with a concrete gate clearance mechanism (ST-11 materialises the DL-003 trigger). Sprint planning team has a clear decision path.
- **EPIC-06 as parallel track:** Correctly identified that BLG-GOV-01 + BLG-GOV-02 (governance tooling, ~40 hrs) should not compete with product delivery sprints. Parallel track designation avoids blocking v2.0 product scope.

---

## Friction Log

---

### Friction Item 1

**Classification:** Type C — Missing Prerequisite: A prerequisite spec or document does not exist when needed for planning

**Recurrence:** No (same pattern noted in v1.9 cycle, addressed by backlog age advisory — but this instance is for new initiatives, not aged items)

**What happened:**
Three v2.0 initiatives (4.1b tax-year P&L, 4.3 signal exposure, 3.5 alerts) all lacked frontend page specs or API endpoint specs. The backend for 4.3 already exists (`signal_endpoints.md` documents `top_n`/`lookback_days`) but no signals page spec exists. The planning run had to front-load spec authoring stories (ST-01, ST-03, ST-06) as Sprint 1 / pre-work items, which reduces the "working software" output of Sprint 1.

**Where in the routine:** STEP 1 — Release Readiness Validation (spec gap detection)

**Root cause:** When initiatives are planned at the roadmap level, spec pre-work is often described qualitatively ("backend already supports this — frontend and spec task") without creating the actual spec document. By the time release planning runs, the specs are still absent and must be written as sprint stories.

**Blast radius analysis:**
- What would have propagated: Sprint 1 would have begun implementation without a signed-off spec, creating rework risk if spec decisions differ from implementation assumptions.
- When it would have surfaced: Sprint planning or mid-sprint when implementation assumptions diverge from spec.
- Recovery cost if uncaught: Medium — spec-first stories (ST-01, ST-03) absorb Sprint 1 capacity, reducing working software output, but prevent downstream rework.

**Process patch:**

→ No immediate patch applied (process is working as designed — spec authoring in Sprint 1 is the correct mitigation). No prompt change required.

→ Advisory note: When the roadmap describes an initiative as "frontend and spec task, not an engineering one" (as for 4.3), consider pre-authoring the spec during the roadmap rebalance cycle rather than deferring it to a Sprint 1 story. This is optional process improvement — not a governance gap.

---

## Prior Cycle Deferred Lessons Status

All deferred patches from 2026-03-15__release-v1.10 lessons_learnt_closure.md confirmed applied before this cycle. Zero carry-forwards.

No OVERDUE items. No escalations from prior cycle.

---

## Deferred Patches (for next governance session)

None. No process patches required from this cycle.

---

```json
// ARTEFACT_STATUS
{
  "file": "lessons_learnt.md",
  "cycle_id": "2026-03-17__release-v2.0",
  "phase": "Release",
  "filed_utc": "2026-03-17T00:25:00Z",
  "friction_item_count": 1,
  "action_now_count": 0,
  "deferred_count": 0,
  "escalation_count": 0,
  "overdue_patches": 0,
  "status": "Complete"
}
```
