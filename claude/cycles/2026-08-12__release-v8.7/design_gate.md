**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-08-12
**Cycle:** 2026-08-12__release-v8.7

# Design Gate Record — 2026-08-12__release-v8.7

## Gate Status: PASSED

Completed: 2026-08-12
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 | Thesis pre-mortem / invalidation-condition capture at trade-plan entry | Design Required | New optional field in the trade plan entry flow; no prior artefact covered this | `docs/design/2026-08-12__release-v8.7/thesis-invalidation-condition/decision_record.md` | `docs/specs/frontend/pages/trade_plan.md` v1.5 (§5.1) | ✅ Cleared | Head of UX & Design |
| ST-02 | Consume trade_plan_linked/trade_plan_id in the position-entry flow | Design Required | New post-submission confirmation UI (toast); §10.2's pre-submit indicator does not cover the best-effort auto-link path's outcome, which is only knowable from the response | `docs/design/2026-08-12__release-v8.7/trade-plan-link-confirmation-toast/decision_record.md` | `docs/specs/frontend/pages/trade_plan.md` v1.5 (§10.6) | ✅ Cleared | Head of UX & Design |
| ST-03 | Persist isAiDraft flag on trade_plans for AI-origin display badges | Design Pre-Approved | Badge display already fully specified (`trade_plan.md` §10.5, v1.4, v8.6; referenced in known deviation `DEV-v8.6-ST02-01`); this item only persists the flag server-side to make the already-approved badge reachable — no new UX decision | N/A | `docs/specs/frontend/pages/trade_plan.md` v1.5 (§10.5, locked reference, unchanged by this item) | ✅ Cleared | Head of UX & Design |
| ST-04 | SI-02 Gate Status section (Reports.js) light/dark theme fix | Design Pre-Approved | Same dark-only-token-pairing defect class as the established `design_system.md` rule (Card Hierarchy note, v1.9 Modal precedent, `BLG-FE-87/88/95` lineage); corrective, not new design | N/A | `docs/specs/frontend/design_system.md` v1.10 (locked reference) | ✅ Cleared | Head of UX & Design |
| ST-05 | Unrealised P&L card (Reports.js) light/dark theme fix | Design Pre-Approved | Identical root cause and precedent as ST-04 (filed as a sibling backlog item, same discovery pass) | N/A | `docs/specs/frontend/design_system.md` v1.10 (locked reference) | ✅ Cleared | Head of UX & Design |
| ST-06 | Convert 4 hardcoded dark-only modals to theme-aware tokens | Design Pre-Approved | Design decision already made and the exact 4 files already named at `design_system.md` v1.9 (Modal / Dialog Theming, v8.6) | N/A | `docs/specs/frontend/design_system.md` v1.10 (§Modal / Dialog Theming, locked reference) | ✅ Cleared | Head of UX & Design |
| ST-07 | Staging verification of ST-03's (v8.6) trade-plan-linkage enforcement, and legacy orphaned-row audit | Design Not Applicable | Backend/DB staging verification and legacy-row audit only; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-08 | Playwright coverage for remaining shadcn token call-site families | Design Not Applicable | Test-coverage-only story for already-shipped tokens; no UI change | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-09 | End-to-end integration assertion for tax-year boundary trade rows | Design Not Applicable | Backend test only; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 | Extend the BLG-BE-57 retry/backoff pattern to Gemini API call sites | Design Not Applicable | Backend reliability wrapper on existing call sites; no UI. §13 boundary pre-check considered: this wraps existing calls with retry/backoff resilience only, does not extend AI-provider call semantics or introduce a new call — no §13 review required | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-11 | N+1 query audit across trade/position list endpoints | Design Not Applicable | Backend performance audit; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-12 | SI-04 schema requirements pre-design | Design Not Applicable | Backend schema documentation only, no feature implementation | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-13 | Prompt-injection resistance test for the Gemini thesis-generation endpoint | Design Not Applicable | Security test exercising an existing endpoint; no UI. §13 boundary pre-check considered: testing only, does not introduce or extend an AI-provider call — no §13 review required | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-14 | Rate-limit audit on unauthenticated/low-auth endpoints | Design Not Applicable | Backend/infra audit; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-15 | Render Starter-tier headroom reassessment | Design Not Applicable | Infra/ops resource assessment; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-16 | Render dashboard-only build/deploy path filter — canonical documentation + onboarding note | Design Not Applicable | Documentation only; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-17 | Fix substring-match false negatives in find_missing_endpoints() | Design Not Applicable | Backend/CI script correctness fix; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-18 | CLAUDE.md §8 rule for shared JSON schema drift mid-sprint between sibling EPIC branches | Design Not Applicable | Governance document only; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-19 | Roadmap Unlock Tracker — consolidated view of all gated features and their conditions | Design Not Applicable | Internal governance/roadmap document (`current_roadmap.md` companion per `BLG-GOV-303`'s own scope statement), not app UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-20 | §13 policy question: confidence-interval-qualified "preview" analytics vs. the deterministic/non-predictive boundary | Design Not Applicable | Governance policy determination recorded in `strategy_rules.md` §13; no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-21 | Canonical "gated" DataState variant and visual/interaction spec for not-yet-unlocked feature surfaces | Design Required | This item is the design decision itself — new shared component variant, no prior artefact existed | `docs/design/2026-08-12__release-v8.7/gated-datastate-variant/decision_record.md` | `docs/specs/frontend/design_system.md` v1.10 (new "Gated variant" subsection, §Shared UI Components → Cards → Data States) | ✅ Cleared | Head of UX & Design |

**Mandatory §13 boundary pre-check (AI-calling proposals):** two items touch AI-adjacent surface area this cycle — ST-10 (retry/backoff wrapper on existing Gemini call sites) and ST-13 (prompt-injection test against the existing Gemini thesis-generation endpoint). Neither introduces or extends a call to an AI provider in the sense the pre-check targets: ST-10 is a non-functional reliability wrapper around already-cleared call sites (no new capability, no new content path); ST-13 is a test suite exercising an already-shipped endpoint. No covering §13 review is required for either; no `§13 PRE-CHECK REQUIRED` flag raised. ST-03's `isAiDraft` persistence and ST-02's link-confirmation toast are both display/metadata work on top of already-cleared AI surfaces (`ai_thesis_generation.md`), not new calls — same conclusion.

## Blocked Items

None. All 21 items cleared on the initial run.

## Notes

- **Three genuinely new design decisions this cycle: ST-01, ST-02, ST-21.** All three are lightweight, narrowly-scoped artefacts (three decision records) rather than open-ended design problems: ST-01 is a single new optional form field with a placement/copy decision; ST-02 is a toast-vs-`StandingAlert` choice for a response-driven confirmation; ST-21 is a new `DataState` branch generalising an already-recurring ad hoc pattern (gated roadmap features) into a documented shared variant. Frontend specs updated same-run: `trade_plan.md` 1.4→1.5, `design_system.md` 1.9→1.10.
- **ST-03, ST-04, ST-05, ST-06 (Design Pre-Approved):** all four are corrective/enforcement work against already-approved design intent. ST-03 makes reachable a badge behaviour already specified at v8.6 (`trade_plan.md` §10.5) and explicitly named as blocked-only-on-persistence in `DEV-v8.6-ST02-01`. ST-04/ST-05/ST-06 all restore compliance with `design_system.md`'s established "no dark-only token" rule — ST-06 in particular was already named by file (`WatchlistModal.js`, `ExportModal.js`, `PositionEntryModal.js`, `WidgetLibrary.js`) as the explicit follow-up to the v8.6 Modal / Dialog Theming decision. None required a new UX decision.
- **ST-19 borderline note:** considered as a candidate frontend/UI item given it produces a "consolidated view," but `BLG-GOV-303`'s own scope statement targets `current_roadmap.md` (a governance document), not an app page — classified Design Not Applicable on that basis, consistent with other governance-documentation items this cycle (ST-18, ST-20).
- **EPIC-02/EPIC-03/EPIC-04/EPIC-05/EPIC-06 (ST-07 through ST-17) all classified Design Not Applicable.** All 11 items are backend correctness/verification work, test-coverage additions, security audits, or infra/ops assessments with no live UI change — consistent with prior cycles' treatment of this item shape (v8.6 ST-11–ST-26).
- No items required the motion/timing-sensitive-interaction clause (`design_gate_prompt.md` §6, `BLG-FE-131`) — none of this cycle's items touch an existing animation/debounce/delay-before-show parameter.
