Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v6.8
Cycle: 2026-07-08__release-v6.8
Last Updated: 2026-07-08

## Release Scope — v6.8 Correctness, Value Pull-Forward & Debt Clearance

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | `BLG-BE-46` — Investigate/fix `trade_plans.position_id` never populated in production |
| S2-02 | EPIC-01 | `BLG-SEC-08` — Unvalidated dict keys used as SQL column names in `database.update_signal()` |
| S2-03 | EPIC-01 | `BLG-SEC-07` — Manual review of existing signals for anomalous ticker/market values |
| S2-04 | EPIC-01 | `BLG-OPS-99` — Provision application `X-API-Key` for governed routines (resolves LP-08) |
| S2-05 | EPIC-02 | `BLG-FEAT-52` — Trade tagging and tag-based performance filtering (descoped, ungated) |
| S2-06 | EPIC-02 | `BLG-FEAT-71` — SI-02 gate visibility indicator (Reports page) |
| S2-07 | EPIC-03 | `BLG-SPEC-58` — Dashboard homepage visual hierarchy review post-v6.2 |
| S2-08 | EPIC-03 | `BLG-SPEC-59` — R-multiple cross-currency normalization specification |
| S2-09 | EPIC-03 | `BLG-SPEC-60` — Trailing stop visual indicator frontend specification |
| S2-10 | EPIC-03 | `BLG-SPEC-61` — Trailing stop effectiveness metric definition |
| S2-11 | EPIC-03 | `BLG-QA-64` — Fix 12 dark spec files surfaced by Playwright glob discovery |
| S2-12 | EPIC-03 | `BLG-GOV-134` — CI inline OpenAPI drift detection for `api_performance_baseline.md` |
| S2-13 | EPIC-03 | `BLG-OPS-74` — Log Anthropic API token usage and cost per morning briefing call |
| S2-14 | EPIC-03 | `BLG-FE-77` — Refactor `Watchlist.js` to ESLint compliance |
| S2-15 | EPIC-03 | `BLG-OPS-61` — `BLG-OPS-13` v5.1–v5.4 endpoint baseline extension |
| S2-16 | EPIC-03 | `BLG-GOV-123` — Extract Playwright test standard from `execution_prompt.md` to `shared_standards.md` |
| S2-17 | EPIC-03 | `BLG-OPS-71` — System threat model document |

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| SI-02 (Behavioural Drift Detection) | Gate NOT MET — 20 closed trades confirmed but 0 linked trade-plans (`position_id` linkage bug, `BLG-BE-46`); not resolvable by trade accumulation alone | Re-check once `BLG-BE-46` (S2-01, this release) resolves and either backfill or new linked closes accrue |
| PO-02 / PO-04 (Arc 4 remainder) | Data-density gates not met (6+ months AI journals / 50+ trades with plans) | Re-check at next release planning readiness scan |
| `BLG-SPEC-35` (PO-02 §13 boundary review) | Gate: PO-02 sprint planning imminent — not met | Re-review when PO-02 sprint planning becomes imminent |
| `BLG-GOV-74` | Genuine calendar gate — first quarterly AI-usage review due 2026-08-29, not yet due. Stale `Provisional-Target: v4.10` label corrected to reflect the true controlling gate date; this is a label correction, not a new deferral | First cycle after 2026-08-29 |
| `BLG-GOV-140` | Genuine calendar gate — first quarterly §13 self-audit due 2026-09-24, not yet due | First cycle after 2026-09-24 |
| `BLG-GOV-141` | Genuine calendar gate — first quarterly AI output logging audit due 2026-09-24, not yet due | First cycle after 2026-09-24 |
| All other backlog items | Not selected this release — either genuinely gated (data-density/§13/design-phase), or ungated but lower priority than the 17 items selected; capacity already at ≈13.9 of a 12–14 day baseline | Re-evaluate at next release planning |

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-07-08__release-v6.8
