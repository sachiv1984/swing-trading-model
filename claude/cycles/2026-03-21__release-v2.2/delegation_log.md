**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-03-23
**Cycle:** 2026-03-21__release-v2.2

---

# Delegation Log — 2026-03-21__release-v2.2

*Append-only. Do not edit previous entries.*

---

## DEL-20260322-01 — ST-01: API Key Authentication for Render Deployment (Spec Phase)

**Date:** 2026-03-22
**Assigned To:** Head of Specs Team
**Classification:** delegated_decision (reclassified from delegated_backend)
**GitHub Issue:** #118
**Branch:** exec/2026-03-21__release-v2.2/EPIC-01
**Status:** Resolved — 2026-03-23

**Resolution:** conventions.md §1 authored (v1.1) and approved by Head of Specs Team (agent-mediated sign-off). ST-01 reclassified to delegated_backend and reassigned to Head of Engineering via DEL-20260323-01.

**Reason for delegation:**
conventions.md §1 explicitly states authentication is "out of scope" — no lockable spec exists for X-API-Key auth. Per execution_prompt §5 rule, a delegated_backend item with no lockable spec must be reclassified to delegated_decision and surfaced to Head of Specs Team.

**Decision required:**
Author a canonical spec section for X-API-Key authentication. Options:
1. Update `docs/specs/api_contracts/conventions.md` §1 to document the X-API-Key scheme, 401 envelope, and exemption list (e.g. GET /health, redirect endpoints).
2. Create a new `docs/specs/api_contracts/security_endpoints.md` or `auth_conventions.md`.

Once spec is locked and marked Canonical, re-classify ST-01 to `delegated_backend` and delegate implementation to Head of Engineering.

**Unblock criteria:**
- Canonical spec section for X-API-Key authentication authored and status set to Canonical
- spec_references field populated in execution_state.json for ST-01
- Head of Engineering assigned implementation

**Commit format when complete:** `[EPIC-01][ST-01] <description>`
**SLA:** 24 hours (lifecycle decision)

---

## DEL-20260323-01 — ST-01: API Key Authentication for Render Deployment (Implementation)

**Date:** 2026-03-23
**Assigned To:** Head of Engineering
**Classification:** delegated_backend
**GitHub Issue:** #118
**Branch:** exec/2026-03-21__release-v2.2/EPIC-01
**Status:** Implementation complete — pending DoQ sign-off
**Supersedes:** DEL-20260322-01 (spec phase — resolved)

**Locked spec:** `docs/specs/api_contracts/conventions.md §1` (v1.1, Canonical)

**Implementation commit:** `43be2ef` — 2026-03-23

**Work completed:**
- FastAPI middleware added to `backend/main.py`: validates `X-API-Key` against `API_KEY` env var; returns `401 {"status":"error","message":"Unauthorized"}` on missing/invalid; exempts `GET /health`
- `src/api/base44Client.js` `doFetch` updated: `X-API-Key` header added from `REACT_APP_API_KEY` env var
- `apiFetch()` helper exported from `base44Client.js` for pages/components using raw `fetch()` calls
- All raw `fetch()` calls migrated to `apiFetch()`: `Dashboard.js` (3), `TradeHistory.js` (2), `Signals.js` (2), `Watchlist.js` (1), `WatchlistModal.js` (3), `SystemStatus.js` (3), `Reports.js` (3)
- `openapi.yaml`: `ApiKey` description cleaned; `GET /health` `security: []` exemption added; global `security:` block confirmed present
- All existing tests pass (19 passed, 13 pre-existing skips)

**Pending:** DoQ sign-off: (a) 401 path tested on staging; (b) `REACT_APP_API_KEY` env var set in Render dashboard confirmed; (c) no endpoint left unprotected

**Original scope (for reference):**

Implement X-API-Key authentication per `conventions.md §1`. The spec is now locked.

**Backend tasks:**
1. Add FastAPI middleware (or dependency injection) that reads `API_KEY` from environment and validates the `X-API-Key` request header on all incoming requests.
2. Return HTTP 401 with `{"status": "error", "message": "Unauthorized"}` on missing or invalid key — per conventions.md §1.3 and §13.
3. Exempt `GET /health` — no auth check required for that path.
4. All existing tests must pass (AC-4).

**Frontend tasks:**
5. Read `REACT_APP_API_KEY` from environment and include as `X-API-Key` header on all API calls via the shared API wrapper (not per-component — per conventions.md §1.2).

**OpenAPI tasks (same commit as implementation):**
6. Add `security: []` path-level override on `GET /health` in `docs/reference/openapi.yaml` to mark it exempt.
7. Remove `description: "API key for authentication (future use)"` from the `ApiKey` securityScheme — replace with `"API key required for all non-exempt endpoints. Passed as X-API-Key header."`.

**DoQ requirements (AC-6):**
- (a) 401 path tested (unit or integration test)
- (b) Frontend env-var wiring confirmed via code review
- (c) No endpoint left unprotected (code review or automated check)

**Commit format:** `[EPIC-01][ST-01] Add X-API-Key authentication middleware and frontend env-var wiring`
**Unblock criteria:** All 7 tasks complete; AC-1 through AC-6 verified; DoQ sign-off obtained.

---

## DEL-20260322-02 — ST-03: Alert Scheduling Design

**Date:** 2026-03-22
**Assigned To:** Product Owner
**Classification:** delegated_decision
**GitHub Issue:** #120
**Branch:** exec/2026-03-21__release-v2.2/EPIC-02
**Status:** Resolved — 2026-03-23

**Resolution:** Product Owner made all four decisions (A–D). Challenger review completed: 4 must-answer challenges resolved, 3 worth-noting items acknowledged and recorded. Decision document authored at `docs/product/decisions/decisions--2026-03-21__release-v2.2.md §ST-03 Execution Decisions`. ST-04 and ST-05 are now unblocked.

**Decision required:**
Product Owner must document the following alert scheduling decisions:
(a) Evaluation frequency — e.g. daily at market close, on-demand only, or external cron
(b) Cooldown policy — for stop_loss_approach and grace_period_warning alert types
(c) Source of truth for market_regime_change trigger
(d) Preferred trigger mechanism — external cron, Render cron job, or other

Decisions must be recorded in `docs/product/decisions/` or as a spec update in `docs/specs/` (alerts_endpoints.md or new scheduling decisions doc).

**Unblock criteria:** AC 1–4 of ST-03 all complete. ST-04 and ST-05 may not begin until this item is unblocked.
**SLA:** 72 hours (strategy decision)

---

## DEL-20260322-03 — ST-09: Execute Notification Scenarios on Staging

**Date:** 2026-03-22
**Assigned To:** QA & Testing Owner
**Classification:** delegated_qa
**GitHub Issue:** #126
**Branch:** exec/2026-03-21__release-v2.2/EPIC-04
**Status:** Pending

**What is needed:**
Execute SC-NOTIF-01 through SC-NOTIF-08 from `docs/testing/notifications_scenarios.md` on staging. Record pass/fail results in `claude/cycles/2026-03-21__release-v2.2/qa_evidence_EPIC-04.md`.

3 of 8 scenarios (stop_loss_approach, grace_period_warning, market_regime_change) require open positions to trigger — partial execution acceptable, blocked scenarios must be documented with: scenario ID, blocker, path to resolution.

**Commit format:** `[EPIC-04][ST-09] Execute notification test scenarios — staging results`
**Unblock criteria:** All 8 scenarios attempted; results recorded; Director of Quality sign-off on evidence record.

---

## DEL-20260322-04 — ST-10: Create Watchlist Test Scenarios

**Date:** 2026-03-22
**Assigned To:** QA & Testing Owner
**Classification:** delegated_qa
**GitHub Issue:** #127
**Branch:** exec/2026-03-21__release-v2.2/EPIC-04
**Status:** Pending

**What is needed:**
Create `docs/testing/watchlist_scenarios.md` covering SC-WATCH-01 through SC-WATCH-06. Each scenario must include: preconditions, steps, expected result.

SC-WATCH-06 must explicitly reference the deferred AC-6 from ST-10 (v2.1) DoQ sign-off as the source requirement.

**Commit format:** `[EPIC-04][ST-10] Create watchlist test scenarios SC-WATCH-01 through SC-WATCH-06`
**Unblock criteria:** File created; all 6 scenarios have full structure; SC-WATCH-06 cross-references v2.1 deferred AC; Director of Quality sign-off.

---

## DEL-20260322-05 — ST-11: Test Automation Readiness Assessment

**Date:** 2026-03-22
**Assigned To:** QA & Testing Owner
**Classification:** delegated_qa
**GitHub Issue:** #128
**Branch:** exec/2026-03-21__release-v2.2/EPIC-04
**Status:** Pending

**What is needed:**
Produce a readiness assessment document in `docs/testing/` covering:
- Current automation coverage quantified (% endpoints with integration tests)
- Map to BLG-QA-01 (Playwright E2E, deferred to v2.3)
- Recommended sequencing for BLG-QA-01 and other automation investments

**Commit format:** `[EPIC-04][ST-11] Add test automation readiness assessment`
**Unblock criteria:** Document produced; coverage quantified; sequencing confirmed; Director of Quality sign-off. Should complete before ST-12.

---

## DEL-20260322-06 — ST-12: Spec-to-Test Traceability Matrix

**Date:** 2026-03-22
**Assigned To:** Director of Quality (with Head of Specs Team co-sign)
**Classification:** delegated_qa
**GitHub Issue:** #129
**Branch:** exec/2026-03-21__release-v2.2/EPIC-04
**Status:** Pending

**What is needed:**
Create a spec-to-test traceability matrix for at least 3 canonical specs (alert rules, portfolio, positions recommended). For each AC in covered specs: map to ≥1 scenario ID, or flag as "No scenario — gap." Gap entries must be added to TEST-GAP tracking.

Gated on ST-11 completion. Target: Sprint 3.

**Commit format:** `[EPIC-04][ST-12] Add spec-to-test traceability matrix`
**Unblock criteria:** Matrix covers ≥3 specs; each AC mapped or flagged; gaps in TEST-GAP tracking; Director of Quality + Head of Specs Team sign-off.

---

## DEL-20260322-07 — ST-13: Roadmap Engine Provisional-Target Field

**Date:** 2026-03-22
**Assigned To:** Head of Specs Team
**Classification:** delegated_decision
**GitHub Issue:** #130
**Branch:** exec/2026-03-21__release-v2.2/EPIC-05
**Status:** Pending

**What is needed:**
Modify the following files per AC 1–3:
1. `claude/system/roadmap_prompt.md` STEP 9 — add Provisional-Target field requirement on new backlog items
2. `claude/system/shared_standards.md` — document Provisional-Target field format and horizon-to-release mapping
3. `claude/system/release_planning_prompt.md` STEP 1 — read Provisional-Target as a candidate prioritisation input

**Mandatory for each modified file (CLAUDE.md §6):**
(a) Version bumped; (b) OPERATIONAL_GUIDE §14 updated; (c) phase section source prompt header updated; (d) `prompt_change_log.md` entry added — all in same commit.

**Commit format:** `[EPIC-05][ST-13] Add Provisional-Target field to roadmap → backlog promotion`
**Unblock criteria:** All 3 files updated; §6 checklist applied to each; external DoQ review of checklist compliance.
**SLA:** 72 hours (governance content decision)

---

## DEL-20260322-08 — ST-14: Release Planning Load scored_initiatives.md

**Date:** 2026-03-22
**Assigned To:** Head of Specs Team
**Classification:** delegated_decision
**GitHub Issue:** #131
**Branch:** exec/2026-03-21__release-v2.2/EPIC-05
**Status:** Pending

**What is needed:**
Modify per AC 1–3:
1. `claude/system/release_planning_prompt.md` STEP 0 — add scored_initiatives.md to load list
2. `claude/system/release_planning_prompt.md` STEP 4 — reference effort bands from scored_initiatives.md; fall back to STEP 4 estimate if absent
3. `claude/system/shared_standards.md` — document the handoff contract between roadmap engine and release planning engine

CLAUDE.md §6 checklist required for all modified files.

**Commit format:** `[EPIC-05][ST-14] Load scored_initiatives.md in release planning for effort band handoff`
**Unblock criteria:** All changes per AC 1–3; §6 checklist applied; Head of Specs Team sign-off.
**SLA:** 72 hours (governance content decision)

---

## DEL-20260322-09 — ST-15: Structured Lessons Learnt Carry-Forward Block

**Date:** 2026-03-22
**Assigned To:** Head of Specs Team
**Classification:** delegated_decision
**GitHub Issue:** #132
**Branch:** exec/2026-03-21__release-v2.2/EPIC-05
**Status:** Pending

**What is needed:**
Modify per AC 1–3:
1. `claude/system/shared_standards.md` — document Carry-Forward section schema (3–5 items: observation, implication, which engine should act)
2. `claude/system/roadmap_prompt.md`, `release_planning_prompt.md`, `sprint_planning_prompt.md` STEP 0 — add carry-forward read-and-acknowledge step
3. `claude/system/post_ship_closure.md` — add Carry-Forward section write as mandatory STEP output

CLAUDE.md §6 checklist required for ALL modified files (largest change set in EPIC-05).

**Commit format:** `[EPIC-05][ST-15] Add structured lessons learnt carry-forward block to all engines`
**Unblock criteria:** All changes per AC 1–3; §6 checklist applied to each modified file; Head of Specs Team sign-off.
**SLA:** 72 hours (governance content decision)

---

## DEL-20260323-02 — ST-04: Alert Threshold Customisation

**Date:** 2026-03-23
**Assigned To:** Base44 Frontend Prompt Owner
**Classification:** delegated_frontend
**GitHub Issue:** #121
**Branch:** exec/2026-03-21__release-v2.2/EPIC-02
**Target branch:** `exec/2026-03-21__release-v2.2/EPIC-02`
**Status:** Pending

**Gate cleared:** ST-03 complete (2026-03-23). ST-04 and ST-05 are now unblocked.

**Locked specs:**
- Frontend: `docs/specs/frontend/pages/notifications.md` v0.2 §Section 2 (Alert Rule Thresholds)
- Backend contract: `docs/specs/api_contracts/alerts_endpoints.md` v0.2 (PATCH /alerts/rules/{rule_id} exists; GET /alerts/rules exists)

---

### Base44 Prompt Draft — ST-04: Alert Threshold Customisation

---

**1. Context — what component is being changed**

The file is `src/components/Notifications.js` (or the component that renders `/notifications/preferences`). This component currently renders two things: (1) a sub-navigation tab bar with "Feed" and "Preferences" tabs, and (2) the Notification Preferences page at `/notifications/preferences`. The Preferences page currently has one section: **Section 1 — Email Preferences**, which shows per-alert-type email toggles persisted via `PATCH /notifications/preferences`.

We are adding a new **Section 2 — Alert Thresholds** below Section 1, and also adding a "History" tab to the sub-nav (the History tab itself links to `/notifications/history` — that page is a separate story; add the tab/link only, not the page content).

---

**2. The change — what needs to be added**

Add the following to the `/notifications/preferences` page (rendered below the existing email preferences section):

**Section heading:** "Alert Thresholds" (sub-heading `h2` or equivalent section header in the design system)

On mount, call `GET /alerts/rules` to load the configured alert rules. Display one row per rule returned.

**Alert Rule List row layout:**
- Bold alert type name (mapped from API value to display label — see mapping below)
- Muted secondary text below name:
  - For `stop_loss_approach` with `threshold_percent = 5.0` (the default): `"Within 5% of stop (default)"`
  - For `stop_loss_approach` with a custom `threshold_percent` value: `"Within N% of stop"` (where N is the actual value)
  - For all other types (`grace_period_warning`, `market_regime_change`, `daily_portfolio_summary`): do **not** show any threshold text — these types have no configurable threshold
- **Edit button** (inline, right-aligned): only shown for `stop_loss_approach`

**Alert type display labels:**

| API value | Display label |
|-----------|--------------|
| `stop_loss_approach` | Stop Loss Approach |
| `grace_period_warning` | Grace Period Warning |
| `market_regime_change` | Market Regime Change |
| `daily_portfolio_summary` | Daily Portfolio Summary |

**Empty state (if `GET /alerts/rules` returns an empty array):**
- Icon: bell with plus
- Heading: "No alert rules configured."
- Body: "Add an alert rule to receive notifications."
- CTA button: "Add alert rule" — opens the create form (see form spec below)

**Edit / Create form:**

Clicking "Edit" on a `stop_loss_approach` row, or "Add alert rule" on the empty state, opens an **inline expanded form** below the row (or section, if empty state). The form does **not** navigate away.

Form fields:
- **Alert type** (display only when editing — shows the alert type name; select dropdown when creating with options: Stop Loss Approach, Grace Period Warning, Market Regime Change, Daily Portfolio Summary)
- **Threshold** (rendered only for `stop_loss_approach`):
  - Label: `"Notify when within ___ % of stop"`
  - Input type: number, decimal (1 decimal place precision)
  - Placeholder: current default value (e.g. `"5"`)
  - Help text below input: `"Leave blank to use the default (5%)."`
  - Pre-filled with the existing `threshold_percent` value when editing

**Threshold input validation (inline, on change):**

| Condition | Error message |
|-----------|--------------|
| Non-numeric value | "Please enter a valid number." |
| Value ≤ 0 | "Threshold must be greater than 0." |
| Value > 50 | "Threshold cannot exceed 50%." |
| Blank / empty | No error — treated as "use default" (5%) |

Display the error message directly below the input field. The Save button is disabled while validation errors are present.

Form actions:
- **Save** button: calls `PATCH /alerts/rules/{rule_id}` with `{ "threshold_percent": <value or 5.0 if blank> }`
  - On success: close the inline form; refresh the rules list; updated threshold shows in the list row
  - On error: inline error above Save button: `"Failed to save alert rule. Please try again."`
- **Cancel** button: closes the form without saving; no API call

---

**3. API contract**

**GET /alerts/rules**
- Method: `GET`
- Path: `/alerts/rules`
- No query parameters
- Response (200): `{ "status": "ok", "data": [ { "id": "<uuid>", "type": "stop_loss_approach" | "grace_period_warning" | "market_regime_change" | "daily_portfolio_summary", "enabled": true|false, "threshold_percent": <float or null>, "created_at": "<ISO>", "updated_at": "<ISO>" } ] }`
- `threshold_percent`: float for `stop_loss_approach`, `null` for all other types
- Default values on first use (seeded by backend): `stop_loss_approach` enabled=true threshold_percent=5.0; all others enabled=true threshold_percent=null

**PATCH /alerts/rules/{rule_id}**
- Method: `PATCH`
- Path: `/alerts/rules/{rule_id}` — `rule_id` is the UUID `id` field from the GET response
- Request body: `{ "threshold_percent": <float> }` — at least one field must be present
- `threshold_percent` must be > 0 and ≤ 100 (frontend validates ≤ 50 per spec)
- Response (200): updated alert rule object (same shape as GET response items)
- Error (400): threshold out of range or no fields provided
- Error (404): rule_id not found

Use the `apiFetch` wrapper (imported from `src/api/base44Client.js`) for all API calls. This wrapper automatically adds the `X-API-Key` header. Do not call `fetch` directly.

---

**4. Behaviour rules**

- Load `GET /alerts/rules` on component mount (alongside the existing `GET /notifications/preferences` call; both can load in parallel with `Promise.all`).
- Loading state for the thresholds section: show 4 skeleton rows at standard row height while the rules load.
- Error state (load failure): inline error panel below the "Alert Thresholds" heading: `"Unable to load alert rules. Please refresh."`
- Only one edit form should be open at a time. Opening one form closes any other open form.
- The form pre-fills the existing `threshold_percent` when editing. If the existing value equals the backend default (5.0) the pre-fill still shows 5.0 (not blank).
- A blank threshold field is accepted as "use default (5%)" — on submit, pass `threshold_percent: 5.0` to the API.
- After a successful save, re-call `GET /alerts/rules` to refresh the displayed values (do not update locally without re-fetch).
- The threshold display in the list should reflect the current API value, not a locally-tracked state.

---

**5. Non-functional rules**

- Do NOT modify the existing email preferences section (Section 1). Its behaviour, layout, and state management must remain identical.
- Do NOT implement the `/notifications/history` page content. The History tab in the sub-nav should appear as a navigation link only (pointing to `/notifications/history`). The page rendering for that route is a separate story.
- Do NOT change the routing logic — only add the History tab to the existing sub-nav component.
- The existing `GET /notifications` feed functionality must not be affected.
- All API calls must use the shared `apiFetch` wrapper from `src/api/base44Client.js`.
- Do not hardcode API base URLs.

---

**6. Expected outcome**

Return the complete updated `Notifications.js` (or whichever file(s) implement the `/notifications/preferences` page and sub-nav) with:
1. "Alert Thresholds" section added below email preferences on the Preferences tab
2. Alert rule list with per-row threshold display and edit button (for `stop_loss_approach`)
3. Inline edit/create form with validation
4. Loading, empty, and error states for the thresholds section
5. "History" tab added to the sub-nav (link only — no page content)

---

**Commit format when complete:** `[EPIC-02][ST-04] Add alert threshold customisation to preferences page`
**Unblock criteria:** All 6 AC from stage4_backlog_slice.md ST-04 verified; threshold customisation confirmed functional; DoQ sign-off.
**SLA:** 72 hours

---

## DEL-20260323-03 — ST-05: Alert History Table

**Date:** 2026-03-23
**Assigned To:** Base44 Frontend Prompt Owner (frontend) + Head of Engineering (backend: alert_evaluations table + GET /alerts/history endpoint)
**Classification:** delegated_frontend
**GitHub Issue:** #122
**Branch:** exec/2026-03-21__release-v2.2/EPIC-02
**Target branch:** `exec/2026-03-21__release-v2.2/EPIC-02`
**Status:** Pending

**Gate cleared:** ST-03 complete (2026-03-23). ST-04 and ST-05 are now unblocked.

**Backend prerequisite (Head of Engineering — same commit):**

Before the frontend can be implemented, the backend must:
1. Create the `alert_evaluations` table (migration with down migration):
   - `id` UUID PK
   - `evaluation_timestamp` ISO 8601 timestamp
   - `rule_type` string (one of the four alert type keys)
   - `symbol` string nullable (null for non-position-specific types)
   - `triggered` boolean
   - `notification_sent` boolean
   - `values_compared` JSONB (key-value map of the comparison values used)
2. Persist a record per rule evaluated in `POST /alerts/evaluate`
3. Implement `GET /alerts/history` endpoint (contract below)
4. Update `docs/specs/api_contracts/alerts_endpoints.md` with `GET /alerts/history` section in the same commit
5. Update `docs/reference/openapi.yaml` with the new endpoint in the same commit

**Locked specs:**
- Frontend: `docs/specs/frontend/pages/notifications.md` v0.2 §Page 3 (Alert History)
- Backend contract (to be authored by Head of Engineering per AC-5): `docs/specs/api_contracts/alerts_endpoints.md` — add `GET /alerts/history` section
- Data model: ST-05 AC-1 fields (see above)

---

### Base44 Prompt Draft — ST-05: Alert History Table

---

**1. Context — what component is being changed**

The file is `src/components/Notifications.js` (or the component rendering the `/notifications` routes). This component renders:
- Sub-navigation with tabs: "Feed" (`/notifications`) and "Preferences" (`/notifications/preferences`)
- The notification feed page at `/notifications`
- The preferences page at `/notifications/preferences`

We are adding a third tab and page: **"History"** at `/notifications/history`. This page shows a table of all alert rule evaluations recorded by the system.

Note: If ST-04 has already been implemented (adding the "History" tab link to the sub-nav), the link already exists — do not duplicate it. If not yet present, add it.

---

**2. The change — what needs to be added**

Add a new page at `/notifications/history` (the "Alert History" page) with the following structure:

**Page header:**
- H1: `"Alert History"`
- Subtitle: `"A log of every alert rule evaluation by the system."`

**Controls (above the table):**
- Right-aligned: filter dropdown
  - Label: `"Filter by type:"`
  - Options: `All types` (default), `Stop Loss Approach`, `Grace Period Warning`, `Market Regime Change`, `Daily Portfolio Summary`
  - Selecting an option filters the table rows to only show that rule type
  - Selecting "All types" clears the filter

**Alert History Table columns:**

| Column header | Source field | Format |
|--------------|-------------|--------|
| Date / Time | `evaluation_timestamp` | `YYYY-MM-DD HH:mm` in local time; full ISO 8601 on hover |
| Alert Type | `rule_type` | Mapped to display label (see mapping) |
| Symbol | `symbol` | Uppercase ticker string; `—` (em dash) if null |
| Triggered | `triggered` | `true` → amber badge with text "Yes"; `false` → grey badge with text "No" |
| Notified | `notification_sent` | `true` → green badge with text "Yes"; `false` → grey badge with text "No" |
| Values | `values_compared` | Compact one-line summary of the key-value map (truncated if long) |

**Rule type display labels:**

| API value | Display label |
|-----------|--------------|
| `stop_loss_approach` | Stop Loss Approach |
| `grace_period_warning` | Grace Period Warning |
| `market_regime_change` | Market Regime Change |
| `daily_portfolio_summary` | Daily Portfolio Summary |
| Unknown value | Show the raw API value as fallback |

**Row expand:**
Clicking any table row expands it inline (not a modal) to show the full `values_compared` map as a formatted key–value list. The expanded values replace the truncated "Values" cell display. Example format:
```
stop_price:        $42.10
current_price:     $43.50
gap_pct:           3.3%
threshold_pct:     5.0%
triggered:         Yes
notification_sent: Yes
```
Clicking the row again collapses it.

**Sort:**
- Default: newest first (descending `evaluation_timestamp`)
- The "Date / Time" column header is clickable to toggle sort direction (ascending / descending)
- Active sort direction indicated by an up/down arrow icon on the column header

**Pagination:**
- Initial load: call `GET /alerts/history?last_n_days=30` (last 30 days)
- If more records may exist: show a **"Load more"** button below the table
- "Load more" calls `GET /alerts/history?last_n_records=200` (or an offset approach if the API supports it)
- No infinite scroll — button only

**"History" tab in sub-nav:**
Add `"History"` as the third tab in the notifications sub-nav, pointing to `/notifications/history`. If ST-04 already added this tab, it should already be present — check before adding.

---

**3. API contract**

**GET /alerts/history**
- Method: `GET`
- Path: `/alerts/history`
- Query parameters:
  - `last_n_days` (integer, optional): return records from the last N days
  - `last_n_records` (integer, optional): return the last N records regardless of date
  - Default if neither provided: last 30 days
- Response (200):
```json
{
  "status": "ok",
  "data": {
    "evaluations": [
      {
        "id": "<uuid>",
        "evaluation_timestamp": "2026-03-21T16:30:00Z",
        "rule_type": "stop_loss_approach",
        "symbol": "AAPL",
        "triggered": true,
        "notification_sent": true,
        "values_compared": {
          "stop_price": 42.10,
          "current_price": 43.50,
          "gap_pct": 3.3,
          "threshold_pct": 5.0
        }
      }
    ],
    "total": 47
  }
}
```
- `symbol` is nullable (null for types not tied to a specific position)
- `values_compared` is a JSON object with arbitrary key–value pairs (backend-defined per rule type)
- `total` is the total number of records matching the query (used to determine whether "Load more" is available)

Use the `apiFetch` wrapper (imported from `src/api/base44Client.js`) for all API calls.

---

**4. Behaviour rules**

- Load `GET /alerts/history?last_n_days=30` on mount.
- Loading state: show 5 skeleton rows at standard table-row height.
- Empty state (no records, no filter applied):
  - Heading: `"No alert history yet."`
  - Body: `"Alert evaluations will appear here once the system has run."`
- Empty state (filter applied but no matches):
  - Body: `"No evaluations found for the selected alert type."`
  - "Clear filter" link that resets the dropdown to "All types"
- Error state (API failure): full-width error panel: `"Unable to load alert history. Please refresh."`
- "Load more" button is shown when `total > evaluations.length` (i.e. there may be more records). Hidden when all records are already loaded.
- The filter is applied client-side to the loaded records. It does not re-call the API.
- Row expand: only one row can be expanded at a time. Expanding a row collapses any previously expanded row.
- Format `evaluation_timestamp` in the user's local timezone for display; show full ISO 8601 on hover.

---

**5. Non-functional rules**

- Do NOT modify the notification feed page or preferences page.
- Do NOT change the existing sub-nav tabs "Feed" and "Preferences".
- All API calls must use `apiFetch` from `src/api/base44Client.js`.
- Do not hardcode API base URLs.
- The table is read-only — no delete, edit, or bulk actions.

---

**6. Expected outcome**

Return the complete updated `Notifications.js` (or separate page component `NotificationsHistory.js` if the routing structure benefits from it) with:
1. New `/notifications/history` route rendering the Alert History page
2. Alert history table with all columns, sort, filter, and row expand
3. "Load more" pagination
4. Loading, empty (both variants), and error states
5. "History" tab added to sub-nav (if not already added by ST-04)

---

**Commit format when complete:** `[EPIC-02][ST-05] Add alert history table and GET /alerts/history endpoint`
**Unblock criteria:** All 6 AC from stage4_backlog_slice.md ST-05 verified; history persists across evaluate calls; migration runs cleanly with down migration; DoQ sign-off.
**SLA:** 72 hours
