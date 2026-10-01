**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-10-01
**Cycle:** 2026-09-30__release-v9.9

# Design Gate Record — 2026-09-30__release-v9.9

## Gate Status: PASSED

Completed: 2026-10-01
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 (BLG-BE-135) | Consolidate ATR implementations; persist recalculation timestamp; expose atr/multiplier/timestamp on GET /positions | Design Pre-Approved | Backend consolidation + API field additions; no frontend component scoped in this item's AC | N/A | N/A (backend-only) | ✅ Cleared | Head of UX & Design |
| ST-02 (BLG-BE-131) | GET /reports/monthly-pnl year bounds check | Design Not Applicable | Pure backend validation/error-handling fix, no user-visible UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-03 (BLG-BE-132) | gemini_service.py Telegram alert timeout → utils.upstream_call | Design Not Applicable | Internal timeout-sourcing refactor; explicitly no behaviour change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-04 (BLG-BE-133) | utils/pricing.py ATR-fallback timeout → utils.upstream_call | Design Not Applicable | Internal timeout-sourcing refactor; explicitly no behaviour change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-05 (BLG-BE-134) | alpaca_paper_sync_service.py timeouts → utils.upstream_call | Design Not Applicable | Internal timeout-sourcing refactor; explicitly no behaviour change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-06 (BLG-SEC-40) | Non-registry dependency guard residual gaps | Design Not Applicable | CI/CD guard hardening, no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-07 (BLG-OPS-172) | POST /ai/check-daily-cost dedup guard | Design Not Applicable | Backend dedup logic on an external (Telegram) notification path, no app UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-08 (BLG-OPS-173) | POST /ai/check-endpoint-anomalies dedup guard | Design Not Applicable | Backend dedup logic on an external (Telegram) notification path, no app UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-09 (BLG-OPS-174) | POST /price-alerts dedup guard | Design Not Applicable | Backend dedup logic, no app UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 (BLG-QA-203) | GET /reports/tax-year 500 against own fixture | Design Not Applicable | Backend/test defect fix, no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-11 (BLG-QA-185) | strategy_rules.md §4–§8 test traceability matrix | Design Not Applicable | Documentation/test artefact only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-12 (BLG-QA-186) | Property-based tests — stop-never-decreases, sizing validity | Design Not Applicable | Backend test coverage only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-13 (BLG-QA-189) | Real-Postgres integration test — reflection-reminder eligibility | Design Not Applicable | Backend test coverage only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-14 (BLG-QA-190) | Convert remaining sys.modules["database"] swap pattern test files | Design Not Applicable | Backend test-isolation refactor only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-15 (BLG-QA-191) | Test coverage for EPIC-04 staleness/CI-usage scripts | Design Not Applicable | Backend/tooling test coverage only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-16 (BLG-QA-192) | test_null_fee_trade_audit.py inspect.getsource() fix | Design Not Applicable | Test infrastructure fix only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-17 (BLG-QA-193) | Prove non-registry dependency check fails a real PR; confirm required status check | Design Not Applicable | CI governance proof-of-operation, no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-18 (BLG-QA-194) | Harden UI-copy boundary lint against obfuscation/cross-node splits | Design Not Applicable | Tooling/lint hardening; does not itself change any rendered UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-19 (BLG-GOV-356) | Overdue 90-day AI feature usage review | Design Not Applicable | Governance review artefact only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-20 (BLG-GOV-358) | gap_risk_service.py §13 review/roster-row determination | Design Not Applicable | Governance decision record only; no AI-provider call introduced by this item itself | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-21 (BLG-GOV-343) | Split roadmap_prompt.md into core + appendix | Design Not Applicable | Governance prompt restructuring, no product UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-22 (BLG-GOV-344) | Parameter-change ledger for strategy_rules.md §11 | Design Not Applicable | Governance documentation only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-23 (BLG-GOV-347) | scan_backlog_gate_conditions.py date-disambiguation fix | Design Not Applicable | Internal tooling fix, no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-24 (BLG-GOV-350) | Canonical "AI adoption window" gate-criteria reference | Design Not Applicable | Governance documentation consolidation only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-25 (BLG-GOV-352) | Script for rebalance diagnostic tallies | Design Not Applicable | Internal tooling only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-26 (BLG-GOV-353) | role_share_history.md governance-authorized home | Design Not Applicable | Governance documentation only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-27 (BLG-GOV-354) | execution_state_path stale-pointer fix | Design Not Applicable | Internal state-pointer fix, no user-visible effect | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-28 (BLG-SPEC-157) | Read-only live-schema vs data_model.md drift detector | Design Not Applicable | Internal tooling only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-29 (BLG-SPEC-164) | Drop 4 orphaned always-NULL positions columns | Design Not Applicable | Database migration only, no API/UI surface | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-30 (BLG-SPEC-165) | Reconcile positions.fees_paid NOT NULL constraint | Design Not Applicable | Database schema reconciliation only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-31 (BLG-SPEC-166) | Cross-reference current_roadmap.md SI-02 to canonical definition | Design Not Applicable | Documentation cross-reference only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-32 (BLG-SPEC-167) | data_model.md DS-19 verification-status correction | Design Not Applicable | Documentation correction only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-33 (BLG-SPEC-168) | Correct BLG-BE-128→BLG-BE-129 citation | Design Not Applicable | Documentation citation correction only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-34 (BLG-SPEC-169) | Correct notifications.md/empty-state docs to shipped no-trailing-period headings | Design Not Applicable | Spec-only correction to match already-shipped code; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-35 (BLG-FE-192) | RecentTradesWidget icon-badge two-way colour logic for zero P&L | **Design Required** | User-facing colour/visual-rendering change (icon badge treatment for `pnl === 0`) | `design_system.md` §Consistency Rules → Number and Currency Formatting (v1.21) — pre-existing canonical "zero renders in the neutral tone" rule; no new wireframe/decision record needed, as the fix brings the icon badge into line with both this rule and the card's own adjacent P&L text, which already implements the correct three-way logic | `docs/specs/frontend/pages/dashboard.md` v3.6 | ✅ Cleared | Head of UX & Design |

## §13 Boundary Pre-Check

No item in this slice introduces or extends a call to an AI provider (Gemini, Claude API, or other LLM/inference service). ST-03 (BLG-BE-132) touches `gemini_service.py` but only re-sources an existing Telegram-alert timeout — it does not add or change any AI-provider call. ST-19/ST-20 are governance review/decision items about already-shipped AI usage, not new AI-calling proposals. No `Gate Status: §13 PRE-CHECK REQUIRED` flags raised this cycle.

## Blocked Items (if any)

None. All 35 items classified and cleared.

## Notes

- Only ST-35 (BLG-FE-192, EPIC-06) was classified **Design Required**, consistent with the backlog slice's own framing (`stage4_backlog_slice.md` intro: "EPIC-06's single item (`BLG-FE-192`) carries an observable UI acceptance criterion — `design_gate_required: true`"). Its design need was fully satisfied by an existing, already-published canonical rule (`design_system.md` v1.21 §Consistency Rules → Number and Currency Formatting: "zero renders unsigned in the neutral tone") combined with an existing in-component precedent (the same `RecentTradesWidget.js` card's P&L value text already implements the correct three-way emerald/rose/neutral logic — only the icon badge's background/foreground used the stale two-way `>= 0` check). No new wireframe or UX decision record was required; Head of UX & Design confirmed the existing artefact is current and directly applicable (STEP 2.1 "yes" path).
- `docs/specs/frontend/pages/dashboard.md` updated v3.5→v3.6: new Design Source line, a documenting bullet added under §4 Card 5 — Recent Activity, and a Change Log row. Logged in `claude/system/prompt_change_log.md` per this engine's STEP 6 governance file edit check.
- **Observation (out of scope, not actioned this gate):** `dashboard.md` §4 Card 5 — Recent Activity's existing prose (event types "opened"/"stop updated", click target `/trades`) does not match what `RecentTradesWidget.js` actually renders (closed trades only, ticker + exit date + P&L + shares, click-through is per-row not card-level). This pre-dates ST-35 and is not touched by its AC. Flagged here for a future spec-debt backlog item (BLG-SPEC-type) rather than fixed inline, to keep this gate's write scope to ST-35's own AC.
- No Post-Gate-Correction Addendum required this cycle — no classification or §13 pre-check work surfaced a correction to the sealed `stage4_backlog_slice.md`.
- No motion/timing-sensitive interaction parameters (§6) are touched by any item in this slice.
- Mandatory frontend-visible-change rule (CLAUDE.md §2): ST-35's AC already requires Playwright coverage for the observable AC — consistent with this gate's Design Required classification.
