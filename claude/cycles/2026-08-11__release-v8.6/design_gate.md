**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-08-11
**Cycle:** 2026-08-11__release-v8.6

# Design Gate Record — 2026-08-11__release-v8.6

## Gate Status: PASSED

Completed: 2026-08-11
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 | Trade plan completion rate tracking | Design Required | New data displayed (plans_created/completed/abandoned, completion_rate); placement/card decision needed | `docs/design/2026-08-11__release-v8.6/trade-plan-completion-rate-metric/decision_record.md` | `docs/specs/frontend/pages/analytics.md` v2.1 (§21) | ✅ Cleared | Head of UX & Design |
| ST-02 | AI-assisted setup thesis digest at order placement | Design Required | New UI element + changed interaction flow at order placement. §13 pre-check: covered by `ai_thesis_generation.md`'s existing §13 compliance note (already on the `strategy_rules.md` §13.5 re-attestation roster) — no fresh §13 review required | `docs/design/2026-08-11__release-v8.6/ai-thesis-digest-order-placement/ux_spec.md` | `docs/specs/frontend/pages/trade_plan.md` v1.4 (§10.5) | ✅ Cleared | Head of UX & Design |
| ST-03 | Enforce trade-plan linkage at position entry + DB-level safeguard | Design Pre-Approved | Corrective/enforcement of the already-approved entry-flow default (`BLG-FE-109`/v7.3, `trade_plan.md` §10 "Start Trade from Plan"); DB-level safeguard is backend-only; no new UX decision | N/A | `docs/specs/frontend/pages/trade_plan.md` v1.4 (§10, locked reference, unchanged by this item) | ✅ Cleared | Head of UX & Design |
| ST-04 | Register remaining unregistered shadcn design tokens in tailwind.config.js | Design Pre-Approved | Restores already-canonical design tokens (already-defined CSS custom properties in `index.css`'s shadcn theme block) broken only at the build-config level — identical root cause to v8.5 ST-06's `-muted` fix; no new visual design decision | N/A | `docs/specs/frontend/design_system.md` v1.9 (locked reference) | ✅ Cleared | Head of UX & Design |
| ST-05 | Playwright coverage for remaining -muted/-muted-foreground call sites | Design Not Applicable | Test-coverage-only story for already-shipped tokens (v8.5 ST-06); no UI change (mirrors v8.5 ST-09 audit precedent) | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-06 | Fix 6 drift instances against v6.7 canonical secondary-text token | Design Pre-Approved | Corrective work restoring an already-canonical token (`design_system.md` §Color Usage "Secondary/label text", v6.7); no new design decision | N/A | `docs/specs/frontend/design_system.md` v1.9 (locked reference, §Color Usage) | ✅ Cleared | Head of UX & Design |
| ST-07 | Design decision: should modals/dialogs support light theme? | Design Required | This item is the design decision itself — genuine design-system judgment call, no pre-existing artefact | `docs/design/2026-08-11__release-v8.6/modal-light-theme-support/decision_record.md` | `docs/specs/frontend/design_system.md` v1.9 (new "Modal / Dialog Theming" subsection) | ✅ Cleared | Head of UX & Design |
| ST-08 | Switch Layout.js's dark-class document.documentElement sync to useLayoutEffect | Design Not Applicable | Technical render-timing fix (React lifecycle hook choice) restoring already-established dark-mode intent (prevents a possible theme flash); no new UI/design decision — AC itself allows a code-comment-only outcome | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-09 | Correct st15_nav_bar_redesign_exploration.md's counts + navigation.md staleness | Design Not Applicable | Documentation correction only; no live UI change (mirrors v8.5 ST-15 exploration-doc precedent) | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 | Migrate CohortAnalysis.js from client-side computation to GET /analytics/cohort | Design Pre-Approved | Corrective architecture fix against an already-approved spec (`analytics.md` §15's existing hard rule already names the backend endpoint as canonical source, `DEV-EPIC02-ST03-01`); AC states no visual change expected | N/A | `docs/specs/frontend/pages/analytics.md` v2.1 (§15, locked reference, unchanged by this item) | ✅ Cleared | Head of UX & Design |
| ST-11 | get_regime_distribution's NULL-exclusion documented behaviour is dead code | Design Not Applicable | Backend documentation/behaviour correctness fix; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-12 | Multi-currency cost-basis rounding consistency check | Design Not Applicable | Backend financial-calculation audit/fix; restores correct already-intended values, no new UI/layout | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-13 | Closed-trade export completeness check against tax-year boundary | Design Not Applicable | Backend export correctness; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-14 | check_dependency_vuln_rescan.py silently treats a failed audit tool as "zero findings" | Design Not Applicable | CI/CD tool robustness fix; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-15 | Add endpoint-level regression test for GET /analytics/tag-performance | Design Not Applicable | Test only; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-16 | Add Playwright coverage for setNarrativeField AI-draft-badge clearing | Design Not Applicable | Test-coverage-only story for already-shipped behaviour; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-17 | Add unit tests for scripts/check_dependency_vuln_rescan.py | Design Not Applicable | Test only; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-18 | Document one-directional limitation of test_alerts_service.py's fixture | Design Not Applicable | Test-infrastructure documentation; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-19 | Align api-key-cross-environment-check.yml's alert-step grep with skip-guard's ::error:: prefix | Design Not Applicable | CI/CD workflow fix; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-20 | Document CVE-2026-4539 ignore rationale | Design Not Applicable | CI/CD documentation; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-21 | Confirm dependency-vuln-rescan.yml runs successfully post-merge | Design Not Applicable | CI/CD verification; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-22 | File retroactive DEV record for the dark-mode/Radix-portal Layout.js fix | Design Not Applicable | Governance record only; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-23 | shared_standards_changelog.md missing v3.27 entry | Design Not Applicable | Governance document fix; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-24 | execution_state.json's deviations_filed field meaning | Design Not Applicable | Governance/schema document fix; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-25 | Annotate BLG-FE-146/BLG-FE-139 with 2026-08-10 trigger-condition re-check | Design Not Applicable | Governance document annotation; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-26 | Correct BLG-GOV-288's Acceptance Criteria text | Design Not Applicable | Governance document correction; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |

**Mandatory §13 boundary pre-check (AI-calling proposals):** one item touches AI-adjacent surface area this cycle — ST-02 (digest reusing the existing Claude thesis generation service at a new touchpoint, order placement). A covering §13 review already exists and PASSed: `docs/specs/api_contracts/ai_thesis_generation.md`'s §13 compliance note (successor to `gemini_thesis_generation.md`, itself already on the `strategy_rules.md` §13.5 semi-annual re-attestation roster as "contract-documented, no standalone review record"). The design decision (§2, `ai-thesis-digest-order-placement/ux_spec.md`) deliberately reuses already-generated content rather than making a fresh inference call at order placement, keeping the item inside that existing clearance's stated scope. No fresh §13 review required; no gate-blocking flag raised.

## Blocked Items

None. All 26 items cleared on the initial run.

## Notes

- **Three genuinely new design decisions this cycle: ST-01, ST-02, ST-07.** All three are lightweight artefacts (two decision records, one ux_spec) rather than open-ended design problems — each had a narrow, well-scoped question (placement of a new metric, a reuse-vs-fresh-call decision for an AI-adjacent digest, a theming-intent decision for an existing gap). Frontend specs updated same-run: `analytics.md` 2.0→2.1, `trade_plan.md` 1.3→1.4, `design_system.md` 1.8→1.9.
- **ST-03, ST-04, ST-06, ST-10 (Design Pre-Approved):** all four are corrective/enforcement work against already-approved design intent — ST-03 strengthens an already-shipped default entry-flow pattern (`BLG-FE-109`); ST-04 restores already-canonical shadcn tokens broken only at build-config level (direct continuation of v8.5 ST-06, same root cause); ST-06 restores an already-canonical secondary-text token (v6.7); ST-10 migrates to an already-specified canonical backend source (`analytics.md` §15's existing hard rule). None required a new UX decision.
- **ST-07's design decision produced a follow-up implementation item, `BLG-FE-156`** (filed separately by PMO Lead, 2026-08-11 — `claude/backlog/backlog.md` was outside this gate's own §5 write scope, so the item was filed as a distinct follow-up action after the gate closed, not during it) — the decision record itself does not ship the 4 hardcoded-modal fixes; that is deliberately separate scope, sequenced after `BLG-FE-147`/ST-04 (this cycle) per the token-registration dependency noted in both the decision record and the backlog item.
- **ST-08 borderline note:** considered against `design_gate_prompt.md` §6's motion/timing-sensitive-interaction clause (BLG-FE-131) before classifying — that clause targets animation/debounce/delay-before-show *parameters*; a `useEffect`→`useLayoutEffect` lifecycle-hook choice for DOM class sync (preventing a possible flash-of-wrong-theme, not an interaction-timing parameter) was judged outside that clause's intent and classified Design Not Applicable, consistent with the AC's own framing (a code-comment-only outcome is an accepted resolution).
- **EPIC-04/EPIC-05/EPIC-06 (ST-11 through ST-26) all classified Design Not Applicable.** All 16 items are backend correctness fixes, test-coverage additions, CI/CD workflow fixes, or governance-document corrections with no live UI change — consistent with prior cycles' treatment of this item shape (v8.5 ST-01–ST-05, ST-09, ST-13–ST-20, ST-22–ST-25).
- **20 of 26 items carried `Provisional-Target: v8.6`** (per `decisions--2026-08-11__release-v8.6.md`) — this design gate did not re-litigate any Sprint Planning scope or sequencing decision, only design classification.
