Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v9.10
Cycle: 2026-10-06__release-v9.10
Last Updated: 2026-10-07

Superseded by: v9.10 ship — 2026-10-07
Changelog: docs/product/changelog.md#v9.10
Verification report: claude/cycles/2026-10-06__release-v9.10/verification_report.md
Cycle: 2026-10-06__release-v9.10

## Release Scope — v9.10

21 items across 4 EPICs, 27.90 estimated days (top of the ~24–28 day band, "use full capacity"). Acceptance criteria: `claude/cycles/2026-10-06__release-v9.10/stage4_backlog_slice.md`.

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | `BLG-BE-138` — One source for §11 stop parameters across the on-load and nightly stop paths |
| S2-02 | EPIC-01 | `BLG-BE-139` — Remove silent ATR fallbacks and record ATR provenance |
| S2-03 | EPIC-01 | `BLG-SPEC-187` — Contract corrections: losing-stop formula, analyze side effects, settings-change effect |
| S2-04 | EPIC-01 | `BLG-QA-207` — Unit-test the live exit decision and grace-period behaviour |
| S2-05 | EPIC-01 | `BLG-BE-137` — Rule on strategy-version registry coverage and enforce it with a test |
| S2-06 | EPIC-02 | `BLG-FE-193` — Show ATR, active multiplier and recalculation source in the stop-loss cell |
| S2-07 | EPIC-02 | `BLG-FE-197` — Trade Entry shows the stop and risk the system will actually store |
| S2-08 | EPIC-02 | `BLG-FE-198` — Exit dialog pre-selects the exit reason the system already knows |
| S2-09 | EPIC-02 | `BLG-FE-199` — Morning briefing card for §8 exit recommendations |
| S2-10 | EPIC-02 | `BLG-FE-194` — Recent Trades badge shows a neutral glyph for a break-even trade |
| S2-11 | EPIC-03 | `BLG-SPEC-185` — Reconcile the lifecycle-state registry with strategy_rules.md §9 |
| S2-12 | EPIC-03 | `BLG-FE-196` — Positions lifecycle badge agrees with the §6 grace window, in calendar days |
| S2-13 | EPIC-03 | `BLG-GOV-365` — Gap Risk Flag §13.3 ruling on UK-ticker earnings flags and day-0 timing |
| S2-14 | EPIC-03 | `BLG-BE-136` — Gap risk flag: disposition the standalone weekend-hold trigger and align trigger-timing label/spec with code |
| S2-15 | EPIC-04 | `BLG-GOV-140` — AI chat advisory §13 quarterly self-audit checklist |
| S2-16 | EPIC-04 | `BLG-GOV-141` — AI model output logging completeness audit |
| S2-17 | EPIC-04 | `BLG-OPS-92` — Quarterly dependency update review |
| S2-18 | EPIC-04 | `BLG-OPS-171` — Confirm the stale-staging-deploy alert fires on a real stale-staging condition |
| S2-19 | EPIC-04 | `BLG-QA-195` — Add the Reports and Notifications pages to the axe accessibility scan |
| S2-20 | EPIC-04 | `BLG-SPEC-171` — Correct the PO-05 pre-assessment and replay page spec wording |
| S2-21 | EPIC-04 | `BLG-GOV-357` — Sign-off single-point-of-failure matrix |

### Items explicitly deferred

| Item | Reason |
|------|--------|
| `BLG-TECH-21` (P2) — CRA → Vite migration | Ready, but its own scope requires a dedicated single-EPIC release, not a mixed-scope sprint (`Provisional-Target: v10.0`). Accept-risk review-by date 2027-02-16. |
| `BLG-GOV-368` (P2) | Prompt half already applied (`execution_prompt.md` v3.82). Narrow or close at the next `groom backlog`. |
| `BLG-GOV-142`, `BLG-GOV-360` (P2) | Already resolved in v9.9 (ST-19, ST-20). Archive at the next `groom backlog`. |
| `BLG-FEAT-73`, `BLG-FEAT-76` | Substantively gate-blocked (no formal Gate field; own text blocks sprint entry). |
| `BLG-FE-195`, `BLG-OPS-179` | Gated on `BLG-BE-138` (ST-01) ruling / ship. Seatable at v9.11. |
| `BLG-FEAT-55`, `BLG-SPEC-65`, `BLG-GOV-121`, `BLG-FEAT-62`, `BLG-OPS-53`, `BLG-FEAT-92` | Date-lapsed gates read individually. Underlying conditions still unmet (see `run_manifest.md`). |
| 61 further ready items (~34.25 days) | Capacity. Includes `BLG-SPEC-170` (⚠ aged 2+ cycles), `BLG-FEAT-59`, `BLG-FEAT-60`, `BLG-FE-84`, `BLG-BE-140`. |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: v9.10 ship — 2026-10-07
Changelog: docs/product/changelog.md#v9.10
Cycle: 2026-10-06__release-v9.10
