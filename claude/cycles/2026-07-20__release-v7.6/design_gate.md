**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-20
**Cycle:** 2026-07-20__release-v7.6

# Design Gate Record — 2026-07-20__release-v7.6

## Gate Status: PASSED

Completed: 2026-07-20
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 (EPIC-01, BLG-FE-119) | Print/PDF export action — WeeklyDigest and TradePlan | Design Required | New UI action on two pages (button, print-stylesheet output) | `docs/design/2026-07-20__release-v7.6/print-pdf-export/ux_spec.md` | `docs/specs/frontend/pages/weekly_digest.md` v0.1 (new file), `docs/specs/frontend/pages/trade_plan.md` v1.2 | ✅ Cleared | Head of UX & Design |
| ST-02 (EPIC-02, BLG-QA-112) | Regression suite baseline update | Design Not Applicable | Documentation-only (regression baseline doc); no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-03 (EPIC-03, BLG-FEAT-79) | P&L export audit trail reconciliation | Design Not Applicable | Backend reconciliation logic against existing data; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-04 (EPIC-04, BLG-BE-65) | Backend error-response envelope standardisation | Design Not Applicable | Backend-only audit/standardisation; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-05 (EPIC-05, BLG-QA-114) | OpenAPI-derived Playwright fixture library | Design Not Applicable | Test tooling/infrastructure; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-06 (EPIC-06, BLG-BE-62) | Nightly batch-job idempotency audit | Design Not Applicable | Backend audit of existing jobs; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-07 (EPIC-07, BLG-FEAT-77) | Consolidated monthly AI cost view (Gemini + Claude) | Design Required | New read-only UI section, new data displayed (neither provider's cost was previously rendered anywhere in the frontend) | `docs/design/2026-07-20__release-v7.6/consolidated-ai-cost-view/ux_spec.md` | `docs/specs/frontend/pages/settings.md` v1.4 | ✅ Cleared | Head of UX & Design |
| ST-08 (EPIC-08, BLG-QA-69) | Ticker/market input sanitisation regression suite | Design Not Applicable | Backend/test regression suite; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |

All 8 items classified per §6 default rule — no disagreement between Product Owner and Head of UX & Design; no downgrade requested. This matches `stage4_backlog_slice.md`'s own sequencing note: ST-01 and ST-07 conditional on Design Gate PASS (RISK-01); ST-02/03/04/05/06/08 have no Design Gate dependency.

## Blocked Items

None.

## Notes

**Scope basis:** This run classifies all 8 items in the current `stage4_backlog_slice.md`, including EPIC-03 through EPIC-08 — added post-publish via the PO-directed capacity-fill reopen (DL-073, `state.json.po_directed_reopen`) after this cycle's release plan had already reached `Published`. That reopen occurred before this Design Gate ran (per its own note: "no Design Gate run, no Sprint Planning run" had yet occurred), so no gate re-evaluation or invalidation is needed here — this is the first Design Gate pass against the full 8-item scope.

**Placement decisions requiring explicit call:**
- **ST-01:** Implemented as a client-side `window.print()` + print-stylesheet action rather than a server-side PDF-rendering endpoint (unlike the existing Tax Year report's "Download PDF"). Rationale: both target pages are already-rendered read-only views (no new data assembly needed); a print stylesheet satisfies both "print-friendly" and "PDF output" via the browser's native "Save as PDF" print destination; avoids two new backend endpoints for an M-effort item. See artefact §2.1 for full rationale.
- **ST-07:** Placed in **Settings** (new §6 "AI Usage & Costs", read-only) rather than **Reports** — neither page was a clean pre-existing fit (Reports is trade-performance-only; Settings is otherwise all editable config), but Settings already houses the closer conceptual neighbour (§2 Commission & Fees — "what does this cost me"). See artefact §2 for full rationale.

**Gap recovery:** `WeeklyDigest.js` (shipped v2.4, ST-09, BLG-FEAT-14) had no canonical frontend spec prior to this run. `docs/specs/frontend/pages/weekly_digest.md` v0.1 was created as part of this gate's STEP 3 work, documenting the existing as-built page in addition to the new §4 Print/Export action — following the same gap-recovery precedent as `trade_plan.md`'s own v0.1/v0.2 history (DEV-01).

**Settings.md secondary fix:** While updating `settings.md`, the top-of-file "Sections:" summary list was found to already be missing the pre-existing "Risk Limits" section (§4 in the body) before this run's edit. Corrected as part of this same edit (see `settings.md` v1.4 changelog entry) rather than filed as a separate follow-up, since it was touched in the same section of the file.

No escalations raised. No items require sprint-execution follow-up beyond the standard implementation of what is now specified.
