Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-05
Cycle: 2026-08-05__release-v8.3
Release: v8.3

# Release Plan — v8.3

## Readiness

Preflight (STEP -1) passed all hard gates. Prior cycle `2026-08-04__release-v8.2` is `Closed` with `post_ship_complete = true` and `next_cycle_unblocked = true`. No `## v8.3` roadmap section exists; this release is scoped via the STEP -1.2 Option (b) equivalence rule, citing the same `2026-07-28__scheduled` rebalance's documented STEP 8.1 Option (b) decision already relied on by `2026-07-30__release-v8.0`, `2026-08-03__release-v8.1`, and `2026-08-04__release-v8.2` (Now horizon fully empty, deferred again; no `run roadmap` invocation has occurred since to supersede it). See `run_manifest.md` for full STEP -1 detail.

**No explicit user scope-priority instruction this session** (contrast `v8.1`/`v8.2`'s "use full capacity, focus on user features"). Scope selected under Product Owner delegated authority. Headline finding: **no ungated P1/P2 U-shaped (build-and-ship product feature) item exists in the backlog** — unchanged since `2026-07-27__scheduled`. The only ready user-adjacent item, `BLG-FEAT-45`, is a lightweight retrospective review, not new build scope.

**STEP 1.4a Perennial-Return Check + STEP 1.4a.1 Sunset Criteria — mandatory this cycle:** `BLG-FEAT-73`/`BLG-FEAT-74` have now received Option (a) "keep as conditional" at 3 consecutive prior cycles (`v8.0`, `v8.1`, `v8.2`); this cycle is the 4th. Per §1.4a.1 the disposition escalates from advisory to mandatory at exactly this count. No materially new gate-clearance path exists for either item. **Product Owner disposition: Option (b) — Remove from horizon, park until gate permanently cleared.** See `run_manifest.md` for full reasoning. The dependent Arc 5 UX-prep cluster remains excluded on the same basis.

**STEP 1.4b Within-sprint date gate check:** `BLG-FEAT-45` clears its `≥ 2026-08-05` gate exactly today. Promoted conditional → firm per the dated Product Owner confirmation recorded in `run_manifest.md`. No other candidate carries a within-sprint date gate.

**Self-caught scan miss:** `BLG-GOV-74` was found, on a full-text re-read, to carry a `**Gate date:** First review due 2026-08-29` field (a variant not caught by the initial field-label scan) — excluded before commit. See `run_manifest.md` and `lessons_learnt.md`.

```yaml
artifacts.stage1_readiness: pass
```

---

## Scope

No scope changes to strategy or roadmap boundaries. This section extracts a backlog-driven scope slice (no formal roadmap release section exists yet for v8.3 — see Readiness above). Items are grouped into 6 thematic EPICs: two operational P1/P2 items lead EPIC-01, followed by balanced Backend/Frontend/QA-Spec/Governance debt clusters and one small product-retrospective EPIC.

### Items in scope

| S2-ID | Epic | Item | Description |
|-------|------|------|-------------|
| S2-01 | EPIC-01 | BLG-OPS-129 | Investigate and fix the SI-05 weekly Telegram digest delivery pipeline |
| S2-01 | EPIC-01 | BLG-OPS-130 | Add delivery-failure alerting for the SI-05 weekly digest |
| S2-01 | EPIC-01 | BLG-OPS-131 | Recurring check confirming staging/production API keys remain distinct |
| S2-01 | EPIC-01 | BLG-SEC-17 | Gemini API key rotation runbook |
| S2-02 | EPIC-02 | BLG-BE-37 | Database index audit for Arc 4 cross-table queries |
| S2-02 | EPIC-02 | BLG-BE-57 | Alpaca API rate-limit backoff audit |
| S2-02 | EPIC-02 | BLG-BE-67 | Canonical enum registry for position_state values shared frontend/backend |
| S2-02 | EPIC-02 | BLG-BE-69 | Conform remaining routers to canonical error envelope + status codes |
| S2-02 | EPIC-02 | BLG-BE-79 | Retry/backoff for Yahoo Finance regime-check call sites |
| S2-02 | EPIC-02 | BLG-BE-80 | Idempotent retry for Alpaca paper-trading order sync |
| S2-03 | EPIC-03 | BLG-FE-103 | Shared modal shell for compliance/checklist components |
| S2-03 | EPIC-03 | BLG-FE-121 | Extract a shared modal-confirmation component |
| S2-03 | EPIC-03 | BLG-FE-126 | Unified loading-skeleton pattern for async-loading cards |
| S2-03 | EPIC-03 | BLG-FE-132 | Standard Base44 prompt section for dark/light theme compliance |
| S2-03 | EPIC-03 | BLG-FE-81 | AI disclaimer component extraction |
| S2-04 | EPIC-04 | BLG-QA-86 | Add baseline Playwright coverage for Watchlist.js |
| S2-04 | EPIC-04 | BLG-QA-94 | OpenAPI drift gate false-negative sweep |
| S2-04 | EPIC-04 | BLG-QA-98 | DoQ sign-off staleness pre-merge lint |
| S2-04 | EPIC-04 | BLG-SPEC-88 | OpenAPI response-example drift spot-check |
| S2-04 | EPIC-04 | BLG-SPEC-96 | API endpoint deprecation-window policy |
| S2-04 | EPIC-04 | BLG-SPEC-108 | Canonical form validation error-message pattern spec |
| S2-05 | EPIC-05 | BLG-GOV-124 | SC-02: Remove RESUME PRECHECK mutation detection block from release_planning_prompt.md |
| S2-05 | EPIC-05 | BLG-GOV-204 | Formal §13 boundary re-attestation cadence |
| S2-05 | EPIC-05 | BLG-GOV-237 | SI-02 trade-count gate threshold calibration review |
| S2-05 | EPIC-05 | BLG-GOV-257 | prompt_change_log.md mixed prepend/append ordering breaks gap detection |
| S2-05 | EPIC-05 | BLG-GOV-270 | Cross-role workload balance check |
| S2-06 | EPIC-06 | BLG-FEAT-45 | Monthly P&L report format review — 3-month usage retrospective |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| BLG-FEAT-73 / BLG-FEAT-74 | SI-02 gate unmet / §13 pre-clearance not run; 4th consecutive Option (a) would have fired — STEP 1.4a.1 mandatory sunset trigger applied, Product Owner disposition **Option (b) — parked** | Unscheduled, pending gate clearance or a materially new gate-clearance path documented at a future cycle |
| Arc 5 UX-prep cluster (BLG-FEAT-44/56, BLG-FE-43/45/54/58/59/62/63/68/69/70/71) | Dependent on the now-parked BLG-FEAT-73 SI-02 UX surface; each item's own Problem statement also names a substantive unmet precondition | Unscheduled, pending respective gate clearance |
| BLG-GOV-74 | Self-caught scan miss — carries `**Gate date:** First review due 2026-08-29`, outside this cycle's execution window | v8.3+ (first cycle on/after 2026-08-29), or the cycle nearest that date |
| BLG-BE-24 | Gate: `red_flag_events` table 6+ months old (post 2026-11-22) | Unscheduled, pending gate |
| Remaining ungated P2/P3 candidates not selected this cycle | Capacity — curated highest-value selection made rather than exhaustive fill | v8.4 candidate pool |

```yaml
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

**Format note:** compact table per IMP-08; full acceptance criteria live in `stage4_backlog_slice.md`.

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-01 (4 items) | Infrastructure & Operations Owner; Cybersecurity & Trust Lead | — | BLG-OPS-130 depends on BLG-OPS-129's root-cause finding |
| EPIC-02 | S2-02 (6 items) | Infrastructure & Operations Owner; Head of Engineering; Data Model & Domain Schema Owner; Backend Engineering Patterns Owner | RISK-01 | None |
| EPIC-03 | S2-03 (5 items) | Base44 Frontend Prompt Owner; Head of Engineering; Head of UX & Design | RISK-02 | None |
| EPIC-04 | S2-04 (6 items) | Director of Quality; API Contracts & Documentation Owner; Frontend Specifications & UX Documentation Owner | — | None |
| EPIC-05 | S2-05 (5 items) | Head of Specs Team; AI Compliance & Governance Officer; Strategy Rules & System Intent Owner; Director of HR | — | None |
| EPIC-06 | S2-06 (1 item) | Financial Reporting & Records Owner | — | None |

EPIC-02: `BLG-BE-69`'s own scope note flags it as "a large mechanical change across ~17 files — apply incrementally, not as one PR"; see RISK-01.

EPIC-03: carries two observable UI acceptance criteria (`BLG-FE-103` and `BLG-FE-81` both require a confirmed no-visual-regression check) — classified `design_gate_required = true` at STEP 4.1 below.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|----------------|
| RISK-01 | EPIC-02 | `BLG-BE-69` touches error-response paths across ~17 router files; a single oversized PR would be difficult to review safely | Low | Apply incrementally per the item's own scope note — split into multiple sequenced commits/PRs rather than one large diff | null |
| RISK-02 | EPIC-03 | `BLG-FE-103` and `BLG-FE-81` both require confirmed no-visual-regression evidence (new Playwright coverage for FE-103; existing assertions re-confirmed for FE-81) before their ACs may be considered met | Low | Run `run design-gate --cycle 2026-08-05__release-v8.3` promptly after this plan publishes; Playwright coverage or a recorded staging sign-off required per CLAUDE.md for each observable AC | null |
| RISK-03 | Release-level | `BLG-FEAT-73`/`BLG-FEAT-74` formally parked this cycle under the STEP 1.4a.1 mandatory sunset trigger — Arc 5's flagship SI-02 frontend feature and the PO-05 replay mode both move from "recurring conditional candidate" to "off active horizon" | Medium (product-value, not delivery risk) | Both items remain in the backlog and can re-enter consideration if a materially new gate-clearance path is documented at a future rebalance or release planning session; no code or spec is lost | null |
| RISK-04 | Release-level | Scope sized to ~25.25 days midpoint against the confirmed ~24-28 day capacity band (~90-105% utilisation depending on denominator) — near the middle-to-top of band, no explicit "full capacity" instruction this cycle so not deliberately padded to the ceiling | Low | STEP 4.5 Capacity Check below confirms no over-allocation against the ceiling | null |

```yaml
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

All EPIC-ID / S2-ID / RISK-ID cross-references above resolve internally (27 items ↔ 6 S2-IDs ↔ 6 EPIC-IDs, grouped 4/6/5/6/5/1; 2 RISK-IDs reference EPIC-02/EPIC-03 plus 2 Release-level RISK-IDs). No orphaned references found.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Capacity Check

**Effort Band Lookup (ST-14):** No matching rows in `scored_initiatives.md` for any of the 27 selected items (0 populated initiative rows this cycle) — Tier 3 applies uniformly; STEP 4 inline per-item estimates used throughout, sourced from each item's own `**Effort:**` field and parenthetical day-range where given, midpoint used where only a letter band is given.

| EPIC | Items | Effort (midpoint days) |
|------|-------|------------------------|
| EPIC-01 | 4 | 4.25 |
| EPIC-02 | 6 | 4.50 |
| EPIC-03 | 5 | 6.00 |
| EPIC-04 | 6 | 4.50 |
| EPIC-05 | 5 | 5.50 |
| EPIC-06 | 1 | 0.50 |
| **Total** | **27** | **25.25** |

Confirmed capacity band: ~24-28 days/sprint (standing, `workforce_capacity.md`, effective 2026-07-17, unchanged across the last several rebalances). ~25.25 days midpoint against this band = **~90-105% utilisation** depending on denominator — within band, no over-allocation, no phasing recommendation required.

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Design Gate Classification (STEP 4.1)

`design_gate_required = true`. `BLG-FE-103` and `BLG-FE-81` (EPIC-03) each carry an observable UI acceptance criterion (confirmed no-visual/behavioural regression). Run `run design-gate --cycle 2026-08-05__release-v8.3` before `plan sprint`.

```yaml
attributes.design_gate_required: true
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity

All S2 IDs (S2-01–S2-06) map to EPICs (EPIC-01–EPIC-06) 1:1. All EPIC IDs in `stage4_backlog_slice.md` match this document's Execution Plan. All RISK IDs referenced in the EPIC table (RISK-01, RISK-02) appear in the Risk Register Summary; RISK-03/RISK-04 are release-level and correctly carry no EPIC reference. No orphaned references found.

**5.7 Decision Record Integrity:** Not applicable — no escalations raised this cycle (`artifacts.escalations` remains `not_started`).

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```

---

## Publish Gate

All conditions met: `open_escalations` empty; no deferred execution blockers; `stage4_5_capacity_check = pass`; `stage5_5_cross_stage_integrity = pass`; `stage5_7_decision_record_integrity = not_applicable`; `stage1_readiness`/`stage3_5_model_integrity = pass`; `plan_structured`/`plan_executable`/`backlog_committed = true`.

`status = Validated`, `publish_eligible = true`.

**Completion condition:** `docs/product/scope/scope--2026-08-05__release-v8.3.md` and `docs/product/decisions/decisions--2026-08-05__release-v8.3.md` both created (see below); `locks.backlog_lock.status = released`; `locks.roadmap_lock.status = released`.
