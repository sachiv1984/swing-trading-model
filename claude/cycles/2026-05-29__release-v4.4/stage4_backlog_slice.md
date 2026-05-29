**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Published
**Cycle:** 2026-05-29__release-v4.4
**Release:** v4.4
**Published:** 2026-05-29
**Sealed:** true

---

# Release Backlog Slice — v4.4

Governance Patches, SI-02 Pre-Planning Sprint & Ops Hardening

13 stories / 4 EPICs / 2 sprints

**Merge order:** EPIC-01 → EPIC-04 (Sprint 1); EPIC-02 → EPIC-03 (Sprint 2)

---

## EPIC-01 — Governance Prompt Patches

**Maps to:** S2-01
**Owner:** Head of Specs Team
**Sprint:** Sprint 1
**Description:** Apply v4.3 OA carry-forward governance prompt patches (BLG-GOV-69/71/72/73/74) and the v4.3 lessons_learnt.md deferred patch for release_planning_prompt.md STEP 7. Resolves all 5 deferred governance patches from the prior cycle.

---

### ST-01 — Apply BLG-GOV-71: roadmap_prompt.md STEP 8.1 advisory for empty Now horizon

**EPIC:** EPIC-01
**Sprint:** Sprint 1
**Owner:** Head of Specs Team
**Effort:** XS (~0.5 hr)
**Classification:** autonomous
**Source:** BLG-GOV-71 (3rd recurrence — v4.1/v4.2/v4.3 STEP -1.2 gate fires after Extended-tier no-change rebalance)
**Staging-only ACs:** None
**spec_references:** claude/system/roadmap_prompt.md

**Acceptance Criteria**
- **AC-01:** Advisory note added to roadmap_prompt.md STEP 8.1 (or nearest Now horizon summary step): "If Now horizon is empty after this rebalance and no next-release section exists in current_roadmap.md for the next anticipated release, the Product Owner should add one now — omitting it will trigger STEP -1.2 of the Release Planning Engine at every subsequent invocation until resolved."
- **AC-02:** Condition scoped to: Extended-tier no-change tier + Now horizon empty + no next-release section in roadmap
- **AC-03:** roadmap_prompt.md version bumped (current v6.5 → v6.6)
- **AC-04:** OPERATIONAL_GUIDE.md §6 source prompt header + §14 Roadmap Engine Source updated; §14 version bumped; changelog row added
- **AC-05:** prompt_change_log.md entry appended in same commit as roadmap_prompt.md change

---

### ST-02 — Apply BLG-GOV-72: sprint_planning_prompt.md frontend classification fast-path

**EPIC:** EPIC-01
**Sprint:** Sprint 1
**Owner:** Head of Specs Team
**Effort:** XS (~0.5 hr)
**Classification:** autonomous
**Source:** BLG-GOV-72 (3rd consecutive sprint — v4.1/v4.2/v4.3 EPIC-04 misclassified as delegated_frontend)
**Staging-only ACs:** None
**spec_references:** claude/system/sprint_planning_prompt.md

**Acceptance Criteria**
- **AC-01:** Frontend classification fast-path section added to sprint_planning_prompt.md (story classification step)
- **AC-02:** Three fast-path conditions explicitly listed with the default-autonomous rule: (a) prop/state threading bug fix; (b) variable rename in React; (c) new section/component against locked spec with Playwright feasibility confirmed → default: autonomous unless new design decisions required
- **AC-03:** sprint_planning_prompt.md version bumped (current v3.7 → v3.8)
- **AC-04:** OPERATIONAL_GUIDE.md §7 source prompt header + §14 Sprint Planning Engine updated; §14 version bumped; changelog row added
- **AC-05:** prompt_change_log.md entry appended in same commit

---

### ST-03 — Apply BLG-GOV-73: execution_prompt.md auto-set deviations_filed on delegation clearance

**EPIC:** EPIC-01
**Sprint:** Sprint 1
**Owner:** Head of Specs Team
**Effort:** XS (~0.5 hr)
**Classification:** autonomous
**Source:** BLG-GOV-73 (batch correction pattern at sprint close for cleared delegated stories)
**Staging-only ACs:** None
**spec_references:** claude/system/execution_prompt.md

**Acceptance Criteria**
- **AC-01:** Delegation sign-off substep updated in execution_prompt.md: when setting sign_off_record.status = "cleared" for a delegated story, if no deviation record was filed, also set deviations_filed = true in the same operation
- **AC-02:** Condition precisely scoped: delegated story + cleared + no DEV-* record filed → deviations_filed = true
- **AC-03:** execution_prompt.md version bumped (current v3.32 → v3.33)
- **AC-04:** OPERATIONAL_GUIDE.md §8 source prompt header + §14 Execution Engine Source updated; §14 version bumped; changelog row added
- **AC-05:** prompt_change_log.md entry appended in same commit

---

### ST-04 — Apply BLG-GOV-69 + BLG-GOV-74: qa_evidence_template.md delegated_qa sign-off format

**EPIC:** EPIC-01
**Sprint:** Sprint 1
**Owner:** Head of Specs Team
**Effort:** XS (~0.5 hr)
**Classification:** autonomous
**Source:** BLG-GOV-69 (delivery verification Phase 4 observation v4.3) + BLG-GOV-74 (post-ship closure item v4.3)
**Staging-only ACs:** None
**spec_references:** claude/system/templates/qa_evidence_template.md

**Acceptance Criteria**
- **AC-01:** qa_evidence_template.md DoQ sign-off block updated to include example for the delegated_qa pattern (where delegatees sign individual stories and DoQ acknowledges in aggregate)
- **AC-02:** Both valid format variants shown: (i) "Signed off by: Director of Quality / Date: YYYY-MM-DD"; (ii) "Director of Quality: Confirmed — [owner] ([N] stories), YYYY-MM-DD"
- **AC-03:** Template clarifies both variants are valid; strict mode literal check alignment noted
- **AC-04:** qa_evidence_template.md version bumped (current v1.3 → v1.4)
- **AC-05:** OPERATIONAL_GUIDE.md §14 QA Evidence Template row updated; §14 version bumped; prompt_change_log.md entry added in same commit

---

### ST-05 — Apply release_planning_prompt.md STEP 7 RESUME PRECHECK patch

**EPIC:** EPIC-01
**Sprint:** Sprint 1
**Owner:** Head of Specs Team
**Effort:** XS (~0.5 hr)
**Classification:** autonomous
**Source:** v4.3 lessons_learnt.md LL-2 (deferred patch — no BLG item); STEP 7 intermediate sync skipped when session resumed via context compaction
**Staging-only ACs:** None
**spec_references:** claude/system/release_planning_prompt.md

**Acceptance Criteria**
- **AC-01:** STEP 7 "Intermediate global state sync" section in release_planning_prompt.md updated with RESUME PRECHECK note
- **AC-02:** Note reads: "RESUME PRECHECK: If the session was resumed via context compaction and STEP 7 has completed without the intermediate sync being performed, execute the intermediate sync immediately before proceeding to STEP 8. Do not proceed to STEP 8 with stale `.claude_current_state.json` state from the prior cycle."
- **AC-03:** release_planning_prompt.md version bumped (current v2.31 → v2.32)
- **AC-04:** OPERATIONAL_GUIDE.md §6B source prompt header + §14 Release Planning Engine updated; §14 version bumped; changelog row added
- **AC-05:** prompt_change_log.md entry appended in same commit

---

## EPIC-02 — SI-02 Backend Pre-Planning

**Maps to:** S2-02
**Owner:** Head of Backend Engineering; Head of Engineering
**Sprint:** Sprint 2
**Description:** Produce the four backend pre-planning documents required before SI-02 (Behavioural Drift Detection) sprint planning can seal: query pre-design (BLG-BE-17), architecture review (BLG-BE-18), index pre-assessment (BLG-BE-23), and background job architecture design (BLG-BE-20, conditional on sprint initiation).

---

### ST-06 — SI-02 drift detection query pre-design (BLG-BE-17)

**EPIC:** EPIC-02
**Sprint:** Sprint 2
**Owner:** Head of Backend Engineering
**Effort:** M (~1–2 days)
**Classification:** delegated_decision
**Source:** BLG-BE-17
**Staging-only ACs:** None — design document, no staging verification required
**spec_references:** []
**delivery_note:** Output: backend/docs/si02_query_predesign.md (or equivalent path under docs/specs/si02/)

**Acceptance Criteria**
- **AC-01:** Query pre-design document produced identifying which fields are required per trade record for SI-02 drift analysis (regime_at_entry, setup_type_at_entry, entry_condition_score, etc.)
- **AC-02:** Draft SQL query patterns documented for rolling win-rate vs stated setup criteria (per entry type, per regime); at minimum: win_rate_by_setup_type, win_rate_by_regime_at_entry
- **AC-03:** Missing data fields (if any) enumerated with schema migration scope estimate (field name, type, migration complexity)
- **AC-04:** Query performance assessment on current trade history volume included (row counts, estimated cost)
- **AC-05:** Document reviewed by Head of Backend Engineering; filed before SI-02 sprint planning seals

---

### ST-07 — Arc 5 backend architecture review for SI query patterns (BLG-BE-18)

**EPIC:** EPIC-02
**Sprint:** Sprint 2
**Owner:** Head of Engineering; Head of Backend Engineering
**Effort:** M (~1–2 days)
**Classification:** delegated_decision
**Source:** BLG-BE-18
**Staging-only ACs:** None — design document
**spec_references:** []
**delivery_note:** Output: docs/specs/si02/arc5_backend_architecture_review.md (or equivalent)

**Acceptance Criteria**
- **AC-01:** Architecture review document produced reviewing current synchronous FastAPI endpoint pattern against SI-02/SI-04 query complexity
- **AC-02:** Synchronous vs background recommendation made with explicit rationale (latency tolerance, query cost, single-user Render constraints)
- **AC-03:** If background layer recommended: Architecture Decision Record (ADR) filed as input to SI-02 sprint planning
- **AC-04:** Document filed before SI-02 sprint planning seals

---

### ST-08 — SI-02 query index pre-assessment (BLG-BE-23)

**EPIC:** EPIC-02
**Sprint:** Sprint 2
**Owner:** Head of Engineering; Head of Backend Engineering
**Effort:** S (~1 day)
**Classification:** autonomous
**Source:** BLG-BE-23 (gate: BLG-GOV-51 ✅ complete v4.1)
**Staging-only ACs:** None — design document
**spec_references:** []
**delivery_note:** Output: docs/specs/si02/si02_index_preassessment.md (or equivalent)

**Acceptance Criteria**
- **AC-01:** Using BLG-GOV-51 EXPLAIN ANALYZE results, required database indexes for SI-02 drift detection queries identified (or confirmed none needed)
- **AC-02:** Migration plan produced for required indexes: index definitions (CREATE INDEX statements), estimated creation cost, migration timing strategy
- **AC-03:** Gate condition verified — BLG-GOV-51 ✅ shipped v4.1 confirmed
- **AC-04:** Document filed as explicit input to SI-02 sprint planning capacity estimate

---

### ST-09 — SI-02 background job architecture design (BLG-BE-20) *(Conditional)*

**EPIC:** EPIC-02
**Sprint:** Sprint 2
**Owner:** Head of Backend Engineering; Head of Engineering
**Effort:** S (~1 day)
**Classification:** delegated_decision
**Source:** BLG-BE-20 (gate: SI-02 sprint planning initiated — interpreted as: after ST-06/07/08 outputs define sprint scope)
**Staging-only ACs:** None — design document
**spec_references:** []
**delivery_note:** Output: docs/specs/si02/si02_background_job_adr.md (or equivalent)
**gate_condition:** ST-06 (BLG-BE-17) and ST-07 (BLG-BE-18) outputs available; SI-02 sprint scope beginning to crystallise

**Acceptance Criteria**
- **AC-01:** Three architecture approaches evaluated: (a) on-demand per-request computation; (b) periodic background cron task; (c) event-triggered on trade close
- **AC-02:** Trade-offs assessed specifically for single-user Render deployment where task queue infrastructure (Celery, etc.) is not available
- **AC-03:** Architecture Decision Record (ADR) produced: approach selected, rationale, constraints, failure modes
- **AC-04:** Gate condition verified — ST-06 + ST-07 outputs reviewed before commencing

---

## EPIC-03 — SI-02 Frontend & QA Pre-Planning

**Maps to:** S2-03
**Owner:** Frontend Specs & UX Documentation Owner; QA & Testing Owner; Director of Quality
**Sprint:** Sprint 2
**Description:** Produce the SI-02 component pre-design, interaction spec, and Playwright scenario pre-design documents required before SI-02 sprint planning seals. FE-53 depends on FE-52 output; QA-31 depends on BE-20 output.

---

### ST-10 — SI-02 drift detection result component pre-design (BLG-FE-52)

**EPIC:** EPIC-03
**Sprint:** Sprint 2
**Owner:** Base44 Frontend; Frontend Specs & UX Documentation Owner
**Effort:** S (~1 day)
**Classification:** delegated_frontend
**Source:** BLG-FE-52 (gate: SI-02 sprint planning imminent ✅)
**Staging-only ACs:** None — pre-design document
**spec_references:** []
**delivery_note:** Output: docs/specs/si02/si02_fe_component_predesign.md (or equivalent)

**Acceptance Criteria**
- **AC-01:** Component interface options documented and one selected/proposed: score badge vs percentage deviation display vs rule list format — with rationale
- **AC-02:** Component data contract defined: data shape (input fields), empty state behaviour, loading state, threshold-breach state
- **AC-03:** Output document explicitly labelled as input to ST-11 (BLG-FE-53 interaction spec)
- **AC-04:** Gate condition verified — SI-02 sprint planning imminent (v4.4 is pre-planning sprint) ✅

---

### ST-11 — SI-02 drift detection interaction spec (BLG-FE-53)

**EPIC:** EPIC-03
**Sprint:** Sprint 2
**Owner:** Frontend Specs & UX Documentation Owner
**Effort:** S (~1 day)
**Classification:** delegated_frontend
**Source:** BLG-FE-53 (gate: SI-02 sprint planning imminent ✅; depends on ST-10 output)
**Staging-only ACs:** None — spec document
**spec_references:** []
**delivery_note:** Output: docs/specs/si02/si02_fe_interaction_spec.md (or equivalent)

**Acceptance Criteria**
- **AC-01:** Interaction spec document produced covering all observable drift detection states: active drift, no drift detected, loading, error
- **AC-02:** Dismissal model defined: dismissable vs persistent; if dismissable — re-appearance logic documented
- **AC-03:** Drill-down behaviour defined: does drift result link to underlying trades? If yes — route and data shape defined
- **AC-04:** Severity state transitions documented (e.g. warning → critical thresholds)
- **AC-05:** Gate: ST-10 (BLG-FE-52) component pre-design output available and reviewed

---

### ST-12 — SI-02 Playwright scenario pre-design (BLG-QA-31) *(Conditional)*

**EPIC:** EPIC-03
**Sprint:** Sprint 2
**Owner:** QA & Testing Owner; Director of Quality
**Effort:** S (~1 day)
**Classification:** autonomous
**Source:** BLG-QA-31 (gate: SI-02 sprint planning initiated; depends on ST-09 architecture output)
**Staging-only ACs:** None — pre-design document
**spec_references:** []
**delivery_note:** Output: docs/qa/si02_playwright_predesign.md (or equivalent)
**gate_condition:** ST-09 (BLG-BE-20) architecture output available; SI-02 drift surfaces defined via ST-10/ST-11

**Acceptance Criteria**
- **AC-01:** Draft Playwright scenario set produced covering expected SI-02 frontend surfaces: drift alert display, "no drift detected" state, drift metric details, period filter (if applicable)
- **AC-02:** Staging-only ACs designated at this pre-design stage (e.g. scenarios requiring live drift data are flagged [staging-only evidence])
- **AC-03:** Director of Quality has reviewed draft; confirmation recorded in delivery note
- **AC-04:** Gate condition verified: ST-09 architecture output reviewed before commencing

---

## EPIC-04 — Ops Documentation Hardening

**Maps to:** S2-04
**Owner:** Infrastructure & Operations Owner
**Sprint:** Sprint 1
**Description:** Add Staging URL disambiguation subsection to OPERATIONAL_GUIDE.md §7, explicitly documenting the Render frontend SPA vs backend API separate service URLs. Resolves BLG-OPS-43 (v4.3 staging friction root cause).

---

### ST-13 — Staging URL disambiguation in OPERATIONAL_GUIDE §7 (BLG-OPS-43)

**EPIC:** EPIC-04
**Sprint:** Sprint 1
**Owner:** Infrastructure & Operations Owner
**Effort:** XS (~0.5 hr)
**Classification:** autonomous
**Source:** BLG-OPS-43 (v4.3 Phase 3 staging friction — health checks targeted frontend URL instead of backend API URL)
**Staging-only ACs:** None
**spec_references:** claude/system/OPERATIONAL_GUIDE.md

**Acceptance Criteria**
- **AC-01:** "Staging URL disambiguation" subsection added to OPERATIONAL_GUIDE.md §7 with clear frontend SPA URL vs backend API URL distinction documented
- **AC-02:** Health check and baseline guidance updated to explicitly reference backend API URL (not frontend SPA URL)
- **AC-03:** Example URL patterns included distinguishing the two Render service types (e.g. `trading-assistant-frontend.onrender.com` vs `trading-assistant-api.onrender.com`)
- **AC-04:** OPERATIONAL_GUIDE.md version bumped; §14 self-metadata Version + Last Updated updated; §14 changelog row added
- **AC-05:** prompt_change_log.md entry appended in same commit (OPERATIONAL_GUIDE is Class 6)

---

<!-- release-plan-marker: RP:v4.4:2026-05-29__release-v4.4 -->
