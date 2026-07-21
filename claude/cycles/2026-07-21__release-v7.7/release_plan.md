**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-21
**Cycle:** 2026-07-21__release-v7.7
**Release:** v7.7

# Release Plan — v7.7 — Strategy Intelligence Surfacing & Notification UX

## Readiness

Roadmap release confirmed: `current_roadmap.md` §3 `### v7.7` section, formalized 2026-07-21 (DL-074), 7 named anchor items. Preflight PASS (see `run_manifest.md` for full STEP -1 detail). Prior cycle `2026-07-20__release-v7.6` closed clean (`post_ship_complete=true`, `next_cycle_unblocked=true`), 0 outstanding action-now gaps.

**Design-gate language scan (1.3):** 4 of 11 scoped items carry observable UI acceptance criteria (EPIC-01/02/03/04) — Design Gate required, see STEP 4.1.

**Gate-condition live re-check (1.4):** SI-02 (`BLG-GOV-107`) re-confirmed **NOT MET** via direct production API, 2026-07-21T08:49 UTC — 9th consecutive byte-identical reading since 2026-07-12 (20 closed trades, 11 trade-plans, 0 linked, `behavioural-drift` still `insufficient_data`/9 trades in 90-day window). Full detail in `run_manifest.md`.

```yaml
artifacts.stage1_readiness: pass
```

## Scope

**Firm scope — 11 items (S2-01–S2-11):**

| S2 | Item | Priority | Effort | Type |
|----|------|----------|--------|------|
| S2-01 | BLG-FEAT-75 — SI-04 Strategy Version Comparison | P2 | H (>5d) | Product Feature, FE+BE |
| S2-02 | BLG-FE-114 — Consolidate notification/digest surfaces | P2 | M (~1–2d) | Frontend/UX |
| S2-03 | BLG-FE-113 — Confirm AiDailyBriefing light-theme rendering | P2 | XS–S | Frontend/UX |
| S2-04 | BLG-FE-120 — Shared toast/notification primitive | P2 | M | Frontend/UX Infra |
| S2-05 | BLG-FEAT-80 — Investigate UX nudge for SI-02 trade-count gate | P2 | M | Product Feature/Growth (investigation) |
| S2-06 | BLG-OPS-108 — CI curl response validation (daily-snapshot.yml) | P1 | S (~0.5–2d) | Ops/Infra |
| S2-07 | BLG-GOV-28 — PT-04 §13 compliance review (retroactive) | P1 | S (~0.5d) | Governance |
| S2-08 | BLG-QA-104 — numpy-scalar regression test (create_rebalance_exit_signal) | P2 | XS (<1d) | QA/Backend |
| S2-09 | BLG-BE-63 — Nightly backtest job idempotency check | P2 | S (~1d) | Backend/Data Integrity |
| S2-10 | BLG-OPS-110 — Nightly backtest job monitoring/alerting | P2 | M (~1–2d) | Operations |
| S2-11 | BLG-QA-102 — Automate endpoint-count drift check (CLAUDE.md §2) | P2 | M | QA/Process Tooling |

**Items explicitly deferred (named on roadmap, excluded from firm scope this cycle):**

| Item | Reason |
|------|--------|
| BLG-FEAT-73 — SI-02 Behavioural Drift Detection frontend build | `BLG-GOV-107` gate re-confirmed NOT MET live 2026-07-21 (9th consecutive identical reading). Per its own LP-05 flag, may not enter sprint planning until independently reconfirmed met. Remains `Provisional-Target: v7.7` on roadmap, unresolved. |
| BLG-FEAT-74 — PO-05 Lightweight Replay Mode | No §13 determinism pre-clearance review on record (required before scope entry). Effort (VH, >2 weeks) also exceeds this release's realistic single-cycle capacity even if the gate cleared. Recommend a dedicated §13 review be scheduled before reconsideration. |

Scope document: `docs/product/scope/scope--2026-07-21__release-v7.7-strategy-intelligence-notification-ux.md`

```yaml
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-01 | Head of Engineering; Head of UX & Design | RISK-01 | First among design-gated items (largest effort) |
| EPIC-02 | S2-02 | Head of UX & Design; Frontend Specs & UX Documentation Owner | RISK-02 | After Design Gate pass |
| EPIC-03 | S2-03 | Head of UX & Design; Frontend Specs & UX Documentation Owner | RISK-02 | After Design Gate pass |
| EPIC-04 | S2-04 | Base44 Frontend Prompt Owner | RISK-02, RISK-03 | After Design Gate pass |
| EPIC-05 | S2-05 | Product Owner | null | No dependency; investigation-only |
| EPIC-06 | S2-06 | Infrastructure & Operations Owner | null | No dependency |
| EPIC-07 | S2-07 | Head of Specs Team | null | No dependency |
| EPIC-08 | S2-08 | QA & Testing Owner | null | No dependency |
| EPIC-09 | S2-09 | Backend Engineering Patterns Owner | null | Before EPIC-10 |
| EPIC-10 | S2-10 | Infrastructure & Operations Owner; Head of Engineering | null | After EPIC-09 |
| EPIC-11 | S2-11 | QA & Testing Owner | null | No dependency |

EPIC-01: SI-04's own backlog note asks Release Planning to confirm whether a trade-volume gate is warranted (unlike SI-02, no such gate is currently stated for SI-04). PO decision: no gate required — SI-04 compares performance across `strategy_rules.md` versions rather than needing an absolute trade count; the version-tagged trade history foundation is already populated and unused. Recorded in `decisions--2026-07-21__release-v7.7.md`.

EPIC-06/07/08/09/10/11 have no UI surface and no cross-EPIC dependency on EPIC-01–04; may execute in parallel to the design-gated cluster.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | Largest single item (H, >5d) — could absorb a disproportionate share of sprint capacity if under-scoped | Medium | Sequence first; sprint planning to confirm a bounded MVP slice (win rate/avg-R/compliance-rate compare) before any stretch scope | null |
| RISK-02 | Release-level (EPIC-01/02/03/04) | 4 of 11 items carry observable UI ACs — Design Gate is a hard prerequisite before Sprint Planning seals | Medium | `run design-gate --cycle 2026-07-21__release-v7.7` must run and PASS (or record a bypass with authority+reason) before `plan sprint` is invoked | null |
| RISK-03 | EPIC-04 | `BLG-FE-120`'s shared toast primitive is listed as an enabler for `BLG-FE-116` (not in this release's scope) | Low | No mitigation required this cycle — build the primitive to spec regardless of the consuming feature's own scheduling | null |
| RISK-04 | Release-level | `BLG-FEAT-73`/`BLG-FEAT-74` remain named `v7.7` anchors on the roadmap despite exclusion from this cycle's firm scope — risk of scope confusion if Sprint Planning reads the roadmap anchor list instead of the backlog slice | Low | `stage4_backlog_slice.md` is the sole authoritative scope source per §8 of this prompt; decisions record states the exclusion explicitly | null |

Decisions record: `docs/product/decisions/decisions--2026-07-21__release-v7.7.md`

```yaml
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

## Integrity Validation — 3.5 Local Model Integrity

All EPIC IDs map to declared S2 IDs; all RISK IDs referenced in the Execution Plan table appear in the Risk Register; no orphaned references. PASS.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

## Capacity Check

**Capacity Inputs** (per `workforce_capacity.md` / DL-069 convention, consistent with v7.6's own capacity doc):
```
Available FTE:   1 (solo developer / autonomous execution engine)
Total capacity:  ~24–28 working-day-equivalent per sprint
```

**Effort Band Lookup (ST-14):** `claude/scoring/scored_initiatives.md` not present — Tier 3, STEP 4 inline estimates used for all 11 EPICs, no advisory required.

| EPIC | Item | Effort | Midpoint (days) |
|------|------|--------|------------------|
| EPIC-01 | BLG-FEAT-75 | H (>5d) | 6.5 |
| EPIC-02 | BLG-FE-114 | M (~1–2d) | 1.5 |
| EPIC-03 | BLG-FE-113 | XS–S | 0.75 |
| EPIC-04 | BLG-FE-120 | M (no range) | 2.0 |
| EPIC-05 | BLG-FEAT-80 | M | 2.0 |
| EPIC-06 | BLG-OPS-108 | S (~0.5–2d) | 1.25 |
| EPIC-07 | BLG-GOV-28 | S (~0.5d) | 0.5 |
| EPIC-08 | BLG-QA-104 | XS (<1d) | 0.5 |
| EPIC-09 | BLG-BE-63 | S (~1d) | 1.0 |
| EPIC-10 | BLG-OPS-110 | M (~1–2d) | 1.5 |
| EPIC-11 | BLG-QA-102 | M (no range) | 2.0 |

**Total estimated effort:** ~19.5 days midpoint (range ~16–24 days).
**Confirmed capacity:** ~24–28 working-day-equivalent.
**Utilisation:** ~70–81% of ceiling.

**No over-allocation. No capacity WARN.** This deliberately maximises utilisation per explicit user instruction ("ensure you use full capacity") while retaining ~20–30% buffer against estimate variance — see `run_manifest.md` Full-Capacity Fill Rationale for the selection method. No Phasing Recommendation needed (outcome is `pass`, not `warn`).

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

## Roadmap Annotation

See `current_roadmap.md` §3 `### v7.7` section — execution notes appended at STEP 5 (below).

## Cross-Stage Integrity (5.5) / Decision Record Integrity (5.7)

**5.5:** All S2 IDs (S2-01–S2-11) map to EPICs (EPIC-01–EPIC-11, 1:1). All EPIC IDs in `stage4_backlog_slice.md` match this Execution Plan. All RISK IDs (RISK-01–04) appear in the Risk Register above. No orphaned references. PASS.

**5.7:** No escalations were raised this cycle (`artifacts.escalations` not present) — this check is `not_applicable`.

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```
