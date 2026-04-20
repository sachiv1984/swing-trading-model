---
**Owner:** PMO Lead
**Class:** Operational Record (Class 3)
**Status:** Closed
**Cycle:** 2026-04-17__release-v2.8
**Release:** v2.8
**Closure Date:** 2026-04-20
---

# Post-Ship Closure Record — v2.8

## §1 Closure Status

| Field | Value |
|-------|-------|
| Cycle ID | 2026-04-17__release-v2.8 |
| Release | v2.8 |
| Closure Status | **Closed_with_actions** |
| Verification Status | Verified — 2026-04-20 |
| Velocity | 1.00 (8/8 stories) |
| Closure Date | 2026-04-20 |
| Closed by | Sprint Execution Engine (post-ship closure v2.5) |

**Closure Status Rationale:** `Closed_with_actions` — post-ship closure complete with 2 deferred prompt patches (execution_prompt.md §3.2.A reclassification note and §3.2 DoQ EPIC template). Both deferred to v2.9 planning sprint under Head of Specs Team ownership. No hard gates outstanding; cycle is fully closed for delivery purposes.

---

## §2 Documents Updated

| Step | File | Change | Status |
|------|------|--------|--------|
| STEP 1 | `docs/product/changelog.md` | v2.8 entry appended (all 8 stories, all 4 EPICs) | Done |
| STEP 2 | `claude/roadmap/current_roadmap.md` | Last Updated, Current Version (v2.7→v2.8), RA:v2.8 annotation "✅ Complete", release table v2.8 "✅ Shipped" | Done |
| STEP 3 | `claude/backlog/backlog.md` | BLG-FE-14 marked COMPLETE; §12 Active Release Slice status Closed + shipped date; Last Updated | Done |
| STEP 4 | `docs/product/scope/scope--2026-04-17__release-v2.8-frontend-completion-test-quality-ai-journal.md` | Status Active → Superseded; supersession note added | Done |
| STEP 4 | `docs/product/decisions/decisions--2026-04-17__release-v2.8.md` | Status Active → Superseded; supersession note added | Done |
| STEP 6 | `claude/cycles/velocity_metrics.md` | v2.8 row appended (8/8, 1.00); rolling average updated (v2.3–v2.8: 0.99) | Done |
| STEP 6 | `docs/System_status_report.md` | Verified status confirmed; corrections already applied at delivery verification STEP 6 | Done (no further change) |
| STEP 7 | `docs/specs/Specs_Index.md` | ai_endpoints.md registered; TSG-v27-01 resolved; §14 TSG-v28-01 added | Done |
| STEP 8 | `claude/system/gh_issue_template.md` | Lifecycle header added (none→v1.0) — immediate patch from lessons_learnt | Done |
| STEP 8 | `claude/system/prompt_change_log.md` | Entry appended for gh_issue_template.md v1.0 | Done |
| STEP 8.5 | `claude/cycles/2026-04-17__release-v2.8/lessons_learnt_closure.md` | Created — 4 friction items, 2 deferred patches, 2 carry-forward items | Done |
| STEP 9 | `claude/cycles/2026-04-17__release-v2.8/closure_record.md` | This file | Done |

**Note:** BLG-QA-13, BLG-FEAT-16, and BLG-GOV-13 were not present in the active backlog at closure. These items were shipped as EPIC-03 sprint stories (ST-02/ST-03/ST-04/ST-05) and were archived at the 2026-04-16 groom run. No action required.

---

## §3 Backlog Additions

| ID | Section | Description | Source |
|----|---------|-------------|--------|
| TEST-GAP-EPIC-04 | §5 QA & Test Automation | AI Journal Summarisation endpoint needs formal docs/testing/ scenario document (POST /api/ai/journal-summary, GET /api/ai/journal-summary/history) | Delivery verification STEP 6 — TSG-v28-01 |

---

## §4 Deviation Compliance

**Deviations this cycle:** 0

No DEV-* entries filed across any qa_evidence_EPIC-*.md file for cycle 2026-04-17__release-v2.8. Deviation compliance: **Clean**.

---

## §5 Lessons Learnt Action Summary

### Immediate patches applied this run

| File | Change | Version | Authority |
|------|--------|---------|-----------|
| `claude/system/gh_issue_template.md` | Lifecycle header added (Owner/Class/Status/Version/Last Updated) per Class 6 standard | (none)→v1.0 | Head of Specs Team (post-ship closure) |

### Deferred patches (not applied this run)

| File | Section | Change Required | Owner | Target |
|------|---------|----------------|-------|--------|
| `claude/system/execution_prompt.md` | §3.2.A reclassification note | When `delegated_frontend→autonomous` reclassification involves frontend-visible changes, Director of Quality counter-sign required at sprint close (not deferred to delivery verification STEP -1.3) | Head of Specs Team | v2.9 planning sprint |
| `claude/system/execution_prompt.md` | §3.2 DoQ sign-off template | EPIC-level DoQ consolidation block required in qa_evidence when story-level sign-offs involve domain-specific authorities (Strategy Rules, Security, etc.) — template must state this explicitly | Head of Specs Team | v2.9 planning sprint |

---

## §6 Outstanding Actions

### OA-v28-01 — AUDIT DUE

**Type:** Advisory
**Trigger:** `completed_cycle_count` reached 12 at STEP 0 (divisible by 3 → audit cadence check fired).
**Action required:** Run `run audit` at start of v2.9 cycle (before or during sprint planning). Prior audit: AUD-2026-04-11 (overall score 65, at-hold threshold). Next audit will assess whether the score has moved.
**Owner:** PMO Lead
**Target:** v2.9 cycle start

---

### OA-v28-02 — SystemStatus.js `/ai` prefix not categorised

**Type:** Frontend advisory
**Trigger:** Endpoint drift check at STEP 6 confirmed 52 openapi paths vs 52 baseline (no drift). However, `SystemStatus.js` `categorizeEndpoint()` does not handle the `/ai` prefix — AI Journal endpoints fall to the `'Other'` category in the system status UI.
**Action required:** Add `/ai` prefix handling to `categorizeEndpoint()` in `SystemStatus.js` — register as a backlog item if not already present.
**Owner:** Frontend Engineer
**Target:** v2.9 backlog (low priority — cosmetic only; no functional impact)

---

### OA-v28-03 — Deferred prompt patches (see §5)

**Type:** Governance
**Trigger:** Two execution_prompt.md gaps identified during post-ship lessons learnt review.
**Action required:** Head of Specs Team to apply §3.2.A reclassification note and §3.2 DoQ EPIC template updates to execution_prompt.md at v2.9 planning sprint.
**Owner:** Head of Specs Team
**Target:** v2.9 planning sprint

---

## §7 Closure Confirmation

Post-ship closure complete — 2026-04-17__release-v2.8 — 2026-04-20.

All 13 steps executed. Cycle status: **Closed_with_actions**.

**Summary:**
- 8/8 stories delivered at 1.00 velocity
- 4 EPICs verified — no deviations
- 1 immediate lessons learnt patch applied (gh_issue_template.md v1.0)
- 2 deferred patches recorded (execution_prompt.md — Head of Specs Team, v2.9)
- 3 outstanding actions (OA-v28-01 audit, OA-v28-02 frontend advisory, OA-v28-03 deferred patches)
- Carry-forward: 2 items to v2.9 sprint planning

**Signed off by:** Sprint Execution Engine (post-ship closure 2026-04-17__release-v2.8)
**Date:** 2026-04-20
