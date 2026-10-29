Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v9.13
Cycle: 2026-10-16__release-v9.13
Last Updated: 2026-10-29

Superseded by: v9.13 ship — 2026-10-29
Changelog: docs/product/changelog.md#v9.13
Verification report: claude/cycles/2026-10-16__release-v9.13/verification_report.md
Cycle: 2026-10-16__release-v9.13

## Release Scope — v9.13

40 items across 6 EPICs, 28.00 estimated days, at the top of the ~24–28 day band ("use full capacity"). Acceptance criteria are in `claude/cycles/2026-10-16__release-v9.13/stage4_backlog_slice.md`.

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | `BLG-FE-226` — Make the Daily Position Monitor's exit confirmation open the real exit flow |
| S2-02 | EPIC-01 | `BLG-SPEC-186` — Define the allowed exit reasons and map each to one of §8's three exit conditions |
| S2-03 | EPIC-01 | `BLG-FE-227` — One shared exit-reason module so Trade Reflections badges and labels match stored values |
| S2-04 | EPIC-01 | `BLG-BE-182` — Record checklist_skipped events and stop offering journal filters that can never match |
| S2-05 | EPIC-01 | `BLG-GOV-391` — Strategy determination on month-end rebalance exits, which are live but not in strategy_rules.md |
| S2-06 | EPIC-02 | `BLG-BE-180` — Reject a fetched ATR that puts the initial stop at or below zero |
| S2-07 | EPIC-02 | `BLG-BE-161` — Align the standalone position_manager.py with §6.3 (no stop ratchet during grace) |
| S2-08 | EPIC-02 | `BLG-API-07` — Reject or flag the four fixed strategy-parameter fields on Settings writes |
| S2-09 | EPIC-02 | `BLG-BE-156` — Keep the Monthly P&L report up when the snapshot store fails |
| S2-10 | EPIC-02 | `BLG-SPEC-188` — Define a stop-freshness metric and show it on System Status |
| S2-11 | EPIC-02 | `BLG-SPEC-180` — Correct metrics_definitions.md's claim about NULL positions.fees_paid |
| S2-12 | EPIC-02 | `BLG-QA-204` — Mock get_settings() so the stored ATR multiplier is asserted exactly |
| S2-13 | EPIC-02 | `BLG-QA-208` — Test the entry required-field set and the non-blocking advisory panel at their boundary |
| S2-14 | EPIC-02 | `BLG-QA-210` — Give the valid-input sizing property a lower bound |
| S2-15 | EPIC-03 | `BLG-AI-17` — Treat UK .L and bare tickers as the same instrument in the briefing ticker filter |
| S2-16 | EPIC-03 | `BLG-AI-18` — Attribute chat stop citations to the focused ticker and case-normalise action tickers |
| S2-17 | EPIC-03 | `BLG-AI-16` — Check the briefing summary text for tickers outside the context |
| S2-18 | EPIC-03 | `BLG-AI-15` — Add an output-language check to the journal summary |
| S2-19 | EPIC-03 | `BLG-AI-14` — Label available cash and starting capital separately in the AI chat context |
| S2-20 | EPIC-03 | `BLG-FE-211` — Keep the debrief card populated when Regenerate returns no data |
| S2-21 | EPIC-03 | `BLG-FE-212` — Give the debrief error text a light-theme colour that passes contrast |
| S2-22 | EPIC-03 | `BLG-FE-208` — Add a useful / not-useful rating to each AI chat answer |
| S2-23 | EPIC-04 | `BLG-QA-228` — CI check that every frontend API call exists in openapi.yaml |
| S2-24 | EPIC-04 | `BLG-QA-227` — Fail Playwright on any 404/405 from the app's API and sweep state-changing actions |
| S2-25 | EPIC-04 | `BLG-FE-221` — Make coloured Buttons render their colour (fix cn() at the root) |
| S2-26 | EPIC-04 | `BLG-FE-209` — Fix the Replay page's light-theme colour contrast |
| S2-27 | EPIC-04 | `BLG-QA-211` — Decide how real-database-bound modules may persist across pytest files |
| S2-28 | EPIC-05 | `BLG-OPS-187` — Make the daily AI cost alert fail loudly on query or workflow failure |
| S2-29 | EPIC-05 | `BLG-OPS-189` — Deploy both staging services from staging-deploy.yml and wait on each |
| S2-30 | EPIC-05 | `BLG-OPS-18` — Produce the combined data-pipeline cost baseline |
| S2-31 | EPIC-05 | `BLG-OPS-19` — Attribute each external API call to the feature that triggered it |
| S2-32 | EPIC-05 | `BLG-OPS-23` — Benchmark the full screener run |
| S2-33 | EPIC-05 | `BLG-OPS-77` — Assess data-provider risk and failover options |
| S2-34 | EPIC-05 | `BLG-TECH-23` — Assess the major and breaking dependency upgrades from the October 2026 review |
| S2-35 | EPIC-06 | `BLG-GOV-390` — Treat Gate criteria: None/N/A as ungated in the gate scan |
| S2-36 | EPIC-06 | `BLG-GOV-373` — Known-false-positive allow-list for the gate scan |
| S2-37 | EPIC-06 | `BLG-SPEC-184` — Compare documented column defaults in check_data_model_drift.py |
| S2-38 | EPIC-06 | `BLG-GOV-376` — Update strategy_rules.md §13.3 now the Gap Risk Flag's weekend-hold trigger is gone |
| S2-39 | EPIC-06 | `BLG-GOV-377` — Correct strategy_rules.md §13.5's PO-05 roster row |
| S2-40 | EPIC-06 | `BLG-GOV-387` — Correct the v9.8–v9.10 compound Owner count in role_share_history.md |

### Items explicitly deferred

| Item | Reason |
|------|--------|
| `BLG-TECH-21` (P2) | Its own scope requires a dedicated single-EPIC release, and it carries `Provisional-Target: v10.0`. §1.4c override, as at v9.10–v9.12. |
| `BLG-GOV-142`, `BLG-GOV-360`, `BLG-SPEC-199` | Resolution banners (v9.9 ST-19/ST-20; PR #2024). Archive at the next `groom backlog`. |
| `BLG-GOV-368`, `BLG-GOV-361`, `BLG-GOV-374` | Closed as met (✅ COMPLETE, 2026-10-15), met by v9.11's `BLG-SPEC-65` re-gate, and delivered by the 2026-10-16 action-now patch respectively. Archive at the next `groom backlog`. |
| `BLG-FEAT-73`, `BLG-FEAT-76` | Substantively gate-blocked (no formal Gate field; their own text blocks sprint entry). |
| `BLG-FE-195` | Gated item already delivered (gating item `BLG-BE-138` shipped). Archive or narrow at `groom backlog`. |
| 84 further ready items (36.65 days, calibrated) | Capacity. Includes 6 of the 16 items tagged `Provisional-Target: v9.13` (`BLG-AI-19`, `BLG-BE-181`, `BLG-OPS-186`, `BLG-QA-221`, `BLG-QA-226`, `BLG-SPEC-195`), 20 stale `v9.12` tags, `BLG-OPS-85` (newly ungated), and the largest items `BLG-GOV-379` (4.0d), `BLG-QA-218`, `BLG-GOV-380` and `BLG-BE-186` (1.5d each). |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*
