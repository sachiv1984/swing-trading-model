Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-08
Cycle: 2026-10-08__release-v9.11

# Sprint Capacity — 2026-10-08__release-v9.11

## Capacity Inputs

```
Sprint duration:    Single sprint covering the full release scope (Product Owner declined RISK-09's optional two-sprint split, 2026-10-08; cadence ~1-2 calendar days between sprint starts, per workforce_capacity.md's Effective 2026-07-17 baseline)
Available FTE:      1 (solo developer, agent-delegated execution)
Total capacity:     ~24-28 working-day-equivalent units (workforce_capacity.md, held unchanged at rebalance 2026-10-08__scheduled)
Skill constraints:  Strategy Rules & System Intent Owner is a ruling dependency for ST-16 (in-grace recalculation) and ST-25 (§13 determination). Infrastructure & Operations Owner and Data Model & Domain Schema Owner are needed for live-environment Human-Delegation on ST-02 (staging AI run), ST-06, ST-17 and ST-20 (live migrations) and ST-42 (branch protection). AI Compliance & Governance Officer signs off ST-01's Condition 2 interpretation. Head of Specs Team + Product Owner sign off BLG-GOV-339 for ST-34's prompt change. No other role is contended.
```

## Item Effort Mapping

An explicit day figure on an item takes precedence over the canonical band-letter midpoint (`workforce_capacity.md` precedence rule, LL-v9.6-P-Closure-01). Range-only items use the range midpoint, and "XS (<0.5d)" items are taken at 0.5d, so every figure reconciles to `release_plan.md ## Capacity Check`.

### EPIC-01 — Post-Trade Debrief & AI Reliability (Owner: Backend Engineering Patterns Owner; AI Compliance & Governance Officer)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-01 | BLG-BE-152 | M (~1-2d; 1.5d midpoint) | 1.50 |
| ST-02 | BLG-BE-150 | S (~0.5d) | 0.50 |
| ST-03 | BLG-BE-151 | S (~0.5d) | 0.50 |
| ST-04 | BLG-QA-217 | S (~0.5d) | 0.50 |
| ST-05 | BLG-FE-205 | S (~0.5d) | 0.50 |
| ST-06 | BLG-AI-08 | S (calibrated to 1.5d for the live migration) | 1.50 |
| ST-07 | BLG-AI-09 | XS (<0.5d plus golden fixture) | 0.50 |
| ST-08 | BLG-BE-141 | S (~0.5-1d; 0.75d midpoint) | 0.75 |
| ST-09 | BLG-BE-142 | S (~0.5d) | 0.50 |
| **EPIC-01 total** | | | **6.75** |

### EPIC-02 — Risk & Position Display Correctness (Owner: Head of Engineering; Head of UX & Design)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-10 | BLG-BE-154 | M (~1-1.5d; 1.25d midpoint) | 1.25 |
| ST-11 | BLG-FE-206 | S (~0.75-1d; 0.875d midpoint) | 0.875 |
| ST-12 | BLG-BE-153 | S (~1d) | 1.00 |
| ST-13 | BLG-BE-155 | S (~1d) | 1.00 |
| ST-14 | BLG-BE-147 | S (~0.5d) | 0.50 |
| ST-15 | BLG-FE-204 | XS (<1h) | 0.15 |
| **EPIC-02 total** | | | **4.775** |

### EPIC-03 — Strategy, Records & Alert Integrity (Owner: Head of Engineering; Strategy Rules & System Intent Owner)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-16 | BLG-BE-143 | S (~0.5-1d; 0.75d midpoint) | 0.75 |
| ST-17 | BLG-FR-06 | S (~1d) | 1.00 |
| ST-18 | BLG-OPS-179 | S (~0.5-1d; 0.75d midpoint) | 0.75 |
| ST-19 | BLG-BE-140 | S (~1-1.5d; 1.25d midpoint) | 1.25 |
| ST-20 | BLG-OPS-175 | XS (calibrated to S 0.5d for the live migration) | 0.50 |
| ST-21 | BLG-OPS-176 | XS (<1h) | 0.15 |
| ST-22 | BLG-API-06 | XS (<1h) | 0.15 |
| **EPIC-03 total** | | | **4.55** |

### EPIC-04 — AI Narrative & Engagement Measurement (Owner: Financial Reporting & Records Owner; Metrics Definitions & Analytics Owner)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-23 | BLG-FEAT-63 | S (~0.5d) | 0.50 |
| ST-24 | BLG-FEAT-60 | S (~0.5-1d; 0.75d midpoint) | 0.75 |
| ST-25 | BLG-FEAT-59 | M (~1-2d; 1.5d midpoint) | 1.50 |
| ST-26 | BLG-SPEC-174 | S (~1d) | 1.00 |
| ST-27 | BLG-FE-84 | S (~1d) | 1.00 |
| ST-28 | BLG-GOV-366 | XS (<1h) | 0.15 |
| **EPIC-04 total** | | | **4.90** |

### EPIC-05 — Spec & Contract Hygiene (Owner: API Contracts & Documentation Owner; Data Model & Domain Schema Owner)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-29 | BLG-SPEC-170 | S (~0.5d) | 0.50 |
| ST-30 | BLG-SPEC-173 | S (~1d) | 1.00 |
| ST-31 | BLG-SPEC-177 | XS (<1h) | 0.15 |
| ST-32 | BLG-SPEC-175 | XS (<1h) | 0.15 |
| **EPIC-05 total** | | | **1.80** |

### EPIC-06 — Governance, QA & Ops Hygiene (Owner: Head of Specs Team; QA & Testing Owner; Infrastructure & Operations Owner)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-33 | BLG-GOV-375 | S (~0.5-1d; 0.75d midpoint) | 0.75 |
| ST-34 | BLG-GOV-355 | S (~0.5-1d; 0.75d midpoint) | 0.75 |
| ST-35 | BLG-GOV-359 | S (~0.5-1d; 0.75d midpoint) | 0.75 |
| ST-36 | BLG-GOV-370 | XS (~0.25d) | 0.25 |
| ST-37 | BLG-QA-196 | XS (<0.5d) | 0.50 |
| ST-38 | BLG-QA-197 | XS (<1h) | 0.15 |
| ST-39 | BLG-QA-199 | S (~0.5-1d; 0.75d midpoint) | 0.75 |
| ST-40 | BLG-QA-200 | S (~0.5d) | 0.50 |
| ST-41 | BLG-QA-201 | XS (<1h) | 0.15 |
| ST-42 | BLG-OPS-177 | XS (<1h) | 0.15 |
| ST-43 | BLG-OPS-178 | S (~0.5d) | 0.50 |
| **EPIC-06 total** | | | **5.20** |

## Total Effort vs Capacity

| Metric | Value |
|--------|-------|
| Total estimated effort | 27.975 days (43 stories) |
| Confirmed capacity | ~24-28 days (top edge 28.00) |
| Utilisation | 27.975 / 28.00 = **99.9%** |
| Over-allocation | No (within band) |
| Capacity check outcome (`release_plan.md`) | `pass` (no WARN, no Phasing Recommendation) |

**§1.5 buffer floor:** 99.9% exceeds the 95% advisory floor. Surfaced to the Product Owner at STEP 3.2. **Product Owner: proceed at ceiling, 2026-10-08**, consistent with the "use full capacity" instruction given at release planning. RISK-09 (43 stories, per-story overhead) is noted: 20 stories are XS or ≤0.5d and grouped by file.

No `[ESTIMATE REQUIRED]` placeholders. No gate-conditional deferred items (§1.4 does not apply).
