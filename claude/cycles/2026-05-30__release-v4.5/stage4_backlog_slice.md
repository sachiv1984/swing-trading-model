**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v4.5
**Cycle:** 2026-05-30__release-v4.5
**Published:** 2026-05-30

---

# Stage 4 Backlog Slice — v4.5

---

## EPIC-01 — Execution Prompt Hardening (S2-01)

**Owner:** Head of Specs Team
**Maps to:** S2-01
**Sprint:** Sprint 1
**Sequencing:** Must complete before v4.5 sprint planning seals (v4.4 OA deadline)
**Description:** Resolve all 4 v4.4 deferred execution_prompt.md patches (OA-01–04). All stories modify execution_prompt.md and must apply CLAUDE.md §6 governance file edit checklist.

---

### ST-01 — execution_prompt.md: split DEL terminal-status write into sign-off and push steps

**Backlog ref:** BLG-GOV-75
**Priority:** P3 (Low)
**Effort:** XS (~0.5 hr)
**Owner:** Head of Specs Team
**EXECUTION:** autonomous
**VERIFICATION:** document inspection (prompt patch applied and version-bumped)

**Acceptance Criteria:**
- [ ] AC-01: execution_prompt.md STEP 3 delegation close sequence updated — DEL record write split into two documented sub-steps: (a) `status = "sign_off_cleared"` written at delegation sign-off time; (b) `commit_sha` written at push step
- [ ] AC-02: Inline note added to delegation close sequence explaining the two-phase write
- [ ] AC-03: execution_prompt.md version bumped; OPERATIONAL_GUIDE.md §14 Execution Engine Source updated; prompt_change_log.md entry appended (CLAUDE.md §6 checklist)
- [ ] AC-04: Head of Specs Team sign-off recorded in QA evidence

---

### ST-02 — execution_prompt.md STEP 3.2.B: explicit pr_status sync after PR open

**Backlog ref:** BLG-GOV-76
**Priority:** P3 (Low)
**Effort:** XS (~0.5 hr)
**Owner:** Head of Specs Team
**EXECUTION:** autonomous
**VERIFICATION:** document inspection (prompt patch applied and version-bumped)

**Acceptance Criteria:**
- [ ] AC-01: execution_prompt.md STEP 3.2.B updated — after recording `pr_number`, explicit step added: `gh pr view <pr_number> --json state` and update `pr_status` in execution_state.json immediately
- [ ] AC-02: EPIC.status update rule added — if PR is already merged at QA evidence commit time, update `EPIC.status` from `"done"` to `"merged"`
- [ ] AC-03: execution_prompt.md version bumped; OPERATIONAL_GUIDE.md §14 updated; prompt_change_log.md entry appended (CLAUDE.md §6 checklist)
- [ ] AC-04: Head of Specs Team sign-off recorded in QA evidence

---

### ST-03 — execution_prompt.md: verification-class sub-criterion for pre-planning sprints

**Backlog ref:** BLG-GOV-77
**Priority:** P3 (Low)
**Effort:** XS (~0.5 hr)
**Owner:** Head of Specs Team
**EXECUTION:** autonomous
**VERIFICATION:** document inspection (prompt patch applied and version-bumped)

**Acceptance Criteria:**
- [ ] AC-01: execution_prompt.md §3.2.A autonomous class sign-off block updated with verification-class sub-criterion: "If all stories' VERIFICATION is by document inspection only, criterion 1 of BLG-GOV-19 autonomous class may be satisfied if criteria 2/3/4 are met"
- [ ] AC-02: Scope note added: applies to pre-planning sprint patterns only (EXECUTION=delegated_decision/delegated_backend, VERIFICATION=document inspection)
- [ ] AC-03: execution_prompt.md version bumped; OPERATIONAL_GUIDE.md §14 updated; prompt_change_log.md entry appended (CLAUDE.md §6 checklist)
- [ ] AC-04: Head of Specs Team sign-off recorded in QA evidence

---

### ST-04 — execution_prompt.md: spec_references policy for documentation-creation stories

**Backlog ref:** BLG-GOV-70
**Priority:** P3 (Low) [stale — AUD-003 mandates entry]
**Effort:** XS (~0.5 hr)
**Owner:** Head of Specs Team
**EXECUTION:** autonomous
**VERIFICATION:** document inspection (prompt patch applied and version-bumped)

**Acceptance Criteria:**
- [ ] AC-01: execution_prompt.md STEP 2 or STEP 3.1.A updated — policy note added: for documentation-creation stories (primary deliverable IS the spec file), `spec_references` may be set to the path of the created/updated artefact; empty `spec_references` is non-compliant except for this case
- [ ] AC-02: Policy note specifies: use `delivery_note` field to record artefact path when spec_references is not applicable
- [ ] AC-03: execution_prompt.md version bumped; OPERATIONAL_GUIDE.md §14 updated; prompt_change_log.md entry appended (CLAUDE.md §6 checklist)
- [ ] AC-04: Head of Specs Team sign-off recorded in QA evidence
- [ ] AC-05: BLG-GOV-70 archived from backlog (marking complete)

---

## EPIC-02 — Agent Header Standardization (S2-02)

**Owner:** Head of Specs Team
**Maps to:** S2-02
**Sprint:** Sprint 1
**Sequencing:** Parallel to EPIC-01; no dependencies
**Description:** Standardize 5 non-compliant agent file role headers to `**Role:**` format per AUD-2026-05-30-005. Resolves Stage 3 audit G1/G2 compliance gaps and enables automated role-line scanning.

---

### ST-05 — Standardize 5 agent file role headers

**Backlog ref:** AUD-2026-05-30-005
**Priority:** P2 (Medium)
**Effort:** S (~1 hr)
**Owner:** Head of Specs Team
**EXECUTION:** autonomous
**VERIFICATION:** document inspection (5 files updated, role headers match `**Role:**` format)

**Acceptance Criteria:**
- [ ] AC-01: `claude/agents/api_contracts_documentation_owner.md` — `## Role: API Contracts & Documentation Owner` replaced with `**Role:** API Contracts & Documentation Owner`
- [ ] AC-02: `claude/agents/backend_engineering_patterns_owner.md` — `**Owner:** Backend Engineering Patterns Owner` replaced with `**Role:** Backend Engineering Patterns Owner`
- [ ] AC-03: `claude/agents/data_model_domain_schema_owner.md` — `## Role: Data Model & Domain Schema Owner` replaced with `**Role:** Data Model & Domain Schema Owner`
- [ ] AC-04: `claude/agents/frontend_specs_ux_documentation_owner.md` — `## Role: Frontend Specifications & UX Documentation Owner` (or equivalent) replaced with `**Role:**` format
- [ ] AC-05: `claude/agents/metrics_definitions_analytics_owner.md` — `## Role: Metrics Definitions & Analytics Canonical Owner` replaced with `**Role:** Metrics Definitions & Analytics Canonical Owner`
- [ ] AC-06: All 5 files retain all other content unchanged
- [ ] AC-07: Head of Specs Team sign-off recorded in QA evidence

---

## EPIC-03 — SI-02 Spec Pre-Sprint Completion (S2-03) — Conditional

**Owner:** Head of Specs Team + Metrics Definitions & Analytics Canonical Owner + Data Model & Domain Schema Owner
**Maps to:** S2-03
**Sprint:** Sprint 2 (conditional)
**Gate condition:** Product Owner explicitly confirms SI-02 sprint planning is imminent before Sprint 2 seals. If gate not confirmed by sprint planning, EPIC-03 is deferred and sprint closes with Sprint 1 stories only.
**Description:** Complete remaining SI-02 pre-sprint spec work to enable SI-02 sprint planning. v4.4 completed all pre-design documents (BLG-BE-17/18/20/23, BLG-FE-52/53, BLG-QA-31). This EPIC covers the remaining gaps: §13 boundary review, metric definition, and data schema pre-definition.

---

### ST-06 — SI-02 §13 formal boundary review

**Backlog ref:** BLG-GOV-39
**Priority:** P1 (High)
**Effort:** S (~0.5 day)
**Owner:** Strategy Rules & System Intent Owner
**EXECUTION:** delegated_decision (Strategy Rules & System Intent Owner)
**VERIFICATION:** document inspection (§13 review document produced with PASS/FAIL determination)

**Gate condition:** PO confirmation that SI-02 sprint planning is imminent (inherited from EPIC-03).

**Acceptance Criteria:**
- [ ] AC-01: §13 review completed against SI-02 story set; determination: PASS or FAIL documented
- [ ] AC-02: Review confirms drift detection output is: deterministic, display-only, no automated recommendations
- [ ] AC-03: Binding conditions documented (e.g., "drift alerts are informational only; no automated position management")
- [ ] AC-04: Sign-off recorded in sprint planning artefact; Strategy Rules & System Intent Owner sign-off confirmed
- [ ] AC-05: If FAIL, escalation raised before Sprint 2 seals

---

### ST-07 — SI-02 drift detection score metric definition

**Backlog ref:** BLG-SPEC-41
**Priority:** P1 (High)
**Effort:** S (~1 day)
**Owner:** Metrics Definitions & Analytics Canonical Owner; Head of Specs Team
**EXECUTION:** delegated_decision (Metrics Definitions & Analytics Canonical Owner)
**VERIFICATION:** document inspection (metric definition document produced)

**Gate condition:** PO confirmation that SI-02 sprint planning is imminent (inherited from EPIC-03). Depends on ST-06 §13 PASS.

**Acceptance Criteria:**
- [ ] AC-01: Metric definition document produced covering: user-facing format (% deviation vs raw count vs index), rolling window, threshold bands (green/amber/red states), warning state triggers
- [ ] AC-02: SI-05 weekly digest integration points documented
- [ ] AC-03: Reviewed and signed off by Metrics Definitions & Analytics Canonical Owner and Head of Specs Team
- [ ] AC-04: Document filed at canonical spec path (e.g., `docs/specs/metrics/si02_drift_score.md`)

---

### ST-08 — SI-02 data schema pre-definition

**Backlog ref:** BLG-SPEC-37
**Priority:** P1 (High)
**Effort:** M (~1–2 days)
**Owner:** Data Model & Domain Schema Owner; Head of Specs Team
**EXECUTION:** delegated_decision (Data Model & Domain Schema Owner)
**VERIFICATION:** document inspection (data schema pre-definition document produced)

**Gate condition:** PO confirmation that SI-02 sprint planning is imminent (inherited from EPIC-03). Informed by ST-07 metric definition.

**Acceptance Criteria:**
- [ ] AC-01: All data fields required for SI-02 drift analysis identified
- [ ] AC-02: Current trade, position, and trade plan schemas compared; gap analysis produced
- [ ] AC-03: Missing fields enumerated with data types, tables affected, and migration complexity estimate
- [ ] AC-04: Data schema pre-definition document produced and filed (e.g., `docs/specs/data_model/si02_data_schema.md`)
- [ ] AC-05: Reviewed and signed off by Data Model & Domain Schema Owner and Head of Specs Team

---

<!-- release-plan-marker: RP:v4.5:2026-05-30__release-v4.5 -->
