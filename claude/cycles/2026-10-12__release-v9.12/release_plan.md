Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v9.12
Cycle: 2026-10-12__release-v9.12
Last Updated: 2026-10-12

# Release Plan — v9.12

## Readiness

Preflight (STEP -1) passed in full. The gate-by-gate record is in `run_manifest.md`. Notable items:
- **§-1.2:** cleared directly. `v9.12` has a roadmap section, named by Product Owner direction at the v9.11 closure (DL-085) in place of a scheduled rebalance, and it commits `BLG-BE-162` (P1).
- **§-1.6 SLA-breach check:** clear. All 15 root `open_escalations` entries are Resolved.
- **§1.3a:** 0 date-lapsed gates, so no gate edit was made and `backlog.md` was not changed by this run.
- **Open v9.11 closure action #8(b)** (extend §1.3a bound 5, deadline "before `plan release v9.12`"): still open. It is a prompt change outside this routine's write scope. No gate removed by a Product Owner decision affects this release's ACs. Surfaced to the user in the session summary.

Several stories carry a ruling or decision as their first sub-step:
- ST-10: manual stop setting under §7.3.
- ST-04: briefing/chat failure action.
- ST-23: whether light mode is supported. This one is pre-sprint (RISK-03).
- ST-43: reduced-roster idea windows.
- ST-27: possible PO accept-risk.

Seven stories expect Human-Delegation for live environments or dashboards: ST-01, ST-26, ST-28, ST-29, ST-30, ST-34 and ST-38 (RISK-01).

## Scope

48 S2-items across 6 EPICs, 27.95 estimated days. Full table: `docs/product/scope/scope--2026-10-12__release-v9.12.md`. Ready pool, selection method and every disposition: `run_manifest.md` Scope Construction.

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 — AI Feature Correctness & Cost Visibility | S2-01–S2-06 | Backend Engineering Patterns Owner; AI Compliance & Governance Officer | RISK-01, RISK-04 | ST-01 first (P1); ST-02 → ST-03 → ST-04 (same briefing module); ST-06 after ST-01 (`ai_endpoints.md`) |
| EPIC-02 — Stop, Sizing & Position Correctness (build-and-ship) | S2-07–S2-16 | Head of Engineering; Strategy Rules & System Intent Owner | RISK-02, RISK-04, RISK-05 | ST-07 → ST-08 → ST-09 (sizing service); ST-10's ruling first, ST-10 before ST-15; ST-11 → ST-12 (recompute paths); ST-16 before ST-26 (cross-EPIC) |
| EPIC-03 — Trade Entry, Settings & Accessibility (build-and-ship) | S2-17–S2-24 | Head of UX & Design; Frontend Specifications & UX Documentation Owner | RISK-03, RISK-04, RISK-05, RISK-06 | ST-23's light-mode decision pre-sprint; ST-17 → ST-18 → ST-19 (Trade Entry); ST-20 → ST-21 |
| EPIC-04 — Security, Operations & Platform | S2-25–S2-32 | Infrastructure & Operations Owner; Cybersecurity & Trust Lead | RISK-01, RISK-05 | ST-26 after ST-16/ST-20/ST-21 (cross-EPIC); ST-29 → ST-30; ST-28 late (one CI run over the final tree) |
| EPIC-05 — Spec & Data Model Hygiene | S2-33–S2-38 | Data Model & Domain Schema Owner; API Contracts & Documentation Owner | RISK-01, RISK-04 | ST-34 → ST-38 (`data_model.md`); ST-37 before ST-14's possible addendum (cross-EPIC, same record) |
| EPIC-06 — Governance Tooling & Test Integrity | S2-39–S2-48 | Head of Specs Team; PMO Lead; QA & Testing Owner | RISK-06, RISK-07 | ST-39 first; ST-40 → ST-41 → ST-42 → ST-43 (sequential governance bumps); ST-45 → ST-44 |

**EPIC-01 note:** ST-01 (`BLG-BE-162`, P1) is the release's anchor. Since 2026-04-18, every journal summary requested from Trade History has failed with HTTP 422. Seating it at P1 was the condition of v9.11's verification acceptance.

**EPIC-02 / EPIC-03 note:** build-and-ship scope leads, with 16 U-shaped items worth 11.85d (42% of effort), up from v9.11's 30%. This answers the last rebalance's Skill-Silo reading (87.4%, above ceiling) and the 7th consecutive PVR Alert.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-01, EPIC-04, EPIC-05 | Seven stories need access the governed environment lacks: live migrations on staging and production (ST-01, ST-26), the Render dashboard (ST-29), a deliberate staging divergence with a Telegram receipt (ST-30), a staging check of the bumped build (ST-28), a production `pg_indexes` read (ST-34), and a live US-row sample (ST-38; staging needs the user's permission). | Medium | Human-Delegation at sprint start to the Infrastructure & Operations Owner or the Data Model & Domain Schema Owner, following the DS-27/28/29 precedent at v9.11. Code and docs proceed regardless. | null |
| RISK-02 | EPIC-02 | ST-10 needs a Strategy Rules & System Intent Owner ruling on whether a user may set or raise a stop manually under §7.3. ST-25's option (b) would need one too. ST-14 may need a dated addendum to the Gap Risk Flag §13 record. | Medium | ST-10's ruling is its first sub-step (`delegated_decision`). ST-25 defaults to option (a), which needs no ruling. ST-14's AC cites §13.3 and §13.5 (v2.61 clause-citation rule). | null |
| RISK-03 | EPIC-03 | ST-23 is the largest story (2.5d), and its first step is deciding whether light mode is a supported theme. The answer changes the work: tokens and fixes across 4 pages, or a recorded decision and a toggle change. | High | **Must resolve before sprint planning seals**, expected at the design gate. Head of UX & Design decides with the Product Owner. If light mode is not supported, Sprint Planning re-estimates ST-23. Listed in `cycle_summary.md`. | null |
| RISK-04 | EPIC-01, EPIC-02, EPIC-03, EPIC-05 | Shared files are edited across EPICs: `openapi.yaml` (ST-01, ST-10 if a route is added, ST-15, ST-17), the `SystemStatus.js` fallback count and `SC-SS-01b` (ST-10 if a route is added, ST-17), and `data_model.md` (ST-01, ST-26, ST-34, ST-38). | Medium | Every contract change updates `openapi.yaml` in the same commit (CLAUDE.md §2). Merges follow CLAUDE.md §8: union of paths, migration blocks in ascending order, and the endpoint count recomputed from `routers/test.py` rather than taken from either side. | null |
| RISK-05 | EPIC-02, EPIC-03, EPIC-04 | The Settings path is edited by three EPICs: ST-16 (`create_settings`), ST-20/ST-21 (`Settings.js`) and ST-26 (settings writes and a new line on `Settings.js`). | Medium | ST-26 is sequenced after ST-16 and ST-20/ST-21. Cross-EPIC merges follow CLAUDE.md §8. | null |
| RISK-06 | EPIC-03, EPIC-06 | Governance-file edits: CLAUDE.md §8 (ST-39), `release_planning_prompt.md` (ST-40), `execution_prompt.md` (ST-41), `roadmap_prompt.md` (ST-42), possibly `idea_intake_prompt.md` (ST-43), and a role charter (ST-21). ST-44 writes `claude/roadmap/role_share_history.md`. | Medium | Every prompt edit runs the CLAUDE.md §6 checklist, sequentially on the EPIC-06 branch, with the §8 step 2a per-file version-collision check at merge. ST-44 is `delegated_decision` under the named-file rule (`ESC-CLOSE-20261006-01`). ST-21's charter edit is under Director of HR authority. ST-39's CLAUDE.md edit is under Head of Specs Team authority. | null |
| RISK-07 | Release-level | Until ST-39 merges, a clean CLAUDE.md §8 merge can splice `backlog.md` item bodies, as `3237cb5e` did at v9.11. | Medium | Apply v9.11 Carry-Forward #3 (diff EPIC/story records and item bodies against both parents) after every merge resolution. Land ST-39 early. | null |
| RISK-08 | Release-level | 48 stories is 5 more than v9.11's 43. Per-story overhead (commits, QA evidence, DoQ blocks) is higher than the day estimate suggests. | Medium | 34 stories are XS or ≤0.5d and are grouped by file. Sprint Planning may split the release into 2 sprints along EPIC lines (EPIC-01/02/03, then EPIC-04/05/06). | null |

## Capacity Check

**Effort Band Lookup (ST-14):** `scored_initiatives.md` holds 0 active initiatives, so there are no pre-assigned bands. All figures are inline STEP-4 estimates under `workforce_capacity.md`'s precedence rule.

**ST-35 calibration check:**
- Raised `BLG-BE-162` (live migration plus staging verification, 0.5→1.0), `BLG-SEC-41` (new table, 1.0→1.5) and `BLG-OPS-182` (live staging divergence, XS→S).
- Held 7 items whose scope names the count: `BLG-QA-209` (11 files), `BLG-TECH-22` (8+20 deps), `BLG-GOV-369` (4 pages), `BLG-SPEC-178` (5 findings), `BLG-SPEC-183` (sample already in the estimate), `BLG-QA-213` (automated static test) and `BLG-OPS-181` (one deploy).

| EPIC | Stories | Days |
|------|---------|------|
| EPIC-01 | 6 | 2.80 |
| EPIC-02 | 10 | 5.55 |
| EPIC-03 | 8 | 7.05 |
| EPIC-04 | 8 | 5.05 |
| EPIC-05 | 6 | 2.10 |
| EPIC-06 | 10 | 5.40 |
| **Total** | **48** | **27.95** |

Confirmed capacity band: **~24–28 working days** (`claude/roadmap/workforce_capacity.md`, reconfirmed under `ESC-EXEC-20260921-07`). 27.95 / 28.00 = **99.8% of the band's top edge**: within band, at the ceiling, per the explicit "full capacity" instruction.

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

No Phasing Recommendation subsection: the outcome is `pass`, not `warn`. RISK-08's optional two-sprint split is advisory.

## Integrity Validation

### 3.5 Local Model Integrity

Each of the 48 S2-items maps to exactly one EPIC:
- S2-01…06 → EPIC-01
- S2-07…16 → EPIC-02
- S2-17…24 → EPIC-03
- S2-25…32 → EPIC-04
- S2-33…38 → EPIC-05
- S2-39…48 → EPIC-06

No item is unmapped or double-mapped. All 8 RISK-IDs declare a `Relates to` EPIC or Release-level. Every cross-EPIC dependency runs one way, so there are no cycles: ST-26 after ST-16/ST-20/ST-21, and ST-37 before ST-14's possible addendum.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

### 5.5 Cross-Stage Integrity

- All 48 S2-IDs map to an EPIC in the Execution Plan table: confirmed.
- EPIC-IDs in `stage4_backlog_slice.md` and `stage4_issue_manifest.json` (EPIC-01–EPIC-06) match the Execution Plan: confirmed.
- All RISK-IDs in the EPIC table (RISK-01 to RISK-07) appear in the Risk Register; RISK-08 is Release-level: confirmed.
- ST-01–ST-48 in the slice match the issue manifest one to one (48 entries, same S2-ID order): confirmed by script.
- No orphaned references.

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
attributes.cross_stage_integrity: pass
```

### 5.7 Decision Record Integrity

Not applicable. This session raised no escalations (`artifacts.escalations = not_present`). `decisions--2026-10-12__release-v9.12.md` is present and populated.

```yaml
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.decisions_validated: not_applicable
```

## Publish Gate Evaluation

All STEP 6 conditions hold:
- This cycle's `open_escalations` is empty.
- There are no deferred escalations or `deferred_execution_blockers`.
- `stage4_5_capacity_check` = pass; `stage5_5_cross_stage_integrity` = pass; `stage5_7` = not_applicable.
- `stage1_readiness` and `stage3_5_model_integrity` = pass.
- `plan_structured`, `plan_executable` and `backlog_committed` = true.
- Backlog and roadmap locks are released.

→ `status = Validated`, `publish_eligible = true`.

## Pre-sprint Planning Required Decisions

RISK-03 (High, must resolve before the sprint planning seal) is carried into `cycle_summary.md`. RISK-02's rulings are resolved inside the sprint as first sub-steps, so they do not gate the seal.
