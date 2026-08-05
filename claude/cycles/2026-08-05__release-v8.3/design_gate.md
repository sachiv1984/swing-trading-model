**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-08-05 (re-run — ST-11 re-classified following `BLG-FE-103` scope correction, ESC-20260805-01 resolved; gate cleared to PASSED)
**Cycle:** 2026-08-05__release-v8.3

# Design Gate Record — 2026-08-05__release-v8.3

## Gate Status: PASSED

Completed: 2026-08-05
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 | Investigate/fix SI-05 weekly Telegram digest delivery pipeline | Design Not Applicable | Backend/infra delivery pipeline fix; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-02 | Delivery-failure alerting for SI-05 weekly digest | Design Not Applicable | Alerting infra; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-03 | Recurring check confirming staging/production API keys remain distinct | Design Not Applicable | Security/infra automated check; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-04 | Gemini API key rotation runbook | Design Not Applicable | Documentation (security register runbook); no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-05 | Database index audit for Arc 4 cross-table queries | Design Not Applicable | Backend audit document; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-06 | Alpaca API rate-limit backoff audit | Design Not Applicable | Backend audit document; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-07 | Canonical enum registry for `position_state` values shared frontend/backend | Design Not Applicable | Shared-constant/reconciliation refactor; no user-visible UI change (values and their rendering are unchanged, only the source of truth) | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-08 | Conform remaining routers to canonical error envelope + status codes | Design Not Applicable | Backend response-shape conformance; AC explicitly excludes frontend error-handling behaviour change without a corresponding check | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-09 | Retry/backoff for Yahoo Finance regime-check call sites | Design Not Applicable | Backend resilience only; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 | Idempotent retry for Alpaca paper-trading order sync | Design Not Applicable | Backend resilience only; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-11 | Migrate `ComplianceRecheckModal.js` onto the shared Dialog primitive | Design Pre-Approved | **Re-classified this run (was Design Required, Blocked).** `BLG-FE-103` corrected by Base44 Frontend Prompt Owner (ESC-20260805-01, resolved 2026-08-05): the "PT-05 checklist modal" second consumer does not exist in source; scope narrowed to a single-file migration of `ComplianceRecheckModal.js` onto the already-existing shared `Dialog`/`DialogContent` primitive (`src/components/ui/dialog.js`), already used by ~11 other modal consumers and already documented as canonical (`design_system.md` §Confirmation Modal, "existing `Dialog` primitive convention" — focus trap + restoration, Escape = Cancel). No new UX decision — applies an already-approved, already-specified pattern with an explicit no-visual/behavioural-regression AC, same basis as ST-15's Design Pre-Approved classification this run. | N/A (existing shared primitive + spec govern) | `docs/specs/frontend/design_system.md` v1.7 (unchanged — §Confirmation Modal already documents the Dialog primitive convention this item migrates onto) | ✅ Cleared | Head of UX & Design |
| ST-12 | Extract a shared modal-confirmation component | Design Required | Genuinely new interaction pattern — no existing artefact defines an undo-window countdown; both existing confirmation-modal instances (`positions.md` §Exit action, `watchlist.md` §Remove Confirmation Prompt) have no undo window | `docs/design/2026-08-05__release-v8.3/shared-confirmation-modal-undo-window/decision_record.md` | `docs/specs/frontend/design_system.md` v1.7 | ✅ Cleared | Head of UX & Design |
| ST-13 | Unified loading-skeleton pattern for async-loading cards | Design Required | New visual pattern — `DataState`'s loading branch is spinner-only today ("no skeleton" per its own source comment); also a new pulse-animation timing parameter, which §6's motion/timing rule (BLG-FE-131 precedent) makes Design Required independent of any layout change | `docs/design/2026-08-05__release-v8.3/loading-skeleton-pattern/decision_record.md` | `docs/specs/frontend/design_system.md` v1.7 | ✅ Cleared | Head of UX & Design |
| ST-14 | Standard Base44 prompt section for dark/light theme compliance | Design Pre-Approved | Codifies the already-fully-specified theme/contrast rules in `design_system.md` §Theme & Colors / §Accessibility into a Base44 prompt template section; no new UX decision | N/A | `docs/specs/frontend/design_system.md` v1.7 (unchanged content governs; template packaging only) | ✅ Cleared | Head of UX & Design |
| ST-15 | AI disclaimer component extraction | Design Pre-Approved | Extraction only, explicit "no visual regression" AC; reuses the already-approved contrast fixes for both existing instances — AI Daily Briefing Advisory Label (`dashboard.md` §Advisory Label, v6.4/v6.7 fixes) and AI Trade Advisor Widget footer (`positions.md` §AI Trade Advisor Widget, v6.4/v6.7 fixes) — verified both are still the shipped, approved values | N/A (existing specs govern) | `docs/specs/frontend/pages/dashboard.md` v3.2 (unchanged), `docs/specs/frontend/pages/positions.md` v2.7 (unchanged) | ✅ Cleared | Head of UX & Design |
| ST-16 | Add baseline Playwright coverage for Watchlist.js | Design Not Applicable | Test infrastructure only; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-17 | OpenAPI drift gate false-negative sweep | Design Not Applicable | QA process procedure; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-18 | DoQ sign-off staleness pre-merge lint | Design Not Applicable | CI/CD lint check; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-19 | OpenAPI response-example drift spot-check | Design Not Applicable | Documentation audit; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-20 | API endpoint deprecation-window policy | Design Not Applicable | API documentation standards; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-21 | Canonical form validation error-message pattern spec | Design Required | New canonical pattern — two shipped instances (`WatchlistModal.js`, `TradePlan.js`) verified to diverge on trigger timing, and both share an unaddressed dark-only colour-token gap; establishing the canonical rule and fixing the token is a genuine UX decision, not a restatement | `docs/design/2026-08-05__release-v8.3/form-validation-error-message-pattern/decision_record.md` | `docs/specs/frontend/design_system.md` v1.7 | ✅ Cleared | Head of UX & Design |
| ST-22 | SC-02: Remove RESUME PRECHECK mutation detection block from release_planning_prompt.md | Design Not Applicable | Governance prompt amendment; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-23 | Formal §13 boundary re-attestation cadence | Design Not Applicable | Governance process cadence; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-24 | SI-02 trade-count gate threshold calibration review | Design Not Applicable | Governance/metrics review; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-25 | `prompt_change_log.md` mixed prepend/append ordering breaks gap detection | Design Not Applicable | Governance file/process fix; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-26 | Cross-role workload balance check | Design Not Applicable | Governance-engine report output (roadmap rebalance), not app UI; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-27 | Monthly P&L report format review — 3-month usage retrospective | Design Not Applicable | Review/recommendations document only; the story itself ships no UI — any identified format change is filed as a separate future item subject to its own design gate | N/A | N/A | ✅ Cleared | Head of UX & Design |

**Mandatory §13 boundary pre-check (AI-calling proposals):** none of the 27 items introduce or extend a call to an AI provider (ST-04 is a key-rotation runbook, not a new call). No item requires a §13 pre-check flag this run.

## Blocked Items

None. ST-11 (the sole blocked item from the initial run) was resolved and re-classified this re-run — see Notes.

## Notes

- **Gate is PASSED on this re-run** — all 27 items cleared. Initial run (2026-08-05T10:15:00Z) blocked on ST-11 (`BLG-FE-103`); resolved via `ESC-20260805-01` (Base44 Frontend Prompt Owner correction, commit `85172aab`) and re-classified in this re-run.
- **ST-11 re-classification (Blocked → Design Pre-Approved):** the original item proposed extracting a *new* shared modal shell spanning two consumers, one of which (the "PT-05 checklist modal") does not exist in source — that premise could not be satisfied as written, so the initial run correctly blocked rather than rubber-stamped it. Base44 Frontend Prompt Owner correction narrowed scope to a single-file migration of `ComplianceRecheckModal.js` onto the *already-existing* shared `Dialog`/`DialogContent` primitive (`src/components/ui/dialog.js`), already used by ~11 other modal consumers and already documented as the canonical modal-accessibility pattern in `design_system.md` §Confirmation Modal ("existing `Dialog` primitive convention" — focus trap + restoration, Escape = Cancel). With the "new shared shell" premise withdrawn, there is no new UX decision left to review — the item now applies an established, already-approved pattern with an explicit no-visual/behavioural-regression AC, matching ST-15's Design Pre-Approved basis exactly. No design artefact or spec version bump required; `design_system.md` v1.7 already governs.
- Three items classified **Design Required** and cleared in the initial run: ST-12 (genuinely new undo-window interaction, no prior artefact), ST-13 (genuinely new skeleton pattern — also a new motion/timing parameter, Design-Required-triggering under §6 independent of layout), ST-21 (genuinely new canonical error-message rule — two shipped instances verified to diverge on trigger timing, plus closes an unaddressed dark-only colour-token gap found during verification, same defect class as `BLG-FE-87/88/95`). All three received lightweight decision records and a single combined `design_system.md` version bump (1.6→1.7) covering all three (same pattern as the v8.2 `reports.md`/`positions.md` combined-story bumps).
- Three items now classified **Design Pre-Approved** on direct verification against source, not discretionary downgrade: ST-14 (theme-compliance rules already fully specified in `design_system.md`, no new decision — packaging into a Base44 prompt template only), ST-15 (both `AiDisclaimer` consumer instances' contrast fixes verified still shipped/unchanged at their approved values — `dashboard.md` v3.2, `positions.md` v2.7 — extraction carries an explicit no-visual-regression AC), and ST-11 (this re-run, per above).
- Per CLAUDE.md §2 / `stage4_backlog_slice.md`'s EPIC-03 header note (RISK-02), the Playwright coverage / staging sign-off requirement for ST-11 and ST-15's observable ACs remains a Sprint Planning / execution-phase evidence obligation independent of this gate.
- No disagreements between Product Owner and Head of UX & Design this run on any of the 27 items.
