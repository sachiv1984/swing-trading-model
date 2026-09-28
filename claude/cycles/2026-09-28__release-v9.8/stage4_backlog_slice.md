Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-28
Cycle: 2026-09-28__release-v9.8
Release: v9.8

# Backlog Slice — v9.8

<!-- release-plan-marker: RP:v9.8:2026-09-28__release-v9.8 -->

39 stories across 6 grouped EPICs, 28.00 estimated days. Full acceptance criteria below (source of truth for Sprint Planning and Execution). Scope set to the top of the confirmed ~24-28 day/sprint capacity band per explicit user "full capacity" instruction (2026-09-28). Ready pool: 65 items / 46.7 days (after excluding 2 substantively gate-blocked items with no formal Gate field — `BLG-FEAT-73`/`76`). Selection method: 0 ready P1 items; all 3 ready P2 items seated first per §1.4c, then category-balanced round-robin oldest-first for remaining P3/P4 — per `release_planning_prompt.md` §1.4c. EPIC-01 leads the table per the Skill-Silo rotation guideline (most execution-heavy category with genuine ready scope; no build-and-ship U-item exists this cycle — see `run_manifest.md`). EPIC-01 items `BLG-FE-184`/`BLG-FE-185`/`BLG-FE-190`/`BLG-FE-191` carry an observable UI acceptance criterion — `design_gate_required: true`.

---

## EPIC-01 — Frontend & UX Debt Clearance

**Maps to:** S2-01, S2-02, S2-03, S2-04, S2-05, S2-06
**Owner:** Head of UX & Design; Frontend Specifications & UX Documentation Owner

### ST-01 — Migrate the remaining toFixed / toLocaleString call sites to the shared formatting helper
**Source:** BLG-FE-184
**Priority:** P3
**Effort:** L (~3-5d)
**Acceptance Criteria:**
- 0 unmigrated money/percentage/R formatting call sites outside `src/lib/format.js` (or an explicit, reasoned allow-list)
- Zero P&L renders unsigned in the neutral tone wherever P&L is coloured
- Playwright test covering the observable AC passes in CI (CLAUDE.md §2 frontend-visible-change rule)

### ST-02 — Drive Screener and Watchlist table body cells from the shared column definitions
**Source:** BLG-FE-185
**Priority:** P4
**Effort:** M (~1-2d)
**Acceptance Criteria:**
- Header, cell and CSV value for every data column come from one definition
- Existing Screener/Watchlist Playwright specs pass unchanged
- Playwright test covering the observable AC passes in CI (CLAUDE.md §2 frontend-visible-change rule)

### ST-03 — Make the Tax Year restated-months notice link to months the Monthly tab actually shows
**Source:** BLG-FE-190
**Priority:** P4
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- A restated-months notice never directs the user to a view that cannot show the months it counts
- Playwright covers the older-tax-year case
- Playwright test covering the observable AC passes in CI (CLAUDE.md §2 frontend-visible-change rule)

### ST-04 — SystemStatus.js categorizeEndpoint() has no case for the new /replay prefix
**Source:** BLG-FE-191
**Priority:** P4
**Effort:** XS (<1h)
**Acceptance Criteria:**
- `POST /replay/run` is categorized under a meaningful label (not `'Other'`) on the System Status dashboard
- No other endpoint's categorization changes
- Playwright test covering the observable AC passes in CI (CLAUDE.md §2 frontend-visible-change rule)

### ST-05 — Responsive-table behaviour spec for Positions, TradeHistory and TradePlans
**Source:** BLG-SPEC-158
**Priority:** P3
**Effort:** S (~0.5–1d)
**Acceptance Criteria:**
- Three tables have stated behaviour in the frontend specs

### ST-06 — Canonical keyboard-shortcut inventory spec
**Source:** BLG-SPEC-159
**Priority:** P4
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- One inventory; conflicts resolved or filed

---

## EPIC-02 — Backend Reliability & Financial Correctness

**Maps to:** S2-07, S2-08
**Owner:** Head of Engineering; Financial Reporting & Records Owner

### ST-07 — Remaining ad hoc `timeout=`/retry call sites not yet on the shared upstream-call helper
**Source:** BLG-BE-128
**Priority:** P3
**Effort:** S (~1d)
**Acceptance Criteria:**
- Every call site listed above is either migrated to `utils.upstream_call` or has an explicit, documented reason it is not (e.g. Stooq/Twelve Data's rate-limit-interaction risk, or ticker_universe.py's different mechanism)
- No behaviour change to any already-working fallback/rate-limit logic (Stooq/Twelve Data cooldown timers, `_TWELVE_DATA_RATE_LIMIT`) as a side effect of any migration performed

### ST-08 — Extend the v9.7 float→Decimal fee-rounding audit to tax-year statement calculations
**Source:** BLG-BE-130
**Priority:** P3
**Effort:** S (~1d)
**Acceptance Criteria:**
- Tax-year statement and carried-forward-loss calculations are confirmed Decimal-consistent at rounding boundaries, or a specific gap is filed with the same rigor as `BLG-BE-127`

---

## EPIC-03 — QA & Test Coverage

**Maps to:** S2-09, S2-10, S2-11, S2-12, S2-13, S2-14, S2-15, S2-16
**Owner:** Director of Quality

### ST-09 — Golden-fixture CI regression for AI prompt templates — boundary-language drift caught at template-change time
**Source:** BLG-AI-07
**Priority:** P3
**Effort:** S (~0.5–1d)
**Acceptance Criteria:**
- CI fails when a disallowed phrase is introduced into any covered template
- CI fails when template text changes without a `prompt_version` change
- The suite runs without `ANTHROPIC_API_KEY`

*Note: `IDEA-ai-compliance-20260919-02` (stamp model/prompt version on audit rows) was rejected as already implemented; its residual value — asserting the version actually moves — is folded into this item's third scope bullet.*

### ST-10 — No end-to-end test confirms backend/main.py's wired root logger actually emits JSON in situ
**Source:** BLG-QA-179
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- A new test fails if `backend/main.py`'s root handler formatter is reverted to plain text or replaced with a non-JSON formatter
- Test passes against the current implementation

### ST-11 — Add Playwright duration-assertion coverage for the 9 toast call sites fixed in ST-42 (Toast Notification Timing standard)
**Source:** BLG-QA-180
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- A regression test exists per call site (or a consolidated test covering all 9) that would fail if a future change silently reverted any site's `duration` back to a non-conforming value
- Tests pass against the current (ST-42) implementation

### ST-12 — Add regression coverage for the motion-timing values fixed in ST-41 (500ms ceiling components)
**Source:** BLG-QA-181
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- A regression test/check exists that would fail if any of the 4 components' `max(delay) + duration` were pushed back over 500ms by a future change
- Test/check passes against the current (ST-41) implementation

### ST-13 — Escaped-defect and follow-on-ratio tracking per cycle
**Source:** BLG-QA-182
**Priority:** P3
**Effort:** S (~0.5–1d)
**Acceptance Criteria:**
- Baseline computed for v9.5
- A per-cycle row is added at each post-ship closure

### ST-14 — DoQ checklist addendum for AI-touching stories
**Source:** BLG-QA-183
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- The addendum exists in the DoQ template
- The next AI-touching story uses it

### ST-15 — Mutation-testing pilot on the sizing calculator and stop ratchet
**Source:** BLG-QA-184
**Priority:** P3
**Effort:** M (~2d)
**Acceptance Criteria:**
- Baseline mutation score recorded for both modules
- Survivors triaged

### ST-16 — Enable Playwright trace and screenshot retain-on-failure
**Source:** BLG-QA-187
**Priority:** P4
**Effort:** XS (<1h)
**Acceptance Criteria:**
- A failing run's report includes a trace

---

## EPIC-04 — Operations & Security Hardening

**Maps to:** S2-17, S2-18, S2-19
**Owner:** Infrastructure & Operations Owner; Cybersecurity & Trust Lead

### ST-17 — No check that the staging backend actually redeployed after a merge that changes startup-applied schema (DS-19 sat unapplied on staging)
**Source:** BLG-OPS-169
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- A merge to `main` that should have redeployed staging but did not produces a visible failure or alert
- The check and its trigger are documented, including the known limits of what can be verified from the repo alone

### ST-18 — No documented allow-list of pre-approved read-only staging-DB query patterns for governed-session gate re-checks
**Source:** BLG-OPS-170
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- `docs/infrastructure/staging_setup.md` §8 states which query patterns a governed session may run against the staging read-only role without seeking additional confirmation each time

### ST-19 — Harden the non-registry dependency guard (missed specifier forms, trailing-comment false positive, no exit-code test)
**Source:** BLG-SEC-39
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Each missed form above is rejected by a test, and the trailing-comment line is accepted
- `main()` exits non-zero on a violation and zero on the current repo tree, asserted by a test

---

## EPIC-05 — Spec & API Contract Debt

**Maps to:** S2-20, S2-21, S2-22, S2-23, S2-24, S2-25, S2-26, S2-27, S2-28, S2-29
**Owner:** Head of Specs Team; Data Model & Domain Schema Owner

### ST-20 — Document idempotency and double-submit behaviour for every mutating endpoint
**Source:** BLG-API-04
**Priority:** P3
**Effort:** S (~0.5–1d)
**Acceptance Criteria:**
- Every `POST`/`PUT`/`PATCH`/`DELETE` heading in `docs/specs/api_contracts/` carries the subsection
- Undefined behaviours are listed and each has a filed backlog item
- Endpoint headings remain `## METHOD /path` (OpenAPI drift gate unaffected)

### ST-21 — Error-payload (4xx/5xx) examples for the 10 most-called endpoints, covered by the example-freshness checker
**Source:** BLG-API-05
**Priority:** P3
**Effort:** S (~0.5–1d)
**Acceptance Criteria:**
- 10 endpoints carry ≥1 error example
- The freshness checker fails when an error example diverges from the envelope

### ST-22 — Full field-level openapi.yaml authoring pass for 20 generic/thin `data` payload schemas
**Source:** BLG-SPEC-152
**Priority:** P3
**Effort:** M (~1–2 days)
**Acceptance Criteria:**
- All 20 endpoints from the triage doc's §5 have a case-by-case disposition recorded
- `scripts/check_contract_example_freshness.py`'s POSSIBLE DRIFT count reflects only genuinely-remaining intentional gaps, each carrying the standard description

### ST-23 — POST /trade-plans and DELETE /trade-plans/{id} declare no response schema in openapi.yaml
**Source:** BLG-SPEC-153
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Both endpoints have a real response schema in `openapi.yaml`
- `scripts/check_contract_example_freshness.py` no longer reports either as SKIPPED

### ST-24 — trade_plans CREATE TABLE / DS-04 CHECK constraint undocumented since ensure_trade_plans_extended_status() shipped
**Source:** BLG-SPEC-154
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- `data_model.md`'s `trade_plans` CHECK constraint and field notes match the live 7-value constraint
- A DS-xx entry exists documenting the migration, matching this doc's own established format

### ST-25 — openapi.yaml's OperationalHealthResponse.ai_journal doesn't model its either/or shape with oneOf
**Source:** BLG-SPEC-155
**Priority:** P4
**Effort:** XS (<1h)
**Acceptance Criteria:**
- `ai_journal`'s schema forbids a response carrying both the metric fields and `status: unavailable` simultaneously

### ST-26 — screener_results.md column list omits the Earnings column that the shipped table has
**Source:** BLG-SPEC-161
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- `screener_results.md` §4 and §5.3 name all ten columns in display order
- The §5.3 list matches `SCREENER_COLUMNS` in `src/pages/Screener.js`

### ST-27 — trade_reflection.md §4 specifies an en dash for a missing R-multiple; the convention is an em dash
**Source:** BLG-SPEC-162
**Priority:** P4
**Effort:** XS (<1h)
**Acceptance Criteria:**
- Spec and modal agree on the missing-value glyph
- The modal's R-multiple, P&L and price fields format via the shared helper

### ST-28 — sprint_velocity_trend_chart.md trend sentence splices non-adjacent PVR readings
**Source:** BLG-SPEC-163
**Priority:** P4
**Effort:** XS (<1h)
**Acceptance Criteria:**
- The trend-narrative sentence in §2 accurately reflects which readings it compares and their actual chronological relationship

### ST-29 — Reconcile the IT-06 §13 review (Alpaca sync recorded as GET-only, no orders placed) with a sync that POSTs orders and DELETEs positions
**Source:** BLG-SPEC-172
**Priority:** P2
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- The IT-06 §13 review and the shipped Alpaca sync agree on whether orders are placed, with the disposition recorded by the Strategy Rules & System Intent Owner

---

## EPIC-06 — Governance & Process Debt

**Maps to:** S2-30, S2-31, S2-32, S2-33, S2-34, S2-35, S2-36, S2-37, S2-38, S2-39
**Owner:** PMO Lead; Head of Specs Team

### ST-30 — Bake accessible-name and heading-order rules into the Base44 prompt template
**Source:** BLG-GOV-338
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- The template carries both rules
- A regenerated page in a test run introduces no new axe-core `KNOWN_VIOLATIONS` entries

### ST-31 — PVR / Skill-Silo measurement package — split debt into user-protective vs hygiene, add effort-weighted PVR, add a leading ungated-U-pool indicator
**Source:** BLG-GOV-339
**Priority:** P3
**Effort:** M (~1.5–2d)
**Acceptance Criteria:**
- Definitions documented in `metrics_definitions.md`
- History file carries both readings for the last 5 windows
- Leading indicator computed at the next rebalance

### ST-32 — Delivery-flow metrics — lead time by priority band and ready-pool runway forecast
**Source:** BLG-GOV-340
**Priority:** P3
**Effort:** S (~1d)
**Acceptance Criteria:**
- Both metrics defined and computed for the last 5 cycles
- The runway figure is cited in the next rebalance's STEP 7.3

### ST-33 — Persist STEP 7.2 role-share tallies as a structured history file
**Source:** BLG-GOV-341
**Priority:** P3
**Effort:** S (~0.5–1d)
**Acceptance Criteria:**
- History backfilled for the last 3 cycles
- STEP 7.2 reads the file instead of re-parsing Owner fields

### ST-34 — JSON Schema for `.claude_current_state.json`, including the `last_updated_utc` field the roadmap engine reads
**Source:** BLG-GOV-342
**Priority:** P3
**Effort:** S (~0.5–1d)
**Acceptance Criteria:**
- The state file validates
- The state-age advisory computes a real age instead of always firing

### ST-35 — Size "grep-and-fix-everywhere" and "verify against live environment" story classes a notch higher by default
**Source:** BLG-GOV-346
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- Either `sprint_planning_prompt.md` or `release_planning_prompt.md` gains a short check/note for this story class at estimate time
- Applied retrospectively: none required — this is a forward-looking calibration note, not a fix to the three already-disclosed instances above

### ST-36 — strategy_rules.md §13.5 roster missing PO-05 row after 2026-09-23 clearance
**Source:** BLG-GOV-348
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- PO-05 appears in the §13.5 roster table with the correct review-record link and clearance release

### ST-37 — governance_sync.yml does not auto-close a phased story's GitHub issue (ST-XXa/b/c vs. the commit tag's bare ST-XX)
**Source:** BLG-GOV-349
**Priority:** P2
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- A fully-done phased story's GitHub issue auto-closes on merge without manual intervention
- A partially-done phased story's issue is correctly NOT closed (no regression of the ST-19/BLG-GOV-314 fix this must coexist with)
- Regression test added

### ST-38 — No scheduled trigger/owner fires the 90-day post-ship AI feature usage review (BLG-GOV-74/140/141/142 cluster)
**Source:** BLG-GOV-351
**Priority:** P2
**Effort:** S (~1d)
**Acceptance Criteria:**
- A named routine/step fires this review automatically at the 90-day mark, without depending on a rebalance's incidental date-lapse scan to notice it
- The 8 downstream gated items above have a concrete path to resolution once the review runs

### ST-39 — PO-04 (Reflection ↔ Outcome Correlation) needs its own §13 boundary review, not just a stub-file note
**Source:** BLG-SPEC-156
**Priority:** P3
**Effort:** XS (~0.5 day)
**Acceptance Criteria:**
- A trackable item (this one, or a successor) exists for PO-04's own §13 review — not just prose in a stub file

---
