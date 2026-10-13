Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-13
Cycle: 2026-10-12__release-v9.12

# Sprint Capacity — 2026-10-12__release-v9.12

## Capacity Inputs

```
Sprint duration:    One sprint covering the full release scope. The Product Owner declined RISK-08's optional two-sprint split on 2026-10-13. Cadence is ~1-2 calendar days between sprint starts, per workforce_capacity.md's Effective 2026-07-17 baseline.
Available FTE:      1 (solo developer, agent-delegated execution)
Total capacity:     ~24-28 working-day-equivalent units (workforce_capacity.md, reconfirmed under ESC-EXEC-20260921-07)
Skill constraints:  The Strategy Rules & System Intent Owner rules on ST-10 (§7.3 manual stop) and records ST-14's §13 addendum (ST-25 too, only if option (b) is taken). The AI Compliance & Governance Officer signs off ST-04's failure action. The Director of HR authorises ST-21's charter change. The Cybersecurity & Trust Lead with the Product Owner decides ST-27. The Data Model & Domain Schema Owner signs off ST-38. The Head of Specs Team with the Product Owner rules on ST-43. The Infrastructure & Operations Owner and the Data Model & Domain Schema Owner are needed for live-environment Human-Delegation on ST-01 and ST-26 (live migrations), ST-28 (staging check), ST-29 (Render dashboard), ST-30 (staging divergence with a Telegram receipt), ST-34 (production pg_indexes read) and ST-38 (live sample). No other role is contended.
```

## Item Effort Mapping

An explicit day figure on an item takes precedence over the canonical band-letter midpoint (`workforce_capacity.md` precedence rule, LL-v9.6-P-Closure-01). Range-only items use the range midpoint, and XS items ("<1h", "<0.5d") are taken at the 0.15d XS midpoint. Every figure reconciles to `release_plan.md ## Capacity Check`. There are no `[ESTIMATE REQUIRED]` placeholders.

### EPIC-01 — AI Feature Correctness & Cost Visibility (Owner: Backend Engineering Patterns Owner; AI Compliance & Governance Officer; Infrastructure & Operations Owner)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-01 | BLG-BE-162 | S (~0.5d; calibrated to 1.0d — live migration plus staging verification) | 1.00 |
| ST-02 | BLG-AI-11 | S (~0.5d) | 0.50 |
| ST-03 | BLG-AI-12 | XS (<1h plus tests) | 0.15 |
| ST-04 | BLG-AI-10 | S (~0.5d) | 0.50 |
| ST-05 | BLG-AI-13 | XS (<1h plus tests) | 0.15 |
| ST-06 | BLG-OPS-183 | S (~0.5 day) | 0.50 |
| **EPIC-01 total** | | | **2.80** |

### EPIC-02 — Stop, Sizing & Position Correctness (build-and-ship) (Owner: Head of Engineering; Strategy Rules & System Intent Owner; Backend Engineering Patterns Owner)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-07 | BLG-BE-157 | S (~0.5d) | 0.50 |
| ST-08 | BLG-BE-158 | XS (<1h plus tests) | 0.15 |
| ST-09 | BLG-QA-205 | S (~0.5d) | 0.50 |
| ST-10 | BLG-BE-159 | S (~0.5-1d) | 0.75 |
| ST-11 | BLG-BE-160 | XS (<0.5d) | 0.15 |
| ST-12 | BLG-BE-145 | S (~0.5 day) | 0.50 |
| ST-13 | BLG-BE-149 | S (~0.5 day) | 0.50 |
| ST-14 | BLG-BE-148 | S (~1 day) | 1.00 |
| ST-15 | BLG-FE-202 | S (~1 day) | 1.00 |
| ST-16 | BLG-BE-144 | S (~0.5 day) | 0.50 |
| **EPIC-02 total** | | | **5.55** |

### EPIC-03 — Trade Entry, Settings & Accessibility (build-and-ship) (Owner: Head of UX & Design; Frontend Specifications & UX Documentation Owner; Head of Engineering)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-17 | BLG-BE-146 | S (~1 day) | 1.00 |
| ST-18 | BLG-FE-203 | S (~0.5 day) | 0.50 |
| ST-19 | BLG-QA-206 | M (~1d) | 1.00 |
| ST-20 | BLG-FE-201 | XS (<0.5 day) | 0.15 |
| ST-21 | BLG-GOV-369 | S (~1-1.5 days) | 1.25 |
| ST-22 | BLG-FE-207 | S (~0.5 day) | 0.50 |
| ST-23 | BLG-FE-200 | M (~2-3 days) | 2.50 |
| ST-24 | BLG-FE-210 | XS (<1h plus test updates) | 0.15 |
| **EPIC-03 total** | | | **7.05** |

### EPIC-04 — Security, Operations & Platform (Owner: Infrastructure & Operations Owner; Cybersecurity & Trust Lead; FinOps & Resource Architect)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-25 | BLG-OPS-184 | S (~0.5d) | 0.50 |
| ST-26 | BLG-SEC-41 | S (~1 day; calibrated to 1.5d — new table, live migration) | 1.50 |
| ST-27 | BLG-SEC-42 | S (~0.5 day) | 0.50 |
| ST-28 | BLG-TECH-22 | S (~0.5-1 day) | 0.75 |
| ST-29 | BLG-OPS-181 | XS (<1h) | 0.15 |
| ST-30 | BLG-OPS-182 | XS (<1h; calibrated to 0.5d — deliberate staging divergence and restore) | 0.50 |
| ST-31 | BLG-OPS-185 | XS (<1h) | 0.15 |
| ST-32 | BLG-GOV-371 | S (~1 day) | 1.00 |
| **EPIC-04 total** | | | **5.05** |

### EPIC-05 — Spec & Data Model Hygiene (Owner: Data Model & Domain Schema Owner; API Contracts & Documentation Owner; Head of Specs Team)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-33 | BLG-SPEC-176 | XS (<1h) | 0.15 |
| ST-34 | BLG-SPEC-178 | S (~1d) | 1.00 |
| ST-35 | BLG-SPEC-179 | XS (<0.5 day) | 0.15 |
| ST-36 | BLG-SPEC-181 | XS (<1h) | 0.15 |
| ST-37 | BLG-SPEC-182 | XS (<1h) | 0.15 |
| ST-38 | BLG-SPEC-183 | S (~0.5d; includes a read-only live sample check) | 0.50 |
| **EPIC-05 total** | | | **2.10** |

### EPIC-06 — Governance Tooling & Test Integrity (Owner: Head of Specs Team; PMO Lead; QA & Testing Owner; Director of Quality)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-39 | BLG-GOV-385 | S (~0.5d) | 0.50 |
| ST-40 | BLG-GOV-386 | S (~0.5–1d) | 0.75 |
| ST-41 | BLG-GOV-363 | S (~0.5d) | 0.50 |
| ST-42 | BLG-GOV-367 | S (~0.5d) | 0.50 |
| ST-43 | BLG-GOV-364 | S (~0.5d) | 0.50 |
| ST-44 | BLG-GOV-372 | S (~0.5 day) | 0.50 |
| ST-45 | BLG-QA-212 | S (~0.5 day) | 0.50 |
| ST-46 | BLG-QA-209 | M (~1d; 11 test files reference `sys.modules["utils…"]`, grep-confirmed 2026-10-12) | 1.00 |
| ST-47 | BLG-QA-213 | S (~0.5d) | 0.50 |
| ST-48 | BLG-QA-202 | XS (<1h) | 0.15 |
| **EPIC-06 total** | | | **5.40** |

## Total Effort vs Capacity

| EPIC | Stories | Days |
|------|---------|------|
| EPIC-01 | 6 | 2.80 |
| EPIC-02 | 10 | 5.55 |
| EPIC-03 | 8 | 7.05 |
| EPIC-04 | 8 | 5.05 |
| EPIC-05 | 6 | 2.10 |
| EPIC-06 | 10 | 5.40 |
| **Total** | **48** | **27.95** |

27.95d is within the confirmed ~24–28d band and is not over-allocated. Capacity check outcome: `pass`, so no WARN acknowledgement or Phasing Recommendation applies.

## Minimum Capacity Buffer Floor (STEP 1.5)

Ratio: 27.95 / 28.00 = **99.8%**, above the 95% advisory floor. Product Owner decision: **proceed at ceiling**, 2026-10-13, matching the explicit "use full capacity" release instruction. The LP-14 pessimistic cases are ST-10 Branch A, ST-27 with a narrower key, and ST-38 with a code fix. Each could add a fraction of a day; see `sprint_planning_notes.md`.

## Conditional (Deferred)

None. All 48 slice items are in sprint scope, and no item is deferred at planning.
