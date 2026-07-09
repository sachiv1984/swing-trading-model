**Owner:** Head of UX & Design
**Class:** Reference Document (Class 2)
**Status:** Published
**Version:** 1.0
**Last Updated:** 2026-07-09
**Story:** ST-09 (BLG-SPEC-60, EPIC-03, v6.8)

---

# Trailing Stop Visual Indicator — Frontend Specification Reconciliation

## Purpose

This document satisfies ST-09 AC-01/AC-02: a frontend specification for the trailing-stop visual indicator (states, colours, placement), reviewed and signed off by Head of UX & Design.

## Finding: the canonical specification already exists

BLG-SPEC-60's original problem statement (filed v6.2) is stale — it states the Positions page "does not display the current trailing stop price or distance-to-stop." That was true when the item was filed, but v6.2 (ST-01/ST-02, BLG-FEAT-46) subsequently shipped the trailing-stop feature **and** its canonical frontend specification:

- **`docs/specs/frontend/pages/positions.md` §Trailing Stop Column (v1.8, approved 2026-06-24)** — defines placement (Table View column, after "Initial Stop"), data source (`current_trailing_stop` from `GET /positions`), colours (breach badge: orange `#EA580C`, label "⚠ BREACH"), and display states (normal / breach / null / Grid View variant with icon-only breach indicator).
- **`docs/design/2026-06-24__release-v6.2/trailing-stop-display/ux_spec.md`** — the underlying design source for the above.

This satisfies AC-01 (placement, data source, and display states are all defined) without a new artefact being required. Re-authoring it would create a duplicate, conflicting canonical source. The correct action for ST-09 is a **reconciliation review**: confirm the existing spec is complete and accurate, and surface where the shipped implementation diverges from it.

## Reconciliation findings — implementation deviations from the approved spec

| # | Spec requirement (`positions.md` §Trailing Stop Column) | Shipped implementation | Divergence |
|---|---|---|---|
| 1 | Breach badge: orange `#EA580C` background, label "⚠ BREACH" | `src/pages/Positions.js:769-775` — `bg-rose-800/80 text-rose-200` (rose/red), `AlertTriangle` icon, label "Breach" | **Colour and label mismatch.** Rose/red is already used elsewhere on the same page for loss indicators (P&L, Stop column text) — using the same hue for "breach" reduces the badge's intended visual distinctiveness from ordinary loss colouring, which was the spec's explicit rationale for choosing orange (a colour not otherwise used on the page). |
| 2 | Grid View: "Trailing stop value shown in card summary alongside Initial Stop. Breach: ⚠ icon appended inline (icon only, no pill)." | `src/components/positions/PositionCard.js:74-79` — shows only a single "Stop" value (`displayStopPrice`, i.e. `stop_price_native`); no `current_trailing_stop` value and no breach indicator of any kind | **Gap — not implemented.** Grid View users have no trailing-stop visibility or breach signal at all, unlike Table View. |

Both are genuine implementation-vs-spec divergences (spec defines the requirement explicitly; code does something else), not spec ambiguity or intent-alignment questions (per LL-v3.4-P3-03) — filed as backlog items below rather than fixed inline, since implementation changes are outside this spec-authoring story's scope (ST-09 is a 0.5-day spec item; the fix is frontend implementation work for a future sprint).

**Follow-ups filed:**
- BLG-FE-96 — Positions Table View breach badge does not match approved spec colour/label (`#EA580C` "⚠ BREACH" vs shipped rose "Breach")
- BLG-FE-97 — Positions Grid View missing trailing-stop value and breach indicator (spec §Trailing Stop Column Grid View clause unimplemented)

## "Distance-to-stop" — confirmed out of current scope

The original BLG-SPEC-60 problem statement also mentioned "distance-to-stop" as a concept, but neither the approved v6.2 design nor the current canonical spec includes it as a display element (the shipped design shows absolute stop price only, not a computed distance/percentage). This was a Product-Owner-approved scope decision at the v6.2 design gate, not an oversight — re-opening it now would exceed this role's authority to redefine product intent (§3.2, Head of UX & Design charter: "does not redefine product intent"). No action taken; noted here for traceability only.

## Conclusion

AC-01 is satisfied by the existing canonical specification (`positions.md` §Trailing Stop Column); no new spec artefact was warranted. Two implementation deviations from that spec were identified during reconciliation and filed as follow-ups (BLG-FE-96, BLG-FE-97) rather than fixed inline, consistent with this story's spec-only scope.
