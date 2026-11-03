Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v9.15
Cycle: 2026-11-03__release-v9.15
Last Updated: 2026-11-03

# Release Plan — v9.15

## Readiness

Preflight (STEP -1) passed in full. The gate-by-gate record is in `run_manifest.md`. Notable items:
- **§-1.2:** cleared by the planned-release section `current_roadmap.md` §3 "v9.15 — Site Structure & Usability, Phase 1", added by roadmap rebalance `2026-11-03__scheduled` (DL-088), which commits 10 items. This meets v9.14 closure Carry-Forward #1 (run a rebalance before `plan release v9.15`).
- **§-1.6 SLA-breach check:** clear. Every root `open_escalations` entry is Resolved. `ESC-EXEC-20260910-01` remains Deferred, outside this check.
- **v9.14 closure outstanding actions:** rows 1, 2, 3, 5, 6 and 7 are resolved. Row 4 (`BLG-GOV-178` split: live sample via `BLG-GOV-399`) and row 8 (link the governance overhead audit at the next `run roadmap`) remain open.
- **§1.3a date-lapsed list:** 1 item. `BLG-OPS-48`'s gate is cleared (a): `BLG-OPS-36` shipped at v4.2 and the 2026-11-01 date has passed. The edit was made under the backlog lock.
- **§1.3a gating-item-shipped list:** 20 items, each read. `BLG-OPS-48` was cleared once under the date-lapsed disposition, and `BLG-FE-195` is already bannered ✅ COMPLETE. The other 18 keep an unmet limb, so none was cleared in place.
- **Already met on reading:** `BLG-GOV-185` and `BLG-GOV-192` were first selected by the round-robin, then found already met and excluded, and the selection was rerun.
- **Product Owner override:** the Site Structure & Usability Phase 2/3 items are held to v9.16/v9.17 (DL-088 phasing). This covers 10 items, 20.00d, including 4 P2 items.

Several stories carry a ruling or decision as their first sub-step: ST-23 (open-position P&L basis), ST-25 (journal-summary check forms), ST-28 (§13 re-read), ST-44 (strategic exclusions) and ST-45 (Priority 3 deferred initiatives).

ST-28 may write `strategy_rules.md` §13 under case (c), depending on its outcome. The Strategy Rules & System Intent Owner must confirm that AC line at the sprint planning seal (RISK-03).

Four stories need access the governed environment lacks: ST-29 (Anthropic console), ST-33 (production read), ST-35 (staging and production constraints) and ST-36 (staging index) (RISK-01).

## Scope

45 S2-items across 7 EPICs, 28.00 estimated days. Full table: `docs/product/scope/scope--2026-11-03__release-v9.15-site-structure-phase-1.md`. Ready pool, selection method and every disposition: `run_manifest.md` Scope Construction.

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 — Trade Entry Integrity & Sizing (build-and-ship) | S2-01–S2-07 | Head of Engineering; Frontend Specifications & UX Documentation Owner | RISK-06 | ST-01 and ST-02 first (P1); ST-02 → ST-03 |
| EPIC-02 — Site Structure & Usability Phase 1 — Specs, Vocabulary & Quick Wins | S2-08–S2-14 | Frontend Specifications & UX Documentation Owner; Head of UX & Design | RISK-02, RISK-04 | ST-08 first; ST-08 approved → ST-11; ST-12 after ST-16 (cross-EPIC) |
| EPIC-03 — Metric & Display Correctness | S2-15–S2-23 | Metrics Definitions & Analytics Canonical Owner; Backend Engineering Patterns Owner | RISK-04, RISK-07 | ST-16 before ST-12 (cross-EPIC); ST-23 decision first |
| EPIC-04 — AI Output Checks & §13 Boundary | S2-24–S2-28 | AI Compliance & Governance Officer; Strategy Rules & System Intent Owner | RISK-03, RISK-07 | ST-25 ruling first; ST-25 → ST-27 |
| EPIC-05 — Operations, Security & Market-Data Monitoring | S2-29–S2-33 | Infrastructure & Operations Owner; Cybersecurity & Trust Lead; FinOps & Resource Architect | RISK-01, RISK-05 | ST-33 conditional (from 2026-11-09) |
| EPIC-06 — Data Model & Spec Debt | S2-34–S2-36 | Data Model & Domain Schema Owner; Head of Specs Team | RISK-01, RISK-04 | ST-35 and ST-36 in either order |
| EPIC-07 — QA & Governance Tooling | S2-37–S2-45 | Director of Quality; Head of Specs Team; PMO Lead; Product Owner | RISK-04, RISK-07 | ST-37, ST-38 early (deferred patches); ST-44, ST-45 decisions first |

**EPIC-01 note:** ST-01 (`BLG-FE-244`) is the release's anchor. Three routes into Trade Entry (sidebar, "New Position", `n`) skip the §4.2 pre-entry checks, including §4.2.1 unknown regime. ST-02 (`BLG-FE-245`) removes the fixed 1.27 FX pre-fill, which distorts US sizing by about 13% at FX 1.35, since sizing scales with FX² after `BLG-BE-190`.

**EPIC-02 note:** ST-08–ST-10 write the specs that the Phase 2 (v9.16) and Phase 3 (v9.17) build items depend on. If one is not approved by sprint close, its dependent items stay not-ready at `plan release v9.16`.

**Build-and-ship share:** 19 frontend and backend build items, 9.45d (34% of effort), against v9.14's 35%. Holding Phase 2/3 to their releases kept build items out of v9.15. A further 6.00d of design specs (ST-08–ST-10) feeds the v9.16/v9.17 build phases. EPIC-01 is build-and-ship and leads the table (STEP 3 rotation advisory; the last Skill-Silo reading was 68.1%, DL-088).

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-05, EPIC-06 | Four stories need access the governed environment lacks: Anthropic console key permissions and rotation (ST-29), production reads 7 days after deploy (ST-33), staging and production constraint changes (ST-35) and a staging index change (ST-36). | Medium | Human-Delegation at sprint start, following the v9.11–v9.14 precedent. Code and docs proceed regardless; production-only ACs are marked post-merge with tracking items at Sprint Planning STEP 6.2. | null |
| RISK-02 | EPIC-02 | ST-08–ST-10 are design specs that need the Head of UX & Design's approval. ST-11 is blocked until ST-08 is approved, and v9.16's Phase 2 depends on ST-08 and ST-09. | Medium | Spec stories start first in EPIC-02. Approval is a named sub-step with the approver in each AC. A spec not approved by close returns with a reason, and its dependants stay not-ready. | null |
| RISK-03 | EPIC-04 | ST-28 may clarify `strategy_rules.md` §13 text under case (c), depending on its outcome. The write is void without the Strategy Rules & System Intent Owner's confirmation in the sealed sign-off summary. | High | **Must resolve before sprint planning seals:** the Strategy Rules & System Intent Owner confirms ST-28 AC 3 (dated) in `sprint_backlog.md`'s sign-off summary, or rules that no §13 write is authorised this sprint. Listed in `cycle_summary.md`. | null |
| RISK-04 | EPIC-02, EPIC-03, EPIC-06, EPIC-07 | Files edited across EPICs: the Dashboard pages (ST-12, ST-16) and `metrics_definitions.md` (ST-15, ST-23). Within EPICs: `data_model.md` (ST-35, ST-36) and the nav/palette Playwright specs (ST-11–ST-14). Governance stories (ST-37, ST-38, ST-43, ST-44) may bump `OPERATIONAL_GUIDE.md`. | Medium | The ST-16 → ST-12 order is fixed in the slice. Merges follow CLAUDE.md §8, including step 2a's per-file version check and step 2c's backlog integrity check. Contract changes update `openapi.yaml` in the same commit. | null |
| RISK-05 | EPIC-05 | ST-33 is conditional (§1.4b). Its earliest clear date is 2026-11-09, and it may return to backlog if the production read is not granted in the sprint window. | Low | Classified conditional, not firm. Promote only on a dated confirmation. A return is expected-path, not a deviation. | null |
| RISK-06 | EPIC-01 | ST-01 adds a check-and-acknowledge step to every unplanned entry route and must record overrides the same way as the plan path, or the Red Flag Journal and SI-05 digest under-count. It is the largest story (2.5d). | Medium | Reuse the Trade Plan panel and validation endpoint (no new check logic). Playwright covers each route, the unknown-regime case and the no-double-panel case. One EPIC branch for all Trade Entry stories. | null |
| RISK-07 | EPIC-03, EPIC-04, EPIC-07 | Rulings or decisions are first sub-steps: ST-23 (P&L basis, Data Model & Domain Schema Owner), ST-25 (check forms, AI Compliance & Governance Officer), ST-28 and ST-44 (Strategy Rules & System Intent Owner) and ST-45 (Product Owner). | Medium | Each is a `delegated_decision` first sub-step. ST-27 waits on ST-25's ruling. | null |

## Capacity Check

**Effort Band Lookup (ST-14):** `scored_initiatives.md` holds 0 active initiatives (CPS=N/A), so there are no pre-assigned bands. All figures are inline STEP 4 estimates under `workforce_capacity.md`'s precedence rule.

**STEP 4 calibration check, run on the whole ready pool before selection (v2.63):** 6 raises, +2.70d. Two are seated: `BLG-SPEC-196` (staging and production migration, 0.5→1.0) and `BLG-SPEC-197` (staging migration, 0.15→0.5). Four are unseated: `BLG-TECH-25`, `BLG-BE-186`, `BLG-SPEC-208` and `BLG-OPS-205`. Two seated items with sweep-style ACs are held, with counts named: `BLG-FE-243` (15 sites in 10 files) and `BLG-FE-246` (about 8 label sites).

| EPIC | Stories | Days |
|------|---------|------|
| EPIC-01 | 7 | 5.05 |
| EPIC-02 | 7 | 8.50 |
| EPIC-03 | 9 | 2.40 |
| EPIC-04 | 5 | 2.20 |
| EPIC-05 | 5 | 2.15 |
| EPIC-06 | 3 | 2.00 |
| EPIC-07 | 9 | 5.70 |
| **Total** | **45** | **28.00** |

Confirmed capacity band: **~24–28 working days** (`claude/roadmap/workforce_capacity.md`). 28.00 / 28.00 = **100% of the band's top edge**. That is within band, at the ceiling, per the explicit "use full capacity" instruction. 0.15d of it (ST-33) is conditional.

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

No Phasing Recommendation subsection: the outcome is `pass`, not `warn`. 15 stories are under half a day and 34 are half a day or less.

## Integrity Validation

### 3.5 Local Model Integrity

Each of the 45 S2-items maps to exactly one EPIC:
- S2-01…07 → EPIC-01
- S2-08…14 → EPIC-02
- S2-15…23 → EPIC-03
- S2-24…28 → EPIC-04
- S2-29…33 → EPIC-05
- S2-34…36 → EPIC-06
- S2-37…45 → EPIC-07

No item is unmapped or double-mapped. All 7 RISK-IDs declare a `Relates to` EPIC. The one cross-EPIC dependency (ST-16 before ST-12) runs one way, and the in-EPIC orders (ST-02 → ST-03, ST-08 → ST-11, ST-25 → ST-27) contain no cycles.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

### 5.5 Cross-Stage Integrity

- All 45 S2-IDs map to an EPIC in the Execution Plan table: confirmed.
- The EPIC-IDs in `stage4_backlog_slice.md` and `stage4_issue_manifest.json` (EPIC-01 to EPIC-07) match the Execution Plan: confirmed.
- All RISK-IDs in the EPIC table (RISK-01 to RISK-07) appear in the Risk Register: confirmed.
- ST-01 to ST-45 in the slice match the issue manifest one to one (45 entries, same S2-ID order, same source IDs): confirmed by script.
- No orphaned references.

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
attributes.cross_stage_integrity: pass
```

### 5.7 Decision Record Integrity

Not applicable. This session raised no escalations (`artifacts.escalations = not_present`). `decisions--2026-11-03__release-v9.15.md` is present and populated.

```yaml
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.decisions_validated: not_applicable
```

## Publish Gate Evaluation

All STEP 6 conditions hold:
- This cycle's `open_escalations` is empty.
- There are no deferred escalations or `deferred_execution_blockers` for this cycle.
- `stage4_5_capacity_check` = pass; `stage5_5_cross_stage_integrity` = pass; `stage5_7` = not_applicable.
- `stage1_readiness` and `stage3_5_model_integrity` = pass.
- `plan_structured`, `plan_executable` and `backlog_committed` = true.
- The backlog and roadmap locks are released.

→ `status = Validated`, `publish_eligible = true`.

## Product Owner Sign-off Summary

- **Override:** Site Structure & Usability Phase 2/3 items held to v9.16/v9.17 (10 items, 20.00d; user decision, 2026-11-03).
- **Gate edit (informational, §1.3a bound 6):** `BLG-OPS-48` gate cleared (a), citing `BLG-OPS-36` (v4.2) and the passed 2026-11-01 date.
- **Exclusions for `groom backlog`:** `BLG-GOV-185` and `BLG-GOV-192` (already met), `BLG-GOV-400` (met by this run), `BLG-OPS-203` (resolved 2026-10-30) and `BLG-FE-195` (✅ COMPLETE).

## Pre-sprint Planning Required Decisions

RISK-03 (High, must resolve before the sprint planning seal) is carried into `cycle_summary.md`. RISK-07's rulings are resolved inside the sprint as first sub-steps, so they do not gate the seal.
