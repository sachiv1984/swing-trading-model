Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v7.3
Cycle: 2026-07-16__release-v7.3
Last Updated: 2026-07-16

---

# Release Plan — v7.3: Dashboard/Trade-Plan/Navigation UX Continuation

## Readiness

Release readiness validated against `claude/roadmap/current_roadmap.md §3` (Now horizon, v7.3 section) and `claude/backlog/backlog.md`.

- All 7 scope candidates are ungated, `Provisional-Target: v7.3`. `BLG-FE-109/110/111` were carried forward unshipped from v7.2 (unblocked 2026-07-15). `BLG-SPEC-91/92/93/94` were filed at roadmap rebalance `2026-07-16__scheduled` as pre-implementation readiness passes for `BLG-FE-115/116/117/118` — those four implementation items are explicitly **not** in this release's scope (see §Scope, Items explicitly deferred).
- `BLG-FE-109/110/111` require no further sequencing within this release — their own pre-implementation readiness passes (`BLG-SPEC-89`/`BLG-SPEC-90`) already shipped in `2026-07-15__release-v7.2`.
- Advisory scans (§1.1–§1.4b) recorded in full in `run_manifest.md`. Summary:
  - §1.1 Backlog Age: no spec/doc-debt item aged 2+ cycles without story assignment (all 4 SPEC items filed this cycle).
  - §1.2 Provisional-Target: 7/7 candidates match `v7.3`.
  - §1.3 Design-Gate Language: `BLG-FE-109`, `BLG-FE-110`, `BLG-FE-111` carry observable UI acceptance criteria — design dependency flagged (see STEP 4.1). These are the same 3 items that already passed a design gate under v7.2 (`claude/cycles/2026-07-15__release-v7.2/design_gate.md`, Passed 2026-07-15) — flagged as advisory evidence for the next `run design-gate` invocation, not a waiver.
  - §1.4a Perennial-Return: `BLG-FE-109/110/111` are on their 2nd release-plan appearance (1st: v7.2, committed but unbuilt; this is not a mid-cycle `returned_to_backlog`/`deferred` status) — below the 2-cycle threshold, no PO disposition required.
  - §1.4b Within-Sprint Date Gate: no scope item carries a calendar-dated gate condition — all classifiable as firm capacity.
  - §1.4 Gate-Condition Proximity: no gate-conditional candidates in scope. SI-02 context noted — unchanged, `BLG-FE-109` remains its UX-side fix.

```yaml
artifacts.stage1_readiness: pass
```

---

## Scope

Scope document: `docs/product/scope/scope--2026-07-16__release-v7.3-dashboard-trade-plan-navigation-ux-continuation.md`

| S2-ID | Backlog Item | Title | Priority | Effort |
|-------|-------------|-------|----------|--------|
| S2-01 | BLG-FE-109 | Trade-plan-to-execution linkage UX ("Start Trade from Plan") | P1 | M (~1–2d) |
| S2-02 | BLG-FE-110 | Dashboard empty/first-run state coverage | P1 | S–M (~0.5–1d) |
| S2-03 | BLG-FE-111 | Dashboard briefing visual hierarchy | P1 | S (~0.5d) |
| S2-04 | BLG-SPEC-91 | Command Palette (BLG-FE-115) pre-implementation spec, prompt template & discoverability/adoption pass | P2 | M (~2–3d) |
| S2-05 | BLG-SPEC-92 | Custom Price Alerts (BLG-FE-116) pre-implementation readiness pass | P2 | L (~3–4d) |
| S2-06 | BLG-SPEC-93 | Bulk Actions (BLG-FE-117) pre-implementation readiness pass | P2 | M (~2d) |
| S2-07 | BLG-SPEC-94 | Saved Filters & Calendar View (BLG-FE-118) pre-implementation spec pass | P2 | M (~2–3d) |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-FE-115 (Global command palette) | Blocked on its own readiness pass (`BLG-SPEC-91`, S2-04) completing first | v7.4 (provisional) |
| BLG-FE-116 (Custom price alerts) | Blocked on its own readiness pass (`BLG-SPEC-92`, S2-05) completing first — including a §13 pre-check that has not yet run | v7.4 (provisional) |
| BLG-FE-117 (Bulk actions) | Blocked on its own readiness pass (`BLG-SPEC-93`, S2-06) completing first | v7.4 (provisional) |
| BLG-FE-118 (Saved filters / calendar view) | Blocked on its own readiness pass (`BLG-SPEC-94`, S2-07) completing first | v7.4 (provisional) |

This mirrors the v7.2 precedent exactly (`BLG-SPEC-89`/`BLG-SPEC-90` readiness passes shipped in Sprint 1, with `BLG-FE-109/110/111` implementation carried to this release): the four `BLG-SPEC-9x` readiness passes are this release's scope; their paired `BLG-FE-11x` implementation items become v7.4 candidates once each pass completes. This is a scope extraction only — no reprioritisation of the global backlog performed.

```yaml
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

**Sequencing note:** `EPIC-01` (`BLG-FE-109/110/111`) has no internal cross-dependency on the other four EPICs — it is ready to build immediately. `EPIC-02`–`EPIC-05` are each an independent readiness/spec pass for a *different* v7.4 candidate feature; they do not depend on each other or on EPIC-01, and may run in any order or in parallel.

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-01, S2-02, S2-03 | Head of UX & Design; Base44 Frontend Prompt Owner | RISK-01 | None — ready now |
| EPIC-02 | S2-04 | Frontend Specs & UX Documentation Owner; Head of UX & Design | RISK-02 | Independent; must complete before `BLG-FE-115` can enter a future sprint |
| EPIC-03 | S2-05 | Data Model & Domain Schema Owner; Backend Engineering Patterns Owner | RISK-03 | Independent; must complete before `BLG-FE-116` can enter a future sprint |
| EPIC-04 | S2-06 | Backend Engineering Patterns Owner; Director of Quality | RISK-04 | Independent; must complete before `BLG-FE-117` can enter a future sprint |
| EPIC-05 | S2-07 | Data Model & Domain Schema Owner; Frontend Specs & UX Documentation Owner | RISK-05 | Independent; must complete before `BLG-FE-118` can enter a future sprint |

EPIC-01: All 3 items already passed design gate review once (under v7.2) with no implementation changes since — Product Owner/Head of UX & Design to confirm at `run design-gate` whether the prior Passed record can be cited directly or whether specs have drifted enough to warrant a fresh pass.

EPIC-03: `BLG-SPEC-92` explicitly scopes a §13 pre-check confirming the feature remains user-defined-threshold-plus-passive-notification, not automated execution — this is the highest-priority readiness gate in this release; if the pre-check finds a genuine §13 concern, `BLG-FE-116` may require PO/Strategy Rules Owner scoping before it can ever enter a future release.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | Items were design-gate-approved under v7.2 but never built; if underlying specs (`design_system.md`, dependent components) drifted since 2026-07-15, the prior Passed record may no longer be a safe basis to skip a fresh review | Medium | Flagged as an explicit advisory for the next `run design-gate` invocation to assess rather than silently reuse or silently redo | null |
| RISK-02 | EPIC-02 | Command palette spec pass could scope-creep into a larger cross-page search-index design than a single readiness pass can absorb at its M (~2–3d) estimate | Low | Scope explicitly bounded to spec/prompt-template/discoverability-plan/API-contract-stub per `BLG-SPEC-91`'s own AC; any larger search-index redesign is out of scope and would be filed as a follow-up | null |
| RISK-03 | EPIC-03 | Custom price alerts pre-check could surface a genuine §13 human-in-the-loop boundary concern (automated background evaluation triggering notifications) that blocks `BLG-FE-116` indefinitely, not just delays it | High | `BLG-SPEC-92` scope explicitly includes a dedicated §13 pre-check with a PASS-or-named-follow-up requirement before the item is considered ready; Strategy Rules & System Intent Owner to review the pre-check finding | null |
| RISK-04 | EPIC-04 | Batch-mutation endpoint pattern could overlap with or duplicate an existing bulk-operation pattern elsewhere in `backend/routers/`, risking two divergent batch conventions | Low | `BLG-SPEC-93` scope requires the pattern to be designed against existing backend conventions, not invented standalone; Backend Engineering Patterns Owner reviews for convention consistency | null |
| RISK-05 | EPIC-05 | Saved-filter persistence schema decision (JSON-column-on-settings vs. dedicated table) is a genuine either/or engineering choice — echoes the v7.1/v7.2 carry-forward pattern of a RISK-tagged fix-vehicle choice deferred past planning | Medium | `BLG-SPEC-94` scope requires the decision to be made and recorded with rationale *during this readiness pass*, not deferred to execution kickoff — directly applying the v7.1/v7.2 carry-forward lesson | null |

Decisions record: `docs/product/decisions/decisions--2026-07-16__release-v7.3.md`

```yaml
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

Checked: all S2-IDs referenced in the Scope table map 1:1 to backlog items that exist in `claude/backlog/backlog.md` (verified by direct read, §STEP 2 above). All EPIC-IDs in the Execution Plan table reference only S2-IDs defined in Scope. No orphaned or undefined identifiers found. Owner/role assignments per EPIC match roles named in `claude/agents/`.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Design Gate Classification (STEP 4.1)

Scan of all 7 ST items for UI-facing scope:

- `ST-01` (`BLG-FE-109`), `ST-02` (`BLG-FE-110`), `ST-03` (`BLG-FE-111`): delegation class `delegated_frontend`, each carrying observable UI acceptance criteria (visible/functional action, empty-state rendering, colour, dual-theme layout hierarchy) — identical to their v7.2 classification.
- `ST-04`, `ST-05`, `ST-06`, `ST-07`: delegation class `autonomous`, no observable UI acceptance criteria (spec/readiness-pass documents — schema decisions, prompt templates, pre-checks, API contract stubs).

**Classification: `design_gate_required = true`** — 3 items (ST-01, ST-02, ST-03) classified as UI-facing.

⚠ DESIGN GATE REQUIRED before plan sprint — 3 items classified as UI-facing. Run: `run design-gate --cycle 2026-07-16__release-v7.3`

```yaml
attributes.design_gate_required: true
```

---

## Capacity Check

**Effort Band Lookup (Tier 3 for all 7 items):** `claude/scoring/scored_initiatives.md` carries no matching initiative row for any of the 7 v7.3 scope items (CPS = N/A this cycle). Using STEP 4 inline estimates; no advisory required (tier 3 is silent by design).

**Capacity inputs:** Sprint capacity baseline ~12–14 working days (solo developer, evenings/weekends — `claude/roadmap/workforce_capacity.md`, Effective 2026-05-27). Warn threshold: effort > 14 days.

| ST-ID | Item | Effort estimate | Midpoint (days) |
|-------|------|------------------|------------------|
| ST-01 | `BLG-FE-109` | M (~1–2 days) | 1.5 |
| ST-02 | `BLG-FE-110` | S–M (~0.5–1 day) | 0.75 |
| ST-03 | `BLG-FE-111` | S (~0.5 day) | 0.5 |
| ST-04 | `BLG-SPEC-91` | M (~2–3 days) | 2.5 |
| ST-05 | `BLG-SPEC-92` | L (~3–4 days) | 3.5 |
| ST-06 | `BLG-SPEC-93` | M (~2 days) | 2.0 |
| ST-07 | `BLG-SPEC-94` | M (~2–3 days) | 2.5 |
| **Total** | | | **13.25** |

At the midpoint, total estimated effort (13.25 days) sits within the ~12–14 day capacity band, but with a materially thinner buffer than v7.2 (0.75 days to the 14-day warn threshold, versus v7.2's 3.5 days). Pessimistic reading (top of every range; `BLG-SPEC-93` has no range, counted at its single 2.0d estimate): 2 + 1 + 0.5 + 3 + 4 + 2 + 3 = 15.5 days — exceeds the band by 1.5 days, same absolute pessimistic total as v7.2 coincidentally, but against a higher midpoint this time.

**Outcome: PASS** (midpoint 13.25d ≤ 14d threshold). No formal Phasing Recommendation is required by rule, but given the thin buffer — directly the pattern flagged in this cycle's own Carry-Forward Advisory (v7.1/v7.2's zero-buffer capacity lesson) — Sprint Planning should treat this as effectively WARN-adjacent: monitor closely whether `BLG-SPEC-92` (the widest single range, L ~3–4d) or `BLG-SPEC-94` (schema-decision item) trend toward their pessimistic estimates early, and be prepared to phase `BLG-SPEC-94` (S2-07, least urgent of the four readiness passes — no other item depends on it within this release) into a second sprint if capacity tightens.

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity

- All S2 IDs map to an EPIC: S2-01, S2-02, S2-03 → EPIC-01; S2-04 → EPIC-02; S2-05 → EPIC-03; S2-06 → EPIC-04; S2-07 → EPIC-05. PASS.
- All EPIC IDs in `stage4_backlog_slice.md` match the Execution Plan (STEP 3): EPIC-01 through EPIC-05 present and consistent in both. PASS.
- All RISK IDs referenced in the Execution Plan EPIC table (RISK-01 through RISK-05) appear as rows in the Risk Register Summary. PASS.
- No orphaned S2/EPIC/RISK references found.

**Outcome: PASS.**

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
attributes.cross_stage_integrity: pass
```

## Integrity Validation — 5.7 Decision Record Integrity

Skipped — `artifacts.escalations` is not `present` this cycle (0 escalations raised). Per STEP 5.5 rule, this check runs only when escalations exist.

```yaml
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.decisions_validated: not_applicable
```

---
