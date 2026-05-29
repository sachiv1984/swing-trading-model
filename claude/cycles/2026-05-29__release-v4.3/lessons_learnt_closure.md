**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Active
**Last Updated:** 2026-05-29
**Cycle:** 2026-05-29__release-v4.3
**Phase:** Post-Ship Closure

---

# Lessons Learnt — Post-Ship Closure v4.3

Cycle: 2026-05-29__release-v4.3
Produced by: Post-Ship Closure Engine (STEP 8.5)
Date: 2026-05-29
Records reviewed: lessons_learnt.md (Release Planning); lessons_learnt_cycle.md (Phase 3 + Phase 4)

---

## Closure-Phase Observations

- **Backlog reconciliation:** 16 of 17 items marked ✅ COMPLETE. BLG-FE-38 not found in active backlog — pre-archived by a prior groom_backlog run. Noted in closure record §3; item confirmed delivered via execution_state.json and changelog.
- **Deviation compliance:** Zero deviations filed this sprint. STEP 5 trivially passes.
- **Specs Index §6/§7:** All open items are RESOLVED. No new spec gaps or compliance issues surfaced during v4.3 delivery. No index updates required.
- **Scope/Decisions documents:** Both superseded with correct notes.
- **Endpoint drift:** No new API endpoints added in v4.3. No drift advisory generated.
- **System Status Report:** Already corrected to "Verified — 2026-05-29" during delivery verification. No further correction needed.

---

## Consolidated Action Summary

### Immediate Actions Applied (3)

| # | Item | Source | Disposition |
|---|------|--------|-------------|
| 1 | v4.2 deferred items (qa_signed_off, branch safety, AC mapping) all resolved in v4.3 ST-01/02/03 — 100% OA carry-forward resolution rate | lessons_learnt_cycle.md Phase 3 | Positive confirmation — no process change needed |
| 2 | ANTHROPIC_API_KEY staging policy changed from production-only to permanent staging — removes recurring staging friction for AI QA | lessons_learnt_cycle.md Phase 3 | Positive infrastructure update — no further action |
| 3 | Clean verification cycle (zero deviations, zero gaps) — gate sequencing and QA evidence readiness working correctly | lessons_learnt_cycle.md Phase 4 | Positive confirmation — no process change needed |

No immediate template or prompt updates applied this run. All immediate items are positive-confirmation no-ops.

### Deferred to Next Cycle (7)

| # | Action | Source | Owner | Target | Backlog ref |
|---|--------|--------|-------|--------|-------------|
| 1 | roadmap_prompt.md STEP 8.1: add advisory — if Now horizon is empty after Extended-tier no-change rebalance and no next-release section exists in current_roadmap.md, PO should add one now to prevent STEP -1.2 gate fire. Recurrence: 2× (v4.2 + v4.3). | lessons_learnt.md Friction 1 | Head of Specs Team | v4.4 | BLG-GOV-71 (to file in STEP 12) |
| 2 | release_planning_prompt.md STEP 7: add RESUME PRECHECK note — if session resumed via context compaction and STEP 7 completed without intermediate sync, perform sync immediately before STEP 8 | lessons_learnt.md Friction 2 | Head of Specs Team | v4.4 | (no new BLG — already deferred in lessons_learnt.md) |
| 3 | OPERATIONAL_GUIDE.md §7 staging guidance (or staging_parity_report template): add "Staging URL disambiguation" section explicitly noting Render deploys two separate services (frontend SPA vs backend API) with different hostnames; health checks and baselines must target backend API URL | lessons_learnt_cycle.md Phase 3 | Infrastructure & Operations Owner | v4.4 | BLG-OPS-43 (pre-named in lessons record) |
| 4 | sprint_planning_prompt.md: add "frontend classification fast-path" — if story involves (a) prop/state threading bug fix, (b) variable rename in React, or (c) new section/component against locked spec with Playwright feasibility confirmed, default to autonomous unless new design decisions required. Third consecutive sprint with unnecessary delegated_frontend planning for this class. | lessons_learnt_cycle.md Phase 3 | Head of Specs Team | v4.4 | BLG-GOV-72 (to file in STEP 12) |
| 5 | execution_prompt.md delegation sign-off substep: when setting sign_off_record.status = "cleared" for a delegated story, also set deviations_filed = true if no deviation record was filed. Prevents batch correction at sprint close. | lessons_learnt_cycle.md Phase 3 | Head of Specs Team | v4.4 | BLG-GOV-73 (to file in STEP 12) |
| 6 | qa_evidence_template.md: update DoQ sign-off block to include example for delegated_qa pattern (where delegatees sign individual stories and DoQ acknowledges in aggregate). Both "Signed off by: Director of Quality" and "Director of Quality: Confirmed — [owner]" formats are valid; template should clarify. | lessons_learnt_cycle.md Phase 4 | Head of Specs Team | v4.4 | BLG-GOV-74 (to file in STEP 12) |
| 7 | execution_prompt.md (or delivery_verification_prompt.md): add spec_references policy note for documentation-creation stories — empty spec_references is acceptable if delivery_note field documents the created artefact path. Prevents false traceability flags for document-creation stories. | lessons_learnt_cycle.md Phase 4 | Head of Specs Team | v4.5 | (to file when applicable) |

### Escalated for Decision (0)

None.

---

## Carry-Forward

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Roadmap TBD gap has now recurred for the 3rd consecutive time (v4.2, v4.3). If BLG-GOV-71 is not applied before v4.4 release planning, treat as systemic governance gap and escalate to Head of Specs Team. | At v4.4 release planning: check claude/backlog/backlog.md for BLG-GOV-71. If absent or not resolved, escalate to HoST before proceeding past STEP -1.2. | Release Planning |
| 2 | delegated_frontend misclassification has occurred for 3 consecutive sprints (v4.1/v4.2/v4.3 EPIC-04). BLG-GOV-72 must be applied in v4.4 sprint planning prompt before the next sprint that includes React-only stories. | At v4.4 sprint planning: confirm sprint_planning_prompt.md has the frontend classification fast-path before classifying EPIC stories. | Sprint Planning |
