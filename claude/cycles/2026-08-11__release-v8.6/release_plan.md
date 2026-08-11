Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v8.6
Cycle: 2026-08-11__release-v8.6
Last Updated: 2026-08-11

---

# Release Plan — v8.6

## Readiness

Backlog-driven release (no formal `## v8.6` roadmap section — cleared via STEP -1.2 Option (b) equivalence, same precedent as `v8.5`; see `run_manifest.md`). User instruction carried into this cycle: fill capacity fully, prioritise user-facing features.

- Preflight: PASS (all sub-checks — see `run_manifest.md`).
- Advisories: none blocking. Backlog Age, Provisional-Target, Design-Gate Language, and Gate-Condition Proximity scans all reviewed — see `run_manifest.md` for detail.
- Gate-detection scan (`scripts/scan_backlog_gate_conditions.py`): 177/311 items gated. `BLG-FEAT-32`'s gate cleared 2026-08-11 (same-day roadmap rebalance); `BLG-BE-91` ungated.
- Perennial-Return Check: not triggered — no candidate item in this cycle's scope has a 2+ consecutive-cycle `returned_to_backlog` history.
- Within-Sprint Date Gate Classification (§1.4b): `BLG-FEAT-56`'s date-half condition (AI adoption window, ~2026-07-25) is cleared and is a pre-sprint-planning gate, not a within-sprint one — §1.4b's mandatory-conditional rule does not apply. Its qualitative-usage-pattern condition is resolved via an explicit Product Owner disposition (see Decisions Record).

```yaml
artifacts.stage1_readiness: pass
```

---

## Scope

**Selection principle (per user instruction):** user-facing feature items led first; `v8.6`-provisioned carryover from `v8.5` PR-review findings closed in full; capacity filled to the top of the confirmed band.

### Items in scope

| S2-ID | EPIC | Theme |
|-------|------|-------|
| S2-01 | EPIC-01 | User-facing product features |
| S2-02 | EPIC-02 | Trade-plan data-integrity foundation |
| S2-03 | EPIC-03 | Frontend design-consistency & correctness carryover |
| S2-04 | EPIC-04 | Backend & financial correctness |
| S2-05 | EPIC-05 | QA test-coverage debt closure |
| S2-06 | EPIC-06 | Operations & governance debt closure |

Full item-level detail (26 stories) is the authoritative scope record in `stage4_backlog_slice.md`.

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| `BLG-FEAT-73` (SI-02 frontend build) | Gate not met — 0/20 closed trades currently have linked trade plans; `BLG-BE-91` (this cycle) enforces linkage going forward but does not backfill, so the gate can only clear via new linked trade plans accruing after this cycle ships. | Re-check next cycle |
| `BLG-FEAT-74` (PO-05 Replay Mode) | Gated — §13 determinism pre-clearance not run; VH effort (>2 weeks) exceeds single-cycle sizing. | Unscheduled — needs phasing decision first |
| `BLG-FEAT-44` (Arc 5 low-volume advisory) | Gate not met — requires Arc5ComplianceSection live 3+ months post-v4.1 ship (2026-05-27 + 3mo = 2026-08-27); 16 days short at cycle date. | Next cycle (gate clears 2026-08-27) |
| `BLG-SPEC-124` (canonical "gated" DataState variant spec) | Ungated but not selected — spec-debt item, lower priority than shipped user-feature/correctness scope this cycle given capacity already filled. | Next cycle |
| All other gated backlog items (175 of 177 scanned) | Gate conditions not met — see `scripts/scan_backlog_gate_conditions.py` output, `run_manifest.md`. | Per individual gate conditions |

```yaml
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-01 | Product Owner | RISK-01 | None — leads the table per Skill-Silo rotation guideline (§3), given the 2026-08-11 rebalance's 3rd-consecutive-worsening Skill-Silo Alert (89.8%) |
| EPIC-02 | S2-02 | Data Model, Domain & Schema Owner; Backend Engineering Patterns Owner | RISK-02 | None |
| EPIC-03 | S2-03 | Frontend Specifications & UX Documentation Owner | RISK-03 | ST-04 (BLG-FE-147, remaining shadcn token registration) should land before/alongside ST-05 (BLG-FE-148, Playwright coverage for those tokens) |
| EPIC-04 | S2-04 | Financial Reporting & Records Owner; Cybersecurity & Trust Lead | RISK-04 | None |
| EPIC-05 | S2-05 | Director of Quality | RISK-05 | None |
| EPIC-06 | S2-06 | Head of Specs Team | RISK-06 | None |

**EPIC-01 note:** Both items are user-facing features explicitly prioritised per this cycle's invocation instruction. `BLG-FEAT-56`'s usage-pattern gate condition is resolved via Product Owner active disposition (Decisions Record) rather than a hard telemetry threshold — tracked as RISK-01.

**EPIC-02 note:** `BLG-BE-91` is the Product Owner's named structural response to the 2026-08-11 rebalance's mandatory Skill-Silo pull-forward finding — it targets the root cause (0/11 trade plans linked to positions) currently blocking `BLG-FEAT-73`'s gate and the wider Arc 5 UX-prep cluster.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | `BLG-FEAT-56`'s "established, validated usage patterns" gate condition is a qualitative PO judgment, not a hard metric — risk of shipping a feature onto an insufficiently-validated AI surface | Medium | Explicit PO written disposition recorded in Decisions Record, citing 47 days of live v6.2 AI-touchpoint usage with no adoption-abandonment signal | null |
| RISK-02 | EPIC-02 | `BLG-BE-91`'s DB-level safeguard (constraint/trigger) risks blocking a legitimate edge-case position-creation flow if scoped too strictly | Medium | Staging verification required before merge per the item's own Acceptance Criteria; Data Model, Domain & Schema Owner + Product Owner sign-off required |  null |
| RISK-03 | EPIC-03 | Design-token and dark-class-sync changes are visually observable app-wide | Medium | Playwright coverage or staging sign-off required per CLAUDE.md's frontend-visible-change hard gate — already an explicit AC on every EPIC-03 item | null |
| RISK-04 | EPIC-04 | Financial-correctness audits (cost-basis rounding, tax-year export boundary) may surface a real historical-data discrepancy requiring a data fix, not just a code fix | Low | Scope is audit-first ("fix any inconsistency found"); Financial Reporting & Records Owner sign-off required before closing | null |
| RISK-05 | EPIC-05, EPIC-06 | 26 items across 6 EPICs for a single solo-dev contributor is a full capacity load — execution overrun risk | Low | STEP 4.5 Capacity Check below confirms fit within the confirmed ~24-28 day band; Sprint Planning may phase across sprints if needed | null |
| RISK-06 | EPIC-06 | Governance/process debt items (EPIC-06) are low-individual-risk but numerous (8 items) — risk of crowding capacity better spent on EPIC-01/02 user-value work | Low | Each item is XS/S effort (~0.4-1.0d); combined EPIC-06 total (~3.4d) is a small fraction of total capacity — accepted as a low-cost cleanup of this cycle's own PR-review findings | null |

```yaml
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
```

---

## Integrity Validation — 3.5 Local Model Integrity

No local model/data-schema changes proposed by this plan beyond what individual stories (`BLG-BE-91`, `BLG-BE-92`) will scope during execution — no plan-time schema conflict identified. PASS.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Capacity Check

**Effort Band Lookup:** `claude/scoring/scored_initiatives.md` not present in this repository — all EPICs fall to tier 3 (inline STEP 4 estimate; no advisory required per the three-tier resolution rule).

| Effort band | Item count | Midpoint days each | Subtotal |
|-------------|------------|---------------------|----------|
| M  | 5  | 1.75 | 8.75 |
| S  | 9  | 1.00 | 9.00 |
| XS | 12 | 0.50 | 6.00 |
| **Total** | **26** | | **~23.75 days** |

Confirmed capacity band: ~24-28 capacity-day units (`workforce_capacity.md`, unchanged since the 2026-07-17 out-of-band raise, last re-affirmed 2026-07-28__scheduled) — solo developer, evenings/weekends, all governance roles agent-embodied over the single contributor. No scarce/role-locked skill constraint flagged.

**Outcome: PASS.** ~23.75 days sits within the confirmed band, near its top — consistent with the explicit "use full capacity" instruction, without exceeding the upper bound. No phasing recommendation required.

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```
