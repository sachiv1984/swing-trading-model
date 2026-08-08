Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-08

# Sprint Execution Escalations — 2026-08-07__release-v8.4

## ESC-EXEC-20260807-01

- **Raised at:** 2026-08-07T16:10:06Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-08-07__release-v8.4
- **Step:** STEP 3 — Execution Loop (EPIC-01/ST-31)
- **ST/EPIC item:** ST-31 (EPIC-01) — Trade-tag/trigger-source column on tax-year P&L CSV export
- **Trigger type:** Quality
- **Blocking statement:** ST-31's acceptance criteria require the tax-year P&L CSV export's new trigger-source column to be "populated correctly for both alert-triggered and manual trades." The story's gate condition (`BLG-FE-116` custom price alerts shipping) was confirmed met at release planning, but that check verified only ship-date, not whether `BLG-FE-116` actually produced a data linkage the column could read from. On inspection: `price_alerts` (the BLG-FE-116 table) has no foreign key to `trade_plans`, `positions`, or `trade_history` — firing an alert (`POST /alerts/evaluate`) only writes a `notifications` row and sets `active=false`/`triggered_at`; it never creates or tags a trade. There is therefore no schema field anywhere that records "this closed trade was opened because a price alert fired." The only existing "trigger"-shaped field is `trade_plans.signal_id`, a nullable FK to the `signals` table — but that is the unrelated momentum-screener signal system, not price alerts. Populating the column from `signal_id` would label trades "Signal" vs "Manual", not "Alert-triggered" vs "Manual" as the AC and backlog item (`BLG-FEAT-78`) specify — a real semantic mismatch in a tax-reporting export, not a naming nicety. Proceeding without a decision risks either (a) fabricating a column that silently misrepresents trade provenance, or (b) building new alert-to-trade linkage plumbing (schema + backend + trade-plan-creation wiring) that is materially larger than this story's S (~1 day) estimate and was not scoped or design-gated for that work.
- **Owning authority:** Product Owner (Financial Reporting & Records Owner as domain sign-off)
- **Unblock criteria:** A decision on one of:
  (a) Reinterpret "trigger-source" as the existing `trade_plans.signal_id` linkage (momentum `signals` system) and relabel the column/AC accordingly (e.g. "Signal-Sourced" vs "Manual") — shippable within current story scope;
  (b) Defer ST-31 to a future cycle, file a new backlog item scoping the actual price-alert-to-trade linkage work (schema + wiring, larger than S effort) as a precondition, and correct `BLG-FEAT-78`'s gate criteria to require that linkage rather than just `BLG-FE-116`'s ship date;
  (c) Some other resolution the Product Owner specifies.
- **SLA due-by:** Before execution (Quality trigger type — may not be marked Accepted Risk)
- **Blocks execution:** No — ST-31 only; ST-01 and other EPICs proceed independently
- **Disposition:** Resolved
- **Resolution summary:** Product Owner selected **Option (a)** (2026-08-07), informed by an agent-mediated domain-perspective analysis on behalf of Financial Reporting & Records Owner (this document is directly this role's territory per its charter — the tax-year P&L CSV is a formal financial record). ST-31 reinterpreted: the column ships this cycle as `trade_origin` (`"Signal"` / `"Manual"`), derived from `trade_plans.signal_id` (the momentum-screener `signals` system, already wired end-to-end) rather than any price-alert linkage, which does not exist in the schema. Implemented in `backend/database.py::get_trade_history_by_tax_year()` (LEFT JOIN to `trade_plans` on `position_id`) and `backend/services/reports_service.py` (JSON + CSV). Documented as a Known Deviation from the original backlog wording in `docs/specs/api_contracts/reports_endpoints.md` (v0.12). `BLG-BE-84` filed for the original alert-linkage ask, tracked separately and unscheduled. No edit made to `BLG-FEAT-78` itself — outside this routine's backlog write scope (new-item-addition only, `execution_prompt.md` §7); flagged here for the next `groom backlog` pass to correct its stale "trigger-source"/alert framing, citing this resolution and `BLG-BE-84`.

## ESC-EXEC-20260808-05

- **Raised at:** 2026-08-08T07:45:00Z
- **Routine:** Sprint Execution
- **Cycle ID:** 2026-08-07__release-v8.4
- **Step:** STEP 3 — Execution Loop (EPIC-06/ST-28)
- **ST/EPIC item:** ST-28 (EPIC-06) — Signal correctness fix impact measurement
- **Trigger type:** Human-Delegation
- **Blocking statement:** ST-28's AC requires running an impact-measurement query against **historical production `signals` table data** generated before the `BLG-BE-40` fix (commit `4d56dc42`, 2026-07-02) to count/quantify affected `suggested_shares` values. This is production historical data with no local/CI equivalent — the same LL-v8.0-P3-01 infra/ops verification pattern as ST-23. **Reclassifying `autonomous` → `delegated_backend`** at STEP 3 (initial-classification correction, no prior delegation record existed for this item). The query itself has been fully authored and is ready to run — see `docs/ops/blg_be_40_impact_measurement_query.sql` (committed this branch) — only its execution against production requires a human with production `DATABASE_URL` access.
- **Owning authority:** Infrastructure & Operations Owner (to execute); Metrics Definitions & Analytics Owner and Product Owner (to review findings per AC)
- **Unblock criteria:** A human with production DB access runs `docs/ops/blg_be_40_impact_measurement_query.sql`, records the output (affected signal count, magnitude, materiality), and both named reviewers sign off per the AC. Findings should be filed as a new `docs/ops/` record (informational — no remediation implied unless a material discrepancy is found, per the story's own scope).
- **SLA due-by:** Next planning checkpoint
- **Blocks execution:** No — ST-28 only; other EPIC-06 items proceed independently
- **Disposition:** Resolved
- **Resolution summary:** Unblocked in-session — Infrastructure & Operations Owner (user) ran `docs/ops/blg_be_40_impact_measurement_query.sql` directly against production, same session as delegation. Result: 0 of 300 pre-fix signals affected (genuine, non-vacuous zero — verified via Step 3's non-zero denominator). Findings documented in `docs/ops/blg_be_40_impact_measurement_findings_2026-08-08.md`. Reviewed by Metrics Definitions & Analytics Owner (agent-mediated, methodology check) and Product Owner (human, confirmed in-session — accepted, no remediation needed). `BLG-QA-70` closed.
