**Owner:** Data Model & Domain Schema Owner
**Class:** Planning Document (Class 4)
**Status:** Submitted
**Submitted by:** Data Model & Domain Schema Owner
**Submitted at:** 2026-03-04
**Window ID:** IW-20260304-01
**Idea ID:** IDEA-data-model-owner-20260304-02

---

# Idea: Data Retention and Archiving Policy

## 1. Problem Statement

Trade and position history accumulates indefinitely in the database with no documented retention or archiving policy. A user who has been trading for 3–5 years could accumulate thousands of closed trade records. There is no specification for when historical trades should be archived, whether soft or hard deletion is used, or what happens to the data of a user who stops using the system. Without a policy, the database grows without bound and any future data subject access request or deletion request has no documented procedure to follow.

## 2. Strategic Alignment

Section reference: §13 — System boundaries ("a single, explicit, human-designed strategy; human-in-the-loop by design")

Alignment rationale: The system boundary definition includes what the system is — a trading decision-support tool. It implicitly includes what data the system is responsible for managing. Data retention is a domain-level governance responsibility: if the system stores financial records, it must specify how long it keeps them and how it handles their lifecycle. This is not a new concern — it is an unspecified aspect of the existing data scope.

## 3. Proposed Solution

Create `docs/specs/data_model/data_retention_policy.md` — a Class 1 canonical document defining: (1) retention periods by data class (open positions: indefinite while open; closed trades: 7 years for UK financial record-keeping compliance; settings: indefinite; analytics history: 5 years), (2) archiving mechanism (e.g., move to a cold storage table after retention threshold), (3) deletion policy (soft delete vs hard delete, who can trigger a deletion, and what audit trail exists), and (4) the review trigger (any schema change affecting retained data classes).

## 4. Expected Value

Prevents unbounded database growth. Provides a documented compliance posture for UK financial record-keeping requirements. Enables a clear procedure if a user requests data deletion. Estimated to prevent 20–30% uncontrolled database growth annually once archiving is implemented. Required before any future data export or multi-user feature is developed.

## 5. Effort Estimate

- [x] Small — days to 1 week

Constraints or dependencies: Requires input from the Product Owner (what data is in scope), the Cybersecurity Lead (deletion requirements), and the Head of Engineering (implementation approach for archiving).

## 6. Reversibility

- [x] Mostly reversible — minor rework required

Reasoning: The policy document is reversible; any archiving infrastructure built to implement it requires more effort to reverse.

## 7. What Would You Stop?

No view — leave to debate.

## 8. Submitter Recommendation

- [x] Soon — worth debating in the next 2–3 cycles

Reasoning: Not urgent today but grows in importance with each month of data accumulation. Should be defined before the database size becomes a problem to solve reactively.

---

## Intake Review

*Completed by the roadmap rebalance engine (STEP 4). Do not fill in this section.*

| Field | Value |
|-------|-------|
| STEP 4 classification | |
| Classification date | |
| Classified by | Product Owner |
| STEP 5 outcome | |
| Outcome date | |
| Notes | |
