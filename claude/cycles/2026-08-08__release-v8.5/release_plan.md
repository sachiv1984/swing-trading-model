Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v8.5
Cycle: 2026-08-08__release-v8.5
Last Updated: 2026-08-08

# Release Plan — v8.5

## Readiness

Preflight passed (see `run_manifest.md §STEP -1`). Post-ship precondition for the prior cycle (`2026-08-07__release-v8.4`) confirmed: `post_ship_complete = true`, `next_cycle_unblocked = true`. No formal `## v8.5` roadmap section exists — cleared via the `2026-07-28__scheduled` rebalance's STEP 8.1 Option (b) decision (same equivalence relied on by every release since `v8.0`). This release is backlog-driven, scoped directly from `claude/backlog/backlog.md`'s ungated/ready pool under Product Owner delegated authority, per explicit user instruction: **"Use fully capacity, focus on user features first."**

**Capacity instruction:** Scope sized to ~27.15 days — the top of the confirmed ~24-28 working-day-equivalent capacity band (Effective 2026-07-17, unchanged since).

**User-feature-priority instruction:** See `run_manifest.md §STEP 2` for the full finding. Summary: the ungated, ready backlog pool contains 0 genuinely new user-facing feature-build items this cycle. All roadmap-flagship features (`BLG-FEAT-73`/`74`/`76`) remain gate-blocked (`73`/`74` formally parked at `v8.3`). The closest available honouring of the instruction is to lead scope with the full ready `BLG-FE-*`/`BLG-FEAT-*` pool (17 of 25 items, 19.9 of 27.15 days — 73% of this cycle's effort) — frontend correctness fixes, design-consistency audits, and UX review/documentation — ahead of non-frontend P2/P3 scope. 2 P1 production-correctness bugs are included ahead of everything per standing precedence (correctness/security over category). See `run_manifest.md §STEP 1.3a` for the scripted gate-detection scan this selection was built from.

Advisory notes (1.1 Backlog Age, 1.2 Provisional-Target, 1.3 Design-Gate Language, 1.4/1.4a/1.4a.1/1.4b Perennial-Return/Gate-Proximity/Sunset/Within-Sprint checks): see `run_manifest.md §STEP 1` for full detail. No hard-gate findings. Design Gate required (multiple UI-facing items with observable ACs) — see STEP 4.1 below.

---

## Scope

25 stories across 6 grouped EPICs (S2-01 through S2-06, 1:1 with EPIC-01 through EPIC-06). Full scope document: `docs/product/scope/scope--2026-08-08__release-v8.5.md`. Full acceptance criteria: `stage4_backlog_slice.md`.

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-01 | Head of Backend Engineering; Infrastructure & Operations Owner | RISK-03 | None — standalone |
| EPIC-02 | S2-02 | Cybersecurity & Trust Lead; Metrics Definitions & Analytics Owner | RISK-06 | None — standalone |
| EPIC-03 | S2-03 | Frontend Specifications & UX Documentation Owner | None | ST-06 before EPIC-04/ST-09, ST-13 |
| EPIC-04 | S2-04 | Frontend Specifications & UX Documentation Owner; Head of UX & Design | RISK-01, RISK-02 | ST-09/ST-13 after EPIC-03/ST-06 |
| EPIC-05 | S2-05 | Head of UX & Design; Frontend Specifications & UX Documentation Owner | RISK-02 | None — standalone |
| EPIC-06 | S2-06 | Metrics Definitions & Analytics Owner; Head of Specs Team; QA & Testing Owner | RISK-04 | None — standalone |

**EPIC-03/EPIC-04 note:** `ST-06` (`BLG-FE-145`) fixes dead Tailwind `-muted` classes that `ST-09`/`ST-13` (design-token/contrast audits) would otherwise be assessing against a broken baseline. Sequence `ST-06` first within the sprint.

**Release-level note:** `RISK-05` below documents the thin-user-feature-pool finding — accepted by Product Owner delegated authority, recorded in `decisions--2026-08-08__release-v8.5.md`.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|-------------|----------------|
| RISK-01 | EPIC-04 | `ST-09`/`ST-13` (contrast/design-token audits) could re-surface the same defect class `ST-06` (EPIC-03) already fixes (dead `-muted` Tailwind classes) if sequenced before it — findings would be based on a known-broken CSS baseline | Medium | `ST-06` sequenced first within the sprint (see Execution Plan note above) | null |
| RISK-02 | EPIC-04, EPIC-05 | 10 of this cycle's 25 items are audit/review/documentation items whose Acceptance Criteria are satisfied by "audit conducted; findings filed" rather than a committed code fix — risk that reviewers expect a shipped fix and flag these as incomplete | Low | ACs are explicit that audit-only completion is valid; called out in `stage4_backlog_slice.md` per-item; DoQ sign-off guidance to reference this note | null |
| RISK-03 | EPIC-01 | `ST-01`'s two candidate fixes (narrow endpoint-level ensure-call vs. broader startup-sequence `ensure_trade_plans_table()` call) have different blast radius — the broader fix touches app startup for all future `trade_plans`-adjacent endpoints | Low | AC allows either approach but requires an explicit no-regression confirmation against existing `trade_plans.py` endpoints before merge | null |
| RISK-04 | EPIC-06 | `ST-23`/`ST-24` (`BLG-GOV-288`/`BLG-GOV-289`) both patch governance files (`release_planning_prompt.md`, `CLAUDE.md`) — omitting the CLAUDE.md §6 Governance File Edit Checklist (version bump, `OPERATIONAL_GUIDE.md` §14 sync, `prompt_change_log.md` entry) in the same commit is itself a non-compliant state | Medium | Explicit governance-file note added to both stories in `stage4_backlog_slice.md`; checklist is a standing CLAUDE.md §6 requirement, not new to this cycle | null |
| RISK-05 | Release-level | 0 of 25 stories are genuine build-and-ship new user features this cycle — the "prioritise user features" instruction is honoured only by leading with the largest available ready frontend/UX pool (correctness fixes, audits, review/documentation), not net-new capability. All roadmap-flagship features remain gate-blocked. | Medium | Documented explicitly in `run_manifest.md §STEP 2` and `decisions--2026-08-08__release-v8.5.md`; accepted by Product Owner delegated authority as the correct honouring of the instruction given the backlog's actual state, not a planning gap | null |
| RISK-06 | EPIC-02 | `ST-04`/`ST-05` (recurring vuln re-scan cadence, key rotation runbook) are process/tooling additions with no immediate production risk being remediated, despite their P2 label | Low | No urgency-driven mitigation needed; sequencing is flexible within the sprint | null |

None of the above risks carry a "must resolve before sprint planning seal" disposition — all are mitigated by in-story acceptance criteria or execution-time sequencing, not pre-sprint decisions. No `## Pre-sprint Planning Required Decisions` section required in `cycle_summary.md`.

---

## Integrity Validation — 3.5 Local Model Integrity

No story in this cycle's scope touches AI model routing, prompt templates, or model version pinning. `ST-07` (AI-provenance field wiring) consumes `model_version`/`prompt_version` already returned by existing generation endpoints; it does not change model selection or invocation behaviour. Pass — no local model/prompt-drift integrity issue identified.

```yaml
# state.json update (STEP 3.5):
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Capacity Check

**Effort Band Lookup (ST-14/shared_standards §16.7):** `scored_initiatives.md` loaded at STEP 0 — 0 matching rows for this cycle's 6 EPICs (all backlog-driven correctness/hardening/audit scope, not roadmap-level scored initiatives). Falling back to inline STEP 4 estimates for all 6 EPICs; no advisory required (no matching row = no advisory per the three-tier rule).

**Estimated effort (midpoint, per item's own backlog `Effort` band):**

| Band | Items (this cycle) | Midpoint days each (approx) | Subtotal |
|------|---------------------|----------------------------|----------|
| XS (<1h–1d) | ST-01, ST-02, ST-07, ST-08, ST-20, ST-23, ST-24 (7) | ~0.2–1.0 (varies) | ~4.1 |
| S (~0.5–2d) | ST-03, ST-04, ST-05, ST-06, ST-09, ST-11, ST-13, ST-16, ST-17, ST-18, ST-21, ST-22, ST-25 (13) | ~0.5–1.25 | ~13.75 |
| M (~1–2d) | ST-10, ST-12, ST-14, ST-15, ST-19 (5) | ~1.5–2.0 | ~9.3 |
| **Total (25 items)** | | | **~27.15 days** |

Estimated total effort ~27.15 days against the confirmed ~24-28 day capacity band — **within band, at the top**, consistent with the explicit user "full capacity" instruction. This is an approximate midpoint estimate; individual item effort bands are indicative per `shared_standards.md`'s standing notice, not committed hours.

**Outcome: PASS** (within the 24-28 day band; does not exceed the 28-day warn threshold).

No `### Phasing Recommendation` subsection required — outcome is `pass`, not `warn`.

```yaml
# state.json update (STEP 4.5):
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity

- All 6 S2-IDs (S2-01–S2-06) map to exactly 1 EPIC each (EPIC-01–EPIC-06) — no orphans, no EPIC without an S2 mapping.
- All 6 EPIC-IDs referenced in `stage4_backlog_slice.md` match the EPIC table in `release_plan.md §Execution Plan` exactly.
- All 6 RISK-IDs (RISK-01–RISK-06) referenced in the EPIC table or release-level note appear as rows in the Risk Register Summary — no orphaned RISK references.
- All 25 ST-IDs in `stage4_backlog_slice.md` appear in `stage4_issue_manifest.json` exactly once each (ST-01–ST-25, no gaps).
- All 25 backlog source IDs referenced in `stage4_backlog_slice.md` match the `v8.5 Release Slice` table committed to `claude/backlog/backlog.md` exactly (25 rows, 1:1).

**Outcome: PASS.**

## Integrity Validation — 5.7 Decision Record Integrity

`artifacts.escalations` is not `present` this cycle (0 escalations raised — no blockers encountered at any hard/conditional gate). Per the engine's own rule, this check is skipped. **Outcome: not_applicable.**

```yaml
# state.json update (STEP 5.5):
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```
