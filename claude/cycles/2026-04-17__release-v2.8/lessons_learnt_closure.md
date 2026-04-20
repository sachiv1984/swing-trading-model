# Lessons Learnt — Post-Ship Closure

Feature / Trigger: v2.8 — Frontend Completion, Test Quality & AI Journal Feature
Run: 2026-04-17__release-v2.8
Reviewed by: PMO Lead
Date filed: 2026-04-20
Prior cycle checked: 2026-04-13__release-v2.7 (lessons_learnt_closure.md loaded — recurrence check complete)

---

## What worked well

- **All 8 stories completed at 1.00 velocity** — no delegation blocks, no returned items, no deferred stories. Sprint goal fully met, cleanest execution record since v2.4.
- **Three prior-cycle friction items closed as sprint stories** — CF-1 (DoQ Date field), CF-2 (deviation terminology), BLG-GOV-13 (backlog archive dedup) all shipped as EPIC-03 stories. The carry-forward mechanism converted Phase 4 observations directly into sprint scope.
- **First AI feature (EPIC-04) delivered within §13 boundary** — Strategy Rules owner sign-off process worked as designed; SRB-v1.7 conditions verified independently at QA and delivery verification. No compliance incidents.
- **Playwright test suite consolidated to single VM** — 3 separate CI jobs merged into one; total e2e coverage (risk-dashboard, chart-interactivity, market-correlation) running in 1 consolidated job; 24/24 tests green on first clean run after consolidation.

---

## Friction Log

---

### Friction Item 1

**Classification:** Type A — Governance Drift: a required lifecycle field (Version: header) was absent from a governed template file.

**Recurrence:** No — first identification (Release Planning lessons_learnt.md 2026-04-17)

**What happened:**
`claude/system/gh_issue_template.md` was missing a lifecycle header (Owner, Class, Status, Version, Last Updated) required per Class 6 governance prompt standard. This was identified at Release Planning time and deferred as a v2.8 sprint advisory. It was not addressed during the sprint and carried to post-ship closure.

**Where in the routine:**
STEP 8 Lessons Learnt Review — Release Planning lessons_learnt.md deferred action.

**Root cause:** Template omission — lifecycle header requirement applies to all Class 6 documents; this file predates the formal Class 6 compliance enforcement.

**Blast radius analysis:**
- What would have propagated: File would be referenced without a version identifier; audit tooling cannot confirm document owner or compliance state without the header.
- When it would have surfaced: Next `run audit` or manual review.
- Recovery cost if uncaught: Low (single file header addition).

**Process patch:**
→ Immediate patch applied this run:
  - File: `claude/system/gh_issue_template.md`
  - Section: Top of file (new lifecycle header)
  - Change: Added Owner/Class/Status/Version/Last Updated header block; set to v1.0 Active.
  - Version: (none) → v1.0
  - Confirmed by: Head of Specs Team
  - Prompt change log entry: Yes — appended to claude/system/prompt_change_log.md (2026-04-20)

---

### Friction Item 2

**Classification:** Type A — Governance Drift: System_status_report.md had incorrect scenario counts and version number at delivery verification entry.

**Recurrence:** No — first identification for this specific document accuracy issue.

**What happened:**
System_status_report.md v2.8 section had been written with estimated counts (SC-CORR-01–09 as 9; SC-SIG-IND-01–08 as 8) rather than actual counts (4 and 2 respectively). The execution_prompt.md version reference was v3.5 rather than the actual shipped v3.7. These were caught and corrected at delivery verification (STEP 6).

**Where in the routine:**
STEP 6 Operational Documents Reconciliation — System_status_report.md cross-check.

**Root cause:** Process gap — system_status_report.md was written at sprint close with planned/estimated values rather than being updated to verified actual values after QA confirmed counts.

**Blast radius analysis:**
- What would have propagated: Incorrect system state record; any downstream tool reading system_status_report.md for capability counts would get wrong data.
- When it would have surfaced: Next manual review or `run audit`.
- Recovery cost if uncaught: Low (corrections are factual only; no system behaviour affected).

**Process patch:**
→ Immediate patch applied this run:
  - File: `docs/System_status_report.md`
  - Section: v2.8 sprint "Capabilities now live" table rows and "Verification inputs ready" section
  - Change: SC-CORR count corrected 9→4; SC-SIG-IND count corrected 8→2; execution_prompt.md version corrected v3.5→v3.7; test scenarios reference updated with Playwright evidence.
  - Version: N/A (operational record, no version bump)
  - Confirmed by: Director of Quality (delivery verification STEP 6)
  - Prompt change log entry: Not applicable — docs/System_status_report.md is an operational record, not a governed prompt.

---

### Friction Item 3

**Classification:** Type C — Dependency Stall: EPIC-01 required a Director of Quality counter-sign that was not completed at sprint close, creating a stall at delivery verification STEP -1.3.

**Recurrence:** No — prior cycle Phase 4 Obs 1 was about Date: field format (different issue). This is a new class: reclassified frontend EPICs creating an implicit counter-sign requirement not enforced at sprint close.

**What happened:**
EPIC-01 was reclassified from `delegated_frontend` to `autonomous` per LL-v2.3-EX-02 (engine completed). Sprint_close.md listed "Sprint Execution Engine (autonomous class)" as sign-off authority. However, EPIC-01 had frontend changes (MarketCorrelationSection.js) — which means the autonomous class criteria (no frontend-visible change) was not fully met at the story level. The delivery verification STEP -1.3 Tier 2 check caught this and required a Director of Quality counter-sign, which was added 2026-04-20. The stall was brief (same session) but required mid-verification remediation.

**Where in the routine:**
Phase 4 STEP -1.3 QA evidence two-tier sign-off check.

**Root cause:** Process gap — the `delegated_frontend → autonomous` reclassification path in execution_prompt.md does not explicitly note that a Director of Quality counter-sign is required when frontend changes are present. The autonomous class exception (BLG-GOV-19) requires all four criteria met at EPIC level; a reclassified story with frontend output creates a gap.

**Blast radius analysis:**
- What would have propagated: Without counter-sign, delivery verification would have halted at STEP -1.3 Tier 2.
- When it would have surfaced: STEP -1.3 in every future verification run involving a reclassified frontend EPIC.
- Recovery cost if uncaught: Medium — would require a Director of Quality session to provide the sign-off before verification could proceed.

**Process patch:**
→ Deferred patch (cannot apply this run without Head of Specs Team session for execution_prompt.md):
  - File: `claude/system/execution_prompt.md`
  - Section: §3.2.A reclassification note (near LL-v2.3-EX-02 reference)
  - Change required: Add note: when a `delegated_frontend` story is reclassified to `autonomous` per LL-v2.3-EX-02 but the EPIC contains frontend-visible changes, the autonomous class DoQ criteria (criterion 3: no frontend-visible change) is not fully met at EPIC level — Director of Quality counter-sign required in addition to engine sign-off. Record this in the sprint_close.md QA sign-off table.
  - Owner: Head of Specs Team
  - Target: v2.9 planning sprint or next cycle touching execution_prompt.md

---

### Friction Item 4

**Classification:** Type C — Dependency Stall: EPIC-04 QA evidence missing EPIC-level DoQ consolidation block at delivery verification entry.

**Recurrence:** No — first time this specific gap (story-level sign-offs present but no EPIC consolidation block) occurred.

**What happened:**
qa_evidence_EPIC-04.md had story-level sign-offs (engine autonomous for ST-07, Strategy Rules owner for ST-08, PO acceptance 2026-04-19/20) but no EPIC-level Director of Quality consolidation block. The delivery verification STEP -1.3 caught this and it was remediated in-session (2026-04-20). No hard gate halt — remediation was same-session.

**Where in the routine:**
Phase 4 STEP -1.3 QA evidence two-tier sign-off check.

**Root cause:** Process gap — qa_evidence template for a `delegated_frontend` story with a domain-specific gate (Strategy Rules owner sign-off) does not explicitly require a separate Director of Quality EPIC-level consolidation block. The template assumes the EPIC-level DoQ sign-off is the primary sign-off, but when story-level gating involves a different authority (Strategy Rules), the DoQ EPIC block can be missed.

**Blast radius analysis:**
- What would have propagated: Delivery verification STEP -1.3 Tier 1 halt on the next occurrence (blank DoQ at EPIC level).
- When it would have surfaced: Any future EPIC with a domain-specific gate (Strategy Rules, Security, etc.) and no DoQ consolidation block.
- Recovery cost if uncaught: Low (same-session addition) — but creates a recurring STEP -1.3 remediation pattern.

**Process patch:**
→ Deferred patch:
  - File: `claude/system/execution_prompt.md`
  - Section: §3.2 DoQ sign-off block (qa_evidence_EPIC-xx.md template or checklist)
  - Change required: When a delegated_frontend story has a domain-specific gate authority (Strategy Rules, Security, etc.) as its primary sign-off, the qa_evidence file must also include a Director of Quality EPIC-level consolidation block summarising all story sign-offs. Template should note: "EPIC-level DoQ sign-off block required regardless of story-level authority delegation."
  - Owner: Head of Specs Team
  - Target: v2.9 planning sprint or next cycle touching execution_prompt.md

---

## Recurrence Escalations

Checking prior cycle (2026-04-13__release-v2.7) lessons_learnt_closure.md:
Prior cycle's outstanding deferred actions checked for carryover without prompt_change_log entry.

**Prior cycle deferred patches from closure:**
- v2.7 post-ship: no standalone lessons_learnt_closure.md was found at `claude/cycles/2026-04-13__release-v2.7/lessons_learnt_closure.md` — checking Phase 3/4 lessons_learnt_cycle.md for deferred patches.

From Phase 4 of v2.7: all 3 friction items were addressed as sprint stories in v2.8 (CF-1→ST-04, CF-2→ST-05, BLG-QA-13→ST-02/ST-03). No outstanding deferred patches with missed prompt_change_log entries from the prior cycle.

None.

---

## Process improvements actioned this run

| File | Section | Change | Version | Prompt change log entry |
|------|---------|--------|---------|------------------------|
| `claude/system/gh_issue_template.md` | Top of file | Lifecycle header (Owner/Class/Status/Version/Last Updated) added per Class 6 standard | (none)→v1.0 | Yes — appended 2026-04-20 |
| `docs/System_status_report.md` | v2.8 sprint section | Scenario counts corrected (CORR: 9→4, SIG-IND: 8→2); execution_prompt.md version corrected (v3.5→v3.7); test scenarios reference updated | N/A (operational record) | Not applicable |

---

## New files created this run

- `claude/cycles/2026-04-17__release-v2.8/verification_report.md` — delivery verification report
- `claude/cycles/2026-04-17__release-v2.8/lessons_learnt_closure.md` — this file
- `claude/cycles/2026-04-17__release-v2.8/closure_record.md` — post-ship closure record
- `claude/cycles/2026-04-17__release-v2.8/closure_state.json` — closure engine state tracker

---

## Outstanding deferred patches

| File | Section | Change required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/execution_prompt.md` | §3.2.A reclassification note | When delegated_frontend→autonomous reclassification involves frontend changes, Director of Quality counter-sign is required at sprint close (not deferred to verification) | Head of Specs Team | v2.9 planning sprint |
| `claude/system/execution_prompt.md` | §3.2 DoQ sign-off template | EPIC-level DoQ consolidation block required in qa_evidence when story-level sign-offs involve domain-specific authorities (Strategy Rules, Security, etc.) | Head of Specs Team | v2.9 planning sprint |

---

## Escalations

None.

---

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | Frontend reclassification (delegated_frontend→autonomous) requires Director of Quality counter-sign when frontend changes are present — this was caught at STEP -1.3 but should be enforced at sprint close | Sprint Execution Engine: at STEP 5 sprint close, if any EPIC has a reclassified autonomous story with frontend output, flag the EPIC for Director of Quality counter-sign in the sprint_close.md QA log | Sprint Planning |
| 2 | Domain-gated EPICs (Strategy Rules, Security, etc.) need a Director of Quality EPIC-level consolidation block in qa_evidence in addition to the domain authority sign-off — absence creates a STEP -1.3 stall | Sprint Execution Engine: execution_prompt.md §3.2 qa_evidence template should explicitly require DoQ EPIC-level consolidation block for delegated_frontend/domain-gated EPICs | Sprint Planning |
