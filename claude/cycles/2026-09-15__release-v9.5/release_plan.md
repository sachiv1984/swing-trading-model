Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-15
Cycle: 2026-09-15__release-v9.5
Release: v9.5

# Release Plan — v9.5

Invocation: `plan release --version "v9.5" --capacity "full capacity"`

---

## Readiness

Preflight (STEP -1) passed in full — see `run_manifest.md`. No formal `## v9.5` roadmap section exists; cleared via the STEP -1.2 Option(b)-equivalence rule against the `2026-09-14__scheduled` rebalance's documented "defer again" decision (13th consecutive release cycle relying on this equivalence, extending the v8.5–v9.4 pattern). `post_ship_complete`/`next_cycle_unblocked` both `true` for prior cycle `2026-09-14__release-v9.4`. All required agent roles present. Write test passed. `open_escalations` empty; `ESC-EXEC-20260910-01` sits in `deferred_escalations` at disposition `Deferred`, not `Open` — SLA-breach carry-forward gate does not fire.

Advisory checks (§1.1–§1.4, full detail in `run_manifest.md`):
- Backlog Age Advisory: no 2+ cycle carried spec/documentation debt item in scope — all 43 selected items enter `stage4_backlog_slice.md` for the first time.
- Provisional-Target Advisory: 7 selected items carry `Provisional-Target: v9.5` (horizon-planned ahead of time from v9.4 sprint execution/PR review); the remaining 36 carry `TBD`/`Unscheduled`.
- Design-Gate Language Scan: all 4 EPIC-06 items carry an observable UI acceptance criterion or UI-shipping Scope text → **`design_gate_required: true`**.
- Gate-Condition Proximity Scan: Arc 4/Arc 5 data-density metrics unchanged since the last rebalance (SI-02/PO-02/PO-04 gates NOT MET). No item in this cycle's scope touches that gate family. Ready pool holds 2 P1 items (first cycle on record with genuine ungated P1 scope), 2 P2 items, 1 P4 item, remainder P3.

```yaml
artifacts.stage1_readiness: pass
```

---

## Scope

Scope document: `docs/product/scope/scope--2026-09-15__release-v9.5-full-capacity-debt-clearance-iii.md`

| S2-ID | Scope theme | Items | Effort (days) |
|-------|-------------|-------|----------------|
| S2-01 | Backend & Platform Engineering Debt | 4 | 6.00 |
| S2-02 | Operations & Security Debt | 10 | 6.30 |
| S2-03 | QA & Test Coverage Debt | 7 | 3.20 |
| S2-04 | Spec & Documentation Debt | 9 | 7.34 |
| S2-05 | Governance Process Debt | 9 | 3.95 |
| S2-06 | Frontend & UX Debt | 4 | 1.20 |
| **Total** | | **43** | **27.99** |

**Items explicitly deferred (not entering v9.5 scope):**
- `BLG-FEAT-73`, `BLG-FEAT-74`, `BLG-FEAT-76` — substantively gate-blocked by their own body text (no formal `Gate` field, but each explicitly states it may not enter sprint planning yet); treated as not-ready.
- 130 formally gated/conditional items — no clearance evidence this cycle (unchanged data-density/AI-adoption/§13-review gates).
- 19 further ungated P3/P4 items, ~16.80 estimated days, left unselected purely on capacity grounds — available for a future release cycle.

**Re-included this cycle (see `run_manifest.md` Friction Item 1):** `BLG-SPEC-56`, `BLG-SPEC-57`, `BLG-QA-59` — previously excluded at v9.3/v9.4 alongside the genuinely gate-blocked trio; re-read this session and found to describe legitimate pre-authoring work performable ahead of the PO-02 gate, not work blocked by it. Selected into EPIC-04/EPIC-03 (`ST-23`, `ST-24`, `ST-15`).

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
| EPIC-01 | S2-01 | Backend Engineering Patterns Owner; Data Model & Domain Schema Owner; API Contracts & Documentation Owner; Head of Engineering | RISK-01 | `ST-01` (`BLG-BE-117`) is CI-blocking for every open/future PR — sequence first within the EPIC and ideally first across the whole cycle so downstream PRs stop inheriting a red CI state |
| EPIC-02 | S2-02 | Infrastructure & Operations Owner; FinOps & Resource Architect | RISK-02 | `ST-05` (`BLG-OPS-160`) is an investigation with "remediation effort TBD" — cap this cycle's scope to investigation + documentation; if a live gap is confirmed, file the wiring fix as its own new backlog item rather than absorbing open-ended scope now |
| EPIC-03 | S2-03 | QA & Testing Owner; Director of Quality | RISK-03 | No UI ACs; independent of other EPICs |
| EPIC-04 | S2-04 | Head of Specs Team; API Contracts & Documentation Owner; Data Model & Domain Schema Owner; Frontend Specifications & UX Documentation Owner | RISK-04 | `ST-22` (`BLG-SPEC-D18`) needs live DB access which has been unavailable in this execution environment across every prior cycle's own risk register — disclose explicitly rather than fabricate if still unavailable |
| EPIC-05 | S2-05 | Head of Specs Team; PMO Lead; FinOps & Resource Architect; Director of HR; Director of Quality | RISK-05 | `ST-37` (`BLG-GOV-322`) and `ST-38` (`BLG-GOV-323`) both edit `workforce_capacity.md` — sequence sequentially, not in parallel commits, to avoid a collision on the same file |
| EPIC-06 | S2-06 | Base44 Frontend Prompt Owner; Head of UX & Design | RISK-06 | **Design-gate-triggering** (all 4 items) — `run design-gate --cycle 2026-09-15__release-v9.5` must pass before `plan sprint` can seal (`sprint_planning_pre_condition`) |

**Design-gate-triggering EPICs this cycle:** EPIC-06 only (4 items). First release since v9.4 (and only the 2nd since v9.0) with observable-UI scope.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | `BLG-BE-114` consolidates 3 duplicated ATR trailing-stop recalculation call sites into one shared implementation; a subtle divergence between the 3 copies could be silently lost (or a bug silently propagated to all 3) during consolidation | Medium | Diff all 3 implementations line-by-line before writing the shared version; preserve whichever behaviour the existing passing tests actually exercise; do not resolve any discovered divergence by guessing — file it as its own item if the correct behaviour is unclear | null |
| RISK-02 | EPIC-02 | `BLG-OPS-160`'s own text flags this as potentially "a live P0-class correctness gap" (trailing stops / rebalance-exit signals silently not running) if no dashboard-native cron is found — effort is explicitly "TBD pending confirmation", risking an open-ended remediation scope inside a fixed-capacity sprint | High | Story author executes only the investigation + documentation-correction ACs this cycle; if a live gap is confirmed and remediation exceeds the story's original small-effort estimate, stop and file the wiring fix as a new backlog item for the next cycle rather than silently absorbing unbounded scope | null |
| RISK-03 | EPIC-03 | `BLG-QA-167`/`BLG-QA-170` cite specific stale counts (39 vs ~100+ spec files; 30 vs 28 tests) as of their 2026-09-07/09 filing dates — the actual current counts may have drifted further by the time this story executes | Low | Story author re-counts against the current repository state before applying any fix, rather than trusting the filed numbers as still accurate | null |
| RISK-04 | EPIC-04 | `BLG-SPEC-D18` requires live production DB access (`DATABASE_URL`) to close its schema-confirmation AC — this constraint has recurred unresolved in every prior cycle's own risk register (v9.2 ST-56, v9.3 ST-13/21/22, v9.4 EPIC-03) | Medium | Implement/prepare the confirmation query regardless; if `DATABASE_URL` remains unset in this execution environment, explicitly disclose the AC as not closeable rather than fabricating a schema confirmation, following the same honest-disclosure precedent as `ESC-EXEC-20260910-01` | null |
| RISK-05 | EPIC-05 | `BLG-GOV-322` and `BLG-GOV-323` both add new sections to `workforce_capacity.md` in the same cycle — parallel edits risk a merge collision or one story silently overwriting the other's addition | Low | Sequence the two stories (one commit lands and merges before the other starts editing the same file), or have one author implement both in a single commit with both sections present | null |
| RISK-06 | EPIC-06 | Design-gate-triggering EPIC — `run design-gate` has not yet been run for this cycle; `sprint_planning_pre_condition` blocks `plan sprint` from sealing until it passes | Medium | Flagged explicitly in `cycle_summary.md`; Product Owner/Head of Specs Team must run `run design-gate --cycle 2026-09-15__release-v9.5` before invoking `plan sprint` | null |

```yaml
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

All 43 ST items in `stage4_backlog_slice.md` carry a `**Source:** BLG-xxx` reference resolving to an existing, currently-open backlog entry in `claude/backlog/backlog.md` (confirmed via the same script-driven extraction used to build the slice — no fabricated or stale IDs). All 6 EPIC IDs are internally consistent between `release_plan.md` and `stage4_backlog_slice.md`. No `[ESTIMATE REQUIRED]` or `[AC REQUIRED]` placeholders present in any of the 43 stories.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Capacity Check

**Effort Band Lookup (ST-14):** `scored_initiatives.md` has 0 active initiatives — no pre-assigned Effort Bands. All 6 EPICs sized via inline STEP 4 estimate from each item's own `**Effort:**` field in `claude/backlog/backlog.md`, using the canonical Effort Band → Days table in `workforce_capacity.md` (XS=0.15d, S=0.5d, M=2.5d, L=3.5d) as the fallback midpoint where an item cites only the bare band letter.

| EPIC | Items | Subtotal (days) |
|------|-------|-------------------|
| EPIC-01 — Backend & Platform Engineering Debt | 4 | 6.00 |
| EPIC-02 — Operations & Security Debt | 10 | 6.30 |
| EPIC-03 — QA & Test Coverage Debt | 7 | 3.20 |
| EPIC-04 — Spec & Documentation Debt | 9 | 7.34 |
| EPIC-05 — Governance Process Debt | 9 | 3.95 |
| EPIC-06 — Frontend & UX Debt | 4 | 1.20 |
| **Total** | **43** | **27.99** |

27.99 days vs the confirmed ~24–28 day band (`claude/roadmap/workforce_capacity.md`, unchanged since 2026-07-17) — within band, effectively at its exact upper bound (99.96% of the 28-day ceiling), matching the explicit "use full capacity" instruction — the tightest full-capacity fit on record. **Capacity check outcome: pass, no WARN.**

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity / 5.7 Decision Record Integrity

**5.5 Cross-Stage Integrity:** All 6 S2 IDs (S2-01..S2-06) map 1:1 to EPIC-01..EPIC-06. All 6 EPIC IDs in `stage4_backlog_slice.md` match the Execution Plan table. All 6 RISK IDs in the EPIC table appear in the Risk Register Summary. No orphaned references found.

**5.7 Decision Record Integrity:** Skipped — `artifacts.escalations` is not `present` for this cycle's own run (no new escalation raised during this release-planning session). `decisions--2026-09-15__release-v9.5.md` is still produced per STEP 3's standing requirement (scope/sequencing decisions, not escalation-driven).

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
| 2026-09-15 | 1.0 | Initial publication — v9.5 release plan, 43 items / 6 EPICs / 27.99 days, full capacity; first cycle with genuine ungated P1 scope; design-gate-triggering (EPIC-06) | Head of Specs Team (Release Planning Engine) |
