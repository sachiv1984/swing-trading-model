Owner: Head of Specs Team
Class: Planning Document (Class 4)
Status: Superseded
Release: v9.12
Cycle: 2026-10-12__release-v9.12
Last Updated: 2026-10-15

Superseded by: v9.12 ship — 2026-10-15
Changelog: docs/product/changelog.md#v9.12
Verification report: claude/cycles/2026-10-12__release-v9.12/verification_report.md
Cycle: 2026-10-12__release-v9.12

## Release Scope — v9.12

48 items across 6 EPICs, 27.95 estimated days, at the top of the ~24–28 day band ("use full capacity"). Acceptance criteria are in `claude/cycles/2026-10-12__release-v9.12/stage4_backlog_slice.md`.

### Items in scope

| S2-ID | Epic | Description |
|-------|------|-------------|
| S2-01 | EPIC-01 | `BLG-BE-162` — Accept UUID trade IDs in the journal summary, end to end |
| S2-02 | EPIC-01 | `BLG-AI-11` — Drop briefing actions that name a ticker outside the context |
| S2-03 | EPIC-01 | `BLG-AI-12` — Label available cash and starting capital separately in the briefing context |
| S2-04 | EPIC-01 | `BLG-AI-10` — Check that briefing and chat responses citing a stop include its recalculation time |
| S2-05 | EPIC-01 | `BLG-AI-13` — Widen the monthly P&L narrative's instrument-directive scan to inflected and indirect wording |
| S2-06 | EPIC-01 | `BLG-OPS-183` — Make the daily AI cost alert count Claude calls |
| S2-07 | EPIC-02 | `BLG-BE-157` — Give zero-ATR signals no allocation in batch sizing |
| S2-08 | EPIC-02 | `BLG-BE-158` — Include entry fees in batch signal total cost |
| S2-09 | EPIC-02 | `BLG-QA-205` — Assert the §4.1.5 FX defaulting/echo and §4.1.6 insufficient-cash sizing results in CI |
| S2-10 | EPIC-02 | `BLG-BE-159` — Make the Trail Stop action work against a real route, or remove it; stop ignoring a supplied entry stop |
| S2-11 | EPIC-02 | `BLG-BE-160` — Never let 2-dp rounding lower a stored stop |
| S2-12 | EPIC-02 | `BLG-BE-145` — Recompute US positions with a NULL fill_price without error, and add US parity cases |
| S2-13 | EPIC-02 | `BLG-BE-149` — Decide Risk page LOSING/PROFITABLE on native P&L, matching the lifecycle badge |
| S2-14 | EPIC-02 | `BLG-BE-148` — Use the US exchange calendar for the gap-risk "next trading session" |
| S2-15 | EPIC-02 | `BLG-FE-202` — Show the user when a position's stop is frozen for lack of ATR |
| S2-16 | EPIC-02 | `BLG-BE-144` — Keep first-time Settings saves from writing NULL strategy columns; snapshot §11 values on trade plans |
| S2-17 | EPIC-03 | `BLG-BE-146` — Add an ATR preview endpoint so Trade Entry shows the stop, risk and size before save |
| S2-18 | EPIC-03 | `BLG-FE-203` — Show the currency unit on Trade Entry's ATR field and reject implausible typed ATRs |
| S2-19 | EPIC-03 | `BLG-QA-206` — Cover the §4.1.7 sizing-widget behaviours with Playwright |
| S2-20 | EPIC-03 | `BLG-FE-201` — Correct the Settings helper text for the fixed strategy parameters |
| S2-21 | EPIC-03 | `BLG-GOV-369` — Strategy-copy conformance: a frontend constants module, a CI lint for UI text restating §5–§11, and a named owner |
| S2-22 | EPIC-03 | `BLG-FE-207` — Link each Grace Period row to its position, and align the panel's text and date format with the spec |
| S2-23 | EPIC-03 | `BLG-FE-200` — Make the Reports and Notifications pages pass WCAG colour contrast in the light theme |
| S2-24 | EPIC-03 | `BLG-FE-210` — Move white-on-amber-600 badges to a passing contrast outside Replay |
| S2-25 | EPIC-04 | `BLG-OPS-184` — Stop the post-grace stop-health monitor alerting on the morning a position's grace ends |
| S2-26 | EPIC-04 | `BLG-SEC-41` — Audit trail for strategy-parameter changes in Settings |
| S2-27 | EPIC-04 | `BLG-SEC-42` — Re-assess the bundled `REACT_APP_API_KEY` against its actual write scope |
| S2-28 | EPIC-04 | `BLG-TECH-22` — Apply the in-range dependency patch/minor bumps from the October 2026 quarterly review |
| S2-29 | EPIC-04 | `BLG-OPS-181` — Find out why a staging-deploy.yml hook deploy of a governance-only commit never went live |
| S2-30 | EPIC-04 | `BLG-OPS-182` — Live-fire the stale-staging check from main against a deliberate divergence |
| S2-31 | EPIC-04 | `BLG-OPS-185` — Add requirements-dev.txt to the local backend setup instructions |
| S2-32 | EPIC-04 | `BLG-GOV-371` — Inventory the scheduled GitHub workflows: owner, cron, tables written, monthly minutes |
| S2-33 | EPIC-05 | `BLG-SPEC-176` — Reconcile DELETE /trade-plans/{id}'s success envelope with conventions.md §12 |
| S2-34 | EPIC-05 | `BLG-SPEC-178` — Triage the drift detector's new live-vs-doc findings |
| S2-35 | EPIC-05 | `BLG-SPEC-179` — Name the Gap Risk Badge's real data source in positions.md |
| S2-36 | EPIC-05 | `BLG-SPEC-181` — Replace positions.stop_price with current_stop in the action-rate spec and docstring |
| S2-37 | EPIC-05 | `BLG-SPEC-182` — Refresh the Gap Risk Flag §13 decision record to match strategy_rules.md v1.14 |
| S2-38 | EPIC-05 | `BLG-SPEC-183` — Settle positions.entry_price's currency in the specs |
| S2-39 | EPIC-06 | `BLG-GOV-385` — Check backlog item integrity after every cross-EPIC merge resolution |
| S2-40 | EPIC-06 | `BLG-GOV-386` — Report gated items whose gating backlog item has shipped, and read that list in Release Planning §1.3a |
| S2-41 | EPIC-06 | `BLG-GOV-363` — Script the execution_state.json read-back check from execution_prompt.md §9.2 |
| S2-42 | EPIC-06 | `BLG-GOV-367` — Name one Skill-Silo aggregation method in roadmap_prompt.md §7.1 |
| S2-43 | EPIC-06 | `BLG-GOV-364` — Rule on reduced-roster idea-intake windows, and cap them if permitted |
| S2-44 | EPIC-06 | `BLG-GOV-372` — Add a split-credit secondary tally to compute_role_share_history.py |
| S2-45 | EPIC-06 | `BLG-QA-212` — Add unit tests for compute_role_share_history.py and a STEP 7.1 pin |
| S2-46 | EPIC-06 | `BLG-QA-209` — Scope utils.* test stubs so a reordered run passes |
| S2-47 | EPIC-06 | `BLG-QA-213` — Guard the positions.fees_paid NOT NULL invariant in the entry flow and SQL seeds |
| S2-48 | EPIC-06 | `BLG-QA-202` — Remove the leaked sandbox /tmp path from backend/setup.cfg |

### Items explicitly deferred

| Item | Reason |
|------|--------|
| `BLG-TECH-21` (P2) | Its own scope requires a dedicated single-EPIC release, and it carries `Provisional-Target: v10.0`. Recorded as a §1.4c override, as at v9.10 and v9.11. |
| `BLG-GOV-142`, `BLG-GOV-360` (P2) | Already resolved in v9.9 (ST-19, ST-20). Archive at the next `groom backlog` (third carry). |
| `BLG-GOV-368` (P2) | Prompt half applied in `execution_prompt.md` v3.82; only the optional CI mirror remains. Narrow or close at the next `groom backlog` (v9.11 closure #6). |
| `BLG-GOV-361` (P4) | Met by v9.11's `BLG-SPEC-65` re-gate. Archive at the next `groom backlog`. |
| `BLG-FEAT-73`, `BLG-FEAT-76` | Substantively gate-blocked (no formal Gate field; their own text blocks sprint entry). |
| `BLG-SPEC-180`, `BLG-SPEC-184`, `BLG-SPEC-186`, `BLG-SPEC-188` | Ready, but capacity. Aged 2+ cycles without a story (§1.1 advisory); recommended for v9.13. |
| 49 further ready items (24.25 days) | Capacity. Includes 22 items tagged `Provisional-Target: v9.12` (`BLG-BE-163`–`172`, `BLG-FE-211`–`217`, `BLG-QA-219`/`220`, `BLG-SPEC-191`/`192`, `BLG-GOV-384`), plus `BLG-GOV-379`/`380`/`383`, `BLG-TECH-23`, `BLG-QA-218` and `BLG-FE-208`/`209`. |

### Supersession note
*To be completed at Post-Ship Closure — do not populate at planning time.*
