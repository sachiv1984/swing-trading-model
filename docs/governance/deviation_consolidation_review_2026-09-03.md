**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Report Date:** 2026-09-03
**Filed:** 2026-09-03
**Cycle:** 2026-08-21__release-v9.0 (post-ship closure STEP 5.1, cadence-triggered — 3rd Post-Ship Closure invocation since last run)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Cross-EPIC Deviation (DEV-*) Consolidation Review — Fourth Run

## Objective

Fourth periodic run of the cross-cycle `DEV-*` consolidation review established by `ST-12` (EPIC-04, `2026-08-03__release-v8.1`, `BLG-QA-129`). Cadence: every 3rd Post-Ship Closure invocation. Prior run: `docs/governance/deviation_consolidation_review_2026-08-13.md` (third run, cataloguing 12 records as of `2026-08-12__release-v8.7`).

## Method

Scanned every canonical/supporting spec file, QA evidence log, decisions record, and verification report under `docs/` and `claude/cycles/` for `## DEV-*` / `### DEV-*` headings and table-row `DEV-*` entries (the `Known Deviations` section convention, `LL-v3.4-P3-04`). 16 distinct deviation records found (4 new since the third run: `DEV-EPIC01-ST02-01`, `DEV-v8.9-ST05-01`, `DEV-v8.9-ST05-02`, `DEV-EPIC03-ST09-01`, all filed at `2026-08-17__release-v8.9`). The two historical pre-convention headings excluded by prior-run precedent (`DEV-EPIC02-ST05-02`, `DEV-HEALTH-001`, both embedded in `claude/cycles/2026-03-21__release-v2.2/verification_report.md`) remain excluded. `2026-08-21__release-v9.0` (this cycle) filed zero new deviations — confirmed via `verification_report.md §4` — so no new records originate from this cycle's own execution; the 4 new records were all filed at the prior cycle (v8.9) and are being catalogued here for the first time because this review did not run between v8.7 and now.

Continued the target-release-elapsed check (established second run): for every `Open`/`Accepted` deviation with a concrete (non-`TBD`) named target release, compared it against the current release (`v9.0`) and flagged any more than 2 releases stale.

## Consolidated Register

| DEV ID | Spec File | Priority | Status | Target/Resolved Release |
|--------|-----------|----------|--------|--------------------------|
| DEV-EPIC02-ST04-01 | `frontend/pages/notifications.md` | P3 | Resolved (v2.3) | v2.3 |
| DEV-EPIC01-ST05-01 | `frontend/pages/positions.md` | P2 | Resolved (v7.1) | v7.1 |
| DEV-EPIC02-ST05-03 | `frontend/pages/positions.md` | P2 | Resolved (v2.4) | v2.4 |
| DEV-EPIC02-ST03-01 | `frontend/pages/analytics.md` | P2 | Resolved (v8.6, ST-10, BLG-FE-155) | v1.10 (originally); resolved v8.6 |
| DEV-REPORTS-ST06-01 | `frontend/pages/reports.md` | P3 | Open | TBD — not yet scheduled |
| DEV-REPORTS-ST01-02 | `frontend/pages/reports.md` | P3 | Resolved (v8.5, ST-08, BLG-FE-144) | v8.5 |
| DEV-ST14-01 | `frontend/pages/trade_history.md` + `docs/testing/slippage_scenarios.md` | P3 | Resolved (v2.5) | v2.5 |
| DEV-NAV-ST06-01 | `frontend/pages/navigation.md` | P1 | Resolved (v8.5) — retroactive record filed v8.6 | v8.5 |
| DEV-EPIC04-ST09-01 | `api_contracts/ticker_universe_api_contract.md` | P3 | Resolved (same release) | v3.8 |
| DEV-ST04-01 | `api_contracts/alerts_endpoints.md` | P2 | Accepted (PO + DoQ, 2026-03-20) | v2.2, pending paid infra (stale — see Finding 2, unchanged) |
| DEV-v51-EPIC01-01 | `product/decisions/si05-telegram-message-format-spec.md` | P3 | Resolved (v5.2) | v5.2 |
| DEV-v8.6-ST02-01 | `frontend/pages/trade_plan.md` | P3 | Resolved (v8.7, ST-03, BLG-BE-95) | v8.7 |
| DEV-EPIC01-ST02-01 | `frontend/pages/positions.md` | **P0** | **New this run.** Resolved same-story (v8.9, ST-02, BLG-BE-103) — carve-out per §7/LL-v8.6-P4-03 | v8.9 |
| DEV-v8.9-ST05-01 | `frontend/pages/trade_plan.md` | P3 | **New this run.** Resolved same-story (v8.9, ST-05) | v8.9 |
| DEV-v8.9-ST05-02 | `frontend/pages/trade_plan.md` | P2 | **New this run.** Resolved same-story (v8.9, ST-05) | v8.9 |
| DEV-EPIC03-ST09-01 | `docs/ops/api_performance_baseline.md` | P3 | **New this run.** Filed v8.9 as Open; **resolved v9.0 (ST-02, BLG-BE-107)** — labeled-field drift found and corrected this same commit, see Finding 1 | Open at v8.9 close → Resolved v9.0 |

**Net change since third run:** 12 → 16 records. 4 new, all filed at `2026-08-17__release-v8.9`. 1 status change during this review's own window: `DEV-EPIC03-ST09-01` moved Open (as of v8.9 close, per that cycle's `Verified_with_deviations` disposition) → Resolved (v9.0, this cycle's ST-02 closing `BLG-BE-107`'s root cause).

## Findings

**Finding 1 — Spec/QA-doc resolution-status drift (recurring pattern, 3rd confirmed instance, corrected this commit):** `DEV-EPIC03-ST09-01` was resolved this cycle (`2026-08-21__release-v9.0`, ST-02, `BLG-BE-107`) — `api_performance_baseline.md §36.7` (added 2026-09-03) records the real Render-log confirmation in full narrative form and states "resolved" in prose. Its own labeled `Known Deviation fields` block at §36.5, however, still read `Target resolution release: Superseded once BLG-BE-107 lands ... no fixed release targeted yet` — not updated to reflect that `BLG-BE-107` has, in fact, landed and the deviation is closed. Corrected in this same commit (see `docs/ops/api_performance_baseline.md` §36.5 labeled fields, Document History v2.32). This is the same drift class identified at the first run (`DEV-ST14-01`) and the third run (`DEV-v8.6-ST02-01`) — now a **3rd confirmed instance across 4 review runs**, spanning three different canonical/supporting documents (`trade_history.md`, `trade_plan.md`, `api_performance_baseline.md`), which rules out a single-document-specific cause.

**Finding 2 — Target-release-elapsed check (continued from second/third runs):** `DEV-ST04-01` (Telegram in place of email delivery, P2, Accepted) remains the sole concrete-target stale entry — target `v2.2, pending paid infrastructure`, now ~48 releases behind `v9.0`. Unchanged assessment: this is an *Accepted* deviation with an explicit infrastructure precondition never having been met, not a neglected Open item. No action recommended.

**Finding 3 — No new drift beyond Finding 1:** The 3 other new records this run (`DEV-EPIC01-ST02-01`, `DEV-v8.9-ST05-01`, `DEV-v8.9-ST05-02`) are each single-location (one canonical spec file each) and internally consistent — resolution narrative present, no separate QA/testing-doc location to drift against. The previously-flagged dual-location records (`DEV-EPIC02-ST05-03`, `DEV-v51-EPIC01-01`, `DEV-ST14-01`) remain Resolved and consistent across both their locations — no new drift found there.

**Finding 4 — `reports.md` concentration signal unchanged:** `reports.md` carries 1 open-shaped entry (`DEV-REPORTS-ST06-01`) and 1 resolved (`DEV-REPORTS-ST01-02`) — unchanged from the third run. No dedicated audit warranted.

**Finding 5 — First P0-priority deviation in the register, carve-out mechanism confirmed working as intended:** `DEV-EPIC01-ST02-01` (Trail Stop tile currency-basis bug, `BLG-BE-103`) is the register's first P0-priority entry across all 4 runs. It qualified for the Resolved-same-story carve-out (§7, `LL-v8.6-P4-03`) rather than blocking `v8.9`'s merge gate, because its canonical spec entry (`positions.md#Known Deviations`) states the full resolution narrative rather than an open/accepted disposition. This review confirms the carve-out mechanism produced the intended outcome here: the underlying currency-basis bug was fixed in the same story that filed the deviation, not deferred, and the spec record reflects that accurately with no drift. Recorded as a positive confirmation, not a new finding requiring action.

## Recommendations

1. **Escalating first/third run's Recommendation (structural fix — resolving-commit-must-update-canonical-spec discipline) for a 3rd consecutive time:** this is now the **3rd confirmed instance** of the same drift pattern across 4 review runs (`DEV-ST14-01` in run 1; none new in run 2; `DEV-v8.6-ST02-01` in run 3; `DEV-EPIC03-ST09-01` in this run), spanning 3 different documents. The structural fix (require any story/engine action that closes a *pre-existing* deviation's root cause to also update that deviation's own labeled Known Deviation fields in the same commit) has now been recommended in 3 of 4 runs with **zero backlog item filed** despite each run explicitly naming this as the next step. Post-ship closure's own write scope does not cover filing net-new process-debt backlog items outside the Phase 4 traceability set, so — consistent with how this has been handled in all 3 prior runs — it is flagged rather than filed directly here, but recorded as an **escalated Outstanding Action** in this cycle's `closure_record.md §6` with an explicit request that the Head of Specs Team file it as a `BLG-GOV-*` item before the *next* Post-Ship Closure review (i.e. before a 4th confirmed instance can accrue with still no tracking item open).
2. **For the next run:** continue the target-release-elapsed check; `DEV-ST04-01` remains the only entry to watch (infra-gated, expected to stay stale until paid infrastructure lands — no re-triage needed absent an infra change).
3. **No action required on Finding 5** — recorded for pattern-tracking continuity only (first P0 in the register; carve-out behaved as designed).

## Sign-off

- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3, per the agent-mediated sign-off convention used consistently throughout this cycle's QA evidence logs and this cycle's own `verification_report.md`)
- Date: 2026-09-03
- Comments: Fourth consolidation review, cadence-triggered (3rd Post-Ship Closure invocation since 2026-08-13). 16 deviation records catalogued (4 new, all filed `v8.9`: `DEV-EPIC01-ST02-01`, `DEV-v8.9-ST05-01`, `DEV-v8.9-ST05-02`, `DEV-EPIC03-ST09-01`). One resolution-status drift found and corrected in the same commit (`DEV-EPIC03-ST09-01` — Finding 1), the 3rd confirmed instance of this pattern across 4 runs; escalated to a recorded Outstanding Action with an explicit request that the structural-fix backlog item be filed before the next review, since 3 prior soft recommendations have not resulted in a filed item. No new stale target-release entries beyond the known infra-gated `DEV-ST04-01`. First P0-priority entry in the register (`DEV-EPIC01-ST02-01`) confirmed the Resolved-same-story carve-out mechanism working as intended.
