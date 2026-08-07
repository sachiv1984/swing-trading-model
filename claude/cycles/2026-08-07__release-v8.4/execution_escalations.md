Owner: PMO Lead
Class: Planning Document (Class 4)
Status: Active
Last Updated: 2026-08-07

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
- **Disposition:** Open
- **Resolution summary:** _(pending)_
