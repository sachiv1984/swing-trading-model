**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-05-30
**Cycle:** 2026-05-30__release-v4.6

---

# Sprint Planning Notes — 2026-05-30__release-v4.6

---

## Backlog Slice Source

Original — `claude/cycles/2026-05-30__release-v4.6/stage4_backlog_slice.md`

No amendment active (`amended_backlog_slice_path` is empty in `.claude_current_state.json`).

---

## Carry-Forward Items

Carry-forward items reviewed: 1 item from cycle `2026-05-30__release-v4.5`.

| # | Observation | Implication | Engine | Status |
|---|-------------|-------------|--------|--------|
| 1 | v4.5 was absent from roadmap when plan release was invoked (annotation approach required). roadmap_prompt.md could set next_release after DL decision to reduce this gap. | At next release planning: check whether roadmap already has an entry for the next version before invoking plan release. Annotation is acceptable per established pattern. | Release Planning | Addressed — OA-02 is ST-22 in EPIC-04 of this cycle |

---

## Pre-Sprint Vulnerability Scan

Pre-sprint pip-audit: **clean** — no known vulnerabilities found across all 60+ dependencies (fastapi, starlette, anthropic, psycopg2, sqlalchemy, uvicorn, pandas, numpy, httpx, etc.).

---

## Prompt Change Log Advisory

⚠ The following Class 6 prompts have version gaps (current version exceeds last logged entry). Advisory only — does not block sprint planning. Add prepended rows per CLAUDE.md §6 when these prompts are next patched.

| Prompt | Current version | Last logged version | Gap |
|--------|----------------|---------------------|-----|
| `sprint_planning_prompt.md` | v3.8 | v3.6 (2026-05-22) | v3.6→v3.8 |
| `delivery_verification_prompt.md` | v2.9 | v2.8 (2026-05-28) | v2.8→v2.9 |
| `roadmap_prompt.md` | v6.6 | v6.5 (2026-05-21) | v6.5→v6.6 |
| `release_planning_prompt.md` | v2.32 | v2.28 (2026-05-14) | v2.28→v2.32 |

---

## Dependency Map

| Item | Depends On | Type | Status |
|------|-----------|------|--------|
| ST-02 (POST /trade-plans capture) | ST-01 (DS-07 migration — columns must exist) | Internal (EPIC-01) | Resolved — sequence enforced |
| ST-03 (drift service) | ST-01 (trade_plans columns available) | Internal (EPIC-01) | Resolved — sequence enforced |
| ST-04 (GET endpoint) | ST-03 (drift service must exist) | Internal (EPIC-01) | Resolved — sequence enforced |
| ST-05 (unit tests) | ST-03 + ST-04 (service + endpoint) | Internal (EPIC-01) | Resolved — can run after ST-03 and concurrently with ST-04 |
| EPIC-02 ST-06–08 (frontend) | EPIC-01 merged to main | Cross-EPIC (Sprint 2) | Conditional — gate on ST-16 result |
| ST-09 (severity field) | None | None | No dependency |
| ST-12 (RFJ scope doc) | ST-09 (optional: if severity field confirmed shipped, include in scope boundary) | Advisory | Non-blocking — ST-12 notes gate date only |
| ST-13 (SI-05 Phase 1) | SI-01 + SI-03 live ≥30 days | External gate | Deferred at planning — gate clears 2026-06-21 |
| ST-15 (release_planning_prompt patch) | None | None | No cross-dependency |
| ST-22 (roadmap_prompt patch) | None | None | No cross-dependency; §6 checklist applied separately from ST-15 |

No circular dependencies detected.

---

## Execution Sequence

### Sprint 1

**Execution order within Sprint 1 (both EPICs run in parallel on separate branches):**

**EPIC-04 branch** (`exec/2026-05-30__release-v4.6/EPIC-04`):
1. ST-14 (XS — fast-follow; document update)
2. ST-15 (release_planning_prompt.md patch + §6 checklist)
3. ST-16 (delegated_decision — PO queries production DB for trade count)
4. ST-17 (delegated_decision — PO + Challenger produce trajectory assessment)
5. ST-18 (delegated_decision — Strategy Rules & System Intent Owner produces §13 pre-assessment)
6. ST-19 (delegated_decision — Data Model owner produces schema audit)
7. ST-20 (autonomous — PMO Lead reviews GitHub Actions logs, produces investigation doc)
8. ST-21 (autonomous — Head of Specs Team produces external API spec template)
9. ST-22 (roadmap_prompt.md advisory patch + §6 checklist)

**EPIC-01 branch** (`exec/2026-05-30__release-v4.6/EPIC-01`):
1. ST-01 (DS-07 migration — two migration files: ALTER TABLE in transaction; CONCURRENTLY indexes outside transaction)
2. ST-02 (POST /trade-plans handler update)
3. ST-03 (behavioural_drift_service.py — 4 metrics)
4. ST-04 (GET /analytics/behavioural-drift endpoint + openapi.yaml + API contract doc)
5. ST-05 (unit test suite — ≥17 test cases)

**Sprint 1 merge order: EPIC-04 → EPIC-01**

### Sprint 2

**Execution order within Sprint 2:**

**EPIC-03 branch** (`exec/2026-05-30__release-v4.6/EPIC-03`):
1. ST-09 (red_flag_events severity field + migration + API update + openapi.yaml)
2. ST-10 (delegated_decision — FinOps produces hosting cost projection)
3. ST-11 (delegated_decision — Head of UX & Design produces nav cohesion review)
4. ST-12 (autonomous — Frontend Specs owner produces RFJ scope document)
5. ST-13 (conditional, deferred at planning — only if gate met before Sprint 2 planning seals)

**EPIC-02 branch** (`exec/2026-05-30__release-v4.6/EPIC-02`, conditional):
1. ST-06 (BehaviouralDriftPanel component)
2. ST-07 (PerformanceAnalytics integration)
3. ST-08 (Playwright test coverage)

**Sprint 2 merge order: EPIC-03 → EPIC-02 (if EPIC-02 gate met)**

---

## Multi-EPIC Execution Notes

### Execution State Ownership (Full Cycle)

**execution_state.json owner: EPIC-04** — first EPIC in execution order for Sprint 1.

All other EPICs (EPIC-01, EPIC-03, EPIC-02) must check for `execution_state.json` existence before creating their own. If found, read it and append their EPIC's section rather than overwrite. This prevents execution-state collisions (recurrence from v3.3 and v3.4).

Execution engine: when initialising execution_state.json (EPIC-04 branch), include `deferred_at_planning` entries for:
- `EPIC-02.stories.ST-06`: `status: deferred_at_planning`, `gate_condition: "ST-16 audit confirms ≥20 closed trades with linked trade_plans; PO confirms EPIC-02 gate met before Sprint 2 planning seals"`
- `EPIC-02.stories.ST-07`: same gate_condition
- `EPIC-02.stories.ST-08`: same gate_condition
- `EPIC-03.stories.ST-13`: `status: deferred_at_planning`, `gate_condition: "SI-01 + SI-03 live ≥30 days (gate clears 2026-06-21); PO confirms gate met before Sprint 2 planning seals with ST-13"`

This ensures delivery verification STEP 1 can account for all slice items without a traceability gap (AUD-2026-05-21-002).

### Shared File Ownership Advisory

| Shared File | EPIC-04 touches? | EPIC-01 touches? | EPIC-03 touches? | EPIC-02 touches? | Owner/Notes |
|-------------|-----------------|-----------------|-----------------|-----------------|-------------|
| `docs/reference/openapi.yaml` | No | Yes (ST-04 — new endpoint) | Yes (ST-09 — severity filter) | No | EPIC-01 is first to touch; EPIC-03 must rebase onto main after EPIC-01 merges before finalising ST-09 openapi.yaml changes |
| `docs/specs/api_contracts/` | No | Yes (ST-04 — new contract doc) | Yes (ST-09 — update existing doc) | No | EPIC-01 creates new doc; EPIC-03 updates existing — no conflict expected, but EPIC-03 should rebase after EPIC-01 merges |
| `OPERATIONAL_GUIDE.md` | Yes (ST-15, ST-22 — §6 checklist) | No | No | No | EPIC-04 only — no cross-EPIC conflict |
| `docs/System_status_report.md` | Yes (ST-14) | No | No | No | EPIC-04 only |

---

## Risk Flags

| Risk ID | Associated Item | Mitigation Status | Notes |
|---------|----------------|------------------|-------|
| RISK-01 | EPIC-01 (ST-01) | Valid | DS-07 migration requires two files (ALTER TABLE in transaction; CONCURRENTLY indexes outside). Execution engine must verify migration runner supports CONCURRENTLY outside transaction before committing ST-01. Schema doc §6 specifies the split pattern. |
| RISK-02 | EPIC-01/02 (ST-16) | Valid — gated | Data density gate: ST-16 runs in Sprint 1. If count < 20, EPIC-02 deferred; release closes with Sprint 1 + EPIC-03 only. Gate is the mitigation. |
| RISK-03 | EPIC-02 | Valid | BehaviouralDriftPanel pre-design may need updates once full metric formulas are published. si02_fe_component_predesign.md v1.0 incorporates metric format decisions. Review at Sprint 2 planning before committing. (Conditional — only relevant if EPIC-02 gate met.) |
| RISK-04 | EPIC-03 (ST-13) | Valid — gated | SI-05 Phase 1 gate (2026-06-21) may not clear before Sprint 2 seal. ST-13 deferred at planning. Sprint 2 closes with ST-09–12 if gate not met. |
| RISK-05 | EPIC-04 | Valid | Two §6 governance checklist applications in one EPIC (ST-15 for release_planning_prompt.md, ST-22 for roadmap_prompt.md). Clear version bump order: ST-15 first, ST-22 second (separate commits). |

---

## Deferred Items

| Item | EPIC | Reason | Next Sprint Candidate? |
|------|------|--------|----------------------|
| ST-06 (BehaviouralDriftPanel) | EPIC-02 | Gate: ST-16 audit must confirm ≥20 closed trades with linked trade_plans | Yes — Sprint 2 if gate met |
| ST-07 (PerformanceAnalytics integration) | EPIC-02 | Same gate as ST-06 | Yes — Sprint 2 if gate met |
| ST-08 (Playwright tests) | EPIC-02 | Same gate as ST-06 | Yes — Sprint 2 if gate met |
| ST-13 (SI-05 Phase 1) | EPIC-03 | Gate: SI-01 + SI-03 live ≥30 days; clears 2026-06-21 | Yes — Sprint 2 if gate clears in time |

---

## Outstanding Actions

| Action | Owner | Required Before Seal? |
|--------|-------|----------------------|
| Resolve prompt change log gaps (sprint_planning v3.6→v3.8, delivery_verification v2.8→v2.9, roadmap v6.5→v6.6, release_planning v2.28→v2.32) | Head of Specs Team | No (advisory — log entries added when those prompts are next patched in regular governance flow) |

No outstanding actions marked `Blocker? Yes`.
