**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-11-03
**Cycle:** 2026-11-03__release-v9.15

# Design Gate Record — 2026-11-03__release-v9.15

## Gate Status: PASSED

Completed: 2026-11-03
PMO Lead: confirmed
Head of UX & Design: confirmed (agent-mediated, Design Gate Engine)
Product Owner: confirmed (the user, in session, 2026-11-03)

All 45 items are classified. 41 are cleared. 4 are conditionally cleared (ST-08, ST-09, ST-10, ST-11): their design work is itself the sprint deliverable or depends on one, as the release plan sets out (RISK-02). None is blocked.

| Classification | Count | Items |
|----------------|-------|-------|
| Design Required | 14 | ST-01, ST-02, ST-03, ST-06, ST-07, ST-08, ST-09, ST-10, ST-11, ST-12, ST-13, ST-14, ST-17, ST-18 |
| Design Pre-Approved | 5 | ST-04, ST-15, ST-16, ST-21, ST-23 |
| Design Not Applicable | 26 | the remaining items |

**Classification notes:**
- **The three spec stories, ST-08, ST-09 and ST-10, are conditionally cleared.** Each one's deliverable is the design: navigation v2 and the glossary's UI labels, the Dashboard "Today" list, and the Journal area. Each is sized at 2 days, and its ACs already name the Head of UX & Design as approver (RISK-02). This gate approved a brief with fixed review criteria (`site-structure-phase1` §2), including a §13 constraint on ST-09's "qualifying entries". It did not write the specs ahead of the stories. The specs are approved inside the sprint. A spec not approved by close returns with a reason, and its dependants stay not-ready. This follows the v8.9 ST-06 conditional-clearance precedent.
- **ST-11 is conditionally cleared on ST-08's approval.** It applies ST-08's labels. Its rule (one label source for sidebar, heading, palette and tab title) is fixed here (`site-structure-phase1` §3.1).
- **ST-12, ST-13 and ST-14 are fully designed here.** Their sections go into `navigation.md` v1.8, and ST-08's v2.0 keeps them.
- **ST-01 depends on a ruling inside the sprint.** The slice's AC 2 ("save requires the acknowledgement") reads against `strategy_rules.md` §4.2.6. Both branches are designed, and the ruling is ST-01's first sub-step (addendum). This follows the v9.14 ST-03 precedent. The user, as Strategy Rules & System Intent Owner, chose on 2026-11-03 to leave the ruling to the sprint.
- **ST-02 and ST-03 share one decision record, as do ST-06 and ST-17.** Each pair edits the same field or modal.
- **ST-03, ST-06's footnote, ST-07's label and ST-17's tooltip are wording only.** The FI-P3-02 code-review exception applies to those ACs. Their other ACs (ST-06's value, ST-07's reason line, ST-17's heading) keep Playwright or unit-test coverage.
- **Pre-Approved items:**
  - **ST-04:** the three date fields already specify "Default: today". The fix makes "today" the user's local date. There is no layout or copy change.
  - **ST-15:** a win test corrected to `metrics_definitions.md` §Win Rate. The displayed field is unchanged.
  - **ST-16:** a value correction on existing widgets. See the addendum: those widgets exist only on the legacy page ST-12 deletes.
  - **ST-21:** shows the fallback that `reports.md` §AI Summary already specifies (`source: "fallback"` row).
  - **ST-23:** if the ruling changes code, the displayed P&L stays in the same fields with no layout change. Any tooltip or label that states the P&L's FX basis or fee treatment must state the ruled basis. A new display element would need its own design pass.
- **ST-05** normalises the ticker for the ATR preview and for save. There is no visible change.

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 (BLG-FE-244) | Show the pre-entry checks on every route into Trade Entry | Design Required | New panel and interaction flow on Trade Entry. The acknowledgement branch is pending a ruling, and both branches are designed. | `docs/design/2026-11-03__release-v9.15/trade-entry-pre-entry-checks/decision_record.md` (new) | `components/position_form.md` v1.11 → v1.12 (§Pre-Entry Checks, §Form Field Order, §Validation Errors) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-02 (BLG-FE-245) | Pre-fill Trade Entry's FX rate from the live rate | Design Required | New data displayed: the rate's source and age next to the field | `docs/design/2026-11-03__release-v9.15/trade-entry-fx-rate/decision_record.md` (new, shared with ST-03) | `components/position_form.md` v1.12 (§FX Rate) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-03 (BLG-FE-246) | Label the FX rate the same way on entry and exit | Design Required | Copy change on three inputs. Wording only (FI-P3-02). | `docs/design/2026-11-03__release-v9.15/trade-entry-fx-rate/decision_record.md` (shared with ST-02) | `components/position_form.md` v1.12; `components/exit_modal.md` v1.1 → v1.2; `pages/trade_plan.md` v1.20 → v1.21 (§5d.2) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-04 (BLG-FE-243) | Default trade, exit and cash dates to the user's local date | Design Pre-Approved | The specs already say "Default: today". This is a correctness fix with no visible design change. | N/A | `components/position_form.md` v1.12 §Entry Date; `components/exit_modal.md` v1.2; `components/cash_management_modal.md` v1.3 (locked references) | ✅ Cleared | Head of UX & Design |
| ST-05 (BLG-FE-222) | Normalise the Trade Entry ticker the same way for the ATR preview and for save | Design Not Applicable | Normalisation and tests. No visible change. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-06 (BLG-BE-173) | Trail Stop modal's ATR trail value uses a hardcoded multiplier and no breakeven floor | Design Required | Corrected displayed value and new footnote copy | `docs/design/2026-11-03__release-v9.15/trail-stop-modal-wording/decision_record.md` (new, shared with ST-17) | `pages/positions.md` v2.21 → v2.22 (§Trail Stop Action) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-07 (BLG-FE-219) | Label signal cost as including fees, and make the zero-ATR sizing reason plain English | Design Required | Copy change on the signal card and in the backend reason | `docs/design/2026-11-03__release-v9.15/signal-card-cost-and-sizing-reason/decision_record.md` (new) | `pages/signals.md` v0.7 → v0.8 (§Signal Card Cost and Sizing Reason) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-08 (BLG-SPEC-214) | Navigation spec v2 and a UI-label section in the glossary | Design Required | The story's deliverable is the navigation design. Approved in the sprint by the Head of UX & Design (AC 1, RISK-02). | Brief: `docs/design/2026-11-03__release-v9.15/site-structure-phase1/decision_record.md` §2.1 (new) | `pages/navigation.md` v1.8 (gate) → v2.0 and `docs/reference/glossary.md` UI-label section (in-sprint) | ⚠️ Conditionally Cleared | Head of UX & Design + Product Owner |
| ST-09 (BLG-SPEC-215) | Dashboard spec: a prioritised "Today" action list | Design Required | The story's deliverable is the home-page design. Approved in the sprint (AC 1, RISK-02). §13 constraint in the brief. | Brief: `site-structure-phase1` §2.2 | `pages/dashboard.md` v3.11 (gate) → revised in-sprint (Class 1, Head of Specs Team) | ⚠️ Conditionally Cleared | Head of UX & Design + Product Owner |
| ST-10 (BLG-SPEC-216) | Spec for one Journal area | Design Required | The story's deliverable is the Journal area design. Approved in the sprint (AC 1). Its §13 confirmation is AC 2. | Brief: `site-structure-phase1` §2.3 | New Journal area spec (in-sprint) | ⚠️ Conditionally Cleared | Head of UX & Design + Product Owner |
| ST-11 (BLG-FE-248) | Use one name per page and action | Design Required | Changed labels across sidebar, headings and palette. The labels come from ST-08. | `site-structure-phase1` §3.1 (rule and dependency) | `docs/reference/glossary.md` UI-label section (ST-08, in-sprint) | ⚠️ Conditionally Cleared (on ST-08 approval) | Head of UX & Design + Product Owner |
| ST-12 (BLG-FE-247) | Remove the legacy widget Dashboard route and its duplicate palette entry | Design Required | Changed navigation: a route removed and redirected, a palette entry removed | `site-structure-phase1` §3.3 | `pages/navigation.md` v1.7 → v1.8 (§Legacy Dashboard Route) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-13 (BLG-FE-249) | Set a browser-tab title for each page | Design Required | New visible text (tab titles) | `site-structure-phase1` §3.2 | `pages/navigation.md` v1.8 (§Browser Tab Title) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-14 (BLG-FE-266) | Fix three small chrome defects | Design Required | New data displayed (the real version) and a layout fix | `site-structure-phase1` §3.4 | `pages/navigation.md` v1.8 (§Sidebar Footer and Height); `pages/dashboard.md` v3.10 → v3.11 (§6A) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-15 (BLG-FE-239) | Trade History counts a break-even trade as a win | Design Pre-Approved | Win test corrected to `metrics_definitions.md` §Win Rate. The display is unchanged. | N/A | `pages/trade_history.md` v1.16 (locked reference — summary "Win rate (%)") | ✅ Cleared | Head of UX & Design |
| ST-16 (BLG-FE-240) | Dashboard win-rate widgets are fed from open positions only | Design Pre-Approved | Data-source correction on existing widgets. They exist only on the legacy page (addendum). | N/A | None. The legacy `Dashboard.js` has no page spec. Value per `metrics_definitions.md` §Win Rate. | ✅ Cleared | Head of UX & Design |
| ST-17 (BLG-FE-218) | Align the View Trail modal wording with the read-only ruling | Design Required | Copy change on the heading, a row label and a tooltip | `docs/design/2026-11-03__release-v9.15/trail-stop-modal-wording/decision_record.md` (shared with ST-06) | `pages/positions.md` v2.22 (§Trail Stop Action) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-18 (BLG-FE-220) | Fix the Rebalance badge's contrast and settle tinted vs filled badges | Design Required | Colour change and a style ruling (filled) | `docs/design/2026-11-03__release-v9.15/exit-reason-badges/decision_record.md` (new) | `pages/strategy_benchmark.md` v0.8 → v0.9 (§7.3) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-19 (BLG-BE-170) | Price-alert duplicate fallback returns 500 at more than 4 dp | Design Not Applicable | Backend | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-20 (BLG-BE-171) | Use the deploy date as strategy v1.15's effective date | Design Not Applicable | Registry data | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-21 (BLG-BE-172) | Show the code-written fallback when the monthly P&L summary's regeneration fails | Design Pre-Approved | The fallback display is already specified. The backend now returns it in one more case. | N/A | `pages/reports.md` v0.26 (locked reference — §AI Summary, Fallback row) | ✅ Cleared | Head of UX & Design |
| ST-22 (BLG-BE-174) | Gap-risk weekend statistic: exchange calendar and ordinary weekends | Design Not Applicable | Backend statistic. The display is unchanged. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-23 (BLG-SPEC-198) | Open-position pnl: FX basis and fee treatment | Design Pre-Approved | A decision first. A code change keeps the same fields, and any basis wording follows the ruling (Classification notes). | N/A | `pages/positions.md` v2.22 (locked reference) | ✅ Cleared | Head of UX & Design |
| ST-24 (BLG-AI-23) | Review logged briefing ticker-caveat tokens | Design Not Applicable | Output filter | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-25 (BLG-AI-24) | Journal summary advisory check: false positives and misses | Design Not Applicable | Output check | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-26 (BLG-AI-25) | Chat stop-time focus rule: ignore upper-case non-ticker words | Design Not Applicable | Validator attribution | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-27 (BLG-AI-26) | Journal summary advisory check: do not flag "could/may help explain" | Design Not Applicable | Output check | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-28 (BLG-GOV-194) | §13 boundary language clarity pass — AI journal summarisation | Design Not Applicable | Governance decision | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-29 (BLG-OPS-48) | ANTHROPIC_API_KEY 6-month scope audit | Design Not Applicable | Security audit | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-30 (BLG-OPS-190) | Rebalance-exit generation checks today's screener run | Design Not Applicable | Backend precondition | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-31 (BLG-OPS-191) | Skip the code-test workflows on governance-only and docs-only pushes | Design Not Applicable | CI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-32 (BLG-OPS-192) | Tell "no qualifying tickers" apart from "momentum run missing" | Design Not Applicable | Backend job | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-33 (BLG-OPS-197) | Record the weekly market-data call-volume baseline | Design Not Applicable | Ops documentation (conditional story) | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-34 (BLG-SPEC-194) | Clear the 8 success-example drifts | Design Not Applicable | Contract text | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-35 (BLG-SPEC-196) | Re-apply NOT NULL on positions.portfolio_id and total_cost | Design Not Applicable | Database migration | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-36 (BLG-SPEC-197) | Apply DS-17's open-position unique index to staging | Design Not Applicable | Database index | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-37 (BLG-GOV-404) | Gate scan treats a shipped roadmap feature ID as a met gate | Design Not Applicable | Governance tooling | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-38 (BLG-QA-240) | Execution-state consistency check counts uninitialised EPICs | Design Not Applicable | Governance tooling | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-39 (BLG-QA-220) | Behavioural tests for live holding days | Design Not Applicable | Tests only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-40 (BLG-QA-221) | Real-Postgres tests for the ai_audit_log and claude_audit_log paths | Design Not Applicable | Tests only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-41 (BLG-QA-222) | Extend the utils.* leak guard | Design Not Applicable | Tests only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-42 (BLG-QA-224) | Make SC-TS-* Playwright scenario IDs unique | Design Not Applicable | Tests only. Coordinate the IDs with ST-17's assertion updates. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-43 (BLG-GOV-193) | Escalation SLA breach dry-run test | Design Not Applicable | Governance test | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-44 (BLG-GOV-195) | Strategic exclusions review cadence | Design Not Applicable | Governance decision | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-45 (BLG-GOV-196) | Sunset review for Priority 3 — Deferred initiatives | Design Not Applicable | Product decision | N/A | N/A | ✅ Cleared | Head of UX & Design |

## §13 Boundary Pre-Check

**No flags.** No item introduces a new AI-calling endpoint or a new AI feature. Each AI-adjacent item narrows, checks, re-reads or audits an existing call that is already covered:

- **ST-24 and ST-26:** daily briefing and chat output filters. Covered by `decisions--2026-06-24__release-v6.2--BLG-FEAT-50-51-section13-review.md` (PASS).
- **ST-25 and ST-27:** journal summary advisory check. Covered by `SRB-v1.7-2026-03-02__release-v1.7.md` and `decisions--2026-04-17__release-v2.8.md` (BLG-FEAT-16). ST-25's ruling is a `delegated_decision` first sub-step (RISK-07).
- **ST-21:** monthly P&L narrative failure path. Covered by `decisions--2026-10-08__release-v9.11--ST-25-monthly-pnl-narrative-section13-review.md` (CONDITIONAL). It makes no new call and returns the existing code-written fallback.
- **ST-28:** is itself a dated §13 re-read of the journal summary. Its slice ACs cite §13.1, §13.2 and the §13.5 roster.
- **ST-10:** the Journal area spec. Its §13 confirmation is AC 2, which cites §13.1 and §13.2 and checks the §13.5 roster if the area surfaces AI journal summaries.
- **ST-29:** audits the existing key's scope. It makes no call.
- **ST-01:** not an AI item. It shows the existing §4.2 deterministic checks on one more route (SI-01 §13 review, `decisions--2026-05-19__release-v3.8--SI-01-section13-review.md`; §13.4). The one §13-relevant question, whether a required acknowledgement is a "hard submission gate" under §4.2.6, is held for the in-sprint ruling (addendum).
- **ST-09:** not an AI item. Its brief bars any new ranking or "do this" wording in the Today list without its own §13 confirmation.

The AI endpoint security checklist is not triggered: no new AI-calling endpoint.

## Blocked Items

None.

## Notes

### Post-gate-correction addendum

`claude/cycles/2026-11-03__release-v9.15/stage4_backlog_slice_addendum.md` was created with 2 entries. Sprint Planning and Sprint Execution must read it together with the sealed slice. Neither entry changes scope.

- **ST-01:** the acknowledgement ruling against `strategy_rules.md` §4.2.6 is the story's first sub-step. Branch A may need a case (c) `strategy_rules.md` write confirmed at the seal, like RISK-03.
- **ST-16:** both win-rate widgets exist only on the legacy `Dashboard.js` that ST-12 deletes. `DashboardHome` has none. **The Product Owner decides at Sprint Planning** whether to keep ST-16 as sliced, defer or close it as superseded by ST-12, or route a home-page win rate into ST-09's spec.

### Artefacts produced and specs updated

- **Design artefacts produced this run:** 6 decision records under `docs/design/2026-11-03__release-v9.15/`:
  - `trade-entry-pre-entry-checks` (ST-01)
  - `trade-entry-fx-rate` (ST-02, ST-03)
  - `trail-stop-modal-wording` (ST-06, ST-17)
  - `signal-card-cost-and-sizing-reason` (ST-07)
  - `exit-reason-badges` (ST-18)
  - `site-structure-phase1` (ST-08 to ST-14: briefs for the three spec stories, designs for ST-12 to ST-14, and ST-11's rule)
- **Frontend specs updated (8 files):** each is logged in `prompt_change_log.md`.
  - `components/position_form.md` 1.11→1.12
  - `components/exit_modal.md` 1.1→1.2
  - `pages/trade_plan.md` 1.20→1.21
  - `pages/positions.md` 2.21→2.22
  - `pages/signals.md` 0.7→0.8
  - `pages/strategy_benchmark.md` 0.8→0.9
  - `pages/navigation.md` 1.7→1.8
  - `pages/dashboard.md` 3.10→3.11
- **Spec corrections found while updating:** `strategy_benchmark.md` §7.3 listed tinted Stop and Rebalance badges and an "Other — Slate default" badge, none of which shipped. The rows now record the shipped filled badges and the plain-text fallback. `navigation.md` §Group Structure has drifted again (it omits Replay, and lists "Trade Reflection" where the sidebar shows "Reflections"). v1.8 notes the drift, and ST-08's v2.0 replaces the table.

### Obligations passed to Sprint Execution (outside this gate's write scope)

- **API changes, each with its contract and `openapi.yaml` in the same commit:**
  - ST-01: `POST /portfolio/position` gains an optional `pre_entry_override_acknowledged`. When it is true, the backend writes a `pre_entry_override` red-flag event with `source: "trade_entry"`.
  - ST-06: `position_endpoints.md`'s stop-trail description states the §7.2 profit formula with the breakeven floor. The response shape is unchanged.
  - ST-07: `signal_endpoints.md` lists the two new zero-ATR `reason` strings.

  No new route is designed at this gate, so the `routers/test.py` / `SystemStatus.js` count / `SC-SS-01b` chain does not apply. ST-12 removes a frontend route only.
- **ST-02:** both `"1.27"` literals leave `TradeEntry.js`, and no other client constant replaces them. The rate comes from `GET /market/status`.
- **ST-17 and ST-42:** both touch SC-TS-* Playwright scenarios. Agree the renamed IDs before either merges (RISK-04).
- **ST-18:** SC-SB-04a's `bg-teal-600` assertion (`tests/e2e/strategy-benchmark.spec.js:282`) becomes `bg-teal-700`.

### Observations for filing (outside this gate's write scope; `/backlog-add` at Sprint Planning)

- `signals.md` §Signal Type Badge Styling specifies `#0891B2` (cyan-600) with white text for "Rebalance Exit", which measures 3.68:1, below WCAG AA. Check the shipped badge against it.
- The sidebar footer's "Docs" link (`src/Layout.js`, next to the version label ST-14 changes) has `href="#"` and goes nowhere.
