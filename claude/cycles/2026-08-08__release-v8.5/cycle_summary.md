Owner: Head of Specs Team
Class: Operational Record (Class 3)
Status: Filed
Report Date: 2026-08-08
Cycle: 2026-08-08__release-v8.5
Release: v8.5
Design Gate Required: true

# Cycle Summary — Release Planning v8.5

## Outcome

Release Plan **Validated**, `publish_eligible = true`. Scope: 25 stories across 6 grouped EPICs, backlog-driven (no formal roadmap release section — STEP -1.2 Option (b) equivalence from `2026-07-28__scheduled`, same decision relied on by every release since `v8.0`), sized to ~27.15 days midpoint (top of band) against the confirmed ~24-28 day capacity band. Explicit user instruction this session: **"Use fully capacity, focus on user features first."** Capacity sized to the top of the band accordingly; scope led by the full ready `BLG-FE-*`/`BLG-FEAT-*` pool (17 of 25 stories, 73% of effort) since 0 genuinely new user-facing feature-build items exist in the ready backlog pool this cycle — all roadmap-flagship features remain gate-blocked.

## EPICs

| EPIC-ID | Theme | Stories | Owner |
|---------|-------|---------|-------|
| EPIC-01 | Production Correctness Fixes | ST-01, ST-02 | Head of Backend Engineering; Infrastructure & Operations Owner |
| EPIC-02 | Security Hardening | ST-03–ST-05 | Cybersecurity & Trust Lead; Metrics Definitions & Analytics Owner |
| EPIC-03 | Frontend Correctness Fixes | ST-06–ST-08 | Frontend Specifications & UX Documentation Owner |
| EPIC-04 | Design System & Contrast Consistency Audit | ST-09–ST-14 | Frontend Specifications & UX Documentation Owner; Head of UX & Design |
| EPIC-05 | Frontend UX Review & Documentation | ST-15–ST-20 | Head of UX & Design; Frontend Specifications & UX Documentation Owner |
| EPIC-06 | Analytics & Governance Process Fixes | ST-21–ST-25 | Metrics Definitions & Analytics Owner; Head of Specs Team; QA & Testing Owner |

## Gate Outcomes

| Gate | Outcome |
|------|---------|
| STEP -1 Preflight | PASS |
| STEP 1 Readiness | pass |
| STEP 3.5 Local Model Integrity | pass |
| STEP 4.5 Capacity Feasibility | pass (~27.15d / ~24-28d band, top of band) |
| STEP 5.5 Cross-Stage Integrity | pass |
| STEP 5.7 Decision Record Integrity | not_applicable (no escalations raised) |
| Publish Gate | pass — `status = Validated`, `publish_eligible = true` |

## Design Gate

`design_gate_required = true`. `ST-06` (dead `-muted` Tailwind classes, visible text/background rendering) and `ST-08` (P&L exact-zero colour convention reconciliation, visible colour) both carry observable UI acceptance criteria that unconditionally require Playwright coverage or staging sign-off per CLAUDE.md's frontend-visible-change rule. Several other EPIC-04/05 items (`ST-10`, `ST-12`, `ST-13`, `ST-19` if triggered) also carry observable-UI scope. Run `run design-gate --cycle 2026-08-08__release-v8.5` before `plan sprint`.

## Deferred / Excluded This Cycle

- `BLG-FEAT-73`/`BLG-FEAT-74` — remain gate-blocked, formally parked at `v8.3` (STEP 1.4a.1 mandatory sunset trigger). No fresh Perennial-Return Check disposition required (same treatment as `v8.4`).
- `BLG-FEAT-76` — hard-blocked on `BLG-FEAT-73`/`75` shipping first.
- ~119 other gate-blocked backlog items (per `scripts/scan_backlog_gate_conditions.py`) — see `run_manifest.md §STEP 1.3a`.
- ~121 remaining ungated P3 backlog items not selected — capacity reached at ~27.15 days; deliberately weighted toward the highest-priority (P1/P2) and largest ready user-facing/frontend pool this cycle.

## Promoted This Cycle

None — no gate-correction promotions found this session (unlike `v8.4`'s `BLG-FEAT-78` finding).

## Escalations

None raised this cycle.

## Advisory Findings (surfaced, not blocking)

- **No user-facing feature-build item exists this cycle:** unlike `v8.2`–`v8.4` (which each found 1–5 genuine `Product Feature`/`Frontend` build items), this cycle's ready pool contains only `BLG-FEAT-29`/`72` (small analytics/governance-tooling additions, not net-new user capability). Scope instead led with the full ready frontend-correctness/design-consistency/UX-review pool as the closest available honouring of the "focus on user features first" instruction. Accepted by Product Owner delegated authority — see `decisions--2026-08-08__release-v8.5.md`.
- **Self-caught 5th gate-detection scan failure mode:** `BLG-FEAT-73` carries unmet-gate language inside square brackets in its `Provisional-Target` field, which `scan_backlog_gate_conditions.py`'s `EMBEDDED_GATE_SIGNAL_RE` (parenthesis-only pattern) does not catch. Manually confirmed still gate-blocked and excluded on that basis. Follow-up filed: `BLG-GOV-292` (extend the regex to also match bracket-delimited gate language) — see `run_manifest.md §STEP 1.3a`/`§STEP 2`.
- **Skill-Silo rotation maintained:** 2 of 25 stories (8%) are governance-process-shaped (`BLG-GOV-288`/`289`), consistent with `v8.4`'s execution-heavy weighting; no mandatory pull-forward triggered.

## Artefacts Produced

- `claude/cycles/2026-08-08__release-v8.5/run_manifest.md`
- `claude/cycles/2026-08-08__release-v8.5/state.json`
- `claude/cycles/2026-08-08__release-v8.5/release_plan.md`
- `claude/cycles/2026-08-08__release-v8.5/stage4_backlog_slice.md`
- `claude/cycles/2026-08-08__release-v8.5/stage4_issue_manifest.json`
- `claude/cycles/2026-08-08__release-v8.5/backlog_txn.json`
- `claude/cycles/2026-08-08__release-v8.5/roadmap_txn.json`
- `docs/product/scope/scope--2026-08-08__release-v8.5.md`
- `docs/product/decisions/decisions--2026-08-08__release-v8.5.md`
- `claude/cycles/2026-08-08__release-v8.5/cycle_summary.md` (this file)
- `claude/cycles/2026-08-08__release-v8.5/lessons_learnt.md`

## Next Step

`run design-gate --cycle 2026-08-08__release-v8.5`, then `plan sprint --cycle 2026-08-08__release-v8.5`.
