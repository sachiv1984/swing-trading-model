Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-07
Cycle: 2026-09-07__release-v9.2
Release: v9.2

# Release Plan — v9.2

Invocation: `plan release --version "v9.2" --capacity "full capacity"`

---

## Readiness

Preflight (STEP -1) passed in full — see `run_manifest.md`. No formal `## v9.2` roadmap section exists; cleared via the STEP -1.2 Option(b)-equivalence rule against the `2026-08-11__scheduled` rebalance's documented "defer again" decision (7th consecutive release cycle relying on this equivalence, v8.5–v9.2). `post_ship_complete`/`next_cycle_unblocked` both `true` for prior cycle `2026-09-03__release-v9.1`. All 9 required agent roles present. Write test passed.

Advisory checks (§1.1–§1.4, full detail in `run_manifest.md`):
- Backlog Age Advisory: no 2+ cycle carried spec/documentation debt items in scope.
- Provisional-Target Advisory: no item carries `Provisional-Target: v9.2` (no horizon signal pre-existed); all 56 selected items carry `Unscheduled`/`TBD`.
- Design-Gate Language Scan: EPIC-01 and EPIC-02 carry observable UI ACs → `design_gate_required: true`.
- Gate-Condition Proximity Scan: `BLG-FEAT-44`'s gate (Arc5ComplianceSection live 3+ months post-v4.1 ship) is now met (103 days elapsed since 2026-05-27 ship). All other P1 items remain Arc 5/SI-02/SI-05/PO-02 gate-conditional — data density metrics unchanged since the last rebalance (0/11 linked trade plans; SI-02/PO-02/PO-04 gates NOT MET). `BLG-BE-91` (trade-plan-linkage enforcement, escalated P1 at `2026-08-11__scheduled`) remains the structural fix to watch for future gate clearance.

```yaml
artifacts.stage1_readiness: pass
```

---

## Scope

Scope document: `docs/product/scope/scope--2026-09-07__release-v9.2-full-capacity-debt-clearance.md`

| S2-ID | Scope theme | Items | Effort (days) |
|-------|-------------|-------|----------------|
| S2-01 | Arc 5 Compliance Score Low-Volume Advisory | 1 | 0.50 |
| S2-02 | Frontend Accessibility & Spec Compliance | 4 | 0.95 |
| S2-03 | QA & CI Reliability Debt | 11 | 4.45 |
| S2-04 | Governance Process Debt | 26 | 13.00 |
| S2-05 | Spec, Tech & Ops Debt | 14 | 8.65 |
| **Total** | | **56** | **27.55** |

**Items explicitly deferred (not entering v9.2 scope):**
- `BLG-FEAT-92` — reconciled sub-scope of `BLG-FEAT-30`, inherits its gate (screener live ≥60 days AND ≥60 closed trades with attribution); standing Product Owner decision from `2026-09-03__release-v9.1`, unchanged.
- `BLG-FEAT-73`, `BLG-FEAT-74`, `BLG-FEAT-76` and all remaining Arc 5 pre-entry-gateway / SI-02 / SI-05 / PO-02-family P1 items (14 of 15 total P1 items) — gate-conditional, no clearance evidence this cycle.
- `BLG-SPEC-56`, `BLG-SPEC-57`, `BLG-QA-59` (Arc 4 PO-02/03/04 pre-authoring work) — premature while the SI-02/PO-02 data-density gate remains unmet; deliberately excluded to avoid pre-work on a gated horizon.

No scope reprioritisation performed beyond selection from the ungated pool — this routine does not alter strategy boundaries.

```yaml
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

**Format note (IMP-08):** full acceptance criteria live in `stage4_backlog_slice.md`; this section is the compact sequencing/risk view.

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-01 | Metrics Definitions & Analytics Owner; Head of UX & Design | RISK-06 | Design gate; sequence first (only genuinely new-scope EPIC, unblocks capacity-planning conversation for sprint planning) |
| EPIC-02 | S2-02 | Frontend Specifications & UX Documentation Owner; Director of Quality | RISK-02 | Design gate; sequence with EPIC-01 (both UI-facing, share one design-gate pass) |
| EPIC-03 | S2-03 | QA Testing Owner; Director of Quality | RISK-03 | No UI ACs; independent of EPIC-01/02 |
| EPIC-04 | S2-04 | Head of Specs Team; PMO Lead | RISK-04 | Sequence governance-prompt-touching stories serially within the sprint (not parallel branches) to avoid version-bump collisions |
| EPIC-05 | S2-05 | Head of Specs Team; Infrastructure & Operations Owner | RISK-05 | Independent; single Head of Specs Team review pass recommended across all items before DoQ |

**EPIC-01 note:** Single-item EPIC (`BLG-FEAT-44`, S2-01). This is the only ungated build-adjacent item found this cycle (see `run_manifest.md` Skill-Silo consideration) — sequenced first per the `roadmap_prompt.md` §7.1 Skill-Silo mitigation rotation guideline even though it falls well short of a full build-and-ship anchor.

**EPIC-04 note:** Largest EPIC by item count (26) but lowest per-item effort (all S/XS) — pure governance process-debt hygiene, consistent with the pattern established v8.5–v9.1 in the absence of a Now-horizon anchor.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | `BLG-FEAT-44`'s Acceptance Criteria requires the Metrics Definitions & Analytics Owner to formally verify the gate condition "before sprint planning" — the calendar-date fact is confirmed but the named owner has not yet signed off | Medium | Owner sign-off recorded before sprint planning seals (tracked as RISK-06 disposition below — same underlying risk, restated with "must resolve before seal" status for the Pre-sprint Planning Required Decisions checklist) | null |
| RISK-02 | EPIC-02 | Observable UI ACs (heading order, aria-labelling, card text/null rendering, motion-vs-contrast guideline) require Playwright coverage or recorded staging sign-off per CLAUDE.md's frontend-visible-changes rule | Low | Story authors add Playwright coverage or record a staging run at DoQ; any AC deferred to post-merge staging must have a backlog item filed before the PR opens | null |
| RISK-03 | EPIC-03 | Several EPIC-03 items are CI-behaviour fixes (`governance_sync.yml`, `playwright.yml` trigger paths) where code review alone cannot confirm the fix — needs a live CI run | Medium | QA sign-off requires an actual CI run's evidence (run URL/log excerpt), not code review alone, before DoQ pass | null |
| RISK-04 | EPIC-04 | 26 items in one EPIC, several independently touching governance prompt versions (`OPERATIONAL_GUIDE.md` §14 table, individual prompt `**Version:**` headers) — cross-item version-bump collision risk within a single sprint | Medium | Sequence governance-file-touching stories serially within EPIC-04's own execution order (not parallel sub-branches); apply CLAUDE.md §6 checklist per item | null |
| RISK-05 | EPIC-05 | 14 spec/tech/ops debt items span multiple documentation owners; several touch overlapping API-contract/spec-index concerns (`BLG-SPEC-119`–`122`) | Low | Single Head of Specs Team review pass across all EPIC-05 items before DoQ sign-off to catch cross-item drift | null |
| RISK-06 | EPIC-01 | `BLG-FEAT-44` gate-condition verification (owner sign-off) — same substance as RISK-01, restated here as the item consumed by STEP 7's Pre-sprint Planning Required Decisions checklist | High | Metrics Definitions & Analytics Owner must record explicit gate-condition confirmation before Sprint Planning Engine STEP -1 seals the sprint | null |

```yaml
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

All 56 ST items in `stage4_backlog_slice.md` carry a `**Source:** BLG-xxx` reference resolving to an existing, currently-open backlog entry in `claude/backlog/backlog.md` (confirmed via the same script-driven extraction used to build the slice — no fabricated or stale IDs). All 5 EPIC IDs are internally consistent between `release_plan.md` and `stage4_backlog_slice.md`. No `[ESTIMATE REQUIRED]` or `[AC REQUIRED]` placeholders present in any of the 56 stories.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Capacity Check

**Effort Band Lookup (ST-14):** `scored_initiatives.md` has 0 active initiatives — no pre-assigned Effort Bands. All 5 EPICs sized via inline STEP 4 estimate from each item's own `**Effort:**` field in `claude/backlog/backlog.md` (band-to-day conversion: XS≈0.15d, S≈0.5d, M≈2.5d, L≈3.5d, per the day-range parentheticals used consistently across the backlog).

| EPIC | Items | Subtotal (days) |
|------|-------|-------------------|
| EPIC-01 — Arc 5 Compliance Score Low-Volume Advisory | 1 | 0.50 |
| EPIC-02 — Frontend Accessibility & Spec Compliance | 4 | 0.95 |
| EPIC-03 — QA & CI Reliability Debt | 11 | 4.45 |
| EPIC-04 — Governance Process Debt | 26 | 13.00 |
| EPIC-05 — Spec, Tech & Ops Debt | 14 | 8.65 |
| **Total** | **56** | **27.55** |

27.55 days vs the confirmed ~24–28 day band (`claude/roadmap/workforce_capacity.md`, unchanged since 2026-07-17) — within band, near its upper bound (~98% of the 28-day ceiling), matching the explicit "use full capacity" instruction. **Capacity check outcome: pass, no WARN.**

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity / 5.7 Decision Record Integrity

**5.5 Cross-Stage Integrity:** All 5 S2 IDs (S2-01..S2-05) map 1:1 to EPIC-01..EPIC-05. All 5 EPIC IDs in `stage4_backlog_slice.md` match the Execution Plan table. All 6 RISK IDs in the EPIC table appear in the Risk Register Summary. No orphaned references found.

**5.7 Decision Record Integrity:** Skipped — `artifacts.escalations` is not `present` (no escalations raised this cycle; all preflight/gate checks passed cleanly). `decisions--2026-09-07__release-v9.2.md` is still produced per STEP 3's standing requirement (scope/sequencing decisions, not escalation-driven).

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```

---

## Change Log

| Date | Version | Change | Authority |
|------|---------|--------|-----------|
| 2026-09-07 | 1.0 | Initial publication — v9.2 release plan, 56 items / 5 EPICs / 27.55 days, full capacity | Head of Specs Team (Release Planning Engine) |
