**Owner:** Head of UX & Design
**Class:** Design Decision Record
**Status:** Approved
**Cycle:** 2026-08-12__release-v8.7
**Story:** ST-01 (EPIC-01, BLG-FEAT-84)

# Decision Record — Thesis Pre-Mortem / Invalidation-Condition Capture at Trade-Plan Entry

## 1. Problem

`BLG-FEAT-84` asks for an optional field at trade-plan entry capturing the trader's own "pre-mortem": under what condition would this thesis be proven wrong? This is distinct from the existing `Early Exit Conditions` field (§5b, AI-generated, execution-level stop/exit logic) — the invalidation condition is a manually-authored, thesis-level statement captured at plan creation, before any AI assist is invoked.

## 2. Decision

Add a new optional field, **"Invalidation Condition"**, to the Trade Plan Creation and Edit Form (`trade_plan.md` §5.1).

- **Placement:** directly below "Risk/Reward Notes" in the form fields table — both are free-text, risk-framing fields entered manually before the AI/checklist sections, so grouping them keeps the form's existing top-to-bottom flow (identity fields → risk framing → tags → checklist) intact rather than inserting a new visual grouping.
- **Type:** Textarea (same control as Risk/Reward Notes).
- **Required:** No.
- **Placeholder / helper copy:** "What would prove this thesis wrong? (optional)" — phrased as a question to prompt the pre-mortem framing, consistent with the field's purpose; not a label restatement.
- **Persistence:** `trade_plans.invalidation_condition` (text, nullable) — implementation detail for `ST-01`, not this record's concern beyond confirming no UI conflict with existing fields.
- **Read-only detail view:** rendered as a labelled text block alongside Risk/Reward Notes in the detail view's existing field list (§7), same treatment — no new component.
- **Not AI-populated:** unlike Setup Thesis / Entry Rationale / Confirmation Criteria / Early Exit Conditions, this field is intentionally excluded from the "Improve with AI" population list (§5b) — the pre-mortem's value depends on it being the trader's own reasoning, not model-suggested text. This is a deliberate scope boundary, not an oversight.

## 3. §13 Compliance

Manually-authored, optional, free-text field. No automated interpretation, no gating of trade entry or plan status. No AI involvement (see exclusion above). Outside `strategy_rules.md §13`'s scope entirely.

## 4. Edge Cases

| State | Behaviour |
|-------|-----------|
| Field left blank | Persists as `null`; no validation error; detail view omits the field entirely (same "hidden entirely when absent" convention used elsewhere in this spec, e.g. §10.3) |
| Field populated, plan later edited | Free text, editable at any time via the standard edit form — no lock/versioning |
| "Improve with AI" invoked | Field is not touched — no AI population, no clearing |

## 5. Approval

Head of UX & Design: confirmed, 2026-08-12.
Product Owner: confirmed, 2026-08-12 (field placement/copy — per `ST-01`'s own AC).
