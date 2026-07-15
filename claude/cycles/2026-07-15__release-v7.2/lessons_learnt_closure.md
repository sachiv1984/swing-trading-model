Owner: PMO Lead
Class: Operational Record (Class 3)
Status: Active
Cycle: 2026-07-15__release-v7.2
Release: v7.2
Last Updated: 2026-07-15
Authority: Post-Ship Closure Engine v2.17

---

# Lessons Learnt — Closure Summary: v7.2

Reviewed by: PMO Lead
Date filed: 2026-07-15
Prior cycle checked: claude/cycles/2026-07-14__release-v7.1/lessons_learnt_closure.md

## Classification Summary

| Count | Category |
|-------|----------|
| 1 | Immediate |
| 1 | Deferred (carried forward as Outstanding Action) |
| 0 | Escalated (new) |

---

## Action Classification Detail

### Immediate (1)

| ID | Source | Summary | File | Version | Prompt change log entry |
|----|--------|---------|------|---------|------------------------|
| Phase 3 Friction Item (LL-v7.2-P3-01) | lessons_learnt_cycle.md `## Phase 3` | Session start trusted local `.claude_current_state.json`/`execution_state.json` without first comparing against `origin/main`, causing a duplicate `execution_state.json` re-initialisation and 5 duplicate GitHub issues (#993–#997) before the actual (much further along) origin state was discovered mid-session. Applied now: `execution_prompt.md` STEP -1 gained a new "Session-start divergence check" (`git fetch origin` + local-vs-`origin/main` comparison, run before any local state file is trusted) plus a companion step 0 in §10 Resumability, generalising the existing LL-v3.9-P3-1 resume-sync pattern (previously scoped only to STEP 4's merge-gate) to the very start of the routine. | `claude/system/execution_prompt.md` | v3.56→v3.57 | Yes — appended to `claude/system/prompt_change_log.md` (2 rows: execution_prompt.md, OPERATIONAL_GUIDE.md v4.97→v4.98) |

### Deferred (1 — carried to next cycle or next relevant engine invocation)

| ID | Source | Summary | Owner | Target |
|----|--------|---------|-------|--------|
| Release Planning Carry-Forward #2 | Release Planning lessons_learnt.md | `BLG-QA-111`'s combined design review + shared Playwright suite plan (EPIC-05) is a soft dependency across EPIC-02/03/04 with no hard gate enforcing it runs first — if it slips, each of `BLG-FE-109`/`BLG-FE-110`/`BLG-FE-111` could get independent design reviews/Playwright files, defeating its purpose. This cycle's own EPIC-05 story (ST-08) confirmed the plan exists and named the shared spec file (`tests/e2e/v7.2-dashboard-tradeplan-ux-hardening.spec.js`), but did not (and could not, being autonomous/planning-only) enforce that the 3 implementation stories actually consume it. | Sprint Planning Engine | Next `plan sprint` invocation that schedules `BLG-FE-109`/`BLG-FE-110`/`BLG-FE-111` — explicitly confirm EPIC-05's shared spec file is referenced by all three stories' sprint-backlog entries before sealing, not just noted as a recommendation |

### Escalated (0 new)

None newly escalated this cycle. **Pre-existing escalation still open, not re-escalated:** Release Planning Friction Item 1 (`lessons_learnt.md`) supplies supporting evidence for the already-open v7.1 escalation (Head of Specs Team, deadline 2026-07-17, re: whether `backlog_management_prompt.md`/`idea_intake_prompt.md` should mandate an explicit day-range alongside the S/M/L/XS letter band) — all 8 v7.2 scope items already carried explicit day ranges without a prompt-level mandate, voluntarily. Deadline (2026-07-17) has not yet passed as of this closure (2026-07-15); no action required from this engine beyond surfacing the data point, which is now recorded here for the Head of Specs Team's disposition.

---

## Closure-Phase Observations

- Both `docs/product/scope/scope--2026-07-15__release-v7.2-dashboard-trade-plan-ux-hardening.md` and `docs/product/decisions/decisions--2026-07-15__release-v7.2.md` were cleanly located and marked Superseded — no "not found" flag needed this cycle.
- Backlog reconciliation (STEP 3): all 5 shipped ST items marked ✅ COMPLETE in `backlog.md` against their `execution_state.json` `done`/`merged` records (`BLG-FE-55` ST-01, `BLG-SPEC-89` ST-02, `BLG-SPEC-90` ST-04, `BLG-FE-112` ST-07, `BLG-QA-111` ST-08). Zero stale parked items (IMP-15 check) — matches `verification_report.md §5`'s own finding of zero `parked`-status items in the authoritative backlog slice. Zero Phase 4 additions required — `verification_report.md §2` confirmed 0 backlog entries added this run.
- Deviation compliance (STEP 5): N/A this cycle — `sprint_close.md` confirms zero deviations filed; all five deliverables are net-new readiness/audit/planning artefacts with no prior canonical spec to diverge from.
- Specs Index (`docs/specs/Specs_Index.md`) required no §6/§7 resolutions this run — no shipped ST item closed an open Pending Spec Work or Open Compliance Issue entry. §6.6 (`BLG-SPEC-72`) remains open, unchanged, out of scope. The one open TSG entry (`TSG-v6.8-01`/`BLG-QA-86`) remains open and unchanged (not resolved this cycle). No new spec gaps surfaced (`verification_report.md §6` confirmed all 5 EPICs short-circuited to `not_applicable`).
- Endpoint coverage drift check (STEP 6): zero new endpoints this cycle (all 5 deliverables are doc/spec artefacts — no `backend/routers/` or `src/pages/`/`src/components/` files touched). The long-standing accumulated `openapi.yaml`/`api_performance_baseline.md` gap was re-measured this cycle (100 registered paths vs. 91 baselined after path-param normalisation — 21 endpoints still missing) and filed as `BLG-OPS-111`, cross-referencing the stale pre-existing `BLG-OPS-13` tracking item for reconciliation rather than restating a fresh untracked gap. Not caused by v7.2.
- Roadmap (STEP 2): v7.2 marked ✅ Complete for the 5 items actually shipped this cycle; the 3 sequencing-gated implementation items (`BLG-FE-109/110/111`) were annotated unblocked and carried forward to next release planning, rather than left showing stale "in progress" language, since both their gate conditions (`BLG-SPEC-89`/`BLG-SPEC-90`) closed this same cycle.
- v7.1's carry-forward item #2 (Sprint Planning should treat the capacity check's Phasing Recommendation as a live option) was not directly exercised this cycle — this sprint's capacity check was a 5-story, single-sprint-scope readiness/audit cycle with no WARN-band capacity result and no RISK-tagged either/or fix-vehicle choice, so the guidance had no applicable trigger condition this cycle. Not treated as unresolved; simply not applicable.

---

## Recurrence Escalations

None. No friction item from this cycle matched a prior-cycle friction item with an unresolved outstanding action requiring automatic escalation. The one deferred patch now applied immediately (LL-v7.2-P3-01) closes out within this same cycle rather than carrying forward — not a 2+-cycle recurrence.

---

## Carry-Forward

Items: 2

| # | Observation | Implication | Engine |
|---|-------------|-------------|--------|
| 1 | `BLG-QA-111`'s combined design review + shared Playwright suite plan (EPIC-05) is a soft dependency across EPIC-02/03/04 with no hard gate enforcing it runs first — the plan exists and names a shared spec file, but nothing yet confirms `BLG-FE-109`/`BLG-FE-110`/`BLG-FE-111` will actually reference it. | Sprint Planning should explicitly confirm EPIC-05's shared spec file is referenced by all three implementation stories' sprint-backlog entries before sealing the next sprint that schedules them. | Sprint Planning |
| 2 | All 8 v7.2 scope items already carried explicit day-range effort estimates without a prompt-level mandate, supporting evidence for the still-open v7.1 escalation (Head of Specs Team, deadline 2026-07-17) on whether to formalise this as a `shared_standards.md §16.12`-style requirement at the idea-intake/ad-hoc-filing stage rather than only at Scoring Matrix Overlay time. | Head of Specs Team to factor this second data point into the escalation disposition before 2026-07-17. | Roadmap |

// ARTEFACT_STATUS
```json
{
  "cycle_id": "2026-07-15__release-v7.2",
  "phase": "Post-Ship Closure",
  "status": "present",
  "generated_utc": "2026-07-16T00:20:00Z"
}
```
