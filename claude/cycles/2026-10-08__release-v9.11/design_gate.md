**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-10-08
**Cycle:** 2026-10-08__release-v9.11

# Design Gate Record — 2026-10-08__release-v9.11

## Gate Status: PASSED

Completed: 2026-10-08
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

All 43 items are classified. 42 are cleared outright, and 1 (ST-25) is conditionally cleared:

| Classification | Count | Items |
|----------------|-------|-------|
| Design Required | 7 | ST-05, ST-10, ST-11, ST-13, ST-14, ST-15 (cleared); ST-25 (conditionally cleared, §13 pre-check required) |
| Design Pre-Approved | 6 | ST-01, ST-12, ST-19, ST-22, ST-29, ST-37 |
| Design Not Applicable | 30 | the remaining items |

All six cleared Design Required items have an approved decision record or pre-existing canonical rule, and an updated frontend spec.

**ST-25** introduces a new AI-provider call and no §13 review covers it. Its design and spec work is deferred into the story, behind a §13 determination. This follows the `2026-08-17__release-v8.9` ST-06 precedent, which was also conditionally cleared. The ordering is recorded in `stage4_backlog_slice_addendum.md`. `sprint_planning_pre_condition` is met. Sprint Planning must still resolve RISK-06 before it seals, as the release plan already requires.

**Classification note:** the slice marks 9 stories UI-facing. Two of them, ST-01 and ST-12, change content or values that existing specs already define, so they are Design Pre-Approved. Three stories not marked UI-facing have a frontend touchpoint and are Pre-Approved with a locked spec reference:
- **ST-19:** the market-regime data source changes, with no visible change.
- **ST-22:** the possible submit guard.
- **ST-37:** the axe scan.

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 (BLG-BE-152) | Give the post-trade debrief R achieved, the stop at exit and entry slippage | Design Pre-Approved | Changes the debrief's summary and focus-area content (backend prompt, numeric check, summary text). The debrief section's layout, states and controls are unchanged, so this is wording only (CLAUDE.md §2 FI-P3-02). Its ACs are backend and fixture tests. §13: covered by `decisions--2026-08-17__release-v8.9--ST-06-section13-review.md` (CONDITIONAL). The Condition 2 interpretation is the AI Compliance & Governance Officer's first sub-step (RISK-01). | N/A | `trade_history.md` v1.15 (locked reference — §Post-Trade Debrief) | ✅ Cleared | Head of UX & Design |
| ST-02 (BLG-BE-150) | Verify all six AI features after the PR #1921 import fix, and file the escaped-defect note | Design Not Applicable | Staging verification and a document. §13: exercises existing features and adds no AI call. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-03 (BLG-BE-151) | Keep the AI-output sampling hook from breaking or hiding errors in AI responses | Design Not Applicable | Backend error handling and logging. Responses are unchanged by design. §13: adds no AI call. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-04 (BLG-QA-217) | Test that every backend module imports with only backend/ on the path | Design Not Applicable | CI test only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-05 (BLG-FE-205) | Make the debrief Regenerate button recognisable, and show failures and the generated time | Design Required | Changed button styling, new generated-time label and a new failure message | `docs/design/2026-10-08__release-v9.11/debrief-regenerate-feedback/decision_record.md` (new) | `trade_history.md` v1.14 → v1.15 (§Post-Trade Debrief) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-06 (BLG-AI-08) | claude_audit_log: add prompt_hash and response_length, and log failed model calls | Design Not Applicable | Audit-log columns and a migration. §13: logging of existing calls, no new AI call. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-07 (BLG-AI-09) | State in the daily-briefing system prompt that output is advisory and cannot execute trades | Design Not Applicable | System-prompt text. The briefing card's layout and existing Advisory Label are unchanged. §13: covered by `decisions--2026-06-24__release-v6.2--BLG-FEAT-50-51-section13-review.md`, and the change strengthens advisory framing. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-08 (BLG-BE-141) | AI briefing and chat state when a quoted stop was last recalculated | Design Not Applicable | Prompt context plus a fixture test. Nothing new is rendered beyond the model's text. §13: covered by the BLG-FEAT-50-51 review. Adds an existing deterministic field (`stop_calculated_at`) to the prompt and no new call. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-09 (BLG-BE-142) | Pin every Claude model ID in one backend module | Design Not Applicable | Backend refactor plus a guard test. §13: same provider and call sites, no new call. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-10 (BLG-BE-154) | Remove the hard-coded ×1.38 US price fallback from GET /portfolio, and flag stale prices | Design Required | New data displayed: a stale-price marker on the Risk Dashboard and Dashboard | `docs/design/2026-10-08__release-v9.11/risk-price-integrity/decision_record.md` (new, shared with ST-11 and ST-13) | `risk_dashboard.md` v0.1.11 → v0.1.12 (§6.6); `dashboard.md` v3.7 → v3.8 (§4 Card 2) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-11 (BLG-FE-206) | Position Risk table: GBP entry prices, and grace-period stops shown as not enforced | Design Required | Changed currency, column headers, new "Not enforced (grace)" cell state, and a sort change for GRACE rows | `docs/design/2026-10-08__release-v9.11/risk-price-integrity/decision_record.md` (new, shared) | `risk_dashboard.md` v0.1.12 (§6.2, §6.2a, §6.4) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-12 (BLG-BE-153) | GET /portfolio computes holding_days live from entry_date | Design Pre-Approved | Corrects values the Risk Dashboard already displays (`display_status`, grace flag, Held). No new element, label or state. | N/A | `risk_dashboard.md` v0.1.12 (locked reference — §5, §6) | ✅ Cleared | Head of UX & Design |
| ST-13 (BLG-BE-155) | Stop Dist % computed in native currency for US positions | Design Required | The column's definition changes from a browser-derived value to the API's `stop_distance_pct`, and its displayed values change for US rows | `docs/design/2026-10-08__release-v9.11/risk-price-integrity/decision_record.md` (new, shared) | `risk_dashboard.md` v0.1.12 (§6.1, §6.2) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-14 (BLG-BE-147) | Grace alert filter and "Day N of 10" label use calendar days since entry | Design Required | Changes which positions get an alert card and the label's day number. The suppression rule follows the same predicate. | `docs/design/2026-10-08__release-v9.11/grace-alert-calendar-days/decision_record.md` (new) | `positions.md` v2.14 → v2.15 (§Grace Period Alert Zone, §Last Reviewed Column) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-15 (BLG-FE-204) | Recent Trades glyph treats a P&L that rounds to £0.00 as break-even | Design Required | Visible glyph and colour change for near-zero trades. Applies the pre-existing `design_system.md` v1.21 zero rule to the displayed figure (v9.9 ST-35 precedent: no new decision record). | Pre-existing canonical rule (`design_system.md` §Consistency Rules → Number and Currency Formatting) | `dashboard.md` v3.8 (§4 Card 5) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-16 (BLG-BE-143) | Rule on and test stop recalculation during grace | Design Not Applicable | Ruling and backend test | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-17 (BLG-FR-06) | Snapshot the strategy parameters in force onto each closed trade | Design Not Applicable | Backend columns and test. Nothing displays the new fields this release. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-18 (BLG-OPS-179) | Post-deploy synthetic check for post-grace stops and §11 multipliers | Design Not Applicable | Ops monitor plus the existing Telegram path | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-19 (BLG-BE-140) | Read-only market-regime source, so viewing regime no longer runs the stop-writing analyze call | Design Pre-Approved | New endpoint and a change of frontend data source. The regime display must be visually identical. Any visible change needs its own design pass. | N/A | `dashboard.md` v3.8 (locked reference — §4 Card 4 Signal Status, market regime) | ✅ Cleared | Head of UX & Design |
| ST-20 (BLG-OPS-175) | DB-level unique constraint for active price alerts | Design Not Applicable | Database constraint and migration | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-21 (BLG-OPS-176) | Make the anomaly-check fingerprint-clear path respect send_alert, or document why not | Design Not Applicable | Backend ops logic and test | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-22 (BLG-API-06) | Guard POST /trade-plans against a double-submitted duplicate plan | Design Pre-Approved | If the disposition is a client-side guard, it must use the existing pattern of disabling the submit button while the request is in flight (pending label), with no new message. A new message or layout needs its own design pass. Accepted risk needs no UI. | N/A | `trade_plan.md` v1.17 (locked reference) | ✅ Cleared | Head of UX & Design |
| ST-23 (BLG-FEAT-63) | Cost estimate for the AI monthly P&L narrative | Design Not Applicable | Document. It is the cost-gating input to ST-25's AI endpoint security checklist. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-24 (BLG-FEAT-60) | Define the AI chat engagement metric set | Design Not Applicable | Metric definitions document | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-25 (BLG-FEAT-59) | AI-assisted monthly P&L narrative | Design Required | New optional, dismissible AI narrative section on Monthly P&L. **§13 PRE-CHECK REQUIRED:** a new AI-provider call with no covering review. The v8.9 debrief review and the v6.2 briefing/chat review cover other features, and neither covers AI text in a financial report. A new AI-calling endpoint also triggers `ai_endpoint_security_checklist.md` (STEP 2.2). | Not yet produced. Deferred into ST-25 behind the §13 determination (RISK-06) and the security checklist; see `stage4_backlog_slice_addendum.md`. Target: `docs/design/2026-10-08__release-v9.11/monthly-pnl-ai-narrative/` | Not updated. Deferred until the §13 determination; target `reports.md` v0.20 → next (§Monthly P&L Report) | ⚠️ Conditionally Cleared — §13 PRE-CHECK REQUIRED | Strategy Rules & System Intent Owner (determination pending), Product Owner |
| ST-26 (BLG-SPEC-174) | Usage counter for the AI monthly P&L narrative | Design Not Applicable | Backend count plus `data_model.md`. Nothing is displayed. Sequenced after ST-25, so it inherits the addendum ordering. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-27 (BLG-FE-84) | AI chat UI interaction study protocol | Design Not Applicable | Research protocol document. No UI change. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-28 (BLG-GOV-366) | Track the 2027-01-03 AI feature usage review | Design Not Applicable | Backlog gate tracking | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-29 (BLG-SPEC-170) | Reconcile the Monthly Restatement Marker spec with GET /reports/monthly-pnl | Design Pre-Approved | Spec and contract reconciliation. If the reconciled spec needs a shipped-UI change beyond wording, the AC's follow-up route applies, and that follow-up needs its own design pass. | N/A | `reports.md` v0.20 (locked reference — §Monthly Restatement Marker) | ✅ Cleared | Head of UX & Design |
| ST-30 (BLG-SPEC-173) | Column provenance annotations in data_model.md | Design Not Applicable | Data model documentation | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-31 (BLG-SPEC-177) | Correct the TradePlan status enum in openapi.yaml | Design Not Applicable | OpenAPI correction | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-32 (BLG-SPEC-175) | Fix the 5 error-response examples that diverge from the canonical envelope | Design Not Applicable | Contract examples or backend error shape. No UI. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-33 (BLG-GOV-375) | Write-time check that sprint_backlog.md Owner values use canonical role names | Design Not Applicable | Governance tooling | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-34 (BLG-GOV-355) | Give the effort-weighted PVR column its home in product_value_ratio_history.md | Design Not Applicable | Governance document | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-35 (BLG-GOV-359) | §13 sign-off ACs must cite every §13 clause that names the feature's subject | Design Not Applicable | Governance prompt | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-36 (BLG-GOV-370) | DoQ sign-off line for stories touching stop, grace, ATR or exit logic | Design Not Applicable | QA template | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-37 (BLG-QA-196) | Extend the axe accessibility scan to the Replay page | Design Pre-Approved | Test coverage. Any serious or critical fix must use existing `design_system.md` tokens and change no layout. A fix needing a new colour or layout needs its own design pass. | N/A | `design_system.md` v1.22; `replay_mode.md` v0.3 (locked references) | ✅ Cleared | Head of UX & Design |
| ST-38 (BLG-QA-197) | Fix SC-REP-04a's signed "+£0.00" expectation | Design Not Applicable | Test expectation brought into line with the existing unsigned-zero convention. No UI change. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-39 (BLG-QA-199) | Mutation-test the US-market and batch-sizing paths | Design Not Applicable | Test only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-40 (BLG-QA-200) | Make the ceiling/count regression tests read the source they claim to verify | Design Not Applicable | Test only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-41 (BLG-QA-201) | Reset the pilot test file's shared database mocks between tests | Design Not Applicable | Test only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-42 (BLG-OPS-177) | Make the Non-Registry Dependency Check a required status check on main | Design Not Applicable | Branch protection | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-43 (BLG-OPS-178) | Move test-only Python packages out of the production build | Design Not Applicable | Build configuration | N/A | N/A | ✅ Cleared | Head of UX & Design |

## §13 Boundary Pre-Check

**One flag: ST-25.** It adds a new AI-provider call (the monthly P&L narrative) and no existing review covers it. The result is `Gate Status: §13 PRE-CHECK REQUIRED`, flagged to the Strategy Rules & System Intent Owner and the Product Owner. This matches RISK-06, which the release plan already marks "must resolve before sprint planning seals". This gate does not perform the review. It blocks design and implementation from starting before one exists. See the addendum.

The other AI-adjacent items each have covering reviews or add no call:

- **ST-01:** debrief prompt change. Covered by `decisions--2026-08-17__release-v8.9--ST-06-section13-review.md` (CONDITIONAL). The Condition 2 sign-off is the story's first sub-step (RISK-01).
- **ST-07 and ST-08:** briefing and chat prompt content. Covered by `decisions--2026-06-24__release-v6.2--BLG-FEAT-50-51-section13-review.md`.
- **ST-02, ST-03, ST-06 and ST-09:** verification, error handling, audit logging and model-ID pinning of existing calls. None adds or extends a call.
- **ST-23, ST-24, ST-26, ST-27 and ST-28:** documents, metrics and counters. None calls a provider.

The AI endpoint security checklist (`ai_endpoint_security_checklist.md`) is triggered by ST-25 only. It is recorded as a pre-design step in the addendum.

## Blocked Items

None. ST-25 is conditionally cleared, not blocked:

| Item ID | Condition | Owner | Required by |
|---------|-----------|-------|-------------|
| ST-25 | §13 determination recorded (RISK-06), then the AI endpoint security checklist, then a design decision record with Product Owner approval and the `reports.md` update, all before any ST-25 implementation commit | Strategy Rules & System Intent Owner (determination); Head of UX & Design, Product Owner, Frontend Specifications & UX Documentation Owner (design and spec) | Determination: before Sprint Planning seals (RISK-06). Design and spec: inside ST-25, before implementation. |

## Notes

### Post-gate-correction addendum

`claude/cycles/2026-10-08__release-v9.11/stage4_backlog_slice_addendum.md` was created with 1 item (ST-25: §13 pre-check ordering). Sprint Planning and Sprint Execution must read it together with the sealed slice. It changes ordering within ST-25's scope, not the scope itself. If the §13 determination requires a full review, the re-scope belongs to Sprint Planning (RISK-06's fallback).

### Artefacts produced and specs updated

- **Design artefacts produced this run (3 decision records, covering 5 items):** under `docs/design/2026-10-08__release-v9.11/`:
  - `debrief-regenerate-feedback` (ST-05)
  - `risk-price-integrity` (ST-10, ST-11 and ST-13, which share one table and one endpoint)
  - `grace-alert-calendar-days` (ST-14)
- **ST-15** uses the pre-existing `design_system.md` rule, with no new record (v9.9 ST-35 precedent).
- **Frontend specs updated (4 files):** each is logged in `prompt_change_log.md`.
  - `trade_history.md` 1.14→1.15
  - `risk_dashboard.md` 0.1.11→0.1.12
  - `dashboard.md` 3.7→3.8
  - `positions.md` 2.14→2.15

### Obligations passed to Sprint Execution (outside this gate's write scope)

- **ST-10** adds `price_is_stale`, and **ST-13** adds `stop_distance_pct`, to `GET /portfolio`. Both must update `portfolio_endpoints.md` and `docs/reference/openapi.yaml` in the same commit (CLAUDE.md §2). Coordinate `openapi.yaml` edits with ST-19 and ST-31 (RISK-04).
- **ST-11 and ST-13** each have an AC to update `risk_dashboard.md` §6. This gate has written the target text, so the stories confirm it against what ships and correct any difference.
- **ST-14:**
  - `GET /positions/grace-period-alerts` selects on `grace_days_remaining ≤ 2`.
  - The `days_in_state` fallback in `Positions.js` is removed.
  - The `GRACE_SUPPRESSION_DAYS_IN_STATE` suppression in `Positions.js` and `PositionCard.js` moves to the same predicate.
  - `grace_period_alert_endpoint.md` is updated (named in its own AC).
- **ST-19** adds a new route. CLAUDE.md §2 registration applies in the same commit: a `##` contract heading, an `openapi.yaml` entry, a `routers/test.py` entry, the `SystemStatus.js` fallback count, and `SC-SS-01b`.
- **ST-05:** no shared relative-time formatter exists (`Research.js` and `RedFlagJournal.js` each have a local one). The story may move it into `src/lib/format`.

### Playwright coverage (CLAUDE.md §2)

Each Design Required decision record's testability section lists its Playwright assertions. Two go beyond the slice's ACs, so execution must add them or file a backlog item before the PR opens:

- **ST-10:** the Dashboard Card 2 stale notice.
- **ST-14:** the "Day 10 of 10" ended state.

ST-01's UI effect is wording only (FI-P3-02), so its fixture tests are sufficient.

### Sequencing (from the slice, still binding)

- ST-10 before ST-11, ST-12 and ST-13.
- ST-01 before ST-05.
- ST-23 and ST-24 before ST-25, then ST-26.
- ST-35, if possible, before ST-25's §13 determination.

### Other

- **Motion and timing (§6):** no motion or timing parameter changes. ST-05's Regenerate keeps its existing pending state.
- **Preflight observation:** the cycle-level `state.json` has no `sprint_sealed` key, while the root pointer has `sprint_sealed: false`. It is treated as unsealed, the same as the v9.6 and v9.10 gates.

### Role sign-offs

Head of UX & Design and Product Owner confirmations are agent-mediated (Design Gate Engine acting under those roles), consistent with prior gates. The product calls the Product Owner may wish to review before `plan sprint` are:

1. Showing "Not enforced (grace)" in place of the grace stop price, rather than showing the price muted (ST-11).
2. Placing the Dashboard stale notice on Card 2 Portfolio Heat, because the homepage has no per-position price display (ST-10).
3. Treating "displays as £0.00" as break-even for the Recent Trades glyph (ST-15).
4. Conditionally clearing ST-25 rather than blocking the gate. RISK-06 still has to be resolved before Sprint Planning seals.
