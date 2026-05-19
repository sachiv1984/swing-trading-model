**Owner:** Product Owner
**Class:** Planning Document (Class 4)
**Status:** Published
**Version:** 1.0
**Cycle:** 2026-05-19__release-v3.8
**Release:** v3.8
**Published:** 2026-05-19

---

# Backlog Slice — v3.8

**Theme:** Arc 5 Strategy Integrity Foundation + Trade Plan Form Enhancements + Ticker Universe Management

<!-- release-plan-marker: RP:v3.8:2026-05-19__release-v3.8 -->

---

## EPIC-04 — Platform & Governance

**Maps to:** S2-04, S2-05
**Owner:** Head of UX & Design; Head of Backend Engineering; Head of Specs Team
**Sprint:** 1
**Merge order:** 1st (fewest shared file conflicts)

### ST-09 — Ticker Universe Management Page

**Source:** BLG-FEAT-22
**Effort:** M (~1–2 days)
**Type:** Product Feature / User Configuration
**Sprint:** 1

**Description:** Build a Ticker Universe Management page in the frontend. Retire the startup sync from `public.tickers` into `ticker_universe` — making `ticker_universe` the sole authoritative source for screener and signal generation. Users can add, toggle active/inactive, and delete tickers; filter by market and active status.

**Acceptance Criteria:**
- `public.tickers` startup sync removed; `ticker_universe` populated only via management UI or seed defaults
- Universe Management page accessible from nav; displays all tickers with market, sector, and active status
- User can add a ticker (US or UK market); appears immediately in the table
- User can toggle a ticker inactive; inactive tickers excluded from next screener/signal run
- User can delete a ticker permanently
- Filter by market (US/UK/All) and active status works
- Screener and signal generation both use only active tickers from `ticker_universe`
- Playwright coverage: add, toggle, delete, and filter scenarios

### ST-10 — Governance Debt Clearance

**Source:** BLG-GOV-24 + DoQ enforcement OA (v3.7 carry-forward)
**Effort:** XS (<1h)
**Type:** Governance Process
**Sprint:** 1

**Description:** Add `gh_issue_template.md` to the §14 governance table in `OPERATIONAL_GUIDE.md`. Implement the DoQ sign-off date enforcement mechanism (PR checklist item or pre-merge comment template) to prevent retrospective sign-off gaps — v3.7 carry-forward from Director of Quality.

**Acceptance Criteria:**
- `gh_issue_template.md` entry added to §14 governance table in `OPERATIONAL_GUIDE.md` with version v1.0
- `/governance-drift` no longer flags the file as UNTRACKED
- DoQ enforcement mechanism implemented (PR checklist entry or pre-merge comment template — format at Director of Quality's discretion)
- OPERATIONAL_GUIDE.md version bumped; prompt_change_log.md entry added

---

## EPIC-03 — Trade Plan Form Enhancements

**Maps to:** S2-03
**Owner:** Head of UX & Design; Backend Engineering Patterns Owner
**Sprint:** 1
**Merge order:** 2nd

### ST-06 — Setup Type Classification Field

**Source:** BLG-FEAT-23
**Effort:** S (~0.5 days)
**Type:** Product Feature / Data Model
**Sprint:** 1

**Description:** Add a "Setup Type" dropdown to the trade plan form with six options: Breakout / Pullback to MA / Momentum Continuation / Mean Reversion / Catalyst-driven / Other. Add `setup_type` column to `trade_plans` table via migration. Update API to accept and persist `setup_type`.

**Acceptance Criteria:**
- `setup_type` (VARCHAR, nullable) column added to `trade_plans` table via migration
- `POST /trade-plans` and `PUT /trade-plans/{id}` accept and persist `setup_type`
- `GET /trade-plans/{id}` includes `setup_type` in response
- Setup type dropdown appears above the setup thesis textarea on the trade plan form
- All six options selectable; selected value saved with the plan
- Existing plans without `setup_type` display field as unset — no breaking change
- When opened from a momentum signal, default is "Momentum Continuation"
- `setup_type` visible in trade plan read view
- Playwright: verify dropdown renders, saves, and displays correctly

### ST-07 — News Context Panel on Trade Plan Form

**Source:** BLG-FE-36
**Effort:** S (~0.5 days)
**Type:** Frontend / UX
**Sprint:** 1
**Dependency:** Alpaca News API already integrated (screener news panel uses same endpoint)

**Description:** Add a collapsible "News Context" panel to the trade plan form shown when a ticker is set. Fetch last 3–5 headlines from Alpaca News API. Display as read-only list with title, source, and relative age. Panel positioned above setup thesis field.

**Acceptance Criteria:**
- News panel visible on trade plan form when a US ticker is set
- Shows up to 5 most recent headlines with title, source, and relative age
- Panel is collapsible; collapsed state persisted in localStorage per ticker
- If news API returns no results, panel hidden entirely (not shown as "No news")
- Existing pre-population of setup thesis and entry rationale fields unchanged
- Backend: `GET /news/{ticker}` proxy endpoint added or existing screener news route reused
- Playwright: panel renders for US ticker; hidden when no news returned

### ST-08 — AI-Assisted Thesis Generation

**Source:** BLG-FEAT-24
**Effort:** M (~1–2 days)
**Type:** Product Feature / UX Enhancement
**Sprint:** 1
**Depends on:** ST-06 (setup type dropdown), ST-07 (news context panel)

**Description:** Add a "Generate thesis" button adjacent to the setup thesis textarea. Template engine (Phase 1, no API call) generates a structured thesis from setup type + signal metrics + top 2 headlines + price data. Optional Phase 2 Gemini Flash integration via env-var gate.

**Acceptance Criteria:**
- "Generate thesis" button present next to setup thesis field
- Template engine generates draft from available signal + news + price data without any API key
- Generated text is editable; saved plan stores user's final version
- "AI draft" badge present on generated text; badge clears on first user edit
- "Improve with AI" button hidden entirely when Gemini API key not configured (not disabled)
- No thesis auto-generated without user clicking the button
- Playwright: button visible; generated text populates textarea; badge clears on edit

---

## EPIC-01 — Arc 5 Strategy Integrity Foundation

**Maps to:** S2-01
**Owner:** Strategy Rules & System Intent Owner; Head of Backend Engineering; Head of UX & Design
**Sprint:** 1 (gate story), 2 (implementation)
**Merge order:** 3rd

### ST-01 — §13 Review Gate for SI-01 Pre-Entry Rule Validation Gate

**Effort:** XS (delegated_decision — Sprint 1)
**Type:** delegated_decision / §13 compliance gate
**Sprint:** 1
**Classification:** delegated_decision — blocks ST-02 and ST-03

**Description:** Strategy Rules & System Intent Owner conducts §13 compliance review for SI-01 Pre-Entry Rule Validation Gate. Determines whether the feature is within system boundaries, and if so documents binding conditions on the implementation. Delivers a formal §13 review decision record.

**Acceptance Criteria:**
- §13 review conducted and decision documented: PASS or FAIL with rationale
- If PASS: binding conditions recorded in `docs/product/decisions/decisions--2026-05-19__release-v3.8--SI-01-section13-review.md`
- If FAIL: EPIC-01 removed from sprint scope and ST-02/ST-03 set to blocked
- Decision record references strategy_rules.md §13 directly
- ST-01 status: done before ST-02 and ST-03 may begin execution

### ST-02 — SI-01 Backend — Pre-Entry Validation Service

**Effort:** M (~1–2 days)
**Type:** Backend / API
**Sprint:** 2
**Depends on:** ST-01 §13 PASS

**Description:** Implement a pre-entry validation service that checks a proposed position against all rules in `strategy_rules.md §11` — regime gate, position sizing within limits, sector concentration, earnings proximity, cash constraint. New endpoint: `GET /portfolio/pre-entry-validation?ticker=X&quantity=N`. Non-blocking advisory output — returns validation result with per-rule pass/fail and aggregate advisory status.

**Acceptance Criteria:**
- `GET /portfolio/pre-entry-validation?ticker={ticker}&quantity={n}` endpoint implemented
- Validates against: regime gate (strategy_rules.md §11), position sizing limits, sector concentration threshold, earnings proximity warning, cash constraint check
- Response includes per-rule result (pass/warn/fail) and aggregate advisory status
- Non-blocking: all checks return advisory results; no hard stops enforced
- Explicit override recorded in response when rules have advisory fails
- Endpoint registered in backend/routers/test.py and openapi.yaml
- Unit tests cover all 5 validation rule types
- §13 binding conditions (from ST-01 decisions record) applied verbatim

### ST-03 — SI-01 Frontend — Pre-Entry Validation Panel

**Effort:** M (~1–2 days)
**Type:** Frontend / UX
**Sprint:** 2
**Depends on:** ST-01 §13 PASS, ST-02

**Description:** Surface the pre-entry validation results as an advisory panel within the Trade Plan creation flow. Non-blocking — displays results as informational checks with clear pass/warn/fail indicators. Explicit override capability (user can acknowledge and proceed). §13 compliant — decision support, not a hard gate.

**Acceptance Criteria:**
- Pre-Entry Validation Panel rendered in Trade Plan form after ticker and quantity are set
- Displays per-rule results: regime gate, sizing, sector concentration, earnings proximity, cash constraint
- Visual indicators: pass (green), warn (amber), fail (red advisory — not blocking)
- "Override" action available when any rule fails; override acknowledgement recorded on trade plan object
- Panel loads validation data from ST-02 endpoint
- Panel hidden if no ticker/quantity set
- §13 binding conditions applied: display-only advisory; no automatic blocking of plan submission
- Playwright coverage: panel renders; override flow works; plan saves with override recorded

---

## EPIC-02 — Arc 2 Completion (Conditional)

**Maps to:** S2-02
**Owner:** Head of Backend Engineering; Metrics & Analytics Owner
**Sprint:** 2
**Merge order:** 4th (last)
**CONDITIONAL:** Product Owner must confirm 20+ closed trades gate met before sprint planning seals. If gate not confirmed: EPIC-02 removed from sprint scope.

### ST-04 — PT-04 Backend — Setup Quality Score (Conditional)

**Effort:** M (~1–2 days)
**Type:** Backend / Analytics
**Sprint:** 2
**Gate:** 20+ closed trades in trade history

**Description:** Implement a deterministic setup quality score (0–100) based on own trade history. When the user has entered with similar regime/signal/ATR conditions before, the score reflects historical win rate under those conditions. No ML — purely deterministic aggregation of own trade data. New endpoint: `GET /trade-plans/setup-quality-score?ticker=X`.

**Acceptance Criteria:**
- `GET /trade-plans/setup-quality-score?ticker={ticker}` endpoint implemented
- Score (0–100) computed from closed trade history matching current regime/signal/ATR conditions
- Gate: returns `{"gate_not_met": true, "min_trades_required": 20}` if fewer than 20 closed trades exist
- No ML, no external models — deterministic aggregation of own trade history
- Score factors documented in response: matching_trades count, win_rate, average_R, score_explanation
- Endpoint registered in backend/routers/test.py and openapi.yaml
- Unit tests cover: gate not met, gate met with mixed history, perfect history

### ST-05 — PT-04 Frontend — Setup Quality Score Display (Conditional)

**Effort:** M (~1–2 days)
**Type:** Frontend / UX
**Sprint:** 2
**Depends on:** ST-04

**Description:** Surface the Setup Quality Score in the Pre-Trade Research View and Trade Plan form. Display score as a gauge/badge with brief explanation of contributing factors. Show "Insufficient history (< 20 trades)" when gate not met.

**Acceptance Criteria:**
- Setup Quality Score displayed in Pre-Trade Research View when ticker is set
- Score also visible in Trade Plan form view (read mode)
- "Insufficient trade history" message shown clearly when gate not met (not hidden)
- Score badge shows numeric value (0–100) and a qualitative label (Excellent/Good/Fair/Low)
- Tooltip/expandable shows: matching trades count, win rate, average R
- Playwright: score renders; gate-not-met message renders; score updates when ticker changes
