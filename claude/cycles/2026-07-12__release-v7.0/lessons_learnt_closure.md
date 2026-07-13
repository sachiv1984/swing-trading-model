Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Cycle: 2026-07-12__release-v7.0
Release: v7.0
Last Updated: 2026-07-13
Authority: Post-Ship Closure Engine v2.17

---

# Lessons Learnt — Closure Summary: v7.0

Reviewed by: PMO Lead
Date filed: 2026-07-13
Prior cycle checked: claude/cycles/2026-07-10__release-v6.9/lessons_learnt_closure.md

## Classification Summary

| Count | Category |
|-------|----------|
| 1 | Immediate (already applied in-session during Sprint Execution; confirmed complete at closure, no prompt patch required) |
| 1 | Deferred (carried forward as Outstanding Action) |
| 0 | Escalated |

---

## Action Classification Detail

### Immediate (1)

| ID | Source | Summary | Disposition |
|----|--------|---------|-------------|
| Phase 3 friction item 1 | Sprint Execution lessons_learnt_cycle.md | ST-04 (EPIC-01) was implemented, pushed (`19d2d5ba`), and QA-signed-off Pass in `qa_evidence_EPIC-01.md`, but its `execution_state.json` entry was left at `status: not_started` / `acceptance_verified: false` — a silent per-item state-tracking gap that survived to EPIC merge, first caught at STEP 5.1 sprint-close resume. | Already applied in-session: `execution_state.json` ST-04 entry corrected to `status: done`, `acceptance_verified: true`, `commit_sha` and `spec_references` backfilled, `sign_off_record` populated from the QA evidence log. No re-work required — data correction only. Confirmed complete at closure. Per the Sprint Execution lessons record, no prompt patch is filed — this is judged a first-occurrence gap already caught by the existing STEP 5.1 safety net, not a structural prompt defect. |

### Deferred (1 — carried to next cycle or next relevant engine invocation)

| ID | Source | Summary | Owner | Target |
|----|--------|---------|-------|--------|
| Release Planning Carry-Forward #1 | Release Planning lessons_learnt.md | This cycle's capacity-filling selection heuristic (favour genuinely ungated product/bug-fix-value items over additional P3 governance/tooling debt while the Product Value Ratio alert is active) was applied ad hoc based on the live alert state, not a codified rule in `release_planning_prompt.md` STEP 2. | Release Planning Engine / Head of Specs Team | Next `plan release` invocation — consider whether STEP 2 should explicitly instruct checking the current Product Value Ratio/Alert state before selecting capacity-filling candidates |

### Escalated (0)

None this cycle. No action item crossed the `lessons_learnt_prompt.md` §3.7 recurrence-escalation threshold.

---

## Closure-Phase Observations

- Both `docs/product/scope/scope--2026-07-12__release-v7.0-*.md` and `docs/product/decisions/decisions--2026-07-12__release-v7.0.md` were cleanly located and marked Superseded — no "not found" flag needed this cycle.
- Specs Index (`docs/specs/Specs_Index.md`) required two resolutions this run: §6.5 (BLG-SPEC-71, Reports.js Tax Year P&L spec sections) and §6.7 (BLG-SPEC-73, Gate Progress Indicator copy) both closed by ST-06 and ST-10 respectively. §6.6 (BLG-SPEC-72) remains open — out of this cycle's scope, left unchanged. No new spec gaps surfaced (verification_report.md §6 confirmed zero test scenario gaps). The one open TSG entry (`TSG-v6.8-01`/`BLG-QA-86`) remains out of scope and unchanged.
- Endpoint coverage drift check (STEP 6) found no drift — the one genuinely new v7.0 endpoint (`PATCH /positions/{id}/mark-reviewed`, ST-15) was already registered in `api_performance_baseline.md` §25 during Sprint Execution; it uses the pre-existing `/positions` top-level path prefix, so no new `SystemStatus.js` `categorizeEndpoint()` prefix gap either.
- STEP 3 (backlog reconciliation) and STEP 5 (deviation compliance) traced cleanly: all 15 shipped ST items marked ✅ COMPLETE in `backlog.md` against their `execution_state.json` `done` records; the sole deviation (DEV-EPIC01-ST05-01) carried all six required fields in `positions.md` Known Deviations with no correction needed.
- No stale parked items found (IMP-15 check) — the authoritative backlog slice contains zero items with `status = parked` (all 15 ST items were firm, in-scope stories) — matches `verification_report.md`'s own STEP 5 finding.
- Both of v6.9's carry-forward items were resolved this cycle: (1) the Grid View badge/trailing-stop parity gap (`PositionCard.js` never rendering the documented-since-v6.2 RISK OFF/Trail Stop badges) was closed directly by this sprint's EPIC-01 (ST-02, ST-03, BLG-FE-102/BLG-FE-97); (2) the Release Planning "surface capacity headroom as a question" recommendation was applied at this cycle's invocation, producing the 15-story maximised scope — see this cycle's own `lessons_learnt.md` "Carry-Forward Item Closed" section for detail.

---

## Carry-Forward

Items: 1

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | This cycle's capacity-filling selection heuristic (favour product/bug-fix value over governance/tooling debt while a Product Value Ratio alert is active) was applied ad hoc based on session-specific judgment rather than a codified instruction. | Release Planning should consider whether `release_planning_prompt.md` STEP 2 should explicitly instruct checking the current Product Value Ratio/Alert state before selecting capacity-filling candidates, so this isn't left to session-specific judgment each time. | Release Planning |

// ARTEFACT_STATUS
```json
{
  "cycle_id": "2026-07-12__release-v7.0",
  "phase": "Post-Ship Closure",
  "status": "present",
  "generated_utc": "2026-07-13T20:30:00Z"
}
```
