**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-08-04
**Cycle:** 2026-08-04__release-v8.2

# Design Gate Record — 2026-08-04__release-v8.2

## Gate Status: PASSED

Completed: 2026-08-04
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 | P&L / tax record reconciliation report (system totals vs individual trade export) | Design Required | Genuinely new user-facing view — no prior artefact or spec section existed for this specific system-total-vs-export-total comparison (the existing `reports.md` reconciliation prose covers different pairs: Monthly-vs-Tax-Year CSV, and Combined Total vs `total_pnl`) | `docs/design/2026-08-04__release-v8.2/pnl-reconciliation-report/decision_record.md` | `docs/specs/frontend/pages/reports.md` v0.13 | ✅ Cleared | Head of UX & Design |
| ST-02 | Compliance Recheck Modal all-pass empty-state design | Design Required | `ComplianceRecheckModal.js` had confirmed designs for Loading/Error/Warn/Fail but no deliberate design for the all-pass case (verified against source — code silently omitted any equivalent-slot content); genuine gap, not a documentation lag | `docs/design/2026-08-04__release-v8.2/compliance-recheck-all-pass-state/decision_record.md` | `docs/specs/frontend/pages/positions.md` v2.7 | ✅ Cleared | Head of UX & Design |
| ST-03 | RFJ event type colour palette refinement | Design Pre-Approved | Full colour mapping already decided and approved in the v6.0 RFJ design review (`docs/design/2026-06-19__release-v6.0/rfj-design-review/review.md`, Head of UX & Design sign-off 2026-06-22), which explicitly states the fix "does not require a sprint story or UX spec — it is a 3-line CSS change." This story (BLG-FE-67) is that already-approved fix, only now being implemented — verified current colours in `RedFlagJournal.js` still match the pre-fix state named in the review (`orange-400`/`rose-400`), confirming no drift since approval | `docs/design/2026-06-19__release-v6.0/rfj-design-review/review.md` (existing, unchanged) | N/A — `red_flag_journal.md` does not document colour tokens; no spec update required, existing design review governs | ✅ Cleared | Head of UX & Design |
| ST-04 | Trade Plan native form fields use a weaker focus indicator than the rest of the codebase | Design Pre-Approved | `design_system.md` v1.4 (§Focus indicator contrast, BLG-FE-127, v7.8) already mandates the `focus-visible:ring-*` pattern at ≥3:1 contrast for all keyboard-focusable elements; verified `TradePlan.js:217`'s checklist checkbox uses the older `focus:ring-amber-500/30` pattern instead of the shared `focus-visible:ring-ring` token used by `src/components/ui/{input,button}.js` — an implementation bug against an already-approved spec, not new UX work (same pattern as the v8.1 ST-01 precedent) | N/A (existing spec governs) | `docs/specs/frontend/design_system.md` v1.4 (unchanged) | ✅ Cleared | Head of UX & Design |
| ST-05 | Drift-detection metric for the behavioural-drift endpoint's `insufficient_data` streak | Design Pre-Approved | "Surfaced alongside the existing SI-02 gate note" reuses the SI-02 Gate Status section's existing stat-grid display pattern (`reports.md` §SI-02 Gate Status v0.12 — verified in `Reports.js`'s `SI02GateStatusSection`, a `text-xs uppercase` label / `text-lg font-semibold` value grid) verbatim; adding one more stat card in the same visual style is not a new UX decision (same pattern as the v8.1 ST-14 precedent). Sign-off owner is Metrics Definitions & Analytics Canonical Owner, consistent with this being a metric-definition task, not new design | N/A (existing spec governs) | `docs/specs/frontend/pages/reports.md` v0.13 (unchanged; version bump deferred to sprint execution when the stat is actually added, matching v8.1 ST-14 precedent) | ✅ Cleared | Head of UX & Design |
| ST-06 | Provision a distinct API key for the staging environment | Design Not Applicable | Infrastructure/credential rotation; no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-07 | Detect silent staging deploy staleness | Design Not Applicable | CI/infra drift-detection check; no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-08 | File SI-05 Phase 1 30-day effectiveness review record | Design Not Applicable | Governance review record; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-09 | `velocity_metrics.md` row-count audit against cycle folder count | Design Not Applicable | Governance/process audit; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 | Confirm Arc 5 composite formula accounts for v6.9 recheck events | Design Not Applicable | Metrics-definition formula review; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-11 | Rebalance-skip advisory should verify next release is actually scoped | Design Not Applicable | Governance prompt logic amendment (`post_ship_closure.md`); no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-12 | AI vendor Terms-of-Service & data-processing review | Design Not Applicable | Compliance/legal review; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-13 | Direct-write / governance-bypass pattern tracker | Design Not Applicable | Governance process log; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-14 | Idea-intake backlog-overlap check effectiveness retrospective | Design Not Applicable | Governance process retrospective; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-15 | SI-02 production credential provisioning decision | Design Not Applicable | Governance/infra decision record; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-16 | Mandatory §13 boundary pre-check at design gate for new AI-calling feature proposals | Design Not Applicable | Amendment to this engine's own prompt (`design_gate_prompt.md`); no product UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-17 | Codify a `Last Updated` header-history retention convention | Design Not Applicable | Governance documentation convention; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-18 | governance_sync.yml auto-close regex cannot distinguish delegation-record commits | Design Not Applicable | CI/CD automation fix; no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-19 | Quarterly dependency-upgrade cadence for backend/requirements.txt | Design Not Applicable | Process/ops cadence documentation; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-20 | CI cache tuning to reduce Playwright suite runtime | Design Not Applicable | CI/CD configuration; no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-21 | Automated commit-message format lint | Design Not Applicable | CI/CD pre-commit hook; no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-22 | Snapshot test for `SystemStatus.js` hardcoded fallback counts | Design Not Applicable | Test infrastructure only; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-23 | Reconstruct 13 undocumented versions in sprint_planning_changelog.md | Design Not Applicable | Documentation reconstruction; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-24 | Remove dead-code duplicate POST /test/endpoints handler | Design Not Applicable | Backend dead-code removal; no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-25 | Design-gate checklist addendum for motion/timing-sensitive chart interactions | Design Not Applicable | Amendment to this engine's own prompt (`design_gate_prompt.md`); no product UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |

## Blocked Items (if any)

None.

## Notes

- Two items classified **Design Required** this cycle: ST-01 (genuinely new reconciliation view, no prior artefact) and ST-02 (genuine gap in an otherwise-designed modal — confirmed against `ComplianceRecheckModal.js` source, not just the spec, that the all-pass case had no deliberate treatment). Both received lightweight decision records (per the v8.0 `entry-checklist-keyboard-accessibility`/`abandon-modal-focus-trap` precedent — interaction/content decisions reusing existing visual language, not new wireframes) and same-run frontend spec updates: `reports.md` 0.12→0.13, `positions.md` 2.6→2.7 (Head of Specs Team confirmed lifecycle compliance on both — correct class, version increment, Last Updated).
- ST-03 was the one borderline candidate resolved to **Design Pre-Approved** rather than Design Required: on inspection, its exact colour-mapping fix was already fully designed and Head-of-UX-signed-off in the v6.0 RFJ design review (`rfj-design-review/review.md`), which explicitly waived the UX-spec requirement for this specific change ("does not require a sprint story or UX spec — it is a 3-line CSS change"). Live code was checked against that review's stated pre-fix colours (`orange-400`/`rose-400`) to confirm no drift since approval before accepting the classification.
- ST-04 and ST-05 were also resolved to **Design Pre-Approved** on direct verification against source, not by discretionary downgrade: ST-04 against `design_system.md` v1.4's already-mandated `focus-visible` pattern (confirmed `TradePlan.js:217` is the non-compliant outlier, shared primitives already correct); ST-05 against `Reports.js`'s existing `SI02GateStatusSection` stat-grid pattern (confirmed the new metric is a same-pattern addition, not a new UI decision).
- Per CLAUDE.md §2, the Playwright coverage / staging sign-off requirements named in the `stage4_backlog_slice.md` header (RISK-01) for ST-01 through ST-04's observable ACs remain a Sprint Planning / execution-phase evidence obligation independent of this gate — this gate confirms the design/interaction contract only, not test evidence.
- No disagreements between Product Owner and Head of UX & Design this run; no item required a discretionary downgrade below the §6 default — every Pre-Approved classification rests on a verified existing artefact or pattern, not judgement alone.
