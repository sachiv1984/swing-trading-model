Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-01
Cycle: 2026-09-30__release-v9.9

# Sprint Capacity — 2026-09-30__release-v9.9

## Capacity Inputs

```
Sprint duration:    Single sprint covering full release scope (cadence ~1-2 calendar days between sprint starts, per workforce_capacity.md Effective 2026-07-17 baseline)
Available FTE:      1 (solo developer, agent-delegated execution)
Total capacity:     ~24-28 working-day-equivalent units (workforce_capacity.md, reconfirmed unchanged 2026-09-23, ESC-EXEC-20260921-07)
Skill constraints:  None flagged — all 6 EPICs map to distinct, non-contended owner roles (Head of Engineering/Backend Engineering Patterns Owner; Infrastructure & Operations Owner/Cybersecurity & Trust Lead; Director of Quality/QA & Testing Owner; Head of Specs Team/PMO Lead; Data Model & Domain Schema Owner/Head of Specs Team; Head of UX & Design/Frontend Specifications & UX Documentation Owner)
```

## Item Effort Mapping

Per-item explicit day figure takes precedence over the canonical band-letter midpoint (`workforce_capacity.md` precedence rule, LL-v9.6-P-Closure-01). All 35 items carry either an explicit day figure/range or a bare band letter resolved via the canonical midpoint table.

### EPIC-01 — Backend Reliability & Data Integrity (Owner: Head of Engineering; Backend Engineering Patterns Owner)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-01 | BLG-BE-135 | L (~6-10d) | 8.00 |
| ST-02 | BLG-BE-131 | XS (<1h) | 0.15 |
| ST-03 | BLG-BE-132 | XS (<1h) | 0.15 |
| ST-04 | BLG-BE-133 | XS (<1h) | 0.15 |
| ST-05 | BLG-BE-134 | XS (<1h) | 0.15 |
| **EPIC-01 total** | | | **8.60** |

### EPIC-02 — Operational Reliability & Security Hardening (Owner: Infrastructure & Operations Owner; Cybersecurity & Trust Lead)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-06 | BLG-SEC-40 | XS (<1h) | 0.15 |
| ST-07 | BLG-OPS-172 | XS (<1h) | 0.15 |
| ST-08 | BLG-OPS-173 | XS (<1h) | 0.15 |
| ST-09 | BLG-OPS-174 | XS (<1h) | 0.15 |
| **EPIC-02 total** | | | **0.60** |

### EPIC-03 — QA & Test Coverage (Owner: Director of Quality; QA & Testing Owner)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-10 | BLG-QA-203 | S (~0.5d) | 0.50 |
| ST-11 | BLG-QA-185 | M (~2d) | 2.00 |
| ST-12 | BLG-QA-186 | S (~1d) | 1.00 |
| ST-13 | BLG-QA-189 | S (~0.5-1d) | 0.75 |
| ST-14 | BLG-QA-190 | M (~1-2d) | 1.50 |
| ST-15 | BLG-QA-191 | S (~0.5d) | 0.50 |
| ST-16 | BLG-QA-192 | XS (<1h) | 0.15 |
| ST-17 | BLG-QA-193 | XS (<1h) | 0.15 |
| ST-18 | BLG-QA-194 | S (~0.5d) | 0.50 |
| **EPIC-03 total** | | | **7.05** |

### EPIC-04 — Governance Process & Strategy Boundary (Owner: Head of Specs Team; PMO Lead)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-19 | BLG-GOV-356 | M (~1-2d) | 1.50 |
| ST-20 | BLG-GOV-358 | S (~1-2d) | 1.50 |
| ST-21 | BLG-GOV-343 | M (~1.5-2d) | 1.75 |
| ST-22 | BLG-GOV-344 | S (~0.5d) | 0.50 |
| ST-23 | BLG-GOV-347 | S (~0.5d) | 0.50 |
| ST-24 | BLG-GOV-350 | S (~0.5d) | 0.50 |
| ST-25 | BLG-GOV-352 | M (~2d) | 2.00 |
| ST-26 | BLG-GOV-353 | XS (<1h) | 0.15 |
| ST-27 | BLG-GOV-354 | XS (<1h) | 0.15 |
| **EPIC-04 total** | | | **8.55** |

### EPIC-05 — Spec & Data-Model Debt Clearance (Owner: Data Model & Domain Schema Owner; Head of Specs Team)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-28 | BLG-SPEC-157 | M (~2d) | 2.00 |
| ST-29 | BLG-SPEC-164 | XS (<1h) | 0.15 |
| ST-30 | BLG-SPEC-165 | XS (<1h) | 0.15 |
| ST-31 | BLG-SPEC-166 | XS (<1h) | 0.15 |
| ST-32 | BLG-SPEC-167 | XS (<1h) | 0.15 |
| ST-33 | BLG-SPEC-168 | XS (<1h) | 0.15 |
| ST-34 | BLG-SPEC-169 | XS (<1h) | 0.15 |
| **EPIC-05 total** | | | **2.90** |

### EPIC-06 — Frontend & UX Debt (Owner: Head of UX & Design; Frontend Specifications & UX Documentation Owner)

| Story | Source | Effort band | Days |
|-------|--------|-------------|------|
| ST-35 | BLG-FE-192 | XS (<1h) | 0.15 |
| **EPIC-06 total** | | | **0.15** |

No `[ESTIMATE REQUIRED]` placeholders — every item carries an effort band with either an explicit day figure/range or a resolvable canonical-midpoint figure.

## Total Effort vs Capacity

**Total estimated effort: 27.85 days.** Confirmed capacity band: ~24-28 working days. 27.85 / 28.00 = **99.5% of the band's top edge** — within band, at its ceiling, matching the release plan's explicit "full capacity" instruction (2026-09-30). No over-allocation — `capacity_check` outcome is `pass`, not `warn`; no Product Owner acknowledgement or scope trim required under §8.

### Minimum Capacity Buffer Floor (Advisory — §1.5)

Scope effort ÷ confirmed capacity = 27.85 / 28.00 = **99.5%**, exceeding the recommended 95% buffer-floor target by 4.5 points. This is the same ceiling-level reading `release_plan.md`'s Capacity Check section already flagged as intentional ("at its ceiling, per explicit 'full capacity' instruction"). Surfaced here per §1.5 as the formal "buffer floor exceeded" note, distinct from the (not-triggered) >100% over-allocation WARN.

**Product Owner acknowledgement (2026-10-01): Proceed at ceiling.** Consistent with the explicit "full capacity" instruction already recorded at release planning (not a default or an oversight) — no scope trim. No further action required; recorded alongside the sprint goal sign-off (STEP 2).

## Gate-Conditional Deferred Items

None. No `execution_state.json` exists yet for this cycle (sprint planning is the first engine to initialise it — see §5.2 of `sprint_planning_prompt.md`); no items in the authoritative backlog slice carry a `status: deferred_at_planning` disposition. All 35 items are included in sprint scope (see STEP 3).
