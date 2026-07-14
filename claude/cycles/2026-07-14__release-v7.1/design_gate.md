**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-14
**Cycle:** 2026-07-14__release-v7.1

# Design Gate Record — 2026-07-14__release-v7.1

## Gate Status: PASSED

Completed: 2026-07-14
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 (BLG-BE-59) | Gate nightly backtest ticker eligibility on `ticker_universe.created_at` | Design Pre-Approved | Backend correctness fix inside the nightly backtest job's signal computation; no UI/layout/component change — only corrects the underlying data later rendered by the existing Strategy Benchmark page | N/A | N/A — `strategy_benchmark.md` (v0.3) unaffected, no visual change | ✅ Cleared | Head of UX & Design |
| ST-02 (BLG-BE-60) | Fix nightly backtest `total_pnl_gbp` non-reproducibility | Design Pre-Approved | Backend data-pipeline correctness fix (price-revision rescaling); no UI change regardless of which fix vehicle (cache/append-only ledger/drift-alert) is selected at execution time | N/A | N/A — no frontend spec touches this story | ✅ Cleared | Head of UX & Design |
| ST-03 (BLG-FE-107) | Table View RISK OFF badge colour/label spec compliance | Design Required | User-facing badge colour/label change (or a formal spec exception) — explicitly sequenced behind the design gate as RISK-03 in the release plan | `docs/design/2026-07-14__release-v7.1/table-view-badge-compliance/decision_record.md` (new, v1.0, Approved) — Option (a) selected: bring Table View into compliance | `positions.md` v2.3 — reviewed and confirmed already compliant (§Alerts Column's Risk-Off Badge table was correct since v6.2); no spec text change required, only the Table View implementation and `SC-RO-02` need correcting in execution | ✅ Cleared | Head of UX & Design |
| ST-04 (BLG-BE-61) | Position review-cadence nudge: backend/data-integrity hardening pass | Design Pre-Approved | IDOR regression check, NULL/backfill semantics, and a lifecycle-state-machine clarification — all backend/documentation, no visual or interaction change | N/A | `positions.md` v2.3 — AC-03's written confirmation is a textual clarification only (state machine remains 4 states); no design gate involvement, locked spec reference for execution | ✅ Cleared | Head of UX & Design |
| ST-05 (BLG-QA-106) | Position review-cadence nudge: frontend/QA polish pass | Design Required | Backlog slice explicitly routes AC-03 (UX consistency review) through the design gate as RISK-04 | `docs/design/2026-07-12__release-v7.0/position-review-cadence-nudge/ux_spec.md` (v1.0, Approved, v7.0) — reviewed this cycle, confirmed still current; explicitly designed to stay visually subordinate to the Alerts column and to follow existing low-friction display-toggle precedent, which is what AC-03 asks to be confirmed | `positions.md` v2.3 §Last Reviewed Column — already documents placement, flag threshold/colour, and the Grace/Drawdown suppression (coexistence) rule AC-02 asks for; confirmed compliant, no change required | ✅ Cleared | Head of UX & Design |
| ST-06 (BLG-SPEC-83) | Realized/unrealized P&L split: spec & metrics hardening pass | Design Required | AC-04 (visual treatment confirmation) is a colour claim | `docs/design/2026-07-12__release-v7.0/realized-unrealized-split/ux_spec.md` (v1.0, Approved, v7.0) — reviewed this cycle, confirmed still current; already specifies profit/loss colour (`text-emerald-400`/`text-rose-400`, aligned with Open Positions Panel convention) | `reports.md` v0.8 → **v0.9** (updated this run) — added the colour-convention sentence to both Unrealised P&L Card sections (Tax Year tab and Monthly P&L Report), closing the gap between the already-approved design source and the canonical spec text | ✅ Cleared | Head of UX & Design |
| ST-07 (BLG-SPEC-84) | Tax-year P&L CSV export: spec & test hardening pass | Design Pre-Approved | Purely backend/API/test/documentation hardening (content-type, auth parity, smoke tests, content-asserting test, pattern doc); no UI change | N/A | `reports.md` v0.9 — confirmed unaffected by this story (no CSV UI/rendering change); locked spec reference for execution | ✅ Cleared | Head of UX & Design |

## Blocked Items (if any)

None.

## Notes

- **ST-03** was the substantive item this cycle. The design review confirmed the existing spec (blue-800 `#1E40AF`, "RISK OFF") is and always was correct — the v6.2 Table View implementation drifted from it, and that drift was accidentally encoded as the expected value in `SC-RO-02`. Accepting the shipped amber as canonical (option b) was rejected because it would invalidate the safety rationale in the v7.0 combined-badge differentiation decision record (hue separation between RISK OFF and GAP RISK), which assumed Table View was blue. Execution must: fix `AlertsCell` (blue-800, label "RISK OFF", drop the unspecified `ShieldAlert` icon) and update `SC-RO-02`'s expected values in the same commit. `DEV-EPIC01-ST05-01` closes on merge.
- **ST-05** and **ST-06** both had approved v7.0 design artefacts that already answered their design-gate-routed ACs (RISK-04 and AC-04 respectively) in substance but not, for ST-06, in the canonical spec's own text — that gap is now closed in `reports.md` v0.9. No new wireframes or decision records were needed for either; STEP 2.1 (existing-artefact confirmation) applied, not STEP 2.2 (new design work).
- **ST-01/ST-02/ST-04/ST-07** are backend/data/test hardening with no UI surface and were classified Design Pre-Approved without further review.
- Minor process note (non-blocking): `design_gate_prompt.md` §5's write-scope bullet list does not explicitly name `docs/design/<cycle_id>/`, though STEP 2.2 and STEP 6 both direct artefacts to be filed and committed there. Treated as an intent gap in the prompt text, not a scope violation — worth a future prompt patch via `prompt_change_log.md`, flagging for PMO Lead rather than actioning unilaterally in this run.
