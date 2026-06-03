**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Sealed
**Last Updated:** 2026-06-03
**Cycle:** 2026-06-03__release-v5.0
**Release:** v5.0
**Sprint Goal:** Close all five AUD-2026-06-02 governance open items, ship the two v4.9 slipped product correctness fixes (FEAT-43, BE-25), and deliver the full SI-05 Phase 1 pre-work documentation suite.
**Backlog Slice Source:** original stage4_backlog_slice.md

---

# Sprint Backlog — 2026-06-03__release-v5.0

## Sprint Scope

### Merge Order

**EPIC-01 → EPIC-02 → EPIC-03 → EPIC-04**

- `execution_state.json` owner: **EPIC-01** (first in execution order)
- EPIC-02/03/04 must check for `execution_state.json` existence before creating their own version; append their EPIC section rather than overwrite
- Shared files: `prompt_change_log.md` (EPIC-01 owns; EPIC-02 rebases after EPIC-01 merges); `backlog.md` (EPIC-03 owns; EPIC-04 rebases after EPIC-03 merges)

---

### EPIC-01 — Governance Document Patches

**Maps to:** S2-01
**Owner:** Head of Specs Team
**Estimated effort:** ~7 hrs (S+S+XS)
**Risk IDs:** RISK-03
**Execution sequence:** 1st

#### ST-01 — Verify and append any missing prompt_change_log.md entries (BLG-GOV-79)

**Owner:** Head of Specs Team
**Estimated effort:** S (~2 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-01`

*(The Execution Engine reads AC from `stage4_backlog_slice.md` directly via `spec_references`. Do not duplicate the full AC table here.)*

**Dependencies:** None

**Notes:** RISK-03 advisory — all 7 target entries may already be present (added as Tier 1 during AUD-2026-06-02). ST-01 verifies first; appends only if gaps confirmed. Story outcome may be verification-only.

**Staging-only ACs:** None

---

#### ST-02 — Fix 5 non-standard agent file headers (BLG-GOV-81)

**Owner:** Head of Specs Team
**Estimated effort:** S (~2.5 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-02`

**Dependencies:** None

**Notes:** Affected files: `ai_compliance_governance_officer.md`, `cybersecurity_trust_lead.md`, `director_of_hr.md`, `financial_reporting_records_owner.md`, `finops_resource_architect.md`. Format correction only — ATX heading + Role field.

**Staging-only ACs:** None

---

#### ST-03 — Add PO acceptance = GitHub Approve note to PR template (BLG-GOV-83)

**Owner:** Director of Quality
**Estimated effort:** XS (~1 hr)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-03`

**Dependencies:** None

**Notes:** Edit `.github/pull_request_template.md` — add explicit note in QA Evidence or PO Acceptance section.

**Staging-only ACs:** None

---

### EPIC-02 — Governance Engine Structural Fixes

**Maps to:** S2-02
**Owner:** Head of Specs Team
**Estimated effort:** ~12 hrs (M+M)
**Risk IDs:** RISK-01
**Execution sequence:** 2nd (after EPIC-01 merges — `prompt_change_log.md` append order)

#### ST-04 — Add governance file edit check to execution_prompt.md STEP 8 commit (BLG-GOV-80)

**Owner:** Head of Specs Team
**Estimated effort:** M (~5 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-04`

**Dependencies:** After EPIC-01 merges (prompt_change_log.md rebase)

**Notes:** EPIC-02 branch must rebase onto main after EPIC-01 merges before committing ST-04 changes to `prompt_change_log.md`. This is the root-cause fix for BLG-GOV-79 (missing change log entries): adds a structural check to STEP 8 of the execution engine.

**Staging-only ACs:** None

---

#### ST-05 — Strengthen post-ship audit advisory + add last_audit_cycle_count to state schema (BLG-GOV-82)

**Owner:** Head of Specs Team / PMO Lead
**Estimated effort:** M (~6 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-05`

**Dependencies:** None (within EPIC-02; independent of ST-04)

**Notes:** RISK-01 — backward-compatible nullable field; null handling defined in AC. Schema evolution for `lifecycle_schema.json` included.

**Staging-only ACs:** None

---

### EPIC-03 — Product Correctness & Ops

**Maps to:** S2-03
**Owner:** Head of Backend Engineering
**Estimated effort:** ~7 hrs (S+S+XS)
**Risk IDs:** None
**Execution sequence:** 3rd (after EPIC-02 merges)

#### ST-06 — allocation_insufficient signal status and inline explanation (BLG-FEAT-43)

**Owner:** Head of Backend Engineering
**Estimated effort:** S (~3 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-06`

**Dependencies:** None

**Notes:** Backend: new status value `allocation_insufficient` + `reason` field. Frontend: inline display on signal card when status = allocation_insufficient, visually distinct from `new`/`watchlisted`. openapi.yaml + backend/routers/test.py + SC-SS-01b e2e test must all be updated in same commit per CLAUDE.md §2.

**Staging-only ACs:** None

---

#### ST-07 — Pre-entry regime gate fix: use shared market status (BLG-BE-25)

**Owner:** Head of Backend Engineering
**Estimated effort:** S (~3 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-07`

**Dependencies:** None

**Notes:** Backend-only fix. `_check_regime()` must use shared cache (5-min TTL minimum). Eliminates independent `yf.download` call from `/portfolio/pre-entry-validation`.

**Staging-only ACs:** None

---

#### ST-08 — Anthropic SDK staging verification (BLG-OPS-52)

**Owner:** Infrastructure & Operations Owner
**Estimated effort:** XS (~1 hr)
**Delegation class:** delegated_qa

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-08`

**Dependencies:** None (staging environment must be live post v4.9 deploy)

**Notes:** Verification-only story — no code to write. Both ACs require human staging run against the live staging environment. Infrastructure & Operations Owner must run the staging checks and record sign-off with verification date. EPIC-03 branch after staging sign-off: close BLG-OPS-52 in backlog.md and commit sign-off record.

**Staging-only ACs:** ST-08-AC-01 (POST /trade-plans/{plan_id}/generate-thesis HTTP 200 + non-null thesis on staging), ST-08-AC-02 (POST /ai/check-daily-cost HTTP 200 + expected cost structure on staging)

---

### EPIC-04 — SI-05 Phase 1 Pre-work

**Maps to:** S2-04 (firm), S2-05 (conditional Sprint 2)
**Owner:** Product Owner / Head of Specs Team
**Estimated effort:** ~15 hrs firm (5×S) + ~6 hrs conditional (ST-14, M)
**Risk IDs:** RISK-02
**Execution sequence:** 4th (after EPIC-03 merges — `backlog.md` rebase)

#### ST-09 — SI-05 notification channel trade-off document (BLG-FE-60)

**Owner:** Product Owner / Head of UX & Design
**Estimated effort:** S (~3 hrs)
**Delegation class:** delegated_decision

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-09`

**Dependencies:** None (first story in EPIC-04; ST-10 depends on this)

**Notes:** Engine produces trade-off analysis document (Telegram vs in-app). PO must record explicit channel decision in the document. ST-10 depends on this decision — execution engine must complete ST-09 and receive PO channel confirmation before beginning ST-10. LL-v2.2-SP-01 advisory: no HoST design artefact found; a HoST design session or channel review is recommended before sprint start (advisory only).

**Staging-only ACs:** None

---

#### ST-10 — SI-05 Phase 1 Telegram message format specification (BLG-GOV-86)

**Owner:** Head of Specs Team
**Estimated effort:** S (~3 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-10`

**Dependencies:** ST-09 (BLG-FE-60 must confirm Telegram channel before authoring)

**Notes:** If ST-09 confirms Telegram: engine authors full format spec per AC. If ST-09 confirms in-app: ST-10 scope shifts to in-app notification spec (per backlog slice note; PO to confirm scope at execution start of ST-10). PO + Head of Specs Team sign-off captured in document sign-off block.

**Staging-only ACs:** None

---

#### ST-11 — SI-02 frontend re-entry trigger criteria definition (BLG-GOV-87)

**Owner:** PMO Lead / Product Owner
**Estimated effort:** S (~3 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-11`

**Dependencies:** None

**Notes:** Criteria document formalises re-entry conditions for SI-02 feature gate. PMO Lead acknowledgement of periodic check cadence (v5.1 earliest, 2026-09) is required in the document.

**Staging-only ACs:** None

---

#### ST-12 — SI-04 formal binding conditions decisions document (BLG-GOV-88)

**Owner:** Strategy Rules & System Intent Owner
**Estimated effort:** S (~3 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-12`

**Dependencies:** None

**Notes:** Formalises 6 binding conditions from `docs/product/ux/si04_section13_preassessment.md`. Cross-reference BLG-SPEC-43 (SI-04 API contract).

**Staging-only ACs:** None

---

#### ST-13 — SI-02 drift summary feasibility assessment (BLG-BE-26)

**Owner:** Product Owner
**Estimated effort:** S (~3 hrs)
**Delegation class:** autonomous

**Acceptance Criteria:** see `stage4_backlog_slice.md#ST-13`

**Dependencies:** None

**Notes:** Assessment-only scope. Engine produces feasibility document covering UX risk evaluation. PO sign-off on assessment outcome closes BLG-BE-26 (or scopes update based on outcome).

**Staging-only ACs:** None

---

## Capacity Summary

| Metric | Value |
|--------|-------|
| Total confirmed capacity | ~40–48 hrs (double) |
| Total estimated effort (Sprint 1 firm) | ~41 hrs |
| Utilisation | ~85–100% |
| Over-allocation | No |

## Items Deferred This Sprint

| Item | EPIC | Reason |
|------|------|--------|
| ST-14 — SI-05 Phase 1 implementation (BLG-GOV-67) | EPIC-04 | Gate condition: SI-01 + SI-03 live ≥ 30 days; clears 2026-06-21. Sprint 2 conditional via amendment cycle. |

## Outstanding Actions at Planning Seal

| Action | Owner | Blocker? |
|--------|-------|---------|
| Populate `design_gate_bypass_authority = "Head of UX & Design + Product Owner"` and `design_gate_bypass_reason` in `.claude_current_state.json` (IMP-04 / IMP-30) | Head of UX & Design + Product Owner | Yes |
| ST-09 EPIC-04 HoST design session / channel review advisory (LL-v2.2-SP-01) | Head of Specs Team | No — advisory only |

---

## Product Owner Sign-Off

**Sprint goal confirmed:** Confirmed
**Scope confirmed:** Confirmed
**Capacity confirmed:** Confirmed
**Deferred execution blockers accepted (if any):** N/A
**Signed off by:** Product Owner
**Date:** 2026-06-03
