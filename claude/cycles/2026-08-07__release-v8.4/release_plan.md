Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v8.4
Cycle: 2026-08-07__release-v8.4
Last Updated: 2026-08-07

# Release Plan — v8.4

## Readiness

Preflight passed (see `run_manifest.md §STEP -1`). Post-ship precondition for the prior cycle (`2026-08-05__release-v8.3`) confirmed: `post_ship_complete = true`, `next_cycle_unblocked = true`. No formal `## v8.4` roadmap section exists — cleared via the `2026-07-28__scheduled` rebalance's STEP 8.1 Option (b) decision (same equivalence relied on by every release since `v8.0`). This release is backlog-driven, scoped directly from `claude/backlog/backlog.md`'s ungated/ready pool under Product Owner delegated authority, per explicit user instruction: **"Use full capacity and prioritise user features."**

**Capacity instruction:** Scope sized to ~28 days — the top of the confirmed ~24-28 working-day-equivalent capacity band (Effective 2026-07-17, unchanged since).

**User-feature-priority instruction:** See `run_manifest.md §STEP 2` for the full finding. Summary: the ungated, ready backlog pool contains 2 genuinely user-facing feature-build items this cycle — `BLG-FE-141` (found directly) and `BLG-FEAT-78` (found via a self-caught stale-gate-field correction; its gate condition, `BLG-FE-116` shipping, was met back at v7.5 but never annotated). All larger roadmap-flagship features (`BLG-FEAT-73`/`74`/`76` etc.) remain gate-blocked on data-density or §13-clearance conditions. `BLG-FE-141` and `BLG-FEAT-78` both lead this release's scope (EPIC-01/ST-01, ST-31); the remaining 29 stories are weighted toward execution/debt scope rather than governance-process scope (see Skill-Silo note in `run_manifest.md §STEP 3`), which is the closest available honouring of the "prioritise user features" instruction given the actual state of the backlog.

Advisory notes (1.1 Backlog Age, 1.2 Provisional-Target, 1.3 Design-Gate Language, 1.4/1.4a/1.4a.1/1.4b Perennial-Return/Gate-Proximity/Sunset/Within-Sprint checks): see `run_manifest.md §STEP 1` for full detail. No hard-gate findings. Design Gate required (2 UI-facing items) — see STEP 4.1 below.

---

## Scope

31 stories across 7 grouped EPICs (S2-01 through S2-07, 1:1 with EPIC-01 through EPIC-07). Full scope document: `docs/product/scope/scope--2026-08-07__release-v8.4.md`. Full acceptance criteria: `stage4_backlog_slice.md`.

---

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|------------------------|
| EPIC-01 | S2-01 | Financial Reporting & Records Owner | RISK-05 | None — standalone |
| EPIC-02 | S2-02 | API Contracts & Documentation Owner; Data Model & Domain Schema Owner | RISK-01 | ST-02 before EPIC-05/ST-20 |
| EPIC-03 | S2-03 | Backend Engineering Patterns Owner; Data Model & Domain Schema Owner; AI Compliance & Governance Officer | RISK-03 | ST-11 after BLG-BE-80 (already shipped v8.3) — no in-cycle dependency |
| EPIC-04 | S2-04 | Head of Engineering; Frontend Specifications & UX Documentation Owner; Cybersecurity & Trust Lead | RISK-02 | ST-01 and ST-16 require Design Gate pass before sprint planning seals |
| EPIC-05 | S2-05 | Infrastructure & Operations Owner; FinOps & Resource Architect | RISK-06 | ST-20 after EPIC-02/ST-02 |
| EPIC-06 | S2-06 | QA & Testing Owner; Director of Quality; Financial Reporting & Records Owner; Metrics Definitions & Analytics Owner | RISK-04 | None — standalone |
| EPIC-07 | S2-07 | Head of Specs Team; Head of Engineering | RISK-07 | None — standalone |

**EPIC-02 note:** ST-02's fix to `openapi.yaml` is foundational — it corrects the file's structural validity (currently not strictly OpenAPI 3.x-compliant) before any further endpoint documentation work (ST-03 through ST-09, and EPIC-05/ST-20) is layered on top. Sequence ST-02 first within EPIC-02/across the sprint.

**EPIC-04 note:** `BLG-FE-141` (ST-01) and `BLG-FE-140` (ST-16) both have observable UI acceptance criteria (visible rendering / colour). Per CLAUDE.md's frontend-testing-gate rule, each requires Playwright coverage or a recorded human staging run before merge — see `stage4_backlog_slice.md` ACs. This also triggers `design_gate_required = true` at STEP 4.1 (below); `run design-gate --cycle 2026-08-07__release-v8.4` must pass before `plan sprint`.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|-------------|----------------|
| RISK-01 | EPIC-02 | Restructuring `openapi.yaml` (moving ~23 endpoints from `components:` to `paths:`) is a large mechanical edit to a file every other contract-facing story this cycle touches — risk of introducing a new structural break while fixing the existing one | High | ST-02's own AC requires `yaml.safe_load(...)['paths']` count to match a raw-text scan, and the OpenAPI Drift Detection CI gate to pass, before merge — both are automated, objective checks | null |
| RISK-02 | EPIC-04 | CSP tightening (`ST-18`, removing blanket `'unsafe-inline'`) risks breaking app load/render if an inline script/style dependency is missed during audit | Medium | ST-18's own AC requires full audit of inline usage first, and confirms no functional regression before merge; narrow, documented exception permitted if full removal isn't feasible | null |
| RISK-03 | EPIC-03 | `ST-13`/`ST-14` (audit-trail extension, auto-generated data dictionary) touch schema-adjacent tooling; risk of scope creep beyond the stated M-effort estimate | Low | Both ACs are narrowly scoped (extend an existing pattern; generate-and-triage, not generate-and-reconcile) with explicit owner sign-off gates | null |
| RISK-04 | EPIC-06 | `ST-26` (backfill 24 undocumented Playwright spec files) is inherently a larger cataloguing effort than its M-effort band suggests, given 24 individual files to enumerate | Low | AC requires an exact count match (spec files / scenarios), which is mechanically verifiable rather than open-ended; Director of Quality sign-off required | null |
| RISK-05 | Release-level | Only 2 of 31 stories are genuine build-and-ship user features this cycle — the "prioritise user features" instruction is only partially satisfiable given current backlog gate states | Medium | Documented explicitly in `run_manifest.md §STEP 2` and `decisions--2026-08-07__release-v8.4.md`; accepted by Product Owner delegated authority as the correct honouring of the instruction given the backlog's actual state, not a planning gap | null |
| RISK-06 | EPIC-05 | `ST-20` (19-endpoint performance baseline) requires live staging access and ≥5 samples per endpoint — a larger execution-time cost than its S-effort band alone suggests | Low | Same shape as prior cycles' equivalent items (`BLG-OPS-133`'s own predecessor pattern); execution-time risk, not planning-time risk | null |
| RISK-07 | EPIC-07 | `ST-30` (dry-run cross-EPIC merge runbook) requires deliberately sequencing 2 genuinely parallel EPIC branches in the same sprint to exercise the runbook — an execution-sequencing dependency on how Sprint Planning assigns branches, not fully controllable at this planning stage | Low | Sprint Planning to be advised of this story's intent when assigning EPIC branches; if no natural parallel-branch opportunity exists this sprint, story carries to the next sprint with capacity where one does | null |

None of the above risks carry a "must resolve before sprint planning seal" disposition — all are mitigated by in-story acceptance criteria or execution-time sequencing, not pre-sprint decisions. No `## Pre-sprint Planning Required Decisions` section required in `cycle_summary.md`.

---

## Integrity Validation — 3.5 Local Model Integrity

No story in this cycle's scope touches AI model routing, prompt templates, or model version pinning. `ST-12` (AI provenance logging) adds a metadata field on write, it does not change model selection or invocation behaviour. Pass — no local model/prompt-drift integrity issue identified.

---

## Capacity Check

**Effort Band Lookup (ST-14/shared_standards §16.7):** `scored_initiatives.md` loaded at STEP 0 — 0 matching rows for this cycle's 7 EPICs (all backlog-driven debt/hardening/single-feature scope, not roadmap-level scored initiatives). Falling back to inline STEP 4 estimates for all 7 EPICs; no advisory required (no matching row = no advisory per the three-tier rule).

**Estimated effort (midpoint, per item's own backlog `Effort` band):**

| Band | Items (this cycle) | Midpoint days each | Subtotal |
|------|---------------------|----------------------|----------|
| XS (<1h–0.5d) | ST-01, ST-03, ST-19, ST-21, ST-25 (5) | ~0.25 | ~1.25 |
| S (~0.5–1d) | ST-04, ST-05, ST-06, ST-07, ST-08, ST-10, ST-11, ST-12, ST-15, ST-16, ST-20, ST-22, ST-23, ST-24, ST-27, ST-28, ST-29, ST-30, ST-31 (19) | ~0.75 | ~14.25 |
| M (~1–2d) | ST-02, ST-09, ST-13, ST-14, ST-17, ST-18, ST-26 (7) | ~1.75 | ~12.25 |
| **Total (31 items)** | | | **~27.75 days** |

Estimated total effort ~27.75 days against the confirmed ~24-28 day capacity band — **within band, at the top**, consistent with the explicit user "full capacity" instruction. This is an approximate midpoint estimate; individual item effort bands are indicative per `shared_standards.md`'s standing notice, not committed hours.

**Outcome: PASS** (within the 24-28 day band; does not exceed the 28-day warn threshold).

No `### Phasing Recommendation` subsection required — outcome is `pass`, not `warn`.

```yaml
# state.json update (STEP 4.5):
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity

- All 7 S2-IDs (S2-01–S2-07) map to exactly 1 EPIC each (EPIC-01–EPIC-07) — no orphans, no EPIC without an S2 mapping.
- All 7 EPIC-IDs referenced in `stage4_backlog_slice.md` match the EPIC table in `release_plan.md §Execution Plan` exactly.
- All 7 RISK-IDs (RISK-01–RISK-07) referenced in the EPIC table appear as rows in the Risk Register Summary — no orphaned RISK references.
- All 31 ST-IDs in `stage4_backlog_slice.md` appear in `stage4_issue_manifest.json` exactly once each (ST-01–ST-30 in original sequence, ST-31 appended as a late-breaking addition per the STEP 2 self-caught-correction finding).
- All 31 backlog source IDs referenced in `stage4_backlog_slice.md` match the `v8.4 Release Slice` table committed to `claude/backlog/backlog.md` exactly (31 rows, 1:1).

**Outcome: PASS.**

## Integrity Validation — 5.7 Decision Record Integrity

`artifacts.escalations` is not `present` this cycle (0 escalations raised — no blockers encountered at any hard/conditional gate). Per the engine's own rule, this check is skipped. **Outcome: not_applicable.**

```yaml
# state.json update (STEP 5.5):
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```
