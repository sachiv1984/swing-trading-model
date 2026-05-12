**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
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
