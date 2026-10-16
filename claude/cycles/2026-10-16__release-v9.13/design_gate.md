**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Last Updated:** 2026-10-16
**Cycle:** 2026-10-16__release-v9.13

# Design Gate Record — 2026-10-16__release-v9.13

## Gate Status: PASSED

Completed: 2026-10-16
PMO Lead: confirmed
Head of UX & Design: confirmed
Product Owner: confirmed

All 40 items are classified and cleared. No item is conditionally cleared or blocked.

| Classification | Count | Items |
|----------------|-------|-------|
| Design Required | 10 | ST-01, ST-03, ST-04, ST-05, ST-06, ST-10, ST-21, ST-22, ST-25, ST-26 |
| Design Pre-Approved | 3 | ST-09, ST-13, ST-20 |
| Design Not Applicable | 27 | the remaining items |

**Classification notes:**
- The slice marks 12 stories UI-facing. Two are Pre-Approved rather than Design Required:
  - **ST-09** makes an already-specified line reachable: "Restatement check unavailable.", `reports.md` v0.24 §Monthly Restatement Marker, Failure.
  - **ST-20** keeps the state the spec already requires: previous debrief or empty state.
- **ST-13** is not marked UI-facing. It is test coverage of the Trade Plan's pre-entry panel and is Pre-Approved with a locked reference (v9.12 ST-19 precedent).
- **ST-21 and ST-26** apply the pre-existing v9.12 light-theme token rule, so no new decision record is needed (v9.12 ST-24 precedent). Their specs were still updated.
- **ST-05** and **ST-06** depend on in-sprint rulings by the Strategy Rules & System Intent Owner. Both outcomes of each are designed (v9.12 ST-10 precedent), and the unused branch is deleted at implementation.
- **ST-16** is not UI-facing. Its AC 4 records the Head of UX & Design's answer on visible "system-added" styling for the stop-time note. That answer needs the `[STOP-TIME-MISSING]` rate as input, which is not available at this gate. It stays an in-sprint step for the Head of UX & Design. Any styling change it leads to is filed separately, per the slice.

## Item Classification Summary

| Item ID | Title | Classification | Rationale | Design Artefact | Frontend Spec | Gate Status | Confirmed by |
|---------|-------|----------------|-----------|-----------------|---------------|-------------|--------------|
| ST-01 (BLG-FE-226) | Make the Daily Position Monitor's exit confirmation open the real exit flow | Design Required | Changed interaction flow: a per-position ExitModal queue, a queue indicator, Monitor-sourced pre-selection and a new failure state | `docs/design/2026-10-16__release-v9.13/monitor-exit-queue/decision_record.md` (new) | `positions.md` v2.19 → v2.20 (§Daily Position Monitor Exit Queue) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-02 (BLG-SPEC-186) | Define the allowed exit reasons and map each to one of §8's three exit conditions | Design Not Applicable | Spec, data model and constraint. The legacy backfill does not change displayed labels, because ST-03's module resolves aliases. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-03 (BLG-FE-227) | One shared exit-reason module so Trade Reflections badges and labels match stored values | Design Required | Changed badge labels and colours, with new light-theme tokens | `docs/design/2026-10-16__release-v9.13/exit-reason-badges/decision_record.md` (new) | `trade_history.md` v1.15 → v1.16 (§Exit Reason Labels and Badges); `reflections.md` v0.2 → v0.3 (§5.2); `trade_reflection.md` v0.3 → v0.4 (§4) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-04 (BLG-BE-182) | Record checklist_skipped events and stop offering journal filters that can never match | Design Required | Changed filter options and empty-state text; new row context | `docs/design/2026-10-16__release-v9.13/red-flag-journal-recorded-types/decision_record.md` (new) | `red_flag_journal.md` v1.3 → v1.4 (§4, §5, §7) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-05 (BLG-GOV-391) | Strategy determination on month-end rebalance exits | Design Required | New interim label on rebalance signals. Both determination outcomes remove it. | `docs/design/2026-10-16__release-v9.13/rebalance-exit-interim-label/decision_record.md` (new) | `signals.md` v0.4 → v0.5 (§Rebalance Exit Interim Label) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-06 (BLG-BE-180) | Reject a fetched ATR that puts the initial stop at or below zero | Design Required | New Initial Stop state and message. Both ruling branches are designed: reject with submit disabled, or floor. | `docs/design/2026-10-16__release-v9.13/initial-stop-at-or-below-zero/decision_record.md` (new) | `components/position_form.md` v1.9 → v1.10 (§Initial Stop, §Validation Errors) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-07 (BLG-BE-161) | Align the standalone position_manager.py with §6.3 | Design Not Applicable | Backend script | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-08 (BLG-API-07) | Reject or flag the four fixed strategy-parameter fields on Settings writes | Design Not Applicable | API response only. The Settings page already treats these four as fixed (`FIXED_STRATEGY_FIELDS`). If execution finds that the page sends them, a Settings-visible effect of the 400 or warning is a defect for ST-08 to prevent, not a design change. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-09 (BLG-BE-156) | Keep the Monthly P&L report up when the snapshot store fails | Design Pre-Approved | Makes the already-specified "Restatement check unavailable." line reachable. The story drops `reports.md`'s Known limitation note in-story (AC 3). | N/A | `reports.md` v0.24 (locked reference — §Monthly Restatement Marker, Failure) | ✅ Cleared | Head of UX & Design |
| ST-10 (BLG-SPEC-188) | Define a stop-freshness metric and show it on System Status | Design Required | New data displayed: the Stop Freshness panel | `docs/design/2026-10-16__release-v9.13/stop-freshness-status/decision_record.md` (new) | `system_status.md` v1.2 → v1.3 (§Stop Freshness Panel) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-11 (BLG-SPEC-180) | Correct metrics_definitions.md's claim about NULL positions.fees_paid | Design Not Applicable | Spec text | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-12 (BLG-QA-204) | Mock get_settings() so the stored ATR multiplier is asserted exactly | Design Not Applicable | Tests only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-13 (BLG-QA-208) | Test the entry required-field set and the non-blocking advisory panel at their boundary | Design Pre-Approved | Test coverage of the existing pre-entry panel. No UI change of its own. | N/A | `trade_plan.md` v1.19 and `components/position_form.md` v1.10 (locked references). The advisory panel is exercised as shipped in `TradePlan.js`, and no spec section is changed. | ✅ Cleared | Head of UX & Design |
| ST-14 (BLG-QA-210) | Give the valid-input sizing property a lower bound | Design Not Applicable | Tests only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-15 (BLG-AI-17) | Treat UK .L and bare tickers as the same instrument in the briefing ticker filter | Design Not Applicable | Output filter. A kept or dropped action renders in the unchanged briefing card. §13: see the pre-check below. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-16 (BLG-AI-18) | Attribute chat stop citations to the focused ticker and case-normalise action tickers | Design Not Applicable | Validator attribution. The appended note is model-text content in the existing bubble (v9.12 ST-04 precedent). AC 4's styling answer stays an in-sprint Head of UX & Design step (see Classification notes). | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-17 (BLG-AI-16) | Check the briefing summary text for tickers outside the context | Design Not Applicable | Output check. A code-written caveat, if chosen, is text in the existing card with no layout change. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-18 (BLG-AI-15) | Add an output-language check to the journal summary | Design Not Applicable | Output check. A code-written fallback, if chosen, renders in the existing summary area under its existing "AI-generated summary" label. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-19 (BLG-AI-14) | Label available cash and starting capital separately in the AI chat context | Design Not Applicable | Prompt context text | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-20 (BLG-FE-211) | Keep the debrief card populated when Regenerate returns no data | Design Pre-Approved | Restores the specified state: the previous debrief stays, or the empty state shows. No new message: the v1.15 regenerate error is for non-2xx responses only. | N/A | `trade_history.md` v1.16 (locked reference — §Post-Trade Debrief) | ✅ Cleared | Head of UX & Design |
| ST-21 (BLG-FE-212) | Give the debrief error text a light-theme colour that passes contrast | Design Required | Colour change. It applies the pre-existing v9.12 light-theme token rule, so no new decision record is needed. The scope clarification is in the addendum. | Pre-existing canonical rule (`docs/design/2026-10-12__release-v9.12/light-theme-support/decision_record.md` §3; `design_system.md` §Light-Theme Colour Tokens, §Error States) | `trade_history.md` v1.16 (§Post-Trade Debrief §Light Theme, error colours) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-22 (BLG-FE-208) | Add a useful / not-useful rating to each AI chat answer | Design Required | New control and states on each chat answer | `docs/design/2026-10-16__release-v9.13/chat-answer-rating/decision_record.md` (new) | `positions.md` v2.20 (§AI Trade Advisor Widget §Answer Rating) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-23 (BLG-QA-228) | CI check that every frontend API call exists in openapi.yaml | Design Not Applicable | CI tooling | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-24 (BLG-QA-227) | Fail Playwright on any 404/405 from the app's API and sweep state-changing actions | Design Not Applicable | Test infrastructure. Exposed defects are filed, not fixed (RISK-05). | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-25 (BLG-FE-221) | Make coloured Buttons render their colour (fix cn() at the root) | Design Required | Button fills change on the sites where the authored fill never rendered. emerald-600 fails AA, so it moves to emerald-700. The scope clarification is in the addendum. | `docs/design/2026-10-16__release-v9.13/coloured-button-fills/decision_record.md` (new) | `screener_results.md` v1.9 → v1.10; `components/cash_management_modal.md` v1.2 → v1.3 | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-26 (BLG-FE-209) | Fix the Replay page's light-theme colour contrast | Design Required | Light-theme colours on three page views. It applies the pre-existing v9.12 light-theme token rule, so no new decision record is needed. | Pre-existing canonical rule (`docs/design/2026-10-12__release-v9.12/light-theme-support/decision_record.md` §3) | `replay_mode.md` v0.3 → v0.4 (§Light Theme) | ✅ Cleared | Head of UX & Design + Product Owner |
| ST-27 (BLG-QA-211) | Decide how real-database-bound modules may persist across pytest files | Design Not Applicable | Tests only | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-28 (BLG-OPS-187) | Make the daily AI cost alert fail loudly on query or workflow failure | Design Not Applicable | Ops monitoring. It counts existing calls and adds none. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-29 (BLG-OPS-189) | Deploy both staging services from staging-deploy.yml and wait on each | Design Not Applicable | CI/CD | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-30 (BLG-OPS-18) | Produce the combined data-pipeline cost baseline | Design Not Applicable | Ops documentation | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-31 (BLG-OPS-19) | Attribute each external API call to the feature that triggered it | Design Not Applicable | Backend instrumentation and report | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-32 (BLG-OPS-23) | Benchmark the full screener run | Design Not Applicable | Ops measurement | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-33 (BLG-OPS-77) | Assess data-provider risk and failover options | Design Not Applicable | Ops documentation | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-34 (BLG-TECH-23) | Assess the major and breaking dependency upgrades | Design Not Applicable | Assessment only. framer-motion and lucide-react are UI libraries. An approved upgrade is filed separately and, if it changes motion or icons, needs its own design pass (§6 motion rule). | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-35 (BLG-GOV-390) | Treat Gate criteria: None/N/A as ungated in the gate scan | Design Not Applicable | Governance tooling | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-36 (BLG-GOV-373) | Known-false-positive allow-list for the gate scan | Design Not Applicable | Governance tooling | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-37 (BLG-SPEC-184) | Compare documented column defaults in check_data_model_drift.py | Design Not Applicable | Spec tooling | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-38 (BLG-GOV-376) | Update strategy_rules.md §13.3 now the Gap Risk Flag's weekend-hold trigger is gone | Design Not Applicable | Strategy text. Not an AI item. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-39 (BLG-GOV-377) | Correct strategy_rules.md §13.5's PO-05 roster row | Design Not Applicable | Strategy text. Not an AI item. | N/A | N/A | ✅ Cleared | Head of UX & Design |
| ST-40 (BLG-GOV-387) | Correct the v9.8–v9.10 compound Owner count in role_share_history.md | Design Not Applicable | Governance record | N/A | N/A | ✅ Cleared | Head of UX & Design |

## §13 Boundary Pre-Check

**No flags.** No item introduces a new AI-calling endpoint or a new AI feature. Each AI-adjacent item changes the inputs, filtering or validation of an existing call that is already covered:

- **ST-15, ST-16, ST-17 and ST-19:** briefing and chat. Covered by `decisions--2026-06-24__release-v6.2--BLG-FEAT-50-51-section13-review.md` (PASS). Each one narrows or checks output, attributes it, or corrects context labels.
- **ST-18:** journal summary. Covered by `SRB-v1.7-2026-03-02__release-v1.7.md` (CONDITIONALLY COMPLIANT) and `decisions--2026-04-17__release-v2.8.md` (BLG-FEAT-16). The output-language check strengthens Condition 2's "not a trading recommendation".
- **The regenerate option (ST-17, ST-18).** If the AI Compliance & Governance Officer picks "regenerate", it re-issues the same reviewed call once, with the same prompt and context. That is not a new call type, and no §13 review is triggered. Each extra call is logged in `claude_audit_log` and counted by the daily cost alert (ST-28).
- **ST-22:** the chat rating calls no AI provider. The rating is not an input to any signal, score or recommendation.
- **ST-28:** counts existing spend and adds no call.

The AI endpoint security checklist is not triggered: no new AI-calling endpoint. ST-38 and ST-39 edit `strategy_rules.md` §13.3 and §13.5 text but are not AI items. The slice's §13 clause-citation note (v2.61) already covers them, and their ACs cite §13.3 and §13.5 (`design_gate_prompt.md` v1.11).

## Blocked Items

None.

## Notes

### Post-gate-correction addendum

`claude/cycles/2026-10-16__release-v9.13/stage4_backlog_slice_addendum.md` was created with 3 items: ST-03, ST-21 and ST-25. Sprint Planning and Sprint Execution must read it together with the sealed slice. Each item clarifies within an item's existing scope. None changes scope. Two flag a possible estimate check at Sprint Planning: ST-03 (+3 files) and ST-21 (XS may become S).

### Artefacts produced and specs updated

- **Design artefacts produced this run:** 8 decision records, one per story, under `docs/design/2026-10-16__release-v9.13/`:
  - `monitor-exit-queue` (ST-01)
  - `exit-reason-badges` (ST-03)
  - `red-flag-journal-recorded-types` (ST-04)
  - `rebalance-exit-interim-label` (ST-05)
  - `initial-stop-at-or-below-zero` (ST-06)
  - `stop-freshness-status` (ST-10)
  - `chat-answer-rating` (ST-22)
  - `coloured-button-fills` (ST-25)
- **ST-21 and ST-26** use the pre-existing v9.12 light-theme rule, with no new record.
- **Frontend specs updated (11 files):** each is logged in `prompt_change_log.md`.
  - `positions.md` 2.19→2.20
  - `trade_history.md` 1.15→1.16
  - `reflections.md` 0.2→0.3
  - `trade_reflection.md` 0.3→0.4
  - `red_flag_journal.md` 1.3→1.4
  - `signals.md` 0.4→0.5
  - `components/position_form.md` 1.9→1.10
  - `system_status.md` 1.2→1.3
  - `replay_mode.md` 0.3→0.4
  - `screener_results.md` 1.9→1.10
  - `components/cash_management_modal.md` 1.2→1.3

  The two `components/` files are the Trade Entry page spec and the global Cash Management modal spec. The v9.10 and v9.12 gates updated `position_form.md` on the same basis.

### Obligations passed to Sprint Execution (outside this gate's write scope)

- **New routes and the CLAUDE.md §2 registration chain (RISK-04):** possible for ST-10 (stop-freshness source) and certain for ST-22 (rating write). Each needs, in the same commit: a `##` contract heading, an `openapi.yaml` entry, a `routers/test.py` entry, the `SystemStatus.js` fallback count and `SC-SS-01b`. If both ship, recompute the count from `routers/test.py` at merge.
- **New response fields:** ST-22's `answer_id` on `POST /ai/chat`, in `ai_endpoints.md` and `openapi.yaml`.
- **ST-01:** deleting `Position.update` is what lets ST-23's openapi check pass on `main`. `ExitModal` gains optional pre-selection and queue props, which default to today's behaviour.
- **ST-25:** the button rule (decision record §2.1) goes into `docs/specs/frontend/design_system.md` §Shared UI Components → Button (Class 1), in-story.
- **Observation, not filed:** the Monitor's own stop predicate (`MonitorModal.js::getPositionStatus`) ignores the grace period and uses `stop_price`, not `current_trailing_stop`. So it can suggest "Stop Loss Hit" during grace, contrary to §8.1. This is outside ST-01's scope. Recommend filing it with `/backlog-add` at Sprint Planning (monitor-exit-queue §7).

### Playwright coverage (CLAUDE.md §2)

Each Design Required decision record's testability section lists its assertions. Two go beyond the slice's ACs, so execution must add them or file a backlog item before the PR opens:
- **ST-01:** the "Exit {i} of {n}" queue indicator with two positions.
- **ST-22:** the save-failed state re-enables the rating buttons.
