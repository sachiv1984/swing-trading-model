**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-11-06
**Cycle:** 2026-11-06__release-v9.16

# Design Gate Record — 2026-11-06__release-v9.16

## Gate Status: PASSED

Completed: 2026-11-06
PMO Lead: confirmed
Head of UX & Design: confirmed (agent-mediated, Design Gate Engine)
Product Owner: confirmed (the user, in session, 2026-11-06). The Product Owner decided ST-04's target and ST-05's age, and approved the ST-07–ST-10 design directions.

All 30 items are classified and cleared. None is blocked or conditionally cleared.

| Classification | Count | Items |
|----------------|-------|-------|
| Design Required | 6 | ST-04, ST-05, ST-07, ST-08, ST-09, ST-10 |
| Design Pre-Approved | 5 | ST-01, ST-02, ST-03, ST-06, ST-12 |
| Design Not Applicable | 19 | ST-11, ST-13 to ST-30 |

**Classification notes:**
- **Phase 2's specs were approved last cycle.** The four EPIC-01 stories and ST-06 build specs approved in the v9.15 sprint (`navigation.md` v2.0, 2026-11-04; `dashboard.md` v4.0, 2026-11-05). Neither file has changed since (git log). Each is the locked reference for its stories, which makes them Design Pre-Approved under §6 ("frontend spec already updated in a prior cycle and confirmed unchanged"). ST-04 is the exception: its slice target, a pre-entry section on the Risk Dashboard, does not exist, so it was designed here.
- **ST-04 is designed as a motion change.** Scroll-to-section is a motion and timing interaction (§6 motion rule). The record fixes when it scrolls, smooth versus instant under reduced motion, focus, and the unknown-id fallback.
- **ST-05 found a gap in the code.** `TradePlan.js` never writes the snapshot that Trade Entry reads. The design has the plan form write a dated snapshot, and the 24-hour age is the Product Owner's choice (addendum).
- **ST-07 and ST-08 share one record**, as do ST-09 and ST-10. Each pair edits the same form or the same colour system.
- **ST-09 introduces no new colours.** Its eight `app-*` tokens reuse the v1.23 pairs whose contrast is already measured.
- **ST-12 is Pre-Approved.** The Trade Plan AI controls must look and behave as they do now in production (`trade_plan.md` §5b). See the addendum for local and CI builds.
- **Not Applicable, but visible:** ST-26 is test-only, ST-27 is a design document (`docs/ux/`) and ST-29 is a governance report. None changes the UI.

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 (BLG-FE-250) | Build the job-based sidebar and surface Trade Plans and Research | Design Pre-Approved | Builds the approved navigation v2. The spec is unchanged since 2026-11-04. | `docs/design/2026-11-03__release-v9.15/site-structure-phase1/decision_record.md` §2.1 (brief) | `pages/navigation.md` v2.0 (locked: §Areas, §Page Placement, §Default Expansion, §Area Header, §Active Item, §Alert Badge Integration, §Responsive Behaviour) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-02 (BLG-FE-251) | Add a parent link on detail pages | Design Pre-Approved | As ST-01 | as ST-01 | `pages/navigation.md` v2.0 (locked: §Parent Links) | ✅ Cleared | Head of UX & Design |
| ST-03 (BLG-FE-252) | Give each dead-end page an onward next-step link | Design Pre-Approved | As ST-01. The scan found 11 dead ends, not 8 (addendum). | as ST-01 | `pages/navigation.md` v2.0 (locked: §Onward Links) | ✅ Cleared | Head of UX & Design |
| ST-04 (BLG-FE-253) | Anchor the digest's Risk Dashboard link to the right section | Design Required | New interaction with motion (scroll-to-section). The slice's target section does not exist, so the anchor goes on Analytics §19 (Product Owner). | `docs/design/2026-11-06__release-v9.16/digest-section-link/decision_record.md` (new) | `pages/analytics.md` v2.2 → v2.3 (§19.1 Section Link) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-05 (BLG-FE-271) | Require the acknowledgement on plan-linked Trade Entry when the plan's checks were WARN/FAIL | Design Required | Changed interaction flow on Trade Entry (panel re-shown, reason line). The plan form now writes a dated snapshot. | `docs/design/2026-11-06__release-v9.16/plan-linked-pre-entry-checks/decision_record.md` (new) | `components/position_form.md` v1.13 → v1.14 (§Pre-Entry Checks); `pages/trade_plan.md` v1.21 → v1.22 (§5e) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-06 (BLG-FE-254) | Build the "Today" action list on the Dashboard | Design Pre-Approved | Builds the approved Today list, including its §13 constraints and its Stops moved data dependency | `site-structure-phase1` §2.2 (brief) | `pages/dashboard.md` v4.0 (locked: §1B; TL-01 to TL-29) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-07 (BLG-FE-255) | Add "Plan this" to Signals and Screener rows | Design Required | New action on two pages, and new route parameters on Trade Plan | `docs/design/2026-11-06__release-v9.16/signal-to-plan-flow/decision_record.md` (new, shared with ST-08) | `pages/signals.md` v0.8 → v0.9; `pages/screener_results.md` v1.10 → v1.11 (§11.1); `pages/trade_plan.md` v1.22 (§2, §5a.1) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-08 (BLG-FE-256) | On Trade Plan, show the suggested size before asking for shares | Design Required | Changed field order, new data displayed, and a pre-fill rule | `signal-to-plan-flow` (shared with ST-07) | `pages/trade_plan.md` v1.22 (§5f) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-09 (BLG-FE-264) | Semantic colour tokens for the base, card and table shells | Design Required | Colour change across every page base, card and table | `docs/design/2026-11-06__release-v9.16/semantic-colour-tokens/decision_record.md` (new, shared with ST-10) | `design_system.md` v1.24 → v1.25 (§Semantic Colour Tokens) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-10 (BLG-FE-223) | Inputs apply dark:text-slate-400 to typed text instead of the placeholder | Design Required | Colour change on inputs | `semantic-colour-tokens` (shared with ST-09) | `design_system.md` v1.25 (§Input Text Colours) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-11 (BLG-OPS-214) | Rotate the Anthropic API key and revoke the old key | Design Not Applicable | Credential operations | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-12 (BLG-OPS-213) | Stop injecting REACT_APP_ANTHROPIC_API_KEY into the public Pages build | Design Pre-Approved | Build-time flag change. The AI controls must behave as they do now (addendum). | N/A | `pages/trade_plan.md` §5b (locked reference) | ✅ Cleared | Head of UX & Design |
| ST-13 (BLG-OPS-197) | Record the weekly market-data call-volume baseline | Design Not Applicable | Ops documentation (conditional story) | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-14 (BLG-OPS-198) | Record the screener run p50/p95 baseline | Design Not Applicable | Ops documentation (conditional story) | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-15 (BLG-OPS-199) | Fail the staging smoke host check with no Render service ID | Design Not Applicable | CI test | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-16 (BLG-BE-175) | US exit with a NULL fill_price fails in the P&L arithmetic | Design Not Applicable | Backend | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-17 (BLG-BE-176) | Lifecycle badge and Risk page disagree for a US row with no fill_price and no fx_rate | Design Not Applicable | Backend fallback. Both surfaces already render the values. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-18 (BLG-BE-177) | Frozen-stop marker not written without a live price | Design Not Applicable | Backend marker. The marker's display is already specified. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-19 (BLG-AI-27) | Read production briefing ticker-caveat tokens | Design Not Applicable | Output filter word list | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-20 (BLG-AI-28) | Handle `_NON_TICKER_WORDS` entries that are real tickers | Design Not Applicable | Output filter rule (`delegated_decision` first) | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-21 (BLG-SPEC-195) | Journal summary: stale AI_MODEL override line | Design Not Applicable | Contract text and cost rates | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-22 (BLG-SPEC-200) | Add the 11 missing positions columns to the data dictionary | Design Not Applicable | Data dictionary | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-23 (BLG-SPEC-201) | Point settings.md at the moved strategy constants module | Design Not Applicable | A path correction in a spec. No UI change. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-24 (BLG-QA-21) | Arc 2 end-to-end QA protocol | Design Not Applicable | QA document and tests | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-25 (BLG-QA-22) | Arc 2 DoQ standards review | Design Not Applicable | Governance review | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-26 (BLG-QA-23) | Trade plan lifecycle end-to-end test | Design Not Applicable | Test only. It must exercise ST-07/ST-08's flow as built. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-27 (BLG-FE-39) | Arc 2 user journey map | Design Not Applicable | A UX analysis document. It changes no UI. Any items it finds are filed, not built. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-28 (BLG-GOV-413) | Split-achievability carve-out | Design Not Applicable | Governance prompt | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-29 (BLG-GOV-26) | Arc velocity tracking dashboard | Design Not Applicable | A governance report, not an app page | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-30 (BLG-GOV-198) | Base44 prompt versioning convention | Design Not Applicable | Governance convention (`delegated_decision` first) | N/A | N/A | ✅ Cleared | Head of UX & Design |

## §13 Boundary Pre-Check

**No flags.** No item introduces a new AI-calling endpoint or a new AI feature. Each AI-adjacent item narrows, re-reads or re-keys an existing call that a §13 review already covers:

- **ST-19 and ST-20:** daily briefing and chat ticker-caveat filters. Covered by `docs/product/decisions/decisions--2026-06-24__release-v6.2--BLG-FEAT-50-51-section13-review.md` (PASS). ST-20's collision ruling is a `delegated_decision` first sub-step.
- **ST-21:** journal summary model and cost text. Covered by `SRB-v1.7-2026-03-02__release-v1.7.md`, `decisions--2026-04-17__release-v2.8.md` (BLG-FEAT-16) and the v9.15 re-read `decisions--2026-11-03__release-v9.15--ST-28-journal-summary-section13-reread.md`. It adds no call.
- **ST-11 and ST-12:** key rotation and a build flag. No call is added or changed.
- **ST-05:** not an AI item. It applies the existing §4.2 deterministic checks on the plan-linked route (SI-01 §13 review; §13.4). The acknowledgement is not a hard gate (§4.2.6 v1.23).
- **ST-06:** not an AI item. `dashboard.md` v4.0 §Strategy constraints (§13) bars ranking and "do this" wording, and ST-06 builds to it.
- **ST-07 and ST-08:** not AI items. "Plan this" only navigates to an unsaved form. The suggested size is the deterministic §4.1 calculation, advisory and editable, as in `trade_plan.md` §10.6a.

The AI endpoint security checklist is not triggered, because no new AI-calling endpoint is introduced.

## Blocked Items

None.

## Notes

### Post-gate-correction addendum

`claude/cycles/2026-11-06__release-v9.16/stage4_backlog_slice_addendum.md` was created with 5 entries. Sprint Planning and Sprint Execution must read it with the sealed slice. No entry changes scope.

- **ST-03:** the scan covers 11 dead-end pages, not 8. The AC already requires 0.
- **ST-04:** the anchor is on Analytics §19, and the digest gains a third link (Product Owner).
- **ST-05:** the plan form must start writing a dated snapshot, and the age is 24 hours (Product Owner).
- **ST-07:** "Plan this" passes `signal_id`, and Signal Context accepts it.
- **ST-12:** "behave as before" is measured against the production Pages build.

### Artefacts produced and specs updated

- **Design artefacts produced this run:** 4 decision records under `docs/design/2026-11-06__release-v9.16/`:
  - `digest-section-link` (ST-04)
  - `plan-linked-pre-entry-checks` (ST-05)
  - `signal-to-plan-flow` (ST-07, ST-08)
  - `semantic-colour-tokens` (ST-09, ST-10)
- **Frontend specs updated (6 files):** each is logged in `prompt_change_log.md`.
  - `components/position_form.md` 1.13→1.14
  - `pages/trade_plan.md` 1.21→1.22
  - `pages/signals.md` 0.8→0.9
  - `pages/screener_results.md` 1.10→1.11
  - `pages/analytics.md` 2.2→2.3
  - `design_system.md` 1.24→1.25
- **Write scope:** `components/position_form.md` and `design_system.md` sit outside `docs/specs/frontend/pages/`. They were updated here on the v9.15 gate's precedent (`position_form.md` 1.11→1.12, `exit_modal.md`), so that STEP 3's hard rule (spec updated before Sprint Planning) holds for ST-05, ST-09 and ST-10.

### Obligations passed to Sprint Execution (outside this gate's write scope)

- **ST-04:** update `si05_digest_service.py` `_format_deep_links()` and its test. Mark journey map F-04 resolved in `docs/ux/si05_user_journey_map.md`.
- **ST-05:** add a pointer from §2.1 of the v9.15 `trade-entry-pre-entry-checks/decision_record.md` to this cycle's record. This is in the story's scope.
- **ST-07:** add Signals → Trade Plan and Screener → Trade Plan rows to `navigation.md` §Onward Links, with ST-03 in the same sprint.
- **ST-09:** regenerate the visual baselines for both themes after EPIC-01 and EPIC-02 merge (RISK-03).

### Observations for filing (outside this gate's write scope; `/backlog-add` at Sprint Planning)

- `trade_plan.md` §5d.4 says `trade_plans` has no entry-price column. `planned_entry_price` and `planned_quantity` are persisted (`TradePlan.js:578–579`), and §5.1's field table lists neither. This is spec debt.
- `trade_plan.md` §2 lists `/trade-plans/...` routes. The live routes are `/TradePlans` and `/TradePlan?…` (`navigation.md` v2.0). This is spec debt. The v1.22 row added here names the live route.
