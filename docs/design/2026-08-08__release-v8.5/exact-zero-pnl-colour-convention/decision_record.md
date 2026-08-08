**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 4)
**Status:** Approved
**Last Updated:** 2026-08-08
**Cycle:** 2026-08-08__release-v8.5
**Story:** ST-08 (BLG-FE-144, EPIC-03)

# UX Decision Record — Exact-Zero Realised P&L Colour Convention (Reports Page)

## 1. Problem

`docs/specs/frontend/pages/reports.md` documents two tables that both render `realised_pnl_gbp`, and — per `DEV-REPORTS-ST01-02` (filed v8.4, ST-01) — the two live components disagree at the exact-zero case: the Tax Year tab's Trades Table (`TaxYearReport`) renders exact-zero **red** (binary `pnl > 0 ? emerald : rose`); the Monthly P&L Report's table (`MonthlyPnlTable`) renders exact-zero **grey/neutral** (dedicated third branch, corrected into the spec at v0.15). The deviation record identified the decision but did not make it. This is classified Design Required per `design_gate_prompt.md` §6 (colour convention decision affecting existing rendering) — narrow in scope, so a lightweight decision record rather than a full UX spec.

## 2. Decision

**Converge both tables on grey/neutral-for-zero.** The Tax Year Trades Table's `Realised P&L` column changes from `pnl > 0 ? emerald : rose` to the three-way rule already implemented by `MonthlyPnlTable`: green if positive, red if negative, grey/neutral if exactly zero.

## 3. Rationale

- A breakeven trade is not a loss. Rendering it identically to a losing trade (red) misrepresents it to the user scanning the table for at-a-glance performance — the same principle already applied when the Avg P&L/Trade column's zero-trade case was designed to avoid a misleading `£0.00` (v8.4, ST-01).
- `MonthlyPnlTable`'s grey-for-zero behaviour was already live in production before this decision (it was the accidental default, not a deliberate implementation) — no code changed by choosing this direction for that table; only the Tax Year table's component changes.
- Grey/neutral-for-zero is directionally named as "arguably better UX" in the deviation record itself (`DEV-REPORTS-ST01-02`) and is consistent with how a third, neutral state is already used elsewhere on this page (e.g. Avg P&L/Trade's "—" no-colour zero-trade case).
- Red-for-zero has no independent rationale beyond "it's what the Tax Year table already does" — a historical accident, not a considered choice (the original spec wording that both tables were meant to match was itself only ever accurate for the Tax Year table).

## 4. Implementation

- `TaxYearReport` (`src/pages/Reports.js`): change the `Realised P&L` cell's colour logic from the binary `pnl > 0 ? "text-emerald-400" : "text-rose-400"` to a three-way rule matching `MonthlyPnlTable`: `pnl > 0 ? "text-emerald-400" : pnl < 0 ? "text-rose-400" : "text-slate-400"` (or the exact neutral token `MonthlyPnlTable` already uses — implementer confirms exact class against that component to keep the two identical rather than introducing a second "neutral" shade).
- `MonthlyPnlTable`: unchanged — already correct.
- No change to non-zero colouring in either table (explicit no-regression AC in the story).

## 5. Scope boundary

Applies to the `Realised P&L` column in both tables only. Does not touch `P&L %`, `Avg P&L/Trade` (already grey-for-zero, unaffected), the Summary Bar's `Total Realised P&L` (an aggregate figure — a zero aggregate across many trades is a different question, out of scope here), or any other page's P&L colouring (Positions, Open Positions Panel — those use their own established convention, not addressed by this record).

## §13 check

Purely presentational colour-rule convergence; no automated decision or AI call. Not applicable.
