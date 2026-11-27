Owner: Director of Quality
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-11-27

# QA Evidence — Weekly Review Loop

**EPIC:** EPIC-03 — Site Structure & Usability Phase 4, Stage 2: Weekly Review Loop (build-and-ship)
**Cycle:** 2026-11-18__release-v9.18
**Sprint goal:** Ship Site Structure & Usability Phase 4 stages 1–2 (… a readable, linked Weekly Digest with this week's loop), put the first-time-right checks in place before v9.19's design gate, and make position figures correct (`sprint_goal.md`). EPIC-03 delivers the Weekly Digest share: the journal completion rename, the readable weekly summary, its onward links, and this week's core loop with its two events.
**Branch:** `exec/2026-11-18__release-v9.18/EPIC-03`
**Test scenarios used:** `tests/e2e/weekly-digest.spec.js`, `tests/e2e/dashboard-today-list.spec.js`, `tests/e2e/accessibility-axe-scan.spec.js`, `tests/e2e/nav-notification-digest-consolidation.spec.js`, `tests/e2e/print-export-pdf.spec.js`, `tests/e2e/system-status.spec.js`, `src/lib/weeklyDigest.test.js`, `tests/test_weekly_digest_data.py`, `tests/test_weekly_digest_postgres.py`, `tests/test_digest_events_router.py`, `tests/test_api_contracts.py`

## Consolidation Block

| ST Item | Spec Reference | What was built | Acceptance criteria | Result | Deviations |
|---------|----------------|----------------|---------------------|--------|------------|
| ST-14 | `digest_endpoints.md` v0.6 `GET /digest/weekly`; `metrics_definitions.md` v1.37.0 §Journal Completion Rate; `weekly_digest.md` v0.4 | `journal_completion_rate_current`/`_7d_ago`, `closed_trades_total`, `closed_trades_total_7d_ago` added; `compliance_score_*` kept as deprecated aliases; each new field `null` on a failed query; a failed optional digest query is rolled back so later fields still compute. Commit `a5438839`. | AC 1 (no UI label or API field named "compliance" carries the rate): SC-DIG-06 (the page reads the new field even when the alias differs), `test_journal_completion_fields`. AC 2 (contract, OpenAPI and `metrics_definitions.md` agree; addendum: predicates match, `closed_trades_total`): all three updated in the commit; `tests/test_weekly_digest_postgres.py` runs the digest and `get_compliance_core_counts` over the same real rows and gets the same rate and count. Addendum "No closed trades yet": SC-DIG-07. | Pass | None |
| ST-15 | `weekly_digest.md` v0.5 §2 (Figures, Freshness Caption, description) | The Field/Unit table becomes five plain-language figures (`<dl>`) with a UTC freshness caption and the new description; rows built in `src/lib/weeklyDigest.js`. Commit `d64cc465`. | AC (no "Field", "Unit" or "timestamp" text; each figure has a plain-language label; light and dark): SC-DIG-02a/b; values, caption and second lines SC-DIG-03; null and zero cases SC-DIG-04, SC-DIG-11; unit tests 36 (now 51). Axe `WeeklyDigestFigures` light and dark, strict incomplete-contrast. | Pass | None |
| ST-16 | `weekly_digest.md` v0.5 §2 links; `navigation.md` v2.7 §Onward Links; `digest_endpoints.md` v0.7 `red_flags_7d` | Realised P&L → Performance Summary on Last 7 Days, journal completion → Performance Compliance, red flags → Journal Red flags; alerts links kept; `red_flags_7d` added (null on failure). Commit `d64cc465`. | AC 1 (each of the three figures links to its section and lands on it): SC-DIG-08 (URL, "Last 7 Days" period, Summary heading in view), SC-DIG-09 (Compliance heading in view and focused), SC-DIG-10 (Red flags tab selected). AC 2 (restated, as corrected by the addendum: journal completion → Performance Compliance, recorded in `navigation.md`): `navigation.md` v2.7 row. Addendum `red_flags_7d`: contract, OpenAPI, pytest (unit and real Postgres either side of the 7 × 24h boundary). | Pass | None |
| ST-17 | `metrics_definitions.md` v1.38.0 §Core Loop Metrics; `data_model.md` v2.73 DS-43; `digest_endpoints.md` v0.8 (`POST /digest/events`, `loop`); `weekly_digest.md` v0.6 §2 This Week's Loop; `dashboard.md` v4.8 TL-31 | `loop_events` table; `POST /digest/events` (with `dry_run`); `GET /digest/weekly` `loop`; "This week's loop" section (counts only, ISO-week caption); one opened event per page load, the digest request waiting for it (max 1.5 s); Today list item links record `due_today_action`; System Status's `POST /trade-plans` check deletes its draft. Commit `544ebe49`. | AC 1 (five metrics with worked examples and owner sign-off): §Core Loop Metrics, approved `ESC-EXEC-20261127-01`. AC 2 (shows five counts for the current week; each links to its page): SC-DIG-12, SC-DIG-14, `test_loop_counts_against_real_rows`. The Reviews count is not linked because its page is the Weekly Digest itself (design record §6; `weekly_digest.md` WD-05 "each linked except the review step"), so this is the designed reading, not a narrowed AC. AC 3 (opening the digest and a Due today action each write one event; nothing else is tracked): SC-DIG-13 (one per load, none on Refresh, event before digest request), SC-TL-31 light/dark (four link kinds one each; regime and overflow none), `tests/test_digest_events_router.py`. AC 4 (Playwright covers rendering and links): SC-DIG-12 to SC-DIG-14, SC-TL-31. CLAUDE.md §2 route rules: contract `## POST /digest/events`, OpenAPI path, `test.py` entry, fallback 133, SC-SS-01b. | Pass | None |

**AC coverage:** every slice AC for ST-14 to ST-17 (read with the addendum) is named in its row above.

**Frontend testing gate:** every observable AC has Playwright coverage (scenario IDs above); none relies on code review alone.

**QA test coverage:**
- Scenarios run: Playwright locally against the E2E bundle — weekly-digest, dashboard-today-list, system-status, print-export-pdf and nav-notification-digest-consolidation together, 111 passed; axe Weekly Digest light, WeeklyDigestFigures light and dark, DashboardPopulated, 3 passed for the final build (strict incomplete contrast: 0 page-content nodes); SC-TL-31 `--repeat-each=3` 6/6. Jest `src`: 425 + 2 passed (weeklyDigest 51). pytest: full Phase A suite 4062 passed, 59 skipped, 6 xfailed (two import-isolation tests deselected: they fail locally only from the gitignored `backend/mutants` tree), then 128 rerun after the ST-17 review fixes; real Postgres (local PostgreSQL 18 cluster) `tests/test_weekly_digest_postgres.py` 3 passed, and fails with the rollback removed.
- Regression areas checked: Weekly Digest print and alert links; Dashboard Today list (all TL scenarios, both themes); System Status endpoint count; Performance Summary and Compliance landing; Journal Red flags and Reflections landing; API contract drift (154 → 155 endpoints, three-way match); API performance baseline drift.
- Known deviations: none found — every story's deviation check completed with nothing to file.

**CI record:** ST-14 `a5438839`: all 11 workflows success (Playwright E2E 46014242050, CI Pytest 46014242227, Frontend Unit Tests 46014242233). ST-15/ST-16 `d64cc465`: 10 of 11 success; Playwright E2E 46018942348 failed only SC-RF-08 (`rules-filter.spec.js`, EPIC-02 ST-13), which also fails about 1 run in 4 locally against main's own build (`e156a6f7`); diagnosed as a Trade History restore/save race and filed as BLG-FE-339 (P2); every digest scenario passed in that run. ST-17 `544ebe49`: all 11 workflows success — Playwright E2E 46034062351 (all shards, every digest, Today list and system-status scenario, and SC-RF-08 passing this run), CI Pytest 46034062693, Frontend Unit Tests 46034062682, Lighthouse 46034062423. Pre-PR review fix `f176cddc` (backend only: alert counts null on failure): all 7 workflows it triggers success (CI Pytest 46034904257, Critical-Path Smoke 46034904374); no `src/` change, so the Playwright E2E result on `544ebe49` stands for the frontend.

## Pre-PR Agent-Mediated Reviews (2026-11-27)

**[Agent-mediated review — on behalf of Director of Quality, pending human confirmation]** ❌ Blocked, then cleared. Sole blocker: CI for `544ebe49` was still running (Playwright E2E, CI Pytest, Lighthouse); cleared when all 11 workflows succeeded (Playwright E2E 46034062351). No code defects found. Also applied: BLG-FE-339 acceptance record (below); migration wording corrected to match `data_model.md` DS-43; ST-17 row states why the Reviews count is unlinked. Checks it ran, with outputs: AC coverage and every cited test ID found; grading (Pass holds; the two addendum corrections are design-gated, not narrowings); route rules (contract heading `digest_endpoints.md:130`, OpenAPI path, `test.py` entry with `dry_run`, AST count 133 = fallback 133 = SC-SS-01b); `check_api_performance_baseline_drift.py` PASSED; `check_openapi_drift.py` 155/155 no drift; execution-state consistency OK; backlog integrity OK; 27 `spec_references` resolve; 5 commits all `[EPIC-03]`; 8 Last Updated headers within 3 entries.

**[Agent-mediated review — on behalf of Product Owner, pending human confirmation]** ⚠️ Approved with Comments. Rulings confirmed applied. Fixed: a failed alerts query now gives `null` ("Not available"), not "0" (`f176cddc`); the behaviour-change list completed (renamed labels, description, new links, rollback); the migration note corrected. Points for the human Product Owner, taken in the acceptance below: deprecated `compliance_score_*` aliases for ST-14 AC 1; the 1.5 s wait; the `due_today_action` tracking; the System Status cleanup; BLG-FE-339; final CI; the migration.

### Product Owner and Director of Quality acceptance (the user, in session, 2026-11-27T16:43:07Z)

The user, who holds the Product Owner and Director of Quality roles, gave both in session: Director of Quality "Sign off"; Product Owner "Accept all". Recorded as given:

1. **Accepted:** every behaviour change listed below, including the up-to-1.5 s wait for the opened event, `due_today_action` as the only new tracking, System Status deleting its test plan, and "Not available" for failed counts.
2. **Accepted:** ST-14 AC 1 is met with `compliance_score_*` kept as deprecated API aliases (same values), as the story scope asked.
3. **Accepted:** `loop_events` self-creates on first use; the deploy migration (Human-Delegation, Infrastructure & Operations Owner) only confirms it.
4. **BLG-FE-339 (P2), accepted for v9.19 by both the Product Owner and the Director of Quality.** Rationale: pre-existing in EPIC-02's Trade History code, not caused by EPIC-03 (EPIC-03 does not touch `TradeHistory.js` or `rules-filter.spec.js`); reproduces about 1 run in 4 against main's own build; no data loss (the Rules filter only resets to All); EPIC-03's final Playwright run passed.
5. Follow-ups BLG-BE-238 and BLG-BE-239 are P3.
6. Confirmed again by the user ("give DOQ and PO acceptance") at 2026-11-27T16:49:15Z and posted on PR #2314 at their direction: https://github.com/sachiv1984/swing-trading-model/pull/2314#issuecomment-7223712359

## Rulings and decisions recorded during execution

All given by the user in session, holding the named role, on 2026-11-27:

- Metrics Definitions & Analytics Owner / Product Owner (ST-14): add `closed_trades_total_7d_ago`, so a week in which every trade closed reads "A week ago: no closed trades", not "0.0%".
- Product Owner (ST-15, time-boundary check): realised P&L's window covers 8 calendar dates while alerts and red flags use 7 × 24h; keep the "last 7 days" labels and file a P3 follow-up (BLG-BE-238).
- Head of UX & Design (ST-16): the realised P&L link adds `period=last_7_days`, so Performance Summary shows the same figure; the Journal Red flags list stays unfiltered, newest first.
- Head of UX & Design (ST-15): "Alerts, last 7 days", not "Alerts sent" (the count is every alert raised; a Feed row can be "Not sent"); description "Most figures link to the page where you review them."
- `ESC-EXEC-20261127-01` — Metrics Definitions & Analytics Owner (ST-17): Signals count distinct (ticker, market); Reviews count distinct UTC days; the Due today action is recorded, not counted; steps are dated by `created_at`; §Core Loop Metrics approved as drafted. ST-17 reclassified `autonomous`.

## Behaviour changes to note for acceptance

- The Weekly Digest is a list of five figures, not a Field/Unit/Value table; "Data Staleness" and "As of (UTC)" become one caption; "Alerts Dismissed (7d)" is the alerts row's "{n} marked read" line (same link); a missing open-P&L change reads "Not enough history yet" (was "—"); realised P&L is signed (+£166.10).
- Labels renamed: "Compliance Score (current)" and "(7d ago)" become "Journal completion (all closed trades)" with an "A week ago: …" second line; "Unrealised P&L Delta (7d)" becomes "Change in open P&L, last 7 days"; "Alerts Fired (7d)" becomes "Alerts, last 7 days"; "Realised P&L (7d)" becomes "Realised P&L, last 7 days". New "Red flags, last 7 days" row and "This week's loop" section. The description "7-day trading summary" becomes "Your last 7 days in figures. Most figures link to the page where you review them."
- New links: journal completion → Performance Compliance; realised P&L → Performance Summary; red flags → Journal Red flags; the five loop counts (except Reviews) → their list pages.
- A failed optional digest query no longer makes the later figures fall back to their defaults (each is rolled back); a failed alerts, journal completion or red flags query reads "Not available" (the alerts API fields are `null`, were 0).
- Journal completion reads "No closed trades yet" with no closed trades, and "Not available" when its query fails; the deprecated `compliance_score_*` API fields keep their old values and 0.0 on failure.
- Realised P&L opens Performance on "Last 7 Days", not the page's default "Last Month". The two match while the server runs on UTC (BLG-BE-239 makes the analytics cutoff UTC).
- The Red flags figure counts the last 7 days; its link opens the full Red flags list, newest first.
- The Weekly Digest shows a loading state for up to 1.5 s while the opened event is written, so Reviews include the visit.
- A System Status "Run Tests" run now deletes the draft AAPL trade plan its `POST /trade-plans` check creates (it was left behind on every run).
- A click on a Today list item link (Review exit, Grace ends today, Stops moved, Research, Plan this) now also sends one `POST /digest/events`; navigation is unchanged.
- `loop_events` is created by the first `POST /digest/events` after deploy (`CREATE TABLE IF NOT EXISTS`), so the first Weekly Digest visit both creates it and records itself; until that first event, Reviews reads "Not available". The planned production migration at deploy (Human-Delegation, Infrastructure & Operations Owner) then only confirms the table and index (DS-43 Verification); it is needed only if the production role cannot create tables, in which case Reviews stays "Not available" until it runs.

## Follow-ups filed during this EPIC

- BLG-BE-238 (P3) — make the realised P&L window 7 dates, or name it (ST-14 first-time-right check 8; Product Owner ruling).
- BLG-BE-239 (P3) — use the UTC date for the analytics period cutoffs (ST-16 review).
- BLG-FE-339 (P2) — Trade History does not always restore the stored rules option; SC-RF-08 fails intermittently, on main too (found in EPIC-03's CI; EPIC-02's code). Accepted for v9.19 by the Product Owner and the Director of Quality, 2026-11-27 (rationale above).

## Standard Sign-Off Block

- [x] All acceptance criteria verified against canonical spec
- [x] No unresolved P0 or P1 deviations
- [x] Regression areas checked
- [x] For any frontend component making direct URL construction (not via api.* wrapper): confirm the URL-base variable is exposed on the imported object (`WeeklyDigest.js` and `src/api/loopEvents.js` build `${REACT_APP_API_URL}/digest/...` with the same `API_BASE_URL` constant pattern as the existing digest fetch)
- [x] **Strategy values checked:** N/A — no stop/grace/ATR/exit/sizing logic touched
- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-11-27
- Comments: Entered at the explicit direction of the user, who holds the Director of Quality role, in session at 2026-11-27T16:43:07Z, after the pre-PR agent-mediated reviews (Director of Quality ❌ Blocked on pending CI, then cleared; Product Owner ⚠️ Approved with Comments, all fixed). Results per the Consolidation Block: ST-14 to ST-17 Pass, no deviations. Frontend-visible changes: every observable AC has Playwright coverage, observed passing in real CI — Playwright E2E 46034062351 on `544ebe49` (all shards); the later commit `f176cddc` changes no frontend code and passed CI Pytest 46034904257. Post-open CI fixes: none yet (PR not opened). Interaction-timing ACs (opened event before the digest request, SC-DIG-13; Today list clicks, SC-TL-31) observed passing in that real CI run. P2 found defect BLG-FE-339 accepted for v9.19 by the Product Owner and the Director of Quality (rationale in the acceptance above).

## Merge Gate Confirmations

Written when the merge is recorded.
