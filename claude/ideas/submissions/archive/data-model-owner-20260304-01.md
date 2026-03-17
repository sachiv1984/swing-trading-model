**Owner:** Data Model & Domain Schema Owner
**Class:** Planning Document (Class 4)
**Status:** Promoted-Added
**Submitted by:** Data Model & Domain Schema Owner
**Submitted at:** 2026-03-04
**Window ID:** IW-20260304-01
**Idea ID:** IDEA-data-model-owner-20260304-01

---

# Idea: Positions Table Data Dictionary

## 1. Problem Statement

The positions table is the central data structure of the trading system — it stores live trading positions that drive every calculation, stop recommendation, and portfolio metric. Yet the meaning, source, and update trigger for each field is not documented in a canonical data dictionary. Fields such as `fx_rate`, `live_fx_rate`, `grace_period`, `grace_days_remaining`, `display_status`, and `current_stop` are present in the API responses, but an engineer joining the team must infer their meaning from the backend code, the API contracts, and the strategy spec simultaneously. This is tribal knowledge risk in the most critical data structure in the system.

## 2. Strategic Alignment

Section reference: §4 — Position entry rules ("required at entry: ticker, entry_date, entry_price, shares, ATR value"); §9 — Position states ("GRACE, LOSING, PROFITABLE, EXITED — states are mutually exclusive and deterministic")

Alignment rationale: The data model must faithfully represent the strategy's state machine. A data dictionary is the canonical mapping between the strategy spec's logical concepts (position state, stop level, grace period) and the database fields that implement them. Without it, there is no systematic way to verify that the database schema correctly implements the strategy spec — which is a category of drift risk the Head of Specs Team has identified as a priority concern.

## 3. Proposed Solution

Create `docs/specs/data_model/positions_data_dictionary.md` — a Class 1 canonical document mapping each column in the positions table to: (1) its canonical definition, (2) its data type and precision, (3) its source (user-entered, system-calculated, FX-derived), (4) the event that triggers an update, and (5) the canonical spec section that governs its value. Cross-reference the strategy_rules.md state machine definitions. Reviewed and updated as part of any schema change PR.

## 4. Expected Value

Reduces onboarding time for engineers working with the positions table from hours of cross-document archaeology to minutes of reading one document. Makes schema changes reviewable against canonical intent. Expected to surface 1–3 fields whose current implementation diverges from their intended meaning as defined in the strategy spec.

## 5. Effort Estimate

- [x] Small — days to 1 week

Constraints or dependencies: Requires collaboration between the Data Model Owner, the Strategy Owner, and the Backend Engineering Patterns Owner to verify field semantics against their respective specifications.

## 6. Reversibility

- [x] Fully reversible — no lasting effects

Reasoning: A documentation artefact; no system changes required.

## 7. What Would You Stop?

No view — leave to debate.

## 8. Submitter Recommendation

- [x] Now — should be in the next roadmap cycle

Reasoning: The positions table data dictionary is a prerequisite for any schema migration governance — it defines what the schema means before any change can be assessed against canonical intent.

---

## Intake Review

*Completed by the roadmap rebalance engine (STEP 4). Do not fill in this section.*

| Field | Value |
|-------|-------|
| STEP 4 classification | 🅿 Parked |
| Classification date | 2026-03-04 |
| Classified by | Product Owner |
| STEP 5 outcome | N/A — not advanced to STEP 5 debate |
| Outcome date | N/A |
| Notes | |
