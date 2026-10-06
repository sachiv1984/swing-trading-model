**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-10-06__release-v9.10
**Story:** ST-01 (EPIC-01, BLG-BE-138)

# Decision Record — How Settings Presents the §11 Stop Parameters

## 1. Problem

ST-01 is mainly a backend change: one source for the stop multipliers and grace length. Two parts of it are visible in the UI:

- **The Settings form fallbacks are wrong.** `src/pages/Settings.js` seeds `min_hold_days: 5`, `atr_multiplier_initial: 2` and `atr_multiplier_trailing: 3` when no settings row loads. `settings.md` §1 already specifies `10`, `14`, `5.0` and `2.0`, the `strategy_rules.md` §11 values. The code has drifted from the spec; the spec is correct.
- **The parameter-authority ruling (ST-01 AC 2) decides whether these fields stay editable.** Ruling (a) says they are fixed and Settings shows them read-only. Ruling (b) is a sanctioned personal override. Ruling (c) allows changes only through a §12.3 change record. The ruling is ST-01's first sub-step and does not exist yet, so this record designs all three outcomes. Execution implements the one that is ruled.

## 2. Decision

### 2.1 Fallback values (all outcomes)

| Field | Fallback |
|-------|----------|
| Minimum Hold Days | `10` |
| ATR Period | `14` |
| Initial Stop (ATR Multiple) | `5.0` |
| Trailing Stop (ATR Multiple) | `2.0` |

These fallbacks are a display safety net only. Under every outcome, the values shown come from ST-01's single parameter source when it is available.

### 2.2 Outcome (a): fixed parameters, shown read-only

- The four Strategy Parameters render as **plain read-only values, not disabled inputs.** A disabled input reads as "temporarily locked" or broken; these values are permanent by design.
- Layout: the existing two-column grid, with each slot showing a label (unchanged text), the value (`text-sm font-medium text-slate-900 dark:text-white`) and the existing helper text beneath.
- A single caption sits under the section header (`text-xs text-slate-600 dark:text-slate-400`, `data-testid="strategy-params-fixed-caption"`): **"These parameters are fixed by the strategy rules (§11) and are shown for reference."**
- The Save action no longer sends these four fields. Default Risk % stays editable; it is a user preference, not a strategy parameter (`settings.md` §1).

### 2.3 Outcome (b): sanctioned personal override

- The inputs remain editable, exactly as today.
- When a saved value differs from the §11 default, an inline muted note appears beneath that input (`data-testid="strategy-param-override-note"`): **"Differs from the strategy default ({default})."** No warning colour is used: an override is sanctioned, not an error.
- The existing **Important** note is replaced with the settings-change-effect text that ST-03 writes into `settings_endpoints.md`, so the UI and the contract say the same thing.

### 2.4 Outcome (c): changeable only through a §12.3 change record

- Same presentation as (a). The caption text is instead: **"These parameters change only through a strategy change record (§12.3) and are shown for reference."**

### 2.5 What this record does not change

- Nothing on the Positions page. Displaying the active multiplier per position is ST-06 (`stop-cell-provenance`).
- Trade Entry's multiplier source is ST-07 (`trade-entry-system-stop`).

## 3. §13 Compliance

Deterministic, display-only. No AI. No automated action.

## 4. Frontend Spec Impact

- `settings.md` v1.6 → v1.7. A new subsection, "Strategy Parameter Editability (v9.10)", records §2.2–§2.4 as ruling-conditional, plus a note that the fallback values must equal the §11 defaults. Once the ruling lands, ST-01's own spec-sync commit removes the branches that were not chosen.

## 5. Testability

- Playwright, with the settings endpoint mocked to return an empty list: the form shows `10` / `14` / `5.0` / `2.0`.
- Outcome (a) or (c): the caption is present and none of the four parameters renders as an `<input>`.
- Outcome (b): an override note appears only for a value that differs from the default.

## 6. Approval

Head of UX & Design: confirmed, 2026-10-06.
Product Owner: confirmed, 2026-10-06. Outcome-conditional design accepted. The choice between outcomes stays with the Strategy Rules & System Intent Owner under ST-01 AC 2.
