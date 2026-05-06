**Owner:** Head of Specs Team
**Class:** Planning Document (Class 4)
**Status:** Active
**Release:** v3.2
**Cycle:** 2026-05-05__release-v3.2
**Last Updated:** 2026-05-05
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Backlog Slice — v3.2 Arc 2 Pre-Trade Research & Planning

<!-- release-plan-marker: RP:v3.2:2026-05-05__release-v3.2 -->

---

## EPIC-01 — Pre-Trade Research View (PT-02 + PT-03)

**Maps to:** S2-01, S2-02
**Sprint:** Sprint 1
**Owner:** Frontend Specifications & UX Documentation Owner
**Description:** Deliver the Pre-Trade Research View frontend, surfacing GET /research/{ticker} data alongside the prospective heat metric from GET /portfolio/prospective-heat. Navigation integration from screener and watchlist surfaces. This is the primary Arc 2 user-value deliverable for v3.2 — the backend is fully shipped; this EPIC is frontend-only.

---

### ST-01 — Pre-trade research view component — data display

**EPIC:** EPIC-01
**Effort:** M
**Depends on:** None (GET /research/{ticker} backend shipped v3.1)

**Description:** Build the pre-trade research view page/panel. Fetch and render data from GET /research/{ticker}: ticker fundamentals (name, sector, market cap), momentum signal status, ATR, current price and change, and recent news headlines from the existing endpoint response.

**Acceptance Criteria:**
- Research view page exists at a routable path (e.g., `/research/{ticker}`)
- Fetches data from GET /research/{ticker} on load
- Displays: ticker name, sector, momentum signal status, ATR, current price/change, and available news headlines
- Loading and error states handled (loading spinner; graceful error message if endpoint unavailable)
- Responsive layout consistent with existing app design patterns
- No new backend endpoints required — consumes existing GET /research/{ticker} only

---

### ST-02 — Trade plan context panel in research view

**EPIC:** EPIC-01
**Effort:** M
**Depends on:** ST-01

**Description:** Within the research view, surface any active or draft Trade Plan for the researched ticker. If a Trade Plan exists for the ticker, show a summary panel (plan status, risk/reward notes, stop level). If no plan exists, provide a "Create Trade Plan" CTA linking to the Trade Plan form.

**Acceptance Criteria:**
- Research view queries trade plans filtered by ticker (GET /trade-plans?ticker={ticker} or equivalent)
- If active/draft plan exists: display plan summary (status, notes summary, stop level)
- If no plan exists: "Create Trade Plan" button/link present and functional
- Plan summary panel is read-only in this view (no inline editing)
- Consistent with Trade Plan list and detail views from v3.1

---

### ST-03 — Prospective heat at entry metric integration (PT-03)

**EPIC:** EPIC-01
**Effort:** S
**Depends on:** ST-01

**Description:** Integrate the prospective heat at entry metric (GET /portfolio/prospective-heat) into the research view. Display the heat metric alongside the existing portfolio heat context so the user can see what adding this ticker at the researched quantity would do to overall portfolio heat.

**Acceptance Criteria:**
- GET /portfolio/prospective-heat called from research view (with appropriate ticker and quantity parameters)
- Prospective heat value displayed in research view with clear label ("Prospective heat at entry")
- Heat value colour-coded consistently with the existing heat display conventions (green/amber/red bands)
- Graceful handling if prospective-heat endpoint is unavailable (show N/A, do not block the view)
- No new backend endpoints — consumes existing GET /portfolio/prospective-heat

---

### ST-04 — Navigation integration — screener and watchlist entry points to research view

**EPIC:** EPIC-01
**Effort:** S
**Depends on:** ST-01

**Description:** Add entry points to the research view from the screener results page and the watchlist page. Per BLG-FE-22 (to be delivered at design gate), the workflow is: screener results → research view (per-ticker). Watchlist entries should also link to the research view for any watchlisted ticker.

**Acceptance Criteria:**
- Each ticker row in the screener results has a "Research" link/button navigating to `/research/{ticker}`
- Each ticker entry in the watchlist has a "Research" link/button navigating to `/research/{ticker}`
- Navigation preserves the user's position in the source list (back navigation returns to screener/watchlist at the same scroll position or equivalent)
- Research view URL is shareable/bookmarkable (ticker in URL path, not query param)
- BLG-FE-22 navigation model adopted — UX spec must be complete before this story is authored into sprint (confirmed via design gate)

---

## EPIC-02 — Pre-Trade Entry Checklist (PT-05)

**Maps to:** S2-03
**Sprint:** Sprint 2
**Owner:** Frontend Specifications & UX Documentation Owner
**Description:** Deliver the Pre-Trade Entry Checklist embedded in the Trade Plan form/flow. A structured checklist the user completes before opening a position, pre-populated from trade plan data where available, persisted as part of the Trade Plan record.

**Sequencing constraint:** Must not begin until EPIC-01 is merged. The checklist should contextually link to the research view for the same ticker.

---

### ST-05 — Entry checklist schema, component, and Trade Plan form integration

**EPIC:** EPIC-02
**Effort:** M
**Depends on:** EPIC-01 merged

**Description:** Define the entry checklist schema and build the checklist component. Embed the checklist into the Trade Plan creation/edit form. Checklist items cover: strategy signal confirmed, position size within heat limits, stop level defined, pre-trade research reviewed.

**Acceptance Criteria:**
- Checklist schema defined with minimum required items (at least: signal confirmed, heat limit check, stop defined, research reviewed)
- Checklist component renders in the Trade Plan creation and edit forms
- Each checklist item is a boolean (checked/unchecked) with label
- Checklist state is saved as part of the Trade Plan record (PUT /trade-plans/{id})
- Checklist items are not mandatory to check before saving a plan (advisory, not gate)
- Checklist is visible in Trade Plan detail view (read-only when plan is not in edit mode)

---

### ST-06 — Checklist pre-population from trade plan data and research view link

**EPIC:** EPIC-02
**Effort:** M
**Depends on:** ST-05

**Description:** Pre-populate checklist items where data is already available in the trade plan (e.g., stop level defined → pre-check "Stop level defined"). Add a "Review research" link from the checklist to `/research/{ticker}` for the plan's ticker, so users can navigate directly from checklist to research view.

**Acceptance Criteria:**
- Stop level defined in trade plan → "Stop level defined" checklist item pre-checked
- Risk/reward notes present in trade plan → "Pre-trade research reviewed" item pre-checked
- "Review research" link present in checklist, linking to `/research/{ticker}` for the plan's ticker
- Pre-population is advisory only — user can uncheck pre-populated items
- Existing checklist state is not overwritten on re-open if user has already modified it

---

## EPIC-03 — Governance & Process Hardening

**Maps to:** S2-04, S2-05
**Sprint:** Sprint 1
**Owner:** Head of Specs Team
**Description:** Clear 4 deferred v3.1 lessons_learnt actions (OA-02 to OA-05) as prompt patches, plus register 2 test scenario gaps from v3.1 delivery verification. All prompt patches require CLAUDE.md §6 compliance (version bump, OPERATIONAL_GUIDE update, prompt_change_log entry — all in same commit).

---

### ST-07 — sprint_planning_prompt.md STEP 0 main-branch verification

**EPIC:** EPIC-03
**Effort:** XS
**Source:** OA-02 / D-01 (v3.1 lessons_learnt_closure.md)

**Description:** Add a hard gate to sprint_planning_prompt.md STEP 0: verify the current branch is `main` before committing any sprint planning artefacts. If on a non-main branch, halt with instruction to checkout main. Prevents recurrence of orphaned sprint planning artefacts (v3.1 incident: sprint planning committed to exec/EPIC-02 branch).

**Acceptance Criteria:**
- sprint_planning_prompt.md STEP 0 includes branch check: `git branch --show-current` must equal `main`
- If not `main`: halt with message identifying the current branch and instructing checkout of main before re-invoking
- Version bumped in sprint_planning_prompt.md header
- OPERATIONAL_GUIDE.md §7 (or relevant Sprint Planning section) source prompt version updated
- prompt_change_log.md entry added (same commit)
- All four CLAUDE.md §6 checklist steps confirmed in QA evidence log

---

### ST-08 — execution_prompt.md STEP 5.1 deviations_filed enforcement

**EPIC:** EPIC-03
**Effort:** XS
**Source:** OA-03 / D-02 (v3.1 lessons_learnt_closure.md)

**Description:** Add a runtime check to execution_prompt.md STEP 5.1 sprint close: verify `deviations_filed = true` for all done items where a deviation was expected. If `deviations_filed = false` and no deviation record exists, auto-correct with a log entry and set flag to true with a note. Prevents ambiguous deviation state at cycle close.

**Acceptance Criteria:**
- execution_prompt.md STEP 5.1 checks `deviations_filed` for each `status: done` story
- If field is `false` and no deviation record exists: set to `true` with log note "No spec deviation found — field corrected at sprint close"
- If field is `false` and a deviation record does exist: surface as a process warning but do not auto-correct (requires human review)
- Version bumped in execution_prompt.md header
- OPERATIONAL_GUIDE.md execution section source prompt version updated
- prompt_change_log.md entry added (same commit)
- All four CLAUDE.md §6 checklist steps confirmed in QA evidence log

---

### ST-09 — execution_prompt.md §3.1.A test_scenarios post-story advisory

**EPIC:** EPIC-03
**Effort:** XS
**Source:** OA-04 / D-03 (v3.1 lessons_learnt_closure.md — recurrence from v3.0 TSG-v30-01)

**Description:** Add an explicit post-story advisory to execution_prompt.md §3.1.A: after any story that creates new test files, the engine must populate `test_scenarios` in `execution_state.json` before moving to the next story. This is a recurrence from v3.0 — the v3.1 delivery verification found the same gap for EPIC-01 and EPIC-03.

**Acceptance Criteria:**
- execution_prompt.md §3.1.A includes a post-story step: "If this story created test files, populate `test_scenarios` in `execution_state.json` now before moving to next story"
- Advisory is explicit and named — not embedded in general notes
- Version bumped in execution_prompt.md header (may be combined with ST-08 if in same commit — both story IDs must appear in commit message per CLAUDE.md governance non-negotiables)
- OPERATIONAL_GUIDE.md updated accordingly
- prompt_change_log.md entry added (same commit)
- All four CLAUDE.md §6 checklist steps confirmed in QA evidence log

---

### ST-10 — Playwright waitFor pattern — test authoring standard

**EPIC:** EPIC-03
**Effort:** XS
**Source:** OA-05 / D-04 (v3.1 lessons_learnt_closure.md — carry-forward from v3.0 CF-03)

**Description:** Adopt the Playwright `waitFor` pattern in place of `networkidle` for CI stability. Document the standard in execution_prompt.md (or a referenced spec) and update any existing Playwright tests that use `networkidle` to use `waitFor` instead.

**Acceptance Criteria:**
- execution_prompt.md references the `waitFor` pattern as the standard for Playwright test authoring (not `networkidle`)
- All existing Playwright test files scanned for `networkidle` usage; any found replaced with appropriate `waitFor` pattern
- Version bumped in execution_prompt.md header (may be combined with ST-08/ST-09 if in same commit)
- OPERATIONAL_GUIDE.md updated accordingly
- prompt_change_log.md entry added (same commit)
- All four CLAUDE.md §6 checklist steps confirmed in QA evidence log

---

### ST-11 — Trade Plan domain test scenario registration (TEST-GAP-EPIC-01)

**EPIC:** EPIC-03
**Effort:** S
**Source:** TEST-GAP-EPIC-01 (v3.1 delivery verification backlog item)

**Description:** Verify and register Trade Plan domain test scenarios in execution_state.json. `tests/e2e/trade-plan.spec.js` (SC-TP-01 to SC-TP-07) was created in EPIC-01 delivery but not registered in `execution_state.json test_scenarios`. QA & Testing Owner to verify coverage completeness and register all Trade Plan test scenarios.

**Acceptance Criteria:**
- `tests/e2e/trade-plan.spec.js` test file exists and is runnable
- All SC-TP-01 to SC-TP-07 scenarios (or current count) registered in execution_state.json `test_scenarios` field
- Backend CRUD integration tests for `/trade-plans` endpoints reviewed — if gaps exist, new tests authored and registered
- TEST-GAP-EPIC-01 backlog item can be marked complete after this story ships
- No regression in existing test pass rate

---

### ST-12 — Earnings Calendar and UK screener test registration (TEST-GAP-EPIC-03)

**EPIC:** EPIC-03
**Effort:** S
**Source:** TEST-GAP-EPIC-03 (v3.1 delivery verification backlog item)

**Description:** Verify and register Earnings Calendar and UK screener suffix test scenarios. `tests/e2e/earnings-calendar.spec.js` (SC-EARN-01 to SC-EARN-09) and `tests/e2e/screener-uk-suffix.spec.js` (SC-UK-01 to SC-UK-04) were created during EPIC-03 delivery but not registered in execution_state.json.

**Acceptance Criteria:**
- Both test files exist and are runnable in CI
- SC-EARN-01 to SC-EARN-09 and SC-UK-01 to SC-UK-04 registered in execution_state.json `test_scenarios`
- TEST-GAP-EPIC-03 backlog item can be marked complete after this story ships
- No regression in existing test pass rate

---

## EPIC-04 — Documentation, Security & Backlog Clearance

**Maps to:** S2-06
**Sprint:** Sprint 2
**Owner:** PMO Lead + Cybersecurity & Trust Lead
**Description:** Clear 5 outstanding backlog items in documentation and security domains. BLG-GOV-11 is on its 3rd consecutive deferral and is mandatory this cycle. BLG-FE-21 depends on BLG-FE-16; sequence ST-14 after ST-13 within the sprint.

---

### ST-13 — React component inventory (BLG-FE-16)

**EPIC:** EPIC-04
**Effort:** M
**Source:** BLG-FE-16

**Description:** Catalogue all existing React UI components in the application. Produce a reference inventory document covering each component's purpose, props summary, variants, and usage locations. Identify duplication or inconsistency.

**Acceptance Criteria:**
- Component inventory document created (e.g., `docs/frontend/component_inventory.md`)
- All existing UI components included: purpose, props summary, variants, usage locations
- Duplication or reuse opportunities noted
- Document usable as a starting reference for Arc 2 UI development
- BLG-FE-16 backlog item marked complete

---

### ST-14 — Design system document (BLG-FE-21)

**EPIC:** EPIC-04
**Effort:** M
**Depends on:** ST-13
**Source:** BLG-FE-21

**Description:** Document the implicit design system: colour palette, typography scale, spacing tokens, icon conventions. Capture current patterns as-is (not aspirational). Coordinate with component inventory (ST-13) — sequence after ST-13.

**Acceptance Criteria:**
- Design system document created (e.g., `docs/frontend/design_system.md`)
- Covers: colour palette, typography scale, spacing conventions, icon set/usage
- Each pattern entry includes current usage and any known inconsistencies
- Document cross-references component inventory (ST-13 output)
- BLG-FE-21 backlog item marked complete

---

### ST-15 — Alpaca credential audit and rotation policy (BLG-SEC-05)

**EPIC:** EPIC-04
**Effort:** S
**Source:** BLG-SEC-05

**Description:** Create a credential inventory and rotation policy for all production API credentials. Document all credentials (Alpaca, Anthropic, others), storage location, last rotation, dependencies. Define rotation frequency, step-by-step rotation procedure for Alpaca key, validation after rotation, and incident response steps.

**Acceptance Criteria:**
- Credential inventory document created (e.g., `docs/operations/credential_policy.md`)
- All production API credentials listed: storage location, last rotation date, system dependencies
- Rotation policy: frequency guidance, step-by-step Alpaca key rotation procedure, validation steps
- Incident response steps documented (rotate, validate, check audit logs)
- BLG-SEC-05 backlog item marked complete

---

### ST-16 — External API dependency risk register (BLG-GOV-18)

**EPIC:** EPIC-04
**Effort:** S
**Source:** BLG-GOV-18

**Description:** Create a lightweight external API dependency risk register covering Alpaca, Yahoo Finance, and Anthropic Claude. Document endpoints used, reliability record, known failure modes, fallback status, and API tier/plan.

**Acceptance Criteria:**
- Risk register document created (e.g., `docs/operations/external_api_risk_register.md`)
- Covers all production external API dependencies: Alpaca, Yahoo Finance, Anthropic
- Each entry: endpoints used, current status, known failure modes, fallback behaviour, renewal/tier info
- Register referenced in run_manifest.md template for future rebalances (add note to run_manifest template or OPERATIONAL_GUIDE)
- BLG-GOV-18 backlog item marked complete

---

### ST-17 — Cycle artefact inventory and maintenance review (BLG-GOV-11)

**EPIC:** EPIC-04
**Effort:** M
**Source:** BLG-GOV-11 (3rd consecutive deferral — mandatory)

**Description:** Produce a consolidated inventory of documents across all closed cycle directories (`claude/cycles/`). Categorise by type, document expected lifecycle (point-in-time vs living), identify maintenance gaps. Produce a reference document or update OPERATIONAL_GUIDE with artefact lifecycle model.

**Acceptance Criteria:**
- Consolidated artefact inventory covers all closed cycles in `claude/cycles/`
- Each document type has a documented lifecycle (point-in-time vs. maintained)
- Maintenance gaps identified; each either resolved or filed as a follow-up backlog item
- Reference document or OPERATIONAL_GUIDE section added
- BLG-GOV-11 backlog item marked complete
