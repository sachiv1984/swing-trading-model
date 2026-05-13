**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Cycle:** 2026-05-09__release-v3.3

---

# Lessons Learnt — 2026-05-09__release-v3.3

---

## Phase 3 — 2026-05-09__release-v3.3

| # | Area | Observation | Action | Priority |
|---|------|-------------|--------|----------|
| 1 | Delegation / Classification | All 4 EPICs had delegated_frontend items that were not completed during the sprint (ST-03, ST-05, ST-07, ST-17 frontend sub-deliverables). The pattern of backend-complete/frontend-deferred is recurring across Arc 3 stories. | Consider front-loading frontend work in next sprint cycle, or explicitly scheduling a dedicated frontend sprint. The feature flag infrastructure (ST-16) is now in place to support staged frontend rollout. | P2 |
| 2 | GitHub Integration | Multi-EPIC PRs conflicting with main required manual rebase on the EPIC branches after sequential EPIC merges. EPIC-04 merged before EPIC-03 and EPIC-02, requiring conflict resolution on both. | Establish explicit merge order at STEP 3 start and document in execution_state.json. When EPIC-04 (governance) merges first, immediately rebase remaining EPICs to avoid accumulating conflicts. | P3 |
| 3 | Execution State Sync | EPIC-04 PR was merged between sessions, leaving execution_state.json with stale pr_status: "open". The STEP 5.0A pr_status sync caught this at sprint close. | The STEP 5.0A pre-seal sync is working as intended. No action needed — process handled correctly. | Observation |
| 4 | QA Evidence Files | qa_evidence_EPIC-03.md and qa_evidence_EPIC-02.md were committed on their respective EPIC branches (not on main). On resume from EPIC-04 branch, these appeared missing from the working directory. | When resuming on a different EPIC branch, check remote branches for QA evidence before flagging as missing: `git show origin/EPIC-xx:path/to/qa_evidence.md`. This avoids false-positive hard gate triggers. | P3 |
| 5 | Acceptance Criteria | ST-08 AC specified specific error codes (404/503/429) that the actual implementation does not return (always 200 with null sub-fields). This was caught as a deviation at delivery. | Research endpoint error handling should be revisited as a P2 backlog item. The spec (research_endpoint.md §Error Responses) now documents the known limitation. | P2 |
| 6 | Governance Compliance | CLAUDE.md §6 checklist (version bump + OPERATIONAL_GUIDE update + prompt_change_log entry) executed correctly for all governance patches in ST-13 and ST-14. No compliance gaps. | Process working. The ST-13 sealed-file check (OA-01/CF-01) is now active in execution_prompt.md and will catch future violations at STEP 0. | Positive |

---

## Phase 4

**Phase:** Delivery Verification
**Cycle:** 2026-05-09__release-v3.3
**Section anchor:** `## Phase 4`
**Filed:** 2026-05-13
**Reviewed by:** PMO Lead

**Prior cycle checked:** 2026-05-05__release-v3.2 (Phase 4 section present — recurrence check complete)

| friction_item | phase | type | classification | action | owner | target_date |
|---------------|-------|------|----------------|--------|-------|-------------|
| ST-08 deviation was filed as P2 in sprint_close.md but DoQ counter-confirmation assessed it as P3. Divergent priority classifications created ambiguity at verification time. Verification engine adopted DoQ authority (P3) but the discrepancy required explicit documentation in verification_report.md §4. | Phase 4 | Type D — Process Gap: no reconciliation step between sprint_close deviation priority and QA evidence priority classification | defer | Add note to sprint_close template "Deviations Filed" table: priority must match qa_evidence_EPIC-xx.md DoQ assessment; if DoQ reclassifies, sprint_close table must be updated before sealing. | Head of Specs Team | v3.5 |
| research_view_protocol.md §2.3 states "backlog item filed" for SC-RV-18/19 Playwright scenarios, but no such item existed. Discovered at STEP 5. Protocol checkbox ([ ] Backlog item filed) was unchecked — open action not closed at sprint close. | Phase 4 | Type D — Process Gap: protocol document self-referential backlog checkboxes not verified at sprint close | defer | Add sprint_close check: verify all protocol document "backlog item filed" checkboxes are actually completed before sealing. Filed TEST-GAP-EPIC-03-v33 to remediate this instance. | PMO Lead | v3.5 |
| Prior cycle Phase 4 action-now items resolved: (1) BLG-GOV-19 criterion-3 explicit check — delivered in EPIC-03 qa_evidence autonomous sign-off block; (2) mock payload advisory — delivered as ST-13/OA-02 in execution_prompt.md §14. Both carry-forwards resolved. | Phase 4 | Type E — Positive pattern | action-now | No action required — both prior cycle deferred items resolved as sprint stories. | PMO Lead | — |
| All 4 QA evidence logs produced with correct DoQ sign-off and clear AC-level evidence. Gate sequencing clean: sprint_close sealed, QA evidence ready, STEP -1 passed first pass. No re-verification required this cycle (improvement from v3.2 which required two passes). | Phase 4 | Type E — Positive pattern | action-now | No action required. | PMO Lead | — |

**Recurrence Notes:**

Prior cycle (2026-05-05__release-v3.2) Phase 4 items:
- BLG-GOV-19 criterion-3 misapplication: RESOLVED ✅
- Playwright mock payload divergence: RESOLVED ✅

New friction items this cycle:
1. P2/P3 priority discrepancy between sprint_close and DoQ assessment — first occurrence; deferred.
2. Protocol backlog-item checkbox not completed — first occurrence; remediated by TEST-GAP-EPIC-03-v33.
