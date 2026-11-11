**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-11-11
**Cycle:** 2026-11-11__release-v9.17

# Design Gate Record — 2026-11-11__release-v9.17

## Gate Status: PASSED

Completed: 2026-11-11
PMO Lead: confirmed
Head of UX & Design: confirmed (agent-mediated, Design Gate Engine)
Product Owner: confirmed (the user, in session, 2026-11-11). The Product Owner chose the near-stop band (ST-01), the single grace view (ST-04), a brief now with the spec in the sprint (ST-06), and a section index over tabs (ST-07).

All 20 items are classified and cleared. ST-06 is cleared on a brief, with its build gated inside the story on the spec's approval (addendum). None is blocked.

| Classification | Count | Items |
|----------------|-------|-------|
| Design Required | 10 | ST-01, ST-02, ST-03, ST-04, ST-06, ST-07, ST-12, ST-13, ST-14, ST-19 |
| Design Pre-Approved | 4 | ST-05, ST-08, ST-10, ST-11 |
| Design Not Applicable | 6 | ST-09, ST-15, ST-16, ST-17, ST-18, ST-20 |

**Classification notes:**
- **EPIC-01 and ST-19 share one record.** All five stories edit `Positions.js`. ST-19's two tooltip wordings are fixed in the record, one for each choice the Strategy Rules & System Intent Owner may make before the seal (RISK-05).
- **ST-05, ST-10 build specs approved in earlier cycles.** `journal.md` v1.0 (approved v9.15, unchanged since 2026-11-05) and `dashboard.md` §1B TL-09/TL-10 (v4.0, clarified v4.1 on 2026-11-09 in an unrelated row). Each is the locked reference for its story.
- **ST-08 introduces no colour.** It applies the eight `app-*` tokens and the measured pairs in `design_system.md` v1.26 (§Semantic Colour Tokens, §Light-Theme Colour Tokens, review-pass rules). The sweep's boundary is Sprint Planning's call (RISK-02), not a design question.
- **ST-11 is Pre-Approved.** Its only visible effect is the existing "Closed" status badge (`trade_plan.md` §9).
- **ST-13 is Design Required only for the spec correction.** The screen does not change; `research_view.md` §4.7 still named a pre-v8 route, corrected here.
- **ST-12's interaction does not depend on the RISK-05 choice.** Both storage options give the user the same reset and note; the record fixes the UI and lists both storage shapes.
- **Not Applicable, but touching UI code:** ST-09 removes a dead branch in `RecentActivityCard.js` with no visible change (slice). ST-15 may file follow-ups from its "what the user sees" check; it ships no UI change.

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 (BLG-FE-260) | Decision-first Positions table | Design Required | New column set, new sort, new expandable row. Near stop = ≤ 5% band (Product Owner). | `docs/design/2026-11-11__release-v9.17/positions-decision-first/decision_record.md` §2–§3 (new) | `pages/positions.md` v2.24 → v2.25 (§Decision-First Table) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-02 (BLG-FE-261) | Card layout for Positions on narrow screens | Design Required | New layout below `md` | `positions-decision-first` §4 | `pages/positions.md` v2.25 (§Responsive Behavior, Table v2.25 row) | ✅ Cleared | Head of UX & Design |
| ST-03 (BLG-FE-262) | Combine the four banners into one strip | Design Required | New component replacing four; changed interaction (disclosure) | `positions-decision-first` §6 | `pages/positions.md` v2.25 (§Warning Strip) | ✅ Cleared | Head of UX & Design |
| ST-04 (BLG-FE-257) | Show grace period in one place, linked from the others | Design Required | Changed component on three pages; dismiss removed; new deep link. Single view chosen by the Product Owner. | `positions-decision-first` §5 | `pages/positions.md` v2.25 (§Grace Period View); `pages/dashboard.md` v4.1 → v4.2 (Card 3); `pages/risk_dashboard.md` v0.1.15 → v0.1.16 (§5) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-05 (BLG-FE-258) | Build the single Journal area | Design Pre-Approved | Builds the approved Journal spec, unchanged since 2026-11-05 | `site-structure-phase1` §2.3 (brief, v9.15) | `pages/journal.md` v1.0 (locked: JA-01..JA-21) | ✅ Cleared | Head of UX & Design |
| ST-06 (BLG-FE-259) | Merge Reports and Performance Analytics into one Performance page | Design Required | New page. Spec is the story's sub-step 1 (RISK-04); brief fixed here (Product Owner). | `docs/design/2026-11-11__release-v9.17/performance-page-brief/decision_record.md` (new) | `pages/performance.md` v1.0 — written and approved in the sprint before the build (addendum) | ✅ Cleared (build gated in-story on spec approval) | Head of UX & Design + Product Owner |
| ST-07 (BLG-FE-263) | Use tabs or sections on the long single-scroll pages | Design Required | New navigation component; motion (jump) behaviour fixed as instant. Index over tabs (Product Owner). | `docs/design/2026-11-11__release-v9.17/long-page-section-index/decision_record.md` (new) | `pages/trade_plan.md` v1.24 → v1.25 (§5g); `pages/strategy_benchmark.md` v0.9 → v0.10 (§3a) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-08 (BLG-FE-265) | Move the remaining pages onto the semantic colour tokens | Design Pre-Approved | Applies existing tokens and measured pairs; no new colour | `docs/design/2026-11-06__release-v9.16/semantic-colour-tokens/decision_record.md` | `design_system.md` v1.26 (locked: §Semantic Colour Tokens, §Light-Theme Colour Tokens) | ✅ Cleared | Head of UX & Design |
| ST-09 (BLG-BE-205) | Record when the nightly job last moved each position's stop | Design Not Applicable | Migration, nightly job and contract; dead-branch removal with no visible change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 (BLG-FE-254 remainder) | Today list "Stops moved" group: TL-09 and TL-10 | Design Pre-Approved | Builds the approved group | `site-structure-phase1` §2.2 (brief, v9.15) | `pages/dashboard.md` v4.1 §1B (locked: TL-09, TL-10; v4.2 changes Card 3 only) | ✅ Cleared | Head of UX & Design |
| ST-11 (BLG-BE-211) | Move a linked trade plan to `closed` when its position closes | Design Pre-Approved | Backend; the visible effect is the existing "Closed" badge | N/A | `pages/trade_plan.md` §9 (locked reference) | ✅ Cleared | Head of UX & Design |
| ST-12 (BLG-FE-278) | Reset the Trade Plan pre-entry acknowledgement when the check result changes | Design Required | Changed interaction flow and new note line | `docs/design/2026-11-11__release-v9.17/trade-plan-found-defects/decision_record.md` §2 (new) | `pages/trade_plan.md` v1.25 (§5e) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-13 (BLG-FE-281) | Pass the market from Research View's "Create Trade Plan" | Design Required | Route parameter; spec named a stale route | `trade-plan-found-defects` §3 | `pages/research_view.md` v1.4 → v1.5 (§4.7) | ✅ Cleared | Head of UX & Design |
| ST-14 (BLG-FE-282) | Pre-fill the Trade Plan stop from §5 and flag a typed stop that differs | Design Required | New data displayed (stored-stop line); pre-fill rule | `trade-plan-found-defects` §4 | `pages/trade_plan.md` v1.25 (§5a.3, §5f) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-15 (BLG-OPS-217) | Find out why most on-demand Yahoo calls fail on production | Design Not Applicable | Production diagnosis and backend fixes | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-16 (BLG-OPS-195) | Alert when weekly market-data call volume exceeds 2× the baseline | Design Not Applicable | Scheduled workflow and Telegram message | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-17 (BLG-BE-178) | Batch signal sizing within available cash after fees | Design Not Applicable | Backend sizing | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-18 (BLG-GOV-419) | §1.3a gate clearance may set a gate-worded Provisional-Target to TBD | Design Not Applicable | Governance prompt | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-19 (BLG-SPEC-202) | Define or remove the 2R Exit Zone threshold | Design Required | Tooltip wording (wording-only, FI-P3-02). Both wordings fixed; strategy owner chooses (RISK-05). | `positions-decision-first` §7 | `pages/positions.md` v2.25 (§Position Lifecycle State Badge tooltip rows) | ✅ Cleared | Head of UX & Design |
| ST-20 (BLG-QA-223) | Stop check_data_model_drift.py reading rollback-only index names | Design Not Applicable | Tooling | N/A | N/A | ✅ Cleared | Head of UX & Design |

## §13 Boundary Pre-Check

**No flags.** No item introduces or extends a call to an AI provider. The AI endpoint security checklist is not triggered.

- **ST-01 to ST-04:** display-only. The urgency tiers apply existing deterministic §7/§8 tests and an existing display band. "Action needed" reuses copy already on the page and in the Today list (`dashboard.md` §1B, which carries its own §13 constraint). Nothing submits an exit.
- **ST-07:** the Trade Plan Thesis section moves into an indexed section with its existing AI controls unchanged (`trade_plan.md` §5b; covered by the existing review). No call is added.
- **ST-12 and ST-14:** restore the advisory acknowledgement flow (`strategy_rules.md` §4.2.1, §4.2.6) and state the deterministic §5 stop. Advisory, editable, no gate.
- **ST-19:** wording. If the owner chooses the §11 write, it is a case (c) `strategy_rules.md` change already listed in the slice; it is not a §13 matter.

## Blocked Items

None.

## Notes

### Post-gate-correction addendum

`claude/cycles/2026-11-11__release-v9.17/stage4_backlog_slice_addendum.md` was created with 5 entries. Sprint Planning and Sprint Execution must read it with the sealed slice. No entry changes scope.

- **ST-01:** near stop is the ≤ 5% band (Product Owner).
- **ST-03/ST-04:** the strip's grace entry expands to `GracePeriodView`, which lists every in-grace position with no dismiss (Product Owner).
- **ST-06:** the build waits for the Head of UX & Design's approval of `performance.md`; the brief covers `BLG-FE-237`.
- **ST-07:** a section index, not tabs (Product Owner).
- **ST-14:** the pre-fill uses the Signal Context panel's suggested-stop value.

### Artefacts produced and specs updated

- **Design artefacts produced this run:** 4 decision records under `docs/design/2026-11-11__release-v9.17/`:
  - `positions-decision-first` (ST-01, ST-02, ST-03, ST-04, ST-19)
  - `performance-page-brief` (ST-06)
  - `long-page-section-index` (ST-07; reused by ST-06)
  - `trade-plan-found-defects` (ST-12, ST-13, ST-14)
- **Frontend specs updated (6 files):** each is logged in `prompt_change_log.md`.
  - `pages/positions.md` 2.24→2.25
  - `pages/dashboard.md` 4.1→4.2
  - `pages/risk_dashboard.md` 0.1.15→0.1.16
  - `pages/trade_plan.md` 1.24→1.25
  - `pages/strategy_benchmark.md` 0.9→0.10
  - `pages/research_view.md` 1.4→1.5

### Decisions still open before the seal (not design-gate items)

- **RISK-05:** the Strategy Rules & System Intent Owner chooses ST-12's storage option (record §2.2) and ST-19's wording row (record §7), dated, in `sprint_backlog.md`'s sign-off summary. The implementing story deletes the unused option from `trade_plan.md` §5e and the unused tooltip row from `positions.md`.
- **RISK-02:** Sprint Planning confirms ST-08's boundary.

### Obligations passed to Sprint Execution (outside this gate's write scope)

- **ST-04:** remove `grace_alert_dismissed_*` reads; update `docs/specs/frontend/pages/positions.md` §Grace Period Alert Zone to a "Superseded" stub when it merges.
- **ST-06:** create `performance.md`, retire `reports.md` and the Performance Analytics part of `analytics.md`, and revise `navigation.md`, the command palette and `glossary.md` §UI Labels. Merge after ST-05 (RISK-04).
- **ST-08:** runs after every other UI EPIC; the new components here (`PositionsWarningStrip`, `GracePeriodView`, `SectionIndex`, decision cards) are specified with `app-*` tokens, so they add nothing to the sweep.
- **ST-12:** record whether the change meets `BLG-FE-269` AC 1 (RISK-07).

### Observations for filing (outside this gate's write scope; `/backlog-add` at Sprint Planning)

- `positions.md` names two different default views: §Table View is headed "(default)" and §Responsive Behavior marks Grid "(default)". The shipped default should be checked and one heading corrected. Spec debt.
- `dashboard.md`'s Morning Briefing table still names "Positions to Act On"; the shipped card is "Positions to Watch" (noted in v4.0, not yet filed).
