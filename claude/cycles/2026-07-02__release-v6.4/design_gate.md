**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-02
**Cycle:** 2026-07-02__release-v6.4

# Design Gate Record — 2026-07-02__release-v6.4

## Gate Status: PASSED

Completed: 2026-07-02
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 | Signal generation reads deprecated `tickers` table (BLG-BE-40) | Design Pre-Approved | Backend ticker-universe data source swap only; no UI, no new/changed rendering | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-02 | Sanitise `context_opts.ticker` before system prompt injection (BLG-SEC-01) | Design Pre-Approved | Backend input validation on request body; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-03 | Validate ticker/market strings at signal write time (BLG-SEC-02) | Design Pre-Approved | Backend write-path validation; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-04 | Fix governance version-sync drift (BLG-GOV-150) | Design Not Applicable | Governance document metadata only; no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-05 | Document hygiene cleanup (BLG-GOV-151) | Design Not Applicable | README/prompt-header text only; no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-06 | Close structural reliability gaps (BLG-GOV-152 + FI-P3-01/FI-P3-02/FI-P4-01) | Design Not Applicable | Governance prompt/process text only; no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-07 | Audit & governance process fixes (BLG-GOV-153) | Design Not Applicable | Governance/audit process text only; no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-08 | Add Open Positions panel to Strategy Benchmark page (BLG-FEAT-54) | Design Required | New UI panel — new component, new layout region, new data displayed | `docs/design/2026-07-02__release-v6.4/open-positions-panel/ux_spec.md` v1.0 | `docs/specs/frontend/pages/strategy_benchmark.md` v0.2 | ✅ Cleared | Head of UX & Design |
| ST-09 | Improve AI daily briefing disclaimer text contrast (BLG-UX-01) | Design Required | Visible colour/contrast change to existing component (default-to-Design-Required per §6) | `docs/specs/qa/ai_disclaimer_visibility_assessment.md` v1.0 (pre-existing, approved 2026-06-29; confirmed current for this gate) | `docs/specs/frontend/pages/dashboard.md` v2.5 | ✅ Cleared | Head of UX & Design |
| ST-10 | Improve AI chat widget footer disclaimer contrast + test coverage (BLG-UX-02) | Design Required | Visible colour/contrast change to existing component + new `data-testid` (default-to-Design-Required per §6) | `docs/specs/qa/ai_disclaimer_visibility_assessment.md` v1.0 (pre-existing, approved 2026-06-29; confirmed current for this gate) | `docs/specs/frontend/pages/positions.md` v1.9 | ✅ Cleared | Head of UX & Design |
| ST-11 | Add v6.3 endpoints to `api_performance_baseline.md` (BLG-OPS-82) | Design Not Applicable | Ops documentation registration only; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-12 | Playwright coverage for ST-01 observable UI ACs (TEST-GAP-EPIC-01) | Design Not Applicable | Test authoring against existing, already-shipped UI; no new/changed rendering | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-13 | Playwright scenario coverage for Strategy Benchmark page (TEST-GAP-EPIC-03) | Design Not Applicable | Test authoring against existing, already-shipped UI; no new/changed rendering | N/A | N/A | ✅ Cleared | Head of UX & Design |

## Blocked Items (if any)

None.

## Notes

- Release plan (`release_plan.md` §Readiness) had already flagged exactly ST-08, ST-09, ST-10 as the 3 UI-facing items requiring Design Gate (RISK-06) — classification in this run confirms that pre-assessment.
- ST-09 and ST-10 are both one-line Tailwind contrast-class fixes with no layout/component change. Rather than commissioning new wireframes, the existing `docs/specs/qa/ai_disclaimer_visibility_assessment.md` (Class 3, already carrying Head of UX & Design + AI Compliance & Governance Officer sign-off from 2026-06-29, ST-05/BLG-GOV-147 v6.3) was used as the authoritative design artefact per STEP 2.1 ("if yes: Head of UX & Design reviews and confirms artefact is current and approved"). It specifies the exact before/after class values for both items; no drift found between it and the current source (`AiDailyBriefing.js`, `AiChatWidget.js`).
- ST-08 required new design work — no prior artefact existed. New UX spec produced at `docs/design/2026-07-02__release-v6.4/open-positions-panel/ux_spec.md`, introducing "Panel 0 — Open Positions" (placed before the existing Panel 1, preserving Panel 1/2/3 numbering referenced elsewhere, notably by ST-13's ACs). Key design decision: the panel respects the Market filter but is exempt from the Year filter, since open positions are current-state rather than historical-per-year data — documented with rationale in both the design artefact and the updated `strategy_benchmark.md` §3/§4.5.
- `strategy_benchmark.md` v0.2 also adds the new `GET /strategy/benchmark/open-positions` endpoint to §9, flagging the same-commit `openapi.yaml`/contract-doc/`test.py` obligations that fall to Sprint Execution (CLAUDE.md §2).
- No design artefact exists yet for the AI Chat Widget as a standalone component (it is documented within `positions.md` §"AI Trade Advisor Widget" rather than a dedicated `docs/specs/frontend/components/` file). Given the write-scope restriction in this engine (`docs/specs/frontend/pages/` only), the ST-10 spec update was made in `positions.md` at its existing documented location rather than creating a new components-directory file.
- No disagreements between Product Owner and Head of UX & Design on any item this run; no downgrades applied.
