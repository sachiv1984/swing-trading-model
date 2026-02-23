Owner: Head of Specs Team
Status: Canonical  
Version: 1.1  
Last Updated: 2026-02-23  

---

# Team Charter – Roles & Accountability

**Momentum Trading Assistant**

---

## 1. Purpose

This document defines **how authority, ownership, and accountability are distributed** across the Momentum Trading Assistant organisation.

It exists to ensure that:

- Every decision domain has a single accountable owner
- Canonical truth prevails over implementation, analytics, or interpretation
- Validation is independent from execution and delivery pressure
- Financial, technical, and strategic integrity are preserved as the system evolves

This charter describes an **authority model**, not a people management structure.

---

## 2. Core Operating Principles

- **Single ownership per decision domain**
- **Canonical documentation over tribal knowledge**
- **Explicit boundaries prevent silent scope creep**
- **Validation is evidence‑based and independent**
- **Analytics explain behaviour; records assert facts**
- **Tools execute decisions; they do not define truth**

---

## 3. Authority Groupings (Conceptual — Thin Layer)

The roles in this organisation are grouped conceptually to clarify **decision domains and escalation paths**.

These groupings:

- Do **not** introduce management layers
- Do **not** change reporting relationships
- Do **not** dilute individual role authority

They exist solely to explain **why multiple roles operate as executive‑level peer authorities** and how responsibilities are partitioned.

---

### 3.1 Product & Strategy Authority

Owns product intent, strategic boundaries, and trading behaviour.

- **Product Owner**  
  Owns product intent, prioritisation, roadmap trade‑offs, and outcome accountability.
- **Strategy Rules & System Intent Owner**  
  Owns the deterministic trading strategy, lifecycle rules, and system boundaries.

---

### 3.2 Specification & Canonical Truth Authority

Owns the definition, coherence, and lifecycle of system truth.

- **Head of Specs Team**  
  Owns the coherence, governance, and lifecycle of all canonical specifications.
- **Data Model & Domain Schema Owner**  
  Owns financial and domain data semantics.
- **Metrics Definitions & Analytics Canonical Owner**  
  Owns analytical meaning, formulas, and validation tolerances.
- **API Contracts & Documentation Owner**  
  Owns API behaviour, request/response contracts, and versioning discipline.
- **Frontend Specifications & UX Documentation Owner**  
  Owns user‑visible behaviour and UX intent as canonical documentation.

---

### 3.3 Delivery & Execution Authority

Owns implementation, operational reliability, and execution discipline.

- **Head of Engineering**  
  Owns system implementation, delivery execution, and operational reliability.
- **Infrastructure & Operations Owner**  
  Owns deployment, environments, runbooks, and operational documentation.
- **Backend Engineering Patterns Owner**  
  Owns backend implementation standards and patterns.
- **Base44 Frontend Prompt Owner**  
  Owns translation of frontend canonical specs into Base44 prompts and code integration.

---

### 3.4 Independent Assurance & Trust

Owns correctness, validation, security, and externally defensible outputs.  
These roles are **structurally independent from delivery pressure**.

- **Director of Quality**
- **QA & Testing Owner**
- **QA Lead**
- **Cybersecurity & Trust Lead**
- **Financial Reporting & Records Owner**
- **AI Compliance & Governance Officer**

---

### 3.5 Delivery Governance

Owns sequencing, state, and process integrity across initiatives.

- **PMO Lead**

---

### 3.6 People & Sustainability

Owns organisational health, resourcing, and long‑term viability.

- **Director of HR**
- **FinOps & Resource Architect**

---

### 3.7 Process Integrity & Challenge Roles (Non‑Decision)

These roles exist to ensure **process correctness, disciplined challenge, and governance enforcement**.

They are explicitly **non‑decision authorities**.

They do **not**:
- Own outcomes
- Set priorities
- Make trade‑offs
- Advocate for initiatives
- Express opinions on value or strategy

They exist to prevent:
- Skipped governance steps
- Implicit or informal decisions
- Unchallenged assumptions
- Process degradation over time

- **Facilitator**  
  Owns execution integrity of governed routines.  
  May halt execution for non‑compliance but may not influence outcomes.

- **Challenger**  
  Owns structured challenge and assumption testing.  
  May delay advancement until questions are answered but may not decide or recommend.

---

## 4. Org Chart (Authority Model)

This chart represents **authority and accountability**, not management.
Executive Leadership
│
├── Product Owner
│   ├── Strategy Rules & System Intent Owner
│   ├── Head of UX & Design
│   └── Head of Specs Team
│       ├── Data Model & Domain Schema Owner
│       ├── Metrics Definitions & Analytics Owner
│       ├── API Contracts & Documentation Owner
│       └── Frontend Specifications & UX Documentation Owner
│
├── Head of Engineering
│   ├── Backend Engineering Patterns Owner
│   ├── Infrastructure & Operations Owner
│   ├── Base44 Frontend Prompt Owner
│   └── QA & Testing Owner
│       └── QA Lead
│
├── Director of Quality
│
├── PMO Lead
│
├── Cybersecurity & Trust Lead
│
├── AI Compliance & Governance Officer
│
├── FinOps & Resource Architect
│
├── Financial Reporting & Records Owner
│
└── Director of HR

* * * * *

## 5. Conflict Resolution Model

- **Within a domain:** resolved by the domain owner
- **Across domains:** escalated to the Head of Specs Team
- **Product trade‑offs:** resolved by the Product Owner
- **Quality disputes:** Director of Quality prevails
- **Financial record disputes:** Financial Reporting & Records Owner prevails
- **No conflict is resolved through implementation or workaround**

---

## 6. Definition of Success

The organisation is functioning correctly when:

- Every decision has a named owner
- Behaviour matches documented intent
- Validation is evidence‑based
- Financial outputs are externally defensible
- Roles are clear, bounded, and non‑overlapping
- Individuals know what they own — and what they do not

---

## 7. Authority Statement

This charter exists to prevent:

- Silent authority drift
- Tool‑driven decision making
- Delivery pressure redefining truth
- Analytics being mistaken for records

If ambiguity arises about **who decides**, this document is the reference.
