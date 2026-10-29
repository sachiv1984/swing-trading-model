**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Report Date:** 2026-10-29
**Filed:** 2026-10-29
**Cycle:** 2026-10-16__release-v9.13 (post-ship closure STEP 5.1, cadence-triggered — 3rd Post-Ship Closure invocation since last run)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Cross-EPIC Deviation (DEV-*) Consolidation Review — Eighth Run

## Objective

Eighth periodic run of the cross-cycle `DEV-*` consolidation review established by `ST-12` (EPIC-04, `2026-08-03__release-v8.1`, `BLG-QA-129`). Cadence: every 3rd Post-Ship Closure invocation. Prior run: `docs/governance/deviation_consolidation_review_2026-10-07.md` (seventh run, 25 records, `2026-10-06__release-v9.10`).

## Method

Covered the three cycles since the last review: `2026-10-08__release-v9.11`, `2026-10-12__release-v9.12` and `2026-10-16__release-v9.13`.

- Scanned every spec, testing doc, decisions record, QA evidence log and verification report under `docs/` and `claude/strategy/` for `DEV-*` identifiers in any format: headings, bold paragraphs and `## Known Deviations` table rows. Also diffed `docs/` and `claude/strategy/` from the last commit on 2026-10-07 to `HEAD` for any added `DEV-*` identifier or "Known deviation" text, so that entries written without a `DEV-*` ID were also found (see Finding 1).
- For every open record, checked that its backlog reference still resolves to an active `claude/backlog/backlog.md` item, not an archived one.
- Re-verified the seventh run's Recommendations 1 and 2, and continued the target-release-elapsed check.

## Consolidated Register

**No new formal `DEV-*` records were filed in the three cycles covered.** `sprint_close.md` for v9.11, v9.12 and v9.13 each reads "No new canonical-spec `DEV-*` records were filed". The diff since 2026-10-07 added no new `DEV-*` identifier; the four that appear in it are status or reference edits to existing records.

Two deviation-shaped records were found that carry no `DEV-*` ID, both in `claude/strategy/strategy_rules.md` and both from v9.13 (marked ‡ below; see Finding 1).

Status changes since the seventh run:
- `DEV-v9.7-ST04-01` changed from Open to **Resolved (v9.11, ST-29, `BLG-SPEC-170`)**. The spec entry carries a ✅ RESOLVED status line.
- `DEV-REPORTS-ST06-01` is still Open, but its tracking is restored: the backlog reference now names `BLG-SPEC-203` (re-filed 2026-10-15), which is active.
- `DEV-v3.4-01` is now marked **Resolved — v3.5** in `trade_plan.md`'s Known Deviations table (v1.19, 2026-10-15).

The register now holds **27 records**: the 25 from the seventh run and the two ‡ records.

| DEV ID | Spec File | Priority | Status | Target/Resolved Release |
|--------|-----------|----------|--------|--------------------------|
| DEV-EPIC02-ST04-01 | `frontend/pages/notifications.md` | P3 | Resolved (v2.3) | v2.3 |
| DEV-EPIC01-ST05-01 | `frontend/pages/positions.md` | P2 | Resolved (v7.1) | v7.1 |
| DEV-EPIC02-ST05-03 | `frontend/pages/positions.md` | P2 | Resolved (v2.4) | v2.4 |
| DEV-EPIC02-ST03-01 | `frontend/pages/analytics.md` | P2 | Resolved (v8.6) | v1.10 (originally); resolved v8.6 |
| DEV-REPORTS-ST06-01 | `frontend/pages/reports.md` | P3 | Open — **tracking restored** (`BLG-SPEC-203`, active) | TBD — not yet scheduled (filed v7.1) |
| DEV-REPORTS-ST01-02 | `frontend/pages/reports.md` | P3 | Resolved (v8.5) | v8.5 |
| DEV-ST14-01 | `frontend/pages/trade_history.md` + `docs/testing/slippage_scenarios.md` | P3 | Resolved (v2.5) | v2.5 |
| DEV-NAV-ST06-01 | `frontend/pages/navigation.md` | P1 | Resolved (v8.5) | v8.5 |
| DEV-EPIC04-ST09-01 | `api_contracts/ticker_universe_api_contract.md` | P3 | Resolved (same release) | v3.8 |
| DEV-ST04-01 | `api_contracts/alerts_endpoints.md` | P2 | Accepted (PO + DoQ, 2026-03-20) | v2.2 — infra-gated, assessment unchanged |
| DEV-v51-EPIC01-01 | `product/decisions/si05-telegram-message-format-spec.md` | P3 | Resolved (v5.2) | v5.2 |
| DEV-v8.6-ST02-01 | `frontend/pages/trade_plan.md` | P3 | Resolved (v8.7) | v8.7 |
| DEV-EPIC01-ST02-01 | `frontend/pages/positions.md` | P0 | Resolved same-story (v8.9) | v8.9 |
| DEV-v8.9-ST05-01 | `frontend/pages/trade_plan.md` | P3 | Resolved same-story (v8.9) | v8.9 |
| DEV-v8.9-ST05-02 | `frontend/pages/trade_plan.md` | P2 | Resolved same-story (v8.9) | v8.9 |
| DEV-EPIC03-ST09-01 | `docs/ops/api_performance_baseline.md` | P3 | Resolved (v9.0) | v9.0 |
| DEV-v9.7-ST05-01 | `frontend/pages/notifications.md` | P4 | Resolved (v9.9, ST-34) | v9.9 |
| DEV-v9.7-ST04-01 | `frontend/pages/reports.md` | P4 | **Resolved (v9.11, ST-29)**, changed this run | v9.11 |
| DEV-v9.7-ST13-01 | `api_contracts/ai_endpoints.md` | P3 | Won't fix (`BLG-BE-128`) | N/A |
| DEV-v9.1-ST13-01 | `frontend/components/arc5_compliance_section.md` | — | Resolved (v9.2, ST-04, `BLG-FE-172`) | v9.2 |
| DEV-v9.3-ST03-01 | `structured_logging_standards.md` | P3 | Resolved (v9.5, ST-02, `BLG-BE-112`) | v9.5 |
| DEV-v9.3-ST03-02 | `structured_logging_standards.md` | P3 | Open — documentation-freshness note, no backlog item by design | Backlog (next revision of §Correlation ID Scheme) |
| DEV-HEALTH-001 | `api_contracts/health_endpoints.md` | — | Resolved (v2.3, ST-07, `BLG-SPEC-D14`) | v2.3 |
| DEV-v3.4-01 | `frontend/pages/trade_plan.md` (Known Deviations table) | P3 | **Resolved — v3.5** (row corrected 2026-10-15, changed this run) | v3.5 |
| DEV-EPIC03-ST05-01 | `docs/testing/risk_dashboard_scenarios.md` (testing doc only) | P3 | Accepted behaviour (SC-DH-10 asserts it) | N/A |
| *(no ID)* ‡ §8.4 known deviation (v1.17) | `claude/strategy/strategy_rules.md` §8.4 | P3 (per `verification_report.md` §4) | Open — **entry lacks Priority, Target, Owner and backlog ID** (Finding 1) | TBD — `BLG-BE-187` (active) |
| *(no ID)* ‡ US sizing FX inversion | `claude/strategy/strategy_rules.md` §4.1.5 | P2 (accepted PO + DoQ, 2026-10-29) | Open — **no Known Deviations entry** (Finding 1) | v9.14 — `BLG-BE-190` (active) |

## Findings

**Finding 1: the STEP 5 route for a missing Known Deviations entry does not reach `strategy_rules.md`.**
- **What happened.** v9.13 produced two deviations against `claude/strategy/strategy_rules.md`. ST-05's §8.4 entry exists as a one-line bullet with a description and canonical requirement, but no Priority, Target resolution release, Owner or backlog ID ("Tracked in the backlog"; the item is `BLG-BE-187`). The ST-14 found defect, `BLG-BE-190` (P2, accepted), has no entry. Delivery Verification routed it to Post-Ship Closure STEP 5, as the `ESC-CLOSE-20260930-03` ruling intends.
- **Why it stalled.** STEP 5's carve-out allows canonical-spec edits, but `post_ship_closure.md` §5 lists `strategy_rules.md` as sealed for that routine, and CLAUDE.md §2 forbids edits to `claude/strategy/` unless the prompt instructs them. An edit also needs a version bump and a `DOCUMENTATION_ONLY_VERSIONS` entry in `backend/strategy_version_registry.py`, a code change. The user chose to escalate: `ESC-CLOSE-20261029-01`, to the Strategy Rules & System Intent Owner.
- **Neither record has a `DEV-*` ID.** `strategy_rules.md` has never used `DEV-*` IDs for its known deviations, so a heading or ID scan finds neither. This run found them only through the "Known deviation" text diff.
- **The seventh run's Finding 5 watch.** That run closed the DEV-ID discipline watch, to be re-opened "only if a future run finds a Known Deviations-shaped disclosure that did not pass through that path". `BLG-BE-190` did pass through the path, but the path ended at a write it cannot make. **This review re-opens the watch, narrowed to `strategy_rules.md`.**

**Finding 2: no resolution-status drift this window.** `DEV-v9.7-ST04-01`'s tracking item `BLG-SPEC-170` shipped in v9.11, and the spec entry was updated in the same story with a ✅ RESOLVED line. This is the sync rule (`BLG-GOV-315` / `BLG-GOV-332`) working as designed.

**Finding 3: the seventh run's recommendations are both closed.**
- Recommendation 1: `DEV-REPORTS-ST06-01` names `BLG-SPEC-203`, which is active (re-filed 2026-10-15, v9.12 closure §6 row 3).
- Recommendation 2: `DEV-v3.4-01` is marked "Resolved — v3.5" in `trade_plan.md` (v1.19, v9.12 closure §6 row 5).

**Finding 4: target-release-elapsed check (continued).**
- `DEV-ST04-01` (P2, Accepted) is still the only stale entry with a concrete target. Its precondition is still unmet infrastructure, and the assessment has not changed across 8 runs.
- `DEV-REPORTS-ST06-01` (P3) has been open since v7.1, with target TBD. It now has active tracking.

## Recommendations

1. **Resolve `ESC-CLOSE-20261029-01`.** Add the `BLG-BE-190` entry under §4.1.5 and complete the §8.4 entry's fields (`BLG-BE-187`). The escalation carries the proposed text. Owner: Strategy Rules & System Intent Owner.
2. **Give `strategy_rules.md` known deviations a path and an ID.** Either authorise Post-Ship Closure STEP 5 to write routed entries in `strategy_rules.md` (with the version-registry step), or route them to the file owner by default. Consider assigning `DEV-*` IDs to `strategy_rules.md` entries so that ID scans find them. Owner: Head of Specs Team, with the Strategy Rules & System Intent Owner. Tracked by the same escalation (option (c)).
3. **For the next run:**
   - Keep the broadened scan, and keep the "Known deviation" text diff for entries with no `DEV-*` ID.
   - Keep the active-backlog-reference check for every open record.
   - Re-verify Recommendations 1 and 2.
   - Continue the target-release-elapsed check.

## Sign-off

- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-10-29
- Comments: Eighth consolidation review, cadence-triggered (3rd Post-Ship Closure invocation since 2026-10-07). Pending human confirmation.
  - No new formal `DEV-*` records in v9.11 to v9.13. `DEV-v9.7-ST04-01` and `DEV-v3.4-01` are now Resolved, and `DEV-REPORTS-ST06-01` has active tracking again.
  - The register grows from 25 to 27, adding two `strategy_rules.md` deviations from v9.13 that have no `DEV-*` ID.
  - Both of those are blocked by a write-scope conflict, escalated as `ESC-CLOSE-20261029-01` (Finding 1). The DEV-ID discipline watch is re-opened, narrowed to `strategy_rules.md`.
