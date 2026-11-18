Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-18
Cycle: 2026-11-18__release-v9.18
Release: v9.18

# Backlog Slice — v9.18

<!-- release-plan-marker: RP:v9.18:2026-11-18__release-v9.18 -->

40 stories across 7 EPICs, 27.95 estimated days. The acceptance criteria below are the source of truth for Sprint Planning and Execution. Scope is sized to the top of the confirmed ~24–28 day capacity band, per the explicit user instruction "use full capacity" (2026-11-18).

**Ready pool:** 233 items, 110.35 days (after the STEP 4 calibration raises, applied to the whole pool before selection). The 20 Phase 4 stage 3–4 items (16.25d, provisional v9.19) are held outside the pool by §1.4c step 0.

**Selection method** (`release_planning_prompt.md` §1.4c, v2.75):
0. **Programme-phase hold (step 0):** the 20 P3 items in Phase 4 stages 3 and 4 (provisional v9.19) are held. Nothing else is held; DL-088's programme plan has shipped in full.
1. No ready P1 item (`BLG-FEAT-73` is not ready). The ready P2 items in ascending ID order: `BLG-BE-208`, `BLG-BE-213`, `BLG-BE-223`, `BLG-FE-294`, `BLG-FE-311`, `BLG-FE-312`, `BLG-GOV-420`, `BLG-GOV-421`, `BLG-GOV-422`, `BLG-OPS-217` (split-achievability remainder only), `BLG-QA-262` and `BLG-SEC-46`. `BLG-TECH-21` stays deferred (standing override).
2. Step 1a, deferred lessons-learnt patch items targeted at v9.18: `BLG-QA-268` (`LL-v9.17-P3-01` (b)) and `BLG-OPS-220` (`LL-v9.17-P3-03`; see `run_manifest.md` for the reading).
3. Step 1b, current programme phase tier: Phase 4 stages 1–2's P3 items `BLG-FE-308`, `BLG-FE-318`, `BLG-FE-320`, `BLG-FE-323`, `BLG-FEAT-103`, `BLG-QA-271`, `BLG-UX-11`, `BLG-UX-12`, `BLG-UX-13`, `BLG-UX-15`, `BLG-UX-19` and `BLG-UX-21`.
4. Product Owner override: `BLG-QA-260` (P3), directed 2026-11-12 and committed in the roadmap's v9.18 section (DL-089).
5. A category-balanced, oldest-first round-robin over P3/P4, run until 0.05 days were left.

**Where an item's own AC is stale, untestable, met elsewhere or extended by the Product Owner, the AC below restates it.** Each change from the source backlog item is marked *(restated)* with the reason. Scope bullets are copied from the source item for convenience; the source item stays authoritative for Problem text. **Planning estimate** is the figure used for capacity (calibrated or remainder-only where noted); **Effort** is the source item's field, unchanged.

**Gates cleared this run:** none. The scan listed 0 date-lapsed items, and each of the 13 gating-item-shipped items still has an unmet limb.

**`strategy_rules.md` writes (case (c), `execution_prompt.md` §7):** ST-27 adds a stock-split rule under §12.3 change control, approved by the Strategy Rules & System Intent Owner before the build (RISK-05).

**§13 clause-citation rule (v2.61):** ST-39 and ST-40 each require a §13 determination. Their restated ACs cite §13.2 (the AI-text sentence names the daily briefing, chat and post-trade debrief) and the matching §13.5 attestation-table rows. No other §13 clause names these subjects.

**Post-merge, production and console ACs (Sprint Planning STEP 6.2):** ST-32 needs a production weekly report (not before 2026-11-20). ST-40 needs a sample of real production debriefs. ST-27's and ST-17's migrations run against production at deploy. ST-35 writes to staging with the user's permission. ST-05's decision is the Cybersecurity & Trust Lead's and the Product Owner's. Sprint Planning marks each `post-merge` or Human-Delegation item with a named tracking item before the seal.

**Conditional stories (§1.4b):** ST-32 (`BLG-OPS-217` remainder). Its AC 2 needs 7 days of production data after the fix, which merged in PR #2259 at 2026-11-13T15:11:51Z (checked with `gh pr view 2259 --json mergedAt`), so the report window closes on 2026-11-20, inside the sprint window. It is classified conditional and may be promoted to firm only when the Infrastructure & Operations Owner confirms the report (dated).

---

## EPIC-01 — Site Structure & Usability Phase 4, Stage 1: Correct and Safe (build-and-ship)

**Maps to:** S2-01 – S2-06
**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner; Cybersecurity & Trust Lead
**Description:** Fix the Level A accessibility failures, make alert-delivery copy truthful, re-review the accepted open-access risk, and measure Core Web Vitals before Phase 4's speed work.
**Estimated days:** 3.65

### ST-01 — Make the four mouse-only controls keyboard-operable
**Source:** BLG-FE-311
**Priority:** P2
**Effort:** S (~0.5-1 day)
**Planning estimate:** 0.75d
**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner
**Sequencing:** First in EPIC-01 with ST-02; both add axe scans to `accessibility-axe-scan.spec.js`.
**UI-facing:** Yes
**Scope:**
- Use a `<button>` (or a checkbox for the monitor's exit selection), with `aria-expanded` on the two toggles
- Give the heatmap detail dialog semantics and focus management (or reuse the shared Dialog)
- Name the Screener close button
**Acceptance Criteria:**
- Each of the four controls can be reached with Tab and operated with Enter/Space, and the toggles expose `aria-expanded` (Playwright, keyboard only)
- axe passes with the heatmap detail and the Screener popover open, with no `button-name` or `aria-dialog-name` violation (Playwright)

### ST-02 — Link the Exit dialog's labels to their inputs
**Source:** BLG-FE-312
**Priority:** P2
**Effort:** XS (<1h, plus a scan of the open dialog)
**Planning estimate:** 0.15d
**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner
**Sequencing:** After ST-01 (same spec file).
**UI-facing:** Yes
**Scope:**
- Add `id`/`htmlFor` pairs for the four fields
- Add an axe scan of the open Exit dialog, light and dark, to `accessibility-axe-scan.spec.js`
**Acceptance Criteria:**
- `getByLabel('Shares to Exit')`, `'Exit Price'`, `'Exit Date'` and `'Exit Note (Optional)'` each resolve to their input (Playwright)
- axe passes on the open dialog with no `label` violation (Playwright, both themes)

### ST-03 — Say Telegram, not email, and show when an alert was not sent
**Source:** BLG-FE-318
**Priority:** P3
**Effort:** S (~0.5 day)
**Planning estimate:** 0.5d
**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner
**Sequencing:** Before ST-04 (same Notification History page).
**UI-facing:** Yes
**Scope:**
- Rename "email" to "Telegram" in the UI and in `notifications.md` (and the `email_enabled` label, keeping the column name if a migration is not wanted)
- When the channel is unconfigured, record `delivered = FALSE` with a clear error, and show "Not sent: Telegram not configured" in Notifications/Notification History
- Add the API contract change if the response gains a delivery-status field (with `openapi.yaml`)
**Acceptance Criteria:**
- No "email" wording remains on Notification Preferences (Playwright)
- With Telegram unconfigured, a new notification is stored as not delivered, and the UI shows that it was not sent (pytest + Playwright)

### ST-04 — Fix Alert History compact values
**Source:** BLG-FE-228
**Priority:** P3
**Effort:** XS (~0.25 day)
**Planning estimate:** 0.25d
**Owner:** Frontend Specifications & UX Documentation Owner
**Sequencing:** After ST-03.
**UI-facing:** Yes
**Scope:**
- Align UI keys and labels with the backend (or rename backend keys) and record the mapping in the Alert History page spec
**Acceptance Criteria:**
- [ ] All 4 alert types show their intended compact fields (unit or Playwright test)

### ST-05 — Re-review the accepted open-access risk
**Source:** BLG-SEC-46
**Priority:** P2
**Effort:** S (~0.5 day review; any chosen remedy is separate)
**Planning estimate:** 0.5d
**Owner:** Cybersecurity & Trust Lead; Product Owner
**Sequencing:** Independent; early, because its decision sets whether Phase 4 needs a v9.20 access remedy.
**UI-facing:** No
**Note:** Review and decision story. Any remedy is filed as its own item (AC 2); the roadmap's conditional v9.20 row depends on it.
**Scope:**
- Re-review the accepted risk with the owner's own data privacy and the URL's discoverability in view
- Record a dated decision: keep the acceptance (with reasons), or add access control in front of the static site, or narrow the front-end key (the accept-risk's option (a)), or another remedy; add `noindex` if the acceptance stands
- Update `credential_policy.md` §1.1 and its review triggers to match
**Acceptance Criteria:**
- `credential_policy.md` §1.1 records the dated re-review decision by the Cybersecurity & Trust Lead and the Product Owner, explicitly covering read access to the owner's data
- Any remedy chosen is filed as its own backlog item

### ST-06 — Measure Core Web Vitals and update the performance budget
**Source:** BLG-QA-271
**Priority:** P3
**Effort:** M (~1-2 days)
**Planning estimate:** 1.5d
**Owner:** QA & Testing Owner; Frontend Specifications & UX Documentation Owner
**Sequencing:** Baseline before any Phase 4 stage 4 speed work (v9.19). Independent of ST-01–ST-05.
**UI-facing:** No
**Scope:**
- Revise `performance_budget.md` to Core Web Vitals (LCP ≤ 2.5 s, INP ≤ 200 ms, CLS ≤ 0.1) on a mobile profile and on desktop; drop TTI
- Add a Lighthouse CI job (mobile and desktop) for Dashboard, Positions, Trade Plan and Performance, against mocked API data, and a bundle-size check against §3.3
- Add `web-vitals` reporting in the app (console in development; a lightweight log in production if wanted)
- Record the first baseline, before `BLG-FE-315`/`316`/`317` land
**Acceptance Criteria:**
- `performance_budget.md` lists CWV targets and a dated baseline per page and profile
- CI runs Lighthouse and the bundle-size check on each PR and reports the values

---

## EPIC-02 — Site Structure & Usability Phase 4, Stage 2: Home Page and Navigation (build-and-ship)

**Maps to:** S2-07 – S2-13
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner; Head of Engineering
**Description:** Revise the navigation and design-system specs for the adopted target state, then build a calm quiet-day Dashboard, one grace definition, checks the system knows shown as status, rules-followed filtering and the two navigation moves.
**Estimated days:** 6.15

### ST-07 — Revise navigation.md and design_system.md for the Phase 4 target state
**Source:** BLG-UX-21
**Priority:** P3
**Effort:** S (~0.5 day decision + `navigation.md` revision)
**Planning estimate:** 0.5d
**Owner:** Product Owner; Head of UX & Design
**Sequencing:** First in EPIC-02. Before ST-08 (navigation moves) and ST-09 (Dashboard).
**UI-facing:** No
**Note:** Source item's AC 1 is met by DL-089; it is carried as context only.
**Scope:**
- Product Owner decides whether to adopt §14 (in whole or in part) as the brief for a "Site Structure & Usability, Phase 4" programme at the next `run roadmap`, and records the decision (decision log)
- If adopted: revise `navigation.md` for the two moves, and record the design direction (§14.5) in `design_system.md`
**Acceptance Criteria:**
- A dated Product Owner decision on §14 is in the decision log
- If adopted: `navigation.md` and `design_system.md` reflect the decisions, with dated Head of UX & Design approval
- *(restated)* The Product Owner decision half is met: DL-089 (roadmap rebalance `2026-11-18__scheduled`) adopted the 2026-11-17 re-review §14 in whole. This story delivers the remaining AC: `navigation.md` (the two §14.2 moves) and `design_system.md` (the §14.5 design direction) reflect the decision, with dated Head of UX & Design approval

### ST-08 — Move Strategy Benchmark into Performance and Ticker Universe into Settings
**Source:** BLG-FE-323
**Priority:** P3
**Effort:** M (~1-1.5 days)
**Planning estimate:** 1.25d
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner; Head of Engineering
**Sequencing:** After ST-07 (`navigation.md` revision).
**UI-facing:** Yes
**Scope:**
- Strategy Benchmark becomes a "Strategy vs backtest" section of Performance, reachable from its section index; the old route redirects to the section
- Ticker Universe moves under Settings; the old route redirects
- Sidebar, command palette (`src/components/CommandPalette.js`) and `src/lib/pageLabels.js` updated
**Acceptance Criteria:**
- Neither page has its own sidebar entry; both old URLs land on the new location
- Playwright covers both redirects and the new entry points

### ST-09 — Make the quiet-day Dashboard a single line
**Source:** BLG-UX-11
**Priority:** P3
**Effort:** M (~1-2 days, spec revision then build)
**Planning estimate:** 1.5d
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Sequencing:** After ST-07. Before ST-10 (same Dashboard specs and baselines).
**UI-facing:** Yes
**Scope:**
- Revise `dashboard.md` §3 and §4A so cards in their zero state collapse on a quiet day (for example one muted "All clear" line naming them, each still a link), while cards with data keep their place and order
- Build it, with Playwright coverage in both themes, and regenerate the Dashboard visual baselines
**Acceptance Criteria:**
- With the quiet-day fixture, the Dashboard shows at most 1 empty-state element below "Due today" (Playwright, light and dark)
- A card with data still renders in its v4.0 position (Playwright)

### ST-10 — Use one grace-period definition across the Dashboard
**Source:** BLG-FE-308
**Priority:** P3
**Effort:** S (~0.5 day)
**Planning estimate:** 0.5d
**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Sequencing:** After ST-09 (same Dashboard cards).
**UI-facing:** Yes
**Scope:**
- Name one in-grace predicate in `dashboard.md` (matching `positions.md` §Grace Period View) and use it in `ExitZoneCard.js` and `OpenPositionsCard.js`
- Point "Positions to Watch" at `/Positions?grace=open` when its count includes in-grace positions
**Acceptance Criteria:**
- With a fixture where `grace_period` and `grace_days_remaining` disagree for one position, every Dashboard grace count shows the same number (Playwright)
- "Positions to Watch" opens the Positions grace view (Playwright)

### ST-11 — Offer "Plan this" on the Today list's New signals rows
**Source:** BLG-UX-13
**Priority:** P3
**Effort:** XS (<1h build, after the spec line)
**Planning estimate:** 0.15d
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Sequencing:** After ST-10 (`dashboard.md` §1B).
**UI-facing:** Yes
**Scope:**
- Decide in `dashboard.md` §1B whether a New signals row offers "Plan this" (to the pre-filled Trade Plan) beside the Research link, consistent with `signals.md` §"Plan this" Action and `BLG-UX-09`
- Build it if chosen
**Acceptance Criteria:**
- `dashboard.md` §1B records the decision; if "Plan this" is added, it opens Trade Plan pre-filled with the signal's ticker and market (Playwright)

### ST-12 — Show machine-checkable checklist items as automatic status
**Source:** BLG-UX-19
**Priority:** P3
**Effort:** S (~0.5-1 day, spec then build)
**Planning estimate:** 0.75d
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Sequencing:** Independent of the Dashboard stories (Trade Plan page).
**UI-facing:** Yes
**Scope:**
- In `trade_plan.md`, split the checklist: system-verified items shown as pass/fail status from the pre-entry checks and the form, and human-judgement items kept as ticks
- Build it; keep the existing acknowledgement before "Create Position" as the pause point
- Check stored `checklist_items` compatibility (existing plans keep their saved ticks)
**Acceptance Criteria:**
- "Position size within heat limits" and "Stop level defined" show as automatic status that follows the inputs and cannot be ticked by hand (Playwright)
- Human-judgement items remain tickable, and existing plans load without losing saved ticks (Playwright + unit test)

### ST-13 — Filter Trade History and Journal by rules followed or broken
**Source:** BLG-FE-320
**Priority:** P3
**Effort:** M (~1-2 days)
**Planning estimate:** 1.5d
**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Sequencing:** Independent. Its metric definition is agreed with the Metrics Definitions owner before the build.
**UI-facing:** Yes
**Scope:**
- Define "rules followed" per closed trade from existing data (pre-entry checks passed or acknowledged, exit reason, red flags), with the Metrics Definitions owner, in `metrics_definitions.md` and `trade_history.md`
- Add a "Rules followed / Rules broken" filter to Trade History (and the Journal's red-flags section if useful), with summary counts
**Acceptance Criteria:**
- The definition is recorded in `metrics_definitions.md`
- With a fixture containing compliant and non-compliant closed trades, each filter shows only the matching trades (Playwright)

---

## EPIC-03 — Site Structure & Usability Phase 4, Stage 2: Weekly Review Loop (build-and-ship)

**Maps to:** S2-14 – S2-17
**Owner:** Head of UX & Design; Metrics Definitions & Analytics Owner; Product Owner
**Description:** Turn the Weekly Digest into a readable weekly summary linked to the pages where each figure is reviewed, name its journal-completion figure correctly, and measure the core loop on it.
**Estimated days:** 4.25

### ST-14 — Rename the Weekly Digest's journal completion figure
**Source:** BLG-SPEC-204
**Priority:** P3
**Effort:** S (~0.5 day)
**Planning estimate:** 0.5d
**Owner:** Metrics Definitions & Analytics Owner; API Contracts & Documentation Owner
**Sequencing:** First in EPIC-03: renames the field ST-15 and ST-16 lay out and link.
**UI-facing:** Yes
**Scope:**
- Relabel the rows "Journal Completion Rate" (or source them from the composite)
- Add `journal_completion_rate_*` fields with the old names as deprecated aliases; update contract and `openapi.yaml`
**Acceptance Criteria:**
- [ ] No UI label or API field named "compliance" carries the journal completion rate
- [ ] Contract, `openapi.yaml` and `metrics_definitions.md` agree

### ST-15 — Rewrite the Weekly Digest as a readable weekly summary
**Source:** BLG-UX-15
**Priority:** P3
**Effort:** S (~0.5-1 day)
**Planning estimate:** 0.75d
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Sequencing:** After ST-14. Built with ST-16 (the source items say do together).
**UI-facing:** Yes
**Scope:**
- Revise `weekly_digest.md`: labelled figures in plain language (for example "Realised P&L this week", "Change in open P&L"), no Unit column, the as-of time as a caption, and a description that says what the page is for
- Build it with `BLG-UX-12`'s onward links
**Acceptance Criteria:**
- No "Field", "Unit" or "timestamp" text renders on the page, and each figure has a plain-language label (Playwright, light and dark)

### ST-16 — Link the Weekly Digest figures to their pages
**Source:** BLG-UX-12
**Priority:** P3
**Effort:** S (~0.5 day)
**Planning estimate:** 0.5d
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Sequencing:** With ST-15.
**UI-facing:** Yes
**Scope:**
- Add `navigation.md` §Onward Links rows and `weekly_digest.md` links: realised P&L to Performance (Summary), compliance score to Performance (Compliance), red flags to Journal (Red flags)
- Build them
**Acceptance Criteria:**
- Each of the three figures links to its section, and the link lands on that section (Playwright)
- *(restated)* If ST-14 relabels the compliance score row as journal completion rate, its link goes to the Journal section that shows journal completion, not Performance (Compliance); the choice is recorded in `navigation.md` §Onward Links

### ST-17 — Measure the core loop and show this week's loop on the Weekly Digest
**Source:** BLG-FEAT-103
**Priority:** P3
**Effort:** M (~2-3 days: metric definitions, one events table, digest section)
**Planning estimate:** 2.5d
**Owner:** Product Owner; Metrics Definitions & Analytics Owner; Data Model & Domain Schema Owner
**Sequencing:** Last in EPIC-03 (adds a section to the page ST-15 rewrites).
**UI-facing:** Yes
**Note:** New events table: `data_model.md` migration block, contract and `openapi.yaml` if an endpoint is added, and `backend/routers/test.py` registration per CLAUDE.md §2.
**Scope:**
- `metrics_definitions.md`: define the five step counts per ISO week and the step-to-step completion rates, with worked examples (quiet week, a week with no signals, a reflection written the week after the exit)
- One small events table for the two steps no existing table records (Weekly Digest opened, Due today action taken); no other page-view tracking
- A "This week's loop" section on the Weekly Digest page (`src/pages/WeeklyDigest.js`) showing the five counts with links to the page behind each
**Acceptance Criteria:**
- The five metrics are in `metrics_definitions.md` with worked examples and owner sign-off
- The Weekly Digest shows the five counts for the current week; each links to its page
- Opening the Weekly Digest and taking a Due today action each write one event row; nothing else is tracked
- Playwright covers the section's rendering and links (CLAUDE.md §2)

---

## EPIC-04 — First-Time-Right Checks (Product Owner direction, 2026-11-12)

**Maps to:** S2-18 – S2-24
**Owner:** Head of Specs Team; QA & Testing Owner; Head of Engineering
**Description:** Add the checks that would have prevented most of v9.17 EPIC-01's follow-up filings: design gate data-source and worked-example checks, frontend unit tests in CI, stricter contrast scanning, a scripted locator-collision check, and enforced pre-commit review and prompt-size budget.
**Estimated days:** 3.70

### ST-18 — Design gate data-source, writer and worked-example checks
**Source:** BLG-GOV-422
**Priority:** P2
**Effort:** S (~0.5d)
**Planning estimate:** 0.75d
**Owner:** Head of Specs Team; Head of UX & Design
**Sequencing:** First in EPIC-04, and early in the sprint: v9.19's design gate is its first real use.
**UI-facing:** No
**Note:** Effort raised 0.5d → 0.75d for the Product Owner's scope extension (two more checks and a second dry run). Release Planning cannot edit the source item (§7); the extension lives here.
**Scope:**
- `design_gate_prompt.md` STEP 2.2: add a **data-source check**. For every field a new or changed view displays, name the endpoint and the contract line showing that the endpoint returns the field for the whole population the view lists. Any gap is either a backend story in the slice or a spec change, decided before the gate passes
- STEP 2.2: add a **worked-examples table** for any value displayed on two or more surfaces, or any rule with a threshold. Take one set of boundary inputs (for example 0, 1, 2 and null days, and true, false and null flags) and give the exact text each surface shows for each
- STEP 2.2: for any rule that depends on another component's state ("active when X would render"), list X's states and the rule's result for each
- CLAUDE.md §6 governance file checklist in the same commit
**Acceptance Criteria:**
- `design_gate_prompt.md` STEP 2.2 requires the data-source check, the worked-examples table and the dependent-state list, and the design gate record template has a place to record each
- Re-running the three checks on the v9.17 `positions-decision-first` decision record finds the BLG-BE-215 gap and the BLG-SPEC-234/235 last-day contradiction (dry run recorded in the commit or a docs/ops note)
- *(restated — scope extension, Product Owner 2026-11-13, v9.17 `execution_state.json` process_note, commit `a207af77`)* STEP 2.2 also requires a **writer check**: for any spec claim that a field is "written by X" or that "only X does Y", grep every writer and cite them
- *(restated — same extension)* The worked-examples table covers **time boundaries**: stale data, a quiet day, weekends, UTC midnight, the latest row closing, and a named source for any run date
- *(restated — same extension)* Re-running the checks on `dashboard.md` v4.0 §1B finds both v9.17 EPIC-04 gaps (dry run recorded in the commit or a docs/ops note)

### ST-19 — Unit-test pure frontend logic in CI
**Source:** BLG-QA-262
**Priority:** P2
**Effort:** M (~1–2d)
**Planning estimate:** 1.5d
**Owner:** QA & Testing Owner; Head of Engineering
**Sequencing:** Early in EPIC-04: ST-21's script and later `src/lib` changes ship with unit tests under its convention.
**UI-facing:** No
**Scope:**
- A CI job that runs `CI=true npm test -- --watchAll=false` on every PR touching `src/**`
- Table-driven unit tests for `src/lib/positionUrgency.js` and `src/lib/exitCondition.js` covering null, missing, string and 0 values for each input
- A rule in the test conventions doc: a new or changed pure module under `src/lib/` ships with unit tests in the same commit
**Acceptance Criteria:**
- The new CI job fails a PR whose `src/lib` unit test fails
- `positionUrgency.test.js` asserts `stopDistanceR` returns null for a 0 stop, and that a null `grace_period` is tiered the same way the cells display it (fails until BLG-FE-289/292 are fixed, or is marked `test.failing` with those IDs)
- The convention is written in the testing standards doc

### ST-20 — Fail the axe scan on incomplete colour-contrast results
**Source:** BLG-QA-260
**Priority:** P3
**Effort:** XS (<1h)
**Planning estimate:** 0.15d
**Owner:** QA & Testing Owner
**Sequencing:** After EPIC-01 merges or rebased on it (shared `runAxeScan` helper with ST-01/ST-02).
**UI-facing:** No
**Note:** Seated by Product Owner direction (2026-11-12, committed in the roadmap's v9.18 section, DL-089) as a recorded §1.4c override; see `run_manifest.md`.
**Scope:**
- Log incomplete color-contrast nodes for every scan
- Add a strict-page set whose incomplete color-contrast nodes fail the scan
**Acceptance Criteria:**
- Incomplete color-contrast nodes appear in the scan output
- A scan of a page in the strict set fails on an incomplete color-contrast node

### ST-21 — Script the locator-collision check and run it from commit-check
**Source:** BLG-QA-268
**Priority:** P3
**Effort:** S (~0.5d)
**Planning estimate:** 0.5d
**Owner:** Head of Specs Team; QA & Testing Owner
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Add a script that lists the visible strings added or removed in a diff under `src/**` and greps `tests/e2e/` for unscoped `getByText`/`getByRole` locators that match them
- Run it from the `commit-check` skill for any diff touching `src/**`
- Name the script in `execution_prompt.md` §3.1.A step 13 (with the CLAUDE.md §6 version-bump checklist)
**Acceptance Criteria:**
- Run against ST-01's `b2d93f6d` diff, the script flags the SC-COMP-03/07 locators; run against ST-03's pre-fix diff, it flags SC-LBG-03
- `commit-check` runs the script for frontend diffs and reports its matches
- §3.1.A step 13 names the script
- *(restated)* "ST-01's `b2d93f6d` diff" and "ST-03's pre-fix diff" are v9.17 ST-01 and ST-03 (`2026-11-11__release-v9.17`)

### ST-22 — Require the pre-commit code review in execution_prompt.md
**Source:** BLG-GOV-420
**Priority:** P2
**Effort:** XS (<1h)
**Planning estimate:** 0.15d
**Owner:** Head of Specs Team
**Sequencing:** Any order. ST-21 also edits `execution_prompt.md`, and ST-18/ST-21/ST-23 also bump `OPERATIONAL_GUIDE.md`: rebase in turn and apply CLAUDE.md §8 step 2a per file.
**UI-facing:** No
**Scope:**
- Add to `execution_prompt.md`'s story-completion steps: run `commit-check` (including Check 11) before every implementation commit
- Complete the CLAUDE.md §6 checklist: version bump, `OPERATIONAL_GUIDE.md` §14 table, phase section header, `prompt_change_log.md` row
**Acceptance Criteria:**
- `execution_prompt.md` requires Check 11 before every implementation commit
- All four §6 steps are in the same commit
- The `governance-drift` skill passes

### ST-23 — Enforce the prompt size budget on direct commits to main
**Source:** BLG-GOV-421
**Priority:** P2
**Effort:** S (~0.5d)
**Planning estimate:** 0.5d
**Owner:** Head of Specs Team; Head of Engineering
**Sequencing:** After ST-22. Bumps `post_ship_closure.md` and `roadmap_prompt.md`.
**UI-facing:** No
**Scope:**
- `.githooks/pre-commit`: when any `claude/system/*.md` file is staged, run `python3 scripts/check_prompt_size_budget.py` and block the commit if it fails
- `prompt-size-budget.yml`: also run on `push` to `main`, so a commit that bypasses the hook shows as a red run on that commit
- `post_ship_closure.md` STEP 8 and `roadmap_prompt.md` STEP 11: run the budget check before committing an action-now patch, and apply §11's headroom rule if it fails (CLAUDE.md §6 checklist for both)
**Acceptance Criteria:**
- A local commit that pushes a `claude/system/` prompt over its baseline is blocked by the pre-commit hook, with the script's message
- The workflow runs on pushes to `main`
- The next post-ship closure after this ships does not raise any baseline in a later PR

### ST-24 — Count an item as shipped only on a ✅ COMPLETE banner line
**Source:** BLG-GOV-388
**Priority:** P3
**Effort:** XS (<1h)
**Planning estimate:** 0.15d
**Owner:** Head of Specs Team; Head of Engineering
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Match the banner only in its conventional positions (the `###` heading line or a line starting `> ✅ COMPLETE` / `**Status:** ✅ COMPLETE`), not as a substring anywhere in the body
- Add a test where an item mentions `✅ COMPLETE` in prose and is still treated as open
**Acceptance Criteria:**
- An item whose only `✅ COMPLETE` occurrence is in prose is not treated as shipped
- Existing `tests/test_scan_backlog_gate_conditions_gating_item_shipped.py` cases still pass

---

## EPIC-05 — Position Data Correctness

**Maps to:** S2-25 – S2-31
**Owner:** Head of Engineering; Backend Engineering Patterns Owner; Strategy Rules & System Intent Owner
**Description:** Make position figures correct at their edges: one native-entry function, live FX instead of a hard-coded rate, stock splits that do not read as stop breaches, tagged basis-correction transitions, a resilient settings read, an honest Reports unrealised P&L, and a cached Trade Entry ATR preview.
**Estimated days:** 6.65

### ST-25 — Use one native-entry function on every position path
**Source:** BLG-BE-208
**Priority:** P2
**Effort:** S (~0.5d)
**Planning estimate:** 0.5d
**Owner:** Head of Engineering
**Sequencing:** First in EPIC-05. Before ST-26 (the source items pair them).
**UI-facing:** No
**Scope:**
- Have `_native_entry()`, `get_portfolio_summary()` and both `portfolio_risk.py` functions call `native_entry_price()` (keeping `_native_entry()`'s caller-supplied `native_entry_price` short-circuit)
- No behaviour change
**Acceptance Criteria:**
- One implementation of the fallback remains
- `tests/test_display_status_native_basis.py` passes unchanged
- `KNOWN_INLINE_NATIVE_ENTRY_COPIES` in `tests/test_fx_market_matrix.py` is lowered to `{}` and the test passes

### ST-26 — Use the live FX rate, not a hard-coded 1.27
**Source:** BLG-BE-213
**Priority:** P2
**Effort:** S (~0.5d)
**Planning estimate:** 0.5d
**Owner:** Head of Engineering
**Sequencing:** After ST-25.
**UI-facing:** No
**Scope:**
- Replace the 1.27 fallback in both `portfolio_risk.py` functions with the live rate, using `native_entry_price()` for the native entry
- Check what `compliance_service.py`'s `fx_rate` feeds; fix it the same way and add it to the matrix if it converts a price or a risk
- No other behaviour change
**Acceptance Criteria:**
- The 3 `xfail` markers tagged `BLG-BE-213` in `tests/test_fx_market_matrix.py` are removed and those tests pass
- `grep -rn "or 1.27" backend/` returns no FX fallback
- `compliance_service.py`'s use is covered by the matrix, or the item records why it does not convert a money value

### ST-27 — Handle a stock split on an open position
**Source:** BLG-BE-223
**Priority:** P2
**Effort:** M (~1.5-2 days: rule text, adjustment record, detection, tests)
**Planning estimate:** 3.5d
**Owner:** Backend Engineering Patterns Owner; Data Model & Domain Schema Owner; Strategy Rules & System Intent Owner
**Sequencing:** Independent; the `strategy_rules.md` rule text is sub-step 1.
**UI-facing:** Yes
**Note:** Calibrated M → L (1.75d → 3.5d): the AC that P&L, R and the tax-year report use adjusted values is a sweep over every price consumer, and the item adds a `strategy_rules.md` rule, a migration, a nightly detection step and a Positions UI state. A case (c) `strategy_rules.md` write (`execution_prompt.md` §7).
**Scope:**
- `strategy_rules.md`: state how a split adjusts entry price, quantity, stop, ATR and the position's R (Strategy Rules & System Intent Owner; §12.3 change control)
- Record a split as an adjustment row against the position (ratio, effective date, source), not as an edit of the stored entry fields, so the original entry stays auditable (`data_model.md` migration block)
- Detect a split on a held ticker from the market-data provider's split history on the nightly run; until it is applied, suppress the stop-breach alert and exit recommendation for that position and show "Split detected — confirm adjustment" on Positions
- Apply the adjustment on confirmation; P&L, R and the tax-year report use adjusted values with the adjustment shown
**Acceptance Criteria:**
- `strategy_rules.md` names the split adjustment for entry, quantity, stop, ATR and R
- A fixture position with a 2:1 split on day D raises no stop breach and no exit recommendation on day D; Positions shows the "Split detected" state
- After confirmation, quantity × adjusted entry equals the original cost, and the stop is the original stop ÷ ratio
- The adjustment row records ratio, effective date and source; the original entry fields are unchanged
- Backend tests cover detection, suppression and the adjustment arithmetic, including a UK (`.L`) ticker
- *(restated)* The `strategy_rules.md` split rule is approved (dated) by the Strategy Rules & System Intent Owner under §12.3 change control before the build

### ST-28 — Tag lifecycle transitions caused by the v9.12 currency correction
**Source:** BLG-BE-179
**Priority:** P3
**Effort:** S (~0.5d)
**Planning estimate:** 0.5d
**Owner:** Head of Engineering; Metrics Definitions & Analytics Owner
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Mark transitions on the first post-deploy recompute with a reason such as `basis_correction`, or exclude them from days-in-state and lifecycle analytics
- Document the convention in `data_model.md`
**Acceptance Criteria:**
- Correction transitions are identifiable or excluded (unit test)

### ST-29 — Keep GET /settings working when the change-log read fails
**Source:** BLG-BE-181
**Priority:** P3
**Effort:** XS (<1h)
**Planning estimate:** 0.15d
**Owner:** Head of Engineering
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Wrap the `get_last_settings_change()` call so a failure logs a warning and returns `last_change: null`; the rest of the settings payload is unaffected
- Add a test: when `get_last_settings_change` raises, `GET /settings` returns 200 with the settings row and `last_change` null
**Acceptance Criteria:**
- With the change-log read raising, `GET /settings` returns 200 and the settings data, with `last_change: null` (test)
- The failure is logged at warning level or above

### ST-30 — Make the Reports unrealised P&L match the Positions basis
**Source:** BLG-SPEC-203
**Priority:** P3
**Effort:** S (~0.5d)
**Planning estimate:** 1d
**Owner:** Frontend Specifications & UX Documentation Owner
**Sequencing:** Independent; the direction (live or labelled snapshot) is sub-step 1.
**UI-facing:** Yes
**Note:** Calibrated 0.5d → 1.0d: option (a)'s AC is verified on staging.
**Scope:**
- Decide one direction: (a) compute the figure live via `get_positions_with_prices()`, or (b) keep the snapshot and add an explicit "as of last nightly update" caveat to `unrealised_note`
- Implement it, and update `reports.md` §Unrealised P&L Card
- Mark `DEV-REPORTS-ST06-01` resolved in `reports.md` Known Deviations
**Acceptance Criteria:**
- If (a): the Reports and Positions unrealised figures match at the same moment (verified on staging)
- If (b): the `unrealised_note` text states the snapshot time basis and is reviewed by the Head of UX & Design
- `DEV-REPORTS-ST06-01` is marked resolved, citing this item

### ST-31 — Cache the Trade Entry ATR preview per ticker and market
**Source:** BLG-FE-225
**Priority:** P3
**Effort:** S (~0.5 day)
**Planning estimate:** 0.5d
**Owner:** Frontend Specifications & UX Documentation Owner
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Move the preview to `useQuery` keyed on `["market-atr", normalisedTicker, market]` with a staleTime (e.g. 5 minutes), keeping the debounce and the idle/loading/ready/none states
**Acceptance Criteria:**
- Playwright: entering the same ticker twice within the staleTime issues one `GET /market/atr` request; SC-TAP-01..05 still pass

---

## EPIC-06 — Market-Data Reliability and CI

**Maps to:** S2-32 – S2-38
**Owner:** Infrastructure & Operations Owner; Head of Engineering; QA & Testing Owner
**Description:** Finish the on-demand Yahoo failure diagnosis, show 'earnings unknown' when a lookup fails, and fix the CI and staging gaps found in v9.12–v9.17.
**Estimated days:** 2.55

### ST-32 — Finish the on-demand Yahoo failure diagnosis (remainder)
**Source:** BLG-OPS-217
**Priority:** P2
**Effort:** S (~0.5d)
**Planning estimate:** 0.25d
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Sequencing:** Conditional (§1.4b): AC 2 needs 7 days of post-fix production data after PR #2259 merged 2026-11-13T15:11:51Z, so not before 2026-11-20. Before ST-33.
**UI-facing:** No
**Note:** Remainder only, 0.25d (Release Planning estimate: no remainder note was written at closure). Human-Delegation: production report.
**Scope:**
- Break the failures down by `endpoint` (provider path) and ticker from production `api_call_log` for each of the four features, and find the cause
- Fix what is broken, or document an expected failure (for example a symbol with no earnings data) so it is not counted as a provider failure
- Check what the user sees when these calls fail (earnings badge, gap-risk warning, positions prices, research)
- If the failure count changes materially, re-record §4's failure column from a new production weekly report
**Acceptance Criteria:**
- Each of the four features has a recorded cause for its failures
- After the fix, one production weekly report shows each feature's failure rate below 10%, or the remaining failures are documented as expected
- `data_pipeline_cost_baseline.md` §4 failures reflect the post-fix state, or state why they were kept
- *(restated — split-achievability remainder, v9.17 closure §6 row 1)* AC 1 was met in v9.17 ST-15. This story carries AC 2 (one post-fix production weekly report: each feature's failure rate below 10%, or the remaining failures documented as expected) and AC 3 (`data_pipeline_cost_baseline.md` §4 reflects the post-fix state)

### ST-33 — Show "earnings unknown" when an earnings or gap-risk lookup fails
**Source:** BLG-FE-294
**Priority:** P2
**Effort:** S (~0.5d)
**Planning estimate:** 0.5d
**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Sequencing:** After ST-32 if its cause changes which lookups fail; otherwise independent.
**UI-facing:** Yes
**Note:** Accepted P2 found defect (v9.17 Carry-Forward #2).
**Scope:**
- Backend: add a field (e.g. `data_status: ok | unavailable`) to `GET /earnings/{ticker}` and to the gap-risk response, so that a failed lookup is distinguishable from a successful lookup with no date (`earnings_endpoints.md`, `openapi.yaml`)
- Frontend: show "Earnings: unknown" on the badge and the gap-risk warning for `unavailable`, and do not cache an `unavailable` answer for the session
- Decide whether the Screener should skip earnings lookups for UK rows, and record the decision in the spec
**Acceptance Criteria:**
- A failed Yahoo lookup returns `data_status: unavailable`; a successful lookup with no upcoming date returns `ok` with a null date (unit tests)
- The Screener, Positions and Watchlist badges show "unknown" for `unavailable` and nothing for `ok` with a null date (Playwright)
- An `unavailable` answer is retried on the next render rather than cached for the session
- The UK-row decision is recorded in the spec

### ST-34 — Let the visual-baseline workflow push regenerated snapshots
**Source:** BLG-OPS-220
**Priority:** P3
**Effort:** XS (<1h)
**Planning estimate:** 0.15d
**Owner:** Infrastructure & Operations Owner
**Sequencing:** Early: EPIC-01–03 regenerate baselines.
**UI-facing:** No
**Note:** Tracks deferred lessons-learnt action `LL-v9.17-P3-03` (seated under §1.4c step 1a; see `run_manifest.md`).
**Scope:**
- Give the job `permissions: contents: write` (or document the repository setting it needs)
- Confirm the commit message it creates passes `.githooks`/`quality_gate.yml` on `exec/**` branches
**Acceptance Criteria:**
- A `workflow_dispatch` run on an `exec/**` branch with changed baselines pushes its commit and concludes `success`
- The workflow header comment states the permission it relies on

### ST-35 — Seed staging's UK positions with the .L suffix
**Source:** BLG-OPS-205
**Priority:** P3
**Effort:** XS (<1h)
**Planning estimate:** 0.5d
**Owner:** Infrastructure & Operations Owner; QA & Testing Owner
**Sequencing:** Independent. Staging write needs the user's permission.
**UI-facing:** No
**Note:** Calibrated XS → S (carried from v9.15): seed sweep plus a staging write.
**Scope:**
- Change the seed to `LGEN.L` and `BARC.L` (and any other UK ticker the seed scripts insert without the suffix)
- Correct the two existing staging rows, with the user's permission (staging write)
**Acceptance Criteria:**
- No seed script inserts a `market = 'UK'` ticker without `.L`
- After a staging reseed or correction, `GET /positions` on staging returns `price_is_stale: false` for both UK positions while Yahoo Finance is reachable

### ST-36 — Build the E2E bundle once per Playwright run
**Source:** BLG-OPS-206
**Priority:** P3
**Effort:** S (~0.5d)
**Planning estimate:** 0.5d
**Owner:** Infrastructure & Operations Owner; Head of Engineering
**Sequencing:** After ST-34 (both edit workflows).
**UI-facing:** No
**Scope:**
- Add one build job that produces the E2E bundle (same `REACT_APP_*` env as `webServer.env`) and uploads it as an artifact
- Have each shard download it and run only `npx serve -s build -l 3000`; keep the local `npm start` path unchanged
**Acceptance Criteria:**
- The 8 shards no longer run `npm run build`, and the E2E suite still passes in CI
- The before and after Playwright E2E wall time and runner time are recorded in `docs/ops/ci_runtime_audit_2026-10-30.md` or `ci_pipeline_baseline.md`

### ST-37 — Keep a bare root pytest out of the mutmut pilot tests
**Source:** BLG-QA-225
**Priority:** P3
**Effort:** XS (<0.5d)
**Planning estimate:** 0.15d
**Owner:** QA & Testing Owner
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Make a bare root `pytest` collect only `tests/` (for example a root pytest config with `testpaths = tests`), confirming that `cd backend && python3 -m mutmut run` still selects `mutmut_pilot_tests/test_pilot.py` with the same rootdir and node IDs
- Or make the pilot's conftest restore `sys.modules["database"]`, if the config route breaks mutmut
**Acceptance Criteria:**
- `backend/.venv/bin/python3 -m pytest --collect-only -q` from the repo root exits 0
- The mutmut pilot's pytest selection still collects its tests from `backend/`

### ST-38 — Run the settings change-log SQL against real Postgres in CI
**Source:** BLG-QA-226
**Priority:** P3
**Effort:** S (~0.5d)
**Planning estimate:** 0.5d
**Owner:** Director of Quality; Head of Engineering
**Sequencing:** After ST-29 (same settings path).
**UI-facing:** No
**Scope:**
- In Phase B, create `settings` and the DS-33 `settings_change_log` table (from `data_model.md` DS-33) and run `create_settings` / `update_settings` / `get_last_settings_change` against it
- Skip cleanly when no real `DATABASE_URL` is available, as the existing Phase A/B split expects
**Acceptance Criteria:**
- A Phase B test saves settings twice against real Postgres and asserts the log rows (field, old, new, source, shared `batch_id`) and the `last_change` payload
- A deliberately broken column name in the insert makes that test fail in CI

---

## EPIC-07 — AI Output Boundary

**Maps to:** S2-39 – S2-40
**Owner:** AI Compliance & Governance Officer; Product Owner; Backend Engineering Patterns Owner
**Description:** Enforce §13.2's AI-text sentence on the daily briefing and chat, and decide whether the post-trade debrief may say more than one restating sentence.
**Estimated days:** 1.00

### ST-39 — Check daily briefing and chat output against §13.2
**Source:** BLG-AI-29
**Priority:** P3
**Effort:** S (~0.5d)
**Planning estimate:** 0.5d
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Sequencing:** Ruling first.
**UI-facing:** No
**Scope:**
- Ask the AI Compliance & Governance Officer which check forms apply to the briefing and chat (briefing actions such as EXIT/HOLD are deterministic outputs, not parameter changes), and how a failure is handled (note, regenerate or fallback)
- Implement the ruled check and log its result in `claude_audit_log.compliance_check_result`
- Add B-DB/B-CH scenarios to `ai_s13_boundary_test_suite.md`
**Acceptance Criteria:**
- The ruling is recorded before the code change
- A briefing or chat output suggesting tightening stops gets the ruled handling, in a test; a deterministic EXIT/HOLD action does not
- Every existing briefing and chat test passes
- *(restated — §13 clause-citation rule)* The ruling and test cite `strategy_rules.md` §13.2 (the AI-text sentence naming the daily briefing and chat) and the §13.5 attestation table row for the BLG-FEAT-50/51 §13 review (`decisions--2026-06-24__release-v6.2--BLG-FEAT-50-51-section13-review.md`), and answer each

### ST-40 — Decide whether the debrief may say more than one restating sentence
**Source:** BLG-GOV-378
**Priority:** P3
**Effort:** S (~0.5d)
**Planning estimate:** 0.5d
**Owner:** AI Compliance Governance Officer; Product Owner
**Sequencing:** Independent. Needs a sample of real (production) debriefs.
**UI-facing:** No
**Note:** Decision story; any implementation is filed as its own item.
**Scope:**
- Once BLG-BE-152 ships, review a sample of real debriefs.
- Decide whether to keep the current limits, or to allow 2–3 observational sentences (still non-prescriptive and number-checked) covering what went well as well as what differed.
- If changed, record the ruling as an amendment to the §13 review and file the implementation item.
**Acceptance Criteria:**
- A recorded decision (keep or amend), with rationale, from the AI Compliance Governance Officer and Product Owner
- *(restated — §13 clause-citation rule)* The decision cites `strategy_rules.md` §13.2 (the AI-text sentence naming the post-trade debrief) and the §13.5 attestation table row for the ST-06 debrief §13 review (`decisions--2026-08-17__release-v8.9--ST-06-section13-review.md`, CONDITIONAL), and answers each
