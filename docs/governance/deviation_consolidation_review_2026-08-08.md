**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Report Date:** 2026-08-08
**Filed:** 2026-08-08
**Cycle:** 2026-08-07__release-v8.4 (post-ship closure STEP 5.1, cadence-triggered — 3rd Post-Ship Closure invocation since last run)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Cross-EPIC Deviation (DEV-*) Consolidation Review — Second Run

## Objective

Second periodic run of the cross-cycle `DEV-*` consolidation review established by `ST-12` (EPIC-04, `2026-08-03__release-v8.1`, `BLG-QA-129`). Cadence: every 3rd Post-Ship Closure invocation. Prior run: `docs/governance/deviation_consolidation_review_2026-08-03.md` (first run, cataloguing 9 records as of `2026-08-03__release-v8.1`).

## Method

Scanned every canonical spec file, QA evidence log, decisions record, and verification report under `docs/` and `claude/cycles/` for `## DEV-*` / `### DEV-*` headings (the `Known Deviations` section convention, LL-v3.4-P3-04). 10 distinct deviation records found (one new since the first run: `DEV-REPORTS-ST01-02`, filed this cycle). Two additional headings pre-dating the LL-v3.4-P3-04 convention (`DEV-EPIC02-ST05-02`, `DEV-HEALTH-001`, both embedded directly in `claude/cycles/2026-03-21__release-v2.2/verification_report.md`) were found but excluded from the register, consistent with the first run's scope — these are one-off historical process-deviation acceptances predating the ongoing canonical-spec Known Deviations convention, not entries in the recurring register. Two records (`DEV-EPIC02-ST05-03`, `DEV-v51-EPIC01-01`) have a second, non-canonical location (a QA evidence log) in addition to their canonical spec entry — both spot-checked for resolution-status drift (see Finding 1).

Per Recommendation 2 of the first run, a target-release-elapsed check was added this run: for every `Open`/`Accepted` deviation with a concrete (non-`TBD`) named target release, compare it against the current release (`v8.4`) and flag any more than 2 releases stale.

## Consolidated Register

| DEV ID | Spec File | Priority | Status | Target/Resolved Release |
|--------|-----------|----------|--------|--------------------------|
| DEV-EPIC02-ST04-01 | `frontend/pages/notifications.md` | P3 | Resolved (v2.3) | v2.3 |
| DEV-EPIC02-ST03-01 | `frontend/pages/analytics.md` | P2 | Open | v1.10 (stale — see Finding 2) |
| DEV-ST04-01 | `api_contracts/alerts_endpoints.md` | P2 | Accepted (PO + DoQ, 2026-03-20) | v2.2, pending paid infra (stale — see Finding 2) |
| DEV-EPIC01-ST05-01 | `frontend/pages/positions.md` | P2 | Resolved (v7.1) | v7.1 |
| DEV-EPIC02-ST05-03 | `frontend/pages/positions.md` | P2 | Resolved (v2.4) | v2.4 |
| DEV-REPORTS-ST06-01 | `frontend/pages/reports.md` | P3 | Open | TBD — not yet scheduled |
| DEV-REPORTS-ST01-02 | `frontend/pages/reports.md` | P3 | Open (new, filed `2026-08-07__release-v8.4`, ST-01) | TBD — not yet scheduled |
| DEV-ST14-01 | `frontend/pages/trade_history.md` + `docs/testing/slippage_scenarios.md` | P3 | Resolved (v2.5) — both locations consistent (corrected by first run's Recommendation 1) | v2.5 |
| DEV-EPIC04-ST09-01 | `api_contracts/ticker_universe_api_contract.md` | P3 | Resolved (same release) | v3.8 |
| DEV-v51-EPIC01-01 | `product/decisions/si05-telegram-message-format-spec.md` | P3 | Resolved (v5.2) | v5.2 |

## Findings

**Finding 1 — No new spec/QA-doc resolution-status drift:** The first run's Finding 3 (`DEV-ST14-01` resolved in `slippage_scenarios.md` but not in the canonical spec) was corrected in that same run and remains consistent in this run's re-check. The two other dual-location records (`DEV-EPIC02-ST05-03`, `DEV-v51-EPIC01-01`) were spot-checked: both non-canonical locations are original filing records (no resolution claim made there), so there is no drift to detect — the canonical spec is the sole source of resolution status for both, correctly. No new instance of the drift pattern found this run.

**Finding 2 — Target-release-elapsed check (new this run, per first run's Recommendation 2):** Two deviations carry a concrete named target release more than 2 releases behind the current release (`v8.4`):
- `DEV-EPIC02-ST03-01` (Cohort Analysis client-side computation, P2, **Open**) — target `v1.10`, ~7 major-minor versions and ~60+ releases stale. No re-triage has occurred since the deviation was accepted. **Recommend Head of Specs Team re-triage:** accept as permanent architectural deviation (update spec to match implementation, closing the gap the first run's Finding 2 raised) or schedule a genuine fix.
- `DEV-ST04-01` (Telegram in place of email delivery, P2, **Accepted** by PO+DoQ 2026-03-20) — target `v2.2, pending paid infrastructure`. This one differs qualitatively from the above: it is an *Accepted* deviation with an explicit infrastructure precondition (paid domain + SMTP), not a neglected Open item — the "stale" reading is an artefact of the precondition never having been met, not oversight. No action recommended beyond noting it remains correctly Accepted and infrastructure-gated.

Both open-non-TBD-target deviations found this run are now flagged; the two new `Open`/`TBD`-target deviations (`DEV-REPORTS-ST06-01`, `DEV-REPORTS-ST01-02`) are exempt from this check by construction (no named version to compare) but remain visible in the register for the next run.

**Finding 3 — No recurring category concentration:** Deviations span frontend visual/copy (2), frontend column/layout (2), backend computation-layer (1), backend delivery-channel infrastructure-constraint (1), navigation/routing (1), analytics computation-method (1), data-freshness/staleness framing (2 — both in `reports.md`, see below). `reports.md` now carries 2 of 10 register entries (`DEV-REPORTS-ST06-01`, `DEV-REPORTS-ST01-02`) — both P3, both data-presentation/framing issues on the same page (not the same underlying defect), first light concentration signal on a single spec file. Below the 3+ threshold that would warrant a dedicated audit; noting it for the next run to watch.

## Recommendations

1. **Action Finding 2 directly:** Head of Specs Team to re-triage `DEV-EPIC02-ST03-01` (the genuinely neglected Open item) — disposition options: (a) accept the client-side computation as canonical and update `analytics.md` §15's hard rule to match reality, or (b) schedule the backend-migration fix. Target: before the next `plan release`.
2. **For the next run of this review:** continue the target-release-elapsed check (now established); watch `reports.md`'s 2-entry concentration — if a 3rd `reports.md` deviation is filed before the next run, escalate to a dedicated audit of that spec's data-presentation conventions.
3. **First run's Recommendation 3 (structural fix — resolving-commit-must-update-canonical-spec discipline) remains unimplemented** — not actioned in this run either; still a backlog-item candidate, not filed as one by either review to date.

## Sign-off

- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-08-08
- Comments: Second consolidation review, cadence-triggered (3rd Post-Ship Closure invocation since 2026-08-03). 10 deviation records catalogued (1 new: `DEV-REPORTS-ST01-02`). No new resolution-status drift found. New target-release-elapsed check (first run's Recommendation 2) applied for the first time — surfaced 1 genuinely stale Open deviation (`DEV-EPIC02-ST03-01`) for Head of Specs Team re-triage; 1 Accepted/infra-gated deviation noted as correctly stable, not neglected. First run's Recommendation 3 (structural fix) remains open across both runs.
