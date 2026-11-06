Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-06
Cycle: 2026-11-06__release-v9.16
Release: v9.16

# Backlog Slice — v9.16

<!-- release-plan-marker: RP:v9.16:2026-11-06__release-v9.16 -->

30 stories across 7 EPICs, 27.95 estimated days. The acceptance criteria below are the source of truth for Sprint Planning and Execution. Scope is sized to the top of the confirmed ~24–28 day capacity band, per the explicit user instruction "use full capacity" (2026-11-06).

**Ready pool:** 159 items, 84.70 days (after the STEP 4 calibration raises, applied to the whole pool before selection).

**Selection method** (`release_planning_prompt.md` §1.4c, v2.72):
0. **Programme-phase hold (step 0, first use):** the 8 Site Structure & Usability Phase 3 items (`BLG-FE-257`–`263`, `265`; provisional v9.17) are held out of the pool, including the Phase 3 P2 `BLG-FE-260`.
1. The ready P1 item, `BLG-OPS-214`, then the ready P2 items in ascending ID order: `BLG-FE-250`, `254`, `255`, `256`, `264`, `271` and `BLG-OPS-213`.
2. **Product Owner override (user decision in session, 2026-11-06):** the three Phase 2 P3 items `BLG-FE-251`, `252` and `253` are seated with the Phase 2 P2s, so Phase 2 ships complete in the release named for it.
3. Step 1a, deferred lessons-learnt patch items targeted at v9.16: `BLG-GOV-413`.
4. A category-balanced, oldest-first round-robin over P3/P4, run until 0.05 days were left.

**Where an item's own AC is stale, untestable, missing or points at text outside the slice, the AC below restates it.** Each change from the source backlog item is marked *(restated)* with the reason. Scope bullets are copied from the source item for convenience; the source item stays authoritative for Problem text.

**Gates cleared this run (§1.3a, gating item shipped, disposition (a)):** `BLG-FE-39`, `BLG-QA-21`, `BLG-QA-22`, `BLG-QA-23` and `BLG-GOV-26`. Each gate named only PT-04 shipping (v6.1) and, for three, Arc 2 being complete (v3.1–v6.1). Each item's AC that names the gate is restated below (ST-24–ST-27, ST-29).

**`strategy_rules.md` writes (case (c), `execution_prompt.md` §7):** ST-05 closes the §4.2.1 Known deviation added at v1.26 for `BLG-FE-271`. Writing that closure in-sprint needs the Strategy Rules & System Intent Owner's confirmation of ST-05 AC 4 in the sealed `sprint_backlog.md` sign-off summary (RISK-02).

**§13 clause-citation rule (v2.61):** no seated AC requires a §13 review, determination or sign-off.

**Post-merge, production and console ACs (Sprint Planning STEP 6.2):** ST-11 and ST-12 need the Anthropic console, Render and GitHub secret access. ST-13 and ST-14 need production reads after a date. ST-19 needs the production log token list. ST-28 AC 2 is met at the next `groom backlog`. Sprint Planning marks each `post-merge` with a named tracking item before the seal.

**Conditional stories (§1.4b):** ST-13 (`BLG-OPS-197`, earliest clear 2026-11-09) and ST-14 (`BLG-OPS-198`, about 2026-11-12). Both dates fall inside the sprint window.

---

## EPIC-01 — Site Structure & Usability Phase 2: Navigation & Wayfinding (build-and-ship)

**Maps to:** S2-01 – S2-04
**Owner:** Head of Engineering; Head of UX & Design
**Description:** Build `navigation.md` v2 (approved at v9.15, `BLG-SPEC-214`): a job-based sidebar that surfaces Trade Plans and Research, a parent link on every detail page, an onward link on each of the eight dead-end pages, and a section-anchored digest link.
**Estimated days:** 6.00

### ST-01 — Build the job-based sidebar and surface Trade Plans and Research
**Source:** BLG-FE-250
**Priority:** P2
**Effort:** M (~2-3 days)
**Owner:** Head of Engineering; Head of UX & Design
**Sequencing:** First in EPIC-01. ST-02 and ST-03 follow, since they use the v2 areas.
**UI-facing:** Yes
**Scope:**
- Implement `navigation.md` v2's areas, placement and default-expanded groups on desktop and the mobile drawer
- Add Trade Plans and Research entry points
**Acceptance Criteria:**
- Sidebar matches `navigation.md` v2 on desktop and mobile
- Trade Plans is reachable from the sidebar in one click
- `alert-nav-badge.spec.js`, `command-palette.spec.js`, `keyboard-shortcuts.spec.js` updated and passing

### ST-02 — Add a parent link on detail pages
**Source:** BLG-FE-251
**Priority:** P3
**Effort:** S (~1 day)
**Owner:** Head of Engineering
**Sequencing:** After ST-01.
**UI-facing:** Yes
**Scope:**
- A parent link (or breadcrumb) on each detail page per `navigation.md` v2 (Trade Plan, Research `/research/:ticker`, Notification Preferences, Notification History)
**Acceptance Criteria:**
- Each listed page shows a parent link that navigates correctly; Playwright coverage passes

### ST-03 — Give each dead-end page an onward next-step link
**Source:** BLG-FE-252
**Priority:** P3
**Effort:** M (~2 days)
**Owner:** Head of Engineering; Head of UX & Design
**Sequencing:** After ST-01.
**UI-facing:** Yes
**Scope:**
- Add the onward link(s) `navigation.md` v2 assigns to each of the eight dead-end pages (Reports, Red Flag Journal, Trade Reflections, Replay, Strategy Benchmark, Ticker Universe, System Status, Notification History)
**Acceptance Criteria:**
- A re-run of the inter-page link scan finds 0 dead-end pages; each new link has Playwright coverage

### ST-04 — Anchor the digest's Risk Dashboard link to the right section
**Source:** BLG-FE-253
**Priority:** P3
**Effort:** S (~0.5 day)
**Owner:** Head of Engineering
**Sequencing:** Independent.
**UI-facing:** Yes
**Scope:**
- Support a section query (e.g. `?section=pre-entry-validation`) that scrolls to the section; use it in the digest's deep link
**Acceptance Criteria:**
- Opening the section link scrolls the named section into view; Playwright coverage passes; digest link updated

---

## EPIC-02 — Site Structure & Usability Phase 2: Today List & Signal-to-Entry Flow (build-and-ship)

**Maps to:** S2-05 – S2-08
**Owner:** Head of Engineering; Head of UX & Design; Frontend Specifications & UX Documentation Owner; Strategy Rules & System Intent Owner
**Description:** Build the Dashboard "Today" list from `dashboard.md` v4.0 §1B, shorten the path from a signal to a checked entry ("Plan this", suggested size on Trade Plan), and close the plan-linked acknowledgement gap ruled at `ESC-CLOSE-20261106-01`.
**Estimated days:** 7.75

### ST-05 — Require the acknowledgement on plan-linked Trade Entry when the plan's checks were WARN/FAIL
**Source:** BLG-FE-271
**Priority:** P2
**Effort:** S (~0.5-1d)
**Owner:** Frontend Specifications & UX Documentation Owner; Strategy Rules & System Intent Owner
**Sequencing:** First in EPIC-02 (accepted v9.15 P2 found gap). Same Trade Entry pre-entry panel as v9.15 ST-01.
**UI-facing:** Yes
**Scope:**
- When the plan's stored snapshot holds a WARN/FAIL with no recorded acknowledgement, or is older than a set age, show the panel on Trade Entry (re-run the checks) instead of the on-plan line, with the same Branch A gating and override event
- Update `position_form.md` §Pre-Entry Checks and the `trade-entry-pre-entry-checks` design record
**Acceptance Criteria:**
- *(restated: the source's AC 1, "A dated ruling is recorded", is met by `ESC-CLOSE-20261106-01`, Strategy Rules & System Intent Owner, 2026-11-06, option (a): §4.2.1 v1.23 applies to the plan-linked route. The source's AC 2 condition "If the ruling applies the rule" is therefore met and dropped.)*
- A plan-linked entry whose snapshot has an unacknowledged WARN/FAIL (or is older than the age set in `position_form.md`) shows the panel once and disables Submit until it is acknowledged; a plan whose checks all passed still shows only the on-plan line (Playwright)
- Saving after the acknowledgement writes one `pre_entry_override` event (`source: trade_entry`) (backend test)
- *(restated: closes the Known deviation that the v1.26 ruling filed)* The §4.2.1 Known deviation (v1.26) is marked resolved as a documentation-only `strategy_rules.md` version, with its `DOCUMENTATION_ONLY_VERSIONS` registry entry. The write is valid only under `execution_prompt.md` §7 case (c), with the Strategy Rules & System Intent Owner's dated confirmation of this AC line in the sealed `sprint_backlog.md` sign-off summary. Without it, the closure is routed to Post-Ship Closure STEP 5 and this AC is met by that routing note

### ST-06 — Build the "Today" action list on the Dashboard
**Source:** BLG-FE-254
**Priority:** P2
**Effort:** L (~3-4 days)
**Owner:** Head of Engineering; Head of UX & Design
**Sequencing:** Independent within EPIC-02. Merges before EPIC-03's ST-09, which regenerates the Dashboard visual baselines (RISK-03).
**UI-facing:** Yes
**Scope:**
- Implement `dashboard.md` v4.0's revised "Today" list (§1B), ordering, quiet-day state and the moved/merged cards
**Acceptance Criteria:**
- Every observable AC in the revised `dashboard.md` (TL-01..TL-29) has Playwright coverage that passes, in light and dark themes, *(restated: `dashboard.md` §1B "Data dependency (Stops moved)")* except TL-09 and TL-10. The Stops moved group needs `stop_last_moved_date`/`previous_stop` from `BLG-BE-205`, which is not seated, so the group is not rendered and its two ACs are not testable this release
- The Stops moved group does not render, and no placeholder for it is shown, while `GET /positions` lacks `stop_last_moved_date` (Playwright)

### ST-07 — Add "Plan this" to Signals and Screener rows
**Source:** BLG-FE-255
**Priority:** P2
**Effort:** M (~2-3 days)
**Owner:** Head of Engineering; Head of UX & Design
**Sequencing:** Before ST-08 (both change the Trade Plan entry path; ST-08 edits `TradePlan.js`).
**UI-facing:** Yes
**Scope:**
- A "Plan this" action on Signals and Screener rows that opens Trade Plan pre-filled with ticker, market, price and signal context (`SignalContextPanel` already exists)
**Acceptance Criteria:**
- From a Signals row and a Screener row, "Plan this" opens a pre-filled Trade Plan in one click; Playwright coverage passes

### ST-08 — On Trade Plan, show the suggested size before asking for shares
**Source:** BLG-FE-256
**Priority:** P2
**Effort:** S (~1 day)
**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner
**Sequencing:** After ST-07.
**UI-facing:** Yes
**Scope:**
- Show the §4.1 suggested size above the shares field and pre-fill the field from it once entry and stop are known; keep it editable
**Acceptance Criteria:**
- With entry and stop entered, the shares field pre-fills with the §4.1 suggestion; Playwright coverage passes

---

## EPIC-03 — Site Structure & Usability Phase 2: Colour Tokens & Input Contrast (build-and-ship)

**Maps to:** S2-09 – S2-10
**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Description:** Introduce semantic light/dark colour tokens for the base, card and table shells, the Phase 2 foundation for Phase 3's token sweep (`BLG-FE-265`), and fix the input placeholder/typed-text dark-mode pair.
**Estimated days:** 3.00

### ST-09 — Semantic colour tokens for the base, card and table shells
**Source:** BLG-FE-264
**Priority:** P2
**Effort:** M (~2-3 days)
**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Sequencing:** EPIC-03 merges after EPIC-01 and EPIC-02, so the regenerated baselines include their changes (RISK-03).
**UI-facing:** Yes
**Scope:**
- Define semantic tokens (surface, surface-raised, text, text-muted, border, positive, negative, warning) for light and dark in `tailwind.config.js`/`index.css`
- Convert the body base, `DashboardCard`, `DataTable` and `PageHeader` shells to them; update `design_system.md`
**Acceptance Criteria:**
- axe `color-contrast` passes in the light theme on Dashboard, Positions (empty and populated), Trade Plan and Settings
- Visual baselines regenerated for both themes

### ST-10 — Inputs apply dark:text-slate-400 to typed text instead of the placeholder
**Source:** BLG-FE-223
**Priority:** P3
**Effort:** S (~0.5 day; held at 0.5d, count named at v9.14: 18 occurrences in 8 files under `src/`)
**Owner:** Frontend Specifications & UX Documentation Owner
**Sequencing:** After ST-09 if it adopts the new text tokens; otherwise independent.
**UI-facing:** Yes
**Scope:**
- Replace with `placeholder:text-slate-600 dark:placeholder:text-slate-400` and an explicit typed-text pair (`text-slate-900 dark:text-white`, or ST-09's text token) across `src/`
**Acceptance Criteria:**
- No input class string uses a bare `dark:text-*` intended for its placeholder (grep check); typed text passes contrast in both themes

---

## EPIC-04 — Anthropic Key Security & Operations Baselines

**Maps to:** S2-11 – S2-15
**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner; FinOps & Resource Architect
**Description:** Rotate the overdue Anthropic key and stop shipping a key copy in the public Pages build (v9.15 closure Carry-Forward #1: the accepted P1 and P2 from ST-29). Record the two production baselines left pending since v9.13, and harden the staging smoke host check.
**Estimated days:** 1.10

### ST-11 — Rotate the Anthropic API key (overdue since 2026-08-25) and revoke the old key
**Source:** BLG-OPS-214
**Priority:** P1
**Effort:** XS (<1h)
**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Delegation note:** Human-Delegation: the Anthropic console, Render environment and GitHub secret steps need the user.
**Sequencing:** First in the sprint (P1). Run with ST-12: ST-12 removes the Pages build's use of the GitHub secret, then this story revokes the old key once.
**UI-facing:** No
**Scope:**
- Create a new key in the Anthropic console; set it as `ANTHROPIC_API_KEY` on Render staging, check one AI endpoint, then production
- Revoke the old key in the console
- Delete the `REACT_APP_ANTHROPIC_API_KEY` GitHub secret (or replace it with a non-secret flag, per ST-12)
- Record the rotation date in `docs/ops/external_api_credential_inventory.md` (`Last rotated`) and `docs/ops/api_key_rotation_and_audit_schedule.md`
**Acceptance Criteria:**
- The console lists one active key, created on the rotation date; the 2026-05-25 key is revoked
- An AI endpoint succeeds on staging and production with the new key
- The inventory's `Last rotated` field and the schedule's next-due date are filled in

### ST-12 — Stop injecting REACT_APP_ANTHROPIC_API_KEY into the public GitHub Pages build
**Source:** BLG-OPS-213
**Priority:** P2
**Effort:** S (~0.5d)
**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Delegation note:** Human-Delegation for the secret deletion and console revocation; the code change is autonomous.
**Sequencing:** With ST-11 (see ST-11).
**UI-facing:** Yes (Trade Plan AI controls must behave as before)
**Scope:**
- Replace `HAS_AI` with a non-secret flag, or remove it if AI is always available through the backend
- Remove `REACT_APP_ANTHROPIC_API_KEY` from `deploy.yml` and delete the GitHub secret
- If the secret held a live key, revoke it in the Anthropic console
**Acceptance Criteria:**
- `grep -rn REACT_APP_ANTHROPIC .github src` finds nothing
- `gh secret list` no longer lists `REACT_APP_ANTHROPIC_API_KEY`
- Any key the secret held shows as revoked in the Anthropic console
- The Trade Plan AI controls behave as before (Playwright or a recorded staging check)

### ST-13 — Record the weekly market-data call-volume baseline from production
**Source:** BLG-OPS-197
**Priority:** P3
**Effort:** XS (<1h)
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Delegation note:** Human-Delegation: production reads.
**Classification:** Conditional (§1.4b). Earliest clear date 2026-11-09 (7 days of production data after the 2026-11-02 deploy). Promote to firm only on a dated confirmation. Returned once before (v9.15 ST-33).
**Sequencing:** Independent; not before 2026-11-09.
**UI-facing:** No
**Scope:**
- After the production deploy, run DS-36's Verification query on production and record it in `data_model.md` DS-36
- 7 full days after deploy, call `GET /ops/api-call-attribution?window=weekly` on production and fill §4's calls and failures per source, with the date and `top_contributors`
- Close `DEL-20261027-04` and `DEL-20261027-06`
**Acceptance Criteria:**
- DS-36 Live Confirmation for production is recorded: `api_call_log.feature` text YES, `screener_runs.duration_seconds` numeric YES, index `idx_acl_called_at_feature`
- `data_pipeline_cost_baseline.md` §4 has weekly calls and failures for each source and combined, from one production weekly report, with its date and `top_contributors` (3 features, or every feature with calls if fewer than 3 made any); the §6 volume sign-off line is ticked

### ST-14 — Record the full screener run p50/p95 baseline from production
**Source:** BLG-OPS-198
**Priority:** P3
**Effort:** XS (<1h)
**Owner:** Infrastructure & Operations Owner
**Delegation note:** Human-Delegation: production API key for the benchmark script.
**Classification:** Conditional (§1.4b). Needs at least 10 nightly production screener runs after the 2026-11-02 deploy, about 2026-11-12. Promote to firm only on a dated confirmation.
**Sequencing:** Independent; not before 10 qualifying runs exist.
**UI-facing:** No
**Scope:**
- After at least 10 nightly production runs, run `API_URL=<production> API_KEY=<key> python3 scripts/screener_run_benchmark.py`
- Record its output (runs counted, min tickers, p50, p95, regression threshold, first and last run) in `api_performance_baseline.md` §53
- Close `DEL-20261027-05`
**Acceptance Criteria:**
- The script exits 0 (at least 10 qualifying runs) and its p50, p95 and 1.5× threshold in seconds are recorded in `api_performance_baseline.md` §53 with the run date range

### ST-15 — Fail the staging smoke host check when the backend reports no Render service ID
**Source:** BLG-OPS-199
**Priority:** P3
**Effort:** XS (<1h)
**Owner:** Infrastructure & Operations Owner
**Sequencing:** Independent. Its dependency, `BLG-OPS-196` (first green staging deploy on `main` showing the host check pass), is complete.
**UI-facing:** No
**Scope:**
- Make a missing `render_service_id` a failure, now that `BLG-OPS-196` has shown the field on staging
- Read the expected service ID from `STAGING_SERVICES`
- Update `tests/test_staging_smoke_test.py`
**Acceptance Criteria:**
- A `/health/detailed` response without `render_service_id` fails the smoke test (test)
- The expected service ID has one definition in the repo

---

## EPIC-05 — Backend Correctness, AI Ticker Check & Spec Debt

**Maps to:** S2-16 – S2-23
**Owner:** Head of Engineering; Backend Engineering Patterns Owner; AI Compliance & Governance Officer; Data Model & Domain Schema Owner; API Contracts & Documentation Owner; Frontend Specifications & UX Documentation Owner
**Description:** Three US-position NULL-field robustness fixes from v9.12, the briefing ticker-caveat follow-ups from v9.15 ST-24/ST-26, and three small spec-debt corrections aged 2+ ready pools.
**Estimated days:** 1.20

### ST-16 — Exiting a US position with a NULL fill_price fails in the P&L arithmetic
**Source:** BLG-BE-175
**Priority:** P3
**Effort:** XS (<0.5d)
**Owner:** Head of Engineering
**Sequencing:** Before ST-17 (same `native_entry_price()` fallback).
**UI-facing:** No
**Scope:**
- Use `native_entry_price(position, <stored fx_rate, else the exit fx_rate>)` in `exit_position()`
- Add a unit test for a US exit with a NULL `fill_price`
**Acceptance Criteria:**
- A US position with a NULL `fill_price` exits without error, and its realised P&L uses `entry_price × fx_rate` as the native entry (unit test)

### ST-17 — Lifecycle badge and Risk page disagree for a US row with no fill_price and no fx_rate
**Source:** BLG-BE-176
**Priority:** P3
**Effort:** XS (<0.5d)
**Owner:** Head of Engineering
**Sequencing:** After ST-16.
**UI-facing:** No
**Scope:**
- Use one fallback on all paths (either all UNKNOWN, or all live-rate), decided against `position_endpoints.md`'s `position_state` field note
- Add a unit test for this row
**Acceptance Criteria:**
- For a US row with NULL `fill_price` and NULL `fx_rate`, `display_status` and `position_state` agree (unit test)

### ST-18 — Frozen-stop marker is not written when the on-load recompute has no live price
**Source:** BLG-BE-177
**Priority:** P3
**Effort:** XS (<0.5d)
**Owner:** Head of Engineering
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Write the marker when the stop is kept for lack of ATR even without a live price, or document the exclusion in `position_endpoints.md`
**Acceptance Criteria:**
- Unit test: no live price and no ATR, post-grace → `stop_frozen_reason = 'atr_unavailable'` (or the contract states the exclusion)

### ST-19 — Read production briefing ticker-caveat tokens and add any non-tickers
**Source:** BLG-AI-27
**Priority:** P3
**Effort:** XS (<1h plus tests)
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Delegation note:** Human-Delegation: the user supplies the token list from production Render logs, or grants a one-off read.
**Sequencing:** Before ST-20 (ST-20's collision ruling may apply to tokens found here).
**UI-facing:** No
**Scope:**
- The user supplies the token list with counts since 2026-10-30, or grants a one-off read
- Classify each token as ticker or non-ticker
- Add the non-tickers to `_NON_TICKER_WORDS` (ruling `ESC-EXEC-20261027-02` (B) condition 2 is a minimum list) and to the `ai_endpoints.md` check 3 list
**Acceptance Criteria:**
- The token list with counts is recorded
- Each non-ticker found is added and covered by `test_non_ticker_words_ignored`, or the review records that none was found

### ST-20 — Handle `_NON_TICKER_WORDS` entries that are also real tickers deliberately
**Source:** BLG-AI-28
**Priority:** P3
**Effort:** XS (<1h plus tests)
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Delegation note:** delegated_decision first sub-step: AI Compliance & Governance Officer ruling on collisions.
**Sequencing:** After ST-19.
**UI-facing:** No
**Scope:**
- Ask the AI Compliance & Governance Officer how to treat collisions: for example, AM/PM count as non-tickers only after a time digit, or a word that is in the scan universe goes to the focus rule's "other ticker" path
- Implement the ruling for PM, MA and ON (and any other universe collision), with tests
- State the collision handling in `ai_endpoints.md` check 3 and in the chat focus paragraph
**Acceptance Criteria:**
- The ruling is recorded before the code change
- With focus `MU` held and PM not held, "PM's stop was hit last week." gets the result the ruling assigns, in a test; "Your stop was hit at 3 PM." still gets the MU note
- All v9.14 ST-16, ST-17 and v9.15 ST-26 tests pass *(restated: the source names ST-16/ST-17/ST-26 without their cycles)*

### ST-21 — Journal summary: remove the stale AI_MODEL override line, or cost the model actually used
**Source:** BLG-SPEC-195
**Priority:** P4
**Effort:** XS (<1h)
**Owner:** API Contracts & Documentation Owner; Backend Engineering Patterns Owner
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Remove the `AI_MODEL` override sentence from the contract (or implement the override and cost by model)
- If a non-Haiku model can ever be passed, select the cost rates by model in `_audit_journal_summary_call()`
**Acceptance Criteria:**
- The contract describes only model selection that exists in code
- A test pins the cost rates to the model used, or the contract states the endpoint is Haiku-only

### ST-22 — Add the 11 missing positions columns to the positions data dictionary
**Source:** BLG-SPEC-200
**Priority:** P4
**Effort:** XS (<1h)
**Owner:** Data Model & Domain Schema Owner
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Add a dictionary row for each of the 11 columns (SQL type, Nullable, description), taken from `data_model.md` §2 and its DS-xx migration sections, in the matching §3.x subsection
- Decide whether to remove the `exit_note` row or keep it as a marked historical row
- Remove the v0.5 coverage note once every column is listed; version bump
**Acceptance Criteria:**
- Every column in `data_model.md` §2's Fields table has a dictionary row, with the same type and Nullable value
- The dictionary lists no column that `data_model.md` §2 does not, other than an explicitly marked historical row

### ST-23 — Point settings.md at the moved strategy constants module
**Source:** BLG-SPEC-201
**Priority:** P4
**Effort:** XS (<1h)
**Owner:** Frontend Specifications & UX Documentation Owner
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Replace the path in `settings.md` with `src/constants/strategy.js`; version bump and changelog row
**Acceptance Criteria:**
- `settings.md` names `src/constants/strategy.js`, and no canonical spec under `docs/specs/` names `src/lib/strategyParameters.js`

---

## EPIC-06 — Arc 2 Retrospective: QA Protocol, Lifecycle Test & Journey Map

**Maps to:** S2-24 – S2-27
**Owner:** QA Lead; Head of Specs Team; Head of UX & Design; Product Owner
**Description:** Four items filed 2026-05-21 and gated on PT-04 shipping, which happened at v6.1 and completed Arc 2. Their gates were cleared this run (§1.3a). The arc-level QA protocol, the DoQ standards review, a full trade-plan lifecycle Playwright test and the Arc 2 journey map. Each reflects the app as it is after EPIC-02's Trade Plan changes, not as it was at v6.1.
**Estimated days:** 6.50

### ST-24 — Arc 2 end-to-end QA protocol
**Source:** BLG-QA-21
**Priority:** P3
**Effort:** M (~2 days)
**Owner:** QA Lead
**Sequencing:** After ST-26 (the protocol's Playwright happy path can reuse ST-26's lifecycle test).
**UI-facing:** No
**Scope:**
- Arc-level E2E test protocol document covering the full Arc 2 flow (Screener, Research View, Trade Plan, Setup Quality Score)
- Playwright automation for the core arc-level happy path
- Manual checklist for Arc 2 edge cases not covered by Playwright
**Acceptance Criteria:**
- Arc 2 E2E protocol document produced and filed in `docs/qa/`
- Core happy path covered by Playwright
- *(restated: the gate was cleared at Release Planning `2026-11-06__release-v9.16`, citing PT-04 ✅ Shipped v6.1 and Arc 2 ✅ Fully Complete in `current_roadmap.md`)* The QA Lead and Product Owner confirm at the sprint planning seal that the cleared gate's evidence holds; no other gate check applies

### ST-25 — Arc 2 DoQ standards review
**Source:** BLG-QA-22
**Priority:** P3
**Effort:** S (~1 day)
**Owner:** QA Lead; Head of Specs Team
**Sequencing:** Independent. If it amends `shared_standards.md`, coordinate the version bump with ST-28 (RISK-07).
**UI-facing:** No
**Scope:**
- Review DoQ standards against Arc 2 EPIC QA evidence files
- Identify any rubric gaps introduced by Arc 2 feature types
- Propose amendments to `shared_standards.md` DoQ section if warranted
**Acceptance Criteria:**
- DoQ standards reviewed; gaps (if any) documented
- If amendments warranted: `shared_standards.md` updated per the CLAUDE.md §6 governance checklist
- *(restated: the gate was cleared at Release Planning `2026-11-06__release-v9.16`, citing PT-04 ✅ Shipped v6.1 and Arc 2 ✅ Fully Complete)* The QA Lead confirms at the sprint planning seal that the cleared gate's evidence holds

### ST-26 — Trade plan lifecycle end-to-end test
**Source:** BLG-QA-23
**Priority:** P3
**Effort:** M (~2 days)
**Owner:** QA Lead
**Sequencing:** After EPIC-02's ST-07 and ST-08 are merged (they change how a Trade Plan is created and sized).
**UI-facing:** No (test only)
**Scope:**
- Playwright E2E test: create plan with quality score visible → link to position → close position → verify plan-vs-reality
- Cover: plan state transitions, quality score persistence, plan-vs-reality accuracy
**Acceptance Criteria:**
- Full lifecycle Playwright test authored and passing in CI
- *(restated: the gate was cleared at Release Planning `2026-11-06__release-v9.16`, citing PT-04 ✅ Shipped v6.1)* The QA Lead and Product Owner confirm at the sprint planning seal that the cleared gate's evidence holds

### ST-27 — Arc 2 user journey map
**Source:** BLG-FE-39
**Priority:** P3
**Effort:** M (~1–2 days)
**Owner:** Head of UX & Design
**Sequencing:** After ST-07 (the map should show the "Plan this" route).
**UI-facing:** No (design document)
**Scope:**
- User journey map covering screener discovery → trade plan creation → execution
- Identify friction points and hand-off gaps between views
- Produce design recommendation: maintain current or file targeted UX improvement items
**Acceptance Criteria:**
- Journey map document produced *(restated: in `docs/ux/`, alongside `si05_user_journey_map.md`)*
- Friction points enumerated; any actionable items filed as backlog entries, cross-checked against the Site Structure & Usability programme items so no duplicate is filed
- *(restated: the gate was cleared at Release Planning `2026-11-06__release-v9.16`, citing PT-04 ✅ Shipped v6.1)* The Product Owner confirms at the sprint planning seal that the cleared gate's evidence holds

---

## EPIC-07 — Governance Process

**Maps to:** S2-28 – S2-30
**Owner:** Head of Specs Team; PMO Lead; Base44 Frontend Prompt Owner
**Description:** Apply the v9.15 deferred lessons-learnt patch for split-achievability closures (§1.4c step 1a), plus two legacy governance items: an Arc 2 velocity report (gate cleared this run) and a Base44 prompt versioning convention.
**Estimated days:** 2.40

### ST-28 — Split-achievability carve-out: close a source item whose whole remainder has its own backlog items
**Source:** BLG-GOV-413
**Priority:** P3
**Effort:** XS (<1h)
**Owner:** Head of Specs Team; PMO Lead
**Sequencing:** Early in EPIC-07 (deferred lessons-learnt patch, §1.4c step 1a). Bumps `post_ship_closure.md` and `OPERATIONAL_GUIDE.md`; see RISK-07.
**UI-facing:** No
**Scope:**
- In `post_ship_closure.md` STEP 3.1, distinguish (i) a remainder tracked only by an escalation or by the source item itself (keep open, as now) from (ii) every unmet AC moved to a named follow-up backlog item filed this cycle (banner the source item ✅ COMPLETE, naming the follow-up items)
- Apply the CLAUDE.md §6 checklist
**Acceptance Criteria:**
- STEP 3.1 states both cases, citing `BLG-AI-23`/`BLG-AI-27` as the case (ii) example
- `BLG-AI-23` and `BLG-OPS-48` are bannered or given a recorded reason to stay open at the next `groom backlog` after the change *(post-merge: met at the next `groom backlog`; Sprint Planning names the tracking item)*

### ST-29 — Arc velocity tracking dashboard
**Source:** BLG-GOV-26
**Priority:** P3
**Effort:** S (~1 day)
**Owner:** PMO Lead
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Arc velocity report: stories/cycle, epic completion rate, arc-level rolling velocity
- Filed in governance reporting; updated at arc close
- Input to release planning engine for arc-boundary cycles
**Acceptance Criteria:**
- *(restated: Arc 2 closed at v6.1, before this item was seated)* An Arc 2 velocity report covering v3.1–v6.1 is produced from `claude/cycles/velocity_metrics.md` and the cycle records
- Report format reusable for Arc 3+
- *(restated: the gate was cleared at Release Planning `2026-11-06__release-v9.16`, citing PT-04 ✅ Shipped v6.1 and Arc 2 ✅ Fully Complete)* The PMO Lead confirms at the sprint planning seal that the cleared gate's evidence holds
- *(restated: the source's "Input to release planning engine" Scope bullet)* Any change to a governance prompt that makes the report a Release Planning input follows CLAUDE.md §6 in the same commit; otherwise it is filed as a backlog item

### ST-30 — Base44 prompt versioning convention
**Source:** BLG-GOV-198
**Priority:** P3
**Effort:** S (~0.5-2 days)
**Owner:** Base44 Frontend Prompt Owner
**Delegation note:** delegated_decision first sub-step: the Base44 Frontend Prompt Owner chooses the convention.
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:** *(restated: the item has a Proposed solution but no AC)*
- A dated decision names the convention: where the ST-id is recorded for each Base44 prompt draft (a comment header, a delegation log field, or both)
- The convention is written into the place `delegated_frontend` drafts are specified (`OPERATIONAL_GUIDE.md` frontend delegation text and/or `execution_prompt.md`) under the CLAUDE.md §6 checklist in the same commit, or, if no governance file changes, into `claude/agents/base44_frontend_prompt_owner.md`'s working notes
- One existing delegation log entry with a Base44 draft is shown to satisfy the convention, or a dry-run example is recorded
