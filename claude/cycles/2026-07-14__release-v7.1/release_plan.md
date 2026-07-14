**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-14
**Cycle:** 2026-07-14__release-v7.1
**Release:** v7.1 — Nightly Backtest Data Integrity

---

# Release Plan — v7.1 — Nightly Backtest Data Integrity

## Readiness

**Roadmap source:** `claude/roadmap/current_roadmap.md` §3, Now horizon, "v7.1 — Nightly Backtest Data Integrity" (opened at rebalance 2026-07-13__scheduled via STEP 8.0 Production Correctness Fast-Track; STEP 8.1 resolved via Option (a)).

**Readiness checks:**
- Roadmap release section exists: PASS (§3, mandatory anchors named).
- Backlog items resolvable: PASS — `BLG-BE-59`, `BLG-BE-60`, `BLG-FE-107` all present in `claude/backlog/backlog.md` with full problem/scope/AC detail.
- No open Lifecycle/Strategy/Quality blockers identified at readiness stage.

### 1.1 Backlog Age Advisory

No spec/documentation debt item in this release's candidate scope has aged 2+ cycles without a story assignment. `BLG-SPEC-83` and `BLG-SPEC-84` were both filed 2026-07-13 (this is their first cycle of eligibility). Skip — no advisory.

### 1.2 Provisional-Target Advisory

7 of 7 items selected into this release's candidate scope carry `Provisional-Target: v7.1` (`BLG-BE-59`, `BLG-BE-60`, `BLG-FE-107`, `BLG-BE-61`, `BLG-QA-106`, `BLG-SPEC-83`, `BLG-SPEC-84`). 0 items with no matching Provisional-Target signal were pulled into scope.

### 1.3 Design-Gate Language Scan

Two items carry design-gate language:
- `BLG-FE-107`: scope note explicitly states "Needs its own design-gate scoping — not a same-sprint fix" and offers two dispositions (spec-compliance fix vs. a fresh design-gate decision to accept the shipped amber treatment as canonical). **Design dependency detected** — surface at Pre-sprint Required Decisions checklist (STEP 7) and at `run design-gate`.
- `BLG-QA-106`: scope item (c) is "UX consistency review against Arc 3 prompt visual precedents" — a design/UX judgment call, not a pure code-review item. **Design dependency detected** — route through design gate alongside `BLG-FE-107`.

Both flagged for Design Gate Engine classification (STEP 4.1).

### 1.4a Perennial-Return Check

No candidate item returned from a prior cycle's `stage4_backlog_slice.md` with `returned_to_backlog`/`deferred` status. All 7 items are first-cycle-eligible. No PO disposition required.

### 1.4b Within-Sprint Date Gate Classification

No candidate item carries a calendar-date gate condition falling inside the planned sprint window. `BLG-BE-59`/`BLG-BE-60` explicitly declare `Gate criteria: None`; the remaining 5 items carry no gate criteria field at all. No mandatory conditional classification triggered.

### 1.4 Gate-Condition Proximity Scan

No gate-conditional item is in this release's scope. Arc 4 data density sub-check (informational, no scope item depends on it):

| Item | Gate condition | Current trajectory | Projected clear date |
|------|-----------------|---------------------|------------------------|
| PO-02 | 6+ months AI journal entries | trajectory unknown | data not available — PO to surface at readiness review |
| PO-04 | 50+ trades with plans | trajectory unknown | data not available — PO to surface at readiness review |
| SI-02 | 20+ trades with plans | 0/11 linked plans, `insufficient_data` drift status (9 trades / 90d, live re-checked 2026-07-13) | NOT MET, no confirmed trajectory |

---

## Scope

Mandatory anchor scope is fixed by the roadmap (§3, Now horizon) — this routine does not alter it. Capacity-filling selection rationale is recorded in `run_manifest.md` §Scope Decision.

| S2-ID | Item | Epic | Description |
|-------|------|------|-------------|
| S2-01 | `BLG-BE-59` | EPIC-01 | Gate nightly backtest ticker eligibility on `ticker_universe.created_at` (point-in-time integrity) — **mandatory anchor** |
| S2-02 | `BLG-BE-60` | EPIC-01 | Nightly backtest `total_pnl_gbp` not reproducible night-to-night with zero exits — **mandatory anchor** |
| S2-03 | `BLG-FE-107` | EPIC-02 | Table View RISK OFF badge colour/label spec compliance — **mandatory anchor** (companion, capacity/sequencing grounds) |
| S2-04 | `BLG-BE-61` | EPIC-03 | Position review-cadence nudge: backend/data-integrity hardening pass |
| S2-05 | `BLG-QA-106` | EPIC-03 | Position review-cadence nudge: frontend/QA polish pass |
| S2-06 | `BLG-SPEC-83` | EPIC-03 | Realized/unrealized P&L split: spec & metrics hardening pass |
| S2-07 | `BLG-SPEC-84` | EPIC-03 | Tax-year P&L CSV export: spec & test hardening pass |

**Items explicitly deferred:** `BLG-BE-62` (idempotent nightly batch-job pattern audit — `Provisional-Target: TBD`, broader cross-job scope not targeted at v7.1); `BLG-SPEC-85` (`trailing_stop_action_rate` spec entry — `Provisional-Target: TBD`, P3).

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01, S2-02 | Backend Engineering Patterns Owner | RISK-01, RISK-02 | No hard dependency between S2-01/S2-02; may run in parallel or sequence — RISK-02 note applies either way |
| EPIC-02 | S2-03 | Head of Engineering / Head of UX & Design | RISK-03 | After Design Gate resolves badge treatment (blocks sprint planning seal structurally — `design_gate_required = true`) |
| EPIC-03 | S2-04, S2-05, S2-06, S2-07 | Backend Engineering Patterns Owner / QA & Testing Owner / Data Model & Domain Schema Owner / API Contracts & Documentation Owner | RISK-04, RISK-05 | Independent of EPIC-01/EPIC-02; no cross-EPIC dependency |

**EPIC-01 note:** `BLG-BE-60`'s proposed solution names three candidate fix vehicles (persist/cache historical prices; append-only trade ledger; wire the existing drift-check to an alert threshold) without selecting one — RISK-01 tracks this. `BLG-BE-59` and `BLG-BE-60` both touch `production_strategy.py`'s core signal/simulation path; sequencing them through the same PR or closely coordinated PRs reduces merge risk (RISK-02).

**EPIC-02 note:** `BLG-FE-107` explicitly requires a design-gate decision between (a) spec-compliance fix or (b) formal acceptance of the shipped amber treatment as canonical — this is not a same-sprint code-only fix. `BLG-QA-106`'s UX consistency review (sub-item c) is routed through the same gate.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | `BLG-BE-60` has 3 undifferentiated candidate fix vehicles (persist/cache, append-only ledger, alert-only) with different effort/risk profiles | Medium | Backend Engineering Patterns Owner selects fix vehicle at EPIC-01 kickoff/early execution; record the choice in sprint planning notes | null |
| RISK-02 | EPIC-01 | `BLG-BE-59`/`BLG-BE-60` both modify the core momentum/backtest simulation path (`production_strategy.py`); uncoordinated concurrent changes risk merge conflicts or re-introducing the same non-reproducibility class of bug | Medium | Sequence or tightly coordinate the two PRs; add a regression check confirming backtest output is deterministic given unchanged inputs before either merges | null |
| RISK-03 | EPIC-02 | `BLG-FE-107` cannot be implemented until a design-gate decision resolves badge colour/label treatment (option a vs b) | High | Route through `run design-gate --cycle 2026-07-14__release-v7.1` before sprint planning seals — already a structural lifecycle gate (`sprint_planning_pre_condition: design_gate_status == Passed`), no additional escalation needed | null |
| RISK-04 | EPIC-03 | `BLG-QA-106` sub-item (c) UX consistency review is a design/UX judgment call, not a pure code-review item | Medium | Route through the same design gate as RISK-03 | null |
| RISK-05 | EPIC-03 | 4 hardening items (S2-04–S2-07) span 4 different owning roles with no single accountable owner for the EPIC as a whole | Low | PMO Lead to confirm sequencing/ownership at sprint planning; items are independent so parallel execution is low-risk | null |

---

## Integrity Validation — 3.5 Local Model Integrity

Checked all data-model references in this release's scope against `docs/specs/data_model.md`:
- `ticker_universe.created_at` (S2-01, `BLG-BE-59`) — existing column (`backend/services/ticker_universe_service.py:100`), currently unused by signal computation. No schema change required; fix gates an existing field into a new code path.
- `positions.last_reviewed_at` (S2-04, `BLG-BE-61`) — existing column, added v7.0 EPIC-03 ST-15 (`docs/specs/data_model.md:1253-1261`). No schema change; hardening pass only.
- No item in this release's scope introduces a new table, column, or migration.

**Outcome: PASS.** No local model integrity conflicts.

---

## Capacity Check

**Effort Band Lookup (Tier 3 for all 7 items):** `claude/scoring/scored_initiatives.md` carries no matching row for any of `BLG-BE-59`, `BLG-BE-60`, `BLG-FE-107`, `BLG-BE-61`, `BLG-QA-106`, `BLG-SPEC-83`, `BLG-SPEC-84` (file explicitly notes CPS=N/A this cycle, tier 3 fallback expected). Using STEP 4 inline estimates; no advisory required (tier 3 is silent by design).

**Capacity inputs:** Sprint capacity baseline ~12–14 working days (solo developer, evenings/weekends — `claude/roadmap/workforce_capacity.md`, Effective 2026-05-27). Warn threshold: effort > 14 days.

| ST-ID | Item | Effort estimate | Midpoint (days) |
|-------|------|------------------|------------------|
| ST-01 | `BLG-BE-59` | M (~1-2 days) | 1.5 |
| ST-02 | `BLG-BE-60` | L (~3-5 days) | 4.0 |
| ST-03 | `BLG-FE-107` | S (~0.5 day) | 0.5 |
| ST-04 | `BLG-BE-61` | M | 2.0 |
| ST-05 | `BLG-QA-106` | M | 2.0 |
| ST-06 | `BLG-SPEC-83` | M | 2.0 |
| ST-07 | `BLG-SPEC-84` | M | 2.0 |
| **Total** | | | **14.0** |

At the midpoint, total estimated effort (14.0 days) sits exactly at the top of the ~12–14 day capacity band with zero buffer. `BLG-BE-60`'s range (3-5 days) and `BLG-BE-59`'s range (1-2 days) both carry meaningful upside uncertainty — a pessimistic reading (top of both ranges: 2 + 5 = 7 instead of 5.5 for EPIC-01 alone) pushes total effort to ~15.5 days, past the warn threshold.

**Outcome: WARN.** Feasible but tight — no slack for estimation variance, particularly on `BLG-BE-60` (RISK-01, undetermined fix vehicle) or the EPIC-02 design-gate item, which cannot be sized precisely until the design gate resolves its treatment.

### Phasing Recommendation

1. State: estimated total effort 14.0 days (midpoint), pessimistic case ~15.5 days; available capacity ~12–14 days.
2. Proposed phasing if sprint planning confirms the pessimistic case is likely:
   - **Phase 1 (Sprint 1):** EPIC-01 (ST-01, ST-02 — ~5.5d) + EPIC-02 (ST-03 — ~0.5d, contingent on design gate) — ~6.0d. These are the roadmap-mandatory anchors; correctness/P1 risk reduction takes priority.
   - **Phase 2 (Sprint 2, same cycle if capacity allows, else next release):** EPIC-03 (ST-04–ST-07 — ~8.0d) — the four capacity-filling hardening items, which are independent of EPIC-01/02 and carry no roadmap-mandatory deadline.
3. Ordering rationale: EPIC-01/EPIC-02 are roadmap-named mandatory anchors (P1 correctness bugs feeding a user-visible page); EPIC-03 is capacity-filling hardening debt with no external deadline pressure — it phases cleanly to Sprint 2 (or defers to v7.2) without violating any commitment if Sprint 1 effort estimates prove pessimistic.

Sprint Planning Engine should confirm actual capacity utilisation against this WARN and apply phasing if Sprint 1 estimates trend toward the pessimistic case (per `shared_standards.md §13`, `plan sprint` surfaces AC gaps and capacity at its own preview step).

---

## Integrity Validation — 5.5 Cross-Stage Integrity

- All S2 IDs map to an EPIC: S2-01, S2-02 → EPIC-01; S2-03 → EPIC-02; S2-04, S2-05, S2-06, S2-07 → EPIC-03. PASS.
- All EPIC IDs in `stage4_backlog_slice.md` match the Execution Plan (STEP 3): EPIC-01, EPIC-02, EPIC-03 present and consistent in both. PASS.
- All RISK IDs referenced in the Execution Plan EPIC table (RISK-01, RISK-02, RISK-03, RISK-04, RISK-05) appear as rows in the Risk Register Summary. PASS.
- No orphaned S2/EPIC/RISK references found.

**Outcome: PASS.**

## Integrity Validation — 5.7 Decision Record Integrity

`artifacts.escalations` = `not_started` (no escalations raised this cycle — no blockers occurred). Per SC-05, this check runs only when escalations are present.

**Outcome: not_applicable.**


