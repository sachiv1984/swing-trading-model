**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-11-03__release-v9.15
**Stories:** ST-01 (EPIC-01, BLG-FE-244)

# Decision Record — Pre-Entry Checks on Trade Entry

## 1. Problem

The `strategy_rules.md` §4.2 pre-entry checks run only on the Trade Plan form (`PreEntryValidationPanel` in `src/pages/TradePlan.js`). The three unplanned routes into Trade Entry (sidebar "Trade Entry", Positions "New Position", the `n` shortcut) run none of them, so an entry in a risk-off or unknown-regime market can be saved without the regime check ever being shown. The Strategy Rules & System Intent Owner confirmed on 2026-11-03 that §4.2 applies to every manual entry, planned or not, and that the checks are display-only.

## 2. Decision

### 2.1 When the panel shows

> **Superseded for the plan-linked rows (v9.16, ST-05, BLG-FE-271):** see `docs/design/2026-11-06__release-v9.16/plan-linked-pre-entry-checks/decision_record.md`. A linked plan's snapshot now hides the panel only when it is less than 24 hours old and either passed or had its warnings acknowledged on the plan.

| Entry state | Panel |
|-------------|-------|
| No plan linked | Shown |
| Plan linked (from "Start Trade from Plan" or the manual link selector, `trade_plan.md` §10.3) and the plan has a stored `pre_entry_validation_snapshot` | Not shown. One muted line in its place: "Pre-entry checks were run on the linked plan." (`data-testid="pre-entry-checks-on-plan"`) |
| Plan linked, but the plan has no stored snapshot | Shown |

The panel therefore appears at most once on the page, and a plan whose checks already ran keeps its current flow (ST-01 AC 3). Linking or unlinking a plan mid-entry switches between the rows above without losing form state.

### 2.2 Placement and content

- **Placement:** directly above the Trade Plan Linkage Advisory (`position_form.md` §Trade Plan Linkage Advisory) and the Submit row, after Tags. It is the last thing read before save.
- **Component:** the existing `PreEntryValidationPanel`, moved to a shared component (for example `src/components/trades/PreEntryValidationPanel.js`) and used by both pages. Same rule labels, status icons, colours, collapse toggle and `data-testid`s (`pre-entry-checks-panel`, `pre-entry-panel-toggle`, `pre-entry-issue-count`, `override-acknowledgement-checkbox`). No new check logic.
- **Inputs:** ticker, market, Shares (quantity), Entry Price and the system Initial Stop (`position_form.md` §Initial Stop) as `stop_price`, sent to the existing `GET /portfolio/pre-entry-validation`.
- **Before Shares is entered:** the panel header renders with the line "Enter shares to run the pre-entry checks." (`data-testid="pre-entry-checks-waiting"`, `text-xs text-slate-600 dark:text-slate-400`). Today the panel renders nothing until a quantity exists, which would hide the regime result on an empty form.
- **Unknown regime:** shown exactly as the endpoint returns it. Under `strategy_rules.md` §4.2.1 (v1.20) an unknown regime FAILs, so it shows the ✗ FAIL row with the endpoint's detail text. It is never shown as a pass.
- **Validation unavailable** (endpoint error): the existing "Validation unavailable — proceed with manual checks" line. Save is not blocked by an endpoint failure under either branch below.

### 2.3 Acknowledgement — two branches, pending the ruling

ST-01's slice AC 2 says "save requires the acknowledgement". `strategy_rules.md` §4.2.6 (binding) says the advisory panel must never prevent or gate a submission, and that any hard submission gate needs a new §13 review. The plan path's checkbox does not disable Save today. ST-01's first sub-step is the Strategy Rules & System Intent Owner's ruling on which branch applies (addendum entry ST-01). Both are designed, and the story deletes the branch not taken (v9.13 ST-05/ST-06 and v9.14 ST-03 precedent).

| | Branch A — acknowledge to proceed | Branch B — advisory only (plan-path parity) |
|---|---|---|
| Checkbox | "I acknowledge the advisory warnings", shown when any check is WARN or FAIL | Same |
| Submit while unacknowledged | Disabled. Helper line under the Submit button (`data-testid="pre-entry-ack-required"`, `text-xs text-amber-700 dark:text-amber-400`): "Tick the acknowledgement in Pre-Entry Checks to save." Submit has `aria-describedby` set to that line. | Enabled. No helper line. |
| Ruling needed | That a one-click, user-passable acknowledgement is not a "hard submission gate" under §4.2.6, or a §13 review per §4.2.6 | None: matches §4.2.6 as written. ST-01 AC 2 is then read as "the regime check shows its FAIL/unknown state and the acknowledgement is offered". |

Under either branch, a WARN/FAIL result never changes any field value, and Save is never blocked by anything other than the Branch A checkbox and the two existing `position_form.md` validations.

### 2.4 Override recording

When the entry is saved with the checkbox ticked, the backend writes one `red_flag_events` row with `event_type = "pre_entry_override"`, the ticker and the new `position_id`, and `context = {"source": "trade_entry", "override_acknowledged": true}`. This is the same event the plan path writes (`backend/routers/trade_plans.py` `_maybe_write_override_event`, `source: "trade_plan"`), so the Red Flag Journal and the SI-05 digest (`si05_digest_service.py`, which counts `event_type = 'pre_entry_override'`) count it with no change on their side. A failed event write must not fail the position save (same `try/except` pattern).

The Red Flag Journal shows these rows with its existing "Pre-Entry Override" type label. No journal UI change.

## 3. §13 Compliance

The checks are the existing §4.2 deterministic rules, already reviewed for SI-01 (`docs/product/decisions/decisions--2026-05-19__release-v3.8--SI-01-section13-review.md`) and re-applied on demand under §13.4. This story shows them on one more route and records the same override event. No AI call, no new rule, no automated action. Branch A's acknowledgement is the only §13-relevant question, and it is held for the ruling in §2.3.

## 4. Frontend Spec Impact

- `components/position_form.md` v1.11 → v1.12: new §Pre-Entry Checks (this record), Form Field Order gains item 10, and §Validation Errors notes the Branch A submit condition.

## 5. Obligations for Sprint Execution

- `POST /portfolio/position` accepts an optional `pre_entry_override_acknowledged` boolean and writes the §2.4 event when it is true. The contract (`position_endpoints.md`) and `openapi.yaml` change in the same commit.
- No new route, so the `routers/test.py` / `SystemStatus.js` count / `SC-SS-01b` chain does not apply.
- Delete the unused branch's rows from `position_form.md` §Pre-Entry Checks in the ruling commit.

## 6. Testability (CLAUDE.md §2)

Playwright, with `GET /portfolio/pre-entry-validation` mocked:
- From each route (sidebar link, Positions "New Position", `n` on Positions), with a ticker and Shares entered, `pre-entry-checks-panel` renders with the mocked results (AC 1).
- With a FAIL regime check and with an unknown-regime FAIL, the regime row shows ✗ and the checkbox is offered. Branch A: Submit is disabled until it is ticked. Branch B: Submit is enabled (AC 2).
- With a linked plan that has a snapshot, `pre-entry-checks-panel` is absent and `pre-entry-checks-on-plan` shows. With a linked plan without one, the panel shows once (AC 3).
- A saved entry with the box ticked sends `pre_entry_override_acknowledged: true` (request assertion). The backend event write is covered by a pytest.

## 7. Approval

Head of UX & Design: confirmed, 2026-11-03 (agent-mediated, Design Gate Engine).
Product Owner: confirmed, 2026-11-03 (the user, in session).
