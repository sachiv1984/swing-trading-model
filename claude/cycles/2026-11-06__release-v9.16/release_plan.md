Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v9.16
Cycle: 2026-11-06__release-v9.16
Last Updated: 2026-11-06

# Release Plan — v9.16

## Readiness

Preflight (STEP -1) passed in full. The gate-by-gate record is in `run_manifest.md`. Notable items:
- **§-1.2:** cleared by the planned-release line in `current_roadmap.md` §1, "Next planned release: v9.16 — Site Structure & Usability, Phase 2", named by the Product Owner on 2026-11-06. The release's provisional content is DL-088's programme plan, Phase 2 row (§3). There is no §3 committed-items section, so the annotation goes on the §1 line, as at v9.14.
- **§-1.6 SLA-breach check:** clear. Every root `open_escalations` entry is Resolved (`ESC-CLOSE-20261106-01`/`-02` resolved 2026-11-06). `ESC-EXEC-20260910-01` remains Deferred, outside this check.
- **v9.15 Carry-Forward:** #1 (`BLG-OPS-214`, `BLG-OPS-213`) seated. #2 post-merge remainders checked, one by one. #3 is a `run roadmap` action. #4 applied: §1.4c step 0 (v2.72) is used for the first time.
- **§1.3a date-lapsed list:** 0 items.
- **§1.3a gating-item-shipped list:** 19 items, each read. 5 were cleared in place (a): `BLG-FE-39`, `BLG-QA-21`, `BLG-QA-22`, `BLG-QA-23` and `BLG-GOV-26`. Each was gated only on PT-04 (✅ Shipped v6.1) or Arc 2 (✅ Fully Complete). This is the first run where the scan reads roadmap feature IDs (v9.15 ST-37). The edits were made under the backlog lock. The other 14 keep an unmet limb.
- **Split-achievability exclusions:** `BLG-OPS-48` and `BLG-AI-23` are not re-seated. Their remainders are `BLG-OPS-214`/`213`/`BLG-SPEC-223` and `BLG-AI-27`. ST-28 (`BLG-GOV-413`) fixes the pattern.
- **§1.4c step 0:** the 8 Phase 3 items (v9.17) are held, including the P2 `BLG-FE-260`.
- **Product Owner override:** the 3 Phase 2 P3 items (`BLG-FE-251`, `252`, `253`; 3.50d) are seated so Phase 2 ships complete (user decision, 2026-11-06).

Several stories carry a ruling or decision as their first sub-step: ST-20 (non-ticker collisions, AI Compliance & Governance Officer) and ST-30 (Base44 convention, Base44 Frontend Prompt Owner).

ST-05 may write `strategy_rules.md` §4.2.1 to close the v1.26 Known deviation, under case (c). The Strategy Rules & System Intent Owner must confirm that AC line at the sprint planning seal (RISK-02).

Five stories need access the governed environment lacks: ST-11 (Anthropic console, Render), ST-12 (GitHub secret, console), ST-13 and ST-14 (production reads after a date) and ST-19 (production log tokens) (RISK-01).

## Scope

30 S2-items across 7 EPICs, 27.95 estimated days. Full table: `docs/product/scope/scope--2026-11-06__release-v9.16-site-structure-phase-2.md`. Ready pool, selection method and every disposition: `run_manifest.md` Scope Construction.

## Execution Plan

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 — Site Structure & Usability Phase 2: Navigation & Wayfinding (build-and-ship) | S2-01–S2-04 | Head of Engineering; Head of UX & Design | RISK-03 | ST-01 first; ST-01 → ST-02, ST-03 |
| EPIC-02 — Site Structure & Usability Phase 2: Today List & Signal-to-Entry Flow (build-and-ship) | S2-05–S2-08 | Head of Engineering; Head of UX & Design; Frontend Specifications & UX Documentation Owner; Strategy Rules & System Intent Owner | RISK-02, RISK-03, RISK-04 | ST-05 first; ST-07 → ST-08 |
| EPIC-03 — Site Structure & Usability Phase 2: Colour Tokens & Input Contrast (build-and-ship) | S2-09–S2-10 | Frontend Specifications & UX Documentation Owner; Head of Engineering | RISK-03 | Merges after EPIC-01 and EPIC-02 (baselines) |
| EPIC-04 — Anthropic Key Security & Operations Baselines | S2-11–S2-15 | Cybersecurity & Trust Lead; Infrastructure & Operations Owner; FinOps & Resource Architect | RISK-01, RISK-05 | ST-11 first in the sprint (P1), with ST-12; ST-13 and ST-14 conditional |
| EPIC-05 — Backend Correctness, AI Ticker Check & Spec Debt | S2-16–S2-23 | Head of Engineering; Backend Engineering Patterns Owner; AI Compliance & Governance Officer; Data Model & Domain Schema Owner; API Contracts & Documentation Owner | RISK-01, RISK-07 | ST-16 → ST-17; ST-19 → ST-20 (ruling first) |
| EPIC-06 — Arc 2 Retrospective: QA Protocol, Lifecycle Test & Journey Map | S2-24–S2-27 | QA Lead; Head of Specs Team; Head of UX & Design | RISK-06, RISK-07 | ST-26 and ST-27 after EPIC-02's ST-07/ST-08; ST-26 → ST-24 |
| EPIC-07 — Governance Process | S2-28–S2-30 | Head of Specs Team; PMO Lead; Base44 Frontend Prompt Owner | RISK-07 | ST-28 early (step 1a); ST-30 decision first |

**EPIC-01–03 note:** the three build-and-ship EPICs deliver all of Site Structure & Usability Phase 2 (DL-088, ≈15.5d), built from the v9.15 specs `navigation.md` v2 and `dashboard.md` v4.0. ST-06's Today list ships without its "Stops moved" group, as `dashboard.md` §1B allows, because `BLG-BE-205` is not seated (RISK-04).

**EPIC-04 note:** ST-11 (`BLG-OPS-214`, P1) rotates an Anthropic key overdue since 2026-08-25. ST-12 removes the key copy that the public Pages build carries. Both were accepted post-merge at v9.15 (ST-29) and lead the sprint.

**Build-and-ship share:** 13 frontend and backend build items, 17.20d (62% of effort), against v9.15's 34%. EPIC-01–03 lead the table (STEP 3 rotation advisory; the last Skill-Silo reading was 68.1%, DL-088).

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|-------------|----------|------------|----------------|
| RISK-01 | EPIC-04, EPIC-05 | Five stories need access the governed environment lacks: Anthropic console and Render env (ST-11), GitHub secret deletion and console revocation (ST-12), production reads after 2026-11-09/~11-12 (ST-13, ST-14) and the production briefing log tokens (ST-19). | Medium | Human-Delegation at sprint start, following the v9.11–v9.15 precedent. Code and docs proceed regardless. Production-only ACs are marked post-merge with tracking items at Sprint Planning STEP 6.2. ST-11 is P1, so its delegation is raised first. | null |
| RISK-02 | EPIC-02 | ST-05 AC 4 may close the `strategy_rules.md` §4.2.1 Known deviation (v1.26) under case (c). The write is void without the Strategy Rules & System Intent Owner's confirmation in the sealed sign-off summary. ST-05 also reopens the locked `trade-entry-pre-entry-checks` design record (AC 3, "not shown twice"). | High | **Must resolve before sprint planning seals:** the Strategy Rules & System Intent Owner confirms ST-05 AC 4 (dated) in `sprint_backlog.md`'s sign-off summary, or rules that the closure goes to Post-Ship Closure STEP 5. The design gate reviews the design record change. Listed in `cycle_summary.md`. | null |
| RISK-03 | EPIC-01, EPIC-02, EPIC-03 | Files edited across EPICs: `Layout.js` and the nav Playwright specs (ST-01–ST-03), `DashboardHome` (ST-06) against the `DashboardCard`/`DataTable`/`PageHeader` shells (ST-09), and `TradePlan.js` (ST-07, ST-08, ST-12). ST-09 regenerates the visual baselines for both themes. | Medium | EPIC-03 merges last, and ST-09 regenerates baselines after EPIC-01 and EPIC-02 are on `main`. Merges follow CLAUDE.md §8, including step 2a's per-file version check and step 2c's backlog integrity check. The ST-07 → ST-08 order is fixed in the slice. | null |
| RISK-04 | EPIC-02 | ST-06 (Today list, L, 3.5d) ships without its "Stops moved" group. `BLG-BE-205` (`stop_last_moved_date`, `previous_stop`) is not seated on capacity grounds, so TL-09/TL-10 are not testable. It is the largest story. | Low | `dashboard.md` §1B already specifies the group's absence until `BLG-BE-205` ships. The AC is restated to exclude TL-09/TL-10 and to test that no placeholder renders. `BLG-BE-205` is the obvious v9.17 pairing. | null |
| RISK-05 | EPIC-04 | ST-13 and ST-14 are conditional (§1.4b). Their earliest clear dates are 2026-11-09 and ~2026-11-12. ST-13 returned once at v9.15. | Low | Classified conditional, not firm. Promote only on a dated confirmation. A return is expected-path, not a deviation, but a second return triggers §1.4a at v9.17. | null |
| RISK-06 | EPIC-06 | The four Arc 2 retrospective items were filed 2026-05-21 against the v6.1 app. Their scope may be stale against today's Trade Plan flow, which EPIC-02 changes again. | Medium | ST-26 and ST-27 run after ST-07/ST-08 merge. ST-27 cross-checks findings against the programme backlog before filing new items. Each cleared gate's evidence is confirmed at the seal (restated ACs). | null |
| RISK-07 | EPIC-05, EPIC-06, EPIC-07 | Rulings and governance-file changes inside the sprint: ST-20 (AI Compliance & Governance Officer ruling), ST-30 (Base44 convention decision), ST-25 (may amend `shared_standards.md`) and ST-28 (`post_ship_closure.md`). ST-25, ST-28, ST-29 and ST-30 may all bump `OPERATIONAL_GUIDE.md`. | Medium | Rulings are `delegated_decision` first sub-steps. Governance stories follow the CLAUDE.md §6 checklist. Concurrent `OPERATIONAL_GUIDE.md` bumps are renumbered at merge under CLAUDE.md §8 step 2a, per file. | null |

## Capacity Check

**Effort Band Lookup (ST-14):** `scored_initiatives.md` holds 0 active initiatives (CPS=N/A), so there are no pre-assigned bands. All figures are inline STEP 4 estimates under `workforce_capacity.md`'s precedence rule.

**STEP 4 calibration check, run on the whole ready pool before selection (v2.63), reading Scope and AC text (v2.71):** 6 raises, +2.85d, none seated. Two are new: `BLG-BE-205` (migration) and `BLG-QA-250` (citation sweep). Four are carried from v9.15. One seated item with a sweep-style AC is held, with its count named: `BLG-FE-223` (18 sites in 8 files).

| EPIC | Stories | Days |
|------|---------|------|
| EPIC-01 | 4 | 6.00 |
| EPIC-02 | 4 | 7.75 |
| EPIC-03 | 2 | 3.00 |
| EPIC-04 | 5 | 1.10 |
| EPIC-05 | 8 | 1.20 |
| EPIC-06 | 4 | 6.50 |
| EPIC-07 | 3 | 2.40 |
| **Total** | **30** | **27.95** |

Confirmed capacity band: **~24–28 working days** (`claude/roadmap/workforce_capacity.md`). 27.95 / 28.00 = **99.8% of the band's top edge**. That is within band, at the ceiling, per the explicit "use full capacity" instruction. 0.30d of it (ST-13, ST-14) is conditional.

```yaml
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

No Phasing Recommendation subsection: the outcome is `pass`, not `warn`. Effort is front-loaded into a few large build stories: ST-06 (3.5d), ST-01, ST-07 and ST-09 (2.5d each), and ST-03, ST-24 and ST-26 (2.0d each) carry 17.0d. 13 stories are under half a day.

## Integrity Validation

### 3.5 Local Model Integrity

Each of the 30 S2-items maps to exactly one EPIC:
- S2-01…04 → EPIC-01
- S2-05…08 → EPIC-02
- S2-09…10 → EPIC-03
- S2-11…15 → EPIC-04
- S2-16…23 → EPIC-05
- S2-24…27 → EPIC-06
- S2-28…30 → EPIC-07

No item is unmapped or double-mapped. All 7 RISK-IDs declare a `Relates to` EPIC. The cross-EPIC orders (EPIC-03 after EPIC-01/02; ST-26 and ST-27 after ST-07/ST-08) run one way, and the in-EPIC orders (ST-01 → ST-02/ST-03, ST-07 → ST-08, ST-16 → ST-17, ST-19 → ST-20, ST-26 → ST-24) contain no cycles.

```yaml
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

### 5.5 Cross-Stage Integrity

- All 30 S2-IDs map to an EPIC in the Execution Plan table: confirmed.
- The EPIC-IDs in `stage4_backlog_slice.md` and `stage4_issue_manifest.json` (EPIC-01 to EPIC-07) match the Execution Plan: confirmed.
- All RISK-IDs in the EPIC table (RISK-01 to RISK-07) appear in the Risk Register: confirmed.
- ST-01 to ST-30 in the slice match the issue manifest one to one (30 entries, same S2-ID order, same source IDs), and the source set equals the selection output: confirmed by script.
- No orphaned references.

```yaml
artifacts.stage5_5_cross_stage_integrity: pass
attributes.cross_stage_integrity: pass
```

### 5.7 Decision Record Integrity

Not applicable. This session raised no escalations (`artifacts.escalations = not_present`). `decisions--2026-11-06__release-v9.16.md` is present and populated.

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

- **Override:** the 3 Site Structure & Usability Phase 2 P3 items (`BLG-FE-251`, `252`, `253`; 3.50d) are seated with the Phase 2 P2s (user decision, 2026-11-06). This displaces 7 round-robin items (3.55d).
- **§1.4c step 0 hold (rule, not an override):** the 8 Phase 3 items (20.50d), including P2 `BLG-FE-260`, stay at v9.17.
- **Gate edits (informational, §1.3a bound 6):** `BLG-FE-39`, `BLG-QA-21`, `BLG-QA-22`, `BLG-QA-23` and `BLG-GOV-26` cleared (a), citing PT-04 ✅ Shipped v6.1 and Arc 2 ✅ Fully Complete.
- **Exclusions for `groom backlog`:** `BLG-GOV-192` (already met); `BLG-OPS-48` and `BLG-AI-23` (split-achievability, see ST-28).

## Pre-sprint Planning Required Decisions

RISK-02 (High, must resolve before the sprint planning seal) is carried into `cycle_summary.md`. RISK-07's rulings are resolved inside the sprint as first sub-steps, so they do not gate the seal.
