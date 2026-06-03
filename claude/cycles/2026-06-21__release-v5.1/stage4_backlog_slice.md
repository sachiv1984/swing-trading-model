**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Cycle:** 2026-06-21__release-v5.1
**Release:** v5.1

---

# Backlog Slice — v5.1 SI-05 Phase 1 & Governance Debt

<!-- release-plan-marker: RP:v5.1:2026-06-21__release-v5.1 -->

---

## EPIC-01 — SI-05 Phase 1: Weekly Strategy Integrity Digest

**Maps to:** S2-01, S2-04  
**Owner:** Head of Backend Engineering; Head of Specs Team  
**Sequencing:** Merge after EPIC-02 (scope verification confirms SI-05 format before implementation)

---

### ST-01 — SI-05 Phase 1: Backend service + Telegram weekly digest implementation

**Source:** BLG-GOV-67  
**Effort:** M (~2–3 days)  
**Class:** Autonomous  
**Staging-only ACs:** AC-07 (Telegram delivery on staging)

**Description:**  
Implement the weekly Strategy Integrity Digest via Telegram (Phase 1 only — no SI-02 component). Uses existing SI-01 (pre-entry validation aggregate data) and SI-03 (red flag journal data) to generate a weekly summary. Format specified in BLG-GOV-86 (Telegram message format spec, shipped v5.0). Deliver via existing Telegram notification infrastructure (v2.4 weekly digest pattern). Confirm financial reporting scope from BLG-SPEC-45 before implementation seals.

**Acceptance Criteria:**
1. Weekly digest message generated using SI-01 `validation_pass_rate` + `override_count` and SI-03 `red_flag_events` frequency trend data
2. Message formatted per BLG-GOV-86 Telegram format spec — section structure, character limits, data field mapping to SI-01/SI-03 endpoint responses
3. Telegram delivery confirmed via existing weekly digest infrastructure (v2.4 pattern)
4. No SI-02 dependency in Phase 1 implementation
5. New endpoint/scheduled trigger documented in `docs/specs/api_contracts/` and `docs/reference/openapi.yaml` in same commit (CLAUDE.md §2)
6. Endpoint registered in `backend/routers/test.py` in same commit (CLAUDE.md §2); `SystemStatus.js` fallback count updated; `SC-SS-01b` in `tests/e2e/system-status.spec.js` updated
7. Unit tests cover: digest generation (data present), empty/zero data state (no red flags, 100% pass rate), Telegram message format compliance (section order, character limit)
8. SI-05 Phase 1 gate confirmed: SI-01 + SI-03 live ≥ 30 days (PMO Lead verification at sprint planning)
9. `**Staging-only ACs:**` Telegram message received and formatted correctly on staging — Infrastructure & Operations Owner sign-off required

---

### ST-02 — BLG-SPEC-45: SI-05 financial reporting scope verification

**Source:** BLG-SPEC-45 (gate: BLG-GOV-86 shipped v5.0 — gate cleared)  
**Effort:** XS (~1 hour)  
**Class:** Autonomous  
**Staging-only ACs:** None

**Description:**  
Review BLG-GOV-86 (SI-05 Telegram message format spec, shipped v5.0) to determine whether financial performance reporting scope was explicitly addressed. If covered: document the decision and close BLG-SPEC-45. If not covered: define a brief supplementary spec clarifying whether weekly financial summary is in or out of scope for Phase 1.

**Acceptance Criteria:**
1. BLG-GOV-86 reviewed; financial reporting scope question explicitly answered (in scope / out of scope for Phase 1)
2. Scope decision documented in a brief verification note
3. If supplementary spec needed: spec document produced before ST-01 sprint planning seals
4. Financial Reporting & Records Owner sign-off on scope decision
5. BLG-SPEC-45 marked COMPLETE or escalated with outstanding decision

---

## EPIC-02 — Governance Patch: Delivery Verification §-1.3 Tier 2 Fix

**Maps to:** S2-02  
**Owner:** Head of Specs Team  
**Sequencing:** Independent; first in merge order

---

### ST-03 — delivery_verification_prompt.md §-1.3 Tier 2: agent-mediated signer format acceptance

**Source:** LL-RP-v5.0-D-2 (lessons_learnt_closure.md 2026-06-03__release-v5.0)  
**Effort:** S (~0.5 day)  
**Class:** Autonomous  
**Staging-only ACs:** None

**Description:**  
EPIC-03 in v5.0 used an agent-mediated DoQ sign-off ("Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)"). This format is not enumerated in delivery_verification_prompt.md §-1.3 Tier 2, causing a recurring Tier 2 advisory for any future mixed-class EPIC. Add an explicit clause accepting this format, preventing recurrence. Apply CLAUDE.md §6 governance file edit checklist in full.

**Acceptance Criteria:**
1. delivery_verification_prompt.md §-1.3 Tier 2 updated — new clause: `"Sprint Execution Engine (agent-mediated, <Role Name> role — §X.Y)" is accepted for mixed-class EPICs as equivalent to agent-mediated sign-off with named role`
2. Version bumped (v2.9→v3.0 or next appropriate increment)
3. OPERATIONAL_GUIDE.md updated: §9 source prompt header + §14 Verification Engine Source version + §14 Version/Last Updated
4. `prompt_change_log.md` entry appended with date, filename, version transition, change summary, authority
5. Head of Specs Team sign-off

---

## EPIC-03 — QA & Documentation Debt Clearance

**Maps to:** S2-03, S2-05, S2-06  
**Owner:** QA Lead; Director of Quality; PMO Lead  
**Sequencing:** Independent; merge alongside EPIC-02

---

### ST-04 — BLG-FE-61: SignalCard allocation_insufficient badge Playwright E2E coverage

**Source:** BLG-FE-61 (Provisional-Target: v5.1 firm; carry-forward LL-RP-v5.0-CF-1)  
**Effort:** XS (<1 hour)  
**Class:** Autonomous  
**Staging-only ACs:** None

**Description:**  
Add Playwright E2E test for the observable AC deferred from v5.0 EPIC-03 ST-06: SignalCard orange "Cannot Size" badge + reason inline when signal status = `allocation_insufficient`. Code review was accepted for the v5.0 PR under the CLAUDE.md §2 hard gate, but a Playwright scenario must be authored before v5.1 sprint planning seals.

**Acceptance Criteria:**
1. Playwright test added to an appropriate `tests/e2e/` spec file
2. Test mocks a signal payload with `status: "allocation_insufficient"` and a non-empty `reason` string
3. Assertions: (a) orange "Cannot Size" badge is visible, (b) reason text rendered inline on signal card, (c) signal is visually distinct from `status: "active"` signals
4. Test passes in CI

---

### ST-05 — BLG-QA-43: compliance_summary field population validation

**Source:** BLG-QA-43 (Provisional-Target: v5.1 or spot-check)  
**Effort:** XS (~1–2 hours)  
**Class:** Autonomous  
**Staging-only ACs:** AC-01 (requires staging/production environment)

**Description:**  
Verify that the `compliance_summary` field in `GET /reports/monthly-pnl` (shipped v4.7) is populated from Arc5ComplianceSection data and matches what is displayed there. A mismatch would be a silent data quality issue.

**Acceptance Criteria:**
1. `**Staging-only ACs:**` Verification performed against staging or production monthly P&L output — Infrastructure & Operations Owner sign-off
2. All 5 Arc 5 compliance metrics (validation_pass_rate, override_count, red_flag_events_count, most_frequent_rule_breach, top_rule_breach) confirmed present in compliance_summary
3. Values match Arc5ComplianceSection display for the same period
4. Verification result documented; any mismatch filed immediately as a P2 bug item with BLG prefix

---

### ST-06 — BLG-GOV-89: Staged verification sprint protocol document

**Source:** BLG-GOV-89 (Provisional-Target: v5.1 or v5.2; pattern validated v4.7 + v5.0)  
**Effort:** S (~0.5 day)  
**Class:** Autonomous  
**Staging-only ACs:** None

**Description:**  
Document the staged verifications sprint pattern: batch-closing staging-only ACs from prior releases in a dedicated sprint. Validated at v4.7 (first use: BLG-OPS-28/44/45) and confirmed at v5.0 (BLG-OPS-52). File in `docs/operations/` or `docs/governance/`.

**Acceptance Criteria:**
1. Protocol document produced covering: (a) trigger conditions (when to declare a "staged verifications" sprint vs inline), (b) batching approach (how to group deferred staging ACs), (c) evidence format (DoQ sign-off requirements), (d) sprint sizing note (how to estimate effort for verification-only stories)
2. Document filed in `docs/operations/staged_verification_sprint_protocol.md` (or `docs/governance/`)
3. Director of Quality sign-off recorded
4. PMO Lead sign-off recorded
