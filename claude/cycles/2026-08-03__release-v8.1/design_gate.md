**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-08-03
**Cycle:** 2026-08-03__release-v8.1

# Design Gate Record — 2026-08-03__release-v8.1

## Gate Status: PASSED

Completed: 2026-08-03
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 | Trade Plan tag-suggestion buttons use `onMouseDown`, not keyboard-operable | Design Pre-Approved | `docs/specs/frontend/components/journal_components.md` §4 already mandates "Suggestion list is keyboard navigable" (unchanged since v1.1, 2026-03-18); `TradeEntry.js` already implements the correct `onClick` pattern. This is an implementation bug against an already-approved spec, not new UX work — no new decision or artefact required | N/A (existing spec governs) | `docs/specs/frontend/components/journal_components.md` v1.1 (unchanged) | ✅ Cleared | Head of UX & Design |
| ST-02 | Recurring manual `pg_dump` backup schedule for production Supabase | Design Not Applicable | Infrastructure/ops runbook; no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-03 | Formal sunset criteria for perennially-returning gated backlog items | Design Not Applicable | Governance process definition; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-04 | Escalation path for Product Value Ratio's persistent Advisory tier | Design Not Applicable | Governance process/prompt drafting; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-05 | Minimum capacity buffer floor recommendation for sprint planning | Design Not Applicable | Governance process recommendation; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-06 | Technical debt registry (consolidated cross-cycle view) | Design Pre-Approved | Internal consolidated registry/document pulling existing backlog categories into one view; no UI shipped by this item | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-07 | Skill-Silo mitigation: rotate execution-heavy story assignment pattern | Design Not Applicable | Governance process guideline documentation; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-08 | Automated PII scan gate for new backend endpoints | Design Not Applicable | CI/CD check on `openapi.yaml` schemas; no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-09 | Governed write path for a non-empty, unversioned Now-horizon carry-forward | Design Not Applicable | Governance process/prompt amendment; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 | Staging sign-off: custom price alert live delivery firing | Design Not Applicable | QA verification task against an already-shipped feature; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-11 | Recurring pre-sprint-planning endpoint test coverage audit | Design Not Applicable | QA/CI process audit; no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-12 | Cross-EPIC deviation (DEV-*) consolidation review across cycles | Design Not Applicable | QA process review; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-13 | Post-parallelization Playwright shard balance audit | Design Not Applicable | Test infrastructure/CI only; no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-14 | Revisit SI-02 Gate Status Condition 2/3 threshold definitions | Design Pre-Approved | `reports.md` v0.6 SI-02 Gate Status section (MET/NOT MET badges) already designed and shipped; AC-01 is a product/spec threshold-value decision (`strategy_rules.md`); AC-02's conditional UI update reuses the existing already-approved badge display — no new UX decision | N/A | `docs/specs/frontend/pages/reports.md` v0.6 (unchanged; version bump only if AC-02 UI update fires) | ✅ Cleared | Head of UX & Design |
| ST-15 | Explicit §13 continuity note for v6.9 on-demand recheck | Design Not Applicable | `strategy_rules.md` documentation note; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-16 | Formally define SI-02 condition-3 "sufficient data" threshold | Design Not Applicable | `strategy_rules.md` §5 spec definition; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-17 | Standardise pagination pattern across list endpoints (consolidated) | Design Not Applicable | Backend pattern + helper/dependency; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-18 | `trade_plans.position_id` historical backfill design | Design Not Applicable | Backend/data scoping document; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-19 | Implement per-EPIC `execution_state.json` files (Option 1) | Design Not Applicable | Governance/engineering process mechanism; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |

## Blocked Items (if any)

None.

## Notes

- No items classified **Design Required** this cycle. ST-01 and ST-14 were the only borderline candidates (both touch existing, already-shipped UI surfaces) and both cleared as **Design Pre-Approved** on direct verification: ST-01 against `journal_components.md` §4 (keyboard-navigable suggestion list already mandated, `TradeEntry.js` already the correct reference implementation — `TradePlan.js` is simply non-compliant with an existing spec); ST-14 against `reports.md` v0.6 (SI-02 Gate Status badge display already designed — only the underlying threshold *value* is under product review, with the UI update conditional and, if it fires, a reuse of the existing display pattern rather than a new one).
- Per CLAUDE.md §2, ST-01's Playwright coverage / recorded staging sign-off requirement (RISK-01, stage4_backlog_slice.md header) remains a Sprint Planning / execution-phase evidence obligation independent of this gate — this gate confirms the design/interaction contract only (i.e., that no new design decision or spec update is owed), not test evidence.
- ST-14 AC-02's frontend spec version bump for `reports.md` is deferred to sprint execution and is conditional on whether the product review actually changes the threshold values — if it does, the Design Pre-Approved classification does not exempt that change from the same-commit frontend spec update rule; it only confirms no *new* UX decision is required to make it.
- No disagreements between Product Owner and Head of UX & Design this run; no borderline item required a downgrade below the §6 default (both borderline items were resolved to Pre-Approved on evidence of an already-approved, unchanged spec, not by a discretionary downgrade from Design Required).
