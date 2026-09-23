**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-09-23
**Cycle:** 2026-09-23__release-v9.7

# Design Gate Record — 2026-09-23__release-v9.7

## Gate Status: PASSED

Completed: 2026-09-23
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

29 of 29 items cleared — 4 Design Required (ST-01 to ST-04), 2 Design Pre-Approved (ST-05, ST-06), 23 Design Not Applicable. No blocked items. `sprint_planning_pre_condition` is met.

**Classification note:** the sealed slice flagged EPIC-01 (ST-01) and EPIC-02 (ST-02 to ST-07) as carrying observable UI acceptance criteria (`design_gate_required: true`). STEP 1 confirmed 4 of those 7 as genuinely Design Required (ST-01 to ST-04); ST-05/ST-06 are shipped-code violations of the already-canonical empty-state microcopy pattern (`design_system.md` §Data States, v1.8) needing no new design decision, classified Design Pre-Approved; ST-07 is CI tooling with no UI surface of its own, classified Design Not Applicable. No item qualified under the §6 motion/timing special rule (BLG-FE-131).

**Artefact-currency finding (ST-03, ST-04):** both items' design work was already done at the `2026-09-21__release-v9.6` gate (fees-not-recorded visibility and month-end restatement diff), but the frontend was never built against it, and the backend that shipped under the same v9.6 stories used different field names/shapes than the approved decision records specified (`reports.md` still read `fees_missing_count`/`fees_missing_total` and a nested `restatement` object; the live API and its own contract, `reports_endpoints.md` v0.13, use `null_fee_trade_count` and flat `snapshotted`/`restated`/`snapshot_realised_pnl_gbp`/`restated_diff_gbp` fields). STEP 2.1's artefact review found the *visual* decisions still current but the *data contract* stale — corrected via two new v9.7 decision records rather than full redesigns, per §6's Design Required path (existing artefact reviewed, correction confirmed, frontend spec updated). One genuine new UX decision fell out of the correction: `restated=true` with `restated_diff_gbp=0` (a trade-count-only restatement) has no snapshot trade-count field to show a numeric diff against, so a fallback line was added (ST-04's decision record §2.3) rather than silently under-reporting the month as unchanged.

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 | PO-05 Lightweight Replay Mode | Design Required | New page: date-range/trade-set selector, retrospective-labelled output view. §13 pre-check: covering review exists, `docs/product/decisions/po05_section13_preassessment.md`, PASS 2026-09-23, 6 binding conditions carried into the design record. Effort is VH — this gate fixes the V1 UI shape and §13-derived constraints; exact wire contract deferred to the item's own scope-confirmation sub-story (Binding Condition 6). | `docs/design/2026-09-23__release-v9.7/po05-replay-mode/decision_record.md` (new) | `replay_mode.md` v0.1 (new — Design Only, Implementation Pending) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-02 | Cloned trade plan can silently get the wrong Setup Type | Design Required | Bug in an existing, already-approved copy/reset table (§4.5) — `setup_type` was never added to it, so clone doesn't copy it and a watchlisted-signal auto-fill silently overwrites it. Fix documents the field as Copied and fixes the ordering. | `docs/design/2026-09-23__release-v9.7/trade-plan-clone-setup-type/decision_record.md` (new) | `trade_plan.md` v1.15 → v1.16 (§4.5) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-03 | Monthly P&L's NULL-fee audit flag has no frontend surfacing | Design Required | v9.6-approved design, never built; data-contract field names corrected to match the live API (`null_fee_trade_count`; no top-level aggregate — now client-side derived). No UX change beyond the correction. | `docs/design/2026-09-23__release-v9.7/monthly-pnl-fees-surfacing/decision_record.md` (correction; supersedes data contract only) | `reports.md` v0.18 → v0.19 (§Fees-Not-Recorded Visibility) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-04 | Month-end P&L restatement diff has no frontend surfacing | Design Required | v9.6-approved design, never built; data-contract corrected from a nested `restatement` object to the live flat fields; detail row reduced to Realised P&L only (no snapshot trade-count field exists); new fallback line for the trade-count-only-restatement edge case. | `docs/design/2026-09-23__release-v9.7/monthly-pnl-restatement-surfacing/decision_record.md` (correction; supersedes data contract only) | `reports.md` v0.19 (§Monthly Restatement Marker) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-05 | AlertThresholdsSection.js empty-state heading has a trailing period | Design Pre-Approved | Shipped-code violation of the already-canonical no-trailing-period microcopy pattern (`design_system.md` §Data States, v1.8) — no new design decision, wording-only per FI-P3-02. | N/A | `design_system.md` v1.22 (locked reference; pattern unchanged) | ✅ Cleared | Head of UX & Design |
| ST-06 | NotificationsHistory.js empty-state heading has a trailing period | Design Pre-Approved | Same as ST-05 — shipped-code violation of the same canonical pattern. | N/A | `design_system.md` v1.22 (locked reference; pattern unchanged) | ✅ Cleared | Head of UX & Design |
| ST-07 | CI lint of static UI copy for forbidden predictive/advice-crossing phrases | Design Not Applicable | CI/tooling (build-time lint), no UI surface of its own | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-08 | UK stamp duty / US FX fee rounding — float vs Decimal | Design Not Applicable | Backend financial calculation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-09 | Reflection reminder over-reported summary / NULL-portfolio gap | Design Not Applicable | Backend job reporting/logic, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 | Generic alert re-delivery ignores read state | Design Not Applicable | Backend delivery logic, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-11 | Month-closure check and Monthly P&L clock-source mismatch | Design Not Applicable | Backend clock-source consistency fix, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-12 | Monthly P&L snapshot lookup — one DB connection per closed month | Design Not Applicable | Backend performance fix, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-13 | `latency_ms`/`elapsed_ms` includes retry backoff time | Design Not Applicable | Backend metric definition, no UI. §13 pre-check: measures timing around *existing* Anthropic calls; introduces no new call, prompt, or output surface — does not apply, same determination as `2026-09-21__release-v9.6`'s ST-13. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-14 | Backend test suite can connect to a real DATABASE_URL | Design Not Applicable | Test-isolation fix, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-15 | CI check flagging merged `.skip()`/`.only()` Playwright specs | Design Not Applicable | CI/CD configuration, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-16 | Recurring pre-sprint endpoint test coverage audit | Design Not Applicable | QA process/audit method, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-17 | Backfill negative-path tests for 3 v9.2/v9.3 routers | Design Not Applicable | Backend test coverage, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-18 | Validate `get_claude_endpoint_cost_windows()` SQL against real Postgres | Design Not Applicable | Backend/QA verification, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-19 | Quarterly "governance overhead ratio" metric | Design Not Applicable | Governance metric/spec documentation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-20 | Review whether the SI-02 gate threshold should scale with trade cadence | Design Not Applicable | Governance/strategy decision, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-21 | Document `ensure_ascii=False` convention for governance JSON writes | Design Not Applicable | Governance documentation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-22 | Reconcile `sprint_planning_prompt.md` STEP -1 wording against `shared_standards.md` §10.1 | Design Not Applicable | Governance prompt wording fix, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-23 | Formal definition of "linked trade plan" counting for the SI-02 gate | Design Not Applicable | Spec documentation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-24 | `positions.exit_note` documented in `data_model.md` but not live | Design Not Applicable | Data model documentation correction, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-25 | 4 orphaned, always-NULL, undocumented columns on live `positions` | Design Not Applicable | Data model disposition + documentation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-26 | `positions.fees_paid` documented NOT NULL but live column nullable | Design Not Applicable | Data model documentation correction, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-27 | Post-deploy staging verification of the reflection-reminder migration/SQL | Design Not Applicable | Ops staging verification, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-28 | External-dependency failure-mode matrix | Design Not Applicable | Ops documentation, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-29 | CI guard rejecting non-registry dependency specifiers | Design Not Applicable | CI/CD configuration, no UI | N/A | N/A | ✅ Cleared | Head of UX & Design |

## Blocked Items

None.

## Notes

- **§13 pre-check scope:** every item was checked (STEP 1). No item introduces or extends a call to an AI/LLM provider. ST-01 has a standalone covering review (`po05_section13_preassessment.md`, PASS) already on file — its 6 binding conditions are carried into the ST-01 decision record's §2.3/§2.4/§13 sections, not re-derived here. ST-13 wraps timing around existing Anthropic calls only. No `§13 PRE-CHECK REQUIRED` flags.
- **AI endpoint security checklist (`ai_endpoint_security_checklist.md`):** not triggered — no new AI-calling endpoint in this cycle.
- **Design artefacts produced this run (4 new + 2 corrections):** `docs/design/2026-09-23__release-v9.7/po05-replay-mode/`, `.../trade-plan-clone-setup-type/`, `.../monthly-pnl-fees-surfacing/` (corrects v9.6's `monthly-pnl-fees-not-recorded` data contract), `.../monthly-pnl-restatement-surfacing/` (corrects v9.6's `monthly-pnl-restatement-diff` data contract).
- **Frontend specs updated (3 files):** `trade_plan.md` 1.15→1.16, `reports.md` 0.18→0.19, and a new file `replay_mode.md` at 0.1. Logged in `prompt_change_log.md`.
- **`design_system.md` unchanged this gate:** ST-05/ST-06 cite the existing v1.22 empty-state microcopy pattern (canonical since v1.8) as-is; no version bump needed.
- **Obligations passed to Sprint Execution (outside this gate's write scope):** ST-01's backend/frontend sub-stories must be checked against both `po05-replay-mode/decision_record.md` and `po05_section13_preassessment.md`'s 6 binding conditions before implementation (per Binding Condition 6); the replay endpoint contract, `docs/specs/api_contracts/`, and `openapi.yaml` all need filing in the same commit once scoped (CLAUDE.md §2). ST-03/ST-04 must build against `reports_endpoints.md` v0.13's real field names, not the v9.6 decision records' original (superseded) data-contract sections. All 4 Design Required items carry an observable UI AC and need Playwright coverage or a dated staging run (CLAUDE.md §2).
- **Sequencing reminder:** ST-03 and ST-04 both touch the Monthly Financial Table in `Reports.js` — sequence to avoid rebase churn on the same render block, same caution already given for v9.6's ST-01/ST-02/ST-06 on `TradePlans.js`.
- **Preflight observation:** the cycle-level `claude/cycles/2026-09-23__release-v9.7/state.json` carries no `sprint_sealed` key (the root pointer, `.claude_current_state.json`, has `sprint_sealed: false`). Treated as unsealed — no seal, amendment, or `sprint_backlog.md` exists yet for this cycle.
- **Role sign-offs:** Head of UX & Design and Product Owner confirmations are agent-mediated (Sprint Execution Engine acting under those roles), consistent with prior cycles' gates. Two decisions the Product Owner may wish to review before `plan sprint`: ST-01's V1 shape (two-mode selector, deferred wire contract) and ST-04's new trade-count-only-restatement fallback line (a genuine new UX decision, not just a correction).
