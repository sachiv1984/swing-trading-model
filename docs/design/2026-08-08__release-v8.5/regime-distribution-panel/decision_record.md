**Owner:** Head of UX & Design
**Class:** Design Artefact (Class 4)
**Status:** Approved
**Last Updated:** 2026-08-08
**Cycle:** 2026-08-08__release-v8.5
**Story:** ST-21 (BLG-FEAT-29, EPIC-06)

# UX Decision Record — Regime Distribution Panel (Screener Results Page)

## 1. Problem

No view shows how the market regime has distributed across screener runs over time — a user can only see today's `regime_status` (§4, `screener_results.md`), not how often the market has been risk-on vs risk-off recently. This is classified Design Required per `design_gate_prompt.md` §6 ("new data displayed"). Note: `BLG-FEAT-29`'s problem statement describes a "bull/bear/neutral/volatile" taxonomy, but the system's actual regime model (`strategy_rules.md` §8.2, §11) is binary — risk-on / risk-off, driven by the relevant index's 200-day moving average. This decision designs against the real, binary taxonomy, not the illustrative four-way one named at idea-intake time.

## 2. Decision

A new compact **"Regime History"** panel on the Screener Results page, placed directly below the page header / above the Sort and Filter Controls section (§5) — visible before the user scans individual ticker rows, since it's context for interpreting the whole result set, not a per-row detail.

**Contents:**
- A rolling-window selector using the page's existing Segmented button pattern (already established for the Market filter, §5.2): **30d / 60d / All**.
- A two-segment horizontal percentage breakdown bar: green segment = % of screener runs in the selected window where `regime_status = risk_on`, red segment = % where `risk_off` — reusing the exact chip colours already defined for the per-row Regime column (§4: `risk_on` → green, `risk_off` → red), so the aggregate view reads as the same concept scaled up, not a second colour convention to learn.
- A single-line numeric readout beneath the bar, e.g. `"Risk-On 72% · Risk-Off 28% (30d)"`.

## 3. Rationale

- Reusing the Market filter's Segmented button pattern for the window selector avoids introducing a third selector shape on a page that already has Segmented (Market) and Toggle (Regime) controls.
- Reusing the existing green/red regime chip colours (rather than a new palette) keeps the aggregate and per-row views visually consistent — a user who has learned "green = risk-on" from the table doesn't need to relearn it for the summary.
- Placement above the table (not inside it, not a separate page) keeps this as page-level context rather than implying it's a property of any individual ticker row.
- No new component: this is a percentage-breakdown bar, the same visual primitive already implied by other percentage-based displays on this page (e.g. Signal Score's bar-indicator option, §4) — no new pattern class introduced to the design system.

## 4. Data source and edge cases

- Sourced from screener run history (already the case — no new backend concept, only a new aggregate query over existing `regime_status` values per run).
- If a window has zero screener runs (e.g. a very new user, `All` on day one): render the panel's `DataState` `empty` branch (per `design_system.md` §Data States) rather than a `0%/0%` bar, which would misleadingly imply data exists and split evenly.

## 5. Scope boundary

Screener Results page only. Does not touch the per-row Regime column (§4, unchanged), the Regime filter Toggle (§5.2, unchanged — filters the table, distinct from this page-level summary), or any other page. Does not add a time-series/trend-line view — the AC calls for "percentage breakdown or time-series chart," and the percentage-breakdown form is chosen as sufficient and simpler to implement correctly (no axis/zoom/hover-tooltip surface to get wrong) for a first pass; a trend-line view remains an option for a future iteration if the percentage breakdown proves insufficient.

## §13 check

Aggregation and display of existing screener-run data; no automated decision or AI call. Not applicable.
