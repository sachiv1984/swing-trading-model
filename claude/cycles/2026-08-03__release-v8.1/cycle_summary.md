Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Filed
Report Date: 2026-08-03
Cycle: 2026-08-03__release-v8.1
Release: v8.1
Design Gate Required: true

# Cycle Summary — Release Planning v8.1

## Outcome

Release Plan **Validated**, `publish_eligible = true`. Scope: 19 stories across 7 grouped EPICs, backlog-driven (no formal roadmap release section — STEP -1.2 Option (b) equivalence from `2026-07-28__scheduled`, same decision already relied on by `2026-07-30__release-v8.0`), sized to the top of the confirmed ~24-28 day capacity band (~25.75 days midpoint, ~92-107% utilisation) per explicit user instruction ("Use full capacity"). Per the user's companion instruction ("Focus on user features where possible"), an exhaustive scan of all `BLG-FEAT-*`/`BLG-FE-*` candidates found **exactly one** ready, ungated, genuinely user-facing item (`BLG-FE-137`) — every other candidate remains gate-blocked on inspection of its substantive Problem statement, most tracing back to the SI-02 trade-plan-linkage data-density gate. This scarcity is a first-class finding, not a selection artefact — see Deferred/Excluded below and `run_manifest.md`.

## EPICs

| EPIC-ID | Theme | Stories | Owner |
|---------|-------|---------|-------|
| EPIC-01 | User-Facing Accessibility Fix | ST-01 | Base44 Frontend Prompt Owner; Head of UX & Design |
| EPIC-02 | Operational Safety | ST-02 | Infrastructure & Operations Owner |
| EPIC-03 | Governance Process Hardening | ST-03–ST-09 | Product Owner; Challenger; FinOps & Resource Architect; Head of Engineering; Director of HR; AI Compliance & Governance Officer; Head of Specs Team |
| EPIC-04 | QA Process & Debt Closure | ST-10–ST-13 | Director of Quality; QA Lead; QA & Testing Owner |
| EPIC-05 | Spec Debt: SI-02 Definitional Clarity | ST-14–ST-16 | Product Owner; Strategy Rules & System Intent Owner; Head of UX & Design |
| EPIC-06 | Backend Hardening | ST-17–ST-18 | Backend Engineering Patterns Owner; Data Model & Domain Schema Owner |
| EPIC-07 | Cross-EPIC Execution State Structural Fix | ST-19 | Head of Engineering |

## Gate Outcomes

| Gate | Outcome |
|------|---------|
| STEP -1 Preflight | PASS |
| STEP 1 Readiness | pass |
| STEP 3.5 Local Model Integrity | pass |
| STEP 4.5 Capacity Feasibility | pass (~25.75d / ~24-28d band, ~92-107% utilisation) |
| STEP 5.5 Cross-Stage Integrity | pass |
| STEP 5.7 Decision Record Integrity | not_applicable (no escalations raised) |
| Publish Gate | pass — `status = Validated`, `publish_eligible = true` |

## Design Gate

`design_gate_required = true`. EPIC-01 (`BLG-FE-137`) carries one observable UI interaction acceptance criterion (keyboard operability of the trade-tag suggestion buttons). Run `run design-gate --cycle 2026-08-03__release-v8.1` before `plan sprint`.

## Deferred / Excluded This Cycle

- `BLG-FEAT-73`/`BLG-FEAT-74` — SI-02 gate NOT MET / §13 pre-clearance not run; 2nd consecutive cycle excluded — STEP 1.4a Perennial-Return Check applied, Product Owner disposition: Option (a), kept conditional with updated per-item evidence.
- Arc 5 UX-prep cluster (`BLG-FEAT-44/56`, `BLG-FE-43/45/54/58/59/62/63/68/69/70/71`) — each item's own Problem statement names a substantive unmet precondition (Arc 6 unscoped, SI-02/SI-04/SI-05 sprint-planning-imminent not true, Phase 2 channel undecided, AI-usage-pattern validation unverifiable in this checkout).
- `BLG-FEAT-45` — gate clears 2026-08-05, inside the likely sprint window; STEP 1.4b mandates conditional-only classification for within-sprint date gates regardless of proximity.
- `BLG-OPS-48` — gate date 2026-11-01, unchanged.
- `BLG-BE-24` — gate: `red_flag_events` table 6+ months old (post 2026-11-22).
- ~140 remaining ungated P2/P3 candidates — capacity reached; carried forward as the `v8.2` candidate pool.

## Escalations

None raised this cycle.

## Advisory Findings (surfaced, not blocking)

- **Product-value scarcity (RISK-03):** 18 of 19 scoped items (~25.25 of ~25.75 days) are governance/QA/spec/backend debt; only 1 item is user-facing. This is consistent with — and further evidence for — the declining Product Value Ratio (0.42 → 0.38 across the last two rebalance windows). `BLG-GOV-280`/`BLG-GOV-268` (this cycle's own scope) are the direct structural remedy; recommend the next `run roadmap` rebalance treat this reading as a strong signal.
- **`prior_cycle` field staleness:** `.claude_current_state.json.prior_cycle` still reads `2026-07-21__release-v7.7`, three releases behind the actual chain. Outside this engine's write scope to correct — flagged for the owning engine (Post-Ship Closure).

## Artefacts Produced

- `claude/cycles/2026-08-03__release-v8.1/run_manifest.md`
- `claude/cycles/2026-08-03__release-v8.1/state.json`
- `claude/cycles/2026-08-03__release-v8.1/release_plan.md`
- `claude/cycles/2026-08-03__release-v8.1/stage4_backlog_slice.md`
- `claude/cycles/2026-08-03__release-v8.1/stage4_issue_manifest.json`
- `claude/cycles/2026-08-03__release-v8.1/backlog_txn.json`
- `claude/cycles/2026-08-03__release-v8.1/roadmap_txn.json`
- `docs/product/scope/scope--2026-08-03__release-v8.1.md`
- `docs/product/decisions/decisions--2026-08-03__release-v8.1.md`
- `claude/cycles/2026-08-03__release-v8.1/cycle_summary.md` (this file)
- `claude/cycles/2026-08-03__release-v8.1/lessons_learnt.md`

## Next Step

`run design-gate --cycle 2026-08-03__release-v8.1`, then `plan sprint --cycle 2026-08-03__release-v8.1`.
