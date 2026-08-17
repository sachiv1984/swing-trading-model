**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-08-17
**Cycle:** 2026-08-17__release-v8.9

# Design Gate Record — 2026-08-17__release-v8.9

## Gate Status: BLOCKED

Completed: 2026-08-17
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

21 of 22 items cleared. 1 item (ST-06) blocked on a mandatory §13 boundary pre-check with no covering review record — see `escalations.md` ESC-20260817-01. `sprint_planning_pre_condition` remains unmet; `plan sprint` may not be issued for this cycle until ST-06 is resolved (either a passing §13 review is produced, or ST-06 is descoped from this cycle's sprint scope by Product Owner decision).

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 | Fix nightly trailing-stop ratchet breakeven floor | Design Pre-Approved | Backend calculation-path fix; corrects the value populating an existing displayed field (positions.md "Init"/live-stop tiles), no new component/layout/interaction | N/A | `docs/specs/frontend/pages/positions.md` v2.7 (locked, unchanged) | ✅ Cleared | Head of UX & Design |
| ST-02 | Fix currency basis of stop fields (US positions) | Design Pre-Approved | Same displayed fields as ST-01, same rationale — data-correctness fix behind existing UI | N/A | `docs/specs/frontend/pages/positions.md` v2.7 (locked, unchanged) | ✅ Cleared | Head of UX & Design |
| ST-03 | Add trailing_stop_action_rate spec entry | Design Not Applicable | Spec-doc entry only (`metrics_definitions.md`), no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-04 | Correlation/sector-concentration-aware sizing | Design Required | New data displayed — "visible reason when reduced or flagged for concentration" on the sizing output | `docs/design/2026-08-17__release-v8.9/correlation-sector-concentration-sizing/decision_record.md` | `docs/specs/frontend/pages/trade_plan.md` v1.7 §10.7 | ✅ Cleared | Head of UX & Design |
| ST-05 | Pre-commit "what-if" sizing/risk simulator | Design Required | New interactive component/interaction flow on the trade-plan form | `docs/design/2026-08-17__release-v8.9/what-if-sizing-risk-simulator/ux_spec.md` | `docs/specs/frontend/pages/trade_plan.md` v1.7 §5d | ✅ Cleared | Head of UX & Design |
| ST-06 | Automated AI post-trade debrief | Design Required | New surface displaying AI-generated content on the closed-trade detail view | PENDING — §13 PRE-CHECK REQUIRED (no covering review; see `arc6_ps03_section13_preassessment.md` and `gemini_thesis_generation.md` — neither covers this proposal) | Not updated | ❌ Blocked | — |
| ST-07 | In-app backtesting engine for strategy rule changes | Design Required | New page section (third tab), new interaction flow | `docs/design/2026-08-17__release-v8.9/in-app-backtesting-engine/ux_spec.md` | `docs/specs/frontend/pages/strategy_benchmark.md` v0.6 §7.6 | ✅ Cleared | Head of UX & Design |
| ST-08 | Investigate GET /trade-plans/tags latency | Design Not Applicable | Backend performance investigation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-09 | Verify duration logging against real invocation | Design Not Applicable | Ops log verification only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 | Wrap audit-trail writes in transaction | Design Not Applicable | Backend/DB transactional fix, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-11 | Confirm/remove dead code (build_trade_history_csv) | Design Not Applicable | Backend code cleanup, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-12 | Test coverage for job-registration wiring | Design Not Applicable | Test-only, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-13 | Decide/apply treatment for trade_plans.setup_type | Design Pre-Approved (PO-confirmed downgrade) | Backend/data-model decision item; any chosen fix (required-field vs. default vs. accept-as-is) reuses existing form-validation patterns already established on this form, introducing no new component or layout. Default per §6 is Design Required when in doubt — Product Owner explicitly accepted the lower classification for this item (recorded here per §6/STEP 1's disagreement-resolution rule). | N/A | No frontend spec change anticipated; if implementation surfaces a UI-visible change, re-classify and return to this gate before merge | ✅ Cleared | Product Owner (downgrade), Head of UX & Design |
| ST-14 | Direct unit tests for 4 backend services | Design Not Applicable | Test-only, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-15 | Playwright coverage for WhatsNewCard rendering | Design Not Applicable | Test coverage for existing rendering, no product/UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-16 | Local dev venv pin enforcement; PUBLIC_URL parity | Design Not Applicable | Dev-ops/config, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-17 | Archive window_summary files >90 days | Design Not Applicable | File housekeeping, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-18 | Document jobs in health_endpoints.md | Design Not Applicable | Spec-doc entry only, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-19 | Fix post_ship_closure.md write behaviour | Design Not Applicable | Governance prompt fix, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-20 | Root-cause execution_state.json timestamp drift | Design Not Applicable | Governance/backend fix, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-21 | Place Displacement Debt Register; wire into roadmap_prompt.md | Design Not Applicable | Governance doc placement, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-22 | Define pruning rule for stale RA markers | Design Not Applicable | Governance doc rule, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |

## Blocked Items

| Item ID | Blocker | Owner | Required by |
|---------|---------|-------|-------------|
| ST-06 | No covering §13 System Boundary Review exists for the AI post-trade debrief proposal (mandatory pre-check, `design_gate_prompt.md` STEP 1) | Strategy Rules & System Intent Owner (review); Product Owner (scoping decision) | Before `plan sprint` for this cycle — see `escalations.md` ESC-20260817-01 |

## Notes

- **§13 pre-check scope:** ST-04, ST-05, and ST-07 were each checked against the mandatory §13 boundary pre-check (STEP 1) — none introduces a new call to an AI/LLM provider (all are deterministic calculations over the user's own data), so the pre-check does not apply to them. ST-06 is the only item in this cycle's scope introducing a materially new AI-provider use.
- **Spec-debt follow-up identified, not filed in this routine:** while documenting ST-04's concentration-reason addition to `PositionSizingWidget` (`trade_plan.md` §10.7), it became clear the widget's baseline (fields, debounce, `POST /portfolio/size` contract) has never had a dedicated frontend spec section — only referenced in passing at §10. This design gate's write scope does not include `claude/backlog/backlog.md` (§5 Write Scope Restriction), so no backlog item was filed here. **Action for PMO Lead / Head of Specs Team:** file a P3 Spec Debt backlog item (`/backlog-add`) for "Document PositionSizingWidget baseline in trade_plan.md" after this routine completes.
- **ST-13 downgrade:** recorded as an explicit Product Owner disagreement-resolution decision per §6/STEP 1, not a silent default. If implementation of ST-13 turns out to require a new UI element (e.g. a new required-field indicator style not already in use on this form), it must be returned to this gate before merge rather than shipped under this Design Pre-Approved classification.
- No items were classified under the "Motion/timing-sensitive interactions" rule (§6) this cycle — none of ST-04/ST-05/ST-07's design work touches animation timing, debounce/throttle parameters beyond reusing the existing 300ms debounce already established for `PositionSizingWidget`, or delay-before-show thresholds.
