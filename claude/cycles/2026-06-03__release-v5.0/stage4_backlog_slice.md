**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Published
**Cycle:** 2026-06-03__release-v5.0
**Release:** v5.0
**Published:** 2026-06-03

---

# Release Backlog Slice — v5.0

**Theme:** Governance Hardening, Product Correctness & SI-05 Phase 1 Pre-work
**Stories:** 13 firm + 1 conditional = 14 total
**Sprints:** 1 firm + 1 conditional (gate 2026-06-21)

---

## EPIC-01: Governance Document Patches

Maps to: S2-01
Owner: Head of Specs Team
Merge order: 1st

### ST-01 — Verify and append any missing prompt_change_log.md entries (BLG-GOV-79)

**EPIC:** EPIC-01
**Effort:** S
**Source:** BLG-GOV-79 (AUD-2026-06-02 AUD-001)
**Staging-only ACs:** None

**Acceptance Criteria**
- Verify the 7 entries specified in BLG-GOV-79 are present in prompt_change_log.md: delivery_verification_prompt.md v2.7→v2.8, post_ship_closure.md v2.11→v2.12, execution_prompt.md v3.33→v3.34, release_planning_prompt.md v2.32→v2.33, roadmap_prompt.md v6.6→v6.7, roadmap_prompt.md v6.7→v6.8, execution_prompt.md v3.34→v3.35
- Append any entries found missing (in reverse-chronological order, newest first)
- Each entry has correct fields: Date, Prompt path, Version transition, Change summary, Authority
- Verify no additional prompt version changes in cycles 31–35 are unlogged beyond the 7 specified
- AUD-2026-06-02 AUD-001 gap confirmed closed (or documented as already closed if all 7 entries present)

---

### ST-02 — Fix 5 non-standard agent file headers (BLG-GOV-81)

**EPIC:** EPIC-01
**Effort:** S
**Source:** BLG-GOV-81 (AUD-2026-06-02 AUD-004; 2nd carry from AUD-2026-05-30-005)
**Staging-only ACs:** None

Affected files:
- `claude/agents/ai_compliance_governance_officer.md`
- `claude/agents/cybersecurity_trust_lead.md`
- `claude/agents/director_of_hr.md`
- `claude/agents/financial_reporting_records_owner.md`
- `claude/agents/finops_resource_architect.md`

**Acceptance Criteria**
- Each of the 5 files uses `# Name` ATX heading (not setext `Name\n====`)
- Each of the 5 files has `**Role:** Name` with no trailing backslash
- Format consistent with the other 18 agent files in claude/agents/
- All other agent files remain unchanged
- Head of Specs Team sign-off

---

### ST-03 — Add PO acceptance = GitHub Approve note to PR template (BLG-GOV-83)

**EPIC:** EPIC-01
**Effort:** XS
**Source:** BLG-GOV-83 (AUD-2026-06-02 AUD-006; v4.9 D-3 first occurrence)
**Staging-only ACs:** None

**Acceptance Criteria**
- `.github/pull_request_template.md` contains explicit note: PO acceptance must be submitted as a GitHub "Approve review" action, not a PR comment
- Note is visible in the QA Evidence or PO Acceptance section of the PR template
- Note visible to any reviewer who opens the PR
- Director of Quality sign-off

---

## EPIC-02: Governance Engine Structural Fixes

Maps to: S2-02
Owner: Head of Specs Team
Merge order: 2nd (after EPIC-01)

### ST-04 — Add governance file edit check to execution_prompt.md STEP 8 commit (BLG-GOV-80)

**EPIC:** EPIC-02
**Effort:** M
**Source:** BLG-GOV-80 (AUD-2026-06-02 AUD-003; root cause of BLG-GOV-79)
**Staging-only ACs:** None

**Acceptance Criteria**
- execution_prompt.md STEP 8 (before commit step) includes governance file edit check: scans git diff --name-only for modified files in `claude/system/`, `claude/charter/`, `claude/agents/`; for each modified governance file, verifies prompt_change_log.md entry exists; appends if missing before proceeding
- Check is STRUCTURAL — not reliant on operator memory
- execution_prompt.md bumped v3.35→v3.36
- OPERATIONAL_GUIDE.md §8 source prompt header updated v3.35→v3.36
- OPERATIONAL_GUIDE.md §14 Execution Engine Source updated v3.35→v3.36
- OPERATIONAL_GUIDE.md version bumped per CLAUDE.md §6 governance file edit checklist
- prompt_change_log.md entry appended for execution_prompt.md v3.35→v3.36
- Head of Specs Team sign-off

---

### ST-05 — Strengthen post-ship audit advisory + add last_audit_cycle_count to state schema (BLG-GOV-82)

**EPIC:** EPIC-02
**Effort:** M
**Source:** BLG-GOV-82 (AUD-2026-06-02 AUD-005)
**Staging-only ACs:** None

**Acceptance Criteria**
- post_ship_closure.md STEP 0 fires AUDIT DUE if `completed_cycle_count % 3 == 0` OR `(completed_cycle_count - last_audit_cycle_count) >= 4`
- `last_audit_cycle_count` field added to `.claude_current_state.json` (set at each post-ship closure when audit runs)
- `claude/system/schemas/lifecycle_schema.json` updated if it defines the state schema (add last_audit_cycle_count field)
- post_ship_closure.md version bumped (v2.12→v2.13)
- OPERATIONAL_GUIDE.md §10 source prompt header updated
- OPERATIONAL_GUIDE.md §14 Post-Ship Closure Engine updated
- OPERATIONAL_GUIDE.md version bumped per CLAUDE.md §6
- prompt_change_log.md entry appended for post_ship_closure.md version change
- Head of Specs Team + PMO Lead sign-off

---

## EPIC-03: Product Correctness & Ops

Maps to: S2-03
Owner: Head of Backend Engineering
Merge order: 3rd

### ST-06 — allocation_insufficient signal status and inline explanation (BLG-FEAT-43)

**EPIC:** EPIC-03
**Effort:** S
**Source:** BLG-FEAT-43 (PO direction 2026-06-02; slipped v4.9)
**Staging-only ACs:** None

**Acceptance Criteria**
- Backend: signal with `price_gbp > allocation_gbp` has status `"allocation_insufficient"` (not `"new"`)
- Backend: a human-readable `reason` string is returned (e.g. "1 share (£1,259) exceeds position allocation (£1,147) — cannot size")
- Frontend: reason string displayed inline on signal card/row when status is `"allocation_insufficient"`
- Frontend: `allocation_insufficient` signals are visually distinct from `new` / `watchlisted` signals
- Existing signals with status `"new"` and `suggested_shares > 0` unaffected
- No change to `already_held` or `watchlisted` status logic
- New `allocation_insufficient` status value registered in endpoint test suite
- openapi.yaml updated with new status enum value and reason field
- New EPIC-03 backend route or updated endpoint registered in `backend/routers/test.py`
- SC-SS-01b in `tests/e2e/system-status.spec.js` updated if endpoint count changes

---

### ST-07 — Pre-entry regime gate fix: use shared market status (BLG-BE-25)

**EPIC:** EPIC-03
**Effort:** S
**Source:** BLG-BE-25 (user-reported 2026-06-02; slipped v4.9)
**Staging-only ACs:** None

**Acceptance Criteria**
- `_check_regime()` in `pre_entry_validation.py` does not call `check_market_regime()` directly; uses shared market status cache or `GET /market/status` result instead
- Server-side cache (5-minute TTL minimum) added to `check_market_regime()` so all callers share one result per window
- Dashboard regime and pre-entry regime gate agree when called within the same session
- No spurious `risk_off` failures when SPY is clearly above its 200MA per the dashboard
- `/portfolio/pre-entry-validation` does not trigger an independent `yf.download` call
- Unit tests updated/added covering the shared-cache path
- No regression in existing pre-entry validation tests

---

### ST-08 — Anthropic SDK staging verification (BLG-OPS-52)

**EPIC:** EPIC-03
**Effort:** XS
**Source:** BLG-OPS-52 (v4.9 ST-02 AC-04 deferred staging gate)
**Staging-only ACs:** ST-08-AC-01, ST-08-AC-02 [staging-only evidence]

**Acceptance Criteria**
- [staging-only evidence] ST-08-AC-01: POST /trade-plans/{plan_id}/generate-thesis returns HTTP 200 with non-null thesis field on staging environment post v4.9 deploy
- [staging-only evidence] ST-08-AC-02: POST /ai/check-daily-cost returns HTTP 200 with expected cost structure on staging post SDK upgrade
- Infrastructure & Operations Owner sign-off recorded with staging verification date
- BLG-OPS-52 closed in backlog

---

## EPIC-04: SI-05 Phase 1 Pre-work

Maps to: S2-04 (firm), S2-05 (conditional Sprint 2)
Owner: Product Owner / Head of Specs Team
Merge order: 4th (after EPIC-03)
Sprint 2 gate: 2026-06-21 (SI-01 + SI-03 live ≥ 30 days)

### ST-09 — SI-05 notification channel trade-off document (BLG-FE-60)

**EPIC:** EPIC-04
**Effort:** S
**Source:** BLG-FE-60 (Provisional-Target: v5.0; sequencing constraint: must complete before BLG-GOV-67 sprint planning seals)
**Staging-only ACs:** None

**Acceptance Criteria**
- Trade-off document produced comparing: Telegram push (existing infra v2.4, character limit constraints, no in-app UX) vs in-app notification (new build, integrated, discoverable)
- Evaluation covers: implementation effort, user discovery, format flexibility, alignment with v2.4 weekly digest pattern
- PO channel decision explicitly recorded in document
- If Telegram confirmed: channel decision note fed to BLG-GOV-86 (ST-10 input)
- Document filed at `docs/product/decisions/` or `docs/product/ux/`
- Product Owner + Head of UX & Design review recorded
- BLG-FE-60 closed in backlog

---

### ST-10 — SI-05 Phase 1 Telegram message format specification (BLG-GOV-86)

**EPIC:** EPIC-04
**Effort:** S
**Source:** BLG-GOV-86 (Provisional-Target: v5.0; depends on BLG-FE-60 confirming Telegram)
**Staging-only ACs:** None
**Depends on:** ST-09 (BLG-FE-60 must confirm Telegram before authoring)

**Acceptance Criteria**
- Message format specification document covers: character limit compliance strategy; section structure (opening summary, Red Flag count, compliance score trend, key rule breach, review recommendation); data field definitions mapping SI-01 and SI-03 endpoint responses to each section; weekly frequency; failure modes when data unavailable
- Telegram character limits verified not exceeded by the specified format
- Product Owner and Head of Specs Team sign-off recorded
- Document filed in `docs/product/` or `claude/` appropriate location
- Gate condition (BLG-FE-60 confirmed Telegram) verified
- BLG-GOV-86 closed in backlog

*If ST-09 selects in-app notification: ST-10 scope shifts to in-app notification spec. PO to confirm scope at sprint planning.*

---

### ST-11 — SI-02 frontend re-entry trigger criteria definition (BLG-GOV-87)

**EPIC:** EPIC-04
**Effort:** S
**Source:** BLG-GOV-87 (Provisional-Target: v5.0)
**Staging-only ACs:** None

**Acceptance Criteria**
- Formal re-entry criteria document produced defining: hard gate (≥ 20 closed trades with linked trade_plans confirmed by PMO Lead via production database query); soft advisory (drift score data accumulation ≥ 3 months qualitative signal); formal trigger (PMO Lead runs re-entry check at each release planning kickoff starting 2026-09-01)
- Document filed in `claude/roadmap/` or `docs/product/decisions/`
- PMO Lead acknowledges ownership of the periodic check
- Product Owner confirms criteria are the intended re-entry conditions
- Check cadence noted: v5.1 release planning (2026-09 earliest)
- BLG-GOV-87 closed in backlog

---

### ST-12 — SI-04 formal binding conditions decisions document (BLG-GOV-88)

**EPIC:** EPIC-04
**Effort:** S
**Source:** BLG-GOV-88 (Provisional-Target: v5.0; formalises si04_section13_preassessment.md)
**Staging-only ACs:** None

**Acceptance Criteria**
- SI-04 §13 compliance decisions document created in `docs/product/decisions/`
- All 6 binding conditions from `docs/product/ux/si04_section13_preassessment.md` reproduced in the decisions document
- Formal sign-off block included per document_lifecycle_guide.md
- BLG-SPEC-43 (SI-04 API contract) cross-referenced
- Strategy Rules & System Intent Owner formal sign-off recorded
- Document class and status set per document_lifecycle_guide.md
- BLG-GOV-88 closed in backlog

---

### ST-13 — SI-02 drift summary feasibility assessment (BLG-BE-26)

**EPIC:** EPIC-04
**Effort:** S
**Source:** BLG-BE-26 (Provisional-Target: v5.0 conditional on assessment outcome)
**Staging-only ACs:** None

**Acceptance Criteria**
- Assessment document produced covering: feasibility of adding read-only drift summary to System Status or Reports page; UX risk evaluation (drift scores with sufficient context/framing/threshold calibration advisory/§13 disclosure)
- If feasible and UX risk manageable: minimal display scope defined (which metrics, where displayed, what framing text) — sprint planning ready
- If UX risk too high: outcome documented as "assess only — not implemented" and item closed with rationale
- Product Owner reviews and signs off on assessment outcome
- Document filed at appropriate location
- BLG-BE-26 closed or scope updated based on assessment outcome

---

## EPIC-04 Sprint 2 — Conditional Story (gate 2026-06-21)

### ST-14 — SI-05 Phase 1 implementation (BLG-GOV-67) [CONDITIONAL]

**EPIC:** EPIC-04
**Sprint:** 2 (conditional; gate: SI-01 + SI-03 live ≥ 30 days; clears 2026-06-21)
**Effort:** M
**Source:** BLG-GOV-67 (gate 2026-06-21)
**Staging-only ACs:** None

**Acceptance Criteria**
- Weekly strategy integrity digest implemented using SI-01 + SI-03 data only (no SI-02 component)
- Metrics delivered: validation_pass_rate, override_count, red_flag_frequency_trend
- Delivery channel: Telegram notification (per ST-09 channel decision) or as confirmed by PO
- Message format conforms to ST-10 specification
- Scheduled weekly trigger integrated with existing Telegram digest infrastructure (v2.4)
- Endpoint or service code implemented and tested
- No SI-02 dependency in Phase 1 implementation
- Gate condition (SI-01 + SI-03 live ≥ 30 days = 2026-06-21) verified by PMO Lead before sprint 2 planning seals
- BLG-GOV-67 closed in backlog

---

*Release Slice marker: <!-- release-plan-marker: RP:v5.0:2026-06-03__release-v5.0 -->*
