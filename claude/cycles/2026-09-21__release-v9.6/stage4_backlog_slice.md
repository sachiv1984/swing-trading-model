Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-09-21
Cycle: 2026-09-21__release-v9.6
Release: v9.6

# Backlog Slice — v9.6

<!-- release-plan-marker: RP:v9.6:2026-09-21__release-v9.6 -->

32 stories across 7 grouped EPICs, 28.00 estimated days. Full acceptance criteria below (source of truth for Sprint Planning and Execution). Scope set to the top of the confirmed ~24-28 day/sprint capacity band per explicit user "use full capacity" instruction (2026-09-21). Ready pool: 76 items / 61.75 days (after excluding 3 substantively gate-blocked items with no formal Gate field — BLG-FEAT-73/74/76 — and 4 items already complete or already satisfied by shipped work — BLG-GOV-335/336/337/326 — and clearing 2 verified lapsed-date gates — BLG-GOV-90/188). Selection method: all ready P2 items first (0 ready P1), then category-balanced round-robin oldest-first for remaining P3/P4 — per `release_planning_prompt.md` §1.4c. EPIC-01 leads the table as this cycle's execution-heavy (build-and-ship) rotation slot and seats the rebalance's mandatory pull-forward items BLG-FEAT-96/97. All 6 EPIC-01 items and both EPIC-02 items carry an observable UI acceptance criterion — `design_gate_required: true`.

---

## EPIC-01 — Product Features & Frontend Build-and-Ship

**Maps to:** S2-01
**Owner:** Head of Engineering; Head of UX & Design; Product Owner; Frontend Specifications & UX Documentation Owner

### ST-01 — 'Clone as new plan' action on the Trade Plans list
**Source:** BLG-FEAT-96
**Priority:** P2
**Effort:** S (~0.5–1d)
**Notes:** Frontend-visible — Playwright coverage required (CLAUDE.md §2). Edits `TradePlans.js`/`TradePlan.js`: land before ST-02 (`BLG-FE-180`, same files) and ST-06 (`BLG-FE-182`).
**Acceptance Criteria:**
- Clicking Clone opens a new, unsaved plan pre-populated from the source
- The cloned plan has status `planned`, fresh dates and no `position_id`
- Playwright test covering the observable AC passes in CI (CLAUDE.md §2 frontend-visible-change rule)

### ST-02 — Flag stale 'planned' trade plans on the Trade Plans list
**Source:** BLG-FE-180
**Priority:** P3
**Effort:** S (~0.5–1d)
**Notes:** Edits `TradePlans.js` — sequence after ST-01 (`BLG-FEAT-96`), not in parallel.
**Acceptance Criteria:**
- A `planned` plan older than the threshold shows the marker; a newer plan does not
- Playwright test covering the observable AC passes in CI (CLAUDE.md §2 frontend-visible-change rule)

### ST-03 — CSV export for Screener results and Watchlist
**Source:** BLG-FEAT-97
**Priority:** P2
**Effort:** S (~0.5–1d)
**Acceptance Criteria:**
- Export downloads a file whose columns equal the visible columns on both pages
- Playwright test covering the observable AC passes in CI (CLAUDE.md §2 frontend-visible-change rule)

### ST-04 — In-app reminder to complete TradeReflection within 48 hours of a trade closing
**Source:** BLG-FEAT-98
**Priority:** P3
**Effort:** M (~1–2d)
**Acceptance Criteria:**
- A closed trade without a reflection produces exactly one reminder after 48h
- Completing the reflection or dismissing suppresses it
- Playwright test covering the observable AC passes in CI (CLAUDE.md §2 frontend-visible-change rule)

### ST-05 — Name one primary next action in every empty state
**Source:** BLG-FE-181
**Priority:** P3
**Effort:** S (~1d)
**Acceptance Criteria:**
- 0 audited empty states without a next-action link
- Playwright test covering the observable AC passes in CI (CLAUDE.md §2 frontend-visible-change rule)

### ST-06 — Single number/currency formatting helper — audit and migrate the highest-traffic tables
**Source:** BLG-FE-182
**Priority:** P3
**Effort:** M (~2d)
**Notes:** Touches Positions, TradeHistory and TradePlans — sequence last within EPIC-01 so it rebases onto ST-01/ST-02's `TradePlans.js` changes.
**Acceptance Criteria:**
- The three tables use the helper with identical negative/decimal conventions
- Playwright test covering the observable AC passes in CI (CLAUDE.md §2 frontend-visible-change rule)

---

## EPIC-02 — Financial Reporting & Records Integrity

**Maps to:** S2-02
**Owner:** Financial Reporting & Records Owner; Backend Engineering Patterns Owner; Metrics Definitions & Analytics Owner

### ST-07 — Audit whether closed-trade P&L is net of fees_paid; flag closed trades with NULL fees_paid in Monthly P&L
**Source:** BLG-FR-04
**Priority:** P3
**Effort:** S (~0.5–1d)
**Notes:** Sequence before ST-08 (`BLG-FR-05`): the net/gross basis must be documented before month-end snapshots freeze figures computed on it. If a gross-vs-net discrepancy is found, file a fix item rather than changing reported figures inside this story.
**Acceptance Criteria:**
- The net/gross basis is documented in the canonical metrics spec
- A NULL-fee closed trade is counted and visible in Monthly P&L

### ST-08 — Month-end immutable snapshot of Monthly P&L and the tax-year table, with a restatement diff
**Source:** BLG-FR-05
**Priority:** P3
**Effort:** M (~2d)
**Notes:** Persisting a read-only snapshot per closed month likely needs a new table/migration plus a `data_model.md` entry; the M (~2d) estimate may understate this — see RISK-02. Observable diff AC is frontend-visible (Playwright or recorded staging run).
**Acceptance Criteria:**
- A snapshot exists per closed month
- Editing a closed trade in a snapshotted month surfaces a restatement diff

---

## EPIC-03 — Backend & Platform Engineering Debt

**Maps to:** S2-03
**Owner:** Backend Engineering Patterns Owner; Strategy Rules & System Intent Owner; Financial Reporting & Records Owner

### ST-09 — calculate_trailing_stop's entry-price floor for profitable positions diverges from strategy_rules.md §7.2/§7.3 and from the backtest tool
**Source:** BLG-BE-119
**Priority:** P2
**Effort:** S (~0.5–1d — mostly decision + documentation; code change scope depends on which side is chosen)
**Notes:** Decision-first story: Strategy Rules & System Intent Owner ratifies which formula is correct before any code change. Option (b) (removing the floor) changes live trading behaviour on real capital and needs explicit sign-off. If no sign-off is obtained this sprint, ship only the golden-output case and the recorded decision, leave `calculate_trailing_stop` unchanged, and disclose. Option (a) requires editing `claude/strategy/strategy_rules.md` §7.2 — a governance file outside Sprint Execution's autonomous write scope (CLAUDE.md §2, §7): that edit must go through the Strategy Rules & System Intent Owner's own change route with explicit sign-off, not be made by the engine on its own. Sequenced ahead of `BLG-BE-122` (ST-13), which also touches the nightly stop-update path.
**Acceptance Criteria:**
- A formal decision is recorded (either updates `strategy_rules.md` §7.2 to include the floor, or removes it from `calculate_trailing_stop` — not both, not neither)
- `position_manager.py`, `calculate_trailing_stop`, and the spec formula all agree after the decision is implemented
- A new golden-output case exercises the previously-untested entry-price-floor-binding scenario
- `BLG-BE-114`/ST-04 unblocked and able to proceed to a single shared implementation

### ST-10 — list_backtest_rule_runs has no negative-limit validation and no offset param
**Source:** BLG-BE-118
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- A negative `limit` on `GET /backtest-rule-changes/runs` returns HTTP 400 `INVALID_PARAMS`, not a 500
- Existing passing behaviour for valid `limit` values is unchanged

### ST-11 — JsonLinesFormatter does not truncate `message` to the spec's 500-char max
**Source:** BLG-BE-120
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- A log message longer than 500 characters is truncated to the spec's limit in the emitted JSON
- Existing `tests/test_json_log_formatter.py` cases still pass unchanged

### ST-12 — Float-vs-Decimal money-arithmetic audit with rounding-boundary golden tests
**Source:** BLG-BE-121
**Priority:** P3
**Effort:** M (~1.5–2d)
**Acceptance Criteria:**
- Inventory recorded in the QA evidence file
- Golden tests for each boundary case pass
- 0 unexplained ≥£0.01 discrepancies across the sizing golden set

### ST-13 — Shared upstream-call helper: uniform timeout and bounded retry budget for yfinance, Alpaca and Anthropic
**Source:** BLG-BE-122
**Priority:** P3
**Effort:** M (~1.5–2d)
**Notes:** Touches the live nightly stop-update path — land after ST-09 (`BLG-BE-119`) so the two do not collide on the same call path.
**Acceptance Criteria:**
- No unbounded upstream call remains in the nightly stop-update path
- Timeout and retry values are configured in one place
- Existing tests still pass; new tests cover timeout and retry-exhaustion

---

## EPIC-04 — Operations & Security Debt

**Maps to:** S2-04
**Owner:** Infrastructure & Operations Owner; FinOps & Resource Architect

### ST-14 — Dead-man's-switch alert when nightly-stop-update has not succeeded within 26 hours
**Source:** BLG-OPS-166
**Priority:** P2
**Effort:** S (~0.5–1d)
**Acceptance Criteria:**
- A simulated missed run raises the alert within the window
- A successful run clears it

### ST-15 — Document GitHub Actions secrets ownership map
**Source:** BLG-OPS-163
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- Every secret referenced in `.github/workflows/*.yml` via `secrets.*` appears in the inventory with its consuming workflow(s) and required access level
- Document is discoverable from the two cross-references named above
- Infrastructure & Operations Owner sign-off

### ST-16 — Confirm synthetic uptime monitor live-fire and notification delivery (ST-11 follow-up)
**Source:** BLG-OPS-164
**Priority:** P3
**Effort:** XS (<1h)
**Notes:** Needs a token/session with Actions-write access and real Telegram receipt confirmation; the prior session's `gh workflow run` returned HTTP 403. If still unavailable, disclose the AC as not closeable rather than fabricating evidence.
**Acceptance Criteria:**
- A real live-fire test run is confirmed to have triggered the alert path (run URL/ID recorded)
- A real Telegram notification is confirmed received (not just that the workflow step executed)
- `docs/ops/synthetic_uptime_monitor_confirmation_2026-09-16.md` §7 and §8 updated to reflect the confirmed result; `BLG-OPS-158`'s (ST-11's) original disclosed gap closed

### ST-17 — CI minutes and artifact-storage visibility; explicit retention on the 3 uploads that lack it
**Source:** BLG-OPS-165
**Priority:** P3
**Effort:** S (~0.5d)
**Acceptance Criteria:**
- A monthly per-workflow figure exists
- All artifact uploads carry explicit retention

---

## EPIC-05 — QA & Test Coverage Debt

**Maps to:** S2-05
**Owner:** QA & Testing Owner; Director of Quality; QA Lead

### ST-18 — Quarterly full-suite Playwright re-run against a fresh staging seed
**Source:** BLG-QA-171
**Priority:** P3
**Effort:** M
**Notes:** Needs a live staging environment and a fresh seed; the first-run AC is environment-dependent — see RISK-05.
**Acceptance Criteria:**
- Cadence and seed procedure documented
- First quarterly run completed with results recorded

### ST-19 — DoQ checklist addendum for flaky-test disposition
**Source:** BLG-QA-172
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- Addendum added to the DoQ checklist
- Cross-reference confirmed correct against the existing quarantine item

### ST-20 — Standing regression check for the OpenAPI Drift Detection gate itself
**Source:** BLG-QA-173
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- Both fixtures exist and pass in CI
- A deliberate revert of the gate's logic is confirmed to fail the fixture (proving the test actually tests something)

### ST-21 — `test_trade_plan_audit_log.py`'s unrestored `sys.modules["database"]` swap is a latent test-isolation hazard
**Source:** BLG-QA-178
**Priority:** P3
**Effort:** XS (<1h)
**Acceptance Criteria:**
- `test_trade_plan_audit_log.py` no longer mutates the shared `sys.modules["database"]` entry
- Full backend test suite (`backend/.venv/bin/python3 -m pytest tests/`) still passes, and a manual reordering check confirms no other order-dependent leakage remains from this specific pattern
- Any other file found with the same unrestored pattern is fixed in the same commit

---

## EPIC-06 — Spec & Documentation Debt

**Maps to:** S2-06
**Owner:** Data Model & Domain Schema Owner; Strategy Rules & System Intent Owner; Frontend Specifications & UX Documentation Owner; Head of Engineering; Metrics Definitions & Analytics Owner

### ST-22 — DS-17 unique index migration not yet applied to live positions table
**Source:** BLG-SPEC-148
**Priority:** P2
**Effort:** XS (<1h)
**Notes:** Applying the DS-17 up-migration needs write access to the live database; the staging credential is read-only. Human/delegated step — disclose if unavailable rather than fabricating a confirmation.
**Acceptance Criteria:**
- `idx_positions_open_ticker_entry_date_unique` exists on the live `positions` table
- DS-17's AC-03 "pending" disclosure in `data_model.md` is updated to confirmed-applied, with date

### ST-23 — PO-05 (Lightweight Replay Mode) §13 determinism pre-clearance review, standalone
**Source:** BLG-SPEC-160
**Priority:** P2
**Effort:** XS (~0.5 day)
**Acceptance Criteria:**
- A dated §13 determination exists
- `BLG-FEAT-74`'s gate line reflects the outcome

### ST-24 — Canonical colour-blind-safe chart palette spec
**Source:** BLG-SPEC-144
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- Palette documented with justification (e.g. a recognised colour-blind-safe source)
- Cross-referenced from at least the design system spec

### ST-25 — Lightweight ADR log for cross-cutting backend decisions
**Source:** BLG-SPEC-145
**Priority:** P3
**Effort:** M
**Acceptance Criteria:**
- File exists with template and at least 2 seeded entries
- Referenced from a relevant onboarding/index document

### ST-26 — Canonicalise the Sharpe-ratio lookback window
**Source:** BLG-SPEC-146
**Priority:** P3
**Effort:** S
**Acceptance Criteria:**
- Canonical window documented with rationale
- Discrepancy noted explicitly for each of the 3 current call sites (fix itself may be a separate follow-on item)

---

## EPIC-07 — Governance Process Debt

**Maps to:** S2-07
**Owner:** Head of Specs Team; Product Owner; PMO Lead; FinOps & Resource Architect; AI Compliance & Governance Officer; Strategy Rules & System Intent Owner

### ST-27 — Release-planning gate scan treats lapsed date gates as permanently gated
**Source:** BLG-GOV-345
**Priority:** P2
**Effort:** S (~0.5–1d)
**Notes:** Edits `scripts/scan_backlog_gate_conditions.py` and `release_planning_prompt.md` §1.3a — CLAUDE.md §6 Governance File Edit Checklist applies (version bump, `OPERATIONAL_GUIDE.md` §14, source-prompt header, `prompt_change_log.md`). Sequence before ST-30 (`BLG-GOV-325`) so the two prompt-version bumps do not collide (RISK-07). The six lapsed-date items named in its Problem were verified at Release Planning — see `run_manifest.md`; `BLG-GOV-90` and `BLG-GOV-188` are already re-included as ST-31/ST-32.
**Acceptance Criteria:**
- Scan reports lapsed-date items separately
- Each of the six items is verified and either cleared (gate line removed, dated note) or re-gated with a new dated condition
- §6 checklist complete for any prompt change

### ST-28 — Re-confirm §13 boundary review cadence
**Source:** BLG-GOV-329
**Priority:** P2
**Effort:** S
**Acceptance Criteria:**
- Explicit decision recorded (schedule now / defer with concrete trigger)
- If deferred again, the new trigger must be more concrete than the prior one (per the STEP 8.1.5 finding)

### ST-29 — Revisit sprint capacity band given sustained ≥90% utilisation
**Source:** BLG-GOV-328
**Priority:** P3
**Effort:** S
**Notes:** Writes to `claude/roadmap/workforce_capacity.md`. Per the 2026-09-19 write-scope ruling (`execution_prompt.md` §7), this is permitted only where the sealed `sprint_backlog.md` names the file in an ST item's AC or sequencing note — Sprint Planning must carry this reference into the sealed sprint backlog.
**Acceptance Criteria:**
- Review completed and documented in `workforce_capacity.md`
- Explicit hold/raise decision recorded, not merely re-noted as "revisit again next cycle"

### ST-30 — Fixed-cadence audit of every governance prompt's §14 version-table entry
**Source:** BLG-GOV-325
**Priority:** P3
**Effort:** S
**Notes:** Edits a governed prompt (`roadmap_prompt.md` or the manage-roadmap prompt) — CLAUDE.md §6 checklist applies; sequence after ST-27.
**Acceptance Criteria:**
- Cadence defined and wired into a governed routine's mandatory steps
- First mandatory-cadence run completed with results recorded

### ST-31 — Claude model deprecation monitoring procedure (consolidated)
**Source:** BLG-GOV-90
**Priority:** P3
**Effort:** S (~0.5 day)
**Notes:** Builds on existing `docs/governance/ai_model_version_pinning_policy.md` (§6–§7) and `ai_model_deprecation_check_v52.md` — do not duplicate them. Gate (`BLG-GOV-74` first quarterly review) verified met at Release Planning: `docs/governance/ai_feature_usage_quarterly_review_2026-09-07.md` (v9.1).
**Acceptance Criteria:**
- Deprecation monitoring procedure defined and documented
- Procedure integrated with BLG-GOV-74 quarterly review cadence
- Gate condition (BLG-GOV-74 first review complete) verified before sprint planning

### ST-32 — Sprint Velocity Trend Chart
**Source:** BLG-GOV-188
**Priority:** P3
**Effort:** S (~1–2 days)
**Notes:** Gate line reads 'None — revival condition confirmed Met 2026-07-08'; verified ungated at Release Planning. A governance artefact (generated chart from `velocity_metrics.md`), not product UI.
**Acceptance Criteria:**
- Chart built, showing at least delivered-story-count and U/G/D/P split per cycle over the available history

---
