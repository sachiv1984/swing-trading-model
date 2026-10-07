**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Report Date:** 2026-10-07
**Filed:** 2026-10-07
**Cycle:** 2026-10-06__release-v9.10 (post-ship closure STEP 5.1, cadence-triggered — 3rd Post-Ship Closure invocation since last run)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Cross-EPIC Deviation (DEV-*) Consolidation Review — Seventh Run

## Objective

Seventh periodic run of the cross-cycle `DEV-*` consolidation review established by `ST-12` (EPIC-04, `2026-08-03__release-v8.1`, `BLG-QA-129`). Cadence: every 3rd Post-Ship Closure invocation. Prior run: `docs/governance/deviation_consolidation_review_2026-09-28.md` (sixth run, 19 records after remediation, `2026-09-23__release-v9.7`).

## Method

Covered the three cycles since the last review: `2026-09-28__release-v9.8`, `2026-09-30__release-v9.9` and `2026-10-06__release-v9.10`.

- Scanned every spec, testing doc, decisions record, QA evidence log and verification report under `docs/` and `claude/cycles/` for `DEV-*` identifiers in any format. The scan was not limited to `## DEV-*` / `### DEV-*` headings. It also covered bold-paragraph entries (`**DEV-…**`) and `## Known Deviations` table rows (see Finding 2).
- For every open record, checked that its backlog reference still resolves to an active `claude/backlog/backlog.md` item, not an archived one (see Finding 1).
- Continued the target-release-elapsed check and the DEV-ID assignment discipline watch from the sixth run.

## Consolidated Register

**No new formal `DEV-*` records were filed in the three cycles covered.** `sprint_close.md` for v9.8, v9.9 and v9.10 each reads "No new canonical-spec `DEV-*` records were filed". The five QA-evidence `Pass_with_deviation` results from those cycles were all assessed at Delivery Verification STEP 3 and recorded as exempt from Known Deviations sync, each with a stated rationale under the `ESC-CLOSE-20260930-03` scope:
- v9.8 ST-17 → `BLG-OPS-171`, shipped v9.10
- v9.9 ST-01 → owner ruling, no remainder
- v9.10 ST-18 → `BLG-OPS-182`
- v9.10 ST-20 → `BLG-GOV-377`

Status changes since the sixth run: `DEV-v9.7-ST05-01` changed from Open to **Resolved (v9.9, ST-34)**.

The broadened scan found 6 canonical-spec records that earlier registers had omitted (marked † below). The register now holds **25 records**.

| DEV ID | Spec File | Priority | Status | Target/Resolved Release |
|--------|-----------|----------|--------|--------------------------|
| DEV-EPIC02-ST04-01 | `frontend/pages/notifications.md` | P3 | Resolved (v2.3) | v2.3 |
| DEV-EPIC01-ST05-01 | `frontend/pages/positions.md` | P2 | Resolved (v7.1) | v7.1 |
| DEV-EPIC02-ST05-03 | `frontend/pages/positions.md` | P2 | Resolved (v2.4) | v2.4 |
| DEV-EPIC02-ST03-01 | `frontend/pages/analytics.md` | P2 | Resolved (v8.6) | v1.10 (originally); resolved v8.6 |
| DEV-REPORTS-ST06-01 | `frontend/pages/reports.md` | P3 | **Open — backlog reference orphaned (Finding 1)** | TBD — not yet scheduled (filed v7.1, ~23 releases open) |
| DEV-REPORTS-ST01-02 | `frontend/pages/reports.md` | P3 | Resolved (v8.5) | v8.5 |
| DEV-ST14-01 | `frontend/pages/trade_history.md` + `docs/testing/slippage_scenarios.md` | P3 | Resolved (v2.5) | v2.5 |
| DEV-NAV-ST06-01 | `frontend/pages/navigation.md` | P1 | Resolved (v8.5) | v8.5 |
| DEV-EPIC04-ST09-01 | `api_contracts/ticker_universe_api_contract.md` | P3 | Resolved (same release) | v3.8 |
| DEV-ST04-01 | `api_contracts/alerts_endpoints.md` | P2 | Accepted (PO + DoQ, 2026-03-20) | v2.2 — ~60 releases behind, infra-gated, assessment unchanged |
| DEV-v51-EPIC01-01 | `product/decisions/si05-telegram-message-format-spec.md` | P3 | Resolved (v5.2) | v5.2 |
| DEV-v8.6-ST02-01 | `frontend/pages/trade_plan.md` | P3 | Resolved (v8.7) | v8.7 |
| DEV-EPIC01-ST02-01 | `frontend/pages/positions.md` | P0 | Resolved same-story (v8.9) | v8.9 |
| DEV-v8.9-ST05-01 | `frontend/pages/trade_plan.md` | P3 | Resolved same-story (v8.9) | v8.9 |
| DEV-v8.9-ST05-02 | `frontend/pages/trade_plan.md` | P2 | Resolved same-story (v8.9) | v8.9 |
| DEV-EPIC03-ST09-01 | `docs/ops/api_performance_baseline.md` | P3 | Resolved (v9.0) | v9.0 |
| DEV-v9.7-ST05-01 | `frontend/pages/notifications.md` | P4 | **Resolved (v9.9, ST-34)**, changed this run | v9.9 |
| DEV-v9.7-ST04-01 | `frontend/pages/reports.md` | P4 | Open | Backlog — `BLG-SPEC-170` (active) |
| DEV-v9.7-ST13-01 | `api_contracts/ai_endpoints.md` | P3 | Won't fix (`BLG-BE-128`) | N/A |
| DEV-v9.1-ST13-01 † | `frontend/components/arc5_compliance_section.md` | — | Resolved (v9.2, ST-04, `BLG-FE-172`) | v9.2 |
| DEV-v9.3-ST03-01 † | `structured_logging_standards.md` | P3 | Resolved (v9.5, ST-02, `BLG-BE-112`) | v9.5 |
| DEV-v9.3-ST03-02 † | `structured_logging_standards.md` | P3 | Open — documentation-freshness note, no backlog item by design | Backlog (next revision of §Correlation ID Scheme) |
| DEV-HEALTH-001 † | `api_contracts/health_endpoints.md` | — | Resolved (v2.3, ST-07, `BLG-SPEC-D14`) | v2.3 |
| DEV-v3.4-01 † | `frontend/pages/trade_plan.md` (Known Deviations table) | P3 | **Resolution-status drift (Finding 3)**: backlog item `BLG-SPEC-31` ✅ COMPLETE v3.5, spec row not marked resolved | v3.5 |
| DEV-EPIC03-ST05-01 † | `docs/testing/risk_dashboard_scenarios.md` (testing doc only) | P3 | Accepted behaviour (SC-DH-10 asserts it) | N/A |

## Findings

**Finding 1: an open P3 deviation's only tracking item was archived without shipping.**
- **What happened.** `DEV-REPORTS-ST06-01` (`reports.md`) gives `BLG-SPEC-87` as its backlog reference. That item was removed from `claude/backlog/backlog.md` at the `2026-08-03__release-v8.1` post-ship closure (commit `47c369ad`). In `backlog_archive.md` it sits directly under `BLG-SPEC-86`'s retirement block, with no retirement header of its own and `Provisional-Target: TBD`.
- **Evidence it never shipped.** `BLG-SPEC-87` does not appear in any cycle's `stage4_backlog_slice.md` or in the changelog. `get_estimated_unrealised_pnl()` (`backend/services/reports_service.py:154`) still sums the stored `positions.pnl`, which is the behaviour the deviation describes.
- **Effect.** Since 2026-08-03 this open deviation has had no active tracking item. No `groom backlog`, roadmap rebalance or release planning pass can surface it. The sixth run did not catch this, because it checked only that a backlog reference was present, not that it was still active.
- **Not remediated here.** `claude/backlog/backlog.md` accepts only shipped-item and Phase-4 additions from this routine, so re-filing is out of scope. The gap is recorded as an Outstanding Action (`closure_record.md §6`) for the Frontend Specifications & UX Documentation Owner, who should restore `BLG-SPEC-87` to the active backlog or re-file it.

**Finding 2: earlier registers missed records that are not written as headings.** The method recorded since the first run scans `## DEV-*` / `### DEV-*` headings. It misses entries written as:
- bold paragraphs, for example `**DEV-v9.3-ST03-01 — RESOLVED …**` in `structured_logging_standards.md`
- `## Known Deviations` table rows, for example `DEV-v3.4-01` in `trade_plan.md`
- testing-doc deviation tables

The sixth run also left out `DEV-v9.1-ST13-01`, which is written as a heading. Six records are added here (marked †). Four are resolved, one is accepted, and one (`DEV-v9.3-ST03-02`) is open with no backlog item, by its own stated design. Apart from Finding 3, none of the six needs action. The only problem is that earlier registers undercounted.

**Finding 3: resolution-status drift on `DEV-v3.4-01`.** `trade_plan.md`'s Known Deviations table still gives "v3.5 — codebase scan; full resolution per BLG-SPEC-31" as the target. `BLG-SPEC-31` is archived ✅ COMPLETE v3.5 (ST-09, 2026-05-15). This is the drift pattern this review exists to catch: a resolved backlog item whose status never reached the spec's own entry. Status is not one of the §3 required fields that STEP 5 may correct, so it is not edited here. Recorded as an Outstanding Action for the Frontend Specifications & UX Documentation Owner. The sync rule for future resolving commits already exists (`BLG-GOV-315` / `BLG-GOV-332`). This entry predates that rule.

**Finding 4: target-release-elapsed check (continued).**
- `DEV-ST04-01` (P2, Accepted) is still the only stale entry with a concrete target. Its precondition is still unmet infrastructure, and the assessment has not changed across 7 runs.
- `DEV-REPORTS-ST06-01` (P3) has been open since v7.1. Per Finding 1, it has also had no active tracking item since v8.1.

**Finding 5: DEV-ID assignment discipline watch (sixth-run Recommendation 1).** No separate `BLG-GOV-*` item was ever filed. However, the `ESC-CLOSE-20260930-03` Head of Specs Team ruling (2026-10-05) now covers the substance:
- Delivery Verification STEP 3 runs a Known Deviations sync for every QA-evidence `Pass_with_deviation`.
- A wholly missing entry is routed to `post_ship_closure.md` STEP 5, which must create it in either mode.

Across v9.8 to v9.10, every deviation-shaped disclosure (5 of them) got an explicit recorded disposition under that rule, and no new instance of the gap appeared. **This review considers the recommendation addressed by the ruling and closes the watch.** Re-open it only if a future run finds a Known Deviations-shaped disclosure that did not pass through that path.

## Recommendations

1. **Restore tracking for `DEV-REPORTS-ST06-01`.** Restore `BLG-SPEC-87` to the active backlog, or re-file it. Owner: Frontend Specifications & UX Documentation Owner. Recorded as an Outstanding Action.
2. **Mark `DEV-v3.4-01` resolved** in `trade_plan.md`'s Known Deviations table, citing `BLG-SPEC-31` (v3.5, ST-09). Owner: Frontend Specifications & UX Documentation Owner. Recorded as an Outstanding Action.
3. **For the next run:**
   - Keep the broadened scan (headings, bold paragraphs, Known Deviations table rows and testing-doc tables).
   - Keep the active-backlog-reference check for every open record.
   - Re-verify Recommendations 1 and 2.
   - Continue the target-release-elapsed check.

## Sign-off

- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-10-07
- Comments: Seventh consolidation review, cadence-triggered (3rd Post-Ship Closure invocation since 2026-09-28). Pending human confirmation.
  - No new formal `DEV-*` records in v9.8 to v9.10. `DEV-v9.7-ST05-01` is now Resolved.
  - The register grows from 19 to 25 because the broadened scan found 6 previously unregistered records.
  - 1 open deviation (`DEV-REPORTS-ST06-01`) has had no active tracking item since v8.1 (Finding 1).
  - 1 resolution-status drift (`DEV-v3.4-01`, Finding 3).
  - Neither is remediated here, because both are outside this routine's write scope. Both are recorded as Outstanding Actions.
  - The DEV-ID discipline watch is closed as addressed by the `ESC-CLOSE-20260930-03` ruling.
