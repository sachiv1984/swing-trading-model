**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-12__release-v9.12
**Story:** ST-15 (EPIC-02, BLG-FE-202)

# Decision Record — Show When a Position's Stop Is Frozen for Lack of ATR

## 1. Problem

When no ATR is available, the on-load recompute keeps the stored stop and sets `atr_unavailable: true`, but only on the `GET /positions/analyze` response. The nightly job skips the position silently. Nothing reaches `GET /positions`, so the user cannot tell that a stop has stopped trailing.

The v9.10 provenance line already reads "ATR unavailable" when `atr_value` is null. That describes a missing value, not a stop that failed to update at the last recompute. A position can have a stored `atr_value` from an earlier day and still be frozen today.

## 2. Decision

### 2.1 Data

`GET /positions` returns `stop_frozen_reason`: `"atr_unavailable"` or `null`. Both the on-load and nightly paths write it when they keep the stop because ATR was unavailable, and clear it on the next recompute that has an ATR. The field is an enum rather than a boolean so later reasons need no new field.

### 2.2 Display

Shown only when `stop_frozen_reason` is set **and** `grace_period` is false. During grace the stop is frozen by rule (§6.3), and the existing grace line already says so.

- **Table View**, under the trailing-stop value, in place of the provenance line: `PauseCircle` icon (lucide, 12 px) plus "Stop frozen · ATR unavailable", `text-xs text-amber-700 dark:text-amber-400`, `data-testid="stop-frozen-indicator"`.
- **Grid View:** the same element under the Stop tile value.
- **Per-row tooltip** ("How this stop was set"): one added row after "Last recalculated": "Not updated at the last recalculation because ATR was unavailable. The stop stays at its current level until ATR returns."
- The trailing-stop value, `Init:` line, breach badge and column header are unchanged.

Amber, not rose: the stop is still enforced at its last level. This is a warning, not an error. Contrast: `amber-700` is 5.02:1 on white and 4.58:1 on `slate-100`; `amber-400` passes on dark surfaces (existing token).

### 2.3 Accessibility

The icon is `aria-hidden`. The text carries the meaning, so colour is not the only signal.

## 3. §13 Compliance

Display-only. No automated action. No change to the stop calculation.

## 4. Frontend Spec Impact

`positions.md` v2.15 → v2.16: new §Frozen Stop Indicator under §Stop Provenance Line.

## 5. Obligations for Sprint Execution

- Add `stop_frozen_reason` to `position_endpoints.md` and `openapi.yaml` in the same commit (AC 1).
- Store it on both recompute paths. The nightly path's "ATR unavailable" skip must set it (AC 2).
- `data_model.md` gains the column if the field is stored rather than derived (RISK-04, shared file).

## 6. Testability (CLAUDE.md §2)

- Playwright, mocked `GET /positions` with `stop_frozen_reason: "atr_unavailable"` and `grace_period: false`: the indicator is visible in Table and Grid views.
- Playwright, the same with `grace_period: true`: no indicator.
- Backend test: the nightly skip sets the field, and a later recompute with ATR clears it.

## 7. Approval

Head of UX & Design: confirmed, 2026-10-12.
Product Owner: confirmed, 2026-10-12.
