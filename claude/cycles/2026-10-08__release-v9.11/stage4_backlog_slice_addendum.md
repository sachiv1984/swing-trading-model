**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Cycle:** 2026-10-08__release-v9.11

# Post-Gate-Correction Addendum — 2026-10-08__release-v9.11

Corrections below are additive to the sealed `stage4_backlog_slice.md` — they do not replace or edit its content. Sprint Planning and Sprint Execution must read both files together as the combined authoritative scope.

## ST-25 — §13 pre-check required; design and frontend spec work deferred until the §13 determination
**Found at:** Design Gate STEP 1 (mandatory §13 boundary pre-check for AI-calling proposals)
**Correction:** ST-25 (`BLG-FEAT-59`, AI-assisted monthly P&L narrative) adds a new call to an AI provider. No existing §13 review covers it. The debrief review (`decisions--2026-08-17__release-v8.9--ST-06-section13-review.md`) and the briefing/chat review (`decisions--2026-06-24__release-v6.2--BLG-FEAT-50-51-section13-review.md`) each cover a different feature, and neither covers AI text inside a financial report. The gate records `Gate Status: §13 PRE-CHECK REQUIRED` and conditionally clears ST-25, following the `2026-08-17__release-v8.9` ST-06 precedent. Within ST-25's existing scope this means:

1. **First sub-step, `delegated_decision`:** the Strategy Rules & System Intent Owner records a §13 determination (PASS, CONDITIONAL or FAIL) for the monthly P&L narrative. It must cite every §13 clause that names AI output or financial reporting (ST-25 AC 2; ST-35's rule if it has landed). This is RISK-06's pre-sprint decision. If the Owner rules that a full §13 review is needed rather than a confirmation, ST-25 is re-scoped at Sprint Planning to that review (RISK-06's stated fallback). That would be a scope change, so it belongs to Sprint Planning or `amend cycle`, not this addendum.
2. **Before any design or build:** ST-25 introduces a new AI-calling endpoint, so the AI endpoint security checklist (`docs/specs/security/ai_endpoint_security_checklist.md`: rate limiting, cost gating, prompt-injection awareness) is completed. ST-23's cost estimate is its cost-gating input (`design_gate_prompt.md` STEP 2.2).
3. **Then, inside ST-25 before implementation:** the Head of UX & Design produces the design decision record under `docs/design/2026-10-08__release-v9.11/monthly-pnl-ai-narrative/`, the Product Owner approves it, and the Frontend Specifications & UX Documentation Owner adds the narrative section to `docs/specs/frontend/pages/reports.md` (§Monthly P&L Report, currently v0.20). The Head of Specs Team confirms lifecycle compliance. The design must show the section as optional and dismissible (AC 1) and carry the advisory framing from `design_system.md` §Shared UI Components → AdvisoryBadge (AC 2).
4. **No ST-25 implementation commit** lands before steps 1–3 are complete and recorded in `execution_state.json`.

ST-26 (usage counter) is sequenced after ST-25 and inherits this ordering.
**Date:** 2026-10-08
