Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-21
Cycle: 2026-08-21__release-v9.0

# Sprint Capacity — 2026-08-21__release-v9.0

## Capacity Inputs

```
Sprint duration:    ~1-2 calendar days between sprint starts (workforce_capacity.md, effective 2026-07-17); single-sprint cycle — no multi-sprint gate story this cycle.
Available capacity: ~24-28 working-day-equivalent units (solo-developer/agent-mediated context; no per-role FTE split — unchanged since 2026-07-17, confirmed current at 2026-07-28 scheduled rebalance and unaltered by the 2026-08-11 no-change rebalance)
Total capacity:     ~24-28 working-day-equivalent units
Skill constraints:  None material. EPIC-01's Backend Engineering Patterns Owner / Strategy Rules & System Intent Owner / AI Compliance & Governance Officer concurrency does not conflict with EPIC-02's Backend Engineering Patterns Owner demand — EPIC-01 is sequenced first (execution order below), so no simultaneous cross-EPIC role contention. EPIC-04's QA-heavy roster (Director of Quality, QA Lead, QA & Testing Owner, Financial Reporting & Records Owner) has no concurrent demand from other EPICs.
```

## Item Effort Mapping

Effort labels and day-range midpoints below are as carried from `claude/backlog/backlog.md` source items (via `stage4_backlog_slice.md`'s bare labels); EPIC day-subtotals are as computed and validated at `release_plan.md ## Capacity Check` (authoritative for the days total — reconciled exactly against the per-item midpoint convention stated there: XS=0.375d/S=1d/M=2d/L=4d defaults, explicit day-range midpoints where stated, `BLG-OPS-147` "<1h" = 0.15d).

| EPIC | Story | Source | Effort label | Midpoint (d) | Notes |
|------|-------|--------|--------------|---------------|-------|
| EPIC-01 | ST-01 | BLG-BE-109 | S (~0.5–1d) | 0.75 | Live production data-correctness bug — leads capacity allocation (RISK-01) |
| EPIC-01 | ST-02 | BLG-BE-107 | S (~0.5d) | 0.50 | |
| EPIC-01 | ST-03 | BLG-BE-108 | S (~0.5d, once decided) | 0.50 | `delegated_decision` — PO data-source decision |
| EPIC-01 | ST-04 | BLG-TECH-17 | S (~0.5–1d) | 0.75 | |
| EPIC-01 | ST-05 | BLG-TECH-15 | M (~1-2d) | 1.50 | Depends on ST-01 (same rebalance-date computation surface); RISK-01 |
| **EPIC-01 subtotal** | | | | **4.00d** | Matches `release_plan.md` exactly |
| EPIC-02 | ST-06 | BLG-BE-105 | S (~0.5–1d) | 0.75 | RISK-02 (live open-position stop backfill) — sequence first within EPIC per Execution Plan |
| EPIC-02 | ST-07 | BLG-FEAT-93 | S (~0.5d) | 0.50 | `delegated_decision` — PO sign-off required |
| EPIC-02 | ST-08 | BLG-BE-106 | S (~0.5d) | 0.50 | |
| EPIC-02 | ST-09 | BLG-BE-49 | S (~1 day) | 1.00 | |
| EPIC-02 | ST-10 | BLG-FE-164 | S (~0.5d) | 0.50 | Design Pre-Approved (PO downgrade) — outcome (FX field vs. spec-wording fix) not yet chosen |
| EPIC-02 | ST-11 | BLG-QA-153 | S (~0.5d) | 0.50 | |
| **EPIC-02 subtotal** | | | | **3.75d** | Matches `release_plan.md` exactly |
| EPIC-03 | ST-12 | BLG-OPS-103 | S (~0.5-2 days) | 1.25 | Staging-only evidence (restore drill against non-prod target) |
| EPIC-03 | ST-13 | BLG-OPS-25 | M (~2 days) | 2.00 | Staging-only evidence (deliberately-broken staging deploy dry run) |
| EPIC-03 | ST-14 | BLG-OPS-90 | M (~2 days) | 2.00 | |
| EPIC-03 | ST-15 | BLG-OPS-147 | XS (<1h) | 0.15 | Staging-only evidence (live Render dashboard confirmation) |
| EPIC-03 | ST-16 | BLG-OPS-148 | S (~0.5d) | 0.50 | |
| **EPIC-03 subtotal** | | | | **5.90d** | Matches `release_plan.md` exactly |
| EPIC-04 | ST-17 | BLG-QA-26 | M (~2 days) | 2.00 | |
| EPIC-04 | ST-18 | BLG-QA-81 | M (~2 days) | 2.00 | |
| EPIC-04 | ST-19 | BLG-QA-89 | S (~0.5-2 days) | 1.25 | |
| EPIC-04 | ST-20 | BLG-QA-144 | S (bare label, no range — default applied) | 1.00 | |
| EPIC-04 | ST-21 | BLG-QA-83 | S (~1 day) | 1.00 | |
| EPIC-04 | ST-22 | BLG-QA-84 | S (~1 day) | 1.00 | |
| **EPIC-04 subtotal** | | | | **8.25d** | Matches `release_plan.md` exactly |
| EPIC-05 | ST-23 | BLG-BE-56 | S (~0.5-2 days) | 1.25 | |
| EPIC-05 | ST-24 | BLG-BE-54 | S (~0.5-2 days) | 1.25 | Staging-only evidence (live connection-usage measurement) |
| EPIC-05 | ST-25 | BLG-OPS-101 | S (~0.5-2 days) | 1.25 | Staging-only evidence (live Render dashboard/usage comparison) |
| EPIC-05 | ST-26 | BLG-OPS-95 | S (~1 day) | 1.00 | |
| EPIC-05 | ST-27 | BLG-OPS-98 | S (~0.5 day per quarter) | 0.50 | `delegated_decision` — policy requires stakeholder agreement |
| **EPIC-05 subtotal** | | | | **5.25d** | Matches `release_plan.md` exactly |

No `[ESTIMATE REQUIRED]` gaps — every item's effort reconciles exactly to `release_plan.md ## Capacity Check`'s per-EPIC subtotals (see column totals above), confirming no drift between the backlog slice's bare labels and the underlying `backlog.md` source items' explicit day ranges.

## Total Effort vs Capacity

| Metric | Value |
|--------|-------|
| Total estimated effort (27 items, all EPICs) | 27.15d |
| Confirmed capacity band | 24-28d |
| Result | **PASS** — within band, near the upper bound (~97-113% of the range). No `warn` outcome (WARN applies only when estimated effort exceeds the band's upper bound). |

No over-allocation requiring Product Owner scope removal. `capacity_warn_acknowledged`: not applicable — capacity check outcome is `pass`, not `warn` (§9 field note).

### Minimum Capacity Buffer Floor Advisory (STEP 1.5)

`scope_effort ÷ confirmed_capacity`: against the lower bound = 27.15 ÷ 24 ≈ **113%**; against the upper bound = 27.15 ÷ 28 ≈ **97%**. The upper-bound ratio exceeds the recommended 95% buffer-floor guideline (advisory only — does not block sealing per §8/STEP 1.5).

**Product Owner acknowledgement (2026-08-21):** Proceed at full ~27.15d scope. This is a direct continuation of the explicit "use full capacity" instruction already recorded in `release_plan.md` (2026-08-21) — the Product Owner widened scope to the top of the band at release planning specifically to draw down 2 further clean, ungated, dependency-free hygiene items (`BLG-OPS-101`, `BLG-BE-54`). No items trimmed at sprint planning.

## Conditional (Deferred)

None. No ST items in the authoritative backlog slice are recorded as `status: deferred_at_planning` with a `gate_condition` in `execution_state.json` — this is a fresh cycle with no prior `execution_state.json`.

## Phasing Recommendation

Not applicable — `release_plan.md ## Capacity Check` contains no `### Phasing Recommendation` subsection this cycle.
