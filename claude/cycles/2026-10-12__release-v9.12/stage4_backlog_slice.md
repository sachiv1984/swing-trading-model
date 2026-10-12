Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-12
Cycle: 2026-10-12__release-v9.12
Release: v9.12

# Backlog Slice — v9.12

<!-- release-plan-marker: RP:v9.12:2026-10-12__release-v9.12 -->

48 stories across 6 EPICs, 27.95 estimated days. The acceptance criteria below are the source of truth for Sprint Planning and Execution. Scope is sized to the top of the confirmed ~24–28 day capacity band, per the explicit user instruction "use full capacity" (2026-10-12).

**Ready pool:** 101 items, 54.70 days (after the STEP 4 calibration raises).

**Selection method** (`release_planning_prompt.md` §1.4c):
1. The 1 ready P1 item.
2. All 8 seatable P2 items (`BLG-TECH-21` deferred by override, as at v9.10 and v9.11).
3. A category-balanced, oldest-first round-robin over P3/P4, run until 0.05 days were left.

The roadmap-committed item (`BLG-BE-162`; Product Owner direction 2026-10-12, DL-085) seats mechanically in the P1 pass.

**Where an item's own AC is stale, untestable or depends on another story, the AC below restates it.** Any change from the source backlog item is marked *(restated)* with the reason.

---

## EPIC-01 — AI Feature Correctness & Cost Visibility

**Maps to:** S2-01 – S2-06
**Owner:** Backend Engineering Patterns Owner; AI Compliance & Governance Officer; Infrastructure & Operations Owner
**Description:** Fix the journal summary's HTTP 422 on UUID trade IDs (P1, a condition of v9.11's verification acceptance), stop the daily briefing inventing tickers or misreading starting cash, check stop-time citations in briefing and chat, widen the monthly narrative's directive scan, and make the daily AI cost alert count Claude spend.
**Estimated days:** 2.80

### ST-01 — Accept UUID trade IDs in the journal summary, end to end
**Source:** BLG-BE-162
**Priority:** P1
**Effort:** S (~0.5d; calibrated to 1.0d — live migration plus staging verification)
**Delegation note:** The `ai_audit_log.trade_ids` migration must be applied on staging and production, and AC 1 needs a staging run from Trade History. Expected Human-Delegation to the Data Model & Domain Schema Owner with the Infrastructure & Operations Owner (RISK-01), following DS-27/28/29 at v9.11.
**Sequencing:** First in EPIC-01. P1, seated per the v9.11 verification acceptance condition (`closure_record.md` §6 row 1).
**UI-facing:** No (restores an existing feature; no rendering change)
**Acceptance Criteria:**
- A journal summary requested from Trade History on staging returns generated content
- The run is written to `ai_audit_log` with the UUID trade IDs
- A backend test posting UUID `trade_ids` passes; integer IDs are rejected with 422
- The `INTEGER[]`→`UUID[]` migration is recorded in `data_model.md` and applied on staging and production, with verification output; `ai_endpoints.md` and `openapi.yaml` describe `trade_ids` as "array of string (UUID)" in the same commit as the code *(restated: the item's Scope made testable, as for v9.11 ST-06)*

### ST-02 — Drop briefing actions that name a ticker outside the context
**Source:** BLG-AI-11
**Priority:** P2
**Effort:** S (~0.5d)
**Sequencing:** Before ST-03 and ST-04 (same prompt module; each bumps `BRIEFING_PROMPT_VERSION`, or Sprint Planning may combine the bumps).
**UI-facing:** No (filters model output; no rendering change)
**Acceptance Criteria:**
- A fixture briefing response with an ENTER for an unknown ticker is not returned as an action, and the drop is logged
- Golden-fixture tests pass with the recorded prompt-version bump

### ST-03 — Label available cash and starting capital separately in the briefing context
**Source:** BLG-AI-12
**Priority:** P3
**Effort:** XS (<1h plus tests)
**Sequencing:** After ST-02.
**UI-facing:** No
**Acceptance Criteria:**
- The briefing context no longer uses "of £{initial_cash}", and omits starting capital when it is 0
- Golden-fixture tests pass with the recorded prompt-version bump

### ST-04 — Check that briefing and chat responses citing a stop include its recalculation time
**Source:** BLG-AI-10
**Priority:** P3
**Effort:** S (~0.5d)
**Delegation note:** AI Compliance & Governance Officer sign-off on the failure action (append the time from context, or log and count) is the first sub-step.
**Sequencing:** After ST-02/ST-03 (same briefing module).
**UI-facing:** No
**Acceptance Criteria:**
- A fixture response citing a stop without its time is caught; one with the time passes
- The chosen failure action is applied and tested for both briefing and chat
- The check is added to the boundary-sample audit, so sampled outputs are scored on it *(restated: Scope item 3 made testable)*

### ST-05 — Widen the monthly P&L narrative's instrument-directive scan to inflected and indirect wording
**Source:** BLG-AI-13
**Priority:** P3
**Effort:** XS (<1h plus tests)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- "Consider buying MSFT" and "sell the position" are reported as `instrument_directive`
- Past-tense reporting ("you sold 9 trades") is not reported (negative B-MPN-04 case) *(restated: Scope's no-false-positive requirement made testable)*
- The representative output and the code-written fallback still scan clean
- `tests/test_monthly_pnl_narrative.py` passes

### ST-06 — Make the daily AI cost alert count Claude calls
**Source:** BLG-OPS-183
**Priority:** P2
**Effort:** S (~0.5 day)
**Sequencing:** Independent. Shares `ai_endpoints.md` with ST-01; land after ST-01 or rebase.
**UI-facing:** No
**Acceptance Criteria:**
- A pytest showing a `claude_audit_log` row counted in the daily total, a plan-generation call counted once, and the alert firing when Claude spend passes the threshold
- The scheduler that calls `POST /ai/check-daily-cost` named in `ai_endpoints.md`, with its last successful run recorded
- The ST-23 cost estimate notes the corrected coverage

---

## EPIC-02 — Stop, Sizing & Position Correctness (build-and-ship)

**Maps to:** S2-07 – S2-16
**Owner:** Head of Engineering; Strategy Rules & System Intent Owner; Backend Engineering Patterns Owner
**Description:** Fix signal sizing (zero-ATR allocation, missing fees) and cover the FX and cash paths, make the Trail Stop action work or remove it, keep stops from rounding down or crashing on NULL fill prices, make LOSING/PROFITABLE agree across pages, use the US exchange calendar for gap risk, surface frozen stops, and stop first-time Settings saves writing NULLs.
**Estimated days:** 5.55

### ST-07 — Give zero-ATR signals no allocation in batch sizing
**Source:** BLG-BE-157
**Priority:** P2
**Effort:** S (~0.5d)
**Sequencing:** First in EPIC-02 (with ST-08, same function).
**UI-facing:** No (value change on the Signals page; no rendering change)
**Acceptance Criteria:**
- In a mixed batch, a zero-ATR signal gets `suggested_shares` 0, `inv_vol_weight` 0 and a reason, and the other signals' weights sum to 1.0
- The existing all-zero and capping tests still pass

### ST-08 — Include entry fees in batch signal total cost
**Source:** BLG-BE-158
**Priority:** P2
**Effort:** XS (<1h plus tests)
**Sequencing:** After ST-07 (same function).
**UI-facing:** No (value change on the Signals page; no rendering change)
**Acceptance Criteria:**
- A UK batch signal's `total_cost` equals gross cost plus stamp duty and commission; a US signal's includes the FX fee in the documented currency
- `signal_endpoints.md` states the currency of `total_cost`

### ST-09 — Assert the §4.1.5 FX defaulting/echo and §4.1.6 insufficient-cash sizing results in CI
**Source:** BLG-QA-205
**Priority:** P3
**Effort:** S (~0.5d)
**Sequencing:** After ST-07/ST-08 (same service module).
**UI-facing:** No
**Acceptance Criteria:**
- Each clause (C4.1.5-01/02/03, C4.1.6-01/02) is asserted by a CI-run test; the traceability matrix rows are updated to Asserted

### ST-10 — Make the Trail Stop action work against a real route, or remove it; stop ignoring a supplied entry stop
**Source:** BLG-BE-159
**Priority:** P2
**Effort:** S (~0.5-1d)
**Delegation note:** Strategy Rules & System Intent Owner ruling on whether a user may set or raise a stop manually under `strategy_rules.md` §7.3 is the first sub-step (`delegated_decision`, RISK-02).
**Sequencing:** Ruling first. Before ST-15 (both edit `Positions.js` and the stop cell area).
**UI-facing:** Yes (Trail Stop modal action)
**Acceptance Criteria:**
- The Strategy Rules & System Intent Owner ruling is recorded before the code change *(restated: Scope's decision step made testable)*
- The Trail Stop modal's action succeeds against a real route, or the action is gone; a Playwright test covers whichever ships
- A supplied entry stop is either stored or rejected with a clear error, never silently ignored
- If a route is added: contract (`##` heading), `openapi.yaml`, `backend/routers/test.py`, the `SystemStatus.js` fallback count and `SC-SS-01b` are updated in the same commit (CLAUDE.md §2) *(restated: registration chain made explicit; see RISK-04)*

### ST-11 — Never let 2-dp rounding lower a stored stop
**Source:** BLG-BE-160
**Priority:** P3
**Effort:** XS (<0.5d)
**Sequencing:** Before ST-12 (same two recompute paths).
**UI-facing:** No
**Acceptance Criteria:**
- A test with a 4-dp stored stop that the recompute keeps shows the written value is never below the stored one, on both the on-load and nightly paths

### ST-12 — Recompute US positions with a NULL fill_price without error, and add US parity cases
**Source:** BLG-BE-145
**Priority:** P3
**Effort:** S (~0.5 day)
**Sequencing:** After ST-11.
**UI-facing:** No
**Acceptance Criteria:**
- A NULL `fill_price` US position recomputes without error on both paths. `tests/test_strategy_parameter_parity.py` and `tests/test_atr_provenance.py` include a US case

### ST-13 — Decide Risk page LOSING/PROFITABLE on native P&L, matching the lifecycle badge
**Source:** BLG-BE-149
**Priority:** P3
**Effort:** S (~0.5 day)
**Sequencing:** Independent.
**UI-facing:** Yes (status shown on the Risk page can change for US positions)
**Acceptance Criteria:**
- For a US position with native P&L > 0 and GBP P&L < 0, `display_status` and `position_state` agree (unit test)
- `position_endpoints.md` / `portfolio_endpoints.md` state the basis of `display_status` *(restated: Scope's documentation step made testable)*

### ST-14 — Use the US exchange calendar for the gap-risk "next trading session"
**Source:** BLG-BE-148
**Priority:** P3
**Effort:** S (~1 day)
**Delegation note:** If the change alters Ruling 3's stated rule, the Strategy Rules & System Intent Owner records a dated addendum in the §13 review record.
**Sequencing:** Independent.
**UI-facing:** No (which positions are flagged can change; no rendering change)
**Acceptance Criteria:**
- A Friday view before a Monday holiday flags Tuesday earnings (unit test)
- A 02:00 UTC view uses the US market date (unit test)
- The calendar is deterministic, with no network call at request time *(restated: Scope constraint made testable)*
- If Ruling 3's rule changes, the dated addendum in `decisions--2026-09-30__release-v9.9--gap-risk-flag-section13-review.md` answers each `strategy_rules.md` §13 clause that names the Gap Risk Flag's subject: §13.3 (the display-only carve-out, including its "falls before that position's next trading session" limb, which this story changes) and §13.5 (the roster row and the 2027-02-06 re-attestation); §13.1/§13.2 apply generally *(restated: §13 clause-citation rule, `release_planning_prompt.md` STEP 4, v2.61)*

### ST-15 — Show the user when a position's stop is frozen for lack of ATR
**Source:** BLG-FE-202
**Priority:** P3
**Effort:** S (~1 day)
**Sequencing:** After ST-10 (both touch the Positions stop area).
**UI-facing:** Yes (Positions stop-cell indicator)
**Acceptance Criteria:**
- A position whose last recompute had no ATR shows a visible indicator on Positions (Playwright). Contract and `openapi.yaml` updated in the same commit
- The nightly job's ATR-unavailable skip sets the same indicator *(restated: the Problem's nightly-path gap made testable)*

### ST-16 — Keep first-time Settings saves from writing NULL strategy columns; snapshot §11 values on trade plans
**Source:** BLG-BE-144
**Priority:** P3
**Effort:** S (~0.5 day)
**Sequencing:** Before ST-26 (EPIC-04, same `create_settings` path; cross-EPIC, RISK-05).
**UI-facing:** No
**Acceptance Criteria:**
- A first-time Settings save leaves the four columns at their defaults (API or Playwright test of the create path)
- New trade-plan snapshots carry the §11 values

---

## EPIC-03 — Trade Entry, Settings & Accessibility (build-and-ship)

**Maps to:** S2-17 – S2-24
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner; Head of Engineering
**Description:** Let Trade Entry preview the stop, risk and size before save, show and validate the ATR unit, cover the sizing widget, correct the Settings helper text and centralise strategy numbers, link and align the Grace Period panel, and fix light-theme and amber-badge contrast.
**Estimated days:** 7.05

### ST-17 — Add an ATR preview endpoint so Trade Entry shows the stop, risk and size before save
**Source:** BLG-BE-146
**Priority:** P3
**Effort:** S (~1 day)
**Sequencing:** First in EPIC-03. Before ST-18 and ST-19 (same page).
**UI-facing:** Yes (Trade Entry preview)
**Acceptance Criteria:**
- With a ticker and entry price entered and ATR blank, Trade Entry shows a numeric system stop, risk and suggested shares before save (Playwright, mocked endpoint)
- The stop shown before save equals the `initial_stop` returned by `POST /portfolio/position` for the same inputs (backend test)
- When the endpoint returns no ATR, the existing "Calculated on save" states remain
- The new endpoint has a contract `##` heading, an `openapi.yaml` entry, a `backend/routers/test.py` entry, and updated `SystemStatus.js` fallback count and `SC-SS-01b`, in the same commit (CLAUDE.md §2) *(restated: registration chain made explicit; see RISK-04)*

### ST-18 — Show the currency unit on Trade Entry's ATR field and reject implausible typed ATRs
**Source:** BLG-FE-203
**Priority:** P3
**Effort:** S (~0.5 day)
**Sequencing:** After ST-17.
**UI-facing:** Yes (ATR label and inline warning)
**Acceptance Criteria:**
- The ATR label shows £ for UK and $ for US (Playwright)
- A typed ATR whose 5× multiple meets or exceeds the entry price is rejected by the API with a 400 and an explanatory message (backend test)
- Trade Entry shows the warning inline and disables submit for that input (Playwright)

### ST-19 — Cover the §4.1.7 sizing-widget behaviours with Playwright
**Source:** BLG-QA-206
**Priority:** P3
**Effort:** M (~1d)
**Sequencing:** After ST-17/ST-18 (tests the changed page).
**UI-facing:** No (tests only)
**Acceptance Criteria:**
- Each listed clause (C4.1.7-01/02/03/05/06/07/08) has a passing CI Playwright scenario with mocked `POST /portfolio/size`; matrix rows updated

### ST-20 — Correct the Settings helper text for the fixed strategy parameters
**Source:** BLG-FE-201
**Priority:** P3
**Effort:** XS (<0.5 day)
**Sequencing:** Before ST-21 (ST-21 moves these numbers into the constants module).
**UI-facing:** Yes (wording only)
**Acceptance Criteria:**
- Each helper line matches `strategy_rules.md` §6/§7.2 wording; covered by Playwright text assertions (wording-only, FI-P3-02 may apply); `settings.md` §1 updated

### ST-21 — Strategy-copy conformance: a frontend constants module, a CI lint for UI text restating §5–§11, and a named owner
**Source:** BLG-GOV-369
**Priority:** P3
**Effort:** S (~1-1.5 days)
**Delegation note:** The charter change in `claude/agents/frontend_specs_ux_documentation_owner.md` needs Director of HR authority (RISK-06).
**Sequencing:** After ST-20 and ST-18. Before ST-26 (EPIC-04 adds a line to Settings; cross-EPIC, RISK-05).
**UI-facing:** Yes (page text sourced from constants; no intended visible change)
**Acceptance Criteria:**
- No strategy-number literals in `TradeEntry.js`, `Settings.js`, `Positions.js` or `SignalContextPanel.js` outside `src/constants/strategy.js`
- The lint runs in CI and reports zero contradictions once ST-20 has landed *(restated: `BLG-FE-196`/`197` shipped in v9.10, and `BLG-FE-195`'s scope was delivered by v9.10 ST-01)*
- The Frontend Specifications & UX Documentation Owner charter names the duty

### ST-22 — Link each Grace Period row to its position, and align the panel's text and date format with the spec
**Source:** BLG-FE-207
**Priority:** P3
**Effort:** S (~0.5 day)
**Delegation note:** Product Owner may prefer the shipped text, in which case `risk_dashboard.md` §5.2 is amended instead.
**Sequencing:** Independent.
**UI-facing:** Yes (link, heading, badge, date format)
**Acceptance Criteria:**
- Playwright: clicking a grace row opens the Positions page showing that position
- Heading, badge and date format match `risk_dashboard.md` §5.2, or §5.2 is amended to the shipped text (wording-only ACs may be code-reviewed per FI-P3-02)

### ST-23 — Make the Reports and Notifications pages pass WCAG colour contrast in the light theme
**Source:** BLG-FE-200
**Priority:** P3
**Effort:** M (~2-3 days)
**Delegation note:** Head of UX & Design (with the Product Owner) decides whether light mode is a supported theme. This is a pre-sprint decision (RISK-03), expected at the design gate.
**Sequencing:** Decision first. Independent of other stories.
**UI-facing:** Yes (light-theme colours)
**Acceptance Criteria:**
- If light mode is supported: light-mode colour tokens are added to `design_system.md`, and the light-theme Reports (Monthly, Tax Year) and Notifications (Preferences, History) axe scans pass with no `color-contrast` entry in the light-theme `KNOWN_VIOLATIONS` baseline
- If light mode is not supported: the decision is recorded in `design_system.md`, and the theme toggle and baseline are handled as that decision specifies *(restated: the Scope's decision step can lead to either branch; the source AC covered only the first)*

### ST-24 — Move white-on-amber-600 badges to a passing contrast outside Replay
**Source:** BLG-FE-210
**Priority:** P3
**Effort:** XS (<1h plus test updates)
**Sequencing:** Independent.
**UI-facing:** Yes (badge colour)
**Acceptance Criteria:**
- No `bg-amber-600 text-white` pair remains in `src/`
- The affected specs pass; an axe scan of each changed component reports no `color-contrast` finding on the badge

---

## EPIC-04 — Security, Operations & Platform

**Maps to:** S2-25 – S2-32
**Owner:** Infrastructure & Operations Owner; Cybersecurity & Trust Lead; FinOps & Resource Architect
**Description:** Stop false post-grace stop-health alerts, audit strategy-parameter changes, re-rate the bundled frontend key, apply the in-range dependency bumps, settle the staging deploy-hook question and live-fire the stale-staging check, fix the local setup instructions, and inventory the scheduled workflows.
**Estimated days:** 5.05

### ST-25 — Stop the post-grace stop-health monitor alerting on the morning a position's grace ends
**Source:** BLG-OPS-184
**Priority:** P2
**Effort:** S (~0.5d)
**Delegation note:** Option (b) changes live stop behaviour and needs a Strategy Rules & System Intent Owner ruling first. Option (a) does not.
**Sequencing:** First in EPIC-04.
**UI-facing:** No
**Acceptance Criteria:**
- `tests/test_post_grace_stop_health.py` passes the new day-10 fixture and still fails `non_s11_multiplier.json` and `missing_stop.json`
- A post-grace position whose multiplier stays null beyond the tolerance window is still reported as a violation (test)
- The chosen option is recorded in the script docstring *(restated: Scope step made testable)*

### ST-26 — Audit trail for strategy-parameter changes in Settings
**Source:** BLG-SEC-41
**Priority:** P3
**Effort:** S (~1 day; calibrated to 1.5d — new table, live migration)
**Delegation note:** The change-log table's migration must be applied on staging and production. Expected Human-Delegation to the Data Model & Domain Schema Owner with the Infrastructure & Operations Owner (RISK-01).
**Sequencing:** After ST-16 (EPIC-02) and ST-20/ST-21 (EPIC-03); cross-EPIC, RISK-05.
**UI-facing:** Yes (last-change line on Settings)
**Acceptance Criteria:**
- Every settings write produces a log row with field, old value, new value, timestamp and request source (test)
- The Settings page shows the last change (Playwright) *(restated: Scope item made testable)*
- The migration is recorded in `data_model.md` and applied on staging and production, with verification output *(restated: Scope's storage made testable)*

### ST-27 — Re-assess the bundled `REACT_APP_API_KEY` against its actual write scope
**Source:** BLG-SEC-42
**Priority:** P3
**Effort:** S (~0.5 day)
**Delegation note:** If the decision is to accept the risk, the Product Owner records it.
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- `credential_policy.md`'s classification states the key's write scope and the decision taken (a narrower frontend key, or an explicit Product Owner accept-risk)

### ST-28 — Apply the in-range dependency patch/minor bumps from the October 2026 quarterly review
**Source:** BLG-TECH-22
**Priority:** P3
**Effort:** S (~0.5-1 day)
**Delegation note:** AC 2 needs a staging deploy of the bumped build. Human-Delegation to the Infrastructure & Operations Owner if the governed environment cannot run it.
**Sequencing:** Late in the sprint, after the other EPIC-03/EPIC-04 frontend changes, so one full CI run covers the final tree.
**UI-facing:** No
**Acceptance Criteria:**
- The 8 backend and 20 frontend bumps listed in `docs/security/dependency_update_review_2026-10-06.md` §3–§5 are applied in one PR. The full pytest suite and all Playwright shards pass in CI, including the focus-restoration specs
- A staging check confirms yfinance price and ATR fetches still work for one US and one UK ticker

### ST-29 — Find out why a staging-deploy.yml hook deploy of a governance-only commit never went live
**Source:** BLG-OPS-181
**Priority:** P3
**Effort:** XS (<1h)
**Delegation note:** Needs Render dashboard access. Expected Human-Delegation to the Infrastructure & Operations Owner (RISK-01).
**Sequencing:** Before ST-30 (both concern staging deploys).
**UI-facing:** No
**Acceptance Criteria:**
- The cause is recorded against this item
- If it is a Build Filter: `docs/ops/staging_deploy_notes.md` says whether a `workflow_dispatch` deploy of a non-code commit is expected to go live

### ST-30 — Live-fire the stale-staging check from main against a deliberate divergence
**Source:** BLG-OPS-182
**Priority:** P3
**Effort:** XS (<1h; calibrated to 0.5d — deliberate staging divergence and restore)
**Delegation note:** Needs control of staging deploys and a real Telegram receipt. Expected Human-Delegation to the Infrastructure & Operations Owner (RISK-01).
**Sequencing:** After ST-29. The item's "EPIC-04 (v9.10) merged" dependency is met *(restated)*.
**UI-facing:** No
**Acceptance Criteria:**
- A failing `main` run URL showing `STALE STAGING DEPLOY` for the deliberate divergence, with the Telegram alert received
- A passing `main` run URL after staging is restored

### ST-31 — Add requirements-dev.txt to the local backend setup instructions
**Source:** BLG-OPS-185
**Priority:** P3
**Effort:** XS (<1h)
**Delegation note:** Mentioning `requirements-dev.txt` in CLAUDE.md §9 needs Head of Specs Team agreement.
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- Following `README.md` from a fresh clone yields a venv in which `backend/.venv/bin/python3 -m pytest --collect-only -q` succeeds
- `grep -rn "pip install -r .*requirements.txt" README.md docs/ops/quarterly_dependency_upgrade_cadence_policy.md` shows `requirements-dev.txt` alongside every test-running install

### ST-32 — Inventory the scheduled GitHub workflows: owner, cron, tables written, monthly minutes
**Source:** BLG-GOV-371
**Priority:** P3
**Effort:** S (~1 day)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- One table in `docs/ops/` lists every scheduled workflow with owner, cron, a "writes" column and minutes/month, and states that it is reviewed at each `run audit`

---

## EPIC-05 — Spec & Data Model Hygiene

**Maps to:** S2-33 – S2-38
**Owner:** Data Model & Domain Schema Owner; API Contracts & Documentation Owner; Head of Specs Team
**Description:** Settle the DELETE envelope exception, triage the drift detector's new findings, correct the Gap Risk Badge's data source and the action-rate column, refresh the Gap Risk Flag §13 record, and settle `positions.entry_price`'s currency.
**Estimated days:** 2.10

### ST-33 — Reconcile DELETE /trade-plans/{id}'s success envelope with conventions.md §12
**Source:** BLG-SPEC-176
**Priority:** P4
**Effort:** XS (<1h)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- `DELETE /trade-plans/{id}`'s documented response and its live behaviour agree, and `conventions.md` §12 either lists this endpoint as an explicit exception or the endpoint is migrated to the standard DELETE envelope

### ST-34 — Triage the drift detector's new live-vs-doc findings
**Source:** BLG-SPEC-178
**Priority:** P3
**Effort:** S (~1d)
**Delegation note:** Finding 1 (DS-17's index absent on staging) needs a read of production's `pg_indexes`. Expected Human-Delegation to the Data Model & Domain Schema Owner (RISK-01).
**Sequencing:** Before ST-38 (both edit `data_model.md`).
**UI-facing:** No
**Acceptance Criteria:**
- Each of the 5 findings has an explicit disposition recorded (matches known pattern / needs live action / false positive / documentation fix), with each of finding 5's 11 names checked individually
- Any genuine gap gets its own canonical-spec correction or migration-scheduling item, per the `BLG-SPEC-150`/`BLG-SPEC-151` precedent

### ST-35 — Name the Gap Risk Badge's real data source in positions.md
**Source:** BLG-SPEC-179
**Priority:** P3
**Effort:** XS (<0.5 day)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- `positions.md` §Gap Risk Badge names `GET /positions/{position_id}/gap-risk`; no remaining reference claims a `gap_risk` field on `GET /positions`; version bump and changelog row added

### ST-36 — Replace positions.stop_price with current_stop in the action-rate spec and docstring
**Source:** BLG-SPEC-181
**Priority:** P3
**Effort:** XS (<1h)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- No spec or code comment refers to `positions.stop_price` as a live column
- `grep -rn "positions.stop_price" docs backend` returns only historical/migration references (DS-24)

### ST-37 — Refresh the Gap Risk Flag §13 decision record to match strategy_rules.md v1.14
**Source:** BLG-SPEC-182
**Priority:** P3
**Effort:** XS (<1h)
**Sequencing:** Coordinate with ST-14 (EPIC-02), which may add an addendum to the same record; land ST-37 first if both run.
**UI-facing:** No
**Acceptance Criteria:**
- No statement in the record's body contradicts `strategy_rules.md` v1.14 §13.3/§13.5 or describes `BLG-GOV-360` as pending
- Binding Condition 6's permitted-trigger scope equals §13.3's carve-out
- §13 clause citation: §13.3 and §13.5 are the clauses naming the Gap Risk Flag; §13.1/§13.2 apply generally. No other §13 clause names gap risk *(restated: §13 clause-citation rule, v2.61)*

### ST-38 — Settle positions.entry_price's currency in the specs
**Source:** BLG-SPEC-183
**Priority:** P3
**Effort:** S (~0.5d; includes a read-only live sample check)
**Delegation note:** The read-only sample of live US rows needs database read access. The sandbox's `DATABASE_URL` points at staging, and querying it requires the user's permission; a production sample is a Human-Delegation to the Data Model & Domain Schema Owner (RISK-01).
**Sequencing:** After ST-34.
**UI-facing:** No
**Acceptance Criteria:**
- `data_model.md`, `data_model_positions_dictionary.md` and DS-23 state one consistent `entry_price` currency that matches `create_position()`'s input
- The dictionary's US `total_cost` derivation matches `position_service.py`'s computation
- The decision (doc fix vs code fix) is recorded with Data Model & Domain Schema Owner sign-off

---

## EPIC-06 — Governance Tooling & Test Integrity

**Maps to:** S2-39 – S2-48
**Owner:** Head of Specs Team; PMO Lead; QA & Testing Owner; Director of Quality
**Description:** Check backlog item integrity after merges, report gates whose gating item has shipped, script the state read-back, settle the Skill-Silo aggregation method and reduced-roster idea windows, add split-credit and tests to the role-share script, scope `utils.*` test stubs, guard the `fees_paid` invariant, and remove a leaked sandbox path.
**Estimated days:** 5.40

### ST-39 — Check backlog item integrity after every cross-EPIC merge resolution
**Source:** BLG-GOV-385
**Priority:** P2
**Effort:** S (~0.5d)
**Delegation note:** Edits CLAUDE.md §8 under Head of Specs Team authority (RISK-06).
**Sequencing:** First in EPIC-06. Until it merges, the manual check in v9.11 closure Carry-Forward #3 stays in force (RISK-07).
**UI-facing:** No
**Acceptance Criteria:**
- `scripts/check_backlog_item_integrity.py` fails on `3237cb5e`'s `backlog.md` and passes on the repaired file
- The check is wired into CI on PRs touching `backlog.md` and named in CLAUDE.md §8

### ST-40 — Report gated items whose gating backlog item has shipped, and read that list in Release Planning §1.3a
**Source:** BLG-GOV-386
**Priority:** P2
**Effort:** S (~0.5–1d)
**Sequencing:** Before ST-41/42/43 if they also bump `OPERATIONAL_GUIDE.md`, so the bumps stay sequential on one branch.
**UI-facing:** No
**Acceptance Criteria:**
- Running the script against a fixture where a gate names only an archived item lists that item under the new heading
- An item whose gate names at least one still-active item is not listed
- `release_planning_prompt.md` §1.3a names the new list, with the version bump, `OPERATIONAL_GUIDE.md` §14 and `prompt_change_log.md` updates in the same commit

### ST-41 — Script the execution_state.json read-back check from execution_prompt.md §9.2
**Source:** BLG-GOV-363
**Priority:** P3
**Effort:** S (~0.5d)
**Sequencing:** After ST-40 (sequential governance bumps).
**UI-facing:** No
**Acceptance Criteria:**
- `scripts/check_execution_state_consistency.py` passes on a consistent file and fails, naming the field, for each of the 4 equality breaks
- Unit tests cover each failure mode
- `execution_prompt.md` §9.2 references the script, with the CLAUDE.md §6 checklist in the same commit *(restated: Scope's prompt reference made testable)*

### ST-42 — Name one Skill-Silo aggregation method in roadmap_prompt.md §7.1
**Source:** BLG-GOV-367
**Priority:** P3
**Effort:** S (~0.5d)
**Sequencing:** After ST-41 (sequential governance bumps).
**UI-facing:** No
**Acceptance Criteria:**
- §7.1 names one aggregation method unambiguously, with the CLAUDE.md §6 checklist in the same commit
- The last 4 readings are restated under that method, or a method-break note is recorded in `roadmap_prompt.md` §7.1 for the next rebalance to honour *(restated: the note's home is named; `claude/roadmap/decision_log.md` is reserved for rebalance decisions and is outside the sprint's write scope)*
- `scripts/compute_rebalance_diagnostics.py`'s output (or a flag) matches the chosen method

### ST-43 — Rule on reduced-roster idea-intake windows, and cap them if permitted
**Source:** BLG-GOV-364
**Priority:** P3
**Effort:** S (~0.5d)
**Delegation note:** A Head of Specs Team + Product Owner ruling (`delegated_decision`).
**Sequencing:** After ST-42 (sequential governance bumps).
**UI-facing:** No
**Acceptance Criteria:**
- A recorded ruling; any adopted change to `idea_intake_prompt.md` (or `roadmap_prompt.md` STEP -1.6) ships with the full CLAUDE.md §6 checklist

### ST-44 — Add a split-credit secondary tally to compute_role_share_history.py
**Source:** BLG-GOV-372
**Priority:** P3
**Effort:** S (~0.5 day)
**Delegation note:** Writes `claude/roadmap/role_share_history.md`. Classified `delegated_decision` under the named-file rule (`ESC-CLOSE-20261006-01`), RISK-06.
**Sequencing:** After ST-45 (extends its tests).
**UI-facing:** No
**Acceptance Criteria:**
- The script emits both tallies (raw primary, split-credit secondary); tests cover compound Owner strings, extending ST-45's test file
- `claude/roadmap/role_share_history.md` gains a split-credit column

### ST-45 — Add unit tests for compute_role_share_history.py and a STEP 7.1 pin
**Source:** BLG-QA-212
**Priority:** P3
**Effort:** S (~0.5 day)
**Sequencing:** Before ST-44.
**UI-facing:** No
**Acceptance Criteria:**
- The new test file passes in CI Phase B and covers compound owners, a missing Owner line and the v9.8 regression pin (39 stories, Head of Specs Team 12)
- The script's total equals the number of ST headings, or it reports the difference
- The STEP 7.1 real-changelog figure (v9.6–v9.8 → 84/99 = 84.8%) is pinned in a test

### ST-46 — Scope utils.* test stubs so a reordered run passes
**Source:** BLG-QA-209
**Priority:** P3
**Effort:** M (~1d; 11 test files reference `sys.modules["utils…"]`, grep-confirmed 2026-10-12)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- `pytest $(ls tests/test_*.py | sort -r)` passes with no failures, matching the default order
- The guard fails a file that leaves a `utils.*` stub installed

### ST-47 — Guard the positions.fees_paid NOT NULL invariant in the entry flow and SQL seeds
**Source:** BLG-QA-213
**Priority:** P3
**Effort:** S (~0.5d)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- Both unit tests fail if `'fees_paid'` is removed from `position_data` in `position_service.py`, or if its value is `None`, for either market
- The static test fails on a fixture or temporary copy of a seed insert that omits `fees_paid`, and passes on the current repo
- Runs under the stub `DATABASE_URL` convention, with no live DB access

### ST-48 — Remove the leaked sandbox /tmp path from backend/setup.cfg
**Source:** BLG-QA-202
**Priority:** P3
**Effort:** XS (<1h)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- `backend/setup.cfg` contains no sandbox-specific `/tmp` path
