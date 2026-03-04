**Owner:** Cybersecurity & Trust Lead
**Class:** Planning Document (Class 4)
**Status:** Submitted
**Submitted by:** Cybersecurity & Trust Lead
**Submitted at:** 2026-03-04
**Window ID:** IW-20260304-01
**Idea ID:** IDEA-cybersecurity-20260304-01

---

# Idea: System Threat Model Document

## 1. Problem Statement

There is no documented threat model for the trading system. It is currently unknown: what authentication is required to access the API endpoints, what happens on repeated failed authentication attempts, what the attack surface is (public endpoints, database access, admin functions), and what the trust boundaries are between the frontend, backend, and database. A system handling real financial data — live trading positions, entry and exit prices, P&L — without a documented threat model is operating with undocumented security assumptions. Undocumented assumptions are vulnerabilities.

## 2. Strategic Alignment

Section reference: Cybersecurity §4.1 — "define and maintain system threat models; identify trust boundaries, attack surfaces, and privilege domains; ensure security assumptions are documented and reviewed"

Alignment rationale: A threat model is the foundational security document from which all other security controls derive. Without it, security decisions are reactive — adding controls only after a threat is observed — rather than proactive. The Cybersecurity role's mandate is explicitly to define and maintain this document; its absence is a gap in the role's core deliverables.

## 3. Proposed Solution

Create `docs/security/threat_model.md` — a Class 1 canonical document covering: (1) system components and their trust boundaries (frontend, FastAPI backend, PostgreSQL database, CI/CD pipeline), (2) identified attack surfaces for each component (API endpoints, database connection strings, admin access), (3) threat actors and their assumed capabilities, (4) existing controls and gaps, and (5) the review cadence (annually at minimum, or after any architectural change). Use the STRIDE methodology (Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege) as the analysis framework.

## 4. Expected Value

Makes security posture explicit and auditable. Required for any future security review, penetration test, or compliance audit. Provides the baseline against which any new feature's security implications can be assessed. Expected to surface 3–7 undocumented trust assumptions in the first iteration.

## 5. Effort Estimate

- [x] Medium — 1–3 weeks

Constraints or dependencies: Requires input from the Head of Engineering (implementation details), the Infrastructure & Operations Owner (deployment topology), and the Backend Engineering Patterns Owner (API authentication model).

## 6. Reversibility

- [x] Fully reversible — no lasting effects

Reasoning: A threat model is documentation; producing it creates no technical commitments.

## 7. What Would You Stop?

No view — leave to debate. Security governance documents are foundational, not optional.

## 8. Submitter Recommendation

- [x] Now — should be in the next roadmap cycle

Reasoning: Every day without a threat model is a day operating with undocumented security assumptions in a system that handles live financial data. This is not a luxury.

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
