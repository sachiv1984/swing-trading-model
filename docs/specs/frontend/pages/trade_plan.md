**Owner:** Frontend Specifications & UX Documentation Owner
**Class:** Supporting Document (Class 2)
**Status:** Active
**Version:** 0.3
**Last Updated:** 2026-05-09
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md
**Design Source (v0.1):** docs/design/2026-04-29__release-v3.1/trade-plan/ux_spec.md (v3.1 — artefact reference only; file not present in repo)
**Design Source (v0.2 checklist):** docs/design/2026-05-05__release-v3.2/pre-trade-entry-checklist/ux_spec.md
**Design Source (v0.3 abandonment + badges):** docs/design/2026-05-09__release-v3.3/trade-plan-quick-wins/ux_spec.md §A, §B
**API contract:** docs/specs/api_contracts/trade_plan_endpoints.md

---

# trade_plan.md — Trade Plan

**Purpose:** The Trade Plan pages cover the trade plan list, creation/edit form, and detail view. Trade Plans capture the pre-trade rationale (ticker, stop level, risk/reward notes, entry checklist) for a prospective or active position. Introduced in v3.1 (PT-01); entry checklist added in v3.2 (PT-05).

---

## 1. Purpose and User Goals

Users should be able to:

- Create a trade plan before opening a position (pre-trade rationale capture)
- Record stop level, risk/reward notes, and complete the pre-trade entry checklist
- View all trade plans and their status
- Edit and update a trade plan as conditions evolve
- Navigate to the research view for the plan's ticker

---

## 2. Navigation and Routes

| Route | Purpose |
|-------|---------|
| `/trade-plans` | Trade plan list |
| `/trade-plans/new` | Create new trade plan (form) |
| `/trade-plans/new?ticker={ticker}` | Create new trade plan pre-populated with ticker |
| `/trade-plans/{id}` | Trade plan detail view |
| `/trade-plans/{id}/edit` | Edit trade plan |

- Top-level nav item: **"Trade Plans"**
- Page title (list): **"Trade Plans"**
- Page title (detail): **"{TICKER} — Trade Plan"**

---

## 3. API Reference

| Endpoint | Purpose |
|----------|---------|
| `GET /trade-plans` | List all trade plans (supports `?ticker={ticker}` filter) |
| `POST /trade-plans` | Create new trade plan |
| `GET /trade-plans/{id}` | Fetch single trade plan |
| `PUT /trade-plans/{id}` | Update trade plan (full replace) |
| `DELETE /trade-plans/{id}` | Delete trade plan |

Canonical contract: `docs/specs/api_contracts/trade_plan_endpoints.md`

---

## 4. Trade Plan List

### 4.1 Page Header

- H1: **"Trade Plans"**
- Right-aligned: **"+ New Trade Plan"** button (primary action)

### 4.2 List Layout

One card or row per trade plan. Default sort: most recently updated first. Abandoned plans shown with muted row styling (opacity 0.7).

| Column | Source | Notes |
|--------|--------|-------|
| Ticker | `ticker` | Uppercase |
| Status | `status` | Badge per §9 Status Badge Scheme |
| Stop Level | `stop_level` | Currency-formatted; `—` if null |
| Notes | `risk_reward_notes` | Truncated to ~60 chars |
| Updated | `updated_at` | Relative timestamp |
| Actions | — | "View" link + "Edit" link (Edit hidden for abandoned plans) |

### 4.3 Empty State

- Heading: **"No trade plans yet."**
- Body: "Create a trade plan before opening your next position."
- **"+ New Trade Plan"** button

### 4.4 Entry Points to Trade Plan Form

Per v3.1 design gate decision:
- Positions table: "Plan" button in Actions column
- Watchlist: "Plan" button in Actions column
- Research view: "Create Trade Plan" CTA (when no plan exists for the ticker)
- Direct URL: `/trade-plans/new`

---

## 5. Trade Plan Creation and Edit Form

### 5.1 Form Fields

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Ticker symbol | Text | Yes | Uppercase-enforced; read-only on edit |
| Market | Radio: UK / US | Yes | |
| Status | Select | Yes | Draft / Active / Closed (Abandoned is set via Abandon action — not in this dropdown) |
| Stop Level | Numeric | No | Positive decimal; native currency |
| Risk/Reward Notes | Textarea | No | Free text; used for pre-population of CHK-04 |
| Pre-Trade Checklist | Component | No | See §6 |

### 5.2 Actions (Form Footer)

- **"Save Trade Plan"** (primary) — `POST /trade-plans` (new) or `PUT /trade-plans/{id}` (edit)
- **"Cancel"** (secondary) — returns to previous page without saving

---

## 6. Pre-Trade Entry Checklist (v3.2 — PT-05)

> **§13 Compliance:** This feature has been reviewed and confirmed §13 compliant — see `docs/specs/compliance/pt05_entry_checklist_s13_review.md`. The system presents checklist items; the human confirms each condition; the system records the human-confirmed state. No automated condition evaluation or recommendation is generated. (ST-15, v3.3)

The checklist is embedded as a grouped section within the Trade Plan creation and edit forms, below the core plan fields.

### 6.1 Section Header

"Pre-Trade Checklist"

### 6.2 Checklist Items

| Item ID | Label | Pre-population |
|---------|-------|----------------|
| CHK-01 | Strategy signal confirmed | Never auto-checked |
| CHK-02 | Position size within heat limits | Never auto-checked |
| CHK-03 | Stop level defined | Auto-checked if `stop_level` is non-null |
| CHK-04 | Pre-trade research reviewed | Auto-checked if `risk_reward_notes` is non-null |

- Each item: checkbox + label
- All items visible regardless of check state
- Pre-population is advisory — user may uncheck any item
- Existing user-set state is not overwritten on re-open

### 6.3 "Review Research" Link

- Label: "Review research →"
- Target: `/research/{ticker}` for the plan's ticker
- Visible only when the plan has a ticker set
- Present in both creation and edit modes

### 6.4 Read-Only State (Detail View)

In the trade plan detail view (not editing):
- Checklist items shown as read-only indicators (no interactive checkboxes)
- "Review research" link remains active

### 6.5 Persistence

Checklist state stored as `checklist` array on the trade plan record. Submitted with `POST /trade-plans` and `PUT /trade-plans/{id}`.

---

## 7. Trade Plan Detail View

- Shows all plan fields in read-only layout
- Pre-trade checklist shown in read-only state (§6.4)
- Action buttons: **"Edit"** (primary) + **"Abandon"** (amber outlined — see §8) + **"Delete"** (destructive, with confirmation)
- **"Review research"** link present if ticker is set
- When `status = 'abandoned'`: "Abandon" and "Edit" buttons hidden; abandonment reason shown (see §8.3)

---

## 8. States

| State | Behaviour |
|-------|-----------|
| Loading (list) | Skeleton rows |
| Loading (detail/form) | Skeleton form fields |
| Error | Inline error message + Retry |
| Empty (list) | See §4.3 |

---

## 8. Trade Plan Abandonment (v3.3 — ST-17 BLG-FEAT-21)

**Design source:** docs/design/2026-05-09__release-v3.3/trade-plan-quick-wins/ux_spec.md §A

### 8.1 Trigger

"Abandon" action button shown in Trade Plan detail view below "Edit":
- Style: secondary, amber outlined (warning-adjacent — not primary; not red)
- Hidden when `status = 'active'` (linked open position; backend enforces with 400 guard)

### 8.2 Abandonment Modal

**Title:** "Abandon trade plan for {TICKER}?"

**Body text:** "This plan will be marked as abandoned. You will not be prompted to enter this position again based on this plan."

**Required field:** Abandonment reason (textarea, 3 rows, min 10 chars). Inline validation on blur. Confirmation button disabled until valid.

**Actions:**
- "Abandon Plan" (primary, amber) — submits `PUT /trade-plans/{id}` with `{status: 'abandoned', abandonment_reason: <text>}`
- "Cancel" (secondary) — closes modal; no change

### 8.3 Abandoned Plan Display

In the detail view when `status = 'abandoned'`:
- Status badge: Abandoned (red — §9)
- Read-only field below status: "Reason for abandoning: {abandonment_reason}"
- "Abandon" and "Edit" hidden; "Delete" remains
- List view row: muted styling (opacity 0.7)

---

## 9. Status Badge Scheme (v3.3 — ST-17 BLG-FE-30)

**Design source:** docs/design/2026-05-09__release-v3.3/trade-plan-quick-wins/ux_spec.md §B

Applied in Trade Plan List and Trade Plan Detail View:

| Status | Badge Label | Colour | Hex |
|--------|------------|--------|-----|
| `draft` | Draft | Grey | `#6B7280` |
| `research_pending` | Research Pending | Amber | `#D97706` |
| `research_complete` | Research Complete | Blue | `#2563EB` |
| `entry_conditions_set` | Entry Ready | Purple | `#7C3AED` |
| `active` | Active | Green | `#16A34A` |
| `closed` | Closed | Slate (muted) | `#94A3B8` |
| `abandoned` | Abandoned | Red | `#DC2626` |

All badges: filled pill, white text. Contrast ≥ 4.5:1 (WCAG AA) for all combinations.

---

## Known Deviations

| ID | Description | Priority | Status |
|----|-------------|----------|--------|
| DEV-01 | v3.1 design gate claimed creation of this spec at v0.1, but the file was not committed to the repository. Recovered at v3.2 design gate. | P2 | Resolved — file created at v3.2 design gate |

---

## Changelog

| Version | Date | Change |
|---------|------|--------|
| 0.3 | 2026-05-09 | v3.3 design gate — added §8 Trade Plan Abandonment (BLG-FEAT-21: abandon action, modal, abandoned display); added §9 Status Badge Scheme (BLG-FE-30: 7-state badge set including Abandoned). Design source: trade-plan-quick-wins/ux_spec.md §A, §B. Approved: Product Owner 2026-05-09. |
| 0.2 | 2026-05-05 | v3.2 design gate — added Pre-Trade Entry Checklist section (§6) for EPIC-02 (ST-05, ST-06). Design source: pre-trade-entry-checklist/ux_spec.md. Also: initial file creation (recovering v3.1 gap — trade_plan.md v0.1 was stated as created in v3.1 design gate but not committed). |
| 0.1 | 2026-04-29 | Initial spec intent — v3.1 design gate (ST-03 — Trade Plan creation flow + detail view). File not committed at the time; recovered at v3.2. |
