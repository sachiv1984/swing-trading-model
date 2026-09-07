**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-09-07
**Cycle:** 2026-09-07__release-v9.2

# Design Gate Record — 2026-09-07__release-v9.2

## Gate Status: PASSED

Completed: 2026-09-07
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

56 of 56 items cleared — 2 Design Required (ST-01, ST-05 — artefacts produced this run, both conditional/standard-setting decisions per precedent), 3 Design Pre-Approved (ST-02, ST-03, ST-04 — semantic-only accessibility fixes and a known-deviation spec correction, no visual/behavioural change, existing conventions govern), 51 Design Not Applicable (pure backend/CI-CD/test-coverage/governance-process/documentation/ops items with no user-visible effect). No blocked items. `sprint_planning_pre_condition` is met.

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 | Arc 5 compliance score utility advisory at low trade volume | Design Required | Assessment's conclusion (advisory warranted or not) not yet known at gate time; default per §6 for a conditional new-UI-element outcome, matching the `2026-08-21__release-v9.0` ST-03/ST-07/ST-10 pattern. Design fixed in advance so execution isn't blocked pending a second gate pass. | `docs/design/2026-09-07__release-v9.2/arc5-low-volume-advisory/decision_record.md` | `docs/specs/frontend/components/arc5_compliance_section.md` v1.1.0 (locked reference at gate time; bumped during execution only if the assessment confirms the advisory ships) | ✅ Cleared | Head of UX & Design |
| ST-02 | Settings page heading-order axe-core finding | Design Pre-Approved | Semantic heading-tag correction only; AC explicitly requires no visual/layout regression (equivalent styling preserved via className) | N/A | `docs/specs/frontend/pages/settings.md` v1.6 (locked, unchanged) | ✅ Cleared | Head of UX & Design |
| ST-03 | aria-label duplicates visible label text (TradePlan.js, Settings.js) | Design Pre-Approved | `aria-labelledby` in place of hardcoded `aria-label` string is an accessible-name mechanism swap with no visible text, layout, or interaction change; `design_system.md`'s existing ARIA-labelling principle already governs — same basis as `2026-09-03__release-v9.1` ST-02/ST-03 | N/A | `docs/specs/frontend/pages/trade_plan.md` v1.12, `docs/specs/frontend/pages/settings.md` v1.6 (both locked, unchanged) | ✅ Cleared | Head of UX & Design |
| ST-04 | Arc5ComplianceSection "Top Rule Breach" card diverges from canonical spec | Design Pre-Approved | Divergence is already documented as a Known Deviation in the spec itself (v1.1.0, target resolution v9.2), which notes the live implementation's spaced-text/em-dash-null behaviour has "no functional/data impact" and already matches the null-display convention used by the component's other three cards. Resolution direction: correct the spec to match the already-shipped, tested, sibling-consistent implementation — no code/UI change. Head of UX & Design confirms this direction rather than requiring an implementation change to match the original spec wording. | N/A | `docs/specs/frontend/components/arc5_compliance_section.md` v1.1.0 (bumped to reflect resolved Known Deviation during execution) | ✅ Cleared | Head of UX & Design |
| ST-05 | Motion-vs-contrast trade-off (entrance fade-in animations) — no design_system.md guideline | Design Required | Motion/timing-sensitive-interaction special rule (§6, BLG-FE-131) — always Design Required regardless of whether a shipped animation actually changes. Standard/scope fixed at gate (mirrors `2026-07-24__release-v7.8` ST-03/ST-04 audit-standard-setting pattern); guideline prose (or explicit no-guideline-needed decision) is the story's own execution deliverable. | `docs/design/2026-09-07__release-v9.2/motion-contrast-guideline-standard/decision_record.md` | `docs/specs/frontend/design_system.md` v1.11 (locked reference at gate time; bumped during execution with the guideline content) | ✅ Cleared | Head of UX & Design |
| ST-06 | playwright.yml CI trigger path filter excludes package.json/package-lock.json | Design Not Applicable | CI/CD workflow trigger-path fix, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-07 | accessibility-axe-scan.spec.js fixed-sleep → condition-based wait | Design Not Applicable | Test-infrastructure timing fix; existing scans must pass unchanged, no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-08 | Arc5ComplianceSection Playwright tests use unscoped text selectors | Design Not Applicable | Test-selector scoping fix, no product/UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-09 | governance_sync.yml over-closing prevention unverified in real CI | Design Not Applicable | CI regression-test coverage, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 | governance_sync.yml split-commit story-issue close gap | Design Not Applicable | CI/CD workflow fix, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-11 | check_specs_index_freshness.py has zero test coverage | Design Not Applicable | Test coverage for existing tooling script, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-12 | Regression suite runtime budget & trend report | Design Not Applicable | Internal QA reporting artefact, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-13 | DEV-* deviation recurrence pattern report | Design Not Applicable | Internal QA reporting artefact, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-14 | pip-audit trend log across sprint-planning runs | Design Not Applicable | Process logging convention, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-15 | DoQ sign-off template alignment check | Design Not Applicable | Process/documentation check, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-16 | Staging sign-off backlog tracker (FI-P3-02 exceptions) | Design Not Applicable | Internal tracker artefact, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-17 | Quarterly model/prompt-drift compliance attestation log | Design Not Applicable | Governance documentation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-18 | Deprecation header convention for retiring API endpoints | Design Not Applicable | Governance/spec convention documentation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-19 | Formal expiry review for §13-adjacent initiatives open >2 cycles | Design Not Applicable | Governance process check, no UI. §13 pre-check: reviews process cadence around existing §13 items, does not itself introduce/extend an AI-provider call — pre-check does not apply. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-20 | stage4_backlog_slice.md post-gate-correction addendum mechanism | Design Not Applicable | Governance prompt patch (`design_gate_prompt.md`), no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-21 | AI response caching evaluation for morning briefing | Design Not Applicable | Evaluation document only; no UI. §13 pre-check: evaluates caching for an already-shipped AI feature, does not introduce/extend an AI-provider call — pre-check does not apply. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-22 | Gemini AI usage audit-trail retention policy | Design Not Applicable | Policy documentation, no UI. §13 pre-check: retention policy for existing AI usage logs, does not introduce/extend an AI-provider call — pre-check does not apply. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-23 | Standardise api_changelog.md entry template | Design Not Applicable | Documentation convention, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-24 | Frame Skill-Silo Alert as workload-composition, not just product-mix | Design Not Applicable | Governance prompt patch (`roadmap_prompt.md`), no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-25 | Governance-cycle wall-clock cost logging | Design Not Applicable | Process logging convention, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-26 | Product Value Ratio historical trend row in velocity_metrics.md | Design Not Applicable | Internal metrics documentation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-27 | Surface meta-review countdown in every run_manifest.md | Design Not Applicable | Governance prompt patch (`roadmap_prompt.md`), no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-28 | Data-retention policy for closed-trade and journal records | Design Not Applicable | Policy documentation only, no implementation this cycle, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-29 | Onboarding checklist for new governance agent roles | Design Not Applicable | Governance process documentation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-30 | Periodic §13 boundary review cadence tied to SI-02's gate history | Design Not Applicable | Governance process documentation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-31 | Due-date index for outstanding deferred-patch reminders | Design Not Applicable | Internal index artefact, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-32 | Agent onboarding runbook for adding a new governance role | Design Not Applicable | Governance process documentation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-33 | Recurring spec-debt backlog review cadence | Design Not Applicable | Governance prompt patch (`backlog_management_prompt.md`), no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-34 | Searchable index of STEP 11.4 meta-review findings | Design Not Applicable | Internal index artefact, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-35 | Document skill-category taxonomy for Skill-Silo classification | Design Not Applicable | Internal metrics documentation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-36 | AI feature cost-vs-value retrospective (6-month actuals) | Design Not Applicable | Retrospective document only, no UI. §13 pre-check: reviews already-shipped AI features' cost/value, does not introduce/extend an AI-provider call — pre-check does not apply. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-37 | Formal alert threshold for cross-role workload-concentration check | Design Not Applicable | Governance prompt patch (`roadmap_prompt.md` §7.2), no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-38 | Formalise condensed-tier trigger thresholds | Design Not Applicable | Governance process review, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-39 | Data-volume threshold trigger for §12.2 review | Design Not Applicable | Governance prompt patch (§12.2), no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-40 | Product Value Ratio rolling-window boundary-trade handling | Design Not Applicable | Internal metrics-definition documentation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-41 | strategy_rules.md version cross-reference consistency check | Design Not Applicable | Governance tooling/process check, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-42 | Strategy rules change-justification template | Design Not Applicable | Governance documentation template, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-43 | Deprecated/superseded endpoint sunset tracker | Design Not Applicable | Internal tracker artefact, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-44 | Contract example-payload freshness check against live response shape | Design Not Applicable | Tooling/process check, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-45 | Base44 prompt-version provenance tag on generated components | Design Not Applicable | Internal tooling convention, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-46 | Base44 regeneration diff checklist — design-token compliance pass | Design Not Applicable | Internal process checklist (uses existing design_system.md tokens as reference, adds no new token/pattern), no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-47 | Component prop-naming convention consistency audit | Design Not Applicable | Internal code-convention audit + documentation, no UI/behavioural change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-48 | Gate-metric naming consistency across roadmap, SI-05 digest, Reports page | Design Not Applicable | Naming/terminology standardisation, no visual/layout/interaction change anticipated | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-49 | Populate Specs_Index.md with 78 unregistered spec files | Design Not Applicable | Documentation-index bookkeeping, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-50 | Scope a future migration off Create React App | Design Not Applicable | Scoping document only, no implementation this cycle, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-51 | Unexplained package-lock.json "dev": true churn | Design Not Applicable | Dependency-resolution investigation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-52 | Remove unused namesquatted/erroneous npm packages | Design Not Applicable | `package.json`/`package-lock.json` cleanup, build must succeed unchanged, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-53 | AI cost-threshold alert value review | Design Not Applicable | Threshold review/documentation, no UI. §13 pre-check: reviews an existing cost-alert threshold, does not introduce/extend an AI-provider call — pre-check does not apply. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-54 | AI endpoint cost & latency drift monitoring | Design Not Applicable | Monitoring/anomaly-check scoping, no UI. §13 pre-check: monitors existing AI-invoking endpoints, does not introduce/extend an AI-provider call — pre-check does not apply. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-55 | Staging environment data-reset cadence review | Design Not Applicable | Ops process review, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-56 | AI feature cost-trend tracking has not kept pace with feature shipping | Design Not Applicable | Cost-trend documentation update, no UI. §13 pre-check: tracks cost of existing AI-invoking endpoints, does not introduce/extend an AI-provider call — pre-check does not apply. | N/A | N/A | ✅ Cleared | Head of UX & Design |

## Blocked Items

None.

## Notes

- **§13 pre-check scope:** Every item was checked against the mandatory §13 boundary pre-check (STEP 1). No item in this cycle's 56-item scope introduces or extends a call to an AI/LLM provider — the AI-adjacent items (ST-19, ST-21, ST-22, ST-36, ST-53, ST-54, ST-56) all evaluate, monitor, or document already-shipped AI touchpoints rather than adding a new one. Flagged individually in the Rationale column above for traceability.
- **Motion/timing-sensitive interactions (§6, BLG-FE-131):** ST-05 is the only item this cycle touching motion/timing subject matter — it is classified Design Required per the special rule even though no shipped animation parameter is being changed this cycle (the story authors a guideline, or an explicit no-guideline-needed decision). No other item in scope touches animation easing/duration, debounce/throttle intervals, or delay-before-show thresholds.
- **Conditional-outcome items (ST-01):** design fixed in advance of the story's own assessment conclusion, per the `2026-08-21__release-v9.0` ST-03/ST-07/ST-10 precedent for items whose need for new UI is not yet determined at gate time. If the assessment or implementation surfaces a treatment beyond the `StandingAlert` Info-tone reuse recorded in the decision record, it must return to this gate before merge.
- **Known-deviation resolution (ST-04):** the spec/implementation divergence was already documented as a Known Deviation in `arc5_compliance_section.md` v1.1.0 with a v9.2 target resolution release. This gate confirms the resolution direction (correct the spec to the already-shipped, tested behaviour) rather than requiring an implementation change — Design Pre-Approved on that basis.
- **Frontend specs:** two page/component specs are referenced as locked reference versions at gate time for possible bump during execution — `arc5_compliance_section.md` v1.1.0 (ST-01 conditional, ST-04 confirmed) and `design_system.md` v1.11 (ST-05). `settings.md` v1.6 and `trade_plan.md` v1.12 are referenced as locked, unchanged (ST-02, ST-03).
- **Design artefacts:** `docs/design/2026-09-07__release-v9.2/arc5-low-volume-advisory/decision_record.md` and `docs/design/2026-09-07__release-v9.2/motion-contrast-guideline-standard/decision_record.md` produced this run for the two Design Required items.
