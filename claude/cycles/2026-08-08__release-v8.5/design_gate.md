**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-08-08
**Cycle:** 2026-08-08__release-v8.5

# Design Gate Record — 2026-08-08__release-v8.5

## Gate Status: PASSED

Completed: 2026-08-08
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 | Fix `GET /analytics/tag-performance` 500 (missing `trade_tags` ensure) | Design Not Applicable | Backend bug fix (DB column ensure); restores an already-existing endpoint's intended behaviour, no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-02 | Confirm `api-key-cross-environment-check.yml` is genuinely running | Design Not Applicable | CI/CD verification; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-03 | Security fix false-positive rate assessment | Design Not Applicable | Measurement/analysis task; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-04 | Recurring dependency vulnerability re-scan cadence | Design Not Applicable | CI/CD ops (pip-audit/npm audit scheduling); no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-05 | API key rotation runbook | Design Not Applicable | Documentation only; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-06 | Register `muted`/`muted-foreground` classes in `tailwind.config.js` | Design Pre-Approved | Restores an already-canonical design token (`design_system.md` §Color Usage "secondary/label text") broken only at the build-config level; no new visual design decision — the intended appearance was already specified, just not compiling | N/A | `docs/specs/frontend/design_system.md` v1.8 | ✅ Cleared | Head of UX & Design |
| ST-07 | Frontend wiring for `thesis_model_version`/`thesis_prompt_version` on save | Design Not Applicable | Hidden metadata fields populated on save; not displayed in any UI; does not itself introduce or extend an AI-provider call (see §13 note below) | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-08 | Reconcile Monthly P&L vs Tax Year table's exact-zero P&L colour convention | Design Required | Genuine colour-convention decision (grey/neutral-for-zero vs red-for-zero) affecting live rendering on both tables; resolves `DEV-REPORTS-ST01-02` | `docs/design/2026-08-08__release-v8.5/exact-zero-pnl-colour-convention/decision_record.md` | `docs/specs/frontend/pages/reports.md` v0.16 | ✅ Cleared | Head of UX & Design |
| ST-09 | Design token audit: v6.7 contrast fix consistency | Design Not Applicable | Audit only — any drift found is filed as a separate follow-up item (which would itself pass through a future design gate); no direct UI change this story | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 | Empty-state illustration/microcopy consistency pass | Design Required | Mechanism (`DataState` `empty` branch) already consistently applied across ≥10 pages; the genuine decision was the microcopy wording/punctuation pattern, and the AC ships a live fix (`TradePlans.js`) this cycle | `docs/design/2026-08-08__release-v8.5/empty-state-microcopy-pattern/decision_record.md` | `docs/specs/frontend/design_system.md` v1.8 | ✅ Cleared | Head of UX & Design |
| ST-11 | Confirm theme-toggle persistence across sessions | Design Not Applicable | Verification of already-established behaviour; any gap found would be a bug fix against existing intent, not a new design decision | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-12 | Mobile responsive audit for PerformanceAnalytics page | Design Pre-Approved | Audits/fixes against the page's already-approved layout spec (`analytics.md`); corrective only (overflow/truncation/unusable-control fixes), no new layout or pattern introduced | N/A | `docs/specs/frontend/pages/analytics.md` v2.0 | ✅ Cleared | Head of UX & Design |
| ST-13 | Dark/light theme contrast audit follow-up | Design Not Applicable | Targeted audit confirming no further gaps beyond BLG-FE-87/88/89's already-fixed instances; no new UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-14 | Ad hoc component inventory for shared design-system extraction | Design Not Applicable | Inventory/ranking deliverable only; no component ships this cycle — any extraction candidate acted on would pass through its own future design gate | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-15 | Nav bar redesign exploration | Design Not Applicable | Exploration/recommendation document; no live UI change this cycle — if redesign is recommended, the resulting implementation item is filed and gated in a future cycle | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-16 | User journey map: SI-05 Telegram digest to app action | Design Not Applicable | Documentation deliverable (journey map); no live UI change this cycle | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-17 | Reusable empty-state component spec for Base44 prompts | Design Not Applicable | Spec-writing deliverable for future reference only ("for future Base44 prompts to reference") — no component ships or is applied this cycle; will draw on ST-10's pattern decision | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-18 | Reports page information hierarchy review | Design Not Applicable | Review/findings deliverable; AC's expected path is "fix filed as a follow-up," not an in-story visual change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-19 | Rework ChartStyle to drop CSP `unsafe-inline`, if/when a consumer adopts `ChartContainer` | Design Not Applicable | Conditional/deferred scope — `chart.js` has zero live consumers today; most likely outcome is "confirmed still unused, no action." If a consumer is adopted this cycle, re-classify as Design Required before implementation proceeds (cannot pre-approve a rendering decision for an unknown future consumer) | N/A | N/A | ✅ Cleared (conditional — see Notes) | Head of UX & Design |
| ST-20 | Playwright/staging visual verification of `calendar.js` when a consumer is added | Design Not Applicable | Deferred-trigger verification story; zero live consumers today; no UI change from this story itself | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-21 | Regime distribution metric over screener history | Design Required | New data displayed (aggregate regime view, not previously shown anywhere); genuine placement/control/colour decision needed | `docs/design/2026-08-08__release-v8.5/regime-distribution-panel/decision_record.md` | `docs/specs/frontend/pages/screener_results.md` v1.4 | ✅ Cleared | Head of UX & Design |
| ST-22 | Product Value Ratio historical trend chart | Design Not Applicable | Internal governance-tooling deliverable (Type: "Governance Tooling" per `BLG-FEAT-72`) sourced from the STEP 2.4 rebalance record — not customer-facing product UI, outside the Head of UX & Design / product frontend-spec scope this gate governs | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-23 | Release Planning does not reset root `sprint_sealed` on new-cycle publish | Design Not Applicable | Governance prompt patch (`release_planning_prompt.md` STEP 0); no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-24 | CLAUDE.md §8 sibling-vs-sibling union clause | Design Not Applicable | Governance file patch (`CLAUDE.md` §8); no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-25 | Fix unrestored `sys.modules` stubbing in `test_alerts_service.py` | Design Not Applicable | Test infrastructure fix; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |

**Mandatory §13 boundary pre-check (AI-calling proposals):** one item touches AI-adjacent surface area this cycle — ST-07 (frontend wiring to populate `thesis_model_version`/`thesis_prompt_version` on save). It does not introduce or extend a call to an AI provider — it populates metadata fields from content an existing, already-covered generation path already produced and saved; no new inference call is made. No item requires a §13 pre-check flag this run.

## Blocked Items

None. All 25 items cleared on the initial run.

## Notes

- **Three genuinely new design decisions this cycle: ST-08, ST-10, ST-21.** All three are lightweight decision records (not full UX specs) — each had a narrow, well-scoped question (a colour convention, a microcopy pattern, a placement/control choice for a new aggregate panel) rather than an open-ended design problem. Frontend specs updated same-run: `reports.md` 0.15→0.16, `design_system.md` 1.7→1.8, `screener_results.md` 1.3→1.4.
- **ST-06 and ST-12 (Design Pre-Approved):** both are corrective work against already-approved design intent — ST-06 restores a token that was already canonical but not compiling; ST-12 fixes responsive defects against the page's existing, unchanged layout spec. Neither required a new UX decision.
- **EPIC-05 (ST-15/16/17/18) all classified Design Not Applicable, despite being owned by Head of UX & Design.** These are UX research/documentation deliverables in their own right (exploration, journey mapping, spec-writing, review) rather than implementation stories that need a pre-approved artefact before they can safely ship code. None of the four AC sets ship a live UI change this cycle (ST-18's "any fix filed as a follow-up" language treats deferral as the expected path, not an in-story visual change). Any resulting implementation work identified by these stories (e.g. a nav redesign recommended by ST-15, or a friction fix found by ST-16) is filed as a separate backlog item and will pass through its own design gate when scheduled.
- **ST-19 conditional scope:** flagged in the classification table rather than silently pre-cleared, since its classification genuinely depends on an unknown (whether a `ChartContainer` consumer is adopted this cycle). If sprint execution finds a consumer has been adopted, Sprint Planning/execution should treat the rendering-and-colour question as needing a fresh design pass before implementing, not proceed on this gate's Design Not Applicable clearance — the "no action needed" outcome is what's cleared here, not a hypothetical redesign.
- **ST-22 scope boundary (governance tooling, not product UI):** confirmed via `backlog.md`'s `BLG-FEAT-72` entry (`Type: Product Feature / Governance Tooling`, sourced from the STEP 2.4 rebalance record) — this is an internal PMO/governance artefact, not a feature of the trading app itself, so it sits outside this gate's product-UX scope. Distinguished from ST-21 (`BLG-FEAT-29`, `Type: Product Feature / Analytics`), which is genuinely in-app and is classified Design Required.
- **ST-21 taxonomy correction:** `BLG-FEAT-29`'s problem statement describes a "bull/bear/neutral/volatile" regime taxonomy; the system's actual regime model (`strategy_rules.md` §8.2/§11, `screener_results.md` §4) is binary — risk-on/risk-off, driven by the relevant index's 200-day moving average. The design decision (and the resulting `screener_results.md` §5.0 spec addition) is against the real binary model, not the illustrative four-way one named at idea-intake time. Recommend the backlog item's own wording be corrected for future readers — not filed as a separate follow-up (a documentation clarity note, not a defect), the correction is recorded here and in the decision record itself.
