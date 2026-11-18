**Owner:** PMO Lead
**Class:** Planning Document (Class 4)
**Status:** Active
**Cycle:** 2026-11-18__release-v9.18

# Post-Gate-Correction Addendum — 2026-11-18__release-v9.18

Corrections below are additive to the sealed `stage4_backlog_slice.md` — they do not replace or edit its content. Sprint Planning and Sprint Execution must read both files together as the combined authoritative scope.

None of these entries adds or removes a story or changes a priority. Each one corrects or makes precise a story's existing scope, using a decision record under `docs/design/2026-11-18__release-v9.18/` and, where named, a Product Owner decision given in session on 2026-11-18.

## ST-03 — `GET /notifications` gains `delivery_status`; error strings renamed
**Found at:** Design Gate STEP 2.2 (data-source check)
**Correction:** `GET /notifications` does not return any delivery field, so the Feed cannot show "Not sent" without one. ST-03 adds a derived `delivery_status` (`sent | not_requested | pending | not_sent`) to each item, per `alert-delivery-truth` §3.2 (`alerts_endpoints.md`, `openapi.yaml`). The backend's user-visible error strings change from `'email not configured'` / `'email disabled'` to `'Telegram not configured'` / `'Telegram off for this alert type'`. "Not sent" shows on Feed rows only. Notification History tracks evaluations, not delivery, and is unchanged.
**Date:** 2026-11-18

## ST-04 — the regime keys are also wrong, and prices need the market currency
**Found at:** Design Gate STEP 2.2 (data-source check)
**Correction:** besides the grace and summary keys the backlog item names, `market_regime_change` writes `spy_risk_on`/`ftse_risk_on`, not `regime`/`previous_regime`. AC "all 4 alert types show their intended compact fields" therefore covers the regime mapping in `notifications.md` v0.12 §Alert History Values. Prices format in the row's market currency, not always USD. ST-04 traces the `symbol` suffix and the UK units, and checks one real UK row before the commit (staging, with permission).
**Date:** 2026-11-18

## ST-07 — this gate wrote the `navigation.md` half
**Found at:** Design Gate STEP 3
**Correction:** ST-08 is Design Required and needs its spec before Sprint Planning, so this gate wrote `navigation.md` v2.5 (the two §14.2 moves, Head of UX & Design approval 2026-11-18). ST-07 delivers the `design_system.md` §14.5 design direction. It also records the dated Head of UX & Design approval of both files, which meets its restated AC. Its 0.5d estimate is not reduced: the `design_system.md` work is most of it.
**Date:** 2026-11-18

## ST-08 — routes and section behaviour fixed
**Found at:** Design Gate STEP 2.2
**Correction:** Ticker Universe's canonical route becomes `/settings/ticker-universe`, a Settings detail page with parent link "Settings", reached from a new Settings §3 "Screener universe" row (`PageHeader` takes one onward link). Inside Performance, the Strategy Benchmark filter bar is not sticky, and its own section index (§3a, v9.17) is retired. Its `section-index.spec.js` scenarios SC-SIX-06 to SC-SIX-08 move to the Performance index or are removed. Specs: `navigation.md` v2.5, `performance.md` v1.3 §4.1, `strategy_benchmark.md` v0.12, `ticker_universe.md` v1.3, `settings.md` v1.11.
**Date:** 2026-11-18

## ST-09 — line wording is "Nothing to show", not "All clear"
**Found at:** Design Gate STEP 2.2
**Correction:** the folded line reads "Nothing to show: …" (`dashboard.md` v4.4 §3A). "All clear" would judge the portfolio safe (§13 tone) and is wrong for a missing compliance score. The AI briefing and What's New entries are disclosure buttons, so Regenerate stays reachable.
**Date:** 2026-11-18

## ST-10 — Card 3 is in scope; its sub-label changes
**Found at:** Design Gate STEP 2.2 (data-source and worked-example checks)
**Correction:** "every Dashboard grace count" includes Card 3 (`GracePeriodCard.js`), which uses a third definition. Its "Next expires" line reads `grace_end_date`, which no endpoint returns (grep 2026-11-18), so it always shows "No expiry date set". Card 3 uses `isInGrace` and the Risk Dashboard's `nextEndsText` (moved to `src/lib/positionUrgency.js`). Positions to Watch drops its "exit zone" wording (`dashboard.md` v4.4 §4B).
**Date:** 2026-11-18

## ST-11 — "Plan this" is added, on `new` and `watchlisted` rows
**Found at:** Design Gate STEP 2.3 (Product Owner decision, 2026-11-18)
**Correction:** the Product Owner chose to add "Plan this". It shows only on statuses where Signals shows it (`new`, `watchlisted`), and uses the `signals.md` route including `entry_price` (`dashboard.md` v4.4 §1B, TL-30).
**Date:** 2026-11-18

## ST-12 — "Position size within heat limits" becomes "Position size checks"; §13 note to confirm
**Found at:** Design Gate STEP 2.2 (spec-premise check; Product Owner decision, 2026-11-18)
**Correction:** `strategy_rules.md` has no heat limit, and no pre-entry check tests heat, so AC 1's "Position size within heat limits" cannot be automatic as worded. The Product Owner chose to rename it "Position size checks", with status from the cash, sector-concentration and sizing-validity checks. AC 1 applies to "Position size checks" and "Stop level defined". `trade_plan.md` §6's §13 note (PT-05 review: "no automated condition evaluation") is amended in v1.30. ST-12 records the Strategy Rules & System Intent Owner's dated confirmation of that amendment before the build.
**Date:** 2026-11-18

## ST-13 — `GET /trades` gains `rules_followed` / `rules_broken`; a "Not known" state
**Found at:** Design Gate STEP 2.2 (data-source check)
**Correction:** `GET /trades` returns no rule-adherence field, and `pre_entry_validation_log` has no position link, so the filter cannot be computed in the browser. ST-13 adds server-computed `rules_followed: true | false | null` and `rules_broken: string[]` to `GET /trades` (`trade_endpoints.md`, `openapi.yaml`, pytest). The UI has a fourth option, "Not known", for trades that cannot be classified. The Journal red-flags filter is decided "not needed" (`trade_history.md` v1.18 §Rules Filter).
**Date:** 2026-11-18

## ST-14 — `closed_trades_total` added; confirm the two journal-completion predicates match
**Found at:** Design Gate STEP 2.2 (worked-example check)
**Correction:** with no closed trades, the digest returns 0.0%, which looks the same as "no notes". ST-14 adds `closed_trades_total` beside the renamed fields (contract, `openapi.yaml`) so the page can show "No closed trades yet". The same rate shows on Performance → Compliance (`GET /analytics/compliance-metrics`). ST-14 confirms the two SQL predicates match, or aligns the digest to `metrics_definitions.md`.
**Date:** 2026-11-18

## ST-16 — the journal completion link goes to Performance Compliance; `red_flags_7d` added
**Found at:** Design Gate STEP 2.2 (data-source check; Product Owner decision, 2026-11-18)
**Correction:** the restated AC says the relabelled row links to "the Journal section that shows journal completion". No Journal section shows it. It is shown on Performance → Compliance (Discipline & Compliance), so the link goes to `/Performance?section=compliance`, recorded in `navigation.md` v2.5. `GET /digest/weekly` has no red-flags figure, so the Product Owner chose to add `red_flags_7d` (`red_flag_events`, last 7 UTC days) to it in ST-16 (`digest_endpoints.md`, `openapi.yaml`, pytest).
**Date:** 2026-11-18

## ST-17 — counts only, with the ISO-week dates named
**Found at:** Design Gate STEP 2.2 (time-boundary check)
**Correction:** the loop section shows the five counts only, with no step-to-step rates (noise at weekly counts of 0–5). Its caption names the ISO-week dates ("Monday {d MMM} to today (UTC)"), because the figures above it use a rolling 7 days. The opened event is written once per page load, not on Refresh (`weekly_digest.md` v0.3).
**Date:** 2026-11-18

## ST-27 — new urgency tier 0 "Split to confirm"
**Found at:** Design Gate STEP 2.2 (dependent-state check)
**Correction:** while a split is unconfirmed, its stop and exit tests are suppressed. Without a tier for that state, the position would sort as tier 4 (healthy). ST-27 adds tier 0 to `src/lib/positionUrgency.js` (with unit tests, per ST-19's convention) and the display in `positions.md` v2.30 §Split Detected State, which has no "Not a split" option.
**Date:** 2026-11-18

## ST-30 — direction (a), compute live
**Found at:** Design Gate STEP 2.3 (Product Owner decision, 2026-11-18)
**Correction:** sub-step 1's direction is decided: option (a). The AC's (a) branch applies (verified on staging). The note sentence and the stale-price line are fixed in `reports.md` v0.28.
**Date:** 2026-11-18

## ST-33 — UK Screener rows make no earnings lookup
**Found at:** Design Gate STEP 2.2
**Correction:** the scope's decision is made: Screener UK rows make no earnings lookup (`strategy_rules.md` §4.2.3 is US-only), recorded in `screener_results.md` v1.12. "Unknown" is muted and never uses the GAP RISK badge's colour or wording. ST-33 cites the gap-risk §13 review's binding conditions.
**Date:** 2026-11-18
