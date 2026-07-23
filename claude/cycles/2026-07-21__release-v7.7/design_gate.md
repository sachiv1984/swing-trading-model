**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-07-21
**Cycle:** 2026-07-21__release-v7.7

# Design Gate Record — 2026-07-21__release-v7.7

## Gate Status: PASSED

Completed: 2026-07-21
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 (EPIC-01, BLG-FEAT-75) | SI-04 strategy-version performance comparison view | Design Required | New comparison view, new data displayed (version-vs-version metrics never previously surfaced) | `docs/design/2026-07-21__release-v7.7/si04-strategy-version-comparison/ux_spec.md` | `docs/specs/frontend/pages/strategy_benchmark.md` v0.4 | ✅ Cleared | Head of UX & Design |
| ST-02 (EPIC-02, BLG-FE-114) | Remove nav duplication, unify digest/notification concepts | Design Required | Modified nav layout/grouping, changed cross-surface interaction flow | `docs/design/2026-07-21__release-v7.7/nav-notification-digest-consolidation/ux_spec.md` | `docs/specs/frontend/pages/navigation.md` v1.4, `docs/specs/frontend/pages/notifications.md` v0.5, `docs/specs/frontend/pages/weekly_digest.md` v0.2 | ✅ Cleared | Head of UX & Design |
| ST-03 (EPIC-03, BLG-FE-113) | AiDailyBriefing light-theme contrast staging check | Design Pre-Approved (downgraded from default Design Required — explicit confirmation, see rationale) | Existing, already-specified component (`dashboard.md` §5 v3.1); verification pass against an already-established light/dark token convention already used on this exact card, not new design work | `docs/design/2026-07-21__release-v7.7/ai-daily-briefing-light-theme/ux_spec.md` (decision record; no wireframe required) | `docs/specs/frontend/pages/dashboard.md` v3.1 (locked spec reference, unchanged) | ✅ Cleared | Head of UX & Design |
| ST-04 (EPIC-04, BLG-FE-120) | Shared "standing alert" component | Design Required | New shared UI component/primitive | `docs/design/2026-07-21__release-v7.7/standing-alert-component/ux_spec.md` | `docs/specs/frontend/design_system.md` — **not updated this run**; design_system.md sits outside `docs/specs/frontend/pages/` (§5 write scope) and is updated during Sprint Execution per precedent (v7.5's command-palette `DataState` `inline` variant landed in the `[EPIC-01][ST-01]` execution commit, not that cycle's design gate commit). Artefact above is the locked spec reference for ST-04's implementation to transcribe into `design_system.md` (target: v1.2 → v1.3). | ✅ Cleared | Head of UX & Design |
| ST-05 (EPIC-05, BLG-FEAT-80) | SI-02 gate acceleration nudge feasibility review | Design Not Applicable | Investigation/recommendation output only — no shipped UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-06 (EPIC-06, BLG-OPS-108) | CI curl response validation (daily-snapshot.yml) | Design Not Applicable | CI/CD workflow change, no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-07 (EPIC-07, BLG-GOV-28) | PT-04 §13 compliance review (retroactive) | Design Not Applicable | Governance/documentation review against existing shipped code, no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-08 (EPIC-08, BLG-QA-104) | numpy-scalar regression coverage | Design Not Applicable | Backend/test-only, no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-09 (EPIC-09, BLG-BE-63) | Nightly backtest job idempotency check | Design Not Applicable | Backend audit/test, no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 (EPIC-10, BLG-OPS-110) | Nightly backtest monitoring/alerting | Design Not Applicable | Infrastructure/observability, no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-11 (EPIC-11, BLG-QA-102) | Endpoint-count drift check CI lint step | Design Not Applicable | CI/CD tooling, no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |

All 11 items classified. Consistent with `stage4_backlog_slice.md`'s own framing (EPIC-01–04 conditional on Design Gate PASS per RISK-02, all four carry observable UI ACs; EPIC-05–11 explicitly no Design Gate dependency). One disagreement from the §6 default rule: ST-03 downgraded from Design Required to Design Pre-Approved — Product Owner and Head of UX & Design both confirmed (see Item Classification Summary rationale and the item's own decision record).

## Blocked Items

None.

## Notes

**BLG-FE-59 status (informational, not a blocker):** EPIC-01's own AC referenced BLG-FE-59 (Arc5ComplianceSection extension spec for SI-02/SI-04) as one of two placement options. BLG-FE-59 remains an unscheduled backlog item — not in this cycle's `stage4_backlog_slice.md`. Resolved by choosing the AC's "dedicated comparison view" alternative instead (see `si04-strategy-version-comparison/ux_spec.md` §2), which avoids pulling an out-of-scope item into v7.7. No action needed against BLG-FE-59 itself this cycle; it remains available for a future `Arc5ComplianceSection` card if executed later.

**API contract gap flagged for Sprint Execution (not a Design Gate blocker):** `docs/specs/api_contracts/strategy_version_comparison_contract.md` v0.1.0 (pre-sprint draft) does not include a `compliance_rate` field, which ST-01's AC requires ("win rate, average R, and compliance rate per version"). This routine's write scope excludes `docs/specs/api_contracts/` (§5), so the contract could not be amended here. The frontend spec (`strategy_benchmark.md` §7.5) accommodates this by rendering the field as pending (`—`) until the contract is updated (0.1.0 → 0.2.0, `compliance_rate` added to both version metric objects) during EPIC-01 implementation. Sourcing decision (journal-completion-rate style vs. Arc 5 composite score) needs Strategy Rules & System Intent Owner confirmation at that time.

**Second API contract gap flagged for Sprint Execution (not a Design Gate blocker):** the Notification Feed endpoint (`GET /notifications`, `alerts_endpoints.md`) needs two new optional query params (`since_days`, `read`) added to support ST-02's Weekly Digest deep-links (`weekly_digest.md` v0.2 §2). Small additive filter, in scope for ST-02's own implementation; flagged here so the contract update lands in the same commit as the frontend change per CLAUDE.md §2, rather than being missed.

**Real bug confirmed during audit (informs ST-02 implementation, not a new finding requiring its own classification):** `src/Layout.js` `NAV_GROUPS` was inspected directly to ground ST-02's design decisions. Confirmed: "Alerts" (Tools group) and "Notifications" (System group) both hard-route to `page: "notifications"` with identical `Bell` icon and no distinguishing visual treatment — exactly the duplication AC1 describes. This is the concrete basis for the nav consolidation decisions in `nav-notification-digest-consolidation/ux_spec.md`.

**Write-scope correction during this run:** `design_system.md` was initially updated in error (Standing Alert component, ST-04) and then reverted — it sits outside `docs/specs/frontend/pages/`, the §5 write-scope boundary for this routine, and is a Sprint Execution update per the v7.5 precedent noted in the classification table above. No other file was affected by the correction.

No escalations raised. No items require sprint-execution follow-up beyond standard implementation of what is now specified, plus the two flagged contract gaps and the design_system.md transcription above.
