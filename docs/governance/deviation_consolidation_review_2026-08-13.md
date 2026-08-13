**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Report Date:** 2026-08-13
**Filed:** 2026-08-13
**Cycle:** 2026-08-12__release-v8.7 (post-ship closure STEP 5.1, cadence-triggered — 3rd Post-Ship Closure invocation since last run)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Cross-EPIC Deviation (DEV-*) Consolidation Review — Third Run

## Objective

Third periodic run of the cross-cycle `DEV-*` consolidation review established by `ST-12` (EPIC-04, `2026-08-03__release-v8.1`, `BLG-QA-129`). Cadence: every 3rd Post-Ship Closure invocation. Prior run: `docs/governance/deviation_consolidation_review_2026-08-08.md` (second run, cataloguing 10 records as of `2026-08-07__release-v8.4`).

## Method

Scanned every canonical/supporting spec file, QA evidence log, decisions record, and verification report under `docs/` and `claude/cycles/` for `## DEV-*` / `### DEV-*` headings and table-row `DEV-*` entries (the `Known Deviations` section convention, `LL-v3.4-P3-04`). 12 distinct deviation records found (two new since the second run: `DEV-NAV-ST06-01`, `DEV-v8.6-ST02-01`, both filed at `2026-08-11__release-v8.6`). The same two historical pre-convention headings excluded by prior-run precedent (`DEV-EPIC02-ST05-02`, `DEV-HEALTH-001`, both embedded in `claude/cycles/2026-03-21__release-v2.2/verification_report.md`) remain excluded — one-off historical process-deviation acceptances predating the ongoing canonical-spec Known Deviations convention.

Continued the target-release-elapsed check (established second run): for every `Open`/`Accepted` deviation with a concrete (non-`TBD`) named target release, compared it against the current release (`v8.7`) and flagged any more than 2 releases stale.

## Consolidated Register

| DEV ID | Spec File | Priority | Status | Target/Resolved Release |
|--------|-----------|----------|--------|--------------------------|
| DEV-EPIC02-ST04-01 | `frontend/pages/notifications.md` | P3 | Resolved (v2.3) | v2.3 |
| DEV-EPIC01-ST05-01 | `frontend/pages/positions.md` | P2 | Resolved (v7.1) | v7.1 |
| DEV-EPIC02-ST05-03 | `frontend/pages/positions.md` | P2 | Resolved (v2.4) | v2.4 |
| DEV-EPIC02-ST03-01 | `frontend/pages/analytics.md` | P2 | **Resolved (v8.6, ST-10, BLG-FE-155)** — was Open at last run | v1.10 (originally); resolved v8.6 |
| DEV-REPORTS-ST06-01 | `frontend/pages/reports.md` | P3 | Open | TBD — not yet scheduled |
| DEV-REPORTS-ST01-02 | `frontend/pages/reports.md` | P3 | **Resolved (v8.5, ST-08, BLG-FE-144)** — was Open at last run | v8.5 |
| DEV-ST14-01 | `frontend/pages/trade_history.md` + `docs/testing/slippage_scenarios.md` | P3 | Resolved (v2.5) | v2.5 |
| DEV-NAV-ST06-01 | `frontend/pages/navigation.md` | P1 | Resolved (v8.5) — retroactive record filed v8.6, fix already shipped | v8.5 |
| DEV-EPIC04-ST09-01 | `api_contracts/ticker_universe_api_contract.md` | P3 | Resolved (same release) | v3.8 |
| DEV-ST04-01 | `api_contracts/alerts_endpoints.md` | P2 | Accepted (PO + DoQ, 2026-03-20) | v2.2, pending paid infra (stale — see Finding 2, unchanged) |
| DEV-v51-EPIC01-01 | `product/decisions/si05-telegram-message-format-spec.md` | P3 | Resolved (v5.2) | v5.2 |
| DEV-v8.6-ST02-01 | `frontend/pages/trade_plan.md` | P3 | **Resolved (v8.7, ST-03, BLG-BE-95)** — corrected in this same commit, see Finding 1 | Resolved v8.7 |

**Net change since second run:** 10 → 12 records. 2 new (`DEV-NAV-ST06-01`, `DEV-v8.6-ST02-01`, both filed at v8.6). 3 status changes: `DEV-EPIC02-ST03-01` and `DEV-REPORTS-ST01-02` both moved Open → Resolved (both actioned by name in the second run's own recommendations/watch items); `DEV-v8.6-ST02-01` moved Accepted(Open) → Resolved this run (see Finding 1).

## Findings

**Finding 1 — Spec/QA-doc resolution-status drift (recurring pattern, 2nd confirmed instance):** `DEV-v8.6-ST02-01` (the "AI draft" badge omission, `trade_plan.md`) was accepted-as-shippable at `v8.6` pending `BLG-BE-95` (persist `is_ai_draft` server-side). `BLG-BE-95` shipped this cycle as `v8.7` ST-03 — `qa_evidence_EPIC-01.md` confirms AC-03 ("badge shown when true") passed, and the story's own notes state it is "closing `DEV-v8.6-ST02-01`'s root cause." The canonical spec's Known Deviations row, however, still read `Disposition: Accepted as shippable ... Unscheduled` — not updated to reflect that the badge is now live. Corrected in this same commit (see `docs/specs/frontend/pages/trade_plan.md` Known Deviations table), following the same-commit-correction precedent set by the first run's Finding 3 (`DEV-ST14-01`). This is the same drift class as the first run's finding, now confirmed to recur: a deviation resolved via a story's own QA evidence does not automatically propagate back to the canonical spec's Known Deviations entry, because no step in the normal `plan release → sprint execution` flow re-visits a *pre-existing* deviation row when the story that closes it is a different, later story than the one that filed it.

**Finding 2 — Target-release-elapsed check (continued from second run):** `DEV-ST04-01` (Telegram in place of email delivery, P2, Accepted) remains the sole concrete-target stale entry — target `v2.2, pending paid infrastructure`, now ~40+ releases behind `v8.7`. Unchanged assessment from the second run: this is an *Accepted* deviation with an explicit infrastructure precondition never having been met, not a neglected Open item. No action recommended.

**Finding 3 — No new resolution-status drift beyond Finding 1:** The two other dual-location records flagged for spot-check in prior runs (`DEV-EPIC02-ST05-03`, `DEV-v51-EPIC01-01`) remain Resolved and consistent across both their locations — no drift. `DEV-EPIC02-ST03-01` and `DEV-REPORTS-ST01-02`'s resolutions (both actioned since the second run, per that run's own Recommendation 1 and watch item) are each internally consistent — single canonical-spec location each, resolution note present, no drift.

**Finding 4 — `reports.md` concentration signal resolved, not escalated:** The second run flagged `reports.md` carrying 2 of 10 register entries as a "first light concentration signal ... below the 3+ threshold." One of those two (`DEV-REPORTS-ST01-02`) is now Resolved, leaving `reports.md` with 1 open-shaped entry (`DEV-REPORTS-ST06-01`). No dedicated audit warranted; concentration signal has receded rather than grown.

## Recommendations

1. **Second run's Recommendation 1 confirmed actioned:** `DEV-EPIC02-ST03-01` was re-triaged and resolved at `v8.6` (ST-10, `BLG-FE-155`) — Head of Specs Team disposition (a) taken (client-side computation confirmed already migrated to backend; tracking record updated to match reality). Closed.
2. **Escalating first run's Recommendation 3 (structural fix — resolving-commit-must-update-canonical-spec discipline):** this is now the **2nd confirmed instance** of the same drift pattern across 3 review runs (`DEV-ST14-01` in run 1; none new in run 2; `DEV-v8.6-ST02-01` in run 3) — a genuine, low-but-nonzero recurrence rate rather than a one-off. The structural fix (require any story that closes a *pre-existing* deviation's root cause to also update that deviation's canonical Known Deviations entry in the same commit, e.g. as a new checklist item in `execution_prompt.md`'s STEP 3.1.A deviation-check flow) remains unimplemented and unfiled as a backlog item after 3 runs. **Recorded as an Outstanding Action in this cycle's `closure_record.md` §6** for the Head of Specs Team to file as a governance-process backlog item (`BLG-GOV-*`) before the next `plan release` — post-ship closure's own write scope does not cover filing net-new process-debt backlog items outside the Phase 4 traceability set, so this is flagged rather than filed directly, consistent with how this recommendation has been handled in both prior runs.
3. **For the next run:** continue the target-release-elapsed check; `DEV-ST04-01` remains the only entry to watch (infra-gated, expected to stay stale until paid infrastructure lands — no re-triage needed absent an infra change).

## Sign-off

- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3, per the agent-mediated sign-off convention used consistently throughout this cycle's QA evidence logs and this cycle's own `verification_report.md`)
- Date: 2026-08-13
- Comments: Third consolidation review, cadence-triggered (3rd Post-Ship Closure invocation since 2026-08-08). 12 deviation records catalogued (2 new: `DEV-NAV-ST06-01`, `DEV-v8.6-ST02-01`, both filed v8.6). One new resolution-status drift found and corrected in the same commit (`DEV-v8.6-ST02-01` — Finding 1), the 2nd confirmed instance of this pattern across 3 runs; escalated to a recorded Outstanding Action recommending the structural fix be filed as a backlog item, since 2 prior soft recommendations have not resulted in a filed item. Two prior runs' Open items (`DEV-EPIC02-ST03-01`, `DEV-REPORTS-ST01-02`) both confirmed resolved this run. No new stale target-release entries beyond the known infra-gated `DEV-ST04-01`.
