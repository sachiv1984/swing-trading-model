Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-06
Cycle: 2026-10-06__release-v9.10

# Sprint Capacity — 2026-10-06__release-v9.10

## Capacity Inputs

```
Sprint duration:    Single sprint covering the full release scope (cadence ~1-2 calendar days between sprint starts, per workforce_capacity.md's Effective 2026-07-17 baseline)
Available FTE:      1 (solo developer, agent-delegated execution)
Total capacity:     ~24-28 working-day-equivalent units (workforce_capacity.md, reconfirmed unchanged 2026-09-23)
Skill constraints:  Strategy Rules & System Intent Owner is a shared ruling dependency for 6 stories across 3 EPICs (ST-01, ST-05, ST-11, ST-13, ST-14, ST-20). Infrastructure & Operations Owner is needed for live-environment Human-Delegation on ST-01 (production settings read) and ST-18 (stale-staging live fire). No other role is contended.
```

## Item Effort Mapping

An explicit day figure on an item takes precedence over the canonical band-letter midpoint (`workforce_capacity.md` precedence rule, LL-v9.6-P-Closure-01). Range-only items use the midpoint the release plan used, so every figure reconciles to `release_plan.md ## Capacity Check`.

### EPIC-01 — Stop-Parameter Correctness & ATR Integrity (Owner: Head of Engineering; Strategy Rules & System Intent Owner)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-01 | BLG-BE-138 | M (~3-5d; 4.0d midpoint) | 4.00 |
| ST-02 | BLG-BE-139 | M (~2-3d) | 2.50 |
| ST-03 | BLG-SPEC-187 | S (~0.5d) | 0.50 |
| ST-04 | BLG-QA-207 | S (~1d) | 1.00 |
| ST-05 | BLG-BE-137 | S (~0.5d) | 0.50 |
| **EPIC-01 total** | | | **8.50** |

### EPIC-02 — Stop & Exit Transparency (Owner: Frontend Specifications & UX Documentation Owner; Head of UX & Design)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-06 | BLG-FE-193 | M (~4-6d; 5.0d midpoint) | 5.00 |
| ST-07 | BLG-FE-197 | M (~2-3d) | 2.50 |
| ST-08 | BLG-FE-198 | S (~1d) | 1.00 |
| ST-09 | BLG-FE-199 | S (~1-1.5d; 1.25d midpoint) | 1.25 |
| ST-10 | BLG-FE-194 | XS (<1h) | 0.15 |
| **EPIC-02 total** | | | **9.90** |

### EPIC-03 — Lifecycle & Gap-Risk Strategy Boundary (Owner: Strategy Rules & System Intent Owner; Head of Engineering)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-11 | BLG-SPEC-185 | S (~1d) | 1.00 |
| ST-12 | BLG-FE-196 | S (~1-2d; 1.5d midpoint) | 1.50 |
| ST-13 | BLG-GOV-365 | S (~0.5d ruling) | 0.50 |
| ST-14 | BLG-BE-136 | S (~1-2d; 1.5d midpoint) | 1.50 |
| **EPIC-03 total** | | | **4.50** |

### EPIC-04 — AI Governance, Ops & QA Hygiene (Owner: AI Compliance & Governance Officer; Infrastructure & Operations Owner)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-15 | BLG-GOV-140 | S (~0.5d) | 0.50 |
| ST-16 | BLG-GOV-141 | S (~0.5d) | 0.50 |
| ST-17 | BLG-OPS-92 | S (~1d) | 1.00 |
| ST-18 | BLG-OPS-171 | S (~0.5d; calibrated up from XS) | 0.50 |
| ST-19 | BLG-QA-195 | S (~0.5d) | 0.50 |
| ST-20 | BLG-SPEC-171 | S (~0.5d) | 0.50 |
| ST-21 | BLG-GOV-357 | S (~1-2d; 1.5d midpoint) | 1.50 |
| **EPIC-04 total** | | | **5.00** |

There are no `[ESTIMATE REQUIRED]` placeholders. Every item has an effort band and a resolvable day figure.

## Total Effort vs Capacity

**Total estimated effort: 27.90 days.** The confirmed capacity band is ~24-28 working days, and 27.90 / 28.00 = **99.6% of the band's top edge**. Scope is within the band, at its ceiling, which matches the release plan's explicit "use full capacity" instruction (2026-10-06). There is no over-allocation. The `capacity_check` outcome is `pass`, not `warn`, so §8 requires neither a WARN acknowledgement nor a scope trim.

### Minimum Capacity Buffer Floor (Advisory — §1.5)

Scope effort ÷ confirmed capacity = 27.90 / 28.00 = **99.6%**. That exceeds the recommended 95% buffer-floor target by 4.6 points. It is recorded here as the formal "buffer floor exceeded" note required by §1.5. This is separate from the >100% over-allocation WARN, which did not trigger.

**Product Owner acknowledgement (2026-10-06): Proceed at ceiling.** This is consistent with the explicit "use full capacity" instruction recorded at release planning. No scope trim.

## Gate-Conditional Deferred Items

None. No item in the authoritative backlog slice is deferred at planning, and all 21 items are in sprint scope.
