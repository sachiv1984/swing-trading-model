Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Last Updated: 2026-03-17
Cycle: 2026-03-17__release-v2.0

---

# Lessons Learnt — Post-Ship Closure Phase (Phase 5) — 2026-03-17__release-v2.0

**Phase:** Post-Ship Closure
**Cycle:** 2026-03-17__release-v2.0
**Filed:** 2026-03-17
**Reviewed by:** PMO Lead

---

## §1 — Records Reviewed

| Record | Location | Friction Items | Action-Now at Source | Deferred at Source |
|--------|----------|----------------|----------------------|--------------------|
| Release Planning lessons | `claude/cycles/2026-03-17__release-v2.0/lessons_learnt.md` | 1 | 0 | 0 |
| Sprint Execution (Phase 3) lessons | `claude/cycles/2026-03-17__release-v2.0/lessons_learnt_cycle.md §Phase 3` | 5 | 3 (applied prior session to CLAUDE.md §2) | 2 |
| Delivery Verification (Phase 4) lessons | `claude/cycles/2026-03-17__release-v2.0/lessons_learnt_cycle.md §Phase 4` | 2 | 0 | 2 |

---

## §2 — Immediate Patches Applied This Session

| Ref | Source Record | Target | Change | Version |
|-----|--------------|--------|--------|---------|
| LL-v2.0-P3-4 | Phase 3 friction item 4 (base44.baseUrl) | `execution_prompt.md` §qa_evidence template | Added DoQ checklist item: "For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object" | v2.3 → v2.4 |
| LL-v2.0-P3-5 | Phase 3 friction item 5 (shared governance file merge conflicts) | `execution_prompt.md` STEP 4 merge gate | Added merge order note: later EPIC branches must rebase onto main after first EPIC merges when >1 EPIC modifies shared governance files | v2.3 → v2.4 |
| LL-v2.0-P4-1 | Phase 4 friction item 1 (qa_evidence file persistence) | `execution_prompt.md` STEP 5.1 | Added QA Evidence Persistence Check: after qa_signed_off: true, confirm qa_evidence Date: field non-blank; if blank, re-apply before STEP 5.3 | v2.3 → v2.4 |
| LL-v2.0-P4-2 | Phase 4 friction item 2 (test scenario gaps for new frontend) | `sprint_planning_prompt.md` STEP 3.1 | Added test scenario gap flag for delegated_frontend items introducing new pages/controls: flag test_scenarios as pending in execution_state.json and sprint_planning_notes.md | v2.1 → v2.2 |

**Total immediate patches applied this session: 4**

**Previously applied this cycle (prior session, action-now at Phase 3 execution):**
- LL-v2.0-P3-1: CLAUDE.md §2 — "Every new API endpoint must be added to openapi.yaml in the same commit as the contract"
- LL-v2.0-P3-2: CLAUDE.md §2 — "Story commits must land on the branch matching their EPIC prefix"
- LL-v2.0-P3-3: CLAUDE.md §2 — "Frontend DoQ verification must state its evidence method explicitly"

---

## §3 — Deferred Items (Carry-Forward)

| Ref | Source Record | Item | Target | Owner | Target Cycle |
|-----|--------------|------|--------|-------|-------------|
| LL-v2.0-RP-1 | Release Planning lessons_learnt.md friction item 1 | Spec authoring in Sprint 1 advisory — no prompt change required per author; optional process improvement (pre-author specs during roadmap rebalance cycle) | N/A — advisory only | PMO Lead (advisory) | N/A — no action required |

---

## §4 — Closure-Phase Observations

### Document gaps surfaced

- None — all required artefacts were present at post-ship closure preflight.

### Deviation compliance corrections

- None — DEV-v2.0-01 (P3 process deviation, BLG-PROC-01 in backlog) and DEV-v2.0-02 (P1 resolved by hotfix bb66b69) do not require canonical spec file entries. No corrections needed.

### Specs Index updates

- §6.3 `GET /portfolio/prospective-heat`: Marked RESOLVED — ST-13 (v2.0 EPIC-04) delivered spec and implementation. BLG-BE-02 closed.

### Backlog reconciliation

- BLG-GOV-01 and BLG-GOV-02 were in the active backlog section but not in the Closed Items table. Added to Closed Items table (EPIC-06/ST-18 and ST-19 respectively).

---

## §5 — Prior Cycle Deferred Patches Status

All v1.10 deferred patches confirmed applied (per lessons_learnt.md "Prior Cycle Deferred Lessons Status: All deferred patches from 2026-03-15__release-v1.10 lessons_learnt_closure.md confirmed applied before this cycle. Zero carry-forwards."):
- LL-v1.10-P3-1: delivery_verification_prompt.md v1.4→v1.5 (resolution path for sealed=false) ✅ Applied in v1.10 post-ship
- LL-v1.10-P3-2: backlog_management_prompt.md v1.2→v1.3 (endpoint cross-check) ✅ Applied in v1.10 post-ship
- LL-v1.10-P3-3: sprint_planning_prompt.md v1.8+/execution_prompt.md v2.1→v2.2 (autonomous classification pattern) ✅ Applied in v1.10 post-ship
- LL-v1.10-P4-1: execution_prompt.md v2.1→v2.2 (qa_evidence authoring note) ✅ Applied in v1.10 post-ship
- LL-v1.10-P4-2: execution_prompt.md v2.1→v2.2 (deviation type distinction) ✅ Applied in v1.10 post-ship
- LL-v1.10-P4-3: OPERATIONAL_GUIDE.md v3.19→v3.20 (staging test data prerequisite) ✅ Applied in v1.10 post-ship

---

## §6 — Summary

```
Lessons learnt records reviewed: 3 (Release Planning + Phase 3 + Phase 4)
Total friction items across all records: 8
Action-now items (applied at source, prior session): 3
Immediate patches applied this session: 4
Deferred items: 1 (advisory only — no action required)
Escalated: 0
Carry-forward obligations: None
```

All lessons learnt action items have a recorded disposition. No unreviewed items.
