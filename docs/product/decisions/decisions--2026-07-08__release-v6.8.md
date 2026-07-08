Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v6.8
Cycle: 2026-07-08__release-v6.8
Last Updated: 2026-07-08

## Planning Decisions — v6.8 Correctness, Value Pull-Forward & Debt Clearance

### Scope decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| Include `BLG-BE-46` as top scope priority (S2-01) | P1 production data-integrity bug blocking SI-02 gate resolution indefinitely; already targeted `v6.8` from the prior cycle's finding | Product Owner | 2026-07-08 |
| Include both mandatory pull-forwards `BLG-FEAT-52`/`BLG-FEAT-71` as firm scope | Binding STEP 2.4 Product Value Alert response from the 2026-07-08 rebalance (ratio 0.26, below the 0.30 floor) | Product Owner (delegated from rebalance decision) | 2026-07-08 |
| Include `BLG-OPS-99` (application API key provisioning) | Resolves a 2-cycle-recurring credential gap (LP-08) that has independently blocked SI-02 verification in both the v6.7 rebalance and v6.7 release-planning sessions; S effort, no gate | Product Owner | 2026-07-08 |
| Promote 4 aged spec-debt items (`BLG-SPEC-58/59/60/61`) to firm scope | 4+ release cycles (v6.4–v6.7) without a story assignment, flagged by this engine's own STEP 1.1 Backlog Age Advisory and independently confirmed by a `groom backlog --dry-run` run immediately prior to this cycle | Product Owner | 2026-07-08 |
| Resolve 3 stale-deferral items directly this cycle (`BLG-OPS-61`, `BLG-GOV-123`, `BLG-OPS-71`) rather than re-park | All 3 are low-effort (XS–S), ungated, and had accumulated 6–12 missed release targets with zero PO re-deferral note on record anywhere in `backlog.md` — resolving now under the Perennial-Return Check's Option (c) rather than letting the pattern continue indefinitely | Product Owner | 2026-07-08 |
| Exclude `BLG-GOV-74`/`BLG-GOV-140`/`BLG-GOV-141` from scope despite their stale version labels | Each carries a genuine, still-future calendar gate date (2026-08-29 / 2026-09-24 / 2026-09-24) — the stale `Provisional-Target` version label was cosmetic, not a sign of neglect; correcting the label is not the same as clearing the gate | Product Owner | 2026-07-08 |
| Accept capacity outcome at ≈13.9 of the 12–14 day baseline (PASS, no phasing recommendation required) | User instruction was to maximise legitimate scope pull-through; 17 items fit within the existing capacity baseline without requiring a WARN/phasing split | Product Owner | 2026-07-08 |

### Sequencing decisions

| Decision | Rationale | Made by | Date |
|----------|-----------|---------|------|
| EPIC-01 (correctness/security/infra) sequenced first within the sprint | `BLG-BE-46`'s root-cause finding may affect how `BLG-FEAT-71`'s gate-visibility indicator should display corrected data; `BLG-OPS-99` (API key) is a pure enabler with no dependents but is cheap to clear early | Product Owner | 2026-07-08 |
| `BLG-FEAT-52`'s new endpoints registered same-commit in `openapi.yaml` + `docs/specs/api_contracts/` + `backend/routers/test.py` | CLAUDE.md hard rule — non-negotiable, called out explicitly so it is not missed at execution | Product Owner | 2026-07-08 |
| `BLG-GOV-123` treated as a governance-file edit subject to CLAUDE.md §6 checklist | It modifies `execution_prompt.md`, a governed prompt — version bump, OPERATIONAL_GUIDE §14 sync, and `prompt_change_log.md` entry are mandatory in the same commit | Product Owner | 2026-07-08 |

### Accepted risks

| ESC ID | Risk domain | Rationale | Accepted by | AR record |
|--------|-------------|-----------|-------------|-----------|
| None | — | No escalations raised this cycle — no blockers encountered during readiness/scope/capacity checks | — | — |

### Supersession note

*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Cycle: 2026-07-08__release-v6.8
