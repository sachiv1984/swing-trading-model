**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Cycle:** 2026-11-06__release-v9.16

# Post-Gate-Correction Addendum — 2026-11-06__release-v9.16

Corrections below are additive to the sealed `stage4_backlog_slice.md` — they do not replace or edit its content. Sprint Planning and Sprint Execution must read both files together as the combined authoritative scope.

None of these entries adds or removes an item or changes a priority.

## ST-03 — The dead-end scan covers eleven pages, not eight
**Found at:** Design Gate STEP 1
**Correction:** The Scope bullet lists the eight dead-end pages named in `BLG-FE-252`. `navigation.md` v2.0 §Onward Links (approved at v9.15, 2026-11-04) re-ran the link scan and found three more: Settings, Trade History, and Analytics, which links out only from its empty state. The AC, "a re-run of the inter-page link scan finds 0 dead-end pages", already covers all eleven. Each page's required link is the one in that table. The three extra links are one line each and stay within the M estimate.
**Date:** 2026-11-06

## ST-04 — The section anchor is on Analytics, and the digest gains a link
**Found at:** Design Gate STEP 1 / STEP 2.2
**Correction:** The Risk Dashboard has no pre-entry-validation or rule-breach section (`risk_dashboard.md` v0.1.15), so there is nothing there to anchor to. The digest's "Top rule breach", with the override rate, is shown in Analytics §19, Arc 5 Signal Compliance. **Product Owner decision (the user, in session, 2026-11-06):** build `?section=` support on Analytics with the id `strategy-compliance`, and add a third digest footer link, "Strategy Compliance", to `/#/PerformanceAnalytics?section=strategy-compliance`. The Risk Dashboard link stays page-level. The AC's "digest link updated" is met by the new link. Spec: `analytics.md` v2.3 §19.1. Design: `docs/design/2026-11-06__release-v9.16/digest-section-link/decision_record.md`.
**Date:** 2026-11-06

## ST-05 — The Trade Plan form must start writing the dated snapshot, and the age is 24 hours
**Found at:** Design Gate STEP 2.2
**Correction:** `TradePlan.js` never sends `pre_entry_validation_snapshot`. It appears in `src/` only at `TradeEntry.js:166`. Plans saved from the app therefore have no snapshot, and the "plan whose checks all passed still shows only the on-plan line" half of AC 1 can't happen in the app. ST-05 therefore includes making the plan form send a dated snapshot on save (`trade_plan.md` v1.22 §5e: `captured_at`, `advisory_status`, `checks`, `inputs`). No schema change is needed, because the column is JSONB. **Product Owner decision (the user, in session, 2026-11-06):** "older than a set age" is 24 hours (`position_form.md` v1.14). "Recorded acknowledgement" means the plan's `pre_entry_override_acknowledged: true`. Design: `docs/design/2026-11-06__release-v9.16/plan-linked-pre-entry-checks/decision_record.md`.
**Date:** 2026-11-06

## ST-07 — "Plan this" passes the signal id, and Signal Context accepts it
**Found at:** Design Gate STEP 2.2
**Correction:** "Signal context" in the Scope needs Trade Plan to know which signal. Today §5a shows Signal Context only for a *watchlisted* signal on the ticker, and a new signal isn't watchlisted. From Signals, "Plan this" passes `signal_id`, and §5a.1 then uses that signal for any status except `dismissed` (`trade_plan.md` v1.22). Screener rows pass no `signal_id`. Clicking "Plan this" does not change the signal's status. Design: `docs/design/2026-11-06__release-v9.16/signal-to-plan-flow/decision_record.md`.
**Date:** 2026-11-06

## ST-12 — "Behave as before" is judged against the production Pages build
**Found at:** Design Gate STEP 1
**Correction:** `HAS_AI` (`TradePlan.js:122`) is true only in builds that have the secret. That is the deployed Pages site, not local or CI builds, where the AI controls are hidden today. AC 4's "behave as before" is measured against production: the controls stay visible there. If `HAS_AI` is removed, or becomes a flag that defaults to on, the controls also appear in local and CI builds. That is expected. Any Playwright spec that asserts they are absent is updated, not treated as a regression.
**Date:** 2026-11-06
