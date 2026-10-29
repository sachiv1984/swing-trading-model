**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Cycle:** 2026-10-29__release-v9.14

# Post-Gate-Correction Addendum — 2026-10-29__release-v9.14

Corrections below are additive to the sealed `stage4_backlog_slice.md` — they do not replace or edit its content. Sprint Planning and Sprint Execution must read both files together as the combined authoritative scope.

## ST-03 — The unknown regime state covers every surface that shows the regime, not only the dashboard
**Found at:** Design Gate STEP 1 (classification) and STEP 2.2 (design work)
**Correction:** The slice's AC 4 names only the dashboard. The source item's Scope says "show the unknown state wherever the regime is shown". The design gate found four such surfaces, and three of them (Dashboard Card 4, the Signals market status bar and the customisable Dashboard regime widgets) render an unknown value as "Risk Off" today. The decision record (`docs/design/2026-10-29__release-v9.14/market-regime-unknown/decision_record.md` §2.1) applies the unknown state to all four. It also adds a Playwright check of the Signals bar and makes the frontend's local fallbacks default to `"unknown"`, not `"risk_on"`. `GET /market/status` and `GET /market/regime` both carry the unknown state (contract and `openapi.yaml` in the same commit). This stays within the item's own Scope. Sprint Planning should check the S (~0.5d) estimate against the four surfaces.
**Date:** 2026-10-29

## ST-04 / ST-05 — The FX source also reaches the Signals page FX tile, and the Signals page's own constant is removed
**Found at:** Design Gate STEP 2.2 (design work)
**Correction:** ST-04's Scope says to expose the rate's source and age "where FX-dependent figures are shown". The Signals page shows the FX rate itself, from `GET /market/status`, and falls back to its own constant, 1.3611, when the field is missing. That is the silent-constant problem BLG-BE-169 describes. The decision record (`docs/design/2026-10-29__release-v9.14/fx-rate-source-indicator/decision_record.md` §2.3, §5) therefore adds `fx_rate_source` and `fx_rate_as_of` to `GET /market/status` as well as `GET /portfolio` and `GET /positions`. The Signals FX tile shows the source line, and the page's 1.3611 constant is removed (it shows "—" when there is no rate). The Positions page indicator is not added: neither story names that page.
**Date:** 2026-10-29
