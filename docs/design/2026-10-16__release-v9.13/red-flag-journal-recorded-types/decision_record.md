**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-16__release-v9.13
**Story:** ST-04 (EPIC-01, BLG-BE-182)

# Decision Record — Red Flag Journal: Show Which Event Types Are Recorded

## 1. Problem

The journal's Event Type filter offers four types. Only `pre_entry_override` has ever been written. ST-04 adds a writer for `checklist_skipped`. `stop_prompt_dismissed` and `drawdown_prompt_dismissed` still have none, so filtering by them always returns an empty list. A user can then conclude they never dismissed a prompt.

## 2. Decision

### 2.1 Filter options

The options for types with no writer stay visible, so the user knows they exist, but are **disabled** and suffixed:

| Option | State |
|--------|-------|
| All types | Enabled (default) |
| Pre-Entry Override | Enabled |
| Checklist Skipped | Enabled (writer added by ST-04) |
| Stop Prompt Dismissed — not yet recorded | Disabled |
| Drawdown Prompt Dismissed — not yet recorded | Disabled |

- The recorded set is a single frontend constant (`RECORDED_EVENT_TYPES`). It must match the backend writer-coverage test's set, so that adding a writer means editing one list on each side.
- A stored filter (`redFlagJournal.filters`) that names a disabled type resets to "All types" on load.

### 2.2 Empty states

| Condition | Display |
|-----------|---------|
| No events, no active filters | "No strategy deviations recorded yet" + "Pre-entry overrides and skipped checklists are recorded here. Stop and drawdown prompt dismissals are not recorded yet." |
| No events, active filters | "No events match your current filters." + "Clear filters" link + the same recorded-types sentence |

The sentence is muted (`text-sm text-slate-600 dark:text-slate-400`), `data-testid="recorded-types-note"`. It is built from `RECORDED_EVENT_TYPES`, so it stays true when a writer is added.

### 2.3 Checklist Skipped rows

They use the existing row layout (icon ☑, label "Checklist Skipped"). The context summary reads "{n} of {m} checklist items unchecked when the plan was saved", or "{n} checklist item(s) unchecked" when the total is absent. The ticker and the relative time are shown as for other rows.

## 3. §13 Compliance

Display and logging only. The event is non-blocking (AC 1). The plan saves whether or not the write succeeds.

## 4. Frontend Spec Impact

`red_flag_journal.md` v1.3 → v1.4: §4 Filter Controls, §5 context summary for `checklist_skipped`, and §7 Empty States.

## 5. Testability (CLAUDE.md §2)

- Playwright (AC 1): save a plan with an incomplete checklist, open the journal, and see one Checklist Skipped row with the unchecked count.
- Playwright (AC 2): the two unrecorded options are disabled and carry "not yet recorded". `recorded-types-note` is visible in both empty states.

## 6. Approval

Head of UX & Design: confirmed, 2026-10-16.
Product Owner: confirmed, 2026-10-16.
