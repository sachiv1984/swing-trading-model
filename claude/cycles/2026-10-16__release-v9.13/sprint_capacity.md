Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-16
Cycle: 2026-10-16__release-v9.13

# Sprint Capacity — 2026-10-16__release-v9.13

## Capacity Inputs

```
Sprint duration:    One sprint covering the full release scope (Product Owner, 2026-10-16). Cadence is ~1-2 calendar days between sprint starts, per workforce_capacity.md's Effective 2026-07-17 baseline.
Available FTE:      1 (solo developer, agent-delegated execution)
Total capacity:     ~24-28 working-day-equivalent units (workforce_capacity.md)
Skill constraints:  The Strategy Rules & System Intent Owner rules on ST-05 (§8 determination), ST-06 (stop floor) and ST-07 (§6.3 alignment), with strategy_rules.md writes authorised under RISK-02 option (a). The API Contracts & Documentation Owner chooses ST-08's behaviour. The AI Compliance & Governance Officer signs off ST-16, ST-17 and ST-18. The Director of Quality reviews ST-27's decision. The Infrastructure & Operations Owner and the FinOps & Resource Architect sign off ST-33. The Infrastructure & Operations Owner and the Data Model & Domain Schema Owner are needed for live-environment Human-Delegation on ST-02 and ST-22 (live constraint/backfill and migration), ST-28 (Telegram receipt), ST-29 (Render dashboard and live run), ST-30/ST-31 (live usage data), ST-32 (full-universe run) and ST-10 (manual check on a deployed environment). No other role is contended.
```

## Item Effort Mapping

An explicit day figure on an item takes precedence over the canonical band-letter midpoint (`workforce_capacity.md` precedence rule, LL-v9.6-P-Closure-01). Range-only items use the range midpoint, and XS items ("<1h", "<0.5d") are taken at the 0.15d XS midpoint. Calibrated figures come from Release Planning's STEP 4 check (`run_manifest.md`). Every figure reconciles to `release_plan.md ## Capacity Check`. There are no `[ESTIMATE REQUIRED]` placeholders.

### EPIC-01 — Exit Flow, Exit Reasons & Red Flag Journal (build-and-ship) (Owner: Head of Engineering; Head of UX & Design; Strategy Rules & System Intent Owner; Data Model & Domain Schema Owner)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-01 | BLG-FE-226 | S (~1-1.5 days) | 1.25 |
| ST-02 | BLG-SPEC-186 | S (~1 day; calibrated to 1.5d — CHECK constraint plus live backfill) | 1.50 |
| ST-03 | BLG-FE-227 | S (~0.5-1 day; addendum's three extra files absorbed, see below) | 0.75 |
| ST-04 | BLG-BE-182 | S (~1-1.5 days) | 1.25 |
| ST-05 | BLG-GOV-391 | S (~0.5-1 day, determination) | 0.75 |
| **EPIC-01 total** | | | **5.50** |

### EPIC-02 — Stop, Sizing & Position Data Correctness (Owner: Backend Engineering Patterns Owner; Strategy Rules & System Intent Owner; Metrics Definitions & Analytics Owner)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-06 | BLG-BE-180 | S (~0.5 day) | 0.50 |
| ST-07 | BLG-BE-161 | XS (<0.5d) | 0.15 |
| ST-08 | BLG-API-07 | S (~0.5 day) | 0.50 |
| ST-09 | BLG-BE-156 | S (~0.5d) | 0.50 |
| ST-10 | BLG-SPEC-188 | S (~0.5 day) | 0.50 |
| ST-11 | BLG-SPEC-180 | XS (<1h) | 0.15 |
| ST-12 | BLG-QA-204 | XS (<1h) | 0.15 |
| ST-13 | BLG-QA-208 | XS (<1h) | 0.15 |
| ST-14 | BLG-QA-210 | XS (<1h) | 0.15 |
| **EPIC-02 total** | | | **2.75** |

### EPIC-03 — AI Output Safety, Debrief & Chat (Owner: AI Compliance & Governance Officer; Backend Engineering Patterns Owner; Frontend Specifications & UX Documentation Owner)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-15 | BLG-AI-17 | XS (<1h plus tests) | 0.15 |
| ST-16 | BLG-AI-18 | S (~0.5d) | 0.50 |
| ST-17 | BLG-AI-16 | S (~0.5d) | 0.50 |
| ST-18 | BLG-AI-15 | S (~0.5d) | 0.50 |
| ST-19 | BLG-AI-14 | XS (<1h plus tests) | 0.15 |
| ST-20 | BLG-FE-211 | XS (<1h plus test) | 0.15 |
| ST-21 | BLG-FE-212 | XS (<1h plus test; addendum scope absorbed, see below) | 0.15 |
| ST-22 | BLG-FE-208 | S (~0.5d; calibrated to 1.0d — live migration) | 1.00 |
| **EPIC-03 total** | | | **3.10** |

### EPIC-04 — API Call Integrity & UI Rendering (Owner: Director of Quality; API Contracts & Documentation Owner; Head of Engineering)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-23 | BLG-QA-228 | S (~1 day) | 1.00 |
| ST-24 | BLG-QA-227 | M (~2-3 days; calibrated to 3.5d — 59 state-changing calls in 22 files) | 3.50 |
| ST-25 | BLG-FE-221 | S (~0.5 day) | 0.50 |
| ST-26 | BLG-FE-209 | S (~0.5-1 day) | 0.75 |
| ST-27 | BLG-QA-211 | S (~0.5d) | 0.50 |
| **EPIC-04 total** | | | **6.25** |

### EPIC-05 — Operations, Cost & Platform (Owner: Infrastructure & Operations Owner; FinOps & Resource Architect; Head of Engineering)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-28 | BLG-OPS-187 | S (~0.5d) | 0.50 |
| ST-29 | BLG-OPS-189 | S (~0.5d; calibrated to 1.0d — Render dashboard hooks, secrets and a live staging run) | 1.00 |
| ST-30 | BLG-OPS-18 | S (~1 day) | 1.00 |
| ST-31 | BLG-OPS-19 | M (~2 days) | 2.00 |
| ST-32 | BLG-OPS-23 | S (~1 day) | 1.00 |
| ST-33 | BLG-OPS-77 | S (~0.5 day) | 0.50 |
| ST-34 | BLG-TECH-23 | M (~2-3 days) | 2.50 |
| **EPIC-05 total** | | | **8.50** |

### EPIC-06 — Governance & Spec Tooling (Owner: Head of Specs Team; PMO Lead; Strategy Rules & System Intent Owner; Data Model & Domain Schema Owner)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-35 | BLG-GOV-390 | XS (<1h, ~0.25d) | 0.25 |
| ST-36 | BLG-GOV-373 | S (~0.5 day) | 0.50 |
| ST-37 | BLG-SPEC-184 | S (~0.5d) | 0.50 |
| ST-38 | BLG-GOV-376 | XS (~0.25 day) | 0.25 |
| ST-39 | BLG-GOV-377 | XS (~0.25 day) | 0.25 |
| ST-40 | BLG-GOV-387 | XS (<1h) | 0.15 |
| **EPIC-06 total** | | | **1.90** |

### Addendum Estimate Checks

The design gate addendum asked Sprint Planning to check two estimates:
- **ST-03:** AC 3 now covers eight files, not five. The three extra files (`ExportModal.js`, `TradeBreakdown.js`, `MonthlyHeatmap.js`) swap a local map for an import. That fits the S range (0.5–1d), so 0.75d holds.
- **ST-21:** the light-theme fix covers the whole debrief section. The gate already fixed the tokens in `trade_history.md` v1.16, and all edits are in one component, so the XS figure holds.

Product Owner accepted both holds on 2026-10-16.

## Total Effort vs Capacity

| EPIC | Stories | Days |
|------|---------|------|
| EPIC-01 | 5 | 5.50 |
| EPIC-02 | 9 | 2.75 |
| EPIC-03 | 8 | 3.10 |
| EPIC-04 | 5 | 6.25 |
| EPIC-05 | 7 | 8.50 |
| EPIC-06 | 6 | 1.90 |
| **Total** | **40** | **28.00** |

28.00d is within the confirmed ~24–28d band and is not over-allocated. Capacity check outcome: `pass`, so no WARN acknowledgement or Phasing Recommendation applies.

## Minimum Capacity Buffer Floor (STEP 1.5)

Ratio: 28.00 / 28.00 = **100%**, above the 95% advisory floor. Product Owner decision: **proceed at ceiling**, 2026-10-16, matching the explicit "use full capacity" release instruction. The LP-14 pessimistic cases are ST-06 (floor vs reject), ST-07 (exception branch), ST-08 (warning field vs 400) and ST-05 (§8 amendment vs withdrawal). Each could add a fraction of a day; see `sprint_planning_notes.md`.

## Conditional (Deferred)

None. All 40 slice items are in sprint scope, and no item is deferred at planning.
