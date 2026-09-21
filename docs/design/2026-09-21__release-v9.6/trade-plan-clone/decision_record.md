**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-09-21__release-v9.6
**Story:** ST-01 (EPIC-01, BLG-FEAT-96)

# Decision Record — "Clone as New Plan" Action on the Trade Plans List

## 1. Problem

A trader planning a similar setup restarts from a blank form. `strategy_rules.md` §4 requires pre-entry planning, so friction here suppresses linked-plan volume (the SI-02 gate's input). The list (`trade_plan.md` §4.2) offers only "View" and "Edit".

## 2. Decision

### 2.1 Entry points

- **List row:** a **"Clone"** text link in the Actions column, after "View" / "Edit". Unlike "Edit", Clone is shown for **every** status including `abandoned` and `closed` — the setup of a dead plan is a legitimate template.
- **Detail view header:** a **"Clone"** secondary (outline) button beside the existing header actions (§7). Same visibility rule.
- `aria-label` on both: `"Clone {TICKER} plan"`.

### 2.2 Behaviour

Clone navigates to `/trade-plans/new?clone_from={plan_id}`. The form loads the source plan through the existing detail read and renders the ordinary creation form pre-populated. **Nothing is persisted until the user clicks "Save Trade Plan"** ("Cancel" discards, unchanged). No new endpoint.

A dismissal-free info banner sits above the form fields (`data-testid="clone-banner"`, `StandingAlert` Info tone, non-dismissible): `"Cloned from {TICKER} plan ({source created date}). Nothing is saved until you click Save Trade Plan."`

### 2.3 What is copied and what is not

| Copied (structural setup fields) | Reset / not copied |
|----------------------------------|--------------------|
| `ticker` (editable, as on any new form), `market` | `id`, `created_at`, `updated_at` — fresh on save |
| `setup_thesis`, `invalidation_condition` | `status` → **`draft`** (see §2.4) |
| `r_target` | `position_id` — **must not be copied** (would corrupt the SI-02 linked-plan count) |
| Tags (§5c) | Price-level fields (stop level, planned entry/stop prices) — date-specific and misleading on a new setup |
| Pre-Trade Checklist **template** (items only) | Checklist **completion state** — every item resets to unchecked |
| | Abandonment reason/timestamp, Setup Quality Score, AI thesis feedback state — derived/historical, recomputed on the new plan |

### 2.4 Status vocabulary correction

The sealed slice describes the clone as starting in `planned` status. **No `planned` status exists** — `trade_plans.status` is `draft | research_pending | research_complete | entry_conditions_set | active | closed | abandoned` (`data_model.md` §Trade Plan Lifecycle; `backend/database.py::ensure_trade_plans_extended_status`; `trade_plan.md` §9). The lifecycle's only entry state is `draft` (`[*] --> draft: POST /trade-plans`). The clone therefore starts as **`draft`**. Recorded as a post-gate correction in `stage4_backlog_slice_addendum.md`.

### 2.5 Failure handling

If the source plan cannot be loaded (deleted, network error) the form opens **blank** and a toast is shown: `"Couldn't load that plan to clone. Starting a blank plan."` — Warning severity, 6s (Toast Notification Timing standard, `design_system.md`).

### 2.6 Motion / timing

None. No animation, debounce or delay is introduced.

## 3. §13 Compliance

Pure client-side field copy of user-authored text. No AI-provider call is introduced or extended; the clone deliberately does **not** carry over AI thesis feedback state. §13 pre-check does not apply.

## 4. Frontend Spec Impact

`docs/specs/frontend/pages/trade_plan.md` v1.14 → v1.15: §2 route row, §4.2 Actions column, new §4.5 Clone as New Plan.

## 5. Testability (CLAUDE.md §2)

Observable ACs each need Playwright coverage: Clone opens `/trade-plans/new?clone_from=…` pre-populated; banner present; saved clone has `draft` status, fresh dates, `position_id` null; Clone present on an abandoned row.

## 6. Approval

Head of UX & Design: confirmed, 2026-09-21.
Product Owner: confirmed, 2026-09-21 (including the `planned` → `draft` correction).
