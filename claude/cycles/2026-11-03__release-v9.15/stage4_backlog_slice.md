Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-03
Cycle: 2026-11-03__release-v9.15
Release: v9.15

# Backlog Slice — v9.15

<!-- release-plan-marker: RP:v9.15:2026-11-03__release-v9.15 -->

45 stories across 7 EPICs, 28.00 estimated days. The acceptance criteria below are the source of truth for Sprint Planning and Execution. Scope is sized to the top of the confirmed ~24–28 day capacity band, per the explicit user instruction "use full capacity" (2026-11-03).

**Ready pool:** 148 items, 75.55 days (after the STEP 4 calibration raises, applied to the whole pool before selection).

**Selection method** (`release_planning_prompt.md` §1.4c):
1. The 10 items committed to v9.15 by roadmap rebalance `2026-11-03__scheduled` (DL-088), including both ready P1 items (`BLG-FE-244`, `BLG-FE-245`).
2. The other ready P2 items, in ascending ID order: `BLG-FE-239`, `BLG-FE-240`, `BLG-FE-243` (the three accepted v9.14 defects, closure Carry-Forward #2) and `BLG-OPS-48` (gate cleared this run).
3. Step 1a, deferred lessons-learnt patch items targeted at v9.15: `BLG-GOV-404` and `BLG-QA-240`.
4. A category-balanced, oldest-first round-robin over P3/P4, run until 0.00 days were left.

**Product Owner override (2026-11-03):** the ungated Site Structure & Usability Phase 2/3 items stay at their DL-088 provisional releases (v9.16/v9.17) instead of being seated by the P2-first step. This covers four P2 items (`BLG-FE-255`, `256`, `260`, `264`; 8.5d) and their P3 siblings.

**Where an item's own AC is stale, untestable, missing or points at text outside the slice, the AC below restates it.** Each change from the source backlog item is marked *(restated)* with the reason. Scope bullets are copied from the source item for convenience; the source item stays authoritative for Problem text.

**`strategy_rules.md` writes (case (c), `execution_prompt.md` §7):** ST-28 may clarify §13 text, depending on its outcome. If it does, the write needs a Strategy Rules & System Intent Owner confirmation for that AC line in the sealed `sprint_backlog.md` sign-off summary (RISK-03).

**§13 clause-citation rule (v2.61):** ST-10 and ST-28 require a §13 confirmation or review. Each cites every §13 clause that names its subject, or says no clause does.

**Post-merge and production-data ACs (Sprint Planning STEP 6.2):** ST-33 AC 1 and AC 2 and ST-35 AC 1 can be met only after merge with production data. ST-29 needs console access. Sprint Planning marks them `post-merge` with a named tracking item before seal.

**Conditional story (§1.4b):** ST-33 (`BLG-OPS-197`). Its earliest clear date, 2026-11-09, falls inside the sprint window.

---

## EPIC-01 — Trade Entry Integrity & Sizing (build-and-ship)

**Maps to:** S2-01 – S2-07
**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner; Strategy Rules & System Intent Owner
**Description:** Close the two P1 Correctness Fast-Track gaps from DL-088: every route into Trade Entry shows the §4.2 pre-entry checks, and the FX field pre-fills from the live rate instead of a fixed 1.27. Label FX consistently, default dates to the local day, and fix three smaller entry/stop/sizing defects on the same pages.
**Estimated days:** 5.05

### ST-01 — Show the pre-entry checks on every route into Trade Entry, not only from a Trade Plan
**Source:** BLG-FE-244
**Priority:** P1
**Effort:** M (~2-3 days)
**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner
**Sequencing:** First in EPIC-01. Reuses the Trade Plan pre-entry panel and validation endpoint.
**UI-facing:** Yes
**Scope:**
- When Trade Entry is opened without a linked Trade Plan that already passed its checks, show the same pre-entry check panel and acknowledge-to-proceed step the plan uses, reusing the existing validation endpoint and components
- Plan-linked entries keep their current flow
- Record overrides from this path the same way the plan path does, so the Red Flag Journal and SI-05 digest count them
- No new check logic and no automatic blocking beyond what §4.2 already defines
**Acceptance Criteria:**
- From each of the three routes (sidebar, "New Position", `n`), Trade Entry shows the pre-entry check results before save
- With a risk-off or unknown regime for the selected market, the regime check shows its FAIL/unknown state and save requires the acknowledgement
- A plan-linked entry does not show the panel twice
- Playwright coverage for each of the above passes in CI

### ST-02 — Pre-fill Trade Entry's FX rate from the live rate, not a fixed 1.27
**Source:** BLG-FE-245
**Priority:** P1
**Effort:** S (~0.5-1 day)
**Owner:** Head of Engineering; Frontend Specifications & UX Documentation Owner
**Sequencing:** Same page as ST-01; either order.
**UI-facing:** Yes
**Scope:**
- Pre-fill from the live (or last-good) rate the backend already serves; show its source and age next to the field; keep it editable
- Fall back to the backend's flagged fallback only when no rate is available, and say so
**Acceptance Criteria:**
- With a mocked live rate of 1.35, a new US entry pre-fills 1.35 with its source and age shown
- With no rate available, the field shows the fallback and a visible "fallback rate" note
- No `"1.27"` literal remains in `TradeEntry.js`
- Playwright coverage passes in CI

### ST-03 — Label the FX rate the same way on entry and exit
**Source:** BLG-FE-246
**Priority:** P2
**Effort:** S (~0.5 day; held at 0.5d, count named: about 8 FX label sites in `src/` (grep, 2026-11-03))
**Owner:** Frontend Specifications & UX Documentation Owner
**Sequencing:** After ST-02 (same FX field).
**UI-facing:** Yes (wording only, FI-P3-02)
**Scope:**
- One label on every FX input: "FX rate — USD per £1 (GBP/USD)", with a one-line hint
- Grep `src/` for other FX input labels and align them
**Acceptance Criteria:**
- Every FX input label in `src/` uses the same wording
- Code review of the static label text is sufficient (wording-only AC, FI-P3-02)

### ST-04 — Default trade, exit and cash dates to the user's local date, not the UTC date
**Source:** BLG-FE-243
**Priority:** P2
**Effort:** S (~0.5d; held at 0.5d, count named: 15 `toISOString()` date sites in 10 files under `src/` (grep, 2026-11-03), a mechanical swap to one local-date helper)
**Owner:** Frontend Specifications & UX Owner
**Sequencing:** Independent.
**UI-facing:** Yes
**Scope:**
- Add one shared helper that returns today's date as `YYYY-MM-DD` in the browser's local timezone, and use it for the four prefill sites listed in `BLG-FE-243`'s Problem
- Check the other `toISOString().split` date uses (`Dashboard.js` peak date, `ExportModal.js`, `PortfolioGrowthChart.js`, `RedFlagsCard.js`, `base44Client.js`, `SystemStatus.js`) and switch any that mean "today for the user"
- Update `tests/e2e/positions-exit-modal.spec.js` SC-PEM-01, which asserts the UTC expression, to assert the local date. Add a Playwright case under `timezoneId: 'Europe/London'` with the clock set to 00:30 BST that checks the Exit, Trade Entry and Cash Management date fields prefill the local date
**Acceptance Criteria:**
- At 00:30 BST under Europe/London, the Exit dialog, Trade Entry and Cash Management date fields prefill the local date, not the previous day
- The new Playwright case passes in CI
- No user-facing "today" date in `src/` comes from `toISOString().split("T")[0]`

### ST-05 — Normalise the Trade Entry ticker the same way for the ATR preview and for save
**Source:** BLG-FE-222
**Priority:** P3
**Effort:** XS (<1h plus tests)
**Owner:** Head of Engineering
**Sequencing:** Independent.
**UI-facing:** No (backend test)
**Scope:**
- Normalise (trim, upper-case) the ticker once, server-side in `AddPositionRequest`/`add_position()`, and in Trade Entry before both the preview and the submit
- Extend `tests/test_market_atr_preview_endpoint.py` AC 2 cases with untrimmed and lower-case input
- Align the two Positions deep links' status test
**Acceptance Criteria:**
- For an untrimmed or lower-case ticker, the preview stop equals the saved `initial_stop` (backend test)
- `?position=` and `?exit=` use the same open-position test

### ST-06 — Trail Stop modal's ATR trail value uses a hardcoded 2.0 multiplier and no breakeven floor
**Source:** BLG-BE-173
**Priority:** P3
**Effort:** S (~0.5d)
**Owner:** Head of Engineering; Strategy Rules & System Intent Owner
**Sequencing:** Independent.
**UI-facing:** Yes (modal footnote wording)
**Scope:**
- Compute `atr_trail_stop` with the same §7.2 formula and §11 multipliers the live recompute uses (`backend/strategy_parameters.py`), including the breakeven floor, or call the shared function
- Update the modal footnote (`positions.md` §Trail Stop Action) and `position_endpoints.md`'s stop-trail description to match; add a unit test
**Acceptance Criteria:**
- For a profitable position, `atr_trail_stop` equals the value `calculate_trailing_stop` would produce from the same inputs (unit test), including a case where the breakeven floor binds
- No literal multiplier remains in the handler or the modal footnote

### ST-07 — Label signal cost as including fees, and make the zero-ATR sizing reason plain English
**Source:** BLG-FE-219
**Priority:** P3
**Effort:** XS (<0.5d)
**Owner:** Frontend Specifications & UX Documentation Owner; Head of Engineering
**Sequencing:** Independent.
**UI-facing:** Yes
**Scope:**
- Label the value "Total cost (incl. fees)"
- Reword the zero-ATR reason in plain English (backend string and `signal_endpoints.md`)
- Playwright test for the reason line
**Acceptance Criteria:**
- The label and reason text are changed, and Playwright asserts the reason line for a zero-ATR signal

## EPIC-02 — Site Structure & Usability Phase 1 — Specs, Vocabulary & Quick Wins

**Maps to:** S2-08 – S2-14
**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design; Head of Engineering
**Description:** Phase 1 of the Site Structure & Usability programme (DL-088): write the navigation v2 + glossary UI-label spec, the Dashboard "Today" spec and the single Journal area spec that Phases 2 and 3 build from; apply one name per page; remove the legacy Dashboard route; set per-page tab titles; fix three chrome defects.
**Estimated days:** 8.50

### ST-08 — Navigation spec v2: job-based areas, plus a UI-label section in the glossary
**Source:** BLG-SPEC-214
**Priority:** P2
**Effort:** M (~2 days)
**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design
**Sequencing:** First in EPIC-02. Blocks ST-11 (labels come from its glossary section).
**UI-facing:** Spec (design-gate review: navigation and labels)
**Scope:**
- Revise `navigation.md`: about five job-based areas (Today · Portfolio · Find trades · Review · Settings), item placement for all 25 pages, default-expanded groups, Trade Plans and Research surfaced, legacy Dashboard removed, parent links for detail pages, onward-link rule for every page, browser-tab title rule
- Add a UI-label section to `glossary.md`: one canonical label per page and primary action, and "trade" vs "position" usage
- Keep the collapsible-sidebar pattern (per the v8.5 recommendation)
**Acceptance Criteria:**
- `navigation.md` revised (version bumped) and `glossary.md` gains the UI-label section, both reviewed by the Head of UX & Design
- Every page in `src/pages/` has a placement and a canonical label

### ST-09 — Dashboard spec: a prioritised "Today" action list
**Source:** BLG-SPEC-215
**Priority:** P2
**Effort:** M (~2 days)
**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design
**Sequencing:** Independent.
**UI-facing:** Spec (design-gate review: home page)
**Scope:**
- Revise `dashboard.md` (Class 1, Head of Specs Team approval): a "Today" list first — regime per market, then exits and stop changes due, then qualifying entries — each item linking to its action (reusing `/Positions?exit=<id>` and similar deep links); a single-line quiet-day state; status cards, What's New and gate progress below
- Define ordering, empty, loading and error states, and which existing cards move or merge
**Acceptance Criteria:**
- `dashboard.md` revised and approved; every observable behaviour has a testable AC for `BLG-FE-254`

### ST-10 — Spec for one Journal area combining reflections, red flags and position notes
**Source:** BLG-SPEC-216
**Priority:** P3
**Effort:** M (~2 days)
**Owner:** Frontend Specifications & UX Documentation Owner; Head of UX & Design
**Sequencing:** Independent. Its §13 confirmation is a sub-step before approval.
**UI-facing:** Spec (design-gate review: Journal area)
**Scope:**
- Specify one Journal area: sections or filters for reflections, red flags and position notes; routes and redirects for the old pages; what happens to the Positions journal view
- Strategy Rules & System Intent Owner confirms the merge moves no §13 boundary for AI-summarised journal surfaces (PO-02 roster rows)
**Acceptance Criteria:** *(restated: §13 clause-citation rule, v2.61)*
- Spec filed and approved by the Head of UX & Design; ACs ready for `BLG-FE-258`
- The §13 confirmation names the §13 clauses it answers: no §13 clause names the journal (reflections, red flags or position notes), so §13.1 and §13.2 apply; if the merged area surfaces AI journal summaries, §13.5's roster is checked and the result recorded

### ST-11 — Use one name per page and action across sidebar, page headings and command palette
**Source:** BLG-FE-248
**Priority:** P2
**Effort:** S (~1 day)
**Owner:** Frontend Specifications & UX Documentation Owner
**Sequencing:** After ST-08 (`BLG-SPEC-214`) is approved.
**UI-facing:** Yes
**Scope:**
- Apply the glossary's canonical labels to `NAV_GROUPS` (`Layout.js`), every `PageHeader` title, `CommandPalette.js` `PAGE_LABELS`, primary buttons and the shortcut legend
- Add Replay and Notifications to the palette labels
**Acceptance Criteria:**
- For every page, sidebar label = page heading = palette label (or the glossary records the deliberate difference)
- Existing nav/palette Playwright specs updated and passing

### ST-12 — Remove the legacy widget Dashboard route and its duplicate command-palette entry
**Source:** BLG-FE-247
**Priority:** P3
**Effort:** S (~0.5 day)
**Owner:** Head of Engineering
**Sequencing:** After ST-16 (`BLG-FE-240`) confirms where its fix lands (Scope bullet 1).
**UI-facing:** Yes
**Scope:**
- Confirm no live surface links to `/Dashboard` and that `BLG-FE-240`'s fix belongs on `DashboardHome` instead (update that item's scope note if so)
- Remove the route, the page and its palette label; redirect `/Dashboard` to `/`
- Remove components used only by the legacy page
**Acceptance Criteria:**
- The command palette shows exactly one "Dashboard" entry
- `/#/Dashboard` lands on the Dashboard home page
- CI passes with the legacy page's specs removed or retargeted

### ST-13 — Set a browser-tab title for each page
**Source:** BLG-FE-249
**Priority:** P3
**Effort:** S (~0.5 day)
**Owner:** Head of Engineering
**Sequencing:** Independent.
**UI-facing:** Yes
**Scope:**
- Set `<page label> · Position Manager` from the layout using the glossary label; Research pages include the ticker
**Acceptance Criteria:**
- Each routed page sets a distinct title; a Playwright check covers three pages

### ST-14 — Fix three small chrome defects: version label, What's New heading, sidebar height
**Source:** BLG-FE-266
**Priority:** P3
**Effort:** S (~0.5 day)
**Owner:** Head of Engineering
**Sequencing:** Independent.
**UI-facing:** Yes
**Scope:**
- Show the real release version; omit the version suffix when absent; make the sidebar background full height
**Acceptance Criteria:**
- Footer shows the current release; no "undefined" in the What's New heading; sidebar background spans the page; Playwright coverage passes

## EPIC-03 — Metric & Display Correctness

**Maps to:** S2-15 – S2-23
**Owner:** Metrics Definitions & Analytics Canonical Owner; Backend Engineering Patterns Owner; Frontend Specifications & UX Documentation Owner
**Description:** Fix the two accepted P2 win-rate defects carried from v9.14 (break-even counted as a win; Dashboard widgets fed from open positions), plus small backend and display correctness items: price-alert duplicates, strategy-version effective dates, monthly P&L fallback, gap-risk weekend statistic, open-position P&L basis, Positions trail wording and badge contrast.
**Estimated days:** 2.40

### ST-15 — Trade History counts a break-even trade as a win
**Source:** BLG-FE-239
**Priority:** P2
**Effort:** XS (<1h)
**Owner:** Metrics Definitions & Analytics Canonical Owner; Frontend Specifications & UX Documentation Owner
**Sequencing:** Independent.
**UI-facing:** Yes
**Scope:**
- Change the win test to `t.pnl > 0`, matching §Win Rate, and decide (with the owner) whether `pnl = 0` belongs in Avg Loss or neither
- Add a Playwright case with one break-even trade asserting the summary win rate
**Acceptance Criteria:**
- With trades of P&L +10, 0 and −10, the Trade History summary shows a 33.3% win rate (Playwright)
- The page's win test matches `metrics_definitions.md` §Win Rate

### ST-16 — Dashboard win-rate widgets are fed from open positions only
**Source:** BLG-FE-240
**Priority:** P2
**Effort:** S (~0.5 day)
**Owner:** Metrics Definitions & Analytics Canonical Owner; Frontend Specifications & UX Documentation Owner
**Sequencing:** Independent.
**UI-facing:** Yes
**Scope:**
- Feed both widgets from closed trades (e.g. the `GET /trades` summary `win_rate`, or `trade_history` rows), computed per `metrics_definitions.md` §Win Rate
- Pass `WinRateChart` the props it reads
- Playwright coverage of both widgets with closed trades present
**Acceptance Criteria:**
- With closed trades of P&L +10 and −10, both widgets show 50% (Playwright)
- Neither widget reads `GET /positions` for closed trades

### ST-17 — Align the View Trail modal wording with the read-only ruling
**Source:** BLG-FE-218
**Priority:** P3
**Effort:** XS (<0.5d)
**Owner:** Frontend Specifications & UX Documentation Owner
**Sequencing:** Independent.
**UI-facing:** Yes
**Scope:**
- Heading "View Trail — {TICKER}"; rename "Raise by" (e.g. "Difference vs current stop"); reword the disabled tooltip
- Update `positions.md` §Trail Stop Action (design pass with the Head of UX & Design)
- Update Playwright SC-TS-* assertions
**Acceptance Criteria:**
- The three texts are changed in `positions.md` and `Positions.js`, and Playwright asserts the new heading and label

### ST-18 — Fix the Strategy Benchmark Rebalance badge's contrast and settle tinted vs filled exit-reason badges
**Source:** BLG-FE-220
**Priority:** P3
**Effort:** XS (<1h plus test updates)
**Owner:** Frontend Specifications & UX Documentation Owner
**Sequencing:** Independent.
**UI-facing:** Yes (contrast)
**Scope:**
- Decide tinted vs filled badges with the Head of UX & Design, and align `strategy_benchmark.md` §7 and `src/pages/StrategyBenchmark.js`
- Move Rebalance to a passing token (e.g. `bg-teal-700`, measured first)
- Update `tests/e2e/strategy-benchmark.spec.js` SC-SB-04a's `bg-teal-600` assertion and add a scoped axe color-contrast check
**Acceptance Criteria:**
- Every exit-reason badge on the Trade Log passes a scoped axe color-contrast scan in both themes
- `strategy_benchmark.md` §7 matches the shipped badge style

### ST-19 — Price-alert duplicate fallback returns 500 when the threshold has more than 4 decimal places
**Source:** BLG-BE-170
**Priority:** P3
**Effort:** XS (<1h plus test)
**Owner:** Backend Engineering Patterns Owner; Data Model & Domain Schema Owner
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Round `threshold_price` to 4 dp in `create_price_alert()` before both SELECTs and the INSERT (or compare with `%s::numeric(10,4)`)
- If the fallback SELECT still finds no row, raise a clear error rather than passing `None` to `_price_alert_row`
**Acceptance Criteria:**
- Submitting the same threshold with 5+ decimal places twice returns the existing alert both times, with one active row (test, including the real-Postgres DS-28 suite)
- No code path calls `_price_alert_row(None)`

### ST-20 — Use the deploy date, not the ruling date, as strategy v1.15's effective date
**Source:** BLG-BE-171
**Priority:** P3
**Effort:** XS (<1h)
**Owner:** Strategy Rules & System Intent Owner; Financial Reporting & Records Owner
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Strategy Rules & System Intent Owner rules whether a behavioural version's effective date is the ruling date or the production deploy date, and records the rule in the registry docstring
- If the ruling is the deploy date: set v1.15's `effective_date` (and the Change Log date, if `tests/test_strategy_version_registry.py` requires them to match) to the actual deploy date
- List any trades entered in the gap and confirm their attribution
**Acceptance Criteria:**
- The rule for behavioural effective dates is written in `strategy_version_registry.py`'s docstring
- v1.15's window and the `strategy_version_at_entry` stamps agree for every trade entered from 9 October 2026 onwards (query output or test)

### ST-21 — Show the code-written fallback when the monthly P&L summary's regeneration call fails
**Source:** BLG-BE-172
**Priority:** P3
**Effort:** XS (<1h)
**Owner:** Head of Engineering; Financial Reporting & Records Owner
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- When attempt 1 failed its checks and attempt 2's model call raises, store and return the fallback summary (`source: "fallback"`) with a terminal audit result. The cap and audit rules still apply.
- Keep 503 for a model failure on attempt 1 (no checked output exists)
- Update the `reports_endpoints.md` 503 row and `metrics_definitions.md` § AI Monthly P&L Narrative Usage if the terminal-result set changes; add a unit test
**Acceptance Criteria:**
- A unit test with attempt 1 failing checks and attempt 2 raising receives `source: "fallback"` and a stored row
- `count_monthly_pnl_narrative_generations` counts that request exactly once

### ST-22 — Gap-risk weekend statistic: pick it by the exchange calendar and count ordinary weekends
**Source:** BLG-BE-174
**Priority:** P3
**Effort:** S (~0.5d)
**Owner:** Head of Engineering; Strategy Rules & System Intent Owner
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Classify a gap as multi-day when it spans one or more non-session days, using the ST-14 calendar
- Select the statistic by whether the next session follows a non-session day
- Convert the earnings timestamp to the America/New_York date
- Re-confirm Binding Condition 4 (retrospective statistic only) in the §13 record's next addendum, if the statistic's definition changes
**Acceptance Criteria:**
- A Friday-to-Monday gap is counted in the weekend set (unit test)
- A Thursday view before Good Friday uses the weekend statistic (unit test)
- An `earningsTimestamp` of 21:00 ET maps to that ET date (unit test)

### ST-23 — Open-position pnl: code uses the live FX rate and does not deduct fees; the dictionary says entry-time FX, fees deducted
**Source:** BLG-SPEC-198
**Priority:** P3
**Effort:** S (~0.5d)
**Owner:** Data Model & Domain Schema Owner; Metrics Definitions & Analytics Owner
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Decide which is canonical, including whether currency movement since entry belongs in unrealised P&L. Check `metrics_definitions.md` and the Positions/Portfolio frontend specs for the displayed definition
- Align the losing side. A code change that alters displayed P&L needs a design pass
- Also correct `metrics_definitions.md` Position Risk's data sources. They still label `positions.entry_price` "native currency", which contradicts the GBP ruling (ST-38, v9.12). For US positions the native entry is `fill_price`; the formula `(entry − stop)` must not mix GBP `entry_price` with the native `initial_stop` (agent-mediated Director of Quality review of EPIC-05, condition C2)
**Acceptance Criteria:**
- `metrics_definitions.md` Position Risk names `fill_price` (US) or `entry_price` (UK) as the native entry, with a version bump
- The dictionary's §5.2 and the `pnl` row state the same FX basis and fee treatment as the code that produces the displayed figure, or a code change brings the code to the spec with Data Model & Domain Schema Owner sign-off
- The decision is recorded with its rationale

## EPIC-04 — AI Output Checks & §13 Boundary

**Maps to:** S2-24 – S2-28
**Owner:** AI Compliance & Governance Officer; Strategy Rules & System Intent Owner
**Description:** Tighten the AI briefing and journal-summary advisory checks (non-ticker tokens, false positives and misses, focus rule) and re-read §13 against the AI journal summary.
**Estimated days:** 2.20

### ST-24 — Review logged briefing ticker-caveat tokens for further non-tickers
**Source:** BLG-AI-23
**Priority:** P3
**Effort:** XS (<1h plus tests)
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- With the user's permission, list the tokens caveated since 2026-10-30 with their counts
- Classify each as ticker or non-ticker
- Add the non-tickers to `_NON_TICKER_WORDS` (ruling `ESC-EXEC-20261027-02` (B) condition 2 is a minimum list)
**Acceptance Criteria:**
- The token list with counts is recorded
- Each non-ticker found is added, and `test_non_ticker_words_ignored` covers it; or the review records that none was found

### ST-25 — Journal summary advisory check: remaining false positives and misses
**Source:** BLG-AI-24
**Priority:** P3
**Effort:** S (~0.5d)
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Delegation note:** delegated_decision: the ruling (AC 1) is the AI Compliance & Governance Officer's.
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Ask the AI Compliance & Governance Officer whether to drop "can" from the passive form, exclude reported speech, and add the missed forms (each is a change to the ruling's forms)
- Implement the ruled forms; add the sentences listed in `BLG-AI-24`'s Problem as positive or negative cases; update `ai_s13_boundary_test_suite.md` B-JS-04
**Acceptance Criteria:**
- The ruling is recorded before the code change
- Each sentence listed in `BLG-AI-24`'s Problem has the result the ruling assigns it, in a test *(restated: "above" pointed at the source item's Problem)*
- Every ST-15 and v9.13 ST-18 case keeps its result

### ST-26 — Chat stop-time focus rule: ignore common upper-case non-ticker words
**Source:** BLG-AI-25
**Priority:** P3
**Effort:** XS (<1h plus tests)
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Add common time, chat and abbreviation words (AM, PM, EOD, EOW, IMO, FYI, NOTE, Q1–Q4, VIX and similar) to `_NON_TICKER_WORDS`, or give the focus rule its own exclusion list; confirm with the AI Compliance & Governance Officer that this stays within the ruling (condition 2 of `ESC-EXEC-20261027-02` (B) is a minimum list)
- Add the sentences listed in `BLG-AI-25`'s Problem as focus-attributed cases
**Acceptance Criteria:**
- Each sentence listed in `BLG-AI-25`'s Problem, with focus `MU` held, gets the MU note *(restated: "above" pointed at the source item's Problem)*
- "TSLA's stop was hit last week." still gets no MU note; all ST-16 and ST-17 tests pass

### ST-27 — Journal summary advisory check: do not flag "could/may help explain"
**Source:** BLG-AI-26
**Priority:** P3
**Effort:** XS (<1h plus tests)
**Owner:** AI Compliance & Governance Officer; Backend Engineering Patterns Owner
**Sequencing:** After ST-25 (`BLG-AI-24`): one ruling can cover both.
**UI-facing:** No
**Scope:**
- Exclude "help explain/account for/show" (help + an explanatory verb) from form (4)'s evaluative phrase, under the AI Compliance & Governance Officer's ruling for BLG-AI-24
- Add both sentences as negative cases in `tests/test_journal_summary_language_check.py` and B-JS-04
**Acceptance Criteria:**
- Both sentences listed in `BLG-AI-26`'s Problem return `[]` *(restated: "above" pointed at the source item's Problem)*
- "Tighter stops could help." and the other six BLG-AI-20 sentences are still caught

### ST-28 — §13 boundary language clarity pass — AI journal summarisation
**Source:** BLG-GOV-194
**Priority:** P3
**Effort:** S (~0.5-2 days)
**Owner:** Strategy Rules & System Intent Owner
**Delegation note:** delegated_decision: Strategy Rules & System Intent Owner.
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:** *(restated: the item has a Proposed solution but no AC; §13 clause-citation rule, v2.61)*
- The Strategy Rules & System Intent Owner records a dated re-read of §13 against the AI journal summary (`BLG-AI-20`, v9.14 ST-15) in `docs/product/decisions/`
- The record answers each clause it cites: no §13 clause names the journal summary, so §13.1 and §13.2 apply; it also states whether the journal summary belongs on §13.5's re-attestation roster
- Outcome is either "boundary language confirmed unambiguous" or a clarified §13 text written under `execution_prompt.md` §7 case (c), with its Change Log row and `strategy_version_registry.py` entry

## EPIC-05 — Operations, Security & Market-Data Monitoring

**Maps to:** S2-29 – S2-33
**Owner:** Infrastructure & Operations Owner; Cybersecurity & Trust Lead; FinOps & Resource Architect
**Description:** Run the 6-month ANTHROPIC_API_KEY scope audit, make rebalance-exit and the screener tell a missing run from an empty one, skip code suites on docs-only pushes, and record the production market-data call baseline.
**Estimated days:** 2.15

### ST-29 — ANTHROPIC_API_KEY 6-month scope audit
**Source:** BLG-OPS-48
**Priority:** P2
**Effort:** S (~0.5 day)
**Owner:** Cybersecurity & Trust Lead; Infrastructure & Operations Owner
**Delegation note:** Human-Delegation: key permissions and rotation are read from the Anthropic console by the Cybersecurity & Trust Lead.
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Review ANTHROPIC_API_KEY permissions against current usage patterns
- Confirm key is not used outside the documented endpoints (generate-thesis, check-daily-cost)
- Verify key rotation has occurred per BLG-OPS-38 policy
- Document review findings
**Acceptance Criteria:** *(restated: Scope lists two endpoints, generate-thesis and check-daily-cost; five AI endpoints are live per `BLG-SPEC-211`)*
- ANTHROPIC_API_KEY scope confirmed minimal: used only by the AI endpoints in the current AI endpoint register, each named
- Key rotation confirmed per BLG-OPS-38 schedule
- Review findings documented

### ST-30 — Rebalance-exit generation should check that today's screener run completed
**Source:** BLG-OPS-190
**Priority:** P3
**Effort:** S (~0.5 day)
**Owner:** Infrastructure & Operations Owner
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Freshness precondition in the rebalance-exit endpoint or workflow: skip and alert if no screener run completed today
**Acceptance Criteria:**
- With no completed screener run today, rebalance-exit creates no signals and raises an alert (test)

### ST-31 — Skip the five code-test workflows on governance-only and docs-only pushes
**Source:** BLG-OPS-191
**Priority:** P3
**Effort:** S (~0.5 day)
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- `paths-ignore: ['claude/**', 'docs/**']` with a pass-through job so required checks still report (constraint noted at `backlog_archive.md:2167`)
**Acceptance Criteria:**
- A governance-only PR completes with all required checks reported, without running the five suites
- A code PR still runs them

### ST-32 — Tell "no qualifying tickers" apart from "momentum run missing" in the month-end rebalance job
**Source:** BLG-OPS-192
**Priority:** P3
**Effort:** S (~0.5 day)
**Owner:** Infrastructure & Operations Owner; Strategy Rules & System Intent Owner
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Persist a completion marker for each momentum signal run (date, tickers ranked, count), or reuse an existing run table
- Rebalance job: no marker today → 503 (unchanged); marker with zero tickers → an empty ranking and the §8.4 recommendations it implies
**Acceptance Criteria:**
- pytest: zero-qualifier completed run → signals for non-risk-off, post-§8.1 positions and no 503; missing run → 503 as now

### ST-33 — Record the weekly market-data call-volume baseline from production
**Source:** BLG-OPS-197
**Priority:** P3
**Effort:** XS (<1h)
**Owner:** FinOps & Resource Architect; Infrastructure & Operations Owner
**Delegation note:** Human-Delegation: production read (`GET /ops/api-call-attribution`, DS-36 query) needs the user's permission or the user runs it.
**Sequencing:** **Conditional (§1.4b):** needs 7 full days of production data after EPIC-05 v9.14 deployed (merged 2026-11-02), so the earliest clear date is 2026-11-09, inside the sprint window. Promote to firm only on a dated confirmation that the week has elapsed and production read access is granted. `BLG-OPS-195` (alert on the baseline) waits for this story and is not in v9.15.
**UI-facing:** No
**Scope:**
- After the production deploy, run DS-36's Verification query on production and record it in `data_model.md` DS-36
- 7 full days after deploy, call `GET /ops/api-call-attribution?window=weekly` on production and fill §4's calls and failures per source, with the date and `top_contributors`
- Close `DEL-20261027-04` and `DEL-20261027-06`
**Acceptance Criteria:**
- DS-36 Live Confirmation for production is recorded: `api_call_log.feature` text YES, `screener_runs.duration_seconds` numeric YES, index `idx_acl_called_at_feature` *(post-merge/production-data: Sprint Planning names the tracking item)*
- `data_pipeline_cost_baseline.md` §4 has weekly calls and failures for each source and combined, from one production weekly report, with its date and `top_contributors` (3 features, or every feature with calls if fewer than 3 made any); the §6 volume sign-off line is ticked *(production-data)*

## EPIC-06 — Data Model & Spec Debt

**Maps to:** S2-34 – S2-36
**Owner:** Data Model & Domain Schema Owner; Head of Specs Team; Metrics Definitions & Analytics Canonical Owner
**Description:** Clear contract-example drift, and re-apply two NOT NULL constraints and DS-17's staging index.
**Estimated days:** 2.00

### ST-34 — Clear the 8 pre-existing success-example drifts so check_contract_example_freshness.py exits 0
**Source:** BLG-SPEC-194
**Priority:** P4
**Effort:** S (~0.5d)
**Owner:** API Contracts & Documentation Owner
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- For each of the 8, decide which side is right (contract example or `openapi.yaml` response schema) and correct it
- Once the script exits 0, consider adding it to `quality_gate.yml` as a gate
**Acceptance Criteria:**
- `python3 scripts/check_contract_example_freshness.py` exits 0 on `main`
- Each correction is recorded in the changed contract's changelog

### ST-35 — Re-apply NOT NULL on positions.portfolio_id and positions.total_cost
**Source:** BLG-SPEC-196
**Priority:** P3
**Effort:** S (~0.5d; pre-check, migration and live confirmation in two environments; calibrated to 1.0d — live migration on staging and production (v9.14 precedent))
**Owner:** Data Model & Domain Schema Owner
**Delegation note:** Human-Delegation: the staging and production constraint changes need the user's permission (production run by the user).
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Read-only pre-check on staging and production: count rows where `portfolio_id IS NULL` or `total_cost IS NULL`
- If both counts are 0, add a DS-xx migration (`ALTER TABLE positions ALTER COLUMN ... SET NOT NULL`, reversible) and apply it to staging, then production, per the DS-23 pattern
- If any row is NULL, record the rows' origin and a backfill decision before migrating
- Remove the "nullable on live staging" notes on both Fields rows once applied
**Acceptance Criteria:**
- `information_schema.columns` reports `is_nullable = NO` for both columns in staging and production, with the output recorded in the DS-xx Live Confirmation *(post-merge: production confirmation after deploy; Sprint Planning names the tracking item)*
- `scripts/check_data_model_drift.py` no longer reports either column as a nullable mismatch

### ST-36 — Apply DS-17's open-position unique index to staging
**Source:** BLG-SPEC-197
**Priority:** P3
**Effort:** XS (<1h; calibrated to 0.5d — staging migration (v9.14 precedent))
**Owner:** Data Model & Domain Schema Owner
**Delegation note:** Human-Delegation: staging index change with the user's permission.
**Sequencing:** Independent of the other DS migration story (`BLG-SPEC-196`); either order.
**UI-facing:** No
**Scope:**
- Run DS-17's duplicate pre-check on staging, then its Up Migration
- Record the staging Live Confirmation in DS-17
- Decide whether `reset-and-seed-staging.yml`'s migrate step should also apply DS-17 (`CREATE UNIQUE INDEX IF NOT EXISTS`) so a future staging rebuild keeps it
**Acceptance Criteria:**
- `pg_indexes` on staging lists `idx_positions_open_ticker_entry_date_unique` with DS-17's definition
- DS-17 records the staging confirmation alongside the production one

## EPIC-07 — QA & Governance Tooling

**Maps to:** S2-37 – S2-45
**Owner:** Director of Quality; Head of Specs Team; PMO Lead; Strategy Rules & System Intent Owner
**Description:** The two deferred lessons-learnt script patches (§1.4c step 1a), four test-suite hygiene items, an end-to-end dry-run of the escalation SLA-breach path, and dated re-confirmations of the strategic exclusions and the Priority 3 deferred initiatives.
**Estimated days:** 5.70

### ST-37 — Gate scan treats a shipped roadmap feature ID (PT-xx, SI-xx, PO-xx) as a met gate
**Source:** BLG-GOV-404
**Priority:** P3
**Effort:** S (~0.5d)
**Owner:** Head of Specs Team; PMO Lead
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Treat a roadmap feature ID (PT-xx, SI-xx, PO-xx) as shipped when `claude/roadmap/current_roadmap.md` or `roadmap_archive.md` marks it ✅ Shipped/Complete
- Report such gates in the "gating item shipped — verify" list so the §1.3a write-back can clear them
- Add tests for a shipped and an unshipped feature ID
**Acceptance Criteria:**
- A gate reading "PT-04 shipped" is reported as gating item shipped (test)
- A gate on an unshipped feature ID is not reported (test)
- The six items named in `BLG-GOV-404`'s Problem (`BLG-FE-39`, `BLG-QA-21`, `BLG-QA-22`, `BLG-QA-23`, `BLG-GOV-26`, `BLG-FEAT-26`) appear in the scan output on the live backlog *(restated: names the items)*

### ST-38 — Make the execution-state consistency check count EPICs not yet initialised as pending
**Source:** BLG-QA-240
**Priority:** P3
**Effort:** XS (<1h plus test)
**Owner:** Director of Quality; Head of Specs Team
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Derive the expected pending set from the sprint's full EPIC list (`merge_order`, or `sprint_backlog_index.json`), not only from initialised EPICs
- Add a test with a partially initialised state (two merged, five not yet initialised)
**Acceptance Criteria:**
- The check passes for `epics_merged` = EPIC-01, EPIC-02, `epics_pending` = the other five, `all_merged: false`
- It fails when `epics_pending` is empty while `merge_order` lists an unmerged EPIC

### ST-39 — Behavioural tests for live holding days in the compliance and AI briefing readers
**Source:** BLG-QA-220
**Priority:** P3
**Effort:** XS (<1h)
**Owner:** QA & Testing Owner
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Tests for `compliance_service` position compliance and the `ai_service` daily-briefing context
**Acceptance Criteria:**
- With stored `holding_days` 9 and `entry_date` 10 days ago, compliance reports the position out of grace and the AI context marks it not in grace

### ST-40 — Real-Postgres tests for the ai_audit_log UUID[] path and the claude_audit_log daily cost sum
**Source:** BLG-QA-221
**Priority:** P3
**Effort:** S (~0.5d)
**Owner:** QA & Testing Owner; Backend Engineering Patterns Owner
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Add Pytest Phase B (real Postgres) tests: DS-31 conversion from an INTEGER[] table, an insert and history filter with UUIDs, and a daily cost sum over claude_audit_log rows across a day boundary
**Acceptance Criteria:**
- The Phase B tests pass in CI and fail if the casts or the table name are wrong

### ST-41 — Extend the utils.* leak guard to attributes patched on the real utils modules
**Source:** BLG-QA-222
**Priority:** P3
**Effort:** S (~0.5d)
**Owner:** Director of Quality; QA & Testing Owner
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Snapshot the public callables of the real `utils.*` modules at session start, and fail any file or test that leaves one replaced, as the module-identity guard does
- Then remove the private-copy workarounds where they become unnecessary
**Acceptance Criteria:**
- The guard fails a test that replaces an attribute on a real `utils.*` module without restoring it
- Default and reverse-order full suites still pass

### ST-42 — Make SC-TS-* Playwright scenario IDs unique across tests/e2e
**Source:** BLG-QA-224
**Priority:** P3
**Effort:** XS (<0.5d)
**Owner:** QA & Testing Owner
**Sequencing:** Independent.
**UI-facing:** No
**Scope:**
- Give one file a distinct prefix and update every citation in `docs/` and `claude/cycles/` that refers to the renamed IDs
**Acceptance Criteria:**
- No scenario ID is used in more than one file under `tests/e2e` (a script or test checks this)

### ST-43 — Escalation SLA breach dry-run test
**Source:** BLG-GOV-193
**Priority:** P3
**Effort:** S (~0.5-2 days)
**Owner:** PMO Lead
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:** *(restated: the item has a Proposed solution but no AC)*
- A dry-run on a scratch copy of the state files (never the live `.claude_current_state.json`) with a synthetic `Open` escalation backdated past its 72h `sla_due_utc` shows the `BLOCKED_SLA_BREACH` notice (`shared_standards.md` §4) and `release_planning_prompt.md` STEP -1.6's `SLA_BREACH_CARRIED` halt both fire
- The dated result is recorded in `docs/ops/`; each defect found is filed as a backlog item

### ST-44 — Strategic exclusions review cadence
**Source:** BLG-GOV-195
**Priority:** P3
**Effort:** S (~0.5-2 days)
**Owner:** Strategy Rules & System Intent Owner
**Delegation note:** delegated_decision: Strategy Rules & System Intent Owner with the Product Owner.
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:** *(restated: the item has a Proposed solution but no AC)*
- A dated decision record in `docs/product/decisions/` re-confirms or flags each of the four product-scope exclusions in `current_roadmap.md` §2 (broker API integration, real-time streaming, social features, options/futures), with a reason for each
- A re-confirmation cadence is recorded in that decision. If it is written into a governance prompt, the change follows CLAUDE.md §6 in the same commit; any change to §2 itself is left to the next `run roadmap`

### ST-45 — Sunset review for Priority 3 — Deferred initiatives
**Source:** BLG-GOV-196
**Priority:** P3
**Effort:** S (~0.5-2 days)
**Owner:** Product Owner
**Delegation note:** delegated_decision: Product Owner.
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:** *(restated: the item has a Proposed solution but no AC)*
- A dated Product Owner decision record in `docs/product/decisions/` re-confirms each of the seven Priority 3 — Deferred initiatives in `initiative_register.md` (Position Correlation Analysis, Backtesting Module, Multi-Portfolio Support, Mobile App, Full Compliance Scoring, Prometheus, Customisable Dashboard Layout) as deliberately deferred, or flags it for review, with a reason for each
- Any change to `initiative_register.md` itself is left to the next `run roadmap`; the decision record is linked as that run's input (carry-forward)
