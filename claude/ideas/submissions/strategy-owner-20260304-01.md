**Owner:** Strategy Rules & System Intent Owner
**Class:** Planning Document (Class 4)
**Status:** Advancing
**Submitted by:** Strategy Rules & System Intent Owner
**Submitted at:** 2026-03-04
**Window ID:** IW-20260304-01
**Idea ID:** IDEA-strategy-owner-20260304-01

---

# Idea: Backtest vs Live Stop Reconciliation Report

## 1. Problem Statement

The live system computes trailing stops daily and stores them in the database. The canonical backtest applies the same rules to historical data. However, there is no automated check that the stops stored in the live database match what the canonical rules would compute for the same positions on the same day. If implementation drift occurs — a calculation function is modified, a parameter is incorrectly applied, or a state transition is handled differently — the live stops may silently diverge from what the strategy specifies. A trader acting on incorrect stop levels is the primary failure mode of this system.

## 2. Strategic Alignment

Section reference: §11 — Current production parameters ("must be consistent across production backtests, live system logic, and reported performance metrics")

Alignment rationale: The strategy rules document is the behavioural contract between strategy intent and system implementation. Section 11 explicitly requires consistency between backtests, live logic, and documentation. The reconciliation report is the mechanism for verifying this constraint is met in production, continuously — not just at implementation time.

## 3. Proposed Solution

Implement a weekly reconciliation script that: (1) reads all open positions from the live database, (2) recomputes what the stop should be per canonical strategy rules using the same inputs (entry_price, ATR, current_price, position_state), and (3) compares the recomputed stop against the stored stop. Any discrepancy greater than the defined precision tolerance is logged as a reconciliation failure and escalated to the Strategy Owner and Head of Engineering. Results are stored as a weekly reconciliation record.

## 4. Expected Value

Detects implementation drift in trailing stop calculations before it causes an incorrect exit recommendation or a missed exit. Target: zero discrepancies per weekly run in steady state. Any week with a discrepancy produces an immediate investigation. Expected to detect the class of bug most likely to cause material trading harm.

## 5. Effort Estimate

- [x] Medium — 1–3 weeks

Constraints or dependencies: The reconciliation script must implement the canonical rules independently from the production code — otherwise it merely re-runs the same potentially-wrong implementation. Requires careful design to ensure the script is the canonical implementation, not a copy.

## 6. Reversibility

- [x] Fully reversible — no lasting effects

Reasoning: The report is read-only; it produces no changes to the live system.

## 7. What Would You Stop?

No view — leave to debate. This is a safety control, not a feature; stopping it would be removing a safety net without replacement.

## 8. Submitter Recommendation

- [x] Now — should be in the next roadmap cycle

Reasoning: Implementation drift in stop calculations is the most consequential possible defect in this system. The cost of not catching it is a real financial loss. The cost of the reconciliation report is one medium task.

---

## Intake Review

*Completed by the roadmap rebalance engine (STEP 4). Do not fill in this section.*

| Field | Value |
|-------|-------|
| STEP 4 classification | ✅ Advancing |
| Classification date | 2026-03-04 |
| Classified by | Product Owner |
| STEP 5 outcome | ✅ Advance — promoted to backlog (dependency: after golden baseline) |
| Outcome date | 2026-03-04 |
| Notes | |
