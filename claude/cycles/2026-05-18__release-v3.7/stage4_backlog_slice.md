Owner: Product Owner
Class: Planning Document (Class 4)
Status: Active
Release: v3.7
Cycle: 2026-05-18__release-v3.7
Last Updated: 2026-05-18

---

# Sprint Backlog Slice — v3.7 Signal-to-Watchlist Workflow + Arc 2 Completion + Governance Hardening

<!-- release-plan-marker: RP:v3.7:2026-05-18__release-v3.7 -->

---

## EPIC-01 — Signals-to-Watchlist Workflow

**Maps to:** S2-01
**Owner:** Head of Engineering
**Risk IDs:** RISK-02
**Sprint:** Sprint 1
**Estimated effort:** ~6 days total (3 × M stories)

Closes the disciplined entry funnel by replacing the "Add Position" CTA on signal cards with "Add to Watchlist", enforcing the signal → watchlist → research → plan → entry workflow. Also surfaces signal context in the trade plan form to eliminate manual context-switching when writing entry rationale.

---

### ST-01 — BLG-FE-33: Signals page backend — watchlisted status support

**Owner:** Head of Engineering
**Estimated effort:** M (~1–2 days)
**Delegation class:** autonomous
**Sprint:** 1
**Dependencies:** None

**Acceptance Criteria:**
- `watchlisted` added to signals table CHECK constraint on `status` column
- `PATCH /signals/{id}` updated to accept `status: "watchlisted"` as a valid value
- `signal_endpoints.md` updated: PATCH endpoint section documents `watchlisted` status (version bumped, changelog entry, OPERATIONAL_GUIDE §14 and prompt_change_log.md updated in same commit)
- `data_model.md` updated: signals table schema reflects `watchlisted` CHECK constraint (version bumped, changelog entry, same commit)
- Existing signal statuses (`active`, `dismissed`, etc.) unaffected
- Backend test in `backend/routers/test.py` covers PATCH `/signals/{id}` with `status=watchlisted`

---

### ST-02 — BLG-FE-33: Signals page frontend — Add to Watchlist CTA

**Owner:** Head of Engineering
**Estimated effort:** M (~1–2 days)
**Delegation class:** standard
**Sprint:** 1
**Dependencies:** ST-01 (PATCH /signals/{id} watchlisted support)

**Acceptance Criteria:**
- Signal card "Add Position" button replaced with "Add to Watchlist" as primary CTA on new signal cards
- Clicking "Add to Watchlist" calls `POST /watchlist` with ticker, market, initial_stop_price pre-filled; on success calls `PATCH /signals/{id} status=watchlisted`
- Signal card transitions to watchlisted state: "View in Watchlist" link shown (→ /watchlist); no action buttons remain
- "Dismiss" button retained as secondary action on new signal cards
- Duplicate add (ticker already on watchlist): toast "Already on your watchlist"; signal still transitions to watchlisted state
- No regression to Add Position flow on signal cards
- `signals.spec.js` page spec updated to document watchlisted card state and Add to Watchlist action
- Playwright scenario SC-SIG-01 (or equivalent) authored covering the Add to Watchlist happy path

---

### ST-03 — BLG-FE-34: Trade plan form signal context panel

**Owner:** Head of Engineering
**Estimated effort:** M (~1–2 days)
**Delegation class:** standard
**Sprint:** 1
**Dependencies:** ST-01, ST-02 (signal → watchlist linkage required to pass signal data through)

**Acceptance Criteria:**
- Read-only "Signal Context" panel shown in trade plan creation form when a linked signal exists for the ticker: rank, momentum %, price vs 200-day MA (% above/below), regime on/off, ATR value, suggested initial stop (entry price − 5 × ATR)
- Entry rationale pre-populated with structured template: "Rank {N} momentum signal. Price {above/below} 200-day MA by {x}%. {US/UK} regime on." (user-editable)
- Confirmation criteria pre-populated with strategy defaults: "Price above 200-day MA at entry. Regime on. Spare cash available." (user-editable)
- Stop field pre-filled with suggested stop: entry price − (5 × ATR matching initial_atr_mult=5)
- Signal Context panel hidden and fields blank when no linked signal exists — no regression to current behaviour
- Signal Context data is read-only within the form
- `trade_plan.md` frontend spec updated (Signal Context section added, version bumped)
- Playwright scenario covering Signal Context panel presence when signal exists; absence when no signal

---

## EPIC-02 — Arc 2 Completion: PT-04 Setup Quality Score (Conditional)

**Maps to:** S2-02
**Owner:** Head of Specs Team + Head of Engineering
**Risk IDs:** RISK-01
**Sprint:** Sprint 2 (conditional on gate)
**Estimated effort:** ~4 days total (1 × XS + 2 × M)

**GATE CONDITION:** Product Owner must confirm 20+ closed trades before sprint planning seals. If not confirmed, entire EPIC-02 defers to v3.8. Sprint Planning Engine STEP -1 must consume this pre-sprint required decision.

PT-04 is the last remaining Arc 2 feature — a deterministic score (0–100) against the user's own historical win conditions. No ML — calculated from own trade history.

---

### ST-04 — PT-04 spec authoring and gate confirmation

**Owner:** Head of Specs Team + Product Owner
**Estimated effort:** XS (~0.5 day)
**Delegation class:** delegated_decision
**Sprint:** 2 (if gate confirmed)
**Dependencies:** Product Owner gate confirmation (20+ closed trades)

**Acceptance Criteria:**
- Product Owner confirms closed trade count ≥ 20 (recorded in sprint_planning_notes.md)
- `docs/specs/pt04_setup_quality_score.md` created — defines: score formula, input fields (regime at entry, signal rank, ATR at entry, sector, momentum %), scaling function, edge case handling (insufficient history → score displayed as "N/A — insufficient history")
- Spec reviewed and signed off by Head of Specs Team
- `docs/reference/openapi.yaml` pre-updated with `GET /trade-plans/{id}/quality-score` endpoint stub

---

### ST-05 — PT-04 backend: quality score calculation endpoint

**Owner:** Head of Engineering
**Estimated effort:** M (~2 days)
**Delegation class:** autonomous
**Sprint:** 2 (if gate confirmed)
**Dependencies:** ST-04 (spec must be signed off)

**Acceptance Criteria:**
- `GET /trade-plans/{id}/quality-score` endpoint returns deterministic score (0–100) or `{"score": null, "reason": "insufficient_history"}` when fewer than 20 closed trades
- Score calculation uses closed trade history: win rate under similar entry conditions (regime, signal rank band, ATR band); no ML; fully deterministic
- Endpoint added to `backend/routers/test.py`
- `docs/reference/openapi.yaml` updated with full response schema in same commit
- Score recalculates on each request (no caching required at this stage)

---

### ST-06 — PT-04 frontend: quality score display

**Owner:** Head of Engineering
**Estimated effort:** M (~2 days)
**Delegation class:** standard
**Sprint:** 2 (if gate confirmed)
**Dependencies:** ST-05

**Acceptance Criteria:**
- Setup Quality Score displayed on Trade Plan detail view (0–100 or "N/A — insufficient history")
- Score displayed on Pre-Trade Research View alongside existing metrics
- Score is read-only and labelled clearly (not presented as a prediction — "based on your own trade history")
- `trade_plan.md` and `pre_trade_research.md` frontend specs updated (Quality Score section added)
- Playwright scenario covering: score shown when ≥ 20 closed trades; "insufficient history" message when < 20

---

## EPIC-03 — Governance Hardening Patches

**Maps to:** S2-03
**Owner:** Head of Specs Team + Director of Quality
**Risk IDs:** RISK-03
**Sprint:** Sprint 1
**Estimated effort:** ~1 day total (2 × S)

Delivers the 4 actionable deferred patches from v3.6 lessons learnt closure (items 1, 2, 4, 5 from the closure record deferred table; item 3 is a PMO enforcement action with no file change).

---

### ST-07 — execution_prompt.md patches ×3 (deviations_filed + backlog verify + spec_references verify)

**Owner:** Head of Specs Team
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Sprint:** 1
**Dependencies:** None

**Acceptance Criteria:**
- **Sub-step 10a (deviations_filed atomic write):** §3.1.A story completion checklist gains explicit sub-step immediately after step 10 deviation check: "Immediately after step 10 deviation check: write `deviations_filed: true` to execution_state.json for this ST item. Do not defer." Make the flag-write atomic with the deviation check (LL-v3.6 item 1)
- **Backlog verify guidance:** §3.1.A story completion checklist gains: "When filing a mandatory backlog item for a deferred staging AC, verify the item appears in backlog.md before closing the story (file read or grep check)." (LL-v3.6 item 4)
- **spec_references path verify guidance:** §3.1.A story completion checklist gains: "When populating spec_references in execution_state.json, verify each path exists using a file read or ls check before recording." (LL-v3.6 item 5)
- execution_prompt.md version bumped; OPERATIONAL_GUIDE §14 + phase section header updated; prompt_change_log.md entry appended — per CLAUDE.md §6 (4-step governance file edit checklist)
- Also retroactively add prompt_change_log.md entries for execution_prompt.md v3.18→v3.22, sprint_planning_prompt.md v3.0→v3.2, backlog_management_prompt.md v1.6→v1.7 (addressing STEP -1.7 advisory gaps from this release planning run)

---

### ST-08 — qa_evidence_template.md: BLG-GOV-19 criterion 3 fail-path

**Owner:** Director of Quality
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Sprint:** 1
**Dependencies:** None

**Acceptance Criteria:**
- `docs/qa/templates/qa_evidence_template.md` BLG-GOV-19 section gains explicit criterion 3 fail-path: "If any story has observable AC → autonomous class does not apply regardless of Playwright coverage. Use standard DoQ sign-off block and record Playwright test file references in DoQ comments." (LL-v3.6 item 2)
- qa_evidence_template.md version bumped; if Class 6 governance file: OPERATIONAL_GUIDE §14 + prompt_change_log.md updated per CLAUDE.md §6

---

## EPIC-04 — Technical Debt Clearance

**Maps to:** S2-04
**Owner:** Head of Engineering + QA & Testing Owner + Facilitator (BLG-GOV-23)
**Sprint:** Sprint 1
**Estimated effort:** ~1.5 days total

---

### ST-09 — BLG-QA-20: Database stub conftest consolidation

**Owner:** QA & Testing Owner
**Estimated effort:** S (~0.5 day)
**Delegation class:** autonomous
**Sprint:** 1
**Dependencies:** None

**Acceptance Criteria:**
- `tests/conftest.py` created with session-scoped database stub fixture containing all current database function mocks
- The four test files (`test_alerts_service.py`, `test_watchlist_service.py`, `test_trade_service.py`, `test_service_coverage.py`) no longer each define their own `types.ModuleType("database")` block
- All existing tests pass (69+ tests collected, no new collection errors)
- CI green after change

---

### ST-10 — BLG-OPS-16 + BLG-FE-35: Pycache git hygiene + Research page font staging

**Owner:** Head of Engineering (BLG-OPS-16) + Head of UX & Design (BLG-FE-35)
**Estimated effort:** XS + XS (~0.5 day combined)
**Delegation class:** autonomous (BLG-OPS-16) / delegated_decision (BLG-FE-35)
**Sprint:** 1
**Dependencies:** None

**Acceptance Criteria — BLG-OPS-16:**
- `git rm -r --cached backend/__pycache__/` run to untrack all pyc files
- `__pycache__/` and `*.pyc` added to `.gitignore`
- CI green after change; no pyc or __pycache__ files tracked in git

**Acceptance Criteria — BLG-FE-35:**
- Head of UX & Design performs side-by-side comparison of Research page rendering against `docs/frontend/design_system.md` typography scale in live/staging environment
- Date of staging run recorded in this story's DoQ sign-off block
- If conformant: BLG-FE-26 and BLG-FE-35 archived to backlog_archive.md
- If non-conformant: new backlog item filed with specific font deviation details; BLG-FE-35 remains open

---

### ST-11 — BLG-GOV-23: scored_initiatives.md comprehensive refresh

**Owner:** Facilitator
**Estimated effort:** S (~0.5–1 day)
**Delegation class:** delegated_decision
**Sprint:** 1
**Dependencies:** None

**Acceptance Criteria:**
- `claude/scoring/scored_initiatives.md` header Last Updated updated to date of refresh
- Arc 3 items (IT-01–IT-06) have scored rows with SPS and effort bands (for historical completeness)
- Active Arc 4–6 roadmap initiatives (PO-01–05, SI-01–05, PS-01–05) have scored rows with current SPS and effort bands per STEP 6 scoring criteria
- All existing scored rows preserved
- OA-RP-05 closed
