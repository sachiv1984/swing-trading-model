Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-03-17
Cycle: 2026-03-17__release-v2.0

---

## Phase 3 — 2026-03-17__release-v2.0

**Phase:** Sprint Execution
**Cycle:** 2026-03-17__release-v2.0
**Section anchor:** `## Phase 3 — 2026-03-17__release-v2.0`
**Filed:** 2026-03-17
**Reviewed by:** PMO Lead

**Recurrence check:** Prior cycle Phase 3 file: `claude/cycles/2026-03-15__release-v1.10/lessons_learnt_cycle.md` — loaded. Prior outstanding deferred patches reviewed:
- Friction item 1 (sprint close re-invocation gap) — delivery_verification_prompt.md STEP -1 halt output patch deferred to this cycle. Not yet applied; recurrence check below.
- Friction item 2 (backlog item endpoint cross-check) — backlog_management_prompt.md patch deferred to next `groom backlog`. Not yet applied.
- Friction item 3 (autonomous classification heuristic) — sprint_planning_prompt.md patch deferred to next sprint planning touching similar items. Not yet applied.

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| New API endpoints (GET /portfolio/prospective-heat, GET /reports/tax-year) were not added to docs/reference/openapi.yaml when the contracts were authored. The OpenAPI drift CI gate blocked all 5 PRs at merge time. Discovered during merge; required manual fix on the EPIC-04 branch before any PR could land. | Phase 3 | B | action-now | Add to CLAUDE.md §2 Governance Non-Negotiables: "Every new API endpoint must be added to `docs/reference/openapi.yaml` in the same commit as the contract." Applied in this session — CLAUDE.md §2 updated. | PMO Lead / Head of Specs Team | Applied 2026-03-17 |
| ST-20 (CohortAnalysis backend scenarios) was committed on EPIC-04 branch but belongs to EPIC-05 scope. No mechanism prevented a commit landing on the wrong branch. | Phase 3 | D | action-now | Add to CLAUDE.md §2 Governance Non-Negotiables: "Story commits must land on the branch matching their EPIC prefix." Applied in this session — CLAUDE.md §2 updated. | PMO Lead / Head of Specs Team | Applied 2026-03-17 |
| Frontend DoQ verification (ST-02, ST-05) relied on code review rather than live staging behavioural test, because staging auto-deploys from main and feature branches are not visible pre-merge. Evidence method was not stated explicitly in initial QA evidence — required correction by DoQ. | Phase 3 | C | action-now | Add to CLAUDE.md §2 Governance Non-Negotiables: "Frontend DoQ verification must state its evidence method explicitly." Also tracked as BLG-OPS-03 (Render PR preview environments) in backlog for structural fix. Applied in this session — CLAUDE.md §2 updated. | PMO Lead / Head of Specs Team | Applied 2026-03-17 |
| base44.baseUrl not exposed on base44 export — src/api/base44Client.js. Reports.js called `${base44.baseUrl}/reports/tax-year` but the property had never been set on the export object. Went undetected through code review and QA; discovered by user on production after merge. | Phase 3 | A | defer | Strengthen frontend DoQ code review checklist: when a new frontend component makes direct URL construction (not via api.* wrapper), verify the URL-base variable is defined on the imported object. Add to DoQ sign-off block in qa_evidence template (execution_prompt.md §qa_evidence template): "For direct URL construction: confirm base URL variable is exposed on imported object." | PMO Lead | next `run sprint` run |
| PR #90 (EPIC-05) merge conflict: 4 shared governance files (execution_state.json, backlog.md, delegation_log.md, .claude_current_state.json) were modified in EPIC-04 (merged first) and also in EPIC-05's earlier commits. Required git rebase and conflict resolution before merge. | Phase 3 | D | defer | Sprint planning engine should note that branches modifying shared governance files (execution_state.json, .claude_current_state.json, backlog.md, delegation_log.md) should be merged in a defined order and later branches should rebase before final QA. Add merge-order note to execution_prompt.md STEP 4 merge gate: "If >1 EPIC branch modifies a shared governance file, rebase later branches onto main after first EPIC merges." | PMO Lead | next `run sprint` run |

**Recurrence Notes:**
- **Friction item 1 (OpenAPI drift gate at merge):** Recurrence of the endpoint cross-check gap flagged in v1.10 Phase 3 friction item 2 (BLG-API-01 endpoint reference in backlog not cross-checked against spec). That item targeted backlog authoring; this item targets the spec → openapi.yaml gap. Both are manifestations of the same root cause: no enforcement that spec-authored endpoints are registered in the drift gate target. The action-now CLAUDE.md patch addresses the enforcement gap at authoring time.
- **Friction items 2–3 (cross-branch commits, DoQ evidence method):** No prior recurrence found.
- **Friction item 4 (base44.baseUrl):** New pattern — no prior occurrence. Root cause: frontend components that bypass the api.* abstraction layer and construct URLs directly are not covered by current QA checklist.
- **Friction item 5 (shared governance file merge conflicts):** Predictable in any multi-EPIC sprint where shared state files are modified per-EPIC. No prior formal record; pattern expected to recur.
