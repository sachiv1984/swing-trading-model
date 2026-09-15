**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Report Date:** 2026-09-15
**Filed:** 2026-09-15
**Cycle:** 2026-09-14__release-v9.4 (post-ship closure STEP 5.1, cadence-triggered — 3rd Post-Ship Closure invocation since last run)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Cross-EPIC Deviation (DEV-*) Consolidation Review — Fifth Run

## Objective

Fifth periodic run of the cross-cycle `DEV-*` consolidation review established by `ST-12` (EPIC-04, `2026-08-03__release-v8.1`, `BLG-QA-129`). Cadence: every 3rd Post-Ship Closure invocation. Prior run: `docs/governance/deviation_consolidation_review_2026-09-03.md` (fourth run, cataloguing 16 records as of `2026-08-21__release-v9.0`).

## Method

Scanned every canonical/supporting spec file, QA evidence log, decisions record, and verification report under `docs/` and `claude/cycles/` for `## DEV-*` / `### DEV-*` headings and table-row `DEV-*` entries (the `Known Deviations` section convention, `LL-v3.4-P3-04`), covering the three cycles since the last review (`2026-09-03__release-v9.1`, `2026-09-07__release-v9.2`, `2026-09-09__release-v9.3`) plus this cycle (`2026-09-14__release-v9.4`).

Continued the target-release-elapsed check (established second run): for every `Open`/`Accepted` deviation with a concrete (non-`TBD`) named target release, compared it against the current release (`v9.4`) and flagged any more than 2 releases stale.

## Consolidated Register

No new entries carry a formal `DEV-*` ID this window — the 16-record register from the fourth run is unchanged in composition. See Finding 1 below for why this is not the same as "no new deviation-adjacent activity."

| DEV ID | Spec File | Priority | Status | Target/Resolved Release |
|--------|-----------|----------|--------|--------------------------|
| DEV-EPIC02-ST04-01 | `frontend/pages/notifications.md` | P3 | Resolved (v2.3) | v2.3 |
| DEV-EPIC01-ST05-01 | `frontend/pages/positions.md` | P2 | Resolved (v7.1) | v7.1 |
| DEV-EPIC02-ST05-03 | `frontend/pages/positions.md` | P2 | Resolved (v2.4) | v2.4 |
| DEV-EPIC02-ST03-01 | `frontend/pages/analytics.md` | P2 | Resolved (v8.6) | v1.10 (originally); resolved v8.6 |
| DEV-REPORTS-ST06-01 | `frontend/pages/reports.md` | P3 | Open — unchanged since 4th run | TBD — not yet scheduled |
| DEV-REPORTS-ST01-02 | `frontend/pages/reports.md` | P3 | Resolved (v8.5) | v8.5 |
| DEV-ST14-01 | `frontend/pages/trade_history.md` + `docs/testing/slippage_scenarios.md` | P3 | Resolved (v2.5) | v2.5 |
| DEV-NAV-ST06-01 | `frontend/pages/navigation.md` | P1 | Resolved (v8.5) | v8.5 |
| DEV-EPIC04-ST09-01 | `api_contracts/ticker_universe_api_contract.md` | P3 | Resolved (same release) | v3.8 |
| DEV-ST04-01 | `api_contracts/alerts_endpoints.md` | P2 | Accepted (PO + DoQ, 2026-03-20) | v2.2 — 55 releases stale, infra-gated, see Finding 2 (unchanged) |
| DEV-v51-EPIC01-01 | `product/decisions/si05-telegram-message-format-spec.md` | P3 | Resolved (v5.2) | v5.2 |
| DEV-v8.6-ST02-01 | `frontend/pages/trade_plan.md` | P3 | Resolved (v8.7) | v8.7 |
| DEV-EPIC01-ST02-01 | `frontend/pages/positions.md` | P0 | Resolved same-story (v8.9) | v8.9 |
| DEV-v8.9-ST05-01 | `frontend/pages/trade_plan.md` | P3 | Resolved same-story (v8.9) | v8.9 |
| DEV-v8.9-ST05-02 | `frontend/pages/trade_plan.md` | P2 | Resolved same-story (v8.9) | v8.9 |
| DEV-EPIC03-ST09-01 | `docs/ops/api_performance_baseline.md` | P3 | Resolved (v9.0) | Open at v8.9 close → Resolved v9.0 |

**Net change since fourth run:** 16 → 16 formal `DEV-*`-ID records (0 new). Re-verified all 3 previously-flagged Open/stale/dual-location entries (`DEV-REPORTS-ST06-01`, `DEV-ST04-01`, and the resolved-and-consistent dual-location group) — no change in status or content for any of them.

## Findings

**Finding 1 — New deviation-adjacent entries filed this window skip the `DEV-*` ID convention entirely, making them invisible to this review's own scan method (new pattern, first observed this run):** Two genuinely new deviation-shaped disclosures were filed in the three cycles since the last review, and neither is catalogued above because neither carries a `### DEV-<id>` heading or a `DEV-<id>`-keyed table row:
- `BLG-FE-172` (Arc5ComplianceSection Card 3 text-format/null-display divergence, filed `2026-09-03__release-v9.1` ST-13, resolved `2026-09-07__release-v9.2` ST-04) — recorded in `docs/specs/frontend/components/arc5_compliance_section.md`'s own `## Known Deviations` section, but as unstructured prose keyed only by the backlog reference (`BLG-FE-172`), not a `### DEV-<id>` heading. Confirmed resolved and internally consistent (Changelog table, resolution note, and test references all agree) — no drift found, purely a format-convention gap.
- `BLG-BE-112` + a second, unnamed correlation-ID-mechanism deviation (both filed `2026-09-09__release-v9.3` ST-03, both Open, target `Backlog`) — recorded in `docs/specs/structured_logging_standards.md`'s own `## Known Deviations` section under bold `**Deviation 1**` / `**Deviation 2**` sub-headings, with all the required Known Deviation Standard fields (Description, Canonical requirement, Priority, Target resolution release, Owner, Backlog reference) present and complete — but again, no `DEV-<id>` assigned to either.

Both entries are fully compliant with the `claude/charter/document_lifecycle_guide.md` §9 Known Deviation Documentation Standard's *required fields* — this is not a STEP 5 field-completeness failure (STEP 5 correctly found 0 gaps this cycle, since neither entry belongs to *this* cycle's own newly-filed deviations). It is a narrower, previously-unobserved gap: the standard's fields are populated, but the `DEV-*` ID itself — the join key this consolidation review, `quality_trend_index.md`, and any future cross-reference tooling rely on to find and track a deviation — was never assigned. Both entries were found only via a full-text grep for their backlog IDs, not via the heading-pattern scan this review's Method section (and all 4 prior runs) describes as the primary discovery mechanism. Had their governing backlog items not been named directly in `sprint_close.md`/`verification_report.md` prose, this review would have undercounted by 2 (or 3, counting the structured_logging_standards.md doc's second entry) without any way to detect the gap from the scan itself — the scan cannot report what it structurally cannot see.

**Recommendation:** file a `BLG-GOV-*` item requiring that any new `## Known Deviations` section entry be headed `### DEV-<id>` (or contain an inline `DEV-<id>` token in a table row), even when the entry's own Known Deviation Standard fields are otherwise complete — the ID is what makes an entry discoverable by this review and by `quality_trend_index.md`, independent of field completeness. Not filed directly here (outside this routine's write scope for net-new process-debt items beyond the Phase 4 traceability set — consistent with how Recommendation 1 was handled in the fourth run); recorded as an Outstanding Action in `closure_record.md §6`.

**Finding 2 — Target-release-elapsed check (continued from second/third/fourth runs):** `DEV-ST04-01` (Telegram in place of email delivery, P2, Accepted) remains the sole concrete-target stale entry — target `v2.2, pending paid infrastructure`, now ~55 releases behind `v9.4`. Unchanged assessment across 5 runs: this is an *Accepted* deviation with an explicit infrastructure precondition never having been met, not a neglected Open item. No action recommended.

**Finding 3 — No resolution-status drift found this run (contrast with 3 prior confirmed instances):** Unlike runs 1, 3, and 4 (each of which found and corrected one dual-location spec/QA-doc resolution-status drift), this run found none — all previously-flagged dual-location or resolved entries remain internally consistent. The structural-fix recommendation escalated at the fourth run (require a resolving commit to also update the canonical spec's own labeled fields) still has no filed backlog item; this run adds no new instance of that specific pattern, so it is not re-escalated with new urgency here, but the outstanding request from the fourth run stands.

**Finding 4 — `DEV-REPORTS-ST06-01` still the only genuinely Open, unresolved, unaccepted deviation in the register:** Unchanged since the third run. No dedicated audit warranted — it is P3, correctly labelled informational-only, with a named backlog reference (`BLG-SPEC-87`) and two candidate fix directions already scoped.

## Recommendations

1. **New — DEV-ID assignment discipline (Finding 1):** file `BLG-GOV-*` (Head of Specs Team) requiring every `## Known Deviations` entry to carry a `DEV-<id>` from the point of filing, regardless of format (heading or table row) — recorded as an Outstanding Action in this cycle's `closure_record.md §6`.
2. **Carried from 4th run, still unfiled after 2 consecutive runs (structural fix — resolving-commit-must-update-canonical-spec discipline):** re-flagged as a standing Outstanding Action, not re-escalated with new urgency since no new drift instance occurred this window (Finding 3).
3. **For the next run:** continue the target-release-elapsed check (`DEV-ST04-01` — no re-triage needed absent an infra change); also spot-check whether Recommendation 1's `BLG-GOV-*` item has been filed, and if so, whether any deviation filed after it correctly carries a `DEV-<id>`.

## Sign-off

- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-09-15
- Comments: Fifth consolidation review, cadence-triggered (3rd Post-Ship Closure invocation since 2026-09-03). Formal `DEV-*`-ID register unchanged at 16 records (0 new, 0 status changes, 0 drift found). New finding: 2 deviation-shaped entries filed this window (`BLG-FE-172`, `BLG-BE-112` +1 unnamed) are fully field-complete per the Known Deviation Standard but were never assigned a `DEV-<id>`, making them invisible to this review's heading-based scan method — recommendation to close this gap recorded as an Outstanding Action rather than filed directly (outside this routine's write scope). No new stale target-release entries beyond the known infra-gated `DEV-ST04-01` (now ~55 releases stale, unchanged assessment).
