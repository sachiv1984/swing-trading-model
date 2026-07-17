**Owner:** Head of Specs Team
**Status:** Published
**Cycle:** 2026-07-17__release-v7.4
**Release:** v7.4
**Last Updated:** 2026-07-17

---

# Release Plan — v7.4 (UI Feature Expansion: Command Palette, Alerts, Bulk Actions, Saved Filters)

## Readiness

**Roadmap authority:** `claude/roadmap/current_roadmap.md` §3 — `### v7.4 — UI Feature Expansion`, formally version-labelled at rebalance `2026-07-17__scheduled` (STEP 8.1 Option (a)). Anchor scope confirmed via `IDEA-product-owner-20260717-01` (Promoted-Added) and reinforced by the Skill-Silo pull-forward response to `IDEA-challenger-20260717-02`.

**Candidate scope (5 items, all P1 except readiness bundle which is also P1):**
- `BLG-FE-115` — Global command palette / cross-page search (M, ~1–2 days)
- `BLG-FE-116` — User-defined custom price alerts (L, ~3–5 days)
- `BLG-FE-117` — Bulk actions on list/table views (M, ~1–2 days)
- `BLG-FE-118` — Saved filter views and calendar view (L, ~3–5 days)
- `BLG-SPEC-95` — v7.4 UI-heavy release readiness bundle (L, ~5–7 days)

All 4 feature items' individual pre-implementation readiness passes (`BLG-SPEC-91/92/93/94`) shipped in v7.3, clearing each item's prior blocking gate. `BLG-FE-116`/`BLG-FE-117` additionally cleared §13 pre-checks (RISK-03/RISK-04, both PASS) at that stage.

### 1.1 Backlog Age Advisory

Scanned `claude/backlog/backlog.md` for spec/documentation debt items in this release's candidate slice with 2+ cycles unassigned. None of the 5 candidate items are spec/documentation debt classified (4 are Frontend/UX feature items, 1 is Spec/Pre-Implementation Readiness filed this cycle — 0 prior cycles aged). No advisory triggered.

### 1.2 Provisional-Target Advisory

9 backlog items carry `Provisional-Target: v7.4`. Of these:
- 5 are this release's candidate scope (`BLG-FE-115/116/117/118`, `BLG-SPEC-95`).
- 3 are governance/process verification items owned by other roles, not implementation scope (`BLG-GOV-248`, `BLG-GOV-249`, `BLG-GOV-250`) — addressed at STEP 3 / flagged forward, not added as ST items (see `run_manifest.md`).
- 1 (`BLG-FE-120` — shared toast/notification primitive, P2) carries `Provisional-Target: v7.4` but is not named in the roadmap's anchor scope for this release. Flagged for Product Owner: candidate for inclusion or explicit deferral to v7.5 — **not added to firm scope by this engine** (roadmap anchor scope takes precedence; PO did not name it in the STEP 8.1 disposition). Recommend Product Owner confirm disposition before or during sprint planning if capacity allows (see Capacity Check, STEP 4.5 — capacity permits absorption if PO elects to add it).

### 1.3 Design-Gate Language Scan

All 4 feature items are UI-facing (delegated_frontend / observable UI ACs — visible rendering, element presence, interaction). `BLG-SPEC-95` is a pre-implementation readiness pass (spec/dependency/design-review document), not itself shippable UI, but two of its 6 scope items ("design review of command-palette keyboard navigation", "UX specs for saved-filters empty state and bulk-actions confirmation modal") are design-decision-shaped. **Design Gate Required — see STEP 4.1.**

### 1.4a Perennial-Return Check

Checked `BLG-FE-115/116/117/118` and `BLG-SPEC-95` against `2026-07-16__release-v7.3`'s `stage4_backlog_slice.md` for `returned_to_backlog`/`deferred` status: none appear there (v7.3's slice was `BLG-FE-109/110/111` + `BLG-SPEC-91/92/93/94`, a disjoint set — the 4 FE items entering scope now were *carried on the roadmap* as unblocked-but-not-yet-scoped, not returned from a sprint backlog). No perennial-return disposition required.

### 1.4b Within-Sprint Date Gate Classification

Scanned all 5 candidate items for gate conditions with a specific calendar clearing date falling inside the planned sprint window. None of the 5 items carry a date-based gate condition — all gates were condition-based (readiness-pass completion, §13 pre-check), already cleared in v7.3. No within-sprint date gate items found; no conditional classification required on this basis.

### 1.4 Gate-Condition Proximity Scan

None of this release's 5 candidate items are gate-blocked (all cleared in v7.3). Gate proximity table below covers the Arc 4/5 gates tracked for future releases, per mandatory sub-check — none affect this release's scope.

| Item | Gate condition | Current trajectory | Projected clear date |
|---|---|---|---|
| SI-02 (Behavioural Drift, Arc 5) | ≥20 closed trades w/ linked trade_plans (1); p99 <2s stable 7-day (2); drift scores meaningful (3) | Re-checked live 2026-07-17 (same-day as this release plan, via rebalance `2026-07-17__scheduled`): `GET /trades`→20, `GET /trade-plans`→11 rows/0 linked, `behavioural-drift`→`insufficient_data` (9 trades/90-day window). 6th consecutive byte-identical reading. `BLG-FE-109` (UX fix targeting condition 1) shipped v7.3 but not yet exercised. | Not yet projectable — awaiting first post-BLG-FE-109 usage signal. Not in this release's scope. |
| PO-02 (Journal Pattern Recognition, Arc 4) | 6+ months AI-summarised journal entries | Trajectory unknown this cycle (not re-queried — no scope item in this release touches Arc 4). | ~2026-10-20 per `strategy_rules.md` §507 (prior estimate, not re-verified this cycle). Not in this release's scope. |
| PO-04 (50+ trades with plans) | 50+ trades with linked plans | Trajectory unknown this cycle (no scope item touches this gate; also blocked by SI-02's same linkage mechanism). | Data not available this cycle — Product Owner to surface at next readiness review if this gate becomes release-relevant. |

**Do not halt** — advisory only. No candidate item in this release is gate-blocked.

```yaml
# state.json update (STEP 1):
artifacts.stage1_readiness: pass
```

---

## Scope

Firm scope (no scope changes from roadmap anchor — all 5 items promoted directly per §3's `IDEA-product-owner-20260717-01` commitment):

| S2-ID | Item | Description |
|-------|------|-------------|
| S2-01 | `BLG-SPEC-95` | v7.4 UI-heavy release readiness bundle — dependency pre-flight (`cmdk`, `react-day-picker`), UX specs (saved-filters empty state, bulk-actions confirmation modal), command-palette keyboard-nav design review, Playwright visual-regression baseline scope, analytics event schema, regression-suite CI tagging |
| S2-02 | `BLG-FE-115` | Global command palette / cross-page search (Cmd/Ctrl-K) |
| S2-03 | `BLG-FE-116` | User-defined custom price alerts |
| S2-04 | `BLG-FE-117` | Bulk actions on list/table views (multi-select, tag/archive/remove) |
| S2-05 | `BLG-FE-118` | Saved filter views and calendar view |

**Items explicitly deferred:** None from the named roadmap anchor scope. `BLG-FE-120` (shared toast/notification primitive, P2) considered per STEP 1.2 advisory and deferred — not part of the PO's named anchor scope for this release; may be revisited at v7.5 scoping or pulled into this sprint later if capacity allows and PO elects (see Capacity Check).

```yaml
# state.json update (STEP 2):
artifacts.stage2_scope_extraction: pass
artifacts.stage2_scope_document: present
```

---

## Execution Plan

**EPIC bundling decision (resolves `BLG-GOV-248`):** `BLG-GOV-248` asked for a cost/benefit note ahead of this invocation, but none had been pre-produced. Analysis performed directly here: the 4 feature items share no data-model dependency (per the backlog item's own problem statement) and touch largely disjoint files (command palette, alerts, bulk-select, saved-filters/calendar). A single bundled EPIC would force one large PR spanning 4 unrelated surfaces, serialise otherwise-parallel work, and increase review/merge risk. **Recommendation: split** — 1 EPIC per feature item plus 1 EPIC for the shared readiness bundle (5 EPICs total), consistent with the per-item EPIC pattern already used for `BLG-SPEC-91–94` in v7.3. Full rationale recorded in `decisions--2026-07-17__release-v7.4.md`.

| EPIC-ID | Scope items | Owner | Key risk | Sequencing constraint |
|---------|-------------|-------|----------|-----------------------|
| EPIC-01 | S2-01 | Frontend Specifications & UX Documentation Owner; Head of UX & Design; Director of Quality | RISK-01 | First — gates EPIC-02/03/04/05 |
| EPIC-02 | S2-02 | Head of UX & Design; Frontend Specs & UX Documentation Owner | RISK-05 | After EPIC-01 |
| EPIC-03 | S2-03 | Head of UX & Design; Frontend Specs & UX Documentation Owner; Backend Engineering Patterns Owner | RISK-03 (cleared) | After EPIC-01 |
| EPIC-04 | S2-04 | Head of UX & Design; Frontend Specs & UX Documentation Owner | RISK-04 (cleared) | After EPIC-01 |
| EPIC-05 | S2-05 | Head of UX & Design; Frontend Specs & UX Documentation Owner | RISK-05, RISK-02 | After EPIC-01 |

EPIC-01: Delivers the `cmdk`/`react-day-picker` dependency additions and UX specs that EPIC-02 and EPIC-05 need before implementation can start cleanly; also delivers the confirmation-modal spec EPIC-04 needs and the keyboard-nav design review EPIC-02 needs. Treat as a hard sprint-1 sequencing gate for the other 4 EPICs.

### Risk Register Summary

| RISK-ID | Relates to | Description | Priority | Mitigation | escalation_ref |
|---------|------------|--------------|----------|------------|----------------|
| RISK-01 | EPIC-01 | Readiness bundle (L, ~5–7 days) is on the critical path for all 4 downstream EPICs; any slip delays the whole release | High | Sequence EPIC-01 first in Sprint 1; do not start EPIC-02/03/04/05 implementation until EPIC-01's dependency-install + spec ACs are met | null |
| RISK-02 | EPIC-01, EPIC-05 | New npm dependency `react-day-picker` (and `cmdk` for EPIC-02) must be added correctly in EPIC-01's pass or EPIC-02/EPIC-05 block on missing deps | Medium | `BLG-SPEC-95` AC explicitly requires both deps added to `package.json` in the same pass; verify at EPIC-01 close before starting EPIC-02/05 | null |
| RISK-03 | EPIC-03 | (Informational — risk already cleared) §13 pre-check for custom price alerts | Low | RISK-03 PASSED at v7.3 readiness-pass stage (`BLG-SPEC-92`); no further action | null |
| RISK-04 | EPIC-04 | (Informational — risk already cleared) §13 pre-check for bulk actions | Low | RISK-04 PASSED at v7.3 readiness-pass stage (`BLG-SPEC-93`); no further action | null |
| RISK-05 | EPIC-02, EPIC-05 | `BLG-FE-115`/`BLG-FE-118` have **no** recorded §13 pre-check (per `BLG-GOV-250`) unlike EPIC-03/EPIC-04 | High — **must resolve before sprint planning seal** | Confirm §13 applicability (or explicit rule-out) for both items at `run design-gate --cycle 2026-07-17__release-v7.4`, before sprint planning seals | null |
| RISK-06 | Release-level | 5 EPICs open concurrently in one cycle — cross-EPIC merge conflicts on shared files (`execution_state.json`, `openapi.yaml`, `api_changelog.md`) discovered reactively on 4 prior occasions (per v7.3 lessons-learnt carry-forward #3) | Medium | Apply `CLAUDE.md` §8 Cross-EPIC Merge Conflict Resolution procedure proactively; merge simplest/smallest-diff EPIC first each time two PRs are open concurrently | null |

## Integrity Validation — 3.5 Local Model Integrity

Verified: all 5 S2-IDs map to exactly one EPIC each (S2-01→EPIC-01 … S2-05→EPIC-05); no orphaned scope items; no EPIC without a Maps-to S2 reference; all 6 RISK-IDs referenced in the EPIC table appear in the Risk Register above; no escalations raised this cycle (`escalation_ref` = null throughout) — `stage5_7` will be `not_applicable`.

```yaml
# state.json update (STEP 3):
artifacts.stage3_execution_plan: pass
artifacts.stage3_decisions_record: present
attributes.plan_structured: true
status: Planning
# state.json update (STEP 3.5):
artifacts.stage3_5_model_integrity: pass
attributes.plan_executable: true
```

---

## Capacity Check

**Design Gate Required:** `true` — 4 of 5 EPICs are UI-facing with observable ACs (EPIC-02/03/04/05); EPIC-01 includes 2 design-decision-shaped sub-items. Run: `run design-gate --cycle 2026-07-17__release-v7.4` before `plan sprint`.

**Effort Band Lookup (ST-14):** No `scored_initiatives.md` rows match this cycle's scope (0 active initiatives, backlog-driven release) — falling back to STEP 4 inline estimates for all 5 EPICs (each carries its own backlog-filed day-range estimate).

| EPIC | Effort (mid-point) |
|------|---------------------|
| EPIC-01 (BLG-SPEC-95) | 6 days |
| EPIC-02 (BLG-FE-115) | 1.5 days |
| EPIC-03 (BLG-FE-116) | 4 days |
| EPIC-04 (BLG-FE-117) | 1.5 days |
| EPIC-05 (BLG-FE-118) | 4 days |
| **Total** | **17 days** |

**Capacity baseline:** ~24–28 working days/sprint (DL-069, effective 2026-07-17 — raised same day as this release plan; supersedes the prior ~12–14 day baseline that produced 3 consecutive near-top-of-band readings at v7.1/v7.2/v7.3, per the v7.3 lessons-learnt carry-forward). 17 days falls comfortably mid-band under the new baseline (61–71% of the 24–28 day range), a materially different picture than it would have been under the old baseline (17 days would have triggered `warn` against a 14-day threshold).

**Outcome: PASS.** No Phasing Recommendation subsection required — total effort is within capacity without needing to split across sprints. Sequencing (EPIC-01 first) is a dependency-driven constraint (§Execution Plan), not a capacity-driven phasing need.

**Forward flag (`BLG-GOV-249`):** This capacity check is release-planning's own estimate; `BLG-GOV-249` (PMO Lead) specifically asks that the *next* `plan sprint` invocation verify its capacity read matches the DL-069 baseline value (~24–28 days) rather than any stale cached figure. Recorded in `cycle_summary.md` for Sprint Planning Engine STEP -1 to consume.

```yaml
# state.json update (STEP 4.5):
artifacts.stage4_5_capacity_check: pass
attributes.capacity_feasible: pass
```

---

## Integrity Validation — 5.5 Cross-Stage Integrity / 5.7 Decision Record Integrity

**5.5 Cross-Stage Integrity:** Verified — all 5 S2-IDs (S2-01…S2-05) map to exactly one EPIC each in `stage4_backlog_slice.md` (EPIC-01…EPIC-05); all 5 EPIC IDs referenced in `release_plan.md §Execution Plan` match `stage4_backlog_slice.md` exactly; all 6 RISK-IDs in the EPIC table appear in the Risk Register Summary; no orphaned references found; `stage4_issue_manifest.json` contains exactly 5 entries (ST-01…ST-05) matching the backlog slice 1:1.

**5.7 Decision Record Integrity:** Skipped (`artifacts.escalations` not present — no escalations raised this cycle). Classification: `not_applicable`.

```yaml
# state.json update (STEP 5.5):
artifacts.stage5_5_cross_stage_integrity: pass
artifacts.stage5_7_decision_record_integrity: not_applicable
attributes.cross_stage_integrity: pass
attributes.decisions_validated: not_applicable
```
