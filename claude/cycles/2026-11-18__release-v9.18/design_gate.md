**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-11-18
**Cycle:** 2026-11-18__release-v9.18

# Design Gate Record — 2026-11-18__release-v9.18

## Gate Status: PASSED

Completed: 2026-11-18
PMO Lead: confirmed
Head of UX & Design: confirmed (agent-mediated, Design Gate Engine)
Product Owner: confirmed (the user, in session, 2026-11-18). The Product Owner made four decisions:
- **ST-12:** "Position size checks" from the cash, sector and sizing checks, because the strategy rules set no heat limit.
- **ST-30:** option (a), compute live.
- **ST-11:** add "Plan this".
- **ST-16:** add `red_flags_7d` to the digest.

All 40 items are classified and cleared. ST-07 is cleared with its `design_system.md` half delivered in-story. None is blocked.

| Classification | Count | Items |
|----------------|-------|-------|
| Design Required | 16 | ST-03, ST-04, ST-07, ST-08, ST-09, ST-10, ST-11, ST-12, ST-13, ST-14, ST-15, ST-16, ST-17, ST-27, ST-30, ST-33 |
| Design Pre-Approved | 3 | ST-01, ST-02, ST-31 |
| Design Not Applicable | 21 | ST-05, ST-06, ST-18, ST-19, ST-20, ST-21, ST-22, ST-23, ST-24, ST-25, ST-26, ST-28, ST-29, ST-32, ST-34, ST-35, ST-36, ST-37, ST-38, ST-39, ST-40 |

**Classification notes:**
- **ST-01 and ST-02 are Pre-Approved.** They bring four controls and the Exit dialog up to standards already in `design_system.md` v1.27: §Accessibility "Full keyboard navigation", the shared `Dialog` convention (focus trap, focus return, Escape = Cancel) and the focus-indicator contrast rule. Nothing visible changes. Each control keeps its look. The heatmap month detail uses the shared `Dialog`. The Monitor row selection exposes `role="checkbox"`/`aria-checked` (or a real checkbox styled as today).
- **ST-31 is Pre-Approved.** Its idle, loading, ready and none states, and its 300 ms debounce, are unchanged (`position_form.md` v1.14 §ATR preview). Caching only removes repeat fetches. No timing parameter changes, so the §6 motion/timing rule does not apply.
- **ST-07 is the spec story itself.** This gate wrote the `navigation.md` half, which ST-08 needs before Sprint Planning (addendum). ST-07 writes `design_system.md` §14.5, which is outside this gate's write scope.
- **ST-14 is Design Required for wording.** The label change is wording-only under FI-P3-02, but it shares a page and a record with ST-15–ST-17.
- **ST-26 is Not Applicable.** Replacing the hard-coded 1.27 FX rate with the live rate changes figures to their correct values. No layout, label or state changes.
- **Not Applicable, but touching UI code:** ST-20 (axe helper, tests only) and ST-06 (`web-vitals` reporting, console in development, no visible change).

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 (BLG-FE-311) | Make the four mouse-only controls keyboard-operable | Design Pre-Approved | Conformance to existing keyboard, dialog and focus standards; no visible change | N/A | `design_system.md` v1.27 (locked: §Accessibility, §Modal / Dialog Theming, focus indicator contrast) | ✅ Cleared | Head of UX & Design |
| ST-02 (BLG-FE-312) | Link the Exit dialog's labels to their inputs | Design Pre-Approved | Label/input association; no visible change | N/A | `design_system.md` v1.27 (locked: §Accessibility) | ✅ Cleared | Head of UX & Design |
| ST-03 (BLG-FE-318) | Say Telegram, not email, and show when an alert was not sent | Design Required | Changed copy; new data displayed (delivery line) | `docs/design/2026-11-18__release-v9.18/alert-delivery-truth/decision_record.md` §2–§3 (new) | `pages/notifications.md` v0.11 → v0.12 | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-04 (BLG-FE-228) | Fix Alert History compact values | Design Required | New data displayed (values the UI never showed) | `alert-delivery-truth` §4 | `pages/notifications.md` v0.12 (§Alert History Values) | ✅ Cleared | Head of UX & Design |
| ST-05 (BLG-SEC-46) | Re-review the accepted open-access risk | Design Not Applicable | Review and decision; `noindex` has no visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-06 (BLG-QA-271) | Measure Core Web Vitals and update the performance budget | Design Not Applicable | CI and measurement | N/A | N/A (`performance_budget.md` in-story) | ✅ Cleared | Head of UX & Design |
| ST-07 (BLG-UX-21) | Revise navigation.md and design_system.md for the Phase 4 target state | Design Required | Records the adopted IA and design direction | `docs/design/2026-11-18__release-v9.18/navigation-phase4-moves/decision_record.md` (new); re-review §14.2, §14.5 (DL-089) | `pages/navigation.md` v2.4 → v2.5 (this gate); `design_system.md` §14.5 in-story | ✅ Cleared (`design_system.md` half in-story; addendum) | Head of UX & Design + Product Owner |
| ST-08 (BLG-FE-323) | Move Strategy Benchmark into Performance and Ticker Universe into Settings | Design Required | Changed navigation, new section, new route | `navigation-phase4-moves` §2–§4 | `pages/navigation.md` v2.5; `pages/performance.md` v1.2 → v1.3 (§4.1); `pages/strategy_benchmark.md` v0.11 → v0.12; `pages/ticker_universe.md` v1.2 → v1.3; `pages/settings.md` v1.10 → v1.11 | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-09 (BLG-UX-11) | Make the quiet-day Dashboard a single line | Design Required | Changed layout | `docs/design/2026-11-18__release-v9.18/dashboard-quiet-day/decision_record.md` §2 (new) | `pages/dashboard.md` v4.3 → v4.4 (§3A) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-10 (BLG-FE-308) | Use one grace-period definition across the Dashboard | Design Required | Changed data displayed; link target | `dashboard-quiet-day` §3 | `pages/dashboard.md` v4.4 (§4B, §1A, Cards 1 and 3) | ✅ Cleared | Head of UX & Design |
| ST-11 (BLG-UX-13) | Offer "Plan this" on the Today list's New signals rows | Design Required | New link on a row; Product Owner chose to add it | `dashboard-quiet-day` §4 | `pages/dashboard.md` v4.4 (§1B, TL-30) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-12 (BLG-UX-19) | Show machine-checkable checklist items as automatic status | Design Required | Changed component and interaction. "Heat limits" item renamed (Product Owner) | `docs/design/2026-11-18__release-v9.18/trade-plan-checklist-status/decision_record.md` (new) | `pages/trade_plan.md` v1.29 → v1.30 (§6) | ✅ Cleared (§13 note confirmation before build; addendum) | Head of UX & Design + Product Owner |
| ST-13 (BLG-FE-320) | Filter Trade History and Journal by rules followed or broken | Design Required | New filter, counts and row line | `docs/design/2026-11-18__release-v9.18/rules-followed-filter/decision_record.md` (new) | `pages/trade_history.md` v1.17 → v1.18 (§Rules Filter) | ✅ Cleared (metric definition in-story, before build) | Head of UX & Design |
| ST-14 (BLG-SPEC-204) | Rename the Weekly Digest's journal completion figure | Design Required | Label wording; API field rename | `docs/design/2026-11-18__release-v9.18/weekly-review/decision_record.md` §4 (new) | `pages/weekly_digest.md` v0.2 → v0.3 | ✅ Cleared | Head of UX & Design |
| ST-15 (BLG-UX-15) | Rewrite the Weekly Digest as a readable weekly summary | Design Required | Changed layout and copy | `weekly-review` §3 | `pages/weekly_digest.md` v0.3 (§2) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-16 (BLG-UX-12) | Link the Weekly Digest figures to their pages | Design Required | New links. New `red_flags_7d` figure (Product Owner) | `weekly-review` §2, §5 | `pages/weekly_digest.md` v0.3; `pages/navigation.md` v2.5 (§Onward Links) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-17 (BLG-FEAT-103) | Measure the core loop and show this week's loop on the Weekly Digest | Design Required | New section | `weekly-review` §6 | `pages/weekly_digest.md` v0.3 (§This Week's Loop) | ✅ Cleared (metric definitions in-story) | Head of UX & Design + Product Owner |
| ST-18 (BLG-GOV-422) | Design gate data-source, writer and worked-example checks | Design Not Applicable | Governance prompt | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-19 (BLG-QA-262) | Unit-test pure frontend logic in CI | Design Not Applicable | CI and tests | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-20 (BLG-QA-260) | Fail the axe scan on incomplete colour-contrast results | Design Not Applicable | Test tooling | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-21 (BLG-QA-268) | Script the locator-collision check | Design Not Applicable | Tooling | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-22 (BLG-GOV-420) | Require the pre-commit code review | Design Not Applicable | Governance prompt | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-23 (BLG-GOV-421) | Enforce the prompt size budget on direct commits to main | Design Not Applicable | Hook and workflow | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-24 (BLG-GOV-388) | Count an item as shipped only on a ✅ COMPLETE banner line | Design Not Applicable | Tooling | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-25 (BLG-BE-208) | Use one native-entry function on every position path | Design Not Applicable | Backend refactor, no behaviour change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-26 (BLG-BE-213) | Use the live FX rate, not a hard-coded 1.27 | Design Not Applicable | Backend correctness; values become correct, no display change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-27 (BLG-BE-223) | Handle a stock split on an open position | Design Required | New state, tier and confirmation dialog on Positions | `docs/design/2026-11-18__release-v9.18/position-data-states/decision_record.md` §2 (new) | `pages/positions.md` v2.29 → v2.30 (§Urgency Order tier 0, §Split Detected State) | ✅ Cleared (rule approval before build, slice AC) | Head of UX & Design + Product Owner |
| ST-28 (BLG-BE-179) | Tag lifecycle transitions caused by the v9.12 currency correction | Design Not Applicable | Data tagging and analytics | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-29 (BLG-BE-181) | Keep GET /settings working when the change-log read fails | Design Not Applicable | Backend resilience. A null `last_change` is already specified (`settings.md` §Last Change Line) | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-30 (BLG-SPEC-203) | Make the Reports unrealised P&L match the Positions basis | Design Required | Changed figure basis and note text. Option (a) (Product Owner) | `position-data-states` §3 | `pages/reports.md` v0.27 → v0.28 (§Unrealised P&L Card) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-31 (BLG-FE-225) | Cache the Trade Entry ATR preview per ticker and market | Design Pre-Approved | States and debounce unchanged | N/A | `components/position_form.md` v1.14 (locked: §ATR preview) | ✅ Cleared | Head of UX & Design |
| ST-32 (BLG-OPS-217) | Finish the on-demand Yahoo failure diagnosis (remainder) | Design Not Applicable | Production diagnosis and report | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-33 (BLG-FE-294) | Show "earnings unknown" when a lookup fails | Design Required | New state on three pages | `position-data-states` §4 | `pages/positions.md` v2.30 (§Earnings Unknown); `pages/screener_results.md` v1.11 → v1.12; `pages/watchlist.md` v0.10 → v0.11 | ✅ Cleared | Head of UX & Design |
| ST-34 (BLG-OPS-220) | Let the visual-baseline workflow push regenerated snapshots | Design Not Applicable | CI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-35 (BLG-OPS-205) | Seed staging's UK positions with the .L suffix | Design Not Applicable | Seed data | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-36 (BLG-OPS-206) | Build the E2E bundle once per Playwright run | Design Not Applicable | CI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-37 (BLG-QA-225) | Keep a bare root pytest out of the mutmut pilot tests | Design Not Applicable | Test config | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-38 (BLG-QA-226) | Run the settings change-log SQL against real Postgres in CI | Design Not Applicable | CI test | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-39 (BLG-AI-29) | Check daily briefing and chat output against §13.2 | Design Not Applicable | Backend output check. Covered §13 review: `docs/product/decisions/decisions--2026-06-24__release-v6.2--BLG-FEAT-50-51-section13-review.md` | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-40 (BLG-GOV-378) | Decide whether the debrief may say more than one restating sentence | Design Not Applicable | Decision story. Covered §13 review: `docs/product/decisions/decisions--2026-08-17__release-v8.9--ST-06-section13-review.md` (CONDITIONAL) | N/A | N/A | ✅ Cleared | Head of UX & Design |

## §13 Boundary Pre-Check

**AI-calling items: no flags.** Two items touch an AI provider's output, and both have a covering §13 review:
- **ST-39:** checks existing briefing and chat output; covered by the BLG-FEAT-50/51 review (path above). If the ruling chooses "regenerate", that is a further call to the existing endpoint, not a new endpoint. The AI endpoint security checklist is therefore not triggered. ST-39's restated AC already cites §13.2 and the §13.5 attestation row.
- **ST-40:** a decision on the debrief, covered by the ST-06 debrief review (CONDITIONAL). Any change is filed as its own item. Its AC cites §13.2 and the §13.5 row.

No other item introduces or extends an AI call.

**Non-AI §13 notes** (recorded, not blocking):
- **ST-12:** the PT-05 §13 review's "no automated condition evaluation" statement becomes stale. The amendment is in `trade_plan.md` v1.30 §6, and the Strategy Rules & System Intent Owner confirms it before the build (addendum). The statuses reuse the SI-01-reviewed §4.2 checks, are advisory (§4.2.6) and gate nothing.
- **ST-11:** "Plan this" is a link to a form, covered by the `signals.md` §"Plan this" Action note. `dashboard.md` §1B's display-only bullet is amended to match.
- **ST-33:** "Earnings: unknown" is a missing-data state, not a new gap-risk trigger. It never uses the GAP RISK badge. ST-33 cites the gap-risk review's binding conditions.
- **ST-27:** suppressing alerts for an unconfirmed split is a `strategy_rules.md` rule (case (c), §12.3), approved before the build. It is not an AI or automation-boundary matter.
- **ST-09:** the line reads "Nothing to show", not "All clear", so the page does not judge the portfolio safe.
- **ST-13, ST-17:** deterministic counts and classifications of the user's own records; no score, ranking or advice.

## Blocked Items

None.

## Notes

### Post-gate-correction addendum

`claude/cycles/2026-11-18__release-v9.18/stage4_backlog_slice_addendum.md` was created with 15 entries. Sprint Planning and Sprint Execution must read it with the sealed slice. No entry changes scope. They correct or make precise ST-03, ST-04, ST-07, ST-08, ST-09, ST-10, ST-11, ST-12, ST-13, ST-14, ST-16, ST-17, ST-27, ST-30 and ST-33. The data-source and premise findings behind them:
- **ST-12:** no heat limit exists.
- **ST-16:** no digest red-flags field, and no Journal section shows journal completion.
- **ST-13:** no rule fields on `GET /trades`.
- **ST-10:** Card 3 reads `grace_end_date`, which is never returned.
- **ST-04:** the regime keys are also wrong.
- **ST-03:** `GET /notifications` returns no delivery fields.

### Checks applied

Each Design Required record ran a data-source check: every displayed field traced to its contract and writer. Where a value shows on two surfaces or a rule has a threshold, the record also has a worked-examples table: grace (5 positions), checklist (6 input sets), split (2:1 fixture), Weekly Digest (null, zero and rounding cases) and earnings (status × date). These anticipate ST-18's checks, which change the design gate prompt only after this gate. They follow the standing first-time-right practice and are not a prompt requirement this run.

### Artefacts produced and specs updated

- **Design artefacts:** 7 decision records under `docs/design/2026-11-18__release-v9.18/`:
  - `alert-delivery-truth` (ST-03, ST-04)
  - `navigation-phase4-moves` (ST-07, ST-08, ST-16's onward links)
  - `dashboard-quiet-day` (ST-09, ST-10, ST-11)
  - `trade-plan-checklist-status` (ST-12)
  - `rules-followed-filter` (ST-13)
  - `weekly-review` (ST-14, ST-15, ST-16, ST-17)
  - `position-data-states` (ST-27, ST-30, ST-33)
- **Frontend specs updated:** 14 files, each logged in `prompt_change_log.md`:
  - `notifications.md` 0.11→0.12
  - `navigation.md` 2.4→2.5
  - `performance.md` 1.2→1.3
  - `strategy_benchmark.md` 0.11→0.12
  - `ticker_universe.md` 1.2→1.3
  - `settings.md` 1.10→1.11
  - `dashboard.md` 4.3→4.4
  - `trade_plan.md` 1.29→1.30
  - `trade_history.md` 1.17→1.18
  - `weekly_digest.md` 0.2→0.3
  - `positions.md` 2.29→2.30
  - `reports.md` 0.27→0.28
  - `screener_results.md` 1.11→1.12
  - `watchlist.md` 0.10→0.11

### Decisions still open before or during the build (not design-gate items)

- **ST-12:** Strategy Rules & System Intent Owner confirms the amended §13 note (dated) before the build.
- **ST-13:** Metrics Definitions & Analytics Owner writes the rules-followed definition before the build.
- **ST-17:** Metrics Definitions & Analytics Owner writes the five step definitions, and signs them off.
- **ST-27:** Strategy Rules & System Intent Owner approves the split rule (§12.3) before the build (slice AC, RISK-05).

### Obligations passed to Sprint Execution (outside this gate's write scope)

- **New API fields:** `GET /notifications` `delivery_status` (ST-03), `GET /trades` `rules_followed`/`rules_broken` (ST-13), `GET /digest/weekly` `journal_completion_rate_*`, `closed_trades_total` (ST-14) and `red_flags_7d` (ST-16), and `GET /earnings/{ticker}` and gap-risk `data_status` (ST-33). Each needs its contract and `openapi.yaml` change in the same commit. No new route is introduced, so `backend/routers/test.py` changes only if ST-17 adds an events endpoint (CLAUDE.md §2).
- **ST-07:** write `design_system.md` §14.5 and date the Head of UX & Design approval of both files.
- **ST-08:** move or remove `section-index.spec.js` SC-SIX-06 to SC-SIX-08, and update `pageLabels.js`, the command palette and `Layout.js`.
- **ST-10:** move `nextEndsText` into `src/lib/positionUrgency.js`, with unit tests per ST-19's convention.
- **ST-27:** add tier 0 to `src/lib/positionUrgency.js`, with unit tests.
- **ST-30:** mark `DEV-REPORTS-ST06-01` resolved and remove the v0.10 snapshot bullet in `reports.md`.

### Observations for filing (outside this gate's write scope; `/backlog-add` at Sprint Planning)

- **Weekly Digest rename:** the re-review's "Weekly review" rename (§14.2) is in no v9.18 story. It is spec-only today.
- **Dashboard spec drift:** `dashboard.md` §1A's Earnings Alert click target says "Earnings calendar or `/watchlist`"; the shipped card links to `/Positions`. Spec drift.
- **Notification re-delivery:** re-delivery retries `delivered = false` rows up to 3 times. With a preference off, a generic notification is never enqueued (`delivery_attempts = 0`). Check whether the re-delivery query sends such rows once a preference is turned on later, as the Reflection Reminder design deliberately avoids.
- **Strategy Benchmark data cost:** inside Performance, its data loads with the page. ST-06's baseline should note whether it was measured before or after ST-08 merged.
