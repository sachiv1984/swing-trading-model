**Owner:** Cybersecurity & Trust Lead
**Class:** Planning Document (Class 4)
**Status:** Parked-cycle-2
**Submitted by:** Cybersecurity & Trust Lead
**Submitted at:** 2026-03-04
**Window ID:** IW-20260304-01
**Idea ID:** IDEA-cybersecurity-20260304-02

---

# Idea: Sensitive Data Classification Policy

## 1. Problem Statement

The system stores financial data (live position prices, entry/exit prices, P&L, portfolio value) and trading behaviour data (entry notes, exit notes, tags) that are inherently sensitive. There is no documented classification of which data fields are sensitive, how they are protected at rest and in transit, and what the data retention or deletion policy is. In the absence of classification, it is impossible to make a principled decision about who can access the data, how long it should be kept, or what constitutes a data breach requiring notification.

## 2. Strategic Alignment

Section reference: Cybersecurity §4.2 — "ensure authentication, authorization, and data protection are explicit; validate alignment between canonical specs and security posture"

Alignment rationale: Data protection requires knowing what data exists and how sensitive it is before any control can be designed or verified. The classification policy is the prerequisite for authentication design, access control, encryption decisions, and retention policies. Without it, every downstream security decision is made without a data inventory — which means it may be wrong in ways that are not visible.

## 3. Proposed Solution

Create `docs/security/data_classification.md` — a Class 1 canonical document defining: (1) sensitivity tiers (Confidential: financial data and credentials; Internal: operational and governance documents; Public: none in this system), (2) protection requirements for each tier (encryption at rest, TLS in transit, access control requirements), (3) a field-level classification of key database tables (positions, trades, portfolio, settings), and (4) a retention and deletion policy (how long each data class is kept, and what triggers a deletion event).

## 4. Expected Value

Provides the data inventory required for authentication design, access control implementation, and retention policy enforcement. Required before any feature that involves sharing data externally (e.g., the benchmark comparison feature, any email digest feature). Expected to surface 2–5 data fields currently stored without documented protection requirements.

## 5. Effort Estimate

- [x] Small — days to 1 week

Constraints or dependencies: Requires input from the Data Model Owner (field inventory) and the Head of Engineering (current protection controls). The classification is a governance document, not a code change.

## 6. Reversibility

- [x] Fully reversible — no lasting effects

Reasoning: A classification document can be revised; it creates no technical commitments.

## 7. What Would You Stop?

No view — leave to debate.

## 8. Submitter Recommendation

- [x] Now — should be in the next roadmap cycle

Reasoning: Should be done alongside or immediately after the threat model, as the two documents are complementary foundations for the security programme.

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
