**Owner:** Director of Quality
**Class:** Operational Record (Class 3)
**Status:** Active
**Report Date:** 2026-09-28
**Filed:** 2026-09-28
**Cycle:** 2026-09-23__release-v9.7 (post-ship closure STEP 5.1, cadence-triggered — 3rd Post-Ship Closure invocation since last run)
**Lifecycle Guide:** claude/charter/document_lifecycle_guide.md

---

# Cross-EPIC Deviation (DEV-*) Consolidation Review — Sixth Run

## Objective

Sixth periodic run of the cross-cycle `DEV-*` consolidation review established by `ST-12` (EPIC-04, `2026-08-03__release-v8.1`, `BLG-QA-129`). Cadence: every 3rd Post-Ship Closure invocation. Prior run: `docs/governance/deviation_consolidation_review_2026-09-15.md` (fifth run, 16 records, `2026-09-14__release-v9.4`).

## Method

Scanned every canonical/supporting spec file, QA evidence log, decisions record, and verification report under `docs/` and `claude/cycles/` for `## DEV-*` / `### DEV-*` headings and table-row `DEV-*` entries, covering the three cycles since the last review (`2026-09-15__release-v9.5`, `2026-09-21__release-v9.6`, `2026-09-23__release-v9.7`). Continued the target-release-elapsed check (established second run) and the DEV-ID-assignment-discipline spot-check the fifth run's Recommendation 3 asked for.

## Consolidated Register

16 → 18 formal `DEV-*`-ID records (2 new, both from this cycle's own EPIC-02, both compliant at filing). The pre-existing 16 are unchanged in status.

| DEV ID | Spec File | Priority | Status | Target/Resolved Release |
|--------|-----------|----------|--------|--------------------------|
| DEV-EPIC02-ST04-01 | `frontend/pages/notifications.md` | P3 | Resolved (v2.3) | v2.3 |
| DEV-EPIC01-ST05-01 | `frontend/pages/positions.md` | P2 | Resolved (v7.1) | v7.1 |
| DEV-EPIC02-ST05-03 | `frontend/pages/positions.md` | P2 | Resolved (v2.4) | v2.4 |
| DEV-EPIC02-ST03-01 | `frontend/pages/analytics.md` | P2 | Resolved (v8.6) | v1.10 (originally); resolved v8.6 |
| DEV-REPORTS-ST06-01 | `frontend/pages/reports.md` | P3 | Open — unchanged since 3rd run | TBD — not yet scheduled (filed v7.1, now ~20 releases open) |
| DEV-REPORTS-ST01-02 | `frontend/pages/reports.md` | P3 | Resolved (v8.5) | v8.5 |
| DEV-ST14-01 | `frontend/pages/trade_history.md` + `docs/testing/slippage_scenarios.md` | P3 | Resolved (v2.5) | v2.5 |
| DEV-NAV-ST06-01 | `frontend/pages/navigation.md` | P1 | Resolved (v8.5) | v8.5 |
| DEV-EPIC04-ST09-01 | `api_contracts/ticker_universe_api_contract.md` | P3 | Resolved (same release) | v3.8 |
| DEV-ST04-01 | `api_contracts/alerts_endpoints.md` | P2 | Accepted (PO + DoQ, 2026-03-20) | v2.2 — ~57 releases stale, infra-gated, unchanged assessment |
| DEV-v51-EPIC01-01 | `product/decisions/si05-telegram-message-format-spec.md` | P3 | Resolved (v5.2) | v5.2 |
| DEV-v8.6-ST02-01 | `frontend/pages/trade_plan.md` | P3 | Resolved (v8.7) | v8.7 |
| DEV-EPIC01-ST02-01 | `frontend/pages/positions.md` | P0 | Resolved same-story (v8.9) | v8.9 |
| DEV-v8.9-ST05-01 | `frontend/pages/trade_plan.md` | P3 | Resolved same-story (v8.9) | v8.9 |
| DEV-v8.9-ST05-02 | `frontend/pages/trade_plan.md` | P2 | Resolved same-story (v8.9) | v8.9 |
| DEV-EPIC03-ST09-01 | `docs/ops/api_performance_baseline.md` | P3 | Resolved (v9.0) | Open at v8.9 close → Resolved v9.0 |
| DEV-v9.7-ST05-01 | `frontend/pages/notifications.md` | P4 | Open (new, this cycle) | Backlog — `BLG-SPEC-169` |
| DEV-v9.7-ST04-01 | `frontend/pages/reports.md` | P4 | Open (new, this cycle) | Backlog — `BLG-SPEC-170` |

**Retroactively added this run (see Finding 1):** `DEV-v9.7-ST13-01` (`api_contracts/ai_endpoints.md`, P3, Won't fix, `BLG-BE-128`) — not counted in the 16→18 delta above because the underlying deviation was already disclosed (Changelog v1.14, 2026-09-24) but had no `### DEV-<id>` heading; this run corrected the section, which still read the stale "None at v1.10." **19 formal `DEV-*`-ID records after this run's remediation.**

## Findings

**Finding 1 — DEV-ID assignment discipline gap recurs a third time, now with a worse variant (canonical spec's own summary line goes stale, not just missing an ID):** The fifth run (2026-09-15) found and recommended (Recommendation 1, unfiled) that every `## Known Deviations` entry should carry a `DEV-<id>` from the point of filing. This run found two further, independent instances from the three cycles since:

- **`BLG-BE-128`** (ST-13, EPIC-03, `2026-09-21__release-v9.6`) — `latency_ms` retry-backoff-inclusion, reviewed and disposed "won't fix" 2026-09-24. Documented only in `ai_endpoints.md`'s Changelog table (v1.14) and an inline "Implementation constraints" bullet — the document's own `## Known Deviations` section still read **"None at v1.10."**, a stale summary a reader checking that section specifically would take at face value. **Remediated in this commit:** added `DEV-v9.7-ST13-01` to the Known Deviations section with the required fields, corrected the stale "None" line (deviation compliance fix, within this routine's permitted write scope per §5).
- **`BLG-BE-127`** (ST-12, EPIC-03, `2026-09-21__release-v9.6`, P2 — the UK stamp duty / US FX fee float-rounding under-charge) — disclosed only in `docs/ops/money_arithmetic_audit_2026-09-22.md` (a Class 3 operational record, not a canonical spec) and in `backlog.md`. No canonical spec (`claude/strategy/strategy_rules.md` §4.1.3, the nearest candidate, governs the *floor* behaviour cited alongside it, not the fee-rounding functions themselves) carries a `## Known Deviations` entry for this P2 finding at all — worse than a missing ID, this is a missing *entry*. **Not remediated here:** `claude/strategy/strategy_rules.md` is an explicitly sealed file under this routine's Write Scope (§5), and no other canonical spec was confirmed as the correct owner within this review's time budget — misfiling a Known Deviations entry in the wrong spec would create a second, competing problem. Recorded as an Outstanding Action (`closure_record.md §6`) for the Backend Engineering Patterns Owner to confirm the correct canonical home and add the entry.

This is the third consecutive run surfacing this same class of gap (5th run: `BLG-FE-172`, `BLG-BE-112`+1; this run: `BLG-BE-128`, `BLG-BE-127`) with the underlying process fix — file a `BLG-GOV-*` item requiring every new deviation-shaped disclosure to carry a `DEV-<id>` at filing time, in the canonical spec, not only in an ops doc or changelog row — still unfiled after being recommended twice. **Escalating:** this review recommends the next Post-Ship Closure or `groom backlog` pass file this item directly rather than deferring a third time, given two more real instances have now accumulated on the "still unfiled" watch.

**Finding 2 — Target-release-elapsed check (continued from 2nd–5th runs):** `DEV-ST04-01` (Telegram in place of email, P2, Accepted) remains the sole concrete-target stale entry, now ~57 releases behind v9.7. Unchanged assessment across 6 runs — Accepted with an explicit unmet infrastructure precondition, not a neglected Open item. No action recommended. `DEV-REPORTS-ST06-01` (P3, `TBD — not yet scheduled`) remains open and unscheduled since `v7.1` (~20 releases) — still correctly P3/informational with two scoped candidate fix directions and a named backlog reference (`BLG-SPEC-87`); no dedicated escalation warranted at P3, but flagging the elapsed duration for visibility.

**Finding 3 — No resolution-status drift found among the pre-existing 16 records this run:** consistent with the fifth run — all previously-flagged dual-location or resolved entries remain internally consistent on re-check.

**Finding 4 — This cycle's own new deviations (`DEV-v9.7-ST05-01`, `DEV-v9.7-ST04-01`) were filed correctly at source, with `DEV-<id>` headings and all required fields present from the point of filing** — confirming the discipline gap in Finding 1 is inconsistent (some stories follow it, some don't) rather than systemic across every story, which is itself useful evidence for scoping the `BLG-GOV-*` fix as a checklist/process reminder rather than a tooling gap.

## Recommendations

1. **Escalated — file the DEV-ID assignment discipline item directly at the next opportunity** (Head of Specs Team owns; not filed here — `claude/backlog/backlog.md` net-new process-debt items are outside this routine's Phase-4-traceability-scoped write permission, consistent with how this has been handled at the 1st and 5th runs). Recorded as an Outstanding Action with an explicit "3rd consecutive run" flag in `closure_record.md §6`.
2. **Confirm the correct canonical-spec owner for fee-calculation deviations** (Backend Engineering Patterns Owner) and add `BLG-BE-127`'s Known Deviations entry there — recorded as a second Outstanding Action.
3. **For the next run:** continue the target-release-elapsed check (no re-triage needed for either open entry absent a status change); re-verify whether Recommendation 1's `BLG-GOV-*` item has finally been filed, and if so, spot-check compliance on any deviation filed after it.

## Sign-off

- Signed off by: Sprint Execution Engine (agent-mediated, Director of Quality role — §5.3)
- Date: 2026-09-28
- Comments: Sixth consolidation review, cadence-triggered (3rd Post-Ship Closure invocation since 2026-09-15). 16 pre-existing records reconfirmed unchanged; 2 new compliant records from this cycle's own EPIC-02; 1 stale "None at v1.10" Known Deviations section found and corrected in this commit (`ai_endpoints.md`, `DEV-v9.7-ST13-01` for `BLG-BE-128`). 1 further gap (`BLG-BE-127`, P2, no canonical-spec entry at all) identified but not remediated here — the nearest candidate spec is sealed to this routine and the correct owner was not confirmed in time; recorded as an Outstanding Action. DEV-ID assignment discipline recommendation now stands unfiled across 3 consecutive runs — escalated for direct filing next opportunity.
