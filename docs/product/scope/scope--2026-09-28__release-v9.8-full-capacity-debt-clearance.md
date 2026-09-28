Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Active
Release: v9.8
Cycle: 2026-09-28__release-v9.8
Last Updated: 2026-09-28

## Release Scope — v9.8 Full-Capacity Debt Clearance

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | `BLG-FE-184` — Migrate the remaining toFixed / toLocaleString call sites to the shared formatting helper |
| S2-02 | EPIC-01 | `BLG-FE-185` — Drive Screener and Watchlist table body cells from the shared column definitions |
| S2-03 | EPIC-01 | `BLG-FE-190` — Make the Tax Year restated-months notice link to months the Monthly tab actually shows |
| S2-04 | EPIC-01 | `BLG-FE-191` — SystemStatus.js categorizeEndpoint() has no case for the new /replay prefix |
| S2-05 | EPIC-01 | `BLG-SPEC-158` — Responsive-table behaviour spec for Positions, TradeHistory and TradePlans |
| S2-06 | EPIC-01 | `BLG-SPEC-159` — Canonical keyboard-shortcut inventory spec |
| S2-07 | EPIC-02 | `BLG-BE-128` — Remaining ad hoc `timeout=`/retry call sites not yet on the shared upstream-call helper |
| S2-08 | EPIC-02 | `BLG-BE-130` — Extend the v9.7 float→Decimal fee-rounding audit to tax-year statement calculations |
| S2-09 | EPIC-03 | `BLG-AI-07` — Golden-fixture CI regression for AI prompt templates — boundary-language drift caught at template-change time |
| S2-10 | EPIC-03 | `BLG-QA-179` — No end-to-end test confirms backend/main.py's wired root logger actually emits JSON in situ |
| S2-11 | EPIC-03 | `BLG-QA-180` — Add Playwright duration-assertion coverage for the 9 toast call sites fixed in ST-42 (Toast Notification Timing standard) |
| S2-12 | EPIC-03 | `BLG-QA-181` — Add regression coverage for the motion-timing values fixed in ST-41 (500ms ceiling components) |
| S2-13 | EPIC-03 | `BLG-QA-182` — Escaped-defect and follow-on-ratio tracking per cycle |
| S2-14 | EPIC-03 | `BLG-QA-183` — DoQ checklist addendum for AI-touching stories |
| S2-15 | EPIC-03 | `BLG-QA-184` — Mutation-testing pilot on the sizing calculator and stop ratchet |
| S2-16 | EPIC-03 | `BLG-QA-187` — Enable Playwright trace and screenshot retain-on-failure |
| S2-17 | EPIC-04 | `BLG-OPS-169` — No check that the staging backend actually redeployed after a merge that changes startup-applied schema (DS-19 sat unapplied on staging) |
| S2-18 | EPIC-04 | `BLG-OPS-170` — No documented allow-list of pre-approved read-only staging-DB query patterns for governed-session gate re-checks |
| S2-19 | EPIC-04 | `BLG-SEC-39` — Harden the non-registry dependency guard (missed specifier forms, trailing-comment false positive, no exit-code test) |
| S2-20 | EPIC-05 | `BLG-API-04` — Document idempotency and double-submit behaviour for every mutating endpoint |
| S2-21 | EPIC-05 | `BLG-API-05` — Error-payload (4xx/5xx) examples for the 10 most-called endpoints, covered by the example-freshness checker |
| S2-22 | EPIC-05 | `BLG-SPEC-152` — Full field-level openapi.yaml authoring pass for 20 generic/thin `data` payload schemas |
| S2-23 | EPIC-05 | `BLG-SPEC-153` — POST /trade-plans and DELETE /trade-plans/{id} declare no response schema in openapi.yaml |
| S2-24 | EPIC-05 | `BLG-SPEC-154` — trade_plans CREATE TABLE / DS-04 CHECK constraint undocumented since ensure_trade_plans_extended_status() shipped |
| S2-25 | EPIC-05 | `BLG-SPEC-155` — openapi.yaml's OperationalHealthResponse.ai_journal doesn't model its either/or shape with oneOf |
| S2-26 | EPIC-05 | `BLG-SPEC-161` — screener_results.md column list omits the Earnings column that the shipped table has |
| S2-27 | EPIC-05 | `BLG-SPEC-162` — trade_reflection.md §4 specifies an en dash for a missing R-multiple; the convention is an em dash |
| S2-28 | EPIC-05 | `BLG-SPEC-163` — sprint_velocity_trend_chart.md trend sentence splices non-adjacent PVR readings |
| S2-29 | EPIC-05 | `BLG-SPEC-172` — Reconcile the IT-06 §13 review (Alpaca sync recorded as GET-only, no orders placed) with a sync that POSTs orders and DELETEs positions |
| S2-30 | EPIC-06 | `BLG-GOV-338` — Bake accessible-name and heading-order rules into the Base44 prompt template |
| S2-31 | EPIC-06 | `BLG-GOV-339` — PVR / Skill-Silo measurement package — split debt into user-protective vs hygiene, add effort-weighted PVR, add a leading ungated-U-pool indicator |
| S2-32 | EPIC-06 | `BLG-GOV-340` — Delivery-flow metrics — lead time by priority band and ready-pool runway forecast |
| S2-33 | EPIC-06 | `BLG-GOV-341` — Persist STEP 7.2 role-share tallies as a structured history file |
| S2-34 | EPIC-06 | `BLG-GOV-342` — JSON Schema for `.claude_current_state.json`, including the `last_updated_utc` field the roadmap engine reads |
| S2-35 | EPIC-06 | `BLG-GOV-346` — Size "grep-and-fix-everywhere" and "verify against live environment" story classes a notch higher by default |
| S2-36 | EPIC-06 | `BLG-GOV-348` — strategy_rules.md §13.5 roster missing PO-05 row after 2026-09-23 clearance |
| S2-37 | EPIC-06 | `BLG-GOV-349` — governance_sync.yml does not auto-close a phased story's GitHub issue (ST-XXa/b/c vs. the commit tag's bare ST-XX) |
| S2-38 | EPIC-06 | `BLG-GOV-351` — No scheduled trigger/owner fires the 90-day post-ship AI feature usage review (BLG-GOV-74/140/141/142 cluster) |
| S2-39 | EPIC-06 | `BLG-SPEC-156` — PO-04 (Reflection ↔ Outcome Correlation) needs its own §13 boundary review, not just a stub-file note |

39 items across 6 EPICs, sized to 28.00 estimated days (top of the confirmed ~24–28 day capacity band per explicit user "full capacity" instruction). Selected via `release_planning_prompt.md` §1.4c (0 ready P1; P2-first; category-balanced round-robin, oldest-filed-first) from a 65-item / 46.7-day ready pool, per `run_manifest.md`'s Scope Construction section.

### Items explicitly deferred

| Item | Reason | Target |
|------|--------|--------|
| `BLG-QA-185`, `BLG-SPEC-157`, `BLG-GOV-352` | Ready but would overshoot the 28.00d capacity ceiling on their category's round-robin turn (2.0d each, the largest remaining items) | v9.9 candidate |
| 23 further ready P3/P4 items across all categories | Capacity-exhausted after 39 items reached 28.00d | v9.9 candidate — see `run_manifest.md` for full ready-pool accounting |
| `BLG-FEAT-59`, `BLG-FEAT-60`, `BLG-FEAT-63`, `BLG-FE-84`, `BLG-OPS-88`, `BLG-GOV-140`, `BLG-GOV-141`, `BLG-GOV-142` | Date-lapsed gate (90-day AI feature usage review, due 2026-09-24, not yet conducted) — remains gated; root-cause trigger gap tracked via `BLG-GOV-351` (seated this cycle as S2-38) | Re-eligible once the review is conducted |
| `BLG-FEAT-73`, `BLG-FEAT-76` | Still gate-blocked (SI-02 linkage / hard `Depends on` chain) | Re-check per each item's own gate condition |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*

Superseded by: [TBD]
Changelog: [TBD]
Verification report: [TBD]
Cycle: 2026-09-28__release-v9.8