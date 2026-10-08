Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-10-08
Cycle: 2026-10-08__release-v9.11
Release: v9.11

# Backlog Slice — v9.11

<!-- release-plan-marker: RP:v9.11:2026-10-08__release-v9.11 -->

43 stories across 6 EPICs, 27.975 estimated days. The acceptance criteria below are the source of truth for Sprint Planning and Execution. Scope is sized to the top of the confirmed ~24–28 day capacity band, per the explicit user instruction "use full capacity" (2026-10-08).

**Ready pool:** 97 items, 61.67 days.

**Selection method** (`release_planning_prompt.md` §1.4c):
1. The 2 ready P1 items.
2. All 9 seatable P2 items (`BLG-TECH-21` deferred by override, as at v9.10).
3. A category-balanced, oldest-first round-robin over P3/P4, run until 0.025 days were left.

All four roadmap-committed items (`BLG-BE-152`, `BLG-BE-150`, `BLG-FE-206`, `BLG-BE-154`; roadmap rebalance `2026-10-08__scheduled`, DL-084) seat mechanically in the P1/P2 passes.

**Where an item's own AC is stale or depends on another story, the AC below restates it.** Any change from the source backlog item is marked *(restated)* with the reason.

---

## EPIC-01 — Post-Trade Debrief & AI Reliability

**Maps to:** S2-01 – S2-09
**Owner:** Backend Engineering Patterns Owner; AI Compliance & Governance Officer; QA & Testing Owner
**Description:** Fix the debrief's missing derived figures (P1 fast-track), verify every AI feature after the PR #1921 import fix, stop the sampling hook from breaking or hiding AI errors, and close the AI audit-logging and prompt gaps.
**Estimated days:** 6.75

### ST-01 — Give the post-trade debrief R achieved, the stop at exit and entry slippage
**Source:** BLG-BE-152
**Priority:** P1
**Effort:** M (~1–2d; 1.5d midpoint)
**Delegation note:** AI Compliance & Governance Officer sign-off on the Condition 2 interpretation (RISK-01) is the first sub-step.
**Sequencing:** First in EPIC-01. P1 Correctness Fast-Track (DL-084).
**UI-facing:** Yes
**Acceptance Criteria:**
- For the three 2026-10-07 production examples (+2.24R vs 2.2R target; 0.86R vs 2.2R; the profitable "Stop Loss Hit" regenerate), the summary states R achieved vs target and the stop at exit, and correctly describes a profitable stop-out as a trailing stop
- A focus area that cites R achieved (e.g. "2.24R") passes the numeric check. A number not derived from source data still fails
- A test shows that a profitable "Stop Loss Hit" trade's prompt includes the trailing stop at exit, so the model has the context to avoid calling it a contradiction
- AI Compliance & Governance Officer sign-off on the Condition 2 interpretation is recorded; `PROMPT_VERSION` is bumped

### ST-02 — Verify all six AI features after the PR #1921 import fix, and file the escaped-defect note
**Source:** BLG-BE-150
**Priority:** P1
**Effort:** S (~0.5d)
**Delegation note:** Running the AI features on staging needs a staging deploy with a working Anthropic key and a person to exercise the UI. Expected Human-Delegation to the Infrastructure & Operations Owner (RISK-02).
**Sequencing:** Before ST-03 and ST-04 close, so the note can cite them.
**UI-facing:** No
**Acceptance Criteria:**
- A dated staging run shows all six AI features (post-trade debrief, journal summary, daily briefing, chat, generate-plan, generate-thesis) returning generated content, not an error or the generic "unavailable" message. The debrief was already verified in production on 2026-10-07 and may cite that record
- At least one sampled output is recorded after opting in, or the sampling path is confirmed working by another recorded check
- The escaped-defect note is filed, explains why ST-23 (v9.4)'s QA evidence and DoQ sign-off missed a production-only import failure, and names the follow-ups (ST-03, ST-04, `BLG-QA-218`) *(restated: follow-up IDs mapped to this release's stories)*

### ST-03 — Keep the AI-output sampling hook from breaking or hiding errors in AI responses
**Source:** BLG-BE-151
**Priority:** P2
**Effort:** S (~0.5d)
**Sequencing:** Pairs with ST-04 (the import test keeps import errors loud in CI).
**UI-facing:** No
**Acceptance Criteria:**
- A test shows that a failure inside the sampling hook, including at import, leaves each AI endpoint's response unchanged
- Daily briefing and chat log the exception (with `exc_info`) when they return their fallback message

### ST-04 — Test that every backend module imports with only backend/ on the path
**Source:** BLG-QA-217
**Priority:** P2
**Effort:** S (~0.5d)
**Sequencing:** After ST-03.
**UI-facing:** No
**Acceptance Criteria:**
- Reintroducing the `ai_output_sampling_service` bare import makes the new test fail
- The test passes on `main` and runs in CI Phase A

### ST-05 — Make the debrief Regenerate button recognisable, and show failures and the generated time
**Source:** BLG-FE-205
**Priority:** P2
**Effort:** S (~0.5d)
**Sequencing:** After ST-01 (same component's content changes).
**UI-facing:** Yes
**Acceptance Criteria:**
- Playwright: Regenerate has a visible border/background in both themes, and the axe scan of the debrief section reports no colour-contrast violations
- Playwright: a mocked 500 on POST shows an error message and keeps the existing debrief
- Playwright: after a successful regenerate, the generated timestamp updates

### ST-06 — claude_audit_log: add prompt_hash and response_length, and log failed model calls
**Source:** BLG-AI-08
**Priority:** P2
**Effort:** S (~1 day plus a live migration; calibrated to 1.5d)
**Delegation note:** Live migration on staging and production needs DB write access. Expected Human-Delegation to the Data Model & Domain Schema Owner with the Infrastructure & Operations Owner (RISK-03), as for DS-17 (`ESC-EXEC-20260921-04`).
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- Successful briefing and chat calls write `prompt_hash` and `response_length`. Unit tests cover both endpoints
- A failed model call writes an audit row marked as failed
- Migration recorded in `data_model.md` and applied live, with verification output; `claude_api_log_hygiene_policy.md` amended to match

### ST-07 — State in the daily-briefing system prompt that output is advisory and cannot execute trades
**Source:** BLG-AI-09
**Priority:** P3
**Effort:** XS (<0.5 day plus golden-fixture update)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- The briefing system prompt states advisory-only and no execution, frames action items as recommendations, and the golden-fixture tests pass with a recorded `prompt_version` bump
- Self-audit checklist A1 passes for both the chat and briefing prompts

### ST-08 — AI briefing and chat state when a quoted stop was last recalculated
**Source:** BLG-BE-141
**Priority:** P3
**Effort:** S (~0.5-1 day)
**Sequencing:** After ST-07 (same prompt module; one `prompt_version` bump each).
**UI-facing:** No
**Acceptance Criteria:**
- Briefing and chat responses that mention a stop include its recalculation time (`stop_calculated_at`), shown by a fixture test

### ST-09 — Pin every Claude model ID in one backend module
**Source:** BLG-BE-142
**Priority:** P3
**Effort:** S (~0.5 day; 4 files named)
**Sequencing:** After ST-01, ST-07, ST-08 (they touch the same call sites).
**UI-facing:** No
**Acceptance Criteria:**
- No `claude-` model literal outside the new module, and no unpinned alias in production code; a test fails if one is reintroduced

---

## EPIC-02 — Risk & Position Display Correctness (build-and-ship)

**Maps to:** S2-10 – S2-15
**Owner:** Head of Engineering; Head of UX & Design; Frontend Specifications & UX Documentation Owner
**Description:** Make the Risk Dashboard and Positions page show what the system actually does: no fabricated prices, correct currency, true stop distance, grace stops shown as not enforced, and grace counts in calendar days.
**Estimated days:** 4.775

### ST-10 — Remove the hard-coded ×1.38 US price fallback from GET /portfolio, and flag stale prices
**Source:** BLG-BE-154
**Priority:** P2
**Effort:** M (~1-1.5 days)
**Sequencing:** First in EPIC-02: it adds a `GET /portfolio` field that ST-13 also extends (RISK-04).
**UI-facing:** Yes
**Acceptance Criteria:**
- Unit test: with the live fetch mocked to fail, a US position's `current_price` equals its stored native price converted at the live FX rate, never `stored × 1.38`, and `price_is_stale` is `true`
- `grep -n "1.38" backend/services/portfolio_service.py` returns nothing
- Playwright: a stale position shows the stale marker on the Risk Dashboard and Dashboard
- `portfolio_endpoints.md` and `docs/reference/openapi.yaml` document `price_is_stale` in the same commit

### ST-11 — Position Risk table: GBP entry prices, and grace-period stops shown as not enforced
**Source:** BLG-FE-206
**Priority:** P2
**Effort:** S (~0.75-1 day)
**Sequencing:** After ST-10 (same table).
**UI-facing:** Yes
**Acceptance Criteria:**
- Playwright: a US row's Entry Price renders with "£" and the GBP value returned by `GET /portfolio`
- Playwright: a GRACE row shows "Not enforced (grace)" in Stop Price and Stop Dist %, with no rose/amber distance colour
- `risk_dashboard.md` §6 documents both behaviours

### ST-12 — GET /portfolio computes holding_days live from entry_date
**Source:** BLG-BE-153
**Priority:** P2
**Effort:** S (~1 day; 3 other readers named)
**Sequencing:** After ST-10 (same service function).
**UI-facing:** Yes
**Acceptance Criteria:**
- Unit test: a position whose stored `holding_days` is 9 but whose `entry_date` is 10 calendar days ago returns post-grace `display_status` and `grace_period: false` from `GET /portfolio`
- The other stored-`holding_days` readers (`alerts_service.py`, `compliance_service.py`, `ai_service.py`) are fixed, or each is filed as a new backlog item with its reason *(restated: "listed in this item" becomes new items, so no existing backlog item is edited)*

### ST-13 — Stop Dist % computed in native currency for US positions
**Source:** BLG-BE-155
**Priority:** P2
**Effort:** S (~1 day)
**Sequencing:** After ST-10 and ST-11 (same endpoint and table).
**UI-facing:** Yes
**Acceptance Criteria:**
- Unit test: US position, native price 100, native stop 92, entry FX 1.27, live FX 1.35 → `stop_distance_pct` = 8.0
- Playwright: the table shows the API's `stop_distance_pct`
- `risk_dashboard.md` §6, `portfolio_endpoints.md` and `openapi.yaml` updated together

### ST-14 — Grace alert filter and "Day N of 10" label use calendar days since entry
**Source:** BLG-BE-147
**Priority:** P2
**Effort:** S (~0.5 day)
**Sequencing:** Independent of ST-10–ST-13 (Positions page, not Risk).
**UI-facing:** Yes
**Acceptance Criteria:**
- A day-8 position whose `state_entered_at` is today still appears in the alert list, labelled "Day 9 of 10" with 2 days left (unit test + Playwright)
- No grace reading on the Positions page uses `days_in_state`; `grace_period_alert_endpoint.md` and `positions.md` §Grace Period Alert Zone updated

### ST-15 — Recent Trades glyph treats a P&L that rounds to £0.00 as break-even
**Source:** BLG-FE-204
**Priority:** P3
**Effort:** XS (<1h)
**Sequencing:** Independent.
**UI-facing:** Yes
**Acceptance Criteria:**
- A trade with `pnl: 0.004` renders the neutral glyph and colour; `pnl: 0.01` still renders the up arrow (`recent-trades-zero-pnl-badge.spec.js`, Playwright)

---

## EPIC-03 — Strategy, Records & Alert Integrity

**Maps to:** S2-16 – S2-22
**Owner:** Head of Engineering; Strategy Rules & System Intent Owner; Infrastructure & Operations Owner
**Description:** Settle in-grace stop recalculation, record the parameters behind each closed trade, monitor post-deploy stop health, stop page views from writing stops, and harden alert de-duplication.
**Estimated days:** 4.55

### ST-16 — Rule on and test stop recalculation during grace
**Source:** BLG-BE-143
**Priority:** P3
**Effort:** S (~0.5-1 day)
**Delegation note:** Strategy Rules & System Intent Owner ruling first (`delegated_decision`, RISK-05).
**Sequencing:** First in EPIC-03.
**UI-facing:** No
**Acceptance Criteria:**
- The ruling on intended in-grace behaviour is recorded. The on-load and nightly paths behave the same during grace, and a test asserts it
- Traceability row C6.3-02 is moved to Asserted with that test

### ST-17 — Snapshot the strategy parameters in force onto each closed trade
**Source:** BLG-FR-06
**Priority:** P3
**Effort:** S (~1 day)
**Delegation note:** If new `trade_history` columns are needed, the live migration follows RISK-03's Human-Delegation path.
**Sequencing:** After ST-16 (the grace ruling may affect the recorded source).
**UI-facing:** No
**Acceptance Criteria:**
- New closed trades carry the active multiplier, ATR, grace length and parameter source (test)
- Any new columns are documented in `data_model.md` and applied live with verification output *(restated: added because the four fields need a home; the source AC did not say where)*

### ST-18 — Post-deploy synthetic check for post-grace stops and §11 multipliers
**Source:** BLG-OPS-179
**Priority:** P3
**Effort:** S (~0.5-1 day)
**Sequencing:** Gate met: `BLG-BE-138` shipped in v9.10 (ruling (a), fixed §11 values).
**UI-facing:** No
**Acceptance Criteria:**
- The monitor fails on a fixture with a non-§11 multiplier or a missing post-grace stop, and alerts through the existing Telegram path

### ST-19 — Read-only market-regime source, so viewing regime no longer runs the stop-writing analyze call
**Source:** BLG-BE-140
**Priority:** P3
**Effort:** S (~1-1.5 days; new endpoint)
**Delegation note:** New endpoint: CLAUDE.md §2 registration steps apply (RISK-05).
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- Rendering market regime makes no call to `/positions/analyze`
- The new endpoint has a `##` contract heading, an `openapi.yaml` entry, a `routers/test.py` entry, and updated `SystemStatus.js` fallback count and `SC-SS-01b`, all in the same commit

### ST-20 — DB-level unique constraint for active price alerts
**Source:** BLG-OPS-175
**Priority:** P4
**Effort:** XS (<1h; calibrated to S 0.5d for the live migration)
**Delegation note:** Live migration — RISK-03 Human-Delegation path.
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- A genuinely concurrent double-submit is rejected or absorbed at the DB layer, not just the application layer
- `data_model.md`'s `price_alerts` section documents the new constraint, applied live with verification output

### ST-21 — Make the anomaly-check fingerprint-clear path respect send_alert, or document why not
**Source:** BLG-OPS-176
**Priority:** P4
**Effort:** XS (<1h)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- Either the clear path is gated on `send_alert` to match the send path, or a comment explains why it deliberately is not
- A test asserts the chosen behaviour explicitly

### ST-22 — Guard POST /trade-plans against a double-submitted duplicate plan
**Source:** BLG-API-06
**Priority:** P4
**Effort:** XS (<1h)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- A disposition is recorded (client-side submit guard added, or accepted risk with rationale) for the double-submit duplicate-plan case

---

## EPIC-04 — AI Narrative & Engagement Measurement (build-and-ship)

**Maps to:** S2-23 – S2-28
**Owner:** Financial Reporting & Records Owner; Metrics Definitions & Analytics Owner; Head of UX & Design
**Description:** Ship the AI-assisted monthly P&L narrative with its cost estimate and usage counter, and define the engagement measures and review trigger that will show whether new AI features raise usage.
**Estimated days:** 4.9

### ST-23 — Cost estimate for the AI monthly P&L narrative
**Source:** BLG-FEAT-63
**Priority:** P3
**Effort:** S (~0.5 day)
**Sequencing:** First in EPIC-04: feeds ST-25.
**UI-facing:** No
**Acceptance Criteria:**
- A cost estimate for the AI-generated P&L narrative is produced before ST-25 is built *(restated: the source AC waited on a gate the Product Owner removed on 2026-10-05)*

### ST-24 — Define the AI chat engagement metric set
**Source:** BLG-FEAT-60
**Priority:** P3
**Effort:** S (~0.5–1 day)
**Sequencing:** Before ST-25, so the new feature's effect can be measured against the 2026-10-05 review baseline (`BLG-GOV-366`'s recommendation).
**UI-facing:** No
**Acceptance Criteria:**
- Engagement metric set (sessions/week, questions/session, response-acceptance rate) defined and documented in `metrics_definitions.md`
- Gate: satisfied — removed by Product Owner decision 2026-10-05; no action *(restated)*

### ST-25 — AI-assisted monthly P&L narrative
**Source:** BLG-FEAT-59
**Priority:** P3
**Effort:** M (~1–2 days)
**Delegation note:** §13 boundary confirmation by the Strategy Rules & System Intent Owner before build (RISK-06, Pre-sprint Required Decision).
**Sequencing:** After ST-23 and ST-24.
**UI-facing:** Yes
**Acceptance Criteria:**
- The narrative section renders on Monthly P&L as optional and dismissible (Playwright)
- Output is framed advisory-only, consistent with §13 SRB-v1.7, and the Strategy Rules & System Intent Owner's §13 confirmation cites every §13 clause naming AI output or financial reporting *(restated: from the item's Scope bullet 2, made testable)*
- Gate: satisfied — removed by Product Owner decision 2026-10-05; no action *(restated)*

### ST-26 — Usage counter for the AI monthly P&L narrative
**Source:** BLG-SPEC-174
**Priority:** P3
**Effort:** S (~1d)
**Sequencing:** After ST-25.
**UI-facing:** No
**Acceptance Criteria:**
- A real, queryable count of AI-assisted monthly P&L narrative generations exists and is documented in `data_model.md`
- The 2027-01-03 AI feature usage review (tracked by ST-28) names this count as its evidence source *(restated: `BLG-FEAT-59`'s gate, which the source AC would have edited, was removed on 2026-10-05)*

### ST-27 — AI chat UI interaction study protocol
**Source:** BLG-FE-84
**Priority:** P3
**Effort:** S (~1 day)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- Interaction study protocol document produced (5 questions targeting chat advisor usage)
- Gate: satisfied — removed by Product Owner decision 2026-10-05; no action *(restated)*

### ST-28 — Track the 2027-01-03 AI feature usage review
**Source:** BLG-GOV-366
**Priority:** P3
**Effort:** XS (<1h)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- `python3 scripts/scan_backlog_gate_conditions.py --as-of 2027-01-04` reports the 2027-01-03 AI usage review (a new gated backlog item) as lapsed, and it matches post-ship STEP 12.6's keyword filter
- The sequencing note (engagement metric before the first new AI feature) is recorded in this slice (ST-24 before ST-25) and in `sprint_backlog.md` *(restated: no edit to the existing `BLG-FEAT-60` item)*

---

## EPIC-05 — Spec & Contract Hygiene

**Maps to:** S2-29 – S2-32
**Owner:** API Contracts & Documentation Owner; Data Model & Domain Schema Owner; Frontend Specifications & UX Documentation Owner
**Description:** Reconcile four spec/contract divergences: the restatement marker, column provenance, the TradePlan status enum and non-canonical error examples.
**Estimated days:** 1.8

### ST-29 — Reconcile the Monthly Restatement Marker spec with GET /reports/monthly-pnl
**Source:** BLG-SPEC-170
**Priority:** P4
**Effort:** S (~0.5d)
**Sequencing:** Aged 2+ cycles (§1.1 advisory).
**UI-facing:** No
**Acceptance Criteria:**
- `reports.md` and `reports_endpoints.md` agree on whether the detail row is dated and on how the unavailable state is signalled
- The shipped UI matches the reconciled spec, or a follow-up is filed for the difference
- DEV-v9.7-ST04-01 is marked resolved with this item's ID

### ST-30 — Column provenance annotations in data_model.md
**Source:** BLG-SPEC-173
**Priority:** P3
**Effort:** S (~1d)
**Sequencing:** After ST-06/ST-17/ST-20 add their columns, so new columns are annotated too.
**UI-facing:** No
**Acceptance Criteria:**
- `positions` and `trade_plans` in `data_model.md` carry a provenance annotation (user-entered / derived / system-stamped) per field
- No field is left ambiguous between user-entered and derived without an explicit note

### ST-31 — Correct the TradePlan status enum in openapi.yaml
**Source:** BLG-SPEC-177
**Priority:** P3
**Effort:** XS (<1h)
**Sequencing:** Coordinate `openapi.yaml` edits with ST-10/ST-13/ST-19 (RISK-04).
**UI-facing:** No
**Acceptance Criteria:**
- `TradePlan.status` enum matches `data_model.md` DS-04's live CHECK constraint exactly (7 values)
- `scripts/check_openapi_drift.py` and `scripts/check_contract_example_freshness.py` both still pass

### ST-32 — Fix the 5 error-response examples that diverge from the canonical envelope
**Source:** BLG-SPEC-175
**Priority:** P4
**Effort:** XS (<1h)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- All 5 flagged cases are resolved (code fixed, documentation corrected, or heading label corrected)
- `python3 scripts/check_contract_example_freshness.py` reports 0 error-envelope violations

---

## EPIC-06 — Governance, QA & Ops Hygiene

**Maps to:** S2-33 – S2-43
**Owner:** Head of Specs Team; QA & Testing Owner; Infrastructure & Operations Owner; Director of Quality
**Description:** Canonical Owner-name check, effort-weighted PVR home, §13 AC citation rule and DoQ strategy-values line; tighten five test-quality gaps; make the non-registry dependency check required and move test-only packages out of the production build.
**Estimated days:** 5.2

### ST-33 — Write-time check that sprint_backlog.md Owner values use canonical role names
**Source:** BLG-GOV-375
**Priority:** P3
**Effort:** S (~0.5-1 day)
**Delegation note:** Edits `idea_intake_prompt.md`: CLAUDE.md §6 checklist and §8 step 2a version-collision check (RISK-07).
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- A non-canonical Owner value fails the check; all v9.9 and v9.10 Owner values pass
- `idea_intake_prompt.md` role list matches the agent files (`Metrics Definitions & Analytics Owner`)

### ST-34 — Give the effort-weighted PVR column its home in product_value_ratio_history.md
**Source:** BLG-GOV-355
**Priority:** P3
**Effort:** S (~0.5-1d)
**Delegation note:** Named-file rule (`ESC-CLOSE-20261006-01`): the AC names `claude/roadmap/product_value_ratio_history.md`, so the story is `delegated_decision` with RISK-07. The `roadmap_prompt.md` STEP 2.4 change needs `BLG-GOV-339`'s Head of Specs Team + Product Owner sign-off.
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- `claude/roadmap/product_value_ratio_history.md`'s `## History` table carries the effort-weighted PVR alongside the story-count PVR, backfilled for the 5 windows already computed in `metrics_definitions.md` Appendix F
- `roadmap_prompt.md` STEP 2.4 appends both readings at future rebalances, once `BLG-GOV-339`'s sign-off is recorded (CLAUDE.md §6 checklist applies)

### ST-35 — §13 sign-off ACs must cite every §13 clause that names the feature's subject
**Source:** BLG-GOV-359
**Priority:** P3
**Effort:** S (~0.5–1 day)
**Delegation note:** Governance prompt edit: CLAUDE.md §6 checklist (RISK-07).
**Sequencing:** Before ST-25's §13 confirmation if possible (it is the first feature that would use the rule).
**UI-facing:** No
**Acceptance Criteria:**
- The governing prompt requires §13 ACs to cite each §13 clause that names the feature's subject, with a worked example referencing the gap-risk case
- CLAUDE.md §6 checklist complete (version bump, OPERATIONAL_GUIDE §14 + phase header, prompt_change_log row)

### ST-36 — DoQ sign-off line for stories touching stop, grace, ATR or exit logic
**Source:** BLG-GOV-370
**Priority:** P3
**Effort:** XS (~0.25 day)
**Sequencing:** Early in the sprint, so EPIC-02/EPIC-03 stories can use it.
**UI-facing:** No
**Acceptance Criteria:**
- The QA evidence template has a conditional DoQ line (values and formulas checked against `strategy_rules.md` §5–§11, sections cited)
- The first qualifying story signed off after the template change completes the line

### ST-37 — Extend the axe accessibility scan to the Replay page
**Source:** BLG-QA-196
**Priority:** P3
**Effort:** XS (<0.5d)
**Sequencing:** `BLG-QA-195` (its dependency) shipped in v9.10.
**UI-facing:** No
**Acceptance Criteria:**
- The axe scan covers the Replay page (both selector modes, populated result) in dark and light themes
- Any serious/critical finding is fixed or has its own filed item

### ST-38 — Fix SC-REP-04a's signed "+£0.00" expectation
**Source:** BLG-QA-197
**Priority:** P3
**Effort:** XS (<1h)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- SC-REP-04a passes and asserts the unsigned "£0.00" zero convention

### ST-39 — Mutation-test the US-market and batch-sizing paths
**Source:** BLG-QA-199
**Priority:** P3
**Effort:** S (~0.5–1d)
**Sequencing:** After ST-41 (same pilot test file).
**UI-facing:** No
**Acceptance Criteria:**
- `size_position`'s US-market path and `size_batch_inv_vol` each have at least one mutation-testing case in the pilot's test file
- The updated mutation score is recorded in `docs/testing/mutation_testing_pilot_sizing_and_stop_ratchet.md`

### ST-40 — Make the ceiling/count regression tests read the source they claim to verify
**Source:** BLG-QA-200
**Priority:** P3
**Effort:** S (~0.5d)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- Each "ceiling" test fails if the actual source value regresses over 500ms, shown by a scratch-branch edit, without relying on the sibling string-match test
- No test in either file asserts purely on hardcoded literals unrelated to the source file's content

### ST-41 — Reset the pilot test file's shared database mocks between tests
**Source:** BLG-QA-201
**Priority:** P3
**Effort:** XS (<1h)
**Sequencing:** Before ST-39.
**UI-facing:** No
**Acceptance Criteria:**
- Each test in `TestSizePositionGoldenVectors` is independently runnable in isolation and in any order with identical results
- A test added without configuring all three database mocks fails loudly

### ST-42 — Make the Non-Registry Dependency Check a required status check on main
**Source:** BLG-OPS-177
**Priority:** P3
**Effort:** XS (<1h)
**Delegation note:** Branch protection needs repository admin access. Expected Human-Delegation to the Infrastructure & Operations Owner (RISK-08).
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- `gh api repos/sachiv1984/swing-trading-model/branches/main` lists the check under `protection.required_status_checks`
- A PR that does not touch dependency files is not left blocked waiting on the check

### ST-43 — Move test-only Python packages out of the production build
**Source:** BLG-OPS-178
**Priority:** P4
**Effort:** S (~0.5d)
**Sequencing:** Independent.
**UI-facing:** No
**Acceptance Criteria:**
- The production build installs no test-only package
- All CI test workflows still pass

---
